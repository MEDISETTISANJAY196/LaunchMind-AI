from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompetitorBase(BaseModel):
    competitors_json: Optional[str] = None # JSON string representing lists of competitors
    market_gaps: Optional[str] = None

class CompetitorCreate(CompetitorBase):
    startup_id: int
    generate_ai: Optional[bool] = True

class CompetitorResponse(CompetitorBase):
    id: int
    startup_id: int
    created_at: datetime

    class Config:
        from_attributes = True
