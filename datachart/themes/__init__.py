"""The module containing the `themes`.

The `themes` module contains the predefined style themes that are used to visualize
the plots.

Attributes:
    DEFAULT_THEME (datachart.typings.StyleAttrs): The default theme style.
    GREYSCALE_THEME (datachart.typings.StyleAttrs): The greyscale theme style.

"""

from .default import DEFAULT_THEME
from .grayscale import GREYSCALE_THEME

__all__ = ["DEFAULT_THEME", "GREYSCALE_THEME"]
