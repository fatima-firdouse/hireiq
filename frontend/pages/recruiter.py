import streamlit as st
import plotly.graph_objects as go
from collections import Counter
from components.utils import detect_bias, analyze_jd, rewrite_jd
from components.charts import quality_score_bar
from components.styles import RECRUITER_CSS

st.markdown(RECRUITER_CSS, unsafe_allow_html=True)

BIAS_IMPACT_DATA = {
    "gender":        "📊 Gender-biased JDs reduce female applicants by up to 40% (Harvard Business Review)",
    "age":           "📊 Age-biased language excludes 35% of experienced workforce candidates",
    "race":          "📊 Name bias: minority candidates need 8 more years experience for same callback rate (U of Chicago)",
    "disability":    "📊 Unnecessary physical requirements exclude 15% of qualified candidates",
    "family_status": "📊 Inflexible work language reduces applications from caregivers by 30%",
    "general":       "📊 Biased JDs reduce diverse applicant pool by up to 50%"
}


def _render_sidebar(active: int = 1):
    progress_pct = {1: 10, 2: 42, 3: 72, 4: 100}.get(active, 10)
    steps = [
        ("1", "Paste Job Description", "Minimum 50 characters"),
        ("2", "Detect Bias",           "Identify biased language"),
        ("3", "Analyze Quality",       "Review JD completeness"),
        ("4", "Full Rewrite",          "AI-improved inclusive JD"),
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
                <div class="sb-pill">🏢</div>
                <span class="sb-name">HireIQ</span>
            </div>
        </div>
        <div class="sb-role">👔 Recruiter Mode</div>
        <div class="prg-label">Workflow Progress</div>
        <div class="prg-wrap"><div class="prg-fill" style="width:{progress_pct}%"></div></div>
        {rows}
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True, key="r_home"):
            st.session_state["role"] = None
            st.rerun()


def show():
    if "recruiter_step" not in st.session_state:
        st.session_state["recruiter_step"] = 1
    _render_sidebar(active=st.session_state["recruiter_step"])

    st.title("🏢 Recruiter — JD Intelligence Tool")
    st.markdown(
        "<p style='font-size:16px;color:rgba(255,255,255,0.70);margin-bottom:8px'>"
        "Analyze job descriptions for <strong>bias</strong>, <strong>quality issues</strong>, "
        "and get an AI-powered inclusive rewrite."
        "</p>", unsafe_allow_html=True
    )

    # JD input — always shown
    st.markdown("---")
    st.markdown('<span class="section-badge">Step 1 — Paste Your JD</span>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description",
        height=280,
        placeholder="Paste your full job description here…",
        help="Minimum 50 characters.",
        key="recruiter_jd"
    )

    jd_len = len(job_description.strip())
    if jd_len > 0:
        st.caption(f"📝 {jd_len} characters")

    # Buttons — always visible
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        run_bias    = st.button("🔍 Detect Bias",    use_container_width=True, key="btn_bias")
    with col2:
        run_quality = st.button("📋 Analyze Quality", use_container_width=True, key="btn_quality")
    with col3:
        run_rewrite = st.button("✍️ Full Rewrite",   use_container_width=True, type="primary", key="btn_rewrite")

    # Validate on click
    if (run_bias or run_quality or run_rewrite) and jd_len < 50:
        st.warning("⚠️ Please paste a complete job description (minimum 50 characters).")
        return

    if run_bias:
        st.session_state["recruiter_step"] = 2
        with st.spinner("Scanning for biased language…"):
            result = detect_bias(job_description)
        if result["success"]:
            _display_bias_results(result["data"])
        else:
            st.error(f"Bias detection failed: {result['error']}")

    if run_quality:
        st.session_state["recruiter_step"] = 3
        with st.spinner("Analyzing JD quality…"):
            result = analyze_jd(job_description)
        if result["success"]:
            _display_quality_results(result["data"])
        else:
            st.error(f"Quality analysis failed: {result['error']}")

    # Full rewrite — only shows summary badges + rewrite output (NOT full bias/quality)
    if run_rewrite:
        st.session_state["recruiter_step"] = 4
        with st.spinner("Running bias + quality analysis + AI rewrite (3 calls — ~30 s)…"):
            result = rewrite_jd(job_description)
        if result["success"]:
            _display_rewrite_summary(result["data"])
            _display_rewrite_results(result["data"])
        else:
            st.error(f"Rewrite failed: {result['error']}")


