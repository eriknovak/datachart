from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import chart_plot_wrapper, plot_box_plot
from ..utils._internal.chart_builder import build_charts_structure, build_attrs_dict
from ..typings import (
    BoxDataPointAttrs,
    BoxStyleAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
)
from ..constants import FIG_SIZE, SHOW_GRID, ORIENTATION

# ================================================
# Main Chart Definition
# ================================================


def BoxPlot(
    data: Union[List[BoxDataPointAttrs], List[List[BoxDataPointAttrs]]],
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
    show_outliers: Optional[bool] = None,
    show_notch: Optional[bool] = None,
    aspect_ratio: Optional[str] = None,
    orientation: Optional[Union[ORIENTATION, str]] = ORIENTATION.VERTICAL,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[BoxStyleAttrs, List[Optional[BoxStyleAttrs]]]] = None,
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
    value: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates the box plot.

    Examples:
        >>> from datachart.charts import BoxPlot
        >>> figure = BoxPlot(
        ...     data=[
        ...         {"label": "Group A", "value": 10},
        ...         {"label": "Group A", "value": 15},
        ...         {"label": "Group A", "value": 12},
        ...         {"label": "Group B", "value": 20},
        ...         {"label": "Group B", "value": 25},
        ...         {"label": "Group B", "value": 22},
        ...     ],
        ...     title="Basic Box Plot",
        ...     xlabel="Group",
        ...     ylabel="Value"
        ... )

    Args:
        data: The data points for the box plot(s). Can be a single list of data points
            for one chart, or a list of lists for multiple charts/subplots.
            Each data point should have a `label` (category) and `value` (numeric).
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
        show_outliers: Whether to show outliers. Defaults to True.
        show_notch: Whether to show notched boxes for median confidence interval.
        aspect_ratio: The aspect ratio of the chart.
        orientation: The orientation of the boxes (vertical or horizontal).
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the box(es).
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        label: The key name in data for label/category values (default: "label").
        value: The key name in data for numeric values (default: "value").

    Returns:
        The figure containing the box plot.

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
        value=value,
    )

    # Build the attrs dict using shared utility
    attrs = build_attrs_dict(
        "boxplot",
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
        show_outliers=show_outliers,
        show_notch=show_notch,
        orientation=orientation,
    )

    return chart_plot_wrapper(plot_box_plot)(attrs)
