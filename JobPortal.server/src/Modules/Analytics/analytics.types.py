from pydantic import BaseModel
from typing import Dict, Any

class AnalyticsSummaryResponse(BaseModel):
    total_candidates: int
    total_jobs: int
    total_applications: int
    active_jobs_count: int
