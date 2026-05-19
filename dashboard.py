"""📈 Model Evaluation Dashboard — aggregate accuracy + drill-down per chart."""

import plotly.graph_objects as go
import streamlit as st

from data.loader import (
    CHECKLIST_CODES,
    ERROR_CODES,
    checklist_summary,
    error_summary,
    load_charts,
)
from components.score_grid import render_chart_detail


def render() -> None:
    """Render the Model Evaluation Dashboard."""
    df = load_charts()

    st.markdown('<div class="sectnum">MODEL EVALUATION DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown(
        """
        ## GPT-4o vs Claude Sonnet 4.6, across 45 healthcare charts.

        Aggregate accuracy at the top; per-chart drill-down at the bottom. Filter the dataset
        with the controls below to see how accuracy and errors break down by chart type and
        complexity.
        """
    )

    # ============================================================
    # FILTERS
    # ============================================================
    st.markdown("<br>", unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        chart_types = st.multiselect(
            "Chart type",
            options=['bar', 'line', 'scatter'],
            default=['bar', 'line', 'scatter'],
            key='dash_type',
        )
    with f2:
        complexities = st.multiselect(
            "Complexity",
            options=['simple', 'moderate', 'complex'],
            default=['simple', 'moderate', 'complex'],
            key='dash_complexity',
        )

    sub = df[df['chart_type'].isin(chart_types) & df['complexity'].isin(complexities)].copy()

    if len(sub) == 0:
        st.warning("No charts match the current filters.")
        return

    st.markdown(
        f'<div style="font-family: \'JetBrains Mono\', monospace; font-size: 10px; '
        f'letter-spacing: 0.2em; text-transform: uppercase; color: #7a6f5f; '
        f'margin-top: 16px;">Showing {len(sub)} of {len(df)} charts</div>',
        unsafe_allow_html=True,
    )

    # ============================================================
    # AGGREGATE: HEADLINE METRICS
    # ============================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectnum">AGGREGATE · HEADLINE METRICS</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    gpt_mean = sub['gpt4o_total'].mean()
    claude_mean = sub['claude_total'].mean()
    gpt_err = sub['gpt4o_err_count'].mean()
    claude_err = sub['claude_err_count'].mean()

    with m1:
        _bigmetric(f"{gpt_mean:.2f}", "/10", "GPT-4o mean accuracy")
    with m2:
        _bigmetric(f"{claude_mean:.2f}", "/10", "Claude mean accuracy")
    with m3:
        _bigmetric(f"{gpt_err:.2f}", "/9", "GPT-4o mean errors")
    with m4:
        _bigmetric(f"{claude_err:.2f}", "/9", "Claude mean errors")

    # ============================================================
    # CHECKLIST AGGREGATE
    # ============================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectnum">AGGREGATE · CHECKLIST PASS RATES (C1\u2013C10)</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <p style="font-family: 'Fraunces', serif; font-style: italic; font-size: 15px;
                  color: #7a6f5f; max-width: 740px; margin-bottom: 24px;">
          For each item, what proportion of the {len(sub)} filtered charts did each model pass?
          Higher is better. Differences highlight where one model systematically out- or under-performs.
        </p>
        """,
        unsafe_allow_html=True,
    )

    gpt_cl = checklist_summary(sub, 'gpt4o')
    claude_cl = checklist_summary(sub, 'claude')
    st.plotly_chart(
        _build_checklist_chart(gpt_cl, claude_cl, total=len(sub)),
        use_container_width=True,
    )

    # ============================================================
    # ERROR TAXONOMY AGGREGATE
    # ============================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectnum">AGGREGATE · ERROR FREQUENCY (FE / HM / OE)</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <p style="font-family: 'Fraunces', serif; font-style: italic; font-size: 15px;
                  color: #7a6f5f; max-width: 740px; margin-bottom: 24px;">
          For each of the nine error categories, how many of the {len(sub)} filtered charts
          contained the error? Lower is better.
        </p>
        """,
        unsafe_allow_html=True,
    )

    gpt_e = error_summary(sub, 'gpt4o')
    claude_e = error_summary(sub, 'claude')
    st.plotly_chart(
        _build_error_chart(gpt_e, claude_e, total=len(sub)),
        use_container_width=True,
    )

    # ============================================================
    # ACCURACY DISTRIBUTION
    # ============================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectnum">AGGREGATE · ACCURACY DISTRIBUTION</div>',
        unsafe_allow_html=True,
    )

    dist_col1, dist_col2 = st.columns(2)
    with dist_col1:
        st.plotly_chart(
            _build_score_distribution(sub, 'gpt4o', 'GPT-4o'),
            use_container_width=True,
        )
    with dist_col2:
        st.plotly_chart(
            _build_score_distribution(sub, 'claude', 'Claude Sonnet 4.6'),
            use_container_width=True,
        )

    # ============================================================
    # PER-CHART DRILL-DOWN
    # ============================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectnum">DRILL-DOWN · ONE CHART AT A TIME</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        Pick a chart from the filtered set to see how both models scored on every checklist item
        and error category, alongside the source caption and the two AI explanations.
        """
    )

    def make_label(row):
        return (
            f"#{int(row['chart_id']):02d} · {row['chart_type']:<7s} · "
            f"{row['complexity']:<8s} · GPT {int(row['gpt4o_total'])}/10 · "
            f"Claude {int(row['claude_total'])}/10 · {row['title'][:60]}"
            + ('…' if len(row['title']) > 60 else '')
        )

    labels = {make_label(row): int(row['chart_id']) for _, row in sub.iterrows()}
    selected_label = st.selectbox(
        "Pick a chart",
        options=list(labels.keys()),
        label_visibility="collapsed",
        key='dashboard_picker',
    )
    selected_id = labels[selected_label]

    st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
    chart_row = df.loc[df['chart_id'] == selected_id].iloc[0]
    render_chart_detail(chart_row, show_image=True)


# ----------------------------------------------------------------
# Helper components
# ----------------------------------------------------------------

def _bigmetric(value: str, suffix: str, label: str) -> None:
    """Render a single big-metric card."""
    st.markdown(
        f"""
        <div class="bigmetric">
          <div class="bigmetric-value">{value}<span class="bigmetric-suffix">{suffix}</span></div>
          <div class="bigmetric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _build_checklist_chart(gpt: dict, claude: dict, total: int) -> go.Figure:
    """Horizontal grouped-bar chart of checklist pass rates."""
    codes = CHECKLIST_CODES
    labels = [c.upper() for c in codes]
    gpt_pct = [100 * gpt[c] / total for c in codes]
    claude_pct = [100 * claude[c] / total for c in codes]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=gpt_pct, name='GPT-4o',
        orientation='h',
        marker_color='#1a1612',
        text=[f'{p:.0f}%' for p in gpt_pct],
        textposition='auto',
        textfont=dict(family='JetBrains Mono, monospace', size=11, color='#f4ede2'),
        hovertemplate='<b>%{y}</b><br>GPT-4o: %{x:.1f}% pass<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=labels, x=claude_pct, name='Claude Sonnet 4.6',
        orientation='h',
        marker_color='#b8341c',
        text=[f'{p:.0f}%' for p in claude_pct],
        textposition='auto',
        textfont=dict(family='JetBrains Mono, monospace', size=11, color='#f4ede2'),
        hovertemplate='<b>%{y}</b><br>Claude: %{x:.1f}% pass<extra></extra>',
    ))
    fig.update_layout(
        barmode='group',
        height=440,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=40, t=40, b=40),
        font=dict(family='Inter Tight, sans-serif', color='#1a1612', size=11),
        xaxis=dict(title='% of charts passing', range=[0, 110], gridcolor='#e8dfd0', showgrid=True),
        yaxis=dict(title='', autorange='reversed', tickfont=dict(family='JetBrains Mono, monospace', size=10)),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0,
            font=dict(family='Inter Tight, sans-serif', size=11),
            bgcolor='rgba(0,0,0,0)',
        ),
        hoverlabel=dict(bgcolor='#1a1612', font=dict(color='#f4ede2')),
    )
    return fig


