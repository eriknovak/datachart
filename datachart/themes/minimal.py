from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS

MINIMAL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": [
            "#2B7FFF",
            "#A9B4BE",
            "#7C8894",
            "#525C66",
            "#2E3740",
        ],
        "color_parallel_hue_continuous": [
            "#D9D9D9",
            "#A9B4BE",
            "#6FA0F5",
            "#2B7FFF",
        ],
        "font_general_color": "#1F1F1F",
        "font_title_color": "#1F1F1F",
        "axes_spines_top_visible": False,
        "axes_spines_right_visible": False,
        "axes_spines_left_visible": False,
        "axes_spines_bottom_visible": False,
        "axes_ticks_length": 0,
        "chart_default_show_values": True,
        "plot_grid_color": "#EFEFEF",
        "plot_grid_alpha": 1.0,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 0,
        "plot_bar_value_fontsize": 9,
        "plot_bar_value_color": "#1F1F1F",
        "plot_hist_edge_width": 0,
        "plot_line_width": 2.0,
        "plot_scatter_edge_color": "#FFFFFF",
        "plot_text_box_edgecolor": "#CFD8DC",
        "plot_text_arrow_color": "#9AA4AE",
        "plot_heatmap_cmap": COLORS.Blues,
        "plot_heatmap_frame_color": "#9AA4AE",
    }
)
