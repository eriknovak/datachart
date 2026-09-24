from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import LINE_STYLE, COLORS

# five slate greys 0.16 apart: six of one hue cannot pass the gate (ADR 0073)
GREYS = [
    "#1A232B",  # near-black slate
    "#424B55",  # dark grey
    "#6F7983",  # medium grey
    "#9EA9B4",  # light grey
    "#D1DCE8",  # very light grey
]

GREYSCALE_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Greys,
        "color_general_multiple": GREYS,
        "color_parallel_hue": GREYS,
        "color_parallel_hue_continuous": [
            "#D9D9D9",
            "#969696",
            "#525252",
            "#000000",
        ],
        "plot_hatch_cycle": ["", "//", "..", "xx", "\\"],
        "plot_linestyle_cycle": ["-", "--", "-.", ":", "-"],
        "plot_marker_cycle": ["o", "s", "^", "D", "v"],
        "plot_bar_edge_width": 0.8,
        "plot_bar_edge_color": "#000000",
        "plot_stackedarea_edge_color": "#000000",
        "plot_sankey_node_edge_color": "#000000",
        "plot_treemap_edge_color": "#000000",
        "plot_network_node_edge_color": "#000000",
        "plot_hist_edge_color": "#000000",
        "plot_vline_color": "#5D6D7E",
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": "#5D6D7E",
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_dline_color": "#5D6D7E",
        "plot_dline_style": LINE_STYLE.DASHED,
        "plot_bracket_color": "#5D6D7E",
        "plot_vspan_color": "#5D6D7E",
        "plot_hspan_color": "#5D6D7E",
        "plot_text_box_edgecolor": "#B0B0B0",
        "plot_text_arrow_color": "#5D6D7E",
        "plot_gantt_dependency_color": "#2C3E50",
        "plot_gantt_today_color": "#2C3E50",
        "plot_dumbbell_start_color": "#9EA9B4",
        "plot_dumbbell_end_color": "#1A232B",
        "plot_dumbbell_edge_color": "#000000",
        "plot_dumbbell_connector_color": "#85929E",
        "plot_dumbbell_arrow_color": "#5D6D7E",
        "plot_heatmap_cmap": COLORS.Greys,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
        "plot_heatmap_frame_color": "#000000",
        "plot_regression_color": "#34495E",
        "plot_box_median_color": "#000000",
        "plot_violin_edgecolor": "#000000",
        "plot_violin_inner_color": "#000000",
        "plot_ridgeline_edgecolor": "#000000",
        "plot_ridgeline_inner_color": "#000000",
    }
)
"""The greyscale theme: five slate greys, hatches, dashes and markers, for print.

The greys sit 0.16 apart in lightness, so every pair reads apart on paper and
for every colour-blind reader alike; bars carry a hatch cycle, lines a dash
cycle and scatter points a marker cycle, so a sixth series still differs.
"""
