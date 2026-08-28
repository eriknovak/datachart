from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import LINE_STYLE, COLORS

GREYS = [
    "#2C3E50",  # dark slate
    "#5D6D7E",  # medium gray
    "#85929E",  # light gray
    "#ABB2B9",  # lighter gray
    "#D5DBDB",  # very light gray
    "#34495E",  # charcoal
]

GREYSCALE_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Greys,
        "color_general_multiple": GREYS,
        "color_parallel_hue": GREYS,
        "color_parallel_hue_continuous": [
            "#D9D9D9",
            "#969696",
            "#525252",
            "#000000",
        ],
        "plot_bar_edge_width": 0.8,
        "plot_bar_edge_color": "#000000",
        "plot_sankey_node_edge_color": "#000000",
        "plot_hist_edge_color": "#000000",
        "plot_vline_color": "#5D6D7E",
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": "#5D6D7E",
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_text_box_edgecolor": "#B0B0B0",
        "plot_text_arrow_color": "#5D6D7E",
        "plot_heatmap_cmap": COLORS.Greys,
        "plot_heatmap_frame_color": "#000000",
        "plot_regression_color": "#34495E",
        "plot_box_median_color": "#000000",
        "plot_violin_edgecolor": "#000000",
        "plot_violin_inner_color": "#000000",
    }
)
"""The greyscale theme: shades of grey for print or colorblind-safe output.

!!! info "Added in v0.5.0"
"""
