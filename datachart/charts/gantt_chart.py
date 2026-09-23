from datetime import date, datetime
from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render
from ..utils._internal.validate import (
    validate_gantt_groups,
    validate_gantt_sort_by,
    validate_gantt_tasks,
    validate_sort,
)
from ..typings import (
    EmphasisRuleAttrs,
    GanttStyleAttrs,
    GanttTaskAttrs,
    LegendSettingAttrs,
    TextSettingAttrs,
    VLineSettingAttrs,
    VSpanSettingAttrs,
)
from ..constants import (
    DATE_FORMAT,
    EMPHASIS,
    FIG_SIZE,
    GANTT_DATE_PERIOD,
    GANTT_SORT_KEY,
    GANTT_VALUE,
    SHOW_GRID,
    SORT,
    VALUE_FORMAT,
)

# ================================================
# Main Chart Definition
# ================================================


def GanttChart(
    data: Union[List[GanttTaskAttrs], List[List[GanttTaskAttrs]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[date, datetime]] = None,
    xmax: Optional[Union[date, datetime]] = None,
    max_cols: Optional[int] = None,
    period: Optional[Union[GANTT_DATE_PERIOD, str]] = None,
    show_group_headers: Optional[bool] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    show_values: Optional[Union[GANTT_VALUE, str]] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    show_dependencies: Optional[bool] = None,
    show_today: Optional[bool] = None,
    today: Optional[Union[date, datetime]] = None,
    today_label: Optional[str] = None,
    sort: Optional[Union[SORT, str]] = None,
    sort_by: Optional[Union[GANTT_SORT_KEY, str]] = None,
    emphasis: Optional[Union[EMPHASIS, str, List[Optional[str]]]] = None,
    emphasis_rule: Optional[EmphasisRuleAttrs] = None,
    style: Optional[Union[GanttStyleAttrs, List[Optional[GanttStyleAttrs]]]] = None,
    xtickrotate: Optional[int] = None,
    ytickrotate: Optional[int] = None,
    xticks_format: Optional[Union[DATE_FORMAT, str]] = None,
    vlines: Optional[Union[VLineSettingAttrs, List[VLineSettingAttrs]]] = None,
    vspans: Optional[Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]] = None,
    texts: Optional[Union[TextSettingAttrs, List[TextSettingAttrs]]] = None,
) -> plt.Figure:
    """Creates the gantt chart.

    A gantt chart shows a schedule: one horizontal bar per task from its
    start to its end over a date axis, one row per task, the first task at
    the top. Use it for project plans, release roadmaps, or any set of
    activities where when and how long matter more than a single value. Task
    groups share a colour or get header rows with summary bars, an optional
    progress fraction fills part of each bar, a task ending when it starts is
    a milestone marker, dependency arrows link tasks, the date axis can be
    divided into calendar periods, and a today line marks the present.

    The chart is always horizontal, so the axis parameters are spatial:
    `xlabel`, `xmin`, `xmax`, and `xticks_format` address the horizontal date
    axis, and `ylabel` the vertical task axis. It composes in `Grid`, but not
    in `Panel`.

    Examples:
        >>> from datetime import date
        >>> from datachart.charts import GanttChart
        >>> figure = GanttChart(
        ...     data=[
        ...         {"task": "Design", "start": date(2024, 1, 1), "end": date(2024, 1, 12),
        ...          "group": "Plan", "progress": 1.0},
        ...         {"task": "Build", "start": date(2024, 1, 10), "end": date(2024, 2, 9),
        ...          "group": "Make", "progress": 0.4, "depends_on": ["Design"]},
        ...         {"task": "Test", "start": date(2024, 2, 5), "end": date(2024, 2, 23),
        ...          "group": "Make", "depends_on": ["Build"]},
        ...     ],
        ...     title="Release Plan",
        ...     show_dependencies=True,
        ... )

    Args:
        data: The task records of the schedule: a list of `{task, start, end}` dicts
            with optional `group`, `progress`, `depends_on`, and `emphasis` keys.
            `start` and `end` are `date`, `datetime`, `numpy.datetime64`, or pandas
            `Timestamp` objects; date strings are never parsed. A list of such lists
            draws one schedule per subplot. See
            [`GanttTaskAttrs`][datachart.typings.GanttTaskAttrs].
        title: The title of the chart.
        xlabel: The label of the horizontal date axis.
        ylabel: The label of the vertical task axis.
        subtitle: The subtitle of each schedule.
        figsize: The size of the figure as (width, height) in inches. See
            [`FIG_SIZE`][datachart.constants.FIG_SIZE].
        xmin: The start of the date window, as a temporal object.
        xmax: The end of the date window, as a temporal object.
        max_cols: The maximum number of subplot columns for several schedules.
        period: The calendar period the date axis is divided into: None (concise date
            ticks), "day", "week", "month", "quarter", "year", or "project_month" (M1,
            M2, … from `xmin` or the earliest start). Lines mark the period edges, each
            period is labelled at its centre, and a row beneath names the enclosing
            month or year. `xticks_format` sets the period labels. See
            [`GANTT_DATE_PERIOD`][datachart.constants.GANTT_DATE_PERIOD].
        show_group_headers: Whether to give each task group a header row with
            a summary bar from its first start to its last end, the group's
            rows clustered beneath it and a gap before the next group. Raises
            when no task carries a `group`.
        show_legend: Whether to show the legend of the task groups. Defaults
            to on when any task carries a `group` and the group headers are
            off.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        show_grid: Which grid lines to show ("both", "x", "y"); `False`
            draws none. See [`SHOW_GRID`][datachart.constants.SHOW_GRID].
        show_values: The label printed past each bar end: None (none), `"duration"` (the
            duration in days), or `"progress"` (the progress as a percentage). A
            milestone prints its date instead, in the `xticks_format` or as day and
            month. See [`GANTT_VALUE`][datachart.constants.GANTT_VALUE].
        value_format: Format string for the value labels: a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] constant or any
            `"{x:.1f}"`, `"{:.1f}%"`, or `"%g"` style string. It formats the duration in
            days, or the progress fraction.
        show_dependencies: Whether to draw an arrow from the end of each task
            named in `depends_on` to the start of the task depending on it.
        show_today: Whether to draw the today line.
        today: The date of the today line; the current date when not given.
        today_label: The text printed at the foot of the today line; none
            when not given.
        sort: The order of the task rows: None (input order), "ascending",
            or "descending" by the key `sort_by` names. Ties keep input
            order. See [`SORT`][datachart.constants.SORT].
        sort_by: The key `sort` orders by: `"start"` (default) orders every row by its
            start; `"group"` clusters the rows by group, the groups ordered by their
            earliest start and the tasks within a group by start. Requires `sort`. See
            [`GANTT_SORT_KEY`][datachart.constants.GANTT_SORT_KEY].
        emphasis: The emphasis role of the whole schedule ("background" or "highlight"),
            or one role per schedule. See [`EMPHASIS`][datachart.constants.EMPHASIS].
        emphasis_rule: A one-key dict that highlights the tasks matching it and mutes
            the rest: `{"above": v}` or `{"below": v}` (strict), `{"between": (lo, hi)}`
            (inclusive), `{"top": n}` or `{"bottom": n}`. Reads each task's duration in
            days; a task's own `emphasis` key wins over the rule. See
            [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        style: Style configuration(s) for the schedule. See
            [`GanttStyleAttrs`][datachart.typings.GanttStyleAttrs].
        xtickrotate: Rotation angle for the date-axis tick labels.
        ytickrotate: Rotation angle for the task-axis tick labels.
        xticks_format: The date-axis tick label format: a
            [`DATE_FORMAT`][datachart.constants.DATE_FORMAT] member or `strftime`
            pattern.
        vlines: Vertical line(s) to plot, at temporal `x` positions.
        vspans: Vertical reference band(s) to shade, between two temporal
            positions.
        texts: Text annotation(s) to draw.

    Returns:
        The figure containing the gantt chart.

    """
    params = dict(locals())

    # records fail here, before layers are built; settings fail in the layer
    schedules = data if data and isinstance(data[0], list) else [data]
    sort_key = validate_gantt_sort_by(validate_sort(sort), sort_by)
    for records in schedules:
        validate_gantt_tasks(records)
        validate_gantt_groups(
            records, sort_key if sort is not None else None, show_group_headers
        )

    return render("ganttchart", params)
