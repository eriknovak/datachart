import matplotlib.pyplot as plt

from ..utils.charts import chart_plot_wrapper, plot_line_chart
from ..typings import LineChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def LineChart(attrs: LineChartAttrs) -> plt.Figure:
    """Creates the line chart.

    Args:
        attrs: The line chart attributes.

    Returns:
        The figure containing the line chart.

    """
    return chart_plot_wrapper(plot_line_chart)({**attrs, "type": "linechart"})
