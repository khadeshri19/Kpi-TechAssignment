from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from src.core.database import get_db
from src.core.dependencies import RoleChecker
from src.models import UserRole
from src.Modules.Candidate.types import CandidateProfileResponse, CandidateProfileCreate, MatchRequest, MatchResponseItem
from src.Modules.Candidate.controller import CandidateController
from src.repositories import CandidateRepository

router = APIRouter(prefix="/candidate", tags=["Candidates"])

candidate_guard = RoleChecker([UserRole.candidate])
match_guard = RoleChecker([UserRole.candidate, UserRole.admin])

@router.get("/profile", response_model=CandidateProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user = Depends(candidate_guard)
):
    """
    Retrieves the current candidate's profile. Accessible by Candidates only.
    """
    return CandidateController.get_profile(db, current_user)

@router.post("/profile", response_model=CandidateProfileResponse)
def upsert_profile(
    payload: CandidateProfileCreate,
    db: Session = Depends(get_db),
    current_user = Depends(candidate_guard)
):
    """
    Creates or updates the candidate profile. Accessible by Candidates only.
    """
    return CandidateController.upsert_profile(payload, db, current_user)

@router.post("/match", response_model=List[MatchResponseItem])
async def ai_match_jobs(
    payload: MatchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(match_guard)
):
    """
    Ranks open job listings using AI semantics matching against candidate's profile.
    Accessible by Candidates or Administrators.
    """
    # Security check: candidates can only run matching on their own profile
    if current_user.role == UserRole.candidate:
        profile = CandidateRepository.get_by_user_id(db, current_user.id)
        if not profile or profile.id != payload.candidate_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Candidates are only authorized to run AI matching on their own profiles."
            )
            
    return await CandidateController.match_candidate(db, payload.candidate_id, payload.query)
