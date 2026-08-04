from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BrandingBase(BaseModel):
    name_suggestions: Optional[str] = None
    slogans: Optional[str] = None
    brand_colors: Optional[str] = None
    logo_description: Optional[str] = None

class BrandingCreate(BrandingBase):
    startup_id: int
    generate_ai: Optional[bool] = True

class BrandingResponse(BrandingBase):
    id: int
    startup_id: int
    created_at: datetime

    class Config:
        from_attributes = True
