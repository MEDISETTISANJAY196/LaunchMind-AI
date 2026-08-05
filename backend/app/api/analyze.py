from fastapi.responses import FileResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import tempfile
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.startup import Startup
from app.services.ai_service import ai_service
from app.core.encryption import decrypt

router = APIRouter(prefix="/analyze", tags=["AI Analysis"])


@router.post("/{startup_id}")
def analyze_startup(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = (
        db.query(Startup)
        .filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id,
        )
        .first()
    )

    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    # Check if user configured Gemini API Key
    from app.core.config import settings

    user_api_key = settings.GEMINI_API_KEY

    if current_user.gemini_api_key:
        user_api_key = decrypt(current_user.gemini_api_key)

    prompt = f"""
Analyze this startup idea.

Startup Name: {startup.name}
Industry: {startup.industry}
Stage: {startup.stage}
Target Audience: {startup.target_audience}
Description: {startup.description}

Return your response in this format:

Startup Score: xx/100

Strengths:
- ...

Weaknesses:
- ...

Opportunities:
- ...

Risks:
- ...

Suggestions:
- ...
"""

    analysis = ai_service._call_llm(prompt, user_api_key)

    return {
        "startup_id": startup.id,
        "startup_name": startup.name,
        "analysis": analysis,
    }

@router.post("/competitor/{startup_id}")
def competitor_analysis(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = (
        db.query(Startup)
        .filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id,
        )
        .first()
    )

    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    from app.core.config import settings

    user_api_key = settings.GEMINI_API_KEY

    if current_user.gemini_api_key:
        user_api_key = decrypt(current_user.gemini_api_key)

    prompt = f"""
You are an experienced startup consultant.

Analyze the following startup and identify its competitors.

Startup Name: {startup.name}
Industry: {startup.industry}
Stage: {startup.stage}
Target Audience: {startup.target_audience}
Description: {startup.description}

Return the response in this format:

Top Competitors:
1. Company Name
   - Description
   - Strengths
   - Weaknesses

2. Company Name
   - Description
   - Strengths
   - Weaknesses

Market Gap:
- ...

Competitive Advantage Suggestions:
- ...
"""

    result = ai_service._call_llm(prompt, user_api_key)

    return {
        "startup_id": startup.id,
        "startup_name": startup.name,
        "competitor_analysis": result,
    }
    
@router.post("/business-model/{startup_id}")
def business_model_canvas(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = (
        db.query(Startup)
        .filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id,
        )
        .first()
    )

    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    from app.core.config import settings

    user_api_key = settings.GEMINI_API_KEY

    if current_user.gemini_api_key:
        user_api_key = decrypt(current_user.gemini_api_key)

    prompt = f"""
You are a startup mentor.

Create a complete Business Model Canvas for this startup.

Startup Name: {startup.name}
Industry: {startup.industry}
Stage: {startup.stage}
Target Audience: {startup.target_audience}
Description: {startup.description}

Return ONLY this format:

Value Proposition:
-

Customer Segments:
-

Channels:
-

Customer Relationships:
-

Revenue Streams:
-

Key Activities:
-

Key Resources:
-

Key Partners:
-

Cost Structure:
-
"""

    result = ai_service._call_llm(prompt, user_api_key)

    return {
        "startup_id": startup.id,
        "startup_name": startup.name,
        "business_model_canvas": result,
    }
@router.post("/pitch-deck/{startup_id}")
def generate_pitch_deck(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = (
        db.query(Startup)
        .filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id,
        )
        .first()
    )

    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    from app.core.config import settings

    user_api_key = settings.GEMINI_API_KEY

    if current_user.gemini_api_key:
        user_api_key = decrypt(current_user.gemini_api_key)

    prompt = f"""
You are an expert startup investor and pitch deck consultant.

Create a professional Startup Pitch Deck.

Startup Name: {startup.name}
Industry: {startup.industry}
Stage: {startup.stage}
Target Audience: {startup.target_audience}
Description: {startup.description}

Return ONLY this format:    

1. Company Overview

2. Problem

3. Solution

4. Market Opportunity

5. Business Model

6. Competitive Advantage

7. Go-To-Market Strategy

8. Revenue Model

9. Financial Projection

10. Funding Ask

11. Vision
"""

    result = ai_service._call_llm(prompt, user_api_key)

    return {
        "startup_id": startup.id,
        "startup_name": startup.name,
        "pitch_deck": result,
    }

