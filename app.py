"""
The Confidence Trap — Streamlit entry point.

A practitioner evidence brief on AI-generated healthcare chart explanations.
Companion digital artefact to the BSc dissertation:
  "Evaluating LLM-Generated Explanations for Healthcare Data Visualisations"
  Amina ElShazly, University of Sheffield, IJC319 (2026).

Run with: streamlit run app.py
"""

import streamlit as st

from components import inject_styles, render_masthead
from pages_content import home, explorer, dashboard, findings, pitfalls


# ============================================================================
# PAGE CONFIG (must be first Streamlit call)
# ============================================================================
st.set_page_config(
    page_title="The Confidence Trap",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# STYLES
# ============================================================================
inject_styles()


# ============================================================================
# SIDEBAR NAV
# ============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 16px 0 24px; border-bottom: 1px solid rgba(244,237,226,0.2); margin-bottom: 24px;">
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.25em;
                      color: rgba(244,237,226,0.5); margin-bottom: 8px;">EVIDENCE BRIEF</div>
          <div style="font-family: 'Fraunces', serif; font-size: 28px; font-weight: 300;
                      line-height: 1; letter-spacing: -0.02em;">The Confidence Trap</div>
          <div style="font-family: 'Fraunces', serif; font-style: italic; font-size: 13px;
                      color: rgba(244,237,226,0.7); margin-top: 12px; line-height: 1.4;">
            Guidelines for AI-generated healthcare chart explanations
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-family: \'Fraunces\', serif; color: rgba(244,237,226,0.7); '
        'font-size: 14px; margin-bottom: 8px;">Navigate to:</div>',
        unsafe_allow_html=True,
    )

    selected = st.radio(
        "Section",
        [
            "🏠 Home",
            "🔍 Visualisation Explorer",
            "📈 Model Evaluation Dashboard",
            "💡 Findings & Guidance",
            "⚠️ Common Pitfalls",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div style="padding: 32px 0 16px; border-top: 1px solid rgba(244,237,226,0.2); margin-top: 32px;">
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 0.2em;
                      color: rgba(244,237,226,0.5); margin-bottom: 8px;">SOURCE</div>
          <div style="font-family: 'Fraunces', serif; font-size: 12px; line-height: 1.5;
                      color: rgba(244,237,226,0.8);">
            ElShazly, A. (2026).<br>
            <em>Evaluating LLM-Generated Explanations for Healthcare Data Visualisations.</em><br>
            University of Sheffield, IJC319.<br><br>
            Supervisor: Harry Kai-Ho Chan
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# MASTHEAD (every page)
# ============================================================================
render_masthead()


# ============================================================================
# ROUTING
# ============================================================================
_PAGE_MAP = {
    "🏠 Home": home,
    "🔍 Visualisation Explorer": explorer,
    "📈 Model Evaluation Dashboard": dashboard,
    "💡 Findings & Guidance": findings,
    "⚠️ Common Pitfalls": pitfalls,
}

_PAGE_MAP[selected].render()
