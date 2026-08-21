"""The module containing the `utils`.

The `utils` module provides a set of public utilities for the package.

This module exports only the public API intended for end users. Internal
implementation details are located in the `_internal` submodule and should
not be imported directly by external code.

Modules:
    stats: The module containing the statistics functions (count, mean, median, etc.).

Methods:
    save_figure(figure, path, dpi, format, transparent):
        Saves the figure into a file using the provided format parameters.
    Panel(charts, title, xlabel, ylabel_left, ylabel_right, figsize, show_legend, ...):
        Overlays rendered chart figures on a single plot with optional dual y-axes.
    Grid(charts, title, max_cols, figsize, sharex, sharey):
        Arranges rendered chart figures in a grid; nested rows define the layout.
    FigureGridLayout(charts, title, max_cols, figsize, sharex, sharey):
        (Deprecated) Use Grid instead.
    figure_grid_layout(figures, title, max_cols, figsize, sharex, sharey):
        (Deprecated) Use Grid instead.

"""

from .figure import save_figure, FigureGridLayout, figure_grid_layout
from .overlay import OverlayChart
from .compose import Panel, Grid
from . import stats

__all__ = [
    "save_figure",
    "Panel",
    "Grid",
    "FigureGridLayout",
    "figure_grid_layout",
    "OverlayChart",
    "stats",
]
