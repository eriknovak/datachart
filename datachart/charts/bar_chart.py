import matplotlib.pyplot as plt

from ..utils.charts import chart_plot_wrapper, plot_bar_chart
from ..typings import BarChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def BarChart(attrs: BarChartAttrs) -> plt.Figure:
    """Creates the bar chart.

    Examples:
        >>> from datachart.charts import BarChart
        >>> figure = BarChart({
        ...     "charts": {
        ...         "data": [
        ...             {"label": "cat1", "y": 5},
        ...             {"label": "cat2", "y": 10},
        ...             {"label": "cat3", "y": 15},
        ...             {"label": "cat4", "y": 20},
        ...             {"label": "cat5", "y": 25}
        ...         ],
        ...     },
        ...     "title": "Basic Bar Chart",
        ...     "xlabel": "LABEL",
        ...     "ylabel": "Y",
        ... })

    Args:
        attrs: The bar chart attributes.

    Returns:
        The figure containing the bar chart.

    """

    return chart_plot_wrapper(plot_bar_chart)({**attrs, "type": "barchart"})
