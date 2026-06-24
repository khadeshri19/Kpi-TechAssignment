from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class MatchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Free-text query to search jobs (e.g. skills, title, experience).")
    limit: Optional[int] = Field(default=5, ge=1, le=50)

class MatchExplanationResponse(BaseModel):
    job_id: UUID
    title: str
    description: str
    required_skills: List[str]
    experience_level: str
    location: str
    score: float
    explanation: str
