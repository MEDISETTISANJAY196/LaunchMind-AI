from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.core.encryption import encrypt

router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)


class GeminiKeyRequest(BaseModel):
    gemini_api_key: str


@router.post("/gemini-key")
def save_gemini_key(
    data: GeminiKeyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    encrypted = encrypt(data.gemini_api_key)

    print("Encrypted Key:", encrypted)

    current_user.gemini_api_key = encrypted

    db.commit()
    db.refresh(current_user)

    print("Saved in DB:", current_user.gemini_api_key)

    return {
        "success": True,
        "message": "Gemini API Key saved successfully"
    }


@router.get("/gemini-key/status")
def gemini_key_status(
    current_user: User = Depends(get_current_user)
):
    print("Stored Key:", current_user.gemini_api_key)

    return {
        "configured": current_user.gemini_api_key is not None
    }

@router.delete("/gemini-key")
def delete_gemini_key(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.gemini_api_key = None

    db.commit()

    return {
        "success": True,
        "message": "Gemini API Key removed successfully"
    }