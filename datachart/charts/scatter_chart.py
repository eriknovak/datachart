from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import chart_plot_wrapper, plot_scatter_chart
from ..utils._internal.chart_builder import build_charts_structure, build_attrs_dict
from ..typings import (
    ScatterDataPointAttrs,
    ScatterStyleAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
)
from ..constants import FIG_SIZE, SHOW_GRID, SCALE

# ================================================
# Main Chart Definition
# ================================================


def ScatterChart(
    data: Union[List[ScatterDataPointAttrs], List[List[ScatterDataPointAttrs]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_regression: Optional[bool] = None,
    show_ci: Optional[bool] = None,
    ci_level: Optional[float] = None,
    show_correlation: Optional[bool] = None,
    aspect_ratio: Optional[str] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[ScatterStyleAttrs, List[Optional[ScatterStyleAttrs]]]] = None,
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
    x: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    size: Optional[Union[str, List[Optional[str]]]] = None,
    hue: Optional[Union[str, List[Optional[str]]]] = None,
    size_range: Optional[Tuple[float, float]] = None,
) -> plt.Figure:
    """Creates a scatter chart.

    Examples:
        >>> from datachart.charts import ScatterChart
        >>> # Basic scatter plot
        >>> figure = ScatterChart(
        ...     data=[
        ...         {"x": 1, "y": 5},
        ...         {"x": 2, "y": 10},
        ...         {"x": 3, "y": 15},
        ...         {"x": 4, "y": 20},
        ...         {"x": 5, "y": 25}
        ...     ],
        ...     title="Basic Scatter Chart",
        ...     xlabel="X",
        ...     ylabel="Y"
        ... )
        >>>
        >>> # Scatter with hue grouping
        >>> figure = ScatterChart(
        ...     data=[
        ...         {"x": 1, "y": 5, "category": "A"},
        ...         {"x": 2, "y": 10, "category": "B"},
        ...     ],
        ...     hue="category",
        ...     show_legend=True
        ... )
        >>>
        >>> # Bubble chart with size variable
        >>> figure = ScatterChart(
        ...     data=[
        ...         {"x": 1, "y": 5, "pop": 100},
        ...         {"x": 2, "y": 10, "pop": 200}
        ...     ],
        ...     size="pop",
        ...     size_range=(20, 200)
        ... )
        >>>
        >>> # Scatter with regression line
        >>> figure = ScatterChart(
        ...     data=[...],
        ...     show_regression=True,
        ...     show_ci=True,
        ...     ci_level=0.95
        ... )
        >>>
        >>> # Scatter with correlation annotation
        >>> figure = ScatterChart(
        ...     data=[...],
        ...     show_correlation=True
        ... )

    Args:
        data: The data points for the scatter chart(s). Can be a single list of data points
            for one chart, or a list of lists for multiple charts/subplots.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts. Used as legend labels.
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show (e.g., "both", "x", "y").
        show_regression: Whether to show the regression line.
        show_ci: Whether to show the confidence interval around the regression line.
        ci_level: The confidence interval level (default 0.95).
        show_correlation: Whether to show the Pearson correlation coefficient (r-value) as an annotation.
        aspect_ratio: The aspect ratio of the chart.
        scalex: The x-axis scale (e.g., "log", "linear").
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the scatter markers.
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        x: The key name in data for x-axis values (default: "x").
        y: The key name in data for y-axis values (default: "y").
        size: The key name in data for marker size values (for bubble charts).
        hue: The key name in data for color grouping (categorical variable).
        size_range: Tuple of (min_size, max_size) for bubble charts (default: (20, 200)).

    Returns:
        The figure containing the scatter chart.

    """
    # Build the charts structure using shared utility
    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        style=style,
        xticks=xticks,
        xticklabels=xticklabels,
        xtickrotate=xtickrotate,
        yticks=yticks,
        yticklabels=yticklabels,
        ytickrotate=ytickrotate,
        vlines=vlines,
        hlines=hlines,
        x=x,
        y=y,
        size=size,
        hue=hue,
    )

    # Build the attrs dict using shared utility
    attrs = build_attrs_dict(
        "scatterchart",
        charts,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=figsize,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        show_legend=show_legend,
        show_grid=show_grid,
        aspect_ratio=aspect_ratio,
        subplots=subplots,
        max_cols=max_cols,
        sharex=sharex,
        sharey=sharey,
        show_regression=show_regression,
        show_ci=show_ci,
        ci_level=ci_level,
        show_correlation=show_correlation,
        scalex=scalex,
        scaley=scaley,
        size_range=size_range,
    )

    return chart_plot_wrapper(plot_scatter_chart)(attrs)
