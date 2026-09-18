# ScatterChart

One point per observation, placed by two numeric variables. The [Scatter Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.ScatterChart

```
ScatterChart(
    data: (
        list[ScatterDataPointAttrs]
        | list[list[ScatterDataPointAttrs]]
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
    show_regression: bool | None = None,
    show_ci: bool | None = None,
    ci_level: float | None = None,
    show_correlation: bool | None = None,
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
        ScatterStyleAttrs
        | list[ScatterStyleAttrs | None]
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
    y: str | list[str | None] | None = None,
    size: str | list[str | None] | None = None,
    hue: str | list[str | None] | None = None,
    label: str | list[str | None] | None = None,
    size_range: tuple[float, float] | None = None
) -> plt.Figure
```

Creates a scatter chart.

Each point is one observation placed by two numeric variables, optionally with a third encoded as marker size. Use it to check whether two variables are related, spot clusters and outliers, and quantify the link with the optional regression line and correlation coefficient. For ordered series use LineChart.

Examples:

```
>>> from datachart.charts import ScatterChart
>>> # Basic scatter plot
>>> figure = ScatterChart(
...     data=[
...         {"x": 1, "y": 5},
...         {"x": 2, "y": 10},
...         {"x": 3, "y": 15},
...         {"x": 4, "y": 20},
...         {"x": 5, "y": 25}
...     ],
...     title="Basic Scatter Chart",
...     xlabel="X",
...     ylabel="Y"
... )
>>>
>>> # Scatter with hue grouping
>>> figure = ScatterChart(
...     data=[
...         {"x": 1, "y": 5, "category": "A"},
...         {"x": 2, "y": 10, "category": "B"},
...     ],
...     hue="category",
...     show_legend=True
... )
>>>
>>> # Bubble chart with size variable
>>> figure = ScatterChart(
...     data=[
...         {"x": 1, "y": 5, "pop": 100},
...         {"x": 2, "y": 10, "pop": 200}
...     ],
...     size="pop",
...     size_range=(20, 200)
... )
>>>
>>> # Scatter with regression line
>>> figure = ScatterChart(
...     data=[...],
...     show_regression=True,
...     show_ci=True,
...     ci_level=0.95
... )
>>>
>>> # Scatter with correlation annotation
>>> figure = ScatterChart(
...     data=[...],
...     show_correlation=True
... )
>>>
>>> # Scatter with a label beside each point
>>> figure = ScatterChart(
...     data=[
...         {"x": 1, "y": 5, "name": "A"},
...         {"x": 2, "y": 10, "name": "B"}
...     ],
...     label="name"
... )
```

| PARAMETER          | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`             | The data points for the scatter chart(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. A point may carry its own emphasis role, which wins over its chart's. **TYPE:** \`list[ScatterDataPointAttrs]                                                                                                                                                                  |
| `title`            | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                      |
| `xlabel`           | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                            |
| `ylabel`           | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                            |
| `subtitle`         | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                |
| `emphasis`         | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, behind the others, no legend entry), "highlight" gives it a contrasting edge and brings it to the front, None leaves it unchanged. **TYPE:** \`EMPHASIS                                                                                                                                        |
| `emphasis_rule`    | A rule that highlights the series matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against a summary of each series's own y values, chosen by by: "mean" (default), "median", "min", "max", or "sum". An explicit emphasis role wins, and a count ranks across every series. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`          | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                 |
| `xmin`             | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                    |
| `xmax`             | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                    |
| `ymin`             | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                    |
| `ymax`             | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                    |
| `show_legend`      | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                 |
| `legend`           | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                       |
| `show_grid`        | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                   |
| `show_regression`  | Whether to show the regression line. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                        |
| `show_ci`          | Whether to show the confidence interval around the regression line. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                         |
| `ci_level`         | The confidence interval level (default 0.95). **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                              |
| `show_correlation` | Whether to show the Pearson correlation coefficient (r-value) as an annotation. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                             |
| `show_values`      | Whether to print each point's y value beside it. Cannot be combined with label: a point carries its label or its value. **TYPE:** \`bool                                                                                                                                                                                                                                                                                     |
| `value_format`     | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                      |
| `value_step`       | Label every Nth point (1 labels all of them). Defaults to the smallest step that keeps neighbouring labels apart. **TYPE:** \`int                                                                                                                                                                                                                                                                                            |
| `aspect_ratio`     | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                 |
| `scalex`           | The x-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                  |
| `scaley`           | The y-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                  |
| `subplots`         | Whether to create separate subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                         |
| `max_cols`         | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                  |
| `sharex`           | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                    |
| `sharey`           | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                    |
| `style`            | Style configuration(s) for the scatter markers. **TYPE:** \`ScatterStyleAttrs                                                                                                                                                                                                                                                                                                                                                |
| `xticks`           | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                          |
| `xticklabels`      | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                             |
| `xtickrotate`      | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                       |
| `yticks`           | Custom y-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                          |
| `yticklabels`      | Custom y-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                             |
| `ytickrotate`      | Rotation angle for y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                       |
| `xticks_format`    | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                    |
| `yticks_format`    | The y-axis tick label format, as xticks_format. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                     |
| `vlines`           | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                      |
| `hlines`           | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                    |
| `vspans`           | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                  |
| `hspans`           | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                |
| `texts`            | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                     |
| `x`                | The key name in data for x-axis values (default: "x"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                       |
| `y`                | The key name in data for y-axis values (default: "y"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                       |
| `size`             | The key name in data for marker size values (for bubble charts). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                             |
| `hue`              | The key name in data for color grouping (categorical variable). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                              |
| `label`            | The key name in data for the point labels (default: "label"), aligned like style for multiple charts; None in the list leaves that chart unlabelled. Each label is drawn beside its marker at the spot with the least overlap against the other markers, labels, and the axes edge; points without the key stay unlabelled. **TYPE:** \`str                                                                                  |
| `size_range`       | Tuple of (min_size, max_size) for bubble charts (default: (20, 200)). **TYPE:** \`tuple[float, float]                                                                                                                                                                                                                                                                                                                        |

| RETURNS      | DESCRIPTION                              |
| ------------ | ---------------------------------------- |
| `plt.Figure` | The figure containing the scatter chart. |

## Data

Each record in `data` is a [`ScatterDataPointAttrs`](#datachart.typings.ScatterDataPointAttrs); the `x`, `y`, `size`, `hue` and `label` parameters rename its keys.

### datachart.typings.ScatterDataPointAttrs

Bases: `TypedDict`

The data point attributes for the scatter chart.

| ATTRIBUTE  | DESCRIPTION                                                                                                                         |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `x`        | The x-axis value. **TYPE:** \`int                                                                                                   |
| `y`        | The y-axis value. **TYPE:** \`int                                                                                                   |
| `size`     | The marker size (for bubble charts). **TYPE:** \`int                                                                                |
| `hue`      | The category for color grouping. **TYPE:** \`str                                                                                    |
| `label`    | The label drawn beside the point. **TYPE:** \`str                                                                                   |
| `emphasis` | The point's own emphasis role ("background" or "highlight"); wins over the chart's emphasis and emphasis_rule. **TYPE:** \`EMPHASIS |

## Style

`style` takes the keys of [`ScatterStyleAttrs`](#datachart.typings.ScatterStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)), the regression line ([`RegressionStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.RegressionStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.ScatterStyleAttrs

Bases: `TypedDict`

The typing for the scatter chart style.

| ATTRIBUTE                 | DESCRIPTION                                       |
| ------------------------- | ------------------------------------------------- |
| `plot_scatter_color`      | The scatter marker color. **TYPE:** \`str         |
| `plot_scatter_alpha`      | The alpha value of the markers. **TYPE:** \`float |
| `plot_scatter_size`       | The marker size. **TYPE:** \`int                  |
| `plot_scatter_marker`     | The marker shape. **TYPE:** \`LINE_MARKER         |
| `plot_scatter_zorder`     | The zorder of the scatter. **TYPE:** \`int        |
| `plot_scatter_edge_width` | The edge width of markers. **TYPE:** \`int        |
| `plot_scatter_edge_color` | The edge color of markers. **TYPE:** \`str        |

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
