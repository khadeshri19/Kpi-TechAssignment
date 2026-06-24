from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from src.Modules.Candidate.service import CandidateService
from src.Modules.Candidate.types import CandidateProfileCreate

class CandidateController:
    @staticmethod
    def get_profile(db: Session, current_user):
        profile = CandidateService.get_profile_by_user(db, current_user.id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate profile has not been configured yet."
            )
        return profile

    @staticmethod
    def upsert_profile(payload: CandidateProfileCreate, db: Session):
        return CandidateService.upsert_profile(db, payload)

    @staticmethod
    async def match_candidate(db: Session, candidate_id: UUID, query: str):
        return await CandidateService.match_candidate(db, candidate_id, query)
