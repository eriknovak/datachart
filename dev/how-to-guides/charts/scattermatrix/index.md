# Scatter Matrix

A scatter matrix is the first look at a table with several numeric columns: it draws a scatter chart for every pair of columns at once, so you can see which pairs move together, which groups separate, and where the outliers are, before picking one pair to study in a [scatter chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md). This guide shows how to create scatter matrices with the [datachart.charts.ScatterMatrix](https://eriknovak.github.io/datachart/dev/references/charts/scattermatrix/#datachart.charts.ScatterMatrix) function, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-scatter-matrix), which maps common tasks to the parameter or style attribute that does the job.

```
from datachart.charts import ScatterMatrix
```

## Basics

The examples in this guide share one dataset: the 342 penguins measured on three islands of the Palmer Archipelago, Antarctica (source: the [Palmer penguins](https://allisonhorst.github.io/palmerpenguins/) dataset, Gorman, Williams and Fraser 2014, released under CC0; the two penguins with no measurements are left out). The data lives in a hidden cell. `penguins` is a list of records, one dictionary per penguin, with four measurements (`"bill length"` and `"bill depth"` in millimeters, `"flipper length"` in millimeters, `"body mass"` in grams) and two categories (`"species"`, one of Adelie, Chinstrap and Gentoo, and `"sex"`, `None` for the nine penguins whose sex was not recorded). `MEASUREMENTS` lists the four measurement names. The table hides a trap that a scatter matrix is good at exposing: pooled over all penguins, deeper bills go with shorter ones, yet within every species the opposite is true.

Each record is one penguin:

```
penguins[:3]
```

**Basic example.** Only the `data` argument is required; `figsize` here fits the matrix to the page width, since by default every cell gets about two inches. Every numeric column becomes a dimension, in the order the columns first appear, so the four measurements make a four-by-four matrix and the text columns are left out. Each cell below the diagonal plots the variable of its row (y-axis) against the variable of its column (x-axis), the diagonal shows a histogram of each variable, and the cells above the diagonal mirror the ones below. Flipper length and body mass rise together almost on a line; the other pairs form clumps, a first hint that the table mixes groups.

```
ScatterMatrix(
    # add the data to the chart
    data=penguins,
    figsize=(6.3, 6.3),
).show()
```

## Customizing the Scatter Matrix

Every customization is either a keyword argument of `ScatterMatrix` or an attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                      | Use                             | See                                                                                                     |
| ----------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------- |
| add a title or resize the figure                | `title`, `figsize`              | [Title and figure size](#title-and-figure-size)                                                         |
| pass the table as columns instead of records    | `data` as a dictionary of lists | [Columns or records](#columns-or-records)                                                               |
| choose and order the variables                  | `dimensions`                    | [Selecting dimensions](#selecting-dimensions)                                                           |
| color the points by a category                  | `hue`                           | [Hue groups](#hue-groups)                                                                               |
| show a density curve or nothing on the diagonal | `diagonal`                      | [Diagonal](#diagonal)                                                                                   |
| drop the mirrored cells                         | `lower_only`                    | [Lower triangle only](#lower-triangle-only)                                                             |
| print the correlation of each pair              | `show_correlation`              | [Correlation](#correlation)                                                                             |
| fit a line to each group                        | `show_regression`               | [Regression lines](#regression-lines)                                                                   |
| give each cell its own axis range               | `sharex`, `sharey`              | [Shared axes](#shared-axes)                                                                             |
| show grid lines                                 | `show_grid`                     | [Grid lines](#grid-lines)                                                                               |
| title, arrange or hide the legend               | `legend`, `show_legend`         | [Legend](#legend)                                                                                       |
| restyle points, bars, curves and lines          | `style`                         | [Scatter matrix style](#scatter-matrix-style)                                                           |
| put two matrices side by side                   | `Grid`                          | [Scatter matrices in a Grid](#scatter-matrices-in-a-grid)                                               |
| change the whole look at once                   | `config.set_theme`              | [Themes](#themes)                                                                                       |
| save the chart to a file                        | `save_figure`                   | [Saving Figures](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/saving/index.md) guide |

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values:

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `diagonal`                                   | [`SCATTER_MATRIX_DIAGONAL`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCATTER_MATRIX_DIAGONAL)                                                                                                     |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |

The full list of style attributes is in the [datachart.typings.ScatterMatrixStyleAttrs](https://eriknovak.github.io/datachart/dev/references/charts/scattermatrix/#datachart.typings.ScatterMatrixStyleAttrs) type; the full list of parameters is in the [datachart.charts.ScatterMatrix](https://eriknovak.github.io/datachart/dev/references/charts/scattermatrix/#datachart.charts.ScatterMatrix) reference.

### Title and figure size

A matrix of sixteen cells needs a title to say what table it shows, and `title` adds one above the whole figure. The default size gives every cell about 2.2 inches a side, which makes a four-by-four matrix almost nine inches wide; `figsize` takes a `(width, height)` tuple in inches for the whole figure instead, and the cells stay square inside it. The title is also the place for the units, since the axis labels are the column names.

```
ScatterMatrix(
    data=penguins,
    # say what the table is, and its units
    title="Palmer penguins (mm, g)",
    # the whole figure, not one cell
    figsize=(6.3, 6.6),
).show()
```

### Columns or records

Data rarely arrives as a list of records: a CSV reader or a data frame hands over one list per column. `data` also takes a dictionary of equal-length columns, and draws the same matrix. Records suit data built row by row; columns suit data read column by column (`frame.to_dict("list")` turns a pandas data frame into this shape). Unlike most charts, a scatter matrix draws one table, so `data` is never a list of tables. Here the three bill and flipper measurements, as columns:

```
columns = {name: [penguin[name] for penguin in penguins] for name in MEASUREMENTS[:3]}

ScatterMatrix(
    # one list per column instead of one dictionary per penguin
    data=columns,
    figsize=(6.3, 6.3),
).show()
```

### Selecting dimensions

A wide table makes a matrix too large to read, and the column order decides which pairs sit next to each other. `dimensions` lists the numeric columns to plot, in order: the first labels the top row and the left column. Here the two bill measurements come first, since their relationship is the story of this guide, followed by body mass. Missing values (`None`) are left out pair by pair, so a record missing one measurement still appears in every cell that does not need it.

```
BILL_AND_MASS = ["bill length", "bill depth", "body mass"]

ScatterMatrix(
    data=penguins,
    # three measurements, bills first
    dimensions=BILL_AND_MASS,
    figsize=(6.3, 6.3),
).show()
```

### Hue groups

The clumps in the matrix above are the three species, and naming them turns clumps into an answer. `hue` names a categorical column: every category gets one color from the theme's palette, the same color in every cell, and one legend beside the matrix names them all. The diagonal overlays one histogram per category. Colored by species, the bill cells separate cleanly: Adelie penguins have short, deep bills, Gentoo penguins long, shallow ones, and Chinstrap penguins long, deep ones. The hue column must be text and must have no missing values; a numeric column raises an error, so bin it into categories first.

```
ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    # one color per species, one legend for the figure
    hue="species",
    figsize=(6.3, 5.4),
).show()
```

### Diagonal

The diagonal cell of a variable shows its own distribution, and the right view depends on the question ([SCATTER_MATRIX_DIAGONAL](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCATTER_MATRIX_DIAGONAL)). `SCATTER_MATRIX_DIAGONAL.HIST`, the default, draws a histogram: honest about the counts, but overlaid histograms of several groups get busy. `SCATTER_MATRIX_DIAGONAL.KDE` draws one smooth density curve per hue group, the clearest way to compare where the groups sit on one variable. The diagonal cell's axis shows its row's scale, like the other cells; the height of the histogram or curve is drawn to its own, unlabelled scale. The density curves show that bill length alone tells Adelie penguins apart, while bill depth alone tells Gentoo penguins apart.

```
from datachart.constants import SCATTER_MATRIX_DIAGONAL

ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    hue="species",
    # one density curve per species
    diagonal=SCATTER_MATRIX_DIAGONAL.KDE,
    figsize=(6.3, 5.4),
).show()
```

When the distributions are not the question, `SCATTER_MATRIX_DIAGONAL.NONE` leaves the diagonal blank, which suits a matrix whose readers only care about the pairs. The tick labels and variable names move to the outermost cell that is drawn:

```
ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    hue="species",
    # nothing on the diagonal
    diagonal=SCATTER_MATRIX_DIAGONAL.NONE,
    figsize=(6.3, 5.4),
).show()
```

### Lower triangle only

The cells above the diagonal repeat the cells below it with the axes swapped, so half the matrix is redundant. `lower_only=True` leaves the upper cells empty, which halves the ink and makes a large matrix easier to scan:

```
ScatterMatrix(
    data=penguins,
    hue="species",
    # draw only the cells below the diagonal
    lower_only=True,
    figsize=(6.3, 5.6),
).show()
```

With a blank diagonal as well, the empty top row and right column are dropped, so the four measurements take a three-by-three grid:

```
ScatterMatrix(
    data=penguins,
    hue="species",
    lower_only=True,
    # no diagonal: the empty top row and right column go
    diagonal=SCATTER_MATRIX_DIAGONAL.NONE,
    figsize=(6.3, 5.0),
).show()
```

### Correlation

A cloud of points shows the shape of a relationship, but not its strength as a number. `show_correlation=True` replaces the cells above the diagonal with the Pearson correlation coefficient of each pair, from -1 (a perfect falling line) to 1 (a perfect rising line). Pooled over all penguins, bill length and bill depth have a coefficient of -0.24: deeper bills seem to go with shorter ones. `lower_only` wins over `show_correlation`: with both set, the upper cells stay empty. The same coefficient is available in code as [datachart.utils.stats.correlation](https://eriknovak.github.io/datachart/dev/references/utils/stats/#datachart.utils.stats.correlation).

```
ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    # print the correlation of each pair above the diagonal
    show_correlation=True,
    figsize=(6.3, 6.3),
).show()
```

With a `hue`, each cell prints one coefficient per group, in the group's color, and the story flips. Within every species, bill length and bill depth rise together (0.39, 0.65 and 0.64), the opposite of the pooled -0.24. This is Simpson's paradox: Gentoo penguins have the longest and the shallowest bills, so pooling the species creates a falling trend that no single species has. Always split by the groups you know about before trusting a pooled coefficient.

```
ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    # one coefficient per species
    hue="species",
    show_correlation=True,
    figsize=(6.3, 5.4),
).show()
```

### Regression lines

A coefficient summarizes a trend; a line shows it where the points are. `show_regression=True` fits a least-squares line to each hue group in every scatter cell, in the group's color. In the bill cell every species slopes up, while the three clusters themselves sit on a falling diagonal: the paradox in one picture. With 342 points the lines are hard to pick out; the [Scatter matrix style](#scatter-matrix-style) section below makes them stand out.

```
ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    hue="species",
    # a least-squares line per species
    show_regression=True,
    show_correlation=True,
    figsize=(6.3, 5.4),
).show()
```

### Shared axes

By default the cells of a column share one x-axis and the cells of a row share one y-axis, the diagonal cells included: only the bottom row and the left column label their ticks, and a point sits at the same position in every cell of its row. That is what makes the matrix scannable. When a group is small and its cells cramped, `sharex=False` and `sharey=False` fit each cell to its own data instead; every cell then labels its own ticks, and the diagonal shows its counts or densities. Here only the Chinstrap penguins are plotted, so each cell zooms in on one species:

```
chinstraps = [penguin for penguin in penguins if penguin["species"] == "Chinstrap"]

ScatterMatrix(
    data=chinstraps,
    dimensions=BILL_AND_MASS,
    title="Chinstrap penguins",
    # fit every cell to its own data
    sharex=False,
    sharey=False,
    figsize=(6.3, 6.3),
).show()
```

### Grid lines

Grid lines help read a point's value off the axes of a crowded cell, far from the tick labels. `show_grid` draws them in every scatter and diagonal cell ([SHOW_GRID](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)): `SHOW_GRID.BOTH`, `SHOW_GRID.X` or `SHOW_GRID.Y`. The cells with correlation text never show them.

```
from datachart.constants import SHOW_GRID

ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    hue="species",
    # grid lines on both axes of every cell
    show_grid=SHOW_GRID.BOTH,
    figsize=(6.3, 5.4),
).show()
```

### Legend

With a `hue`, one legend to the right of the matrix names the groups, whatever the number of cells. The column name alone is often a poor legend title, and `legend` sets the `title`, the number of columns `ncols` and the `alignment` of the entries ([LEGEND_ALIGN](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN)); the legend always sits to the right, so its `location` has no effect here ([LegendSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.LegendSettingAttrs)). `show_legend=False` hides it, for a figure whose caption already names the colors.

```
ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    hue="species",
    # a proper title for the legend
    legend={"title": "Penguin species"},
    figsize=(6.3, 5.4),
).show()
```

### Scatter matrix style

With 342 penguins the points overlap, and the regression lines drown in them. `style` applies to every cell. The points take the `plot_scatter_*` attributes and the histograms the `plot_hist_*` attributes, as in the [scatter chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md) and the [histogram](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/histogram/index.md); the `plot_scatter_matrix_*` attributes style what the matrix adds: the regression lines, the correlation text, the density curves and the transparency of the overlaid histograms. The current values come from the [config](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/#what-a-theme-controls):

```
from datachart.config import config

{key: value for key, value in config.config.items() if key.startswith("plot_scatter_matrix_")}
```

Smaller, fainter points let the density show through, dashed dark lines stand out from any group color, and thin unfilled density curves keep the diagonal light:

```
from datachart.constants import LINE_STYLE

ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    hue="species",
    diagonal=SCATTER_MATRIX_DIAGONAL.KDE,
    show_regression=True,
    style={
        # smaller, fainter points
        "plot_scatter_size": 14,
        "plot_scatter_alpha": 0.4,
        # dark dashed regression lines
        "plot_scatter_matrix_regression_color": "#222222",
        "plot_scatter_matrix_regression_style": LINE_STYLE.DASHED,
        # thin density curves without a fill
        "plot_scatter_matrix_kde_width": 1.0,
        "plot_scatter_matrix_kde_alpha": 0,
    },
    figsize=(6.3, 5.4),
).show()
```

## Multiple Scatter Matrices

A scatter matrix owns its whole grid of axes, so it cannot be overlaid on another chart with [datachart.utils.Panel](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel). It can sit beside other charts, or beside another matrix, in a [datachart.utils.Grid](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Grid).

### Scatter matrices in a Grid

Two groupings of the same table are easiest to compare side by side. `Grid` places each matrix in one cell, with its title as the cell's heading. Colored by species, the two bill measurements split into three clusters; colored by sex, the colors mix within every cluster. Males have somewhat larger bills than females of their species, but the differences between species are far larger, so species is the grouping to split by. The penguins without a recorded sex are left out, since a `hue` column cannot have missing values.

```
from datachart.utils import Grid

sexed = [penguin for penguin in penguins if penguin["sex"] is not None]

by_species = ScatterMatrix(
    data=sexed,
    dimensions=["bill length", "bill depth"],
    hue="species",
    diagonal=SCATTER_MATRIX_DIAGONAL.KDE,
    legend={"title": "Species"},
    style={"plot_scatter_size": 12},
    title="By species",
)
by_sex = ScatterMatrix(
    data=sexed,
    dimensions=["bill length", "bill depth"],
    hue="sex",
    diagonal=SCATTER_MATRIX_DIAGONAL.KDE,
    legend={"title": "Sex"},
    style={"plot_scatter_size": 12},
    title="By sex",
)

# one matrix per cell
Grid([[by_species, by_sex]], title="Penguin bills", figsize=(6.3, 3.0)).show()
```

## Additional Features

### Themes

A theme sets the palette, the fonts and the marks of every cell at once, which matters for a matrix of many cells that a per-call `style` would have to restyle one attribute at a time. Apply one with [datachart.config.Config.set_theme](https://eriknovak.github.io/datachart/dev/references/config/#datachart.config.Config.set_theme); the [Theme Gallery](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/theme-gallery/index.md) shows every chart under each theme. The figure is drawn when the chart is created, so the theme is reset right after:

```
from datachart.constants import THEME

config.set_theme(THEME.MINIMAL)
figure = ScatterMatrix(
    data=penguins,
    dimensions=BILL_AND_MASS,
    hue="species",
    figsize=(6.3, 5.4),
)
config.set_theme(THEME.DEFAULT)
figure.show()
```

## Real-World Examples

The examples below put the features above to work on real or realistic data, each one answering a question. The data lives in hidden cells; each example says what its data is and where it comes from.

### Example 1: Which Car Specs Predict Fuel Economy? (Density Diagonal, Correlation and Regression)

`cars` holds four columns for the 32 cars of the classic `mtcars` table (Henderson and Velleman 1981, from the 1974 *Motor Trend* US magazine): fuel economy in miles per gallon (`"mpg"`), gross horsepower (`"horsepower"`), weight in thousands of pounds (`"weight"`) and the number of cylinders (`"cylinders"`, as text so it can color the points). The question is which spec tracks fuel economy most closely. Coloring by cylinders shows that the engine size already splits the cars into three bands, the density curves on the diagonal show how far apart the bands sit, and the correlations and regression lines show how much of the trend survives within each band. Pooled over all cars, weight (r = -0.87) and horsepower (r = -0.78) both track fuel economy. Within each engine size, weight still does (-0.65 to -0.71), while the link to horsepower weakens (-0.13 to -0.52): heavier cars use more fuel whatever their engine.

```
ScatterMatrix(
    data=cars,
    hue="cylinders",
    # one density curve per engine size
    diagonal=SCATTER_MATRIX_DIAGONAL.KDE,
    # the strength and the slope of each trend, per engine size
    show_correlation=True,
    show_regression=True,
    legend={"title": "Engine"},
    title="Fuel economy, power and weight of 32 cars (1974)",
    figsize=(6.3, 5.4),
).show()
```

### Example 2: Which Evaluation Metrics Move Together? (Lower Triangle, Blank Diagonal and Regression)

`runs` holds the scores of twenty training runs of a classifier with different decision thresholds (illustrative values): precision, recall, F1 and the mean prediction latency in milliseconds. Before reporting one metric, it is worth knowing which ones carry the same information. Only the pairs matter, so the matrix drops the redundant upper cells and the diagonal, and a regression line per cell shows the trend. Precision and recall trade off along a falling line. Recall moves more than precision across these thresholds, so F1 follows recall and falls as precision rises: reporting F1 alone would hide the precision gain. Latency is unrelated to the other three; its slopes are noise.

```
ScatterMatrix(
    data=runs,
    # only the pairs: no upper cells, no diagonal
    lower_only=True,
    diagonal=SCATTER_MATRIX_DIAGONAL.NONE,
    # the trend of each pair
    show_regression=True,
    title="Twenty training runs",
    figsize=(6.3, 6.3),
).show()
```

### Example 3: Do Sepals or Petals Tell the Iris Species Apart? (Two Matrices in a Grid)

`sepals` and `petals` hold the length and width, in centimeters, of the sepals and the petals of 150 iris flowers, 50 of each species (source: Anderson 1935, published by Fisher 1936, the classic `iris` dataset). The question is which part of the flower tells the species apart. Two small matrices in a `Grid` put the answer side by side: the sepal clouds of *versicolor* and *virginica* overlap, while the petal clouds separate all three species, *setosa* by a wide margin. The density curves on the diagonals show the same thing one measurement at a time, and one legend is enough for the two matrices.

```
sepal_matrix = ScatterMatrix(
    data=sepals,
    hue="species",
    diagonal=SCATTER_MATRIX_DIAGONAL.KDE,
    # the petal matrix names the species
    show_legend=False,
    title="Sepals (cm)",
)
petal_matrix = ScatterMatrix(
    data=petals,
    hue="species",
    diagonal=SCATTER_MATRIX_DIAGONAL.KDE,
    legend={"title": "Species"},
    title="Petals (cm)",
)

Grid(
    [[sepal_matrix, petal_matrix]],
    title="Iris flowers: which part tells the species apart?",
    figsize=(6.3, 3.0),
).show()
```
