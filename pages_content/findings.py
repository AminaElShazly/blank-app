"""💡 Findings & Guidance — the four key findings + ten practical rules."""

import plotly.graph_objects as go
import streamlit as st

from data.loader import load_charts


_COMMUNICATOR_RULES = [
    ("01", "Never deploy an AI explanation without a verified ground-truth caption.",
     "Even the better-performing model failed checklist item C10 — capturing the paper's primary finding — on a non-trivial share of charts. <strong>Treat AI output as a draft, not a deliverable.</strong>"),
    ("02", "Audit for hallucinated causation, not just numerical errors.",
     "The most frequent failure mode (HM2) was the introduction of causal mechanisms absent from the data — \"driven by modern medicine,\" \"due to lifestyle factors.\" These are the hardest errors to catch because they sound knowledgeable."),
    ("03", "Pair explanations with a comprehension prompt, not just a \"read more\" link.",
     "A short, specific question (\"which group changed most?\") forces re-engagement with the chart and disrupts the substitution effect. Passive disclaimers do not."),
    ("04", "Do not assume your expert audiences are protected.",
     "Visualisation experience showed <strong>zero protective effect</strong> (ρ = −0.005). The \"we're only sending this to clinicians\" defence is empirically unsupported."),
    ("05", "Increase scrutiny as chart complexity rises.",
     "Both models degraded monotonically with complexity (ρ ≈ −0.65). Information density is the primary driver of accuracy loss — not chart type. Multi-series, multi-axis, or annotated charts need the most review."),
]


_DESIGNER_RULES = [
    ("01", "Build calibration-aware UIs, not just accurate models.",
     "Accuracy and user confidence dissociated in this study: confidence stayed flat even when accuracy varied (ρ = +0.37, ns). Surfacing uncertainty <strong>at the point of reading</strong> matters more than improving the model in isolation."),
    ("02", "Mark inferential content distinctly from descriptive content.",
     "The dangerous output blends what the chart shows with what the model thinks it means. Visually separate the two — descriptive sentences should look and feel different from inferential ones."),
    ("03", "Require prompted self-verification before high-stakes actions.",
     "When an explanation precedes a clinical, financial, or policy decision, interpose a step that requires the user to locate the relevant value on the chart themselves. The friction is the feature."),
    ("04", "Test for over-reliance, not just accuracy benchmarks.",
     "A chart-explanation feature can score well on standard NLG metrics and still degrade comprehension. Run within-subjects user studies with comprehension questions — the dissociation only shows up against a chart-only baseline."),
    ("05", "Suppress causal language unless the chart supports it.",
     "HM2 hallucinations appeared on 43 of 45 Claude explanations under a structured prompt. A simple post-hoc filter — \"does this sentence describe data, or causation?\" — would catch most of them at low cost."),
]


