# RaincloudPlot

A half violin, the raw points, and a box per group. The [Raincloud Plot guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/raincloudplot/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.RaincloudPlot

```
RaincloudPlot(
    data: (
        list[RaincloudDataPointAttrs]
        | list[list[RaincloudDataPointAttrs]]
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
    show_outliers: bool | None = True,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    mode: SWARM_MODE | str = SWARM_MODE.SWARM,
    jitter: float = 0.4,
    bandwidth: BANDWIDTH | str | float | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    orientation: (
        ORIENTATION | str | None
    ) = ORIENTATION.VERTICAL,
    scaley: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        RaincloudStyleAttrs
        | list[RaincloudStyleAttrs | None]
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
    value: str | list[str | None] | None = None
) -> plt.Figure
```

Creates the raincloud plot.

A raincloud plot draws each group as a cloud (a half violin of its density), its rain (the raw observations), and a box (the quartile summary) side by side at one category position, all in the group's palette color. Use it when you want the shape, the summary statistics, and the individual observations in a single view, for example when reporting experimental results per condition. Vertical rainclouds keep the cloud on the right; horizontal ones keep it above.

Examples:

```
>>> from datachart.charts import RaincloudPlot
>>> figure = RaincloudPlot(
...     data=[
...         {"label": "Group A", "value": 10},
...         {"label": "Group A", "value": 15},
...         {"label": "Group A", "value": 12},
...         {"label": "Group B", "value": 20},
...         {"label": "Group B", "value": 25},
...         {"label": "Group B", "value": 22},
...     ],
...     title="Basic Raincloud Plot",
...     xlabel="Group",
...     ylabel="Value"
... )
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The data points for the raincloud plot(s). Can be a single list of data points for one chart, or a list of lists for multiple charts (drawn as subplots). Each data point should have a label (category) and value (numeric). **TYPE:** \`list[RaincloudDataPointAttrs]                                                                                                                                                             |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                             |
| `xlabel`        | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                   |
| `ylabel`        | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                   |
| `subtitle`      | The subtitle(s) for individual charts. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                              |
| `emphasis`      | The emphasis role(s), aligned with the group labels of one call (a single value applies to every group): "background" mutes a group's cloud, rain, and box, "highlight" bolds their edges, None leaves them unchanged. **TYPE:** \`EMPHASIS                                                                                                                                                                                         |
| `emphasis_rule` | A rule that highlights the groups matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against a summary of each group's values, chosen by by: "median" (default), "mean", "min", "max", or "sum". An explicit emphasis role wins, and a count ranks across every group of every chart. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`       | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                        |
| `xmin`          | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `xmax`          | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymin`          | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymax`          | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `show_legend`   | Whether to show the legend; one entry per group. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                   |
| `legend`        | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                              |
| `show_grid`     | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                          |
| `show_outliers` | Whether the box shows outliers. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                    |
| `show_values`   | Whether to print each group's median beside its box, and its minimum and maximum beside the rain points holding them. **TYPE:** \`bool                                                                                                                                                                                                                                                                                              |
| `value_format`  | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                             |
| `mode`          | How the rain spreads across its width. See SWARM_MODE: "swarm" packs the points so none overlap; "strip" jitters them uniformly. **TYPE:** \`SWARM_MODE                                                                                                                                                                                                                                                                             |
| `jitter`        | The strip jitter width, as a fraction of the category width like SwarmPlot, scaled down to the rain's narrower cell. Only used with mode="strip". **TYPE:** `float` **DEFAULT:** `0.4`                                                                                                                                                                                                                                              |
| `bandwidth`     | The cloud's KDE bandwidth: None or "scott" (Scott's rule), "silverman" (Silverman's rule), or a scalar factor. See BANDWIDTH. **TYPE:** \`BANDWIDTH                                                                                                                                                                                                                                                                                 |
| `aspect_ratio`  | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                        |
| `orientation`   | The orientation of the rainclouds (vertical or horizontal). **TYPE:** \`ORIENTATION                                                                                                                                                                                                                                                                                                                                                 |
| `scaley`        | The y-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                         |
| `subplots`      | Whether to create separate subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                |
| `max_cols`      | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                         |
| `sharex`        | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                           |
| `sharey`        | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                           |
| `style`         | Style configuration(s); the violin keys style the cloud, the swarm keys the rain, and the box keys the box. **TYPE:** \`RaincloudStyleAttrs                                                                                                                                                                                                                                                                                         |
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

| RETURNS      | DESCRIPTION                               |
| ------------ | ----------------------------------------- |
| `plt.Figure` | The figure containing the raincloud plot. |

## Data

Each record in `data` is a [`RaincloudDataPointAttrs`](#datachart.typings.RaincloudDataPointAttrs); the `label` and `value` parameters rename its keys.

### datachart.typings.RaincloudDataPointAttrs

Bases: `TypedDict`

The data point attributes for the raincloud plot.

| ATTRIBUTE | DESCRIPTION                         |
| --------- | ----------------------------------- |
| `label`   | The category label. **TYPE:** `str` |
| `value`   | The numeric value. **TYPE:** \`int  |

## Style

`style` takes the keys of [`RaincloudStyleAttrs`](#datachart.typings.RaincloudStyleAttrs). RaincloudStyleAttrs is the union of [`ViolinStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/violinplot/#datachart.typings.ViolinStyleAttrs), [`SwarmStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/#datachart.typings.SwarmStyleAttrs) and [`BoxStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/#datachart.typings.BoxStyleAttrs), one per part of the chart. The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.RaincloudStyleAttrs

Bases: `ViolinStyleAttrs`, `SwarmStyleAttrs`, `BoxStyleAttrs`

The typing for the raincloud plot style.

The union of the violin (cloud), swarm (rain), and box style keys; each key styles its own part of the raincloud.

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                   |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `mode`                                       | [`SWARM_MODE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SWARM_MODE)                                                                                                                               |
| `bandwidth`                                  | [`BANDWIDTH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.BANDWIDTH)                                                                                                                                 |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                           |
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION)                                                                                                                             |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE)                                                                                                                                         |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
