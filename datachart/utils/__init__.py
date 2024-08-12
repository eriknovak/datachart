"""The module containing the `utils`.

The `utils` module provides a set of utilities used in the package.

Modules:
    stats: The module containing the statistics functions.

Methods:
    save_figure(figure, path, dpi, format, transparent):
        Saves the figure into a file using the provided format parameters.

"""

from .figure import save_figure
from . import stats


__all__ = ["save_figure", "stats"]
