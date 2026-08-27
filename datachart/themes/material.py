from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS

MATERIAL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": [
            "#4285F4",
            "#FBBC04",
            "#34A853",
            "#EA4335",
            "#7BAAF7",
            "#46BDC6",
        ],
        "color_parallel_hue_continuous": [
            "#C6DAFC",
            "#7BAAF7",
            "#4285F4",
            "#1B5FD9",
        ],
        "font_general_sansserif": ["Roboto", "Arial", "Helvetica"],
        "axes_spines_top_visible": False,
        "axes_spines_right_visible": False,
        "axes_spines_left_visible": False,
        "chart_default_show_values": True,
        "plot_grid_color": "#E0E0E0",
        "plot_grid_alpha": 1.0,
        "plot_grid_linewidth": 0.8,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 0,
        "plot_hist_edge_width": 0,
        "plot_line_width": 2.0,
        "plot_text_box_edgecolor": "#757575",
        "plot_text_arrow_color": "#757575",
        "plot_heatmap_cmap": COLORS.Blues,
        "plot_heatmap_frame_color": "#000000",
    }
)
"""The material theme: Google palette, light grid.

!!! info "Added in v0.8.0"
"""
