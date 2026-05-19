"""🏠 Home — landing page with the headline finding and study metadata."""

import streamlit as st

from data.loader import load_charts


def render() -> None:
    """Render the Home page."""
    df = load_charts()

    st.markdown(
        '<div class="eyebrow">━━━━ A POLICY BRIEF ON GENERATIVE AI IN HEALTHCARE COMMUNICATION</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <h1 class="hero-title">
          AI explanations made readers <em>more confident</em><br>
          and <span class="strike">more correct</span> <em>less correct.</em>
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <p class="deck">
          Across forty-five healthcare visualisations and forty users, fluent AI-generated chart
          explanations reduced comprehension while inflating certainty. This brief translates those
          findings into guidelines for the people building, buying, and deploying these tools.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Live metadata strip from the dataset itself
    st.markdown(
        '<div style="border-top: 1px solid #c9bfae; padding-top: 24px; margin-top: 16px;"></div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(5)
    n_charts = len(df)
    n_simple = (df['complexity'] == 'simple').sum()
    n_moderate = (df['complexity'] == 'moderate').sum()
    n_complex = (df['complexity'] == 'complex').sum()
    n_bar = (df['chart_type'] == 'bar').sum()
    n_line = (df['chart_type'] == 'line').sum()
    n_scatter = (df['chart_type'] == 'scatter').sum()

    metadata = [
        ('Charts', f'{n_charts} healthcare<br>visualisations'),
        ('Chart types', f'{n_bar} bar · {n_line} line · {n_scatter} scatter'),
        ('Complexity', f'{n_simple} · {n_moderate} · {n_complex}<br>simple · moderate · complex'),
        ('Participants', '40 users,<br>within-subjects'),
        ('Models', 'GPT-4o &<br>Claude Sonnet 4.6'),
    ]
    for col, (label, value) in zip(cols, metadata):
        with col:
            st.markdown(
                f"""
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px;
                            letter-spacing: 0.2em; text-transform: uppercase; color: #7a6f5f;
                            margin-bottom: 6px;">{label}</div>
                <div style="font-family: 'Fraunces', serif; font-size: 15px; font-weight: 500;
                            line-height: 1.4; color: #1a1612;">{value}</div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sectnum">§ 00 — WHAT THIS BRIEF IS</div>', unsafe_allow_html=True)
    st.markdown(
        """
        ### A practitioner-facing summary of empirical findings on AI chart explanations in healthcare.

        This is an interactive companion to the dissertation — not a substitute for it. Each section
        is short and self-contained. Use the sidebar to navigate.

        - 🔍 **Visualisation Explorer** — browse the 45 charts used in the study. For any chart, see
          the source paper's caption (ground truth), both AI explanations side-by-side, and how each
          model scored on the checklist and error taxonomy.
        - 📈 **Model Evaluation Dashboard** — aggregate accuracy across all 45 charts: GPT-4o vs
          Claude on every checklist item and error category, broken down by chart type and complexity.
          Drill into any chart for detail.
        - 💡 **Findings & Guidance** — the four key findings from the user study and ten practical
          rules for healthcare communicators and AI tool designers.
        - ⚠️ **Common Pitfalls** — the nine-item error taxonomy as a field checklist for screening
          AI-generated chart copy before publication.

        The brief should be read alongside the dissertation's stated limitations — particularly the
        modest user-study sample (n=40) and the use of a single prompt strategy.
        """
    )

    # Quick stats from real data
    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sectnum">AT A GLANCE</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="bigmetric">
              <div class="bigmetric-value">{df['gpt4o_total'].mean():.1f}<span class="bigmetric-suffix">/10</span></div>
              <div class="bigmetric-label">GPT-4o mean accuracy</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="bigmetric">
              <div class="bigmetric-value">{df['claude_total'].mean():.1f}<span class="bigmetric-suffix">/10</span></div>
              <div class="bigmetric-label">Claude mean accuracy</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="bigmetric">
              <div class="bigmetric-value">{df['gpt4o_hm2'].sum()}<span class="bigmetric-suffix">/45</span></div>
              <div class="bigmetric-label">GPT-4o HM2 errors</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class="bigmetric">
              <div class="bigmetric-value">{df['claude_hm2'].sum()}<span class="bigmetric-suffix">/45</span></div>
              <div class="bigmetric-label">Claude HM2 errors</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
