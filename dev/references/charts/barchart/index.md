# BarChart

A value per category as bars; series grouped, stacked, or overlaid. The [Bar Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/barchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.BarChart

```
BarChart(
    data: (
        list[BarDataPointAttrs]
        | list[list[BarDataPointAttrs]]
    ),
    *,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    subtitle: str | list[str | None] | None = None,
    emphasis: (
        EMPHASIS | str | list[str | None] | None
    ) = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    xmin: int | float | None = None,
    xmax: int | float | None = None,
    ymin: int | float | None = None,
    ymax: int | float | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_yerr: bool | None = None,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    orientation: (
        ORIENTATION | str | None
    ) = ORIENTATION.VERTICAL,
    bar_mode: BAR_MODE | str | None = None,
    sort: SORT | str | None = None,
    sort_by: str | None = None,
    emphasis_rule: EmphasisRuleAttrs | None = None,
    scalex: SCALE | str | None = None,
    scaley: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        BarStyleAttrs | list[BarStyleAttrs | None] | None
    ) = None,
    xticks: (
        list[int | float] | list[list[int | float]] | None
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
    label: str | list[str | None] | None = None,
    y: str | list[str | None] | None = None,
    yerr: str | list[str | None] | None = None
) -> plt.Figure
```

Creates the bar chart.

Bars compare a numeric value across discrete categories: each label gets a bar whose length encodes its value. Use it when the categories are few and unordered (or ordinal) and the question is "which is bigger, and by how much"; several series can be grouped, stacked, or overlaid via `bar_mode`. For a continuous x-axis reach for LineChart, for distributions for Histogram.

Examples:

```
>>> from datachart.charts import BarChart
>>> figure = BarChart(
...     data=[
...         {"label": "cat1", "y": 5},
...         {"label": "cat2", "y": 10},
...         {"label": "cat3", "y": 15},
...         {"label": "cat4", "y": 20},
...         {"label": "cat5", "y": 25}
...     ],
...     title="Basic Bar Chart",
...     xlabel="LABEL",
...     ylabel="Y"
... )
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                     |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The data points for the bar chart(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. **TYPE:** \`list[BarDataPointAttrs]                                                                                                                                   |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                         |
| `xlabel`        | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                               |
| `ylabel`        | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                               |
| `subtitle`      | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** \`str                                                                                                                                                                                                                                   |
| `emphasis`      | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, behind the others, no legend entry), "highlight" bolds its edges and brings it to the front, None leaves it unchanged. See EMPHASIS. **TYPE:** \`EMPHASIS                         |
| `figsize`       | The size of the figure as (width, height) in inches. See FIG_SIZE. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                         |
| `xmin`          | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                       |
| `xmax`          | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                       |
| `ymin`          | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                       |
| `ymax`          | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                       |
| `show_legend`   | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                    |
| `legend`        | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                          |
| `show_grid`     | Which grid lines to show ("both", "x", "y"); False draws none. See SHOW_GRID. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                             |
| `show_yerr`     | Whether to show y-axis error bars. **TYPE:** \`bool                                                                                                                                                                                                                                                             |
| `show_values`   | Whether to show bar value labels at the edge of each bar. **TYPE:** \`bool                                                                                                                                                                                                                                      |
| `value_format`  | Format string for bar value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                         |
| `aspect_ratio`  | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                    |
| `bar_mode`      | How multiple bar series share the axis: "group" (side-by-side), "stack" (stacked), or "overlay" (overlapping). See BAR_MODE. **TYPE:** \`BAR_MODE                                                                                                                                                               |
| `sort`          | The order the categories are drawn in: None (input order), "ascending", or "descending" by value. One order serves every series, keyed by the total across them; ties keep input order. See SORT. **TYPE:** \`SORT                                                                                              |
| `sort_by`       | The subtitle of the one series whose values key the sort instead of the total. A category that series lacks sorts last. **TYPE:** \`str                                                                                                                                                                         |
| `emphasis_rule` | A one-key dict that highlights the bars matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}. Reads each bar's own value; a record's own emphasis key wins over the rule. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `orientation`   | The orientation of the bars ("vertical" or "horizontal"). See ORIENTATION. **TYPE:** \`ORIENTATION                                                                                                                                                                                                              |
| `scalex`        | The x-axis scale ("linear", "log", "symlog", "asinh"). Useful for horizontal bars. See SCALE. **TYPE:** \`SCALE                                                                                                                                                                                                 |
| `scaley`        | The y-axis scale ("linear", "log", "symlog", "asinh"). Useful for vertical bars. See SCALE. **TYPE:** \`SCALE                                                                                                                                                                                                   |
| `subplots`      | Whether to create separate subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                            |
| `max_cols`      | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                     |
| `sharex`        | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                       |
| `sharey`        | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                       |
| `style`         | Style configuration(s) for the bar(s). **TYPE:** \`BarStyleAttrs                                                                                                                                                                                                                                                |
| `xticks`        | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                             |
| `xticklabels`   | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                |
| `xtickrotate`   | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                          |
| `yticks`        | Custom y-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                             |
| `yticklabels`   | Custom y-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                |
| `ytickrotate`   | Rotation angle for y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                          |
| `xticks_format` | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                       |
| `yticks_format` | The y-axis tick label format, as xticks_format. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                        |
| `vlines`        | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                         |
| `hlines`        | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                       |
| `dlines`        | Diagonal line(s) to plot, by slope and intercept. **TYPE:** \`DLineSettingAttrs                                                                                                                                                                                                                                 |
| `vspans`        | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                     |
| `hspans`        | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                   |
| `texts`         | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                        |
| `label`         | The key name in data for label values (default: "label"). **TYPE:** \`str                                                                                                                                                                                                                                       |
| `y`             | The key name in data for y-axis values (default: "y"). **TYPE:** \`str                                                                                                                                                                                                                                          |
| `yerr`          | The key name in data for y-axis error values (default: "yerr"). **TYPE:** \`str                                                                                                                                                                                                                                 |

| RETURNS      | DESCRIPTION                          |
| ------------ | ------------------------------------ |
| `plt.Figure` | The figure containing the bar chart. |

## Data

Each record in `data` is a [`BarDataPointAttrs`](#datachart.typings.BarDataPointAttrs); the `emphasis`, `label`, `y` and `yerr` parameters rename its keys.

### datachart.typings.BarDataPointAttrs

Bases: `TypedDict`

The data point attributes for the bar chart.

| ATTRIBUTE  | DESCRIPTION                                                                                                          |
| ---------- | -------------------------------------------------------------------------------------------------------------------- |
| `label`    | The label. **TYPE:** `str`                                                                                           |
| `y`        | The y-axis value. **TYPE:** \`int                                                                                    |
| `yerr`     | The y-axis error value. **TYPE:** \`int                                                                              |
| `emphasis` | The bar's own emphasis role ("background" or "highlight"); wins over the chart's emphasis_rule. **TYPE:** \`EMPHASIS |

## Style

`style` takes the keys of [`BarStyleAttrs`](#datachart.typings.BarStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.BarStyleAttrs

Bases: `TypedDict`

The typing for the bar chart style.

| ATTRIBUTE                  | DESCRIPTION                                                        |
| -------------------------- | ------------------------------------------------------------------ |
| `plot_bar_color`           | The bar color. **TYPE:** \`str                                     |
| `plot_bar_alpha`           | The alpha value of the bar. **TYPE:** \`float                      |
| `plot_bar_width`           | The width of the bar. **TYPE:** \`int                              |
| `plot_bar_zorder`          | The zorder of the bar. **TYPE:** \`int                             |
| `plot_bar_hatch`           | The hatch style of the bar. **TYPE:** \`HATCH_STYLE                |
| `plot_bar_edge_width`      | The edge width of the bar. **TYPE:** \`int                         |
| `plot_bar_edge_color`      | The edge color of the bar. **TYPE:** \`str                         |
| `plot_bar_error_color`     | The color of the error line of the bar. **TYPE:** \`str            |
| `plot_bar_value_fontsize`  | Alias of plot_value_fontsize. **TYPE:** \`int                      |
| `plot_bar_value_color`     | Alias of plot_value_color. **TYPE:** \`str                         |
| `plot_bar_value_padding`   | Alias of plot_value_padding. **TYPE:** \`int                       |
| `plot_xticks_label_rotate` | The label rotation of the xticks in the bar chart. **TYPE:** \`int |
| `plot_yticks_label_rotate` | The label rotation of the yticks in the bar chart. **TYPE:** \`int |

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
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION)                                                                                                                             |
| `bar_mode`                                   | [`BAR_MODE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.BAR_MODE)                                                                                                                                   |
| `sort`                                       | [`SORT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SORT)                                                                                                                                           |
| `scalex`                                     | [`SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE)                                                                                                                                         |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE)                                                                                                                                         |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
