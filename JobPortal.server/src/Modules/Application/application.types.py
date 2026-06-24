from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Dict, Any, Optional
from src.models import ApplicationStatus

class ApplicationBase(BaseModel):
    job_id: UUID
    candidate_id: UUID

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: ApplicationStatus

class ApplicationResponse(ApplicationBase):
    id: UUID
    status: ApplicationStatus
    applied_at: datetime
    profile_snapshot: Dict[str, Any]
    model_config = ConfigDict(from_attributes=True)

class ApplicationDetailResponse(ApplicationResponse):
    candidate_name: str
    candidate_email: str
    candidate_skills: list
