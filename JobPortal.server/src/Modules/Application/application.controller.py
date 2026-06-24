from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from src.Modules.Application.service import ApplicationService
from src.Modules.Application.types import ApplicationCreate, ApplicationUpdate
from src.repositories import CandidateRepository

class ApplicationController:
    @staticmethod
    def apply_to_job(payload: ApplicationCreate, db: Session, current_user):
        candidate = CandidateRepository.get_by_user_id(db, current_user.id)
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate profile not found for the current user. Please create a profile first."
            )
        # Override the candidate_id in payload with the logged-in candidate's profile ID for security
        payload.candidate_id = candidate.id
        return ApplicationService.apply_to_job(db, payload)

    @staticmethod
    def get_candidate_applications(db: Session, current_user):
        candidate = CandidateRepository.get_by_user_id(db, current_user.id)
        if not candidate:
            return []
        return ApplicationService.get_candidate_applications(db, candidate.id)

    @staticmethod
    def get_job_applications(job_id: UUID, db: Session):
        return ApplicationService.get_job_applications(db, job_id)

    @staticmethod
    def get_job_applications_details(job_id: UUID, db: Session):
        return ApplicationService.get_job_applications_details(db, job_id)

    @staticmethod
    def update_application_status(id: UUID, payload: ApplicationUpdate, db: Session):
        return ApplicationService.update_application_status(db, id, payload)
