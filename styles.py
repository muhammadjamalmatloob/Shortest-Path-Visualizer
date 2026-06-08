"""
styles.py
---------
Global CSS for the Shortest Path Visualizer app.
Call inject_styles() once at the top of app.py.
Theme inspired by App.css (Sentix design system).
"""

import streamlit as st


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── Design tokens (mirrors App.css) ── */
:root {
    --bg-deep:        #06040f;
    --bg-card:        rgba(14, 10, 28, 0.85);
    --bg-surface:     rgba(24, 18, 48, 0.90);
    --bg-input:       rgba(255, 255, 255, 0.04);
    --accent:         #9b5de5;
    --accent-bright:  #c77dff;
    --accent-hot:     #f72585;
    --accent-teal:    #4cc9f0;
    --accent-glow:    rgba(155, 93, 229, 0.35);
    --accent-dim:     rgba(155, 93, 229, 0.50);
    --accent-subtle:  rgba(155, 93, 229, 0.10);
    --success:        #0bf0a8;
    --warning:        #ffbe0b;
    --text-primary:   #f2eeff;
    --text-secondary: #a89cc8;
    --text-muted:     #5c5178;
    --font-main:      'Plus Jakarta Sans', sans-serif;
    --font-display:   'Space Grotesk', sans-serif;
    --font-mono:      'Space Mono', monospace;
    --radius-sm:      8px;
    --radius-md:      14px;
    --radius-lg:      22px;
    --dur-fast:       180ms;
    --ease-snap:      cubic-bezier(0.4, 0, 0.2, 1);
    --ease-spring:    cubic-bezier(0.16, 1, 0.3, 1);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: var(--font-main);
    background-color: var(--bg-deep);
    color: var(--text-primary);
}

/* ── Main app background — radial glow like Sentix ── */
.stApp {
    background:
        radial-gradient(circle at 15% 0%,   rgba(155, 93, 229, 0.17), transparent 32rem),
        radial-gradient(circle at 85% 18%,  rgba(76, 201, 240, 0.09), transparent 30rem),
        var(--bg-deep);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(6, 4, 15, 0.92);
    border-right: 1px solid rgba(155, 93, 229, 0.18);
    backdrop-filter: blur(24px);
}

[data-testid="stSidebar"] h2 {
    font-family: var(--font-display);
    color: var(--text-primary);
    font-weight: 700;
}

/* ── Sidebar buttons — base ── */
[data-testid="stSidebar"] .stButton button {
    width: 100%;
    border-radius: var(--radius-sm);
    font-family: var(--font-main);
    font-size: 0.85rem;
    font-weight: 700;
    border: 1px solid rgba(155, 93, 229, 0.22);
    background: rgba(255, 255, 255, 0.04);
    color: var(--text-secondary);
    transition: all var(--dur-fast) var(--ease-snap);
}
[data-testid="stSidebar"] .stButton button:hover {
    transform: translateY(-2px);
    background: rgba(155, 93, 229, 0.12) !important;
    border-color: rgba(155, 93, 229, 0.45) !important;
    color: var(--text-primary) !important;
    box-shadow: 0 6px 20px rgba(155, 93, 229, 0.28);
}

/* ── Primary "Run Algorithm" button ── */
[data-testid="stSidebar"] button[data-testid="baseButton-primary"],
[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), #6a0dad) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 8px 24px rgba(155, 93, 229, 0.30);
}
[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover,
[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(155, 93, 229, 0.45) !important;
    background: linear-gradient(135deg, var(--accent-bright), var(--accent)) !important;
}

/* ── Sidebar inputs ── */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stTextInput input {
    background: var(--bg-input) !important;
    border: 1px solid rgba(155, 93, 229, 0.22) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-main) !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(155, 93, 229, 0.20) !important;
}

/* ── Sidebar selectbox ── */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: var(--bg-input) !important;
    border: 1px solid rgba(155, 93, 229, 0.22) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Sidebar labels & text ── */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] p {
    color: var(--text-secondary) !important;
    font-family: var(--font-main) !important;
    font-weight: 500;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] .stCheckbox [data-testid="stMarkdownContainer"] p {
    color: var(--text-secondary) !important;
}

/* ── Main panel headings ── */
h1 {
    font-family: var(--font-display);
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}
h2, h3 {
    font-family: var(--font-display);
    font-weight: 600;
    color: var(--accent-bright);
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--bg-card);
    border-radius: var(--radius-md);
    padding: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(155, 93, 229, 0.20);
    border-left: 4px solid var(--accent);
    backdrop-filter: blur(12px);
}
[data-testid="metric-container"] label,
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-family: var(--font-main) !important;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
    font-weight: 700;
}

