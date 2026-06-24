from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from src.core.database import get_db
from src.core.dependencies import RoleChecker
from src.models import UserRole
from src.Modules.Candidate.types import CandidateProfileResponse, CandidateProfileCreate, MatchRequest, MatchResponseItem
from src.Modules.Candidate.controller import CandidateController

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
    _current_user = Depends(candidate_guard)
):
    """
    Creates or updates the candidate profile. Accessible by Candidates only.
    """
    return CandidateController.upsert_profile(payload, db)

@router.post("/match", response_model=List[MatchResponseItem])
async def ai_match_jobs(
    payload: MatchRequest,
    db: Session = Depends(get_db),
    _current_user = Depends(match_guard)
):
    """
    Ranks open job listings using AI semantics matching against candidate's profile.
    Accessible by Candidates or Administrators.
    """
    return await CandidateController.match_candidate(db, payload.candidate_id, payload.query)
