from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from src.repositories import ApplicationRepository, JobRepository, CandidateRepository
from src.models import Application, JobStatus
from src.Modules.Application.types import ApplicationCreate, ApplicationUpdate
from typing import List, Any

class ApplicationService:
    """
    Houses all business logic workflows for job applications and status pipelines.
    """

    @staticmethod
    def apply_to_job(db: Session, payload: ApplicationCreate) -> Application:
        """
        Creates a new job application after running validation checks.
        Saves a frozen snapshot of the candidate's profile state at the moment of submission.
        """
        # Validate job existence and verify that it is accepting applications
        job = JobRepository.get_by_id(db, payload.job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job listing not found."
            )
        if job.status != JobStatus.open:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This job listing is closed for applications."
            )

        # Validate candidate profile existence
        candidate = CandidateRepository.get_by_id(db, payload.candidate_id)
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate profile not found."
            )

        # Ensure applicant hasn't already submitted for this specific listing
        existing_app = ApplicationRepository.get_by_job_and_candidate(db, payload.job_id, payload.candidate_id)
        if existing_app:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied for this job."
            )

        # Capture a static profile snapshot to preserve historical data
        profile_snapshot_data = {
            "skills": candidate.skills,
            "education": candidate.education,
            "project_summaries": candidate.project_summaries,
            "preferences": candidate.preferences
        }

        # Build application instance
        application = Application(
            job_id=payload.job_id,
            candidate_id=payload.candidate_id,
            profile_snapshot=profile_snapshot_data
        )

        return ApplicationRepository.create(db, application)

    @staticmethod
    def get_job_applications(db: Session, job_id: UUID) -> List[Application]:
        """
        Retrieves all application records for a job.
        """
        job = JobRepository.get_by_id(db, job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job listing not found."
            )
        return ApplicationRepository.list_by_job_id(db, job_id)

    @staticmethod
    def get_candidate_applications(db: Session, candidate_id: UUID) -> List[Application]:
        """
        Retrieves all application records submitted by a candidate.
        """
        return ApplicationRepository.list_by_candidate_id(db, candidate_id)

    @staticmethod
    def get_job_applications_details(db: Session, job_id: UUID) -> List[Any]:
        """
        Retrieves application records with full candidate details for recruitment views.
        """
        job = JobRepository.get_by_id(db, job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job listing not found."
            )
        return ApplicationRepository.list_details_by_job_id(db, job_id)

    @staticmethod
    def update_application_status(db: Session, application_id: UUID, payload: ApplicationUpdate) -> Application:
        """
        Updates the status of an application (e.g. applied, shortlisted, rejected).
        """
        application = ApplicationRepository.get_by_id(db, application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application record not found."
            )
        
        application.status = payload.status
        return ApplicationRepository.update(db, application)
