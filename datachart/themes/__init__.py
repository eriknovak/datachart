"""The module containing the `themes`.

The `themes` module contains the predefined style themes that are used to visualize
the plots. Themes are named for their look, never for a use case or
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
from .harbor import HARBOR_THEME
from .muted import MUTED_THEME
from .contrast import CONTRAST_THEME
from .mutedhatch import MUTEDHATCH_THEME
from .slatehatch import SLATEHATCH_THEME
from .dark import DARK_THEME
from .derive import derive_theme
from .score import PaletteScore, score_palette

__all__ = [
    "derive_theme",
    "score_palette",
    "PaletteScore",
    "DEFAULT_THEME",
    "GREYSCALE_THEME",
    "INK_THEME",
    "HATCH_THEME",
    "MINIMAL_THEME",
    "MATERIAL_THEME",
    "SKETCH_THEME",
    "QUILL_THEME",
    "HARBOR_THEME",
    "MUTED_THEME",
    "CONTRAST_THEME",
    "MUTEDHATCH_THEME",
    "SLATEHATCH_THEME",
    "DARK_THEME",
]
