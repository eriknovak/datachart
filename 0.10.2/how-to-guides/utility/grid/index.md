# Grid

Some questions need several charts side by side: one place against others, one quantity next to another, a headline with its details. A grid takes figures already drawn by the chart functions of the [datachart.charts](https://eriknovak.github.io/datachart/0.10.2/references/charts/index.md) module (any chart from the [Charts](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/charts/index.md) guides) and redraws each one into its own cell of one combined figure, so the reader compares them at a glance. Where the [Panel](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/utility/panel/index.md) overlays figures in one coordinate space, the grid keeps every figure in a coordinate space of its own: reach for a panel to read series against each other, and for a grid to compare them side by side. This guide shows how to build grids with the [datachart.utils.Grid](https://eriknovak.github.io/datachart/0.10.2/references/utils/#datachart.utils.Grid) function, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-grid), which maps common tasks to the parameter or layout option that does the job.

```
from datachart.charts import BarChart, LineChart
from datachart.utils import Grid
```

## Basics

The examples in this guide share one dataset: the climate of Ljubljana, set against eight other European cities. For Ljubljana, `temperature_data` holds the mean temperature (in °C) and `precipitation_data` the total precipitation (in mm) of each month, rounded from the published 1991–2020 normals of its weather station (the same values as in the [Panel](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/utility/panel/index.md) guide). `city_data` holds the mean monthly temperature of nine cities, Ljubljana included, rounded to the nearest degree from the published climate normals of each city. One chart rarely says whether a climate is mild or harsh; a grid of them does. The data lives in a hidden cell.

Each temperature data point is a dictionary with the month index as `x` and the value as `y`:

```
city_data["Ljubljana"][:3]
```

A grid arranges figures, so the first step is to draw each chart on its own. The `title` of a chart becomes the heading of its cell (with the `subtitle` as the fallback), so each part is named where it is drawn. The charts are drawn at half the page width, `HALF_SHORT` from [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.FIG_SIZE), because a grid sizes itself from its first figure (see [Figure size](#figure-size)). `city_chart` draws the temperature of one city the same way every time, with a tick every quarter so that small cells stay readable:

```
from datachart.constants import FIG_SIZE

# a tick every quarter keeps small cells readable
QUARTERS = {"xticks": [0, 3, 6, 9], "xticklabels": ["Jan", "Apr", "Jul", "Oct"]}

temperature = LineChart(
    data=temperature_data, title="Temperature (°C)", figsize=FIG_SIZE.HALF_SHORT, **QUARTERS
)
precipitation = BarChart(
    data=precipitation_data, title="Precipitation (mm)", figsize=FIG_SIZE.HALF_SHORT, xtickrotate=90
)


def city_chart(city, **kwargs):
    return LineChart(
        data=city_data[city], title=city, figsize=FIG_SIZE.HALF_SHORT, **QUARTERS, **kwargs
    )
```

**Basic example.** Only the list of figures is required. A flat list is arranged automatically into rows of up to four cells, so two figures make one row of two, and each cell keeps its own axes and scales:

```
Grid(
    # add the figures to the grid
    [temperature, precipitation]
).show()
```

## Customizing the Grid

Every customization is either a keyword argument of `Grid` or the shape of the list it is given: nested rows, or a flat list with layout options. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                            | Use                                | See                                                                                                        |
| ------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| add a title over the whole grid       | `title`                            | [Title and axis labels](#title-and-axis-labels)                                                            |
| label the axes once for every cell    | `xlabel`, `ylabel`                 | [Title and axis labels](#title-and-axis-labels)                                                            |
| resize the figure                     | `figsize`                          | [Figure size](#figure-size)                                                                                |
| let the grid lay the figures out      | a flat list, `max_cols`            | [Automatic layout](#automatic-layout)                                                                      |
| set the rows myself                   | nested rows                        | [Nested rows](#nested-rows)                                                                                |
| leave a cell blank                    | `None` in a row                    | [Blank cells](#blank-cells)                                                                                |
| compare the cells on one scale        | `sharex`, `sharey`                 | [Sharing axes](#sharing-axes)                                                                              |
| span a figure across rows or columns  | per-figure `"layout_spec"`         | [Irregular layouts](#irregular-layouts)                                                                    |
| use a grid or a panel as one cell     | nest `Grid` and `Panel` figures    | [Nesting grids and panels](#nesting-grids-and-panels)                                                      |
| put a chart with subplots in one cell | a chart drawn with `subplots=True` | [Subplot figures](#subplot-figures)                                                                        |
| annotate a chart in the grid          | the charts' `texts`, `Annotate`    | [Annotations](#annotations)                                                                                |
| save the grid to a file               | `save_figure`                      | [Saving Figures](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/utility/saving/index.md) guide |

The full list of parameters and layout options is in the [datachart.utils.Grid](https://eriknovak.github.io/datachart/0.10.2/references/utils/#datachart.utils.Grid) reference. The look of each figure (colors, line widths, markers, labels) is set on the chart itself through its attributes and `style`; see the guide of each chart in the [Charts](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/charts/index.md) section.

### Title and axis labels

A grid is one figure, and it needs one name that says what the cells have in common. `title` names the whole grid, while each cell keeps the heading of its own chart. When every cell measures the same quantity, labeling each one repeats the same words: `xlabel` and `ylabel` are drawn once for the whole grid, below the bottom row and to the left of the leftmost column. Here two cities share one quantity, so one pair of labels serves both:

```
Grid(
    [city_chart("Ljubljana"), city_chart("London")],
    # add the title of the whole grid
    title="Mean monthly temperature",
    # one label per axis for the whole grid
    xlabel="Month",
    ylabel="Temperature (°C)",
).show()
```

### Figure size

A grid needs room for every cell, and it guesses that room from its first figure: the default size is the first figure's size times the number of columns and of rows. Two half-width charts side by side fill the page width, which is why the charts above are drawn at `HALF_SHORT`; three of them in a row would be 9 inches wide and shrink on the page. `figsize` takes a `(width, height)` tuple in inches or one of the [FIG_SIZE](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.FIG_SIZE) presets, and it overrides the guess whatever the sizes of the figures inside:

```
Grid(
    [city_chart("Helsinki"), city_chart("Berlin"), city_chart("Lisbon")],
    title="Mean monthly temperature (°C)",
    # three cells in one full-width row
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

### Automatic layout

Most grids are a list of similar charts, and the only question is how many to put in a row. With a flat list the grid answers it: `max_cols` caps the number of columns (four by default), the number of rows follows from the number of figures, and cells left over in the last row stay empty. Four cities with `max_cols=2` make a 2×2 grid, which the default size fits to the page width:

```
Grid(
    [city_chart(city) for city in ["Reykjavík", "London", "Ljubljana", "Athens"]],
    # cap the automatic layout at two columns
    max_cols=2,
    title="Mean monthly temperature (°C)",
).show()
```

### Nested rows

A dashboard has a headline and its details, and the headline deserves the width. Nested rows set the layout directly: every inner list is one row of the grid, in the order given. Rows need not be equally long; the cells of a shorter row stretch to fill the width, so a single-figure row becomes a full-width headline. Here Ljubljana's precipitation heads the grid, with the temperature of three cities below it:

```
Grid(
    [
        # the first row: one figure stretched across the full width
        [precipitation],
        # the second row: three figures side by side
        [city_chart("Ljubljana"), city_chart("Berlin"), city_chart("Athens")],
    ],
    title="Climate of Ljubljana",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Blank cells

A stretched row suits a headline, but a short row in a table of equals should keep the column width of the rows above it, so that its axes line up with theirs. `None` holds the place of a missing cell. Here each row is a group of cities, the northern ones above and the southern ones below; the southern group has one city fewer, and `None` keeps its two cells the size of the ones above:

```
Grid(
    [
        [city_chart("Reykjavík"), city_chart("Helsinki"), city_chart("Moscow")],
        # None keeps the last cell of the row blank
        [city_chart("Lisbon"), city_chart("Madrid"), None],
    ],
    title="Mean monthly temperature (°C)",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Sharing axes

Each cell scales its axes to its own data. That serves unrelated quantities, but misleads when the cells hold the same one: drawn with free y-axes, the curves of Reykjavík, Ljubljana and Athens all fill their cells and look alike, although Reykjavík's warmest month is barely warmer than Athens' coldest.

```
extremes = [city_chart("Reykjavík"), city_chart("Ljubljana"), city_chart("Athens")]

Grid(
    extremes,
    title="Mean monthly temperature (°C)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

`sharex` and `sharey` put every cell on one x or y scale. Sharing is honest when the cells hold the same quantity in the same units, as here; sharing a scale between a temperature and a precipitation would squeeze one of them flat and invite a comparison that means nothing. In an automatic (flat-list) grid, shared axes are also labeled only once per row or column, which declutters the cells. With a shared y-axis the three climates separate at a glance:

```
Grid(
    extremes,
    # read every cell against the same y-axis
    sharey=True,
    title="Mean monthly temperature (°C)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

### Irregular layouts

Some layouts are not rows at all: a tall main chart with smaller ones stacked beside it. For those, wrap the figures of a flat list in dictionaries and add the per-figure `"layout_spec"` option, a dictionary with the `"row"` and `"col"` of the top-left cell and the `"rowspan"` and `"colspan"` the figure covers. Nested rows and `"layout_spec"` cannot be mixed in one call. Here Ljubljana's temperature takes the left column top to bottom, with the two extremes stacked to its right:

```
Grid(
    [
        # Ljubljana spans both rows of the left column
        {"figure": temperature, "layout_spec": {"row": 0, "col": 0, "rowspan": 2, "colspan": 1}},
        {"figure": city_chart("Reykjavík"), "layout_spec": {"row": 0, "col": 1, "rowspan": 1, "colspan": 1}},
        {"figure": city_chart("Athens"), "layout_spec": {"row": 1, "col": 1, "rowspan": 1, "colspan": 1}},
    ],
    title="Ljubljana between the extremes",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Nesting grids and panels

A dashboard is often built from parts that are compositions themselves. Grid figures nest: a grid placed in a cell occupies exactly that cell and rebuilds its layout inside it, to any depth. The nested grid keeps its own title (a heading over its cells) and its own `sharex` and `sharey` among its own cells, while the outer grid's settings apply only to its top-level cells. [Panel](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/utility/panel/index.md) figures nest the same way, so an overlay can take one cell; the reverse, a grid inside a panel, raises a `ValueError`. Here the climograph of the Panel guide sits beside a nested grid that shares its y-axis:

```
from datachart.constants import LEGEND_LOCATION
from datachart.utils import Panel

# a panel as one cell: precipitation bars and the temperature line
climograph = Panel(
    [
        {"figure": precipitation, "y_axis": "left", "legend_label": "Precipitation (mm)"},
        {"figure": temperature, "y_axis": "right", "legend_label": "Temperature (°C)"},
    ],
    title="Ljubljana (mm, °C)",
    show_legend=True,
    # the legend between the title and the axes, clear of the bars
    legend={"location": LEGEND_LOCATION.OUTSIDE_TOP},
)

# a grid as another cell, with its own title and shared y-axis
extremes_grid = Grid(
    [[city_chart("Reykjavík")], [city_chart("Athens")]],
    title="The extremes (°C)",
    sharey=True,
)

Grid(
    [[climograph, extremes_grid]],
    title="Climate of Ljubljana",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Subplot figures

A chart drawn with `subplots=True` is already a small grid, and it takes one cell as it is. The cell rebuilds the chart's subplots inside it, each headed by its `subtitle` and scaled on its own. Here the temperatures of Ljubljana and Moscow, drawn as one chart with two subplots, share a grid with Ljubljana's precipitation:

```
pair = LineChart(
    data=[city_data["Ljubljana"], city_data["Moscow"]],
    # one subplot per city, headed by its subtitle
    subtitle=["Ljubljana (°C)", "Moscow (°C)"],
    subplots=True,
    **QUARTERS,
)

Grid(
    # the subplot figure takes the whole first row
    [[pair], [precipitation]],
    title="Ljubljana and Moscow",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Annotations

A note belongs to the chart it explains, and it should not get lost when the chart moves into a grid. Notes travel with their charts in both forms: the `texts` argument of a chart function, and [datachart.utils.Annotate](https://eriknovak.github.io/datachart/0.10.2/references/utils/#datachart.utils.Annotate), which adds notes to a figure that is already drawn. The [Annotations](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/utility/annotations/index.md) guide covers both. `Annotate` does not accept a grid figure, so annotate the charts before composing them:

```
from datachart.utils import Annotate

# a note declared with the chart
warmest = LineChart(
    data=temperature_data,
    title="Temperature (°C)",
    figsize=FIG_SIZE.HALF_SHORT,
    texts={"text": "warmest: July", "x": 0.5, "y": 18, "target": (6, 22.0)},
    **QUARTERS,
)
# a note added to a chart that is already drawn
wettest = Annotate(
    precipitation,
    texts={"text": "wettest: Sep–Oct", "x": 0, "y": 135, "target": (8, 147)},
)

Grid([warmest, wettest], title="Climate of Ljubljana").show()
```

## Real-World Examples

The examples below put the features above to work on the climate data of the [Basics](#basics), each one answering a question. Any data they derive lives in hidden cells. The chart functions they arrange are imported as needed; any chart from the [Charts](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/charts/index.md) guides can take a cell of a grid.

### Example 1: Which Cities Share Ljubljana's Climate? (Small Multiples With Shared Axes)

`city_data` holds the mean monthly temperature of the nine cities. Small multiples, one small cell per city with identical axes everywhere, let the eye sweep across many groups and compare shapes rather than read single values; `sharex` and `sharey` are what make the cells comparable. Each cell draws its city over Ljubljana, muted by the `"background"` [emphasis](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/styling/highlighting/index.md), so every cell answers the question on its own. The cities are ordered from the coldest year to the warmest: the maritime cities (Reykjavík, London, Lisbon) draw flat curves, the continental ones (Helsinki, Moscow) wide swings, and Berlin follows Ljubljana almost exactly.

```
from datachart.constants import EMPHASIS

Grid(
    [
        LineChart(
            # the city over Ljubljana, muted as context
            data=[city_data["Ljubljana"], city_data[city]],
            emphasis=[EMPHASIS.BACKGROUND, None],
            title=city,
            figsize=FIG_SIZE.HALF_SHORT,
            **QUARTERS,
        )
        for city in CITIES_BY_WARMTH
    ],
    max_cols=3,
    # identical axes make the nine cells comparable
    sharex=True,
    sharey=True,
    title="Mean monthly temperature, against Ljubljana (grey)",
    xlabel="Month",
    ylabel="Temperature (°C)",
    figsize=FIG_SIZE.FULL_TALL,
).show()
```

### Example 2: Which Climates Swing the Most? (An Irregular Layout)

`swing` holds, for each city, the difference between its warmest and its coldest month (in °C), derived from `city_data`. The ranking is the answer, so a sorted horizontal bar chart of it spans two rows and two columns of a `"layout_spec"` grid, with Ljubljana highlighted and the other cities muted; the two ends of the ranking, Moscow and Reykjavík, are stacked to its right as evidence. `sharey` would also tie the bar chart to the temperature scale, so the two line charts fix the same range themselves with `ymin` and `ymax` instead.

```
from datachart.constants import ORIENTATION, SORT

ranking = BarChart(
    data=swing,
    title="Warmest minus coldest month (°C)",
    orientation=ORIENTATION.HORIZONTAL,
    # ascending from the bottom: the largest swing on top
    sort=SORT.ASCENDING,
    show_values=True,
)
# the same range on both line charts, instead of sharey
same_range = {"ymin": -10, "ymax": 25}

Grid(
    [
        # the ranking spans two rows and two columns
        {"figure": ranking, "layout_spec": {"row": 0, "col": 0, "rowspan": 2, "colspan": 2}},
        {"figure": city_chart("Moscow", **same_range), "layout_spec": {"row": 0, "col": 2, "rowspan": 1, "colspan": 1}},
        {"figure": city_chart("Reykjavík", **same_range), "layout_spec": {"row": 1, "col": 2, "rowspan": 1, "colspan": 1}},
    ],
    title="How much does the temperature swing over a year?",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Example 3: What Is a Year in Ljubljana Like? (A Dashboard of a Panel, Annotations, and a Nested Grid)

`temperature_data` and `precipitation_data` hold Ljubljana's monthly normals, and `city_data` the temperatures of two cities from Example 1, Berlin and Madrid. The dashboard answers the question in two rows. The headline is the climograph, a panel of the precipitation bars and the temperature line, with notes on the warmest and the wettest months; the notes are declared on the charts, so they travel through the panel into the grid. Below it, a nested grid with its own title and shared y-axis sets Ljubljana against a slightly colder city and a warmer one, so the reader sees where its year sits among its neighbours.

```
year_temperature = LineChart(
    data=temperature_data,
    texts={"text": "warmest: July, 22 °C", "x": 0.5, "y": 25, "target": (6, 22.0)},
)
year_precipitation = BarChart(
    data=precipitation_data,
    texts={"text": "wettest: Sep–Oct", "x": 9.6, "y": 185, "target": (8.5, 147)},
)

climograph = Panel(
    [
        {"figure": year_precipitation, "y_axis": "left", "legend_label": "Precipitation (mm)"},
        {"figure": year_temperature, "y_axis": "right", "legend_label": "Temperature (°C)"},
    ],
    # both value axes start at zero, with room for the notes
    ymin=0,
    ymax=200,
    ymin_right=0,
    ymax_right=30,
    show_legend=True,
    legend={"location": LEGEND_LOCATION.OUTSIDE_TOP, "ncols": 2},
)

neighbours = Grid(
    [
        LineChart(
            data=[city_data["Ljubljana"], city_data[city]],
            emphasis=[EMPHASIS.BACKGROUND, None],
            title=city,
            **QUARTERS,
        )
        for city in ["Berlin", "Madrid"]
    ],
    # the nested grid shares its own y-axis
    sharey=True,
    title="Against its neighbours, Ljubljana in grey (°C)",
)

Grid(
    [[climograph], [neighbours]],
    title="A year in Ljubljana",
    figsize=FIG_SIZE.FULL_TALL,
).show()
```
