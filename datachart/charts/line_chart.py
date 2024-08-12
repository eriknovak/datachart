import matplotlib.pyplot as plt

from ..utils.charts import chart_plot_wrapper, plot_line_chart
from ..typings import LineChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def LineChart(attrs: LineChartAttrs) -> plt.Figure:
    """Creates the line chart.

    Examples:
        >>> from datachart.charts import LineChart
        >>> figure = LineChart({
        ...     "charts": {
        ...         "data": [
        ...             {"x": 1, "y": 5},
        ...             {"x": 2, "y": 10},
        ...             {"x": 3, "y": 15},
        ...             {"x": 4, "y": 20},
        ...             {"x": 5, "y": 25}
        ...         ],
        ...     },
        ...     "title": "Basic Line Chart",
        ...     "xlabel": "X",
        ...     "ylabel": "Y",
        ... })

    Args:
        attrs: The line chart attributes.

    Returns:
        The figure containing the line chart.

    """
    return chart_plot_wrapper(plot_line_chart)({**attrs, "type": "linechart"})
