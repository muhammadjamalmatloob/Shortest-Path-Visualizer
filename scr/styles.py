"""
styles.py
---------
Global CSS for the Shortest Path Visualizer app.
Call inject_styles() once at the top of app.py.
"""

import streamlit as st


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f7f3ee;
}

/* Sidebar */

[data-testid="stSidebar"] h2 {
    color: #1a0533;
}

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #ffffff 0%, #f0eaff 100%);
    border-right: 2px solid #e0d5f5;
    
}
[data-testid="stSidebar"] .stButton button {
    width: 100%;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    border: none;
    transition: all 0.18s;
}
[data-testid="stSidebar"] .stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    background-color: #4a4a4a !important;
    color: #ffffff !important;
}

/* Main title */
h1 { font-family: 'DM Sans', sans-serif; font-weight: 800; color: #1a0533; letter-spacing: -1px; }
h2, h3 { font-family: 'DM Sans', sans-serif; font-weight: 700; color: #2d1b69; }

/* Metric cards */
[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-left: 4px solid #7c3aed;
}

/* Step card styling */
.step-card {
    background: white;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 8px 0;
    border-left: 5px solid #10b981;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    color: #1a0533;
    transition: all 0.2s;
}
.step-card.relax  { border-left-color: #10b981; }
.step-card.visit  { border-left-color: #f59e0b; }
.step-card.final  { border-left-color: #7c3aed; background: #f5f0ff; font-weight: 700; }
.step-card.init   { border-left-color: #3b82f6; }

/* Dist table */
.dist-table {
    display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0;
}
.dist-cell {
    background: #ede9fe;
    border-radius: 8px;
    padding: 6px 12px;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    color: #4c1d95;
    border: 1.5px solid #c4b5fd;
}
.dist-cell.updated {
    background: #d1fae5;
    border-color: #34d399;
    color: #064e3b;
}

/* Info boxes */
.info-box {
    background: linear-gradient(135deg, #ede9fe, #dbeafe);
    border-radius: 12px;
    padding: 16px 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.83rem;
    color: #1e1b4b;
    margin-bottom: 16px;
}
.path-highlight {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    border-radius: 12px;
    padding: 14px 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: #064e3b;
    font-weight: 700;
    margin-top: 10px;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
}

/* Section dividers */
.section-head {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #7c3aed;
    margin: 18px 0 6px 0;
}

/* Algorithm badge */
.algo-badge {
    display: inline-block;
    background: #7c3aed;
    color: white;
    border-radius: 20px;
    padding: 4px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Dark labels for radio buttons, checkboxes, and all sidebar form labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    color: #1a0533 !important;
    font-weight: 500;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] .stCheckbox [data-testid="stMarkdownContainer"] p {
    color: #1a0533 !important;
}
</style>
"""


def inject_styles():
    """Inject the global CSS into the Streamlit page."""
    st.markdown(CSS, unsafe_allow_html=True)
