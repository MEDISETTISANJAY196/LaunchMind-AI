from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.competitor import CompetitorAnalysis
from app.models.startup import Startup
from app.schemas.competitor import CompetitorCreate, CompetitorResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import ai_service
import json

router = APIRouter(prefix="/competitor", tags=["Competitor Analysis"])

@router.get("/startup/{startup_id}", response_model=CompetitorResponse)
def get_competitor_by_startup(startup_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    comp = db.query(CompetitorAnalysis).filter(CompetitorAnalysis.startup_id == startup_id).order_by(CompetitorAnalysis.id.desc()).first()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competitor analysis not found for this startup")
    return comp

@router.post("/", response_model=CompetitorResponse)
def create_or_update_competitor(comp_in: CompetitorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == comp_in.startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    comp = db.query(CompetitorAnalysis).filter(CompetitorAnalysis.startup_id == comp_in.startup_id).order_by(CompetitorAnalysis.id.desc()).first()
    
    if comp_in.generate_ai:
        ai_data = ai_service.generate_competitor_analysis(
            name=startup.name,
            industry=startup.industry or "",
            description=startup.description or ""
        )
        competitors_json = json.dumps(ai_data.get("competitors", []))
        market_gaps = ai_data.get("market_gaps", "")
    else:
        competitors_json = comp_in.competitors_json
        market_gaps = comp_in.market_gaps

    if not comp:
        comp = CompetitorAnalysis(startup_id=comp_in.startup_id)
        db.add(comp)
        
    comp.competitors_json = competitors_json
    comp.market_gaps = market_gaps
    
    db.commit()
    db.refresh(comp)
    return comp
