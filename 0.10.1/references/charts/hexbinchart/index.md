# HexbinChart

Point density on the plane, as colored hexagons. The [Hexbin Chart guide](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/charts/hexbinchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.HexbinChart

```
HexbinChart(
    data: HexbinDataAttrs | list[HexbinDataAttrs],
    *,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    subtitle: str | list[str | None] | None = None,
    emphasis: None = None,
    emphasis_rule: EmphasisRuleAttrs | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    xmin: int | float | datetime | None = None,
    xmax: int | float | datetime | None = None,
    ymin: int | float | None = None,
    ymax: int | float | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_colorbars: bool = True,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    scalex: SCALE | str | None = None,
    scaley: SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        HexbinStyleAttrs
        | list[HexbinStyleAttrs | None]
        | None
    ) = None,
    gridsize: int | list[int | None] | None = None,
    reduce: (
        HEXBIN_REDUCE | str | list[str | None] | None
    ) = None,
    mincnt: int | list[int | None] | None = None,
    norm: str | list[str | None] | None = None,
    vmin: float | list[float | None] | None = None,
    vmax: float | list[float | None] | None = None,
    valfmt: (
        VALUE_FORMAT | str | list[str | None] | None
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
    colorbar: (
        ColorbarSettingAttrs
        | list[ColorbarSettingAttrs | None]
        | None
    ) = None,
    texts: (
        TextSettingAttrs
        | list[TextSettingAttrs]
        | list[
            TextSettingAttrs | list[TextSettingAttrs] | None
        ]
        | None
    ) = None
) -> plt.Figure
```

Creates the hexbin chart.

A hexbin chart tiles the plane with hexagons and colors each by the number of points falling in it — or, with a per-point `c`, by an aggregate of those values. Use it where a scatter chart turns into an opaque blob: thousands of points, overlapping clusters, or a value that varies across the plane. For the points themselves use ScatterChart; for a smooth density estimate use ContourChart on stats.kde2d.

Examples:

```
>>> from datachart.charts import HexbinChart
>>> figure = HexbinChart(
...     data={
...         "x": [0.1, 0.4, 0.5, 1.2, 1.3, 2.0],
...         "y": [0.2, 0.3, 0.6, 1.1, 1.4, 2.1],
...     },
...     title="Basic Hexbin Chart",
...     xlabel="X",
...     ylabel="Y"
... )
```

| PARAMETER        | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`           | The points to bin: a dictionary with the x and y columns and an optional c column of per-point values, or a list of them for multiple charts/subplots. **TYPE:** \`HexbinDataAttrs                                                                                                                                                                                                                                                              |
| `title`          | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                         |
| `xlabel`         | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                               |
| `ylabel`         | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                               |
| `subtitle`       | The subtitle(s) for individual charts. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                          |
| `emphasis`       | Not supported: a hexbin chart is a single colormapped layer with no series to mute or highlight. Passing a value raises ValueError. **TYPE:** `None` **DEFAULT:** `None`                                                                                                                                                                                                                                                                        |
| `emphasis_rule`  | A rule that highlights the bins matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against each bin's aggregated value (its count, or c reduced by reduce). Bins exist only once drawn, so a count ranks the bins of each chart on its own, and an empty bin never matches. The rule takes no by. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`        | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                                    |
| `xmin`           | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                       |
| `xmax`           | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                       |
| `ymin`           | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                       |
| `ymax`           | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                       |
| `show_legend`    | Whether to show the legend; it lists the labelled reference lines and bands. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                   |
| `legend`         | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                                          |
| `show_grid`      | Which grid lines to show (e.g., "both", "x", "y"); False draws none. Off by default: the hexagons cover it. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                               |
| `show_colorbars` | Whether to show the colorbar(s). **TYPE:** `bool` **DEFAULT:** `True`                                                                                                                                                                                                                                                                                                                                                                           |
| `aspect_ratio`   | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                                    |
| `scalex`         | The x-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                                     |
| `scaley`         | The y-axis scale (e.g., "log", "linear"). **TYPE:** \`SCALE                                                                                                                                                                                                                                                                                                                                                                                     |
| `subplots`       | Whether to create separate subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                            |
| `max_cols`       | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                     |
| `sharex`         | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                       |
| `sharey`         | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                       |
| `style`          | Style configuration(s) for the hexbin chart(s). **TYPE:** \`HexbinStyleAttrs                                                                                                                                                                                                                                                                                                                                                                    |
| `gridsize`       | The number of hexagons across the x-axis; the plot_hexbin_gridsize config value by default. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                     |
| `reduce`         | How the c values in a hexagon collapse into its color, one of HEXBIN_REDUCE (the mean by default). Ignored without c, where every hexagon shows its point count. **TYPE:** \`HEXBIN_REDUCE                                                                                                                                                                                                                                                      |
| `mincnt`         | The point count below which a hexagon stays blank; every hexagon is drawn by default. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                           |
| `norm`           | Value normalization method(s) of the colormap; "log" spreads heavy-tailed counts. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                               |
| `vmin`           | Minimum value(s) for normalization. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                           |
| `vmax`           | Maximum value(s) for normalization. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                           |
| `valfmt`         | Format string(s) for the colorbar tick labels, with the value named x (e.g., "{x:.0f}"). See VALUE_FORMAT. The format field of the colorbar setting wins when set. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                     |
| `xticks`         | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                             |
| `xticklabels`    | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                                |
| `xtickrotate`    | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                          |
| `yticks`         | Custom y-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                             |
| `yticklabels`    | Custom y-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                                |
| `ytickrotate`    | Rotation angle for y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                          |
| `xticks_format`  | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                       |
| `yticks_format`  | The y-axis tick label format, as xticks_format. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                                        |
| `vlines`         | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                         |
| `hlines`         | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                       |
| `vspans`         | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                                     |
| `hspans`         | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                                   |
| `colorbar`       | The colorbar setting(s): label, location, tick format, and tick positions. See ColorbarSettingAttrs. **TYPE:** \`ColorbarSettingAttrs                                                                                                                                                                                                                                                                                                           |
| `texts`          | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                        |

| RETURNS      | DESCRIPTION                             |
| ------------ | --------------------------------------- |
| `plt.Figure` | The figure containing the hexbin chart. |

## Data

Each record in `data` is a [`HexbinDataAttrs`](#datachart.typings.HexbinDataAttrs).

### datachart.typings.HexbinDataAttrs

Bases: `TypedDict`

The data attributes for the hexbin chart.

| ATTRIBUTE | DESCRIPTION                                                                                                                                  |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `x`       | The x values of the points. **TYPE:** \`list\[int                                                                                            |
| `y`       | The y values of the points, one per x. **TYPE:** \`list\[int                                                                                 |
| `c`       | The value of each point, one per x; when given, every hexagon shows their reduce aggregate instead of its point count. **TYPE:** \`list\[int |

## Style

`style` takes the keys of [`HexbinStyleAttrs`](#datachart.typings.HexbinStyleAttrs). The chart also reads the shared groups it draws: reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/0.10.1/references/config/index.md).

### datachart.typings.HexbinStyleAttrs

Bases: `TypedDict`

The typing for the hexbin chart style.

| ATTRIBUTE                | DESCRIPTION                                                                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_hexbin_cmap`       | The colormap of the hexagons (palette name, single color, list of hex colors, or colormap); None takes the heatmap colormap. **TYPE:** \`str |
| `plot_hexbin_alpha`      | The alpha value of the hexagons. **TYPE:** \`float                                                                                           |
| `plot_hexbin_edge_width` | The width of the hexagon edges; 0 draws none. **TYPE:** \`int                                                                                |
| `plot_hexbin_edge_color` | The color of the hexagon edges. **TYPE:** \`str                                                                                              |
| `plot_hexbin_gridsize`   | The number of hexagons across the x-axis when the chart sets no gridsize. **TYPE:** \`int                                                    |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.1/references/constants/index.md) that lists its values.

| Parameter                                                       | Constant                                                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `reduce`                                                        | [`HEXBIN_REDUCE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.HEXBIN_REDUCE)                                                                                                                                                                                                                                                     |
| `figsize`                                                       | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                                                                                                                                               |
| `show_grid`                                                     | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                                                                                                                                             |
| `aspect_ratio`                                                  | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                                                                                                                                                       |
| `scalex`                                                        | [`SCALE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SCALE)                                                                                                                                                                                                                                                                     |
| `scaley`                                                        | [`SCALE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SCALE)                                                                                                                                                                                                                                                                     |
| `norm`                                                          | [`NORMALIZE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.NORMALIZE)                                                                                                                                                                                                                                                             |
| `valfmt`                                                        | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                                                                                                                                                       |
| `xticks_format`                                                 | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.DATE_FORMAT)                                                                                                                                  |
| `yticks_format`                                                 | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.DATE_FORMAT)                                                                                                                                  |
| `colorbar={"location": ..., "format": ..., "orientation": ...}` | [`COLORBAR_LOCATION`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.COLORBAR_LOCATION), [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT), [`ORIENTATION`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.ORIENTATION) |
