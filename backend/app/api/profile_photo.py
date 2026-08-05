from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/profile-photo", tags=["Profile Photo"])

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
def upload_photo(
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get file extension (.jpg, .png, .jpeg, ...)
    extension = os.path.splitext(photo.filename)[1]

    # Save image as user_1.jpg, user_2.png, ...
    filename = f"user_{current_user.id}{extension}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    current_user.profile_image = filename
    db.commit()

    return {
        "message": "Photo uploaded successfully",
        "image": filename,
    }