# ContourChart

A surface sampled on a grid, as iso-lines or filled bands. The [Contour Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/contourchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.ContourChart

```
ContourChart(
    data: ContourDataAttrs | list[ContourDataAttrs],
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
    filled: bool | None = None,
    levels: (
        CONTOUR_LEVELS | str | int | list[float] | None
    ) = None,
    show_labels: bool | None = None,
    show_colorbars: bool | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    scalex: AXIS_SCALE | str | None = None,
    scaley: AXIS_SCALE | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        ContourStyleAttrs
        | list[ContourStyleAttrs | None]
        | None
    ) = None,
    norm: COLOR_NORM | str | list[str | None] | None = None,
    vmin: float | list[float | None] | None = None,
    vmax: float | list[float | None] | None = None,
    vcenter: float | list[float | None] | None = None,
    value_format: (
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
    ) = None,
    valfmt: (
        VALUE_FORMAT | str | list[str | None] | None
    ) = None
) -> plt.Figure
```

Creates the contour chart.

A contour chart draws a surface sampled on a grid — a loss landscape, a 2-D density, a terrain — as iso-lines of equal value, or as filled bands between them. Use it to read the shape of a function of two variables: where its minima and ridges sit and how steeply it changes. Lines overlay on other charts and on each other; fills stand alone, with an optional colorbar. For a per-cell view of a matrix use Heatmap; for the raw points behind a density use ScatterChart.

Examples:

```
>>> from datachart.charts import ContourChart
>>> figure = ContourChart(
...     data={
...         "x": [0, 1, 2],
...         "y": [0, 1, 2],
...         "z": [
...             [0, 1, 4],
...             [1, 2, 5],
...             [4, 5, 8],
...         ],
...     },
...     title="Basic Contour Chart",
...     xlabel="X",
...     ylabel="Y"
... )
```

| PARAMETER        | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`           | The gridded surface(s): a dictionary with the 2-D z grid and the optional x and y axis values (one per column and per row of z, the indices by default), or a list of them for multiple charts/subplots. **TYPE:** \`ContourDataAttrs                                                                                                                                                                                                 |
| `title`          | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                               |
| `xlabel`         | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                     |
| `ylabel`         | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                     |
| `subtitle`       | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                         |
| `emphasis`       | The emphasis role(s) for individual line contours, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, behind the others, no legend entry), "highlight" bolds it and brings it to the front, None leaves it unchanged. Not supported for filled contours: passing a value with filled=True raises ValueError. **TYPE:** \`EMPHASIS                                                                      |
| `emphasis_rule`  | A rule that highlights the line contours matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against a summary of each contour's own z values, chosen by by: "mean" (default), "median", "min", "max", or "sum". An explicit emphasis role wins, and a count ranks across every contour. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`        | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                          |
| `xmin`           | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                             |
| `xmax`           | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                             |
| `ymin`           | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                             |
| `ymax`           | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                             |
| `show_legend`    | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                          |
| `legend`         | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                                |
| `show_grid`      | Which grid lines to show (e.g., "both", "x", "y"); False draws none. Off by default for filled contours. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                        |
| `filled`         | Whether to fill the bands between the levels (colored by the colormap) instead of drawing iso-lines (in the chart's color). **TYPE:** \`bool                                                                                                                                                                                                                                                                                          |
| `levels`         | Which levels cut the surface: a rule of CONTOUR_LEVELS ("auto", the default, leaves the choice to matplotlib), a target level count, or an explicit list of level values. Filled values beyond a list's ends take the end colors, and the colorbar marks the overflow. **TYPE:** \`CONTOUR_LEVELS                                                                                                                                     |
| `show_labels`    | Whether to write the level values along the iso-lines. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                               |
| `show_colorbars` | Whether to show the colorbar(s) of filled contours. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                  |
| `aspect_ratio`   | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                          |
| `scalex`         | The x-axis scale (e.g., "log", "linear"). **TYPE:** \`AXIS_SCALE                                                                                                                                                                                                                                                                                                                                                                      |
| `scaley`         | The y-axis scale (e.g., "log", "linear"). **TYPE:** \`AXIS_SCALE                                                                                                                                                                                                                                                                                                                                                                      |
| `subplots`       | Whether to create separate subplots for each chart. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                  |
| `max_cols`       | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                           |
| `sharex`         | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                             |
| `sharey`         | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                             |
| `style`          | Style configuration(s) for the contour chart(s). **TYPE:** \`ContourStyleAttrs                                                                                                                                                                                                                                                                                                                                                        |
| `norm`           | Value normalization method(s) of the colormap. "centered" and "twoslope" hold vcenter in the middle of the theme's diverging colormap; see COLOR_NORM. **TYPE:** \`COLOR_NORM                                                                                                                                                                                                                                                         |
| `vmin`           | Minimum value(s) for normalization. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                 |
| `vmax`           | Maximum value(s) for normalization. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                 |
| `vcenter`        | The value(s) a centred normalization holds in the middle of the colormap (0 by default); ignored by every other norm. **TYPE:** \`float                                                                                                                                                                                                                                                                                               |
| `value_format`   | Format string(s) for the inline level labels, with the value named x (e.g., "{x:.1f}"). See VALUE_FORMAT. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                    |
| `xticks`         | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                   |
| `xticklabels`    | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                      |
| `xtickrotate`    | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                |
| `yticks`         | Custom y-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                   |
| `yticklabels`    | Custom y-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                      |
| `ytickrotate`    | Rotation angle for y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                |
| `xticks_format`  | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                             |
| `yticks_format`  | The y-axis tick label format, as xticks_format. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                              |
| `vlines`         | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                               |
| `hlines`         | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                                             |
| `dlines`         | Diagonal line(s) to plot, by slope and intercept. **TYPE:** \`DLineSettingAttrs                                                                                                                                                                                                                                                                                                                                                       |
| `brackets`       | Pairwise comparison bracket(s) to draw between two categories, with an optional text such as a p-value. **TYPE:** \`BracketSettingAttrs                                                                                                                                                                                                                                                                                               |
| `vspans`         | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                           |
| `hspans`         | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                                                                                                                                                         |
| `colorbar`       | The colorbar setting(s): label, location, tick format, and tick positions. See ColorbarSettingAttrs. **TYPE:** \`ColorbarSettingAttrs                                                                                                                                                                                                                                                                                                 |
| `texts`          | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                              |
| `valfmt`         | Deprecated; use value_format. Removed in the next release. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                   |

| RETURNS      | DESCRIPTION                              |
| ------------ | ---------------------------------------- |
| `plt.Figure` | The figure containing the contour chart. |

## Data

Each record in `data` is a [`ContourDataAttrs`](#datachart.typings.ContourDataAttrs).

### datachart.typings.ContourDataAttrs

Bases: `TypedDict`

The data attributes for the contour chart.

| ATTRIBUTE | DESCRIPTION                                                                                     |
| --------- | ----------------------------------------------------------------------------------------------- |
| `x`       | The x-axis values, one per column of z. Defaults to the column indices. **TYPE:** \`list\[int   |
| `y`       | The y-axis values, one per row of z. Defaults to the row indices. **TYPE:** \`list\[int         |
| `z`       | The 2-D grid of surface values, one row per y and one column per x. **TYPE:** \`list\[list\[int |

## Style

`style` takes the keys of [`ContourStyleAttrs`](#datachart.typings.ContourStyleAttrs). The chart also reads the shared groups it draws: reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineStyleAttrs)), pairwise brackets ([`BracketStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.BracketStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.ContourStyleAttrs

Bases: `TypedDict`

The typing for the contour chart style.

| ATTRIBUTE                       | DESCRIPTION                                                                                                                                                                      |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_contour_color`            | The color of the iso-lines; None takes the panel's color cycle. **TYPE:** \`str                                                                                                  |
| `plot_contour_cmap`             | The colormap of the filled bands (palette name, single color, list of hex colors, or colormap); None takes the heatmap colormap. Iso-lines use it only when set. **TYPE:** \`str |
| `plot_contour_line_width`       | The width of the iso-lines; None takes the line chart width. **TYPE:** \`int                                                                                                     |
| `plot_contour_line_style`       | The style of the iso-lines. **TYPE:** \`LINE_STYLE                                                                                                                               |
| `plot_contour_alpha`            | The alpha value of the contour. **TYPE:** \`float                                                                                                                                |
| `plot_contour_zorder`           | The z-order of the contour. **TYPE:** \`int                                                                                                                                      |
| `plot_contour_label_font_size`  | The font size of the inline level labels; None takes the general font size minus two. **TYPE:** \`int                                                                            |
| `plot_contour_label_font_color` | The color of the inline level labels; None takes the line color. **TYPE:** \`str                                                                                                 |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                                       | Constant                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `levels`                                                        | [`CONTOUR_LEVELS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.CONTOUR_LEVELS)                                                                                                                                                                                                                                             |
| `xticks_format`                                                 | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)                                                                                                                               |
| `emphasis`                                                      | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                                                                                                                                         |
| `figsize`                                                       | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                                                                                                                                         |
| `legend={"location": ..., "alignment": ...}`                    | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN)                                                                                                                       |
| `show_grid`                                                     | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                                                                                                                                       |
| `aspect_ratio`                                                  | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                                                                                                                                                 |
| `scalex`                                                        | [`AXIS_SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.AXIS_SCALE)                                                                                                                                                                                                                                                     |
| `scaley`                                                        | [`AXIS_SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.AXIS_SCALE)                                                                                                                                                                                                                                                     |
| `norm`                                                          | [`COLOR_NORM`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.COLOR_NORM)                                                                                                                                                                                                                                                     |
| `value_format`                                                  | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                                                                                                                                                 |
| `yticks_format`                                                 | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)                                                                                                                               |
| `colorbar={"location": ..., "format": ..., "orientation": ...}` | [`COLORBAR_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.COLORBAR_LOCATION), [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`ORIENTATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION) |
