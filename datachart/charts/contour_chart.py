from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..typings import (
    ContourDataAttrs,
    ContourStyleAttrs,
    HeatmapColorbarAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
    TextAttrs,
)
from ..constants import (
    ASPECT_RATIO,
    CONTOUR_LEVELS,
    EMPHASIS,
    FIG_SIZE,
    SHOW_GRID,
    SCALE,
    VALUE_FORMAT,
)

# ================================================
# Main Chart Definition
# ================================================


def ContourChart(
    data: Union[ContourDataAttrs, List[ContourDataAttrs]],
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
    filled: Optional[bool] = None,
    levels: Optional[Union[CONTOUR_LEVELS, str, int, List[float]]] = None,
    show_labels: Optional[bool] = None,
    show_colorbars: Optional[bool] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[ContourStyleAttrs, List[Optional[ContourStyleAttrs]]]] = None,
    norm: Optional[Union[str, List[Optional[str]]]] = None,
    vmin: Optional[Union[float, List[Optional[float]]]] = None,
    vmax: Optional[Union[float, List[Optional[float]]]] = None,
    valfmt: Optional[Union[VALUE_FORMAT, str, List[Optional[str]]]] = None,
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
    colorbar: Optional[
        Union[HeatmapColorbarAttrs, List[Optional[HeatmapColorbarAttrs]]]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
) -> plt.Figure:
    """Creates the contour chart.

    A contour chart draws a surface sampled on a grid — a loss landscape, a
    2-D density, a terrain — as iso-lines of equal value, or as filled bands
    between them. Use it to read the shape of a function of two variables:
    where its minima and ridges sit and how steeply it changes. Lines overlay
    on other charts and on each other; fills stand alone, with an optional
    colorbar. For a per-cell view of a matrix use
    [`Heatmap`][datachart.charts.Heatmap]; for the raw points behind a density
    use [`ScatterChart`][datachart.charts.ScatterChart].

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.charts import ContourChart
        >>> figure = ContourChart(
        ...     data={
        ...         "x": [0, 1, 2],
        ...         "y": [0, 1, 2],
        ...         "z": [
        ...             [0, 1, 4],
        ...             [1, 2, 5],
        ...             [4, 5, 8],
        ...         ],
        ...     },
        ...     title="Basic Contour Chart",
        ...     xlabel="X",
        ...     ylabel="Y"
        ... )

    Args:
        data: The gridded surface(s): a dictionary with the 2-D `z` grid and
            the optional `x` and `y` axis values (one per column and per row
            of `z`, the indices by default), or a list of them for multiple
            charts/subplots.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts. Used as legend labels.
        emphasis: The emphasis role(s) for individual line contours, aligned
            like `style`: "background" mutes a chart (theme muted color,
            lowered alpha, behind the others, no legend entry), "highlight"
            bolds it and brings it to the front, None leaves it unchanged.
            Not supported for filled contours: passing a value with
            `filled=True` raises `ValueError`.
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show (e.g., "both", "x", "y"). Off by
            default for filled contours.
        filled: Whether to fill the bands between the levels (colored by the
            colormap) instead of drawing iso-lines (in the chart's color).
        levels: Which levels cut the surface: a rule of `CONTOUR_LEVELS`
            (`"auto"`, the default, leaves the choice to matplotlib), a target
            level count, or an explicit list of level values.
        show_labels: Whether to write the level values along the iso-lines.
        show_colorbars: Whether to show the colorbar(s) of filled contours.
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            `ASPECT_RATIO`.
        scalex: The x-axis scale (e.g., "log", "linear").
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the contour chart(s).
        norm: Value normalization method(s) of the colormap.
        vmin: Minimum value(s) for normalization.
        vmax: Maximum value(s) for normalization.
        valfmt: Format string(s) for the inline level labels, with the value
            named `x` (e.g., `"{x:.1f}"`). See `VALUE_FORMAT`.
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        colorbar: Colorbar configuration(s).
        texts: Text annotation(s) to draw.

    Returns:
        The figure containing the contour chart.

    """
    if filled and emphasis is not None:
        raise ValueError(
            "ContourChart does not support `emphasis` when `filled=True`: "
            "filled bands take the colormap, not a series color to mute or "
            "highlight. Use line contours instead."
        )

    # Build the charts structure using shared utility
    # Note: a contour chart's data is one grid dict, so we use is_2d_data=True
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
        is_2d_data=True,
        norm=norm,
        vmin=vmin,
        vmax=vmax,
        valfmt=valfmt,
        colorbar=colorbar,
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
        "filled": filled,
        "levels": levels,
        "show_labels": show_labels,
        "show_colorbars": show_colorbars,
        "scalex": scalex,
        "scaley": scaley,
    }

    return render_chart("contourchart", charts, settings)
