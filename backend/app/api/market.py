from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.market import MarketResearch
from app.models.startup import Startup
from app.schemas.market import MarketResearchCreate, MarketResearchResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import ai_service

router = APIRouter(prefix="/market", tags=["Market Research"])

@router.get("/startup/{startup_id}", response_model=MarketResearchResponse)
def get_market_by_startup(startup_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    market = db.query(MarketResearch).filter(MarketResearch.startup_id == startup_id).order_by(MarketResearch.id.desc()).first()
    if not market:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Market research not found for this startup")
    return market

@router.post("/", response_model=MarketResearchResponse)
def create_or_update_market(market_in: MarketResearchCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == market_in.startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    market = db.query(MarketResearch).filter(MarketResearch.startup_id == market_in.startup_id).order_by(MarketResearch.id.desc()).first()
    
    if market_in.generate_ai:
        ai_data = ai_service.generate_market_research(
            name=startup.name,
            industry=startup.industry or "",
            description=startup.description or ""
        )
        tam = ai_data.get("tam", "")
        sam = ai_data.get("sam", "")
        som = ai_data.get("som", "")
        target_demographics = ai_data.get("target_demographics", "")
        customer_personas = ai_data.get("customer_personas", "")
        ai_feedback = ai_data.get("ai_feedback", "")
    else:
        tam = market_in.tam
        sam = market_in.sam
        som = market_in.som
        target_demographics = market_in.target_demographics
        customer_personas = market_in.customer_personas
        ai_feedback = market_in.ai_feedback

    if not market:
        market = MarketResearch(startup_id=market_in.startup_id)
        db.add(market)
        
    market.tam = tam
    market.sam = sam
    market.som = som
    market.target_demographics = target_demographics
    market.customer_personas = customer_personas
    market.ai_feedback = ai_feedback
    
    db.commit()
    db.refresh(market)
    return market
