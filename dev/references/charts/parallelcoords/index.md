# ParallelCoords

Each record as a polyline across one axis per dimension. The [Parallel Coordinates guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/parallelcoords/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.ParallelCoords

```
ParallelCoords(
    data: (
        list[ParallelCoordsDataPointAttrs]
        | list[list[ParallelCoordsDataPointAttrs]]
    ),
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
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    style: (
        ParallelCoordsStyleAttrs
        | list[ParallelCoordsStyleAttrs | None]
        | None
    ) = None,
    dimensions: list[str] | list[list[str]] | None = None,
    hue: str | list[str | None] | None = None,
    category_orders: dict[str, list[str]] | None = None,
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

Creates the parallel coordinates chart.

Parallel coordinates draw each record as a polyline across one vertical axis per dimension. Use it to explore multivariate data: clusters show as bundles of similar lines, and correlations between neighboring dimensions show as parallel or crossing segments. Works best with a handful of dimensions; color the records by group with `hue` to compare groups.

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

| PARAMETER         | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                               |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`            | The data points for the chart. Each data point is a dictionary where keys are dimension names and values are numeric or string values. Can optionally include a hue key for categorical coloring. **TYPE:** \`list[ParallelCoordsDataPointAttrs]                                                                                                                                                                          |
| `title`           | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                   |
| `xlabel`          | The x-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                         |
| `ylabel`          | The y-axis label. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                         |
| `subtitle`        | The subtitle(s) for individual charts. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                    |
| `emphasis`        | The emphasis role(s), aligned with the data rows (a single value applies to every row): "background" mutes a row (theme muted color, lowered alpha, thinner line, behind the others, no hue legend entry), "highlight" bolds it and brings it to the front among the data rows, None leaves it unchanged. **TYPE:** \`EMPHASIS                                                                                            |
| `emphasis_rule`   | A rule that highlights the data rows matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against each row's numeric hue value; no hue, or a non-numeric one, raises. An explicit emphasis role wins, and a count ranks across the rows of every chart. The rule takes no by. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs |
| `figsize`         | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                              |
| `show_legend`     | Whether to show the legend (for hue categories). **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                         |
| `legend`          | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                    |
| `show_grid`       | Which grid lines to show (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                |
| `aspect_ratio`    | The aspect ratio of the axes ("auto" or "equal"). See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                              |
| `style`           | Style configuration(s) for the lines. **TYPE:** \`ParallelCoordsStyleAttrs                                                                                                                                                                                                                                                                                                                                                |
| `dimensions`      | List of dimension names to include and their order. If None, all columns (except hue) are auto-detected. With several data sets, a flat list applies to every set and a list of lists gives one list per set; every set shares one axis, so the lists must be equal. **TYPE:** \`list[str]                                                                                                                                |
| `hue`             | The key name in data for line coloring. String values color categorically: data points with the same hue value get the same color from color_parallel_hue. Numeric values color continuously along the theme's color_parallel_hue_continuous ramp, which spans every row, muted ones included. **TYPE:** \`str                                                                                                            |
| `category_orders` | Dictionary mapping dimension names to lists of category values in the desired order. Example: {"rating": ["Low", "Medium", "High"]}. Categories not in the list will be appended at the end (sorted). **TYPE:** \`dict\[str, list[str]\]                                                                                                                                                                                  |
| `texts`           | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                  |

| RETURNS      | DESCRIPTION                                           |
| ------------ | ----------------------------------------------------- |
| `plt.Figure` | The figure containing the parallel coordinates chart. |

## Data

Each record in `data` is a [`ParallelCoordsDataPointAttrs`](#datachart.typings.ParallelCoordsDataPointAttrs); the `hue` parameter renames its keys.

### datachart.typings.ParallelCoordsDataPointAttrs

Bases: `TypedDict`

The data point attributes for the parallel coordinates chart.

A dictionary where keys are dimension names and values are numeric values. Can optionally include a 'hue' key for categorical coloring.

| ATTRIBUTE | DESCRIPTION                                      |
| --------- | ------------------------------------------------ |
| `hue`     | The category for color grouping. **TYPE:** \`str |

## Style

`style` takes the keys of [`ParallelCoordsStyleAttrs`](#datachart.typings.ParallelCoordsStyleAttrs). The chart also reads the shared groups it draws: text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.ParallelCoordsStyleAttrs

Bases: `TypedDict`

The typing for the parallel coordinates chart style.

| ATTRIBUTE                           | DESCRIPTION                                                                                                           |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `plot_parallel_color`               | The line color. **TYPE:** \`str                                                                                       |
| `plot_parallel_alpha`               | The alpha value of the lines. **TYPE:** \`float                                                                       |
| `plot_parallel_width`               | The line width. **TYPE:** \`int                                                                                       |
| `plot_parallel_style`               | The line style. **TYPE:** \`LINE_STYLE                                                                                |
| `plot_parallel_marker`              | The marker style for data points. **TYPE:** \`LINE_MARKER                                                             |
| `plot_parallel_zorder`              | The draw order of data lines. **TYPE:** \`int                                                                         |
| `plot_parallel_axis_color`          | The vertical axis line color. **TYPE:** \`str                                                                         |
| `plot_parallel_axis_width`          | The vertical axis line width. **TYPE:** \`int                                                                         |
| `plot_parallel_axis_zorder`         | The vertical axis line draw order. **TYPE:** \`int                                                                    |
| `plot_parallel_tick_color`          | The tick mark color. **TYPE:** \`str                                                                                  |
| `plot_parallel_tick_width`          | The tick mark line width. **TYPE:** \`int                                                                             |
| `plot_parallel_tick_length`         | The tick mark length. **TYPE:** \`float                                                                               |
| `plot_parallel_tick_label_size`     | The tick label font size. **TYPE:** \`int                                                                             |
| `plot_parallel_tick_label_color`    | The tick label font color. **TYPE:** \`str                                                                            |
| `plot_parallel_tick_label_bg_color` | The tick label background color; None draws no box and strokes the label with the value halo instead. **TYPE:** \`str |
| `plot_parallel_tick_label_bg_alpha` | The tick label background alpha. **TYPE:** \`float                                                                    |
| `plot_parallel_dim_label_size`      | The dimension label font size. **TYPE:** \`int                                                                        |
| `plot_parallel_dim_label_color`     | The dimension label font color. **TYPE:** \`str                                                                       |
| `plot_parallel_dim_label_rotation`  | The dimension label rotation. **TYPE:** \`int                                                                         |
| `plot_parallel_dim_label_pad`       | The dimension label padding from axis. **TYPE:** \`int                                                                |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                   |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                           |

## Composition

Whether the figure composes with each composition function.

| Function                                                                                     | Composes |
| -------------------------------------------------------------------------------------------- | -------- |
| [`Grid`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Grid)   | yes      |
| [`Panel`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) | yes      |
