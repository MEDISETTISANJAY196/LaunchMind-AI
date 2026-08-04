from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.startup import Startup
from app.schemas.startup import StartupCreate, StartupResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.utils.notifications import create_notification

router = APIRouter(prefix="/startups", tags=["Startups"])

@router.get("/", response_model=List[StartupResponse])
def get_startups(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Startup).filter(Startup.user_id == current_user.id).all()

@router.post("/", response_model=StartupResponse, status_code=status.HTTP_201_CREATED)
def create_startup(startup_in: StartupCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_startup = Startup(
        name=startup_in.name,
        industry=startup_in.industry,
        description=startup_in.description,
        stage=startup_in.stage,
        target_audience=startup_in.target_audience,
        user_id=current_user.id
    )
    db.add(db_startup)
    db.commit()
    db.refresh(db_startup)
    create_notification(
        db=db,
        user_id=current_user.id,
        message=f"🚀 Startup '{db_startup.name}' created successfully."
    )
    return db_startup

@router.get("/{startup_id}", response_model=StartupResponse)
def get_startup(startup_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
    return startup

@router.put("/{startup_id}", response_model=StartupResponse)
def update_startup(startup_id: int, startup_in: StartupCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
    
    startup.name = startup_in.name
    startup.industry = startup_in.industry
    startup.description = startup_in.description
    startup.stage = startup_in.stage
    startup.target_audience = startup_in.target_audience
    
    db.commit()
    db.refresh(startup)
    create_notification(
        db=db,
        user_id=current_user.id,
        message=f"✏️ Startup '{startup.name}' updated."
    )
    return startup

@router.delete("/{startup_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_startup(startup_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
    create_notification(
        db=db,
        user_id=current_user.id,
        message=f"🗑️ Startup '{startup.name}' deleted."
    )
    db.delete(startup)
    db.commit()
    return
