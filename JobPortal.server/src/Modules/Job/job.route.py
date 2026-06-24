from fastapi import APIRouter, Depends, Query, status, Header
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from src.core.database import get_db
from src.core.dependencies import RoleChecker
from src.models import UserRole
from src.core.security import decode_token
from src.Modules.Job.types import JobListingCreate, JobListingUpdate, JobListingResponse
from src.Modules.Job.controller import JobController

router = APIRouter(prefix="/jobs", tags=["Jobs"])

admin_guard = RoleChecker([UserRole.admin])

@router.post("", response_model=JobListingResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    payload: JobListingCreate,
    db: Session = Depends(get_db),
    _current_user = Depends(admin_guard)
):
    """
    Creates a new job listing. Accessible by Administrators only.
    """
    return JobController.create_job(payload, db)

@router.get("", response_model=List[JobListingResponse])
def list_jobs(
    skill: Optional[str] = Query(None, description="Filter by required skill"),
    location: Optional[str] = Query(None, description="Filter by location (case-insensitive)"),
    experience_level: Optional[str] = Query(None, description="Filter by experience level (case-insensitive)"),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Lists job listings. Filters to show only active listings for candidates/guests,
    or shows all listings if authorization token belongs to an administrator.
    """
    role = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        payload = decode_token(token)
        if payload:
            role = payload.get("role")

    return JobController.list_jobs(db, skill, location, experience_level, current_user_role=role)

@router.put("/{id}", response_model=JobListingResponse)
def update_job(
    id: UUID,
    payload: JobListingUpdate,
    db: Session = Depends(get_db),
    _current_user = Depends(admin_guard)
):
    """
    Updates an existing job listing's properties. Accessible by Administrators only.
    """
    return JobController.update_job(id, payload, db)
