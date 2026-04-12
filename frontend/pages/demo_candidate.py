"""
pages/demo_candidate.py
Candidate demo page — Fatima Firdouse vs Cami.AI Data Engineering Trainee
All results are pre-computed mock data. No API calls.
"""
import streamlit as st
from components.styles import CANDIDATE_CSS

st.markdown(CANDIDATE_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# MOCK DATA
# ─────────────────────────────────────────────────────────────────
RESUME = {
    "name":       "Fatima Firdouse",
    "title":      "B.Tech AI & Data Science · Final Year",
    "summary":    "ML engineer with deployed projects: RAG pipeline (AWS EC2), Resume Analyzer (Flask + TF-IDF), and BCG Forage churn model (500k+ records, Random Forest).",
    "top_skills": ["Python", "Machine Learning", "LangChain", "RAG", "FastAPI", "Streamlit", "AWS EC2", "SQL", "Flask", "ChromaDB"],
}

JD = {
    "role":    "Data Engineering Trainee",
    "company": "Cami.AI",
    "location":"Kochi, India · Fast-growing SaaS",
    "stack":   ["Python", "AWS Sagemaker", "AWS Glue", "Node.js", "Delta Lake", "Spark"],
    "summary": "Build reusable data integrations, write ML workers, collaborate with engineering team on scalable microservices.",
}

RESULTS = {
    "score":   62,
    "matched": ["Python", "OOP", "REST APIs", "AWS", "SQL", "Pandas", "Git", "Flask", "Microservices"],
    "missing": ["AWS Sagemaker", "AWS Glue", "Node.js", "Apache Spark", "Delta Lake"],
    "exp": "0–1 yr preferred · BCG simulation + 3 deployed projects ✓",
    "edu": "B.Tech CS/related required · B.Tech AI & Data Science ✓",
    "suggestions": [
        "Highlight your ETL pipeline from BCG explicitly — Cami.AI specifically wants data integration experience.",
        "Mention your Flask REST API deployment prominently — it directly maps to their microservices requirement.",
        "Add a small Spark or AWS Glue project to close the biggest technical gap on your resume.",
    ],
    "questions": [
        {"q": "Describe a time you built or automated a data pipeline. What was the scale and what did you optimize for?",
         "topic": "Data Engineering", "diff": "medium"},
        {"q": "Tell me about a REST API or integration you built. How did you handle errors and edge cases?",
         "topic": "API Development", "diff": "medium"},
        {"q": "How do you approach learning a new technology quickly when a project requires it?",
         "topic": "Learning Agility", "diff": "easy"},
    ],
    "jd_bias":    "🟢 Low Bias",
    "jd_quality": 74,
}

DIFF_COLOR = {"easy": ("#6EE7B7", "rgba(46,204,113,0.14)", "rgba(46,204,113,0.45)"),
              "medium": ("#FDE68A", "rgba(243,156,18,0.14)", "rgba(243,156,18,0.45)"),
              "hard": ("#FCA5A5", "rgba(231,76,60,0.14)", "rgba(231,76,60,0.45)")}


# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
def _sidebar():
    steps = [
        ("✓", "Resume Loaded",    "Fatima Firdouse · AI Engineer"),
        ("✓", "JD Matched",       "Data Engineering Trainee · Cami.AI"),
        ("✓", "Analysis Complete","62% match · 5 gaps found"),
    ]
    rows = "".join(
        f'<div class="step-row sd">'
        f'<div class="sc-w"><div class="sc sd">{n}</div></div>'
        f'<div class="si"><div class="si-n sd">{name}</div>'
        f'<div class="si-h sd">{hint}</div></div></div>'
        for n, name, hint in steps
    )
    with st.sidebar:
        st.markdown(f"""
        <div class="sb-header">
          <div class="sb-logo">
            <div class="sb-pill">✨</div>
            <span class="sb-name">HireIQ</span>
          </div>
        </div>
        <div class="sb-role" style="color:rgba(244,165,186,0.85)!important;">🎯 Candidate Demo</div>
        <div class="prg-label">Demo Progress</div>
        <div class="prg-wrap"><div class="prg-fill" style="width:100%"></div></div>
        {rows}
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True, key="dc_home"):
            st.session_state.update({"role": None, "demo_step": None}); st.rerun()
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("📄 Try with My Resume", use_container_width=True, key="dc_real"):
            st.session_state.update({"role": "candidate", "demo_step": None}); st.rerun()


# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def _tag(text, color, bg, border):
    return (f"<span style='display:inline-block;margin:4px;padding:7px 16px;"
            f"border-radius:100px;font-size:13px;font-weight:700;"
            f"color:{color};background:{bg};border:1.5px solid {border};"
            f"box-shadow:0 0 10px {bg};'>{text}</span>")

def _mini_label(text):
    return (f"<p style='font-size:11px;font-weight:700;color:rgba(255,255,255,0.36);"
            f"text-transform:uppercase;letter-spacing:1px;margin-bottom:9px;'>{text}</p>")

def _section_divider(step_num, title, icon):
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:14px;margin:28px 0 18px;'>
      <div style='width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#DA7B93,#8B2252);
        display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:900;color:white;
        box-shadow:0 0 14px rgba(218,123,147,0.50);flex-shrink:0;'>{step_num}</div>
      <div style='font-size:18px;font-weight:800;background:linear-gradient(90deg,#F4A5BA,#DA7B93);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>{icon} {title}</div>
      <div style='flex:1;height:1px;background:linear-gradient(90deg,rgba(218,123,147,0.30),transparent);'></div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
def show():
    _sidebar()

    # Demo banner
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(218,123,147,0.15),rgba(139,34,82,0.10));
      border:1.5px solid rgba(218,123,147,0.40);border-radius:14px;
      padding:12px 22px;margin-bottom:24px;display:flex;align-items:center;gap:12px;'>
      <span style='font-size:18px;'>✨</span>
      <div>
        <span style='font-size:13px;font-weight:800;color:#F4A5BA;'>Demo Mode</span>
        <span style='font-size:13px;color:rgba(255,255,255,0.50);margin-left:10px;'>
          Fatima Firdouse resume · Cami.AI Data Engineering Trainee JD · All results are pre-computed samples
        </span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.title("🎯 Candidate — Resume Analysis Demo")

    # ── STEP 1: Resume + JD Preview ─────────────────────────────
    _section_divider("1", "Sample Inputs", "📋")

    col_r, col_j = st.columns(2, gap="medium")

    with col_r:
        st.markdown(f"""
        <div style='background:rgba(218,123,147,0.08);border:1.5px solid rgba(218,123,147,0.38);
          border-radius:18px;padding:22px;box-shadow:0 8px 28px rgba(0,0,0,0.40);height:100%;'>
          <div style='font-size:11px;font-weight:700;color:rgba(255,255,255,0.36);text-transform:uppercase;
            letter-spacing:1px;margin-bottom:14px;'>📄 Resume</div>
          <div style='font-size:18px;font-weight:800;color:white;margin-bottom:4px;'>{RESUME["name"]}</div>
          <div style='font-size:13px;color:rgba(244,165,186,0.80);margin-bottom:14px;'>{RESUME["title"]}</div>
          <div style='font-size:14px;color:rgba(255,255,255,0.68);line-height:1.7;margin-bottom:16px;'>{RESUME["summary"]}</div>
          <div style='display:flex;flex-wrap:wrap;gap:6px;'>
            {"".join(f'<span style="font-size:12px;font-weight:600;color:#F4A5BA;background:rgba(218,123,147,0.12);padding:4px 12px;border-radius:100px;border:1px solid rgba(218,123,147,0.30);">{s}</span>' for s in RESUME["top_skills"])}
          </div>
        </div>""", unsafe_allow_html=True)

    with col_j:
        st.markdown(f"""
        <div style='background:rgba(58,191,208,0.06);border:1.5px solid rgba(58,191,208,0.32);
          border-radius:18px;padding:22px;box-shadow:0 8px 28px rgba(0,0,0,0.40);height:100%;'>
          <div style='font-size:11px;font-weight:700;color:rgba(255,255,255,0.36);text-transform:uppercase;
            letter-spacing:1px;margin-bottom:14px;'>💼 Job Description</div>
          <div style='font-size:18px;font-weight:800;color:white;margin-bottom:4px;'>{JD["role"]}</div>
          <div style='font-size:13px;color:rgba(126,221,232,0.80);margin-bottom:6px;'>{JD["company"]}</div>
          <div style='font-size:13px;color:rgba(255,255,255,0.45);margin-bottom:14px;'>{JD["location"]}</div>
          <div style='font-size:14px;color:rgba(255,255,255,0.68);line-height:1.7;margin-bottom:16px;'>{JD["summary"]}</div>
          <div style='display:flex;flex-wrap:wrap;gap:6px;'>
            {"".join(f'<span style="font-size:12px;font-weight:600;color:#7EDDE8;background:rgba(58,191,208,0.10);padding:4px 12px;border-radius:100px;border:1px solid rgba(58,191,208,0.28);">{s}</span>' for s in JD["stack"])}
          </div>
        </div>""", unsafe_allow_html=True)

    # ── STEP 2: Match Score ──────────────────────────────────────
    _section_divider("2", "Match Analysis", "📊")

    score = RESULTS["score"]
    s_color = "#6EE7B7" if score >= 70 else "#FDE68A" if score >= 50 else "#FCA5A5"

    st.markdown(
        f"<div style='display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px;'>"
        f"<span style='font-size:16px;font-weight:700;color:rgba(255,255,255,0.72);'>Resume Match Score</span>"
        f"<span style='font-size:42px;font-weight:900;color:{s_color};"
        f"text-shadow:0 0 22px {s_color}88;'>{score}%</span></div>",
        unsafe_allow_html=True
    )
    st.progress(score / 100)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("✅ Skills Matched", len(RESULTS["matched"]))
    m2.metric("❌ Skills Missing", len(RESULTS["missing"]))
    m3.metric("📊 Overall Fit",    f"{score}%")

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # Skills
    col_m, col_n = st.columns(2, gap="medium")
    with col_m:
        st.markdown(_mini_label("✅ Matched Skills"), unsafe_allow_html=True)
        tags = "".join(_tag(f"✓ {s}", "#6EE7B7", "rgba(46,204,113,0.12)", "rgba(46,204,113,0.50)")
                       for s in RESULTS["matched"])
        st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)
    with col_n:
        st.markdown(_mini_label("❌ Skills to Add"), unsafe_allow_html=True)
        tags = "".join(_tag(f"✗ {s}", "#FCA5A5", "rgba(231,76,60,0.10)", "rgba(231,76,60,0.45)")
                       for s in RESULTS["missing"])
        st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # Experience + Education
    e1, e2 = st.columns(2, gap="medium")
    for col, icon, label, val in [
        (e1, "💼", "Experience Match", RESULTS["exp"]),
        (e2, "🎓", "Education Match",  RESULTS["edu"]),
    ]:
        with col:
            st.markdown(
                f"<div style='background:rgba(255,255,255,0.04);border:1.5px solid rgba(255,255,255,0.09);"
                f"border-radius:14px;padding:16px 18px;'>"
                f"<div style='font-size:11px;font-weight:700;color:rgba(255,255,255,0.34);"
                f"text-transform:uppercase;letter-spacing:0.8px;margin-bottom:6px;'>{icon} {label}</div>"
                f"<div style='font-size:14px;color:rgba(255,255,255,0.82);line-height:1.6;'>{val}</div>"
                f"</div>", unsafe_allow_html=True
            )

    # ── STEP 3: Improvement Suggestions ─────────────────────────
    _section_divider("3", "Resume Improvements", "💡")

    for i, s in enumerate(RESULTS["suggestions"], 1):
        st.markdown(
            f"<div style='background:rgba(243,156,18,0.08);border:1.5px solid rgba(243,156,18,0.35);"
            f"border-radius:14px;padding:15px 20px;margin-bottom:10px;"
            f"display:flex;gap:13px;align-items:flex-start;'>"
            f"<span style='font-size:18px;flex-shrink:0;'>💡</span>"
            f"<div><strong style='color:#FDE68A;'>{i}.</strong> "
            f"<span style='font-size:15px;color:rgba(255,255,255,0.85);line-height:1.7;'>{s}</span></div>"
            f"</div>", unsafe_allow_html=True
        )

    # ── STEP 4: STAR Interview Questions ────────────────────────
    _section_divider("4", "STAR Interview Prep", "🎤")
    st.markdown(
        "<p style='font-size:14px;color:rgba(255,255,255,0.50);margin-bottom:16px;'>"
        "Generated from your skill gaps · <strong>S</strong>ituation · "
        "<strong>T</strong>ask · <strong>A</strong>ction · <strong>R</strong>esult</p>",
        unsafe_allow_html=True
    )

    for i, q in enumerate(RESULTS["questions"], 1):
        tc, bg, border = DIFF_COLOR[q["diff"]]
        with st.expander(f"Q{i}: {q['q'][:72]}…"):
            st.markdown(
                f"<div style='display:flex;gap:9px;margin-bottom:12px;'>"
                f"<span style='padding:5px 14px;border-radius:100px;font-size:12px;font-weight:700;"
                f"color:{tc};background:{bg};border:1.5px solid {border};'>{q['diff'].capitalize()}</span>"
                f"<span style='padding:5px 14px;border-radius:100px;font-size:12px;font-weight:700;"
                f"color:#F4A5BA;background:rgba(218,123,147,0.12);border:1.5px solid rgba(218,123,147,0.35);'>"
                f"{q['topic']}</span></div>"
                f"<p style='font-size:15px;color:rgba(255,255,255,0.88);line-height:1.7;'>{q['q']}</p>",
                unsafe_allow_html=True
            )

    # ── STEP 5: JD Bias + Quality snapshot ──────────────────────
    _section_divider("5", "JD Quick Check", "🔍")
    bq1, bq2 = st.columns(2, gap="medium")
    with bq1:
        st.markdown(
            "<div style='background:rgba(46,204,113,0.08);border:1.5px solid rgba(46,204,113,0.40);"
            "border-radius:14px;padding:18px 22px;text-align:center;'>"
            "<div style='font-size:11px;font-weight:700;color:rgba(255,255,255,0.34);"
            "text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px;'>JD Bias Level</div>"
            "<div style='font-size:22px;font-weight:900;color:#6EE7B7;'>"
            + RESULTS["jd_bias"] + "</div></div>",
            unsafe_allow_html=True
        )
    with bq2:
        q = RESULTS["jd_quality"]
        st.markdown(
            f"<div style='background:rgba(255,255,255,0.04);border:1.5px solid rgba(255,255,255,0.09);"
            f"border-radius:14px;padding:18px 22px;text-align:center;'>"
            f"<div style='font-size:11px;font-weight:700;color:rgba(255,255,255,0.34);"
            f"text-transform:uppercase;letter-spacing:0.8px;margin-bottom:6px;'>JD Quality Score</div>"
            f"<div style='font-size:36px;font-weight:900;color:#7EDDE8;"
            f"text-shadow:0 0 18px rgba(58,191,208,0.55);'>{q}"
            f"<span style='font-size:16px;color:rgba(255,255,255,0.30);'>/100</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )

    # ── CTA ──────────────────────────────────────────────────────
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='background:rgba(218,123,147,0.06);border:1.5px solid rgba(218,123,147,0.28);"
        "border-radius:16px;padding:20px 24px;text-align:center;margin-top:8px;'>"
        "<div style='font-size:16px;font-weight:800;color:white;margin-bottom:6px;'>Ready to try with your own resume?</div>"
        "<div style='font-size:14px;color:rgba(255,255,255,0.45);'>Upload your PDF or DOCX and paste any job description.</div>"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    _, cc1, cc2, _ = st.columns([1, 1.2, 1.2, 1])
    with cc1:
        if st.button("📄 Analyze My Resume", use_container_width=True, type="primary", key="dc_go"):
            st.session_state.update({"role": "candidate", "demo_step": None}); st.rerun()
    with cc2:
        if st.button("🏠 Back to Home", use_container_width=True, key="dc_back"):
            st.session_state.update({"role": None, "demo_step": None}); st.rerun()

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)