# Heatmap

A two-dimensional matrix as colored cells. The [Heatmap guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/heatmap/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.Heatmap

```
Heatmap(
    data: HeatmapDataAttrs | list[HeatmapDataAttrs],
    *,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    subtitle: str | list[str | None] | None = None,
    emphasis: None = None,
    emphasis_rule: EmphasisRuleAttrs | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    xmin: int | float | None = None,
    xmax: int | float | None = None,
    ymin: int | float | None = None,
    ymax: int | float | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_colorbars: bool | None = None,
    show_heatmap_values: bool | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        HeatmapStyleAttrs
        | list[HeatmapStyleAttrs | None]
        | None
    ) = None,
    norm: str | list[str | None] | None = None,
    vmin: float | list[float | None] | None = None,
    vmax: float | list[float | None] | None = None,
    vcenter: float | list[float | None] | None = None,
    valfmt: (
        VALUE_FORMAT | str | list[str | None] | None
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

Creates the heatmap.

A heatmap maps every cell of a 2-D matrix to a color, so structure in a grid of numbers (correlations, confusion matrices, feature-by-time tables) reads at a glance. Use it when both axes are categorical or gridded and the value is what matters; the color scale, colorbar, and cell value labels are all configurable.

Examples:

```
>>> from datachart.charts import Heatmap
>>> figure = Heatmap(
...     data={
...         "x": ["a", "b", "c"],
...         "y": ["p", "q", "r"],
...         "z": [
...             [1, 2, 3],
...             [4, 5, 6],
...             [7, 8, 9],
...         ],
...     },
...     title="Basic Heatmap",
...     xlabel="X",
...     ylabel="Y"
... )
```

| PARAMETER             | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`                | The labelled grid(s) for the heatmap(s): one {x, y, z} dict, or a list of them for multiple heatmaps/subplots. z is the 2-D matrix of cell values (rows along y, columns along x; None cells stay blank); x and y are optional tick labels for its columns and rows (any values, the indices by default). An explicit xticks/xticklabels (yticks/yticklabels) overrides them. An optional emphasis grid aligned with z gives a cell its own role: "background" fades it to the theme's muted alpha, "highlight" outlines it, None leaves it unchanged. **TYPE:** \`HeatmapDataAttrs |
| `title`               | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `xlabel`              | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `ylabel`              | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `subtitle`            | The subtitle(s) for individual charts. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `emphasis`            | Not supported: a heatmap has no series to mute or highlight; set per-cell roles through the emphasis grid of data. Passing a value raises ValueError. **TYPE:** `None` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                          |
| `emphasis_rule`       | A rule that highlights the cells matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against each cell's value; a blank cell never matches. A cell's role in the emphasis grid of data wins. The rule takes no by. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs                                                                                                                                                                                                                     |
| `figsize`             | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `xmin`                | The minimum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `xmax`                | The maximum x-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymin`                | The minimum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymax`                | The maximum y-axis value. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `show_legend`         | Whether to show the legend (not typical for heatmaps). **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `legend`              | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                                              |
| `show_grid`           | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `show_colorbars`      | Whether to show the colorbar(s). **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `show_heatmap_values` | Whether to show values on the heatmap cells. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `aspect_ratio`        | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `subplots`            | Whether to create separate subplots for each heatmap. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `max_cols`            | Maximum number of columns in subplots (when subplots=True). **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `sharex`              | Whether to share the x-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `sharey`              | Whether to share the y-axis in subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `style`               | Style configuration(s) for the heatmap(s). **TYPE:** \`HeatmapStyleAttrs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `norm`                | Value normalization method(s). "centered" and "twoslope" hold vcenter in the middle of the theme's diverging colormap; see NORMALIZE. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `vmin`                | Minimum value(s) for normalization. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `vmax`                | Maximum value(s) for normalization. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `vcenter`             | The value(s) a centred normalization holds in the middle of the colormap (0 by default); ignored by every other norm. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `valfmt`              | Format string(s) for cell values, with the value named x (e.g., "{x:.1f}"). See VALUE_FORMAT. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `xticks`              | Custom x-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `xticklabels`         | Custom x-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `xtickrotate`         | Rotation angle for x-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `yticks`              | Custom y-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `yticklabels`         | Custom y-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `ytickrotate`         | Rotation angle for y-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `xticks_format`       | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                                                                           |
| `yticks_format`       | The y-axis tick label format, as xticks_format. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `colorbar`            | The colorbar setting(s): label, location, tick format, and tick positions. See ColorbarSettingAttrs. **TYPE:** \`ColorbarSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `texts`               | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

| RETURNS      | DESCRIPTION                        |
| ------------ | ---------------------------------- |
| `plt.Figure` | The figure containing the heatmap. |

## Data

Each record in `data` is a [`HeatmapDataAttrs`](#datachart.typings.HeatmapDataAttrs); the `emphasis` parameter renames its keys.

### datachart.typings.HeatmapDataAttrs

Bases: `TypedDict`

The data attributes for the heatmap chart.

| ATTRIBUTE  | DESCRIPTION                                                                                                                                      |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `x`        | The column labels, one per column of z. Defaults to the column indices. **TYPE:** \`list\[str                                                    |
| `y`        | The row labels, one per row of z. Defaults to the row indices. **TYPE:** \`list\[str                                                             |
| `z`        | The 2-D grid of cell values, one row per y and one column per x. **TYPE:** \`list\[list\[int                                                     |
| `emphasis` | The per-cell emphasis roles, aligned with z ("background" or "highlight"); wins over the chart's emphasis_rule. **TYPE:** \`list\[list\[EMPHASIS |

## Style

`style` takes the keys of [`HeatmapStyleAttrs`](#datachart.typings.HeatmapStyleAttrs). The chart also reads the shared groups it draws: text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.HeatmapStyleAttrs

Bases: `TypedDict`

The typing for the heatmap chart style.

| ATTRIBUTE                     | DESCRIPTION                                                                                                                                                                   |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_heatmap_cmap`           | The color map of the heatmap (palette name, single color, list of hex colors, or colormap). **TYPE:** \`str                                                                   |
| `plot_heatmap_cmap_diverging` | The color map a centred norm ("centered" or "twoslope") draws in, in place of plot_heatmap_cmap; a plot_heatmap_cmap set in the chart's own style still wins. **TYPE:** \`str |
| `plot_heatmap_alpha`          | The alpha value of the heatmap. **TYPE:** \`float                                                                                                                             |
| `plot_heatmap_font_size`      | The font size of the heatmap. **TYPE:** \`int                                                                                                                                 |
| `plot_heatmap_font_color`     | The font color of the heatmap. **TYPE:** \`str                                                                                                                                |
| `plot_heatmap_font_style`     | The font style of the heatmap. **TYPE:** \`FONT_STYLE                                                                                                                         |
| `plot_heatmap_font_weight`    | The font weight of the heatmap. **TYPE:** \`FONT_WEIGHT                                                                                                                       |
| `plot_heatmap_frame_color`    | The color of the frame always drawn around heatmap axes. **TYPE:** \`str                                                                                                      |
| `plot_heatmap_edge_width`     | The width of the borders drawn between the cells (0 draws none). **TYPE:** \`int                                                                                              |
| `plot_heatmap_edge_color`     | The color of the borders drawn between the cells. **TYPE:** \`str                                                                                                             |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                                       | Constant                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `figsize`                                                       | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                                                                                                                                         |
| `legend={"location": ..., "alignment": ...}`                    | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN)                                                                                                                       |
| `show_grid`                                                     | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                                                                                                                                       |
| `aspect_ratio`                                                  | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                                                                                                                                                 |
| `norm`                                                          | [`NORMALIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.NORMALIZE)                                                                                                                                                                                                                                                       |
| `valfmt`                                                        | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                                                                                                                                                 |
| `xticks_format`                                                 | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)                                                                                                                               |
| `yticks_format`                                                 | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)                                                                                                                               |
| `colorbar={"location": ..., "format": ..., "orientation": ...}` | [`COLORBAR_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.COLORBAR_LOCATION), [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`ORIENTATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION) |
