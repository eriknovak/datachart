from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS

# the two-tone ground: a near-black page with the plotting area a step lighter
PAGE = "#14171C"
PANEL = "#1C2027"
# the furniture, stepped from the brightest text down to the grid hairlines
BRIGHT = "#E6EDF3"
TEXT = "#C9D1D9"
DIM = "#8B949E"
LINE = "#3A414B"
GRID = "#2A2F37"

DARK_THEME: StyleAttrs = make_theme(
    {
        # azure, amber, mint, rose, violet and a near-white, every one lifted
        # clear of the panel; every pair stays apart for deutan, protan and
        # tritan readers (OKLab ΔE ≥ 11.0)
        "color_general_singular": COLORS.Viridis,
        "color_general_multiple": [
            "#63A6DE",
            "#CFA23A",
            "#4FE49B",
            "#DC5470",
            "#A35CE8",
            "#E6E9F2",
        ],
        # the bright half of the value scale; its dark end would sink into the panel
        "color_parallel_hue_continuous": [
            "#009C95",
            "#00BE7D",
            "#98D84A",
            "#FDE333",
        ],
        # a background-emphasis layer recedes towards the panel, not away from it
        "muted_color": "#4A515B",
        "font_general_color": TEXT,
        "font_title_color": BRIGHT,
        "font_subtitle_color": DIM,
        "font_xlabel_color": TEXT,
        "font_ylabel_color": TEXT,
        "figure_facecolor": PAGE,
        "axes_facecolor": PANEL,
        "axes_spines_color": LINE,
        "axes_ticks_color": LINE,
        "plot_grid_color": GRID,
        "plot_grid_alpha": 1.0,
        "plot_legend_label_color": TEXT,
        "plot_legend_edge_color": LINE,
        "plot_legend_face_color": PANEL,
        # a separator between neighbouring marks is the ground showing through
        "plot_stackedarea_edge_color": PAGE,
        "plot_sankey_node_edge_color": PAGE,
        "plot_treemap_edge_color": PAGE,
        "plot_network_node_edge_color": PAGE,
        "plot_network_edge_color": DIM,
        "plot_bar_edge_color": PAGE,
        "plot_bar_error_color": TEXT,
        "plot_hist_edge_color": PAGE,
        "plot_hexbin_edge_color": PAGE,
        "plot_scatter_edge_color": PAGE,
        "plot_swarm_edge_color": PAGE,
        "plot_gantt_dependency_color": DIM,
        "plot_gantt_today_color": "#FF6B6B",
        "plot_dumbbell_start_color": "#CFA23A",
        "plot_dumbbell_end_color": "#63A6DE",
        "plot_dumbbell_edge_color": PAGE,
        "plot_dumbbell_connector_color": "#6E7681",
        "plot_dumbbell_arrow_color": DIM,
        "plot_value_color": BRIGHT,
        "plot_text_color": BRIGHT,
        "plot_text_box_facecolor": "#242A33",
        "plot_text_box_edgecolor": LINE,
        "plot_text_arrow_color": DIM,
        # Viridis reads dark-to-light, so a cell's value rises off the panel
        "plot_heatmap_cmap": COLORS.Viridis,
        "plot_heatmap_cmap_diverging": COLORS.Coolwarm,
        # the cell label follows its own cell, so a light cell keeps the base
        # dark text; only the frame and the separators invert (ADR 0058)
        "plot_heatmap_frame_color": TEXT,
        "plot_heatmap_edge_color": PAGE,
        "plot_calendar_heatmap_edge_color": PAGE,
        "plot_calendar_heatmap_month_line_color": TEXT,
        "plot_parallel_axis_color": TEXT,
        "plot_parallel_tick_color": TEXT,
        "plot_parallel_tick_label_color": BRIGHT,
        "plot_parallel_tick_label_bg_color": PANEL,
        "plot_parallel_dim_label_color": TEXT,
        "plot_box_edgecolor": TEXT,
        "plot_box_median_color": BRIGHT,
        "plot_box_whisker_color": TEXT,
        "plot_box_cap_color": TEXT,
        "plot_box_outlier_color": PANEL,
        "plot_box_outlier_edge_color": TEXT,
    }
)
"""The dark theme: bright marks on a near-black page.

The page is near-black and the plotting area a step lighter, so the panel
reads as a card. Every furniture colour — spines, ticks, fonts, grid, legend
frame, value labels, annotation boxes, heatmap frame and separators — carries
a light counterpart, and the marks take a six-colour bright palette over the
Viridis value scale.
"""
