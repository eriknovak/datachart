from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..typings import (
    LineDataPointAttrs,
    StackedAreaStyleAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
    TextAttrs,
)
from ..constants import (
    ASPECT_RATIO,
    BASELINE,
    EMPHASIS,
    FIG_SIZE,
    SHOW_GRID,
    SCALE,
)

# ================================================
# Main Chart Definition
# ================================================


def StackedAreaChart(
    data: Union[List[LineDataPointAttrs], List[List[LineDataPointAttrs]]],
    *,
    baseline: Optional[Union[BASELINE, str]] = None,
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
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[StackedAreaStyleAttrs, List[Optional[StackedAreaStyleAttrs]]]
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
    x: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates the stacked area chart.

    Stacked areas fill each series on top of the previous one along an ordered
    axis, so the top edge traces the total and the bands show how it splits into
    parts — class proportions over time, traffic by channel per year. Every
    series must share the same `x` values. Use it for composition that changes
    along an axis; for the trajectories themselves use
    [`LineChart`][datachart.charts.LineChart], and for composition at a few
    discrete categories use [`BarChart`][datachart.charts.BarChart] with
    `bar_mode="stack"`.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.charts import StackedAreaChart
        >>> figure = StackedAreaChart(
        ...     data=[
        ...         [{"x": 1, "y": 3}, {"x": 2, "y": 4}, {"x": 3, "y": 5}],
        ...         [{"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 3, "y": 1}],
        ...     ],
        ...     subtitle=["Mobile", "Desktop"],
        ...     title="Traffic by Device",
        ...     xlabel="Year",
        ...     ylabel="Visits",
        ... )

    Args:
        data: The data points for the stacked series. A single list of points
            draws one band; a list of lists draws one band per series, the
            first at the bottom. Every series must hold the same `x` values in
            the same order.
        baseline: Where the first series starts: "zero" (default), "percent"
            (each `x` normalised to 100), "sym" (centred on zero), "wiggle" or
            "weighted_wiggle" (streamgraph baselines). See `BASELINE`.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual series. Used as legend labels.
        emphasis: The emphasis role(s) for individual series, aligned like
            `style`: "background" mutes a band (theme muted color, lowered
            alpha, no legend entry), "highlight" brings it to the front, None
            leaves it unchanged.
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show (e.g., "both", "x", "y").
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            `ASPECT_RATIO`.
        scalex: The x-axis scale (e.g., "log", "linear").
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to draw each series unstacked in its own subplot.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the band(s).
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        texts: Text annotation(s) to draw.
        x: The key name in data for x-axis values (default: "x").
        y: The key name in data for y-axis values (default: "y").

    Returns:
        The figure containing the stacked area chart.

    Raises:
        ValueError: If the series do not share the same `x` values, or
            `baseline` is not a `BASELINE` value.

    """
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
        x=x,
        y=y,
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
        "aspect_ratio": aspect_ratio,
        "subplots": subplots,
        "max_cols": max_cols,
        "sharex": sharex,
        "sharey": sharey,
        "baseline": baseline,
        "scalex": scalex,
        "scaley": scaley,
    }

    return render_chart("stackedareachart", charts, settings)
