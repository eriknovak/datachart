from ..utils.charts import chart_wrapper, draw_histogram
from ..typings import HistogramChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def Histogram(attrs: HistogramChartAttrs):
    """Draw a line chart

    Parameters
    ----------
    attrs : HistChartAttrs
        The chart attributes.

    """

    return chart_wrapper(draw_histogram)({**attrs, "type": "histogram"})
