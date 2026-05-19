"""Shared UI components."""

from .styling import inject_styles
from .masthead import render_masthead
from .score_grid import render_score_grid, render_chart_detail

__all__ = [
    'inject_styles',
    'render_masthead',
    'render_score_grid',
    'render_chart_detail',
]
