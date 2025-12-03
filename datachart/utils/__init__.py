"""The module containing the `utils`.

The `utils` module provides a set of public utilities for the package.

This module exports only the public API intended for end users. Internal
implementation details are located in the `_internal` submodule and should
not be imported directly by external code.

Public Modules:
    stats: The module containing the statistics functions (count, mean, median, etc.).

Public Methods:
    save_figure(figure, path, dpi, format, transparent):
        Saves the figure into a file using the provided format parameters.

Note:
    The `_internal` submodule contains internal utilities (plot_engine, config_helpers,
    colors) that are used by the datachart package but are not part of the public API
    and may change without notice.

"""

from .figure import save_figure
from . import stats


__all__ = ["save_figure", "stats"]
