import matplotlib.pyplot as plt

from ..utils.charts import chart_plot_wrapper, plot_histogram
from ..typings import HistogramChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def Histogram(attrs: HistogramChartAttrs) -> plt.Figure:
    """Creates the histogram.

    Examples:
        >>> from datachart.charts import Histogram
        >>> figure = Histogram({
        ...     "charts": {
        ...         "data": [
        ...             {"x": 1},
        ...             {"x": 2},
        ...             {"x": 3},
        ...             {"x": 4},
        ...             {"x": 5}
        ...         ],
        ...     },
        ...     "title": "Basic Histogram",
        ...     "xlabel": "X",
        ...     "ylabel": "Y",
        ... })

    Args:
        attrs: The histogram chart attributes.

    Returns:
        The figure containing the histogram.

    """

    return chart_plot_wrapper(plot_histogram)({**attrs, "type": "histogram"})
