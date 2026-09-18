# RadialChart

Series on polar axes, as a radar line, an area, bars, or a histogram. The [Radial Chart guide](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/charts/radialchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.RadialChart

```
RadialChart(
    data: (
        list[RadialDataPointAttrs]
        | list[list[RadialDataPointAttrs]]
    ),
    *,
    type: RADIAL_TYPE | str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    subtitle: str | list[str | None] | None = None,
    emphasis: (
        EMPHASIS | str | list[str | None] | None
    ) = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    ymin: int | float | None = None,
    ymax: int | float | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_yerr: bool | None = None,
    show_area: bool | None = None,
    show_values: bool | None = None,
    show_tip_labels: bool | None = None,
    show_border: bool | None = None,
    value_format: str | None = None,
    bar_mode: BAR_MODE | str | None = None,
    sort: SORT | str | None = None,
    sort_by: str | None = None,
    emphasis_rule: EmphasisRuleAttrs | None = None,
    num_bins: int | None = None,
    startangle: str | int | float | None = None,
    direction: RADIAL_DIRECTION | str | None = None,
    innerradius: float | None = None,
    scalex: SCALE | str | None = None,
    scaley: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        _RadialStyleAttrs
        | list[_RadialStyleAttrs | None]
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
    vlines: dict | None = None,
    hlines: dict | None = None,
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
    label: str | list[str | None] | None = None,
    x: str | list[str | None] | None = None,
    y: str | list[str | None] | None = None,
    yerr: str | list[str | None] | None = None
) -> plt.Figure
```

Creates the radial chart.

A radial chart plots series on polar axes: as a line (radar) profile, an area, bars, or a histogram, chosen with `type`. Use the radar form to compare a few entities across several metrics on a shared scale, and the bar and histogram forms for cyclic categories such as hours, weekdays, or compass directions.

Examples:

```
>>> from datachart.charts import RadialChart
>>> figure = RadialChart(
...     data=[
...         {"label": "N", "y": 5},
...         {"label": "E", "y": 10},
...         {"label": "S", "y": 15},
...         {"label": "W", "y": 20}
...     ],
...     title="Basic Radial Chart"
... )
```

| PARAMETER         | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`            | The data points for the radial chart(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. The line, bar, and scatter visuals take label/y points whose labels are placed evenly around the circle; the histogram visual takes numeric x observations in degrees, binned over \[0, 360). **TYPE:** \`list[RadialDataPointAttrs] |
| `type`            | The visual the whole figure draws: "line" (default), "bar", "scatter", or "histogram". See RADIAL_TYPE. **TYPE:** \`RADIAL_TYPE                                                                                                                                                                                                                                                   |
| `title`           | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                           |
| `xlabel`          | The angular-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                           |
| `ylabel`          | The radial-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                            |
| `subtitle`        | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** \`str                                                                                                                                                                                                                                                                                                     |
| `emphasis`        | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart, "highlight" bolds it, None leaves it unchanged. **TYPE:** \`EMPHASIS                                                                                                                                                                                                                  |
| `figsize`         | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                      |
| `ymin`            | The minimum radial-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                    |
| `ymax`            | The maximum radial-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                    |
| `show_legend`     | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                      |
| `legend`          | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                            |
| `show_grid`       | Which grid lines to draw: "x" the spokes only, "y" the rings only, "both" both, False neither. Left unset, spokes and rings are both drawn and the theme's own choice is the one drawn in the faint grid color; the other stays a darker grey. **TYPE:** \`SHOW_GRID                                                                                                              |
| `show_yerr`       | Whether to show the radial error band (line visual). **TYPE:** \`bool                                                                                                                                                                                                                                                                                                             |
| `show_area`       | Whether to fill the area inside the line (line visual). **TYPE:** \`bool                                                                                                                                                                                                                                                                                                          |
| `show_values`     | Whether to write each mark's value at its tip, rotated along the spoke. **TYPE:** \`bool                                                                                                                                                                                                                                                                                          |
| `show_tip_labels` | Whether to write the category labels at the mark tips, rotated along their spokes, instead of around the circle. **TYPE:** \`bool                                                                                                                                                                                                                                                 |
| `show_border`     | Whether to draw the outer border circle. Defaults to the theme's spine visibility; False hides it. **TYPE:** \`bool                                                                                                                                                                                                                                                               |
| `value_format`    | Format for the values written by show_values — a printf format (e.g. "%.1f") or a {x}-style string. See VALUE_FORMAT. **TYPE:** \`str                                                                                                                                                                                                                                             |
| `bar_mode`        | How multiple bar series share the circle: "group", "stack", or "overlay" (bar visual). See BAR_MODE. **TYPE:** \`BAR_MODE                                                                                                                                                                                                                                                         |
| `sort`            | The order the categories are drawn in around the circle: None (input order), "ascending", or "descending" by value (bar visual). One order serves every series, keyed by the total across them; ties keep input order. See SORT. **TYPE:** \`SORT                                                                                                                                 |
| `sort_by`         | The subtitle of the one series whose values key the sort instead of the total (bar visual). A category that series lacks sorts last. **TYPE:** \`str                                                                                                                                                                                                                              |
| `emphasis_rule`   | A one-key dict that highlights the bars matching it and mutes the rest (bar visual): {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}. Reads each bar's own value; a record's own emphasis key wins over the rule. **TYPE:** \`EmphasisRuleAttrs                                                                             |
| `num_bins`        | The number of angular bins over \[0, 360) (histogram visual). **TYPE:** \`int                                                                                                                                                                                                                                                                                                     |
| `startangle`      | Where the first point sits: a compass location ("N", "NE", "E", "SE", "S", "SW", "W", "NW") or a numeric compass bearing in degrees clockwise from north. Defaults to "N". **TYPE:** \`str                                                                                                                                                                                        |
| `direction`       | Which way the angles increase: "clockwise" (default) or "counterclockwise". See RADIAL_DIRECTION. **TYPE:** \`RADIAL_DIRECTION                                                                                                                                                                                                                                                    |
| `innerradius`     | The donut hole, as a fraction (0 \<= f < 1) of the radial extent. Defaults to 0. **TYPE:** \`float                                                                                                                                                                                                                                                                                |
| `scalex`          | Not supported; the angular axis has no scale. Raises when passed. **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                               |
| `scaley`          | The radial-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                  |
| `subplots`        | Whether to create separate polar subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                        |
| `max_cols`        | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                       |
| `sharex`          | Whether to share the angular axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                   |
| `sharey`          | Whether to share the radial axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                    |
| `style`           | Style configuration(s) for the chart(s); radial visuals obey the matching cartesian style family (plot_line\_\*, plot_bar\_\*, plot_hist\_\*, plot_scatter\_\*). **TYPE:** \`\_RadialStyleAttrs                                                                                                                                                                                   |
| `texts`           | Text annotation(s) to draw. On the polar axes, data coordinates are (angle in radians, radius); axes-fraction coordinates ("coords": "axes") are often easier. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                       |
| `vlines`          | Not supported on a polar axes. Raises when passed. **TYPE:** \`dict                                                                                                                                                                                                                                                                                                               |
| `hlines`          | Not supported on a polar axes. Raises when passed. **TYPE:** \`dict                                                                                                                                                                                                                                                                                                               |
| `vspans`          | Angular wedge(s) to shade over the full radius; xmin and xmax are angles in degrees from the start angle, an omitted bound running to 0 or 360. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                     |
| `hspans`          | Annulus (annuli) to shade over the full circle; ymin and ymax are radial values, an omitted bound running to the radial limit. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                      |
| `label`           | The key name in data for the category labels (default: "label"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                  |
| `x`               | The key name in data for the histogram observations (default: "x"). **TYPE:** \`str                                                                                                                                                                                                                                                                                               |
| `y`               | The key name in data for radial values (default: "y"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                            |
| `yerr`            | The key name in data for radial error values (default: "yerr"). **TYPE:** \`str                                                                                                                                                                                                                                                                                                   |

| RETURNS      | DESCRIPTION                             |
| ------------ | --------------------------------------- |
| `plt.Figure` | The figure containing the radial chart. |

## Data

Each record in `data` is a [`RadialDataPointAttrs`](#datachart.typings.RadialDataPointAttrs); the `label`, `x`, `y` and `yerr` parameters rename its keys.

### datachart.typings.RadialDataPointAttrs

Bases: `TypedDict`

The data point attributes for the radial chart.

The line, bar, and scatter visuals take `label`/`y` points whose labels are placed evenly around the circle; the histogram visual takes numeric `x` observations in degrees.

| ATTRIBUTE  | DESCRIPTION                                                                                                                       |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `label`    | The category label (line, bar, and scatter visuals). **TYPE:** `str`                                                              |
| `y`        | The radial value (line, bar, and scatter visuals). **TYPE:** \`int                                                                |
| `yerr`     | The radial error value. **TYPE:** \`int                                                                                           |
| `x`        | The angular observation in degrees (histogram visual). **TYPE:** \`int                                                            |
| `emphasis` | The bar's own emphasis role ("background" or "highlight"); wins over the chart's emphasis_rule (bar visual). **TYPE:** \`EMPHASIS |

## Style

`style` takes the keys of [`LineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/charts/linechart/#datachart.typings.LineStyleAttrs), [`BarStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/charts/barchart/#datachart.typings.BarStyleAttrs), [`HistStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/charts/histogram/#datachart.typings.HistStyleAttrs) and [`ScatterStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/charts/scatterchart/#datachart.typings.ScatterStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.ValueLabelStyleAttrs)), the area fill ([`AreaStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.AreaStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/0.10.1/references/config/index.md).

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.1/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                                       | [`RADIAL_TYPE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.RADIAL_TYPE)                                                                                                                                |
| `direction`                                  | [`RADIAL_DIRECTION`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.RADIAL_DIRECTION)                                                                                                                      |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                      |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                      |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                    |
| `bar_mode`                                   | [`BAR_MODE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.BAR_MODE)                                                                                                                                      |
| `sort`                                       | [`SORT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SORT)                                                                                                                                              |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
