from ..utils.charts import chart_wrapper, draw_heatmap
from ..definitions import HeatmapChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def heatmap(attrs: HeatmapChartAttrs):
    """Draw a heatmap chart

    Parameters
    ----------
    attrs : HeatmapChartAttrs
        The chart attributes.

    """
    return chart_wrapper(draw_heatmap)({**attrs, "type": "heatmap"})
