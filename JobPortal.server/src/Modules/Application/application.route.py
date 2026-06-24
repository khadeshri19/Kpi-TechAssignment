from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from src.core.database import get_db
from src.core.dependencies import RoleChecker
from src.models import UserRole
from src.Modules.Application.types import ApplicationCreate, ApplicationUpdate, ApplicationResponse, ApplicationDetailResponse
from src.Modules.Application.controller import ApplicationController

router = APIRouter(tags=["Applications"])

candidate_guard = RoleChecker([UserRole.candidate])
admin_guard = RoleChecker([UserRole.admin])

@router.post("/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_to_job(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(candidate_guard)
):
    """
    Submits a new job application. Accessible by Candidates only.
    """
    return ApplicationController.apply_to_job(payload, db, current_user)

@router.get("/candidate/applications", response_model=List[ApplicationResponse])
def get_candidate_applications(
    db: Session = Depends(get_db),
    current_user = Depends(candidate_guard)
):
    """
    Retrieves all applications submitted by the current candidate. Accessible by Candidates only.
    """
    return ApplicationController.get_candidate_applications(db, current_user)

@router.get("/jobs/{id}/applications", response_model=List[ApplicationResponse])
def get_job_applications(
    id: UUID,
    db: Session = Depends(get_db),
    _current_user = Depends(admin_guard)
):
    """
    Lists applications for a specific job listing. Accessible by Administrators only.
    """
    return ApplicationController.get_job_applications(id, db)

@router.get("/jobs/{id}/applications/details", response_model=List[ApplicationDetailResponse])
def get_job_applications_details(
    id: UUID,
    db: Session = Depends(get_db),
    _current_user = Depends(admin_guard)
):
    """
    Lists detailed application profiles (with candidate credentials). Accessible by Administrators only.
    """
    return ApplicationController.get_job_applications_details(id, db)

@router.patch("/applications/{id}/status", response_model=ApplicationResponse)
def update_application_status(
    id: UUID,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    _current_user = Depends(admin_guard)
):
    """
    Updates the application status pipeline (applied, shortlisted, rejected). Accessible by Administrators only.
    """
    return ApplicationController.update_application_status(id, payload, db)
