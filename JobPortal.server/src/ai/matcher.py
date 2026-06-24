import logging
from typing import List, Dict, Any, Optional
from src.ai.embeddings import encode_text
import numpy as np

logger = logging.getLogger(__name__)

def calculate_cosine_similarity(v1: Any, v2: Any) -> float:
    """
    Computes cosine similarity between two vectors.
    """
    try:
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return float(dot_product / (norm_v1 * norm_v2))
    except Exception as e:
        logger.error(f"Error calculating cosine similarity: {str(e)}")
        return 0.0

def score_match(
    candidate_profile_data: Dict[str, Any],
    job: Dict[str, Any],
    user_query: str
) -> Dict[str, Any]:
    """
    Computes a score from 1-100 and tracks overlap metrics for a single job match.
    """
    candidate_skills = candidate_profile_data.get("skills", [])
    candidate_skills_set = set(s.lower().strip() for s in candidate_skills)
    education = candidate_profile_data.get("education", "")
    projects = candidate_profile_data.get("project_summaries", "")
    
    candidate_text = (
        f"Query: {user_query}. "
        f"Skills: {', '.join(candidate_skills)}. "
        f"Education: {education}. "
        f"Projects: {projects}."
    )

    job_id = job.get("id")
    title = job.get("title", "")
    desc = job.get("description", "")
    req_skills = job.get("required_skills", [])
    req_skills_set = set(s.lower().strip() for s in req_skills)
    exp_level = job.get("experience_level", "")

    # Compute skill overlap metrics
    matched_skills = candidate_skills_set.intersection(req_skills_set)
    missing_skills = req_skills_set.difference(candidate_skills_set)

    # 1. Try semantic embeddings
    candidate_emb = encode_text(candidate_text)
    score = 0.0

    if candidate_emb is not None:
        try:
            job_text = f"Title: {title}. Description: {desc}. Required Skills: {', '.join(req_skills)}. Experience: {exp_level}."
            job_emb = encode_text(job_text)
            if job_emb is not None:
                similarity = calculate_cosine_similarity(candidate_emb, job_emb)
                # Map cosine similarity (usually 0.1 to 0.8 for text) to 0-100 scale
                semantic_score = max(0, min(100, int((similarity + 0.2) * 100)))
                
                # Combine semantic score (70%) with direct skill overlap (30%)
                skill_ratio = len(matched_skills) / len(req_skills_set) if req_skills_set else 1.0
                score = int(0.7 * semantic_score + 0.3 * (skill_ratio * 100))
            else:
                candidate_emb = None # Trigger keyword fallback if job embedding fails
        except Exception as e:
            logger.error(f"Embedding match failed for job {job_id}: {str(e)}")
            candidate_emb = None # Trigger keyword fallback

    # 2. Fallback to Jaccard similarity & keyword weights if no embeddings
    if candidate_emb is None:
        total_req = len(req_skills_set)
        skill_ratio = len(matched_skills) / total_req if total_req > 0 else 1.0
        
        # Simple keyword match in description/title
        desc_lower = desc.lower()
        query_match_count = sum(1 for word in user_query.lower().split() if word in desc_lower or word in title.lower())
        query_score = min(100, (query_match_count / max(1, len(user_query.split()))) * 100)
        
        score = int(0.6 * (skill_ratio * 100) + 0.4 * query_score)

    score = max(1, min(100, int(score)))

    return {
        "job": job,
        "score": score,
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills)
    }
