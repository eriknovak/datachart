# GanttChart

A schedule: one bar per task from its start to its end over a date axis. The [Gantt Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/ganttchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.GanttChart

```
GanttChart(
    data: list[GanttTaskAttrs] | list[list[GanttTaskAttrs]],
    *,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    subtitle: str | list[str | None] | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    xmin: date | datetime | None = None,
    xmax: date | datetime | None = None,
    max_cols: int | None = None,
    period: GANTT_DATE_PERIOD | str | None = None,
    show_group_headers: bool | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_values: bool | None = None,
    value_kind: GANTT_VALUE | str | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    show_dependencies: bool | None = None,
    show_today: bool | None = None,
    today: date | datetime | None = None,
    today_label: str | None = None,
    sort: SORT | str | None = None,
    sort_by: GANTT_SORT_KEY | str | None = None,
    emphasis: (
        EMPHASIS | str | list[str | None] | None
    ) = None,
    emphasis_rule: EmphasisRuleAttrs | None = None,
    style: (
        GanttStyleAttrs
        | list[GanttStyleAttrs | None]
        | None
    ) = None,
    xtickrotate: int | list[int | None] | None = None,
    ytickrotate: int | list[int | None] | None = None,
    xticks_format: DATE_FORMAT | str | None = None,
    vlines: (
        VLineSettingAttrs
        | list[VLineSettingAttrs]
        | list[
            VLineSettingAttrs
            | list[VLineSettingAttrs]
            | None
        ]
        | None
    ) = None,
    vspans: (
        VSpanSettingAttrs
        | list[VSpanSettingAttrs]
        | list[
            VSpanSettingAttrs
            | list[VSpanSettingAttrs]
            | None
        ]
        | None
    ) = None,
    texts: (
        TextSettingAttrs
        | list[TextSettingAttrs]
        | list[
            TextSettingAttrs | list[TextSettingAttrs] | None
        ]
        | None
    ) = None,
    task: str | list[str | None] | None = None,
    start: str | list[str | None] | None = None,
    end: str | list[str | None] | None = None,
    group: str | list[str | None] | None = None,
    progress: str | list[str | None] | None = None,
    depends_on: str | list[str | None] | None = None
) -> plt.Figure
```

Creates the gantt chart.

A gantt chart shows a schedule: one horizontal bar per task from its start to its end over a date axis, one row per task, the first task at the top. Use it for project plans, release roadmaps, or any set of activities where when and how long matter more than a single value. Task groups share a colour or get header rows with summary bars, an optional progress fraction fills part of each bar, a task ending when it starts is a milestone marker, dependency arrows link tasks, the date axis can be divided into calendar periods, and a today line marks the present.

The chart is always horizontal, so the axis parameters are spatial: `xlabel`, `xmin`, `xmax`, and `xticks_format` address the horizontal date axis, and `ylabel` the vertical task axis. It composes in `Grid`, but not in `Panel`.

Examples:

```
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
```

| PARAMETER            | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `data`               | The task records of the schedule: a list of {task, start, end} dicts with optional group, progress, depends_on, and emphasis keys. start and end are date, datetime, numpy.datetime64, or pandas Timestamp objects; date strings are never parsed. A list of such lists draws one schedule per subplot. See GanttTaskAttrs. **TYPE:** \`list[GanttTaskAttrs]                                                 |
| `title`              | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                      |
| `xlabel`             | The label of the horizontal date axis. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                       |
| `ylabel`             | The label of the vertical task axis. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                         |
| `subtitle`           | The subtitle of each schedule. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                               |
| `figsize`            | The size of the figure as (width, height) in inches. See FIG_SIZE. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                      |
| `xmin`               | The start of the date window, as a temporal object. **TYPE:** \`date                                                                                                                                                                                                                                                                                                                                         |
| `xmax`               | The end of the date window, as a temporal object. **TYPE:** \`date                                                                                                                                                                                                                                                                                                                                           |
| `max_cols`           | The maximum number of subplot columns for several schedules. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                 |
| `period`             | The calendar period the date axis is divided into: None (concise date ticks), "day", "week", "month", "quarter", "year", or "project_month" (M1, M2, … from xmin or the earliest start). Lines mark the period edges, each period is labelled at its centre, and a row beneath names the enclosing month or year. xticks_format sets the period labels. See GANTT_DATE_PERIOD. **TYPE:** \`GANTT_DATE_PERIOD |
| `show_group_headers` | Whether to give each task group a header row with a summary bar from its first start to its last end, the group's rows clustered beneath it and a gap before the next group. Raises when no task carries a group. **TYPE:** \`bool                                                                                                                                                                           |
| `show_legend`        | Whether to show the legend of the task groups. Defaults to on when any task carries a group and the group headers are off. **TYPE:** \`bool                                                                                                                                                                                                                                                                  |
| `legend`             | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                       |
| `show_grid`          | Which grid lines to show ("both", "x", "y"); False draws none. See SHOW_GRID. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                          |
| `show_values`        | Whether to print a label past each bar end, the one value_kind names. A milestone prints its date instead, in the xticks_format or as day and month. **TYPE:** \`bool                                                                                                                                                                                                                                        |
| `value_kind`         | The label show_values prints: "duration" (default, the duration in days) or "progress" (the progress as a percentage). Ignored while show_values is off. See GANTT_VALUE. **TYPE:** \`GANTT_VALUE                                                                                                                                                                                                            |
| `value_format`       | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. It formats the duration in days, or the progress fraction. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                           |
| `show_dependencies`  | Whether to draw an arrow from the end of each task named in depends_on to the start of the task depending on it. **TYPE:** \`bool                                                                                                                                                                                                                                                                            |
| `show_today`         | Whether to draw the today line. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                             |
| `today`              | The date of the today line; the current date when not given. **TYPE:** \`date                                                                                                                                                                                                                                                                                                                                |
| `today_label`        | The text printed at the foot of the today line; none when not given. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                         |
| `sort`               | The order of the task rows: None (input order), "ascending", or "descending" by the key sort_by names. Ties keep input order. See SORT. **TYPE:** \`SORT                                                                                                                                                                                                                                                     |
| `sort_by`            | The key sort orders by: "start" (default) orders every row by its start; "group" clusters the rows by group, the groups ordered by their earliest start and the tasks within a group by start. Requires sort. See GANTT_SORT_KEY. **TYPE:** \`GANTT_SORT_KEY                                                                                                                                                 |
| `emphasis`           | The emphasis role of the whole schedule ("background" or "highlight"), or one role per schedule. See EMPHASIS. **TYPE:** \`EMPHASIS                                                                                                                                                                                                                                                                          |
| `emphasis_rule`      | A one-key dict that highlights the tasks matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}. Reads each task's duration in days; a task's own emphasis key wins over the rule. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs                                                                                       |
| `style`              | Style configuration(s) for the schedule. See GanttStyleAttrs. **TYPE:** \`GanttStyleAttrs                                                                                                                                                                                                                                                                                                                    |
| `xtickrotate`        | Rotation angle for the date-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                |
| `ytickrotate`        | Rotation angle for the task-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                |
| `xticks_format`      | The date-axis tick label format: a DATE_FORMAT member or strftime pattern. **TYPE:** \`DATE_FORMAT                                                                                                                                                                                                                                                                                                           |
| `vlines`             | Vertical line(s) to plot, at temporal x positions. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                                                             |
| `vspans`             | Vertical reference band(s) to shade, between two temporal positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                           |
| `texts`              | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                     |
| `task`               | The key name in data for the task names (default: "task"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                   |
| `start`              | The key name in data for the task starts (default: "start"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                 |
| `end`                | The key name in data for the task ends (default: "end"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                     |
| `group`              | The key name in data for the task groups (default: "group"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                 |
| `progress`           | The key name in data for the task progress (default: "progress"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                            |
| `depends_on`         | The key name in data for the task dependencies (default: "depends_on"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                      |

| RETURNS      | DESCRIPTION                            |
| ------------ | -------------------------------------- |
| `plt.Figure` | The figure containing the gantt chart. |

## Data

Each record in `data` is a [`GanttTaskAttrs`](#datachart.typings.GanttTaskAttrs); the `emphasis` parameter renames its keys.

### datachart.typings.GanttTaskAttrs

Bases: `TypedDict`

The task record attributes for the gantt chart.

| ATTRIBUTE    | DESCRIPTION                                                                                                                                          |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `task`       | The task name, unique within the chart; the label of its row. **TYPE:** `str`                                                                        |
| `start`      | When the task starts: a date, datetime, numpy.datetime64, or pandas Timestamp. Date strings are never parsed. **TYPE:** \`date                       |
| `end`        | When the task ends, of the same temporal types; never before start. A task ending when it starts is a milestone, drawn as a marker. **TYPE:** \`date |
| `group`      | The task group; tasks of one group share a color and a legend entry. **TYPE:** \`str                                                                 |
| `progress`   | The fraction of the task done, in [0, 1]; drawn as an inner bar. **TYPE:** \`int                                                                     |
| `depends_on` | The names of the tasks this task depends on. **TYPE:** \`list[str]                                                                                   |
| `emphasis`   | The task's own emphasis role ("background" or "highlight"); wins over the chart's emphasis_rule. **TYPE:** \`EMPHASIS                                |

## Style

`style` takes the keys of [`GanttStyleAttrs`](#datachart.typings.GanttStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.GanttStyleAttrs

Bases: `TypedDict`

The typing for the gantt chart style.

The range bars take the `plot_bar_*` keys (color, alpha, edge, hatch, zorder); these keys set what is specific to a gantt chart.

| ATTRIBUTE                      | DESCRIPTION                                                                                               |
| ------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `plot_gantt_bar_height`        | The height of a task bar, as a fraction of its row. **TYPE:** \`int                                       |
| `plot_gantt_progress_color`    | The color of the progress bar; None darkens the task bar's color. **TYPE:** \`str                         |
| `plot_gantt_progress_alpha`    | The alpha value of the progress bar. **TYPE:** \`float                                                    |
| `plot_gantt_progress_height`   | The height of the progress bar, as a fraction of the task bar. **TYPE:** \`int                            |
| `plot_gantt_dependency_color`  | The color of the dependency arrows. **TYPE:** \`str                                                       |
| `plot_gantt_dependency_width`  | The line width of the dependency arrows. **TYPE:** \`int                                                  |
| `plot_gantt_dependency_style`  | The arrow head of the dependency arrows, as a matplotlib arrow style. **TYPE:** \`str                     |
| `plot_gantt_dependency_zorder` | The zorder of the dependency arrows. **TYPE:** \`int                                                      |
| `plot_gantt_dependency_entry`  | The side of the dependent task a dependency arrow enters ("top" or "left"). **TYPE:** \`GANTT_ARROW_ENTRY |
| `plot_gantt_summary_height`    | The height of a group's summary bar under show_group_headers, as a fraction of its row. **TYPE:** \`int   |
| `plot_gantt_summary_color`     | The color of the summary bars; None takes each group's color. **TYPE:** \`str                             |
| `plot_gantt_group_gap`         | The empty space before each group header, in rows. **TYPE:** \`int                                        |
| `plot_gantt_milestone_marker`  | The marker of a milestone, a task whose start equals its end. **TYPE:** \`LINE_MARKER                     |
| `plot_gantt_milestone_size`    | The size of the milestone marker, in points. **TYPE:** \`int                                              |
| `plot_gantt_today_color`       | The color of the today line. **TYPE:** \`str                                                              |
| `plot_gantt_today_style`       | The line style of the today line. **TYPE:** \`LINE_STYLE                                                  |
| `plot_gantt_today_width`       | The line width of the today line. **TYPE:** \`int                                                         |
| `plot_gantt_today_alpha`       | The alpha value of the today line. **TYPE:** \`float                                                      |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `period`                                     | [`GANTT_DATE_PERIOD`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.GANTT_DATE_PERIOD)                                                                                                                 |
| `value_kind`                                 | [`GANTT_VALUE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.GANTT_VALUE)                                                                                                                             |
| `sort_by`                                    | [`GANTT_SORT_KEY`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.GANTT_SORT_KEY)                                                                                                                       |
| `xticks_format`                              | [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)                                                                                                                             |
| `style={"plot_gantt_dependency_entry": ...}` | [`GANTT_ARROW_ENTRY`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.GANTT_ARROW_ENTRY)                                                                                                                 |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `sort`                                       | [`SORT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SORT)                                                                                                                                           |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                   |
