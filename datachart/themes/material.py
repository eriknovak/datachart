from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS

MATERIAL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        # Google's hues in brand order, blue, red, yellow, green, stepped in
        # lightness so red and green stay apart for deutan readers
        "color_general_multiple": [
            "#1A73E8",
            "#BC261D",
            "#EFB04E",
            "#269F47",
            "#19ACC1",
            "#7C48B5",
        ],
        "color_parallel_hue_continuous": [
            "#C6DAFC",
            "#7BAAF7",
            "#1A73E8",
            "#174EA6",
        ],
        "font_general_sansserif": ["Roboto", "Arial", "Helvetica", "Liberation Sans"],
        "axes_spines_top_visible": False,
        "axes_spines_right_visible": False,
        "axes_spines_left_visible": False,
        "plot_grid_color": "#E0E0E0",
        "plot_grid_alpha": 1.0,
        "plot_grid_linewidth": 0.8,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 0,
        "plot_stackedarea_edge_width": 0,
        "plot_hist_edge_width": 0,
        "plot_line_width": 2.0,
        "plot_text_box_edgecolor": "#757575",
        "plot_text_arrow_color": "#757575",
        "plot_dumbbell_start_color": "#EFB04E",
        "plot_dumbbell_end_color": "#1A73E8",
        "plot_dumbbell_edge_width": 0,
        "plot_heatmap_cmap": COLORS.Blues,
        "plot_heatmap_cmap_diverging": COLORS.PuOr,
        "plot_heatmap_frame_color": "#000000",
    }
)
"""The material theme: Google palette, light grid.
"""
