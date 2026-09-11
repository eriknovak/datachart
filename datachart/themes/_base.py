"""The shared base for the predefined themes.

`BASE_THEME` holds the complete modern default style; every theme is built by
overriding just the attributes that define its identity via `make_theme`.
"""

import copy

from ..typings import StyleAttrs
from ..constants import (
    ARROW_STYLE,
    LINE_STYLE,
    FONT_STYLE,
    FONT_WEIGHT,
    LINE_DRAW_STYLE,
    COLORS,
    LEGEND_LOCATION,
    SHOW_GRID,
)

# the bar-specific value label keys predate the shared family; they resolve
# to it wherever a style is read (ADR 0033)
STYLE_ALIASES = {
    "plot_bar_value_fontsize": "plot_value_fontsize",
    "plot_bar_value_color": "plot_value_color",
    "plot_bar_value_padding": "plot_value_padding",
}


def canonical_style(style: dict) -> dict:
    """`style` with every alias key renamed.

    An alias present in `style` wins over the canonical key: the alias was
    written by hand, while the canonical key usually arrives by spreading a
    predefined theme underneath it.
    """

    resolved = {k: v for k, v in style.items() if k not in STYLE_ALIASES}
    for alias, key in STYLE_ALIASES.items():
        if alias in style:
            resolved[key] = style[alias]
    return resolved


