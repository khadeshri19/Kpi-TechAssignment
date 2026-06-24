from sqlalchemy.orm import Session
from uuid import UUID
from src.models import Application, CandidateProfile, User
from typing import List, Optional, Any

class ApplicationRepository:
    """
    Handles all database operations for the Application model.
    """

    @staticmethod
    def create(db: Session, application: Application) -> Application:
        """
        Saves a new job application.
        """
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def get_by_id(db: Session, application_id: UUID) -> Optional[Application]:
        """
        Retrieves a single application by its primary key UUID.
        """
        return db.query(Application).filter(Application.id == application_id).first()

    @staticmethod
    def get_by_job_and_candidate(db: Session, job_id: UUID, candidate_id: UUID) -> Optional[Application]:
        """
        Checks for an existing application by a specific candidate for a specific job.
        """
        return db.query(Application).filter(
            Application.job_id == job_id,
            Application.candidate_id == candidate_id
        ).first()

    @staticmethod
    def list_by_job_id(db: Session, job_id: UUID) -> List[Application]:
        """
        Retrieves all simple application records for a specific job.
        """
        return db.query(Application).filter(Application.job_id == job_id).all()

    @staticmethod
    def list_by_candidate_id(db: Session, candidate_id: UUID) -> List[Application]:
        """
        Retrieves all application records submitted by a specific candidate.
        """
        return db.query(Application).filter(Application.candidate_id == candidate_id).all()

    @staticmethod
    def list_details_by_job_id(db: Session, job_id: UUID) -> List[Any]:
        """
        Performs a detailed JOIN query across Applications, Candidate Profiles, and Users
        to fetch candidate information (name, email, skills, education) for admin dashboards.
        """
        return db.query(
            Application.id,
            Application.job_id,
            Application.candidate_id,
            Application.status,
            Application.applied_at,
            Application.profile_snapshot,
            User.name.label("candidate_name"),
            User.email.label("candidate_email"),
            CandidateProfile.skills.label("candidate_skills"),
            CandidateProfile.education.label("candidate_education"),
            CandidateProfile.project_summaries.label("candidate_project_summaries")
        ).select_from(Application)\
         .join(CandidateProfile, Application.candidate_id == CandidateProfile.id)\
         .join(User, CandidateProfile.user_id == User.id)\
         .filter(Application.job_id == job_id)\
         .all()

    @staticmethod
    def get_applications_count_per_job(db: Session) -> List[Any]:
        """
        Calculates applications count per job listing for admin statistics.
        """
        from src.models import JobListing
        from sqlalchemy import func
        return db.query(
            JobListing.title,
            func.count(Application.id).label("count")
        ).outerjoin(Application, JobListing.id == Application.job_id)\
         .group_by(JobListing.id, JobListing.title)\
         .all()

    @staticmethod
    def get_status_counts(db: Session) -> List[Any]:
        """
        Aggregates application records count by pipeline status.
        """
        from sqlalchemy import func
        return db.query(
            Application.status,
            func.count(Application.id).label("count")
        ).group_by(Application.status)\
         .all()

    @staticmethod
    def update(db: Session, application: Application) -> Application:
        """
        Saves updates (such as status changes) to an application.
        """
        db.commit()
        db.refresh(application)
        return application

