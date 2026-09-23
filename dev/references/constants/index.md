# Constants Module

## datachart.constants

Module containing the `constants`.

The `constants` module provides a set of predefined constants used in the package. These include figure size, format, style, and other figure manipulation values.

**Figure Constants**

| CLASS        | DESCRIPTION                   |
| ------------ | ----------------------------- |
| `FIG_SIZE`   | The predefined figure sizes.  |
| `FIG_FORMAT` | The supported figure formats. |

**Font Constants**

| CLASS         | DESCRIPTION                 |
| ------------- | --------------------------- |
| `FONT_STYLE`  | The supported font styles.  |
| `FONT_WEIGHT` | The supported font weights. |

**Line Constants**

| CLASS             | DESCRIPTION                                    |
| ----------------- | ---------------------------------------------- |
| `LINE_MARKER`     | The supported line markers.                    |
| `LINE_STYLE`      | The supported line styles.                     |
| `LINE_DRAW_STYLE` | The supported line draw styles.                |
| `ARROW_STYLE`     | The supported text annotation connector looks. |

**Style Constants**

| CLASS         | DESCRIPTION                   |
| ------------- | ----------------------------- |
| `HATCH_STYLE` | The supported hatch styles.   |
| `COLORS`      | The predefined colors.        |
| `THEME`       | The predefined themes.        |
| `EMPHASIS`    | The supported emphasis roles. |

**Legend Constants**

| CLASS             | DESCRIPTION                      |
| ----------------- | -------------------------------- |
| `LEGEND_ALIGN`    | The supported legend alignments. |
| `LEGEND_LOCATION` | The supported legend locations.  |

**Chart Constants**

| CLASS               | DESCRIPTION                                            |
| ------------------- | ------------------------------------------------------ |
| `BAR_MODE`          | The supported bar modes.                               |
| `SORT`              | The supported category sort orders.                    |
| `NORMALIZE`         | The supported normalization options.                   |
| `ORIENTATION`       | The supported orientations.                            |
| `VIOLIN_INNER`      | The supported violin inner marks.                      |
| `BANDWIDTH`         | The supported kernel density bandwidth rules.          |
| `SWARM_MODE`        | The supported swarm plot modes.                        |
| `VALUE_FORMAT`      | The predefined value formats.                          |
| `DATE_FORMAT`       | The predefined date formats.                           |
| `SHOW_GRID`         | The supported show grid options.                       |
| `SCALE`             | The supported scale options.                           |
| `ASPECT_RATIO`      | The supported aspect ratio options.                    |
| `COLORBAR_LOCATION` | The supported colorbar locations.                      |
| `DRAW_POSITION`     | The supported draw positions of the image and basemap. |

**Chart-Specific Constants**

| CLASS                     | DESCRIPTION                                   |
| ------------------------- | --------------------------------------------- |
| `STACKED_AREA_BASELINE`   | The supported stacked area baselines.         |
| `BUMP_RANK`               | The supported bump chart ranking rules.       |
| `BUMP_LABEL_POSITION`     | The supported end label positions.            |
| `RADIAL_TYPE`             | The supported radial chart visuals.           |
| `RADIAL_DIRECTION`        | The supported angular directions.             |
| `CALENDAR_WEEKDAY`        | The supported week start days.                |
| `GANTT_DATE_PERIOD`       | The supported date axis periods.              |
| `GANTT_VALUE`             | The supported gantt chart value labels.       |
| `GANTT_SORT_KEY`          | The supported gantt chart sort keys.          |
| `GANTT_ARROW_ENTRY`       | The supported gantt dependency arrow entries. |
| `DUMBBELL_VALUE`          | The supported dumbbell chart value labels.    |
| `DUMBBELL_SORT_KEY`       | The supported dumbbell chart sort keys.       |
| `HISTOGRAM_TYPE`          | The supported histogram types.                |
| `RIDGELINE_SCALE`         | The supported ridgeline density scales.       |
| `CONTOUR_LEVELS`          | The supported contour level rules.            |
| `HEXBIN_REDUCE`           | The supported hexbin aggregations.            |
| `NETWORK_LAYOUT`          | The supported network chart layouts.          |
| `NETWORK_LABEL_POSITION`  | The supported network node label positions.   |
| `SCATTER_MATRIX_DIAGONAL` | The supported scatter matrix diagonal cells.  |
| `BASEMAP_FEATURE`         | The supported basemap features.               |
| `BASEMAP_RESOLUTION`      | The supported basemap outline resolutions.    |

## Constants by Chart

Which constants the parameters of each chart accept, by chart family. A constant used by one chart carries that chart's prefix; one shared across charts carries none. Style attributes take the constants named in their [typings](https://eriknovak.github.io/datachart/dev/references/typings/index.md).

### Trends and Comparisons

