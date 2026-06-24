from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from src.repositories import JobRepository
from src.models import JobListing, UserRole
from src.Modules.Job.types import JobListingCreate, JobListingUpdate
from typing import List, Optional

class JobService:
    """
    Houses all business logic workflows for managing job listings.
    """

    @staticmethod
    def create_job(db: Session, payload: JobListingCreate) -> JobListing:
        """
        Creates a new job listing record.
        """
        job = JobListing(
            title=payload.title,
            description=payload.description,
            required_skills=payload.required_skills,
            experience_level=payload.experience_level,
            location=payload.location,
            status=payload.status
        )
        return JobRepository.create(db, job)

    @staticmethod
    def get_job(db: Session, job_id: UUID) -> JobListing:
        """
        Retrieves a job listing, raising a 404 error if it does not exist.
        """
        job = JobRepository.get_by_id(db, job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job listing not found."
            )
        return job

    @staticmethod
    def update_job(db: Session, job_id: UUID, payload: JobListingUpdate) -> JobListing:
        """
        Updates an existing job listing's properties.
        """
        job = JobService.get_job(db, job_id)
        
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(job, key, value)
            
        return JobRepository.update(db, job)

    @staticmethod
    def list_jobs(
        db: Session,
        skill: Optional[str] = None,
        location: Optional[str] = None,
        experience_level: Optional[str] = None,
        current_user_role: Optional[str] = None
    ) -> List[JobListing]:
        """
        Retrieves list of jobs.
        Candidates/anonymous users only see 'open' jobs, while admins can list all jobs.
        """
        if current_user_role == UserRole.admin.value:
            # Admins get all records for management pipelines
            return JobRepository.list_all(db)
        
        # Candidates/guests only get matching open positions
        return JobRepository.list_active(db, skill, location, experience_level)
