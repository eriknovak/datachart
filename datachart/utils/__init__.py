"""The module containing the `utils`.

The `utils` module provides a set of public utilities for the package: the
composition of finished figures (`Panel`, `Grid`, `Annotate`), saving them
(`save_figure`), and the statistics behind the charts (`stats`).

This module exports only the public API intended for end users. Internal
implementation details are located in the `_internal` submodule and should
not be imported directly by external code.

"""

from .figure import save_figure
from .compose import Panel, Grid, Annotate
from . import stats

__all__ = [
    "save_figure",
    "Panel",
    "Grid",
    "Annotate",
    "stats",
]
