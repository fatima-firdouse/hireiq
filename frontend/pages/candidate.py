import streamlit as st
from components.utils import upload_resume, analyze_match
from components.charts import match_score_gauge, skills_gap_chart
from components.styles import CANDIDATE_CSS

st.markdown(CANDIDATE_CSS, unsafe_allow_html=True)

MAX_JD_CHARS = 1800

BIAS_IMPACT_DATA = {
    "gender": "Gender-biased JDs reduce female applicants by up to 40%",
    "age": "Age-biased language excludes 35% of experienced workforce",
    "race": "Name bias means minority candidates need 8 more years experience for same callback rate",
    "general": "Biased JDs reduce diverse applicant pool by up to 50%",
    "disability": "Unnecessary physical requirements exclude 15% of qualified candidates",
    "family_status": "Inflexible work language reduces applications from caregivers by 30%"
}


def _render_sidebar():
    resume_done = "collection_name" in st.session_state
    analysis_done = "last_analysis" in st.session_state
    active = 3 if analysis_done else (2 if resume_done else 1)
    progress_pct = {1: 12, 2: 52, 3: 100}.get(active, 12)

    steps = [
        ("1", "Upload Resume",        "PDF or DOCX, max 5MB"),
        ("2", "Paste Job Description", "The role you are applying for"),
        ("3", "View Analysis",         "Match score, gaps & interview prep"),
    ]

    def sc(idx):
        if idx < active: return "sd"
        if idx == active: return "sa"
        return ""

    rows = "".join(
        f'<div class="step-row {sc(i)}">'
        f'<div class="sc-w"><div class="sc {sc(i)}">{num}</div></div>'
        f'<div class="si"><div class="si-n {sc(i)}">{name}</div>'
        f'<div class="si-h {sc(i)}">{hint}</div></div></div>'
        for i, (num, name, hint) in enumerate(steps, 1)
    )

    with st.sidebar:
        st.markdown(f"""
        <div class="sb-header">
            <div class="sb-logo">
                <div class="sb-pill">🎯</div>
                <span class="sb-name">HireIQ</span>
            </div>
        </div>
        <div class="sb-role">🧑‍💼 Candidate Mode</div>
        <div class="prg-label">Your Progress</div>
        <div class="prg-wrap"><div class="prg-fill" style="width:{progress_pct}%"></div></div>
        {rows}
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        if st.button("🏠 Home", use_container_width=True, key="c_home"):
            st.session_state["role"] = None
            st.rerun()

        if resume_done:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("🔄 Start Over", use_container_width=True, key="c_reset"):
                for k in ["collection_name", "filename", "last_analysis"]:
                    st.session_state.pop(k, None)
                st.rerun()


def show():
    _render_sidebar()

    st.title("🎯 Candidate — Resume Analyzer")
    st.markdown(
        "<p style='font-size:16px;color:rgba(255,255,255,0.70);margin-bottom:8px'>"
        "Upload your resume · Paste a job description · Get your <strong>match score</strong>, "
        "skill gaps, and STAR interview prep."
        "</p>", unsafe_allow_html=True
    )

    # ── Step 1 ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<span class="section-badge">Step 1</span>', unsafe_allow_html=True)
    st.subheader("Upload Your Resume")

    uploaded_file = st.file_uploader(
        "Choose your resume (PDF or DOCX, max 5 MB)",
        type=["pdf", "docx"],
        help="PDF or DOCX format. Max 5MB."
    )

    if uploaded_file:
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if file_size_mb > 5:
            st.error(f"File too large ({file_size_mb:.1f} MB). Please keep it under 5 MB.")
            return

        st.markdown(
            f'<div class="fc"><div class="fc-icon">📄</div>'
            f'<div><div class="fc-name">{uploaded_file.name}</div>'
            f'<div class="fc-size">{file_size_mb:.2f} MB</div></div></div>',
            unsafe_allow_html=True
        )

        if st.button("📤 Upload & Process Resume", type="primary"):
            with st.spinner("Extracting text · Generating embeddings · Storing in vector DB…"):
                result = upload_resume(uploaded_file)

            if result["success"]:
                st.session_state["collection_name"] = result["data"]["collection_name"]
                st.session_state["filename"] = uploaded_file.name
                st.success("✅ Resume processed successfully!")
                st.rerun()
            else:
                st.error(f"Upload failed: {result['error']}")

    # ── Step 2 ─────────────────────────────────────────────
    if "collection_name" in st.session_state:
        st.markdown("---")
        st.markdown('<span class="section-badge">Step 2</span>', unsafe_allow_html=True)
        st.subheader("Paste Job Description")
        st.caption(f"Resume loaded: **{st.session_state.get('filename', '')}**")

        job_description = st.text_area(
            "Job Description",
            height=240,
            placeholder="Paste the full job description here…",
            help="Minimum 50 characters. Longer JDs will be auto-trimmed to stay within the AI token limit.",
            key="jd_input"
        )

        col_opt1, col_opt2 = st.columns([1, 2])
        with col_opt1:
            blind_mode = st.toggle(
                "🔒 Blind Screening Mode",
                value=False,
                help="Strips name, email, phone, and URLs before analysis."
            )
        with col_opt2:
            if blind_mode:
                st.info("🔒 **Blind mode ON** — PII stripped. Scoring based on skills only.")

        if st.button("🔍 Analyze Match", type="primary"):
            jd = job_description.strip()
            if len(jd) < 50:
                st.warning("Please paste a complete job description (minimum 50 characters).")
            else:
                # Silently trim to avoid 413 token errors — no warning shown
                jd_to_send = jd[:MAX_JD_CHARS]
                with st.spinner("Retrieving resume sections · Analyzing with AI…"):
                    result = analyze_match(
                        st.session_state["collection_name"],
                        jd_to_send,
                        blind_mode=blind_mode
                    )

                if result["success"]:
                    st.session_state["last_analysis"] = result["data"]
                    _display_match_results(result["data"])
                else:
                    err = str(result["error"])
                    if "413" in err or "tokens" in err.lower() or "rate_limit" in err.lower():
                        st.error(
                            "⚠️ AI token limit exceeded. Try a shorter job description "
                            "(under 1 500 characters) and click Analyze again."
                        )
                    else:
                        st.error(f"Analysis failed: {err}")


def _display_match_results(data: dict):
    st.markdown("---")
    st.markdown('<span class="section-badge">Analysis Results</span>', unsafe_allow_html=True)

    if data.get("blind_mode_used"):
        st.info("🔒 Blind Screening Mode — PII excluded from analysis.")

    # Score + Quick Summary
    col1, col2 = st.columns([1, 1])
    with col1:
        score = data.get("match_score", 0)
        fig = match_score_gauge(score)
        st.plotly_chart(fig, use_container_width=True, key="gauge")
    with col2:
        st.markdown(
            '<span class="grad-heading">Quick Summary</span>',
            unsafe_allow_html=True
        )
        st.markdown(data.get("score_reasoning", ""))
        matched = data.get("matched_skills", [])
        missing = data.get("missing_skills", [])
        c1, c2, c3 = st.columns(3)
        c1.metric("Skills Matched", len(matched))
        c2.metric("Skills Missing", len(missing))
        c3.metric("Relevance", f"{data.get('avg_chunk_relevance', 0):.2f}")

    # Skills gap chart
    if matched or missing:
        st.markdown("---")
        fig2 = skills_gap_chart(matched, missing)
        st.plotly_chart(fig2, use_container_width=True, key="skills_gap")

    # Experience + Education
    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<span class="grad-heading-green">💼 Experience Match</span>', unsafe_allow_html=True)
        exp = data.get("experience_match", {})
        st.markdown(f'<div class="c-card-green"><p><strong>Required:</strong> {exp.get("required","N/A")}</p><p><strong>You have:</strong> {exp.get("candidate_has","N/A")}</p></div>', unsafe_allow_html=True)
        gap = exp.get("gap", "None")
        if gap and gap.lower() != "none":
            st.warning(f"**Gap:** {gap}")
        else:
            st.success("✅ No experience gap")

    with col4:
        st.markdown('<span class="grad-heading-green">🎓 Education Match</span>', unsafe_allow_html=True)
        edu = data.get("education_match", {})
        st.markdown(f'<div class="c-card-green"><p><strong>Required:</strong> {edu.get("required","N/A")}</p><p><strong>You have:</strong> {edu.get("candidate_has","N/A")}</p></div>', unsafe_allow_html=True)
        gap = edu.get("gap", "None")
        if gap and gap.lower() != "none":
            st.warning(f"**Gap:** {gap}")
        else:
            st.success("✅ No education gap")

    # Improvement Suggestions
    suggestions = data.get("improvement_suggestions", [])
    if suggestions:
        st.markdown("---")
        st.markdown('<span class="grad-heading-gold">💡 Resume Improvement Suggestions</span>', unsafe_allow_html=True)
        for i, s in enumerate(suggestions, 1):
            st.markdown(
                f'<div class="ic"><div class="ic-i">💡</div><div class="ic-t"><strong>{i}.</strong> {s}</div></div>',
                unsafe_allow_html=True
            )

    # STAR Interview Guide
    questions = data.get("interview_guide", [])
    if questions:
        st.markdown("---")
        st.markdown('<span class="grad-heading">🎤 STAR Interview Preparation Guide</span>', unsafe_allow_html=True)
        st.caption("Generated from your skill gaps · STAR = **S**ituation · **T**ask · **A**ction · **R**esult")

        with st.expander("📖 How to use STAR format"):
            st.markdown("""
**S — Situation:** Set the context. *"I was working on a project where…"*  
**T — Task:** Your responsibility. *"My task was to…"*  
**A — Action:** What YOU did. *"I implemented… I led…"*  
**R — Result:** Measurable outcome. *"Reduced by X% · delivered in Y days…"*
            """)

        for i, q in enumerate(questions, 1):
            diff = q.get("difficulty", "medium")
            badge = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}.get(diff, "🟡")
            with st.expander(f"{badge} Q{i}: {q.get('question','')}"):
                ca, cb = st.columns(2)
                with ca:
                    st.markdown(f"**Topic:** {q.get('topic','General')}")
                    st.markdown(f"**Difficulty:** {diff.capitalize()}")
                    st.markdown(f"**Format:** {q.get('format','STAR')}")
                with cb:
                    if q.get("what_to_look_for"):
                        st.markdown("**✅ Strong answer includes:**")
                        st.success(q["what_to_look_for"])
                    if q.get("red_flags"):
                        st.markdown("**🚩 Red flags to avoid:**")
                        st.error(q["red_flags"])