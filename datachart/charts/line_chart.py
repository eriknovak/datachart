from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import chart_plot_wrapper, plot_line_chart
from ..typings import (
    LineDataPointAttrs,
    LineSingleChartAttrs,
    LineStyleAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
)
from ..constants import FIG_SIZE, SHOW_GRID, SCALE

# ================================================
# Main Chart Definition
# ================================================


def LineChart(
    data: Union[List[LineDataPointAttrs], List[List[LineDataPointAttrs]]],
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
    show_area: Optional[bool] = None,
    aspect_ratio: Optional[str] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[LineStyleAttrs, List[Optional[LineStyleAttrs]]]] = None,
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
    yerr: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates the line chart.

    Examples:
        >>> from datachart.charts import LineChart
        >>> figure = LineChart(
        ...     data=[
        ...         {"x": 1, "y": 5},
        ...         {"x": 2, "y": 10},
        ...         {"x": 3, "y": 15},
        ...         {"x": 4, "y": 20},
        ...         {"x": 5, "y": 25}
        ...     ],
        ...     title="Basic Line Chart",
        ...     xlabel="X",
        ...     ylabel="Y"
        ... )

    Args:
        data: The data points for the line chart(s). Can be a single list of data points
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
        show_area: Whether to show the area under the line.
        aspect_ratio: The aspect ratio of the chart.
        scalex: The x-axis scale (e.g., "log", "linear").
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the line(s).
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
        yerr: The key name in data for y-axis error values (default: "yerr").

    Returns:
        The figure containing the line chart.

    """
    # Detect if data is for multiple charts
    is_multi_chart = (
        isinstance(data, list) and len(data) > 0 and isinstance(data[0], list)
    )

    # Build the charts structure
    if is_multi_chart:
        charts = []
        for i, chart_data in enumerate(data):
            chart_dict = {"data": chart_data}

            # Add per-chart attributes
            if subtitle is not None and isinstance(subtitle, list):
                chart_dict["subtitle"] = subtitle[i] if i < len(subtitle) else None
            elif subtitle is not None:
                chart_dict["subtitle"] = subtitle

            if style is not None and isinstance(style, list):
                style_val = style[i] if i < len(style) else None
                chart_dict["style"] = style_val if style_val is not None else {}
            elif style is not None:
                chart_dict["style"] = style

            if xticks is not None and isinstance(xticks[0] if xticks else None, list):
                chart_dict["xticks"] = xticks[i] if i < len(xticks) else None
            elif xticks is not None:
                chart_dict["xticks"] = xticks

            if xticklabels is not None and isinstance(
                xticklabels[0] if xticklabels else None, list
            ):
                chart_dict["xticklabels"] = (
                    xticklabels[i] if i < len(xticklabels) else None
                )
            elif xticklabels is not None:
                chart_dict["xticklabels"] = xticklabels

            if xtickrotate is not None and isinstance(xtickrotate, list):
                chart_dict["xtickrotate"] = (
                    xtickrotate[i] if i < len(xtickrotate) else None
                )
            elif xtickrotate is not None:
                chart_dict["xtickrotate"] = xtickrotate

            if yticks is not None and isinstance(yticks[0] if yticks else None, list):
                chart_dict["yticks"] = yticks[i] if i < len(yticks) else None
            elif yticks is not None:
                chart_dict["yticks"] = yticks

            if yticklabels is not None and isinstance(
                yticklabels[0] if yticklabels else None, list
            ):
                chart_dict["yticklabels"] = (
                    yticklabels[i] if i < len(yticklabels) else None
                )
            elif yticklabels is not None:
                chart_dict["yticklabels"] = yticklabels

            if ytickrotate is not None and isinstance(ytickrotate, list):
                chart_dict["ytickrotate"] = (
                    ytickrotate[i] if i < len(ytickrotate) else None
                )
            elif ytickrotate is not None:
                chart_dict["ytickrotate"] = ytickrotate

            if vlines is not None and isinstance(vlines, list) and i < len(vlines):
                chart_dict["vlines"] = vlines[i]
            elif vlines is not None and not isinstance(vlines, list):
                chart_dict["vlines"] = vlines

            if hlines is not None and isinstance(hlines, list) and i < len(hlines):
                chart_dict["hlines"] = hlines[i]
            elif hlines is not None and not isinstance(hlines, list):
                chart_dict["hlines"] = hlines

            if x is not None and isinstance(x, list):
                chart_dict["x"] = x[i] if i < len(x) else None
            elif x is not None:
                chart_dict["x"] = x

            if y is not None and isinstance(y, list):
                chart_dict["y"] = y[i] if i < len(y) else None
            elif y is not None:
                chart_dict["y"] = y

            if yerr is not None and isinstance(yerr, list):
                chart_dict["yerr"] = yerr[i] if i < len(yerr) else None
            elif yerr is not None:
                chart_dict["yerr"] = yerr

            charts.append(chart_dict)
    else:
        # Single chart
        chart_dict = {"data": data}
        if subtitle is not None:
            chart_dict["subtitle"] = (
                subtitle
                if isinstance(subtitle, str)
                else (subtitle[0] if subtitle else None)
            )
        if style is not None:
            chart_dict["style"] = (
                style if isinstance(style, dict) else (style[0] if style else None)
            )
        if xticks is not None:
            chart_dict["xticks"] = xticks
        if xticklabels is not None:
            chart_dict["xticklabels"] = xticklabels
        if xtickrotate is not None:
            chart_dict["xtickrotate"] = (
                xtickrotate
                if isinstance(xtickrotate, int)
                else (xtickrotate[0] if xtickrotate else None)
            )
        if yticks is not None:
            chart_dict["yticks"] = yticks
        if yticklabels is not None:
            chart_dict["yticklabels"] = yticklabels
        if ytickrotate is not None:
            chart_dict["ytickrotate"] = (
                ytickrotate
                if isinstance(ytickrotate, int)
                else (ytickrotate[0] if ytickrotate else None)
            )
        if vlines is not None:
            chart_dict["vlines"] = vlines
        if hlines is not None:
            chart_dict["hlines"] = hlines
        if x is not None:
            chart_dict["x"] = x if isinstance(x, str) else (x[0] if x else None)
        if y is not None:
            chart_dict["y"] = y if isinstance(y, str) else (y[0] if y else None)
        if yerr is not None:
            chart_dict["yerr"] = (
                yerr if isinstance(yerr, str) else (yerr[0] if yerr else None)
            )

        charts = chart_dict

    # Build the attrs dict for the internal API
    attrs = {
        "type": "linechart",
        "charts": charts,
    }

    # Add global attributes
    if title is not None:
        attrs["title"] = title
    if xlabel is not None:
        attrs["xlabel"] = xlabel
    if ylabel is not None:
        attrs["ylabel"] = ylabel
    if figsize is not None:
        attrs["figsize"] = figsize
    if xmin is not None:
        attrs["xmin"] = xmin
    if xmax is not None:
        attrs["xmax"] = xmax
    if ymin is not None:
        attrs["ymin"] = ymin
    if ymax is not None:
        attrs["ymax"] = ymax
    if show_legend is not None:
        attrs["show_legend"] = show_legend
    if show_grid is not None:
        attrs["show_grid"] = show_grid
    if show_yerr is not None:
        attrs["show_yerr"] = show_yerr
    if show_area is not None:
        attrs["show_area"] = show_area
    if aspect_ratio is not None:
        attrs["aspect_ratio"] = aspect_ratio
    if scalex is not None:
        attrs["scalex"] = scalex
    if scaley is not None:
        attrs["scaley"] = scaley
    if subplots is not None:
        attrs["subplots"] = subplots
    if max_cols is not None:
        attrs["max_cols"] = max_cols
    if sharex is not None:
        attrs["sharex"] = sharex
    if sharey is not None:
        attrs["sharey"] = sharey

    return chart_plot_wrapper(plot_line_chart)(attrs)
