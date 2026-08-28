# Typings Module

## datachart.typings

Module containing the `typings`.

The `typings` module contains the typings for all chart components. The module is intended to contain the typings for easier input value format checkup.

| CLASS                            | DESCRIPTION                                                     |
| -------------------------------- | --------------------------------------------------------------- |
| `ChartCommonAttrs`               | The chart attributes common to all chart types.                 |
| `VLinePlotAttrs`                 | The vertical line plot attributes.                              |
| `HLinePlotAttrs`                 | The horizontal line plot attributes.                            |
| `TextAttrs`                      | The text annotation attributes.                                 |
| `LineSingleChartAttrs`           | The single chart attributes for the line chart.                 |
| `LineDataPointAttrs`             | The data point attributes for the line chart.                   |
| `StackedAreaSingleChartAttrs`    | The single chart attributes for the stacked area chart.         |
| `SankeySingleChartAttrs`         | The single chart attributes for the Sankey chart.               |
| `SankeyLinkAttrs`                | The link record attributes for the Sankey chart.                |
| `BarSingleChartAttrs`            | The single chart attributes for the bar chart.                  |
| `BarDataPointAttrs`              | The data point attributes for the bar chart.                    |
| `HistogramSingleChartAttrs`      | The single chart attributes for the histogram chart.            |
| `HistDataPointAttrs`             | The data point attributes for the histogram chart.              |
| `HeatmapSingleChartAttrs`        | The single chart attributes for the heatmap chart.              |
| `HeatmapDataAttrs`               | The data attributes for the heatmap chart.                      |
| `HeatmapColorbarAttrs`           | The heatmap colorbar attributes.                                |
| `ContourSingleChartAttrs`        | The single chart attributes for the contour chart.              |
| `ContourDataAttrs`               | The data attributes for the contour chart.                      |
| `HexbinSingleChartAttrs`         | The single chart attributes for the hexbin chart.               |
| `HexbinDataAttrs`                | The data attributes for the hexbin chart.                       |
| `ScatterSingleChartAttrs`        | The single chart attributes for the scatter chart.              |
| `ScatterDataPointAttrs`          | The data point attributes for the scatter chart.                |
| `BoxSingleChartAttrs`            | The single chart attributes for the box plot.                   |
| `BoxDataPointAttrs`              | The data point attributes for the box plot.                     |
| `SwarmSingleChartAttrs`          | The single chart attributes for the swarm plot.                 |
| `SwarmDataPointAttrs`            | The data point attributes for the swarm plot.                   |
| `ViolinSingleChartAttrs`         | The single chart attributes for the violin plot.                |
| `ViolinDataPointAttrs`           | The data point attributes for the violin plot.                  |
| `RaincloudSingleChartAttrs`      | The single chart attributes for the raincloud plot.             |
| `RaincloudDataPointAttrs`        | The data point attributes for the raincloud plot.               |
| `ParallelCoordsSingleChartAttrs` | The single chart attributes for the parallel coordinates chart. |
| `ParallelCoordsDataPointAttrs`   | The data point attributes for the parallel coordinates chart.   |
| `RadialSingleChartAttrs`         | The single chart attributes for the radial chart.               |
| `RadialDataPointAttrs`           | The data point attributes for the radial chart.                 |
| `StyleAttrs`                     | The style typing.                                               |
| `ColorStyleAttrs`                | The typing for the general color style.                         |
| `FontStyleAttrs`                 | The typing for the font style.                                  |
| `AxesStyleAttrs`                 | The typing for the axes style.                                  |
| `LegendStyleAttrs`               | The typing for the legend style.                                |
| `AreaStyleAttrs`                 | The typing for the area style.                                  |
| `GridStyleAttrs`                 | The typing for the grid style.                                  |
| `LineStyleAttrs`                 | The typing for the line style.                                  |
| `StackedAreaStyleAttrs`          | The typing for the stacked area chart style.                    |
| `SankeyStyleAttrs`               | The typing for the Sankey chart style.                          |
| `BarStyleAttrs`                  | The typing for the bar style.                                   |
| `HistStyleAttrs`                 | The typing for the histogram style.                             |
| `VLineStyleAttrs`                | The typing for the vertical line style.                         |
| `HLineStyleAttrs`                | The typing for the horizontal line style.                       |
| `TextStyleAttrs`                 | The typing for the text annotation style.                       |
| `HeatmapStyleAttrs`              | The typing for the heatmap style.                               |
| `ContourStyleAttrs`              | The typing for the contour chart style.                         |
| `HexbinStyleAttrs`               | The typing for the hexbin chart style.                          |
| `ScatterStyleAttrs`              | The typing for the scatter chart style.                         |
| `RegressionStyleAttrs`           | The typing for the regression line style.                       |
| `BoxStyleAttrs`                  | The typing for the box plot style.                              |
| `SwarmStyleAttrs`                | The typing for the swarm plot style.                            |
| `ViolinStyleAttrs`               | The typing for the violin plot style.                           |
| `RaincloudStyleAttrs`            | The typing for the raincloud plot style.                        |
| `ParallelCoordsStyleAttrs`       | The typing for the parallel coordinates chart style.            |
| `ThemeDefaultAttrs`              | The typing for theme-driven defaults and cycles.                |

## Chart Typings

### Common Chart Typings

#### datachart.typings.ChartCommonAttrs

Bases: `TypedDict`

The chart attributes common to all chart types.

| ATTRIBUTE      | DESCRIPTION                                                                                                          |
| -------------- | -------------------------------------------------------------------------------------------------------------------- |
| `title`        | The title of the charts. **TYPE:** `Union[str, None]`                                                                |
| `xlabel`       | The xlabel of the charts. **TYPE:** `Union[str, None]`                                                               |
| `ylabel`       | The ylabel of the charts. **TYPE:** `Union[str, None]`                                                               |
| `figsize`      | The size of the figure. **TYPE:** `Union[FIG_SIZE, Tuple[float, float], None]`                                       |
| `xmin`         | Determine the minimum x-axis value. **TYPE:** `Union[int, float, None]`                                              |
| `xmax`         | Determine the maximum x-axis value. **TYPE:** `Union[int, float, None]`                                              |
| `ymin`         | Determine the minimum y-axis value. **TYPE:** `Union[int, float, None]`                                              |
| `ymax`         | Determine the maximum y-axis value. **TYPE:** `Union[int, float, None]`                                              |
| `show_legend`  | Whether or not to show the legend. **TYPE:** `Union[bool, None]`                                                     |
| `show_grid`    | Determine which grid lines to show. **TYPE:** `Union[SHOW_GRID, str, None]`                                          |
| `aspect_ratio` | The aspect ratio of the charts. **TYPE:** `Union[ASPECT_RATIO, str, None]`                                           |
| `subplots`     | Whether or not to create a separate subplot for each chart. **TYPE:** `Union[bool, None]`                            |
| `max_cols`     | The maximum number of columns in the subplots. Active only when subplots is True. **TYPE:** `Union[int, None]`       |
| `sharex`       | Whether or not to share the x-axis in the subplots. Active only when subplots is True. **TYPE:** `Union[bool, None]` |
| `sharey`       | Whether or not to share the y-axis in the subplots. Active only when subplots is True. **TYPE:** `Union[bool, None]` |

#### datachart.typings.VLinePlotAttrs

Bases: `TypedDict`

The vertical line plot attributes.

