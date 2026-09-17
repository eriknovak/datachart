---
title: Constants Module
---

# Constants Module

::: datachart.constants
    options:
        members: False
        heading_level: 2

## Constants by Chart

Which constants the parameters of each chart accept, by chart family. A constant used by one chart carries that chart's prefix; one shared across charts carries none. Style attributes take the constants named in their [typings](typings.md).

### Trends and Comparisons

| Chart | Chart-specific | Shared |
| :-- | :-- | :-- |
| [LineChart](charts/linechart.md#datachart.charts.LineChart) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [StackedAreaChart](charts/stackedareachart.md#datachart.charts.StackedAreaChart) | [`STACKED_AREA_BASELINE`](#datachart.constants.STACKED_AREA_BASELINE) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [BumpChart](charts/bumpchart.md#datachart.charts.BumpChart) | [`BUMP_RANK`](#datachart.constants.BUMP_RANK), [`BUMP_LABEL_POSITION`](#datachart.constants.BUMP_LABEL_POSITION) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [BarChart](charts/barchart.md#datachart.charts.BarChart) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`BAR_MODE`](#datachart.constants.BAR_MODE), [`SORT`](#datachart.constants.SORT), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [PyramidChart](charts/pyramidchart.md#datachart.charts.PyramidChart) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID) |
| [RadialChart](charts/radialchart.md#datachart.charts.RadialChart) | [`RADIAL_TYPE`](#datachart.constants.RADIAL_TYPE), [`RADIAL_DIRECTION`](#datachart.constants.RADIAL_DIRECTION) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`BAR_MODE`](#datachart.constants.BAR_MODE), [`SORT`](#datachart.constants.SORT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE) |
| [CalendarHeatmap](charts/calendarheatmap.md#datachart.charts.CalendarHeatmap) | [`CALENDAR_WEEKDAY`](#datachart.constants.CALENDAR_WEEKDAY) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION) |
| [GanttChart](charts/ganttchart.md#datachart.charts.GanttChart) | [`GANTT_DATE_PERIOD`](#datachart.constants.GANTT_DATE_PERIOD), [`GANTT_VALUE`](#datachart.constants.GANTT_VALUE), [`GANTT_SORT_KEY`](#datachart.constants.GANTT_SORT_KEY), [`GANTT_ARROW_ENTRY`](#datachart.constants.GANTT_ARROW_ENTRY) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID) |
| [DumbbellChart](charts/dumbbellchart.md#datachart.charts.DumbbellChart) | [`DUMBBELL_VALUE`](#datachart.constants.DUMBBELL_VALUE), [`DUMBBELL_SORT_KEY`](#datachart.constants.DUMBBELL_SORT_KEY) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LINE_MARKER`](#datachart.constants.LINE_MARKER), [`LINE_STYLE`](#datachart.constants.LINE_STYLE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE) |

### Distributions

| Chart | Chart-specific | Shared |
| :-- | :-- | :-- |
| [Histogram](charts/histogram.md#datachart.charts.Histogram) | [`HISTOGRAM_TYPE`](#datachart.constants.HISTOGRAM_TYPE) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`BAR_MODE`](#datachart.constants.BAR_MODE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [BoxPlot](charts/boxplot.md#datachart.charts.BoxPlot) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [ViolinPlot](charts/violinplot.md#datachart.charts.ViolinPlot) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VIOLIN_INNER`](#datachart.constants.VIOLIN_INNER), [`BANDWIDTH`](#datachart.constants.BANDWIDTH), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [SwarmPlot](charts/swarmplot.md#datachart.charts.SwarmPlot) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`SWARM_MODE`](#datachart.constants.SWARM_MODE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [RaincloudPlot](charts/raincloudplot.md#datachart.charts.RaincloudPlot) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`BANDWIDTH`](#datachart.constants.BANDWIDTH), [`SWARM_MODE`](#datachart.constants.SWARM_MODE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [RidgelinePlot](charts/ridgelineplot.md#datachart.charts.RidgelinePlot) | [`RIDGELINE_SCALE`](#datachart.constants.RIDGELINE_SCALE) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VIOLIN_INNER`](#datachart.constants.VIOLIN_INNER), [`BANDWIDTH`](#datachart.constants.BANDWIDTH), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |

### Relationships

| Chart | Chart-specific | Shared |
| :-- | :-- | :-- |
| [ScatterChart](charts/scatterchart.md#datachart.charts.ScatterChart) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [Heatmap](charts/heatmap.md#datachart.charts.Heatmap) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION) |
| [ContourChart](charts/contourchart.md#datachart.charts.ContourChart) | [`CONTOUR_LEVELS`](#datachart.constants.CONTOUR_LEVELS) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION) |
| [HexbinChart](charts/hexbinchart.md#datachart.charts.HexbinChart) | [`HEXBIN_REDUCE`](#datachart.constants.HEXBIN_REDUCE) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION) |
| [ParallelCoords](charts/parallelcoords.md#datachart.charts.ParallelCoords) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [NetworkChart](charts/networkchart.md#datachart.charts.NetworkChart) | [`NETWORK_LAYOUT`](#datachart.constants.NETWORK_LAYOUT), [`NETWORK_LABEL_POSITION`](#datachart.constants.NETWORK_LABEL_POSITION) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT) |
| [ScatterMatrix](charts/scattermatrix.md#datachart.charts.ScatterMatrix) | [`SCATTER_MATRIX_DIAGONAL`](#datachart.constants.SCATTER_MATRIX_DIAGONAL) | [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SHOW_GRID`](#datachart.constants.SHOW_GRID) |

### Flows

| Chart | Chart-specific | Shared |
| :-- | :-- | :-- |
| [SankeyChart](charts/sankeychart.md#datachart.charts.SankeyChart) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT) |

### Part of a Whole

| Chart | Chart-specific | Shared |
| :-- | :-- | :-- |
| [Treemap](charts/treemap.md#datachart.charts.Treemap) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT) |

## Figure Constants

::: datachart.constants.FIG_SIZE
    options:
        heading_level: 3

::: datachart.constants.FIG_FORMAT
    options:
        heading_level: 3

## Font Constants

::: datachart.constants.FONT_STYLE
    options:
        heading_level: 3

::: datachart.constants.FONT_WEIGHT
    options:
        heading_level: 3

## Line Constants

::: datachart.constants.LINE_MARKER
    options:
        heading_level: 3

::: datachart.constants.LINE_STYLE
    options:
        heading_level: 3

::: datachart.constants.LINE_DRAW_STYLE
    options:
        heading_level: 3

::: datachart.constants.ARROW_STYLE
    options:
        heading_level: 3

## Style Constants

::: datachart.constants.HATCH_STYLE
    options:
        heading_level: 3

::: datachart.constants.COLORS
    options:
        heading_level: 3

::: datachart.constants.THEME
    options:
        heading_level: 3

::: datachart.constants.EMPHASIS
    options:
        heading_level: 3

## Legend Constants

::: datachart.constants.LEGEND_ALIGN
    options:
        heading_level: 3

::: datachart.constants.LEGEND_LOCATION
    options:
        heading_level: 3

## Chart Constants

Constants several charts share.

::: datachart.constants.BAR_MODE
    options:
        heading_level: 3

::: datachart.constants.SORT
    options:
        heading_level: 3

::: datachart.constants.NORMALIZE
    options:
        heading_level: 3

::: datachart.constants.ORIENTATION
    options:
        heading_level: 3

::: datachart.constants.VIOLIN_INNER
    options:
        heading_level: 3

::: datachart.constants.BANDWIDTH
    options:
        heading_level: 3

::: datachart.constants.SWARM_MODE
    options:
        heading_level: 3

::: datachart.constants.VALUE_FORMAT
    options:
        heading_level: 3

::: datachart.constants.DATE_FORMAT
    options:
        heading_level: 3

::: datachart.constants.SHOW_GRID
    options:
        heading_level: 3

::: datachart.constants.SCALE
    options:
        heading_level: 3

::: datachart.constants.ASPECT_RATIO
    options:
        heading_level: 3

::: datachart.constants.COLORBAR_LOCATION
    options:
        heading_level: 3

## Chart-Specific Constants

Constants one chart owns, in the order of the [charts reference](charts/index.md).

::: datachart.constants.STACKED_AREA_BASELINE
    options:
        heading_level: 3

::: datachart.constants.BUMP_RANK
    options:
        heading_level: 3

::: datachart.constants.BUMP_LABEL_POSITION
    options:
        heading_level: 3

::: datachart.constants.RADIAL_TYPE
    options:
        heading_level: 3

::: datachart.constants.RADIAL_DIRECTION
    options:
        heading_level: 3

::: datachart.constants.CALENDAR_WEEKDAY
    options:
        heading_level: 3

::: datachart.constants.GANTT_DATE_PERIOD
    options:
        heading_level: 3

::: datachart.constants.GANTT_VALUE
    options:
        heading_level: 3

::: datachart.constants.GANTT_SORT_KEY
    options:
        heading_level: 3

::: datachart.constants.GANTT_ARROW_ENTRY
    options:
        heading_level: 3

::: datachart.constants.DUMBBELL_VALUE
    options:
        heading_level: 3

::: datachart.constants.DUMBBELL_SORT_KEY
    options:
        heading_level: 3

::: datachart.constants.HISTOGRAM_TYPE
    options:
        heading_level: 3

::: datachart.constants.RIDGELINE_SCALE
    options:
        heading_level: 3

::: datachart.constants.CONTOUR_LEVELS
    options:
        heading_level: 3

::: datachart.constants.HEXBIN_REDUCE
    options:
        heading_level: 3

::: datachart.constants.NETWORK_LAYOUT
    options:
        heading_level: 3

::: datachart.constants.NETWORK_LABEL_POSITION
    options:
        heading_level: 3

::: datachart.constants.SCATTER_MATRIX_DIAGONAL
    options:
        heading_level: 3
