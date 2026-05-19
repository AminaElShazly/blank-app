"""
Data loader for the Confidence Trap app.

Reads `data/charts.csv` once per session (cached by Streamlit) and exposes
typed helpers used by the page modules.
"""

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / 'data' / 'charts.csv'
CHARTS_DIR = ROOT / 'assets' / 'charts'

# The nine error-taxonomy codes, in the order they appear in the dissertation.
ERROR_CODES = ['fe1', 'fe2', 'fe3a', 'fe3b', 'fe4', 'fe5', 'hm1', 'hm2', 'oe1']
ERROR_LABELS = {
    'fe1': 'FE1 — Value error',
    'fe2': 'FE2 — Label error',
    'fe3a': 'FE3A — Trend direction',
    'fe3b': 'FE3B — Trend pattern',
    'fe4': 'FE4 — Magnitude error',
    'fe5': 'FE5 — Extremum error',
    'hm1': 'HM1 — Fabricated content',
    'hm2': 'HM2 — Unsupported inference',
    'oe1': 'OE1 — Critical omission',
}
ERROR_DESCRIPTIONS = {
    'fe1': 'A numerical value in the explanation does not match the chart.',
    'fe2': 'An axis or category label is named incorrectly.',
    'fe3a': 'A trend direction (rise / fall / flat) is reversed.',
    'fe3b': 'A trend pattern (linear / curved / volatile) is misdescribed.',
    'fe4': 'The magnitude of a difference or change is misstated.',
    'fe5': 'The highest or lowest value is misidentified.',
    'hm1': 'A data point, year, or entity that is not on the chart appears in the text.',
    'hm2': 'An unsupported causal or interpretive claim is added.',
    'oe1': 'A finding central to the chart is omitted from the explanation.',
}

# The ten checklist items.
CHECKLIST_CODES = [f'c{i}' for i in range(1, 11)]
CHECKLIST_LABELS = {
    'c1': 'C1 — Chart type named correctly',
    'c2': 'C2 — X-axis identified',
    'c3': 'C3 — Y-axis identified',
    'c4': 'C4 — Highest value correct',
    'c5': 'C5 — Lowest value correct',
    'c6': 'C6 — Trend direction correct',
    'c7': 'C7 — Trend pattern correct',
    'c8': 'C8 — Comparisons accurate',
    'c9': 'C9 — No fabrication',
    'c10': 'C10 — Captures primary finding',
}


@st.cache_data
def load_charts() -> pd.DataFrame:
    """Load the 45-chart dataset. Cached across reruns."""
    return pd.read_csv(DATA_PATH)


def get_chart(chart_id: int) -> pd.Series:
    """Return one chart's row by ID (1–45)."""
    df = load_charts()
    return df.loc[df['chart_id'] == chart_id].iloc[0]


def image_path(chart_id: int) -> Path:
    """Resolve the on-disk path to a chart's image."""
    return CHARTS_DIR / f'viz{chart_id}.jpg'


def error_summary(df: pd.DataFrame, model: str) -> dict:
    """
    Return a dict of {error_code: chart_count} for a model across the
    given subset of charts. Used by the Dashboard's aggregate view.
    """
    return {code: int(df[f'{model}_{code}'].sum()) for code in ERROR_CODES}


def checklist_summary(df: pd.DataFrame, model: str) -> dict:
    """Return a dict of {checklist_code: chart_count_passing}."""
    return {code: int(df[f'{model}_{code}'].sum()) for code in CHECKLIST_CODES}
