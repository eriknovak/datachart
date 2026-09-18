from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS

CONTRAST_THEME: StyleAttrs = make_theme(
    {
        # navy, straw, dusty rose, charcoal and grey stepped in lightness, so a
        # photocopy keeps every series apart; every pair stays apart for
        # deutan, protan and tritan readers too (OKLab ΔE ≥ 10.1)
        "color_general_singular": COLORS.Cividis,
        "color_general_multiple": [
            "#1F4E79",
            "#D4B24C",
            "#B45C6A",
            "#2B2B2B",
            "#9A9A9A",
        ],
        "color_parallel_hue_continuous": [
            "#BCAE6C",
            "#7D7C78",
            "#434E6C",
            "#00224E",
        ],
        "plot_linestyle_cycle": ["-", "--", "-.", ":", "-"],
        "plot_marker_cycle": ["o", "s", "^", "D", "v"],
        "plot_hatch_cycle": ["", "//", "..", "xx", "\\"],
        "plot_line_width": 1.4,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_color": "#000000",
        "plot_bar_edge_width": 0.8,
        "plot_hist_edge_color": "#000000",
        "plot_grid_color": "#C8C8C8",
        "plot_dumbbell_start_color": "#D4B24C",
        "plot_dumbbell_end_color": "#1F4E79",
        "plot_heatmap_cmap": COLORS.Cividis,
    }
)
"""The contrast theme: lightness-stepped colours plus hatches, print-safe.

Navy, straw, dusty rose, charcoal and grey, each a clear lightness step from
the next, so a greyscale print or photocopy still tells the series apart, and
every pair stays distinct for deutan, protan and tritan readers. Bars take a
hatch cycle and black edges, lines a dash cycle, scatter points a marker cycle.
The value scale is Cividis.
"""
