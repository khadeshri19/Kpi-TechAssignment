from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from src.Modules.Job.service import JobService
from src.Modules.Job.types import JobListingCreate, JobListingUpdate

class JobController:
    @staticmethod
    def create_job(payload: JobListingCreate, db: Session):
        return JobService.create_job(db, payload)

    @staticmethod
    def list_jobs(db: Session, skill: Optional[str], location: Optional[str], experience_level: Optional[str], current_user_role: Optional[str]):
        return JobService.list_jobs(db, skill, location, experience_level, current_user_role)

    @staticmethod
    def update_job(id: UUID, payload: JobListingUpdate, db: Session):
        return JobService.update_job(db, id, payload)
