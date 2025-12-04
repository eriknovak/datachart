from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import chart_plot_wrapper, plot_histogram
from ..utils._internal.chart_builder import build_charts_structure, build_attrs_dict
from ..typings import (
    HistDataPointAttrs,
    HistStyleAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
)
from ..constants import FIG_SIZE, SHOW_GRID, ORIENTATION, SCALE

# ================================================
# Main Chart Definition
# ================================================


def Histogram(
    data: Union[List[HistDataPointAttrs], List[List[HistDataPointAttrs]]],
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
    show_density: Optional[bool] = None,
    show_cumulative: Optional[bool] = None,
    aspect_ratio: Optional[str] = None,
    orientation: Optional[Union[ORIENTATION, str]] = ORIENTATION.VERTICAL,
    num_bins: Optional[int] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[HistStyleAttrs, List[Optional[HistStyleAttrs]]]] = None,
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
) -> plt.Figure:
    """Creates the histogram.

    Examples:
        >>> from datachart.charts import Histogram
        >>> figure = Histogram(
        ...     data=[
        ...         {"x": 1},
        ...         {"x": 2},
        ...         {"x": 3},
        ...         {"x": 4},
        ...         {"x": 5}
        ...     ],
        ...     title="Basic Histogram",
        ...     xlabel="X",
        ...     ylabel="Y"
        ... )

    Args:
        data: The data points for the histogram(s). Can be a single list of data points
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
        show_density: Whether to plot the density histogram.
        show_cumulative: Whether to plot the cumulative histogram.
        aspect_ratio: The aspect ratio of the chart.
        orientation: The orientation of the histogram (vertical or horizontal).
        num_bins: The number of bins to split the data into.
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the histogram(s).
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        x: The key name in data for x-axis values (default: "x").

    Returns:
        The figure containing the histogram.

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
    )

    # Build the attrs dict using shared utility
    attrs = build_attrs_dict(
        "histogram",
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
        show_density=show_density,
        show_cumulative=show_cumulative,
        orientation=orientation,
        num_bins=num_bins,
        scaley=scaley,
    )

    return chart_plot_wrapper(plot_histogram)(attrs)
