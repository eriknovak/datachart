# RidgelinePlot

One density ridge per group, stacked and partly overlapping. The [Ridgeline Plot guide](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/charts/ridgelineplot/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.RidgelinePlot

```
RidgelinePlot(
    data: (
        list[RidgelineDataPointAttrs]
        | list[list[RidgelineDataPointAttrs]]
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
    aspect_ratio: ASPECT_RATIO | str | None = None,
    orientation: (
        ORIENTATION | str | None
    ) = ORIENTATION.HORIZONTAL,
    scaley: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        RidgelineStyleAttrs
        | list[RidgelineStyleAttrs | None]
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
    bandwidth: BANDWIDTH | str | float | None = None,
    overlap: float | None = None,
    normalize: (
        RIDGELINE_SCALE | str | None
    ) = RIDGELINE_SCALE.PER_ROW,
    inner: VIOLIN_INNER | str | None = None,
    fill: bool = True,
    show_outline: bool = True,
    sort: SORT | str | None = SORT.NONE
) -> plt.Figure
```

Creates the ridgeline plot.

A ridgeline plot (joy plot) draws the kernel density estimate of each group's numeric distribution as a ridge on its own row, the rows stacked and partly overlapping, first row at the top. Use it to show how one distribution shifts across many groups in the space a grid of histograms would spend on a few.

Examples:

```
>>> from datachart.charts import RidgelinePlot
>>> figure = RidgelinePlot(
...     data=[
...         {"label": "Group A", "value": 10},
...         {"label": "Group A", "value": 15},
...         {"label": "Group A", "value": 12},
...         {"label": "Group B", "value": 20},
...         {"label": "Group B", "value": 25},
...         {"label": "Group B", "value": 22},
...     ],
...     title="Basic Ridgeline Plot",
...     xlabel="Value",
...     ylabel="Group"
... )
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The data points for the ridgeline plot(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. Each data point should have a label (category) and value (numeric). **TYPE:** \`list[RidgelineDataPointAttrs]                                                                                                                                                                        |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                             |
| `xlabel`        | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                   |
| `ylabel`        | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                   |
| `subtitle`      | The subtitle(s) for individual charts (subplots). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                   |
| `emphasis`      | The emphasis role(s), aligned with the ridge labels of one call in input order (a single value applies to every ridge): "background" mutes a ridge and its inner marks, "highlight" bolds its outline, None leaves it unchanged. **TYPE:** \`EMPHASIS                                                                                                                                                                               |
| `emphasis_rule` | A rule that highlights the groups matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against a summary of each group's values, chosen by by: "median" (default), "mean", "min", "max", or "sum". An explicit emphasis role wins, and a count ranks across every group of every chart. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`       | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                        |
| `xmin`          | The minimum x-axis value; on the value axis it also bounds the density grid. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                        |
| `xmax`          | The maximum x-axis value; on the value axis it also bounds the density grid. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                        |
| `ymin`          | The minimum y-axis value; bounds the grid when vertical. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                            |
| `ymax`          | The maximum y-axis value; bounds the grid when vertical. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                            |
| `show_legend`   | Whether to show the legend; the ridges add no entries, their labels sit on the category axis. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                      |
| `legend`        | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                              |
| `show_grid`     | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                          |
| `aspect_ratio`  | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                        |
| `orientation`   | "horizontal" (default) runs the value axis along x and stacks the rows along y, first row at the top; "vertical" runs the rows along x, first row at the left, each ridge rising rightward from its tick. See ORIENTATION. **TYPE:** \`ORIENTATION                                                                                                                                                                                  |
| `scaley`        | The value-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                     |
| `subplots`      | Whether to create separate subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                |
| `max_cols`      | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                         |
| `sharex`        | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                           |
| `sharey`        | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                           |
| `style`         | Style configuration(s) for the ridges. **TYPE:** \`RidgelineStyleAttrs                                                                                                                                                                                                                                                                                                                                                              |
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
| `vspans`        | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                         |
| `hspans`        | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                       |
| `texts`         | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                            |
| `label`         | The key name in data for label/category values (default: "label"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                  |
| `value`         | The key name in data for numeric values (default: "value"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                         |
| `bandwidth`     | The KDE bandwidth: None or "scott" (Scott's rule), "silverman", or a scalar factor. See BANDWIDTH. **TYPE:** \`BANDWIDTH                                                                                                                                                                                                                                                                                                            |
| `overlap`       | How far a ridge's peak rises into the row above, in \[0, 1\]: a ridge rises from its tick and its peak stands 1 + overlap rows above it, so 0 makes rows touch. None takes the theme's plot_ridgeline_overlap. **TYPE:** \`float                                                                                                                                                                                                    |
| `normalize`     | "per_row" scales every ridge to the same peak so shapes compare; "common" keeps one density scale so heights compare. See RIDGELINE_SCALE. **TYPE:** \`RIDGELINE_SCALE                                                                                                                                                                                                                                                              |
| `inner`         | The marks drawn inside each ridge, up to its height: "median" (one line), "quartiles" (dashed median, dotted Q1/Q3), or None. See VIOLIN_INNER; "box" is not supported. **TYPE:** \`VIOLIN_INNER                                                                                                                                                                                                                                    |
| `fill`          | Whether to fill each ridge. **TYPE:** `bool` **DEFAULT:** `True`                                                                                                                                                                                                                                                                                                                                                                    |
| `show_outline`  | Whether to stroke each ridge's density curve. **TYPE:** `bool` **DEFAULT:** `True`                                                                                                                                                                                                                                                                                                                                                  |
| `sort`          | The row order: None keeps input order, "ascending" or "descending" orders the rows by their median; ties keep input order. See SORT. **TYPE:** \`SORT                                                                                                                                                                                                                                                                               |

| RETURNS      | DESCRIPTION                               |
| ------------ | ----------------------------------------- |
| `plt.Figure` | The figure containing the ridgeline plot. |

| RAISES       | DESCRIPTION                                                                            |
| ------------ | -------------------------------------------------------------------------------------- |
| `ValueError` | If overlap is outside [0, 1], inner is "box", or both fill and show_outline are False. |

## Data

Each record in `data` is a [`RidgelineDataPointAttrs`](#datachart.typings.RidgelineDataPointAttrs); the `label` and `value` parameters rename its keys.

### datachart.typings.RidgelineDataPointAttrs

Bases: `TypedDict`

The data point attributes for the ridgeline plot.

| ATTRIBUTE | DESCRIPTION                                              |
| --------- | -------------------------------------------------------- |
| `label`   | The category label; one ridge per label. **TYPE:** `str` |
| `value`   | The numeric value. **TYPE:** \`int                       |

## Style

`style` takes the keys of [`RidgelineStyleAttrs`](#datachart.typings.RidgelineStyleAttrs). The chart also reads the shared groups it draws: reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/0.10.2/references/config/index.md).

### datachart.typings.RidgelineStyleAttrs

Bases: `TypedDict`

The typing for the ridgeline plot style.

| ATTRIBUTE                        | DESCRIPTION                                                               |
| -------------------------------- | ------------------------------------------------------------------------- |
| `plot_ridgeline_color`           | The ridge fill color; defaults to the palette color. **TYPE:** \`str      |
| `plot_ridgeline_alpha`           | The alpha value of the ridge fill. **TYPE:** \`float                      |
| `plot_ridgeline_linewidth`       | The line width of the ridge outline. **TYPE:** \`int                      |
| `plot_ridgeline_edgecolor`       | The color of the ridge outline; defaults to the fill. **TYPE:** \`str     |
| `plot_ridgeline_overlap`         | How far a peak rises into the row above, in [0, 1]. **TYPE:** \`float     |
| `plot_ridgeline_inner_color`     | The color of the inner marks; defaults to the font color. **TYPE:** \`str |
| `plot_ridgeline_inner_linewidth` | The line width of the inner marks. **TYPE:** \`int                        |
| `plot_ridgeline_hatch`           | The hatch pattern of the ridge fill. **TYPE:** \`HATCH_STYLE              |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.2/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `normalize`                                  | [`RIDGELINE_SCALE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.RIDGELINE_SCALE)                                                                                                                        |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                      |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                      |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                    |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                              |
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.ORIENTATION)                                                                                                                                |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.DATE_FORMAT)         |
| `bandwidth`                                  | [`BANDWIDTH`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.BANDWIDTH)                                                                                                                                    |
| `inner`                                      | [`VIOLIN_INNER`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VIOLIN_INNER)                                                                                                                              |
| `sort`                                       | [`SORT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SORT)                                                                                                                                              |
