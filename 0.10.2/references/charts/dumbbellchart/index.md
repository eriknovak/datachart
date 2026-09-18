# DumbbellChart

Two values per category, a dot at each and a connector between them. The [Dumbbell Chart guide](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/charts/dumbbellchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.DumbbellChart

```
DumbbellChart(
    data: (
        list[DumbbellRecordAttrs]
        | list[list[DumbbellRecordAttrs]]
    ),
    *,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    subtitle: str | list[str | None] | None = None,
    start_name: str | None = None,
    end_name: str | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    xmin: int | float | None = None,
    xmax: int | float | None = None,
    ymin: int | float | None = None,
    ymax: int | float | None = None,
    orientation: (
        ORIENTATION | str | None
    ) = ORIENTATION.HORIZONTAL,
    scaley: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_values: DUMBBELL_VALUE | str | None = None,
    show_direction: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    sort: SORT | str | None = None,
    sort_by: DUMBBELL_SORT_KEY | str | None = None,
    marker: (
        tuple[LINE_MARKER | str, LINE_MARKER | str] | None
    ) = None,
    connector_style: LINE_STYLE | str | None = None,
    emphasis: (
        EMPHASIS | str | list[str | None] | None
    ) = None,
    emphasis_rule: EmphasisRuleAttrs | None = None,
    style: (
        DumbbellStyleAttrs
        | list[DumbbellStyleAttrs | None]
        | None
    ) = None,
    xtickrotate: int | list[int | None] | None = None,
    ytickrotate: int | list[int | None] | None = None,
    vlines: (
        VLineSettingAttrs | list[VLineSettingAttrs] | None
    ) = None,
    hlines: (
        HLineSettingAttrs | list[HLineSettingAttrs] | None
    ) = None,
    vspans: (
        VSpanSettingAttrs | list[VSpanSettingAttrs] | None
    ) = None,
    hspans: (
        HSpanSettingAttrs | list[HSpanSettingAttrs] | None
    ) = None,
    texts: (
        TextSettingAttrs | list[TextSettingAttrs] | None
    ) = None
) -> plt.Figure
```

Creates the dumbbell chart.

A dumbbell chart shows two values per category: a dot at `start`, a dot at `end`, and a connector between them. Use it for a change between two states (before and after, one year and the next) or for a range (a minimum and a maximum), when the gap matters as much as either value. Rows read top to bottom in input order, or sorted by start, end, or the delta `end - start`; the endpoints print their values, or the delta prints at the connector midpoint, and an optional thin arrow shows which way each value moved.

The rows sit on the category index the box, violin and swarm plots share, so the chart composes with them and with other dumbbell charts in `Panel`, and in `Grid`. Several data lists overlay in distinct colors, each start dot a lighter shade of its end dot.

Examples:

```
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
```

| PARAMETER         | DESCRIPTION                                                                                                                                                                                                                                                                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`            | The records of the chart: a list of {label, start, end} dicts with an optional emphasis key. label names the category and is unique within the list; start and end are finite numbers. A list of such lists overlays several charts, or draws one per subplot with subplots. See DumbbellRecordAttrs. **TYPE:** \`list[DumbbellRecordAttrs] |
| `title`           | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                     |
| `xlabel`          | The label of the horizontal axis. **TYPE:** \`str                                                                                                                                                                                                                                                                                           |
| `ylabel`          | The label of the vertical axis. **TYPE:** \`str                                                                                                                                                                                                                                                                                             |
| `subtitle`        | The subtitle of each chart; the legend label of an overlaid chart. **TYPE:** \`str                                                                                                                                                                                                                                                          |
| `start_name`      | The name of the start endpoint, shown in the legend. **TYPE:** \`str                                                                                                                                                                                                                                                                        |
| `end_name`        | The name of the end endpoint, shown in the legend. **TYPE:** \`str                                                                                                                                                                                                                                                                          |
| `figsize`         | The size of the figure as (width, height) in inches. See FIG_SIZE. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                     |
| `xmin`            | The minimum value of the x-axis. **TYPE:** \`int                                                                                                                                                                                                                                                                                            |
| `xmax`            | The maximum value of the x-axis. **TYPE:** \`int                                                                                                                                                                                                                                                                                            |
| `ymin`            | The minimum value of the y-axis. **TYPE:** \`int                                                                                                                                                                                                                                                                                            |
| `ymax`            | The maximum value of the y-axis. **TYPE:** \`int                                                                                                                                                                                                                                                                                            |
| `orientation`     | Which axis the values run along: "horizontal" (default, one row per category, the first at the top) or "vertical" (one column per category). See ORIENTATION. **TYPE:** \`ORIENTATION                                                                                                                                                       |
| `scaley`          | The scale of the value axis ("linear", "log", "symlog", "logit"), whichever way it runs, as on the box plot. See SCALE. **TYPE:** \`SCALE                                                                                                                                                                                                   |
| `subplots`        | Whether to draw each data list in its own subplot. **TYPE:** \`bool                                                                                                                                                                                                                                                                         |
| `max_cols`        | The maximum number of subplot columns. **TYPE:** \`int                                                                                                                                                                                                                                                                                      |
| `sharex`          | Whether the subplots share the x-axis. **TYPE:** \`bool                                                                                                                                                                                                                                                                                     |
| `sharey`          | Whether the subplots share the y-axis. **TYPE:** \`bool                                                                                                                                                                                                                                                                                     |
| `show_legend`     | Whether to show the legend. Defaults to on when start_name or end_name is given. **TYPE:** \`bool                                                                                                                                                                                                                                           |
| `legend`          | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                      |
| `show_grid`       | Which grid lines to show ("both", "x", "y"); False draws none. Unset, the theme's grid runs along the value axis, whichever way it points. See SHOW_GRID. **TYPE:** \`SHOW_GRID                                                                                                                                                             |
| `show_values`     | The value labels: None (none), "endpoints" (each endpoint's value past its dot, away from the connector), or "delta" (end - start at the connector midpoint). See DUMBBELL_VALUE. **TYPE:** \`DUMBBELL_VALUE                                                                                                                                |
| `show_direction`  | Whether to draw a thin arrow beside each connector, pointing from start to end: above a horizontal dumbbell, right of a vertical one. Records whose endpoints coincide draw none. **TYPE:** \`bool                                                                                                                                          |
| `value_format`    | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:+.1f}", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                     |
| `sort`            | The order of the categories: None (input order), "ascending", or "descending" by the key sort_by names. Ties keep input order. See SORT. **TYPE:** \`SORT                                                                                                                                                                                   |
| `sort_by`         | The key sort orders by: "start" (default), "end", or "delta". Requires sort. See DUMBBELL_SORT_KEY. **TYPE:** \`DUMBBELL_SORT_KEY                                                                                                                                                                                                           |
| `marker`          | The (start, end) marker pair of the dots; a chart style sets them per chart. See LINE_MARKER. **TYPE:** \`tuple\[LINE_MARKER                                                                                                                                                                                                                |
| `connector_style` | The line style of the connectors; a chart style sets it per chart. See LINE_STYLE. **TYPE:** \`LINE_STYLE                                                                                                                                                                                                                                   |
| `emphasis`        | The emphasis role of each chart ("background" or "highlight"), or one role per chart. See EMPHASIS. **TYPE:** \`EMPHASIS                                                                                                                                                                                                                    |
| `emphasis_rule`   | A one-key dict that highlights the records matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}. Reads each record's delta; a record's own emphasis key wins over the rule. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs                           |
| `style`           | Style configuration(s) for each chart. See DumbbellStyleAttrs. **TYPE:** \`DumbbellStyleAttrs                                                                                                                                                                                                                                               |
| `xtickrotate`     | Rotation angle for the x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                  |
| `ytickrotate`     | Rotation angle for the y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                  |
| `vlines`          | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                     |
| `hlines`          | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                                                   |
| `vspans`          | Vertical reference band(s) to shade. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                          |
| `hspans`          | Horizontal reference band(s) to shade. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                        |
| `texts`           | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                    |

| RETURNS      | DESCRIPTION                               |
| ------------ | ----------------------------------------- |
| `plt.Figure` | The figure containing the dumbbell chart. |

## Data

Each record in `data` is a [`DumbbellRecordAttrs`](#datachart.typings.DumbbellRecordAttrs); the `emphasis` parameter renames its keys.

### datachart.typings.DumbbellRecordAttrs

Bases: `TypedDict`

The record attributes for the dumbbell chart.

| ATTRIBUTE  | DESCRIPTION                                                                                                             |
| ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| `label`    | The category, unique within the chart; the label of its row (or column). **TYPE:** `str`                                |
| `start`    | The value of the start endpoint. **TYPE:** \`int                                                                        |
| `end`      | The value of the end endpoint. **TYPE:** \`int                                                                          |
| `emphasis` | The record's own emphasis role ("background" or "highlight"); wins over the chart's emphasis_rule. **TYPE:** \`EMPHASIS |

## Style

`style` takes the keys of [`DumbbellStyleAttrs`](#datachart.typings.DumbbellStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/0.10.2/references/config/index.md).

### datachart.typings.DumbbellStyleAttrs

Bases: `TypedDict`

The typing for the dumbbell chart style.

The value labels take the shared `plot_value_*` keys.

| ATTRIBUTE                        | DESCRIPTION                                                                                                                                           |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_dumbbell_start_color`      | The color of the start dots; None takes the first color of the PaperAccent pair. **TYPE:** \`str                                                      |
| `plot_dumbbell_end_color`        | The color of the end dots; None takes the second color of the PaperAccent pair. **TYPE:** \`str                                                       |
| `plot_dumbbell_alpha`            | The alpha value of the dots. **TYPE:** \`float                                                                                                        |
| `plot_dumbbell_size`             | The size of the dots, in points squared. **TYPE:** \`int                                                                                              |
| `plot_dumbbell_start_marker`     | The marker of the start dots. **TYPE:** \`LINE_MARKER                                                                                                 |
| `plot_dumbbell_end_marker`       | The marker of the end dots. **TYPE:** \`LINE_MARKER                                                                                                   |
| `plot_dumbbell_edge_width`       | The edge width of the dots. **TYPE:** \`int                                                                                                           |
| `plot_dumbbell_edge_color`       | The edge color of the dots. **TYPE:** \`str                                                                                                           |
| `plot_dumbbell_zorder`           | The zorder of the dots. **TYPE:** \`int                                                                                                               |
| `plot_dumbbell_connector_color`  | The color of the connectors. **TYPE:** \`str                                                                                                          |
| `plot_dumbbell_connector_width`  | The line width of the connectors. **TYPE:** \`int                                                                                                     |
| `plot_dumbbell_connector_style`  | The line style of the connectors. **TYPE:** \`LINE_STYLE                                                                                              |
| `plot_dumbbell_connector_zorder` | The zorder of the connectors; below the dots by default. **TYPE:** \`int                                                                              |
| `plot_dumbbell_arrow_color`      | The color of the direction arrows under show_direction. **TYPE:** \`str                                                                               |
| `plot_dumbbell_arrow_width`      | The line width of the direction arrows. **TYPE:** \`int                                                                                               |
| `plot_dumbbell_arrow_style`      | The direction arrow head, as a matplotlib arrow style. **TYPE:** \`str                                                                                |
| `plot_dumbbell_arrow_gap`        | The space between a dot's edge and its direction arrow, in points. **TYPE:** \`int                                                                    |
| `plot_dumbbell_grid_minor`       | The parts each step between labelled values splits into with fainter gridlines, on a gridded linear value axis; 0 or None draws none. **TYPE:** \`int |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.2/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `show_values`                                | [`DUMBBELL_VALUE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.DUMBBELL_VALUE)                                                                                                                          |
| `sort_by`                                    | [`DUMBBELL_SORT_KEY`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.DUMBBELL_SORT_KEY)                                                                                                                    |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                      |
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.ORIENTATION)                                                                                                                                |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                    |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                              |
| `sort`                                       | [`SORT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SORT)                                                                                                                                              |
| `marker`                                     | [`LINE_MARKER`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LINE_MARKER)                                                                                                                                |
| `connector_style`                            | [`LINE_STYLE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LINE_STYLE)                                                                                                                                  |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                      |
