# Typings Module

## datachart.typings

Module containing the `typings`.

The `typings` module holds the dictionary contracts of the package: the records a chart's `data` takes, the settings passed beside it (reference lines and bands, texts, legend, emphasis rule, colorbar), and the style keys a chart's `style` and the theme accept. A per-chart contract is documented on that chart's reference page; the shared ones on the typings page.

## Typings by Chart

The records a chart's `data` takes and the keys its `style` accepts are documented on the chart's own reference page, next to the function that reads them.

### Trends and Comparisons

| Chart                                                                                                     | Shows                                                                    | Data                                                                                                                                                  | Style                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [LineChart](https://eriknovak.github.io/datachart/dev/references/charts/linechart/index.md)               | A value along an ordered axis, one line per series.                      | [`LineDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/linechart/#datachart.typings.LineDataPointAttrs)                   | [`LineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/linechart/#datachart.typings.LineStyleAttrs)                                                                                                                                                                                                                                                                                                                                                                                              |
| [StackedAreaChart](https://eriknovak.github.io/datachart/dev/references/charts/stackedareachart/index.md) | Parts of a total along an ordered axis, filled on top of each other.     | [`LineDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/linechart/#datachart.typings.LineDataPointAttrs)                   | [`StackedAreaStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/stackedareachart/#datachart.typings.StackedAreaStyleAttrs)                                                                                                                                                                                                                                                                                                                                                                         |
| [BumpChart](https://eriknovak.github.io/datachart/dev/references/charts/bumpchart/index.md)               | Rank over time, one line per series.                                     | [`LineDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/linechart/#datachart.typings.LineDataPointAttrs)                   | [`BumpStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/bumpchart/#datachart.typings.BumpStyleAttrs)                                                                                                                                                                                                                                                                                                                                                                                              |
| [BarChart](https://eriknovak.github.io/datachart/dev/references/charts/barchart/index.md)                 | A value per category as bars; series grouped, stacked, or overlaid.      | [`BarDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/barchart/#datachart.typings.BarDataPointAttrs)                      | [`BarStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/barchart/#datachart.typings.BarStyleAttrs)                                                                                                                                                                                                                                                                                                                                                                                                 |
| [PyramidChart](https://eriknovak.github.io/datachart/dev/references/charts/pyramidchart/index.md)         | Two series as horizontal bars mirrored around a shared category axis.    | [`BarDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/barchart/#datachart.typings.BarDataPointAttrs)                      | [`BarStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/barchart/#datachart.typings.BarStyleAttrs)                                                                                                                                                                                                                                                                                                                                                                                                 |
| [RadialChart](https://eriknovak.github.io/datachart/dev/references/charts/radialchart/index.md)           | Series on polar axes, as a radar line, an area, bars, or a histogram.    | [`RadialDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/radialchart/#datachart.typings.RadialDataPointAttrs)             | [`LineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/linechart/#datachart.typings.LineStyleAttrs), [`BarStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/barchart/#datachart.typings.BarStyleAttrs), [`HistStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/histogram/#datachart.typings.HistStyleAttrs), [`ScatterStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/scatterchart/#datachart.typings.ScatterStyleAttrs) |
| [CalendarHeatmap](https://eriknovak.github.io/datachart/dev/references/charts/calendarheatmap/index.md)   | One colored cell per day, weeks as columns and weekdays as rows.         | [`CalendarHeatmapDataAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/calendarheatmap/#datachart.typings.CalendarHeatmapDataAttrs) | [`CalendarHeatmapStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/calendarheatmap/#datachart.typings.CalendarHeatmapStyleAttrs)                                                                                                                                                                                                                                                                                                                                                                  |
| [GanttChart](https://eriknovak.github.io/datachart/dev/references/charts/ganttchart/index.md)             | A schedule: one bar per task from its start to its end over a date axis. | [`GanttTaskAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/ganttchart/#datachart.typings.GanttTaskAttrs)                          | [`GanttStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/ganttchart/#datachart.typings.GanttStyleAttrs)                                                                                                                                                                                                                                                                                                                                                                                           |
| [DumbbellChart](https://eriknovak.github.io/datachart/dev/references/charts/dumbbellchart/index.md)       | Two values per category, a dot at each and a connector between them.     | [`DumbbellRecordAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/dumbbellchart/#datachart.typings.DumbbellRecordAttrs)             | [`DumbbellStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/dumbbellchart/#datachart.typings.DumbbellStyleAttrs)                                                                                                                                                                                                                                                                                                                                                                                  |

### Distributions

| Chart                                                                                               | Shows                                                        | Data                                                                                                                                              | Style                                                                                                                                     |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [Histogram](https://eriknovak.github.io/datachart/dev/references/charts/histogram/index.md)         | The distribution of one numeric variable, binned.            | [`HistDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/histogram/#datachart.typings.HistDataPointAttrs)               | [`HistStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/histogram/#datachart.typings.HistStyleAttrs)               |
| [BoxPlot](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/index.md)             | Median, quartiles, whiskers, and outliers per group.         | [`BoxDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/#datachart.typings.BoxDataPointAttrs)                   | [`BoxStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/#datachart.typings.BoxStyleAttrs)                   |
| [ViolinPlot](https://eriknovak.github.io/datachart/dev/references/charts/violinplot/index.md)       | The density profile of each group's distribution.            | [`ViolinDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/violinplot/#datachart.typings.ViolinDataPointAttrs)          | [`ViolinStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/violinplot/#datachart.typings.ViolinStyleAttrs)          |
| [SwarmPlot](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/index.md)         | Every observation as a point, spread within its group.       | [`SwarmDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/#datachart.typings.SwarmDataPointAttrs)             | [`SwarmStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/#datachart.typings.SwarmStyleAttrs)             |
| [RaincloudPlot](https://eriknovak.github.io/datachart/dev/references/charts/raincloudplot/index.md) | A half violin, the raw points, and a box per group.          | [`RaincloudDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/raincloudplot/#datachart.typings.RaincloudDataPointAttrs) | [`RaincloudStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/raincloudplot/#datachart.typings.RaincloudStyleAttrs) |
| [RidgelinePlot](https://eriknovak.github.io/datachart/dev/references/charts/ridgelineplot/index.md) | One density ridge per group, stacked and partly overlapping. | [`RidgelineDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/ridgelineplot/#datachart.typings.RidgelineDataPointAttrs) | [`RidgelineStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/ridgelineplot/#datachart.typings.RidgelineStyleAttrs) |

### Relationships

| Chart                                                                                                 | Shows                                                                                       | Data                                                                                                                                                         | Style                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ScatterChart](https://eriknovak.github.io/datachart/dev/references/charts/scatterchart/index.md)     | One point per observation, placed by two numeric variables.                                 | [`ScatterDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/scatterchart/#datachart.typings.ScatterDataPointAttrs)                 | [`ScatterStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/scatterchart/#datachart.typings.ScatterStyleAttrs)                 |
| [Heatmap](https://eriknovak.github.io/datachart/dev/references/charts/heatmap/index.md)               | A two-dimensional matrix as colored cells.                                                  | [`HeatmapDataAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/heatmap/#datachart.typings.HeatmapDataAttrs)                                | [`HeatmapStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/heatmap/#datachart.typings.HeatmapStyleAttrs)                      |
| [ContourChart](https://eriknovak.github.io/datachart/dev/references/charts/contourchart/index.md)     | A surface sampled on a grid, as iso-lines or filled bands.                                  | [`ContourDataAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/contourchart/#datachart.typings.ContourDataAttrs)                           | [`ContourStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/contourchart/#datachart.typings.ContourStyleAttrs)                 |
| [HexbinChart](https://eriknovak.github.io/datachart/dev/references/charts/hexbinchart/index.md)       | Point density on the plane, as colored hexagons.                                            | [`HexbinDataAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/hexbinchart/#datachart.typings.HexbinDataAttrs)                              | [`HexbinStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/hexbinchart/#datachart.typings.HexbinStyleAttrs)                    |
| [ParallelCoords](https://eriknovak.github.io/datachart/dev/references/charts/parallelcoords/index.md) | Each record as a polyline across one axis per dimension.                                    | [`ParallelCoordsDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/parallelcoords/#datachart.typings.ParallelCoordsDataPointAttrs) | [`ParallelCoordsStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/parallelcoords/#datachart.typings.ParallelCoordsStyleAttrs) |
| [NetworkChart](https://eriknovak.github.io/datachart/dev/references/charts/networkchart/index.md)     | Nodes joined by edges, placed by a layout.                                                  | [`NetworkSingleChartAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/networkchart/#datachart.typings.NetworkSingleChartAttrs)             | [`NetworkStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/networkchart/#datachart.typings.NetworkStyleAttrs)                 |
| [ScatterMatrix](https://eriknovak.github.io/datachart/dev/references/charts/scattermatrix/index.md)   | A scatter chart for every pair of dimensions, distributions on the diagonal.                | [`ScatterMatrixDataPointAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/scattermatrix/#datachart.typings.ScatterMatrixDataPointAttrs)    | [`StyleAttrs`](#datachart.typings.StyleAttrs)                                                                                                        |
| [ImageChart](https://eriknovak.github.io/datachart/dev/references/charts/imagechart/index.md)         | A picture in data coordinates, under or over the other charts.                              | [`ImageDataAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/imagechart/#datachart.typings.ImageDataAttrs)                                 | [`ImageStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/imagechart/#datachart.typings.ImageStyleAttrs)                       |
| [BasemapChart](https://eriknovak.github.io/datachart/dev/references/charts/basemapchart/index.md)     | Coastlines, land, borders, lakes, rivers and roads under a chart of longitude and latitude. | [`BasemapDataAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/basemapchart/#datachart.typings.BasemapDataAttrs)                           | [`BasemapStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/basemapchart/#datachart.typings.BasemapStyleAttrs)                 |

### Flows

| Chart                                                                                           | Shows                                                               | Data                                                                                                                                          | Style                                                                                                                             |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| [SankeyChart](https://eriknovak.github.io/datachart/dev/references/charts/sankeychart/index.md) | Weighted flows between categories, as ribbons between node columns. | [`SankeySingleChartAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/sankeychart/#datachart.typings.SankeySingleChartAttrs) | [`SankeyStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/sankeychart/#datachart.typings.SankeyStyleAttrs) |

### Part of a Whole

| Chart                                                                                   | Shows                                                   | Data                                                                                                                                        | Style                                                                                                                           |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [Treemap](https://eriknovak.github.io/datachart/dev/references/charts/treemap/index.md) | Part-of-whole data as nested rectangles sized by value. | [`TreemapSingleChartAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/treemap/#datachart.typings.TreemapSingleChartAttrs) | [`TreemapStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/charts/treemap/#datachart.typings.TreemapStyleAttrs) |

## Settings

The dictionaries a chart takes beside its data: reference lines and bands, text annotations, the legend, the emphasis rule, and the colorbar. Each is a parameter of the chart function, and a field left out or set to `None` falls back to the theme.

| I want to…                                    | Pass               | As                                                                                                                       |
| --------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| mark a value on the x or y axis               | `vlines`, `hlines` | [`VLineSettingAttrs`](#datachart.typings.VLineSettingAttrs), [`HLineSettingAttrs`](#datachart.typings.HLineSettingAttrs) |
| draw a line through the data, such as parity  | `dlines`           | [`DLineSettingAttrs`](#datachart.typings.DLineSettingAttrs)                                                              |
| compare two categories with a bracket         | `brackets`         | [`BracketSettingAttrs`](#datachart.typings.BracketSettingAttrs)                                                          |
| shade a range of the x or y axis              | `vspans`, `hspans` | [`VSpanSettingAttrs`](#datachart.typings.VSpanSettingAttrs), [`HSpanSettingAttrs`](#datachart.typings.HSpanSettingAttrs) |
| write a note on the chart                     | `texts`            | [`TextSettingAttrs`](#datachart.typings.TextSettingAttrs)                                                                |
| title, place, or lay out the legend           | `legend`           | [`LegendSettingAttrs`](#datachart.typings.LegendSettingAttrs)                                                            |
| highlight the series or marks matching a rule | `emphasis_rule`    | [`EmphasisRuleAttrs`](#datachart.typings.EmphasisRuleAttrs)                                                              |
| place or format the colorbar                  | `colorbar`         | [`ColorbarSettingAttrs`](#datachart.typings.ColorbarSettingAttrs)                                                        |

### datachart.typings.VLineSettingAttrs

Bases: `TypedDict`

The vertical reference line setting, passed to a chart front as `vlines`.

| ATTRIBUTE | DESCRIPTION                                                     |
| --------- | --------------------------------------------------------------- |
| `x`       | The x-axis position of the line. **TYPE:** \`int                |
| `ymin`    | The minimum y-axis position value. **TYPE:** \`int              |
| `ymax`    | The maximum y-axis position value. **TYPE:** \`int              |
| `style`   | The vertical line style attributes. **TYPE:** \`VLineStyleAttrs |
| `label`   | The label of the vertical line. **TYPE:** \`str                 |

### datachart.typings.HLineSettingAttrs

Bases: `TypedDict`

The horizontal reference line setting, passed to a chart front as `hlines`.

| ATTRIBUTE | DESCRIPTION                                                       |
| --------- | ----------------------------------------------------------------- |
| `y`       | The x-axis position of the line. **TYPE:** \`int                  |
| `xmin`    | The minimum y-axis position value. **TYPE:** \`int                |
| `xmax`    | The maximum y-axis position value. **TYPE:** \`int                |
| `style`   | The horizontal line style attributes. **TYPE:** \`HLineStyleAttrs |
| `label`   | The label of the horizontal line. **TYPE:** \`str                 |

### datachart.typings.DLineSettingAttrs

Bases: `TypedDict`

The diagonal reference line setting, passed to a chart front as `dlines`.

The line is straight in data coordinates, so it curves on a log axis, where it is drawn between the axis limits. On linear axes, and without `xmin` and `xmax`, it spans the axes and follows the zoom.

| ATTRIBUTE   | DESCRIPTION                                                           |
| ----------- | --------------------------------------------------------------------- |
| `slope`     | The slope of the line. Defaults to 1. **TYPE:** \`int                 |
| `intercept` | The y-axis value of the line at x = 0. Defaults to 0. **TYPE:** \`int |
| `xmin`      | The x-axis position the line starts at. **TYPE:** \`int               |
| `xmax`      | The x-axis position the line ends at. **TYPE:** \`int                 |
| `style`     | The diagonal line style attributes. **TYPE:** \`DLineStyleAttrs       |
| `label`     | The label of the diagonal line. **TYPE:** \`str                       |

### datachart.typings.BracketSettingAttrs

```
BracketSettingAttrs = TypedDict(
    "BracketSettingAttrs",
    {
        "from": Union[str, int, float],
        "to": Union[str, int, float],
        "text": Union[str, None],
        "y": Union[int, float, None],
        "style": Union[BracketStyleAttrs, None],
    },
    total=False,
)
```

### datachart.typings.VSpanSettingAttrs

Bases: `TypedDict`

The vertical reference band setting, passed to a chart front as `vspans`.

A vertical band shades the region between two x-axis positions over the full height of the axes. On a radial chart the bounds are angles in degrees and the band is a wedge over the full radius.

| ATTRIBUTE | DESCRIPTION                                                           |
| --------- | --------------------------------------------------------------------- |
| `xmin`    | The lower x-axis bound. Defaults to the axis minimum. **TYPE:** \`int |
| `xmax`    | The upper x-axis bound. Defaults to the axis maximum. **TYPE:** \`int |
| `style`   | The vertical band style attributes. **TYPE:** \`VSpanStyleAttrs       |
| `label`   | The label of the band (shown in the legend). **TYPE:** \`str          |

### datachart.typings.HSpanSettingAttrs

Bases: `TypedDict`

The horizontal reference band setting, passed to a chart front as `hspans`.

A horizontal band shades the region between two y-axis positions over the full width of the axes. On a radial chart the bounds are radii and the band is an annulus over the full circle.

| ATTRIBUTE | DESCRIPTION                                                           |
| --------- | --------------------------------------------------------------------- |
| `ymin`    | The lower y-axis bound. Defaults to the axis minimum. **TYPE:** \`int |
| `ymax`    | The upper y-axis bound. Defaults to the axis maximum. **TYPE:** \`int |
| `style`   | The horizontal band style attributes. **TYPE:** \`HSpanStyleAttrs     |
| `label`   | The label of the band (shown in the legend). **TYPE:** \`str          |

### datachart.typings.TextSettingAttrs

Bases: `TypedDict`

The text annotation setting, passed to a chart front as `texts`.

| ATTRIBUTE | DESCRIPTION                                                                                                                                                                                                                       |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`    | The annotation text. **TYPE:** `str`                                                                                                                                                                                              |
| `x`       | The x-axis position of the text. **TYPE:** \`int                                                                                                                                                                                  |
| `y`       | The y-axis position of the text. **TYPE:** \`int                                                                                                                                                                                  |
| `coords`  | The coordinate system of the text position: "data" (default) or "axes" (axes fraction, 0–1). **TYPE:** \`str                                                                                                                      |
| `target`  | The data point the connector points to, always in data coordinates. When present, a connector is drawn from the text to the target. **TYPE:** \`tuple\[int                                                                        |
| `style`   | The per-text style attributes. **TYPE:** \`TextStyleAttrs                                                                                                                                                                         |
| `subplot` | The 0-based index, in render order, of the subplot the text lands in. Read only by Annotate on a multi-subplot figure, where every text must name one; chart fronts target subplots with a list of lists instead. **TYPE:** \`int |

### datachart.typings.LegendSettingAttrs

Bases: `TypedDict`

The per-figure legend setting, passed to a chart front as `legend`.

Every field is optional; a `None` field falls back to the theme's `plot_legend_*` attribute of the same name.

| ATTRIBUTE   | DESCRIPTION                                                                                           |
| ----------- | ----------------------------------------------------------------------------------------------------- |
| `title`     | The legend title; an empty string draws none. **TYPE:** \`str                                         |
| `location`  | The legend location. An outside member places the legend beside the axes. **TYPE:** \`LEGEND_LOCATION |
| `ncols`     | The number of legend columns. **TYPE:** \`int                                                         |
| `alignment` | The legend alignment. **TYPE:** \`LEGEND_ALIGN                                                        |

### datachart.typings.EmphasisRuleAttrs

Bases: `TypedDict`

The emphasis rule setting, passed to a chart front as `emphasis_rule`.

Exactly one comparison key: a unit matching it is highlighted and every other unit muted. Each front selects its own unit — a bar, leaf, node, row, cell or bin reads its one value; a group or series reads a summary of its values, chosen by `by`. A unit's explicit `emphasis` role wins.

| ATTRIBUTE | DESCRIPTION                                                                                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `above`   | Highlight values strictly above this. **TYPE:** \`int                                                                                                                                             |
| `below`   | Highlight values strictly below this. **TYPE:** \`int                                                                                                                                             |
| `between` | Highlight values within (lo, hi), both bounds inclusive. **TYPE:** \`tuple\[int                                                                                                                   |
| `top`     | Highlight the n largest values; ties keep input order. **TYPE:** `int`                                                                                                                            |
| `bottom`  | Highlight the n smallest values; ties keep input order. **TYPE:** `int`                                                                                                                           |
| `by`      | The summary a group or series is read by. Groups default to "median", series to "mean"; a front reading one value per unit rejects it. **TYPE:** `Literal['mean', 'median', 'min', 'max', 'sum']` |

### datachart.typings.ColorbarSettingAttrs

Bases: `TypedDict`

The per-figure colorbar setting, passed to a chart front as `colorbar`.

Every field is optional. `location` is the control: it places the bar on any edge of the chart. With no `location`, `orientation` derives the edge: vertical means right, horizontal means top. When both are given `location` wins.

| ATTRIBUTE     | DESCRIPTION                                                                                                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `label`       | The caption beside the bar, reading along it; drawn in the font_ylabel\_\* theme font. **TYPE:** \`str                                                                   |
| `location`    | The chart edge the bar sits on. **TYPE:** \`COLORBAR_LOCATION                                                                                                            |
| `format`      | The format of the bar's tick labels, with the value named x (e.g. "{x:.0f}"). On a hexbin chart, value_format still applies when this is unset. **TYPE:** \`VALUE_FORMAT |
| `ticks`       | Explicit tick positions on the bar; positions outside the mapped value range are not drawn. **TYPE:** \`list\[int                                                        |
| `orientation` | The orientation; derives the edge when location is unset. **TYPE:** \`ORIENTATION                                                                                        |

## Shared Style

Style groups several charts read from their `style` dictionary: the value labels `show_values` prints, the area fill, the regression line, reference lines and bands, and text annotations. A chart's reference page says which of them it draws, and every key is also a theme key.

### datachart.typings.ValueLabelStyleAttrs

Bases: `TypedDict`

The typing for the value labels: the numbers a chart prints beside its marks when `show_values` is on. One style serves every chart that takes `show_values`; the `plot_bar_value_*` keys of `BarStyleAttrs` are aliases.

| ATTRIBUTE               | DESCRIPTION                                                                                                                                                                                                                                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_value_fontsize`   | The font size of the value labels. **TYPE:** \`int                                                                                                                                                                                                              |
| `plot_value_color`      | The color of the value labels. **TYPE:** \`str                                                                                                                                                                                                                  |
| `plot_value_padding`    | The gap between a mark and its value label, in points. **TYPE:** \`int                                                                                                                                                                                          |
| `plot_value_halo_width` | The width, in points, of the halo, in the axes face color, stroked around the value labels so they stay legible over marks and lines. None or 0 draws no halo. **TYPE:** \`int                                                                                  |
| `plot_value_tab`        | The tab a value label is set on, a rounded box in the ground color like a label ribbon on an engraved chart. Keys: facecolor, edgecolor, line_width (points), pad (in font sizes) and rounding (in font sizes). None draws no tab. **TYPE:** \`dict\[str, float |

### datachart.typings.AreaStyleAttrs

Bases: `TypedDict`

The typing for the area style.

| ATTRIBUTE             | DESCRIPTION                                          |
| --------------------- | ---------------------------------------------------- |
| `plot_area_alpha`     | The alpha value of the area. **TYPE:** \`float       |
| `plot_area_color`     | The color of the area. **TYPE:** \`str               |
| `plot_area_linewidth` | The line width of the area. **TYPE:** \`int          |
| `plot_area_hatch`     | The hatch style of the area. **TYPE:** \`HATCH_STYLE |
| `plot_area_zorder`    | The zorder of the area. **TYPE:** \`int              |

### datachart.typings.RegressionStyleAttrs

Bases: `TypedDict`

The typing for regression line style.

| ATTRIBUTE                  | DESCRIPTION                                         |
| -------------------------- | --------------------------------------------------- |
| `plot_regression_color`    | The regression line color. **TYPE:** \`str          |
| `plot_regression_alpha`    | The alpha of the regression line. **TYPE:** \`float |
| `plot_regression_width`    | The line width. **TYPE:** \`int                     |
| `plot_regression_style`    | The line style. **TYPE:** \`LINE_STYLE              |
| `plot_regression_ci_alpha` | Confidence interval alpha. **TYPE:** \`float        |

### datachart.typings.VLineStyleAttrs

Bases: `TypedDict`

The typing for the vertical line style.

| ATTRIBUTE          | DESCRIPTION                                             |
| ------------------ | ------------------------------------------------------- |
| `plot_vline_color` | The color of the vertical line. **TYPE:** \`str         |
| `plot_vline_style` | The style of the vertical line. **TYPE:** \`LINE_STYLE  |
| `plot_vline_width` | The width of the vertical line. **TYPE:** \`int         |
| `plot_vline_alpha` | The alpha value of the vertical line. **TYPE:** \`float |

### datachart.typings.HLineStyleAttrs

Bases: `TypedDict`

The typing for the horizontal line style.

| ATTRIBUTE          | DESCRIPTION                                               |
| ------------------ | --------------------------------------------------------- |
| `plot_hline_color` | The color of the horizontal line. **TYPE:** \`str         |
| `plot_hline_style` | The style of the horizontal line. **TYPE:** \`LINE_STYLE  |
| `plot_hline_width` | The width of the horizontal line. **TYPE:** \`int         |
| `plot_hline_alpha` | The alpha value of the horizontal line. **TYPE:** \`float |

### datachart.typings.DLineStyleAttrs

Bases: `TypedDict`

The typing for the diagonal line style.

| ATTRIBUTE          | DESCRIPTION                                             |
| ------------------ | ------------------------------------------------------- |
| `plot_dline_color` | The color of the diagonal line. **TYPE:** \`str         |
| `plot_dline_style` | The style of the diagonal line. **TYPE:** \`LINE_STYLE  |
| `plot_dline_width` | The width of the diagonal line. **TYPE:** \`int         |
| `plot_dline_alpha` | The alpha value of the diagonal line. **TYPE:** \`float |

### datachart.typings.BracketStyleAttrs

Bases: `TypedDict`

The typing for the pairwise comparison bracket style.

| ATTRIBUTE            | DESCRIPTION                                                       |
| -------------------- | ----------------------------------------------------------------- |
| `plot_bracket_color` | The color of the bracket line and its text. **TYPE:** \`str       |
| `plot_bracket_width` | The width of the bracket line. **TYPE:** \`int                    |
| `plot_bracket_tick`  | The length of the bracket's end ticks, in points. **TYPE:** \`int |
| `plot_bracket_alpha` | The alpha value of the bracket. **TYPE:** \`float                 |

### datachart.typings.VSpanStyleAttrs

Bases: `TypedDict`

The typing for the vertical reference band style.

| ATTRIBUTE               | DESCRIPTION                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------ |
| `plot_vspan_color`      | The fill color of the band. Defaults to the theme's muted color. **TYPE:** \`str           |
| `plot_vspan_alpha`      | The alpha value of the band. **TYPE:** \`float                                             |
| `plot_vspan_hatch`      | The hatch pattern of the band. **TYPE:** \`HATCH_STYLE                                     |
| `plot_vspan_edge_color` | The edge color of the band; the hatch draws in it. **TYPE:** \`str                         |
| `plot_vspan_edge_width` | The edge line width of the band. **TYPE:** \`int                                           |
| `plot_vspan_zorder`     | The zorder of the band. Defaults to sit over the grid and under the marks. **TYPE:** \`int |

### datachart.typings.HSpanStyleAttrs

Bases: `TypedDict`

The typing for the horizontal reference band style.

| ATTRIBUTE               | DESCRIPTION                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------ |
| `plot_hspan_color`      | The fill color of the band. Defaults to the theme's muted color. **TYPE:** \`str           |
| `plot_hspan_alpha`      | The alpha value of the band. **TYPE:** \`float                                             |
| `plot_hspan_hatch`      | The hatch pattern of the band. **TYPE:** \`HATCH_STYLE                                     |
| `plot_hspan_edge_color` | The edge color of the band; the hatch draws in it. **TYPE:** \`str                         |
| `plot_hspan_edge_width` | The edge line width of the band. **TYPE:** \`int                                           |
| `plot_hspan_zorder`     | The zorder of the band. Defaults to sit over the grid and under the marks. **TYPE:** \`int |

### datachart.typings.TextStyleAttrs

Bases: `TypedDict`

The typing for the text annotation style.

| ATTRIBUTE                  | DESCRIPTION                                                                                   |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| `plot_text_color`          | The text color; falls back to the general font color. **TYPE:** \`str                         |
| `plot_text_size`           | The text font size. **TYPE:** \`int                                                           |
| `plot_text_weight`         | The text font weight. **TYPE:** \`FONT_WEIGHT                                                 |
| `plot_text_halign`         | The horizontal alignment of the text. **TYPE:** \`str                                         |
| `plot_text_valign`         | The vertical alignment of the text. **TYPE:** \`str                                           |
| `plot_text_alpha`          | The alpha value of the text. **TYPE:** \`float                                                |
| `plot_text_box_visible`    | Whether to draw the background box. **TYPE:** \`bool                                          |
| `plot_text_box_style`      | The matplotlib box style (e.g. "round,pad=0.4"). **TYPE:** \`str                              |
| `plot_text_box_facecolor`  | The face color of the box. **TYPE:** \`str                                                    |
| `plot_text_box_edgecolor`  | The edge color of the box. **TYPE:** \`str                                                    |
| `plot_text_box_edge_width` | The edge width of the box. **TYPE:** \`int                                                    |
| `plot_text_box_alpha`      | The alpha value of the box. **TYPE:** \`float                                                 |
| `plot_text_arrow_style`    | The connector look (see ARROW_STYLE) or a raw matplotlib arrow style. **TYPE:** \`ARROW_STYLE |
| `plot_text_arrow_curve`    | The connector curvature; overrides the look's own. **TYPE:** \`float                          |
| `plot_text_arrow_color`    | The connector color. **TYPE:** \`str                                                          |
| `plot_text_arrow_width`    | The connector line width. **TYPE:** \`int                                                     |

## Theme Style

The keys a theme defines and [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md) holds: colors, fonts, axes, legend, grid, the theme-driven defaults, and the sketch and ink looks. `StyleAttrs` is their union together with every chart's own style keys; the [config methods](https://eriknovak.github.io/datachart/dev/references/config/#datachart.config.Config) and [`register_theme`](https://eriknovak.github.io/datachart/dev/references/config/#datachart.config.Config.register_theme) take it, and the [Themes guide](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/index.md) shows how a theme is built from it.

### datachart.typings.StyleAttrs

Bases: `ColorStyleAttrs`, `FontStyleAttrs`, `AxesStyleAttrs`, `LegendStyleAttrs`, `AreaStyleAttrs`, `GridStyleAttrs`, `LineStyleAttrs`, `StackedAreaStyleAttrs`, `BumpStyleAttrs`, `SankeyStyleAttrs`, `TreemapStyleAttrs`, `NetworkStyleAttrs`, `BarStyleAttrs`, `ValueLabelStyleAttrs`, `HistStyleAttrs`, `VLineStyleAttrs`, `HLineStyleAttrs`, `DLineStyleAttrs`, `BracketStyleAttrs`, `VSpanStyleAttrs`, `HSpanStyleAttrs`, `TextStyleAttrs`, `HeatmapStyleAttrs`, `CalendarHeatmapStyleAttrs`, `GanttStyleAttrs`, `DumbbellStyleAttrs`, `ContourStyleAttrs`, `HexbinStyleAttrs`, `ImageStyleAttrs`, `BasemapStyleAttrs`, `ScatterStyleAttrs`, `RegressionStyleAttrs`, `BoxStyleAttrs`, `SwarmStyleAttrs`, `ViolinStyleAttrs`, `RidgelineStyleAttrs`, `ParallelCoordsStyleAttrs`, `ScatterMatrixStyleAttrs`, `ThemeDefaultAttrs`, `SketchStyleAttrs`, `InkStyleAttrs`

The style attributes. Combines all style typings.

### datachart.typings.ColorStyleAttrs

Bases: `TypedDict`

The typing for the general color style.

| ATTRIBUTE                       | DESCRIPTION                                                                                                                                                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `color_general_singular`        | The colors used where a chart needs one color rather than a series palette: the parallel coords numeric hue ramp and the network node base color (palette name, single color, or list of hex colors). **TYPE:** \`COLORS |
| `color_general_multiple`        | The colors used when the datasets share one coordinate space, which is the default for every chart (palette name, single color, or list of hex colors). **TYPE:** \`COLORS                                               |
| `color_parallel_hue`            | The color palette for parallel coords hue categories (palette name, single color, or list of hex colors); None takes color_general_multiple. **TYPE:** \`COLORS                                                          |
| `color_parallel_hue_continuous` | The sequential ramp for parallel coords numeric hue columns (palette name, single color, or list of hex colors). **TYPE:** \`COLORS                                                                                      |
| `muted_color`                   | The color applied to background-emphasis layers. **TYPE:** \`str                                                                                                                                                         |
| `muted_alpha`                   | The alpha applied to background-emphasis layers. **TYPE:** \`float                                                                                                                                                       |

### datachart.typings.FontStyleAttrs

Bases: `TypedDict`

The typing for the font style.

| ATTRIBUTE                | DESCRIPTION                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------ |
| `font_general_family`    | The general font family. **TYPE:** \`str                                             |
| `font_general_sansserif` | The general sans-serif font. **TYPE:** \`list[str]                                   |
| `font_general_serif`     | The general serif font stack, used when the family is "serif". **TYPE:** \`list[str] |
| `font_general_color`     | The general font color. **TYPE:** \`str                                              |
| `font_general_size`      | The general font size. **TYPE:** \`int                                               |
| `font_general_style`     | The general font style. **TYPE:** \`FONT_STYLE                                       |
| `font_general_weight`    | The general font weight. **TYPE:** \`FONT_WEIGHT                                     |
| `font_title_size`        | The title font size. **TYPE:** \`int                                                 |
| `font_title_color`       | The title font color. **TYPE:** \`str                                                |
| `font_title_style`       | The title font style. **TYPE:** \`FONT_STYLE                                         |
| `font_title_weight`      | The title font weight. **TYPE:** \`FONT_WEIGHT                                       |
| `font_subtitle_size`     | The subtitle font size. **TYPE:** \`int                                              |
| `font_subtitle_color`    | The subtitle font color. **TYPE:** \`str                                             |
| `font_subtitle_style`    | The subtitle font style. **TYPE:** \`FONT_STYLE                                      |
| `font_subtitle_weight`   | The subtitle font weight. **TYPE:** \`FONT_WEIGHT                                    |
| `font_xlabel_size`       | The xlabel font size. **TYPE:** \`int                                                |
| `font_xlabel_color`      | The xlabel font color. **TYPE:** \`str                                               |
| `font_xlabel_style`      | The xlabel font style. **TYPE:** \`FONT_STYLE                                        |
| `font_xlabel_weight`     | The xlabel font weight. **TYPE:** \`FONT_WEIGHT                                      |
| `font_ylabel_size`       | The ylabel font size. **TYPE:** \`int                                                |
| `font_ylabel_color`      | The ylabel font color. **TYPE:** \`str                                               |
| `font_ylabel_style`      | The ylabel font style. **TYPE:** \`FONT_STYLE                                        |
| `font_ylabel_weight`     | The ylabel font weight. **TYPE:** \`FONT_WEIGHT                                      |

### datachart.typings.AxesStyleAttrs

Bases: `TypedDict`

The typing for the axes style.

| ATTRIBUTE                    | DESCRIPTION                                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `axes_spines_top_visible`    | Make the top plot spine visible. **TYPE:** \`bool                                                           |
| `axes_spines_right_visible`  | Make the right plot spine visible. **TYPE:** \`bool                                                         |
| `axes_spines_bottom_visible` | Make the bottom plot spine visible. **TYPE:** \`bool                                                        |
| `axes_spines_left_visible`   | Make the left plot spine visible. **TYPE:** \`bool                                                          |
| `axes_spines_width`          | The width of the spines. **TYPE:** \`int                                                                    |
| `axes_spines_zorder`         | The zorder of the spines. **TYPE:** \`int                                                                   |
| `axes_ticks_length`          | The length of the ticks. **TYPE:** \`int                                                                    |
| `axes_ticks_label_size`      | The size of the tick labels. **TYPE:** \`int                                                                |
| `figure_facecolor`           | The color of the figure ground. None keeps matplotlib's. **TYPE:** \`str                                    |
| `axes_facecolor`             | The color of the axes ground; label halos and etch washes take it. None keeps matplotlib's. **TYPE:** \`str |
| `axes_spines_color`          | The color of the spines. None keeps matplotlib's. **TYPE:** \`str                                           |
| `axes_ticks_color`           | The color of the tick marks. None keeps matplotlib's. **TYPE:** \`str                                       |

### datachart.typings.LegendStyleAttrs

Bases: `TypedDict`

The typing for the legend style.

| ATTRIBUTE                 | DESCRIPTION                                                           |
| ------------------------- | --------------------------------------------------------------------- |
| `plot_legend_shadow`      | Show the legends shadow. **TYPE:** \`bool                             |
| `plot_legend_frameon`     | Show the legends frame. **TYPE:** \`bool                              |
| `plot_legend_alignment`   | The legend alignment. **TYPE:** \`LEGEND_ALIGN                        |
| `plot_legend_location`    | The legend location. **TYPE:** \`LEGEND_LOCATION                      |
| `plot_legend_font_size`   | The font size within the legend. **TYPE:** \`int                      |
| `plot_legend_title_size`  | The title size of the legend. **TYPE:** \`int                         |
| `plot_legend_label_color` | The label color of the legend. **TYPE:** \`str                        |
| `plot_legend_title`       | The legend title; an empty string draws none. **TYPE:** \`str         |
| `plot_legend_ncols`       | The number of legend columns. **TYPE:** \`int                         |
| `plot_legend_edge_color`  | The legend frame color. None keeps matplotlib's. **TYPE:** \`str      |
| `plot_legend_face_color`  | The legend background color. None keeps matplotlib's. **TYPE:** \`str |

### datachart.typings.GridStyleAttrs

Bases: `TypedDict`

The typing for the grid style.

| ATTRIBUTE             | DESCRIPTION                                        |
| --------------------- | -------------------------------------------------- |
| `plot_grid_alpha`     | The alpha value of the grid. **TYPE:** \`float     |
| `plot_grid_color`     | The color of the grid. **TYPE:** \`str             |
| `plot_grid_linewidth` | The line width of the grid. **TYPE:** \`int        |
| `plot_grid_linestyle` | The line style of the grid. **TYPE:** \`LINE_STYLE |
| `plot_grid_zorder`    | The zorder of the grid. **TYPE:** \`int            |

### datachart.typings.ThemeDefaultAttrs

Bases: `TypedDict`

The typing for theme-driven defaults and cycles.

| ATTRIBUTE                           | DESCRIPTION                                                                                                                                                                                                                                                                           |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chart_default_show_grid`           | The theme default for show_grid, applied when a chart call leaves it unset. Never applies to heatmaps. None means the theme has no opinion. **TYPE:** \`SHOW_GRID                                                                                                                     |
| `chart_default_show_values`         | The theme default for show_values, applied to every chart that takes it when the chart call leaves it unset. None means the theme has no opinion. **TYPE:** \`bool                                                                                                                    |
| `chart_default_node_label_position` | The theme default for the network chart's label_position, applied when the chart call leaves it unset. None means the theme has no opinion. **TYPE:** \`NETWORK_LABEL_POSITION                                                                                                        |
| `plot_hatch_cycle`                  | The hatch patterns assigned per bar/histogram series, parallel to the color cycle; with plot_etch on, line area fills and stacked areas take them too. An explicit per-chart hatch style wins. None disables the cycle. **TYPE:** \`list[str]                                         |
| `plot_linestyle_cycle`              | The line styles assigned per line, bump and radial line series, parallel to the color cycle. An explicit per-chart line style wins. None disables the cycle. **TYPE:** \`list\[LINE_STYLE                                                                                             |
| `plot_marker_cycle`                 | The markers assigned per scatter and radial scatter series, parallel to the color cycle, and per network node group: a marker, or {"marker": ..., "hollow": True} to draw it as an outline. An explicit per-chart marker wins. None disables the cycle. **TYPE:** \`list\[LINE_MARKER |

### datachart.typings.SketchStyleAttrs

Bases: `TypedDict`

The typing for the sketch attributes: the theme's render-scoped rc-level look (path wobble, halo stroke). The panel snapshots the wobble at build time and applies it inside a scoped matplotlib rc context, so no global rc setting changes; the halo resolves like any style key, so a chart's `style` can override it. Composition keeps the look of the figures it was built from.

| ATTRIBUTE                | DESCRIPTION                                                                                                                                                                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_sketch_params`     | The path wobble as matplotlib sketch parameters [scale, length, randomness]; plt.xkcd() uses [1, 100, 2]. None draws clean paths. **TYPE:** \`list[float]                                                                                                |
| `plot_sketch_halo_width` | The extra width, added to the line width, of the halo (in the axes face color) stroked under series lines (line, radial, regression), so crossing lines read as cut-outs; marks, text and patches stay clean. None or 0 draws no halo. **TYPE:** \`float |

### datachart.typings.InkStyleAttrs

Bases: `TypedDict`

The typing for the ink attributes: marks drawn as a quill and an etching needle would draw them. Every attribute resolves when the chart is built and rides on its artists, so composition keeps the look; `None` turns it off.

| ATTRIBUTE         | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_ink_stroke` | The broad-nib pen the series lines (line, bump, radial, regression) are drawn with, as a filled ribbon whose width varies along the line. Keys: width_scale (the nib width over the line width), nib_angle (degrees), nib_floor (the hairline width as a share of the nib), wobble (the ink wobble amplitude), taper (the end taper, in pixels). None draws plain lines. **TYPE:** \`dict[str, float]                                                                                        |
| `plot_etch`       | The etching that replaces the hatch tile of a hatched fill with hand-drawn lines clipped to its outline; the hatch pattern still picks the lines and . stipples. Keys: spacing (points between lines), jitter (the spacing jitter as a share of it), angle_jitter (degrees), line_width (points), wash (the share of the face color laid over the axes face under the lines; fills under lines take none), color (the etch ink). None keeps matplotlib's hatch. **TYPE:** \`dict\[str, float |
| `plot_value_etch` | The steps a value scale draws in when plot_etch is on: washes (one fill color per step, lightest first) and hatches (one pattern per step, sparsest first). Heatmap, calendar heatmap and hexbin cells and filled contour bands take the step their value falls in, a filled contour draws its level lines and labels over the bands, and a legend of the steps replaces the colorbar. None keeps the colormap. **TYPE:** \`dict\[str, list[str]\]                                           |