/* ── Graph canvas wrapper — glow border, no white outline ── */
iframe {
    border: none !important;
    outline: none !important;
    border-radius: var(--radius-md) !important;
    box-shadow:
        0 0 0 1px rgba(155, 93, 229, 0.30),
        0 0 28px rgba(155, 93, 229, 0.18),
        0 0 70px rgba(76, 201, 240, 0.07),
        0 16px 48px rgba(0, 0, 0, 0.45) !important;
}

/* ── Step cards ── */
.step-card {
    background: var(--bg-card);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    margin: 8px 0;
    border-left: 5px solid var(--success);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.30);
    border-top: 1px solid rgba(155, 93, 229, 0.12);
    border-right: 1px solid rgba(155, 93, 229, 0.12);
    font-family: var(--font-mono);
    font-size: 0.82rem;
    color: var(--text-primary);
    backdrop-filter: blur(12px);
    transition: all var(--dur-fast);
}
.step-card.relax  { border-left-color: var(--success); }
.step-card.visit  { border-left-color: var(--warning); }
.step-card.final  {
    border-left-color: var(--accent);
    background: rgba(155, 93, 229, 0.08);
    font-weight: 700;
    color: var(--accent-bright);
    box-shadow: 0 0 24px rgba(155, 93, 229, 0.15), 0 4px 20px rgba(0,0,0,0.30);
}
.step-card.init   { border-left-color: var(--accent-teal); }

/* ── Distance table ── */
.dist-table {
    display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0;
}
.dist-cell {
    background: rgba(155, 93, 229, 0.10);
    border-radius: var(--radius-sm);
    padding: 6px 12px;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--accent-bright);
    border: 1px solid rgba(155, 93, 229, 0.25);
}
.dist-cell.updated {
    background: rgba(11, 240, 168, 0.10);
    border-color: rgba(11, 240, 168, 0.40);
    color: var(--success);
}

/* ── Info / path boxes ── */
.info-box {
    background: var(--bg-card);
    border: 1px solid rgba(155, 93, 229, 0.20);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    font-family: var(--font-mono);
    font-size: 0.83rem;
    color: var(--text-secondary);
    margin-bottom: 16px;
    backdrop-filter: blur(12px);
}
.path-highlight {
    background: rgba(11, 240, 168, 0.07);
    border: 1px solid rgba(11, 240, 168, 0.30);
    border-radius: var(--radius-md);
    padding: 14px 20px;
    font-family: var(--font-mono);
    font-size: 0.9rem;
    color: var(--success);
    font-weight: 700;
    margin-top: 10px;
    box-shadow: 0 0 20px rgba(11, 240, 168, 0.08);
}

/* ── Section dividers ── */
.section-head {
    font-family: var(--font-main);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 18px 0 6px 0;
}

/* ── Algorithm badge ── */
.algo-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--accent), #6a0dad);
    color: white;
    border-radius: 999px;
    padding: 5px 16px;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(155, 93, 229, 0.30);
    letter-spacing: 0.03em;
}

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div {
    background: rgba(155, 93, 229, 0.15) !important;
    border-radius: 999px;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent-bright)) !important;
    border-radius: 999px;
    box-shadow: 0 0 10px rgba(155, 93, 229, 0.40);
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid rgba(155, 93, 229, 0.18) !important;
    border-radius: var(--radius-md) !important;
    backdrop-filter: blur(12px);
}
[data-testid="stExpander"] summary {
    color: var(--text-secondary) !important;
    font-family: var(--font-main) !important;
    font-weight: 600;
}

/* ── Divider ── */
hr {
    border-color: rgba(155, 93, 229, 0.18) !important;
}

/* ── Main panel nav buttons (|< < > >|) ── */
.stButton button {
    background: rgba(255, 255, 255, 0.04);
    color: var(--text-secondary);
    border: 1px solid rgba(155, 93, 229, 0.22);
    border-radius: var(--radius-sm);
    font-family: var(--font-main);
    font-weight: 700;
    transition: all var(--dur-fast) var(--ease-snap);
}
.stButton button:hover {
    background: rgba(155, 93, 229, 0.12) !important;
    color: var(--text-primary) !important;
    border-color: rgba(155, 93, 229, 0.45) !important;
    box-shadow: 0 4px 16px rgba(155, 93, 229, 0.25);
    transform: translateY(-1px);
}

/* ── General text ── */
p, span, div {
    color: var(--text-primary);
    font-family: var(--font-main);
}
</style>
"""


def inject_styles():
    """Inject the global CSS into the Streamlit page."""
    st.markdown(CSS, unsafe_allow_html=True)