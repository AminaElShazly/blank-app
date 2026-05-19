"""
Reusable visual components for displaying scoring data.

- `render_score_grid` shows a row of pass/fail cells for a 10- or 9-item series.
- `render_chart_detail` shows one chart's full information: image, source caption,
  both AI explanations, and a comparison of checklist + error scores.
"""

from pathlib import Path

import streamlit as st

from data.loader import (
    CHECKLIST_CODES,
    CHECKLIST_LABELS,
    ERROR_CODES,
    ERROR_LABELS,
    image_path,
)


def render_score_grid(scores: dict, codes: list[str], label_map: dict | None = None) -> None:
    """
    Render a horizontal row of binary score cells.

    Args:
        scores: dict mapping code -> 0/1
        codes:  the order in which to render the codes
        label_map: optional dict mapping code -> short label shown in cell
                   (default uses uppercase code, e.g. 'C1', 'HM2')
    """
    cells = []
    for code in codes:
        passed = bool(scores.get(code, 0))
        cls = 'score-pass' if passed else 'score-fail'
        # For pass/fail we show ✓ / ✗ — but a code-letter is more legible
        label = (label_map or {}).get(code, code.upper())
        cells.append(f'<div class="score-cell {cls}" title="{label}">{label}</div>')
    st.markdown(f'<div class="score-grid">{"".join(cells)}</div>', unsafe_allow_html=True)


def _short_codes(prefix: str = '') -> dict[str, str]:
    """Generate short labels for checklist cells: C1, C2 ... C10."""
    return {f'{prefix}c{i}': f'C{i}' for i in range(1, 11)}


def _error_short_codes() -> dict[str, str]:
    """Short labels for error taxonomy cells."""
    return {
        'fe1': 'FE1', 'fe2': 'FE2', 'fe3a': 'F3A', 'fe3b': 'F3B',
        'fe4': 'FE4', 'fe5': 'FE5', 'hm1': 'HM1', 'hm2': 'HM2', 'oe1': 'OE1',
    }


def _highlight_errors(text: str, errors_present: dict[str, bool]) -> str:
    """
    Lightly mark places in an AI explanation that *might* correspond to errors.

    We can't pin errors to exact sentences without per-error annotations, so we
    use a conservative heuristic: if HM2 is flagged, highlight obvious causal
    phrases ('driven by', 'caused by', 'due to'). This is illustrative, not
    forensic — the score grid below the text shows the authoritative coding.
    """
    if errors_present.get('hm2'):
        causal_phrases = [
            'driven by', 'caused by', 'due to', 'as a result of',
            'led to', 'attributable to', 'because of', 'resulting from',
        ]
        for phrase in causal_phrases:
            for variant in [phrase, phrase.capitalize()]:
                if variant in text:
                    # Wrap the phrase and a few following words
                    idx = text.find(variant)
                    end = text.find('.', idx)
                    if end == -1:
                        end = min(len(text), idx + 80)
                    # Don't double-wrap
                    if '<span class="err"' in text[max(0, idx - 30):idx]:
                        continue
                    text = (
                        text[:idx]
                        + f'<span class="err">{text[idx:end]}</span>'
                        + text[end:]
                    )
    return text