| ATTRIBUTE | DESCRIPTION                                                                  |
| --------- | ---------------------------------------------------------------------------- |
| `x`       | The x-axis position of the line. **TYPE:** `Union[int, float]`               |
| `ymin`    | The minimum y-axis position value. **TYPE:** `Union[int, float, None]`       |
| `ymax`    | The maximum y-axis position value. **TYPE:** `Union[int, float, None]`       |
| `style`   | The vertical line style attributes. **TYPE:** `Union[VLineStyleAttrs, None]` |
| `label`   | The label of the vertical line. **TYPE:** `Union[str, None]`                 |

#### datachart.typings.HLinePlotAttrs

Bases: `TypedDict`

The horizontal line plot attributes.

| ATTRIBUTE | DESCRIPTION                                                                    |
| --------- | ------------------------------------------------------------------------------ |
| `y`       | The x-axis position of the line. **TYPE:** `Union[int, float]`                 |
| `xmin`    | The minimum y-axis position value. **TYPE:** `Union[int, float, None]`         |
| `xmax`    | The maximum y-axis position value. **TYPE:** `Union[int, float, None]`         |
| `style`   | The horizontal line style attributes. **TYPE:** `Union[HLineStyleAttrs, None]` |
| `label`   | The label of the horizontal line. **TYPE:** `Union[str, None]`                 |

#### datachart.typings.TextAttrs

Bases: `TypedDict`

The text annotation attributes.

