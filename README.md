# LaunchMind-AI

An AI-powered SaaS platform designed to assist entrepreneurs, startup founders, and mentors in analyzing, refining, and launching business ideas.

## Project Structure
* `frontend/` - React + Vite + TailwindCSS
* `backend/` - FastAPI + LangChain + Gemini
* `database/` - PostgreSQL schema and scripts
* `knowledge_base/` - Source materials for RAG
* `uploads/` - User uploaded documents
* `vector_db/` - FAISS / ChromaDB vector stores

## Setup & Launching

### Backend
1. Navigate to `/backend`
2. Create `.env` file from `.env.example`
3. Run `pip install -r requirements.txt`
4. Run `uvicorn app.main:app --reload`

### Frontend
1. Navigate to `/frontend`
2. Run `npm install`
3. Run `npm run dev`
