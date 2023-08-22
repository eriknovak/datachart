from ..utils.charts import chart_wrapper, draw_hist_chart
from ..schema.definitions import HistChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def hist_chart(attrs: HistChartAttrs):
    """Draw a line chart

    Parameters
    ----------
    attrs : HistChartAttrs
        The chart attributes.

    """

    return chart_wrapper(draw_hist_chart)(attrs)
