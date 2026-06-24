from sqlalchemy.orm import Session
from typing import Dict, Any, List
from src.repositories import ApplicationRepository
from src.models import CandidateProfile

class DashboardService:
    """
    Houses business logic workflows for the admin metrics dashboard (Step 9).
    """

    @staticmethod
    def get_dashboard_metrics(db: Session) -> Dict[str, Any]:
        """
        Retrieves applications per job, skill distributions, and status count pipelines.
        """
        # 1. Fetch applications per job
        job_counts_raw = ApplicationRepository.get_applications_count_per_job(db)
        applications_per_job = [
            {"job_title": row[0], "count": row[1]}
            for row in job_counts_raw
        ]

        # 2. Fetch application pipeline status distribution
        status_counts_raw = ApplicationRepository.get_status_counts(db)
        status_counts = {"applied": 0, "shortlisted": 0, "rejected": 0}
        for row in status_counts_raw:
            if row[0] is not None:
                status_counts[row[0].value] = row[1]

        # 3. Fetch candidate profile skill counts
        profiles = db.query(CandidateProfile.skills).all()
        skill_counts = {}
        for (skills,) in profiles:
            if skills:
                for skill in skills:
                    normalized = skill.strip().lower()
                    if normalized:
                        skill_counts[normalized] = skill_counts.get(normalized, 0) + 1

        # Sort and take top 10 most common skills
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        skill_distribution = [{"skill": s, "count": c} for s, c in sorted_skills]

        return {
            "applications_per_job": applications_per_job,
            "pipeline_status_counts": status_counts,
            "skill_distribution": skill_distribution
        }
