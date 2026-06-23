import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, ARRAY, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
 
class UserRole(str, enum.Enum):
    admin = "admin"
    candidate = "candidate"
 
class JobStatus(str, enum.Enum):
    open = "open"
    closed = "closed"
 
class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    shortlisted = "shortlisted"
    rejected = "rejected"
 
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(Enum(UserRole, name="user_role_enum", create_type=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    profile = relationship("CandidateProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
 
class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    skills = Column(ARRAY(String), nullable=False, default=list) 
    education = Column(Text, nullable=True)
    project_summaries = Column(Text, nullable=True)
    preferences = Column(JSONB, nullable=False, default=dict) 
    user = relationship("User", back_populates="profile")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")
 
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
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
 
class Application(Base):
    __tablename__ = "applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_listings.id", ondelete="CASCADE"), nullable=False)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(ApplicationStatus, name="application_status_enum", create_type=True), nullable=False, default=ApplicationStatus.applied)
    applied_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    job = relationship("JobListing", back_populates="applications")
    candidate = relationship("CandidateProfile", back_populates="applications")
