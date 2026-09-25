import warnings
from datetime import datetime
from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render
from ..typings import (
    EmphasisRuleAttrs,
    LegendSettingAttrs,
    LineRecordAttrs,
    LineStyleAttrs,
    VLineSettingAttrs,
    HLineSettingAttrs,
    DLineSettingAttrs,
    BracketSettingAttrs,
    VSpanSettingAttrs,
    HSpanSettingAttrs,
    TextSettingAttrs,
)
from ..constants import (
    ASPECT_RATIO,
    EMPHASIS,
    FIG_SIZE,
    SHOW_GRID,
    AXIS_SCALE,
    VALUE_FORMAT,
    DATE_FORMAT,
    LINE_LABEL_POSITION,
)

# ================================================
# Main Chart Definition
# ================================================


def LineChart(
    data: Union[List[LineRecordAttrs], List[List[LineRecordAttrs]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: Optional[Union[EMPHASIS, str, List[Optional[str]]]] = None,
    emphasis_rule: Optional[EmphasisRuleAttrs] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float, datetime]] = None,
    xmax: Optional[Union[int, float, datetime]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    show_yerr: Optional[bool] = None,
    show_area: Optional[bool] = None,
    show_labels: Optional[bool] = None,
    label_position: Optional[Union[LINE_LABEL_POSITION, str]] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    value_step: Optional[int] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[AXIS_SCALE, str]] = None,
    scaley: Optional[Union[AXIS_SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[LineStyleAttrs, List[Optional[LineStyleAttrs]]]] = None,
    xticks: Optional[
        Union[
            List[Union[int, float, datetime]],
            List[List[Union[int, float, datetime]]],
        ]
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
    dlines: Optional[
        Union[
            DLineSettingAttrs,
            List[DLineSettingAttrs],
            List[Union[DLineSettingAttrs, List[DLineSettingAttrs], None]],
        ]
    ] = None,
    brackets: Optional[
        Union[
            BracketSettingAttrs,
            List[BracketSettingAttrs],
            List[Union[BracketSettingAttrs, List[BracketSettingAttrs], None]],
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
    x: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    yerr: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates the line chart.

    Lines connect ordered (x, y) points to show how a value changes along a continuous
    axis, typically time. Use it for trends, growth, and comparing the trajectories of
    several series on the same scale. For unordered categories use
    [`BarChart`][datachart.charts.BarChart]; for unconnected samples use
    [`ScatterChart`][datachart.charts.ScatterChart].

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
        emphasis: The emphasis role(s) for individual charts, aligned like
            `style`: "background" mutes a chart (theme muted color, lowered
            alpha, thinner line, behind the others, no legend entry),
            "highlight" bolds it and brings it to the front, None leaves it
            unchanged.
        emphasis_rule: A rule that highlights the lines matching it and mutes the rest:
            `{"above": v}` or `{"below": v}` (strict), `{"between": (lo, hi)}`
            (inclusive), `{"top": n}` or `{"bottom": n}`, read against a summary of each
            line's own `y` values, chosen by `by`: `"mean"` (default), `"median"`,
            `"min"`, `"max"`, or `"sum"`. An explicit `emphasis` role wins, and a count
            ranks across every line. See
            [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        show_grid: Which grid lines to show (e.g., "both", "x", "y");
            `False` draws none.
        show_yerr: Whether to show y-axis error bars.
        show_area: Whether to show the area under the line.
        show_labels: Whether to print each series' subtitle beside its line
            end, in the text color. Labels that would overlap spread apart
            along the value axis. Defaults to False.
        label_position: Which line end carries the label, a
            [`LINE_LABEL_POSITION`][datachart.constants.LINE_LABEL_POSITION]
            member: `START`, `END` (default), or `BOTH`.
        show_values: Whether to print each point's value above or below it.
        value_format: Format string for the value labels: a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] constant or any
            `"{x:.1f}"`, `"{:.1f}%"`, or `"%g"` style string.
        value_step: Label every Nth point (`1` labels all of them). Defaults
            to the smallest step that keeps neighbouring labels apart.
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            [`ASPECT_RATIO`][datachart.constants.ASPECT_RATIO].
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
        xticks_format: The x-axis tick label format: a
            [`DATE_FORMAT`][datachart.constants.DATE_FORMAT] member or `strftime`
            pattern on a datetime axis, else a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] member or `"{x:.1f}"`
            style string.
        yticks_format: The y-axis tick label format, as `xticks_format`.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        dlines: Diagonal line(s) to plot, by slope and intercept.
        brackets: Pairwise comparison bracket(s) to draw between two
            categories, with an optional text such as a p-value.
        vspans: Vertical reference band(s) to shade, between two x positions.
        hspans: Horizontal reference band(s) to shade, between two y positions.
        texts: Text annotation(s) to draw.
        x: The key name in data for x-axis values (default: "x").
        y: The key name in data for y-axis values (default: "y").
        yerr: The key name in data for y-axis error values (default: "yerr").

    Returns:
        The figure containing the line chart.

    """
    params = dict(locals())

    if show_yerr and show_area:
        warnings.warn(
            "Both the `show_yerr` and `show_area` will be used. "
            + "Only one of them should be True."
        )
    return render("linechart", params)