| ATTRIBUTE | DESCRIPTION                                                                                                                                                                                              |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`    | The annotation text. **TYPE:** `str`                                                                                                                                                                     |
| `x`       | The x-axis position of the text. **TYPE:** `Union[int, float]`                                                                                                                                           |
| `y`       | The y-axis position of the text. **TYPE:** `Union[int, float]`                                                                                                                                           |
| `coords`  | The coordinate system of the text position: "data" (default) or "axes" (axes fraction, 0–1). **TYPE:** `Union[str, None]`                                                                                |
| `target`  | The data point the connector points to, always in data coordinates. When present, a connector is drawn from the text to the target. **TYPE:** `Union[Tuple[Union[int, float], Union[int, float]], None]` |
| `style`   | The per-text style attributes. **TYPE:** `Union[TextStyleAttrs, None]`                                                                                                                                   |

### Line Chart Typings

#### datachart.typings.LineSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the line chart.

| ATTRIBUTE     | DESCRIPTION                                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------------------------- |
| `data`        | The list of data points defining the line chart. **TYPE:** `List[LineDataPointAttrs]`                       |
| `subtitle`    | The subtitle of the line chart. Also used as the label in the legend. **TYPE:** `Union[str, None]`          |
| `xlabel`      | The xlabel of the line chart. **TYPE:** `Union[str, None]`                                                  |
| `ylabel`      | The ylabel of the line chart. **TYPE:** `Union[str, None]`                                                  |
| `style`       | The style of the line chart. **TYPE:** `Union[LineStyleAttrs, None]`                                        |
| `xticks`      | The xtick positions list. **TYPE:** `Union[int, float, None]`                                               |
| `xticklabels` | The xtick labels. **TYPE:** `Union[List[str], None]`                                                        |
| `xtickrotate` | The xtick rotation value. **TYPE:** `Union[int, None]`                                                      |
| `yticks`      | the ytick position list. **TYPE:** `Union[int, float, None]`                                                |
| `yticklabels` | The ytick labels. **TYPE:** `Union[List[str], None]`                                                        |
| `ytickrotate` | The ytick rotation value. **TYPE:** `Union[int, None]`                                                      |
| `vlines`      | The vertical lines to be plot. **TYPE:** `Union[VLinePlotAttrs, List[VLinePlotAttrs], None]`                |
| `hlines`      | The horizontal lines to be plot. **TYPE:** `Union[HLinePlotAttrs, List[HLinePlotAttrs], None]`              |
| `texts`       | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                       |
| `x`           | The key name in data that contains the x-axis value. Defaults to "x". **TYPE:** `Union[str, None]`          |
| `y`           | The key name in data that contains the y-axis value. Defaults to "y". **TYPE:** `Union[str, None]`          |
| `yerr`        | The key name in data that contains the y-axis error value. Defaults to "yerr". **TYPE:** `Union[str, None]` |

#### datachart.typings.LineDataPointAttrs

Bases: `TypedDict`

The data point attributes for the line chart.

| ATTRIBUTE | DESCRIPTION                                                     |
| --------- | --------------------------------------------------------------- |
| `x`       | The x-axis value. **TYPE:** `Union[int, float]`                 |
| `y`       | The y-axis value. **TYPE:** `Union[int, float]`                 |
| `yerr`    | The y-axis error value. **TYPE:** `Optional[Union[int, float]]` |

### Bar Chart Typings

#### datachart.typings.BarSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the bar chart.

| ATTRIBUTE     | DESCRIPTION                                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------------------------- |
| `data`        | The list of data points defining the bar chart. **TYPE:** `List[BarDataPointAttrs]`                         |
| `subtitle`    | The subtitle of the bar chart. Also used as the label in the legend. **TYPE:** `Union[str, None]`           |
| `xlabel`      | The xlabel of the bar chart. **TYPE:** `Union[str, None]`                                                   |
| `ylabel`      | The ylabel of the bar chart. **TYPE:** `Union[str, None]`                                                   |
| `style`       | The style of the bar chart. **TYPE:** `Union[BarStyleAttrs, None]`                                          |
| `xticks`      | The xtick positions list. **TYPE:** `Union[int, float, None]`                                               |
| `xticklabels` | The xtick labels. **TYPE:** `Union[List[str], None]`                                                        |
| `xtickrotate` | The xtick rotation value. **TYPE:** `Union[int, None]`                                                      |
| `yticks`      | the ytick position list. **TYPE:** `Union[int, float, None]`                                                |
| `yticklabels` | The ytick labels. **TYPE:** `Union[List[str], None]`                                                        |
| `ytickrotate` | The ytick rotation value. **TYPE:** `Union[int, None]`                                                      |
| `vlines`      | The vertical lines to be plot. **TYPE:** `Union[VLinePlotAttrs, List[VLinePlotAttrs], None]`                |
| `hlines`      | The horizontal lines to be plot. **TYPE:** `Union[HLinePlotAttrs, List[HLinePlotAttrs], None]`              |
| `texts`       | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                       |
| `label`       | The key name in data that contains the label value. Defaults to "label". **TYPE:** `Union[str, None]`       |
| `y`           | The key name in data that contains the y-axis value. Defaults to "y". **TYPE:** `Union[str, None]`          |
| `yerr`        | The key name in data that contains the y-axis error value. Defaults to "yerr". **TYPE:** `Union[str, None]` |

#### datachart.typings.BarDataPointAttrs

Bases: `TypedDict`

The data point attributes for the bar chart.

| ATTRIBUTE | DESCRIPTION                                                     |
| --------- | --------------------------------------------------------------- |
| `label`   | The label. **TYPE:** `str`                                      |
| `y`       | The y-axis value. **TYPE:** `Union[int, float]`                 |
| `yerr`    | The y-axis error value. **TYPE:** `Optional[Union[int, float]]` |

### Histogram Typings

#### datachart.typings.HistogramSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the histogram chart.

| ATTRIBUTE     | DESCRIPTION                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------- |
| `data`        | The list of data points defining the histogram chart. **TYPE:** `List[HistDataPointAttrs]`              |
| `subtitle`    | The subtitle of the histogram chart. Also used as the label in the legend. **TYPE:** `Union[str, None]` |
| `xlabel`      | The xlabel of the histogram chart. **TYPE:** `Union[str, None]`                                         |
| `ylabel`      | The ylabel of the histogram chart. **TYPE:** `Union[str, None]`                                         |
| `style`       | The style of the histogram chart. **TYPE:** `Union[HistStyleAttrs, None]`                               |
| `xticks`      | The xtick positions list. **TYPE:** `Union[int, float, None]`                                           |
| `xticklabels` | The xtick labels. **TYPE:** `Union[List[str], None]`                                                    |
| `xtickrotate` | The xtick rotation value. **TYPE:** `Union[int, None]`                                                  |
| `yticks`      | the ytick position list. **TYPE:** `Union[int, float, None]`                                            |
| `yticklabels` | The ytick labels. **TYPE:** `Union[List[str], None]`                                                    |
| `ytickrotate` | The ytick rotation value. **TYPE:** `Union[int, None]`                                                  |
| `vlines`      | The vertical lines to be plot. **TYPE:** `Union[VLinePlotAttrs, List[VLinePlotAttrs], None]`            |
| `hlines`      | The horizontal lines to be plot. **TYPE:** `Union[HLinePlotAttrs, List[HLinePlotAttrs], None]`          |
| `texts`       | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                   |
| `x`           | The key name in data that contains the x-axis value. Defaults to "x". **TYPE:** `Union[str, None]`      |

#### datachart.typings.HistDataPointAttrs

Bases: `TypedDict`

The data point attributes for the histogram chart.

| ATTRIBUTE | DESCRIPTION                                     |
| --------- | ----------------------------------------------- |
| `x`       | The x-axis value. **TYPE:** `Union[int, float]` |

### Heatmap Typings

#### datachart.typings.HeatmapSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the heatmap chart.

| ATTRIBUTE     | DESCRIPTION                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `data`        | The labelled grid defining the heatmap chart. **TYPE:** `HeatmapDataAttrs`                            |
| `subtitle`    | The subtitle of the heatmap chart. Also used as the label in the legend. **TYPE:** `Union[str, None]` |
| `xlabel`      | The xlabel of the heatmap chart. **TYPE:** `Union[str, None]`                                         |
| `ylabel`      | The ylabel of the heatmap chart. **TYPE:** `Union[str, None]`                                         |
| `style`       | The style of the heatmap chart. **TYPE:** `Union[HeatmapStyleAttrs, None]`                            |
| `norm`        | The value normalization. **TYPE:** `Union[NORMALIZE, str, None]`                                      |
| `vmin`        | The minimum value to normalize the data points. **TYPE:** `Union[str, None]`                          |
| `vmax`        | The maximum value to normalize the data points. **TYPE:** `Union[str, None]`                          |
| `xticks`      | The xtick positions list. **TYPE:** `Union[int, float, None]`                                         |
| `xticklabels` | The xtick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `xtickrotate` | The xtick rotation value. **TYPE:** `Union[int, None]`                                                |
| `yticks`      | the ytick position list. **TYPE:** `Union[int, float, None]`                                          |
| `yticklabels` | The ytick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `ytickrotate` | The ytick rotation value. **TYPE:** `Union[int, None]`                                                |
| `colorbar`    | The heatmap colorbar attributes. **TYPE:** `Union[HeatmapColorbarAttrs, None]`                        |
| `texts`       | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                 |

#### datachart.typings.HeatmapDataAttrs

Bases: `TypedDict`

The data attributes for the heatmap chart.

| ATTRIBUTE | DESCRIPTION                                                                                                                   |
| --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `x`       | The column labels, one per column of z. Defaults to the column indices. **TYPE:** `Union[List[Union[str, int, float]], None]` |
| `y`       | The row labels, one per row of z. Defaults to the row indices. **TYPE:** `Union[List[Union[str, int, float]], None]`          |
| `z`       | The 2-D grid of cell values, one row per y and one column per x. **TYPE:** `List[List[Union[int, float, None]]]`              |

#### datachart.typings.HeatmapColorbarAttrs

Bases: `TypedDict`

The heatmap colorbar attributes.

| ATTRIBUTE     | DESCRIPTION                                                |
| ------------- | ---------------------------------------------------------- |
| `orientation` | The orientation. **TYPE:** `Union[ORIENTATION, str, None]` |

### Scatter Chart Typings

#### datachart.typings.ScatterSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the scatter chart.

| ATTRIBUTE     | DESCRIPTION                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `data`        | The list of data points defining the scatter chart. **TYPE:** `List[ScatterDataPointAttrs]`           |
| `subtitle`    | The subtitle of the scatter chart. Also used as the label in the legend. **TYPE:** `Union[str, None]` |
| `xlabel`      | The xlabel of the scatter chart. **TYPE:** `Union[str, None]`                                         |
| `ylabel`      | The ylabel of the scatter chart. **TYPE:** `Union[str, None]`                                         |
| `style`       | The style of the scatter chart. **TYPE:** `Union[ScatterStyleAttrs, None]`                            |
| `xticks`      | The xtick positions list. **TYPE:** `Union[int, float, None]`                                         |
| `xticklabels` | The xtick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `xtickrotate` | The xtick rotation value. **TYPE:** `Union[int, None]`                                                |
| `yticks`      | The ytick position list. **TYPE:** `Union[int, float, None]`                                          |
| `yticklabels` | The ytick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `ytickrotate` | The ytick rotation value. **TYPE:** `Union[int, None]`                                                |
| `vlines`      | The vertical lines to be plot. **TYPE:** `Union[VLinePlotAttrs, List[VLinePlotAttrs], None]`          |
| `hlines`      | The horizontal lines to be plot. **TYPE:** `Union[HLinePlotAttrs, List[HLinePlotAttrs], None]`        |
| `texts`       | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                 |
| `x`           | The key name in data that contains the x-axis value. Defaults to "x". **TYPE:** `Union[str, None]`    |
| `y`           | The key name in data that contains the y-axis value. Defaults to "y". **TYPE:** `Union[str, None]`    |
| `size`        | The key name in data that contains the marker size value. **TYPE:** `Union[str, None]`                |
| `hue`         | The key name in data that contains the hue/category value. **TYPE:** `Union[str, None]`               |

#### datachart.typings.ScatterDataPointAttrs

Bases: `TypedDict`

The data point attributes for the scatter chart.

| ATTRIBUTE | DESCRIPTION                                                                  |
| --------- | ---------------------------------------------------------------------------- |
| `x`       | The x-axis value. **TYPE:** `Union[int, float]`                              |
| `y`       | The y-axis value. **TYPE:** `Union[int, float]`                              |
| `size`    | The marker size (for bubble charts). **TYPE:** `Optional[Union[int, float]]` |
| `hue`     | The category for color grouping. **TYPE:** `Optional[str]`                   |

### Box Chart (Box Plot) Typings

#### datachart.typings.BoxSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the box plot.

| ATTRIBUTE     | DESCRIPTION                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `data`        | The list of data points defining the box plot. **TYPE:** `List[BoxDataPointAttrs]`                    |
| `subtitle`    | The subtitle of the box plot. Also used as the label in the legend. **TYPE:** `Union[str, None]`      |
| `xlabel`      | The xlabel of the box plot. **TYPE:** `Union[str, None]`                                              |
| `ylabel`      | The ylabel of the box plot. **TYPE:** `Union[str, None]`                                              |
| `style`       | The style of the box plot. **TYPE:** `Union[BoxStyleAttrs, None]`                                     |
| `xticks`      | The xtick positions list. **TYPE:** `Union[int, float, None]`                                         |
| `xticklabels` | The xtick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `xtickrotate` | The xtick rotation value. **TYPE:** `Union[int, None]`                                                |
| `yticks`      | The ytick position list. **TYPE:** `Union[int, float, None]`                                          |
| `yticklabels` | The ytick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `ytickrotate` | The ytick rotation value. **TYPE:** `Union[int, None]`                                                |
| `vlines`      | The vertical lines to be plot. **TYPE:** `Union[VLinePlotAttrs, List[VLinePlotAttrs], None]`          |
| `hlines`      | The horizontal lines to be plot. **TYPE:** `Union[HLinePlotAttrs, List[HLinePlotAttrs], None]`        |
| `texts`       | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                 |
| `label`       | The key name in data that contains the label value. Defaults to "label". **TYPE:** `Union[str, None]` |
| `value`       | The key name in data that contains the value. Defaults to "value". **TYPE:** `Union[str, None]`       |

#### datachart.typings.BoxDataPointAttrs

Bases: `TypedDict`

The data point attributes for the box plot.

| ATTRIBUTE | DESCRIPTION                                      |
| --------- | ------------------------------------------------ |
| `label`   | The category label. **TYPE:** `str`              |
| `value`   | The numeric value. **TYPE:** `Union[int, float]` |

### Swarm Plot Typings

#### datachart.typings.SwarmSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the swarm plot.

| ATTRIBUTE     | DESCRIPTION                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `data`        | The list of data points defining the swarm plot. **TYPE:** `List[SwarmDataPointAttrs]`                |
| `subtitle`    | The subtitle of the swarm plot. Also used as the label in the legend. **TYPE:** `Union[str, None]`    |
| `xlabel`      | The xlabel of the swarm plot. **TYPE:** `Union[str, None]`                                            |
| `ylabel`      | The ylabel of the swarm plot. **TYPE:** `Union[str, None]`                                            |
| `style`       | The style of the swarm plot. **TYPE:** `Union[SwarmStyleAttrs, None]`                                 |
| `xticks`      | The xtick positions list. **TYPE:** `Union[int, float, None]`                                         |
| `xticklabels` | The xtick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `xtickrotate` | The xtick rotation value. **TYPE:** `Union[int, None]`                                                |
| `yticks`      | The ytick position list. **TYPE:** `Union[int, float, None]`                                          |
| `yticklabels` | The ytick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `ytickrotate` | The ytick rotation value. **TYPE:** `Union[int, None]`                                                |
| `vlines`      | The vertical lines to be plot. **TYPE:** `Union[VLinePlotAttrs, List[VLinePlotAttrs], None]`          |
| `hlines`      | The horizontal lines to be plot. **TYPE:** `Union[HLinePlotAttrs, List[HLinePlotAttrs], None]`        |
| `texts`       | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                 |
| `label`       | The key name in data that contains the label value. Defaults to "label". **TYPE:** `Union[str, None]` |
| `value`       | The key name in data that contains the value. Defaults to "value". **TYPE:** `Union[str, None]`       |

### datachart.typings.SwarmDataPointAttrs

Bases: `TypedDict`

The data point attributes for the swarm plot.

| ATTRIBUTE | DESCRIPTION                                      |
| --------- | ------------------------------------------------ |
| `label`   | The category label. **TYPE:** `str`              |
| `value`   | The numeric value. **TYPE:** `Union[int, float]` |

### Violin Plot Typings

#### datachart.typings.ViolinSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the violin plot.

| ATTRIBUTE     | DESCRIPTION                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `data`        | The list of data points defining the violin plot. **TYPE:** `List[ViolinDataPointAttrs]`              |
| `subtitle`    | The subtitle of the violin plot. Also used as the label in the legend. **TYPE:** `Union[str, None]`   |
| `xlabel`      | The xlabel of the violin plot. **TYPE:** `Union[str, None]`                                           |
| `ylabel`      | The ylabel of the violin plot. **TYPE:** `Union[str, None]`                                           |
| `style`       | The style of the violin plot. **TYPE:** `Union[ViolinStyleAttrs, None]`                               |
| `xticks`      | The xtick positions list. **TYPE:** `Union[int, float, None]`                                         |
| `xticklabels` | The xtick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `xtickrotate` | The xtick rotation value. **TYPE:** `Union[int, None]`                                                |
| `yticks`      | The ytick position list. **TYPE:** `Union[int, float, None]`                                          |
| `yticklabels` | The ytick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `ytickrotate` | The ytick rotation value. **TYPE:** `Union[int, None]`                                                |
| `vlines`      | The vertical lines to be plot. **TYPE:** `Union[VLinePlotAttrs, List[VLinePlotAttrs], None]`          |
| `hlines`      | The horizontal lines to be plot. **TYPE:** `Union[HLinePlotAttrs, List[HLinePlotAttrs], None]`        |
| `texts`       | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                 |
| `label`       | The key name in data that contains the label value. Defaults to "label". **TYPE:** `Union[str, None]` |
| `value`       | The key name in data that contains the value. Defaults to "value". **TYPE:** `Union[str, None]`       |

#### datachart.typings.ViolinDataPointAttrs

Bases: `TypedDict`

The data point attributes for the violin plot.

| ATTRIBUTE | DESCRIPTION                                      |
| --------- | ------------------------------------------------ |
| `label`   | The category label. **TYPE:** `str`              |
| `value`   | The numeric value. **TYPE:** `Union[int, float]` |

### Raincloud Plot Typings

#### datachart.typings.RaincloudSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the raincloud plot.

| ATTRIBUTE     | DESCRIPTION                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `data`        | The list of data points defining the raincloud plot. **TYPE:** `List[RaincloudDataPointAttrs]`        |
| `subtitle`    | The subtitle of the raincloud plot. **TYPE:** `Union[str, None]`                                      |
| `xlabel`      | The xlabel of the raincloud plot. **TYPE:** `Union[str, None]`                                        |
| `ylabel`      | The ylabel of the raincloud plot. **TYPE:** `Union[str, None]`                                        |
| `style`       | The style of the raincloud plot. **TYPE:** `Union[RaincloudStyleAttrs, None]`                         |
| `xticks`      | The xtick positions list. **TYPE:** `Union[int, float, None]`                                         |
| `xticklabels` | The xtick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `xtickrotate` | The xtick rotation value. **TYPE:** `Union[int, None]`                                                |
| `yticks`      | The ytick position list. **TYPE:** `Union[int, float, None]`                                          |
| `yticklabels` | The ytick labels. **TYPE:** `Union[List[str], None]`                                                  |
| `ytickrotate` | The ytick rotation value. **TYPE:** `Union[int, None]`                                                |
| `vlines`      | The vertical lines to be plot. **TYPE:** `Union[VLinePlotAttrs, List[VLinePlotAttrs], None]`          |
| `hlines`      | The horizontal lines to be plot. **TYPE:** `Union[HLinePlotAttrs, List[HLinePlotAttrs], None]`        |
| `texts`       | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                 |
| `label`       | The key name in data that contains the label value. Defaults to "label". **TYPE:** `Union[str, None]` |
| `value`       | The key name in data that contains the value. Defaults to "value". **TYPE:** `Union[str, None]`       |

#### datachart.typings.RaincloudDataPointAttrs

Bases: `TypedDict`

The data point attributes for the raincloud plot.

| ATTRIBUTE | DESCRIPTION                                      |
| --------- | ------------------------------------------------ |
| `label`   | The category label. **TYPE:** `str`              |
| `value`   | The numeric value. **TYPE:** `Union[int, float]` |

### Parallel Coordinates Plot Typings

#### datachart.typings.ParallelCoordsSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the parallel coordinates chart.

| ATTRIBUTE         | DESCRIPTION                                                                            |
| ----------------- | -------------------------------------------------------------------------------------- |
| `data`            | The list of data points. **TYPE:** `List[ParallelCoordsDataPointAttrs]`                |
| `subtitle`        | The subtitle of the chart. **TYPE:** `Union[str, None]`                                |
| `xlabel`          | The xlabel of the chart. **TYPE:** `Union[str, None]`                                  |
| `ylabel`          | The ylabel of the chart. **TYPE:** `Union[str, None]`                                  |
| `style`           | The style of the chart. **TYPE:** `Union[ParallelCoordsStyleAttrs, None]`              |
| `dimensions`      | The dimensions to include and their order. **TYPE:** `Union[List[str], None]`          |
| `hue`             | The key name in data for categorical coloring. **TYPE:** `Union[str, None]`            |
| `category_orders` | Custom order for categorical dimensions. **TYPE:** `Union[Dict[str, List[str]], None]` |
| `texts`           | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`  |

