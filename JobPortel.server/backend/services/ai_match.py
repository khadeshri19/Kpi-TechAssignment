import os
import json
import google.generativeai as genai
from typing import List, Dict, Any

# Configure Gemini SDK
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

async def match_candidate_to_jobs(
    candidate_profile_data: Dict[str, Any],
    open_jobs_data: List[Dict[str, Any]],
    user_query: str
) -> List[Dict[str, Any]]:
    """
    Interfaces with the Gemini API to match and rank open jobs against candidate data.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not configured.")

    if not open_jobs_data:
        return []

    # Construct the instruction prompt
    system_prompt = (
        "You are an expert technical recruiter and talent matching system.\n"
        "Your task is to match a candidate profile against a list of open job listings based on "
        "their skills, education, experience, preferences, and a natural language query.\n\n"
        "Instructions:\n"
        "1. Evaluate every job in the list.\n"
        "2. Provide a match score from 1 to 100 for each job.\n"
        "3. Provide a strict 2-sentence explanation of the engineering justification for the score.\n"
        "4. Return ONLY a valid JSON array of objects. Do NOT wrap the JSON in ```json markdown or add any introductory text. "
        "The output must match this schema exactly:\n"
        "[\n"
        "  {\n"
        "    \"job_id\": \"string (UUID of the job)\",\n"
        "    \"match_score\": integer,\n"
        "    \"explanation\": \"string (exactly 2 sentences)\"\n"
        "  }\n"
        "]"
    )

    prompt = (
        f"Candidate Query: \"{user_query}\"\n\n"
        f"Candidate Profile:\n{json.dumps(candidate_profile_data, indent=2)}\n\n"
        f"Open Jobs:\n{json.dumps(open_jobs_data, indent=2)}\n"
    )

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt,
        generation_config={"response_mime_type": "application/json"}
    )

    response = await model.generate_content_async(prompt)
    
    try:
        results = json.loads(response.text)
        # Ensure the results are sorted by match_score in descending order
        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        return results
    except Exception as e:
        # If the response text fails to parse, try cleaning markdown wrappers if present
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
