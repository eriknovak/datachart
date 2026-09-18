# Parallel Coordinates

A parallel coordinates chart draws one vertical axis per variable and one line per record, so it shows many variables of many records at once: records with a similar profile run together as a bundle, and the segments between two neighboring axes show how those two variables relate (parallel segments for a positive relation, crossing segments for a negative one, a trade-off). This guide shows how to create parallel coordinates charts with the [datachart.charts.ParallelCoords](https://eriknovak.github.io/datachart/0.10.0/references/charts/parallelcoords/#datachart.charts.ParallelCoords) function, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-parallel-coordinates), which maps common tasks to the parameter or style attribute that does the job.

```
from datachart.charts import ParallelCoords
```

## Basics

The examples in this guide share one dataset: 30 penguins from the [Palmer penguins](https://allisonhorst.github.io/palmerpenguins/) dataset (Gorman, Williams and Fraser, 2014; CC0), the first ten recorded penguins of each species (Adelie, Chinstrap, Gentoo). Every penguin has four body measurements, its `bill length` and `bill depth`, its `flipper length` (all in mm) and its `body mass` (in g), and three categorical attributes: its `species`, the `island` it was observed on, and its `sex`. The data lives in a hidden cell as `penguins`, a list of one dictionary per penguin. The measurements hold a question a parallel coordinates chart answers well: do the three species differ on every measurement, or only on some?

Each data point is a dictionary: the dictionary is one line of the chart, and each key is one axis. Numeric values make a numeric axis; string values make a categorical axis with one tick per category:

```
penguins[:2]
```

**Basic example.** Only the `data` argument is required. Every key becomes an axis, in the order the keys first appear, and every axis covers its values from bottom to top (a numeric axis rounds outward to about five ticks labeled with round values, so the smallest and largest values sit at or just inside the ends). Even without color, two bundles show: a group of lines with shallow bills, long flippers and heavy bodies, and everyone else.

```
ParallelCoords(
    # add the data to the chart
    data=penguins
).show()
```

## Customizing the Parallel Coordinates

Every customization is either a keyword argument of `ParallelCoords` or a `plot_parallel_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                  | Use                                                                                    | See                                                                                                        |
| ------------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| add a title and axis labels                 | `title`, `xlabel`, `ylabel`                                                            | [Title and axis labels](#title-and-axis-labels)                                                            |
| resize the figure                           | `figsize`                                                                              | [Figure size](#figure-size)                                                                                |
| choose the axes and their order             | `dimensions`                                                                           | [Selecting and ordering dimensions](#selecting-and-ordering-dimensions)                                    |
| color the lines by a category or a value    | `hue`, `show_legend`                                                                   | [Hue](#hue)                                                                                                |
| order the categories on an axis             | `category_orders`                                                                      | [Category order](#category-order)                                                                          |
| title and place the legend                  | `legend`                                                                               | [Legend](#legend)                                                                                          |
| change the line color, alpha, width, marker | `style={"plot_parallel_color": ..., "plot_parallel_alpha": ...}`                       | [Line style](#line-style)                                                                                  |
| style the vertical axes                     | `style={"plot_parallel_axis_color": ..., "plot_parallel_axis_width": ...}`             | [Axis style](#axis-style)                                                                                  |
| style the tick marks and their labels       | `style={"plot_parallel_tick_color": ..., "plot_parallel_tick_label_size": ...}`        | [Tick marks and labels](#tick-marks-and-labels)                                                            |
| style or rotate the axis names              | `style={"plot_parallel_dim_label_size": ..., "plot_parallel_dim_label_rotation": ...}` | [Dimension labels](#dimension-labels)                                                                      |
| highlight some records, mute the rest       | `emphasis`, `emphasis_rule`                                                            | [Emphasis](#emphasis)                                                                                      |
| put a note on the chart                     | `texts`                                                                                | [Text annotations](#text-annotations)                                                                      |
| draw several sets of records on one chart   | `data` as a list of lists; `style`, `hue` per set; `dimensions`                        | [Multiple Parallel Coordinates Charts](#multiple-parallel-coordinates-charts)                              |
| use dates as an axis                        | `date` values in `data`                                                                | [Date dimensions](#date-dimensions)                                                                        |
| save the chart to a file                    | `save_figure`                                                                          | [Saving Figures](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/utility/saving/index.md) guide |

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.0/references/constants/index.md) that lists its values:

| Parameter                                    | Constant                                                                                                                                                                                                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                      |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                      |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                    |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                              |

The full list of style attributes is in the [datachart.typings.ParallelCoordsStyleAttrs](https://eriknovak.github.io/datachart/0.10.0/references/charts/parallelcoords/#datachart.typings.ParallelCoordsStyleAttrs) type; the full list of parameters is in the [datachart.charts.ParallelCoords](https://eriknovak.github.io/datachart/0.10.0/references/charts/parallelcoords/#datachart.charts.ParallelCoords) reference.

### Title and axis labels

A reader who does not know the data cannot tell what the lines stand for; `title` says it. The axes name themselves, so `xlabel` is for what they have in common (here, the attributes of a penguin). The height of a line on an axis is its position within that axis's own range, not a shared unit; `ylabel` can say so, though most charts leave it out.

```
ParallelCoords(
    data=penguins,
    # add the title
    title="Palmer penguins",
    # add the x and y axis labels
    xlabel="Penguin attribute",
    ylabel="Position within the range",
).show()
```

### Figure size

Every axis carries its tick labels beside it, so a chart with many axes needs width to keep the labels of neighbors apart. `figsize` takes a `(width, height)` tuple in inches or one of the presets in [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.FIG_SIZE), sized for a full or half page width. A full-width, short figure fits the chart into a page of text; the lines flatten, but the bundles still show. `show_grid` and `aspect_ratio` are accepted like on the other charts, but a parallel coordinates chart has no value axis for grid lines: the vertical axes are its grid.

```
from datachart.constants import FIG_SIZE

ParallelCoords(
    data=penguins,
    title="Palmer penguins",
    # a full-width, short figure
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

### Selecting and ordering dimensions

Only neighboring axes can be compared: the segments between two axes show how those two variables relate, and a relation between axes that are far apart is lost. `dimensions` lists the keys to draw, in order, so it both drops the axes a question does not need and puts the variables to compare next to each other. Here the categorical attributes go, and bill depth sits between bill length and flipper length. The segments from bill depth to flipper length cross in an X: the penguins with the shallowest bills have the longest flippers, a negative relation. The segments from flipper length to body mass run parallel: long flippers go with heavy bodies. The four measurements are the axes of most examples below, so they are kept in `MEASUREMENTS`.

```
MEASUREMENTS = ["bill length", "bill depth", "flipper length", "body mass"]

ParallelCoords(
    data=penguins,
    title="Palmer penguins: the measurements",
    # the axes to draw, in this order
    dimensions=MEASUREMENTS,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Hue

One color for every line hides which record belongs to which group. `hue` names the key the lines are colored by; the key is left out of the automatic axes, so list it in `dimensions` to keep it as an axis too.

**Categorical hue.** When the hue values are strings, every category gets its own color from the theme's `color_parallel_hue` palette, and `show_legend` names them. Colored by species, the bundles of the basic example become three profiles: the Gentoo are the heavy penguins with long flippers and shallow bills, the Adelie have the shortest bills, and the Chinstrap have deep bills like the Adelie but long ones like the Gentoo. No single axis separates all three species; the profile across the axes does.

```
ParallelCoords(
    data=penguins,
    title="Palmer penguins by species",
    dimensions=MEASUREMENTS,
    # color the lines by the species
    hue="species",
    # name the species in a legend
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

**Numeric hue.** When the hue values are numbers, the lines are shaded along the theme's `color_parallel_hue_continuous` ramp, from the lightest color at the smallest value to the darkest at the largest. A continuous hue has no legend: keep its key as an axis, and that axis is the scale. Shaded by body mass, the heaviest penguins are the darkest lines, and they can be followed back to the long-flipper, shallow-bill end of the other axes.

```
ParallelCoords(
    data=penguins,
    title="Palmer penguins by body mass",
    # the hue key stays as the last axis, which serves as the scale
    dimensions=MEASUREMENTS,
    # shade the lines by the body mass
    hue="body mass",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Category order

Categories are spaced evenly along their axis in alphabetical order, from the bottom up, and alphabetical order rarely matches the data: lines then cross on their way into a categorical axis only because of how its categories are sorted. `category_orders` maps a dimension to the order of its categories (any category left out follows, sorted). The island axis sorts as Biscoe, Dream, Torgersen, which sends the heavy Gentoo (all from Biscoe) to the bottom; putting Biscoe on top lets the heavy lines run straight across, and the crossings that remain are the Adelie, who live on all three islands.

```
ParallelCoords(
    data=penguins,
    title="Palmer penguins by island",
    dimensions=MEASUREMENTS + ["island"],
    hue="species",
    show_legend=True,
    # bottom to top, instead of alphabetical
    category_orders={"island": ["Torgersen", "Dream", "Biscoe"]},
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Legend

The default legend sits where the theme puts it, which on a chart full of lines is often over some of them. `legend` sets the `title`, the `location` from [LEGEND_LOCATION](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LEGEND_LOCATION), the number of columns `ncols`, and the `alignment` of the entries from [LEGEND_ALIGN](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LEGEND_ALIGN); a field left out falls back to the theme ([LegendSettingAttrs](https://eriknovak.github.io/datachart/0.10.0/references/typings/#datachart.typings.LegendSettingAttrs)). A titled legend in one row above the axes covers no line at all.

```
from datachart.constants import LEGEND_LOCATION

ParallelCoords(
    data=penguins,
    title="Palmer penguins by species",
    dimensions=MEASUREMENTS,
    hue="species",
    show_legend=True,
    # a titled, one-row legend above the axes
    legend={"title": "Species", "location": LEGEND_LOCATION.OUTSIDE_TOP, "ncols": 3},
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Line style

Lines pile up on a parallel coordinates chart, and the line style decides whether a dense region reads as a band or as a solid block. The `plot_parallel_*` line attributes set the color (which overrides the hue colors, so leave it out when coloring by `hue`), the alpha, the width, the line style from [LINE_STYLE](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LINE_STYLE), the marker drawn where a line crosses an axis from [LINE_MARKER](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LINE_MARKER), and the draw order (`plot_parallel_zorder`; the axes are drawn above the lines). A lower alpha lets overlapping lines darken where the records agree, and markers show where the values sit, which helps on a categorical axis where many lines meet at one tick. Any attribute left out keeps the value of the active theme.

```
from datachart.constants import LINE_STYLE, LINE_MARKER

ParallelCoords(
    data=penguins,
    # translucent lines with a marker at every axis crossing
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

The default axes are black and heavier than the lines, so they read as the frame of the chart. When the story is in the lines, lighter and thinner axes hand the attention to them: `plot_parallel_axis_color` and `plot_parallel_axis_width` set the look, and `plot_parallel_axis_zorder` the draw order (above the lines by default; the tick marks and labels are drawn just above the axes).

```
ParallelCoords(
    data=penguins,
    # light, thin axes
    style={
        "plot_parallel_axis_color": "#9a9a9a",
        "plot_parallel_axis_width": 1.0,
    },
    title="Palmer penguins by species",
    dimensions=MEASUREMENTS,
    hue="species",
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Tick marks and labels

The tick labels sit right where the lines cross the axes, so they have to stay legible over the lines. Every axis carries tick marks (about five round values on a numeric axis, one per category on a categorical one), each with a label on a background box, white at 80% alpha by default. `plot_parallel_tick_color`, `plot_parallel_tick_width` and `plot_parallel_tick_length` (a fraction of the spacing between two axes) style the marks; `plot_parallel_tick_label_size`, `plot_parallel_tick_label_color`, `plot_parallel_tick_label_bg_color` and `plot_parallel_tick_label_bg_alpha` style the labels. The example matches the marks to grey axes and puts the labels on an opaque light box, so no line shows through them.

```
ParallelCoords(
    data=penguins,
    style={
        "plot_parallel_axis_color": "#9a9a9a",
        "plot_parallel_axis_width": 1.0,
        # grey, longer tick marks
        "plot_parallel_tick_color": "#9a9a9a",
        "plot_parallel_tick_width": 1.0,
        "plot_parallel_tick_length": 0.04,
        # small labels on an opaque box
        "plot_parallel_tick_label_size": 8,
        "plot_parallel_tick_label_color": "#4a4a4a",
        "plot_parallel_tick_label_bg_color": "#f3f3f3",
        "plot_parallel_tick_label_bg_alpha": 1.0,
    },
    title="Palmer penguins by species",
    dimensions=MEASUREMENTS,
    hue="species",
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Dimension labels

The dimension labels name the axes along the bottom of the chart, and with many axes or long names they run into each other. `plot_parallel_dim_label_rotation` tilts them (in degrees), `plot_parallel_dim_label_pad` moves them away from the bottom tick labels (in points), and `plot_parallel_dim_label_size` and `plot_parallel_dim_label_color` set the font. Tilted, the names of all seven attributes of the dataset fit at full width.

```
ParallelCoords(
    data=penguins,
    # tilted, padded axis names
    style={
        "plot_parallel_dim_label_size": 10,
        "plot_parallel_dim_label_color": "#2a6f97",
        "plot_parallel_dim_label_rotation": 20,
        "plot_parallel_dim_label_pad": 10,
    },
    title="Palmer penguins",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Emphasis

When the question is about some of the records, the others should step back without leaving. `emphasis` takes one role per record, aligned with `data` (a single string applies to every record): `"background"` mutes a record (the theme's muted color, a lower alpha, a thinner line, drawn behind the rest, with no hue color and no legend entry), `"highlight"` bolds it and brings it to the front of the lines (still below the axes and labels), and `None` leaves it as it is. The roles are also the [EMPHASIS](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.EMPHASIS) constants, and the [Highlighting](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/styling/highlighting/index.md) guide covers emphasis on every chart. Singling out the Chinstrap shows the species in between: Adelie bill depth, Gentoo bill length.

```
from datachart.constants import EMPHASIS

ParallelCoords(
    data=penguins,
    # one role per penguin: the Chinstrap in front, the rest muted
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

`emphasis_rule` picks the records from the data instead. It is a one-key dictionary read against each record's numeric `hue` value: `{"top": n}` or `{"bottom": n}` by rank, `{"above": v}` or `{"below": v}` (strict), or `{"between": (lo, hi)}` (inclusive). The records that match are highlighted, the rest muted, and an explicit `emphasis` role wins over the rule. Without a numeric `hue` the rule raises a `ValueError`. The hue ramp still spans every record, muted ones included, so a highlighted line keeps the color it had before the rule; a fixed `plot_parallel_color` instead paints every line one color, while the rule still reads the `hue` values. Keeping the penguins above 5 kg answers *what do the heaviest penguins have in common*: long flippers and shallow bills.

```
ParallelCoords(
    data=penguins,
    title="Palmer penguins above 5 kg",
    dimensions=MEASUREMENTS,
    # the rule reads the body mass; the style fixes the color
    hue="body mass",
    style={"plot_parallel_color": "#0f7173"},
    # highlight the records whose hue value is above 5000 g
    emphasis_rule={"above": 5000},
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Text annotations

A crossing between two axes is easy to miss for a reader who does not know to look for it; a note points it out. `texts` places text on the chart, with an optional `target` to draw a connector. In data coordinates, `x` counts the axes from `0` (a half-integer sits between two axes) and `y` runs from `0` at the bottom of every axis to `1` at the top; `"coords": "axes"` places the text in axes fractions instead. The [Text Annotations](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/utility/annotations/index.md) guide covers placement, connectors and styling.

```
ParallelCoords(
    data=penguins,
    title="Palmer penguins by species",
    dimensions=MEASUREMENTS,
    hue="species",
    show_legend=True,
    # a note on the crossing between bill depth (axis 1) and flipper length (axis 2)
    texts={
        "text": "shallow bills, long flippers:\na negative relation",
        "x": 1.5,
        "y": 0.9,
        "target": (1.5, 0.5),
    },
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

## Multiple Parallel Coordinates Charts

To draw several sets of records on one chart, pass a list of lists to `data`. The sets share the axes: every axis spans the values of all sets together, so a value lands at the same height whichever set it is in. The per-set attributes `dimensions`, `style` and `hue` take lists aligned with `data`, and a single value applies to every set; for `dimensions` a flat list of names is that single value. The sets share one row of axes, so per-set `dimensions` lists must be equal. `subtitle` is accepted for consistency with the other charts, but the chart has no per-set heading to draw it in: the sets are told apart by their style or by the hue legend.

The example draws the Adelie and Chinstrap as a grey context and the Gentoo in a bold color over them, on the four measurements.

```
gentoo = [p for p in penguins if p["species"] == "Gentoo"]
others = [p for p in penguins if p["species"] != "Gentoo"]

ParallelCoords(
    # one list per set of records
    data=[others, gentoo],
    # one list of axes for every set
    dimensions=MEASUREMENTS,
    # one style per set: grey context, bold foreground
    style=[
        {"plot_parallel_color": "#c0c0c0", "plot_parallel_alpha": 0.8},
        {"plot_parallel_color": "#0f7173", "plot_parallel_width": 2.0},
    ],
    title="Palmer penguins: the Gentoo against the rest",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

With `hue` as a list, each set is colored by its own key, or not at all. Coloring only the Gentoo by their sex shows that, within the Gentoo, the males are the heavier half, while the other species stay a grey context. A hue key is not an axis, so the axes are still the four measurements.

```
ParallelCoords(
    data=[others, gentoo],
    dimensions=MEASUREMENTS,
    style=[{"plot_parallel_color": "#c0c0c0", "plot_parallel_alpha": 0.8}, None],
    # no hue for the context, the sex for the Gentoo
    hue=[None, "sex"],
    show_legend=True,
    title="Gentoo penguins by sex, against the rest",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

## Additional Features

### Date dimensions

A record often carries a date: a release, a survey wave, a measurement day. A dimension whose values are real temporal objects (`datetime`, `date`, `numpy.datetime64` or a pandas `Timestamp`) becomes a categorical axis ordered by time, each date printed as its ISO label; date strings are not parsed, and sort as plain text. `releases`, defined in a hidden cell, holds six illustrative releases of a mobile app: the `version`, the `released` date, the app size, the share of crash-free sessions, and the average store rating. With the date as the first axis, the segments from the date to the size run nearly parallel: the later the release, the larger the app. Highlighting release 3.0 shows the one release whose stability dropped, and its rating dropped with it.

```
ParallelCoords(
    data=releases,
    title="App releases",
    # the date is an axis ordered by time
    dimensions=["released", "size (MB)", "crash-free (%)", "rating"],
    # release 3.0 in front, the others muted
    emphasis=[
        EMPHASIS.HIGHLIGHT if r["version"] == "3.0" else EMPHASIS.BACKGROUND
        for r in releases
    ],
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

## Real-World Examples

The examples below put the features above to work on real or realistic data, each one answering a question. The data lives in hidden cells; each example says what its data is and where it comes from.

### Example 1: Heavier Cars Travel Fewer Miles per Gallon (Categorical Axis and Category Order)

`cars` holds 30 cars from the [Auto MPG](https://archive.ics.uci.edu/dataset/9/auto+mpg) dataset of the UCI Machine Learning Repository (CC BY 4.0), sold in the United States between 1970 and 1982: the `model` name, the number of `cylinders`, the `horsepower`, the `weight (lb)`, the fuel economy in `mpg`, and the region of `origin`. The question is the trade-off between size and economy, so `weight (lb)` sits right next to `mpg`, where the segments cross in an X. The model name is a label, not a variable (as an axis it would have 30 ticks), so `dimensions` leaves it out. The origin is both the `hue` and the last axis; `category_orders` puts the USA at the bottom and Japan at the top, the order the regions take on the mpg axis next to it, so the lines reach the last axis without needless crossings. The American cars have the most cylinders, the most power and the heaviest bodies, and the fewest miles per gallon; the Japanese cars are their mirror image.

```
ParallelCoords(
    data=cars,
    title="Cars of the 1970s by region of origin",
    # the model name is a label, not an axis; weight sits next to mpg
    dimensions=["cylinders", "horsepower", "weight (lb)", "mpg", "origin"],
    # color by the origin, and keep it as the last axis
    hue="origin",
    show_legend=True,
    legend={"title": "Origin", "location": LEGEND_LOCATION.OUTSIDE_RIGHT},
    # bottom to top, the order the regions take on the mpg axis
    category_orders={"origin": ["USA", "Europe", "Japan"]},
    style={"plot_parallel_alpha": 0.7, "plot_parallel_width": 1.5},
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Example 2: What the Best Runs Share (Emphasis Rule on a Numeric Hue)

`runs` holds the 24 runs of an illustrative hyperparameter search of an image classifier, in the shape a tracking tool such as MLflow or Optuna reports them: the `optimizer`, the `log10 learning rate` (the rate was sampled on a logarithmic grid from 10⁻⁴ to 10⁻², and on a linear axis the raw values would pile up at the bottom), the `batch size`, the `dropout`, the number of `epochs`, and the validation `accuracy` the run reached. A parallel coordinates chart is the standard view of such a search, and its question is which settings lead to a high score. The `hue` on the accuracy gives `emphasis_rule={"top": 3}` its values, the rule mutes all but the three best runs, and a fixed line color keeps the three equally visible (see [Emphasis](#emphasis)). The accuracy stays as the last axis, so the three lines end at the top of it, and their shared path stands out: Adam, a learning rate of 10⁻³, a dropout of 0.2 to 0.3 and 25 to 30 epochs. The batch size is where they disagree, so it matters least.

```
ParallelCoords(
    data=runs,
    title="Hyperparameter search: the three best runs",
    # the accuracy stays as the last axis
    dimensions=RUN_COLUMNS,
    # the rule ranks the runs by the hue key
    hue="accuracy",
    # keep the three most accurate runs, mute the rest
    emphasis_rule={"top": 3},
    style={"plot_parallel_color": "#c1121f"},
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Example 3: What Sets Each Penguin Species Apart (Emphasis, Notes and a Grid)

Back to the 30 Palmer penguins of the shared dataset, with one chart per species. Each chart highlights one species against the other two with `emphasis`, and a note from `texts` points at the trait that sets it apart: the Adelie's short bills, the Chinstrap's bills that are both long and deep, the Gentoo's shallow bills and long flippers. [Grid](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/utility/grid/index.md) stacks the three charts in one figure, and the notes travel with their charts. The charts draw the same records, so their axes span the same ranges and a height means the same value in each.

```
from datachart.utils import Grid

# each species' note, its position, and the point it names (x = axis index)
TRAITS = {
    "Adelie": ("short bills", (0.45, 0.1), (0.02, 0.15)),
    "Chinstrap": ("long, deep bills", (0.5, 1.05), (0.1, 0.9)),
    "Gentoo": ("shallow bills,\nlong flippers", (1.3, 0.12), (1.02, 0.05)),
}


def species_profile(species):
    # one species in front, the other two muted, and a note on its trait
    text, (x, y), target = TRAITS[species]
    return ParallelCoords(
        data=penguins,
        title=species,
        dimensions=MEASUREMENTS,
        hue="species",
        emphasis=[
            EMPHASIS.HIGHLIGHT if p["species"] == species else EMPHASIS.BACKGROUND
            for p in penguins
        ],
        texts={"text": text, "x": x, "y": y, "target": target},
    )


Grid(
    [[species_profile("Adelie")], [species_profile("Chinstrap")], [species_profile("Gentoo")]],
    title="What sets each penguin species apart",
    figsize=FIG_SIZE.FULL_TALL,
).show()
```
