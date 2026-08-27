# Charts Module

## datachart.charts

Module containing the `charts`.

The `charts` module contains the methods to create the plots and figures, grouped by the question they answer.

| FUNCTION         | DESCRIPTION                             |
| ---------------- | --------------------------------------- |
| `LineChart`      | Creates the line chart.                 |
| `BarChart`       | Creates the bar chart.                  |
| `PyramidChart`   | Creates the pyramid chart.              |
| `RadialChart`    | Creates the radial chart.               |
| `Histogram`      | Creates the histogram.                  |
| `BoxPlot`        | Creates the box plot.                   |
| `ViolinPlot`     | Creates the violin plot.                |
| `SwarmPlot`      | Creates the swarm plot.                 |
| `RaincloudPlot`  | Creates the raincloud plot.             |
| `ScatterChart`   | Creates the scatter chart.              |
| `Heatmap`        | Creates the heatmap.                    |
| `ContourChart`   | Creates the contour chart.              |
| `HexbinChart`    | Creates the hexbin chart.               |
| `ParallelCoords` | Creates the parallel coordinates chart. |

## Trends and Comparisons

### datachart.charts.LineChart

```
LineChart(
    data: Union[
        List[LineDataPointAttrs],
        List[List[LineDataPointAttrs]],
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_yerr: Optional[bool] = None,
    show_area: Optional[bool] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            LineStyleAttrs, List[Optional[LineStyleAttrs]]
        ]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    x: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    yerr: Optional[Union[str, List[Optional[str]]]] = None
) -> plt.Figure
```

Creates the line chart.

Lines connect ordered (x, y) points to show how a value changes along a continuous axis, typically time. Use it for trends, growth, and comparing the trajectories of several series on the same scale. For unordered categories use BarChart; for unconnected samples use ScatterChart.

Examples:

```
>>> from datachart.charts import LineChart
>>> figure = LineChart(
...     data=[
...         {"x": 1, "y": 5},
...         {"x": 2, "y": 10},
...         {"x": 3, "y": 15},
...         {"x": 4, "y": 20},
...         {"x": 5, "y": 25}
...     ],
...     title="Basic Line Chart",
...     xlabel="X",
...     ylabel="Y"
... )
```