#### datachart.typings.ParallelCoordsDataPointAttrs

Bases: `TypedDict`

The data point attributes for the parallel coordinates chart.

A dictionary where keys are dimension names and values are numeric values. Can optionally include a 'hue' key for categorical coloring.

| ATTRIBUTE | DESCRIPTION                                                |
| --------- | ---------------------------------------------------------- |
| `hue`     | The category for color grouping. **TYPE:** `Optional[str]` |

### Radial Chart Typings

#### datachart.typings.RadialSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the radial chart.

| ATTRIBUTE  | DESCRIPTION                                                                                                                                   |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`     | The list of data points defining the radial chart. **TYPE:** `List[RadialDataPointAttrs]`                                                     |
| `subtitle` | The subtitle of the radial chart. Also used as the label in the legend. **TYPE:** `Union[str, None]`                                          |
| `style`    | The style of the radial chart, matching its visual. **TYPE:** `Union[LineStyleAttrs, BarStyleAttrs, HistStyleAttrs, ScatterStyleAttrs, None]` |
| `texts`    | The text annotations to be drawn. **TYPE:** `Union[TextAttrs, List[TextAttrs], None]`                                                         |
| `label`    | The key name in data that contains the category label. Defaults to "label". **TYPE:** `Union[str, None]`                                      |
| `x`        | The key name in data that contains the angular observation. Defaults to "x". **TYPE:** `Union[str, None]`                                     |
| `y`        | The key name in data that contains the radial value. Defaults to "y". **TYPE:** `Union[str, None]`                                            |
| `yerr`     | The key name in data that contains the radial error value. Defaults to "yerr". **TYPE:** `Union[str, None]`                                   |

#### datachart.typings.RadialDataPointAttrs

Bases: `TypedDict`

The data point attributes for the radial chart.

The line, bar, and scatter visuals take `label`/`y` points whose labels are placed evenly around the circle; the histogram visual takes numeric `x` observations in degrees.

| ATTRIBUTE | DESCRIPTION                                                                                    |
| --------- | ---------------------------------------------------------------------------------------------- |
| `label`   | The category label (line, bar, and scatter visuals). **TYPE:** `str`                           |
| `y`       | The radial value (line, bar, and scatter visuals). **TYPE:** `Union[int, float]`               |
| `yerr`    | The radial error value. **TYPE:** `Optional[Union[int, float]]`                                |
| `x`       | The angular observation in degrees (histogram visual). **TYPE:** `Optional[Union[int, float]]` |

## Style Typings

### datachart.typings.StyleAttrs

Bases: `ColorStyleAttrs`, `FontStyleAttrs`, `AxesStyleAttrs`, `LegendStyleAttrs`, `AreaStyleAttrs`, `GridStyleAttrs`, `LineStyleAttrs`, `StackedAreaStyleAttrs`, `SankeyStyleAttrs`, `BarStyleAttrs`, `HistStyleAttrs`, `VLineStyleAttrs`, `HLineStyleAttrs`, `TextStyleAttrs`, `HeatmapStyleAttrs`, `ContourStyleAttrs`, `HexbinStyleAttrs`, `ScatterStyleAttrs`, `RegressionStyleAttrs`, `BoxStyleAttrs`, `SwarmStyleAttrs`, `ViolinStyleAttrs`, `ParallelCoordsStyleAttrs`, `ThemeDefaultAttrs`

The style attributes. Combines all style typings.

### datachart.typings.ColorStyleAttrs

Bases: `TypedDict`

The typing for the general color style.

| ATTRIBUTE                       | DESCRIPTION                                                                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `color_general_singular`        | The general color for the singular-typed charts. **TYPE:** `Union[COLORS, str, None]`                                                             |
| `color_general_multiple`        | The general color for the multiple-typed charts (palette name or list of hex colors). **TYPE:** `Union[COLORS, str, List[str], None]`             |
| `color_parallel_hue`            | The color palette for parallel coords hue categories (palette name or list of hex colors). **TYPE:** `Union[COLORS, str, List[str], None]`        |
| `color_parallel_hue_continuous` | The sequential ramp for parallel coords numeric hue columns (palette name or list of hex colors). **TYPE:** `Union[COLORS, str, List[str], None]` |
| `muted_color`                   | The color applied to background-emphasis layers. **TYPE:** `Union[str, None]`                                                                     |
| `muted_alpha`                   | The alpha applied to background-emphasis layers. **TYPE:** `Union[float, None]`                                                                   |

### datachart.typings.FontStyleAttrs

Bases: `TypedDict`

The typing for the font style.

| ATTRIBUTE                | DESCRIPTION                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| `font_general_family`    | The general font family. **TYPE:** `Union[str, None]`                                             |
| `font_general_sansserif` | The general sans-serif font. **TYPE:** `Union[List[str], None]`                                   |
| `font_general_serif`     | The general serif font stack, used when the family is "serif". **TYPE:** `Union[List[str], None]` |
| `font_general_color`     | The general font color. **TYPE:** `Union[str, None]`                                              |
| `font_general_size`      | The general font size. **TYPE:** `Union[int, float, str, None]`                                   |
| `font_general_style`     | The general font style. **TYPE:** `Union[FONT_STYLE, str, None]`                                  |
| `font_general_weight`    | The general font weight. **TYPE:** `Union[FONT_WEIGHT, str, None]`                                |
| `font_title_size`        | The title font size. **TYPE:** `Union[int, float, str, None]`                                     |
| `font_title_color`       | The title font color. **TYPE:** `Union[str, None]`                                                |
| `font_title_style`       | The title font style. **TYPE:** `Union[FONT_STYLE, str, None]`                                    |
| `font_title_weight`      | The title font weight. **TYPE:** `Union[FONT_WEIGHT, str, None]`                                  |
| `font_subtitle_size`     | The subtitle font size. **TYPE:** `Union[int, float, str, None]`                                  |
| `font_subtitle_color`    | The subtitle font color. **TYPE:** `Union[str, None]`                                             |
| `font_subtitle_style`    | The subtitle font style. **TYPE:** `Union[FONT_STYLE, None]`                                      |
| `font_subtitle_weight`   | The subtitle font weight. **TYPE:** `Union[FONT_WEIGHT, None]`                                    |
| `font_xlabel_size`       | The xlabel font size. **TYPE:** `Union[int, float, str, None]`                                    |
| `font_xlabel_color`      | The xlabel font color. **TYPE:** `Union[str, None]`                                               |
| `font_xlabel_style`      | The xlabel font style. **TYPE:** `Union[FONT_STYLE, str, None]`                                   |
| `font_xlabel_weight`     | The xlabel font weight. **TYPE:** `Union[FONT_WEIGHT, str, None]`                                 |
| `font_ylabel_size`       | The ylabel font size. **TYPE:** `Union[int, float, str, None]`                                    |
| `font_ylabel_color`      | The ylabel font color. **TYPE:** `Union[str, None]`                                               |
| `font_ylabel_style`      | The ylabel font style. **TYPE:** `Union[FONT_STYLE, str, None]`                                   |
| `font_ylabel_weight`     | The ylabel font weight. **TYPE:** `Union[FONT_WEIGHT, str, None]`                                 |

### datachart.typings.AxesStyleAttrs

Bases: `TypedDict`

The typing for the axes style.

| ATTRIBUTE                    | DESCRIPTION                                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| `axes_spines_top_visible`    | Make the top plot spine visible. **TYPE:** `Union[bool, None]`    |
| `axes_spines_right_visible`  | Make the right plot spine visible. **TYPE:** `Union[bool, None]`  |
| `axes_spines_bottom_visible` | Make the bottom plot spine visible. **TYPE:** `Union[bool, None]` |
| `axes_spines_left_visible`   | Make the left plot spine visible. **TYPE:** `Union[bool, None]`   |
| `axes_spines_width`          | The width of the spines. **TYPE:** `Union[int, float, None]`      |
| `axes_spines_zorder`         | The zorder of the spines. **TYPE:** `Union[int, None]`            |
| `axes_ticks_length`          | The length of the ticks. **TYPE:** `Union[int, float, None]`      |
| `axes_ticks_label_size`      | The size of the tick labels. **TYPE:** `Union[int, float, None]`  |

### datachart.typings.LegendStyleAttrs

Bases: `TypedDict`

The typing for the legend style.

| ATTRIBUTE                 | DESCRIPTION                                                               |
| ------------------------- | ------------------------------------------------------------------------- |
| `plot_legend_shadow`      | Show the legends shadow. **TYPE:** `Union[bool, None]`                    |
| `plot_legend_frameon`     | Show the legends frame. **TYPE:** `Union[bool, None]`                     |
| `plot_legend_alignment`   | The legend alignment. **TYPE:** `Union[LEGEND_ALIGN, str, None]`          |
| `plot_legend_location`    | The legend location. **TYPE:** `Union[LEGEND_LOCATION, str, None]`        |
| `plot_legend_font_size`   | The font size within the legend. **TYPE:** `Union[int, float, str, None]` |
| `plot_legend_title_size`  | The title size of the legend. **TYPE:** `Union[int, float, str, None]`    |
| `plot_legend_label_color` | The label color of the legend. **TYPE:** `Union[str, None]`               |

### datachart.typings.AreaStyleAttrs

Bases: `TypedDict`

The typing for the area style.

| ATTRIBUTE             | DESCRIPTION                                                            |
| --------------------- | ---------------------------------------------------------------------- |
| `plot_area_alpha`     | The alpha value of the area. **TYPE:** `Union[float, None]`            |
| `plot_area_color`     | The color of the area. **TYPE:** `Union[str, None]`                    |
| `plot_area_linewidth` | The line width of the area. **TYPE:** `Union[int, float, None]`        |
| `plot_area_hatch`     | The hatch style of the area. **TYPE:** `Union[HATCH_STYLE, str, None]` |
| `plot_area_zorder`    | The zorder of the area. **TYPE:** `Union[int, None]`                   |

### datachart.typings.GridStyleAttrs

Bases: `TypedDict`

The typing for the grid style.

| ATTRIBUTE             | DESCRIPTION                                                          |
| --------------------- | -------------------------------------------------------------------- |
| `plot_grid_alpha`     | The alpha value of the grid. **TYPE:** `Union[float, None]`          |
| `plot_grid_color`     | The color of the grid. **TYPE:** `Union[str, None]`                  |
| `plot_grid_linewidth` | The line width of the grid. **TYPE:** `Union[int, float, None]`      |
| `plot_grid_linestyle` | The line style of the grid. **TYPE:** `Union[LINE_STYLE, str, None]` |
| `plot_grid_zorder`    | The zorder of the grid. **TYPE:** `Union[int, None]`                 |

### datachart.typings.LineStyleAttrs

Bases: `TypedDict`

The typing for the line chart style.

| ATTRIBUTE                  | DESCRIPTION                                                                             |
| -------------------------- | --------------------------------------------------------------------------------------- |
| `plot_line_color`          | The line color. **TYPE:** `Union[str, None]`                                            |
| `plot_line_alpha`          | The alpha value of the line. **TYPE:** `Union[float, None]`                             |
| `plot_line_style`          | The line style. **TYPE:** `Union[LINE_STYLE, str, None]`                                |
| `plot_line_marker`         | The line marker. **TYPE:** `Union[LINE_MARKER, str, None]`                              |
| `plot_line_width`          | The line width. **TYPE:** `Union[int, float, None]`                                     |
| `plot_line_drawstyle`      | The line draw style. **TYPE:** `Union[LINE_DRAW_STYLE, str, None]`                      |
| `plot_line_zorder`         | The zorder of the line. **TYPE:** `Union[int, float, None]`                             |
| `plot_xticks_label_rotate` | The label rotation of the xticks in the line chart. **TYPE:** `Union[int, float, None]` |
| `plot_yticks_label_rotate` | The label rotation of the yticks in the line chart. **TYPE:** `Union[int, float, None]` |

### datachart.typings.BarStyleAttrs

Bases: `TypedDict`

The typing for the bar chart style.

| ATTRIBUTE                  | DESCRIPTION                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------- |
| `plot_bar_color`           | The bar color. **TYPE:** `Union[str, None]`                                            |
| `plot_bar_alpha`           | The alpha value of the bar. **TYPE:** `Union[float, None]`                             |
| `plot_bar_width`           | The width of the bar. **TYPE:** `Union[int, float, None]`                              |
| `plot_bar_zorder`          | The zorder of the bar. **TYPE:** `Union[int, float, None]`                             |
| `plot_bar_hatch`           | The hatch style of the bar. **TYPE:** `Union[HATCH_STYLE, str, None]`                  |
| `plot_bar_edge_width`      | The edge width of the bar. **TYPE:** `Union[int, float, None]`                         |
| `plot_bar_edge_color`      | The edge color of the bar. **TYPE:** `Union[str, None]`                                |
| `plot_bar_error_color`     | The color of the error line of the bar. **TYPE:** `Union[str, None]`                   |
| `plot_bar_value_fontsize`  | The font size of the bar value labels. **TYPE:** `Union[int, float, None]`             |
| `plot_bar_value_color`     | The color of the bar value labels. **TYPE:** `Union[str, None]`                        |
| `plot_bar_value_padding`   | The padding between bar edge and value label. **TYPE:** `Union[int, float, None]`      |
| `plot_xticks_label_rotate` | The label rotation of the xticks in the bar chart. **TYPE:** `Union[int, float, None]` |
| `plot_yticks_label_rotate` | The label rotation of the yticks in the bar chart. **TYPE:** `Union[int, float, None]` |

### datachart.typings.HistStyleAttrs

Bases: `TypedDict`

The typing for the histogram chart style.

| ATTRIBUTE                  | DESCRIPTION                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| `plot_hist_color`          | The color of the histogram. **TYPE:** `Union[str, None]`                                     |
| `plot_hist_alpha`          | The alpha value of the histogram. **TYPE:** `Union[float, None]`                             |
| `plot_hist_zorder`         | The zorder of the histogram. **TYPE:** `Union[int, float, None]`                             |
| `plot_hist_fill`           | The fill of the histogram. **TYPE:** `Union[str, None]`                                      |
| `plot_hist_hatch`          | The hatch style in the histogram. **TYPE:** `Union[HATCH_STYLE, str, None]`                  |
| `plot_hist_type`           | The type of the histogram. **TYPE:** `Union[HISTOGRAM_TYPE, str, None]`                      |
| `plot_hist_align`          | The alignment of the histogram. **TYPE:** `Union[str, None]`                                 |
| `plot_hist_edge_width`     | The edge width of the histogram. **TYPE:** `Union[int, float, None]`                         |
| `plot_hist_edge_color`     | The edge color of the histogram. **TYPE:** `Union[str, None]`                                |
| `plot_xticks_label_rotate` | The label rotation of the xticks in the histogram chart. **TYPE:** `Union[int, float, None]` |
| `plot_yticks_label_rotate` | The label rotation of the yticks in the histogram chart. **TYPE:** `Union[int, float, None]` |

### datachart.typings.VLineStyleAttrs

Bases: `TypedDict`

The typing for the vertical line style.

| ATTRIBUTE          | DESCRIPTION                                                              |
| ------------------ | ------------------------------------------------------------------------ |
| `plot_vline_color` | The color of the vertical line. **TYPE:** `Union[str, None]`             |
| `plot_vline_style` | The style of the vertical line. **TYPE:** `Union[LINE_STYLE, str, None]` |
| `plot_vline_width` | The width of the vertical line. **TYPE:** `Union[int, float, None]`      |
| `plot_vline_alpha` | The alpha value of the vertical line. **TYPE:** `Union[float, None]`     |

### datachart.typings.HLineStyleAttrs

Bases: `TypedDict`

The typing for the horizontal line style.

| ATTRIBUTE          | DESCRIPTION                                                                |
| ------------------ | -------------------------------------------------------------------------- |
| `plot_hline_color` | The color of the horizontal line. **TYPE:** `Union[str, None]`             |
| `plot_hline_style` | The style of the horizontal line. **TYPE:** `Union[LINE_STYLE, str, None]` |
| `plot_hline_width` | The width of the horizontal line. **TYPE:** `Union[int, float, None]`      |
| `plot_hline_alpha` | The alpha value of the horizontal line. **TYPE:** `Union[float, None]`     |

### datachart.typings.TextStyleAttrs

Bases: `TypedDict`

The typing for the text annotation style.

| ATTRIBUTE                  | DESCRIPTION                                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `plot_text_color`          | The text color; falls back to the general font color. **TYPE:** `Union[str, None]`                              |
| `plot_text_size`           | The text font size. **TYPE:** `Union[int, float, str, None]`                                                    |
| `plot_text_weight`         | The text font weight. **TYPE:** `Union[FONT_WEIGHT, str, None]`                                                 |
| `plot_text_halign`         | The horizontal alignment of the text. **TYPE:** `Union[str, None]`                                              |
| `plot_text_valign`         | The vertical alignment of the text. **TYPE:** `Union[str, None]`                                                |
| `plot_text_alpha`          | The alpha value of the text. **TYPE:** `Union[float, None]`                                                     |
| `plot_text_box_visible`    | Whether to draw the background box. **TYPE:** `Union[bool, None]`                                               |
| `plot_text_box_style`      | The matplotlib box style (e.g. "round,pad=0.4"). **TYPE:** `Union[str, None]`                                   |
| `plot_text_box_facecolor`  | The face color of the box. **TYPE:** `Union[str, None]`                                                         |
| `plot_text_box_edgecolor`  | The edge color of the box. **TYPE:** `Union[str, None]`                                                         |
| `plot_text_box_edge_width` | The edge width of the box. **TYPE:** `Union[int, float, None]`                                                  |
| `plot_text_box_alpha`      | The alpha value of the box. **TYPE:** `Union[float, None]`                                                      |
| `plot_text_arrow_style`    | The connector look (see ARROW_STYLE) or a raw matplotlib arrow style. **TYPE:** `Union[ARROW_STYLE, str, None]` |
| `plot_text_arrow_curve`    | The connector curvature; overrides the look's own. **TYPE:** `Union[float, None]`                               |
| `plot_text_arrow_color`    | The connector color. **TYPE:** `Union[str, None]`                                                               |
| `plot_text_arrow_width`    | The connector line width. **TYPE:** `Union[int, float, None]`                                                   |

### datachart.typings.HeatmapStyleAttrs

Bases: `TypedDict`

The typing for the heatmap chart style.

| ATTRIBUTE                  | DESCRIPTION                                                                                                                                           |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_heatmap_cmap`        | The color map of the heatmap (palette name, list of hex colors, or colormap). **TYPE:** `Union[str, List[str], colors.LinearSegmentedColormap, None]` |
| `plot_heatmap_alpha`       | The alpha value of the heatmap. **TYPE:** `Union[float, None]`                                                                                        |
| `plot_heatmap_font_size`   | The font size of the heatmap. **TYPE:** `Union[int, float, str, None]`                                                                                |
| `plot_heatmap_font_color`  | The font color of the heatmap. **TYPE:** `Union[str, None]`                                                                                           |
| `plot_heatmap_font_style`  | The font style of the heatmap. **TYPE:** `Union[FONT_STYLE, str, None]`                                                                               |
| `plot_heatmap_font_weight` | The font weight of the heatmap. **TYPE:** `Union[FONT_WEIGHT, str, None]`                                                                             |
| `plot_heatmap_frame_color` | The color of the frame always drawn around heatmap axes. **TYPE:** `Union[str, None]`                                                                 |
| `plot_heatmap_edge_width`  | The width of the borders drawn between the cells (0 draws none). **TYPE:** `Union[int, float, None]`                                                  |
| `plot_heatmap_edge_color`  | The color of the borders drawn between the cells. **TYPE:** `Union[str, None]`                                                                        |

