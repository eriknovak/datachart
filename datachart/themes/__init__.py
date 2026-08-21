"""The module containing the `themes`.

The `themes` module contains the predefined style themes that are used to visualize
the plots. Themes are named for their visual trait, never for a use case or
audience.

Attributes:
    DEFAULT_THEME (datachart.typings.StyleAttrs): The default theme style.
    GREYSCALE_THEME (datachart.typings.StyleAttrs): The greyscale theme style.
    INK_THEME (datachart.typings.StyleAttrs): The ink theme style (dark-ink accents, print-ready).
    HATCH_THEME (datachart.typings.StyleAttrs): The hatch theme style (hatch cycle, value labels, dotted grid).
    MINIMAL_THEME (datachart.typings.StyleAttrs): The minimal theme style (accent blue, no spines, flat bars).
    MATERIAL_THEME (datachart.typings.StyleAttrs): The material theme style (Google palette, light grid).

"""

from .default import DEFAULT_THEME
from .grayscale import GREYSCALE_THEME
from .ink import INK_THEME
from .hatch import HATCH_THEME
from .minimal import MINIMAL_THEME
from .material import MATERIAL_THEME

__all__ = [
    "DEFAULT_THEME",
    "GREYSCALE_THEME",
    "INK_THEME",
    "HATCH_THEME",
    "MINIMAL_THEME",
    "MATERIAL_THEME",
]
