from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import (
    validate_dumbbell_records,
    validate_dumbbell_show_values,
    validate_dumbbell_sort_by,
    validate_marker_pair,
    validate_sort,
)
from ..typings import (
    DumbbellRecordAttrs,
    DumbbellStyleAttrs,
    EmphasisRuleAttrs,
    HLineSettingAttrs,
    HSpanSettingAttrs,
    LegendSettingAttrs,
    TextSettingAttrs,
    VLineSettingAttrs,
    VSpanSettingAttrs,
)
from ..constants import (
    DUMBBELL_SORT_KEY,
    DUMBBELL_VALUE,
    EMPHASIS,
    FIG_SIZE,
    LINE_MARKER,
    LINE_STYLE,
    ORIENTATION,
    SCALE,
    SHOW_GRID,
    SORT,
    VALUE_FORMAT,
)

# ================================================
# Main Chart Definition
# ================================================


def DumbbellChart(
    data: Union[List[DumbbellRecordAttrs], List[List[DumbbellRecordAttrs]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    start_name: Optional[str] = None,
    end_name: Optional[str] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    orientation: Optional[Union[ORIENTATION, str]] = ORIENTATION.HORIZONTAL,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_values: Optional[Union[DUMBBELL_VALUE, str]] = None,
    show_direction: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    sort: Optional[Union[SORT, str]] = None,
    sort_by: Optional[Union[DUMBBELL_SORT_KEY, str]] = None,
    marker: Optional[Tuple[Union[LINE_MARKER, str], Union[LINE_MARKER, str]]] = None,
    connector_style: Optional[Union[LINE_STYLE, str]] = None,
    emphasis: Optional[Union[EMPHASIS, str, List[Optional[str]]]] = None,
    emphasis_rule: Optional[EmphasisRuleAttrs] = None,
    style: Optional[
        Union[DumbbellStyleAttrs, List[Optional[DumbbellStyleAttrs]]]
    ] = None,
    xtickrotate: Optional[Union[int, List[Optional[int]]]] = None,
    ytickrotate: Optional[Union[int, List[Optional[int]]]] = None,
    vlines: Optional[Union[VLineSettingAttrs, List[VLineSettingAttrs]]] = None,
    hlines: Optional[Union[HLineSettingAttrs, List[HLineSettingAttrs]]] = None,
    vspans: Optional[Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]] = None,
    hspans: Optional[Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]] = None,
    texts: Optional[Union[TextSettingAttrs, List[TextSettingAttrs]]] = None,
) -> plt.Figure:
    """Creates the dumbbell chart.

    A dumbbell chart shows two values per category: a dot at `start`, a dot
    at `end`, and a connector between them. Use it for a change between two
    states (before and after, one year and the next) or for a range (a
    minimum and a maximum), when the gap matters as much as either value.
    Rows read top to bottom in input order, or sorted by start, end, or the
    delta `end - start`; the endpoints print their values, or the delta
    prints at the connector midpoint, and an optional thin arrow shows
    which way each value moved.

    The rows sit on the category index the box, violin and swarm plots
    share, so the chart composes with them and with other dumbbell charts in
    `Panel`, and in `Grid`. Several data lists overlay in distinct colors,
    each start dot a lighter shade of its end dot.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.charts import DumbbellChart
        >>> figure = DumbbellChart(
        ...     data=[
        ...         {"label": "Norway", "start": 79.8, "end": 83.2},
        ...         {"label": "Chile", "start": 77.1, "end": 81.2},
        ...         {"label": "India", "start": 62.5, "end": 70.9},
        ...     ],
        ...     title="Life Expectancy",
        ...     start_name="2000",
        ...     end_name="2019",
        ...     show_values="delta",
        ... )

    Args:
        data: The records of the chart: a list of `{label, start, end}` dicts with an
            optional `emphasis` key. `label` names the category and is unique within the
            list; `start` and `end` are finite numbers. A list of such lists overlays
            several charts, or draws one per subplot with `subplots`. See
            [`DumbbellRecordAttrs`][datachart.typings.DumbbellRecordAttrs].
        title: The title of the chart.
        xlabel: The label of the horizontal axis.
        ylabel: The label of the vertical axis.
        subtitle: The subtitle of each chart; the legend label of an overlaid
            chart.
        start_name: The name of the start endpoint, shown in the legend.
        end_name: The name of the end endpoint, shown in the legend.
        figsize: The size of the figure as (width, height) in inches. See
            [`FIG_SIZE`][datachart.constants.FIG_SIZE].
        xmin: The minimum value of the x-axis.
        xmax: The maximum value of the x-axis.
        ymin: The minimum value of the y-axis.
        ymax: The maximum value of the y-axis.
        orientation: Which axis the values run along: "horizontal" (default,
            one row per category, the first at the top) or "vertical" (one
            column per category). See [`ORIENTATION`][datachart.constants.ORIENTATION].
        scaley: The scale of the value axis ("linear", "log", "symlog", "logit"),
            whichever way it runs, as on the box plot. See
            [`SCALE`][datachart.constants.SCALE].
        subplots: Whether to draw each data list in its own subplot.
        max_cols: The maximum number of subplot columns.
        sharex: Whether the subplots share the x-axis.
        sharey: Whether the subplots share the y-axis.
        show_legend: Whether to show the legend. Defaults to on when
            `start_name` or `end_name` is given.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        show_grid: Which grid lines to show ("both", "x", "y"). Unset, the
            theme's grid runs along the value axis, whichever way it points.
            See [`SHOW_GRID`][datachart.constants.SHOW_GRID].
        show_values: The value labels: None (none), `"endpoints"` (each
            endpoint's value past its dot, away from the connector), or
            `"delta"` (`end - start` at the connector midpoint). See
            [`DUMBBELL_VALUE`][datachart.constants.DUMBBELL_VALUE].
        show_direction: Whether to draw a thin arrow beside each connector,
            pointing from `start` to `end`: above a horizontal dumbbell, right
            of a vertical one. Records whose endpoints coincide draw none.
        value_format: Format string for the value labels: a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] constant or any
            `"{x:.1f}"`, `"{:+.1f}"`, or `"%g"` style string.
        sort: The order of the categories: None (input order), "ascending",
            or "descending" by the key `sort_by` names. Ties keep input
            order. See [`SORT`][datachart.constants.SORT].
        sort_by: The key `sort` orders by: `"start"` (default), `"end"`, or `"delta"`.
            Requires `sort`. See
            [`DUMBBELL_SORT_KEY`][datachart.constants.DUMBBELL_SORT_KEY].
        marker: The `(start, end)` marker pair of the dots; a chart style
            sets them per chart. See [`LINE_MARKER`][datachart.constants.LINE_MARKER].
        connector_style: The line style of the connectors; a chart style
            sets it per chart. See [`LINE_STYLE`][datachart.constants.LINE_STYLE].
        emphasis: The emphasis role of each chart ("background" or "highlight"), or one
            role per chart. See [`EMPHASIS`][datachart.constants.EMPHASIS].
        emphasis_rule: A one-key dict that highlights the records matching it and mutes
            the rest: `{"above": v}` or `{"below": v}` (strict), `{"between": (lo, hi)}`
            (inclusive), `{"top": n}` or `{"bottom": n}`. Reads each record's delta; a
            record's own `emphasis` key wins over the rule. See
            [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        style: Style configuration(s) for each chart. See
            [`DumbbellStyleAttrs`][datachart.typings.DumbbellStyleAttrs].
        xtickrotate: Rotation angle for the x-axis tick labels.
        ytickrotate: Rotation angle for the y-axis tick labels.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        vspans: Vertical reference band(s) to shade.
        hspans: Horizontal reference band(s) to shade.
        texts: Text annotation(s) to draw.

    Returns:
        The figure containing the dumbbell chart.

    """
    # records and settings fail here, before layers are built
    nested = isinstance(data, list) and bool(data) and isinstance(data[0], list)
    charts_data = data if nested else [data]
    for records in charts_data:
        validate_dumbbell_records(records)
    validate_dumbbell_sort_by(validate_sort(sort), sort_by)
    validate_dumbbell_show_values(show_values)
    validate_marker_pair(marker)

    if show_legend is None and not subplots:
        show_legend = start_name is not None or end_name is not None

    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        style=style,
        xtickrotate=xtickrotate,
        ytickrotate=ytickrotate,
        vlines=vlines,
        hlines=hlines,
        vspans=vspans,
        hspans=hspans,
        texts=texts,
        emphasis=emphasis,
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
        "orientation": orientation,
        "scaley": scaley,
        "subplots": subplots,
        "max_cols": max_cols,
        "sharex": sharex,
        "sharey": sharey,
        "show_legend": show_legend,
        "legend": legend,
        "show_grid": show_grid,
        "show_values": show_values,
        "show_direction": show_direction,
        "value_format": value_format,
        "sort": sort,
        "sort_by": sort_by,
        "start_name": start_name,
        "end_name": end_name,
        "marker": marker,
        "connector_style": connector_style,
        "emphasis_rule": emphasis_rule,
    }

    return render_chart("dumbbellchart", charts, settings)
