from sqlalchemy.orm import Session
from uuid import UUID
from src.models import JobListing, JobStatus
from typing import List, Optional

class JobRepository:
    """
    Handles all database operations for the JobListing model.
    """
    
    @staticmethod
    def create(db: Session, job: JobListing) -> JobListing:
        """
        Persists a new job listing to the database.
        """
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def get_by_id(db: Session, job_id: UUID) -> Optional[JobListing]:
        """
        Retrieves a single job listing by its UUID primary key.
        """
        return db.query(JobListing).filter(JobListing.id == job_id).first()

    @staticmethod
    def list_active(
        db: Session,
        skill: Optional[str] = None,
        location: Optional[str] = None,
        experience_level: Optional[str] = None
    ) -> List[JobListing]:
        """
        Lists all jobs that are 'open', optionally filtered by skill, location, or experience level.
        """
        query = db.query(JobListing).filter(JobListing.status == JobStatus.open)
        
        if skill:
            query = query.filter(JobListing.required_skills.any(skill))
        if location:
            query = query.filter(JobListing.location.ilike(f"%{location}%"))
        if experience_level:
            query = query.filter(JobListing.experience_level.ilike(f"%{experience_level}%"))
            
        return query.all()

    @staticmethod
    def list_all(db: Session) -> List[JobListing]:
        """
        Lists all job listings (both open and closed), primarily for admin dashboards.
        """
        return db.query(JobListing).all()

    @staticmethod
    def update(db: Session, job: JobListing) -> JobListing:
        """
        Commits any pending updates on the job listing instance to the database.
        """
        db.commit()
        db.refresh(job)
        return job