| PARAMETER      | DESCRIPTION                                                                                                                                                                                                                                                                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`         | The data points for the line chart(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. **TYPE:** `Union[List[LineDataPointAttrs], List[List[LineDataPointAttrs]]]`                                                                                                                          |
| `title`        | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                           |
| `xlabel`       | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                 |
| `ylabel`       | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                 |
| `subtitle`     | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                         |
| `emphasis`     | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, thinner line, behind the others, no legend entry), "highlight" bolds it and brings it to the front, None leaves it unchanged. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None` |
| `figsize`      | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                          |
| `xmin`         | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                           |
| `xmax`         | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                           |
| `ymin`         | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                           |
| `ymax`         | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                           |
| `show_legend`  | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                      |
| `show_grid`    | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                              |
| `show_yerr`    | Whether to show y-axis error bars. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                               |
| `show_area`    | Whether to show the area under the line. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                         |
| `aspect_ratio` | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                                                          |
| `scalex`       | The x-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                           |
| `scaley`       | The y-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                           |
| `subplots`     | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                              |
| `max_cols`     | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                                       |
| `sharex`       | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                         |
| `sharey`       | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                         |
| `style`        | Style configuration(s) for the line(s). **TYPE:** `Optional[Union[LineStyleAttrs, List[Optional[LineStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                         |
| `xticks`       | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                           |
| `xticklabels`  | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                          |
| `xtickrotate`  | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                |
| `yticks`       | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                           |
| `yticklabels`  | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                          |
| `ytickrotate`  | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                |
| `vlines`       | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                        |
| `hlines`       | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                      |
| `texts`        | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                          |
| `x`            | The key name in data for x-axis values (default: "x"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                |
| `y`            | The key name in data for y-axis values (default: "y"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                |
| `yerr`         | The key name in data for y-axis error values (default: "yerr"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                       |

| RETURNS      | DESCRIPTION                           |
| ------------ | ------------------------------------- |
| `plt.Figure` | The figure containing the line chart. |

### datachart.charts.BarChart

```
BarChart(
    data: Union[
        List[BarDataPointAttrs],
        List[List[BarDataPointAttrs]],
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_yerr: Optional[bool] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    orientation: Optional[
        Union[ORIENTATION, str]
    ] = ORIENTATION.VERTICAL,
    bar_mode: Optional[Union[BAR_MODE, str]] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[BarStyleAttrs, List[Optional[BarStyleAttrs]]]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    yerr: Optional[Union[str, List[Optional[str]]]] = None
) -> plt.Figure
```

Creates the bar chart.

Bars compare a numeric value across discrete categories: each label gets a bar whose length encodes its value. Use it when the categories are few and unordered (or ordinal) and the question is "which is bigger, and by how much"; several series can be grouped, stacked, or overlaid via `bar_mode`. For a continuous x-axis reach for LineChart, for distributions for Histogram.

Examples:

```
>>> from datachart.charts import BarChart
>>> figure = BarChart(
...     data=[
...         {"label": "cat1", "y": 5},
...         {"label": "cat2", "y": 10},
...         {"label": "cat3", "y": 15},
...         {"label": "cat4", "y": 20},
...         {"label": "cat5", "y": 25}
...     ],
...     title="Basic Bar Chart",
...     xlabel="LABEL",
...     ylabel="Y"
... )
```

| PARAMETER      | DESCRIPTION                                                                                                                                                                                                                                                                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `data`         | The data points for the bar chart(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. **TYPE:** `Union[List[BarDataPointAttrs], List[List[BarDataPointAttrs]]]`                                                                                                                                    |
| `title`        | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                  |
| `xlabel`       | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                        |
| `ylabel`       | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                        |
| `subtitle`     | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                |
| `emphasis`     | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, behind the others, no legend entry), "highlight" bolds its edges and brings it to the front, None leaves it unchanged. See EMPHASIS. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None` |
| `figsize`      | The size of the figure as (width, height) in inches. See FIG_SIZE. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                      |
| `xmin`         | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                  |
| `xmax`         | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                  |
| `ymin`         | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                  |
| `ymax`         | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                  |
| `show_legend`  | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                             |
| `show_grid`    | Which grid lines to show ("both", "x", "y"). See SHOW_GRID. **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                            |
| `show_yerr`    | Whether to show y-axis error bars. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                      |
| `show_values`  | Whether to show bar value labels at the edge of each bar. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                               |
| `value_format` | Format string for bar value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** `Optional[Union[VALUE_FORMAT, str]]` **DEFAULT:** `None`                                                                                                                                                                      |
| `aspect_ratio` | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                 |
| `bar_mode`     | How multiple bar series share the axis: "group" (side-by-side), "stack" (stacked), or "overlay" (overlapping). See BAR_MODE. **TYPE:** `Optional[Union[BAR_MODE, str]]` **DEFAULT:** `None`                                                                                                                                                            |
| `orientation`  | The orientation of the bars ("vertical" or "horizontal"). See ORIENTATION. **TYPE:** `Optional[Union[ORIENTATION, str]]` **DEFAULT:** `ORIENTATION.VERTICAL`                                                                                                                                                                                           |
| `scalex`       | The x-axis scale ("linear", "log", "symlog", "asinh"). Useful for horizontal bars. See SCALE. **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                              |
| `scaley`       | The y-axis scale ("linear", "log", "symlog", "asinh"). Useful for vertical bars. See SCALE. **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                |
| `subplots`     | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                     |
| `max_cols`     | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                                              |
| `sharex`       | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                |
| `sharey`       | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                |
| `style`        | Style configuration(s) for the bar(s). **TYPE:** `Optional[Union[BarStyleAttrs, List[Optional[BarStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                   |
| `xticks`       | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                  |
| `xticklabels`  | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                 |
| `xtickrotate`  | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                       |
| `yticks`       | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                  |
| `yticklabels`  | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                 |
| `ytickrotate`  | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                       |
| `vlines`       | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                               |
| `hlines`       | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                             |
| `texts`        | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                                 |
| `label`        | The key name in data for label values (default: "label"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                    |
| `y`            | The key name in data for y-axis values (default: "y"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                       |
| `yerr`         | The key name in data for y-axis error values (default: "yerr"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                              |

| RETURNS      | DESCRIPTION                          |
| ------------ | ------------------------------------ |
| `plt.Figure` | The figure containing the bar chart. |

### datachart.charts.PyramidChart

```
PyramidChart(
    data: List[List[BarDataPointAttrs]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_yerr: Optional[bool] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    style: Optional[
        Union[BarStyleAttrs, List[Optional[BarStyleAttrs]]]
    ] = None,
    xticks: Optional[List[Union[int, float]]] = None,
    xticklabels: Optional[List[str]] = None,
    xtickrotate: Optional[int] = None,
    yticks: Optional[List[Union[int, float]]] = None,
    yticklabels: Optional[List[str]] = None,
    ytickrotate: Optional[int] = None,
    vlines: Optional[
        Union[VLinePlotAttrs, List[VLinePlotAttrs]]
    ] = None,
    hlines: Optional[
        Union[HLinePlotAttrs, List[HLinePlotAttrs]]
    ] = None,
    texts: Optional[
        Union[TextAttrs, List[TextAttrs]]
    ] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    yerr: Optional[Union[str, List[Optional[str]]]] = None
) -> plt.Figure
```

Creates the pyramid chart.

A pyramid chart draws exactly two series as horizontal bars mirrored around a shared category axis, the first series to the left and the second to the right: the classic age-sex population pyramid. Use it to compare the distribution of two groups over the same ordered categories, such as age bands, where the symmetry (or lack of it) is the message.

Both series are supplied as positive values; value ticks and labels show absolute values. Unlike the other chart fronts, the axis parameters are spatial: `xlabel`, `xticks`, and `xmax` address the horizontal value axis, and `ylabel` the vertical category axis.

Added in v0.8.0

Examples:

```
>>> from datachart.charts import PyramidChart
>>> figure = PyramidChart(
...     data=[
...         [
...             {"label": "0-14", "y": 12},
...             {"label": "15-29", "y": 18},
...             {"label": "30-44", "y": 22},
...         ],
...         [
...             {"label": "0-14", "y": 11},
...             {"label": "15-29", "y": 19},
...             {"label": "30-44", "y": 24},
...         ],
...     ],
...     subtitle=["Group A", "Group B"],
...     title="Basic Pyramid Chart",
...     show_legend=True,
... )
```

| PARAMETER      | DESCRIPTION                                                                                                                                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`         | Exactly two lists of data points — the first is the left side, the second the right. Values are positive for both sides; the chart mirrors the left side itself. **TYPE:** `List[List[BarDataPointAttrs]]` |
| `title`        | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                      |
| `xlabel`       | The label of the horizontal value axis. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                      |
| `ylabel`       | The label of the vertical category axis. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                     |
| `subtitle`     | The names of the two sides. Used as legend labels. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                               |
| `figsize`      | The size of the figure as (width, height) in inches. See FIG_SIZE. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                          |
| `xmin`         | Not supported; the value axis is always symmetric around zero. Raises when passed. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                             |
| `xmax`         | The maximum per-side value; the value axis spans (-xmax, xmax). **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                |
| `show_legend`  | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                 |
| `show_grid`    | Which grid lines to show ("both", "x", "y"). See SHOW_GRID. **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                |
| `show_yerr`    | Whether to show error bars on the bars. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                     |
| `show_values`  | Whether to show bar value labels at the edge of each bar. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                   |
| `value_format` | Format string for bar value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** `Optional[Union[VALUE_FORMAT, str]]` **DEFAULT:** `None`                          |
| `style`        | Style configuration(s) for the bars, per side. **TYPE:** `Optional[Union[BarStyleAttrs, List[Optional[BarStyleAttrs]]]]` **DEFAULT:** `None`                                                               |
| `xticks`       | Custom value-axis tick positions, as positive values; each is mirrored to both halves. **TYPE:** `Optional[List[Union[int, float]]]` **DEFAULT:** `None`                                                   |
| `xticklabels`  | Custom value-axis tick labels (same length as xticks), applied to both mirrored halves. **TYPE:** `Optional[List[str]]` **DEFAULT:** `None`                                                                |
| `xtickrotate`  | Rotation angle for value-axis tick labels. **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                   |
| `yticks`       | Custom category-axis tick positions. **TYPE:** `Optional[List[Union[int, float]]]` **DEFAULT:** `None`                                                                                                     |
| `yticklabels`  | Custom category-axis tick labels. **TYPE:** `Optional[List[str]]` **DEFAULT:** `None`                                                                                                                      |
| `ytickrotate`  | Rotation angle for category-axis tick labels. **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                |
| `vlines`       | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs]]]` **DEFAULT:** `None`                                                                                            |
| `hlines`       | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs]]]` **DEFAULT:** `None`                                                                                          |
| `texts`        | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs]]]` **DEFAULT:** `None`                                                                                                    |
| `label`        | The key name in data for label values (default: "label"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                        |
| `y`            | The key name in data for the bar values (default: "y"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                          |
| `yerr`         | The key name in data for the bar error values (default: "yerr"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                 |

| RETURNS      | DESCRIPTION                              |
| ------------ | ---------------------------------------- |
| `plt.Figure` | The figure containing the pyramid chart. |

### datachart.charts.RadialChart

```
RadialChart(
    data: Union[
        List[RadialDataPointAttrs],
        List[List[RadialDataPointAttrs]],
    ],
    *,
    type: Optional[Union[RADIAL_TYPE, str]] = None,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_yerr: Optional[bool] = None,
    show_area: Optional[bool] = None,
    show_values: Optional[bool] = None,
    show_tip_labels: Optional[bool] = None,
    show_border: Optional[bool] = None,
    value_format: Optional[str] = None,
    bar_mode: Optional[Union[BAR_MODE, str]] = None,
    num_bins: Optional[int] = None,
    startangle: Optional[Union[str, int, float]] = None,
    direction: Optional[Union[DIRECTION, str]] = None,
    innerradius: Optional[float] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            _RadialStyleAttrs,
            List[Optional[_RadialStyleAttrs]],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    vlines: Optional[dict] = None,
    hlines: Optional[dict] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    x: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    yerr: Optional[Union[str, List[Optional[str]]]] = None
) -> plt.Figure
```

Creates the radial chart.

A radial chart plots series on polar axes: as a line (radar) profile, an area, bars, or a histogram, chosen with `type`. Use the radar form to compare a few entities across several metrics on a shared scale, and the bar and histogram forms for cyclic categories such as hours, weekdays, or compass directions.

Added in v0.8.0

Examples:

```
>>> from datachart.charts import RadialChart
>>> figure = RadialChart(
...     data=[
...         {"label": "N", "y": 5},
...         {"label": "E", "y": 10},
...         {"label": "S", "y": 15},
...         {"label": "W", "y": 20}
...     ],
...     title="Basic Radial Chart"
... )
```

| PARAMETER         | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`            | The data points for the radial chart(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. The line, bar, and scatter visuals take label/y points whose labels are placed evenly around the circle; the histogram visual takes numeric x observations in degrees, binned over \[0, 360). **TYPE:** `Union[List[RadialDataPointAttrs], List[List[RadialDataPointAttrs]]]` |
| `type`            | The visual the whole figure draws: "line" (default), "bar", "scatter", or "histogram". See RADIAL_TYPE. **TYPE:** `Optional[Union[RADIAL_TYPE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                  |
| `title`           | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                      |
| `xlabel`          | The angular-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                      |
| `ylabel`          | The radial-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                       |
| `subtitle`        | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                    |
| `emphasis`        | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart, "highlight" bolds it, None leaves it unchanged. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                            |
| `figsize`         | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                     |
| `ymin`            | The minimum radial-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                 |
| `ymax`            | The maximum radial-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                 |
| `show_legend`     | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                 |
| `show_grid`       | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                         |
| `show_yerr`       | Whether to show the radial error band (line visual). **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                        |
| `show_area`       | Whether to fill the area inside the line (line visual). **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                     |
| `show_values`     | Whether to write each mark's value at its tip, rotated along the spoke. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                     |
| `show_tip_labels` | Whether to write the category labels at the mark tips, rotated along their spokes, instead of around the circle. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                            |
| `show_border`     | Whether to draw the outer border circle. Defaults to the theme's spine visibility; False hides it. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                          |
| `value_format`    | Format for the values written by show_values — a printf format (e.g. "%.1f") or a {x}-style string. See VALUE_FORMAT. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                        |
| `bar_mode`        | How multiple bar series share the circle: "group", "stack", or "overlay" (bar visual). See BAR_MODE. **TYPE:** `Optional[Union[BAR_MODE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                        |
| `num_bins`        | The number of angular bins over \[0, 360) (histogram visual). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                |
| `startangle`      | Where the first point sits: a compass location ("N", "NE", "E", "SE", "S", "SW", "W", "NW") or a numeric compass bearing in degrees clockwise from north. Defaults to "N". **TYPE:** `Optional[Union[str, int, float]]` **DEFAULT:** `None`                                                                                                                                                                                |
| `direction`       | Which way the angles increase: "clockwise" (default) or "counterclockwise". See DIRECTION. **TYPE:** `Optional[Union[DIRECTION, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                 |
| `innerradius`     | The donut hole, as a fraction (0 \<= f < 1) of the radial extent. Defaults to 0. **TYPE:** `Optional[float]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                           |
| `scalex`          | Not supported; the angular axis has no scale. Raises when passed. **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                              |
| `scaley`          | The radial-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                 |
| `subplots`        | Whether to create separate polar subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                   |
| `max_cols`        | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                  |
| `sharex`          | Whether to share the angular axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                              |
| `sharey`          | Whether to share the radial axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                               |
| `style`           | Style configuration(s) for the chart(s); radial visuals obey the matching cartesian style family (plot_line\_\*, plot_bar\_\*, plot_hist\_\*, plot_scatter\_\*). **TYPE:** `Optional[Union[_RadialStyleAttrs, List[Optional[_RadialStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                     |
| `texts`           | Text annotation(s) to draw. On the polar axes, data coordinates are (angle in radians, radius); axes-fraction coordinates ("coords": "axes") are often easier. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                  |
| `vlines`          | Not supported on a polar axes. Raises when passed. **TYPE:** `Optional[dict]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                          |
| `hlines`          | Not supported on a polar axes. Raises when passed. **TYPE:** `Optional[dict]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                          |
| `label`           | The key name in data for the category labels (default: "label"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                 |
| `x`               | The key name in data for the histogram observations (default: "x"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                              |
| `y`               | The key name in data for radial values (default: "y"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                           |
| `yerr`            | The key name in data for radial error values (default: "yerr"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                  |

| RETURNS      | DESCRIPTION                             |
| ------------ | --------------------------------------- |
| `plt.Figure` | The figure containing the radial chart. |

## Distributions

### datachart.charts.Histogram

```
Histogram(
    data: Union[
        List[HistDataPointAttrs],
        List[List[HistDataPointAttrs]],
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_density: Optional[bool] = None,
    show_cumulative: Optional[bool] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    orientation: Optional[
        Union[ORIENTATION, str]
    ] = ORIENTATION.VERTICAL,
    bar_mode: Optional[Union[BAR_MODE, str]] = None,
    num_bins: Optional[int] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            HistStyleAttrs, List[Optional[HistStyleAttrs]]
        ]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    x: Optional[Union[str, List[Optional[str]]]] = None
) -> plt.Figure
```

Creates the histogram.

A histogram bins a single numeric variable and draws the count (or density) per bin, revealing the shape of its distribution: center, spread, skew, modes, and outliers. Use it to inspect one variable or compare a few overlaid distributions. For side-by-side group summaries use BoxPlot or ViolinPlot.

Examples:

```
>>> from datachart.charts import Histogram
>>> figure = Histogram(
...     data=[
...         {"x": 1},
...         {"x": 2},
...         {"x": 3},
...         {"x": 4},
...         {"x": 5}
...     ],
...     title="Basic Histogram",
...     xlabel="X",
...     ylabel="Y"
... )
```

| PARAMETER         | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `data`            | The data points for the histogram(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. **TYPE:** `Union[List[HistDataPointAttrs], List[List[HistDataPointAttrs]]]`                                                                                                                                                                                                          |
| `title`           | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                          |
| `xlabel`          | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                |
| `ylabel`          | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                |
| `subtitle`        | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                        |
| `emphasis`        | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, behind the others, no legend entry), "highlight" bolds it and brings it to the front, None leaves it unchanged. When any chart carries a role, the histograms draw individually overlaid instead of stacked. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None` |
| `figsize`         | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                         |
| `xmin`            | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                          |
| `xmax`            | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                          |
| `ymin`            | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                          |
| `ymax`            | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                          |
| `show_legend`     | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                     |
| `show_grid`       | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                             |
| `show_density`    | Whether to plot the density histogram. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                          |
| `show_cumulative` | Whether to plot the cumulative histogram. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                       |
| `aspect_ratio`    | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                         |
| `orientation`     | The orientation of the histogram (vertical or horizontal). **TYPE:** `Optional[Union[ORIENTATION, str]]` **DEFAULT:** `ORIENTATION.VERTICAL`                                                                                                                                                                                                                                                                                   |
| `bar_mode`        | How multiple histogram series share the axis: "stack" (stacked on shared bins, the default) or "overlay" (each series drawn individually over the others). "group" has no histogram meaning and behaves like "overlay". See BAR_MODE. **TYPE:** `Optional[Union[BAR_MODE, str]]` **DEFAULT:** `None`                                                                                                                           |
| `num_bins`        | The number of bins to split the data into. **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                       |
| `scalex`          | The x-axis scale (e.g., "log", "linear"). Useful for log-distributed data. **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                         |
| `scaley`          | The y-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                          |
| `subplots`        | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                             |
| `max_cols`        | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                      |
| `sharex`          | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                        |
| `sharey`          | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                        |
| `style`           | Style configuration(s) for the histogram(s). **TYPE:** `Optional[Union[HistStyleAttrs, List[Optional[HistStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                   |
| `xticks`          | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                          |
| `xticklabels`     | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                         |
| `xtickrotate`     | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                               |
| `yticks`          | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                          |
| `yticklabels`     | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                         |
| `ytickrotate`     | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                               |
| `vlines`          | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                       |
| `hlines`          | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                     |
| `texts`           | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                         |
| `x`               | The key name in data for x-axis values (default: "x"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                               |

| RETURNS      | DESCRIPTION                          |
| ------------ | ------------------------------------ |
| `plt.Figure` | The figure containing the histogram. |

### datachart.charts.BoxPlot

```
BoxPlot(
    data: Union[
        List[BoxDataPointAttrs],
        List[List[BoxDataPointAttrs]],
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_outliers: Optional[bool] = None,
    show_notch: Optional[bool] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    orientation: Optional[
        Union[ORIENTATION, str]
    ] = ORIENTATION.VERTICAL,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[BoxStyleAttrs, List[Optional[BoxStyleAttrs]]]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    value: Optional[Union[str, List[Optional[str]]]] = None
) -> plt.Figure
```

Creates the box plot.

A box plot summarizes a numeric distribution per group by its median, quartiles, whiskers, and outliers. Use it to compare the level and spread of many groups compactly, or to spot skew and outliers, when the full distribution shape is not needed. For shape use ViolinPlot; for the raw points use SwarmPlot.

Added in v0.7.0

Examples:

```
>>> from datachart.charts import BoxPlot
>>> figure = BoxPlot(
...     data=[
...         {"label": "Group A", "value": 10},
...         {"label": "Group A", "value": 15},
...         {"label": "Group A", "value": 12},
...         {"label": "Group B", "value": 20},
...         {"label": "Group B", "value": 25},
...         {"label": "Group B", "value": 22},
...     ],
...     title="Basic Box Plot",
...     xlabel="Group",
...     ylabel="Value"
... )
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The data points for the box plot(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. Each data point should have a label (category) and value (numeric). **TYPE:** `Union[List[BoxDataPointAttrs], List[List[BoxDataPointAttrs]]]`                                                |
| `title`         | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                 |
| `xlabel`        | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                       |
| `ylabel`        | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                       |
| `subtitle`      | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                               |
| `emphasis`      | The emphasis role(s), aligned with the box labels of one call (a single value applies to every box): "background" mutes a box and its whiskers, caps, median, and outliers, "highlight" bolds the box edges and median, None leaves it unchanged. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None` |
| `figsize`       | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                |
| `xmin`          | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                 |
| `xmax`          | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                 |
| `ymin`          | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                 |
| `ymax`          | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                 |
| `show_legend`   | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                            |
| `show_grid`     | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                    |
| `show_outliers` | Whether to show outliers. Defaults to True. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                            |
| `show_notch`    | Whether to show notched boxes for median confidence interval. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                          |
| `aspect_ratio`  | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                                                |
| `orientation`   | The orientation of the boxes (vertical or horizontal). **TYPE:** `Optional[Union[ORIENTATION, str]]` **DEFAULT:** `ORIENTATION.VERTICAL`                                                                                                                                                                                              |
| `scaley`        | The y-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                 |
| `subplots`      | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                    |
| `max_cols`      | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                             |
| `sharex`        | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                               |
| `sharey`        | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                               |
| `style`         | Style configuration(s) for the box(es). **TYPE:** `Optional[Union[BoxStyleAttrs, List[Optional[BoxStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                 |
| `xticks`        | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                 |
| `xticklabels`   | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                |
| `xtickrotate`   | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                      |
| `yticks`        | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                 |
| `yticklabels`   | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                |
| `ytickrotate`   | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                      |
| `vlines`        | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                              |
| `hlines`        | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                            |
| `texts`         | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                |
| `label`         | The key name in data for label/category values (default: "label"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                          |
| `value`         | The key name in data for numeric values (default: "value"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                 |

| RETURNS      | DESCRIPTION                         |
| ------------ | ----------------------------------- |
| `plt.Figure` | The figure containing the box plot. |

### datachart.charts.ViolinPlot

```
ViolinPlot(
    data: Union[
        List[ViolinDataPointAttrs],
        List[List[ViolinDataPointAttrs]],
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    orientation: Optional[
        Union[ORIENTATION, str]
    ] = ORIENTATION.VERTICAL,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            ViolinStyleAttrs,
            List[Optional[ViolinStyleAttrs]],
        ]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    value: Optional[Union[str, List[Optional[str]]]] = None,
    inner: Optional[
        Union[VIOLIN_INNER, str]
    ] = VIOLIN_INNER.BOX,
    bandwidth: Optional[
        Union[BANDWIDTH, str, float]
    ] = None,
    split: Optional[str] = None
) -> plt.Figure
```

Creates the violin plot.

A violin plot draws the kernel density estimate of each group's numeric distribution as a mirrored profile, showing shape (multimodality, skew, tails) that a box plot hides. Use it to compare distributions across groups when shape matters and each group has enough samples for a density estimate.

Added in Unreleased

Examples:

```
>>> from datachart.charts import ViolinPlot
>>> figure = ViolinPlot(
...     data=[
...         {"label": "Group A", "value": 10},
...         {"label": "Group A", "value": 15},
...         {"label": "Group A", "value": 12},
...         {"label": "Group B", "value": 20},
...         {"label": "Group B", "value": 25},
...         {"label": "Group B", "value": 22},
...     ],
...     title="Basic Violin Plot",
...     xlabel="Group",
...     ylabel="Value"
... )
```

| PARAMETER      | DESCRIPTION                                                                                                                                                                                                                                                                                                     |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`         | The data points for the violin plot(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. Each data point should have a label (category) and value (numeric). **TYPE:** `Union[List[ViolinDataPointAttrs], List[List[ViolinDataPointAttrs]]]`                 |
| `title`        | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                           |
| `xlabel`       | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                 |
| `ylabel`       | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                 |
| `subtitle`     | The subtitle(s) for individual charts (subplots). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                     |
| `emphasis`     | The emphasis role(s), aligned with the violin labels of one call (a single value applies to every violin): "background" mutes a violin body and its inner marks, "highlight" bolds the body edge, None leaves it unchanged. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None` |
| `figsize`      | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                          |
| `xmin`         | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                           |
| `xmax`         | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                           |
| `ymin`         | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                           |
| `ymax`         | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                           |
| `show_legend`  | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                      |
| `show_grid`    | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                              |
| `aspect_ratio` | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                          |
| `orientation`  | The orientation of the violins (vertical or horizontal). **TYPE:** `Optional[Union[ORIENTATION, str]]` **DEFAULT:** `ORIENTATION.VERTICAL`                                                                                                                                                                      |
| `scaley`       | The y-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                           |
| `subplots`     | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                              |
| `max_cols`     | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                       |
| `sharex`       | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                         |
| `sharey`       | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                         |
| `style`        | Style configuration(s) for the violin(s). **TYPE:** `Optional[Union[ViolinStyleAttrs, List[Optional[ViolinStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                   |
| `xticks`       | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                           |
| `xticklabels`  | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                          |
| `xtickrotate`  | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                |
| `yticks`       | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                           |
| `yticklabels`  | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                          |
| `ytickrotate`  | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                |
| `vlines`       | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                        |
| `hlines`       | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                      |
| `texts`        | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                          |
| `label`        | The key name in data for label/category values (default: "label"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                    |
| `value`        | The key name in data for numeric values (default: "value"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                           |
| `inner`        | The marks drawn inside each body: "box" (quartile bar, 1.5·IQR whisker, median dot), "quartiles" (dashed median, dotted Q1/Q3), "median" (one line), or None (body only). See VIOLIN_INNER. **TYPE:** `Optional[Union[VIOLIN_INNER, str]]` **DEFAULT:** `VIOLIN_INNER.BOX`                                      |
| `bandwidth`    | The KDE bandwidth: None or "scott" (Scott's rule), "silverman", or a scalar factor. See BANDWIDTH. **TYPE:** `Optional[Union[BANDWIDTH, str, float]]` **DEFAULT:** `None`                                                                                                                                       |
| `split`        | The key name in data whose exactly two distinct values become the left and right halves of each violin, colored from the multiple palette and listed in the legend. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                               |

| RETURNS      | DESCRIPTION                            |
| ------------ | -------------------------------------- |
| `plt.Figure` | The figure containing the violin plot. |

### datachart.charts.SwarmPlot

```
SwarmPlot(
    data: Union[
        List[SwarmDataPointAttrs],
        List[List[SwarmDataPointAttrs]],
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    mode: Union[SWARM_MODE, str] = SWARM_MODE.SWARM,
    jitter: float = 0.4,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    orientation: Optional[
        Union[ORIENTATION, str]
    ] = ORIENTATION.VERTICAL,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            SwarmStyleAttrs, List[Optional[SwarmStyleAttrs]]
        ]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    value: Optional[Union[str, List[Optional[str]]]] = None
) -> plt.Figure
```

Creates the swarm plot.

A swarm plot draws every observation as a point at its group's category position, spread across the category width so the points do not hide each other, making counts and gaps visible. Use it for small-to-medium samples where each observation matters, or overlay it on a BoxPlot with `Panel` (the two share positions). For large samples prefer ViolinPlot.

Added in Unreleased

Examples:

```
>>> from datachart.charts import SwarmPlot
>>> figure = SwarmPlot(
...     data=[
...         {"label": "Group A", "value": 10},
...         {"label": "Group A", "value": 15},
...         {"label": "Group A", "value": 12},
...         {"label": "Group B", "value": 20},
...         {"label": "Group B", "value": 25},
...         {"label": "Group B", "value": 22},
...     ],
...     title="Basic Swarm Plot",
...     xlabel="Group",
...     ylabel="Value"
... )
```

| PARAMETER      | DESCRIPTION                                                                                                                                                                                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`         | The data points for the swarm plot(s). Can be a single list of data points for one chart, or a list of lists for multiple charts. Each data point should have a label (category) and value (numeric). **TYPE:** `Union[List[SwarmDataPointAttrs], List[List[SwarmDataPointAttrs]]]`                     |
| `title`        | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                   |
| `xlabel`       | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                         |
| `ylabel`       | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                         |
| `subtitle`     | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                 |
| `emphasis`     | The emphasis role(s), aligned with the group labels of one call (a single value applies to every group): "background" mutes a group's points, "highlight" bolds their edges, None leaves them unchanged. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None`            |
| `figsize`      | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                  |
| `xmin`         | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                   |
| `xmax`         | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                   |
| `ymin`         | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                   |
| `ymax`         | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                   |
| `show_legend`  | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                              |
| `show_grid`    | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                      |
| `mode`         | How the points spread across the category width. See SWARM_MODE: "swarm" packs the points so none overlap, from the marker size at draw time (axis limits changed afterwards can shift the spacing); "strip" jitters them uniformly. **TYPE:** `Union[SWARM_MODE, str]` **DEFAULT:** `SWARM_MODE.SWARM` |
| `jitter`       | The strip jitter width, as a fraction of the category width. Only used with mode="strip". **TYPE:** `float` **DEFAULT:** `0.4`                                                                                                                                                                          |
| `aspect_ratio` | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                  |
| `orientation`  | The orientation of the swarms (vertical or horizontal). **TYPE:** `Optional[Union[ORIENTATION, str]]` **DEFAULT:** `ORIENTATION.VERTICAL`                                                                                                                                                               |
| `scaley`       | The y-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                   |
| `subplots`     | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                      |
| `max_cols`     | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                               |
| `sharex`       | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                 |
| `sharey`       | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                 |
| `style`        | Style configuration(s) for the points. **TYPE:** `Optional[Union[SwarmStyleAttrs, List[Optional[SwarmStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                |
| `xticks`       | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                   |
| `xticklabels`  | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                  |
| `xtickrotate`  | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                        |
| `yticks`       | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                   |
| `yticklabels`  | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                  |
| `ytickrotate`  | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                        |
| `vlines`       | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                |
| `hlines`       | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                              |
| `texts`        | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                  |
| `label`        | The key name in data for label/category values (default: "label"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                            |
| `value`        | The key name in data for numeric values (default: "value"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                   |

| RETURNS      | DESCRIPTION                           |
| ------------ | ------------------------------------- |
| `plt.Figure` | The figure containing the swarm plot. |

### datachart.charts.RaincloudPlot

```
RaincloudPlot(
    data: Union[
        List[RaincloudDataPointAttrs],
        List[List[RaincloudDataPointAttrs]],
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_outliers: Optional[bool] = True,
    mode: Union[SWARM_MODE, str] = SWARM_MODE.SWARM,
    jitter: float = 0.4,
    bandwidth: Optional[
        Union[BANDWIDTH, str, float]
    ] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    orientation: Optional[
        Union[ORIENTATION, str]
    ] = ORIENTATION.VERTICAL,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            RaincloudStyleAttrs,
            List[Optional[RaincloudStyleAttrs]],
        ]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    value: Optional[Union[str, List[Optional[str]]]] = None
) -> plt.Figure
```

Creates the raincloud plot.

A raincloud plot draws each group as a cloud (a half violin of its density), its rain (the raw observations), and a box (the quartile summary) side by side at one category position, all in the group's palette color. Use it when you want the shape, the summary statistics, and the individual observations in a single view, for example when reporting experimental results per condition. Vertical rainclouds keep the cloud on the left; horizontal ones keep it above.

Added in Unreleased

Examples:

```
>>> from datachart.charts import RaincloudPlot
>>> figure = RaincloudPlot(
...     data=[
...         {"label": "Group A", "value": 10},
...         {"label": "Group A", "value": 15},
...         {"label": "Group A", "value": 12},
...         {"label": "Group B", "value": 20},
...         {"label": "Group B", "value": 25},
...         {"label": "Group B", "value": 22},
...     ],
...     title="Basic Raincloud Plot",
...     xlabel="Group",
...     ylabel="Value"
... )
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The data points for the raincloud plot(s). Can be a single list of data points for one chart, or a list of lists for multiple charts (drawn as subplots). Each data point should have a label (category) and value (numeric). **TYPE:** `Union[List[RaincloudDataPointAttrs], List[List[RaincloudDataPointAttrs]]]` |
| `title`         | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                               |
| `xlabel`        | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                     |
| `ylabel`        | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                     |
| `subtitle`      | The subtitle(s) for individual charts. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                    |
| `emphasis`      | The emphasis role(s), aligned with the group labels of one call (a single value applies to every group): "background" mutes a group's cloud, rain, and box, "highlight" bolds their edges, None leaves them unchanged. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None`          |
| `figsize`       | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                              |
| `xmin`          | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                               |
| `xmax`          | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                               |
| `ymin`          | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                               |
| `ymax`          | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                               |
| `show_legend`   | Whether to show the legend; one entry per group. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                     |
| `show_grid`     | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                  |
| `show_outliers` | Whether the box shows outliers. **TYPE:** `Optional[bool]` **DEFAULT:** `True`                                                                                                                                                                                                                                      |
| `mode`          | How the rain spreads across its width. See SWARM_MODE: "swarm" packs the points so none overlap; "strip" jitters them uniformly. **TYPE:** `Union[SWARM_MODE, str]` **DEFAULT:** `SWARM_MODE.SWARM`                                                                                                                 |
| `jitter`        | The strip jitter width, as a fraction of the category width like SwarmPlot, scaled down to the rain's narrower cell. Only used with mode="strip". **TYPE:** `float` **DEFAULT:** `0.4`                                                                                                                              |
| `bandwidth`     | The cloud's KDE bandwidth: None or "scott" (Scott's rule), "silverman" (Silverman's rule), or a scalar factor. See BANDWIDTH. **TYPE:** `Optional[Union[BANDWIDTH, str, float]]` **DEFAULT:** `None`                                                                                                                |
| `aspect_ratio`  | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                              |
| `orientation`   | The orientation of the rainclouds (vertical or horizontal). **TYPE:** `Optional[Union[ORIENTATION, str]]` **DEFAULT:** `ORIENTATION.VERTICAL`                                                                                                                                                                       |
| `scaley`        | The y-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                               |
| `subplots`      | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                  |
| `max_cols`      | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                           |
| `sharex`        | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                             |
| `sharey`        | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                             |
| `style`         | Style configuration(s); the violin keys style the cloud, the swarm keys the rain, and the box keys the box. **TYPE:** `Optional[Union[RaincloudStyleAttrs, List[Optional[RaincloudStyleAttrs]]]]` **DEFAULT:** `None`                                                                                               |
| `xticks`        | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                               |
| `xticklabels`   | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                              |
| `xtickrotate`   | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                    |
| `yticks`        | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                               |
| `yticklabels`   | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                              |
| `ytickrotate`   | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                    |
| `vlines`        | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                            |
| `hlines`        | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                          |
| `texts`         | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                              |
| `label`         | The key name in data for label/category values (default: "label"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                        |
| `value`         | The key name in data for numeric values (default: "value"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                               |

| RETURNS      | DESCRIPTION                               |
| ------------ | ----------------------------------------- |
| `plt.Figure` | The figure containing the raincloud plot. |

## Relationships

### datachart.charts.ScatterChart

```
ScatterChart(
    data: Union[
        List[ScatterDataPointAttrs],
        List[List[ScatterDataPointAttrs]],
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_regression: Optional[bool] = None,
    show_ci: Optional[bool] = None,
    ci_level: Optional[float] = None,
    show_correlation: Optional[bool] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            ScatterStyleAttrs,
            List[Optional[ScatterStyleAttrs]],
        ]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    x: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    size: Optional[Union[str, List[Optional[str]]]] = None,
    hue: Optional[Union[str, List[Optional[str]]]] = None,
    size_range: Optional[Tuple[float, float]] = None
) -> plt.Figure
```

Creates a scatter chart.

Each point is one observation placed by two numeric variables, optionally with a third encoded as marker size. Use it to check whether two variables are related, spot clusters and outliers, and quantify the link with the optional regression line and correlation coefficient. For ordered series use LineChart.

Added in v0.7.0

Examples:

```
>>> from datachart.charts import ScatterChart
>>> # Basic scatter plot
>>> figure = ScatterChart(
...     data=[
...         {"x": 1, "y": 5},
...         {"x": 2, "y": 10},
...         {"x": 3, "y": 15},
...         {"x": 4, "y": 20},
...         {"x": 5, "y": 25}
...     ],
...     title="Basic Scatter Chart",
...     xlabel="X",
...     ylabel="Y"
... )
>>>
>>> # Scatter with hue grouping
>>> figure = ScatterChart(
...     data=[
...         {"x": 1, "y": 5, "category": "A"},
...         {"x": 2, "y": 10, "category": "B"},
...     ],
...     hue="category",
...     show_legend=True
... )
>>>
>>> # Bubble chart with size variable
>>> figure = ScatterChart(
...     data=[
...         {"x": 1, "y": 5, "pop": 100},
...         {"x": 2, "y": 10, "pop": 200}
...     ],
...     size="pop",
...     size_range=(20, 200)
... )
>>>
>>> # Scatter with regression line
>>> figure = ScatterChart(
...     data=[...],
...     show_regression=True,
...     show_ci=True,
...     ci_level=0.95
... )
>>>
>>> # Scatter with correlation annotation
>>> figure = ScatterChart(
...     data=[...],
...     show_correlation=True
... )
```

| PARAMETER          | DESCRIPTION                                                                                                                                                                                                                                                                                                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`             | The data points for the scatter chart(s). Can be a single list of data points for one chart, or a list of lists for multiple charts/subplots. **TYPE:** `Union[List[ScatterDataPointAttrs], List[List[ScatterDataPointAttrs]]]`                                                                                                                      |
| `title`            | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                |
| `xlabel`           | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                      |
| `ylabel`           | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                      |
| `subtitle`         | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                              |
| `emphasis`         | The emphasis role(s) for individual charts, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, behind the others, no legend entry), "highlight" gives it a contrasting edge and brings it to the front, None leaves it unchanged. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None` |
| `figsize`          | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                               |
| `xmin`             | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                |
| `xmax`             | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                |
| `ymin`             | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                |
| `ymax`             | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                |
| `show_legend`      | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                           |
| `show_grid`        | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                   |
| `show_regression`  | Whether to show the regression line. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                  |
| `show_ci`          | Whether to show the confidence interval around the regression line. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                   |
| `ci_level`         | The confidence interval level (default 0.95). **TYPE:** `Optional[float]` **DEFAULT:** `None`                                                                                                                                                                                                                                                        |
| `show_correlation` | Whether to show the Pearson correlation coefficient (r-value) as an annotation. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                       |
| `aspect_ratio`     | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                                                               |
| `scalex`           | The x-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                |
| `scaley`           | The y-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                |
| `subplots`         | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                   |
| `max_cols`         | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                                            |
| `sharex`           | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                              |
| `sharey`           | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                              |
| `style`            | Style configuration(s) for the scatter markers. **TYPE:** `Optional[Union[ScatterStyleAttrs, List[Optional[ScatterStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                |
| `xticks`           | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                |
| `xticklabels`      | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                               |
| `xtickrotate`      | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                     |
| `yticks`           | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                |
| `yticklabels`      | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                               |
| `ytickrotate`      | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                     |
| `vlines`           | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                             |
| `hlines`           | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                           |
| `texts`            | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                               |
| `x`                | The key name in data for x-axis values (default: "x"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                     |
| `y`                | The key name in data for y-axis values (default: "y"). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                     |
| `size`             | The key name in data for marker size values (for bubble charts). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                           |
| `hue`              | The key name in data for color grouping (categorical variable). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                            |
| `size_range`       | Tuple of (min_size, max_size) for bubble charts (default: (20, 200)). **TYPE:** `Optional[Tuple[float, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                  |

| RETURNS      | DESCRIPTION                              |
| ------------ | ---------------------------------------- |
| `plt.Figure` | The figure containing the scatter chart. |

### datachart.charts.Heatmap

```
Heatmap(
    data: Union[HeatmapDataAttrs, List[HeatmapDataAttrs]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: None = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_colorbars: Optional[bool] = None,
    show_heatmap_values: Optional[bool] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            HeatmapStyleAttrs,
            List[Optional[HeatmapStyleAttrs]],
        ]
    ] = None,
    norm: Optional[Union[str, List[Optional[str]]]] = None,
    vmin: Optional[
        Union[float, List[Optional[float]]]
    ] = None,
    vmax: Optional[
        Union[float, List[Optional[float]]]
    ] = None,
    valfmt: Optional[
        Union[VALUE_FORMAT, str, List[Optional[str]]]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    colorbar: Optional[
        Union[
            HeatmapColorbarAttrs,
            List[Optional[HeatmapColorbarAttrs]],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None
) -> plt.Figure
```

Creates the heatmap.

A heatmap maps every cell of a 2-D matrix to a color, so structure in a grid of numbers (correlations, confusion matrices, feature-by-time tables) reads at a glance. Use it when both axes are categorical or gridded and the value is what matters; the color scale, colorbar, and cell value labels are all configurable.

Added in v0.4.0

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

| PARAMETER             | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`                | The labelled grid(s) for the heatmap(s): one {x, y, z} dict, or a list of them for multiple heatmaps/subplots. z is the 2-D matrix of cell values (rows along y, columns along x; None cells stay blank); x and y are optional tick labels for its columns and rows (any values, the indices by default). An explicit xticks/xticklabels (yticks/yticklabels) overrides them. **TYPE:** `Union[HeatmapDataAttrs, List[HeatmapDataAttrs]]` |
| `title`               | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                     |
| `xlabel`              | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                           |
| `ylabel`              | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                           |
| `subtitle`            | The subtitle(s) for individual charts. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                          |
| `emphasis`            | Not supported: a heatmap is a single raster layer with no series to mute or highlight. Passing a value raises ValueError. **TYPE:** `None` **DEFAULT:** `None`                                                                                                                                                                                                                                                                            |
| `figsize`             | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                    |
| `xmin`                | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                     |
| `xmax`                | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                     |
| `ymin`                | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                     |
| `ymax`                | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                     |
| `show_legend`         | Whether to show the legend (not typical for heatmaps). **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                     |
| `show_grid`           | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                        |
| `show_colorbars`      | Whether to show the colorbar(s). **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                           |
| `show_heatmap_values` | Whether to show values on the heatmap cells. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                               |
| `aspect_ratio`        | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                    |
| `subplots`            | Whether to create separate subplots for each heatmap. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                      |
| `max_cols`            | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                 |
| `sharex`              | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                   |
| `sharey`              | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                   |
| `style`               | Style configuration(s) for the heatmap(s). **TYPE:** `Optional[Union[HeatmapStyleAttrs, List[Optional[HeatmapStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                          |
| `norm`                | Value normalization method(s). **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                  |
| `vmin`                | Minimum value(s) for normalization. **TYPE:** `Optional[Union[float, List[Optional[float]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                         |
| `vmax`                | Maximum value(s) for normalization. **TYPE:** `Optional[Union[float, List[Optional[float]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                         |
| `valfmt`              | Format string(s) for cell values, with the value named x (e.g., "{x:.1f}"). See VALUE_FORMAT. **TYPE:** `Optional[Union[VALUE_FORMAT, str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                     |
| `xticks`              | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                     |
| `xticklabels`         | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                    |
| `xtickrotate`         | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                          |
| `yticks`              | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                     |
| `yticklabels`         | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                    |
| `ytickrotate`         | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                          |
| `colorbar`            | Colorbar configuration(s). **TYPE:** `Optional[Union[HeatmapColorbarAttrs, List[Optional[HeatmapColorbarAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                    |
| `texts`               | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                    |

| RETURNS      | DESCRIPTION                        |
| ------------ | ---------------------------------- |
| `plt.Figure` | The figure containing the heatmap. |

### datachart.charts.ContourChart

```
ContourChart(
    data: Union[ContourDataAttrs, List[ContourDataAttrs]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    filled: Optional[bool] = None,
    levels: Optional[
        Union[CONTOUR_LEVELS, str, int, List[float]]
    ] = None,
    show_labels: Optional[bool] = None,
    show_colorbars: Optional[bool] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            ContourStyleAttrs,
            List[Optional[ContourStyleAttrs]],
        ]
    ] = None,
    norm: Optional[Union[str, List[Optional[str]]]] = None,
    vmin: Optional[
        Union[float, List[Optional[float]]]
    ] = None,
    vmax: Optional[
        Union[float, List[Optional[float]]]
    ] = None,
    valfmt: Optional[
        Union[VALUE_FORMAT, str, List[Optional[str]]]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    colorbar: Optional[
        Union[
            HeatmapColorbarAttrs,
            List[Optional[HeatmapColorbarAttrs]],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None
) -> plt.Figure
```

Creates the contour chart.

A contour chart draws a surface sampled on a grid — a loss landscape, a 2-D density, a terrain — as iso-lines of equal value, or as filled bands between them. Use it to read the shape of a function of two variables: where its minima and ridges sit and how steeply it changes. Lines overlay on other charts and on each other; fills stand alone, with an optional colorbar. For a per-cell view of a matrix use Heatmap; for the raw points behind a density use ScatterChart.

Added in Unreleased

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

| PARAMETER        | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`           | The gridded surface(s): a dictionary with the 2-D z grid and the optional x and y axis values (one per column and per row of z, the indices by default), or a list of them for multiple charts/subplots. **TYPE:** `Union[ContourDataAttrs, List[ContourDataAttrs]]`                                                                                                                                                            |
| `title`          | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                           |
| `xlabel`         | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                 |
| `ylabel`         | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                 |
| `subtitle`       | The subtitle(s) for individual charts. Used as legend labels. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                         |
| `emphasis`       | The emphasis role(s) for individual line contours, aligned like style: "background" mutes a chart (theme muted color, lowered alpha, behind the others, no legend entry), "highlight" bolds it and brings it to the front, None leaves it unchanged. Not supported for filled contours: passing a value with filled=True raises ValueError. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None` |
| `figsize`        | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                          |
| `xmin`           | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                           |
| `xmax`           | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                           |
| `ymin`           | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                           |
| `ymax`           | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                           |
| `show_legend`    | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                      |
| `show_grid`      | Which grid lines to show (e.g., "both", "x", "y"). Off by default for filled contours. **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                          |
| `filled`         | Whether to fill the bands between the levels (colored by the colormap) instead of drawing iso-lines (in the chart's color). **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                      |
| `levels`         | Which levels cut the surface: a rule of CONTOUR_LEVELS ("auto", the default, leaves the choice to matplotlib), a target level count, or an explicit list of level values. **TYPE:** `Optional[Union[CONTOUR_LEVELS, str, int, List[float]]]` **DEFAULT:** `None`                                                                                                                                                                |
| `show_labels`    | Whether to write the level values along the iso-lines. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                           |
| `show_colorbars` | Whether to show the colorbar(s) of filled contours. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                              |
| `aspect_ratio`   | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                          |
| `scalex`         | The x-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                           |
| `scaley`         | The y-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                           |
| `subplots`       | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                              |
| `max_cols`       | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                       |
| `sharex`         | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                         |
| `sharey`         | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                         |
| `style`          | Style configuration(s) for the contour chart(s). **TYPE:** `Optional[Union[ContourStyleAttrs, List[Optional[ContourStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                          |
| `norm`           | Value normalization method(s) of the colormap. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                        |
| `vmin`           | Minimum value(s) for normalization. **TYPE:** `Optional[Union[float, List[Optional[float]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                               |
| `vmax`           | Maximum value(s) for normalization. **TYPE:** `Optional[Union[float, List[Optional[float]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                               |
| `valfmt`         | Format string(s) for the inline level labels, with the value named x (e.g., "{x:.1f}"). See VALUE_FORMAT. **TYPE:** `Optional[Union[VALUE_FORMAT, str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                               |
| `xticks`         | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                           |
| `xticklabels`    | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                          |
| `xtickrotate`    | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                |
| `yticks`         | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                           |
| `yticklabels`    | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                          |
| `ytickrotate`    | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                |
| `vlines`         | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                        |
| `hlines`         | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                      |
| `colorbar`       | Colorbar configuration(s). **TYPE:** `Optional[Union[HeatmapColorbarAttrs, List[Optional[HeatmapColorbarAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                          |
| `texts`          | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                          |

| RETURNS      | DESCRIPTION                              |
| ------------ | ---------------------------------------- |
| `plt.Figure` | The figure containing the contour chart. |

### datachart.charts.HexbinChart

```
HexbinChart(
    data: Union[HexbinDataAttrs, List[HexbinDataAttrs]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: None = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_colorbars: bool = True,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[
            HexbinStyleAttrs,
            List[Optional[HexbinStyleAttrs]],
        ]
    ] = None,
    gridsize: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    reduce: Optional[
        Union[HEXBIN_REDUCE, str, List[Optional[str]]]
    ] = None,
    mincnt: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    norm: Optional[Union[str, List[Optional[str]]]] = None,
    vmin: Optional[
        Union[float, List[Optional[float]]]
    ] = None,
    vmax: Optional[
        Union[float, List[Optional[float]]]
    ] = None,
    valfmt: Optional[
        Union[VALUE_FORMAT, str, List[Optional[str]]]
    ] = None,
    xticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    xticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    xtickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    yticks: Optional[
        Union[
            List[Union[int, float]],
            List[List[Union[int, float]]],
        ]
    ] = None,
    yticklabels: Optional[
        Union[List[str], List[List[str]]]
    ] = None,
    ytickrotate: Optional[
        Union[int, List[Optional[int]]]
    ] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[
                Union[
                    VLinePlotAttrs,
                    List[VLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[
                Union[
                    HLinePlotAttrs,
                    List[HLinePlotAttrs],
                    None,
                ]
            ],
        ]
    ] = None,
    colorbar: Optional[
        Union[
            HeatmapColorbarAttrs,
            List[Optional[HeatmapColorbarAttrs]],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None
) -> plt.Figure
```

Creates the hexbin chart.

A hexbin chart tiles the plane with hexagons and colors each by the number of points falling in it — or, with a per-point `c`, by an aggregate of those values. Use it where a scatter chart turns into an opaque blob: thousands of points, overlapping clusters, or a value that varies across the plane. For the points themselves use ScatterChart; for a smooth density estimate use ContourChart on stats.kde2d.

Added in Unreleased

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

| PARAMETER        | DESCRIPTION                                                                                                                                                                                                                                               |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`           | The points to bin: a dictionary with the x and y columns and an optional c column of per-point values, or a list of them for multiple charts/subplots. **TYPE:** `Union[HexbinDataAttrs, List[HexbinDataAttrs]]`                                          |
| `title`          | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                     |
| `xlabel`         | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                           |
| `ylabel`         | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                           |
| `subtitle`       | The subtitle(s) for individual charts. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                          |
| `emphasis`       | Not supported: a hexbin chart is a single colormapped layer with no series to mute or highlight. Passing a value raises ValueError. **TYPE:** `None` **DEFAULT:** `None`                                                                                  |
| `figsize`        | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                    |
| `xmin`           | The minimum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                     |
| `xmax`           | The maximum x-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                     |
| `ymin`           | The minimum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                     |
| `ymax`           | The maximum y-axis value. **TYPE:** `Optional[Union[int, float]]` **DEFAULT:** `None`                                                                                                                                                                     |
| `show_grid`      | Which grid lines to show (e.g., "both", "x", "y"). Off by default: the hexagons cover it. **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                 |
| `show_colorbars` | Whether to show the colorbar(s). **TYPE:** `bool` **DEFAULT:** `True`                                                                                                                                                                                     |
| `aspect_ratio`   | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                    |
| `scalex`         | The x-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                     |
| `scaley`         | The y-axis scale (e.g., "log", "linear"). **TYPE:** `Optional[Union[SCALE, str]]` **DEFAULT:** `None`                                                                                                                                                     |
| `subplots`       | Whether to create separate subplots for each chart. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                        |
| `max_cols`       | Maximum number of columns in subplots (when subplots=True). **TYPE:** `Optional[int]` **DEFAULT:** `None`                                                                                                                                                 |
| `sharex`         | Whether to share the x-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                   |
| `sharey`         | Whether to share the y-axis in subplots. **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                   |
| `style`          | Style configuration(s) for the hexbin chart(s). **TYPE:** `Optional[Union[HexbinStyleAttrs, List[Optional[HexbinStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                       |
| `gridsize`       | The number of hexagons across the x-axis; the plot_hexbin_gridsize config value by default. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                     |
| `reduce`         | How the c values in a hexagon collapse into its color, one of HEXBIN_REDUCE (the mean by default). Ignored without c, where every hexagon shows its point count. **TYPE:** `Optional[Union[HEXBIN_REDUCE, str, List[Optional[str]]]]` **DEFAULT:** `None` |
| `mincnt`         | The point count below which a hexagon stays blank; every hexagon is drawn by default. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                           |
| `norm`           | Value normalization method(s) of the colormap; "log" spreads heavy-tailed counts. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                               |
| `vmin`           | Minimum value(s) for normalization. **TYPE:** `Optional[Union[float, List[Optional[float]]]]` **DEFAULT:** `None`                                                                                                                                         |
| `vmax`           | Maximum value(s) for normalization. **TYPE:** `Optional[Union[float, List[Optional[float]]]]` **DEFAULT:** `None`                                                                                                                                         |
| `valfmt`         | Format string(s) for the colorbar tick labels, with the value named x (e.g., "{x:.0f}"). See VALUE_FORMAT. **TYPE:** `Optional[Union[VALUE_FORMAT, str, List[Optional[str]]]]` **DEFAULT:** `None`                                                        |
| `xticks`         | Custom x-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                     |
| `xticklabels`    | Custom x-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                    |
| `xtickrotate`    | Rotation angle for x-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                          |
| `yticks`         | Custom y-axis tick positions. **TYPE:** `Optional[Union[List[Union[int, float]], List[List[Union[int, float]]]]]` **DEFAULT:** `None`                                                                                                                     |
| `yticklabels`    | Custom y-axis tick labels. **TYPE:** `Optional[Union[List[str], List[List[str]]]]` **DEFAULT:** `None`                                                                                                                                                    |
| `ytickrotate`    | Rotation angle for y-axis tick labels. **TYPE:** `Optional[Union[int, List[Optional[int]]]]` **DEFAULT:** `None`                                                                                                                                          |
| `vlines`         | Vertical line(s) to plot. **TYPE:** `Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs], List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                  |
| `hlines`         | Horizontal line(s) to plot. **TYPE:** `Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs], List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]]]]` **DEFAULT:** `None`                                                                                |
| `colorbar`       | Colorbar configuration(s). **TYPE:** `Optional[Union[HeatmapColorbarAttrs, List[Optional[HeatmapColorbarAttrs]]]]` **DEFAULT:** `None`                                                                                                                    |
| `texts`          | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                    |

| RETURNS      | DESCRIPTION                             |
| ------------ | --------------------------------------- |
| `plt.Figure` | The figure containing the hexbin chart. |

### datachart.charts.ParallelCoords

```
ParallelCoords(
    data: Union[
        List[ParallelCoordsDataPointAttrs],
        List[List[ParallelCoordsDataPointAttrs]],
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[
        Union[str, List[Optional[str]]]
    ] = None,
    emphasis: Optional[
        Union[EMPHASIS, str, List[Optional[str]]]
    ] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    style: Optional[
        Union[
            ParallelCoordsStyleAttrs,
            List[Optional[ParallelCoordsStyleAttrs]],
        ]
    ] = None,
    dimensions: Optional[List[str]] = None,
    hue: Optional[Union[str, List[Optional[str]]]] = None,
    category_orders: Optional[Dict[str, List[str]]] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None
) -> plt.Figure
```

Creates the parallel coordinates chart.

Parallel coordinates draw each record as a polyline across one vertical axis per dimension. Use it to explore multivariate data: clusters show as bundles of similar lines, and correlations between neighboring dimensions show as parallel or crossing segments. Works best with a handful of dimensions; color the records by group with `hue` to compare groups.

Added in v0.7.0

Examples:

```
>>> from datachart.charts import ParallelCoords
>>> figure = ParallelCoords(
...     data=[
...         {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2, "species": "setosa"},
...         {"sepal_length": 4.9, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.2, "species": "setosa"},
...         {"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4, "species": "versicolor"},
...     ],
...     title="Iris Dataset",
...     hue="species",
...     dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"],
...     show_legend=True
... )
```

| PARAMETER         | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`            | The data points for the chart. Each data point is a dictionary where keys are dimension names and values are numeric or string values. Can optionally include a hue key for categorical coloring. **TYPE:** `Union[List[ParallelCoordsDataPointAttrs], List[List[ParallelCoordsDataPointAttrs]]]`                                                                                             |
| `title`           | The title of the chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                         |
| `xlabel`          | The x-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                               |
| `ylabel`          | The y-axis label. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                               |
| `subtitle`        | The subtitle(s) for individual charts. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                              |
| `emphasis`        | The emphasis role(s), aligned with the data rows (a single value applies to every row): "background" mutes a row (theme muted color, lowered alpha, thinner line, behind the others, no hue legend entry), "highlight" bolds it and brings it to the front among the data rows, None leaves it unchanged. **TYPE:** `Optional[Union[EMPHASIS, str, List[Optional[str]]]]` **DEFAULT:** `None` |
| `figsize`         | The size of the figure. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                        |
| `show_legend`     | Whether to show the legend (for hue categories). **TYPE:** `Optional[bool]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                               |
| `show_grid`       | Which grid lines to show (e.g., "both", "x", "y"). **TYPE:** `Optional[Union[SHOW_GRID, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                            |
| `aspect_ratio`    | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** `Optional[Union[ASPECT_RATIO, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                        |
| `style`           | Style configuration(s) for the lines. **TYPE:** `Optional[Union[ParallelCoordsStyleAttrs, List[Optional[ParallelCoordsStyleAttrs]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                     |
| `dimensions`      | List of dimension names to include and their order. If None, all columns (except hue) are auto-detected. **TYPE:** `Optional[List[str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                  |
| `hue`             | The key name in data for line coloring. String values color categorically: data points with the same hue value get the same color from color_parallel_hue. Numeric values color continuously along the theme's color_parallel_hue_continuous ramp. **TYPE:** `Optional[Union[str, List[Optional[str]]]]` **DEFAULT:** `None`                                                                  |
| `category_orders` | Dictionary mapping dimension names to lists of category values in the desired order. Example: {"rating": ["Low", "Medium", "High"]}. Categories not in the list will be appended at the end (sorted). **TYPE:** `Optional[Dict[str, List[str]]]` **DEFAULT:** `None`                                                                                                                          |
| `texts`           | Text annotation(s) to draw. **TYPE:** `Optional[Union[TextAttrs, List[TextAttrs], List[Union[TextAttrs, List[TextAttrs], None]]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                        |

| RETURNS      | DESCRIPTION                                           |
| ------------ | ----------------------------------------------------- |
| `plt.Figure` | The figure containing the parallel coordinates chart. |
