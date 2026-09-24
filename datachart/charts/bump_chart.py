from datetime import datetime
from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render
from ..typings import (
    BumpStyleAttrs,
    EmphasisRuleAttrs,
    LegendSettingAttrs,
    LineDataPointAttrs,
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
    BUMP_LABEL_POSITION,
    BUMP_RANK,
    DATE_FORMAT,
    EMPHASIS,
    FIG_SIZE,
    AXIS_SCALE,
    SHOW_GRID,
    VALUE_FORMAT,
)

# ================================================
# Main Chart Definition
# ================================================


def BumpChart(
    data: Union[List[LineDataPointAttrs], List[List[LineDataPointAttrs]]],
    *,
    rank_by: Optional[Union[BUMP_RANK, str]] = None,
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
    show_labels: Optional[bool] = None,
    label_position: Optional[Union[BUMP_LABEL_POSITION, str]] = None,
    show_markers: Optional[bool] = None,
    line_curve: Optional[float] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    value_step: Optional[int] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[AXIS_SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[BumpStyleAttrs, List[Optional[BumpStyleAttrs]]]] = None,
    xticks: Optional[
        Union[
            List[Union[int, float, datetime]],
            List[List[Union[int, float, datetime]]],
        ]
    ] = None,
    xticklabels: Optional[Union[List[str], List[List[str]]]] = None,
    xtickrotate: Optional[Union[int, List[Optional[int]]]] = None,
    xticks_format: Optional[Union[VALUE_FORMAT, DATE_FORMAT, str]] = None,
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
) -> plt.Figure:
    """Creates the bump chart.

    A bump chart shows rank over time: one line per series, rank 1 at the top,
    a marker at every period, and the series named at the line's end in place
    of a y-axis. Use it for league tables, popularity, or market-share rankings,
    where the order matters more than the gaps between values. Periods may be
    numbers, dates, or strings; strings draw as categories in first-seen order.
    For the values themselves use [`LineChart`][datachart.charts.LineChart];
    for a single period's order use [`BarChart`][datachart.charts.BarChart]
    with `sort`.

    Examples:
        >>> from datachart.charts import BumpChart
        >>> figure = BumpChart(
        ...     data=[
        ...         [{"x": 2022, "y": 71}, {"x": 2023, "y": 64}, {"x": 2024, "y": 80}],
        ...         [{"x": 2022, "y": 68}, {"x": 2023, "y": 75}, {"x": 2024, "y": 77}],
        ...         [{"x": 2022, "y": 59}, {"x": 2023, "y": 70}, {"x": 2024, "y": 62}],
        ...     ],
        ...     subtitle=["Ljubljana", "Maribor", "Celje"],
        ...     title="League Table",
        ...     xlabel="Season",
        ...     ylabel="Rank",
        ... )

    Args:
        data: The data points of the series. Can be a single list of data
            points for one series, or a list of lists for several.
        rank_by: How `y` becomes a rank, a [`BUMP_RANK`][datachart.constants.BUMP_RANK]
            member: `VALUE_DESCENDING` (default) ranks the highest value first at each
            period, `VALUE_ASCENDING` the lowest, and `GIVEN` reads `y` as the rank (a
            positive integer). Ranking reads the series present at a period; a series
            without a point there leaves a gap. Ties keep input order.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) of the series. Used as end labels and
            legend labels.
        emphasis: The emphasis role(s) for individual series, aligned like
            `style`: "background" mutes a series, "highlight" bolds it and
            brings it to the front, None leaves it unchanged.
        emphasis_rule: A rule that highlights the series matching it and mutes the rest,
            read against a summary of each series' ranks, chosen by `by` (`"mean"` by
            default): `{"top": n}` picks the `n` best-ranked series, `{"bottom": n}` the
            worst, and `{"above": v}`, `{"below": v}`, `{"between": (lo, hi)}` compare
            the rank number itself. An explicit `emphasis` role wins. See
            [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum rank shown (the top of the axis).
        ymax: The maximum rank shown (the bottom of the axis).
        show_labels: Whether to print each series' subtitle beside its line
            end, in the series color. Defaults to True.
        label_position: Which line end carries the label, a
            [`BUMP_LABEL_POSITION`][datachart.constants.BUMP_LABEL_POSITION]
            member: `START`, `END` (default), or `BOTH`.
        show_markers: Whether to draw a marker at every period. Defaults to True.
        line_curve: How far each segment eases between two periods, in
            `[0, 1]`: `0` (default) draws straight segments, `1` a full
            sigmoid. The points never move.
        show_legend: Whether to show the legend. Defaults to on only when
            `show_labels` is off.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        show_grid: Which grid lines to show (e.g., "both", "x", "y"); `False`
            draws none. A bump chart draws none unless asked: the ranks read
            from the lines.
        show_values: Whether to print each point's original `y` value beside it.
        value_format: Format string for the value labels: a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] constant or any
            `"{x:.1f}"`, `"{:.1f}%"`, or `"%g"` style string.
        value_step: Label every Nth point (`1` labels all of them). Defaults
            to the smallest step that keeps neighbouring labels apart.
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            [`ASPECT_RATIO`][datachart.constants.ASPECT_RATIO].
        scalex: The x-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each series; the
            ranks still read every series.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the series. See
            [`BumpStyleAttrs`][datachart.typings.BumpStyleAttrs].
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        xticks_format: The x-axis tick label format: a
            [`DATE_FORMAT`][datachart.constants.DATE_FORMAT] member or `strftime`
            pattern on a datetime axis, else a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] member or `"{x:.1f}"`
            style string.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot, at rank positions.
        dlines: Diagonal line(s) to plot, by slope and intercept.
        brackets: Pairwise comparison bracket(s) to draw between two
            categories, with an optional text such as a p-value.
        vspans: Vertical reference band(s) to shade, between two x positions.
        hspans: Horizontal reference band(s) to shade, between two ranks.
        texts: Text annotation(s) to draw.
        x: The key name in data for x-axis values (default: "x").
        y: The key name in data for the ranked values (default: "y").

    Returns:
        The figure containing the bump chart.

    """
    params = dict(locals())
    return render("bumpchart", params)