def render() -> None:
    """Render the Findings & Guidance page."""
    df = load_charts()

    st.markdown('<div class="sectnum">FINDINGS & GUIDANCE</div>', unsafe_allow_html=True)
    st.markdown(
        """
        ## Four findings, ten rules.

        The findings below come from the user study (n = 40, within-subjects). Each rule that follows
        is keyed to one of these findings, and is addressed to one of two audiences with the most
        leverage over how AI chart explanations land in practice.
        """
    )

    # ====================================================
    # FOUR FINDINGS
    # ====================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sectnum">THE FOUR FINDINGS</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown(
            """
            <div class="finding critical">
              <div class="finding-label"><span>FINDING 01 · COMPREHENSION</span><span>r = −0.72</span></div>
              <div class="finding-stat">−36<span class="finding-suffix">% drop</span></div>
              <div class="finding-headline">AI explanations reduced comprehension scores by roughly a third compared to chart-only reading.</div>
              <div class="finding-detail">
                Median comprehension fell from 11.00 (chart only) to 7.00 (with AI explanation).
                Participants substituted reading the explanation for actively interrogating the chart —
                a cognitive shortcut that misfired most when explanations were partially correct rather than wholly wrong.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="finding">
              <div class="finding-label"><span>FINDING 02 · CALIBRATION</span><span>r = +0.91</span></div>
              <div class="finding-stat">51.7<span class="finding-suffix">%</span></div>
              <div class="finding-headline">of AI-assisted answers were high-confidence <em>and</em> wrong.</div>
              <div class="finding-detail">
                Versus 20.8% in the chart-only condition. The proportion of confidently-incorrect
                answers more than doubled when an AI explanation was present.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col3, col4 = st.columns(2)
    with col3:
        # Use real HM2 counts from the dataset
        claude_hm2 = int(df['claude_hm2'].sum())
        gpt_hm2 = int(df['gpt4o_hm2'].sum())
        st.markdown(
            f"""
            <div class="finding">
              <div class="finding-label"><span>FINDING 03 · HALLUCINATION</span><span>HM2 errors</span></div>
              <div class="finding-stat">{claude_hm2}<span class="finding-suffix">/ 45</span></div>
              <div class="finding-headline">Claude Sonnet 4.6 explanations introduced unsupported causal mechanisms — across {claude_hm2} of 45 charts.</div>
              <div class="finding-detail">
                GPT-4o exhibited the same failure on {gpt_hm2} of 45. These hallucinations were fluent,
                plausible-sounding, and absent from the chart's data — the textbook profile of
                extrinsic hallucination in a domain where invented causation has real-world stakes.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            """
            <div class="finding">
              <div class="finding-label"><span>FINDING 04 · LITERACY</span><span>ρ = −0.005</span></div>
              <div class="finding-stat">0.0<span class="finding-suffix"> protective effect</span></div>
              <div class="finding-headline">Visualisation experience offered <em>no measurable protection</em> against AI-induced error.</div>
              <div class="finding-detail">
                Frequent chart users were as susceptible to misleading AI explanations as novices.
                Over-reliance is not a literacy problem solved by targeting expert audiences — it is
                broadly distributed across the population that will encounter these tools.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ====================================================
    # COMPARISON BARS
    # ====================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectnum">CONDITIONS COMPARED</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Comprehension fell. Confidence-in-error rose.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(_comprehension_chart(), use_container_width=True)
    with col_b:
        st.plotly_chart(_confidence_chart(), use_container_width=True)

    # ====================================================
    # GUIDELINES
    # ====================================================
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectnum">PRACTICAL GUIDANCE</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        ## Two audiences, ten rules.

        Each rule below traces back to a specific finding above.
        """
    )

    tab1, tab2 = st.tabs([
        "FOR HEALTHCARE COMMUNICATORS",
        "FOR AI TOOL DESIGNERS",
    ])

    with tab1:
        _render_audience(
            label="AUDIENCE A",
            name="Healthcare <em>communicators</em>",
            tagline="If you produce, commission, or distribute AI-generated chart explanations to non-expert audiences.",
            rules=_COMMUNICATOR_RULES,
        )

    with tab2:
        _render_audience(
            label="AUDIENCE B",
            name="AI tool <em>designers</em>",
            tagline="If you build, fine-tune, or ship chart-explanation features into products that touch healthcare data.",
            rules=_DESIGNER_RULES,
        )


def _render_audience(label: str, name: str, tagline: str, rules: list) -> None:
    """Render an audience header followed by its numbered rule cards."""
    st.markdown(
        f"""
        <div class="audience-header">
          <div class="audience-label">{label}</div>
          <div class="audience-name">{name}</div>
          <div class="audience-tagline">{tagline}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for num, title, body in rules:
        st.markdown(
            f"""
            <div class="guideline-card">
              <div class="guideline-num">{num}</div>
              <div class="guideline-title">{title}</div>
              <div class="guideline-body">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _comprehension_chart() -> go.Figure:
    """Median comprehension by condition."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Chart only", "Chart + AI explanation"],
        y=[11.0, 7.0],
        marker_color=["#1a1612", "#b8341c"],
        text=["11.0", "7.0"],
        textposition="outside",
        textfont=dict(family="Fraunces, serif", size=20, color="#1a1612"),
        hovertemplate="<b>%{x}</b><br>Median: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(
            text='Median comprehension score (max 36)',
            font=dict(family='Fraunces, serif', size=15, color='#1a1612'),
            x=0, xanchor='left',
        ),
        height=320,
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=40, t=60, b=50),
        font=dict(family="Inter Tight, sans-serif", color="#1a1612"),
        xaxis=dict(showgrid=False, tickfont=dict(family="JetBrains Mono, monospace", size=11, color="#7a6f5f")),
        yaxis=dict(showgrid=True, gridcolor="#e8dfd0", range=[0, 14]),
        showlegend=False,
        bargap=0.5,
    )
    return fig


def _confidence_chart() -> go.Figure:
    """False-confidence rate by condition."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Chart only", "Chart + AI explanation"],
        y=[20.8, 51.7],
        marker_color=["#1a1612", "#b8341c"],
        text=["20.8%", "51.7%"],
        textposition="outside",
        textfont=dict(family="Fraunces, serif", size=20, color="#1a1612"),
        hovertemplate="<b>%{x}</b><br>%{y}% high-confidence errors<extra></extra>",
    ))
    fig.update_layout(
        title=dict(
            text='High-confidence errors (% of answers)',
            font=dict(family='Fraunces, serif', size=15, color='#1a1612'),
            x=0, xanchor='left',
        ),
        height=320,
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=40, t=60, b=50),
        font=dict(family="Inter Tight, sans-serif", color="#1a1612"),
        xaxis=dict(showgrid=False, tickfont=dict(family="JetBrains Mono, monospace", size=11, color="#7a6f5f")),
        yaxis=dict(showgrid=True, gridcolor="#e8dfd0", range=[0, 65]),
        showlegend=False,
        bargap=0.5,
    )
    return fig
