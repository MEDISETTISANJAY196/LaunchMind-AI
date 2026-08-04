from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class CompetitorAnalysis(Base):
    __tablename__ = "competitor_analyses"

    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    competitors_json = Column(Text, nullable=True) # JSON list of competitors
    market_gaps = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    startup = relationship("Startup", back_populates="competitor_analyses")
