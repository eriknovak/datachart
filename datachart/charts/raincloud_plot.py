from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import validate_bandwidth
from ..typings import (
    RaincloudDataPointAttrs,
    RaincloudStyleAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
    TextAttrs,
)
from ..constants import (
    ASPECT_RATIO,
    BANDWIDTH,
    EMPHASIS,
    FIG_SIZE,
    SHOW_GRID,
    ORIENTATION,
    SCALE,
    SWARM_MODE,
)

# ================================================
# Main Chart Definition
# ================================================


def RaincloudPlot(
    data: Union[List[RaincloudDataPointAttrs], List[List[RaincloudDataPointAttrs]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: Optional[Union[EMPHASIS, str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_outliers: Optional[bool] = True,
    mode: Union[SWARM_MODE, str] = SWARM_MODE.SWARM,
    jitter: float = 0.4,
    bandwidth: Optional[Union[BANDWIDTH, str, float]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    orientation: Optional[Union[ORIENTATION, str]] = ORIENTATION.VERTICAL,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[RaincloudStyleAttrs, List[Optional[RaincloudStyleAttrs]]]
    ] = None,
    xticks: Optional[
        Union[List[Union[int, float]], List[List[Union[int, float]]]]
    ] = None,
    xticklabels: Optional[Union[List[str], List[List[str]]]] = None,
    xtickrotate: Optional[Union[int, List[Optional[int]]]] = None,
    yticks: Optional[
        Union[List[Union[int, float]], List[List[Union[int, float]]]]
    ] = None,
    yticklabels: Optional[Union[List[str], List[List[str]]]] = None,
    ytickrotate: Optional[Union[int, List[Optional[int]]]] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    value: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates the raincloud plot.

    A raincloud plot draws each group as a cloud (a half violin of its
    density), its rain (the raw observations), and a box (the quartile
    summary) side by side at one category position, all in the group's palette
    color. Use it when you want the shape, the summary statistics, and the
    individual observations in a single view, for example when reporting
    experimental results per condition. Vertical rainclouds keep the cloud on
    the left; horizontal ones keep it above.

    !!! info "Added in 0.9.0"

    Examples:
        >>> from datachart.charts import RaincloudPlot
        >>> figure = RaincloudPlot(
        ...     data=[
        ...         {"label": "Group A", "value": 10},
        ...         {"label": "Group A", "value": 15},
        ...         {"label": "Group A", "value": 12},
        ...         {"label": "Group B", "value": 20},
        ...         {"label": "Group B", "value": 25},
        ...         {"label": "Group B", "value": 22},
        ...     ],
        ...     title="Basic Raincloud Plot",
        ...     xlabel="Group",
        ...     ylabel="Value"
        ... )

    Args:
        data: The data points for the raincloud plot(s). Can be a single list of
            data points for one chart, or a list of lists for multiple charts
            (drawn as subplots). Each data point should have a `label`
            (category) and `value` (numeric).
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts.
        emphasis: The emphasis role(s), aligned with the group labels of one
            call (a single value applies to every group): "background" mutes
            a group's cloud, rain, and box, "highlight" bolds their edges,
            None leaves them unchanged.
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend; one entry per group.
        show_grid: Which grid lines to show (e.g., "both", "x", "y").
        show_outliers: Whether the box shows outliers.
        mode: How the rain spreads across its width. See `SWARM_MODE`:
            "swarm" packs the points so none overlap; "strip" jitters them
            uniformly.
        jitter: The strip jitter width, as a fraction of the category width
            like `SwarmPlot`, scaled down to the rain's narrower cell. Only
            used with `mode="strip"`.
        bandwidth: The cloud's KDE bandwidth: None or "scott" (Scott's rule),
            "silverman" (Silverman's rule), or a scalar factor. See `BANDWIDTH`.
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            `ASPECT_RATIO`.
        orientation: The orientation of the rainclouds (vertical or horizontal).
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s); the violin keys style the cloud, the
            swarm keys the rain, and the box keys the box.
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        texts: Text annotation(s) to draw.
        label: The key name in data for label/category values (default: "label").
        value: The key name in data for numeric values (default: "value").

    Returns:
        The figure containing the raincloud plot.

    """
    validate_bandwidth(bandwidth)

    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        emphasis=emphasis,
        style=style,
        xticks=xticks,
        xticklabels=xticklabels,
        xtickrotate=xtickrotate,
        yticks=yticks,
        yticklabels=yticklabels,
        ytickrotate=ytickrotate,
        vlines=vlines,
        hlines=hlines,
        texts=texts,
        label=label,
        value=value,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "figsize": figsize,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "show_legend": show_legend,
        "show_grid": show_grid,
        "show_outliers": show_outliers,
        "aspect_ratio": aspect_ratio,
        "subplots": subplots,
        "max_cols": max_cols,
        "sharex": sharex,
        "sharey": sharey,
        "mode": mode,
        "jitter": jitter,
        "bandwidth": bandwidth,
        "orientation": orientation,
        "scaley": scaley,
    }

    return render_chart("raincloudplot", charts, settings)
