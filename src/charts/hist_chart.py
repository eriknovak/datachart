from utils.charts import chart_wrapper, draw_hist_chart

# ================================================
# Main Chart Definition
# ================================================


def hist_chart(attrs):
    """Draw a line chart

    Args:
        attrs (dict): The chart attributes.
    """
    return chart_wrapper(draw_hist_chart)(attrs)
