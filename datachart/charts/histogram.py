from ..utils.charts import chart_wrapper, draw_histogram
from ..definitions import HistChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def histogram(attrs: HistChartAttrs):
    """Draw a line chart

    Parameters
    ----------
    attrs : HistChartAttrs
        The chart attributes.

    """

    return chart_wrapper(draw_histogram)({**attrs, "type": "histogram"})
