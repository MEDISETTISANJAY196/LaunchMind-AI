import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.mentorship import MentorshipSession
from app.models.startup import Startup
from app.schemas.mentorship import MentorshipChatRequest, MentorshipSessionResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import ai_service
from app.services.rag_service import rag_service

router = APIRouter(prefix="/mentor", tags=["Mentorship"])

@router.get("/session/{startup_id}/{mentor_name}", response_model=MentorshipSessionResponse)
def get_session(startup_id: int, mentor_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    session = db.query(MentorshipSession).filter(
        MentorshipSession.startup_id == startup_id,
        MentorshipSession.mentor_name == mentor_name
    ).first()
    
    if not session:
        # Create a new session if none exists
        session = MentorshipSession(
            startup_id=startup_id,
            mentor_name=mentor_name,
            messages_json="[]"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
    return session

@router.post("/chat")
def chat_with_mentor(chat_in: MentorshipChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == chat_in.startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    session = db.query(MentorshipSession).filter(
        MentorshipSession.startup_id == chat_in.startup_id,
        MentorshipSession.mentor_name == chat_in.mentor_name
    ).first()
    
    if not session:
        session = MentorshipSession(
            startup_id=chat_in.startup_id,
            mentor_name=chat_in.mentor_name,
            messages_json="[]"
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    try:
        messages = json.loads(session.messages_json)
    except Exception:
        messages = []

    # 1. Append user message
    user_msg = {"role": "user", "content": chat_in.message}
    messages.append(user_msg)

    # 2. Run RAG context retrieval
    context_docs = rag_service.search(query=chat_in.message, k=3)

    # 3. Generate Mentor response
    reply = ai_service.generate_mentor_reply(
        startup_name=startup.name,
        startup_desc=startup.description or "",
        mentor_name=chat_in.mentor_name,
        chat_history=messages[:-1], # pass history before current message
        query=chat_in.message,
        context_docs=context_docs
    )

    # 4. Append AI reply
    assistant_msg = {"role": "assistant", "content": reply}
    messages.append(assistant_msg)

    # Save to session
    session.messages_json = json.dumps(messages)
    db.commit()

    return {
        "reply": reply,
        "history": messages
    }
