import matplotlib.pyplot as plt

from ..utils.charts import chart_plot_wrapper, plot_histogram
from ..typings import HistogramChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def Histogram(attrs: HistogramChartAttrs) -> plt.Figure:
    """Creates the histogram.

    Args:
        attrs: The histogram chart attributes.

    Returns:
        The figure containing the histogram.

    """

    return chart_plot_wrapper(plot_histogram)({**attrs, "type": "histogram"})
