from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List, Dict, Optional

class CandidateProfilePreferences(BaseModel):
    desired_roles: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    experience_level: str = Field("", max_length=50)

class CandidateProfileBase(BaseModel):
    user_id: UUID
    skills: List[str] = Field(default_factory=list)
    education: str = Field("", max_length=500)
    project_summaries: str = Field("", max_length=2000)
    preferences: CandidateProfilePreferences = Field(default_factory=CandidateProfilePreferences)

class CandidateProfileCreate(CandidateProfileBase):
    pass

class CandidateProfileUpdate(CandidateProfileBase):
    pass

class CandidateProfileResponse(CandidateProfileBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MatchRequest(BaseModel):
    candidate_id: UUID
    query: str

class MatchResponseItem(BaseModel):
    job_id: UUID
    match_score: int
    explanation: str
