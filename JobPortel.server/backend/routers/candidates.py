from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from backend.database import get_db
from backend.models import CandidateProfile, JobListing, JobStatus
from backend.schemas import CandidateProfileCreate, CandidateProfileResponse
from backend.services.ai_match import match_candidate_to_jobs
from pydantic import BaseModel

router = APIRouter(prefix="/candidate", tags=["Candidates"])

class MatchRequest(BaseModel):
    candidate_id: UUID
    query: str

class MatchResponseItem(BaseModel):
    job_id: UUID
    match_score: int
    explanation: str

@router.post("/profile", response_model=CandidateProfileResponse)
def upsert_profile(payload: CandidateProfileCreate, db: Session = Depends(get_db)):
    # Check if a profile already exists for the given user_id
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == payload.user_id).first()
    
    profile_data = payload.model_dump()
    # Ensure preferences is saved as a dictionary (nested Pydantic model serialization)
    if "preferences" in profile_data and hasattr(payload.preferences, "model_dump"):
        profile_data["preferences"] = payload.preferences.model_dump()

    if profile:
        # Update existing profile
        for key, value in profile_data.items():
            setattr(profile, key, value)
    else:
        # Create new profile
        profile = CandidateProfile(**profile_data)
        db.add(profile)
        
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/match", response_model=List[MatchResponseItem])
async def ai_match_jobs(payload: MatchRequest, db: Session = Depends(get_db)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.id == payload.candidate_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate profile not found")

    open_jobs = db.query(JobListing).filter(JobListing.status == JobStatus.open).all()
    if not open_jobs:
        return []

    # Map models to raw dictionary representation for the AI match payload
    profile_dict = {
        "id": str(profile.id),
        "skills": profile.skills,
        "education": profile.education,
        "project_summaries": profile.project_summaries,
        "preferences": profile.preferences
    }

    open_jobs_list = [
        {
            "id": str(job.id),
            "title": job.title,
            "description": job.description,
            "required_skills": job.required_skills,
            "experience_level": job.experience_level,
            "location": job.location
        }
        for job in open_jobs
    ]

    try:
        results = await match_candidate_to_jobs(
            candidate_profile_data=profile_dict,
            open_jobs_data=open_jobs_list,
            user_query=payload.query
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Matching Service failed: {str(e)}"
        )