### datachart.typings.ScatterStyleAttrs

Bases: `TypedDict`

The typing for the scatter chart style.

| ATTRIBUTE                 | DESCRIPTION                                                    |
| ------------------------- | -------------------------------------------------------------- |
| `plot_scatter_color`      | The scatter marker color. **TYPE:** `Union[str, None]`         |
| `plot_scatter_alpha`      | The alpha value of the markers. **TYPE:** `Union[float, None]` |
| `plot_scatter_size`       | The marker size. **TYPE:** `Union[int, float, None]`           |
| `plot_scatter_marker`     | The marker shape. **TYPE:** `Union[LINE_MARKER, str, None]`    |
| `plot_scatter_zorder`     | The zorder of the scatter. **TYPE:** `Union[int, float, None]` |
| `plot_scatter_edge_width` | The edge width of markers. **TYPE:** `Union[int, float, None]` |
| `plot_scatter_edge_color` | The edge color of markers. **TYPE:** `Union[str, None]`        |

### datachart.typings.RegressionStyleAttrs

Bases: `TypedDict`

The typing for regression line style.

| ATTRIBUTE                  | DESCRIPTION                                                      |
| -------------------------- | ---------------------------------------------------------------- |
| `plot_regression_color`    | The regression line color. **TYPE:** `Union[str, None]`          |
| `plot_regression_alpha`    | The alpha of the regression line. **TYPE:** `Union[float, None]` |
| `plot_regression_width`    | The line width. **TYPE:** `Union[int, float, None]`              |
| `plot_regression_style`    | The line style. **TYPE:** `Union[LINE_STYLE, str, None]`         |
| `plot_regression_ci_alpha` | Confidence interval alpha. **TYPE:** `Union[float, None]`        |

