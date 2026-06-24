import importlib.util
import pathlib
import sys
from typing import Dict, Any, List

def _load_module(name, filename):
    path = pathlib.Path(__file__).parent / filename
    module_name = f"src.ai.{name}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

# Load modules
embeddings_mod = _load_module("embeddings", "embeddings.ai.py")
explainer_mod = _load_module("explainer", "explainer.ai.py")
matcher_mod = _load_module("matcher", "matcher.ai.py")

# Expose key functions
encode_text = embeddings_mod.encode_text
generate_explanation = explainer_mod.generate_explanation
score_match = matcher_mod.score_match

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
