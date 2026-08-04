from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Branding(Base):
    __tablename__ = "brandings"

    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    name_suggestions = Column(Text, nullable=True) # JSON or Comma-separated list
    slogans = Column(Text, nullable=True)
    brand_colors = Column(Text, nullable=True)
    logo_description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    startup = relationship("Startup", back_populates="brandings")
