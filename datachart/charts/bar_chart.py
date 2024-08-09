import matplotlib.pyplot as plt

from ..utils.charts import chart_plot_wrapper, plot_bar_chart
from ..typings import BarChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def BarChart(attrs: BarChartAttrs) -> plt.Figure:
    """Creates the bar chart.

    Args:
        attrs: The bar chart attributes.

    Returns:
        The figure containing the bar chart.

    """

    return chart_plot_wrapper(plot_bar_chart)({**attrs, "type": "barchart"})