### datachart.typings.BoxStyleAttrs

Bases: `TypedDict`

The typing for the box plot style.

| ATTRIBUTE                     | DESCRIPTION                                                           |
| ----------------------------- | --------------------------------------------------------------------- |
| `plot_box_color`              | The box fill color. **TYPE:** `Union[str, None]`                      |
| `plot_box_alpha`              | The alpha value of the box. **TYPE:** `Union[float, None]`            |
| `plot_box_linewidth`          | The line width of the box. **TYPE:** `Union[int, float, None]`        |
| `plot_box_edgecolor`          | The edge color of the box. **TYPE:** `Union[str, None]`               |
| `plot_box_outlier_marker`     | The outlier marker style. **TYPE:** `Union[LINE_MARKER, str, None]`   |
| `plot_box_outlier_size`       | The outlier marker size. **TYPE:** `Union[int, float, None]`          |
| `plot_box_outlier_color`      | The outlier marker color. **TYPE:** `Union[str, None]`                |
| `plot_box_outlier_edge_color` | The outlier marker edge color. **TYPE:** `Union[str, None]`           |
| `plot_box_median_color`       | The median line color. **TYPE:** `Union[str, None]`                   |
| `plot_box_median_linewidth`   | The median line width. **TYPE:** `Union[int, float, None]`            |
| `plot_box_whisker_color`      | The whisker line color. **TYPE:** `Union[str, None]`                  |
| `plot_box_whisker_linewidth`  | The whisker line width. **TYPE:** `Union[int, float, None]`           |
| `plot_box_cap_color`          | The cap line color. **TYPE:** `Union[str, None]`                      |
| `plot_box_cap_linewidth`      | The cap line width. **TYPE:** `Union[int, float, None]`               |
| `plot_xticks_label_rotate`    | The label rotation of the xticks. **TYPE:** `Union[int, float, None]` |
| `plot_yticks_label_rotate`    | The label rotation of the yticks. **TYPE:** `Union[int, float, None]` |

