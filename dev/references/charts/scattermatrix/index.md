# ScatterMatrix

A scatter chart for every pair of dimensions, distributions on the diagonal. The [Scatter Matrix guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scattermatrix/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.ScatterMatrix

```
ScatterMatrix(
    data: (
        dict[str, list[Any]]
        | list[ScatterMatrixRecordAttrs]
    ),
    *,
    dimensions: list[str] | None = None,
    hue: str | None = None,
    diagonal: SCATTER_MATRIX_DIAGONAL | str | None = None,
    lower_only: bool | None = None,
    show_regression: bool | None = None,
    show_correlation: bool | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    title: str | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    style: StyleAttrs | None = None
) -> plt.Figure
```

Creates a scatter matrix.

Every pair of numeric dimensions gets a scatter chart, and each dimension's own distribution sits on the diagonal. Use it to scan many variables for relationships, clusters and outliers at once, optionally split by a categorical `hue`. For two variables use ScatterChart; for many dimensions per observation read as lines, use ParallelCoords.

The figure is a grid: it nests inside Grid and cannot be overlaid with Panel.

Examples:

```
>>> from datachart.charts import ScatterMatrix
>>> figure = ScatterMatrix(
...     data={
...         "length": [5.1, 4.9, 6.3, 5.8, 7.1, 6.5],
...         "width": [3.5, 3.0, 3.3, 2.7, 3.0, 3.2],
...         "petal": [1.4, 1.4, 6.0, 5.1, 5.9, 5.1],
...         "species": ["a", "a", "b", "b", "b", "b"],
...     },
...     hue="species",
... )
>>>
>>> # records work too; correlations above the diagonal
>>> records = [
...     {"length": 5.1, "width": 3.5, "petal": 1.4},
...     {"length": 6.3, "width": 3.3, "petal": 6.0},
...     {"length": 5.8, "width": 2.7, "petal": 5.1},
... ]
>>> figure = ScatterMatrix(
...     data=records,
...     diagonal="kde",
...     show_correlation=True,
...     show_regression=True,
... )
```

| PARAMETER          | DESCRIPTION                                                                                                                                                                                                                                                                                                                                           |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`             | The observations: a dict of equal-length columns, or a list of records. Missing values (None) are left out pair by pair. **TYPE:** \`dict\[str, list[Any]\]                                                                                                                                                                                           |
| `dimensions`       | The numeric columns to plot, in order. Defaults to every numeric column except the hue, in input order. **TYPE:** \`list[str]                                                                                                                                                                                                                         |
| `hue`              | The column whose categories colour the points, one colour per category and one legend for the whole figure. A numeric column raises. **TYPE:** \`str                                                                                                                                                                                                  |
| `diagonal`         | What each dimension's own cell shows: a histogram ("hist", default), a density curve ("kde"), or nothing ("none"). See SCATTER_MATRIX_DIAGONAL. **TYPE:** \`SCATTER_MATRIX_DIAGONAL                                                                                                                                                                   |
| `lower_only`       | Whether to leave the cells above the diagonal empty. Wins over show_correlation. **TYPE:** \`bool                                                                                                                                                                                                                                                     |
| `show_regression`  | Whether to draw a least-squares line per hue group in every scatter cell. **TYPE:** \`bool                                                                                                                                                                                                                                                            |
| `show_correlation` | Whether to replace the scatters above the diagonal with the Pearson correlation of each hue group. **TYPE:** \`bool                                                                                                                                                                                                                                   |
| `sharex`           | Whether the cells of a column share one x-axis and only the bottom row labels its ticks (default True). **TYPE:** \`bool                                                                                                                                                                                                                              |
| `sharey`           | Whether the cells of a row share one y-axis and only the left column labels its ticks (default True). A diagonal cell's axis shows its row's scale too; its histogram or density curve keeps its own, unlabelled height. **TYPE:** \`bool                                                                                                             |
| `title`            | The title of the figure. **TYPE:** \`str                                                                                                                                                                                                                                                                                                              |
| `figsize`          | The size of the figure; the cells stay square inside it. Defaults to 2.2 inches per cell, shrunk so the figure is at most 6.3 inches (a full page width) wide. **TYPE:** \`FIG_SIZE                                                                                                                                                                   |
| `show_legend`      | Whether to show the legend of the hue groups (default True when hue is set). **TYPE:** \`bool                                                                                                                                                                                                                                                         |
| `legend`           | The legend setting: title, column count, alignment and location. The title defaults to the hue column's name; an empty string hides it. The location is one of the four LEGEND_LOCATION.OUTSIDE\_\* edges (default right); a legend above or below the matrix lays its entries out in one row. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs |
| `show_grid`        | Which grid lines to show in the cells (e.g., "both", "x", "y"); False draws none. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                               |
| `style`            | Style attributes for every cell: the scatter, histogram, plot text and plot_scatter_matrix\_\* keys. See ScatterMatrixStyleAttrs. **TYPE:** \`StyleAttrs                                                                                                                                                                                              |

| RETURNS      | DESCRIPTION                               |
| ------------ | ----------------------------------------- |
| `plt.Figure` | The figure containing the scatter matrix. |

| RAISES       | DESCRIPTION                                                                                                                                                                                |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ValueError` | If data is malformed or has no numeric column, a dimension is missing or not numeric, or hue is missing, has missing values, or is numeric, or the legend location is not an outside edge. |

## Data

Each record in `data` is a [`ScatterMatrixRecordAttrs`](#datachart.typings.ScatterMatrixRecordAttrs); the `hue` parameter renames its keys.

### datachart.typings.ScatterMatrixRecordAttrs

Bases: `TypedDict`

The record attributes for the scatter matrix.

A dictionary where keys are column names: numeric columns become dimensions, and one categorical column may be named as the `hue`. The same columns can be passed as one dictionary of lists instead.

| ATTRIBUTE | DESCRIPTION                                                                                   |
| --------- | --------------------------------------------------------------------------------------------- |
| `hue`     | The category for color grouping, under the column name the hue setting names. **TYPE:** \`str |

## Style

`style` takes the keys of [`StyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.StyleAttrs). Its own keys are those of [`ScatterMatrixStyleAttrs`](#datachart.typings.ScatterMatrixStyleAttrs). The chart also reads the shared groups it draws: the regression line ([`RegressionStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.RegressionStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.ScatterMatrixStyleAttrs

Bases: `TypedDict`

The typing for the scatter matrix style.

The cells take the scatter, histogram and plot text keys; these keys style what the matrix adds on top of them.

| ATTRIBUTE                                | DESCRIPTION                                                                                                 |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `plot_scatter_matrix_regression_color`   | The color of the regression lines under show_regression; None takes each hue group's color. **TYPE:** \`str |
| `plot_scatter_matrix_regression_width`   | The line width of the regression lines. **TYPE:** \`int                                                     |
| `plot_scatter_matrix_regression_style`   | The line style of the regression lines. **TYPE:** \`LINE_STYLE                                              |
| `plot_scatter_matrix_correlation_size`   | The font size of the correlation text under show_correlation. **TYPE:** \`int                               |
| `plot_scatter_matrix_correlation_weight` | The font weight of the correlation text. **TYPE:** \`FONT_WEIGHT                                            |
| `plot_scatter_matrix_kde_width`          | The line width of the diagonal density curves. **TYPE:** \`int                                              |
| `plot_scatter_matrix_kde_alpha`          | The alpha value of the fill under the diagonal density curves; 0 draws no fill. **TYPE:** \`float           |
| `plot_scatter_matrix_diagonal_alpha`     | The alpha value of the diagonal histograms, overlaid per hue group. **TYPE:** \`float                       |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `diagonal`                                   | [`SCATTER_MATRIX_DIAGONAL`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCATTER_MATRIX_DIAGONAL)                                                                                                     |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |

## Composition

Whether the figure composes with each composition function.

| Function                                                                                           | Composes |
| -------------------------------------------------------------------------------------------------- | -------- |
| [`Grid`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Grid)         | yes      |
| [`Panel`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel)       | no       |
| [`Annotate`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Annotate) | no       |
