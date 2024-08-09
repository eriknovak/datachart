from ..utils.charts import chart_wrapper, draw_bar_chart
from ..typings import BarChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def BarChart(attrs: BarChartAttrs):
    """Draw a bar chart

    Parameters
    ----------
    attrs : BarChartAttrs
        The chart attributes.

    """
    return chart_wrapper(draw_bar_chart)({**attrs, "type": "barchart"})