### datachart.typings.SwarmStyleAttrs

Bases: `TypedDict`

The typing for the swarm plot style.

| ATTRIBUTE               | DESCRIPTION                                                       |
| ----------------------- | ----------------------------------------------------------------- |
| `plot_swarm_color`      | The point color. **TYPE:** `Union[str, None]`                     |
| `plot_swarm_alpha`      | The alpha value of the points. **TYPE:** `Union[float, None]`     |
| `plot_swarm_size`       | The point size. **TYPE:** `Union[int, float, None]`               |
| `plot_swarm_marker`     | The point marker shape. **TYPE:** `Union[LINE_MARKER, str, None]` |
| `plot_swarm_zorder`     | The zorder of the points. **TYPE:** `Union[int, float, None]`     |
| `plot_swarm_edge_width` | The edge width of the points. **TYPE:** `Union[int, float, None]` |
| `plot_swarm_edge_color` | The edge color of the points. **TYPE:** `Union[str, None]`        |

### datachart.typings.ViolinStyleAttrs

Bases: `TypedDict`

The typing for the violin plot style.

| ATTRIBUTE                     | DESCRIPTION                                                                            |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| `plot_violin_color`           | The violin fill color. **TYPE:** `Union[str, None]`                                    |
| `plot_violin_alpha`           | The alpha value of the violin body. **TYPE:** `Union[float, None]`                     |
| `plot_violin_linewidth`       | The line width of the body edge. **TYPE:** `Union[int, float, None]`                   |
| `plot_violin_edgecolor`       | The edge color of the body; defaults to the fill. **TYPE:** `Union[str, None]`         |
| `plot_violin_width`           | The maximum width of the body. **TYPE:** `Union[int, float, None]`                     |
| `plot_violin_inner_color`     | The color of the inner marks; defaults to the font color. **TYPE:** `Union[str, None]` |
| `plot_violin_inner_linewidth` | The line width of the inner marks. **TYPE:** `Union[int, float, None]`                 |
| `plot_violin_median_color`    | The color of the median dot. **TYPE:** `Union[str, None]`                              |
| `plot_violin_median_size`     | The size of the median dot. **TYPE:** `Union[int, float, None]`                        |

