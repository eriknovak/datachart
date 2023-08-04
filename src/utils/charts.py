import numpy as np
import matplotlib.pyplot as plt
from utils.stats import get_min_max_values
from utils.attrs import (
    get_line_config,
    get_area_config,
    get_grid_config,
    get_attr_value,
)


# ================================================
# Draw Line Chart
# ================================================


def draw_line_chart(
    ax: plt.Axes, chart: dict, draw_ci: bool = False, draw_grid: bool = False
) -> None:
    """Draw a line chart

    Args:
        ax: The axis to draw the chart.
        chart: The chart data.
        draw_ci: Whether to draw the confidence interval.
        draw_grid: Whether to draw the grid.
    """

    # get the chart style attributes
    style = chart.get("style", {})

    # retrieve the chart attributes
    x_attr = get_attr_value("x", chart, "x")
    y_attr = get_attr_value("y", chart, "y")
    delta_attr = get_attr_value("delta", chart, "delta")

    # retrieve the chart data points
    x = np.array([d[x_attr] for d in chart["data"]])
    y = np.array([d[y_attr] for d in chart["data"]])
    delta = np.array([d[delta_attr] for d in chart["data"] if delta_attr in d])

    if draw_ci and len(delta) == len(x) and len(delta) == len(y):
        # draw the confidence interval around the line
        y_min = y - delta
        y_max = y + delta
        ax.fill_between(x, y_min, y_max, **get_area_config(style))

    # draw the line chart
    ax.plot(x, y, **get_line_config(style))

    if draw_grid:
        # show the chart grid
        ax.grid(axis="both", **get_grid_config(chart))

    # set the x-axis limit
    xmin, xmax = get_min_max_values(x)
    ax.set_xlim(xmin, xmax)
