import numpy as np
import matplotlib.pyplot as plt

# input the configuration
from config import config

from utils.charts import draw_line_chart
from utils.attrs import (
    configure_axes_spines,
    configure_axis_ticks,
    get_subplot_config,
    get_text_config,
)


# ================================================
# Import Schema Definitions
# ================================================

from schema.definitions import LineChartAttrs


# ================================================
# Main Chart Definition
# ================================================


def line_chart(attrs: LineChartAttrs):
    # check how many data point are there
    if not isinstance(attrs["charts"], dict) and not isinstance(attrs["charts"], list):
        raise ValueError("Parameter `attrs['charts']` is not correctly structured")

    # retrieve attributes
    charts = attrs.get("charts")
    draw_ci = attrs.get("draw_confidence_interval", False)
    draw_sep = attrs.get("draw_separate", False)
    draw_grid = attrs.get("draw_grid", False)
    title = attrs.get("title", None)
    sharex = attrs.get("sharex", False)
    sharey = attrs.get("sharey", False)

    # format the data into a 1D array
    _charts = charts if isinstance(charts, list) else [charts]
    _charts = np.array(_charts)

    # get the number of rows and columns of the chart
    subplot_config = get_subplot_config(draw_sep, n_charts=_charts.shape[0], max_cols=4)

    figure, axes = plt.subplots(
        **subplot_config,
        sharex=sharex,
        sharey=sharey,
        squeeze=False,
        constrained_layout=True,
    )

    # prepare the axes based on the draw type
    axes = (
        [axes[0, 0] for _ in range(_charts.shape[0])]
        if not draw_sep
        else axes.flatten()
    )

    # hide all axes
    for ax in axes:
        ax.axis("off")

    for chart, ax in zip(_charts, axes):
        # draws the line chart
        draw_line_chart(ax, chart, draw_ci=draw_ci, draw_grid=draw_grid)

        # graph configuration using actions
        configuration_actions = [
            ("subtitle", ax.set_title),
            ("xlabel", ax.set_xlabel),
            ("ylabel", ax.set_ylabel),
        ]

        for attr, action in configuration_actions:
            if attr in chart:
                action(chart[attr], **get_text_config(config, attr))

        # configure the axes and their ticks
        configure_axes_spines(ax, config)
        configure_axis_ticks(ax, config, "xaxis")
        configure_axis_ticks(ax, config, "yaxis")

    # add the title of the figure
    figure.suptitle(title, **get_text_config(config, "title"))

    # plot the figure
    plt.show()
