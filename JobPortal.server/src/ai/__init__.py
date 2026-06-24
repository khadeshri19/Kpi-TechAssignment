from src.ai.matcher import score_match
from src.ai.explainer import generate_explanation
from typing import Dict, Any, List

def run_candidate_matching(
    candidate_profile_data: Dict[str, Any],
    open_jobs_data: List[Dict[str, Any]],
    user_query: str
) -> List[Dict[str, Any]]:
    """
    Orchestrates the scoring and explanation generation for a set of jobs.
    Returns a sorted list of matches: [{'job_id': ..., 'match_score': ..., 'explanation': ...}]
    """
    results = []
    for job in open_jobs_data:
        # Score the candidate against the job
        score_res = score_match(candidate_profile_data, job, user_query)
        
        # Generate semantic plain-text explanation
        explanation = generate_explanation(
            matched_skills=score_res["matched_skills"],
            missing_skills=score_res["missing_skills"],
            score=score_res["score"]
        )
        
        results.append({
            "job_id": job["id"],
            "match_score": score_res["score"],
            "explanation": explanation
        })
        
    # Sort results descending by score
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
