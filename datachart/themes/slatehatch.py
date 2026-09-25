from ..typings import StyleAttrs
from ..constants import COLORS, TRAIT
from .default import DEFAULT_THEME
from .derive import derive_theme
from .hatch import HATCH_FURNITURE

SLATEHATCH_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.Slate,
    traits=[TRAIT.HATCHED, TRAIT.OUTLINED],
    color_general_singular=COLORS.PuBu,
    color_parallel_hue_continuous=["#F1EEF6", "#A6BDDB", "#3690C0", "#023858"],
    plot_dumbbell_start_color="#4F6D8F",
    plot_dumbbell_end_color="#743538",
    plot_heatmap_cmap=COLORS.PuBu,
    plot_heatmap_cmap_diverging=COLORS.BrBG,
    **HATCH_FURNITURE,
)
"""The slate-hatch theme: the hatch theme without rust.

The `Slate` lead, slate blue, sand, wine, green, orchid and sky blue, under
the hatch theme's hatched and outlined traits and dotted grid; every pair
stays apart for deutan and protan readers. The value scale is PuBu.
"""
