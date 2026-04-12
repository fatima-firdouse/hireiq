# intelligence/bias_detector.py
# No RAG needed here — bias is detected directly from JD text.
# The JD itself is the full input.

from core.llm_client import call_llm_json
from prompts.bias_detection import BIAS_SYSTEM_PROMPT, BIAS_USER_PROMPT


def detect_bias(job_description: str) -> dict:
    """
    Analyze job description for biased language.
    
    No retrieval step needed — the JD is sent directly to the LLM.
    JDs are typically short enough to fit in context window.
    
    Args:
        job_description: raw JD text
    
    Returns:
        Structured bias report dict
    """
    if len(job_description.strip()) < 50:
        raise ValueError("Job description too short for meaningful analysis. Minimum 50 characters.")

    user_prompt = BIAS_USER_PROMPT.format(job_description=job_description)
    result = call_llm_json(
    BIAS_SYSTEM_PROMPT,
    user_prompt,
    trace_name="bias_detection"
)
    return result