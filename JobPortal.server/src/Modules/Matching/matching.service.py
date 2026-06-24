from typing import List, Dict, Any
from src.ai import run_candidate_matching

class MatchingService:
    """
    Business service coordinating candidate-job semantic matching.
    """

    @staticmethod
    async def match_candidate_to_jobs(
        candidate_profile_data: Dict[str, Any],
        open_jobs_data: List[Dict[str, Any]],
        user_query: str
    ) -> List[Dict[str, Any]]:
        """
        Orchestrates and triggers the AI ranking algorithm on the provided inputs.
        """
        return run_candidate_matching(
            candidate_profile_data=candidate_profile_data,
            open_jobs_data=open_jobs_data,
            user_query=user_query
        )
