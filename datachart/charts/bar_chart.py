from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import chart_plot_wrapper, plot_bar_chart
from ..utils._internal.chart_builder import build_charts_structure, build_attrs_dict
from ..typings import (
    BarDataPointAttrs,
    BarStyleAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
)
from ..constants import FIG_SIZE, SHOW_GRID, ORIENTATION, SCALE

# ================================================
# Main Chart Definition
# ================================================


def BarChart(
    data: Union[List[BarDataPointAttrs], List[List[BarDataPointAttrs]]],
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
    show_yerr: Optional[bool] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[str] = None,
    aspect_ratio: Optional[str] = None,
    orientation: Optional[Union[ORIENTATION, str]] = ORIENTATION.VERTICAL,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[BarStyleAttrs, List[Optional[BarStyleAttrs]]]] = None,
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
    label: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    yerr: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates the bar chart.

    Examples:
        >>> from datachart.charts import BarChart
        >>> figure = BarChart(
        ...     data=[
        ...         {"label": "cat1", "y": 5},
        ...         {"label": "cat2", "y": 10},
        ...         {"label": "cat3", "y": 15},
        ...         {"label": "cat4", "y": 20},
        ...         {"label": "cat5", "y": 25}
        ...     ],
        ...     title="Basic Bar Chart",
        ...     xlabel="LABEL",
        ...     ylabel="Y"
        ... )

    Args:
        data: The data points for the bar chart(s). Can be a single list of data points
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
        show_yerr: Whether to show y-axis error bars.
        show_values: Whether to show bar value labels at the edge of each bar.
        value_format: Format string for bar value labels (e.g., "{:.1f}%").
        aspect_ratio: The aspect ratio of the chart.
        orientation: The orientation of the bars (vertical or horizontal).
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the bar(s).
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        label: The key name in data for label values (default: "label").
        y: The key name in data for y-axis values (default: "y").
        yerr: The key name in data for y-axis error values (default: "yerr").

    Returns:
        The figure containing the bar chart.

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
        label=label,
        y=y,
        yerr=yerr,
    )

    # Build the attrs dict using shared utility
    attrs = build_attrs_dict(
        "barchart",
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
        show_yerr=show_yerr,
        show_values=show_values,
        value_format=value_format,
        orientation=orientation,
        scaley=scaley,
    )

    return chart_plot_wrapper(plot_bar_chart)(attrs)
