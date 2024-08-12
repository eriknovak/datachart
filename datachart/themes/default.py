from ..typings import StyleAttrs
from ..constants import (
    LINE_STYLE,
    FONT_STYLE,
    FONT_WEIGHT,
    LINE_DRAW_STYLE,
    COLORS,
)

DEFAULT_THEME: StyleAttrs = {
    # general color style
    "color_general_singular": COLORS.Blue,
    "color_general_multiple": COLORS.Spectral,
    # general font style
    "font_general_family": "sans-serif",
    "font_general_sansserif": ["Helvetica", "Arial"],
    "font_general_color": "#000000",
    "font_general_size": 11,
    "font_general_style": FONT_STYLE.NORMAL,
    "font_general_weight": FONT_WEIGHT.NORMAL,
    # title size style
    "font_title_size": 12,
    "font_title_color": "#000000",
    "font_title_style": FONT_STYLE.NORMAL,
    "font_title_weight": FONT_WEIGHT.NORMAL,
    # subtitle size style
    "font_subtitle_size": 11,
    "font_subtitle_color": "#000000",
    "font_subtitle_style": FONT_STYLE.NORMAL,
    "font_subtitle_weight": FONT_WEIGHT.NORMAL,
    # xlabel size style
    "font_xlabel_size": 10,
    "font_xlabel_color": "#000000",
    "font_xlabel_style": FONT_STYLE.NORMAL,
    "font_xlabel_weight": FONT_WEIGHT.NORMAL,
    # ylabel size style
    "font_ylabel_size": 10,
    "font_ylabel_color": "#000000",
    "font_ylabel_style": FONT_STYLE.NORMAL,
    "font_ylabel_weight": FONT_WEIGHT.NORMAL,
    # plot axes style
    "axes_spines_top_visible": True,
    "axes_spines_right_visible": True,
    "axes_spines_bottom_visible": True,
    "axes_spines_left_visible": True,
    "axes_spines_width": 0.5,
    "axes_spines_zorder": 100,
    "axes_ticks_length": 2,
    "axes_ticks_label_size": 9,
    # plot legend style
    "plot_legend_shadow": False,
    "plot_legend_frameon": True,
    "plot_legend_alignment": "left",
    "plot_legend_font_size": 9,
    "plot_legend_title_size": 10,
    "plot_legend_label_color": "#000000",
    # plot area style
    "plot_area_alpha": 0.3,
    "plot_area_color": None,
    "plot_area_linewidth": 0,
    "plot_area_hatch": None,
    "plot_area_zorder": 3,
    # plot grid style
    "plot_grid_alpha": 1,
    "plot_grid_color": "#E6E6E6",
    "plot_grid_linewidth": 0.5,
    "plot_grid_linestyle": LINE_STYLE.SOLID,
    "plot_grid_zorder": 0,
    # plot line style
    "plot_line_color": None,
    "plot_line_style": LINE_STYLE.SOLID,
    "plot_line_marker": None,
    "plot_line_width": 1,
    "plot_line_alpha": 1.0,
    "plot_line_drawstyle": LINE_DRAW_STYLE.DEFAULT,
    "plot_line_zorder": 3,
    # plot bar style
    "plot_bar_color": None,
    "plot_bar_alpha": 1.0,
    "plot_bar_width": 0.8,
    "plot_bar_zorder": 3,
    "plot_bar_hatch": None,
    "plot_bar_edge_width": 0.5,
    "plot_bar_edge_color": "#000000",
    "plot_bar_error_color": "#000000",
    # plot hist style
    "plot_hist_color": None,
    "plot_hist_alpha": 1.0,
    "plot_hist_zorder": 3,
    "plot_hist_fill": None,
    "plot_hist_hatch": None,
    "plot_hist_type": "bar",
    "plot_hist_align": "mid",
    "plot_hist_edge_width": 0.5,
    "plot_hist_edge_color": "#000000",
    # plot vline style
    "plot_vline_color": None,
    "plot_vline_style": LINE_STYLE.SOLID,
    "plot_vline_width": 1,
    "plot_vline_alpha": 1.0,
    # plot hline style
    "plot_hline_color": None,
    "plot_hline_style": LINE_STYLE.SOLID,
    "plot_hline_width": 1,
    "plot_hline_alpha": 1.0,
    # plot heatmap style
    "plot_heatmap_cmap": COLORS.Blue,
    "plot_heatmap_alpha": 1.0,
    "plot_heatmap_font_size": 9,
    "plot_heatmap_font_color": "#000000",
    "plot_heatmap_font_style": FONT_STYLE.NORMAL,
    "plot_heatmap_font_weight": FONT_WEIGHT.NORMAL,
}
