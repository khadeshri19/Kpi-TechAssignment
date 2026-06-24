import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.models.base import Base, ApplicationStatus

class Application(Base):
    __tablename__ = "applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_listings.id", ondelete="CASCADE"), nullable=False)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(ApplicationStatus, name="application_status_enum", create_type=True), nullable=False, default=ApplicationStatus.applied)
    applied_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    profile_snapshot = Column(JSONB, nullable=True)
    
    # Relationships
    job = relationship("JobListing", back_populates="applications")
    candidate = relationship("CandidateProfile", back_populates="applications")
