from utils.charts import chart_wrapper, draw_bar_chart


# ================================================
# Main Chart Definition
# ================================================


def bar_chart(attrs):
    """Draw a bar chart

    Args:
        attrs (dict): The chart attributes.
    """
    return chart_wrapper(draw_bar_chart)(attrs)
