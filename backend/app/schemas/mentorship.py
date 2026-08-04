from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MentorshipMessage(BaseModel):
    role: str # user or assistant
    content: str

class MentorshipChatRequest(BaseModel):
    startup_id: int
    mentor_name: str
    message: str

class MentorshipSessionResponse(BaseModel):
    id: int
    startup_id: int
    mentor_name: str
    messages_json: str # Raw JSON list of messages
    created_at: datetime

    class Config:
        from_attributes = True
