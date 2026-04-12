# intelligence/jd_rewriter.py
# Split into TWO LLM calls to avoid truncation:
# Call 1 → rewritten JD text only
# Call 2 → changes + highlights only

from core.llm_client import call_llm, call_llm_json
from intelligence.bias_detector import detect_bias
from intelligence.jd_analyzer import analyze_jd


def rewrite_jd(job_description: str) -> dict:
    """
    Rewrite JD using 4 total LLM calls:
    1. detect_bias()
    2. analyze_jd()
    3. rewrite the JD text only
    4. generate changes + highlights only
    """
    # Step 1 & 2: Gather issues
    bias_report = detect_bias(job_description)
    quality_report = analyze_jd(job_description)

    # Build issues summary
    issues_parts = []

    bias_instances = bias_report.get("bias_instances", [])
    if bias_instances:
        issues_parts.append("BIAS ISSUES:")
        for b in bias_instances[:5]:
            issues_parts.append(
                f"  - '{b['text']}' ({b['bias_type']}): replace with '{b['suggested_replacement']}'"
            )

    vague_terms = quality_report.get("vague_terms", [])
    if vague_terms:
        issues_parts.append("VAGUE LANGUAGE:")
        for v in vague_terms[:5]:
            issues_parts.append(f"  - '{v['term']}': {v['fix']}")

    missing_info = quality_report.get("missing_information", [])
    if missing_info:
        issues_parts.append("MISSING INFO:")
        for m in missing_info:
            issues_parts.append(f"  - Add {m['field']}: {m['suggestion']}")

    issues_summary = "\n".join(issues_parts) if issues_parts else "No major issues."

    # Step 3: Get ONLY the rewritten JD text — no JSON, plain text
    rewrite_system = """
You are an expert technical writer specializing in inclusive job descriptions.
Rewrite the given job description to be bias-free, clear, and inclusive.
Rules:
- Remove all biased language identified in the issues
- Replace vague terms with specific language
- Add placeholders [SALARY_RANGE], [LOCATION], [WORK_MODE] where missing
- Use gender-neutral language
- Keep it under 500 words
- Return ONLY the rewritten JD text — no JSON, no explanation, no markdown
"""

    rewrite_user = f"""
ORIGINAL JD:
{job_description}

ISSUES TO FIX:
{issues_summary}

Write the improved JD now (plain text only, no JSON):
"""

    rewritten_text = call_llm(
        system_prompt=rewrite_system,
        user_prompt=rewrite_user,
        temperature=0.2,
        trace_name="jd_rewrite_text"
    )

    # Step 4: Get changes + highlights as JSON — separate call, small output
    analysis_system = """
You are an expert HR consultant.
Compare an original and rewritten job description.
Return ONLY valid JSON — no explanation, no markdown, no extra text.
"""

    analysis_user = f"""
ORIGINAL JD:
{job_description[:1000]}

REWRITTEN JD:
{rewritten_text[:1000]}

ISSUES FIXED:
{issues_summary}

Return this exact JSON (keep all text SHORT — max 10 words per field):

{{
  "changes_made": [
    {{
      "original": "<short original phrase>",
      "replacement": "<short new phrase>",
      "reason": "<one sentence>"
    }}
  ],
  "improvement_highlights": [
    "<highlight 1 — one sentence>",
    "<highlight 2 — one sentence>",
    "<highlight 3 — one sentence>"
  ]
}}

Maximum 5 changes_made entries. Return ONLY the JSON.
"""

    analysis_result = call_llm_json(
        system_prompt=analysis_system,
        user_prompt=analysis_user,
        trace_name="jd_rewrite_analysis"
    )

    # Combine everything
    return {
        "rewritten_jd": rewritten_text.strip(),
        "changes_made": analysis_result.get("changes_made", []),
        "improvement_highlights": analysis_result.get("improvement_highlights", []),
        "bias_report": bias_report,
        "quality_report": quality_report
    }