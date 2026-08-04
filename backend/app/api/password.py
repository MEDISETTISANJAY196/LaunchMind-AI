from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/password", tags=["Password"])


class PasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.put("/")
def change_password(
    payload: PasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if not pwd_context.verify(
        payload.current_password,
        current_user.hashed_password,
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect",
        )

    current_user.hashed_password = pwd_context.hash(
        payload.new_password
    )

    db.commit()

    return {
        "message": "Password updated successfully"
    }