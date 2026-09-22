# BumpChart

Rank over time, one line per series. The [Bump Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/bumpchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.BumpChart

```
BumpChart(
    data: (
        list[LineDataPointAttrs]
        | list[list[LineDataPointAttrs]]
    ),
    *,
    rank_by: BUMP_RANK | str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    subtitle: str | list[str | None] | None = None,
    emphasis: (
        EMPHASIS | str | list[str | None] | None
    ) = None,
    emphasis_rule: EmphasisRuleAttrs | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    xmin: int | float | datetime | None = None,
    xmax: int | float | datetime | None = None,
    ymin: int | float | None = None,
    ymax: int | float | None = None,
    show_labels: bool | None = None,
    label_position: BUMP_LABEL_POSITION | str | None = None,
    show_markers: bool | None = None,
    line_curve: float | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    value_step: int | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    scalex: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        BumpStyleAttrs | list[BumpStyleAttrs | None] | None
    ) = None,
    xticks: (
        list[int | float | datetime]
        | list[list[int | float | datetime]]
        | None
    ) = None,
    xticklabels: list[str] | list[list[str]] | None = None,
    xtickrotate: int | list[int | None] | None = None,
    xticks_format: (
        VALUE_FORMAT | DATE_FORMAT | str | None
    ) = None,
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
    hlines: (
        HLineSettingAttrs
        | list[HLineSettingAttrs]
        | list[
            HLineSettingAttrs
            | list[HLineSettingAttrs]
            | None
        ]
        | None
    ) = None,
    dlines: (
        DLineSettingAttrs
        | list[DLineSettingAttrs]
        | list[
            DLineSettingAttrs
            | list[DLineSettingAttrs]
            | None
        ]
        | None
    ) = None,
    brackets: (
        BracketSettingAttrs
        | list[BracketSettingAttrs]
        | list[
            BracketSettingAttrs
            | list[BracketSettingAttrs]
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
    hspans: (
        HSpanSettingAttrs
        | list[HSpanSettingAttrs]
        | list[
            HSpanSettingAttrs
            | list[HSpanSettingAttrs]
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
    x: str | list[str | None] | None = None,
    y: str | list[str | None] | None = None
) -> plt.Figure
```

Creates the bump chart.

A bump chart shows rank over time: one line per series, rank 1 at the top, a marker at every period, and the series named at the line's end in place of a y-axis. Use it for league tables, popularity, or market-share rankings, where the order matters more than the gaps between values. Periods may be numbers, dates, or strings; strings draw as categories in first-seen order. For the values themselves use LineChart; for a single period's order use BarChart with `sort`.

Examples:

```
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
```

| PARAMETER        | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `data`           | The data points of the series. Can be a single list of data points for one series, or a list of lists for several. **TYPE:** \`list[LineDataPointAttrs]                                                                                                                                                                                                                                          |
| `rank_by`        | How y becomes a rank, a BUMP_RANK member: VALUE_DESCENDING (default) ranks the highest value first at each period, VALUE_ASCENDING the lowest, and GIVEN reads y as the rank (a positive integer). Ranking reads the series present at a period; a series without a point there leaves a gap. Ties keep input order. **TYPE:** \`BUMP_RANK                                                       |
| `title`          | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                          |
| `xlabel`         | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                |
| `ylabel`         | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                |
| `subtitle`       | The subtitle(s) of the series. Used as end labels and legend labels. **TYPE:** \`str                                                                                                                                                                                                                                                                                                             |
| `emphasis`       | The emphasis role(s) for individual series, aligned like style: "background" mutes a series, "highlight" bolds it and brings it to the front, None leaves it unchanged. **TYPE:** \`EMPHASIS                                                                                                                                                                                                     |
| `emphasis_rule`  | A rule that highlights the series matching it and mutes the rest, read against a summary of each series' ranks, chosen by by ("mean" by default): {"top": n} picks the n best-ranked series, {"bottom": n} the worst, and {"above": v}, {"below": v}, {"between": (lo, hi)} compare the rank number itself. An explicit emphasis role wins. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`        | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                     |
| `xmin`           | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                        |
| `xmax`           | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                        |
| `ymin`           | The minimum rank shown (the top of the axis). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                    |
| `ymax`           | The maximum rank shown (the bottom of the axis). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                 |
| `show_labels`    | Whether to print each series' subtitle beside its line end, in the series color. Defaults to True. **TYPE:** \`bool                                                                                                                                                                                                                                                                              |
| `label_position` | Which line end carries the label, a BUMP_LABEL_POSITION member: START, END (default), or BOTH. **TYPE:** \`BUMP_LABEL_POSITION                                                                                                                                                                                                                                                                   |
| `show_markers`   | Whether to draw a marker at every period. Defaults to True. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                     |
| `line_curve`     | How far each segment eases between two periods, in \[0, 1\]: 0 (default) draws straight segments, 1 a full sigmoid. The points never move. **TYPE:** \`float                                                                                                                                                                                                                                     |
| `show_legend`    | Whether to show the legend. Defaults to on only when show_labels is off. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                        |
| `legend`         | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                           |
| `show_grid`      | Which grid lines to show (e.g., "both", "x", "y"); False draws none. A bump chart draws none unless asked: the ranks read from the lines. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                  |
| `show_values`    | Whether to print each point's original y value beside it. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                       |
| `value_format`   | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                          |
| `value_step`     | Label every Nth point (1 labels all of them). Defaults to the smallest step that keeps neighbouring labels apart. **TYPE:** \`int                                                                                                                                                                                                                                                                |
| `aspect_ratio`   | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                     |
| `scalex`         | The x-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                      |
| `subplots`       | Whether to create separate subplots for each series; the ranks still read every series. **TYPE:** \`bool                                                                                                                                                                                                                                                                                         |
| `max_cols`       | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                      |
| `sharex`         | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                        |
| `sharey`         | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                        |
| `style`          | Style configuration(s) for the series. See BumpStyleAttrs. **TYPE:** \`BumpStyleAttrs                                                                                                                                                                                                                                                                                                            |
| `xticks`         | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                              |
| `xticklabels`    | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                 |
| `xtickrotate`    | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                           |
| `xticks_format`  | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                        |
| `vlines`         | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                                                                          |
| `hlines`         | Horizontal line(s) to plot, at rank positions. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                                                                                     |
| `dlines`         | Diagonal line(s) to plot, by slope and intercept. **TYPE:** \`DLineSettingAttrs                                                                                                                                                                                                                                                                                                                  |
| `brackets`       | Pairwise comparison bracket(s) to draw between two categories, with an optional text such as a p-value. **TYPE:** \`BracketSettingAttrs                                                                                                                                                                                                                                                          |
| `vspans`         | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                      |
| `hspans`         | Horizontal reference band(s) to shade, between two ranks. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                          |
| `texts`          | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                         |
| `x`              | The key name in data for x-axis values (default: "x"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                           |
| `y`              | The key name in data for the ranked values (default: "y"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                       |

| RETURNS      | DESCRIPTION                           |
| ------------ | ------------------------------------- |
| `plt.Figure` | The figure containing the bump chart. |

## Data

Each record in `data` is a [`LineDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/linechart/#datachart.typings.LineDataPointAttrs); the `x` and `y` parameters rename its keys.

## Style

`style` takes the keys of [`BumpStyleAttrs`](#datachart.typings.BumpStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineStyleAttrs)), pairwise brackets ([`BracketStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.BracketStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.BumpStyleAttrs

Bases: `TypedDict`

The typing for the bump chart style.

The line takes the `plot_line_*` keys (color, alpha, style, zorder); these keys set what is specific to a bump chart.

| ATTRIBUTE                 | DESCRIPTION                                                              |
| ------------------------- | ------------------------------------------------------------------------ |
| `plot_bump_line_width`    | The line width. **TYPE:** \`int                                          |
| `plot_bump_marker`        | The marker at every period. **TYPE:** \`LINE_MARKER                      |
| `plot_bump_marker_size`   | The marker size. **TYPE:** \`int                                         |
| `plot_bump_label_padding` | The gap between a line end and its end label, in points. **TYPE:** \`int |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rank_by`                                    | [`BUMP_RANK`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.BUMP_RANK)                                                                                                                                 |
| `label_position`                             | [`BUMP_LABEL_POSITION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.BUMP_LABEL_POSITION)                                                                                                             |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                   |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                           |
| `scalex`                                     | [`SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE)                                                                                                                                         |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
