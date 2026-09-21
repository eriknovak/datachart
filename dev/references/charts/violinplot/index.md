# ViolinPlot

The density profile of each group's distribution. The [Violin Plot guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/violinplot/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.ViolinPlot

```
ViolinPlot(
    data: (
        list[ViolinDataPointAttrs]
        | list[list[ViolinDataPointAttrs]]
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
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    orientation: (
        ORIENTATION | str | None
    ) = ORIENTATION.VERTICAL,
    sort: SORT | str | None = None,
    scaley: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        ViolinStyleAttrs
        | list[ViolinStyleAttrs | None]
        | None
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
    value: str | list[str | None] | None = None,
    inner: VIOLIN_INNER | str | None = VIOLIN_INNER.BOX,
    bandwidth: BANDWIDTH | str | float | None = None,
    split: str | None = None
) -> plt.Figure
```

Creates the violin plot.

A violin plot draws the kernel density estimate of each group's numeric distribution as a mirrored profile, showing shape (multimodality, skew, tails) that a box plot hides. Use it to compare distributions across groups when shape matters and each group has enough samples for a density estimate.

Examples:

```
>>> from datachart.charts import ViolinPlot
>>> figure = ViolinPlot(
...     data=[
...         {"label": "Group A", "value": 10},
...         {"label": "Group A", "value": 15},
...         {"label": "Group A", "value": 12},
...         {"label": "Group B", "value": 20},
...         {"label": "Group B", "value": 25},
...         {"label": "Group B", "value": 22},
...     ],
...     title="Basic Violin Plot",
...     xlabel="Group",
...     ylabel="Value"
... )
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The data points for the violin plot(s). Can be a single list of data points for one chart, or a list of lists for subplots (requires subplots=True). Each data point should have a label (category) and value (numeric). **TYPE:** \`list[ViolinDataPointAttrs]                                                                                                                                                                     |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                             |
| `xlabel`        | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                   |
| `ylabel`        | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                   |
| `subtitle`      | The subtitle(s) for individual charts: the subplot title and the legend label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                      |
| `emphasis`      | The emphasis role(s), aligned with the violin labels of one call in input order, whatever the sort (a single value applies to every violin): "background" mutes a violin body and its inner marks, "highlight" bolds the body edge, None leaves it unchanged. **TYPE:** \`EMPHASIS                                                                                                                                                  |
| `emphasis_rule` | A rule that highlights the groups matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against a summary of each group's values, chosen by by: "median" (default), "mean", "min", "max", or "sum". An explicit emphasis role wins, and a count ranks across every group of every chart. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`       | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                        |
| `xmin`          | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `xmax`          | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymin`          | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymax`          | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `show_legend`   | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                        |
| `legend`        | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                              |
| `show_grid`     | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                          |
| `show_values`   | Whether to print each group's median beside its median line. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                       |
| `value_format`  | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                             |
| `aspect_ratio`  | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                        |
| `orientation`   | The orientation of the violins (vertical or horizontal). **TYPE:** \`ORIENTATION                                                                                                                                                                                                                                                                                                                                                    |
| `sort`          | The order the groups are drawn in: None (input order), "ascending", or "descending" by each group's median; ties keep input order. One call draws one violin dataset per axes, so there is no second series to key on and no sort_by. See SORT. **TYPE:** \`SORT                                                                                                                                                                    |
| `scaley`        | The y-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                         |
| `subplots`      | Whether to create separate subplots for each chart; required for a list of datasets. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                               |
| `max_cols`      | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                         |
| `sharex`        | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                           |
| `sharey`        | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                           |
| `style`         | Style configuration(s) for the violin(s). **TYPE:** \`ViolinStyleAttrs                                                                                                                                                                                                                                                                                                                                                              |
| `xticks`        | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                 |
| `xticklabels`   | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                    |
| `xtickrotate`   | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                              |
| `yticks`        | Custom y-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                 |
| `yticklabels`   | Custom y-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                    |
| `ytickrotate`   | Rotation angle for y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                              |
| `xticks_format` | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                           |
| `yticks_format` | The y-axis tick label format, as xticks_format. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                            |
| `vlines`        | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                             |
| `hlines`        | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                           |
| `dlines`        | Diagonal line(s) to plot, by slope and intercept. **TYPE:** \`DLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                     |
| `vspans`        | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                         |
| `hspans`        | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                       |
| `texts`         | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                            |
| `label`         | The key name in data for label/category values (default: "label"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                  |
| `value`         | The key name in data for numeric values (default: "value"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                         |
| `inner`         | The marks drawn inside each body: "box" (quartile bar, 1.5·IQR whisker, median dot), "quartiles" (dashed median, dotted Q1/Q3), "median" (one line), or None (body only). See VIOLIN_INNER. **TYPE:** \`VIOLIN_INNER                                                                                                                                                                                                                |
| `bandwidth`     | The KDE bandwidth: None or "scott" (Scott's rule), "silverman", or a scalar factor. See BANDWIDTH. **TYPE:** \`BANDWIDTH                                                                                                                                                                                                                                                                                                            |
| `split`         | The key name in data whose exactly two distinct values become the left and right halves of each violin, colored from the multiple palette and listed in the legend. **TYPE:** \`str                                                                                                                                                                                                                                                 |

| RETURNS      | DESCRIPTION                            |
| ------------ | -------------------------------------- |
| `plt.Figure` | The figure containing the violin plot. |

## Data

Each record in `data` is a [`ViolinDataPointAttrs`](#datachart.typings.ViolinDataPointAttrs); the `label` and `value` parameters rename its keys.

### datachart.typings.ViolinDataPointAttrs

Bases: `TypedDict`

The data point attributes for the violin plot.

| ATTRIBUTE | DESCRIPTION                         |
| --------- | ----------------------------------- |
| `label`   | The category label. **TYPE:** `str` |
| `value`   | The numeric value. **TYPE:** \`int  |

## Style

`style` takes the keys of [`ViolinStyleAttrs`](#datachart.typings.ViolinStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.ViolinStyleAttrs

Bases: `TypedDict`

The typing for the violin plot style.

| ATTRIBUTE                     | DESCRIPTION                                                               |
| ----------------------------- | ------------------------------------------------------------------------- |
| `plot_violin_color`           | The violin fill color. **TYPE:** \`str                                    |
| `plot_violin_alpha`           | The alpha value of the violin body. **TYPE:** \`float                     |
| `plot_violin_linewidth`       | The line width of the body edge. **TYPE:** \`int                          |
| `plot_violin_edgecolor`       | The edge color of the body; defaults to the fill. **TYPE:** \`str         |
| `plot_violin_width`           | The maximum width of the body. **TYPE:** \`int                            |
| `plot_violin_inner_color`     | The color of the inner marks; defaults to the font color. **TYPE:** \`str |
| `plot_violin_inner_linewidth` | The line width of the inner marks. **TYPE:** \`int                        |
| `plot_violin_median_color`    | The color of the median dot. **TYPE:** \`str                              |
| `plot_violin_median_size`     | The size of the median dot. **TYPE:** \`int                               |
| `plot_violin_hatch`           | The hatch pattern of the body. **TYPE:** \`HATCH_STYLE                    |

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
| `sort`                                       | [`SORT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SORT)                                                                                                                                           |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE)                                                                                                                                         |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
| `inner`                                      | [`VIOLIN_INNER`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VIOLIN_INNER)                                                                                                                           |
| `bandwidth`                                  | [`BANDWIDTH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.BANDWIDTH)                                                                                                                                 |
