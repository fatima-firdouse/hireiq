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
    max_tokens: int = 4096,
    response_format: dict = None,
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
        kwargs = {
            "model": GROQ_MODEL,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ]
        }
        if response_format:
            kwargs["response_format"] = response_format

        response = client.chat.completions.create(**kwargs)
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
        max_tokens=4096,
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
    Uses stack-based bracket/brace tracking so nesting is preserved.
    """
    import json

    # If text ends with an unclosed key or value after comma, strip back to last comma
    last_comma = text.rfind(",")
    if last_comma != -1:
        text = text[:last_comma]

    stack = []
    in_str = False
    esc = False
    for c in text:
        if esc:
            esc = False
            continue
        if c == "\\":
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if not in_str:
            if c in "{[":
                stack.append("}" if c == "{" else "]")
            elif c in "}]":
                if stack and stack[-1] == c:
                    stack.pop()

    if in_str:
        text += '"'

    while stack:
        text += stack.pop()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None