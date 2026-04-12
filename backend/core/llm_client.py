# core/llm_client.py — full updated version with Langfuse

import json
import re
import time
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from observability.langfuse_logger import log_llm_call, log_error

_client = None

def get_groq_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def call_llm(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    trace_name: str = "llm_call",
    metadata: dict = None
) -> str:
    """
    Call Groq LLM and log to Langfuse automatically.
    trace_name identifies which feature triggered this call.
    """
    client = get_groq_client()
    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            temperature=temperature,
            max_tokens=4096,        # ← ADD THIS LINE
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ]
        )
        result = response.choices[0].message.content

        # Log successful call
        latency_ms = (time.time() - start_time) * 1000
        log_llm_call(
            trace_name=trace_name,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response=result,
            latency_ms=round(latency_ms, 2),
            metadata=metadata
        )

        return result

    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        log_error(trace_name, str(e), metadata)
        raise


def call_llm_json(
    system_prompt: str,
    user_prompt: str,
    trace_name: str = "llm_call",
    metadata: dict = None
) -> dict:
    raw = call_llm(
        system_prompt,
        user_prompt,
        temperature=0.1,
        trace_name=trace_name,
        metadata=metadata
    )
    return extract_json(raw)

def extract_json(text: str) -> dict:
    """
    Extract JSON from LLM response with multiple fallback strategies.
    Handles truncated responses by attempting to repair them.
    """
    import re
    import json

    # Strategy 1: Direct parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # Strategy 2: Extract from markdown code block
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Strategy 3: Find first complete { } block
    brace_match = re.search(r"\{[\s\S]*\}", text)
    if brace_match:
        try:
            return json.loads(brace_match.group())
        except json.JSONDecodeError:
            pass

    # Strategy 4: Attempt to repair truncated JSON
    # Find the opening brace and try to close it
    first_brace = text.find("{")
    if first_brace != -1:
        partial = text[first_brace:]
        repaired = _repair_truncated_json(partial)
        if repaired:
            return repaired

    raise ValueError(
        f"LLM did not return valid JSON.\nRaw response:\n{text[:500]}"
    )


def _repair_truncated_json(text: str) -> dict:
    """
    Attempt to repair JSON truncated mid-generation.
    Closes unclosed strings, arrays, and objects.
    """
    import json

    # Count open braces and brackets
    open_braces = text.count("{") - text.count("}")
    open_brackets = text.count("[") - text.count("]")

    repaired = text.rstrip()

    # Remove trailing incomplete string or key
    # Find last complete value (ends with ", or } or ] or a complete string)
    last_comma = repaired.rfind(",")
    last_close = max(repaired.rfind("}"), repaired.rfind("]"))

    if last_comma > last_close:
        # Truncated after a comma — remove the incomplete entry
        repaired = repaired[:last_comma]

    # Close open brackets first (inner → outer)
    repaired += "]" * open_brackets
    repaired += "}" * open_braces

    try:
        return json.loads(repaired)
    except json.JSONDecodeError:
        return None