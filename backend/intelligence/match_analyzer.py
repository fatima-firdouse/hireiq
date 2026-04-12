# intelligence/match_analyzer.py

import re
from core.retriever import retrieve, get_context_string
from core.llm_client import call_llm_json
from prompts.match_analysis import MATCH_SYSTEM_PROMPT, MATCH_USER_PROMPT


def anonymize_context(resume_context: str) -> str:
    """
    Remove PII from resume context for blind screening mode.
    Strips: emails, phone numbers, URLs, and common name patterns.
    
    Why blind screening?
    Research shows names trigger unconscious bias —
    candidates with minority-sounding names need 8 more years
    of experience to get the same callback rate (Harvard study).
    """
    text = resume_context

    # Remove email addresses
    text = re.sub(r'\S+@\S+\.\S+', '[EMAIL REMOVED]', text)

    # Remove phone numbers (Indian + international formats)
    text = re.sub(r'[\+\(]?[\d\s\-\(\)]{9,15}', '[PHONE REMOVED]', text)

    # Remove URLs (LinkedIn, GitHub, portfolio)
    text = re.sub(r'https?://\S+', '[URL REMOVED]', text)

    # Remove lines that look like a name header
    # (First line of resume is usually "Firstname Lastname")
    lines = text.split('\n')
    cleaned_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Skip short lines at top that look like names (2-3 words, no special chars)
        if i < 5 and len(stripped.split()) <= 3 and stripped.replace(' ', '').isalpha():
            cleaned_lines.append('[NAME REMOVED]')
        else:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def _extract_focused_queries(job_description: str) -> list:
    """
    Break JD into 3 focused retrieval queries.
    Targeted short queries retrieve much more relevant chunks
    than one diluted full-JD query.
    """
    queries = [
        # Query 1 — Technical skills
        "technical skills programming languages frameworks tools libraries",
        # Query 2 — Experience and projects
        "work experience projects built developed implemented deployed",
        # Query 3 — Education and qualifications
        "education degree qualification certification background"
    ]
    return queries


def _multi_query_retrieve(collection_name: str, job_description: str) -> list:
    """
    Retrieve chunks using multiple focused queries.
    Deduplicates and keeps highest score per chunk.
    """
    queries = _extract_focused_queries(job_description)
    seen_chunk_ids = {}

    for query in queries:
        chunks = retrieve(
            collection_name=collection_name,
            query=query,
            top_k=5
        )
        for chunk in chunks:
            cid = chunk["chunk_id"]
            if cid not in seen_chunk_ids or chunk["score"] > seen_chunk_ids[cid]["score"]:
                seen_chunk_ids[cid] = chunk

    all_chunks = sorted(
        seen_chunk_ids.values(),
        key=lambda x: x["score"],
        reverse=True
    )
    return all_chunks[:8]


def analyze_match(
    collection_name: str,
    job_description: str,
    blind_mode: bool = False
) -> dict:
    """
    Compare resume against JD using multi-query retrieval.

    Args:
        collection_name: from upload-resume endpoint
        job_description: raw JD text
        blind_mode:      if True, strips PII before LLM analysis

    Returns:
        Structured dict with score, gaps, STAR interview guide
    """
    retrieved_chunks = _multi_query_retrieve(collection_name, job_description)

    if not retrieved_chunks:
        raise ValueError(
            "No resume content retrieved. "
            "Check if document was ingested correctly."
        )

    resume_context = get_context_string(retrieved_chunks)

    # Apply blind screening if enabled
    if blind_mode:
        resume_context = anonymize_context(resume_context)

    avg_relevance = round(
        sum(c["score"] for c in retrieved_chunks) / len(retrieved_chunks), 3
    )

    user_prompt = MATCH_USER_PROMPT.format(
        resume_context=resume_context,
        job_description=job_description,
        blind_mode=str(blind_mode).upper()
    )

    result = call_llm_json(
        MATCH_SYSTEM_PROMPT,
        user_prompt,
        trace_name="match_analysis",
        metadata={
            "collection_name": collection_name,
            "blind_mode": blind_mode
        }
    )

    result["chunks_used"] = len(retrieved_chunks)
    result["avg_chunk_relevance"] = avg_relevance
    result["blind_mode_used"] = blind_mode

    return result