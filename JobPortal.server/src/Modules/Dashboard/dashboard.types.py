from pydantic import BaseModel
from typing import List, Dict

class DashboardMetricsResponse(BaseModel):
    applications_per_job: List[dict]
    pipeline_status_counts: dict
    skill_distribution: List[dict]
