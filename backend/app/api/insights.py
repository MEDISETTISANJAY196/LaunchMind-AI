from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/insights", tags=["AI Insights"])

@router.get("/")
def get_ai_insights(current_user: User = Depends(get_current_user)):
    return {
        "startup_readiness": 84,
        "recommendations": [
            "Improve Market Validation",
            "Generate Investor Pitch",
            "Expand Marketing Strategy",
            "Complete Financial Forecast"
        ]
    }