# Parallel Coordinates

This section showcases the parallel coordinates chart. It contains examples of how to create parallel coordinates charts using the [datachart.charts.ParallelCoords](https://eriknovak.github.io/datachart/0.8.0/references/charts/#datachart.charts.ParallelCoords) function.

A parallel coordinates chart draws one vertical axis per variable and one line per data point, connecting its values across the axes. It shows many variables of many records at once, which makes it a natural fit for comparing groups in multivariate data — species of animals, models of cars, runs of a hyperparameter search.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-parallel-coordinates), which maps common tasks to the parameter or style attribute that does the job.

As mentioned above, the parallel coordinates charts are created using the `ParallelCoords` function found in the [datachart.charts](https://eriknovak.github.io/datachart/0.8.0/references/charts/index.md) module. Let's import it:

```
from datachart.charts import ParallelCoords
```

## Parallel Coordinates Input Attributes

The `ParallelCoords` function accepts keyword arguments for chart configuration. The main argument is `data`, which contains the data points. Each data point is a dictionary whose keys are the dimension names and whose values are numeric or categorical (string). For a single chart, `data` is a list of data points; for multiple charts drawn on the same axes, `data` is a list of such lists.

```
ParallelCoords(
    data=[{                                             # A list of data points (or list of lists for multiple charts)
        "dim1": Union[int, float],                      # Numeric dimension
        "dim2": Union[int, float],                      # Numeric dimension
        "dim3": str,                                    # Categorical dimension (string)
        # ... more dimensions
    }],
    style={                                             # The style of the chart (optional; or list for multiple charts)
        "plot_parallel_color":               Optional[str],          # The color of the lines (hex color code; overrides hue)
        "plot_parallel_alpha":               Optional[float],        # The alpha of the lines (how visible they are)
        "plot_parallel_width":               Optional[float],        # The width of the lines
        "plot_parallel_style":               Optional[LINE_STYLE],   # The line style (solid, dashed, etc.)
        "plot_parallel_marker":              Optional[LINE_MARKER],  # The marker drawn where a line crosses an axis
        "plot_parallel_zorder":              Optional[int],          # The draw order of the lines
        "plot_parallel_axis_color":          Optional[str],          # The color of the vertical axes (hex color code)
        "plot_parallel_axis_width":          Optional[float],        # The width of the vertical axes
        "plot_parallel_axis_zorder":         Optional[int],          # The draw order of the vertical axes
        "plot_parallel_tick_color":          Optional[str],          # The color of the tick marks (hex color code)
        "plot_parallel_tick_width":          Optional[float],        # The width of the tick marks
        "plot_parallel_tick_length":         Optional[float],        # The length of the tick marks (in axis spacings)
        "plot_parallel_tick_label_size":     Optional[float],        # The font size of the tick labels
        "plot_parallel_tick_label_color":    Optional[str],          # The font color of the tick labels (hex color code)
        "plot_parallel_tick_label_bg_color": Optional[str],          # The background color of the tick labels (hex color code)
        "plot_parallel_tick_label_bg_alpha": Optional[float],        # The background alpha of the tick labels
        "plot_parallel_dim_label_size":      Optional[float],        # The font size of the dimension labels
        "plot_parallel_dim_label_color":     Optional[str],          # The font color of the dimension labels (hex color code)
        "plot_parallel_dim_label_rotation":  Optional[float],        # The rotation of the dimension labels (degrees)
        "plot_parallel_dim_label_pad":       Optional[float],        # The padding between the axes and the dimension labels
    },
    subtitle=Optional[str],                             # The subtitle of the chart (accepted, not drawn; or list for multiple charts)
    title=Optional[str],                                # The title of the chart
    xlabel=Optional[str],                               # The x-axis label
    ylabel=Optional[str],                               # The y-axis label

    figsize=Optional[Tuple[float, float]],              # The figure size in inches
    show_legend=Optional[bool],                         # Whether to show the legend (of the hue categories)
    show_grid=Optional[str],                            # Which grid lines to show (accepted; the chart draws none)

    dimensions=Optional[List[str]],                     # The dimensions to draw, in order (default: every key but the hue)
    hue=Optional[str],                                  # The key to color the lines by (categorical or numeric; or list for multiple charts)
    category_orders=Optional[Dict[str, List[str]]],     # The order of the categories of categorical dimensions
    emphasis=Optional[Union[str, List[Optional[str]]]], # The emphasis role of every row ("background", "highlight"; or one role for all rows)
)
```

**Dimension types.** Every dimension is one vertical axis, and each axis runs from its smallest value at the bottom to its largest at the top:

- **Numeric dimensions** are normalized to the 0–1 range of the axis, with tick marks at 0 %, 25 %, 50 %, 75 % and 100 % labeled with the actual values.
- **Categorical dimensions** are detected from their string values and spaced evenly along the axis, with one labeled tick mark per category. The categories are sorted alphabetically unless `category_orders` says otherwise.

For more details, see the [datachart.charts.ParallelCoords](https://eriknovak.github.io/datachart/0.8.0/references/charts/#datachart.charts.ParallelCoords) function.

## Basics

The examples in this guide share one dataset: a sample of 30 penguins from the [Palmer penguins](https://allisonhorst.github.io/palmerpenguins/) dataset (CC0), ten of each species. Every penguin has four body measurements — bill length and depth (in mm), flipper length (in mm) and body mass (in g) — and three categorical attributes: its species, sex and the island it was observed on. The data is hard-coded in a hidden cell as `penguins`, a list of one dictionary per penguin.

The data is a plain list of dictionaries: each dictionary is one data point (one line of the chart), and each key is one dimension (one axis):

```
penguins[:2]
```

**Basic example.** Only the `data` argument is required to draw the chart. Every key becomes an axis, in the order the keys first appear: the four measurements as numeric axes, and the species, island and sex as categorical axes with one tick per category. Each penguin is one line, drawn in the theme's default color.

```
ParallelCoords(
    # add the data to the chart
    data=penguins
).show()
```

## Customizing the Parallel Coordinates

Every customization is either a keyword argument of `ParallelCoords` or a `plot_parallel_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                   | Use                                                                                         | See                                                                              |
| -------------------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| add a title and axis labels                  | `title`, `xlabel`, `ylabel`                                                                 | [Title and axis labels](#title-and-axis-labels)                                  |
| resize the figure                            | `figsize`                                                                                   | [Figure size](#figure-size)                                                      |
| choose and order the axes                    | `dimensions`                                                                                | [Selecting dimensions](#selecting-dimensions)                                    |
| color the lines by a category                | `hue`, `show_legend`                                                                        | [Hue](#hue)                                                                      |
| color the lines by a value                   | `hue` on a numeric key                                                                      | [Hue](#hue)                                                                      |
| order the categories on an axis              | `category_orders`                                                                           | [Example 1: Car Specs](#example-1-car-specs-categorical-axes-and-category-order) |
| change the line color, transparency or width | `style={"plot_parallel_color": ..., "plot_parallel_alpha": ..., ...}`                       | [Line style](#line-style)                                                        |
| style the vertical axes                      | `style={"plot_parallel_axis_color": ..., "plot_parallel_axis_width": ..., ...}`             | [Axis style](#axis-style)                                                        |
| style the tick marks and their labels        | `style={"plot_parallel_tick_color": ..., "plot_parallel_tick_label_size": ..., ...}`        | [Tick marks and labels](#tick-marks-and-labels)                                  |
| style the dimension labels                   | `style={"plot_parallel_dim_label_size": ..., "plot_parallel_dim_label_rotation": ..., ...}` | [Dimension labels](#dimension-labels)                                            |
| highlight some rows, mute the rest           | `emphasis`                                                                                  | [Emphasis](#emphasis)                                                            |
| overlay several sets of data points          | `data` as a list of lists, `style` and `hue` as lists                                       | [Multiple Parallel Coordinates Charts](#multiple-parallel-coordinates-charts)    |
| save the chart to a file                     | `save_figure`                                                                               | [Saving the Chart as an Image](#saving-the-chart-as-an-image)                    |

The full list of style attributes is in the [datachart.typings.ParallelCoordsStyleAttrs](https://eriknovak.github.io/datachart/0.8.0/references/typings/#datachart.typings.ParallelCoordsStyleAttrs) type; the full list of parameters is in the [datachart.charts.ParallelCoords](https://eriknovak.github.io/datachart/0.8.0/references/charts/#datachart.charts.ParallelCoords) reference.

### Title and axis labels

To add the chart title and axis labels, add the `title`, `xlabel` and `ylabel` attributes. The y-axis label describes what the height of a line means — the position of every value within the range of its axis — so it is rarely needed; the x-axis label names what the axes are.

```
ParallelCoords(
    data=penguins,
    # add the title
    title="Palmer penguins",
    # add the x and y axis labels
    xlabel="Measurement",
    ylabel="Position within the range",
).show()
```

### Figure size

To change the figure size, add the `figsize` attribute. The `figsize` attribute can be a tuple (width, height), values are in inches. The `datachart` package provides a [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.FIG_SIZE) constant, which contains some of the predefined figure sizes. A parallel coordinates chart grows with the number of axes, so a wide figure keeps the tick labels of neighboring axes apart.

The `show_grid` attribute of the other charts is accepted as well, but it has nothing to draw here: the chart has no y-axis ticks, and its x positions are the vertical axes themselves — they are the grid.

```
from datachart.constants import FIG_SIZE
```

```
ParallelCoords(
    data=penguins,
    title="Palmer penguins",
    # add to determine the figure size
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Selecting dimensions

By default every key of the data points is an axis, except the `hue` key. To draw a subset of the keys, or to draw them in a different order, add the `dimensions` attribute with the list of keys. The order matters: patterns are easiest to read between neighboring axes, so put the dimensions you want to compare next to each other. The example drops the island and sex and puts the flipper length next to the body mass, the two measurements that grow together. The four measurements are the axes of most examples below, so they are kept in `MEASUREMENTS`.

```
MEASUREMENTS = ["bill length", "bill depth", "flipper length", "body mass"]

ParallelCoords(
    data=penguins,
    title="Palmer penguins",
    # choose the axes and their order
    dimensions=MEASUREMENTS + ["species"],
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Hue

To color the lines by one of the keys, add the `hue` attribute with its name. The key is dropped from the auto-detected dimensions — list it in `dimensions` to keep it as an axis as well.

**Categorical hue.** When the hue values are strings, every category gets its own color from the theme's `color_parallel_hue` palette, and `show_legend` adds the legend that names them. Coloring by species is what turns the penguin sample into three readable groups: the Gentoo are the heaviest with the longest flippers, the Adelie have the shortest bills, and the Chinstrap sit in between with the deepest bills.

```
ParallelCoords(
    data=penguins,
    title="Palmer penguins",
    dimensions=MEASUREMENTS,
    # color the lines by the species
    hue="species",
    # show the legend that names the species
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

**Numeric hue.** When the hue values are numbers, the lines are colored continuously along the theme's `color_parallel_hue_continuous` ramp, from the lightest color at the smallest value to the darkest at the largest. There is no legend for a continuous hue — the axis of the hue key, kept in `dimensions`, is the scale. Coloring by the body mass makes the heaviest penguins the darkest lines on every axis.

```
ParallelCoords(
    data=penguins,
    title="Palmer penguins",
    # keep the hue key (the body mass) as an axis
    dimensions=MEASUREMENTS,
    # color the lines continuously by the body mass
    hue="body mass",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Line style

To change the style of the lines, add the `style` attribute with the corresponding attributes. The supported attributes are shown in the [datachart.typings.ParallelCoordsStyleAttrs](https://eriknovak.github.io/datachart/0.8.0/references/typings/#datachart.typings.ParallelCoordsStyleAttrs) type; the ones that style the lines are:

| Attribute                | Description                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `"plot_parallel_color"`  | The color of the lines. It overrides the hue colors, so leave it out when coloring by `hue`.                              |
| `"plot_parallel_alpha"`  | The alpha of the lines (how visible they are).                                                                            |
| `"plot_parallel_width"`  | The width of the lines.                                                                                                   |
| `"plot_parallel_style"`  | The line style (solid, dashed, etc.).                                                                                     |
| `"plot_parallel_marker"` | The marker drawn where a line crosses an axis (none by default).                                                          |
| `"plot_parallel_zorder"` | The draw order of the lines (1 by default); the axes are drawn at `plot_parallel_axis_zorder` (2 by default), above them. |

Again, to help with the style settings, the [datachart.constants](https://eriknovak.github.io/datachart/0.8.0/references/constants/index.md) module contains the following constants:

| Constant                                                                                                                             | Description                              |
| ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| [datachart.constants.LINE_STYLE](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.LINE_STYLE)   | The line style (solid, dashed, etc.).    |
| [datachart.constants.LINE_MARKER](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.LINE_MARKER) | The line markers (circle, square, etc.). |

The alpha is the attribute that matters most: lines overlap by nature, and a lower alpha lets the dense regions show as darker bands while every single line stays traceable. A marker on the axis crossings shows where the values actually sit, which helps on the categorical axes where many lines meet at the same tick. Any attribute you leave out keeps the value of the active theme.

```
from datachart.constants import LINE_STYLE, LINE_MARKER
```

```
ParallelCoords(
    data=penguins,
    # define the style of the lines
    style={
        "plot_parallel_color": "#2a6f97",
        "plot_parallel_alpha": 0.35,
        "plot_parallel_width": 1.5,
        "plot_parallel_style": LINE_STYLE.SOLID,
        "plot_parallel_marker": LINE_MARKER.CIRCLE,
    },
    title="Palmer penguins",
    dimensions=MEASUREMENTS + ["species"],
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Axis style

The vertical axes have their own style attributes:

| Attribute                     | Description                                                                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `"plot_parallel_axis_color"`  | The color of the vertical axes.                                                                                                     |
| `"plot_parallel_axis_width"`  | The width of the vertical axes.                                                                                                     |
| `"plot_parallel_axis_zorder"` | The draw order of the vertical axes (2 by default, above the lines). The tick marks and their labels are drawn just above the axes. |

The default axes are black and heavier than the lines, so they read as the frame of the chart. Lighter, thinner axes hand the attention to the lines, which suits a chart whose story is in the data rather than in the scales.

```
ParallelCoords(
    data=penguins,
    # define the style of the vertical axes
    style={
        "plot_parallel_axis_color": "#9a9a9a",
        "plot_parallel_axis_width": 1.0,
    },
    title="Palmer penguins",
    dimensions=MEASUREMENTS,
    hue="species",
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Tick marks and labels

Every axis carries tick marks — five on a numeric axis, one per category on a categorical axis — and each tick mark has a label. Both have their own style attributes:

| Attribute                             | Description                                                                                    |
| ------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `"plot_parallel_tick_color"`          | The color of the tick marks.                                                                   |
| `"plot_parallel_tick_width"`          | The width of the tick marks.                                                                   |
| `"plot_parallel_tick_length"`         | The length of the tick marks, as a fraction of the spacing between two axes (0.02 by default). |
| `"plot_parallel_tick_label_size"`     | The font size of the tick labels.                                                              |
| `"plot_parallel_tick_label_color"`    | The font color of the tick labels.                                                             |
| `"plot_parallel_tick_label_bg_color"` | The background color of the tick labels.                                                       |
| `"plot_parallel_tick_label_bg_alpha"` | The background alpha of the tick labels.                                                       |

The tick labels sit right next to the axes, where the lines cross, so they are drawn on a background box that keeps them legible over the lines; the box is white at 80 % alpha by default. The example tones the tick marks down to match the grey axes of the previous section, enlarges the labels and gives them an opaque light box so no line shows through.

```
ParallelCoords(
    data=penguins,
    style={
        "plot_parallel_axis_color": "#9a9a9a",
        "plot_parallel_axis_width": 1.0,
        # define the style of the tick marks
        "plot_parallel_tick_color": "#9a9a9a",
        "plot_parallel_tick_width": 1.0,
        "plot_parallel_tick_length": 0.04,
        # define the style of the tick labels
        "plot_parallel_tick_label_size": 9,
        "plot_parallel_tick_label_color": "#4a4a4a",
        "plot_parallel_tick_label_bg_color": "#f3f3f3",
        "plot_parallel_tick_label_bg_alpha": 1.0,
    },
    title="Palmer penguins",
    dimensions=MEASUREMENTS,
    hue="species",
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Dimension labels

The dimension labels name the axes along the bottom of the chart. Their style attributes are:

| Attribute                            | Description                                                                     |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| `"plot_parallel_dim_label_size"`     | The font size of the dimension labels.                                          |
| `"plot_parallel_dim_label_color"`    | The font color of the dimension labels.                                         |
| `"plot_parallel_dim_label_rotation"` | The rotation of the dimension labels, in degrees.                               |
| `"plot_parallel_dim_label_pad"`      | The padding between the bottom of the axes and the dimension labels, in points. |

Rotation is the attribute to reach for when the labels are long or the axes many: rotated labels no longer run into each other. A larger pad keeps them clear of the bottom tick labels.

```
ParallelCoords(
    data=penguins,
    # define the style of the dimension labels
    style={
        "plot_parallel_dim_label_size": 11,
        "plot_parallel_dim_label_color": "#2a6f97",
        "plot_parallel_dim_label_rotation": 20,
        "plot_parallel_dim_label_pad": 14,
    },
    title="Palmer penguins",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Emphasis

When the story is about some of the rows, the `emphasis` attribute tells the rest to step back. It takes one role per data point, aligned with the rows of `data` (a single string applies the same role to every row):

- `"background"` mutes a row: it takes the active theme's `muted_color` at `muted_alpha`, gets a thinner line, drops behind the other rows, and claims no hue color and no legend entry.
- `"highlight"` bolds a row and brings it to the front of the rows — but stays below the axes, tick marks and labels, so the scales remain readable.
- `None` draws the row unchanged.

The role strings are also available as constants in [datachart.constants.EMPHASIS](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.EMPHASIS). Because the background rows leave the legend, a hue legend over an emphasized chart names only the groups that are still colored. The example singles out the Chinstrap penguins: they are highlighted, the other two species are muted, and the legend names the Chinstrap alone. See the [Highlighting](https://eriknovak.github.io/datachart/0.8.0/how-to-guides/styling/highlighting/index.md) guide for how emphasis works across the other charts and in composed figures.

```
from datachart.constants import EMPHASIS
```

```
ParallelCoords(
    data=penguins,
    # one role per row: highlight the Chinstrap, mute the other species
    emphasis=[
        EMPHASIS.HIGHLIGHT if p["species"] == "Chinstrap" else EMPHASIS.BACKGROUND
        for p in penguins
    ],
    title="Palmer penguins: the Chinstrap",
    dimensions=MEASUREMENTS,
    hue="species",
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

## Multiple Parallel Coordinates Charts

To draw several sets of data points on one chart, pass a list of lists to the `data` argument. The sets share the axes: the dimensions are the union of their keys, and every axis is normalized over the values of all sets together, so the same value lands at the same height whichever set it belongs to. What the sets do not share is their style: `style` and `hue` can be passed as lists, where each element applies to the corresponding set (a single value applies to every set), so one set can be drawn in a color of its own while another is colored by its hue. The `subtitle` attribute is accepted for consistency with the other charts, but a parallel coordinates chart has no per-set heading to draw it in — the sets are told apart by their style or by the hue legend.

Multiple charts pattern

For multiple charts, `data` becomes a list of lists of data points, and per-chart attributes like `style` and `hue` become lists where each element applies to the corresponding chart.

The axes of multiple charts come from the keys of the data points, so each set is reduced to the keys it should be drawn on. The example separates the Gentoo penguins from the other two species: the Adelie and Chinstrap are drawn as a light grey context, the Gentoo in a bold color on top. The per-dimension ranges are the same as in the previous examples, because they are computed over both sets.

```
# keep only the measurements: the keys of the data points are the axes
gentoo = [{k: p[k] for k in MEASUREMENTS} for p in penguins if p["species"] == "Gentoo"]
others = [{k: p[k] for k in MEASUREMENTS} for p in penguins if p["species"] != "Gentoo"]

figure = ParallelCoords(
    # use a list of lists to define multiple charts
    data=[others, gentoo],
    # style can be a list (one per chart) or a single dict (applies to all)
    style=[
        {"plot_parallel_color": "#c0c0c0", "plot_parallel_alpha": 0.8},
        {"plot_parallel_color": "#0f7173", "plot_parallel_width": 2.0},
    ],
    title="Palmer penguins: the Gentoo against the rest",
    figsize=FIG_SIZE.FULL_MEDIUM,
)
figure.show()
```

## Saving the Chart as an Image

To save the chart as an image, use the [datachart.utils.save_figure](https://eriknovak.github.io/datachart/0.8.0/references/utils#datachart.utils.save_figure) function.

```
from datachart.utils import save_figure
```

```
save_figure(figure, "./fig_parallel_coords.png", dpi=300)
```

The figure should be saved in the current working directory.

## Real-World Examples

The following examples put the features above to work on real or realistic data. Each one states what its data is and where it comes from; the data itself lives in a hidden cell.

### Example 1: Car Specs (Categorical Axes and Category Order)

`cars` holds the specifications of 30 cars from the [Auto MPG](https://archive.ics.uci.edu/dataset/9/auto+mpg) dataset of the UCI Machine Learning Repository (CC BY 4.0), which describes cars sold in the United States between 1970 and 1982: the number of cylinders, the horsepower, the weight (in lb), the fuel consumption (in mpg) and the region of origin. The sample spans the three regions and the whole range from heavy V8 sedans to small four-cylinder imports.

Every car also has a `model` name. It is a label, not a variable — as a categorical axis it would have 30 ticks — so `dimensions` lists the axes to draw and leaves it out. The origin is both the `hue` and the last axis, which fans the lines out into the three regions at the right edge. Its categories would be sorted alphabetically (Europe, Japan, USA); `category_orders` puts the USA at the bottom and Japan at the top instead — the order the regions take on the mpg axis next to it — so the lines reach the last axis without crossing. The chart then tells the dataset's story at a glance: the American cars have the most cylinders, the most horsepower and the heaviest bodies, and travel the fewest miles per gallon; the Japanese cars are the mirror image.

```
ParallelCoords(
    data=cars,
    title="Cars of the 1970s: specifications by region of origin",
    # the model name is a label, not an axis
    dimensions=["cylinders", "horsepower", "weight (lb)", "mpg", "origin"],
    # color the lines by the origin, and keep the origin as the last axis
    hue="origin",
    show_legend=True,
    # order the origins instead of sorting them alphabetically
    category_orders={"origin": ["USA", "Europe", "Japan"]},
    style={"plot_parallel_alpha": 0.7, "plot_parallel_width": 1.5},
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Example 2: Hyperparameter Search (Numeric Hue)

`runs` holds the 24 runs of an illustrative hyperparameter search of an image classifier, in the shape a tracking tool such as Weights & Biases or Optuna reports them: each run is one combination of optimizer, learning rate, batch size, dropout and number of epochs, and the validation accuracy it reached. The learning rate was sampled on a logarithmic grid from 10⁻⁴ to 10⁻², so it is stored as its base-10 logarithm — on a linear axis the raw values would pile up at the bottom.

A parallel coordinates chart is the standard view of such a search, and its one question is which settings lead to a high score. Coloring the lines by the accuracy answers it: with the numeric `hue`, every run is shaded along the continuous ramp from the lightest (worst) to the darkest (best), and the dark lines can be followed back across the hyperparameter axes. The accuracy is kept as the last axis, so the ramp can be read off it. Here the best runs cluster around Adam, a learning rate of 10⁻³, a moderate dropout and the full 30 epochs, while the runs at either end of the learning-rate axis stay pale.

```
ParallelCoords(
    data=runs,
    title="Hyperparameter search: 24 runs colored by validation accuracy",
    # keep the accuracy as the last axis, so the color ramp can be read off it
    dimensions=RUN_COLUMNS,
    # color the lines continuously by the accuracy
    hue="accuracy",
    style={"plot_parallel_alpha": 0.8, "plot_parallel_width": 1.5},
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Example 3: Best Runs (Emphasis)

The same search, asked a sharper question: what do the three best runs have in common? The numeric hue grades every run; `emphasis` answers a yes-or-no question instead. The three runs with the highest accuracy are picked in code and given the `"highlight"` role, every other run the `"background"` role, so the field becomes a muted grey context and the three best runs are the only colored lines. The highlighted rows keep their hue color — here the categorical hue on the optimizer — and because the muted rows leave the legend, it names only the optimizer the best runs used. All three ran Adam at a learning rate of 10⁻³ with a dropout of 0.2 to 0.3 for 25 to 30 epochs; the batch size is what they disagree on.

```
best = sorted(runs, key=lambda run: run["accuracy"])[-3:]

ParallelCoords(
    data=runs,
    # highlight the three best runs, mute the rest
    emphasis=[
        EMPHASIS.HIGHLIGHT if run in best else EMPHASIS.BACKGROUND for run in runs
    ],
    title="Hyperparameter search: the three best runs",
    dimensions=RUN_COLUMNS,
    # the highlighted runs keep their hue color; the muted ones leave the legend
    hue="optimizer",
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```
