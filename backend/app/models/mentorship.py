from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class MentorshipSession(Base):
    __tablename__ = "mentorship_sessions"

    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"), nullable=False)
    mentor_name = Column(String, nullable=False) # e.g. Steve Jobs, Paul Graham, etc.
    messages_json = Column(Text, nullable=True, default="[]") # JSON list of messages
    created_at = Column(DateTime, default=datetime.utcnow)

    startup = relationship("Startup", back_populates="mentorships")
