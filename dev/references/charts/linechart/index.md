# LineChart

A value along an ordered axis, one line per series. The [Line Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/linechart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.LineChart

```
LineChart(
    data: (
        list[LineDataPointAttrs]
        | list[list[LineDataPointAttrs]]
    ),
    *,
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
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_yerr: bool | None = None,
    show_area: bool | None = None,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    value_step: int | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    scalex: SCALE | str | None = None,
    scaley: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        LineStyleAttrs | list[LineStyleAttrs | None] | None
    ) = None,
    xticks: (
        list[int | float | datetime]
        | list[list[int | float | datetime]]
        | None
    ) = None,
    xticklabels: list[str] | list[list[str]] | None = None,
    xtickrotate: int | list[int | None] | None = None,
    yticks: (
        list[int | float] | list[list[int | float]] | None
    ) = None,
    yticklabels: list[str] | list[list[str]] | None = None,
    ytickrotate: int | list[int | None] | None = None,
    xticks_format: (
        VALUE_FORMAT | DATE_FORMAT | str | None
    ) = None,
    yticks_format: (
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
    y: str | list[str | None] | None = None,
    yerr: str | list[str | None] | None = None
) -> plt.Figure
```

Creates the line chart.

Lines connect ordered (x, y) points to show how a value changes along a continuous axis, typically time. Use it for trends, growth, and comparing the trajectories of several series on the same scale. For unordered categories use BarChart; for unconnected samples use ScatterChart.

Examples:

```
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
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The data points for the line chart(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. **TYPE:** \`list[LineDataPointAttrs]                                                                                                                                                                                                                                         |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                 |
| `xlabel`        | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                       |
| `ylabel`        | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                       |
| `subtitle`      | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                           |
| `emphasis`      | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, thinner line, behind the others, no legend entry), "highlight" bolds it and brings it to the front, None leaves it unchanged. **TYPE:** \`EMPHASIS                                                                                                                                        |
| `emphasis_rule` | A rule that highlights the lines matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against a summary of each line's own y values, chosen by by: "mean" (default), "median", "min", "max", or "sum". An explicit emphasis role wins, and a count ranks across every line. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`       | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                            |
| `xmin`          | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                               |
| `xmax`          | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                               |
| `ymin`          | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                               |
| `ymax`          | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                               |
| `show_legend`   | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                            |
| `legend`        | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                  |
| `show_grid`     | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                              |
| `show_yerr`     | Whether to show y-axis error bars. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                     |
| `show_area`     | Whether to show the area under the line. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                               |
| `show_values`   | Whether to print each point's value above or below it. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                 |
| `value_format`  | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                 |
| `value_step`    | Label every Nth point (1 labels all of them). Defaults to the smallest step that keeps neighbouring labels apart. **TYPE:** \`int                                                                                                                                                                                                                                                                                       |
| `aspect_ratio`  | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                            |
| `scalex`        | The x-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                             |
| `scaley`        | The y-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                             |
| `subplots`      | Whether to create separate subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                    |
| `max_cols`      | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                             |
| `sharex`        | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                               |
| `sharey`        | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                               |
| `style`         | Style configuration(s) for the line(s). **TYPE:** \`LineStyleAttrs                                                                                                                                                                                                                                                                                                                                                      |
| `xticks`        | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                     |
| `xticklabels`   | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                        |
| `xtickrotate`   | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                  |
| `yticks`        | Custom y-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                     |
| `yticklabels`   | Custom y-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                        |
| `ytickrotate`   | Rotation angle for y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                  |
| `xticks_format` | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                               |
| `yticks_format` | The y-axis tick label format, as xticks_format. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                |
| `vlines`        | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                 |
| `hlines`        | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                               |
| `dlines`        | Diagonal line(s) to plot, by slope and intercept. **TYPE:** \`DLineSettingAttrs                                                                                                                                                                                                                                                                                                                                         |
| `vspans`        | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                                             |
| `hspans`        | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                                           |
| `texts`         | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                |
| `x`             | The key name in data for x-axis values (default: "x"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                  |
| `y`             | The key name in data for y-axis values (default: "y"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                  |
| `yerr`          | The key name in data for y-axis error values (default: "yerr"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                         |

| RETURNS      | DESCRIPTION                           |
| ------------ | ------------------------------------- |
| `plt.Figure` | The figure containing the line chart. |

## Data

Each record in `data` is a [`LineDataPointAttrs`](#datachart.typings.LineDataPointAttrs); the `x`, `y` and `yerr` parameters rename its keys.

### datachart.typings.LineDataPointAttrs

Bases: `TypedDict`

The data point attributes for the line chart.

| ATTRIBUTE | DESCRIPTION                             |
| --------- | --------------------------------------- |
| `x`       | The x-axis value. **TYPE:** \`int       |
| `y`       | The y-axis value. **TYPE:** \`int       |
| `yerr`    | The y-axis error value. **TYPE:** \`int |

## Style

`style` takes the keys of [`LineStyleAttrs`](#datachart.typings.LineStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)), the area fill ([`AreaStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.AreaStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.LineStyleAttrs

Bases: `TypedDict`

The typing for the line chart style.

| ATTRIBUTE                  | DESCRIPTION                                                         |
| -------------------------- | ------------------------------------------------------------------- |
| `plot_line_color`          | The line color. **TYPE:** \`str                                     |
| `plot_line_alpha`          | The alpha value of the line. **TYPE:** \`float                      |
| `plot_line_style`          | The line style. **TYPE:** \`LINE_STYLE                              |
| `plot_line_marker`         | The line marker. **TYPE:** \`LINE_MARKER                            |
| `plot_line_width`          | The line width. **TYPE:** \`int                                     |
| `plot_line_drawstyle`      | The line draw style. **TYPE:** \`LINE_DRAW_STYLE                    |
| `plot_line_zorder`         | The zorder of the line. **TYPE:** \`int                             |
| `plot_xticks_label_rotate` | The label rotation of the xticks in the line chart. **TYPE:** \`int |
| `plot_yticks_label_rotate` | The label rotation of the yticks in the line chart. **TYPE:** \`int |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                   |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                           |
| `scalex`                                     | [`SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE)                                                                                                                                         |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE)                                                                                                                                         |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
