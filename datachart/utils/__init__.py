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
    figure_grid_layout(figures, title, max_cols, figsize, sharex, sharey):
        Combines multiple figure objects into a single grid layout.

"""

from .figure import save_figure, figure_grid_layout
from . import stats


__all__ = ["save_figure", "figure_grid_layout", "stats"]
