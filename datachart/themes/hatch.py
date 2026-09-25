from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import LINE_STYLE, COLORS

HATCH_THEME: StyleAttrs = make_theme(
    {
        # muted print tones under black edges and hatches, rust first, the
        # green deep enough to stay apart from rust for deutan readers
        "color_general_singular": COLORS.YlOrBr,
        "color_general_multiple": [
            "#B5563A",
            "#5A6F86",
            "#EBBC63",
            "#2C4A34",
            "#9F9A8D",
            "#966AD5",
        ],
        "color_parallel_hue_continuous": [
            "#F3E0C3",
            "#E0AE6A",
            "#B5563A",
            "#6B2E1A",
        ],
        "font_general_sansserif": [
            "Helvetica",
            "Arial",
            "Liberation Sans",
            "DejaVu Sans",
        ],
        # one hatch per series, so bar four never repeats bar one's solid
        "plot_hatch_cycle": ["", "//", "..", "xx", "\\", "--"],
        "plot_grid_color": "#D0D0D0",
        "plot_grid_linestyle": LINE_STYLE.DOTTED,
        "plot_grid_alpha": 0.8,
        "plot_bar_edge_color": "#000000",
        "plot_stackedarea_edge_color": "#000000",
        "plot_sankey_node_edge_color": "#000000",
        "plot_treemap_edge_color": "#000000",
        "plot_network_node_edge_color": "#000000",
        "plot_bar_edge_width": 0.8,
        "plot_bar_alpha": 1.0,
        "plot_hist_edge_color": "#000000",
        "plot_scatter_edge_color": "#000000",
        "plot_scatter_edge_width": 0.6,
        "plot_swarm_edge_color": "#000000",
        "plot_swarm_edge_width": 0.6,
        "plot_text_box_edgecolor": "#000000",
        "plot_text_arrow_color": "#000000",
        "plot_gantt_dependency_color": "#000000",
        "plot_gantt_today_color": "#000000",
        "plot_dumbbell_start_color": "#5A6F86",
        "plot_dumbbell_end_color": "#B5563A",
        "plot_dumbbell_edge_color": "#000000",
        "plot_dumbbell_connector_color": "#8C8C8C",
        "plot_dumbbell_arrow_color": "#000000",
        "plot_heatmap_cmap": COLORS.YlOrBr,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
        "plot_heatmap_frame_color": "#000000",
        "plot_violin_edgecolor": "#000000",
        "plot_ridgeline_edgecolor": "#000000",
    }
)
"""The hatch theme: hatch cycle, black edges, dotted grid.
"""
