import uuid
from sqlalchemy import Column, String, ForeignKey, Text, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.models.base import Base

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    skills = Column(ARRAY(String), nullable=False, default=list) 
    education = Column(Text, nullable=True)
    project_summaries = Column(Text, nullable=True)
    preferences = Column(JSONB, nullable=False, default=dict) 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")
