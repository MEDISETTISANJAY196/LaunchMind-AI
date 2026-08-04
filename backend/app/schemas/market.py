from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MarketResearchBase(BaseModel):
    tam: Optional[str] = None
    sam: Optional[str] = None
    som: Optional[str] = None
    target_demographics: Optional[str] = None
    customer_personas: Optional[str] = None
    ai_feedback: Optional[str] = None

class MarketResearchCreate(MarketResearchBase):
    startup_id: int
    generate_ai: Optional[bool] = True

class MarketResearchResponse(MarketResearchBase):
    id: int
    startup_id: int
    created_at: datetime

    class Config:
        from_attributes = True
