from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.database import engine, Base

# Import models
from app.models import *

# API Routers
from app.api.auth import router as auth_router
from app.api.startups import router as startups_router
from app.api.swot import router as swot_router
from app.api.canvas import router as canvas_router
from app.api.branding import router as branding_router
from app.api.competitor import router as competitor_router
from app.api.market import router as market_router
from app.api.mentor import router as mentor_router
from app.api.reports import router as reports_router
from app.api.settings import router as settings_router
from app.api import analyze
from app.api.analytics import router as analytics_router
from app.api.profile import router as profile_router
from app.api.password import router as password_router
from app.api.notifications import router as notifications_router
from app.api.insights import router as insights_router
from app.api.profile_photo import router as profile_photo_router
# Create database tables
Base.metadata.create_all(bind=engine)

# Create required folders
for path in (
    settings.UPLOADS_DIR,
    settings.VECTOR_DB_DIR,
    settings.KNOWLEDGE_BASE_DIR,
):
    os.makedirs(path, exist_ok=True)

# FastAPI app
app = FastAPI(
    title="LaunchMind-AI API",
    description="Backend AI Services for Startup Analysis, SWOT, Business Model Canvas, and Mentorship.",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_router, prefix="/api")
app.include_router(startups_router, prefix="/api")
app.include_router(swot_router, prefix="/api")
app.include_router(canvas_router, prefix="/api")
app.include_router(branding_router, prefix="/api")
app.include_router(competitor_router, prefix="/api")
app.include_router(market_router, prefix="/api")
app.include_router(mentor_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(settings_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(password_router, prefix="/api")
app.include_router(notifications_router, prefix="/api")
app.include_router(insights_router, prefix="/api")
app.include_router(profile_photo_router, prefix="/api")
app.mount("/uploads", StaticFiles(directory="/tmp/uploads"), name="uploads")

@app.get("/")
def read_root():
    return {
        "name": "LaunchMind-AI API",
        "status": "healthy",
        "version": "1.0.0",
    }