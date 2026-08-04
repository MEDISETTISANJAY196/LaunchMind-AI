from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class BusinessCanvas(Base):
    __tablename__ = "business_canvases"

    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    
    # 9 building blocks
    customer_segments = Column(Text, nullable=True)
    value_propositions = Column(Text, nullable=True)
    channels = Column(Text, nullable=True)
    customer_relationships = Column(Text, nullable=True)
    revenue_streams = Column(Text, nullable=True)
    key_resources = Column(Text, nullable=True)
    key_activities = Column(Text, nullable=True)
    key_partners = Column(Text, nullable=True)
    cost_structure = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    startup = relationship("Startup", back_populates="business_canvases")
