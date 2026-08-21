from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import LINE_STYLE, COLORS

PUBLICATION_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": COLORS.PaperYlGnBu,
        "color_parallel_hue": COLORS.PaperYlGnBu,
        "color_parallel_hue_continuous": [
            "#C7E9B4",
            "#7FCDBB",
            "#41B6C4",
            "#225EA8",
        ],
        "font_general_sansserif": ["Helvetica", "Arial", "DejaVu Sans"],
        "plot_grid_color": "#DDE3E8",
        "plot_bar_edge_width": 1.0,
        "plot_bar_edge_color": "#0B1F44",
        "plot_hist_edge_color": "#0B1F44",
        "plot_vline_color": "#7F8C8D",
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": "#7F8C8D",
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_heatmap_cmap": COLORS.YlGnBu,
        "plot_heatmap_frame_color": "#0B1F44",
        "plot_scatter_edge_width": 0.6,
        "plot_scatter_edge_color": "#0B1F44",
        "plot_regression_color": "#34495E",
        "plot_parallel_axis_color": "#34495E",
        "plot_parallel_tick_color": "#34495E",
        "plot_parallel_tick_label_color": "#34495E",
        "plot_parallel_dim_label_color": "#34495E",
        "plot_box_edgecolor": "#34495E",
        "plot_box_median_color": "#34495E",
    }
)
