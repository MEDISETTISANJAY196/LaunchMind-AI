from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime
from app.core.database import get_db
from app.models.report import Report
from app.models.startup import Startup
from app.models.swot import SWOTAnalysis
from app.models.canvas import BusinessCanvas
from app.models.market import MarketResearch
from app.models.branding import Branding
from app.api.deps import get_current_user
from app.models.user import User
from app.services.pdf_service import pdf_service

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/startup/{startup_id}", response_model=List[dict])
def get_reports_by_startup(startup_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    reports = db.query(Report).filter(Report.startup_id == startup_id).order_by(Report.id.desc()).all()
    return [
        {
            "id": r.id,
            "startup_id": r.startup_id,
            "title": r.title,
            "created_at": r.created_at
        }
        for r in reports
    ]

@router.post("/generate/{startup_id}")
def generate_report(startup_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Fetch startup
    startup = db.query(Startup).filter(Startup.id == startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found")
        
    # 2. Gather latest modules, defaults if missing
    swot = db.query(SWOTAnalysis).filter(SWOTAnalysis.startup_id == startup_id).order_by(SWOTAnalysis.id.desc()).first()
    swot_dict = {
        "strengths": swot.strengths if swot else "N/A",
        "weaknesses": swot.weaknesses if swot else "N/A",
        "opportunities": swot.opportunities if swot else "N/A",
        "threats": swot.threats if swot else "N/A",
        "ai_feedback": swot.ai_feedback if swot else ""
    }

    canvas = db.query(BusinessCanvas).filter(BusinessCanvas.startup_id == startup_id).order_by(BusinessCanvas.id.desc()).first()
    canvas_dict = {
        "customer_segments": canvas.customer_segments if canvas else "N/A",
        "value_propositions": canvas.value_propositions if canvas else "N/A",
        "channels": canvas.channels if canvas else "N/A",
        "customer_relationships": canvas.customer_relationships if canvas else "N/A",
        "revenue_streams": canvas.revenue_streams if canvas else "N/A",
        "key_resources": canvas.key_resources if canvas else "N/A",
        "key_activities": canvas.key_activities if canvas else "N/A",
        "key_partners": canvas.key_partners if canvas else "N/A",
        "cost_structure": canvas.cost_structure if canvas else "N/A",
    }

    market = db.query(MarketResearch).filter(MarketResearch.startup_id == startup_id).order_by(MarketResearch.id.desc()).first()
    market_dict = {
        "tam": market.tam if market else "N/A",
        "sam": market.sam if market else "N/A",
        "som": market.som if market else "N/A",
        "target_demographics": market.target_demographics if market else "",
        "customer_personas": market.customer_personas if market else "",
    }

    branding = db.query(Branding).filter(Branding.startup_id == startup_id).order_by(Branding.id.desc()).first()
    branding_dict = {
        "name_suggestions": branding.name_suggestions if branding else "N/A",
        "slogans": branding.slogans if branding else "N/A",
        "brand_colors": branding.brand_colors if branding else "N/A",
        "logo_description": branding.logo_description if branding else "N/A",
    }

    # 3. Create file info
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{startup_id}_{timestamp}.pdf"
    title = f"Report for {startup.name} - {datetime.now().strftime('%B %d, %Y')}"
    
    # 4. Generate
    try:
        filepath = pdf_service.generate_startup_report(
            startup_name=startup.name,
            industry=startup.industry or "N/A",
            stage=startup.stage or "N/A",
            description=startup.description or "",
            swot_data=swot_dict,
            canvas_data=canvas_dict,
            market_data=market_dict,
            branding_data=branding_dict,
            output_filename=filename
        )
        
        # 5. Save report row
        report = Report(
            startup_id=startup_id,
            title=title,
            filepath=filepath
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return {
            "status": "success",
            "message": "Report generated successfully",
            "report_id": report.id,
            "title": report.title
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF: {str(e)}"
        )

@router.get("/download/{report_id}")
def download_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
        
    # Verify startup belongs to user
    startup = db.query(Startup).filter(Startup.id == report.startup_id, Startup.user_id == current_user.id).first()
    if not startup:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        
    if not os.path.exists(report.filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF file not found on disk")
        
    return FileResponse(
        path=report.filepath,
        filename=os.path.basename(report.filepath),
        media_type="application/pdf"
    )
