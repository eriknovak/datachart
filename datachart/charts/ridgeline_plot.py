from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import validate_bandwidth
from ..typings import (
    EmphasisRuleAttrs,
    LegendSettingAttrs,
    RidgelineDataPointAttrs,
    RidgelineStyleAttrs,
    VLineSettingAttrs,
    HLineSettingAttrs,
    VSpanSettingAttrs,
    HSpanSettingAttrs,
    TextSettingAttrs,
)
from ..constants import (
    DATE_FORMAT,
    VALUE_FORMAT,
    ASPECT_RATIO,
    EMPHASIS,
    FIG_SIZE,
    SHOW_GRID,
    ORIENTATION,
    SCALE,
    SORT,
    VIOLIN_INNER,
    BANDWIDTH,
    RIDGELINE_SCALE,
)

# ================================================
# Main Chart Definition
# ================================================


def RidgelinePlot(
    data: Union[List[RidgelineDataPointAttrs], List[List[RidgelineDataPointAttrs]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: Optional[Union[EMPHASIS, str, List[Optional[str]]]] = None,
    emphasis_rule: Optional[EmphasisRuleAttrs] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    orientation: Optional[Union[ORIENTATION, str]] = ORIENTATION.HORIZONTAL,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[RidgelineStyleAttrs, List[Optional[RidgelineStyleAttrs]]]
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
    xticks_format: Optional[Union[VALUE_FORMAT, DATE_FORMAT, str]] = None,
    yticks_format: Optional[Union[VALUE_FORMAT, DATE_FORMAT, str]] = None,
    vlines: Optional[
        Union[
            VLineSettingAttrs,
            List[VLineSettingAttrs],
            List[Union[VLineSettingAttrs, List[VLineSettingAttrs], None]],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLineSettingAttrs,
            List[HLineSettingAttrs],
            List[Union[HLineSettingAttrs, List[HLineSettingAttrs], None]],
        ]
    ] = None,
    vspans: Optional[
        Union[
            VSpanSettingAttrs,
            List[VSpanSettingAttrs],
            List[Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]],
        ]
    ] = None,
    hspans: Optional[
        Union[
            HSpanSettingAttrs,
            List[HSpanSettingAttrs],
            List[Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextSettingAttrs,
            List[TextSettingAttrs],
            List[Union[TextSettingAttrs, List[TextSettingAttrs], None]],
        ]
    ] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    value: Optional[Union[str, List[Optional[str]]]] = None,
    bandwidth: Optional[Union[BANDWIDTH, str, float]] = None,
    overlap: Optional[float] = None,
    normalize: Optional[Union[RIDGELINE_SCALE, str]] = RIDGELINE_SCALE.PER_ROW,
    inner: Optional[Union[VIOLIN_INNER, str]] = None,
    fill: bool = True,
    show_outline: bool = True,
    sort: Optional[Union[SORT, str]] = SORT.NONE,
) -> plt.Figure:
    """Creates the ridgeline plot.

    A ridgeline plot (joy plot) draws the kernel density estimate of each
    group's numeric distribution as a ridge on its own row, the rows stacked
    and partly overlapping, first row at the top. Use it to show how one
    distribution shifts across many groups in the space a grid of histograms
    would spend on a few.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.charts import RidgelinePlot
        >>> figure = RidgelinePlot(
        ...     data=[
        ...         {"label": "Group A", "value": 10},
        ...         {"label": "Group A", "value": 15},
        ...         {"label": "Group A", "value": 12},
        ...         {"label": "Group B", "value": 20},
        ...         {"label": "Group B", "value": 25},
        ...         {"label": "Group B", "value": 22},
        ...     ],
        ...     title="Basic Ridgeline Plot",
        ...     xlabel="Value",
        ...     ylabel="Group"
        ... )

    Args:
        data: The data points for the ridgeline plot(s). Can be a single list of data points
            for one chart, or a list of lists for multiple charts/subplots.
            Each data point should have a `label` (category) and `value` (numeric).
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts (subplots).
        emphasis: The emphasis role(s), aligned with the ridge labels of one
            call in input order (a single value applies to every ridge):
            "background" mutes a ridge and its inner marks, "highlight" bolds
            its outline, None leaves it unchanged.
        emphasis_rule: A rule that highlights the groups matching it and mutes the rest:
            `{"above": v}` or `{"below": v}` (strict), `{"between": (lo, hi)}`
            (inclusive), `{"top": n}` or `{"bottom": n}`, read against a summary of each
            group's values, chosen by `by`: `"median"` (default), `"mean"`, `"min"`,
            `"max"`, or `"sum"`. An explicit `emphasis` role wins, and a count ranks
            across every group of every chart. See
            [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        figsize: The size of the figure.
        xmin: The minimum x-axis value; on the value axis it also bounds the
            density grid.
        xmax: The maximum x-axis value; on the value axis it also bounds the
            density grid.
        ymin: The minimum y-axis value; bounds the grid when vertical.
        ymax: The maximum y-axis value; bounds the grid when vertical.
        show_legend: Whether to show the legend; the ridges add no entries,
            their labels sit on the category axis.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        show_grid: Which grid lines to show (e.g., "both", "x", "y");
            `False` draws none.
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            [`ASPECT_RATIO`][datachart.constants.ASPECT_RATIO].
        orientation: "horizontal" (default) runs the value axis along x and
            stacks the rows along y, first row at the top; "vertical" runs
            the rows along x, first row at the left, each ridge rising
            rightward from its tick.
            See [`ORIENTATION`][datachart.constants.ORIENTATION].
        scaley: The value-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the ridges.
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        xticks_format: The x-axis tick label format: a
            [`DATE_FORMAT`][datachart.constants.DATE_FORMAT] member or `strftime`
            pattern on a datetime axis, else a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] member or `"{x:.1f}"`
            style string.
        yticks_format: The y-axis tick label format, as `xticks_format`.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        vspans: Vertical reference band(s) to shade, between two x positions.
        hspans: Horizontal reference band(s) to shade, between two y positions.
        texts: Text annotation(s) to draw.
        label: The key name in data for label/category values (default: "label").
        value: The key name in data for numeric values (default: "value").
        bandwidth: The KDE bandwidth: None or "scott" (Scott's rule), "silverman", or a
            scalar factor. See [`BANDWIDTH`][datachart.constants.BANDWIDTH].
        overlap: How far a ridge's peak rises into the row above, in `[0, 1]`:
            a ridge rises from its tick and its peak stands `1 + overlap`
            rows above it, so 0 makes rows touch. None takes the theme's `plot_ridgeline_overlap`.
        normalize: "per_row" scales every ridge to the same peak so shapes
            compare; "common" keeps one density scale so heights compare. See
            [`RIDGELINE_SCALE`][datachart.constants.RIDGELINE_SCALE].
        inner: The marks drawn inside each ridge, up to its height: "median" (one line),
            "quartiles" (dashed median, dotted Q1/Q3), or None. See
            [`VIOLIN_INNER`][datachart.constants.VIOLIN_INNER]; "box" is not supported.
        fill: Whether to fill each ridge.
        show_outline: Whether to stroke each ridge's density curve.
        sort: The row order: None keeps input order, "ascending" or
            "descending" orders the rows by their median; ties keep input
            order. See [`SORT`][datachart.constants.SORT].

    Returns:
        The figure containing the ridgeline plot.

    Raises:
        ValueError: If `overlap` is outside `[0, 1]`, `inner` is "box", or
            both `fill` and `show_outline` are False.

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
        vspans=vspans,
        hspans=hspans,
        texts=texts,
        label=label,
        value=value,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "emphasis_rule": emphasis_rule,
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "figsize": figsize,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "show_legend": show_legend,
        "legend": legend,
        "show_grid": show_grid,
        "aspect_ratio": aspect_ratio,
        "subplots": subplots,
        "max_cols": max_cols,
        "sharex": sharex,
        "sharey": sharey,
        "bandwidth": bandwidth,
        "overlap": overlap,
        "normalize": normalize,
        "inner": inner,
        "fill": fill,
        "show_outline": show_outline,
        "sort": sort,
        "orientation": orientation,
        "scaley": scaley,
        "xticks_format": xticks_format,
        "yticks_format": yticks_format,
    }

    return render_chart("ridgelineplot", charts, settings)
