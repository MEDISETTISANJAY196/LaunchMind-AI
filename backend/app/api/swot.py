from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.swot import SWOTAnalysis
from app.models.startup import Startup
from app.schemas.swot import SWOTCreate, SWOTResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import ai_service

router = APIRouter(prefix="/swot", tags=["SWOT Analysis"])

@router.get("/startup/{startup_id}", response_model=SWOTResponse)
def get_swot_by_startup(startup_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verify startup ownership
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    swot = db.query(SWOTAnalysis).filter(SWOTAnalysis.startup_id == startup_id).order_by(SWOTAnalysis.id.desc()).first()
    if not swot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SWOT analysis not found for this startup")
    return swot

@router.post("/", response_model=SWOTResponse)
def create_or_update_swot(swot_in: SWOTCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == swot_in.startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    # Check if latest SWOT exists, to update it or create a new version
    swot = db.query(SWOTAnalysis).filter(SWOTAnalysis.startup_id == swot_in.startup_id).order_by(SWOTAnalysis.id.desc()).first()
    
    if swot_in.generate_ai:
        # Generate SWOT using AI based on startup name, industry, and description
        ai_data = ai_service.generate_swot(
            name=startup.name,
            industry=startup.industry or "",
            description=startup.description or ""
        )
        strengths = ", ".join(ai_data.get("strengths", []))
        weaknesses = ", ".join(ai_data.get("weaknesses", []))
        opportunities = ", ".join(ai_data.get("opportunities", []))
        threats = ", ".join(ai_data.get("threats", []))
        ai_feedback = ai_data.get("ai_feedback", "")
    else:
        strengths = swot_in.strengths
        weaknesses = swot_in.weaknesses
        opportunities = swot_in.opportunities
        threats = swot_in.threats
        ai_feedback = swot_in.ai_feedback

    if not swot:
        swot = SWOTAnalysis(startup_id=swot_in.startup_id)
        db.add(swot)
        
    swot.strengths = strengths
    swot.weaknesses = weaknesses
    swot.opportunities = opportunities
    swot.threats = threats
    swot.ai_feedback = ai_feedback
    
    db.commit()
    db.refresh(swot)
    return swot
