import random

# ─────────────────────────────────────────────────────────────────────
# HOME PAGE CSS
# ─────────────────────────────────────────────────────────────────────
HOME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }

/* Remove top gap */
[data-testid="stAppViewContainer"] > .main > .block-container {
    padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important;
}
.main .block-container { padding-top: 0 !important; }

.stApp {
    background: linear-gradient(135deg, #0D1B2A 0%, #1B2A3B 50%, #0D1B2A 100%) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: white !important; min-height: 100vh;
}
header[data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; }
footer, .stDeployButton { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

/* Navbar */
.hn { display: flex; align-items: center; padding: 18px 44px 14px; border-bottom: 1px solid rgba(70,197,211,0.15); background: rgba(0,0,0,0.25); }
.hn-logo { display: flex; align-items: center; gap: 13px; }
.hn-pill { background: linear-gradient(135deg, #DA7B93, #3ABFD0) !important; width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 0 28px rgba(70,197,211,0.55); }
.hn-name { font-size: 26px; font-weight: 900; background: linear-gradient(90deg, #7EDDE8, #F4A5BA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

/* Hero */
.hh { max-width: 860px; margin: 0 auto; padding: 44px 24px 18px; text-align: center; }
.hh-eyebrow { display: inline-flex; align-items: center; gap: 8px; background: rgba(70,197,211,0.10); border: 1.5px solid rgba(70,197,211,0.45); border-radius: 100px; padding: 8px 22px; font-size: 13px; font-weight: 700; color: #7EDDE8; margin-bottom: 24px; letter-spacing: 1px; box-shadow: 0 0 18px rgba(70,197,211,0.20); }
.hh-title { font-size: clamp(42px, 6vw, 70px); font-weight: 900; line-height: 1.1; letter-spacing: -2px; color: white; margin-bottom: 16px; }
.hh-title span { background: linear-gradient(135deg, #7EDDE8 0%, #DA7B93 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hh-sub { font-size: 19px; color: rgba(255,255,255,0.70); line-height: 1.8; margin-bottom: 34px; }

/* Feature cards */
.hh-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 740px; margin: 26px auto 0; }
.hc { background: rgba(10,25,40,0.65); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1.5px solid rgba(70,197,211,0.30); border-radius: 22px; padding: 34px; transition: all 0.3s ease; box-shadow: 0 8px 32px rgba(0,0,0,0.45), 0 0 18px rgba(70,197,211,0.07); }
.hc:hover { border-color: rgba(70,197,211,0.65); transform: translateY(-8px); box-shadow: 0 16px 48px rgba(0,0,0,0.55), 0 0 30px rgba(70,197,211,0.18); }
.hc-icon { font-size: 44px; margin-bottom: 16px; display: block; }
.hc-title { font-size: 21px; font-weight: 800; color: white; margin-bottom: 10px; }
.hc-desc { font-size: 15px; color: rgba(255,255,255,0.68); line-height: 1.7; margin-bottom: 20px; }
.hc-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.hc-tag { font-size: 12px; font-weight: 700; color: #7EDDE8; background: rgba(70,197,211,0.10); padding: 5px 14px; border-radius: 100px; border: 1px solid rgba(70,197,211,0.35); }

/* ── Buttons ── */
.stButton > button { font-family: 'Plus Jakarta Sans', sans-serif !important; border-radius: 13px !important; font-size: 16px !important; font-weight: 700 !important; padding: 14px 28px !important; transition: all 0.25s !important; cursor: pointer !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #3ABFD0, #186690) !important; color: white !important; border: none !important; box-shadow: 0 4px 22px rgba(58,191,208,0.50) !important; }
.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(58,191,208,0.68) !important; }
.stButton > button:not([kind="primary"]) { background: rgba(10,25,40,0.65) !important; color: white !important; border: 1.5px solid rgba(70,197,211,0.40) !important; box-shadow: 0 0 12px rgba(70,197,211,0.12) !important; }
.stButton > button:not([kind="primary"]):hover { background: rgba(70,197,211,0.15) !important; border-color: rgba(70,197,211,0.70) !important; box-shadow: 0 0 22px rgba(70,197,211,0.28) !important; transform: translateY(-2px) !important; }

/* ── Try Demo button — special gradient ── */
.demo-btn .stButton > button {
    background: linear-gradient(135deg, #DA7B93 0%, #3ABFD0 100%) !important;
    color: white !important; border: none !important;
    font-size: 17px !important; padding: 15px 36px !important;
    box-shadow: 0 6px 28px rgba(218,123,147,0.50), 0 0 0 1px rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
}
.demo-btn .stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 40px rgba(218,123,147,0.65), 0 0 0 1px rgba(255,255,255,0.12) !important;
}

/* ── Demo results panel ── */
.demo-panel {
    max-width: 860px; margin: 36px auto 0;
    background: rgba(10,20,35,0.72);
    backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
    border: 1.5px solid rgba(70,197,211,0.30);
    border-radius: 24px; padding: 36px 40px;
    box-shadow: 0 16px 60px rgba(0,0,0,0.55), 0 0 30px rgba(70,197,211,0.08);
    animation: fadeUp 0.45s ease both;
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(22px); }
    to   { opacity:1; transform:translateY(0); }
}
.demo-panel-title {
    font-size: 15px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: rgba(255,255,255,0.40);
    margin-bottom: 28px; display: flex; align-items: center; gap: 10px;
}
.demo-panel-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(70,197,211,0.30), transparent);
}

/* Score row */
.demo-score-wrap { margin-bottom: 28px; }
.demo-score-label {
    display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 10px;
}
.demo-score-name { font-size: 15px; font-weight: 700; color: rgba(255,255,255,0.75); }
.demo-score-val  { font-size: 32px; font-weight: 900; color: #7EDDE8;
    text-shadow: 0 0 20px rgba(58,191,208,0.60); }
.demo-bar-bg { background: rgba(255,255,255,0.07); border-radius: 100px; height: 10px; overflow: hidden; }
.demo-bar-fill {
    height: 10px; border-radius: 100px;
    background: linear-gradient(90deg, #3ABFD0, #7EDDE8);
    box-shadow: 0 0 14px rgba(58,191,208,0.60);
    transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
}

/* Three stat cards */
.demo-stats { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin-bottom: 28px; }
.demo-stat {
    background: rgba(255,255,255,0.04);
    border: 1.5px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 20px 18px;
    text-align: center; transition: border-color 0.2s;
}
.demo-stat:hover { border-color: rgba(70,197,211,0.35); }
.demo-stat-val { font-size: 28px; font-weight: 900; margin-bottom: 4px; }
.demo-stat-lbl { font-size: 12px; font-weight: 700; color: rgba(255,255,255,0.42);
    text-transform: uppercase; letter-spacing: 0.7px; }

/* Skill tags */
.demo-section-lbl { font-size: 12px; font-weight: 700; color: rgba(255,255,255,0.40);
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }
.demo-tags { display: flex; flex-wrap: wrap; gap: 9px; margin-bottom: 28px; }
.demo-tag-match {
    font-size: 13px; font-weight: 700; padding: 7px 16px; border-radius: 100px;
    background: rgba(46,204,113,0.12); border: 1.5px solid rgba(46,204,113,0.50);
    color: #6EE7B7; box-shadow: 0 0 10px rgba(46,204,113,0.16);
}
.demo-tag-miss {
    font-size: 13px; font-weight: 700; padding: 7px 16px; border-radius: 100px;
    background: rgba(231,76,60,0.10); border: 1.5px solid rgba(231,76,60,0.45);
    color: #FCA5A5; box-shadow: 0 0 10px rgba(231,76,60,0.14);
}

/* Bias badge */
.demo-bias-row { display: flex; align-items: center; gap: 16px; }
.demo-bias-badge {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 14px; font-weight: 800; padding: 10px 22px;
    border-radius: 100px; letter-spacing: 0.3px;
}
.demo-bias-low  { background: rgba(46,204,113,0.14); border: 1.5px solid rgba(46,204,113,0.55); color: #6EE7B7; box-shadow: 0 0 16px rgba(46,204,113,0.22); }
.demo-bias-med  { background: rgba(243,156,18,0.14); border: 1.5px solid rgba(243,156,18,0.55); color: #FDE68A; box-shadow: 0 0 16px rgba(243,156,18,0.22); }
.demo-bias-high { background: rgba(231,76,60,0.14);  border: 1.5px solid rgba(231,76,60,0.55);  color: #FCA5A5; box-shadow: 0 0 16px rgba(231,76,60,0.22); }
.demo-bias-note { font-size: 13px; color: rgba(255,255,255,0.45); line-height: 1.5; }

/* CTA row at bottom of demo */
.demo-cta { margin-top: 30px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.07); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
.demo-cta-note { font-size: 14px; color: rgba(255,255,255,0.40); }

/* ── Divider between hero buttons and feature cards ── */
.section-sep { height: 1px; max-width: 480px; margin: 40px auto; background: linear-gradient(90deg, transparent, rgba(70,197,211,0.25), transparent); }
</style>
"""

# ─────────────────────────────────────────────────────────────────────
# CANDIDATE CSS  —  Rose/Pink theme
# ─────────────────────────────────────────────────────────────────────
CANDIDATE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
* { box-sizing: border-box; }

/* Force background — overrides HOME_CSS bleed */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(135deg, #1A0F1E 0%, #2F1B28 55%, #1A1030 100%) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main > .block-container {
    padding-top: 1.5rem !important; background: transparent !important;
}

/* Typography */
h1 { font-size: 2.1rem !important; font-weight: 900 !important; color: white !important; }
h2 { font-size: 1.6rem !important; font-weight: 800 !important; color: white !important; }
h3 { font-size: 1.25rem !important; font-weight: 700 !important; color: #F4A5BA !important; }
p, li { font-size: 15px !important; color: rgba(255,255,255,0.85) !important; line-height: 1.75 !important; }
label { color: rgba(255,255,255,0.88) !important; font-size: 15px !important; font-weight: 600 !important; }
strong { color: white !important; }

header[data-testid="stHeader"] { background: rgba(26,15,30,0.80) !important; border-bottom: 1px solid rgba(218,123,147,0.20) !important; backdrop-filter: blur(12px) !important; }
footer, .stDeployButton { display: none !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #140A18 0%, #0D0810 100%) !important;
    border-right: 2px solid rgba(218,123,147,0.40) !important;
    box-shadow: 4px 0 28px rgba(0,0,0,0.60) !important;
}
section[data-testid="stSidebar"] > div { padding: 28px 22px !important; }

.sb-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.sb-logo { display: flex; align-items: center; gap: 10px; }
.sb-pill { width: 42px; height: 42px; border-radius: 11px; background: linear-gradient(135deg, #DA7B93, #8B2252) !important; display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 0 18px rgba(218,123,147,0.55); }
.sb-name { font-size: 20px; font-weight: 900; background: linear-gradient(90deg, #F4A5BA, #DA7B93); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.sb-role { font-size: 11px; color: rgba(255,255,255,0.40) !important; margin-bottom: 22px; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; }
.prg-label { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.38) !important; text-transform: uppercase; letter-spacing: 1.8px; margin-bottom: 7px; }
.prg-wrap { background: rgba(255,255,255,0.07); border-radius: 100px; height: 5px; margin-bottom: 22px; overflow: hidden; }
.prg-fill { height: 5px; border-radius: 100px; background: linear-gradient(90deg, #DA7B93, #F4A5BA) !important; transition: width 0.5s; box-shadow: 0 0 12px rgba(218,123,147,0.55); }
.step-row { display: flex; align-items: flex-start; gap: 13px; margin-bottom: 4px; position: relative; }
.step-row:not(:last-child) .sc-w::after { content: ''; position: absolute; left: 20px; top: 48px; width: 2px; height: 26px; background: rgba(255,255,255,0.08); border-radius: 2px; }
.step-row.sd:not(:last-child) .sc-w::after { background: rgba(218,123,147,0.45); }
.step-row.sa:not(:last-child) .sc-w::after { background: linear-gradient(180deg, rgba(218,123,147,0.6), transparent); }
.sc-w { position: relative; flex-shrink: 0; }
.sc { width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 800; border: 2px solid rgba(255,255,255,0.10); color: rgba(255,255,255,0.28) !important; background: rgba(255,255,255,0.04); transition: all 0.3s; }
.sc.sa { background: linear-gradient(135deg, #DA7B93, #8B2252) !important; border-color: #F4A5BA !important; color: white !important; box-shadow: 0 0 0 5px rgba(218,123,147,0.18), 0 0 20px rgba(218,123,147,0.55); }
.sc.sd { background: rgba(218,123,147,0.18); border-color: rgba(218,123,147,0.45); color: #F4A5BA !important; }
.si { padding-top: 4px; }
.si-n { font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.28) !important; }
.si-n.sa { color: white !important; font-weight: 800; }
.si-n.sd { color: #F4A5BA !important; }
.si-h { font-size: 12px; color: rgba(255,255,255,0.20) !important; margin-top: 1px; }
.si-h.sa { color: rgba(255,255,255,0.52) !important; }

/* Gradient headings */
.grad-heading { font-size: 1.2rem; font-weight: 800; background: linear-gradient(90deg, #F4A5BA, #DA7B93); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 14px; display: block; }
.grad-heading-green { font-size: 1.2rem; font-weight: 800; background: linear-gradient(90deg, #6EE7B7, #2ECC71); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 14px; display: block; }
.grad-heading-gold { font-size: 1.2rem; font-weight: 800; background: linear-gradient(90deg, #FDE68A, #F59E0B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 14px; display: block; }

/* Glass cards */
.c-card { background: rgba(20,10,25,0.65); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1.5px solid rgba(218,123,147,0.38); border-radius: 18px; padding: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.50), 0 0 18px rgba(218,123,147,0.10); margin-bottom: 16px; }
.c-card-green { background: rgba(5,20,15,0.65); backdrop-filter: blur(14px); border: 1.5px solid rgba(46,204,113,0.45); border-radius: 18px; padding: 22px; box-shadow: 0 8px 28px rgba(0,0,0,0.45), 0 0 16px rgba(46,204,113,0.12); margin-bottom: 14px; }
.c-card-red { background: rgba(25,8,8,0.65); backdrop-filter: blur(14px); border: 1.5px solid rgba(231,76,60,0.45); border-radius: 18px; padding: 22px; box-shadow: 0 8px 28px rgba(0,0,0,0.45), 0 0 16px rgba(231,76,60,0.12); margin-bottom: 14px; }
.c-card-gold { background: rgba(22,16,5,0.65); backdrop-filter: blur(14px); border: 1.5px solid rgba(243,156,18,0.45); border-radius: 18px; padding: 22px; box-shadow: 0 8px 28px rgba(0,0,0,0.45), 0 0 16px rgba(243,156,18,0.12); margin-bottom: 14px; }

/* Skill pills */
.skill-card-match { background: rgba(46,204,113,0.10) !important; border: 1.5px solid rgba(46,204,113,0.50) !important; border-radius: 12px !important; padding: 12px 18px !important; margin-bottom: 8px !important; font-size: 15px !important; color: #6EE7B7 !important; font-weight: 600 !important; box-shadow: 0 0 10px rgba(46,204,113,0.12) !important; }
.skill-card-missing { background: rgba(231,76,60,0.10) !important; border: 1.5px solid rgba(231,76,60,0.48) !important; border-radius: 12px !important; padding: 12px 18px !important; margin-bottom: 8px !important; font-size: 15px !important; color: #FCA5A5 !important; font-weight: 600 !important; box-shadow: 0 0 10px rgba(231,76,60,0.12) !important; }
.skill-card-empty { background: rgba(218,123,147,0.06) !important; border: 1.5px dashed rgba(218,123,147,0.30) !important; border-radius: 12px !important; padding: 18px !important; font-size: 15px !important; color: rgba(255,255,255,0.45) !important; text-align: center !important; }

/* Upload hero */
.up-hero { background: linear-gradient(135deg, rgba(218,123,147,0.18), rgba(139,34,82,0.12)) !important; backdrop-filter: blur(12px); border: 2px dashed rgba(218,123,147,0.50); border-radius: 24px; padding: 54px 40px; text-align: center; margin-bottom: 22px; position: relative; overflow: hidden; box-shadow: 0 0 40px rgba(218,123,147,0.12); }
.uph-icon { font-size: 66px; display: block; margin-bottom: 14px; filter: drop-shadow(0 0 18px rgba(244,165,186,0.50)); }
.uph-title { font-size: 25px; font-weight: 900; margin-bottom: 10px; background: linear-gradient(90deg, #F4A5BA, white); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.uph-sub { font-size: 15px; color: rgba(255,255,255,0.72) !important; line-height: 1.7; }

/* File card */
.fc { background: rgba(218,123,147,0.10); border: 1.5px solid rgba(218,123,147,0.50); border-radius: 14px; padding: 17px 22px; display: flex; align-items: center; gap: 13px; margin: 14px 0; box-shadow: 0 0 16px rgba(218,123,147,0.14); }
.fc-icon { font-size: 30px; }
.fc-name { font-weight: 700; color: white !important; font-size: 15px; }
.fc-size { font-size: 13px; color: rgba(255,255,255,0.60) !important; margin-top: 2px; }

/* Improvement item */
.ic { background: rgba(243,156,18,0.08); border: 1.5px solid rgba(243,156,18,0.38); border-radius: 14px; padding: 15px 18px; margin-bottom: 10px; display: flex; gap: 13px; align-items: flex-start; box-shadow: 0 0 10px rgba(243,156,18,0.08); }
.ic-i { font-size: 22px; flex-shrink: 0; }
.ic-t { font-size: 15px; color: rgba(255,255,255,0.88) !important; line-height: 1.7; }

/* Interview difficulty badges */
.qt { font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 100px; }
.qt.easy { background: rgba(46,204,113,0.14); color: #6EE7B7 !important; border: 1px solid rgba(46,204,113,0.40); }
.qt.medium { background: rgba(243,156,18,0.14); color: #FDE68A !important; border: 1px solid rgba(243,156,18,0.40); }
.qt.hard { background: rgba(231,76,60,0.14); color: #FCA5A5 !important; border: 1px solid rgba(231,76,60,0.40); }
.qt.topic { background: rgba(218,123,147,0.14); color: #F4A5BA !important; border: 1px solid rgba(218,123,147,0.40); }

/* Section badge pill */
.section-badge { display: inline-flex; align-items: center; gap: 7px; background: rgba(218,123,147,0.12); border: 1.5px solid rgba(218,123,147,0.45); border-radius: 100px; padding: 5px 16px; font-size: 11px; font-weight: 700; color: #F4A5BA !important; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 14px; box-shadow: 0 0 12px rgba(218,123,147,0.16); }

/* Buttons */
.stButton > button { font-family: 'Plus Jakarta Sans', sans-serif !important; border-radius: 12px !important; font-size: 15px !important; font-weight: 700 !important; padding: 12px 22px !important; transition: all 0.22s !important; cursor: pointer !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #DA7B93, #8B2252) !important; color: white !important; border: none !important; box-shadow: 0 4px 20px rgba(218,123,147,0.55) !important; }
.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 30px rgba(218,123,147,0.70) !important; }
.stButton > button:not([kind="primary"]) { background: rgba(20,10,25,0.55) !important; color: white !important; border: 1.5px solid rgba(218,123,147,0.40) !important; box-shadow: 0 0 10px rgba(218,123,147,0.14) !important; }
.stButton > button:not([kind="primary"]):hover { border-color: rgba(218,123,147,0.70) !important; background: rgba(218,123,147,0.12) !important; box-shadow: 0 0 18px rgba(218,123,147,0.28) !important; transform: translateY(-2px) !important; }

/* Text area */
.stTextArea textarea { border: 1.5px solid rgba(218,123,147,0.38) !important; border-radius: 14px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 15px !important; color: rgba(255,255,255,0.92) !important; background: rgba(20,10,25,0.60) !important; box-shadow: inset 0 0 20px rgba(0,0,0,0.25) !important; }
.stTextArea textarea:focus { border-color: #DA7B93 !important; box-shadow: 0 0 0 3px rgba(218,123,147,0.20), inset 0 0 20px rgba(0,0,0,0.25) !important; }

/* Metrics */
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.55) !important; font-size: 12px !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.5px; }
[data-testid="stMetricValue"] { color: #F4A5BA !important; font-size: 28px !important; font-weight: 900 !important; text-shadow: 0 0 18px rgba(218,123,147,0.50); }
[data-testid="stMetric"] { background: rgba(20,10,25,0.60) !important; border: 1.5px solid rgba(218,123,147,0.35) !important; border-radius: 16px !important; padding: 16px 14px !important; box-shadow: 0 4px 18px rgba(0,0,0,0.35), 0 0 12px rgba(218,123,147,0.10) !important; }

/* Expanders */
.streamlit-expanderHeader { font-weight: 700 !important; color: #F4A5BA !important; font-size: 15px !important; background: rgba(20,10,25,0.55) !important; border: 1.5px solid rgba(218,123,147,0.35) !important; border-radius: 12px !important; padding: 12px 16px !important; box-shadow: 0 0 10px rgba(218,123,147,0.10) !important; }
.streamlit-expanderContent { background: rgba(15,8,20,0.50) !important; border: 1.5px solid rgba(218,123,147,0.25) !important; border-top: none !important; border-radius: 0 0 12px 12px !important; padding: 14px 16px !important; }

/* Alert boxes */
[data-testid="stAlert"] { border-radius: 14px !important; font-size: 15px !important; backdrop-filter: blur(8px) !important; }

/* Dividers */
hr { border: none !important; height: 1px !important; background: linear-gradient(90deg, transparent, #DA7B93, transparent) !important; margin: 18px 0 !important; opacity: 0.5 !important; }

/* Caption */
.stCaption, [data-testid="stCaptionContainer"] { color: rgba(255,255,255,0.50) !important; font-size: 13px !important; }

/* File uploader */
[data-testid="stFileUploader"] { background: rgba(20,10,25,0.50) !important; border: 2px dashed rgba(218,123,147,0.38) !important; border-radius: 16px !important; padding: 10px !important; }

/* Code */
code { background: rgba(20,10,25,0.65) !important; border: 1px solid rgba(218,123,147,0.30) !important; color: #F4A5BA !important; border-radius: 7px !important; padding: 2px 8px !important; }
</style>
"""

# ─────────────────────────────────────────────────────────────────────
# RECRUITER CSS  —  Teal/Cyan theme
# ─────────────────────────────────────────────────────────────────────
RECRUITER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
* { box-sizing: border-box; }

/* Force background */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(135deg, #071820 0%, #0D2535 55%, #071820 100%) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main > .block-container {
    padding-top: 1.5rem !important; background: transparent !important;
}

/* Typography */
h1 { font-size: 2.1rem !important; font-weight: 900 !important; color: white !important; }
h2 { font-size: 1.6rem !important; font-weight: 800 !important; color: white !important; }
h3 { font-size: 1.25rem !important; font-weight: 700 !important; color: #7EDDE8 !important; }
p, li { font-size: 15px !important; color: rgba(255,255,255,0.85) !important; line-height: 1.75 !important; }
label { color: rgba(255,255,255,0.88) !important; font-size: 15px !important; font-weight: 600 !important; }
strong { color: white !important; }

header[data-testid="stHeader"] { background: rgba(7,24,32,0.85) !important; border-bottom: 1px solid rgba(58,191,208,0.20) !important; backdrop-filter: blur(12px) !important; }
footer, .stDeployButton { display: none !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060F18 0%, #040C14 100%) !important;
    border-right: 2px solid rgba(58,191,208,0.40) !important;
    box-shadow: 4px 0 28px rgba(0,0,0,0.65) !important;
}
section[data-testid="stSidebar"] > div { padding: 28px 22px !important; }

.sb-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.sb-logo { display: flex; align-items: center; gap: 10px; }
.sb-pill { width: 42px; height: 42px; border-radius: 11px; background: linear-gradient(135deg, #3ABFD0, #186690) !important; display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 0 18px rgba(58,191,208,0.55); }
.sb-name { font-size: 20px; font-weight: 900; background: linear-gradient(90deg, #7EDDE8, #3ABFD0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.sb-role { font-size: 11px; color: rgba(255,255,255,0.38) !important; margin-bottom: 22px; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; }
.prg-label { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.36) !important; text-transform: uppercase; letter-spacing: 1.8px; margin-bottom: 7px; }
.prg-wrap { background: rgba(255,255,255,0.07); border-radius: 100px; height: 5px; margin-bottom: 22px; overflow: hidden; }
.prg-fill { height: 5px; border-radius: 100px; background: linear-gradient(90deg, #3ABFD0, #7EDDE8) !important; transition: width 0.5s; box-shadow: 0 0 12px rgba(58,191,208,0.55); }
.step-row { display: flex; align-items: flex-start; gap: 13px; margin-bottom: 4px; position: relative; }
.step-row:not(:last-child) .sc-w::after { content: ''; position: absolute; left: 20px; top: 48px; width: 2px; height: 26px; background: rgba(255,255,255,0.07); border-radius: 2px; }
.step-row.sd:not(:last-child) .sc-w::after { background: rgba(58,191,208,0.42); }
.step-row.sa:not(:last-child) .sc-w::after { background: linear-gradient(180deg, rgba(58,191,208,0.6), transparent); }
.sc-w { position: relative; flex-shrink: 0; }
.sc { width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 800; border: 2px solid rgba(255,255,255,0.09); color: rgba(255,255,255,0.26) !important; background: rgba(255,255,255,0.04); transition: all 0.3s; }
.sc.sa { background: linear-gradient(135deg, #3ABFD0, #186690) !important; border-color: #7EDDE8 !important; color: white !important; box-shadow: 0 0 0 5px rgba(58,191,208,0.18), 0 0 20px rgba(58,191,208,0.55); }
.sc.sd { background: rgba(58,191,208,0.16); border-color: rgba(58,191,208,0.42); color: #7EDDE8 !important; }
.si { padding-top: 4px; }
.si-n { font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.26) !important; }
.si-n.sa { color: white !important; font-weight: 800; }
.si-n.sd { color: #7EDDE8 !important; }
.si-h { font-size: 12px; color: rgba(255,255,255,0.18) !important; margin-top: 1px; }
.si-h.sa { color: rgba(255,255,255,0.50) !important; }

/* Gradient headings */
.grad-heading { font-size: 1.2rem; font-weight: 800; background: linear-gradient(90deg, #7EDDE8, #3ABFD0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 14px; display: block; }
.grad-heading-purple { font-size: 1.2rem; font-weight: 800; background: linear-gradient(90deg, #D8B4FE, #9B59B6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 14px; display: block; }
.grad-heading-green { font-size: 1.2rem; font-weight: 800; background: linear-gradient(90deg, #6EE7B7, #2ECC71); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 14px; display: block; }
.grad-heading-gold { font-size: 1.2rem; font-weight: 800; background: linear-gradient(90deg, #FDE68A, #F59E0B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 14px; display: block; }
.grad-heading-red { font-size: 1.2rem; font-weight: 800; background: linear-gradient(90deg, #FCA5A5, #E74C3C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 14px; display: block; }

/* Glass cards — each section a different accent */
.r-card { background: rgba(5,15,25,0.68); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1.5px solid rgba(58,191,208,0.38); border-radius: 18px; padding: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.55), 0 0 18px rgba(58,191,208,0.08); margin-bottom: 16px; }
.r-card-purple { background: rgba(12,5,25,0.68); backdrop-filter: blur(14px); border: 1.5px solid rgba(155,89,182,0.45); border-radius: 18px; padding: 22px; box-shadow: 0 8px 28px rgba(0,0,0,0.50), 0 0 16px rgba(155,89,182,0.10); margin-bottom: 14px; }
.r-card-red { background: rgba(25,5,5,0.68); backdrop-filter: blur(14px); border: 1.5px solid rgba(231,76,60,0.45); border-radius: 18px; padding: 22px; box-shadow: 0 8px 28px rgba(0,0,0,0.50), 0 0 16px rgba(231,76,60,0.10); margin-bottom: 14px; }
.r-card-green { background: rgba(5,22,14,0.68); backdrop-filter: blur(14px); border: 1.5px solid rgba(46,204,113,0.45); border-radius: 18px; padding: 22px; box-shadow: 0 8px 28px rgba(0,0,0,0.50), 0 0 16px rgba(46,204,113,0.10); margin-bottom: 14px; }
.r-card-gold { background: rgba(22,16,4,0.68); backdrop-filter: blur(14px); border: 1.5px solid rgba(243,156,18,0.45); border-radius: 18px; padding: 22px; box-shadow: 0 8px 28px rgba(0,0,0,0.50), 0 0 16px rgba(243,156,18,0.10); margin-bottom: 14px; }

/* Inline tags */
.bias-tag { display: inline-block; background: rgba(231,76,60,0.12); border: 1.5px solid rgba(231,76,60,0.50); border-radius: 8px; padding: 5px 14px; font-size: 14px; font-weight: 700; color: #FCA5A5 !important; margin: 4px; box-shadow: 0 0 10px rgba(231,76,60,0.16); }
.fix-tag { display: inline-block; background: rgba(46,204,113,0.10); border: 1.5px solid rgba(46,204,113,0.45); border-radius: 8px; padding: 5px 14px; font-size: 14px; font-weight: 700; color: #6EE7B7 !important; margin: 4px; box-shadow: 0 0 10px rgba(46,204,113,0.14); }
.masc-word-tag { display: inline-block; background: rgba(155,89,182,0.10); border: 1.5px solid rgba(155,89,182,0.42); border-radius: 100px; padding: 5px 14px; font-size: 13px; font-weight: 700; color: #D8B4FE !important; margin: 4px; box-shadow: 0 0 8px rgba(155,89,182,0.14); }

/* Quick win */
.quick-win { background: rgba(46,204,113,0.08); border: 1px solid rgba(46,204,113,0.35); border-left: 4px solid #2ECC71; border-radius: 10px; padding: 12px 18px; font-size: 15px; color: rgba(255,255,255,0.88) !important; margin-bottom: 8px; box-shadow: 0 0 10px rgba(46,204,113,0.08); }

/* Section badge */
.section-badge { display: inline-flex; align-items: center; gap: 7px; background: rgba(58,191,208,0.10); border: 1.5px solid rgba(58,191,208,0.42); border-radius: 100px; padding: 5px 16px; font-size: 11px; font-weight: 700; color: #7EDDE8 !important; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 14px; box-shadow: 0 0 12px rgba(58,191,208,0.16); }

/* Change item */
.change-item { background: rgba(5,15,25,0.65); border: 1.5px solid rgba(58,191,208,0.28); border-radius: 12px; padding: 13px 17px; margin-bottom: 8px; box-shadow: 0 0 10px rgba(58,191,208,0.06); }
.change-from { text-decoration: line-through; color: rgba(252,165,165,0.80) !important; font-size: 14px; }
.change-to { color: #6EE7B7 !important; font-size: 14px; font-weight: 700; }

/* Buttons */
.stButton > button { font-family: 'Plus Jakarta Sans', sans-serif !important; border-radius: 12px !important; font-size: 15px !important; font-weight: 700 !important; padding: 12px 22px !important; transition: all 0.22s !important; cursor: pointer !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #3ABFD0, #186690) !important; color: white !important; border: none !important; box-shadow: 0 4px 20px rgba(58,191,208,0.55) !important; }
.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 30px rgba(58,191,208,0.70) !important; }
.stButton > button:not([kind="primary"]) { background: rgba(5,15,25,0.60) !important; color: white !important; border: 1.5px solid rgba(58,191,208,0.38) !important; box-shadow: 0 0 10px rgba(58,191,208,0.12) !important; }
.stButton > button:not([kind="primary"]):hover { border-color: rgba(58,191,208,0.68) !important; background: rgba(58,191,208,0.12) !important; box-shadow: 0 0 18px rgba(58,191,208,0.26) !important; transform: translateY(-2px) !important; }

/* Text area */
.stTextArea textarea { border: 1.5px solid rgba(58,191,208,0.36) !important; border-radius: 14px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 15px !important; color: rgba(255,255,255,0.92) !important; background: rgba(5,15,25,0.65) !important; box-shadow: inset 0 0 20px rgba(0,0,0,0.30) !important; }
.stTextArea textarea:focus { border-color: #3ABFD0 !important; box-shadow: 0 0 0 3px rgba(58,191,208,0.18), inset 0 0 20px rgba(0,0,0,0.30) !important; }

/* Metrics */
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.52) !important; font-size: 12px !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.5px; }
[data-testid="stMetricValue"] { color: #7EDDE8 !important; font-size: 28px !important; font-weight: 900 !important; text-shadow: 0 0 18px rgba(58,191,208,0.50); }
[data-testid="stMetric"] { background: rgba(5,15,25,0.65) !important; border: 1.5px solid rgba(58,191,208,0.32) !important; border-radius: 16px !important; padding: 16px 14px !important; box-shadow: 0 4px 18px rgba(0,0,0,0.40), 0 0 12px rgba(58,191,208,0.08) !important; }

/* Expanders */
.streamlit-expanderHeader { font-weight: 700 !important; color: #7EDDE8 !important; font-size: 15px !important; background: rgba(5,15,25,0.60) !important; border: 1.5px solid rgba(58,191,208,0.32) !important; border-radius: 12px !important; padding: 12px 16px !important; box-shadow: 0 0 10px rgba(58,191,208,0.08) !important; }
.streamlit-expanderContent { background: rgba(5,12,20,0.55) !important; border: 1.5px solid rgba(58,191,208,0.22) !important; border-top: none !important; border-radius: 0 0 12px 12px !important; padding: 14px 16px !important; }

/* Alert boxes */
[data-testid="stAlert"] { border-radius: 14px !important; font-size: 15px !important; backdrop-filter: blur(8px) !important; }

/* Dividers */
hr { border: none !important; height: 1px !important; background: linear-gradient(90deg, transparent, #3ABFD0, transparent) !important; margin: 18px 0 !important; opacity: 0.45 !important; }

/* Caption */
.stCaption, [data-testid="stCaptionContainer"] { color: rgba(255,255,255,0.48) !important; font-size: 13px !important; }

/* File uploader */
[data-testid="stFileUploader"] { background: rgba(5,15,25,0.55) !important; border: 2px dashed rgba(58,191,208,0.36) !important; border-radius: 16px !important; padding: 10px !important; }

/* Code */
code { background: rgba(5,15,25,0.70) !important; border: 1px solid rgba(58,191,208,0.28) !important; color: #7EDDE8 !important; border-radius: 7px !important; padding: 2px 8px !important; }
</style>
"""


def generate_stars_html(n=60):
    s = ""
    for _ in range(n):
        sz = random.uniform(1.2, 3)
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        d = random.uniform(2, 8)
        dl = random.uniform(0, 5)
        col = random.choice(["rgba(70,197,211,0.7)", "rgba(218,123,147,0.7)", "rgba(255,255,255,0.6)"])
        s += (f'<div style="position:absolute;width:{sz}px;height:{sz}px;'
              f'border-radius:50%;background:{col};'
              f'left:{x}%;top:{y}%;animation:tw {d}s {dl}s infinite linear;"></div>')
    return (f'<style>@keyframes tw{{0%,100%{{opacity:.1}}50%{{opacity:.9}}}}</style>'
            f'<div style="position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden;">{s}</div>')