@router.post("/financial-projection/{startup_id}")
def financial_projection(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = (
        db.query(Startup)
        .filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id,
        )
        .first()
    )

    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    from app.core.config import settings

    user_api_key = settings.GEMINI_API_KEY

    if current_user.gemini_api_key:
        user_api_key = decrypt(current_user.gemini_api_key)

    prompt = f"""
You are a startup financial consultant.

Create a professional Financial Projection for this startup.

Startup Name: {startup.name}
Industry: {startup.industry}
Stage: {startup.stage}
Target Audience: {startup.target_audience}
Description: {startup.description}

Return ONLY this format:

💰 Financial Projection

Initial Investment:
-

Monthly Operating Cost:
-

Estimated Monthly Revenue:
-

Break-even Point:
-

Revenue Forecast:
Year 1:
Year 2:
Year 3:

Profit Margin:
-

Funding Requirement:
-

ROI Estimate:
-

Financial Risks:
-

Recommendations:
-
"""

    result = ai_service._call_llm(prompt, user_api_key)

    return {
        "startup_id": startup.id,
        "startup_name": startup.name,
        "financial_projection": result,
    }

@router.post("/investor-readiness/{startup_id}")
def investor_readiness(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = (
        db.query(Startup)
        .filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id,
        )
        .first()
    )

    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    from app.core.config import settings

    user_api_key = settings.GEMINI_API_KEY

    if current_user.gemini_api_key:
        user_api_key = decrypt(current_user.gemini_api_key)

    prompt = f"""
You are a professional Venture Capital investor.

Evaluate this startup and generate an Investor Readiness Report.

Startup Name: {startup.name}
Industry: {startup.industry}
Stage: {startup.stage}
Target Audience: {startup.target_audience}
Description: {startup.description}

Return ONLY this format:

🎯 Overall Investor Readiness Score:
__/100

Market Validation:
__/20

Business Model:
__/20

Competitive Advantage:
__/20

Financial Readiness:
__/20

Innovation:
__/20

Funding Readiness:
Low / Medium / High

Investor Verdict:
-

Top Strengths:
-

Major Risks:
-

Recommendations:
-
"""

    result = ai_service._call_llm(prompt, user_api_key)

    return {
        "startup_id": startup.id,
        "startup_name": startup.name,
        "investor_readiness": result,
    }
@router.post("/go-to-market/{startup_id}")
def go_to_market_strategy(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = (
        db.query(Startup)
        .filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id,
        )
        .first()
    )

    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    from app.core.config import settings

    user_api_key = settings.GEMINI_API_KEY

    if current_user.gemini_api_key:
        user_api_key = decrypt(current_user.gemini_api_key)

    prompt = f"""
You are a startup growth consultant.

Create a complete Go-To-Market Strategy for this startup.

Startup Name: {startup.name}
Industry: {startup.industry}
Stage: {startup.stage}
Target Audience: {startup.target_audience}
Description: {startup.description}

Return ONLY this format:

📈 Go-To-Market Strategy

Target Customers:
-

Unique Value Proposition:
-

Marketing Channels:
-

Customer Acquisition Strategy:
-

Pricing Strategy:
-

Sales Strategy:
-

Launch Plan:
Week 1:
Week 2:
Month 1:

Growth Strategy:
Month 3:
Month 6:
Month 12:

KPIs to Track:
-

Risks:
-

Recommendations:
-
"""

    result = ai_service._call_llm(prompt, user_api_key)

    return {
        "startup_id": startup.id,
        "startup_name": startup.name,
        "go_to_market": result,
    }
@router.get("/download-report/{startup_id}")
def download_report(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = (
        db.query(Startup)
        .filter(
            Startup.id == startup_id,
            Startup.user_id == current_user.id,
        )
        .first()
    )

    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    pdf_path = os.path.join(
        tempfile.gettempdir(),
        f"LaunchMind_Report_{startup.id}.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>LaunchMind AI Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Startup:</b> {startup.name}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Industry:</b> {startup.industry}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Stage:</b> {startup.stage}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Audience:</b> {startup.target_audience}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Description:</b> {startup.description}", styles["BodyText"]))

    story.append(Paragraph("<br/><b>Generated by LaunchMind AI</b>", styles["Heading2"]))

    doc.build(story)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{startup.name}_Report.pdf"
    )