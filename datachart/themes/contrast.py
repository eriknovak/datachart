from ..typings import StyleAttrs
from ..constants import COLORS, TRAIT
from .default import DEFAULT_THEME
from .derive import derive_theme

CONTRAST_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.Contrast,
    traits=[TRAIT.PATTERNED, TRAIT.HATCHED],
    color_general_singular=COLORS.Cividis,
    color_parallel_hue_continuous=["#BCAE6C", "#7D7C78", "#434E6C", "#00224E"],
    plot_line_width=1.4,
    plot_grid_color="#C8C8C8",
    plot_dumbbell_start_color="#D4B24C",
    plot_dumbbell_end_color="#1F4E79",
    plot_heatmap_cmap=COLORS.Cividis,
    plot_heatmap_cmap_diverging=COLORS.RdBu,
)
"""The contrast theme: lightness-stepped colours plus hatches, print-safe.

The `Contrast` lead, navy, straw, dusty rose, charcoal and grey, each a clear
lightness step from the next, so a greyscale print or photocopy still tells
the series apart, and every pair stays distinct for deutan, protan and tritan
readers. The hatched trait gives bars a hatch cycle and black edges, the
patterned trait lines a dash cycle and scatter points a marker cycle. The
value scale is Cividis.
"""
