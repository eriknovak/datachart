"""The module containing the `themes`.

The `themes` module contains the predefined style themes that are used to visualize
the plots.

Attributes:
    DEFAULT_THEME (datachart.typings.StyleAttrs): The default theme style.
    GREYSCALE_THEME (datachart.typings.StyleAttrs): The greyscale theme style.
    PUBLICATION_THEME (datachart.typings.StyleAttrs): The publication theme style.
    BACKGROUND_THEME (datachart.typings.StyleAttrs): The background theme style (light gray for de-emphasized elements).
    MINIMAL_THEME (datachart.typings.StyleAttrs): The minimal theme style (accent blue, no spines, flat bars).
    MATERIAL_THEME (datachart.typings.StyleAttrs): The material theme style (Google palette, light grid).
    ACADEMIC_THEME (datachart.typings.StyleAttrs): The academic theme style (serif fonts, hatch cycle).

"""

from .default import DEFAULT_THEME
from .grayscale import GREYSCALE_THEME
from .publication import PUBLICATION_THEME
from .background import BACKGROUND_THEME
from .minimal import MINIMAL_THEME
from .material import MATERIAL_THEME
from .academic import ACADEMIC_THEME

__all__ = [
    "DEFAULT_THEME",
    "GREYSCALE_THEME",
    "PUBLICATION_THEME",
    "BACKGROUND_THEME",
    "MINIMAL_THEME",
    "MATERIAL_THEME",
    "ACADEMIC_THEME",
]