# ─────────────────────────────────────────────────────────────────
def _display_bias_results(data: dict):
    st.markdown("---")
    st.markdown('<span class="section-badge">🔍 Bias Detection Report</span>', unsafe_allow_html=True)

    level = data.get("overall_bias_level", "unknown")
    badge_map = {"low": ("🟢 Low Bias", "success"), "medium": ("🟡 Medium Bias", "warning"), "high": ("🔴 High Bias", "error")}
    badge_text, badge_type = badge_map.get(level, ("❓ Unknown", "info"))
    getattr(st, badge_type)(badge_text)

    c1, c2 = st.columns(2)
    c1.metric("Inclusivity Score", f"{data.get('inclusivity_score', 0)}/100")
    instances = data.get("bias_instances", [])
    c2.metric("Bias Instances", len(instances))

    if data.get("bias_summary"):
        st.markdown(
            f'<div class="r-card"><p>{data["bias_summary"]}</p></div>',
            unsafe_allow_html=True
        )

    # Affinity bias
    affinity = data.get("affinity_bias_risk", {})
    if affinity.get("detected"):
        st.markdown("---")
        st.markdown('<span class="grad-heading-purple">🤝 Affinity Bias Risk</span>', unsafe_allow_html=True)
        st.markdown('<div class="r-card-purple">', unsafe_allow_html=True)
        st.warning("Affinity bias causes recruiters to favour candidates similar to the existing team, reducing diversity.")
        if affinity.get("phrases"):
            phr = "` `".join(affinity["phrases"])
            st.markdown(f"**Phrases found:** `{phr}`")
        if affinity.get("explanation"):
            st.markdown(f"**Impact:** {affinity['explanation']}")
        if affinity.get("fix"):
            st.success(f"**Fix:** {affinity['fix']}")
        st.markdown('</div>', unsafe_allow_html=True)

    # CSS horizontal bar chart — no plotly, always renders
    if instances:
        st.markdown("---")
        st.markdown('<span class="grad-heading-red">📊 Bias Breakdown</span>', unsafe_allow_html=True)
        _counts = Counter(b.get("bias_type", "general") for b in instances)
        _total  = sum(_counts.values()) or 1
        _PALETTE = {
            "gender": "#E74C3C", "age": "#F39C12", "race": "#9B59B6",
            "disability": "#3ABFD0", "family_status": "#2ECC71", "general": "#DA7B93",
        }
        _rows = ""
        for _label, _cnt in sorted(_counts.items(), key=lambda x: -x[1]):
            _pct   = round((_cnt / _total) * 100)
            _color = _PALETTE.get(_label, "#7EDDE8")
            _rows += (
                f'<div style="margin-bottom:14px;">'
                f'<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
                f'<span style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.82);">'
                f'{_label.replace("_"," ").title()}</span>'
                f'<span style="font-size:13px;font-weight:800;color:{_color};">'
                f'{_cnt} instance{"s" if _cnt>1 else ""} &nbsp;·&nbsp; {_pct}%</span>'
                f'</div>'
                f'<div style="background:rgba(255,255,255,0.07);border-radius:100px;height:10px;">'
                f'<div style="width:{_pct}%;height:10px;border-radius:100px;'
                f'background:{_color};box-shadow:0 0 12px {_color}70;"></div>'
                f'</div></div>'
            )
        st.markdown(
            f'<div style="background:rgba(5,15,25,0.65);border:1.5px solid rgba(58,191,208,0.28);'
            f'border-radius:16px;padding:22px 26px;margin-bottom:8px;">'
            f'<div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.34);'
            f'text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;">Breakdown by Bias Type</div>'
            f'{_rows}</div>',
            unsafe_allow_html=True
        )

        st.markdown('<span class="grad-heading-red">Bias Instances — Details</span>', unsafe_allow_html=True)
        for b in instances:
            btype = b.get("bias_type", "general")
            impact = BIAS_IMPACT_DATA.get(btype, BIAS_IMPACT_DATA["general"])
            with st.expander(f"❌ `{b.get('text','')}` — {btype}"):
                st.markdown(
                    f'<span class="bias-tag">🚩 {b.get("text","")}</span>'
                    f'<span class="fix-tag">✅ {b.get("suggested_replacement","")}</span>',
                    unsafe_allow_html=True
                )
                st.markdown(f"**Why it's biased:** {b.get('explanation','')}")
                st.info(f"**Research says:** {impact}")
                if b.get("business_impact"):
                    st.warning(f"**Business impact:** {b['business_impact']}")

    # Quick wins
    quick_wins = data.get("quick_wins", [])
    if quick_wins:
        st.markdown("---")
        st.markdown('<span class="grad-heading-green">⚡ Quick Wins</span>', unsafe_allow_html=True)
        for w in quick_wins:
            st.markdown(f'<div class="quick-win">⚡ {w}</div>', unsafe_allow_html=True)

    # Masculine-coded words
    masc = data.get("masculine_coded_words", [])
    if masc:
        st.markdown("---")
        st.markdown('<span class="grad-heading-purple">⚧ Masculine-Coded Words</span>', unsafe_allow_html=True)
        tags = "".join(f'<span class="masc-word-tag">{w}</span>' for w in masc)
        st.markdown(f'<div class="r-card-purple">{tags}<p style="margin-top:14px;font-size:13px;color:rgba(255,255,255,0.60)">Masculine-coded language reduces female applications by up to 40%.</p></div>', unsafe_allow_html=True)


