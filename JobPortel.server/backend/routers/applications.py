from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from backend.database import get_db
from backend.models import Application, JobListing, CandidateProfile, User
from backend.schemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse, ApplicationDetailResponse

router = APIRouter(tags=["Applications"])

@router.post("/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_to_job(payload: ApplicationCreate, db: Session = Depends(get_db)):
    # Validate job existence
    job = db.query(JobListing).filter(JobListing.id == payload.job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job listing not found")

    # Validate candidate profile existence
    candidate = db.query(CandidateProfile).filter(CandidateProfile.id == payload.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate profile not found")

    # Check for existing duplicate application
    existing_app = db.query(Application).filter(
        Application.job_id == payload.job_id,
        Application.candidate_id == payload.candidate_id
    ).first()
    if existing_app:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate has already applied to this job."
        )

    application = Application(**payload.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

@router.get("/jobs/{id}/applications", response_model=List[ApplicationResponse])
def get_job_applications(id: UUID, db: Session = Depends(get_db)):
    job = db.query(JobListing).filter(JobListing.id == id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job listing not found")

    applications = db.query(Application).filter(Application.job_id == id).all()
    return applications

@router.get("/jobs/{id}/applications/details", response_model=List[ApplicationDetailResponse])
def get_job_applications_details(id: UUID, db: Session = Depends(get_db)):
    job = db.query(JobListing).filter(JobListing.id == id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job listing not found")

    results = db.query(
        Application.id,
        Application.job_id,
        Application.candidate_id,
        Application.status,
        Application.applied_at,
        User.name.label("candidate_name"),
        User.email.label("candidate_email"),
        CandidateProfile.skills.label("candidate_skills"),
        CandidateProfile.education.label("candidate_education"),
        CandidateProfile.project_summaries.label("candidate_project_summaries")
    ).select_from(Application)\
     .join(CandidateProfile, Application.candidate_id == CandidateProfile.id)\
     .join(User, CandidateProfile.user_id == User.id)\
     .filter(Application.job_id == id)\
     .all()

    return results


@router.patch("/applications/{id}/status", response_model=ApplicationResponse)
def update_application_status(id: UUID, payload: ApplicationUpdate, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    application.status = payload.status
    db.commit()
    db.refresh(application)
    return application
