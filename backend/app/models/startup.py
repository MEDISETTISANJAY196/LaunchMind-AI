from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Startup(Base):
    __tablename__ = "startups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    industry = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    stage = Column(String, default="Ideation") # Ideation, Validation, Scaling
    target_audience = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="startups")
    swots = relationship("SWOTAnalysis", back_populates="startup", cascade="all, delete-orphan")
    market_researches = relationship("MarketResearch", back_populates="startup", cascade="all, delete-orphan")
    competitor_analyses = relationship("CompetitorAnalysis", back_populates="startup", cascade="all, delete-orphan")
    business_canvases = relationship("BusinessCanvas", back_populates="startup", cascade="all, delete-orphan")
    brandings = relationship("Branding", back_populates="startup", cascade="all, delete-orphan")
    mentorships = relationship("MentorshipSession", back_populates="startup", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="startup", cascade="all, delete-orphan")
