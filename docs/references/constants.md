---
title: Constants Module
---

# Constants Module

::: datachart.constants
    options:
        members: False
        heading_level: 2

## Constants by Chart

Which constants the parameters of each chart accept. A constant used by one chart carries that chart's prefix; one shared across charts carries none. Style attributes take the constants named in their [typings](typings.md).

| Chart | Chart-specific | Shared |
| :-- | :-- | :-- |
| [LineChart](charts.md#datachart.charts.LineChart) | — | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`SCALE`](#datachart.constants.SCALE), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [StackedAreaChart](charts.md#datachart.charts.StackedAreaChart) | [`STACKED_AREA_BASELINE`](#datachart.constants.STACKED_AREA_BASELINE) | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`SCALE`](#datachart.constants.SCALE), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [BumpChart](charts.md#datachart.charts.BumpChart) | [`BUMP_RANK`](#datachart.constants.BUMP_RANK), [`BUMP_LABEL_POSITION`](#datachart.constants.BUMP_LABEL_POSITION) | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`SCALE`](#datachart.constants.SCALE), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [BarChart](charts.md#datachart.charts.BarChart) | — | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`BAR_MODE`](#datachart.constants.BAR_MODE), [`SORT`](#datachart.constants.SORT), [`SCALE`](#datachart.constants.SCALE), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [PyramidChart](charts.md#datachart.charts.PyramidChart) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`SORT`](#datachart.constants.SORT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [RadialChart](charts.md#datachart.charts.RadialChart) | [`RADIAL_TYPE`](#datachart.constants.RADIAL_TYPE), [`RADIAL_DIRECTION`](#datachart.constants.RADIAL_DIRECTION) | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`BAR_MODE`](#datachart.constants.BAR_MODE), [`SORT`](#datachart.constants.SORT), [`SCALE`](#datachart.constants.SCALE) |
| [CalendarHeatmap](charts.md#datachart.charts.CalendarHeatmap) | [`CALENDAR_WEEKDAY`](#datachart.constants.CALENDAR_WEEKDAY) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION) |
| [GanttChart](charts.md#datachart.charts.GanttChart) | [`GANTT_DATE_PERIOD`](#datachart.constants.GANTT_DATE_PERIOD), [`GANTT_VALUE`](#datachart.constants.GANTT_VALUE), [`GANTT_SORT_KEY`](#datachart.constants.GANTT_SORT_KEY), [`GANTT_ARROW_ENTRY`](#datachart.constants.GANTT_ARROW_ENTRY) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`SORT`](#datachart.constants.SORT), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [DumbbellChart](charts.md#datachart.charts.DumbbellChart) | [`DUMBBELL_VALUE`](#datachart.constants.DUMBBELL_VALUE), [`DUMBBELL_SORT_KEY`](#datachart.constants.DUMBBELL_SORT_KEY) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`SCALE`](#datachart.constants.SCALE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`SORT`](#datachart.constants.SORT), [`LINE_MARKER`](#datachart.constants.LINE_MARKER), [`LINE_STYLE`](#datachart.constants.LINE_STYLE), [`EMPHASIS`](#datachart.constants.EMPHASIS) |
| [Histogram](charts.md#datachart.charts.Histogram) | [`HISTOGRAM_TYPE`](#datachart.constants.HISTOGRAM_TYPE) | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`BAR_MODE`](#datachart.constants.BAR_MODE), [`SCALE`](#datachart.constants.SCALE) |
| [BoxPlot](charts.md#datachart.charts.BoxPlot) | — | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`SCALE`](#datachart.constants.SCALE), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [ViolinPlot](charts.md#datachart.charts.ViolinPlot) | — | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`SCALE`](#datachart.constants.SCALE), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`VIOLIN_INNER`](#datachart.constants.VIOLIN_INNER), [`BANDWIDTH`](#datachart.constants.BANDWIDTH) |
| [SwarmPlot](charts.md#datachart.charts.SwarmPlot) | — | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SWARM_MODE`](#datachart.constants.SWARM_MODE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`SCALE`](#datachart.constants.SCALE), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [RaincloudPlot](charts.md#datachart.charts.RaincloudPlot) | — | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`SWARM_MODE`](#datachart.constants.SWARM_MODE), [`BANDWIDTH`](#datachart.constants.BANDWIDTH), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`SCALE`](#datachart.constants.SCALE), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [RidgelinePlot](charts.md#datachart.charts.RidgelinePlot) | [`RIDGELINE_SCALE`](#datachart.constants.RIDGELINE_SCALE) | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`SCALE`](#datachart.constants.SCALE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`BANDWIDTH`](#datachart.constants.BANDWIDTH), [`VIOLIN_INNER`](#datachart.constants.VIOLIN_INNER), [`SORT`](#datachart.constants.SORT) |
| [ScatterChart](charts.md#datachart.charts.ScatterChart) | — | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`SCALE`](#datachart.constants.SCALE), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT) |
| [Heatmap](charts.md#datachart.charts.Heatmap) | — | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION) |
| [ContourChart](charts.md#datachart.charts.ContourChart) | [`CONTOUR_LEVELS`](#datachart.constants.CONTOUR_LEVELS) | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`SCALE`](#datachart.constants.SCALE), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION) |
| [HexbinChart](charts.md#datachart.charts.HexbinChart) | [`HEXBIN_REDUCE`](#datachart.constants.HEXBIN_REDUCE) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`SCALE`](#datachart.constants.SCALE), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION) |
| [ParallelCoords](charts.md#datachart.charts.ParallelCoords) | — | [`EMPHASIS`](#datachart.constants.EMPHASIS), [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [NetworkChart](charts.md#datachart.charts.NetworkChart) | [`NETWORK_LAYOUT`](#datachart.constants.NETWORK_LAYOUT), [`NODE_LABEL_POSITION`](#datachart.constants.NODE_LABEL_POSITION) | [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`FIG_SIZE`](#datachart.constants.FIG_SIZE) |
| [ScatterMatrix](charts.md#datachart.charts.ScatterMatrix) | [`SCATTER_MATRIX_DIAGONAL`](#datachart.constants.SCATTER_MATRIX_DIAGONAL) | [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`SHOW_GRID`](#datachart.constants.SHOW_GRID) |
| [SankeyChart](charts.md#datachart.charts.SankeyChart) | — | [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`FIG_SIZE`](#datachart.constants.FIG_SIZE) |
| [Treemap](charts.md#datachart.charts.Treemap) | — | [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`FIG_SIZE`](#datachart.constants.FIG_SIZE) |

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

Constants one chart owns, in the order of the [charts reference](charts.md).

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

::: datachart.constants.NODE_LABEL_POSITION
    options:
        heading_level: 3

::: datachart.constants.SCATTER_MATRIX_DIAGONAL
    options:
        heading_level: 3
