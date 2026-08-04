from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StartupBase(BaseModel):
    name: str
    industry: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[str] = "Ideation"
    target_audience: Optional[str] = None

class StartupCreate(StartupBase):
    pass

class StartupResponse(StartupBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