### datachart.typings.RaincloudStyleAttrs

Bases: `ViolinStyleAttrs`, `SwarmStyleAttrs`, `BoxStyleAttrs`

The typing for the raincloud plot style.

The union of the violin (cloud), swarm (rain), and box style keys; each key styles its own part of the raincloud.

### datachart.typings.ParallelCoordsStyleAttrs

Bases: `TypedDict`

The typing for the parallel coordinates chart style.

| ATTRIBUTE                           | DESCRIPTION                                                                 |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `plot_parallel_color`               | The line color. **TYPE:** `Union[str, None]`                                |
| `plot_parallel_alpha`               | The alpha value of the lines. **TYPE:** `Union[float, None]`                |
| `plot_parallel_width`               | The line width. **TYPE:** `Union[int, float, None]`                         |
| `plot_parallel_style`               | The line style. **TYPE:** `Union[LINE_STYLE, str, None]`                    |
| `plot_parallel_marker`              | The marker style for data points. **TYPE:** `Union[LINE_MARKER, str, None]` |
| `plot_parallel_zorder`              | The draw order of data lines. **TYPE:** `Union[int, None]`                  |
| `plot_parallel_axis_color`          | The vertical axis line color. **TYPE:** `Union[str, None]`                  |
| `plot_parallel_axis_width`          | The vertical axis line width. **TYPE:** `Union[int, float, None]`           |
| `plot_parallel_axis_zorder`         | The vertical axis line draw order. **TYPE:** `Union[int, None]`             |
| `plot_parallel_tick_color`          | The tick mark color. **TYPE:** `Union[str, None]`                           |
| `plot_parallel_tick_width`          | The tick mark line width. **TYPE:** `Union[int, float, None]`               |
| `plot_parallel_tick_length`         | The tick mark length. **TYPE:** `Union[float, None]`                        |
| `plot_parallel_tick_label_size`     | The tick label font size. **TYPE:** `Union[int, float, None]`               |
| `plot_parallel_tick_label_color`    | The tick label font color. **TYPE:** `Union[str, None]`                     |
| `plot_parallel_tick_label_bg_color` | The tick label background color. **TYPE:** `Union[str, None]`               |
| `plot_parallel_tick_label_bg_alpha` | The tick label background alpha. **TYPE:** `Union[float, None]`             |
| `plot_parallel_dim_label_size`      | The dimension label font size. **TYPE:** `Union[int, float, None]`          |
| `plot_parallel_dim_label_color`     | The dimension label font color. **TYPE:** `Union[str, None]`                |
| `plot_parallel_dim_label_rotation`  | The dimension label rotation. **TYPE:** `Union[int, float, None]`           |
| `plot_parallel_dim_label_pad`       | The dimension label padding from axis. **TYPE:** `Union[int, float, None]`  |

### datachart.typings.ThemeDefaultAttrs

Bases: `TypedDict`

The typing for theme-driven defaults and cycles.

| ATTRIBUTE                   | DESCRIPTION                                                                                                                                                                            |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chart_default_show_grid`   | The theme default for show_grid, applied when a chart call leaves it unset. Never applies to heatmaps. None means the theme has no opinion. **TYPE:** `Union[SHOW_GRID, str, None]`    |
| `chart_default_show_values` | The theme default for show_values, applied when a chart call leaves it unset. None means the theme has no opinion. **TYPE:** `Union[bool, None]`                                       |
| `plot_hatch_cycle`          | The hatch patterns assigned per bar/histogram series, parallel to the color cycle. An explicit per-chart hatch style wins. None disables the cycle. **TYPE:** `Union[List[str], None]` |
