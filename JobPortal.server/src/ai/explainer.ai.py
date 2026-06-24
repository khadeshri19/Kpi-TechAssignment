from typing import List

def generate_explanation(matched_skills: List[str], missing_skills: List[str], score: int) -> str:
    """
    Generates a 1-2 sentence explanation outlining why the candidate is a match
    and where they might have gaps.
    """
    matched_str = ", ".join(sorted(matched_skills)) if matched_skills else "general qualifications"
    missing_str = ", ".join(sorted(missing_skills)) if missing_skills else "none"

    sentence_1 = f"Matches candidate's expertise in {matched_str} with {score}% query-to-job relevance."
    if missing_skills:
        sentence_2 = f"Some skill gaps remain in {missing_str} compared to job requirements."
    else:
        sentence_2 = "The candidate satisfies all requested technical requirements."

    return f"{sentence_1} {sentence_2}"