| Chart                                                                                                                               | Chart-specific                                                                                                                                                                                                                           | Shared                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [LineChart](https://eriknovak.github.io/datachart/dev/references/charts/linechart/#datachart.charts.LineChart)                      | —                                                                                                                                                                                                                                        | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO)                                                                                                                                      |
| [StackedAreaChart](https://eriknovak.github.io/datachart/dev/references/charts/stackedareachart/#datachart.charts.StackedAreaChart) | [`STACKED_AREA_BASELINE`](#datachart.constants.STACKED_AREA_BASELINE)                                                                                                                                                                    | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO)                                                                                                                                      |
| [BumpChart](https://eriknovak.github.io/datachart/dev/references/charts/bumpchart/#datachart.charts.BumpChart)                      | [`BUMP_RANK`](#datachart.constants.BUMP_RANK), [`BUMP_LABEL_POSITION`](#datachart.constants.BUMP_LABEL_POSITION)                                                                                                                         | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO)                                                                                                                                      |
| [BarChart](https://eriknovak.github.io/datachart/dev/references/charts/barchart/#datachart.charts.BarChart)                         | —                                                                                                                                                                                                                                        | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`BAR_MODE`](#datachart.constants.BAR_MODE), [`SORT`](#datachart.constants.SORT), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [PyramidChart](https://eriknovak.github.io/datachart/dev/references/charts/pyramidchart/#datachart.charts.PyramidChart)             | —                                                                                                                                                                                                                                        | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID)                                                                                                                                                                                                                                          |
| [RadialChart](https://eriknovak.github.io/datachart/dev/references/charts/radialchart/#datachart.charts.RadialChart)                | [`RADIAL_TYPE`](#datachart.constants.RADIAL_TYPE), [`RADIAL_DIRECTION`](#datachart.constants.RADIAL_DIRECTION)                                                                                                                           | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`BAR_MODE`](#datachart.constants.BAR_MODE), [`SORT`](#datachart.constants.SORT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE)                                                                                                                                                                                                                 |
| [CalendarHeatmap](https://eriknovak.github.io/datachart/dev/references/charts/calendarheatmap/#datachart.charts.CalendarHeatmap)    | [`CALENDAR_WEEKDAY`](#datachart.constants.CALENDAR_WEEKDAY)                                                                                                                                                                              | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION)                                                                                                                                                                                                                                                                           |
| [GanttChart](https://eriknovak.github.io/datachart/dev/references/charts/ganttchart/#datachart.charts.GanttChart)                   | [`GANTT_DATE_PERIOD`](#datachart.constants.GANTT_DATE_PERIOD), [`GANTT_VALUE`](#datachart.constants.GANTT_VALUE), [`GANTT_SORT_KEY`](#datachart.constants.GANTT_SORT_KEY), [`GANTT_ARROW_ENTRY`](#datachart.constants.GANTT_ARROW_ENTRY) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID)                                                                                                                                                                                             |
| [DumbbellChart](https://eriknovak.github.io/datachart/dev/references/charts/dumbbellchart/#datachart.charts.DumbbellChart)          | [`DUMBBELL_VALUE`](#datachart.constants.DUMBBELL_VALUE), [`DUMBBELL_SORT_KEY`](#datachart.constants.DUMBBELL_SORT_KEY)                                                                                                                   | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LINE_MARKER`](#datachart.constants.LINE_MARKER), [`LINE_STYLE`](#datachart.constants.LINE_STYLE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE)                                                  |

### Distributions

| Chart                                                                                                                      | Chart-specific                                            | Shared                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Histogram](https://eriknovak.github.io/datachart/dev/references/charts/histogram/#datachart.charts.Histogram)             | [`HISTOGRAM_TYPE`](#datachart.constants.HISTOGRAM_TYPE)   | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`BAR_MODE`](#datachart.constants.BAR_MODE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO)                                                                                                                                                |
| [BoxPlot](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/#datachart.charts.BoxPlot)                   | —                                                         | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO)                                                                                                     |
| [ViolinPlot](https://eriknovak.github.io/datachart/dev/references/charts/violinplot/#datachart.charts.ViolinPlot)          | —                                                         | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VIOLIN_INNER`](#datachart.constants.VIOLIN_INNER), [`BANDWIDTH`](#datachart.constants.BANDWIDTH), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |
| [SwarmPlot](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/#datachart.charts.SwarmPlot)             | —                                                         | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`SWARM_MODE`](#datachart.constants.SWARM_MODE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO)                                                                                         |
| [RaincloudPlot](https://eriknovak.github.io/datachart/dev/references/charts/raincloudplot/#datachart.charts.RaincloudPlot) | —                                                         | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`BANDWIDTH`](#datachart.constants.BANDWIDTH), [`SWARM_MODE`](#datachart.constants.SWARM_MODE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO)                                          |
| [RidgelinePlot](https://eriknovak.github.io/datachart/dev/references/charts/ridgelineplot/#datachart.charts.RidgelinePlot) | [`RIDGELINE_SCALE`](#datachart.constants.RIDGELINE_SCALE) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SORT`](#datachart.constants.SORT), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VIOLIN_INNER`](#datachart.constants.VIOLIN_INNER), [`BANDWIDTH`](#datachart.constants.BANDWIDTH), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO) |

### Relationships

| Chart                                                                                                                         | Chart-specific                                                                                                                   | Shared                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ScatterChart](https://eriknovak.github.io/datachart/dev/references/charts/scatterchart/#datachart.charts.ScatterChart)       | —                                                                                                                                | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO)                                                                                                                                                                  |
| [Heatmap](https://eriknovak.github.io/datachart/dev/references/charts/heatmap/#datachart.charts.Heatmap)                      | —                                                                                                                                | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION)                                                                                     |
| [ContourChart](https://eriknovak.github.io/datachart/dev/references/charts/contourchart/#datachart.charts.ContourChart)       | [`CONTOUR_LEVELS`](#datachart.constants.CONTOUR_LEVELS)                                                                          | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION) |
| [HexbinChart](https://eriknovak.github.io/datachart/dev/references/charts/hexbinchart/#datachart.charts.HexbinChart)          | [`HEXBIN_REDUCE`](#datachart.constants.HEXBIN_REDUCE)                                                                            | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`NORMALIZE`](#datachart.constants.NORMALIZE), [`ORIENTATION`](#datachart.constants.ORIENTATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](#datachart.constants.DATE_FORMAT), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`SCALE`](#datachart.constants.SCALE), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`COLORBAR_LOCATION`](#datachart.constants.COLORBAR_LOCATION)                                              |
| [ParallelCoords](https://eriknovak.github.io/datachart/dev/references/charts/parallelcoords/#datachart.charts.ParallelCoords) | —                                                                                                                                | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`EMPHASIS`](#datachart.constants.EMPHASIS), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO)                                                                                                                                                                                                                                                                                                                 |
| [NetworkChart](https://eriknovak.github.io/datachart/dev/references/charts/networkchart/#datachart.charts.NetworkChart)       | [`NETWORK_LAYOUT`](#datachart.constants.NETWORK_LAYOUT), [`NETWORK_LABEL_POSITION`](#datachart.constants.NETWORK_LABEL_POSITION) | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT)                                                                                                                                                                                                                                                                                                                                                                                                             |
| [ScatterMatrix](https://eriknovak.github.io/datachart/dev/references/charts/scattermatrix/#datachart.charts.ScatterMatrix)    | [`SCATTER_MATRIX_DIAGONAL`](#datachart.constants.SCATTER_MATRIX_DIAGONAL)                                                        | [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`SHOW_GRID`](#datachart.constants.SHOW_GRID)                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [ImageChart](https://eriknovak.github.io/datachart/dev/references/charts/imagechart/#datachart.charts.ImageChart)             | —                                                                                                                                | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`DRAW_POSITION`](#datachart.constants.DRAW_POSITION)                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [BasemapChart](https://eriknovak.github.io/datachart/dev/references/charts/basemapchart/#datachart.charts.BasemapChart)       | [`BASEMAP_FEATURE`](#datachart.constants.BASEMAP_FEATURE), [`BASEMAP_RESOLUTION`](#datachart.constants.BASEMAP_RESOLUTION)       | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`SHOW_GRID`](#datachart.constants.SHOW_GRID), [`ASPECT_RATIO`](#datachart.constants.ASPECT_RATIO), [`DRAW_POSITION`](#datachart.constants.DRAW_POSITION)                                                                                                                                                                                                                                                                                                                                                                                                                       |

### Flows

| Chart                                                                                                                | Chart-specific | Shared                                                                                           |
| -------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| [SankeyChart](https://eriknovak.github.io/datachart/dev/references/charts/sankeychart/#datachart.charts.SankeyChart) | —              | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT) |

### Part of a Whole

| Chart                                                                                                    | Chart-specific | Shared                                                                                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Treemap](https://eriknovak.github.io/datachart/dev/references/charts/treemap/#datachart.charts.Treemap) | —              | [`FIG_SIZE`](#datachart.constants.FIG_SIZE), [`LEGEND_ALIGN`](#datachart.constants.LEGEND_ALIGN), [`LEGEND_LOCATION`](#datachart.constants.LEGEND_LOCATION), [`VALUE_FORMAT`](#datachart.constants.VALUE_FORMAT) |

## Figure Constants

### datachart.constants.FIG_SIZE

The predefined figure sizes.

All values are `(width, height)` in inches, matplotlib's `figsize` unit. Paper figures are anchored to the printable area of an A4 page with standard 2.5 cm margins — a 6.3 x 9.7 in (16.0 x 24.6 cm) text block. `FULL` spans the text-block width; `HALF` spans one of two columns separated by a 0.3 in (0.8 cm) gap (3.0 in / 7.6 cm each). Widths cross with a height — `SHORT` (2.4 in / 6.1 cm), `MEDIUM` (4.8 in / 12.2 cm), or `TALL` (7.2 in / 18.3 cm). Passed as the `figsize` chart setting.

Examples:

```
>>> from datachart.constants import FIG_SIZE
>>> FIG_SIZE.DEFAULT
(6.4, 4.8)
```

| ATTRIBUTE      | DESCRIPTION                                                                                                                        |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT`      | The default figure size. Equals to (6.4, 4.8) in (16.3 x 12.2 cm). **TYPE:** `Tuple[float, float]`                                 |
| `FULL_SHORT`   | The short, full-width figure size. Equals to (6.3, 2.4) in (16.0 x 6.1 cm). **TYPE:** `Tuple[float, float]`                        |
| `FULL_MEDIUM`  | The medium, full-width figure size. Equals to (6.3, 4.8) in (16.0 x 12.2 cm). **TYPE:** `Tuple[float, float]`                      |
| `FULL_TALL`    | The tall, full-width figure size. Equals to (6.3, 7.2) in (16.0 x 18.3 cm). **TYPE:** `Tuple[float, float]`                        |
| `HALF_SHORT`   | The short, half-width figure size. Equals to (3.0, 2.4) in (7.6 x 6.1 cm). **TYPE:** `Tuple[float, float]`                         |
| `HALF_MEDIUM`  | The medium, half-width figure size. Equals to (3.0, 4.8) in (7.6 x 12.2 cm). **TYPE:** `Tuple[float, float]`                       |
| `HALF_TALL`    | The tall, half-width figure size. Equals to (3.0, 7.2) in (7.6 x 18.3 cm). **TYPE:** `Tuple[float, float]`                         |
| `HALF_SQUARE`  | The square, half-width figure size. Equals to (3.0, 3.0) in (7.6 x 7.6 cm). **TYPE:** `Tuple[float, float]`                        |
| `A4_PORTRAIT`  | The A4 portrait printable-area figure size. Equals to (6.3, 9.7) in (16.0 x 24.6 cm). **TYPE:** `Tuple[float, float]`              |
| `A4_LANDSCAPE` | The A4 landscape printable-area figure size. Equals to (9.7, 6.3) in (24.6 x 16.0 cm). **TYPE:** `Tuple[float, float]`             |
| `SQUARE`       | The square figure size. Equals to (4.8, 4.8) in (12.2 x 12.2 cm). **TYPE:** `Tuple[float, float]`                                  |
| `SLIDE_16_9`   | The 16:9 slide figure size (PowerPoint/Google Slides). Equals to (13.33, 7.5) in (33.9 x 19.1 cm). **TYPE:** `Tuple[float, float]` |
| `SLIDE_4_3`    | The 4:3 slide figure size (PowerPoint/Google Slides). Equals to (10.0, 7.5) in (25.4 x 19.1 cm). **TYPE:** `Tuple[float, float]`   |
| `BEAMER_16_9`  | The 16:9 beamer frame figure size. Equals to (6.3, 3.54) in (16.0 x 9.0 cm). **TYPE:** `Tuple[float, float]`                       |
| `BEAMER_4_3`   | The 4:3 beamer frame figure size. Equals to (5.04, 3.78) in (12.8 x 9.6 cm). **TYPE:** `Tuple[float, float]`                       |

### datachart.constants.FIG_FORMAT

The supported figure formats.

Passed as the `format` argument of save_figure.

Examples:

```
>>> from datachart.constants import FIG_FORMAT
>>> FIG_FORMAT.DEFAULT
"png"
```

| ATTRIBUTE | DESCRIPTION                                                                |
| --------- | -------------------------------------------------------------------------- |
| `DEFAULT` | The default format. Same as FIG_FORMAT.PNG. **TYPE:** `str`                |
| `SVG`     | The svg format. Equals to "svg". **TYPE:** `str`                           |
| `PDF`     | The pdf format. Equals to "pdf". **TYPE:** `str`                           |
| `PNG`     | The png format. Equals to "png". **TYPE:** `str`                           |
| `WEBP`    | The webp format. Equals to "webp". **TYPE:** `str`                         |
| `EPS`     | The eps format (Encapsulated PostScript). Equals to "eps". **TYPE:** `str` |
| `JPG`     | The jpg format. Equals to "jpg". **TYPE:** `str`                           |
| `TIFF`    | The tiff format. Equals to "tiff". **TYPE:** `str`                         |

## Font Constants

### datachart.constants.FONT_STYLE

The supported font styles.

Examples:

```
>>> from datachart.constants import FONT_STYLE
>>> FONT_STYLE.DEFAULT
"normal"
```

| ATTRIBUTE | DESCRIPTION                                                        |
| --------- | ------------------------------------------------------------------ |
| `DEFAULT` | The default font style. Same as FONT_STYLE.NORMAL. **TYPE:** `str` |
| `NORMAL`  | The normal font style. Equals to "normal". **TYPE:** `str`         |
| `ITALIC`  | The italic font style. Equals to "italic". **TYPE:** `str`         |
| `OBLIQUE` | The oblique font style. Equals to "oblique". **TYPE:** `str`       |

### datachart.constants.FONT_WEIGHT

The supported font weights.

Used by the `font_*_weight` style attributes (general, title, subtitle, axis labels).

Examples:

```
>>> from datachart.constants import FONT_WEIGHT
>>> FONT_WEIGHT.DEFAULT
"normal"
```

| ATTRIBUTE     | DESCRIPTION                                                          |
| ------------- | -------------------------------------------------------------------- |
| `DEFAULT`     | The default font weight. Same as FONT_WEIGHT.NORMAL. **TYPE:** `str` |
| `ULTRA_LIGHT` | The ultra light font weight. Equals to "ultralight". **TYPE:** `str` |
| `LIGHT`       | The light font weight. Equals to "light". **TYPE:** `str`            |
| `NORMAL`      | The normal font weight. Equals to "normal". **TYPE:** `str`          |
| `MEDIUM`      | The medium font weight. Equals to "medium". **TYPE:** `str`          |
| `SEMIBOLD`    | The semibold font weight. Equals to "semibold". **TYPE:** `str`      |
| `BOLD`        | The bold font weight. Equals to "bold". **TYPE:** `str`              |
| `EXTRA_BOLD`  | The extra bold font weight. Equals to "extra bold". **TYPE:** `str`  |
| `HEAVY`       | The heavy font weight. Equals to "heavy". **TYPE:** `str`            |
| `BLACK`       | The black font weight. Equals to "black". **TYPE:** `str`            |

## Line Constants

### datachart.constants.LINE_MARKER

The supported line markers.

Used by the `plot_line_marker` (line charts) and `plot_scatter_marker` (scatter charts) style attributes.

Examples:

```
>>> from datachart.constants import LINE_MARKER
>>> LINE_MARKER.PIXEL
","
```

| ATTRIBUTE        | DESCRIPTION                                                    |
| ---------------- | -------------------------------------------------------------- |
| `NONE`           | No marker. Equals to "". **TYPE:** `str`                       |
| `PIXEL`          | The pixel line marker. Equals to ",". **TYPE:** `str`          |
| `POINT`          | The point line marker. Equals to ".". **TYPE:** `str`          |
| `CIRCLE`         | The circle line marker. Equals to "o". **TYPE:** `str`         |
| `DIAMOND`        | The diamond line marker. Equals to "D". **TYPE:** `str`        |
| `THIN_DIAMOND`   | The thin diamond line marker. Equals to "d". **TYPE:** `str`   |
| `TRIANGLE`       | The triangle (up) line marker. Equals to "^". **TYPE:** `str`  |
| `TRIANGLE_DOWN`  | The triangle down line marker. Equals to "v". **TYPE:** `str`  |
| `TRIANGLE_LEFT`  | The triangle left line marker. Equals to "\<". **TYPE:** `str` |
| `TRIANGLE_RIGHT` | The triangle right line marker. Equals to ">". **TYPE:** `str` |
| `SQUARE`         | The square line marker. Equals to "s". **TYPE:** `str`         |
| `PENTAGON`       | The pentagon line marker. Equals to "p". **TYPE:** `str`       |
| `HEXAGON`        | The hexagon line marker. Equals to "h". **TYPE:** `str`        |
| `STAR`           | The star line marker. Equals to "\*". **TYPE:** `str`          |
| `CROSS`          | The cross line marker. Equals to "x". **TYPE:** `str`          |
| `PLUS`           | The plus line marker. Equals to "+". **TYPE:** `str`           |
| `VLINE`          | The vertical line marker. Equals to "                          |
| `HLINE`          | The horizontal line marker. Equals to "\_". **TYPE:** `str`    |

### datachart.constants.LINE_STYLE

The supported line styles.

Used by the `plot_line_style` style attribute of line charts.

Examples:

```
>>> from datachart.constants import LINE_STYLE
>>> LINE_STYLE.SOLID
"-"
```

| ATTRIBUTE | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `NONE`    | No line style. Equals to "". **TYPE:** `str`            |
| `SOLID`   | The solid line style. Equals to "-". **TYPE:** `str`    |
| `DASHED`  | The dashed line style. Equals to "--". **TYPE:** `str`  |
| `DASHDOT` | The dashdot line style. Equals to "-.". **TYPE:** `str` |
| `DOTTED`  | The dotted line style. Equals to ":". **TYPE:** `str`   |

### datachart.constants.LINE_DRAW_STYLE

The supported line draw styles.

Used by the `plot_line_drawstyle` style attribute of line charts.

Examples:

```
>>> from datachart.constants import LINE_DRAW_STYLE
>>> LINE_DRAW_STYLE.DEFAULT
"default"
```

| ATTRIBUTE    | DESCRIPTION                                                             |
| ------------ | ----------------------------------------------------------------------- |
| `DEFAULT`    | The default line draw style. Equals to "default". **TYPE:** `str`       |
| `STEPS_PRE`  | The pre-steps line draw style. Equals to "steps-pre". **TYPE:** `str`   |
| `STEPS_MID`  | The mid-steps line draw style. Equals to "steps-mid". **TYPE:** `str`   |
| `STEPS_POST` | The post-steps line draw style. Equals to "steps-post". **TYPE:** `str` |

### datachart.constants.ARROW_STYLE

The supported connector looks.

The one constant for every drawn connector: the `plot_text_arrow_style` style attribute of text annotations and the `plot_network_edge_style` style attribute of network charts. Each value names a complete connector look — the line shape, curvature, and the gap on the text side. For an annotation, a curved look bows toward the side with the most open space around the chart's data; `plot_text_arrow_curve` pins the bow exactly, and the other `plot_text_arrow_*` style attributes override single properties of the chosen look. A raw matplotlib arrow style string (e.g. `"-|>"`) is also accepted. A network edge takes only the two headless looks, `CURVE` and `STRAIGHT`, bowed by `plot_network_edge_curve`; its arrowhead comes from the chart's `directed` argument.

Examples:

```
>>> from datachart.constants import ARROW_STYLE
>>> ARROW_STYLE.CURVE
"curve"
```

| ATTRIBUTE     | DESCRIPTION                                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `CURVE`       | A curved plain line with a small text-side gap. The default. Text annotations and network edges. Equals to "curve". **TYPE:** `str` |
| `CURVE_ARROW` | The same curve with an arrowhead at the target. Text annotations only. Equals to "curve-arrow". **TYPE:** `str`                     |
| `STRAIGHT`    | A straight plain line with a small text-side gap. Text annotations and network edges. Equals to "straight". **TYPE:** `str`         |
| `TOUCHING`    | A straight plain line starting flush at the text box border. Text annotations only. Equals to "touching". **TYPE:** `str`           |
| `ARROW`       | A straight line with an arrowhead at the target. Text annotations only. Equals to "arrow". **TYPE:** `str`                          |

## Style Constants

### datachart.constants.HATCH_STYLE

The supported hatch styles.

Used by the `plot_bar_hatch` and `plot_hist_hatch` style attributes, and by the `HATCH` theme's hatch cycle.

Examples:

```
>>> from datachart.constants import HATCH_STYLE
>>> HATCH_STYLE.DEFAULT
None
```

| ATTRIBUTE          | DESCRIPTION                                                      |
| ------------------ | ---------------------------------------------------------------- |
| `DEFAULT`          | The default hatch style. Equals to None. **TYPE:** `str`         |
| `DIAGONAL`         | The diagonal hatch style. Equals to "/". **TYPE:** `str`         |
| `BACK_DIAGONAL`    | The back diagonal hatch style. Equals to "\\". **TYPE:** `str`   |
| `VERTICAL`         | The vertical hatch style. Equals to "                            |
| `HORIZONTAL`       | The horizontal hatch style. Equals to "-". **TYPE:** `str`       |
| `CROSSED`          | The crossed hatch style. Equals to "+". **TYPE:** `str`          |
| `CROSSED_DIAGONAL` | The crossed diagonal hatch style. Equals to "x". **TYPE:** `str` |
| `DOTS`             | The dots hatch style. Equals to ".". **TYPE:** `str`             |
| `CIRCLES`          | The circles hatch style. Equals to "o". **TYPE:** `str`          |
| `STARS`            | The stars hatch style. Equals to "\*". **TYPE:** `str`           |

### datachart.constants.COLORS

The predefined colors using [pypalettes](https://y-sunflower.github.io/pypalettes/).

All palette names are valid pypalettes identifiers. You can use any of the 2500+ palettes available in pypalettes by passing the palette name as a string. Accepted anywhere a palette is: the `color_general_singular` and `color_general_multiple` config attributes, and the heatmap and parallel coords color settings. All predefined palettes are rendered in the [Colormaps guide](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/colormaps/index.md).

A single matplotlib color (`"#B5651D"`, `"tab:blue"`, `"rebeccapurple"`) is accepted in the same places and is used as a palette of one, repeated for every series that asks for a color. A name that is both a palette and a color, such as `"Red"` or `"pink"`, is read as the palette.

Examples:

```
>>> from datachart.constants import COLORS
>>> COLORS.Blues
'Blues'
```

| ATTRIBUTE        | DESCRIPTION                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| `Blues`          | Sequential blue palette. Equals to "Blues". **TYPE:** `str`                                       |
| `Greens`         | Sequential green palette. Equals to "Greens". **TYPE:** `str`                                     |
| `Oranges`        | Sequential orange palette. Equals to "Oranges". **TYPE:** `str`                                   |
| `Purples`        | Sequential purple palette. Equals to "Purples". **TYPE:** `str`                                   |
| `Reds`           | Sequential red palette. Equals to "Reds". **TYPE:** `str`                                         |
| `Sunset2`        | Multi-hue sunset palette. Equals to "Sunset2". **TYPE:** `str`                                    |
| `YlGnBu`         | Multi-hue yellow-green-blue palette. Equals to "YlGnBu". **TYPE:** `str`                          |
| `YlOrRd`         | Multi-hue yellow-orange-red palette. Equals to "YlOrRd". **TYPE:** `str`                          |
| `YlOrBr`         | Multi-hue yellow-orange-brown palette. Equals to "YlOrBr". **TYPE:** `str`                        |
| `PuBuGn`         | Multi-hue purple-blue-green palette. Equals to "PuBuGn". **TYPE:** `str`                          |
| `GnBu`           | Multi-hue green-blue palette. Equals to "GnBu". **TYPE:** `str`                                   |
| `BuPu`           | Multi-hue blue-purple palette. Equals to "BuPu". **TYPE:** `str`                                  |
| `PuBu`           | Multi-hue purple-blue palette. Equals to "PuBu". **TYPE:** `str`                                  |
| `Egypt`          | Multi-hue Egypt palette. Equals to "Egypt". **TYPE:** `str`                                       |
| `Hiroshige`      | Multi-hue Hiroshige palette. Equals to "Hiroshige". **TYPE:** `str`                               |
| `Lake`           | Multi-hue lake palette. Equals to "Lake". **TYPE:** `str`                                         |
| `Neon`           | Multi-hue neon palette. Equals to "Neon". **TYPE:** `str`                                         |
| `RdBu`           | Diverging red-blue palette. Equals to "RdBu". **TYPE:** `str`                                     |
| `BrBG`           | Diverging brown-blue-green palette. Equals to "BrBG". **TYPE:** `str`                             |
| `PuOr`           | Diverging purple-orange palette. Equals to "PuOr". **TYPE:** `str`                                |
| `Spectral`       | Diverging spectral palette. Equals to "Spectral". **TYPE:** `str`                                 |
| `RdYlBu`         | Diverging red-yellow-blue palette. Equals to "RdYlBu". **TYPE:** `str`                            |
| `RdYlGn`         | Diverging red-yellow-green palette. Equals to "RdYlGn". **TYPE:** `str`                           |
| `Pastel`         | Soft pastel categorical palette. Equals to "Pastel". **TYPE:** `str`                              |
| `Set2`           | ColorBrewer Set2 categorical palette. Equals to "Set2". **TYPE:** `str`                           |
| `Accent`         | ColorBrewer Accent categorical palette. Equals to "Accent". **TYPE:** `str`                       |
| `Dark2`          | ColorBrewer Dark2 categorical palette. Equals to "Dark2". **TYPE:** `str`                         |
| `Paired`         | ColorBrewer Paired categorical palette (high contrast). Equals to "Paired". **TYPE:** `str`       |
| `Set1`           | ColorBrewer Set1 categorical palette (high contrast). Equals to "Set1". **TYPE:** `str`           |
| `Greys`          | Grayscale palette for monochrome visualizations. Equals to "Greys". **TYPE:** `str`               |
| `Viridis`        | Perceptually uniform, color-blind friendly. Equals to "Viridis". **TYPE:** `str`                  |
| `Cividis`        | Color-blind friendly (optimized for CVD). Equals to "Cividis". **TYPE:** `str`                    |
| `Inferno`        | Perceptually uniform, color-blind friendly. Equals to "Inferno". **TYPE:** `str`                  |
| `Plasma`         | Perceptually uniform, color-blind friendly. Equals to "Plasma". **TYPE:** `str`                   |
| `Magma`          | Perceptually uniform, color-blind friendly. Equals to "magma". **TYPE:** `str`                    |
| `Turbo`          | Rainbow-like but perceptually better. Equals to "turbo". **TYPE:** `str`                          |
| `OkabeIto`       | Okabe-Ito categorical palette, color-blind safe. Equals to "OkabeIto". **TYPE:** `str`            |
| `OkabeIto_Black` | Okabe-Ito palette including black. Equals to "OkabeIto_black". **TYPE:** `str`                    |
| `Coolwarm`       | Diverging cool-warm palette. Equals to "coolwarm". **TYPE:** `str`                                |
| `Tab10`          | Tableau 10-color categorical palette. Equals to "tab10". **TYPE:** `str`                          |
| `Tab20`          | Tableau 20-color categorical palette. Equals to "tab20". **TYPE:** `str`                          |
| `PaperYlGnBu`    | Diversified YlGnBu categorical palette for publications. Equals to "PaperYlGnBu". **TYPE:** `str` |
| `PaperAccent`    | Two-color blue/red accent pair for publications. Equals to "PaperAccent". **TYPE:** `str`         |

### datachart.constants.THEME

The predefined themes.

Applied with config.set_theme. Every theme applied to the same set of charts is shown in the [Theme Gallery](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/theme-gallery/index.md).

Examples:

```
>>> from datachart.constants import THEME
>>> THEME.DEFAULT
"default"
```

| ATTRIBUTE    | DESCRIPTION                                                                                                                           |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT`    | The default theme. Equals to "default". **TYPE:** `str`                                                                               |
| `GREYSCALE`  | The greyscale theme. Equals to "greyscale". **TYPE:** `str`                                                                           |
| `INK`        | The ink theme (dark-ink accents, print-ready). Equals to "ink". **TYPE:** `str`                                                       |
| `HATCH`      | The hatch theme (hatch cycle, value labels, dotted grid). Equals to "hatch". **TYPE:** `str`                                          |
| `MINIMAL`    | The minimal theme (accent violet, no spines, flat bars). Equals to "minimal". **TYPE:** `str`                                         |
| `MATERIAL`   | The material theme (Google palette, light grid). Equals to "material". **TYPE:** `str`                                                |
| `SKETCH`     | The sketch theme (hand-drawn, xkcd-style wobble and halo, Comic Neue font). Equals to "sketch". **TYPE:** `str`                       |
| `QUILL`      | The quill theme (black ink on white paper: pen-stroked lines, etched fills, IM Fell English font). Equals to "quill". **TYPE:** `str` |
| `HARBOR`     | The harbor theme (navy and amber in lightness steps, colour-blind safe). Equals to "harbor". **TYPE:** `str`                          |
| `MUTED`      | The muted theme (Tol's muted colours, dash and marker cycles, colour-blind safe). Equals to "muted". **TYPE:** `str`                  |
| `CONTRAST`   | The contrast theme (lightness-stepped colours plus hatches, print-safe). Equals to "contrast". **TYPE:** `str`                        |
| `MUTEDHATCH` | The muted-hatch theme (Tol's muted colours under hatches, BuPu value scale). Equals to "mutedhatch". **TYPE:** `str`                  |
| `SLATEHATCH` | The slate-hatch theme (the hatch theme without rust, slate blue first, PuBu value scale). Equals to "slatehatch". **TYPE:** `str`     |
| `DARK`       | The dark theme (bright marks on a near-black page, light furniture, Viridis value scale). Equals to "dark". **TYPE:** `str`           |

### datachart.constants.EMPHASIS

The supported emphasis roles.

Set per chart via the `emphasis` key in a charts list, or per figure via the `emphasis` argument of Panel.

Examples:

```
>>> from datachart.constants import EMPHASIS
>>> EMPHASIS.BACKGROUND
"background"
```

| ATTRIBUTE    | DESCRIPTION                                                                                                                                                |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BACKGROUND` | Mute a series into context: theme muted color, lowered alpha, thinner strokes, behind the others, no legend entry. Equals to "background". **TYPE:** `str` |
| `HIGHLIGHT`  | Bold a series and bring it to the front of the data layers; it keeps its color and legend entry. Equals to "highlight". **TYPE:** `str`                    |

## Legend Constants

### datachart.constants.LEGEND_ALIGN

The supported legend alignments.

Used by the `plot_legend_alignment` style attribute; aligns the legend's title and entries against each other.

Examples:

```
>>> from datachart.constants import LEGEND_ALIGN
>>> LEGEND_ALIGN.DEFAULT
"left"
```

| ATTRIBUTE | DESCRIPTION                                                              |
| --------- | ------------------------------------------------------------------------ |
| `DEFAULT` | The default legend alignment. Same as LEGEND_ALIGN.LEFT. **TYPE:** `str` |
| `CENTER`  | The center legend alignment. Equals to "center". **TYPE:** `str`         |
| `RIGHT`   | The right legend alignment. Equals to "right". **TYPE:** `str`           |
| `LEFT`    | The left legend alignment. Equals to "left". **TYPE:** `str`             |

### datachart.constants.LEGEND_LOCATION

The supported legend locations.

Used by the `plot_legend_location` style attribute and the `location` field of a chart's `legend` setting. The in-axes members place the legend within the chart; the `OUTSIDE_*` members place it beside the axes, on the named edge, with nothing clipped.

Examples:

```
>>> from datachart.constants import LEGEND_LOCATION
>>> LEGEND_LOCATION.BEST
"best"
```

| ATTRIBUTE        | DESCRIPTION                                                                    |
| ---------------- | ------------------------------------------------------------------------------ |
| `BEST`           | Automatic best location. Equals to "best". **TYPE:** `str`                     |
| `UPPER_RIGHT`    | Upper right corner. Equals to "upper right". **TYPE:** `str`                   |
| `UPPER_LEFT`     | Upper left corner. Equals to "upper left". **TYPE:** `str`                     |
| `LOWER_LEFT`     | Lower left corner. Equals to "lower left". **TYPE:** `str`                     |
| `LOWER_RIGHT`    | Lower right corner. Equals to "lower right". **TYPE:** `str`                   |
| `RIGHT`          | Center right. Equals to "right". **TYPE:** `str`                               |
| `CENTER_LEFT`    | Center left. Equals to "center left". **TYPE:** `str`                          |
| `CENTER_RIGHT`   | Center right. Equals to "center right". **TYPE:** `str`                        |
| `LOWER_CENTER`   | Lower center. Equals to "lower center". **TYPE:** `str`                        |
| `UPPER_CENTER`   | Upper center. Equals to "upper center". **TYPE:** `str`                        |
| `CENTER`         | Center. Equals to "center". **TYPE:** `str`                                    |
| `OUTSIDE_RIGHT`  | Beside the right edge, top-aligned. Equals to "outside right". **TYPE:** `str` |
| `OUTSIDE_LEFT`   | Beside the left edge, top-aligned. Equals to "outside left". **TYPE:** `str`   |
| `OUTSIDE_TOP`    | Above the axes, centered. Equals to "outside top". **TYPE:** `str`             |
| `OUTSIDE_BOTTOM` | Below the axes, centered. Equals to "outside bottom". **TYPE:** `str`          |

## Chart Constants

Constants several charts share.

### datachart.constants.BAR_MODE

The supported bar modes.

Passed as the `bar_mode` setting of bar charts, histograms, and Panel: how multiple series share the axis. Bar charts and panels default to `GROUP`; histograms default to `STACK`, and treat `GROUP` (which has no histogram meaning) as `OVERLAY`.

Examples:

```
>>> from datachart.constants import BAR_MODE
>>> BAR_MODE.DEFAULT
"group"
```

| ATTRIBUTE | DESCRIPTION                                                                                     |
| --------- | ----------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default bar mode. Same as BAR_MODE.GROUP. **TYPE:** `str`                                   |
| `GROUP`   | The series are drawn side by side. Equals to "group". **TYPE:** `str`                           |
| `STACK`   | The series are stacked on top of each other. Equals to "stack". **TYPE:** `str`                 |
| `OVERLAY` | The series are drawn over each other at the same position. Equals to "overlay". **TYPE:** `str` |

### datachart.constants.SORT

The supported category sort orders.

Passed as the `sort` setting of the bar-type fronts (`BarChart`, `PyramidChart`, and the `RadialChart` bar visual): the order the categories are drawn in, by value. One order serves every series in the chart, keyed by the total across them or by the series `sort_by` names; ties keep input order.

Examples:

```
>>> from datachart.constants import SORT
>>> SORT.DEFAULT
None
```

| ATTRIBUTE    | DESCRIPTION                                                  |
| ------------ | ------------------------------------------------------------ |
| `DEFAULT`    | The default sort. Same as SORT.NONE. **TYPE:** `None`        |
| `NONE`       | Input order. Equals to None. **TYPE:** `None`                |
| `ASCENDING`  | Smallest value first. Equals to "ascending". **TYPE:** `str` |
| `DESCENDING` | Largest value first. Equals to "descending". **TYPE:** `str` |

### datachart.constants.NORMALIZE

The supported normalization options.

Passed as the heatmap's `norm` attribute: normalizes the cell values before they are mapped to colors. Distinct from SCALE, which sets an axis scale.

Examples:

```
>>> from datachart.constants import NORMALIZE
>>> NORMALIZE.LINEAR
"linear"
```

| ATTRIBUTE  | DESCRIPTION                                                                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LINEAR`   | The linear normalization. Equals to "linear". **TYPE:** `str`                                                                                           |
| `LOG`      | The logistic normalization. Equals to "log". **TYPE:** `str`                                                                                            |
| `SYMLOG`   | The symlog normalization. Equals to "symlog". **TYPE:** `str`                                                                                           |
| `ASINH`    | The asinh normalization. Equals to "asinh". **TYPE:** `str`                                                                                             |
| `LOGIT`    | The logit normalization. Equals to "logit". **TYPE:** `str`                                                                                             |
| `CENTERED` | The normalization holding vcenter in the middle of the colormap, the same distance to each side of it. Equals to "centered". **TYPE:** `str`            |
| `TWOSLOPE` | The normalization holding vcenter in the middle of the colormap, with vmin and vmax at unequal distances from it. Equals to "twoslope". **TYPE:** `str` |

`CENTERED` and `TWOSLOPE` are read by the heatmap and calendar heatmap, which draw them in the theme's diverging colormap; the other charts taking a `norm` support the first five.

### datachart.constants.ORIENTATION

The supported orientations.

Passed as the `orientation` setting of bar charts, histograms, box plots, and violin plots.

Examples:

```
>>> from datachart.constants import ORIENTATION
>>> ORIENTATION.HORIZONTAL
"horizontal"
```

| ATTRIBUTE    | DESCRIPTION                                                         |
| ------------ | ------------------------------------------------------------------- |
| `HORIZONTAL` | The horizontal orientation. Equals to "horizontal". **TYPE:** `str` |
| `VERTICAL`   | The vertical orientation. Equals to "vertical". **TYPE:** `str`     |

### datachart.constants.VIOLIN_INNER

The supported violin inner marks.

Passed as the `inner` setting of violin plots; `None` draws the body only.

Examples:

```
>>> from datachart.constants import VIOLIN_INNER
>>> VIOLIN_INNER.BOX
"box"
```

| ATTRIBUTE   | DESCRIPTION                                                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- |
| `BOX`       | A thin quartile bar, a 1.5·IQR whisker line, and a median dot. Equals to "box". **TYPE:** `str`                             |
| `QUARTILES` | A dashed median line and dotted first and third quartile lines, clipped to the body. Equals to "quartiles". **TYPE:** `str` |
| `MEDIAN`    | A single solid median line clipped to the body. Equals to "median". **TYPE:** `str`                                         |

### datachart.constants.BANDWIDTH

The supported kernel density bandwidth rules.

Passed as the `bandwidth` setting of violin plots: the rule of thumb that sizes the Gaussian kernel. A number is also accepted, as a factor applied to the standard deviation of the values — smaller is sharper, larger is smoother.

Examples:

```
>>> from datachart.constants import BANDWIDTH
>>> BANDWIDTH.DEFAULT
"scott"
```

| ATTRIBUTE   | DESCRIPTION                                                                                                                                                                       |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT`   | The default rule. Same as BANDWIDTH.SCOTT. **TYPE:** `str`                                                                                                                        |
| `SCOTT`     | Scott's rule of thumb, n \*\* (-1/5) times the standard deviation. Equals to "scott". **TYPE:** `str`                                                                             |
| `SILVERMAN` | Silverman's rule of thumb, (3n/4) \*\* (-1/5) times the standard deviation — about 6% wider than Scott's, so the two look nearly the same. Equals to "silverman". **TYPE:** `str` |

### datachart.constants.SWARM_MODE

The supported swarm plot modes.

Passed as the `mode` setting of swarm plots: how the points of one group spread across the category width.

Examples:

```
>>> from datachart.constants import SWARM_MODE
>>> SWARM_MODE.SWARM
"swarm"
```

| ATTRIBUTE | DESCRIPTION                                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------ |
| `SWARM`   | The beeswarm mode: non-overlapping offsets computed from the marker size. Equals to "swarm". **TYPE:** `str` |
| `STRIP`   | The strip mode: seeded uniform jitter. Equals to "strip". **TYPE:** `str`                                    |

### datachart.constants.VALUE_FORMAT

The predefined value formats.

Passed as the `value_format` attribute of every chart that takes `show_values` (the value labels printed beside its marks) or as the heatmap's `valfmt` attribute (the values drawn in the cells).

Examples:

```
>>> from datachart.constants import VALUE_FORMAT
>>> VALUE_FORMAT.DEFAULT
"{x}"
```

| ATTRIBUTE     | DESCRIPTION                                                                          |
| ------------- | ------------------------------------------------------------------------------------ |
| `DEFAULT`     | The default value format. Equals to "{x}". **TYPE:** `str`                           |
| `INTEGER`     | The integer value format (works on floats too). Equals to "{x:.0f}". **TYPE:** `str` |
| `DECIMAL`     | The decimal value format (1 decimal place). Equals to "{x:.1f}". **TYPE:** `str`     |
| `DECIMAL_2`   | The decimal value format (2 decimal places). Equals to "{x:.2f}". **TYPE:** `str`    |
| `DECIMAL_3`   | The decimal value format (3 decimal places). Equals to "{x:.3f}". **TYPE:** `str`    |
| `PERCENT`     | The percentage value format (1 decimal place). Equals to "{x:.1%}". **TYPE:** `str`  |
| `PERCENT_INT` | The percentage value format (no decimals). Equals to "{x:.0%}". **TYPE:** `str`      |
| `SCIENTIFIC`  | The scientific notation format. Equals to "{x:.2e}". **TYPE:** `str`                 |
| `THOUSANDS`   | The thousands separator format. Equals to "{x:,.0f}". **TYPE:** `str`                |

### datachart.constants.DATE_FORMAT

The predefined date formats.

Passed as the `xticks_format` or `yticks_format` attribute of a chart whose axis holds datetime values, to label its ticks. Every member but `AUTO` is a `strftime` pattern; any other pattern is accepted as well. On a time axis `AUTO` picks concise, non-repeating labels for the visible span; on a category axis with date labels it prints the ISO date, plus the time when any label carries one.

Examples:

```
>>> from datachart.constants import DATE_FORMAT
>>> DATE_FORMAT.YEAR_MONTH
"%Y-%m"
```

| ATTRIBUTE    | DESCRIPTION                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------------ |
| `AUTO`       | Pick the labels from the visible span: concise, non-repeating. Equals to "auto". **TYPE:** `str` |
| `ISO`        | The ISO 8601 date. Equals to "%Y-%m-%d". **TYPE:** `str`                                         |
| `YEAR`       | The four-digit year. Equals to "%Y". **TYPE:** `str`                                             |
| `YEAR_MONTH` | The year and month. Equals to "%Y-%m". **TYPE:** `str`                                           |
| `MONTH_DAY`  | The month and day. Equals to "%m-%d". **TYPE:** `str`                                            |
| `DAY`        | The day of the month. Equals to "%d". **TYPE:** `str`                                            |
| `TIME`       | The hour and minute. Equals to "%H:%M". **TYPE:** `str`                                          |

### datachart.constants.SHOW_GRID

The supported show grid options.

Passed as the `show_grid` chart setting: which grid lines to draw. When unset (or `NONE`), the theme's `chart_default_show_grid` fills in. The members name a set to draw, so there is no member for "no grid at all": pass `False` for that.

Examples:

```
>>> from datachart.constants import SHOW_GRID
>>> SHOW_GRID.DEFAULT
None
```

| ATTRIBUTE | DESCRIPTION                                                                   |
| --------- | ----------------------------------------------------------------------------- |
| `DEFAULT` | The default show grid. Same as SHOW_GRID.NONE. **TYPE:** `str`                |
| `NONE`    | No explicit grid; the theme default applies. Equals to None. **TYPE:** `None` |
| `X`       | Show the x-axis grid. Equals to "x". **TYPE:** `str`                          |
| `Y`       | Show the y-axis grid. Equals to "y". **TYPE:** `str`                          |
| `BOTH`    | Show both the x- and y-axis grid. Equals to "both". **TYPE:** `str`           |

### datachart.constants.SCALE

The supported scale options.

Passed as the `scalex`/`scaley` chart settings to set an axis scale. Distinct from NORMALIZE, which normalizes heatmap colors.

Examples:

```
>>> from datachart.constants import SCALE
>>> SCALE.DEFAULT
"linear"
```

| ATTRIBUTE | DESCRIPTION                                              |
| --------- | -------------------------------------------------------- |
| `DEFAULT` | The default scale. Same as SCALE.LINEAR. **TYPE:** `str` |
| `LINEAR`  | The linear scale. Equals to "linear". **TYPE:** `str`    |
| `LOG`     | The log scale. Equals to "log". **TYPE:** `str`          |
| `SYMLOG`  | The symlog scale. Equals to "symlog". **TYPE:** `str`    |
| `ASINH`   | The asinh scale. Equals to "asinh". **TYPE:** `str`      |

### datachart.constants.ASPECT_RATIO

The supported aspect ratio options.

Passed as the `aspect_ratio` chart setting: the ratio of the y-unit to the x-unit on screen.

Examples:

```
>>> from datachart.constants import ASPECT_RATIO
>>> ASPECT_RATIO.DEFAULT
"auto"
```

| ATTRIBUTE    | DESCRIPTION                                                                                                                                                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `DEFAULT`    | The default aspect ratio. Same as ASPECT_RATIO.AUTO. **TYPE:** `str`                                                                                                                                                                 |
| `AUTO`       | Automatic aspect ratio. Equals to "auto". **TYPE:** `str`                                                                                                                                                                            |
| `EQUAL`      | Equal aspect ratio (1:1). Equals to "equal". **TYPE:** `str`                                                                                                                                                                         |
| `GEOGRAPHIC` | Longitude on x and latitude on y at true proportions: one degree of longitude is narrowed by the cosine of the latitude in the middle of the y-axis. The y-axis must stay within -90 and 90. Equals to "geographic". **TYPE:** `str` |

### datachart.constants.COLORBAR_LOCATION

The supported colorbar locations.

Used by the `location` field of a chart's `colorbar` setting (`ColorbarSettingAttrs`): the chart edge the bar sits on.

Examples:

```
>>> from datachart.constants import COLORBAR_LOCATION
>>> COLORBAR_LOCATION.RIGHT
"right"
```

| ATTRIBUTE | DESCRIPTION                                                 |
| --------- | ----------------------------------------------------------- |
| `RIGHT`   | Right side of the chart. Equals to "right". **TYPE:** `str` |
| `LEFT`    | Left side of the chart. Equals to "left". **TYPE:** `str`   |
| `TOP`     | Top of the chart. Equals to "top". **TYPE:** `str`          |
| `BOTTOM`  | Bottom of the chart. Equals to "bottom". **TYPE:** `str`    |

### datachart.constants.DRAW_POSITION

The supported draw positions of the image and basemap.

Passed as the `position` setting of the image chart and the basemap chart: where the picture or the map sits in the draw order of the axes it shares with other charts. The position decides it, never the order of the figures in `Panel`.

Examples:

```
>>> from datachart.constants import DRAW_POSITION
>>> DRAW_POSITION.DEFAULT
"below"
```

| ATTRIBUTE | DESCRIPTION                                                                                                                   |
| --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default position. Same as DRAW_POSITION.BELOW. **TYPE:** `str`                                                            |
| `BELOW`   | Under every mark and under the gridlines, so the grid and the data read over the picture. Equals to "below". **TYPE:** `str`  |
| `ABOVE`   | Over the marks, under the reference lines and the text annotations; a watermark or a mask. Equals to "above". **TYPE:** `str` |

## Chart-Specific Constants

Constants one chart owns, in the order of the [charts reference](https://eriknovak.github.io/datachart/dev/references/charts/index.md).

### datachart.constants.STACKED_AREA_BASELINE

The supported stacked area baselines.

Passed as the `baseline` attribute of stacked area charts: where the first series starts, and so how the whole stack sits on the y-axis.

Examples:

```
>>> from datachart.constants import STACKED_AREA_BASELINE
>>> STACKED_AREA_BASELINE.DEFAULT
"zero"
```

| ATTRIBUTE         | DESCRIPTION                                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------------ |
| `DEFAULT`         | The default baseline. Same as STACKED_AREA_BASELINE.ZERO. **TYPE:** `str`                                    |
| `ZERO`            | The stack starts at zero. Equals to "zero". **TYPE:** `str`                                                  |
| `PERCENT`         | Each x is normalised so the stack spans 0 to 100. Equals to "percent". **TYPE:** `str`                       |
| `SYM`             | The stack is centred on zero. Equals to "sym". **TYPE:** `str`                                               |
| `WIGGLE`          | The baseline minimises the sum of squared slopes. Equals to "wiggle". **TYPE:** `str`                        |
| `WEIGHTED_WIGGLE` | The baseline minimises the size-weighted sum of squared slopes. Equals to "weighted_wiggle". **TYPE:** `str` |

### datachart.constants.BUMP_RANK

The supported bump chart ranking rules.

Passed as the `rank_by` setting of the bump chart: whether each series' `y` is already a rank or a value ranked per period, over the series present there. Ties keep input order.

Examples:

```
>>> from datachart.constants import BUMP_RANK
>>> BUMP_RANK.DEFAULT
"value_descending"
```

| ATTRIBUTE          | DESCRIPTION                                                                  |
| ------------------ | ---------------------------------------------------------------------------- |
| `DEFAULT`          | The default ranking. Same as BUMP_RANK.VALUE_DESCENDING. **TYPE:** `str`     |
| `VALUE_DESCENDING` | The highest value ranks first. Equals to "value_descending". **TYPE:** `str` |
| `VALUE_ASCENDING`  | The lowest value ranks first. Equals to "value_ascending". **TYPE:** `str`   |
| `GIVEN`            | y is the rank, a positive integer. Equals to "given". **TYPE:** `str`        |

### datachart.constants.BUMP_LABEL_POSITION

The supported end label positions.

Passed as the `label_position` setting of the bump chart: beside which end of each line its series label prints.

Examples:

```
>>> from datachart.constants import BUMP_LABEL_POSITION
>>> BUMP_LABEL_POSITION.DEFAULT
"end"
```

| ATTRIBUTE | DESCRIPTION                                                            |
| --------- | ---------------------------------------------------------------------- |
| `DEFAULT` | The default position. Same as BUMP_LABEL_POSITION.END. **TYPE:** `str` |
| `START`   | Beside the first point. Equals to "start". **TYPE:** `str`             |
| `END`     | Beside the last point. Equals to "end". **TYPE:** `str`                |
| `BOTH`    | Beside the first and the last point. Equals to "both". **TYPE:** `str` |

### datachart.constants.RADIAL_TYPE

The supported radial chart visuals.

Passed as the `type` setting of radial charts: the mark family the whole figure draws. The area visual is the line visual with `show_area=True`; stacked bars are the bar visual with `bar_mode="stack"`.

Examples:

```
>>> from datachart.constants import RADIAL_TYPE
>>> RADIAL_TYPE.LINE
"line"
```

| ATTRIBUTE   | DESCRIPTION                                                                      |
| ----------- | -------------------------------------------------------------------------------- |
| `LINE`      | The line (radar) visual. Equals to "line". **TYPE:** `str`                       |
| `BAR`       | The bar visual, one sector per label. Equals to "bar". **TYPE:** `str`           |
| `SCATTER`   | The scatter visual. Equals to "scatter". **TYPE:** `str`                         |
| `HISTOGRAM` | The angular histogram (wind rose) visual. Equals to "histogram". **TYPE:** `str` |

### datachart.constants.RADIAL_DIRECTION

The supported angular directions.

Passed as the `direction` setting of radial charts: which way the angles increase around the circle.

Examples:

```
>>> from datachart.constants import RADIAL_DIRECTION
>>> RADIAL_DIRECTION.CLOCKWISE
"clockwise"
```

| ATTRIBUTE          | DESCRIPTION                                                                         |
| ------------------ | ----------------------------------------------------------------------------------- |
| `CLOCKWISE`        | The angles increase clockwise. Equals to "clockwise". **TYPE:** `str`               |
| `COUNTERCLOCKWISE` | The angles increase counterclockwise. Equals to "counterclockwise". **TYPE:** `str` |

### datachart.constants.CALENDAR_WEEKDAY

The supported week start days.

Passed as the `week_start` setting of the calendar heatmap: the weekday drawn in the top row of every week column. The theme's `plot_calendar_heatmap_week_start` supplies the default.

Examples:

```
>>> from datachart.constants import CALENDAR_WEEKDAY
>>> CALENDAR_WEEKDAY.MONDAY
"monday"
```

| ATTRIBUTE | DESCRIPTION                                                            |
| --------- | ---------------------------------------------------------------------- |
| `MONDAY`  | Weeks run from Monday to Sunday. Equals to "monday". **TYPE:** `str`   |
| `SUNDAY`  | Weeks run from Sunday to Saturday. Equals to "sunday". **TYPE:** `str` |

### datachart.constants.GANTT_DATE_PERIOD

The supported date axis periods.

Passed as the `period` setting of the gantt chart: the calendar period the date axis is divided into. Lines mark the period edges, each period is labelled at its centre, and a second row names the enclosing period.

Examples:

```
>>> from datachart.constants import GANTT_DATE_PERIOD
>>> GANTT_DATE_PERIOD.MONTH
"month"
```

| ATTRIBUTE       | DESCRIPTION                                                                                                                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NONE`          | Concise date ticks, no period edges. Equals to None. **TYPE:** `None`                                                                                                                         |
| `DAY`           | Days, under their month. Equals to "day". **TYPE:** `str`                                                                                                                                     |
| `WEEK`          | ISO weeks starting on Monday, under their month. Equals to "week". **TYPE:** `str`                                                                                                            |
| `MONTH`         | Months, under their year. Equals to "month". **TYPE:** `str`                                                                                                                                  |
| `QUARTER`       | Quarters, under their year. Equals to "quarter". **TYPE:** `str`                                                                                                                              |
| `YEAR`          | Years. Equals to "year". **TYPE:** `str`                                                                                                                                                      |
| `PROJECT_MONTH` | Months counted from the project start, M1, M2, …, under their project year, Y1, Y2, …. The start is xmin when given, else the earliest task start. Equals to "project_month". **TYPE:** `str` |

### datachart.constants.GANTT_VALUE

The supported gantt chart value labels.

Passed as the `show_values` setting of the gantt chart: what each bar prints past its end. None prints nothing.

Examples:

```
>>> from datachart.constants import GANTT_VALUE
>>> GANTT_VALUE.DURATION
"duration"
```

| ATTRIBUTE  | DESCRIPTION                                                                |
| ---------- | -------------------------------------------------------------------------- |
| `NONE`     | No value labels. Equals to None. **TYPE:** `None`                          |
| `DURATION` | The task's duration in days. Equals to "duration". **TYPE:** `str`         |
| `PROGRESS` | The task's progress as a percentage. Equals to "progress". **TYPE:** `str` |

### datachart.constants.GANTT_SORT_KEY

The supported gantt chart sort keys.

Passed as the `sort_by` setting of the gantt chart: what a `sort` other than `SORT.NONE` orders the task rows by.

Examples:

```
>>> from datachart.constants import GANTT_SORT_KEY
>>> GANTT_SORT_KEY.DEFAULT
"start"
```

| ATTRIBUTE | DESCRIPTION                                                                                                                   |
| --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default key. Same as GANTT_SORT_KEY.START. **TYPE:** `str`                                                                |
| `START`   | Every row by its start. Equals to "start". **TYPE:** `str`                                                                    |
| `GROUP`   | Rows clustered by group, groups by their earliest start and tasks within a group by start. Equals to "group". **TYPE:** `str` |

### datachart.constants.GANTT_ARROW_ENTRY

The supported gantt dependency arrow entries.

Passed as the `plot_gantt_dependency_entry` style attribute of the gantt chart: which side of the dependent task a dependency arrow enters.

Examples:

```
>>> from datachart.constants import GANTT_ARROW_ENTRY
>>> GANTT_ARROW_ENTRY.DEFAULT
"top"
```

| ATTRIBUTE | DESCRIPTION                                                                                                                  |
| --------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default entry. Same as GANTT_ARROW_ENTRY.TOP. **TYPE:** `str`                                                            |
| `TOP`     | Along the dependency's row, then down (or up) onto the dependent bar's start. Equals to "top". **TYPE:** `str`               |
| `LEFT`    | Down (or up) from the dependency's end, then into the dependent bar's start from the left. Equals to "left". **TYPE:** `str` |

### datachart.constants.DUMBBELL_VALUE

The supported dumbbell chart value labels.

Passed as the `show_values` setting of the dumbbell chart: what each record prints. None prints nothing.

Examples:

```
>>> from datachart.constants import DUMBBELL_VALUE
>>> DUMBBELL_VALUE.DELTA
"delta"
```

| ATTRIBUTE   | DESCRIPTION                                                                                          |
| ----------- | ---------------------------------------------------------------------------------------------------- |
| `NONE`      | No value labels. Equals to None. **TYPE:** `None`                                                    |
| `ENDPOINTS` | Each endpoint's value, past its dot, away from the connector. Equals to "endpoints". **TYPE:** `str` |
| `DELTA`     | The record's end - start, at the connector midpoint. Equals to "delta". **TYPE:** `str`              |

### datachart.constants.DUMBBELL_SORT_KEY

The supported dumbbell chart sort keys.

Passed as the `sort_by` setting of the dumbbell chart: what a `sort` other than `SORT.NONE` orders the categories by.

Examples:

```
>>> from datachart.constants import DUMBBELL_SORT_KEY
>>> DUMBBELL_SORT_KEY.DEFAULT
"start"
```

| ATTRIBUTE | DESCRIPTION                                                          |
| --------- | -------------------------------------------------------------------- |
| `DEFAULT` | The default key. Same as DUMBBELL_SORT_KEY.START. **TYPE:** `str`    |
| `START`   | Each category by its start. Equals to "start". **TYPE:** `str`       |
| `END`     | Each category by its end. Equals to "end". **TYPE:** `str`           |
| `DELTA`   | Each category by its end - start. Equals to "delta". **TYPE:** `str` |

### datachart.constants.HISTOGRAM_TYPE

The supported histogram types.

Passed as the `plot_hist_type` style attribute of histograms: how each series is rendered. How multiple series share the axis is the `bar_mode` setting's job — see `BAR_MODE`.

Examples:

```
>>> from datachart.constants import HISTOGRAM_TYPE
>>> HISTOGRAM_TYPE.BAR
"bar"
```

| ATTRIBUTE     | DESCRIPTION                                                                                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `BAR`         | The bar histogram style. Equals to "bar". **TYPE:** `str`                                                                                                          |
| `STEP`        | The step histogram style: an unfilled outline in the series color. Stacked series draw as STEP_FILLED, since a stack needs area. Equals to "step". **TYPE:** `str` |
| `STEP_FILLED` | The filled step histogram style. Equals to "stepfilled". **TYPE:** `str`                                                                                           |

### datachart.constants.RIDGELINE_SCALE

The supported ridgeline density scales.

Passed as the `normalize` setting of ridgeline plots: whether every ridge is scaled to the same peak height, so their shapes compare, or all ridges share one density scale, so their heights compare.

Examples:

```
>>> from datachart.constants import RIDGELINE_SCALE
>>> RIDGELINE_SCALE.DEFAULT
"per_row"
```

| ATTRIBUTE | DESCRIPTION                                                                                                                         |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default scale. Same as RIDGELINE_SCALE.PER_ROW. **TYPE:** `str`                                                                 |
| `PER_ROW` | Every ridge reaches the same peak height. Equals to "per_row". **TYPE:** `str`                                                      |
| `COMMON`  | One density scale: the tallest ridge reaches the peak height and the others stay in proportion. Equals to "common". **TYPE:** `str` |

### datachart.constants.CONTOUR_LEVELS

The supported contour level rules.

Passed as the `levels` setting of contour charts: the rule that picks how many iso-lines (or filled bands) cut the surface. An integer target count or an explicit list of level values is also accepted. Every rule is evaluated on the per-axis resolution of the grid (the square root of its cell count), so a finer grid draws more levels; the count is clamped to the 4–20 range and snapped to round values.

Examples:

```
>>> from datachart.constants import CONTOUR_LEVELS
>>> CONTOUR_LEVELS.DEFAULT
"auto"
```

| ATTRIBUTE | DESCRIPTION                                                                                                                                                |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default rule. Same as CONTOUR_LEVELS.AUTO. **TYPE:** `str`                                                                                             |
| `AUTO`    | Matplotlib's own choice, about eight round values across the surface. Equals to "auto". **TYPE:** `str`                                                    |
| `RICE`    | The Rice rule, 2 * n \*\* (1/3) levels — about ten on a 120×120 grid. Equals to "rice". **TYPE:** `str`                                                    |
| `FD`      | The Freedman–Diaconis rule, the value range over 2 * IQR * n \*\* (-1/3) — about twice as dense as Rice on a 120×120 grid. Equals to "fd". **TYPE:** `str` |

### datachart.constants.HEXBIN_REDUCE

The supported hexbin aggregations.

Passed as the `reduce` attribute of hexbin charts: how the `c` values of the points in a hexagon collapse into the one value that colors it. Ignored without `c`, where every hexagon shows its point count.

Examples:

```
>>> from datachart.constants import HEXBIN_REDUCE
>>> HEXBIN_REDUCE.DEFAULT
"mean"
```

| ATTRIBUTE | DESCRIPTION                                                          |
| --------- | -------------------------------------------------------------------- |
| `DEFAULT` | The default aggregation. Same as HEXBIN_REDUCE.MEAN. **TYPE:** `str` |
| `MEAN`    | The mean of the c values. Equals to "mean". **TYPE:** `str`          |
| `SUM`     | The sum of the c values. Equals to "sum". **TYPE:** `str`            |
| `MEDIAN`  | The median of the c values. Equals to "median". **TYPE:** `str`      |
| `MIN`     | The smallest c value. Equals to "min". **TYPE:** `str`               |
| `MAX`     | The largest c value. Equals to "max". **TYPE:** `str`                |

### datachart.constants.NETWORK_LAYOUT

The supported network chart layouts.

Passed as the `layout` attribute of network charts: the rule that places the nodes in the 0–1 layout space. Layout changes what the picture means, so it is a chart attribute and not a style key.

Examples:

```
>>> from datachart.constants import NETWORK_LAYOUT
>>> NETWORK_LAYOUT.DEFAULT
"spring"
```

Under `WEIGHTED`, and between the groups of `GROUPED`, an edge of weight (w) pulls its nodes together at (s(w)) times the `SPRING` pull:

[s(w) = 0.1 + 2.9,\\frac{w - w\_{\\min}}{w\_{\\max} - w\_{\\min}}]

The lightest edge pulls at a tenth, the heaviest at three times, the rest linearly between; an edge without a weight pulls as the lightest. With no weights, or all equal, every edge pulls at one and the picture is the `SPRING` picture.

| ATTRIBUTE  | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT`  | The default layout. Same as NETWORK_LAYOUT.SPRING. **TYPE:** `str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `SPRING`   | A force-directed (Fruchterman–Reingold) layout: linked nodes pull together, every pair pushes apart. Seeded by the chart's seed argument, so the same data renders the same picture. Costs the square of the node count: fine up to about 1,000 nodes, slow and memory-hungry past that. Equals to "spring". **TYPE:** `str`                                                                                                                                                                                                                        |
| `WEIGHTED` | The spring layout with each edge's pull set by its weight, as above: heavy edges draw their nodes close, light ones let them drift. Same cost as SPRING. Equals to "weighted". **TYPE:** `str`                                                                                                                                                                                                                                                                                                                                                      |
| `GROUPED`  | The nodes clustered by their group, a node without one being a group of its own. Each group is laid out by the spring on its own edges; the groups are then laid out as a smaller network by the weighted spring, an edge between two groups weighing the sum of the edges joining them, so strongly linked clusters sit close. A translucent disc in the group color marks each cluster (plot_network_group_alpha; 0 disables it). Costs about what SPRING costs at worst, far less when the groups are many. Equals to "grouped". **TYPE:** `str` |
| `CIRCULAR` | The nodes evenly spaced on a circle in input order, starting at the top. Equals to "circular". **TYPE:** `str`                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `FIXED`    | Each node at its own x/y, in the 0–1 layout space; a node without them raises. Equals to "fixed". **TYPE:** `str`                                                                                                                                                                                                                                                                                                                                                                                                                                   |

### datachart.constants.NETWORK_LABEL_POSITION

The supported node label positions.

Passed as the `label_position` setting of the network chart: where each node's name prints against its marker.

Examples:

```
>>> from datachart.constants import NETWORK_LABEL_POSITION
>>> NETWORK_LABEL_POSITION.DEFAULT
"center"
```

| ATTRIBUTE | DESCRIPTION                                                                                                                                                      |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default position. Same as NETWORK_LABEL_POSITION.CENTER. **TYPE:** `str`                                                                                     |
| `CENTER`  | On the marker. Equals to "center". **TYPE:** `str`                                                                                                               |
| `ABOVE`   | Above the marker, clear of it, like a place name on a map. Equals to "above". **TYPE:** `str`                                                                    |
| `BEST`    | Beside the marker, at the spot with the least overlap with other nodes, edges, and labels, as scatter point labels are placed. Equals to "best". **TYPE:** `str` |

### datachart.constants.SCATTER_MATRIX_DIAGONAL

The supported scatter matrix diagonal cells.

Passed as the `diagonal` setting of the scatter matrix: what each dimension's own cell shows.

Examples:

```
>>> from datachart.constants import SCATTER_MATRIX_DIAGONAL
>>> SCATTER_MATRIX_DIAGONAL.DEFAULT
"hist"
```

| ATTRIBUTE | DESCRIPTION                                                                                  |
| --------- | -------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default diagonal. Same as SCATTER_MATRIX_DIAGONAL.HIST. **TYPE:** `str`                  |
| `HIST`    | A histogram of the dimension, one per hue group. Equals to "hist". **TYPE:** `str`           |
| `KDE`     | A kernel density curve of the dimension, one per hue group. Equals to "kde". **TYPE:** `str` |
| `NONE`    | A blank cell. Equals to "none". **TYPE:** `str`                                              |

### datachart.constants.BASEMAP_FEATURE

The supported basemap features.

Passed as the `features` of the basemap chart: which of the bundled Natural Earth 1:110m outlines are drawn. The ocean is not a feature; it is the axes background the land sits on.

Examples:

```
>>> from datachart.constants import BASEMAP_FEATURE
>>> BASEMAP_FEATURE.DEFAULT
("coastline", "land")
```

| ATTRIBUTE   | DESCRIPTION                                                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `DEFAULT`   | The default features. Same as (BASEMAP_FEATURE.COASTLINE, BASEMAP_FEATURE.LAND). **TYPE:** `Tuple[str, str]`                   |
| `COASTLINE` | The coastlines, as lines. Equals to "coastline". **TYPE:** `str`                                                               |
| `LAND`      | The land, as a filled area. Equals to "land". **TYPE:** `str`                                                                  |
| `COUNTRIES` | The land, one filled area per country, so the highlight setting can pick countries out. Equals to "countries". **TYPE:** `str` |
| `BORDERS`   | The land borders between countries, as lines. Equals to "borders". **TYPE:** `str`                                             |
| `LAKES`     | The large lakes, filled with the axes background. Equals to "lakes". **TYPE:** `str`                                           |

### datachart.constants.BASEMAP_RESOLUTION

The supported basemap outline resolutions.

Passed as the `resolution` of the basemap chart: the Natural Earth scale the outlines are drawn at. The coarsest ships with the package; the finer ones are downloaded the first time they are asked for and kept in a local cache, so they need the network once. The cache folder is `DATACHART_CACHE_DIR` when that environment variable is set, else `datachart` under `XDG_CACHE_HOME` or `~/.cache`.

Examples:

```
>>> from datachart.constants import BASEMAP_RESOLUTION
>>> BASEMAP_RESOLUTION.DEFAULT
"110m"
```

| ATTRIBUTE | DESCRIPTION                                                                                                |
| --------- | ---------------------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default resolution. Same as BASEMAP_RESOLUTION.LOW. **TYPE:** `str`                                    |
| `LOW`     | 1:110 million, bundled; a continent or a region. Equals to "110m". **TYPE:** `str`                         |
| `MEDIUM`  | 1:50 million, about 5 MB on first use; a country. Equals to "50m". **TYPE:** `str`                         |
| `HIGH`    | 1:10 million, about 28 MB on first use; a coast or a city's surroundings. Equals to "10m". **TYPE:** `str` |
