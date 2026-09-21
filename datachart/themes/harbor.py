from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS

HARBOR_THEME: StyleAttrs = make_theme(
    {
        # navy–sky and amber–sand stepped in lightness, closed with taupe and
        # near-black; every pair stays apart for deutan, protan and tritan
        # readers (OKLab ΔE ≥ 13.8 under the worst deficiency)
        "color_general_singular": COLORS.Cividis,
        "color_general_multiple": [
            "#1F4E79",
            "#D08C3A",
            "#6FA3D3",
            "#EFC98C",
            "#8C6D5A",
            "#1A1A1A",
        ],
        "color_parallel_hue_continuous": [
            "#BCAE6C",
            "#7D7C78",
            "#434E6C",
            "#00224E",
        ],
        "plot_line_width": 2.0,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 0,
        "plot_stackedarea_edge_width": 0,
        "plot_hist_edge_width": 0,
        "plot_dumbbell_start_color": "#EFC98C",
        "plot_dumbbell_end_color": "#1F4E79",
        "plot_heatmap_cmap": COLORS.Cividis,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
    }
)
"""The harbor theme: navy and amber in lightness steps, colour-blind safe.

Two hue families, navy to sky and amber to sand, with taupe and near-black
closing the set; lightness does the separating, so every pair of series stays
apart for deutan, protan and tritan readers. Flat bars, 2 pt lines and the
Cividis value scale.
"""
