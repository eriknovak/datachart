from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import LINE_STYLE, COLORS

HATCH_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": [
            "#5B84C4",
            "#C85450",
            "#8C8C8C",
            "#6C9A78",
            "#A8C4E8",
            "#C9A227",
        ],
        "color_parallel_hue_continuous": [
            "#D3DEF0",
            "#A8C4E8",
            "#5B84C4",
            "#2E4E8F",
        ],
        "font_general_sansserif": ["Helvetica", "Arial", "DejaVu Sans"],
        "chart_default_show_values": True,
        "plot_hatch_cycle": ["", "//", ".."],
        "plot_grid_color": "#D0D0D0",
        "plot_grid_linestyle": LINE_STYLE.DOTTED,
        "plot_grid_alpha": 0.8,
        "plot_bar_edge_color": "#000000",
        "plot_sankey_node_edge_color": "#000000",
        "plot_bar_edge_width": 0.8,
        "plot_bar_alpha": 1.0,
        "plot_hist_edge_color": "#000000",
        "plot_scatter_edge_color": "#000000",
        "plot_scatter_edge_width": 0.6,
        "plot_swarm_edge_color": "#000000",
        "plot_swarm_edge_width": 0.6,
        "plot_text_box_edgecolor": "#000000",
        "plot_text_arrow_color": "#000000",
        "plot_heatmap_cmap": COLORS.Blues,
        "plot_heatmap_frame_color": "#000000",
        "plot_violin_edgecolor": "#000000",
    }
)
"""The hatch theme: hatch cycle, value labels, dotted grid.

!!! info "Added in v0.8.0"
"""
