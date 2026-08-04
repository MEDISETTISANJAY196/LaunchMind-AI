from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SWOTBase(BaseModel):
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    opportunities: Optional[str] = None
    threats: Optional[str] = None
    ai_feedback: Optional[str] = None

class SWOTCreate(SWOTBase):
    startup_id: int
    generate_ai: Optional[bool] = True

class SWOTResponse(SWOTBase):
    id: int
    startup_id: int
    created_at: datetime

    class Config:
        from_attributes = True
