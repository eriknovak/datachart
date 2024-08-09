from ..utils.charts import chart_wrapper, draw_line_chart
from ..typings import LineChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def LineChart(attrs: LineChartAttrs):
    """Draw a line chart

    Parameters
    ----------
    attrs : LineChartAttrs
        The chart attributes.

    """
    return chart_wrapper(draw_line_chart)({**attrs, "type": "linechart"})
