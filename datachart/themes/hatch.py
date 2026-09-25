from ..typings import StyleAttrs
from ..constants import COLORS, TRAIT
from .default import DEFAULT_THEME
from .derive import derive_theme

# the furniture both hatch themes keep beside their traits (ADR 0074)
HATCH_FURNITURE: StyleAttrs = {
    "font_general_sansserif": ["Helvetica", "Arial", "Liberation Sans", "DejaVu Sans"],
    "plot_grid_color": "#D0D0D0",
    "plot_grid_alpha": 0.8,
}

HATCH_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.Rust,
    traits=[TRAIT.HATCHED, TRAIT.OUTLINED],
    color_general_singular=COLORS.YlOrBr,
    color_parallel_hue_continuous=["#F3E0C3", "#E0AE6A", "#B5563A", "#6B2E1A"],
    plot_dumbbell_start_color="#5A6F86",
    plot_dumbbell_end_color="#B5563A",
    plot_heatmap_cmap=COLORS.YlOrBr,
    plot_heatmap_cmap_diverging=COLORS.RdBu,
    **HATCH_FURNITURE,
)
"""The hatch theme: hatch cycle, black edges, light grid.

The `Rust` lead, muted print tones with rust first and the green deep enough
to stay apart from rust for deutan readers; the hatched trait gives every bar
series its own hatch under black edges, the outlined trait black outlines on
every other mark, and the grid is a light solid hairline. The value scale is
YlOrBr.
"""
