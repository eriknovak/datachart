from ._base import make_theme, register_bundled_fonts
from ..typings import StyleAttrs
from ..constants import (
    ARROW_STYLE,
    COLORS,
    FONT_STYLE,
    FONT_WEIGHT,
    LINE_STYLE,
    NETWORK_LABEL_POSITION,
)

# IM Fell English Roman, Italic and SC (SIL OFL, licence alongside)
register_bundled_fonts("IMFeENrm28P.ttf", "IMFeENit28P.ttf", "IMFeENsc28P.ttf")

INK = "#1A120A"
PAPER = "#FFFFFF"
# iron-gall ink faded to brown, for the hairlines behind the marks
FADED_INK = "#6B5A3C"

QUILL_THEME: StyleAttrs = make_theme(
    {
        # one ink: series differ by line style, marker and etching, never color
        "color_general_singular": COLORS.Greys,
        "color_general_multiple": [INK],
        "color_parallel_hue": [INK],
        "color_parallel_hue_continuous": ["#D9CCAA", "#8C7E5E", "#4A3C2A", INK],
        "muted_color": "#C9B892",
        "font_general_family": "serif",
        # the fallbacks only apply when the bundled face fails to register
        "font_general_serif": ["IM FELL English", "IM FELL English SC", "Georgia"],
        "font_general_size": 11,
        "font_general_color": INK,
        "font_title_size": 16,
        "font_title_color": INK,
        "font_title_style": FONT_STYLE.ITALIC,
        "font_title_weight": FONT_WEIGHT.NORMAL,
        "font_subtitle_color": INK,
        "font_xlabel_color": INK,
        "font_ylabel_color": INK,
        "axes_spines_color": INK,
        "axes_ticks_color": INK,
        "axes_spines_width": 1.4,
        "axes_ticks_length": 5,
        "axes_ticks_label_size": 9,
        "chart_default_show_grid": None,
        "chart_default_node_label_position": NETWORK_LABEL_POSITION.ABOVE,
        "plot_hatch_cycle": ["/", ".", "\\", "x", "-", "|"],
        # lists, not tuples, so the theme survives a JSON round trip (ADR 0040)
        "plot_linestyle_cycle": [
            "-",
            "--",
            ":",
            "-.",
            [0, [7, 2, 1, 2, 1, 2]],
            [0, [2, 2]],
        ],
        # shape and fill alternate so neighbouring series never look alike
        "plot_marker_cycle": [
            "o",
            {"marker": "s", "hollow": True},
            "^",
            {"marker": "D", "hollow": True},
            "v",
            {"marker": "P", "hollow": True},
        ],
        "plot_sketch_params": [0.7, 90, 2],
        # a broad nib at 32 degrees, 1.6 times the line width
        "plot_ink_stroke": {
            "width_scale": 1.6,
            "nib_angle": 32,
            "nib_floor": 0.35,
            "wobble": 0.22,
            "taper": 7,
        },
        # a 10% ink wash under the etching of bars and bodies
        "plot_etch": {
            "spacing": 4.2,
            "jitter": 0.3,
            "angle_jitter": 2.5,
            "line_width": 0.6,
            "wash": 0.1,
            "color": INK,
        },
        # a value scale reads as etch density alone, on bare paper
        "plot_value_etch": {
            "washes": [PAPER] * 5,
            "hatches": ["", ".", "..", "//", "xx"],
        },
        "plot_legend_label_color": INK,
        "plot_legend_font_size": 9,
        "plot_legend_title_size": 10,
        "plot_legend_edge_color": INK,
        "plot_line_width": 2.2,
        "plot_area_alpha": 1.0,
        "plot_area_linewidth": 0.8,
        "plot_stackedarea_alpha": 1.0,
        "plot_stackedarea_outline": True,
        "plot_stackedarea_edge_color": INK,
        "plot_stackedarea_edge_width": 0.9,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 1.0,
        "plot_bar_edge_color": INK,
        "plot_bar_error_color": INK,
        "plot_value_color": INK,
        # a value over marks sits on a ruled paper tab, as a label ribbon on an
        # engraving; the halo serves the labels that take no tab
        "plot_value_halo_width": 5,
        "plot_value_tab": {
            "facecolor": PAPER,
            "edgecolor": INK,
            "line_width": 0.6,
            "pad": 0.16,
            "rounding": 0.1,
        },
        "plot_hist_alpha": 1.0,
        "plot_hist_edge_width": 1.0,
        "plot_hist_edge_color": INK,
        "plot_vline_color": INK,
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": INK,
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_dline_color": INK,
        "plot_dline_style": LINE_STYLE.DASHED,
        "plot_bracket_color": INK,
        "plot_vspan_color": INK,
        "plot_hspan_color": INK,
        "plot_vspan_alpha": 1.0,
        "plot_hspan_alpha": 1.0,
        "plot_vspan_hatch": ".",
        "plot_hspan_hatch": ".",
        "plot_vspan_edge_color": INK,
        "plot_hspan_edge_color": INK,
        "plot_text_color": INK,
        "plot_text_box_facecolor": PAPER,
        "plot_text_box_edgecolor": INK,
        "plot_text_box_style": "round,pad=0.4,rounding_size=0.2",
        "plot_text_arrow_color": INK,
        "plot_gantt_dependency_color": INK,
        "plot_gantt_today_color": INK,
        "plot_dumbbell_start_color": PAPER,
        "plot_dumbbell_end_color": INK,
        "plot_dumbbell_edge_color": INK,
        "plot_dumbbell_edge_width": 0.8,
        "plot_dumbbell_connector_color": INK,
        "plot_dumbbell_arrow_color": INK,
        "plot_dumbbell_connector_width": 1.2,
        "plot_heatmap_cmap": COLORS.Greys,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
        "plot_heatmap_frame_color": INK,
        "plot_heatmap_font_color": INK,
        # IM Fell's old-style figures run small: values sit a size up
        "plot_heatmap_font_size": 10,
        "plot_calendar_heatmap_font_size": 8,
        "plot_heatmap_edge_width": 0.6,
        "plot_heatmap_edge_color": INK,
        "plot_calendar_heatmap_edge_color": PAPER,
        "plot_calendar_heatmap_month_line_color": INK,
        "plot_contour_color": INK,
        "plot_contour_line_width": 1.8,
        "plot_hexbin_edge_width": 0.3,
        "plot_hexbin_edge_color": INK,
        "plot_scatter_edge_width": 0.8,
        "plot_scatter_edge_color": INK,
        "plot_scatter_alpha": 0.8,
        "plot_swarm_edge_width": 0.6,
        "plot_swarm_edge_color": INK,
        "plot_swarm_alpha": 0.9,
        "plot_regression_color": INK,
        "plot_regression_ci_alpha": 0.12,
        "plot_parallel_color": INK,
        "plot_parallel_alpha": 0.35,
        "plot_parallel_axis_color": INK,
        "plot_parallel_tick_color": INK,
        "plot_parallel_tick_label_color": INK,
        "plot_parallel_tick_label_size": 9,
        # labels read through a paper halo, as Sankey and treemap labels do
        "plot_parallel_tick_label_bg_color": None,
        "plot_parallel_dim_label_color": INK,
        "plot_box_edgecolor": INK,
        "plot_box_linewidth": 1.2,
        "plot_box_hatch": "/",
        "plot_box_median_color": INK,
        "plot_box_median_linewidth": 2.5,
        "plot_box_whisker_color": INK,
        "plot_box_whisker_linewidth": 1.2,
        "plot_box_cap_color": INK,
        "plot_box_cap_linewidth": 1.2,
        "plot_box_outlier_color": PAPER,
        "plot_box_outlier_edge_color": INK,
        "plot_box_alpha": 1.0,
        "plot_violin_edgecolor": INK,
        "plot_violin_linewidth": 1.2,
        "plot_violin_alpha": 1.0,
        "plot_violin_hatch": "\\",
        "plot_violin_inner_color": INK,
        "plot_violin_median_color": PAPER,
        "plot_ridgeline_edgecolor": INK,
        "plot_ridgeline_linewidth": 1.2,
        "plot_ridgeline_alpha": 1.0,
        "plot_ridgeline_hatch": "/",
        "plot_ridgeline_inner_color": INK,
        "plot_sankey_link_alpha": 0.25,
        "plot_sankey_node_edge_color": INK,
        "plot_sankey_node_edge_width": 1.0,
        "plot_sankey_node_fill": False,
        "plot_treemap_edge_color": INK,
        "plot_treemap_edge_width": 1.0,
        "plot_treemap_level_shade": 0.55,
        # dense around a group's band and gutters, sparse on its tiles
        "plot_treemap_etch_density": [3, 1, 0],
        "plot_network_node_edge_color": INK,
        "plot_network_node_edge_width": 1.2,
        "plot_network_node_size": 70,
        "plot_network_node_alpha": 1.0,
        # groups differ by the marker cycle's shapes, filled and hollow
        "plot_network_edge_color": FADED_INK,
        "plot_network_edge_alpha": 0.6,
        "plot_network_edge_style": ARROW_STYLE.STRAIGHT,
        "plot_network_edge_curve": 0.0,
        # hairline roads, as the rhumb lines of a portolan chart, stay countable
        "plot_network_edge_width_min": 0.5,
        "plot_network_edge_width_max": 1.3,
        "plot_network_edge_ink_stroke": {
            "width_scale": 1.0,
            "nib_floor": 1.0,
            "wobble": 0.0,
            "swell": 0.0,
            "noise": 0.05,
        },
        # names in small caps; the halo clears the plate round each, as an
        # engraver leaves it bare, so edges stop short of a label
        "plot_network_label_family": "IM FELL English SC",
        "plot_network_label_halo_width": 5,
        "plot_network_group_linestyle": LINE_STYLE.DOTTED,
    }
)
"""The quill theme: black ink on white paper, as a quill and an etching needle draw.

One ink only: series differ by line style, marker and etching, never by
color. Series lines are broad-nib pen strokes whose width varies along the
line, bars, areas and bodies are etched by hand instead of hatched, the
furniture wobbles, and text is set in IM Fell English, which ships with the
package, titles in its italic.
"""
