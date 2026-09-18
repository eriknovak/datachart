# StackedAreaChart

Parts of a total along an ordered axis, filled on top of each other. The [Stacked Area Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/stackedareachart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.StackedAreaChart

```
StackedAreaChart(
    data: (
        list[LineDataPointAttrs]
        | list[list[LineDataPointAttrs]]
    ),
    *,
    baseline: STACKED_AREA_BASELINE | str | None = None,
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
        StackedAreaStyleAttrs
        | list[StackedAreaStyleAttrs | None]
        | None
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

Creates the stacked area chart.

Stacked areas fill each series on top of the previous one along an ordered axis, so the top edge traces the total and the bands show how it splits into parts — class proportions over time, traffic by channel per year. Every series must share the same `x` values. Use it for composition that changes along an axis; for the trajectories themselves use LineChart, and for composition at a few discrete categories use BarChart with `bar_mode="stack"`.

Examples:

```
>>> from datachart.charts import StackedAreaChart
>>> figure = StackedAreaChart(
...     data=[
...         [{"x": 1, "y": 3}, {"x": 2, "y": 4}, {"x": 3, "y": 5}],
...         [{"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 3, "y": 1}],
...     ],
...     subtitle=["Mobile", "Desktop"],
...     title="Traffic by Device",
...     xlabel="Year",
...     ylabel="Visits",
... )
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                  |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The data points for the stacked series. A single list of points draws one band; a list of lists draws one band per series, the first at the bottom. Every series must hold the same x values in the same order. **TYPE:** \`list[LineDataPointAttrs]                                                                                                                                                                         |
| `baseline`      | Where the first series starts: "zero" (default), "percent" (each x normalised to 100), "sym" (centred on zero), "wiggle" or "weighted_wiggle" (streamgraph baselines). See STACKED_AREA_BASELINE. **TYPE:** \`STACKED_AREA_BASELINE                                                                                                                                                                                          |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                      |
| `xlabel`        | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                            |
| `ylabel`        | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                            |
| `subtitle`      | The subtitle(s) for individual series. Used as legend labels. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                |
| `emphasis`      | The emphasis role(s) for individual series, aligned like style: "background" mutes a band (theme muted color, lowered alpha, no legend entry), "highlight" brings it to the front, None leaves it unchanged. **TYPE:** \`EMPHASIS                                                                                                                                                                                            |
| `emphasis_rule` | A rule that highlights the series matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against a summary of each series's own y values, chosen by by: "mean" (default), "median", "min", "max", or "sum". An explicit emphasis role wins, and a count ranks across every series. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`       | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                 |
| `xmin`          | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                    |
| `xmax`          | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                    |
| `ymin`          | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                    |
| `ymax`          | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                    |
| `show_legend`   | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                 |
| `legend`        | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                       |
| `show_grid`     | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                   |
| `show_values`   | Whether to print each value at the midpoint of its band. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                    |
| `value_format`  | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                      |
| `value_step`    | Label every Nth x position (1 labels all of them). Defaults to the smallest step that keeps neighbouring labels apart. **TYPE:** \`int                                                                                                                                                                                                                                                                                       |
| `aspect_ratio`  | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                 |
| `scalex`        | The x-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                  |
| `scaley`        | The y-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                  |
| `subplots`      | Whether to draw each series unstacked in its own subplot. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                   |
| `max_cols`      | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                  |
| `sharex`        | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                    |
| `sharey`        | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                    |
| `style`         | Style configuration(s) for the band(s). **TYPE:** \`StackedAreaStyleAttrs                                                                                                                                                                                                                                                                                                                                                    |
| `xticks`        | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                          |
| `xticklabels`   | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                             |
| `xtickrotate`   | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                       |
| `yticks`        | Custom y-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                          |
| `yticklabels`   | Custom y-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                             |
| `ytickrotate`   | Rotation angle for y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                       |
| `xticks_format` | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                    |
| `yticks_format` | The y-axis tick label format, as xticks_format. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                     |
| `vlines`        | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                      |
| `hlines`        | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                    |
| `vspans`        | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                  |
| `hspans`        | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                |
| `texts`         | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                     |
| `x`             | The key name in data for x-axis values (default: "x"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                       |
| `y`             | The key name in data for y-axis values (default: "y"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                       |

| RETURNS      | DESCRIPTION                                   |
| ------------ | --------------------------------------------- |
| `plt.Figure` | The figure containing the stacked area chart. |

| RAISES       | DESCRIPTION                                                                                     |
| ------------ | ----------------------------------------------------------------------------------------------- |
| `ValueError` | If the series do not share the same x values, or baseline is not a STACKED_AREA_BASELINE value. |

## Data

Each record in `data` is a [`LineDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/linechart/#datachart.typings.LineDataPointAttrs); the `x` and `y` parameters rename its keys.

## Style

`style` takes the keys of [`StackedAreaStyleAttrs`](#datachart.typings.StackedAreaStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.StackedAreaStyleAttrs

Bases: `TypedDict`

The typing for the stacked area chart style.

The fill takes the `plot_area_*` keys (color, hatch, zorder) and the outline the `plot_line_*` keys; these keys switch what is specific to a stack.

| ATTRIBUTE                     | DESCRIPTION                                                      |
| ----------------------------- | ---------------------------------------------------------------- |
| `plot_stackedarea_alpha`      | The alpha value of the stacked bands. **TYPE:** \`float          |
| `plot_stackedarea_outline`    | Whether each band draws its top edge as a line. **TYPE:** \`bool |
| `plot_stackedarea_edge_color` | The stroke color between the bands. **TYPE:** \`str              |
| `plot_stackedarea_edge_width` | The stroke width between the bands. **TYPE:** \`float            |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `baseline`                                   | [`STACKED_AREA_BASELINE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.STACKED_AREA_BASELINE)                                                                                                         |
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