def _display_quality_results(data: dict):
    st.markdown("---")
    st.markdown('<span class="section-badge">📋 JD Quality Report</span>', unsafe_allow_html=True)

    score = data.get("overall_quality_score", 0)
    try:
        fig = quality_score_bar(score)
        if fig is None:
            raise ValueError("None")
        st.plotly_chart(fig, use_container_width=True, key="quality_bar")
    except Exception:
        color = "#2ECC71" if score >= 70 else "#F39C12" if score >= 40 else "#E74C3C"
        st.markdown(
            f'<div class="r-card" style="text-align:center">'
            f'<div style="font-size:52px;font-weight:900;color:{color};text-shadow:0 0 20px {color}88">{score}</div>'
            f'<div style="font-size:14px;color:rgba(255,255,255,0.55);text-transform:uppercase;letter-spacing:1px">Overall Quality Score / 100</div>'
            f'</div>', unsafe_allow_html=True
        )

    if data.get("quality_summary"):
        st.markdown(f'<div class="r-card"><p>{data["quality_summary"]}</p></div>', unsafe_allow_html=True)

    # Requirement inflation score
    inf_score = data.get("requirement_inflation_score")
    if inf_score is not None:
        st.markdown("---")
        st.markdown('<span class="grad-heading-gold">📈 Requirements Inflation Score</span>', unsafe_allow_html=True)
        ci1, ci2 = st.columns([1, 2])
        with ci1:
            icon = "🔴" if inf_score < 40 else "🟡" if inf_score < 70 else "🟢"
            st.metric("Calibration Score", f"{icon} {inf_score}/100")
            st.caption("100 = perfectly calibrated · 0 = massively inflated")
        with ci2:
            expl = data.get("requirement_inflation_explanation", "")
            if expl:
                if inf_score < 40:   st.error(f"⚠️ {expl}")
                elif inf_score < 70: st.warning(f"⚠️ {expl}")
                else:                st.success(f"✅ {expl}")

    col3, col4 = st.columns(2)
    with col3:
        vague = data.get("vague_terms", [])
        st.markdown(f'<span class="grad-heading-gold">💬 Vague Terms ({len(vague)})</span>', unsafe_allow_html=True)
        for v in vague:
            with st.expander(f"`{v.get('term','')}`"):
                st.markdown(f"**Problem:** {v.get('problem','')}")
                st.markdown(f"**Fix:** {v.get('fix','')}")

    with col4:
        missing = data.get("missing_information", [])
        st.markdown(f'<span class="grad-heading-gold">📋 Missing Info ({len(missing)})</span>', unsafe_allow_html=True)
        for m in missing:
            imp = m.get("importance","")
            icon = {"critical":"🔴","important":"🟡","nice_to_have":"🟢"}.get(imp,"⚪")
            with st.expander(f"{icon} {m.get('field','').replace('_',' ').title()}"):
                st.markdown(f"**Importance:** {imp}")
                st.markdown(f"**Suggestion:** {m.get('suggestion','')}")

    unrealistic = data.get("unrealistic_expectations", [])
    if unrealistic:
        st.markdown("---")
        st.markdown(f'<span class="grad-heading-red">⚠️ Unrealistic Expectations ({len(unrealistic)})</span>', unsafe_allow_html=True)
        for u in unrealistic:
            with st.expander(f"`{u.get('requirement','')}`"):
                st.markdown(f"**Problem:** {u.get('problem','')}")
                st.markdown(f"**Fix:** {u.get('fix','')}")

    inflation_list = data.get("requirement_inflation", [])
    if inflation_list:
        st.markdown("---")
        st.markdown('<span class="grad-heading-gold">📊 Should Be "Preferred" Not "Required"</span>', unsafe_allow_html=True)
        for item in inflation_list:
            st.markdown(f'<div class="quick-win">📌 {item}</div>', unsafe_allow_html=True)

    strengths = data.get("strengths", [])
    if strengths:
        st.markdown("---")
        st.markdown('<span class="grad-heading-green">✅ Strengths</span>', unsafe_allow_html=True)
        for s in strengths:
            st.markdown(f'<div class="quick-win">✅ {s}</div>', unsafe_allow_html=True)


