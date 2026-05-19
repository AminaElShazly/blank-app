"""🔍 Visualisation Explorer — browse the 45 study charts."""

import streamlit as st

from data.loader import load_charts
from components.score_grid import render_chart_detail


def render() -> None:
    """Render the Visualisation Explorer page."""
    df = load_charts()

    st.markdown('<div class="sectnum">VISUALISATION EXPLORER</div>', unsafe_allow_html=True)
    st.markdown(
        """
        ## All 45 healthcare charts from the study.

        Filter by chart type and complexity, pick a chart, and see the source paper's caption
        alongside both AI explanations and their checklist + error-taxonomy scoring.
        """
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # ============================================================
    # FILTERS
    # ============================================================
    fcol1, fcol2, fcol3 = st.columns([1, 1, 2])

    with fcol1:
        chart_types = st.multiselect(
            "Chart type",
            options=['bar', 'line', 'scatter'],
            default=['bar', 'line', 'scatter'],
            key='filter_type',
        )
    with fcol2:
        complexities = st.multiselect(
            "Complexity",
            options=['simple', 'moderate', 'complex'],
            default=['simple', 'moderate', 'complex'],
            key='filter_complexity',
        )
    with fcol3:
        sort_by = st.selectbox(
            "Sort by",
            options=[
                'Chart ID (1 → 45)',
                'GPT-4o accuracy (high → low)',
                'GPT-4o accuracy (low → high)',
                'Claude accuracy (high → low)',
                'Claude accuracy (low → high)',
                'GPT-4o vs Claude gap (biggest first)',
            ],
            key='filter_sort',
        )

    # Apply filters
    filtered = df[
        df['chart_type'].isin(chart_types)
        & df['complexity'].isin(complexities)
    ].copy()

    # Apply sort
    if sort_by == 'Chart ID (1 → 45)':
        filtered = filtered.sort_values('chart_id')
    elif sort_by == 'GPT-4o accuracy (high → low)':
        filtered = filtered.sort_values('gpt4o_total', ascending=False)
    elif sort_by == 'GPT-4o accuracy (low → high)':
        filtered = filtered.sort_values('gpt4o_total', ascending=True)
    elif sort_by == 'Claude accuracy (high → low)':
        filtered = filtered.sort_values('claude_total', ascending=False)
    elif sort_by == 'Claude accuracy (low → high)':
        filtered = filtered.sort_values('claude_total', ascending=True)
    elif sort_by == 'GPT-4o vs Claude gap (biggest first)':
        filtered = filtered.assign(gap=(filtered['gpt4o_total'] - filtered['claude_total']).abs())
        filtered = filtered.sort_values('gap', ascending=False)

    st.markdown(
        f"""
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px;
                    letter-spacing: 0.2em; text-transform: uppercase; color: #7a6f5f;
                    margin-top: 16px; margin-bottom: 8px;">
          {len(filtered)} of {len(df)} charts shown
        </div>
        """,
        unsafe_allow_html=True,
    )

    if len(filtered) == 0:
        st.warning("No charts match the current filters. Adjust filters above.")
        return

    # ============================================================
    # CHART PICKER
    # ============================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)

    # Build human-readable labels for the selectbox
    def make_label(row):
        return (
            f"#{int(row['chart_id']):02d} · {row['chart_type']:<7s} · "
            f"{row['complexity']:<8s} · GPT {int(row['gpt4o_total'])}/10 · "
            f"Claude {int(row['claude_total'])}/10 · {row['title'][:60]}"
            + ('…' if len(row['title']) > 60 else '')
        )

    labels = {make_label(row): int(row['chart_id']) for _, row in filtered.iterrows()}

    st.markdown(
        '<div class="sectnum" style="margin-top: 0;">SELECT A CHART</div>',
        unsafe_allow_html=True,
    )

    selected_label = st.selectbox(
        "Pick a chart to explore",
        options=list(labels.keys()),
        label_visibility="collapsed",
        key='chart_picker',
    )
    selected_id = labels[selected_label]

    st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)

    # ============================================================
    # DETAIL VIEW
    # ============================================================
    chart_row = df.loc[df['chart_id'] == selected_id].iloc[0]
    render_chart_detail(chart_row, show_image=True)

    # ============================================================
    # HELP EXPANDER
    # ============================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    with st.expander("How to read this page"):
        st.markdown(
            """
            **The source caption** (green border) is the ground-truth interpretation as written by
            the paper's authors. This is what an accurate AI explanation should match.

            **The two AI explanations** (red border) are the actual outputs generated by GPT-4o and
            Claude Sonnet 4.6 under a structured six-component prompt grounded in
            Lundgard & Satyanarayan (2022). Phrases that *may* correspond to flagged HM2
            (unsupported inference) errors are highlighted — these are illustrative cues, not a
            forensic mark-up. The score grid below is the authoritative coding.

            **The checklist (C1–C10)** scores each model's explanation against ten accuracy items
            (chart type, axes, extremums, direction, pattern, comparisons, no fabrication, primary
            finding). Green cells indicate pass; red cells indicate fail.

            **The error taxonomy (FE/HM/OE)** scores each model against the nine binary error
            categories from Huang et al.'s (2024) CHOCOLATE framework. Here the colour is inverted:
            green means the error was absent; red means the error was present.
            """
        )
