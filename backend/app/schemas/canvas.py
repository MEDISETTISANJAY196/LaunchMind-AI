from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CanvasBase(BaseModel):
    customer_segments: Optional[str] = None
    value_propositions: Optional[str] = None
    channels: Optional[str] = None
    customer_relationships: Optional[str] = None
    revenue_streams: Optional[str] = None
    key_resources: Optional[str] = None
    key_activities: Optional[str] = None
    key_partners: Optional[str] = None
    cost_structure: Optional[str] = None

class CanvasCreate(CanvasBase):
    startup_id: int
    generate_ai: Optional[bool] = True

class CanvasResponse(CanvasBase):
    id: int
    startup_id: int
    created_at: datetime

    class Config:
        from_attributes = True
