"""The module containing the `themes`.

The `themes` module contains the predefined style themes that are used to visualize
the plots. Themes are named for their visual trait, never for a use case or
audience; each is a complete `StyleAttrs` dictionary that `config.set_theme`
applies.

"""

from .default import DEFAULT_THEME
from .grayscale import GREYSCALE_THEME
from .ink import INK_THEME
from .hatch import HATCH_THEME
from .minimal import MINIMAL_THEME
from .material import MATERIAL_THEME
from .sketch import SKETCH_THEME
from .quill import QUILL_THEME

__all__ = [
    "DEFAULT_THEME",
    "GREYSCALE_THEME",
    "INK_THEME",
    "HATCH_THEME",
    "MINIMAL_THEME",
    "MATERIAL_THEME",
    "SKETCH_THEME",
    "QUILL_THEME",
]
