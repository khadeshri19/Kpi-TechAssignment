from sqlalchemy.orm import Session
from uuid import UUID
from src.Modules.Application.service import ApplicationService
from src.Modules.Application.types import ApplicationCreate, ApplicationUpdate
from src.repositories import CandidateRepository

class ApplicationController:
    @staticmethod
    def apply_to_job(payload: ApplicationCreate, db: Session):
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
