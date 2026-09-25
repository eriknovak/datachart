from ..typings import StyleAttrs
from ..constants import COLORS, TRAIT
from .default import DEFAULT_THEME
from .derive import derive_theme

HARBOR_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.Harbor,
    traits=[TRAIT.FLAT],
    color_general_singular=COLORS.Cividis,
    color_parallel_hue_continuous=["#BCAE6C", "#7D7C78", "#434E6C", "#00224E"],
    plot_dumbbell_start_color="#EFC98C",
    plot_dumbbell_end_color="#1F4E79",
    plot_heatmap_cmap=COLORS.Cividis,
    plot_heatmap_cmap_diverging=COLORS.RdBu,
)
"""The harbor theme: navy and amber in lightness steps, colour-blind safe.

The `Harbor` lead, two hue families, navy to sky and amber to sand, with taupe
and near-black closing the set; lightness does the separating, so every pair
of series stays apart for deutan, protan and tritan readers. The flat trait
gives edgeless opaque bars and 2 pt lines; the value scale is Cividis.
"""
