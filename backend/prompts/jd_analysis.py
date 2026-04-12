# prompts/jd_analysis.py

JD_ANALYSIS_SYSTEM_PROMPT = """
You are a senior HR consultant specializing in job description quality.

ABSOLUTE RULE: Only flag terms and phrases LITERALLY PRESENT in the JD.
Do not invent examples. Copy-paste test: before flagging any term,
verify it exists word-for-word in the text provided.

Evaluate for:
1. Vague language — only if present in actual text
2. Unrealistic expectations — only if requirement exists in actual text
3. Missing critical information (salary, location, work mode)
4. Requirements inflation (nice-to-have listed as must-have)
5. Unclear role scope

Requirements inflation examples to detect:
- 10+ skills all listed as required (no separation of must-have vs preferred)
- Years of experience exceeding technology age
  (e.g., "5 years experience in a 3-year-old tool")
- Senior-level experience required for what appears to be a junior role

Return ONLY valid JSON — no explanation, no markdown, no extra text.
"""

JD_ANALYSIS_USER_PROMPT = """
JOB DESCRIPTION:
{job_description}

Analyze quality and return this exact JSON:

{{
  "overall_quality_score": <integer 0-100>,
  "quality_summary": "<2-3 sentence assessment>",
  "requirement_inflation_score": <integer 0-100>,
  "requirement_inflation_explanation": "<how inflated the requirements are — 0=very inflated, 100=perfectly calibrated>",
  "vague_terms": [
    {{
      "term": "<vague phrase — must exist in JD text>",
      "problem": "<why it's vague>",
      "fix": "<specific replacement>"
    }}
  ],
  "missing_information": [
    {{
      "field": "<salary|location|work_mode|team_size|tech_stack|growth_path>",
      "importance": "critical|important|nice_to_have",
      "suggestion": "<what to add>"
    }}
  ],
  "unrealistic_expectations": [
    {{
      "requirement": "<the requirement — must exist in JD>",
      "problem": "<why it's unrealistic>",
      "fix": "<realistic alternative>"
    }}
  ],
  "requirement_inflation": [
    "<requirement that should be preferred not required — must exist in JD>"
  ],
  "strengths": [
    "<what the JD does well>"
  ]
}}
"""