def render_chart_detail(chart_row, show_image: bool = True) -> None:
    """
    Render the full detail view for one chart.

    Used by:
      - Visualisation Explorer when a chart is selected
      - Model Evaluation Dashboard's drill-down panel
    """
    # Image
    if show_image:
        img = image_path(int(chart_row['chart_id']))
        if img.exists():
            st.image(str(img), use_container_width=True)
        else:
            st.warning(f"Image not found: {img.name}")

    # Title + metadata
    st.markdown(
        f"""
        <div style="margin-top: 16px;">
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px;
                      letter-spacing: 0.2em; text-transform: uppercase; color: #7a6f5f;
                      margin-bottom: 6px;">
            CHART #{chart_row['chart_id']} · {chart_row['chart_type'].upper()} · {chart_row['complexity'].upper()}
          </div>
          <div style="font-family: 'Fraunces', serif; font-size: 22px; font-weight: 500;
                      line-height: 1.3; color: #1a1612; margin-bottom: 24px;">
            {chart_row['title']}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Source caption
    st.markdown(
        f"""
        <div class="source-panel">
          <div class="source-label">SOURCE PAPER · GROUND TRUTH</div>
          {chart_row['source_caption']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="margin-top: 32px;"></div>', unsafe_allow_html=True)

    # Two-column AI explanations
    col_g, col_c = st.columns(2)

    with col_g:
        gpt_errors = {code: bool(chart_row[f'gpt4o_{code}']) for code in ERROR_CODES}
        highlighted = _highlight_errors(str(chart_row['gpt4o_explanation']), gpt_errors)
        st.markdown(
            f"""
            <div class="ai-panel">
              <div class="ai-label">GPT-4O EXPLANATION</div>
              {highlighted.replace(chr(10), '<br>')}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_c:
        claude_errors = {code: bool(chart_row[f'claude_{code}']) for code in ERROR_CODES}
        highlighted = _highlight_errors(str(chart_row['claude_explanation']), claude_errors)
        st.markdown(
            f"""
            <div class="ai-panel">
              <div class="ai-label">CLAUDE SONNET 4.6 EXPLANATION</div>
              {highlighted.replace(chr(10), '<br>')}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sect-divider"></div>', unsafe_allow_html=True)

    # Scoring tables
    st.markdown(
        '<div class="sectnum">CHECKLIST SCORING · C1\u2013C10</div>',
        unsafe_allow_html=True,
    )
    _render_score_comparison_table(chart_row, kind='checklist')

    st.markdown(
        '<div class="sectnum" style="margin-top: 24px;">ERROR TAXONOMY · 9 CATEGORIES</div>',
        unsafe_allow_html=True,
    )
    _render_score_comparison_table(chart_row, kind='errors')


def _render_score_comparison_table(chart_row, kind: str) -> None:
    """Render a two-row table comparing GPT-4o and Claude scores."""
    if kind == 'checklist':
        codes = CHECKLIST_CODES
        label_map = {f'c{i}': f'C{i}' for i in range(1, 11)}
        labels = label_map
        gpt_total = int(chart_row['gpt4o_total'])
        claude_total = int(chart_row['claude_total'])
        total_label = '/10'
        # For checklist, 1 = pass (good); 0 = fail
        invert = False
    else:
        codes = ERROR_CODES
        labels = _error_short_codes()
        label_map = labels
        gpt_total = int(chart_row['gpt4o_err_count'])
        claude_total = int(chart_row['claude_err_count'])
        total_label = '/9 errors'
        # For errors, 1 = error present (bad); 0 = clean
        invert = True

    # GPT-4o row
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.markdown(
            '<div class="score-row-label" style="padding-top: 6px;">GPT-4o</div>',
            unsafe_allow_html=True,
        )
    with col2:
        gpt_scores = {code: int(chart_row[f'gpt4o_{code}']) for code in codes}
        if invert:
            # Flip so "1" (error present) shows as fail (red), "0" (no error) shows as pass (green)
            gpt_scores_display = {k: (0 if v else 1) for k, v in gpt_scores.items()}
        else:
            gpt_scores_display = gpt_scores
        render_score_grid(gpt_scores_display, codes, labels)
    with col3:
        st.markdown(
            f'<div style="font-family: \'Fraunces\', serif; font-size: 20px; '
            f'font-weight: 500; color: #1a1612; text-align: right;">'
            f'{gpt_total}<span style="color: #7a6f5f; font-size: 13px;">{total_label}</span></div>',
            unsafe_allow_html=True,
        )

    # Claude row
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.markdown(
            '<div class="score-row-label" style="padding-top: 6px;">Claude</div>',
            unsafe_allow_html=True,
        )
    with col2:
        claude_scores = {code: int(chart_row[f'claude_{code}']) for code in codes}
        if invert:
            claude_scores_display = {k: (0 if v else 1) for k, v in claude_scores.items()}
        else:
            claude_scores_display = claude_scores
        render_score_grid(claude_scores_display, codes, labels)
    with col3:
        st.markdown(
            f'<div style="font-family: \'Fraunces\', serif; font-size: 20px; '
            f'font-weight: 500; color: #1a1612; text-align: right;">'
            f'{claude_total}<span style="color: #7a6f5f; font-size: 13px;">{total_label}</span></div>',
            unsafe_allow_html=True,
        )