def _display_rewrite_summary(data: dict):
    """Compact 4-metric summary only — no full reports."""
    st.markdown("---")
    st.markdown('<span class="section-badge">Analysis Summary</span>', unsafe_allow_html=True)
    bias_d = data.get("bias_report", {})
    qual_d = data.get("quality_report", {})
    level  = bias_d.get("overall_bias_level", "unknown")
    badge_map = {"low": "🟢 Low", "medium": "🟡 Medium", "high": "🔴 High"}
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bias Level",        badge_map.get(level, "❓"))
    c2.metric("Inclusivity",       f"{bias_d.get('inclusivity_score', 0)}/100")
    c3.metric("Quality Score",     f"{qual_d.get('overall_quality_score', 0)}/100")
    c4.metric("Bias Instances",    len(bias_d.get("bias_instances", [])))
    st.info("💡 Use **Detect Bias** or **Analyze Quality** buttons for the full detailed reports.")


def _display_rewrite_results(data: dict):
    st.markdown("---")
    st.markdown('<span class="section-badge">✍️ Rewritten Job Description</span>', unsafe_allow_html=True)

    rewritten = data.get("rewritten_jd", "")
    if rewritten:
        st.markdown('<span class="grad-heading">🌟 Improved JD</span>', unsafe_allow_html=True)
        st.markdown('<div class="rewrite-box">', unsafe_allow_html=True)
        st.text_area("Copy this improved version:", value=rewritten, height=420, key="rw_out")
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button("⬇️ Download Improved JD", data=rewritten, file_name="improved_jd.txt", mime="text/plain")

    changes = data.get("changes_made", [])
    if changes:
        st.markdown("---")
        st.markdown(f'<span class="grad-heading-gold">🔄 Changes Made ({len(changes)})</span>', unsafe_allow_html=True)
        for c in changes:
            st.markdown(
                f'<div class="change-item">'
                f'<span class="change-from">{c.get("original","")}</span>'
                f' → <span class="change-to">{c.get("replacement","")}</span>'
                f'</div>', unsafe_allow_html=True
            )
            # show reason inline without expander for a cleaner look
            if c.get("reason"):
                st.caption(f"  ↳ {c['reason']}")

    highlights = data.get("improvement_highlights", [])
    if highlights:
        st.markdown("---")
        st.markdown('<span class="grad-heading-green">🌟 Key Improvements</span>', unsafe_allow_html=True)
        for h in highlights:
            st.markdown(f'<div class="quick-win">🌟 {h}</div>', unsafe_allow_html=True)