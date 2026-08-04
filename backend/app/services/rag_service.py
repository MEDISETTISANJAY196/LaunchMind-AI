import os
import logging
from typing import List, Dict, Any

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings

logger = logging.getLogger("app.rag_service")


class RAGService:
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.db_path = os.path.join(settings.VECTOR_DB_DIR, "faiss_index")

        # Initialize embeddings only if a server Gemini API key exists
        if settings.GEMINI_API_KEY:
            try:
                self.embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/embedding-001",
                    google_api_key=settings.GEMINI_API_KEY,
                )

                self.load_index()
                logger.info("RAG embeddings initialized successfully.")

            except Exception as e:
                logger.error(f"Failed to initialize Gemini embeddings: {e}")

        else:
            logger.info(
                "No server Gemini API key configured. "
                "RAG will use the logged-in user's API key when available."
            )

    def load_index(self):
        """Load FAISS index if it already exists."""

        if self.embeddings and os.path.exists(self.db_path):
            try:
                self.vector_store = FAISS.load_local(
                    self.db_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )

                logger.info("Successfully loaded FAISS vector database.")

            except Exception as e:
                logger.error(f"Failed to load FAISS index: {e}")

    def ingest_documents(self) -> Dict[str, Any]:
        """Read documents from knowledge base and build FAISS index."""

        if not self.embeddings:
            return {
                "status": "error",
                "message": "Cannot ingest documents because no Gemini embedding model is available.",
            }

        documents = []
        kb_dir = settings.KNOWLEDGE_BASE_DIR

        os.makedirs(kb_dir, exist_ok=True)

        supported_extensions = (".txt", ".md")

        for root, _, files in os.walk(kb_dir):
            for file in files:
                if file.endswith(supported_extensions):
                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read().strip()

                        if content:
                            documents.append(
                                {
                                    "page_content": content,
                                    "metadata": {
                                        "source": file,
                                        "category": os.path.basename(root),
                                        "path": file_path,
                                    },
                                }
                            )

                    except Exception as e:
                        logger.error(f"Failed to read {file_path}: {e}")

        if not documents:
            return {
                "status": "success",
                "message": "No documents found in knowledge base.",
                "count": 0,
            }

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
        )

        chunks = []

        for doc in documents:
            for chunk in splitter.split_text(doc["page_content"]):
                chunks.append(
                    type(
                        "Document",
                        (object,),
                        {
                            "page_content": chunk,
                            "metadata": doc["metadata"],
                        },
                    )()
                )

        try:
            self.vector_store = FAISS.from_documents(
                chunks,
                self.embeddings,
            )

            self.vector_store.save_local(self.db_path)

            logger.info(
                f"Indexed {len(documents)} documents into {len(chunks)} chunks."
            )

            return {
                "status": "success",
                "message": "Knowledge base indexed successfully.",
                "count": len(chunks),
            }

        except Exception as e:
            logger.error(f"Failed to build FAISS index: {e}")

            return {
                "status": "error",
                "message": str(e),
            }

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search vector database or fall back to keyword search."""

        if self.vector_store:
            try:
                results = self.vector_store.similarity_search(query, k=k)

                return [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                    }
                    for doc in results
                ]

            except Exception as e:
                logger.error(f"Vector search failed: {e}")

        results = []

        kb_dir = settings.KNOWLEDGE_BASE_DIR

        if os.path.exists(kb_dir):
            for root, _, files in os.walk(kb_dir):
                for file in files:
                    if file.endswith((".txt", ".md")):

                        file_path = os.path.join(root, file)

                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                text = f.read()

                            if query.lower() in text.lower():

                                idx = text.lower().find(query.lower())

                                start = max(0, idx - 300)
                                end = min(len(text), idx + 700)

                                results.append(
                                    {
                                        "content": text[start:end],
                                        "metadata": {
                                            "source": file,
                                            "category": os.path.basename(root),
                                            "path": file_path,
                                            "fallback": True,
                                        },
                                    }
                                )

                                if len(results) >= k:
                                    return results

                        except Exception as e:
                            logger.error(f"Keyword search failed: {e}")

        return results


rag_service = RAGService()