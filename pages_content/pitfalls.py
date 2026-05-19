"""⚠️ Common Pitfalls — the nine-item error taxonomy as a field checklist."""

import plotly.graph_objects as go
import streamlit as st

from data.loader import ERROR_CODES, ERROR_DESCRIPTIONS, ERROR_LABELS, load_charts


_DETAIL = {
    'hm2': 'Does the explanation make causal or interpretive claims absent from the chart? "Driven by," "caused by," "due to" are the giveaway phrases. This is the most consequential flag because it sounds like expertise.',
    'hm1': 'Does any number, year, or category in the text fail to appear in the chart itself?',
    'fe5': 'Are the named highest and lowest values actually the highest and lowest on the chart?',
    'fe1': 'Is a numerical value stated correctly, matching the chart?',
    'fe2': 'Are the x- and y-axes named correctly, with the correct units and labels?',
    'fe3a': 'If the chart shows decline, does the text describe rise — or vice versa?',
    'fe3b': 'Is a steady trend called volatile, a curve called linear, a divergence called convergence?',
    'fe4': 'Is the magnitude of a stated difference or change correct, or has it been exaggerated or understated?',
    'oe1': 'Has the explanation omitted a finding that is central to the chart\'s message? OE1 typically co-occurs with C10 failures.',
}


def render() -> None:
    """Render the Common Pitfalls page."""
    df = load_charts()

    st.markdown('<div class="sectnum">COMMON PITFALLS</div>', unsafe_allow_html=True)
    st.markdown(
        """
        ## A field checklist: *nine red flags* in an AI chart explanation.

        These are the nine error categories used to code the 90 AI explanations in this study (45
        charts × 2 models). Use them as a quick screening tool when reviewing AI-generated chart
        copy before publication. Frequencies shown are from the actual dataset.
        """
    )

    st.markdown(
        """
        <p style="font-family: 'Fraunces', serif; font-style: italic; font-size: 15px;
                  color: #7a6f5f; margin: 16px 0 32px 0;">
          The single highest-frequency flag — HM2, unsupported inferential content — is the one
          most often missed by reviewers because it reads as expertise rather than error.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # ====================================================
    # FREQUENCY CHART
    # ====================================================
    st.markdown('<div class="sectnum">ERROR FREQUENCY ACROSS THE FULL DATASET</div>', unsafe_allow_html=True)
    st.plotly_chart(_build_frequency_chart(df), use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ====================================================
    # NINE FLAGS
    # ====================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sectnum">THE NINE FLAGS</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-family: \'Fraunces\', serif; font-style: italic; font-size: 15px; '
        'color: #7a6f5f; margin-bottom: 24px;">'
        'Ordered by total frequency across both models. Rates shown are out of 45 charts.</p>',
        unsafe_allow_html=True,
    )

    # Sort flags by total frequency
    flags_ranked = sorted(
        ERROR_CODES,
        key=lambda c: -(int(df[f'gpt4o_{c}'].sum()) + int(df[f'claude_{c}'].sum())),
    )

    for i in range(0, len(flags_ranked), 2):
        c1, c2 = st.columns(2)
        with c1:
            _render_flag(flags_ranked[i], df)
        with c2:
            if i + 1 < len(flags_ranked):
                _render_flag(flags_ranked[i + 1], df)

    # ====================================================
    # WORKFLOW EXPANDER
    # ====================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    with st.expander("How to use this checklist in practice"):
        st.markdown(
            """
            **A suggested workflow for reviewing AI-generated chart copy before publication:**

            1. **Read the chart first, without reading the explanation.** Write down — in one sentence —
               what the chart actually shows. This is your ground truth.

            2. **Then read the explanation.** Compare it against your one-sentence ground truth.
               If they disagree, the explanation has likely failed C10 — the most consequential failure.

            3. **Highlight every causal claim in the explanation.** Words like *driven by*, *caused by*,
               *due to*, *as a result of*. For each, ask: is this causation visible in the chart, or
               has the model added it? Causal additions are HM2 hallucinations.

            4. **Verify every named number and extremum** against the chart (HM1, FE1, FE5).

            5. **Check the structural facts** — chart type (C1), axis labels (FE2), direction
               of trends (FE3A), pattern descriptions (FE3B), magnitude (FE4), comparison claims
               (C8), omissions (OE1).

            If you reach the end without flagging anything, the explanation is publishable. In this
            study's sample, this was the exception rather than the rule.
            """
        )


def _render_flag(code: str, df) -> None:
    """Render a single red-flag card with real frequencies from the dataset."""
    gpt_count = int(df[f'gpt4o_{code}'].sum())
    claude_count = int(df[f'claude_{code}'].sum())
    total = len(df)

    label = ERROR_LABELS[code]
    detail = _DETAIL[code]

    st.markdown(
        f"""
        <div class="redflag">
          <div class="redflag-rate">GPT-4o {gpt_count}/{total} · Claude {claude_count}/{total}</div>
          <div class="redflag-code">{code.upper()}</div>
          <div class="redflag-title">{label.split(' — ')[1] if ' — ' in label else label}</div>
          <div class="redflag-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _build_frequency_chart(df) -> go.Figure:
    """Diverging horizontal bar chart showing error frequency for both models."""
    codes = ERROR_CODES
    # Order by total frequency (highest first)
    codes_sorted = sorted(
        codes, key=lambda c: -(int(df[f'gpt4o_{c}'].sum()) + int(df[f'claude_{c}'].sum())),
    )
    labels = [c.upper() for c in codes_sorted]
    gpt = [int(df[f'gpt4o_{c}'].sum()) for c in codes_sorted]
    claude = [int(df[f'claude_{c}'].sum()) for c in codes_sorted]
    total = len(df)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=gpt, name='GPT-4o',
        orientation='h',
        marker_color='#1a1612',
        text=[f'{c}' for c in gpt],
        textposition='outside',
        textfont=dict(family='JetBrains Mono, monospace', size=11, color='#1a1612'),
        hovertemplate='<b>%{y}</b><br>GPT-4o: %{x} of ' + str(total) + ' charts<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=labels, x=claude, name='Claude Sonnet 4.6',
        orientation='h',
        marker_color='#b8341c',
        text=[f'{c}' for c in claude],
        textposition='outside',
        textfont=dict(family='JetBrains Mono, monospace', size=11, color='#1a1612'),
        hovertemplate='<b>%{y}</b><br>Claude: %{x} of ' + str(total) + ' charts<extra></extra>',
    ))
    fig.update_layout(
        barmode='group',
        height=440,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=40, t=40, b=40),
        font=dict(family='Inter Tight, sans-serif', color='#1a1612', size=11),
        xaxis=dict(
            title=f'Number of charts (of {total}) where the error appeared',
            gridcolor='#e8dfd0', showgrid=True, range=[0, total + 5],
        ),
        yaxis=dict(title='', autorange='reversed', tickfont=dict(family='JetBrains Mono, monospace', size=11)),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0,
            font=dict(family='Inter Tight, sans-serif', size=11),
            bgcolor='rgba(0,0,0,0)',
        ),
        hoverlabel=dict(bgcolor='#1a1612', font=dict(color='#f4ede2')),
    )
    return fig
