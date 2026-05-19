"""All custom CSS for the Confidence Trap app — editorial/clinical aesthetic."""

import streamlit as st


_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400&family=JetBrains+Mono:wght@400;500;700&family=Inter+Tight:wght@400;500;600;700&display=swap');

  :root {
    --paper: #f4ede2;
    --paper-deep: #ebe1d0;
    --ink: #1a1612;
    --ink-soft: #443a30;
    --ink-faint: #7a6f5f;
    --rule: #c9bfae;
    --accent: #b8341c;
    --accent-deep: #8a2614;
    --accent-soft: #f5d5cc;
    --good: #2d5f3f;
    --good-soft: #d4e3d8;
    --warn: #c08820;
  }

  .stApp {
    background: #f4ede2;
    background-image:
      radial-gradient(ellipse at top left, rgba(184, 52, 28, 0.04) 0%, transparent 50%),
      radial-gradient(ellipse at bottom right, rgba(45, 95, 63, 0.03) 0%, transparent 50%);
  }
  .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1280px; }

  html, body, [class*="css"] { font-family: 'Fraunces', Georgia, serif; color: #1a1612; }
  h1 { font-family: 'Fraunces', serif !important; font-weight: 300 !important; letter-spacing: -0.03em !important; line-height: 1 !important; color: #1a1612 !important; }
  h2 { font-family: 'Fraunces', serif !important; font-weight: 400 !important; letter-spacing: -0.02em !important; color: #1a1612 !important; }
  h3 { font-family: 'Fraunces', serif !important; font-weight: 500 !important; color: #1a1612 !important; }
  p, li, span, div { font-family: 'Fraunces', serif; color: #1a1612; }

  /* Sidebar */
  [data-testid="stSidebar"] { background: #1a1612; }
  [data-testid="stSidebar"] * { color: #f4ede2 !important; }
  [data-testid="stSidebar"] .stRadio > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
  }
  [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #f4ede2 !important; }

  /* Masthead */
  .masthead {
    border-top: 1px solid #c9bfae;
    border-bottom: 1px solid #c9bfae;
    padding: 14px 0;
    margin-bottom: 48px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7a6f5f;
    display: flex;
    justify-content: space-between;
  }
  .masthead-dot {
    display: inline-block; width: 6px; height: 6px;
    background: #b8341c; border-radius: 50%;
    margin-right: 8px; vertical-align: middle;
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

  /* Section markers */
  .sectnum {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; letter-spacing: 0.25em;
    color: #b8341c;
    margin-bottom: 16px; margin-top: 32px;
    display: flex; align-items: center; gap: 12px;
    text-transform: uppercase;
  }
  .sectnum::before { content: ''; width: 24px; height: 1px; background: #b8341c; }

  .eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; letter-spacing: 0.3em;
    color: #b8341c; text-transform: uppercase; margin-bottom: 24px;
  }

  /* Hero */
  .hero-title {
    font-family: 'Fraunces', serif; font-weight: 300;
    font-size: clamp(40px, 6vw, 72px);
    line-height: 0.98; letter-spacing: -0.035em;
    margin-bottom: 32px; color: #1a1612;
  }
  .hero-title em { font-style: italic; color: #b8341c; font-weight: 400; }
  .hero-title .strike { position: relative; display: inline-block; }
  .hero-title .strike::after {
    content: ''; position: absolute;
    left: -4%; right: -4%; top: 52%;
    height: 4px; background: #b8341c; transform: rotate(-2deg);
  }
  .deck {
    font-family: 'Fraunces', serif; font-style: italic;
    font-size: 20px; line-height: 1.5;
    color: #443a30; margin-bottom: 48px; max-width: 820px;
  }

  /* Findings */
  .finding {
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid #c9bfae;
    padding: 32px; margin-bottom: 16px;
    min-height: 280px;
  }
  .finding.critical { background: #b8341c; color: #f4ede2; border-color: #8a2614; }
  .finding.critical .finding-label, .finding.critical .finding-detail, .finding.critical .finding-suffix { color: rgba(244, 237, 226, 0.85); }
  .finding-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.25em; text-transform: uppercase;
    color: #7a6f5f; margin-bottom: 20px;
    display: flex; justify-content: space-between;
  }
  .finding-stat {
    font-family: 'Fraunces', serif; font-weight: 300;
    font-size: 68px; line-height: 0.9; letter-spacing: -0.04em;
    margin-bottom: 16px;
  }
  .finding-suffix { font-size: 24px; color: #7a6f5f; font-weight: 400; }
  .finding-headline {
    font-family: 'Fraunces', serif; font-size: 18px; font-weight: 500;
    line-height: 1.25; margin-bottom: 12px;
  }
  .finding-headline em { color: #b8341c; font-style: italic; }
  .finding.critical .finding-headline em {
    color: #f4ede2; text-decoration: underline;
    text-decoration-thickness: 1px; text-underline-offset: 4px;
  }
  .finding-detail {
    font-family: 'Inter Tight', sans-serif;
    font-size: 13px; line-height: 1.6; color: #443a30;
  }

  /* Chart cards (used in Explorer drill-down list) */
  .chart-card {
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid #c9bfae;
    padding: 16px; margin-bottom: 12px;
    display: flex; gap: 16px; align-items: center;
    transition: all 0.2s ease;
  }
  .chart-card:hover { border-color: #1a1612; }
  .chart-card-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px; font-weight: 700; color: #b8341c;
    min-width: 40px;
  }
  .chart-card-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.15em; text-transform: uppercase;
    color: #7a6f5f; margin-bottom: 4px;
  }
  .chart-card-title {
    font-family: 'Fraunces', serif;
    font-size: 14px; line-height: 1.4; color: #1a1612;
  }

  /* AI explanation panel (with error highlights) */
  .ai-panel {
    background: rgba(255, 255, 255, 0.65);
    border-left: 3px solid #b8341c;
    padding: 20px 24px;
    font-family: 'Fraunces', serif;
    font-size: 15px; line-height: 1.65; color: #1a1612;
  }
  .ai-panel .err {
    background: #f5d5cc;
    border-bottom: 2px solid #b8341c;
    padding: 0 2px;
  }
  .ai-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.25em; text-transform: uppercase;
    color: #b8341c; margin-bottom: 12px;
  }
  .ai-label::before { content: '● '; }

  .source-panel {
    background: rgba(255, 255, 255, 0.5);
    border-left: 3px solid #2d5f3f;
    padding: 20px 24px;
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 14.5px; line-height: 1.6; color: #443a30;
  }
  .source-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.25em; text-transform: uppercase;
    color: #2d5f3f; margin-bottom: 12px;
  }
  .source-label::before { content: '● '; }

  /* Score badges */
  .score-grid {
    display: flex; gap: 4px; flex-wrap: wrap;
  }
  .score-cell {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; font-weight: 700;
    width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 2px;
    letter-spacing: 0.02em;
  }
  .score-pass { background: #d4e3d8; color: #2d5f3f; }
  .score-fail { background: #f5d5cc; color: #8a2614; }
  .score-row-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.2em; text-transform: uppercase;
    color: #7a6f5f; min-width: 70px; padding-right: 12px;
  }

  /* Big metric */
  .bigmetric { text-align: center; padding: 24px 16px; }
  .bigmetric-value {
    font-family: 'Fraunces', serif; font-weight: 300;
    font-size: 56px; line-height: 1; letter-spacing: -0.03em;
    color: #1a1612;
  }
  .bigmetric-suffix { font-size: 22px; color: #7a6f5f; }
  .bigmetric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px; letter-spacing: 0.25em; text-transform: uppercase;
    color: #7a6f5f; margin-top: 8px;
  }

  /* Guideline cards */
  .guideline-card {
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid #c9bfae;
    padding: 28px 32px 28px 80px;
    margin-bottom: 16px; position: relative;
  }
  .guideline-num {
    position: absolute; left: 28px; top: 30px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px; font-weight: 700; color: #b8341c; letter-spacing: 0.05em;
  }
  .guideline-title {
    font-family: 'Fraunces', serif;
    font-size: 19px; font-weight: 500;
    line-height: 1.25; margin-bottom: 8px; color: #1a1612;
  }
  .guideline-body {
    font-family: 'Inter Tight', sans-serif;
    font-size: 13.5px; line-height: 1.6; color: #443a30;
  }
  .guideline-body strong { color: #1a1612; }

  /* Audience header */
  .audience-header {
    padding: 24px 0 8px; border-top: 2px solid #1a1612; margin-bottom: 24px;
  }
  .audience-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.3em; text-transform: uppercase;
    color: #7a6f5f; margin-bottom: 8px;
  }
  .audience-name {
    font-family: 'Fraunces', serif;
    font-size: 30px; font-weight: 400; line-height: 1.1; margin-bottom: 6px;
  }
  .audience-name em { font-style: italic; color: #b8341c; }
  .audience-tagline {
    font-family: 'Fraunces', serif; font-style: italic;
    font-size: 15px; color: #7a6f5f; margin-bottom: 16px;
  }

  /* Pitfalls */
  .redflag {
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid #c9bfae;
    padding: 20px 24px; margin-bottom: 12px; position: relative;
  }
  .redflag-code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; font-weight: 700; letter-spacing: 0.15em;
    color: #b8341c; margin-bottom: 6px;
  }
  .redflag-rate {
    position: absolute; top: 20px; right: 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: #7a6f5f; letter-spacing: 0.05em;
  }
  .redflag-title {
    font-family: 'Fraunces', serif;
    font-size: 16px; font-weight: 500; line-height: 1.3;
    margin-bottom: 6px; padding-right: 60px;
  }
  .redflag-detail {
    font-family: 'Inter Tight', sans-serif;
    font-size: 12.5px; line-height: 1.55; color: #443a30;
  }

  /* Hide Streamlit chrome */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  header { visibility: hidden; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { gap: 0; border-bottom: 1px solid #c9bfae; }
  .stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important; letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 14px 24px !important;
    background: transparent !important;
    border-radius: 0 !important;
    color: #7a6f5f !important;
  }
  .stTabs [aria-selected="true"] { background: #1a1612 !important; color: #f4ede2 !important; }

  /* Selectbox + multiselect cleanup */
  .stSelectbox label, .stMultiSelect label, .stSlider label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #7a6f5f !important;
  }

  /* Section divider */
  .sect-divider { border-top: 1px solid #c9bfae; margin: 56px 0 0 0; }

  /* Expander */
  .streamlit-expanderHeader {
    font-family: 'Fraunces', serif !important;
    font-style: italic !important;
  }
</style>
"""


def inject_styles() -> None:
    """Inject the app's custom CSS into the current Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)
