from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.canvas import BusinessCanvas
from app.models.startup import Startup
from app.schemas.canvas import CanvasCreate, CanvasResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import ai_service

router = APIRouter(prefix="/canvas", tags=["Business Model Canvas"])

@router.get("/startup/{startup_id}", response_model=CanvasResponse)
def get_canvas_by_startup(startup_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    canvas = db.query(BusinessCanvas).filter(BusinessCanvas.startup_id == startup_id).order_by(BusinessCanvas.id.desc()).first()
    if not canvas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canvas not found for this startup")
    return canvas

@router.post("/", response_model=CanvasResponse)
def create_or_update_canvas(canvas_in: CanvasCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == canvas_in.startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    canvas = db.query(BusinessCanvas).filter(BusinessCanvas.startup_id == canvas_in.startup_id).order_by(BusinessCanvas.id.desc()).first()
    
    if canvas_in.generate_ai:
        ai_data = ai_service.generate_canvas(
            name=startup.name,
            industry=startup.industry or "",
            description=startup.description or ""
        )
        cust_seg = ai_data.get("customer_segments", "")
        val_prop = ai_data.get("value_propositions", "")
        chan = ai_data.get("channels", "")
        cust_rel = ai_data.get("customer_relationships", "")
        rev = ai_data.get("revenue_streams", "")
        key_res = ai_data.get("key_resources", "")
        key_act = ai_data.get("key_activities", "")
        key_part = ai_data.get("key_partners", "")
        cost = ai_data.get("cost_structure", "")
    else:
        cust_seg = canvas_in.customer_segments
        val_prop = canvas_in.value_propositions
        chan = canvas_in.channels
        cust_rel = canvas_in.customer_relationships
        rev = canvas_in.revenue_streams
        key_res = canvas_in.key_resources
        key_act = canvas_in.key_activities
        key_part = canvas_in.key_partners
        cost = canvas_in.cost_structure

    if not canvas:
        canvas = BusinessCanvas(startup_id=canvas_in.startup_id)
        db.add(canvas)
        
    canvas.customer_segments = cust_seg
    canvas.value_propositions = val_prop
    canvas.channels = chan
    canvas.customer_relationships = cust_rel
    canvas.revenue_streams = rev
    canvas.key_resources = key_res
    canvas.key_activities = key_act
    canvas.key_partners = key_part
    canvas.cost_structure = cost
    
    db.commit()
    db.refresh(canvas)
    return canvas
