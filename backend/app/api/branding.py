from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.branding import Branding
from app.models.startup import Startup
from app.schemas.branding import BrandingCreate, BrandingResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import ai_service

router = APIRouter(prefix="/branding", tags=["Branding"])

@router.get("/startup/{startup_id}", response_model=BrandingResponse)
def get_branding_by_startup(startup_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    branding = db.query(Branding).filter(Branding.startup_id == startup_id).order_by(Branding.id.desc()).first()
    if not branding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branding not found for this startup")
    return branding

@router.post("/", response_model=BrandingResponse)
def create_or_update_branding(brand_in: BrandingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == brand_in.startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    branding = db.query(Branding).filter(Branding.startup_id == brand_in.startup_id).order_by(Branding.id.desc()).first()
    
    if brand_in.generate_ai:
        ai_data = ai_service.generate_branding(
            name=startup.name,
            industry=startup.industry or "",
            description=startup.description or ""
        )
        names = ai_data.get("name_suggestions", "")
        slogans = ai_data.get("slogans", "")
        colors = ai_data.get("brand_colors", "")
        logo = ai_data.get("logo_description", "")
    else:
        names = brand_in.name_suggestions
        slogans = brand_in.slogans
        colors = brand_in.brand_colors
        logo = brand_in.logo_description

    if not branding:
        branding = Branding(startup_id=brand_in.startup_id)
        db.add(branding)
        
    branding.name_suggestions = names
    branding.slogans = slogans
    branding.brand_colors = colors
    branding.logo_description = logo
    
    db.commit()
    db.refresh(branding)
    return branding
