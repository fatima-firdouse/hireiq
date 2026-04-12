# observability/langfuse_logger.py
# Wraps every LLM call with Langfuse tracing.
# Tracks: prompt, response, latency, token count, errors.

import time
from typing import Optional

# Langfuse import with graceful fallback
# If keys are missing, logging silently does nothing
# App still works — observability is non-blocking
try:
    from langfuse import Langfuse
    from config import LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST

    if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
        _langfuse = Langfuse(
            public_key=LANGFUSE_PUBLIC_KEY,
            secret_key=LANGFUSE_SECRET_KEY,
            host=LANGFUSE_HOST
        )
        LANGFUSE_ENABLED = True
    else:
        _langfuse = None
        LANGFUSE_ENABLED = False

except Exception:
    _langfuse = None
    LANGFUSE_ENABLED = False


def log_llm_call(
    trace_name: str,
    system_prompt: str,
    user_prompt: str,
    response: str,
    latency_ms: float,
    metadata: Optional[dict] = None
) -> None:
    """
    Log a single LLM call to Langfuse.

    Args:
        trace_name:    name of the feature (e.g. "match_analysis")
        system_prompt: the system prompt sent to LLM
        user_prompt:   the user prompt sent to LLM
        response:      raw LLM response text
        latency_ms:    time taken in milliseconds
        metadata:      any extra info (collection_name, score, etc.)
    """
    if not LANGFUSE_ENABLED or _langfuse is None:
        return

    try:
        trace = _langfuse.trace(
            name=trace_name,
            metadata=metadata or {}
        )

        trace.generation(
            name=f"{trace_name}_generation",
            model="llama-3.1-8b-instant",
            model_parameters={"temperature": 0.1},
            input={
                "system": system_prompt,
                "user": user_prompt[:2000]  # truncate for display
            },
            output=response[:2000],
            usage={
                "input": len(user_prompt.split()),   # approximate tokens
                "output": len(response.split()),
            },
            metadata={
                "latency_ms": latency_ms,
                **(metadata or {})
            }
        )

        _langfuse.flush()  # ensure data is sent immediately

    except Exception:
        pass  # never let logging crash the main app


def log_error(trace_name: str, error: str, metadata: Optional[dict] = None) -> None:
    """Log an error event to Langfuse."""
    if not LANGFUSE_ENABLED or _langfuse is None:
        return

    try:
        trace = _langfuse.trace(
            name=f"{trace_name}_error",
            metadata={"error": error, **(metadata or {})}
        )
        _langfuse.flush()
    except Exception:
        pass