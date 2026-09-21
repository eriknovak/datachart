from ..typings import StyleAttrs
from ..constants import COLORS
from .hatch import HATCH_THEME

SLATEHATCH_THEME: StyleAttrs = {
    **HATCH_THEME,
    # the hatch theme with slate blue leading instead of rust; every pair stays
    # apart for deutan and protan readers (OKLab ΔE ≥ 9.6)
    "color_general_singular": COLORS.PuBu,
    "color_general_multiple": [
        "#4F6D8F",
        "#D4D389",
        "#743538",
        "#67A652",
        "#C06AC9",
        "#8EB2D2",
    ],
    "color_parallel_hue_continuous": [
        "#F1EEF6",
        "#A6BDDB",
        "#3690C0",
        "#023858",
    ],
    "plot_dumbbell_start_color": "#4F6D8F",
    "plot_dumbbell_end_color": "#743538",
    "plot_heatmap_cmap": COLORS.PuBu,
    "plot_heatmap_cmap_diverging": COLORS.BrBG,
}
"""The slate-hatch theme: the hatch theme without rust.

Slate blue, sand, wine, green, orchid and sky blue under black edges and hatches,
with a dotted grid. The value scale is PuBu.
"""
