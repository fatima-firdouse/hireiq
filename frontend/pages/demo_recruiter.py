"""
pages/demo_recruiter.py
Recruiter demo — Cami.AI JD · Bias Detection + Quality + Rewrite
All results are pre-computed mock data. No API calls.
"""
import streamlit as st
from components.styles import RECRUITER_CSS

st.markdown(RECRUITER_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# MOCK DATA — Cami.AI JD analysis
# ─────────────────────────────────────────────────────────────────
JD_SNIPPET = (
    "Cami.AI is looking for a Data Engineering Trainee who wants to work with significant autonomy "
    "on a small, entrepreneurial team. Build reusable integrations between Cami.AI systems and customer "
    "platforms. Write ML workers on top of extracted data. Tech: Python, AWS Sagemaker, AWS Glue, "
    "Node.js, Delta Lake, Spark."
)

BIAS = {
    "level": "low",
    "inclusivity": 86,
    "summary": "The JD is largely inclusive. Two minor phrases could subtly narrow your applicant pool — quick fixes, big impact.",
    "instances": [
        {
            "text":        "high performance high energy team",
            "bias_type":   "disability",
            "explanation": "Can discourage applicants with chronic illness, ADHD, or different work styles — even highly capable ones.",
            "fix":         "collaborative, results-driven team",
            "impact":      "Removing this phrase can increase diversity applications by ~12%.",
        },
        {
            "text":        "fast growing SAAS platform",
            "bias_type":   "age",
            "explanation": "Startup growth language signals a youth-oriented culture, subtly discouraging experienced candidates.",
            "fix":         "growing, ambitious SaaS platform",
            "impact":      "Neutral phrasing attracts a broader experience range without changing meaning.",
        },
    ],
    "quick_wins": [
        "Replace 'high performance high energy' → 'collaborative, results-driven'",
        "Add: 'We welcome applicants of all backgrounds and experience levels'",
        "Specify remote/hybrid policy — this increases applicant pool by up to 35%",
    ],
    "masculine_words": ["autonomy", "entrepreneurial"],
}

QUALITY = {
    "score": 74,
    "inflation_score": 78,
    "summary": "Well-structured with a clear tech stack and responsibilities. Key gaps: no salary range, no remote policy, and one requirement that's too senior for a trainee role.",
    "vague": [
        {"term": "competitive compensation",
         "problem": "Candidates can't self-filter without a number.",
         "fix": "Add a specific range, e.g. ₹4–6 LPA + equity"},
        {"term": "significant autonomy",
         "problem": "Ambiguous — unsupported vs genuinely independent.",
         "fix": "'Own integrations end-to-end with senior engineering support'"},
    ],
    "missing": [
        {"field": "Salary Range",   "importance": "critical",    "suggestion": "List ₹ range or stipend — top candidates filter by this"},
        {"field": "Remote Policy",  "importance": "important",   "suggestion": "72% of candidates prioritize hybrid/remote clarity"},
        {"field": "Team Size",      "importance": "nice_to_have","suggestion": "e.g. '8-person engineering team' sets context"},
    ],
    "inflation": ["'Experienced using unit testing' → 'Exposure to testing practices' (right-sized for trainee)"],
    "strengths": [
        "Clear tech stack listed upfront — great for candidate self-screening",
        "Specific responsibilities with actionable verbs (Develop, Design, Collaborate)",
        "Honest about company stage and growth trajectory",
    ],
}

REWRITE_SNIPPET = """\
Data Engineering Trainee — Cami.AI (Kochi, India | Hybrid)

Compensation: ₹4–6 LPA + equity participation
Work Mode: Hybrid — Kochi office + remote flexibility

About the Role:
As a Data Engineering Trainee, you'll own integrations between Cami.AI systems and customer
platforms, working closely with our collaborative 8-person engineering team.

What You'll Work On:
• Build reusable data integrations (inbound/outbound) between Cami.AI and customer platforms
• Write ML workers on top of extracted data to grow system intelligence
• Develop performant, scalable, documented, maintainable code

Tech Stack: Python, AWS Sagemaker, AWS Glue, Node.js, Delta Lake, Spark

What We're Looking For:
• B.Tech in CS, Engineering, or related field
• Familiarity with JSON, XML, flat-file data formats
• Solid OOP fundamentals and reusable coding practices
• Python experience; REST APIs/microservices knowledge is a plus
• Exposure to testing and documentation practices

We welcome applicants of all backgrounds. If you meet most (not all) qualifications — apply!\
"""

CHANGES = [
    {"from": "high performance high energy team",  "to": "collaborative 8-person engineering team", "why": "Removes disability-exclusionary language"},
    {"from": "competitive compensation",           "to": "₹4–6 LPA + equity participation",         "why": "Specific salary increases application rate by 30%+"},
    {"from": "significant autonomy",               "to": "own integrations with senior support",     "why": "Clarifies independence vs unsupported"},
    {"from": "Experienced using unit testing",     "to": "Exposure to testing practices",            "why": "Right-sized for a trainee role"},
]

HIGHLIGHTS = [
    "Added salary range — expected to increase application rate by 30%+",
    "Added hybrid/remote statement — reaches 72% more candidates",
    "Right-sized 'experienced' → 'exposure to' for a trainee role",
    "Added team size and inclusion statement",
]


# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def _sidebar():
    steps = [
        ("✓", "JD Loaded",          "Cami.AI · Data Engineering Trainee"),
        ("✓", "Bias Detected",      "Low Bias · 2 instances · 86/100"),
        ("✓", "Quality Analyzed",   "Score 74/100 · 3 gaps found"),
        ("✓", "Rewrite Generated",  "4 improvements applied"),
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
        <div class="sb-role" style="color:rgba(126,221,232,0.85)!important;">🏢 Recruiter Demo</div>
        <div class="prg-label">Demo Progress</div>
        <div class="prg-wrap"><div class="prg-fill" style="width:100%"></div></div>
        {rows}
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True, key="dr_home"):
            st.session_state.update({"role": None, "demo_step": None}); st.rerun()
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("🏢 Try with My JD", use_container_width=True, key="dr_real"):
            st.session_state.update({"role": "recruiter", "demo_step": None}); st.rerun()


def _section_divider(n, title, icon):
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:14px;margin:28px 0 18px;'>
      <div style='width:34px;height:34px;border-radius:50%;
        background:linear-gradient(135deg,#3ABFD0,#186690);
        display:flex;align-items:center;justify-content:center;
        font-size:14px;font-weight:900;color:white;
        box-shadow:0 0 14px rgba(58,191,208,0.50);flex-shrink:0;'>{n}</div>
      <div style='font-size:18px;font-weight:800;
        background:linear-gradient(90deg,#7EDDE8,#3ABFD0);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;'>{icon} {title}</div>
      <div style='flex:1;height:1px;
        background:linear-gradient(90deg,rgba(58,191,208,0.30),transparent);'></div>
    </div>""", unsafe_allow_html=True)


def _bias_bars(instances):
    """Pure CSS horizontal bar chart — no plotly, always renders."""
    from collections import Counter
    counts = Counter(b["bias_type"] for b in instances)
    total  = sum(counts.values())
    PALETTE = {
        "gender": "#E74C3C", "age": "#F39C12", "race": "#9B59B6",
        "disability": "#3ABFD0", "family_status": "#2ECC71", "general": "#DA7B93",
    }
    rows = ""
    for label, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        pct   = round((cnt / total) * 100)
        color = PALETTE.get(label, "#7EDDE8")
        rows += (
            f'<div style="margin-bottom:14px;">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
            f'<span style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.82);">'
            f'{label.replace("_"," ").title()}</span>'
            f'<span style="font-size:13px;font-weight:800;color:{color};">'
            f'{cnt} instance{"s" if cnt>1 else ""} &nbsp;·&nbsp; {pct}%</span>'
            f'</div>'
            f'<div style="background:rgba(255,255,255,0.07);border-radius:100px;height:10px;">'
            f'<div style="width:{pct}%;height:10px;border-radius:100px;'
            f'background:{color};box-shadow:0 0 12px {color}70;"></div>'
            f'</div></div>'
        )
    st.markdown(
        f'<div style="background:rgba(5,15,25,0.65);border:1.5px solid rgba(58,191,208,0.28);'
        f'border-radius:16px;padding:22px 26px;margin:12px 0;">'
        f'<div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.34);"'
        f' style="text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;">Breakdown by Type</div>'
        f'{rows}</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
def show():
    _sidebar()

    # Demo banner
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(58,191,208,0.12),rgba(24,102,144,0.08));
      border:1.5px solid rgba(58,191,208,0.38);border-radius:14px;
      padding:12px 22px;margin-bottom:24px;display:flex;align-items:center;gap:12px;'>
      <span style='font-size:18px;'>✨</span>
      <div>
        <span style='font-size:13px;font-weight:800;color:#7EDDE8;'>Demo Mode</span>
        <span style='font-size:13px;color:rgba(255,255,255,0.48);margin-left:10px;'>
          Cami.AI Data Engineering Trainee JD · All results are pre-computed samples
        </span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.title("🏢 Recruiter — JD Intelligence Demo")

    # ── STEP 1: JD Preview ──────────────────────────────────────
    _section_divider("1", "Sample Job Description", "📋")

    st.markdown(f"""
    <div style='background:rgba(5,15,25,0.65);border:1.5px solid rgba(58,191,208,0.30);
      border-radius:18px;padding:24px 28px;
      box-shadow:0 8px 28px rgba(0,0,0,0.45);'>
      <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;'>
        <div>
          <div style='font-size:20px;font-weight:800;color:white;margin-bottom:4px;'>Data Engineering Trainee</div>
          <div style='font-size:14px;color:#7EDDE8;margin-bottom:2px;'>Cami.AI &nbsp;·&nbsp; Kochi, India</div>
          <div style='font-size:13px;color:rgba(255,255,255,0.40);'>Full-time · Fresher/Trainee</div>
        </div>
        <div style='display:flex;gap:7px;flex-wrap:wrap;justify-content:flex-end;'>
          <span style='font-size:11px;font-weight:700;color:#7EDDE8;background:rgba(58,191,208,0.12);
            padding:4px 12px;border-radius:100px;border:1px solid rgba(58,191,208,0.30);'>Python</span>
          <span style='font-size:11px;font-weight:700;color:#7EDDE8;background:rgba(58,191,208,0.12);
            padding:4px 12px;border-radius:100px;border:1px solid rgba(58,191,208,0.30);'>AWS Sagemaker</span>
          <span style='font-size:11px;font-weight:700;color:#7EDDE8;background:rgba(58,191,208,0.12);
            padding:4px 12px;border-radius:100px;border:1px solid rgba(58,191,208,0.30);'>Apache Spark</span>
        </div>
      </div>
      <div style='font-size:14px;color:rgba(255,255,255,0.68);line-height:1.75;border-top:1px solid rgba(255,255,255,0.07);
        padding-top:14px;'>{JD_SNIPPET}</div>
    </div>""", unsafe_allow_html=True)

    # ── STEP 2: Bias Detection ───────────────────────────────────
    _section_divider("2", "Bias Detection", "🔍")

    level = BIAS["level"]
    badge_map = {
        "low":    ("🟢 Low Bias",    "#6EE7B7", "rgba(46,204,113,0.14)",  "rgba(46,204,113,0.50)"),
        "medium": ("🟡 Medium Bias", "#FDE68A", "rgba(243,156,18,0.14)",  "rgba(243,156,18,0.50)"),
        "high":   ("🔴 High Bias",   "#FCA5A5", "rgba(231,76,60,0.14)",   "rgba(231,76,60,0.50)"),
    }
    btxt, bcol, bbg, bborder = badge_map[level]

    bc1, bc2 = st.columns(2)
    bc1.metric("Inclusivity Score", f"{BIAS['inclusivity']}/100")
    bc2.metric("Bias Instances",    len(BIAS["instances"]))

    st.markdown(
        f"<div style='background:{bbg};border:1.5px solid {bborder};border-radius:100px;"
        f"display:inline-flex;align-items:center;gap:8px;padding:10px 22px;"
        f"font-size:16px;font-weight:800;color:{bcol};margin:12px 0;"
        f"box-shadow:0 0 16px {bbg};'>{btxt}</div>"
        f"<p style='font-size:14px;color:rgba(255,255,255,0.55);margin-top:6px;margin-bottom:16px;'>"
        f"{BIAS['summary']}</p>",
        unsafe_allow_html=True
    )

    # CSS bar chart (replaces plotly pie — always renders)
    _bias_bars(BIAS["instances"])

    # Bias instance cards
    st.markdown(
        "<p style='font-size:12px;font-weight:700;color:rgba(255,255,255,0.36);"
        "text-transform:uppercase;letter-spacing:1px;margin:18px 0 10px;'>Instance Details</p>",
        unsafe_allow_html=True
    )
    for b in BIAS["instances"]:
        with st.expander(f"❌  `{b['text']}`  —  {b['bias_type'].title()}"):
            col_l, col_r = st.columns([1, 1], gap="medium")
            with col_l:
                st.markdown(
                    f"<span style='display:inline-block;padding:5px 14px;border-radius:8px;"
                    f"background:rgba(231,76,60,0.12);border:1.5px solid rgba(231,76,60,0.45);"
                    f"color:#FCA5A5;font-size:13px;font-weight:700;margin-bottom:10px;'>🚩 {b['text']}</span>"
                    f"<p style='font-size:14px;color:rgba(255,255,255,0.78);line-height:1.7;'>{b['explanation']}</p>",
                    unsafe_allow_html=True
                )
            with col_r:
                st.markdown(
                    f"<span style='display:inline-block;padding:5px 14px;border-radius:8px;"
                    f"background:rgba(46,204,113,0.10);border:1.5px solid rgba(46,204,113,0.45);"
                    f"color:#6EE7B7;font-size:13px;font-weight:700;margin-bottom:10px;'>✅ {b['fix']}</span>"
                    f"<p style='font-size:13px;color:rgba(255,255,255,0.50);line-height:1.6;'>{b['impact']}</p>",
                    unsafe_allow_html=True
                )

    # Quick wins
    st.markdown(
        "<p style='font-size:12px;font-weight:700;color:rgba(255,255,255,0.36);"
        "text-transform:uppercase;letter-spacing:1px;margin:18px 0 10px;'>⚡ Quick Wins</p>",
        unsafe_allow_html=True
    )
    for w in BIAS["quick_wins"]:
        st.markdown(
            f"<div style='background:rgba(46,204,113,0.07);border:1px solid rgba(46,204,113,0.32);"
            f"border-left:4px solid #2ECC71;border-radius:10px;padding:11px 17px;"
            f"font-size:14px;color:rgba(255,255,255,0.85);margin-bottom:8px;'>⚡ {w}</div>",
            unsafe_allow_html=True
        )

    # Masculine-coded words
    if BIAS["masculine_words"]:
        tags = "".join(
            f"<span style='display:inline-block;margin:4px;padding:5px 14px;border-radius:100px;"
            f"font-size:13px;font-weight:700;color:#D8B4FE;"
            f"background:rgba(155,89,182,0.10);border:1.5px solid rgba(155,89,182,0.40);'>{w}</span>"
            for w in BIAS["masculine_words"]
        )
        st.markdown(
            f"<p style='font-size:12px;font-weight:700;color:rgba(255,255,255,0.36);"
            f"text-transform:uppercase;letter-spacing:1px;margin:18px 0 8px;'>⚧ Masculine-Coded Words</p>"
            f"<div style='background:rgba(15,5,30,0.60);border:1.5px solid rgba(155,89,182,0.35);"
            f"border-radius:14px;padding:16px 18px;'>{tags}"
            f"<p style='font-size:13px;color:rgba(255,255,255,0.40);margin-top:12px;'>"
            f"Masculine-coded language can reduce female applications by up to 40%.</p></div>",
            unsafe_allow_html=True
        )

    # ── STEP 3: Quality Analysis ─────────────────────────────────
    _section_divider("3", "Quality Analysis", "📋")

    score = QUALITY["score"]
    q_color = "#6EE7B7" if score >= 70 else "#FDE68A" if score >= 45 else "#FCA5A5"

    qc1, qc2 = st.columns([1, 2])
    with qc1:
        st.markdown(
            f"<div style='background:rgba(5,15,25,0.60);border:1.5px solid rgba(58,191,208,0.28);"
            f"border-radius:16px;padding:22px;text-align:center;'>"
            f"<div style='font-size:11px;font-weight:700;color:rgba(255,255,255,0.34);"
            f"text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px;'>Overall Quality</div>"
            f"<div style='font-size:50px;font-weight:900;color:{q_color};"
            f"text-shadow:0 0 22px {q_color}88;'>{score}"
            f"<span style='font-size:18px;color:rgba(255,255,255,0.28);'>/100</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )
    with qc2:
        st.markdown(
            f"<div style='background:rgba(5,15,25,0.60);border:1.5px solid rgba(58,191,208,0.28);"
            f"border-radius:16px;padding:18px 22px;height:100%;'>"
            f"<div style='font-size:14px;color:rgba(255,255,255,0.72);line-height:1.75;'>{QUALITY['summary']}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    vc, mc = st.columns(2, gap="medium")

    with vc:
        st.markdown(
            f"<p style='font-size:13px;font-weight:700;color:#FDE68A;margin-bottom:10px;'>💬 Vague Terms ({len(QUALITY['vague'])})</p>",
            unsafe_allow_html=True
        )
        for v in QUALITY["vague"]:
            with st.expander(f"`{v['term']}`"):
                st.markdown(f"**Problem:** {v['problem']}")
                st.markdown(f"**Fix:** {v['fix']}")

    with mc:
        st.markdown(
            f"<p style='font-size:13px;font-weight:700;color:#FDE68A;margin-bottom:10px;'>📋 Missing Info ({len(QUALITY['missing'])})</p>",
            unsafe_allow_html=True
        )
        imp_icon = {"critical": "🔴", "important": "🟡", "nice_to_have": "🟢"}
        for m in QUALITY["missing"]:
            with st.expander(f"{imp_icon.get(m['importance'],'⚪')} {m['field']}"):
                st.markdown(f"**Importance:** {m['importance'].replace('_',' ').title()}")
                st.markdown(f"**Suggestion:** {m['suggestion']}")

    # Strengths
    st.markdown(
        "<p style='font-size:12px;font-weight:700;color:rgba(255,255,255,0.36);"
        "text-transform:uppercase;letter-spacing:1px;margin:18px 0 10px;'>✅ Strengths</p>",
        unsafe_allow_html=True
    )
    for s in QUALITY["strengths"]:
        st.markdown(
            f"<div style='background:rgba(46,204,113,0.07);border:1px solid rgba(46,204,113,0.30);"
            f"border-left:4px solid #2ECC71;border-radius:10px;padding:11px 17px;"
            f"font-size:14px;color:rgba(255,255,255,0.85);margin-bottom:8px;'>✅ {s}</div>",
            unsafe_allow_html=True
        )

    # ── STEP 4: AI Rewrite ───────────────────────────────────────
    _section_divider("4", "AI-Improved Rewrite", "✍️")

    st.markdown(
        "<p style='font-size:14px;color:rgba(255,255,255,0.50);margin-bottom:14px;'>"
        "4 changes applied · Bias removed · Salary added · Requirements right-sized</p>",
        unsafe_allow_html=True
    )
    st.text_area("Improved JD (copy or download):", value=REWRITE_SNIPPET, height=340, key="dr_rw")
    st.download_button("⬇️ Download Improved JD", data=REWRITE_SNIPPET,
                       file_name="cami_ai_improved_jd.txt", mime="text/plain")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # Changes made
    st.markdown(
        "<p style='font-size:12px;font-weight:700;color:rgba(255,255,255,0.36);"
        "text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;'>🔄 Changes Applied</p>",
        unsafe_allow_html=True
    )
    for c in CHANGES:
        st.markdown(
            f"<div style='background:rgba(5,15,25,0.60);border:1.5px solid rgba(58,191,208,0.24);"
            f"border-radius:12px;padding:13px 18px;margin-bottom:8px;'>"
            f"<span style='text-decoration:line-through;color:rgba(252,165,165,0.75);font-size:14px;'>{c['from']}</span>"
            f"<span style='color:rgba(255,255,255,0.35);font-size:14px;'> → </span>"
            f"<span style='color:#6EE7B7;font-size:14px;font-weight:700;'>{c['to']}</span>"
            f"<div style='font-size:13px;color:rgba(255,255,255,0.40);margin-top:5px;'>↳ {c['why']}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Key improvements
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    for h in HIGHLIGHTS:
        st.markdown(
            f"<div style='background:rgba(46,204,113,0.07);border:1px solid rgba(46,204,113,0.28);"
            f"border-left:4px solid #2ECC71;border-radius:10px;padding:11px 17px;"
            f"font-size:14px;color:rgba(255,255,255,0.85);margin-bottom:8px;'>🌟 {h}</div>",
            unsafe_allow_html=True
        )

    # ── CTA ──────────────────────────────────────────────────────
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='background:rgba(58,191,208,0.06);border:1.5px solid rgba(58,191,208,0.26);"
        "border-radius:16px;padding:20px 24px;text-align:center;'>"
        "<div style='font-size:16px;font-weight:800;color:white;margin-bottom:6px;'>Ready to audit your own JD?</div>"
        "<div style='font-size:14px;color:rgba(255,255,255,0.45);'>Paste any job description and get bias + quality analysis in seconds.</div>"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    _, rc1, rc2, _ = st.columns([1, 1.2, 1.2, 1])
    with rc1:
        if st.button("🏢 Audit My JD", use_container_width=True, type="primary", key="dr_go"):
            st.session_state.update({"role": "recruiter", "demo_step": None}); st.rerun()
    with rc2:
        if st.button("🏠 Back to Home", use_container_width=True, key="dr_back"):
            st.session_state.update({"role": None, "demo_step": None}); st.rerun()

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)