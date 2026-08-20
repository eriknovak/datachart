from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import LINE_STYLE, COLORS

# light grays for background/de-emphasized elements
LIGHT_GREYS = [
    "#CCCCCC",  # very light gray
    "#D3D3D3",  # light gray
    "#DCDCDC",  # gainsboro
    "#E0E0E0",  # lighter gray
    "#E8E8E8",  # very light
    "#F0F0F0",  # almost white
]

BACKGROUND_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": LIGHT_GREYS,
        "color_general_multiple": LIGHT_GREYS,
        "color_parallel_hue": LIGHT_GREYS,
        "color_parallel_hue_continuous": list(reversed(LIGHT_GREYS)),
        "plot_area_alpha": 0.15,
        "plot_grid_color": "#E6E6E6",
        "plot_line_width": 1.2,
        "plot_line_alpha": 0.4,
        "plot_bar_alpha": 0.3,
        "plot_bar_edge_width": 0.5,
        "plot_bar_edge_color": "#B0B0B0",
        "plot_bar_error_color": "#B0B0B0",
        "plot_bar_value_color": "#B0B0B0",
        "plot_hist_alpha": 0.3,
        "plot_hist_edge_width": 0.5,
        "plot_hist_edge_color": "#B0B0B0",
        "plot_vline_color": "#CCCCCC",
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_vline_alpha": 0.5,
        "plot_hline_color": "#CCCCCC",
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_hline_alpha": 0.5,
        "plot_heatmap_cmap": COLORS.Greys,
        "plot_heatmap_frame_color": "#B0B0B0",
        "plot_scatter_alpha": 0.4,
        "plot_scatter_edge_color": "#D0D0D0",
        "plot_regression_color": "#CCCCCC",
        "plot_regression_alpha": 0.5,
        "plot_regression_ci_alpha": 0.1,
        "plot_parallel_alpha": 0.3,
        "plot_box_alpha": 0.3,
        "plot_box_edgecolor": "#B0B0B0",
        "plot_box_outlier_color": "#E0E0E0",
        "plot_box_outlier_edge_color": "#B0B0B0",
        "plot_box_median_color": "#999999",
        "overlay_bar_alpha": 0.25,
        "overlay_hist_alpha": 0.25,
    }
)
