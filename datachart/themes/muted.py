from ..typings import StyleAttrs
from ..constants import COLORS, TRAIT
from .default import DEFAULT_THEME
from .derive import derive_theme

# the furniture both muted themes keep beside their traits (ADR 0074)
MUTED_FURNITURE: StyleAttrs = {
    "plot_line_width": 1.2,
    "plot_grid_color": "#C8C8C8",
    "plot_dumbbell_start_color": "#DDCC77",
    "plot_dumbbell_end_color": "#332288",
}

MUTED_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.TolMuted,
    traits=[TRAIT.PATTERNED, TRAIT.EDGED],
    color_general_singular=COLORS.YlOrBr,
    color_parallel_hue_continuous=["#FEE391", "#FE9929", "#CC4C02", "#662506"],
    plot_heatmap_cmap=COLORS.YlOrBr,
    **MUTED_FURNITURE,
    plot_heatmap_cmap_diverging=COLORS.RdBu,
)
"""The muted theme: Tol's muted colours, dashes and markers, colour-blind safe.

The `TolMuted` lead, indigo, cyan, sand, rose and wine from Paul Tol's muted
scheme, every pair distinct for deutan, protan and tritan readers. The
patterned trait gives lines a dash and scatter points a marker, the edged
trait black bar edges, so a figure survives a greyscale print; the grid is a
light solid hairline. The value scale is YlOrBr.
"""
