from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render
from ..utils._internal.validate import (
    validate_dumbbell_value_kind,
    validate_dumbbell_sort_by,
    validate_marker_pair,
)
from ..typings import (
    DLineSettingAttrs,
    BracketSettingAttrs,
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
    AXIS_SCALE,
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
    orientation: Optional[Union[ORIENTATION, str]] = None,
    scaley: Optional[Union[AXIS_SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    show_values: Optional[bool] = None,
    value_kind: Optional[Union[DUMBBELL_VALUE, str]] = None,
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
    label: Optional[Union[str, List[Optional[str]]]] = None,
    start: Optional[Union[str, List[Optional[str]]]] = None,
    end: Optional[Union[str, List[Optional[str]]]] = None,
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
        ...     show_values=True,
        ...     value_kind="delta",
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
            [`AXIS_SCALE`][datachart.constants.AXIS_SCALE].
        subplots: Whether to draw each data list in its own subplot.
        max_cols: The maximum number of subplot columns.
        sharex: Whether the subplots share the x-axis.
        sharey: Whether the subplots share the y-axis.
        show_legend: Whether to show the legend. Defaults to on when
            `start_name` or `end_name` is given.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        show_grid: Which grid lines to show ("both", "x", "y"); `False`
            draws none. Unset, the theme's grid runs along the value axis,
            whichever way it points. See
            [`SHOW_GRID`][datachart.constants.SHOW_GRID].
        show_values: Whether to print the value labels `value_kind` names.
        value_kind: The value labels `show_values` prints: `"endpoints"`
            (default, each endpoint's value past its dot, away from the
            connector) or `"delta"` (`end - start` at the connector midpoint).
            Ignored while `show_values` is off. See
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
        dlines: Diagonal line(s) to plot, by slope and intercept.
        brackets: Pairwise comparison bracket(s) to draw between two
            categories, with an optional text such as a p-value.
        vspans: Vertical reference band(s) to shade.
        hspans: Horizontal reference band(s) to shade.
        texts: Text annotation(s) to draw.
        label: The key name in data for the category labels (default: "label").
        start: The key name in data for the start values (default: "start").
        end: The key name in data for the end values (default: "end").

    Returns:
        The figure containing the dumbbell chart.

    """
    params = dict(locals())

    # settings fail here, before layers are built
    validate_dumbbell_sort_by(sort, sort_by)
    params["show_values"], params["value_kind"] = validate_dumbbell_value_kind(
        show_values, value_kind
    )
    validate_marker_pair(marker)

    return render("dumbbellchart", params)
