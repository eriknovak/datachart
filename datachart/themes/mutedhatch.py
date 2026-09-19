from ..typings import StyleAttrs
from ..constants import COLORS
from .muted import MUTED_THEME
from .contrast import CONTRAST_THEME

MUTEDHATCH_THEME: StyleAttrs = {
    **MUTED_THEME,
    # bars need a second cue on greyscale print: Contrast's hatches; the
    # value scale swaps YlOrBr for BuPu, the family of indigo and wine
    "color_general_singular": COLORS.BuPu,
    "color_parallel_hue_continuous": [
        "#EDF8FB",
        "#9EBCDA",
        "#8856A7",
        "#4D004B",
    ],
    "plot_hatch_cycle": CONTRAST_THEME["plot_hatch_cycle"],
    "plot_bar_edge_width": 0.8,
    "plot_heatmap_cmap": COLORS.BuPu,
}
"""The muted-hatch theme: Tol's muted colours under Contrast's hatches.

Indigo, cyan, sand, rose and wine bars take the hatch cycle and black edges;
lines keep the muted dashes and markers. The value scale is BuPu.
"""
