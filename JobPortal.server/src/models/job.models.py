import uuid
from sqlalchemy import Column, String, DateTime, ARRAY, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.models.base import Base, JobStatus

class JobListing(Base):
    __tablename__ = "job_listings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(ARRAY(String), nullable=False, default=list)
    experience_level = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(Enum(JobStatus, name="job_status_enum", create_type=True), nullable=False, default=JobStatus.open)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship to applications
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
