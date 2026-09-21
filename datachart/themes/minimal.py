from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS

MINIMAL_THEME: StyleAttrs = make_theme(
    {
        # one violet accent, then greys stepped wide enough to stay apart
        "color_general_singular": COLORS.Purples,
        "color_general_multiple": [
            "#7048E8",
            "#1F2933",
            "#8A97A3",
            "#C5CDD4",
        ],
        "color_parallel_hue_continuous": [
            "#DCD3F7",
            "#A796EE",
            "#7048E8",
            "#3B1E9E",
        ],
        "font_general_color": "#1F1F1F",
        "font_title_color": "#1F1F1F",
        "axes_spines_top_visible": False,
        "axes_spines_right_visible": False,
        "axes_spines_left_visible": False,
        "axes_spines_bottom_visible": False,
        "axes_ticks_length": 0,
        "plot_grid_color": "#EFEFEF",
        "plot_grid_alpha": 1.0,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 0,
        "plot_stackedarea_edge_width": 0,
        "plot_value_fontsize": 9,
        "plot_value_color": "#1F1F1F",
        "plot_hist_edge_width": 0,
        "plot_line_width": 2.0,
        "plot_scatter_edge_color": "#FFFFFF",
        "plot_swarm_edge_color": "#FFFFFF",
        "plot_dumbbell_start_color": "#C5CDD4",
        "plot_dumbbell_end_color": "#7048E8",
        "plot_dumbbell_connector_color": "#DDE3E8",
        "plot_text_box_edgecolor": "#CFD8DC",
        "plot_text_arrow_color": "#9AA4AE",
        "plot_heatmap_cmap": COLORS.Purples,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
        "plot_heatmap_frame_color": "#9AA4AE",
    }
)
"""The minimal theme: accent violet, no spines, flat bars.
"""
