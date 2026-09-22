---
title: Charts Module
---

# Charts Module

::: datachart.charts
    options:
        members: False
        heading_level: 2

## Charts by Family

One page per chart: the function and its parameters, the shape of its data, the keys `style` takes, and the constant each parameter accepts. Pick the chart by the question it answers; the [chart guides](../../how-to-guides/charts/index.md) show each one on real data.

### Trends and Comparisons

| Chart | Shows | Data | Style | Guide |
| :-- | :-- | :-- | :-- | :-- |
| [LineChart](linechart.md) | A value along an ordered axis, one line per series. | [`LineDataPointAttrs`](linechart.md#datachart.typings.LineDataPointAttrs) | [`LineStyleAttrs`](linechart.md#datachart.typings.LineStyleAttrs) | [Line Chart](../../how-to-guides/charts/linechart.ipynb) |
| [StackedAreaChart](stackedareachart.md) | Parts of a total along an ordered axis, filled on top of each other. | [`LineDataPointAttrs`](linechart.md#datachart.typings.LineDataPointAttrs) | [`StackedAreaStyleAttrs`](stackedareachart.md#datachart.typings.StackedAreaStyleAttrs) | [Stacked Area Chart](../../how-to-guides/charts/stackedareachart.ipynb) |
| [BumpChart](bumpchart.md) | Rank over time, one line per series. | [`LineDataPointAttrs`](linechart.md#datachart.typings.LineDataPointAttrs) | [`BumpStyleAttrs`](bumpchart.md#datachart.typings.BumpStyleAttrs) | [Bump Chart](../../how-to-guides/charts/bumpchart.ipynb) |
| [BarChart](barchart.md) | A value per category as bars; series grouped, stacked, or overlaid. | [`BarDataPointAttrs`](barchart.md#datachart.typings.BarDataPointAttrs) | [`BarStyleAttrs`](barchart.md#datachart.typings.BarStyleAttrs) | [Bar Chart](../../how-to-guides/charts/barchart.ipynb) |
| [PyramidChart](pyramidchart.md) | Two series as horizontal bars mirrored around a shared category axis. | [`BarDataPointAttrs`](barchart.md#datachart.typings.BarDataPointAttrs) | [`BarStyleAttrs`](barchart.md#datachart.typings.BarStyleAttrs) | [Pyramid Chart](../../how-to-guides/charts/pyramidchart.ipynb) |
| [RadialChart](radialchart.md) | Series on polar axes, as a radar line, an area, bars, or a histogram. | [`RadialDataPointAttrs`](radialchart.md#datachart.typings.RadialDataPointAttrs) | [`LineStyleAttrs`](linechart.md#datachart.typings.LineStyleAttrs), [`BarStyleAttrs`](barchart.md#datachart.typings.BarStyleAttrs), [`HistStyleAttrs`](histogram.md#datachart.typings.HistStyleAttrs), [`ScatterStyleAttrs`](scatterchart.md#datachart.typings.ScatterStyleAttrs) | [Radial Chart](../../how-to-guides/charts/radialchart.ipynb) |
| [CalendarHeatmap](calendarheatmap.md) | One colored cell per day, weeks as columns and weekdays as rows. | [`CalendarHeatmapDataAttrs`](calendarheatmap.md#datachart.typings.CalendarHeatmapDataAttrs) | [`CalendarHeatmapStyleAttrs`](calendarheatmap.md#datachart.typings.CalendarHeatmapStyleAttrs) | [Calendar Heatmap](../../how-to-guides/charts/calendarheatmap.ipynb) |
| [GanttChart](ganttchart.md) | A schedule: one bar per task from its start to its end over a date axis. | [`GanttTaskAttrs`](ganttchart.md#datachart.typings.GanttTaskAttrs) | [`GanttStyleAttrs`](ganttchart.md#datachart.typings.GanttStyleAttrs) | [Gantt Chart](../../how-to-guides/charts/ganttchart.ipynb) |
| [DumbbellChart](dumbbellchart.md) | Two values per category, a dot at each and a connector between them. | [`DumbbellRecordAttrs`](dumbbellchart.md#datachart.typings.DumbbellRecordAttrs) | [`DumbbellStyleAttrs`](dumbbellchart.md#datachart.typings.DumbbellStyleAttrs) | [Dumbbell Chart](../../how-to-guides/charts/dumbbellchart.ipynb) |

### Distributions

| Chart | Shows | Data | Style | Guide |
| :-- | :-- | :-- | :-- | :-- |
| [Histogram](histogram.md) | The distribution of one numeric variable, binned. | [`HistDataPointAttrs`](histogram.md#datachart.typings.HistDataPointAttrs) | [`HistStyleAttrs`](histogram.md#datachart.typings.HistStyleAttrs) | [Histogram](../../how-to-guides/charts/histogram.ipynb) |
| [BoxPlot](boxplot.md) | Median, quartiles, whiskers, and outliers per group. | [`BoxDataPointAttrs`](boxplot.md#datachart.typings.BoxDataPointAttrs) | [`BoxStyleAttrs`](boxplot.md#datachart.typings.BoxStyleAttrs) | [Box Plot](../../how-to-guides/charts/boxplot.ipynb) |
| [ViolinPlot](violinplot.md) | The density profile of each group's distribution. | [`ViolinDataPointAttrs`](violinplot.md#datachart.typings.ViolinDataPointAttrs) | [`ViolinStyleAttrs`](violinplot.md#datachart.typings.ViolinStyleAttrs) | [Violin Plot](../../how-to-guides/charts/violinplot.ipynb) |
| [SwarmPlot](swarmplot.md) | Every observation as a point, spread within its group. | [`SwarmDataPointAttrs`](swarmplot.md#datachart.typings.SwarmDataPointAttrs) | [`SwarmStyleAttrs`](swarmplot.md#datachart.typings.SwarmStyleAttrs) | [Swarm Plot](../../how-to-guides/charts/swarmplot.ipynb) |
| [RaincloudPlot](raincloudplot.md) | A half violin, the raw points, and a box per group. | [`RaincloudDataPointAttrs`](raincloudplot.md#datachart.typings.RaincloudDataPointAttrs) | [`RaincloudStyleAttrs`](raincloudplot.md#datachart.typings.RaincloudStyleAttrs) | [Raincloud Plot](../../how-to-guides/charts/raincloudplot.ipynb) |
| [RidgelinePlot](ridgelineplot.md) | One density ridge per group, stacked and partly overlapping. | [`RidgelineDataPointAttrs`](ridgelineplot.md#datachart.typings.RidgelineDataPointAttrs) | [`RidgelineStyleAttrs`](ridgelineplot.md#datachart.typings.RidgelineStyleAttrs) | [Ridgeline Plot](../../how-to-guides/charts/ridgelineplot.ipynb) |

### Relationships

| Chart | Shows | Data | Style | Guide |
| :-- | :-- | :-- | :-- | :-- |
| [ScatterChart](scatterchart.md) | One point per observation, placed by two numeric variables. | [`ScatterDataPointAttrs`](scatterchart.md#datachart.typings.ScatterDataPointAttrs) | [`ScatterStyleAttrs`](scatterchart.md#datachart.typings.ScatterStyleAttrs) | [Scatter Chart](../../how-to-guides/charts/scatterchart.ipynb) |
| [Heatmap](heatmap.md) | A two-dimensional matrix as colored cells. | [`HeatmapDataAttrs`](heatmap.md#datachart.typings.HeatmapDataAttrs) | [`HeatmapStyleAttrs`](heatmap.md#datachart.typings.HeatmapStyleAttrs) | [Heatmap](../../how-to-guides/charts/heatmap.ipynb) |
| [ContourChart](contourchart.md) | A surface sampled on a grid, as iso-lines or filled bands. | [`ContourDataAttrs`](contourchart.md#datachart.typings.ContourDataAttrs) | [`ContourStyleAttrs`](contourchart.md#datachart.typings.ContourStyleAttrs) | [Contour Chart](../../how-to-guides/charts/contourchart.ipynb) |
| [HexbinChart](hexbinchart.md) | Point density on the plane, as colored hexagons. | [`HexbinDataAttrs`](hexbinchart.md#datachart.typings.HexbinDataAttrs) | [`HexbinStyleAttrs`](hexbinchart.md#datachart.typings.HexbinStyleAttrs) | [Hexbin Chart](../../how-to-guides/charts/hexbinchart.ipynb) |
| [ParallelCoords](parallelcoords.md) | Each record as a polyline across one axis per dimension. | [`ParallelCoordsDataPointAttrs`](parallelcoords.md#datachart.typings.ParallelCoordsDataPointAttrs) | [`ParallelCoordsStyleAttrs`](parallelcoords.md#datachart.typings.ParallelCoordsStyleAttrs) | [Parallel Coordinates](../../how-to-guides/charts/parallelcoords.ipynb) |
| [NetworkChart](networkchart.md) | Nodes joined by edges, placed by a layout. | [`NetworkSingleChartAttrs`](networkchart.md#datachart.typings.NetworkSingleChartAttrs) | [`NetworkStyleAttrs`](networkchart.md#datachart.typings.NetworkStyleAttrs) | [Network Chart](../../how-to-guides/charts/networkchart.ipynb) |
| [ScatterMatrix](scattermatrix.md) | A scatter chart for every pair of dimensions, distributions on the diagonal. | [`ScatterMatrixDataPointAttrs`](scattermatrix.md#datachart.typings.ScatterMatrixDataPointAttrs) | [`StyleAttrs`](../typings.md#datachart.typings.StyleAttrs) | [Scatter Matrix](../../how-to-guides/charts/scattermatrix.ipynb) |
| [ImageChart](imagechart.md) | A picture in data coordinates, under or over the other charts. | [`ImageDataAttrs`](imagechart.md#datachart.typings.ImageDataAttrs) | [`ImageStyleAttrs`](imagechart.md#datachart.typings.ImageStyleAttrs) | [Image Chart](../../how-to-guides/charts/imagechart.ipynb) |
| [BasemapChart](basemapchart.md) | Coastlines, land, borders and lakes under a chart of longitude and latitude. | [`BasemapDataAttrs`](basemapchart.md#datachart.typings.BasemapDataAttrs) | [`BasemapStyleAttrs`](basemapchart.md#datachart.typings.BasemapStyleAttrs) | [Basemap Chart](../../how-to-guides/charts/basemapchart.ipynb) |

### Flows

| Chart | Shows | Data | Style | Guide |
| :-- | :-- | :-- | :-- | :-- |
| [SankeyChart](sankeychart.md) | Weighted flows between categories, as ribbons between node columns. | [`SankeySingleChartAttrs`](sankeychart.md#datachart.typings.SankeySingleChartAttrs) | [`SankeyStyleAttrs`](sankeychart.md#datachart.typings.SankeyStyleAttrs) | [Sankey Chart](../../how-to-guides/charts/sankeychart.ipynb) |

### Part of a Whole

| Chart | Shows | Data | Style | Guide |
| :-- | :-- | :-- | :-- | :-- |
| [Treemap](treemap.md) | Part-of-whole data as nested rectangles sized by value. | [`TreemapSingleChartAttrs`](treemap.md#datachart.typings.TreemapSingleChartAttrs) | [`TreemapStyleAttrs`](treemap.md#datachart.typings.TreemapStyleAttrs) | [Treemap](../../how-to-guides/charts/treemap.ipynb) |
