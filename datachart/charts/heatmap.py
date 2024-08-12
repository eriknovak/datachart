import matplotlib.pyplot as plt

from ..utils.charts import chart_plot_wrapper, plot_heatmap
from ..typings import HeatmapChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def Heatmap(attrs: HeatmapChartAttrs) -> plt.Figure:
    """Creates the heatmap.

    Examples:
        >>> from datachart.charts import Heatmap
        >>> figure = Heatmap({
        ...     "charts": {
        ...         "data": [
        ...             [1, 2, 3],
        ...             [4, 5, 6],
        ...             [7, 8, 9]
        ...         ],
        ...     },
        ...     "title": "Basic Heatmap",
        ...     "xlabel": "X",
        ...     "ylabel": "Y",
        ... })


    Args:
        attrs: The heatmap chart attributes.

    Returns:
        The figure containing the heatmap.

    """

    return chart_plot_wrapper(plot_heatmap)({**attrs, "type": "heatmap"})
