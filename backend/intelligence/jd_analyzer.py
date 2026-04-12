# intelligence/jd_analyzer.py

from core.llm_client import call_llm_json
from prompts.jd_analysis import JD_ANALYSIS_SYSTEM_PROMPT, JD_ANALYSIS_USER_PROMPT


def analyze_jd(job_description: str) -> dict:
    """
    Analyze job description for quality issues.

    Checks:
    - Vague language
    - Missing info (salary, location, work mode)
    - Unrealistic expectations
    - Requirement inflation score
    - Role clarity

    Args:
        job_description: raw JD text

    Returns:
        Structured quality analysis dict with inflation score
    """
    if len(job_description.strip()) < 50:
        raise ValueError("Job description too short for analysis.")

    user_prompt = JD_ANALYSIS_USER_PROMPT.format(
        job_description=job_description
    )

    result = call_llm_json(
        JD_ANALYSIS_SYSTEM_PROMPT,
        user_prompt,
        trace_name="jd_analysis"
    )

    return result