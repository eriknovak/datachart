from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS, FONT_WEIGHT

SKETCH_THEME: StyleAttrs = make_theme(
    {
        # marker-pen tones, vermilion first; the green is greyed towards sage
        # so it stays apart from vermilion for deutan readers
        "color_general_singular": COLORS.YlOrRd,
        "color_general_multiple": [
            "#E4572E",
            "#3F84A3",
            "#F4BA2D",
            "#784AAD",
            "#90B376",
        ],
        "color_parallel_hue_continuous": [
            "#FDD49E",
            "#FC8D59",
            "#E4572E",
            "#99000D",
        ],
        "font_general_family": "sans-serif",
        # Comic Neue downloads on first use; the fallbacks cover an offline miss
        "font_general_sansserif": ["Comic Neue", "Humor Sans", "Comic Sans MS"],
        "font_general_size": 11,
        "font_general_color": "#222222",
        "font_title_size": 15,
        "font_title_color": "#222222",
        "font_title_weight": FONT_WEIGHT.BOLD,
        "axes_spines_width": 1.6,
        "axes_ticks_length": 5,
        "chart_default_show_grid": None,
        "plot_line_width": 2.5,
        "plot_bar_alpha": 1.0,
        # one edge for bars, histograms and pyramids: 1.6 swallows thin bars
        "plot_bar_edge_width": 1.0,
        "plot_hist_edge_width": 1.0,
        "plot_scatter_edge_color": "#222222",
        "plot_dumbbell_start_color": "#3F84A3",
        "plot_dumbbell_end_color": "#E4572E",
        "plot_dumbbell_edge_color": "#222222",
        "plot_dumbbell_connector_color": "#8A8A8A",
        "plot_heatmap_cmap": COLORS.YlOrRd,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
        # a wobbled box around wobbled tiles reads as a second drawing; the
        # band and the pad already mark the group
        "plot_treemap_group_edge_width": 0,
        # half the amplitude of matplotlib's xkcd mode (1, 100, 2), plus a
        # halo of 0.75pt each side of every series line; a list, not a tuple,
        # so the theme survives a JSON theme-file round trip (ADR 0040)
        "plot_sketch_params": [0.5, 100, 2],
        "plot_sketch_halo_width": 1.5,
    }
)
"""The sketch theme: hand-drawn, xkcd-style wobble and halo, Comic Neue font.

Paths wobble, lines carry a white halo, spines and lines are thick, the grid is
off, and text is set in Comic Neue, downloaded on first use; Humor Sans and Comic
Sans MS are the fallbacks should the download fail.
"""
