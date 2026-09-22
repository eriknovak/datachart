---
title: Typings Module
---

# Typings Module

::: datachart.typings
    options:
        members: False
        heading_level: 2
        annotations_path: brief

## Typings by Chart

The records a chart's `data` takes and the keys its `style` accepts are documented on the chart's own reference page, next to the function that reads them.

### Trends and Comparisons

| Chart | Shows | Data | Style |
| :-- | :-- | :-- | :-- |
| [LineChart](charts/linechart.md) | A value along an ordered axis, one line per series. | [`LineDataPointAttrs`](charts/linechart.md#datachart.typings.LineDataPointAttrs) | [`LineStyleAttrs`](charts/linechart.md#datachart.typings.LineStyleAttrs) |
| [StackedAreaChart](charts/stackedareachart.md) | Parts of a total along an ordered axis, filled on top of each other. | [`LineDataPointAttrs`](charts/linechart.md#datachart.typings.LineDataPointAttrs) | [`StackedAreaStyleAttrs`](charts/stackedareachart.md#datachart.typings.StackedAreaStyleAttrs) |
| [BumpChart](charts/bumpchart.md) | Rank over time, one line per series. | [`LineDataPointAttrs`](charts/linechart.md#datachart.typings.LineDataPointAttrs) | [`BumpStyleAttrs`](charts/bumpchart.md#datachart.typings.BumpStyleAttrs) |
| [BarChart](charts/barchart.md) | A value per category as bars; series grouped, stacked, or overlaid. | [`BarDataPointAttrs`](charts/barchart.md#datachart.typings.BarDataPointAttrs) | [`BarStyleAttrs`](charts/barchart.md#datachart.typings.BarStyleAttrs) |
| [PyramidChart](charts/pyramidchart.md) | Two series as horizontal bars mirrored around a shared category axis. | [`BarDataPointAttrs`](charts/barchart.md#datachart.typings.BarDataPointAttrs) | [`BarStyleAttrs`](charts/barchart.md#datachart.typings.BarStyleAttrs) |
| [RadialChart](charts/radialchart.md) | Series on polar axes, as a radar line, an area, bars, or a histogram. | [`RadialDataPointAttrs`](charts/radialchart.md#datachart.typings.RadialDataPointAttrs) | [`LineStyleAttrs`](charts/linechart.md#datachart.typings.LineStyleAttrs), [`BarStyleAttrs`](charts/barchart.md#datachart.typings.BarStyleAttrs), [`HistStyleAttrs`](charts/histogram.md#datachart.typings.HistStyleAttrs), [`ScatterStyleAttrs`](charts/scatterchart.md#datachart.typings.ScatterStyleAttrs) |
| [CalendarHeatmap](charts/calendarheatmap.md) | One colored cell per day, weeks as columns and weekdays as rows. | [`CalendarHeatmapDataAttrs`](charts/calendarheatmap.md#datachart.typings.CalendarHeatmapDataAttrs) | [`CalendarHeatmapStyleAttrs`](charts/calendarheatmap.md#datachart.typings.CalendarHeatmapStyleAttrs) |
| [GanttChart](charts/ganttchart.md) | A schedule: one bar per task from its start to its end over a date axis. | [`GanttTaskAttrs`](charts/ganttchart.md#datachart.typings.GanttTaskAttrs) | [`GanttStyleAttrs`](charts/ganttchart.md#datachart.typings.GanttStyleAttrs) |
| [DumbbellChart](charts/dumbbellchart.md) | Two values per category, a dot at each and a connector between them. | [`DumbbellRecordAttrs`](charts/dumbbellchart.md#datachart.typings.DumbbellRecordAttrs) | [`DumbbellStyleAttrs`](charts/dumbbellchart.md#datachart.typings.DumbbellStyleAttrs) |

### Distributions

| Chart | Shows | Data | Style |
| :-- | :-- | :-- | :-- |
| [Histogram](charts/histogram.md) | The distribution of one numeric variable, binned. | [`HistDataPointAttrs`](charts/histogram.md#datachart.typings.HistDataPointAttrs) | [`HistStyleAttrs`](charts/histogram.md#datachart.typings.HistStyleAttrs) |
| [BoxPlot](charts/boxplot.md) | Median, quartiles, whiskers, and outliers per group. | [`BoxDataPointAttrs`](charts/boxplot.md#datachart.typings.BoxDataPointAttrs) | [`BoxStyleAttrs`](charts/boxplot.md#datachart.typings.BoxStyleAttrs) |
| [ViolinPlot](charts/violinplot.md) | The density profile of each group's distribution. | [`ViolinDataPointAttrs`](charts/violinplot.md#datachart.typings.ViolinDataPointAttrs) | [`ViolinStyleAttrs`](charts/violinplot.md#datachart.typings.ViolinStyleAttrs) |
| [SwarmPlot](charts/swarmplot.md) | Every observation as a point, spread within its group. | [`SwarmDataPointAttrs`](charts/swarmplot.md#datachart.typings.SwarmDataPointAttrs) | [`SwarmStyleAttrs`](charts/swarmplot.md#datachart.typings.SwarmStyleAttrs) |
| [RaincloudPlot](charts/raincloudplot.md) | A half violin, the raw points, and a box per group. | [`RaincloudDataPointAttrs`](charts/raincloudplot.md#datachart.typings.RaincloudDataPointAttrs) | [`RaincloudStyleAttrs`](charts/raincloudplot.md#datachart.typings.RaincloudStyleAttrs) |
| [RidgelinePlot](charts/ridgelineplot.md) | One density ridge per group, stacked and partly overlapping. | [`RidgelineDataPointAttrs`](charts/ridgelineplot.md#datachart.typings.RidgelineDataPointAttrs) | [`RidgelineStyleAttrs`](charts/ridgelineplot.md#datachart.typings.RidgelineStyleAttrs) |

### Relationships

| Chart | Shows | Data | Style |
| :-- | :-- | :-- | :-- |
| [ScatterChart](charts/scatterchart.md) | One point per observation, placed by two numeric variables. | [`ScatterDataPointAttrs`](charts/scatterchart.md#datachart.typings.ScatterDataPointAttrs) | [`ScatterStyleAttrs`](charts/scatterchart.md#datachart.typings.ScatterStyleAttrs) |
| [Heatmap](charts/heatmap.md) | A two-dimensional matrix as colored cells. | [`HeatmapDataAttrs`](charts/heatmap.md#datachart.typings.HeatmapDataAttrs) | [`HeatmapStyleAttrs`](charts/heatmap.md#datachart.typings.HeatmapStyleAttrs) |
| [ContourChart](charts/contourchart.md) | A surface sampled on a grid, as iso-lines or filled bands. | [`ContourDataAttrs`](charts/contourchart.md#datachart.typings.ContourDataAttrs) | [`ContourStyleAttrs`](charts/contourchart.md#datachart.typings.ContourStyleAttrs) |
| [HexbinChart](charts/hexbinchart.md) | Point density on the plane, as colored hexagons. | [`HexbinDataAttrs`](charts/hexbinchart.md#datachart.typings.HexbinDataAttrs) | [`HexbinStyleAttrs`](charts/hexbinchart.md#datachart.typings.HexbinStyleAttrs) |
| [ParallelCoords](charts/parallelcoords.md) | Each record as a polyline across one axis per dimension. | [`ParallelCoordsDataPointAttrs`](charts/parallelcoords.md#datachart.typings.ParallelCoordsDataPointAttrs) | [`ParallelCoordsStyleAttrs`](charts/parallelcoords.md#datachart.typings.ParallelCoordsStyleAttrs) |
| [NetworkChart](charts/networkchart.md) | Nodes joined by edges, placed by a layout. | [`NetworkSingleChartAttrs`](charts/networkchart.md#datachart.typings.NetworkSingleChartAttrs) | [`NetworkStyleAttrs`](charts/networkchart.md#datachart.typings.NetworkStyleAttrs) |
| [ScatterMatrix](charts/scattermatrix.md) | A scatter chart for every pair of dimensions, distributions on the diagonal. | [`ScatterMatrixDataPointAttrs`](charts/scattermatrix.md#datachart.typings.ScatterMatrixDataPointAttrs) | [`StyleAttrs`](#datachart.typings.StyleAttrs) |

### Flows

| Chart | Shows | Data | Style |
| :-- | :-- | :-- | :-- |
| [SankeyChart](charts/sankeychart.md) | Weighted flows between categories, as ribbons between node columns. | [`SankeySingleChartAttrs`](charts/sankeychart.md#datachart.typings.SankeySingleChartAttrs) | [`SankeyStyleAttrs`](charts/sankeychart.md#datachart.typings.SankeyStyleAttrs) |

### Part of a Whole

| Chart | Shows | Data | Style |
| :-- | :-- | :-- | :-- |
| [Treemap](charts/treemap.md) | Part-of-whole data as nested rectangles sized by value. | [`TreemapSingleChartAttrs`](charts/treemap.md#datachart.typings.TreemapSingleChartAttrs) | [`TreemapStyleAttrs`](charts/treemap.md#datachart.typings.TreemapStyleAttrs) |

## Settings

The dictionaries a chart takes beside its data: reference lines and bands, text annotations, the legend, the emphasis rule, and the colorbar. Each is a parameter of the chart function, and a field left out or set to `None` falls back to the theme.

| I want to…                                  | Pass                  | As |
| :------------------------------------------ | :-------------------- | :-- |
| mark a value on the x or y axis             | `vlines`, `hlines`    | [`VLineSettingAttrs`](#datachart.typings.VLineSettingAttrs), [`HLineSettingAttrs`](#datachart.typings.HLineSettingAttrs) |
| draw a line through the data, such as parity | `dlines`              | [`DLineSettingAttrs`](#datachart.typings.DLineSettingAttrs) |
| compare two categories with a bracket        | `brackets`            | [`BracketSettingAttrs`](#datachart.typings.BracketSettingAttrs) |
| shade a range of the x or y axis            | `vspans`, `hspans`    | [`VSpanSettingAttrs`](#datachart.typings.VSpanSettingAttrs), [`HSpanSettingAttrs`](#datachart.typings.HSpanSettingAttrs) |
| write a note on the chart                   | `texts`               | [`TextSettingAttrs`](#datachart.typings.TextSettingAttrs) |
| title, place, or lay out the legend         | `legend`              | [`LegendSettingAttrs`](#datachart.typings.LegendSettingAttrs) |
| highlight the series or marks matching a rule | `emphasis_rule`     | [`EmphasisRuleAttrs`](#datachart.typings.EmphasisRuleAttrs) |
| place or format the colorbar                | `colorbar`            | [`ColorbarSettingAttrs`](#datachart.typings.ColorbarSettingAttrs) |

::: datachart.typings.VLineSettingAttrs
    options:
        heading_level: 3

::: datachart.typings.HLineSettingAttrs
    options:
        heading_level: 3

::: datachart.typings.DLineSettingAttrs
    options:
        heading_level: 3

::: datachart.typings.BracketSettingAttrs
    options:
        heading_level: 3

::: datachart.typings.VSpanSettingAttrs
    options:
        heading_level: 3

::: datachart.typings.HSpanSettingAttrs
    options:
        heading_level: 3

::: datachart.typings.TextSettingAttrs
    options:
        heading_level: 3

::: datachart.typings.LegendSettingAttrs
    options:
        heading_level: 3

::: datachart.typings.EmphasisRuleAttrs
    options:
        heading_level: 3

::: datachart.typings.ColorbarSettingAttrs
    options:
        heading_level: 3

## Shared Style

Style groups several charts read from their `style` dictionary: the value labels `show_values` prints, the area fill, the regression line, reference lines and bands, and text annotations. A chart's reference page says which of them it draws, and every key is also a theme key.

::: datachart.typings.ValueLabelStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.AreaStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.RegressionStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.VLineStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.HLineStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.DLineStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.BracketStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.VSpanStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.HSpanStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.TextStyleAttrs
    options:
        heading_level: 3

## Theme Style

The keys a theme defines and [`config`](config.md) holds: colors, fonts, axes, legend, grid, the theme-driven defaults, and the sketch and ink looks. `StyleAttrs` is their union together with every chart's own style keys; the [config methods](config.md#datachart.config.Config) and [`register_theme`](config.md#datachart.config.Config.register_theme) take it, and the [Themes guide](../how-to-guides/styling/themes.ipynb) shows how a theme is built from it.

::: datachart.typings.StyleAttrs
    options:
        heading_level: 3

::: datachart.typings.ColorStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.FontStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.AxesStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.LegendStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.GridStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.ThemeDefaultAttrs
    options:
        heading_level: 3

::: datachart.typings.SketchStyleAttrs
    options:
        heading_level: 3

::: datachart.typings.InkStyleAttrs
    options:
        heading_level: 3
