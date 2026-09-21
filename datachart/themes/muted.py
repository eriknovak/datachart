from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS, LINE_STYLE

MUTED_THEME: StyleAttrs = make_theme(
    {
        # Paul Tol's muted scheme without its green family: indigo, cyan, sand,
        # rose, wine; every pair stays apart for deutan, protan and tritan
        # readers (OKLab ΔE ≥ 10.5); dashes and markers carry identity on a
        # greyscale print
        "color_general_singular": COLORS.YlOrBr,
        "color_general_multiple": [
            "#332288",
            "#88CCEE",
            "#DDCC77",
            "#CC6677",
            "#882255",
        ],
        "color_parallel_hue_continuous": [
            "#FEE391",
            "#FE9929",
            "#CC4C02",
            "#662506",
        ],
        "plot_linestyle_cycle": ["-", "--", "-.", ":", "-"],
        "plot_marker_cycle": ["o", "s", "^", "D", "v"],
        "plot_line_width": 1.2,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_color": "#000000",
        "plot_bar_edge_width": 0.6,
        "plot_hist_edge_color": "#000000",
        "plot_grid_linestyle": LINE_STYLE.DOTTED,
        "plot_grid_color": "#C8C8C8",
        "plot_dumbbell_start_color": "#DDCC77",
        "plot_dumbbell_end_color": "#332288",
        "plot_heatmap_cmap": COLORS.YlOrBr,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
    }
)
"""The muted theme: Tol's muted colours, dashes and markers, colour-blind safe.

Indigo, cyan, sand, rose and wine from Paul Tol's muted scheme, every pair
distinct for deutan, protan and tritan readers. Lines also differ by dash and
scatter points by marker, bars carry black edges, and the grid is dotted, so a
figure survives a greyscale print. The value scale is YlOrBr.
"""
