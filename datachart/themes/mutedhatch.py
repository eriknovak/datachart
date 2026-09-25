from ..typings import StyleAttrs
from ..constants import COLORS, TRAIT
from .default import DEFAULT_THEME
from .derive import derive_theme
from .muted import MUTED_FURNITURE

MUTEDHATCH_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.TolMuted,
    traits=[TRAIT.PATTERNED, TRAIT.HATCHED],
    # the value scale is BuPu, the family of indigo and wine
    color_general_singular=COLORS.BuPu,
    color_parallel_hue_continuous=["#EDF8FB", "#9EBCDA", "#8856A7", "#4D004B"],
    plot_heatmap_cmap=COLORS.BuPu,
    plot_heatmap_cmap_diverging=COLORS.BrBG,
    **MUTED_FURNITURE,
)
"""The muted-hatch theme: Tol's muted colours under hatches.

The muted theme with the hatched trait in place of the edged one: indigo,
cyan, sand, rose and wine bars take the hatch cycle and black edges, lines
keep the muted dashes and markers. The value scale is BuPu.
"""
