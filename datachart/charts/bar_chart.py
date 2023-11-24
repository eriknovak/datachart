from ..utils.charts import chart_wrapper, draw_bar_chart
from ..definitions import BarChartAttrs

# ================================================
# Main Chart Definition
# ================================================


def bar_chart(attrs: BarChartAttrs):
    """Draw a bar chart

    Parameters
    ----------
    attrs : BarChartAttrs
        The chart attributes.

    """
    return chart_wrapper(draw_bar_chart)({**attrs, "type": "barchart"})