def _build_error_chart(gpt: dict, claude: dict, total: int) -> go.Figure:
    """Horizontal grouped-bar chart of error frequencies."""
    codes = ERROR_CODES
    labels = [c.upper() for c in codes]
    gpt_counts = [gpt[c] for c in codes]
    claude_counts = [claude[c] for c in codes]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=gpt_counts, name='GPT-4o',
        orientation='h',
        marker_color='#1a1612',
        text=[f'{c}/{total}' for c in gpt_counts],
        textposition='auto',
        textfont=dict(family='JetBrains Mono, monospace', size=11, color='#f4ede2'),
        hovertemplate='<b>%{y}</b><br>GPT-4o: %{x} of ' + str(total) + ' charts<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=labels, x=claude_counts, name='Claude Sonnet 4.6',
        orientation='h',
        marker_color='#b8341c',
        text=[f'{c}/{total}' for c in claude_counts],
        textposition='auto',
        textfont=dict(family='JetBrains Mono, monospace', size=11, color='#f4ede2'),
        hovertemplate='<b>%{y}</b><br>Claude: %{x} of ' + str(total) + ' charts<extra></extra>',
    ))
    fig.update_layout(
        barmode='group',
        height=420,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=40, t=40, b=40),
        font=dict(family='Inter Tight, sans-serif', color='#1a1612', size=11),
        xaxis=dict(title=f'Number of charts (out of {total}) with this error', gridcolor='#e8dfd0', showgrid=True),
        yaxis=dict(title='', autorange='reversed', tickfont=dict(family='JetBrains Mono, monospace', size=10)),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0,
            font=dict(family='Inter Tight, sans-serif', size=11),
            bgcolor='rgba(0,0,0,0)',
        ),
        hoverlabel=dict(bgcolor='#1a1612', font=dict(color='#f4ede2')),
    )
    return fig


def _build_score_distribution(sub, model: str, label: str) -> go.Figure:
    """Histogram of checklist totals (0-10) for one model."""
    counts = [(sub[f'{model}_total'] == i).sum() for i in range(11)]
    color = '#1a1612' if model == 'gpt4o' else '#b8341c'

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(range(11)), y=counts,
        marker_color=color,
        text=[str(c) if c > 0 else '' for c in counts],
        textposition='outside',
        textfont=dict(family='Fraunces, serif', size=14, color='#1a1612'),
        hovertemplate=f'<b>{label}</b><br>Score: %{{x}}/10<br>Charts: %{{y}}<extra></extra>',
    ))
    fig.update_layout(
        title=dict(
            text=f'<b>{label}</b> — checklist score distribution',
            font=dict(family='Fraunces, serif', size=16, color='#1a1612'),
            x=0, xanchor='left',
        ),
        height=320,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=40, t=60, b=50),
        font=dict(family='Inter Tight, sans-serif', color='#1a1612'),
        xaxis=dict(
            title='Checklist score (0–10)',
            tickmode='linear', tick0=0, dtick=1,
            tickfont=dict(family='JetBrains Mono, monospace', size=10),
            showgrid=False,
        ),
        yaxis=dict(
            title='Number of charts',
            gridcolor='#e8dfd0', showgrid=True,
            range=[0, max(counts) * 1.25 if counts else 1],
        ),
        showlegend=False,
        bargap=0.2,
    )
    return fig
