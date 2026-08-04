import os
import sys

# Ensure backend directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rag_service import rag_service

def main():
    print("Starting document ingestion into FAISS vector database...")
    result = rag_service.ingest_documents()
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    print(f"Chunks Indexed: {result.get('count', 0)}")

if __name__ == "__main__":
    main()
