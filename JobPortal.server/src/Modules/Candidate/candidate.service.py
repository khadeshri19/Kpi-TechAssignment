from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from src.repositories import CandidateRepository
from src.models import CandidateProfile
from src.Modules.Candidate.types import CandidateProfileCreate
from typing import Optional

class CandidateService:
    """
    Houses all business logic workflows for candidate profile management.
    """

    @staticmethod
    def get_profile(db: Session, profile_id: UUID) -> CandidateProfile:
        """
        Retrieves a candidate profile, raising 404 if not found.
        """
        profile = CandidateRepository.get_by_id(db, profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate profile not found."
            )
        return profile

    @staticmethod
    def get_profile_by_user(db: Session, user_id: UUID) -> Optional[CandidateProfile]:
        """
        Retrieves a candidate profile by its associated User UUID, returning None if missing.
        """
        return CandidateRepository.get_by_user_id(db, user_id)

    @staticmethod
    def upsert_profile(db: Session, payload: CandidateProfileCreate) -> CandidateProfile:
        """
        Creates a new candidate profile or updates an existing one for the specified user.
        """
        profile = CandidateRepository.get_by_user_id(db, payload.user_id)
        
        profile_data = payload.model_dump()
        # Serialize preferences dictionary if nested object matches Pydantic validation structure
        if "preferences" in profile_data and hasattr(payload.preferences, "model_dump"):
            profile_data["preferences"] = payload.preferences.model_dump()

        if profile:
            # Update existing candidate record
            for key, value in profile_data.items():
                setattr(profile, key, value)
            return CandidateRepository.update(db, profile)
        else:
            # Create a brand new record
            new_profile = CandidateProfile(**profile_data)
            return CandidateRepository.create(db, new_profile)

    @staticmethod
    async def match_candidate(db: Session, candidate_id: UUID, query: str):
        """
        Coordinates candidate profile lookup, listing open jobs, and executing the AI match algorithm.
        """
        from src.repositories import JobRepository
        
        profile = CandidateRepository.get_by_id(db, candidate_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate profile not found."
            )
            
        open_jobs = JobRepository.list_active(db)
        if not open_jobs:
            return []

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

        from src.ai import run_candidate_matching
        try:
            return run_candidate_matching(
                candidate_profile_data=profile_dict,
                open_jobs_data=open_jobs_list,
                user_query=query
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI Matching Service failed: {str(e)}"
            )
