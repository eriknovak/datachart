# SwarmPlot

Every observation as a point, spread within its group. The [Swarm Plot guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/swarmplot/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.SwarmPlot

```
SwarmPlot(
    data: (
        list[SwarmDataPointAttrs]
        | list[list[SwarmDataPointAttrs]]
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
    mode: SWARM_MODE | str | None = None,
    jitter: float = 0.4,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    orientation: ORIENTATION | str | None = None,
    scaley: AXIS_SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        SwarmStyleAttrs
        | list[SwarmStyleAttrs | None]
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
    label: str | list[str | None] | None = None,
    value: str | list[str | None] | None = None
) -> plt.Figure
```

Creates the swarm plot.

A swarm plot draws every observation as a point at its group's category position, spread across the category width so the points do not hide each other, making counts and gaps visible. Use it for small-to-medium samples where each observation matters, or overlay it on a BoxPlot with `Panel` (the two share positions). For large samples prefer ViolinPlot.

Examples:

```
>>> from datachart.charts import SwarmPlot
>>> figure = SwarmPlot(
...     data=[
...         {"label": "Group A", "value": 10},
...         {"label": "Group A", "value": 15},
...         {"label": "Group A", "value": 12},
...         {"label": "Group B", "value": 20},
...         {"label": "Group B", "value": 25},
...         {"label": "Group B", "value": 22},
...     ],
...     title="Basic Swarm Plot",
...     xlabel="Group",
...     ylabel="Value"
... )
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The data points for the swarm plot(s). Can be a single list of data points for one chart, or a list of lists for multiple charts. Each data point should have a label (category) and value (numeric), and may carry its own emphasis role, which wins over its group's. **TYPE:** \`list[SwarmDataPointAttrs]                                                                                                                       |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                             |
| `xlabel`        | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                   |
| `ylabel`        | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                   |
| `subtitle`      | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                       |
| `emphasis`      | The emphasis role(s), aligned with the group labels of one call (a single value applies to every group): "background" mutes a group's points, "highlight" bolds their edges, None leaves them unchanged. **TYPE:** \`EMPHASIS                                                                                                                                                                                                       |
| `emphasis_rule` | A rule that highlights the groups matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against a summary of each group's values, chosen by by: "median" (default), "mean", "min", "max", or "sum". An explicit emphasis role wins, and a count ranks across every group of every chart. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`       | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                        |
| `xmin`          | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `xmax`          | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymin`          | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymax`          | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                           |
| `show_legend`   | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                        |
| `legend`        | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                              |
| `show_grid`     | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                          |
| `mode`          | How the points spread across the category width. See SWARM_MODE: "swarm" packs the points so none overlap, from the marker size at draw time (axis limits changed afterwards can shift the spacing); "strip" jitters them uniformly. **TYPE:** \`SWARM_MODE                                                                                                                                                                         |
| `jitter`        | The strip jitter width, as a fraction of the category width. Only used with mode="strip". **TYPE:** `float` **DEFAULT:** `0.4`                                                                                                                                                                                                                                                                                                      |
| `show_values`   | Whether to print each group's minimum, median, and maximum beside the points nearest them. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                         |
| `value_format`  | Format string for the value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                             |
| `aspect_ratio`  | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                        |
| `orientation`   | The orientation of the swarms (vertical or horizontal). **TYPE:** \`ORIENTATION                                                                                                                                                                                                                                                                                                                                                     |
| `scaley`        | The y-axis scale (e.g., "log", "linear"). **TYPE:** \`AXIS_SCALE                                                                                                                                                                                                                                                                                                                                                                    |
| `subplots`      | Whether to create separate subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                |
| `max_cols`      | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                         |
| `sharex`        | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                           |
| `sharey`        | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                           |
| `style`         | Style configuration(s) for the points. **TYPE:** \`SwarmStyleAttrs                                                                                                                                                                                                                                                                                                                                                                  |
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
| `brackets`      | Pairwise comparison bracket(s) to draw between two categories, with an optional text such as a p-value. **TYPE:** \`BracketSettingAttrs                                                                                                                                                                                                                                                                                             |
| `vspans`        | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                         |
| `hspans`        | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                       |
| `texts`         | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                            |
| `label`         | The key name in data for label/category values (default: "label"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                  |
| `value`         | The key name in data for numeric values (default: "value"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                         |

| RETURNS      | DESCRIPTION                           |
| ------------ | ------------------------------------- |
| `plt.Figure` | The figure containing the swarm plot. |

## Data

Each record in `data` is a [`SwarmDataPointAttrs`](#datachart.typings.SwarmDataPointAttrs); the `emphasis`, `label` and `value` parameters rename its keys.

### datachart.typings.SwarmDataPointAttrs

Bases: `TypedDict`

The data point attributes for the swarm plot.

| ATTRIBUTE  | DESCRIPTION                                                                                                                                     |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `label`    | The category label. **TYPE:** `str`                                                                                                             |
| `value`    | The numeric value. **TYPE:** \`int                                                                                                              |
| `emphasis` | The point's own emphasis role ("background" or "highlight"); wins over its group's emphasis and the chart's emphasis_rule. **TYPE:** \`EMPHASIS |

## Style

`style` takes the keys of [`SwarmStyleAttrs`](#datachart.typings.SwarmStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineStyleAttrs)), pairwise brackets ([`BracketStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.BracketStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.SwarmStyleAttrs

Bases: `TypedDict`

The typing for the swarm plot style.

| ATTRIBUTE               | DESCRIPTION                                      |
| ----------------------- | ------------------------------------------------ |
| `plot_swarm_color`      | The point color. **TYPE:** \`str                 |
| `plot_swarm_alpha`      | The alpha value of the points. **TYPE:** \`float |
| `plot_swarm_size`       | The point size. **TYPE:** \`int                  |
| `plot_swarm_marker`     | The point marker shape. **TYPE:** \`LINE_MARKER  |
| `plot_swarm_zorder`     | The zorder of the points. **TYPE:** \`int        |
| `plot_swarm_edge_width` | The edge width of the points. **TYPE:** \`int    |
| `plot_swarm_edge_color` | The edge color of the points. **TYPE:** \`str    |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                   |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |
| `mode`                                       | [`SWARM_MODE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SWARM_MODE)                                                                                                                               |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                           |
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION)                                                                                                                             |
| `scaley`                                     | [`AXIS_SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.AXIS_SCALE)                                                                                                                               |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
