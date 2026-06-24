from sqlalchemy.orm import Session
from src.models import CandidateProfile, JobListing, Application, JobStatus

class AnalyticsService:
    @staticmethod
    def get_analytics_summary(db: Session) -> dict:
        total_candidates = db.query(CandidateProfile).count()
        total_jobs = db.query(JobListing).count()
        total_applications = db.query(Application).count()
        active_jobs = db.query(JobListing).filter(JobListing.status == JobStatus.open).count()

        return {
            "total_candidates": total_candidates,
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "active_jobs_count": active_jobs
        }