BASE_THEME: StyleAttrs = {
    # general color style
    "color_general_singular": COLORS.Blues,
    "color_general_multiple": [
        "#4E79A7",
        "#F28E2B",
        "#59A14F",
        "#E15759",
        "#B07AA1",
        "#76B7B2",
    ],
    "color_parallel_hue": COLORS.Tab10,
    "color_parallel_hue_continuous": ["#C6DBEF", "#6BAED6", "#2171B5", "#08306B"],
    # muted style, applied to background-emphasis layers (ADR 0009)
    "muted_color": "#CFCFCF",
    "muted_alpha": 0.5,
    # general font style
    "font_general_family": "sans-serif",
    "font_general_sansserif": ["Helvetica", "Arial", "Liberation Sans"],
    "font_general_serif": None,
    "font_general_color": "#000000",
    "font_general_size": 10,
    "font_general_style": FONT_STYLE.NORMAL,
    "font_general_weight": FONT_WEIGHT.NORMAL,
    # title size style
    "font_title_size": 14,
    "font_title_color": "#000000",
    "font_title_style": FONT_STYLE.NORMAL,
    "font_title_weight": FONT_WEIGHT.NORMAL,
    # subtitle size style
    "font_subtitle_size": 10,
    "font_subtitle_color": "#000000",
    "font_subtitle_style": FONT_STYLE.NORMAL,
    "font_subtitle_weight": FONT_WEIGHT.NORMAL,
    # xlabel size style
    "font_xlabel_size": 9,
    "font_xlabel_color": "#000000",
    "font_xlabel_style": FONT_STYLE.NORMAL,
    "font_xlabel_weight": FONT_WEIGHT.NORMAL,
    # ylabel size style
    "font_ylabel_size": 9,
    "font_ylabel_color": "#000000",
    "font_ylabel_style": FONT_STYLE.NORMAL,
    "font_ylabel_weight": FONT_WEIGHT.NORMAL,
    # plot axes style
    "axes_spines_top_visible": False,
    "axes_spines_right_visible": False,
    "axes_spines_bottom_visible": True,
    "axes_spines_left_visible": True,
    "axes_spines_width": 0.8,
    "axes_spines_zorder": 100,
    "axes_ticks_length": 3,
    "axes_ticks_label_size": 8,
    # theme-level chart-setting defaults (ADR 0004)
    "chart_default_show_grid": SHOW_GRID.Y,
    "chart_default_show_values": None,
    "plot_hatch_cycle": None,
    # render-scoped rc attributes (ADR 0027); None means off
    "plot_sketch_params": None,
    "plot_sketch_halo_width": None,
    # plot legend style
    "plot_legend_shadow": False,
    "plot_legend_frameon": True,
    "plot_legend_alignment": "left",
    "plot_legend_location": LEGEND_LOCATION.BEST,
    "plot_legend_font_size": 8,
    "plot_legend_title_size": 9,
    "plot_legend_label_color": "#000000",
    "plot_legend_title": "Legend",
    "plot_legend_ncols": 1,
    # plot area style
    "plot_area_alpha": 0.25,
    "plot_area_color": None,
    "plot_area_linewidth": 0,
    "plot_area_hatch": None,
    "plot_area_zorder": 3,
    # plot stackedarea style; the fill reuses the area keys and the band
    # stroke mirrors plot_bar_edge_* (ADR 0025)
    "plot_stackedarea_alpha": 0.8,
    "plot_stackedarea_outline": False,
    "plot_stackedarea_edge_color": "#FFFFFF",
    "plot_stackedarea_edge_width": 0.6,
    # plot sankey style; the node stroke mirrors plot_bar_edge_* (ADR 0026)
    "plot_sankey_node_width": 0.04,
    "plot_sankey_node_pad": 0.10,
    "plot_sankey_node_edge_color": "#FFFFFF",
    "plot_sankey_node_edge_width": 0.6,
    "plot_sankey_link_color": "source",
    "plot_sankey_link_alpha": 0.4,
    "plot_sankey_label_halo_width": 2,
    # plot treemap style; the leaf stroke mirrors plot_bar_edge_* (ADR 0028)
    "plot_treemap_edge_color": "#FFFFFF",
    "plot_treemap_edge_width": 0.6,
    "plot_treemap_group_edge_width": 1.0,
    "plot_treemap_group_pad": 0.01,
    "plot_treemap_level_shade": 0.35,
    "plot_treemap_level_font_scale": 0.85,
    "plot_treemap_min_fontsize": 6,
    "plot_treemap_highlight_edge_width": 2.0,
    "plot_treemap_label_halo_width": 2,
    # plot network style; nodes mirror plot_scatter_*, edges take the Sankey
    # grey (ADR 0029)
    "plot_network_node_color": None,
    "plot_network_node_alpha": 0.95,
    "plot_network_node_marker": "o",
    "plot_network_node_size": 200,
    "plot_network_node_size_min": 80,
    "plot_network_node_size_max": 900,
    "plot_network_node_edge_color": "#FFFFFF",
    "plot_network_node_edge_width": 0.8,
    "plot_network_edge_style": ARROW_STYLE.CURVE,
    "plot_network_edge_curve": 0.2,
    "plot_network_edge_color": "#9E9E9E",
    "plot_network_edge_alpha": 0.6,
    "plot_network_edge_width_min": 0.8,
    "plot_network_edge_width_max": 4.0,
    "plot_network_highlight_edge_width": 2.0,
    "plot_network_label_halo_width": 2,
    "plot_network_group_alpha": 0.12,
    # plot grid style
    "plot_grid_alpha": 0.5,
    "plot_grid_color": "#EAEAEA",
    "plot_grid_linewidth": 0.5,
    "plot_grid_linestyle": LINE_STYLE.SOLID,
    "plot_grid_zorder": 0,
    # plot line style
    "plot_line_color": None,
    "plot_line_style": LINE_STYLE.SOLID,
    "plot_line_marker": None,
    "plot_line_width": 1.5,
    "plot_line_alpha": 1.0,
    "plot_line_drawstyle": LINE_DRAW_STYLE.DEFAULT,
    "plot_line_zorder": 3,
    # plot bar style
    "plot_bar_color": None,
    "plot_bar_alpha": 0.9,
    "plot_bar_width": 0.8,
    "plot_bar_zorder": 3,
    "plot_bar_hatch": None,
    "plot_bar_edge_width": 0.6,
    "plot_bar_edge_color": "#FFFFFF",
    "plot_bar_error_color": "#000000",
    # value label style, shared by every chart that prints values (ADR 0033)
    "plot_value_fontsize": 8,
    "plot_value_color": "#000000",
    "plot_value_padding": 3,
    "plot_value_halo_width": 2,
    # plot hist style
    "plot_hist_color": None,
    "plot_hist_alpha": 0.9,
    "plot_hist_zorder": 3,
    "plot_hist_fill": None,
    "plot_hist_hatch": None,
    "plot_hist_type": "bar",
    "plot_hist_align": "mid",
    "plot_hist_edge_width": 0.8,
    "plot_hist_edge_color": "#FFFFFF",
    # plot vline style
    "plot_vline_color": None,
    "plot_vline_style": LINE_STYLE.SOLID,
    "plot_vline_width": 1,
    "plot_vline_alpha": 0.7,
    # plot hline style
    "plot_hline_color": None,
    "plot_hline_style": LINE_STYLE.SOLID,
    "plot_hline_width": 1,
    "plot_hline_alpha": 0.7,
    # plot vspan (vertical reference band) style; None color: the muted color
    "plot_vspan_color": None,
    "plot_vspan_alpha": 0.25,
    "plot_vspan_hatch": None,
    "plot_vspan_edge_color": None,
    "plot_vspan_edge_width": 0.8,
    "plot_vspan_zorder": 1.75,
    # plot hspan (horizontal reference band) style
    "plot_hspan_color": None,
    "plot_hspan_alpha": 0.25,
    "plot_hspan_hatch": None,
    "plot_hspan_edge_color": None,
    "plot_hspan_edge_width": 0.8,
    "plot_hspan_zorder": 1.75,
    # plot text (annotation) style
    "plot_text_color": None,
    "plot_text_size": 9.5,
    "plot_text_weight": FONT_WEIGHT.NORMAL,
    "plot_text_halign": "left",
    "plot_text_valign": "center",
    "plot_text_alpha": 1.0,
    "plot_text_box_visible": True,
    "plot_text_box_style": "round,pad=0.4",
    "plot_text_box_facecolor": "#FFFFFF",
    "plot_text_box_edgecolor": "#B4BCC4",
    "plot_text_box_edge_width": 0.8,
    "plot_text_box_alpha": 0.92,
    "plot_text_arrow_style": ARROW_STYLE.CURVE,
    "plot_text_arrow_curve": None,
    "plot_text_arrow_color": "#7F8C8D",
    "plot_text_arrow_width": 1.0,
    # plot heatmap style
    "plot_heatmap_cmap": COLORS.Blues,
    "plot_heatmap_alpha": 0.95,
    "plot_heatmap_font_size": 8,
    "plot_heatmap_font_color": "#000000",
    "plot_heatmap_font_style": FONT_STYLE.NORMAL,
    "plot_heatmap_font_weight": FONT_WEIGHT.NORMAL,
    "plot_heatmap_frame_color": "#333333",
    "plot_heatmap_edge_width": 0,
    "plot_heatmap_edge_color": "#FFFFFF",
    # plot contour style; None derives from the line/heatmap/font keys (ADR 0022)
    "plot_contour_color": None,
    "plot_contour_cmap": None,
    "plot_contour_line_width": None,
    "plot_contour_line_style": LINE_STYLE.SOLID,
    "plot_contour_alpha": 1.0,
    "plot_contour_zorder": 3,
    "plot_contour_label_font_size": None,
    "plot_contour_label_font_color": None,
    # plot hexbin style; None cmap derives from the heatmap cmap (ADR 0024)
    "plot_hexbin_cmap": None,
    "plot_hexbin_alpha": 1.0,
    "plot_hexbin_edge_width": 0,
    "plot_hexbin_edge_color": "#FFFFFF",
    "plot_hexbin_gridsize": 30,
    # plot scatter style
    "plot_scatter_color": None,
    "plot_scatter_alpha": 0.75,
    "plot_scatter_size": 36,
    "plot_scatter_marker": "o",
    "plot_scatter_zorder": 3,
    "plot_scatter_edge_width": 0.5,
    "plot_scatter_edge_color": "#FFFFFF",
    # plot regression style
    "plot_regression_color": None,
    "plot_regression_alpha": 0.9,
    "plot_regression_width": 2,
    "plot_regression_style": LINE_STYLE.SOLID,
    "plot_regression_ci_alpha": 0.15,
    # plot parallel coords style
    "plot_parallel_color": None,
    "plot_parallel_alpha": 0.6,
    "plot_parallel_width": 1.2,
    "plot_parallel_style": LINE_STYLE.SOLID,
    "plot_parallel_marker": None,
    "plot_parallel_zorder": 1,
    "plot_parallel_axis_color": "#000000",
    "plot_parallel_axis_width": 1.5,
    "plot_parallel_axis_zorder": 2,
    "plot_parallel_tick_color": "#000000",
    "plot_parallel_tick_width": 1.5,
    "plot_parallel_tick_length": 0.02,
    "plot_parallel_tick_label_size": 8,
    "plot_parallel_tick_label_color": "#000000",
    "plot_parallel_tick_label_bg_color": "#FFFFFF",
    "plot_parallel_tick_label_bg_alpha": 0.8,
    "plot_parallel_dim_label_size": 9,
    "plot_parallel_dim_label_color": "#000000",
    "plot_parallel_dim_label_rotation": 0,
    "plot_parallel_dim_label_pad": 8,
    # plot box style
    "plot_box_color": None,
    "plot_box_alpha": 0.85,
    "plot_box_linewidth": 0.8,
    "plot_box_edgecolor": "#000000",
    "plot_box_outlier_marker": "o",
    "plot_box_outlier_size": 5,
    "plot_box_outlier_color": "#FFFFFF",
    "plot_box_outlier_edge_color": "#000000",
    "plot_box_median_color": "#2C3E50",
    "plot_box_median_linewidth": 2,
    "plot_box_whisker_color": "#000000",
    "plot_box_whisker_linewidth": 0.8,
    "plot_box_cap_color": "#000000",
    "plot_box_cap_linewidth": 0.8,
    # plot swarm style; zorder sits above the box patches and strokes
    "plot_swarm_color": None,
    "plot_swarm_size": 18,
    "plot_swarm_alpha": 0.85,
    "plot_swarm_marker": "o",
    "plot_swarm_edge_width": 0.5,
    "plot_swarm_edge_color": "#FFFFFF",
    "plot_swarm_zorder": 3,
    # plot violin style
    "plot_violin_color": None,
    "plot_violin_alpha": 1.0,
    "plot_violin_linewidth": 1.0,
    "plot_violin_edgecolor": None,
    "plot_violin_width": 0.8,
    "plot_violin_inner_color": None,
    "plot_violin_inner_linewidth": 1.0,
    "plot_violin_median_color": "#FFFFFF",
    "plot_violin_median_size": 4,
    "plot_xticks_label_rotate": None,
    "plot_yticks_label_rotate": None,
    # overlay chart style
    "overlay_auto_threshold": 3.0,
    "overlay_bar_alpha": 0.7,
    "overlay_hist_alpha": 0.6,
    "overlay_default_zorder_bar": 1,
    "overlay_default_zorder_line": 2,
    "overlay_default_zorder_scatter": 2,
    "overlay_default_zorder_hist": 1,
    "overlay_bar_mode": "group",
    "overlay_warn_thin_bars": True,
    "overlay_warn_scale_groups": True,
    "overlay_warn_scale_conflict": True,
}


def make_theme(overrides: StyleAttrs) -> StyleAttrs:
    """Build a complete theme: the base with the theme's own attributes applied."""

    theme = copy.deepcopy(BASE_THEME)
    theme.update(copy.deepcopy(overrides))
    return theme
