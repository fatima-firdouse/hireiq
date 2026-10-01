import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from components.styles import HOME_CSS, generate_stars_html

API_URL = "https://hireiq-backend-f829.onrender.com"


st.set_page_config(
    page_title="HireIQ — Hire smarter. Hire fair.",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(HOME_CSS, unsafe_allow_html=True)

# ── Session defaults ────────────────────────────────────────────────
for k, v in [("role", None), ("demo_step", None), ("candidate_step", 1), ("recruiter_step", 1)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Routing ─────────────────────────────────────────────────────────
if st.session_state["role"] == "candidate":
    from pages.candidate import show; show(); st.stop()
if st.session_state["role"] == "recruiter":
    from pages.recruiter import show; show(); st.stop()
if st.session_state["role"] == "demo_candidate":
    from pages.demo_candidate import show; show(); st.stop()
if st.session_state["role"] == "demo_recruiter":
    from pages.demo_recruiter import show; show(); st.stop()

# ════════════════════════════════════════════════════════════════════
# HOME PAGE
# ════════════════════════════════════════════════════════════════════
st.markdown(generate_stars_html(55), unsafe_allow_html=True)

st.markdown("""
<div class="hn">
  <div class="hn-logo">
    <div class="hn-pill">🧠</div>
    <div class="hn-name">HireIQ</div>
  </div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="hh">
  <div class="hh-eyebrow">✦ RAG Pipeline · LLaMA 3.1 · ChromaDB</div>
  <div class="hh-title">Hire smarter.<br><span>Hire fair.</span></div>
  <div class="hh-sub">Analyze resumes. Match jobs. Detect bias instantly.</div>
</div>""", unsafe_allow_html=True)

# ── Hero buttons ─────────────────────────────────────────────────────
_, mid, _ = st.columns([1, 2, 1])
with mid:
    st.markdown('<div class="demo-btn">', unsafe_allow_html=True)
    if st.button("✨ Try Demo", use_container_width=True, key="try_demo"):
        # Toggle the who-are-you step
        st.session_state["demo_step"] = None if st.session_state["demo_step"] == "who" else "who"


# ════════════════════════════════════════════════════════════════════
# STEP A — "Who are you?" selection (shown after Try Demo click)
# ════════════════════════════════════════════════════════════════════
if st.session_state["demo_step"] == "who":
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # Section title
    _, title_col, _ = st.columns([1, 2, 1])
    with title_col:
        st.markdown("""
        <div style='text-align:center;margin-bottom:6px;'>
          <div style='font-size:11px;font-weight:700;letter-spacing:1.4px;
            text-transform:uppercase;color:rgba(70,197,211,0.70);margin-bottom:10px;'>Step 1 of 1</div>
          <div style='font-size:26px;font-weight:900;color:white;margin-bottom:8px;'>Who are you?</div>
          <div style='font-size:15px;color:rgba(255,255,255,0.45);'>
            Pick your role — we'll show you a full demo tailored to you.
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Two role cards
    _, card_col, _ = st.columns([0.5, 3, 0.5])
    with card_col:
        col_a, col_b = st.columns(2, gap="medium")

        with col_a:
            st.markdown("""
            <div style='background:rgba(218,123,147,0.08);
              border:1.5px solid rgba(218,123,147,0.38);border-radius:22px;
              padding:32px 28px;text-align:center;margin-bottom:12px;
              box-shadow:0 8px 32px rgba(0,0,0,0.45),0 0 20px rgba(218,123,147,0.10);'>
              <div style='font-size:52px;margin-bottom:14px;'>🧑‍💼</div>
              <div style='font-size:20px;font-weight:800;color:white;margin-bottom:10px;'>I'm a Candidate</div>
              <div style='font-size:14px;color:rgba(255,255,255,0.55);line-height:1.7;margin-bottom:18px;'>
                See how HireIQ matches your resume to a job description,<br>
                finds skill gaps, and preps you for interviews.
              </div>
              <div style='display:flex;flex-wrap:wrap;gap:7px;justify-content:center;'>
                <span style='font-size:12px;font-weight:700;color:#F4A5BA;background:rgba(218,123,147,0.14);
                  padding:4px 13px;border-radius:100px;border:1px solid rgba(218,123,147,0.35);'>Match Score</span>
                <span style='font-size:12px;font-weight:700;color:#F4A5BA;background:rgba(218,123,147,0.14);
                  padding:4px 13px;border-radius:100px;border:1px solid rgba(218,123,147,0.35);'>Skill Gaps</span>
                <span style='font-size:12px;font-weight:700;color:#F4A5BA;background:rgba(218,123,147,0.14);
                  padding:4px 13px;border-radius:100px;border:1px solid rgba(218,123,147,0.35);'>Interview Prep</span>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button("🧑‍💼 See Candidate Demo →", use_container_width=True, key="demo_as_cand"):
                st.session_state.update({"role": "demo_candidate", "demo_step": None})
                st.rerun()

        with col_b:
            st.markdown("""
            <div style='background:rgba(58,191,208,0.08);
              border:1.5px solid rgba(58,191,208,0.38);border-radius:22px;
              padding:32px 28px;text-align:center;margin-bottom:12px;
              box-shadow:0 8px 32px rgba(0,0,0,0.45),0 0 20px rgba(58,191,208,0.10);'>
              <div style='font-size:52px;margin-bottom:14px;'>🏢</div>
              <div style='font-size:20px;font-weight:800;color:white;margin-bottom:10px;'>I'm a Recruiter</div>
              <div style='font-size:14px;color:rgba(255,255,255,0.55);line-height:1.7;margin-bottom:18px;'>
                See how HireIQ audits your job description for bias,<br>
                scores quality, and rewrites it to attract more talent.
              </div>
              <div style='display:flex;flex-wrap:wrap;gap:7px;justify-content:center;'>
                <span style='font-size:12px;font-weight:700;color:#7EDDE8;background:rgba(58,191,208,0.14);
                  padding:4px 13px;border-radius:100px;border:1px solid rgba(58,191,208,0.35);'>Bias Detection</span>
                <span style='font-size:12px;font-weight:700;color:#7EDDE8;background:rgba(58,191,208,0.14);
                  padding:4px 13px;border-radius:100px;border:1px solid rgba(58,191,208,0.35);'>Quality Score</span>
                <span style='font-size:12px;font-weight:700;color:#7EDDE8;background:rgba(58,191,208,0.14);
                  padding:4px 13px;border-radius:100px;border:1px solid rgba(58,191,208,0.35);'>AI Rewrite</span>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button("🏢 See Recruiter Demo →", use_container_width=True, key="demo_as_rec"):
                st.session_state.update({"role": "demo_recruiter", "demo_step": None})
                st.rerun()



_, mid, _ = st.columns([1, 2, 1])
with mid:
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("👤 Candidate Portal", use_container_width=True, key="go_cand"):
            st.session_state.update({"role": "candidate", "demo_step": None}); st.rerun()
    with c2:
        if st.button("🏢 Recruiter Portal", use_container_width=True, key="go_rec"):
            st.session_state.update({"role": "recruiter", "demo_step": None}); st.rerun()
    st.markdown(
        "<p style='text-align:center;margin-top:10px;font-size:13px;"
        "color:rgba(255,255,255,0.28);'>No sign-up required · 100% free to try</p>",
        unsafe_allow_html=True
    )




# ════════════════════════════════════════════════════════════════════
# FEATURE CARDS (always shown below)
# ════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="hh-cards">
  <div class="hc">
    <span class="hc-icon">🎯</span>
    <div class="hc-title">Resume Match Analysis</div>
    <div class="hc-desc">Upload any resume and get a precision match score, highlighted skill gaps, and STAR interview prep — powered by RAG + LLaMA 3.1.</div>
    <div class="hc-tags">
      <span class="hc-tag">Match Score</span>
      <span class="hc-tag">Skill Gaps</span>
      <span class="hc-tag">Interview Prep</span>
      <span class="hc-tag">Blind Mode</span>
    </div>
  </div>
  <div class="hc">
    <span class="hc-icon">🏢</span>
    <div class="hc-title">JD Intelligence Suite</div>
    <div class="hc-desc">Detect biased language, score JD quality, flag inflated requirements, and get a full AI-rewritten inclusive job description in one click.</div>
    <div class="hc-tags">
      <span class="hc-tag">Bias Detection</span>
      <span class="hc-tag">Quality Score</span>
      <span class="hc-tag">AI Rewrite</span>
      <span class="hc-tag">Research-backed</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
