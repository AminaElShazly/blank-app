"""The top masthead bar shown on every page."""

import streamlit as st


def render_masthead() -> None:
    """Render the editorial-style masthead at the top of every page."""
    st.markdown(
        """
        <div class="masthead">
          <div>
            <span class="masthead-dot"></span>EVIDENCE BRIEF &nbsp;·&nbsp; VOL. 01 / NO. 01 &nbsp;·&nbsp; MAY 2026
          </div>
          <div>UNIVERSITY OF SHEFFIELD · IJC319</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
