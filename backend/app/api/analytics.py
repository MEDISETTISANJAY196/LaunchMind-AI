from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.startup import Startup

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
def dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startups = (
        db.query(Startup)
        .filter(Startup.user_id == current_user.id)
        .all()
    )

    total_startups = len(startups)

    total_swots = 0
    total_market = 0
    total_competitors = 0
    total_canvas = 0
    total_branding = 0
    total_mentor = 0
    total_reports = 0

    for startup in startups:
        total_swots += len(startup.swots)
        total_market += len(startup.market_researches)
        total_competitors += len(startup.competitor_analyses)
        total_canvas += len(startup.business_canvases)
        total_branding += len(startup.brandings)
        total_mentor += len(startup.mentorships)
        total_reports += len(startup.reports)

    total_analysis = (
        total_swots
        + total_market
        + total_competitors
        + total_canvas
        + total_branding
    )

    avg_score = 0
    if total_startups > 0:
        avg_score = min(100, 70 + (total_analysis * 3))

    return {
        "total_startups": total_startups,
        "analyses": total_analysis,
        "mentor_chats": total_mentor,
        "reports": total_reports,
        "avg_score": avg_score,
    }