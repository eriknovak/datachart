import matplotlib.pyplot as plt

from ..utils.charts import chart_plot_wrapper, plot_heatmap
from ..typings import HeatmapChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def Heatmap(attrs: HeatmapChartAttrs) -> plt.Figure:
    """Creates the heatmap.

    Args:
        attrs: The heatmap chart attributes.

    Returns:
        The figure containing the heatmap.

    """

    return chart_plot_wrapper(plot_heatmap)({**attrs, "type": "heatmap"})
