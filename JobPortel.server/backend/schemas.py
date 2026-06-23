from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from backend.models import UserRole, JobStatus, ApplicationStatus
 
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: UserRole
 
class UserCreate(UserBase):
    pass
 
class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
 
class CandidateProfilePreferences(BaseModel):
    location: Optional[str] = None
    role_type: Optional[str] = None
    domain_interest: Optional[str] = None
 
class CandidateProfileBase(BaseModel):
    skills: List[str] = Field(default_factory=list)
    education: Optional[str] = None
    project_summaries: Optional[str] = None
    preferences: CandidateProfilePreferences = Field(default_factory=CandidateProfilePreferences)
 
class CandidateProfileCreate(CandidateProfileBase):
    user_id: UUID
 
class CandidateProfileUpdate(CandidateProfileBase):
    pass
 
class CandidateProfileResponse(CandidateProfileBase):
    id: UUID
    user_id: UUID
    model_config = ConfigDict(from_attributes=True)
 
class JobListingBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str
    required_skills: List[str] = Field(default_factory=list)
    experience_level: str
    location: str
    status: JobStatus = JobStatus.open
 
class JobListingCreate(JobListingBase):
    pass
 
class JobListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    experience_level: Optional[str] = None
    location: Optional[str] = None
    status: Optional[JobStatus] = None
 
class JobListingResponse(JobListingBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
 
class ApplicationBase(BaseModel):
    job_id: UUID
    candidate_id: UUID
    status: ApplicationStatus = ApplicationStatus.applied
 
class ApplicationCreate(ApplicationBase):
    pass
 
class ApplicationUpdate(BaseModel):
    status: ApplicationStatus
 
class ApplicationResponse(ApplicationBase):
    id: UUID
    applied_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ApplicationDetailResponse(BaseModel):
    id: UUID
    job_id: UUID
    candidate_id: UUID
    status: ApplicationStatus
    applied_at: datetime
    candidate_name: str
    candidate_email: str
    candidate_skills: List[str]
    candidate_education: Optional[str] = None
    candidate_project_summaries: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

