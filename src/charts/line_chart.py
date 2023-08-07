from utils.charts import chart_wrapper, draw_line_chart

# ================================================
# Main Chart Definition
# ================================================


def line_chart(attrs):
    """Draw a line chart

    Args:
        attrs (dict): The chart attributes.
    """
    return chart_wrapper(draw_line_chart)(attrs)
