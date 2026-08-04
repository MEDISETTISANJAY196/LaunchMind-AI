from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class MarketResearch(Base):
    __tablename__ = "market_researches"

    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    tam = Column(String, nullable=True) # Total Addressable Market size/desc
    sam = Column(String, nullable=True) # Serviceable Addressable Market
    som = Column(String, nullable=True) # Serviceable Obtainable Market
    target_demographics = Column(Text, nullable=True)
    customer_personas = Column(Text, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    startup = relationship("Startup", back_populates="market_researches")
