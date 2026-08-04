from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class SWOTAnalysis(Base):
    __tablename__ = "swot_analyses"

    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    strengths = Column(Text, nullable=True) # Comma-separated or markdown list
    weaknesses = Column(Text, nullable=True)
    opportunities = Column(Text, nullable=True)
    threats = Column(Text, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    startup = relationship("Startup", back_populates="swots")
