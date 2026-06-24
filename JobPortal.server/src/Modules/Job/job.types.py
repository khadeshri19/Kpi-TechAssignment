from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from src.models import JobStatus

class JobListingBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: str = Field(..., min_length=10, max_length=4000)
    required_skills: List[str] = Field(default_factory=list)
    experience_level: str = Field(..., max_length=50)
    location: str = Field(..., max_length=100)
    status: JobStatus = JobStatus.open

class JobListingCreate(JobListingBase):
    pass

class JobListingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = Field(None, min_length=10, max_length=4000)
    required_skills: Optional[List[str]] = None
    experience_level: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    status: Optional[JobStatus] = None

class JobListingResponse(JobListingBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
