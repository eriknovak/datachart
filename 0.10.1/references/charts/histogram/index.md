# Histogram

The distribution of one numeric variable, binned. The [Histogram guide](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/charts/histogram/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.Histogram

```
Histogram(
    data: (
        list[HistDataPointAttrs]
        | list[list[HistDataPointAttrs]]
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
    xmin: int | float | None = None,
    xmax: int | float | None = None,
    ymin: int | float | None = None,
    ymax: int | float | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_density: bool | None = None,
    show_cumulative: bool | None = None,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    orientation: (
        ORIENTATION | str | None
    ) = ORIENTATION.VERTICAL,
    bar_mode: BAR_MODE | str | None = None,
    num_bins: int | None = None,
    scalex: SCALE | str | None = None,
    scaley: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        HistStyleAttrs | list[HistStyleAttrs | None] | None
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
    x: str | list[str | None] | None = None
) -> plt.Figure
```

Creates the histogram.

A histogram bins a single numeric variable and draws the count (or density) per bin, revealing the shape of its distribution: center, spread, skew, modes, and outliers. Use it to inspect one variable or compare a few overlaid distributions. For side-by-side group summaries use BoxPlot or ViolinPlot.

Examples:

```
>>> from datachart.charts import Histogram
>>> figure = Histogram(
...     data=[
...         {"x": 1},
...         {"x": 2},
...         {"x": 3},
...         {"x": 4},
...         {"x": 5}
...     ],
...     title="Basic Histogram",
...     xlabel="X",
...     ylabel="Y"
... )
```

| PARAMETER         | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`            | The data points for the histogram(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. **TYPE:** \`list[HistDataPointAttrs]                                                                                                                                                                                                                                                         |
| `title`           | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                |
| `xlabel`          | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                      |
| `ylabel`          | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                      |
| `subtitle`        | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                          |
| `emphasis`        | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, behind the others, no legend entry), "highlight" bolds it and brings it to the front, None leaves it unchanged. When any chart carries a role, the histograms draw individually overlaid instead of stacked. **TYPE:** \`EMPHASIS                                                                        |
| `emphasis_rule`   | A rule that highlights the histograms matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against a summary of each histogram's own x values, chosen by by: "mean" (default), "median", "min", "max", or "sum". An explicit emphasis role wins, and a count ranks across every histogram. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`         | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                           |
| `xmin`            | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                              |
| `xmax`            | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                              |
| `ymin`            | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                              |
| `ymax`            | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                              |
| `show_legend`     | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                           |
| `legend`          | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                                 |
| `show_grid`       | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                             |
| `show_density`    | Whether to plot the density histogram. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                |
| `show_cumulative` | Whether to plot the cumulative histogram. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                             |
| `show_values`     | Whether to print each bin's height at its top; empty bins stay bare. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                  |
| `value_format`    | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                |
| `aspect_ratio`    | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                           |
| `orientation`     | The orientation of the histogram (vertical or horizontal). **TYPE:** \`ORIENTATION                                                                                                                                                                                                                                                                                                                                                     |
| `bar_mode`        | How multiple histogram series share the axis: "stack" (stacked on shared bins, the default) or "overlay" (each series drawn individually over the others). "group" has no histogram meaning and behaves like "overlay". See BAR_MODE. **TYPE:** \`BAR_MODE                                                                                                                                                                             |
| `num_bins`        | The number of bins to split the data into. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                             |
| `scalex`          | The x-axis scale (e.g., "log", "linear"). Useful for log-distributed data. **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                           |
| `scaley`          | The y-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                            |
| `subplots`        | Whether to create separate subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                   |
| `max_cols`        | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                            |
| `sharex`          | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                              |
| `sharey`          | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                              |
| `style`           | Style configuration(s) for the histogram(s). **TYPE:** \`HistStyleAttrs                                                                                                                                                                                                                                                                                                                                                                |
| `xticks`          | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                    |
| `xticklabels`     | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                       |
| `xtickrotate`     | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                 |
| `yticks`          | Custom y-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                    |
| `yticklabels`     | Custom y-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                       |
| `ytickrotate`     | Rotation angle for y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                 |
| `vlines`          | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                |
| `hlines`          | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                              |
| `vspans`          | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                            |
| `hspans`          | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                          |
| `texts`           | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                               |
| `x`               | The key name in data for x-axis values (default: "x"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                 |

| RETURNS      | DESCRIPTION                          |
| ------------ | ------------------------------------ |
| `plt.Figure` | The figure containing the histogram. |

## Data

Each record in `data` is a [`HistDataPointAttrs`](#datachart.typings.HistDataPointAttrs); the `x` parameter renames its keys.

### datachart.typings.HistDataPointAttrs

Bases: `TypedDict`

The data point attributes for the histogram chart.

| ATTRIBUTE | DESCRIPTION                       |
| --------- | --------------------------------- |
| `x`       | The x-axis value. **TYPE:** \`int |

## Style

`style` takes the keys of [`HistStyleAttrs`](#datachart.typings.HistStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/0.10.1/references/config/index.md).

### datachart.typings.HistStyleAttrs

Bases: `TypedDict`

The typing for the histogram chart style.

| ATTRIBUTE                  | DESCRIPTION                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `plot_hist_color`          | The color of the histogram. **TYPE:** \`str                              |
| `plot_hist_alpha`          | The alpha value of the histogram. **TYPE:** \`float                      |
| `plot_hist_zorder`         | The zorder of the histogram. **TYPE:** \`int                             |
| `plot_hist_fill`           | The fill of the histogram. **TYPE:** \`str                               |
| `plot_hist_hatch`          | The hatch style in the histogram. **TYPE:** \`HATCH_STYLE                |
| `plot_hist_type`           | The type of the histogram. **TYPE:** \`HISTOGRAM_TYPE                    |
| `plot_hist_align`          | The alignment of the histogram. **TYPE:** \`str                          |
| `plot_hist_edge_width`     | The edge width of the histogram. **TYPE:** \`int                         |
| `plot_hist_edge_color`     | The edge color of the histogram. **TYPE:** \`str                         |
| `plot_xticks_label_rotate` | The label rotation of the xticks in the histogram chart. **TYPE:** \`int |
| `plot_yticks_label_rotate` | The label rotation of the yticks in the histogram chart. **TYPE:** \`int |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.1/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `style={"plot_hist_type": ...}`              | [`HISTOGRAM_TYPE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.HISTOGRAM_TYPE)                                                                                                                          |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                      |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                      |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                    |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                              |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                              |
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.ORIENTATION)                                                                                                                                |
| `bar_mode`                                   | [`BAR_MODE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.BAR_MODE)                                                                                                                                      |
| `scalex`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
