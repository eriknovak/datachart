# Grid

This section showcases the grid. It contains examples of how to arrange several charts in a grid of cells using the [datachart.utils.Grid](https://eriknovak.github.io/datachart/0.8.1/references/utils/#datachart.utils.Grid) function.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-grid), which maps common tasks to the parameter or layout option that does the job.

A grid does not draw data of its own: it takes figures already drawn by the chart functions of the [datachart.charts](https://eriknovak.github.io/datachart/0.8.1/references/charts/index.md) module — any of the charts from the [Charts](https://eriknovak.github.io/datachart/0.8.1/how-to-guides/charts/index.md) guides — and redraws each one into its own cell of one combined figure. Where the [Panel](https://eriknovak.github.io/datachart/0.8.1/how-to-guides/utility/panel/index.md) overlays figures in one coordinate space, the grid keeps every figure in a coordinate space of its own: reach for a panel to read series against each other, and for a grid to compare them side by side. The `Grid` function is found in the [datachart.utils](https://eriknovak.github.io/datachart/0.8.1/references/utils/index.md) module. Let's import it, together with the two chart functions the examples below arrange:

```
from datachart.charts import BarChart, LineChart
from datachart.utils import Grid
```

## Grid Input Attributes

The `Grid` function accepts a list of figures as its first argument and keyword arguments for the grid configuration. The list comes in two forms: nested rows, where each inner list is one row of the grid, or a flat list that the grid arranges automatically.

```
Grid(
    [                                                   # Nested rows: each inner list is one grid row of
        [Figure, Figure],                               #   bare datachart figures, where
        [Figure, None],                                 #   None leaves a blank cell
    ],
    # or
    [                                                   # A flat list arranged automatically, each item either
        Figure,                                         #   a bare datachart figure, or
        {                                               #   a dict with the figure and its layout options
            "figure": Figure,                           # The datachart figure (required)
            "layout_spec": Optional[dict],              # The cell of the figure ("row", "col", "rowspan", "colspan")
        },
    ],
    title=Optional[str],                                # The title of the grid
    max_cols=int,                                       # The column cap of the flat-list automatic layout (default: 4)
    figsize=Optional[Tuple[float, float]],              # The figure size in inches (default: calculated from the first figure)
    sharex=bool,                                        # Whether the cells share the x-axis (default: False)
    sharey=bool,                                        # Whether the cells share the y-axis (default: False)
)
```

For more details, see the [datachart.utils.Grid](https://eriknovak.github.io/datachart/0.8.1/references/utils/#datachart.utils.Grid) function. The reference is generated from the function itself, so it always lists the current parameters and layout options.

## Basics

The examples in this guide share one dataset: the monthly climate normals of Slovenian weather stations — for Ljubljana the mean temperature (in °C), the total precipitation (in mm), the sunshine duration (in hours) and the mean relative humidity (in %) of each month, and for two contrasting stations, coastal Portorož and mountain Kredarica, the mean temperature. The values are rounded from the published normals. The data lives in a hidden cell.

A grid arranges figures, so the first step is to draw each chart on its own. The `title` of a chart becomes the heading of its cell in the grid (with the `subtitle` as the fallback), so each part is named where it is drawn:

```
temperature = LineChart(data=temperature_data, title="Temperature (°C)")
precipitation = BarChart(data=precipitation_data, title="Precipitation (mm)")
sunshine = BarChart(data=sunshine_data, title="Sunshine (hours)")
humidity = LineChart(data=humidity_data, title="Humidity (%)")
```

**Basic example.** Only the list of figures is required to draw the grid. A flat list is arranged automatically into rows of up to `max_cols` cells, so two figures make one row of two. Each cell keeps its own axes and scales — the [Sharing axes](#sharing-axes) section shows how to align them:

```
Grid(
    # add the figures to the grid
    [temperature, precipitation]
).show()
```

## Customizing the Grid

Every customization is either a keyword argument of `Grid` or the shape of the list it is given — nested rows, or a flat list with layout options. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                           | Use                             | See                                                           |
| ------------------------------------ | ------------------------------- | ------------------------------------------------------------- |
| add a title over the whole grid      | `title`                         | [Title](#title)                                               |
| let the grid lay the figures out     | a flat list, `max_cols`         | [Automatic layout](#automatic-layout)                         |
| set the rows myself                  | nested rows                     | [Nested rows](#nested-rows)                                   |
| leave a cell blank                   | `None` in a row                 | [Nested rows](#nested-rows)                                   |
| resize the figure                    | `figsize`                       | [Figure size](#figure-size)                                   |
| compare the cells on one scale       | `sharex`, `sharey`              | [Sharing axes](#sharing-axes)                                 |
| span a figure across rows or columns | per-figure `"layout_spec"`      | [Irregular layouts](#irregular-layouts)                       |
| use a grid or a panel as one cell    | nest `Grid` and `Panel` figures | [Nesting grids and panels](#nesting-grids-and-panels)         |
| save the grid to a file              | `save_figure`                   | [Saving the Chart as an Image](#saving-the-chart-as-an-image) |

The full list of parameters is in the [datachart.utils.Grid](https://eriknovak.github.io/datachart/0.8.1/references/utils/#datachart.utils.Grid) function. The look of each figure — colors, line widths, markers, labels — is set on the chart itself through its attributes and `style`; see the guide of each chart in the [Charts](https://eriknovak.github.io/datachart/0.8.1/how-to-guides/charts/index.md) section.

### Title

To add a title over the whole grid, add the `title` attribute. The heading of each cell comes from its own chart — the `title` given to the chart function — so the grid title names the composition and the cell headings name the parts:

```
Grid(
    [temperature, precipitation],
    # add the title of the whole grid
    title="Climate of Ljubljana",
).show()
```

### Automatic layout

With a flat list, the grid computes the layout on its own: the `max_cols` attribute caps the number of columns (at 4 by default), and the number of rows follows from the number of figures. Cells left over in the last row stay hidden. The four charts of the dataset with `max_cols=2` make a 2×2 grid:

```
Grid(
    [temperature, precipitation, sunshine, humidity],
    # cap the automatic layout at two columns
    max_cols=2,
    title="Climate of Ljubljana",
).show()
```

### Nested rows

To set the layout yourself, pass nested rows: every inner list is one row of the grid, in the order given. Rows need not be equally long — the cells of a shorter row stretch to fill the width — so a single-figure row becomes a full-width headline:

```
Grid(
    [
        # the first row: one figure stretched across the full width
        [temperature],
        # the second row: three figures side by side
        [precipitation, sunshine, humidity],
    ],
    title="Climate of Ljubljana",
).show()
```

To leave a cell empty instead of stretching its neighbors, put `None` in its place:

```
Grid(
    [
        [temperature, precipitation],
        # None keeps the second cell of the row blank
        [sunshine, None],
    ],
    title="Climate of Ljubljana",
).show()
```

### Figure size

To change the figure size, add the `figsize` attribute. The `figsize` attribute can be a tuple (width, height), values are in inches; when it is not given, it is calculated from the size of the first figure and the shape of the grid. The `datachart` package provides a [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/0.8.1/references/constants/#datachart.constants.FIG_SIZE) constant, which contains the most common figure sizes:

```
from datachart.constants import FIG_SIZE
```

```
Grid(
    [temperature, precipitation, sunshine, humidity],
    max_cols=2,
    title="Climate of Ljubljana",
    # add to determine the figure size
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Sharing axes

Each cell scales its axes to its own data. That serves unrelated quantities, but misleads when the cells hold the same quantity: drawn with free y-axes, the temperatures of the three stations all fill their cell, and the curves look interchangeable —

```
station_charts = [
    LineChart(data=[{"x": i, "y": value} for i, value in enumerate(temps)], title=station)
    for station, temps in STATION_TEMPERATURES.items()
]

Grid(
    station_charts,
    title="Mean monthly temperature (°C)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

— although Kredarica, an alpine station at 2,514 m, is some fifteen degrees colder than the coast. To read every cell against the same scale, add the `sharex` and `sharey` attributes: `sharex=True` shares the x-axis across the cells and `sharey=True` the y-axis. In an automatic (flat-list) grid, shared axes are also labeled only once per row or column, which declutters the cells:

```
Grid(
    station_charts,
    # read every cell against the same y-axis
    sharey=True,
    title="Mean monthly temperature (°C)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

### Irregular layouts

Nested rows cover most layouts; for a figure that spans several rows or columns, wrap the figures of a flat list in dictionaries and add the `"layout_spec"` option — a dict with the `"row"` and `"col"` of the cell and its `"rowspan"` and `"colspan"`. Nested rows and `layout_spec` cannot be mixed in one call. Here the temperature takes the left column top to bottom, with two charts stacked to its right:

```
Grid(
    [
        # the temperature spans both rows of the left column
        {"figure": temperature, "layout_spec": {"row": 0, "col": 0, "rowspan": 2, "colspan": 1}},
        {"figure": precipitation, "layout_spec": {"row": 0, "col": 1, "rowspan": 1, "colspan": 1}},
        {"figure": sunshine, "layout_spec": {"row": 1, "col": 1, "rowspan": 1, "colspan": 1}},
    ],
    title="Climate of Ljubljana",
).show()
```

### Nesting grids and panels

Grid figures nest: a grid placed in a cell occupies exactly that cell and rebuilds its layout inside it, to any depth. The nested grid keeps its own title — drawn as a heading spanning its subgrid — and its own `sharex`/`sharey` among its own cells, while the outer grid's settings apply only to its top-level cells. [Panel](https://eriknovak.github.io/datachart/0.8.1/how-to-guides/utility/panel/index.md) figures nest the same way, so an overlay can take one cell of a grid; the reverse — a grid inside a panel — raises a `ValueError`.

```
from datachart.utils import Panel

# a panel as one cell: the climograph of the Panel guide
climograph = Panel(
    [
        {"figure": precipitation, "legend_label": "Precipitation (mm)"},
        {"figure": temperature, "legend_label": "Temperature (°C)"},
    ],
    show_legend=True,
)

# a grid as another cell, with its own title and shared x-axis
sun_and_moisture = Grid(
    [[sunshine], [humidity]],
    title="Sun and moisture",
    sharex=True,
)

Grid(
    [[climograph, sun_and_moisture]],
    title="Climate of Ljubljana",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

## Saving the Chart as an Image

To save the grid as an image, use the [datachart.utils.save_figure](https://eriknovak.github.io/datachart/0.8.1/references/utils/#datachart.utils.save_figure) function.

```
from datachart.utils import save_figure
```

```
figure = Grid(
    [temperature, precipitation, sunshine, humidity],
    max_cols=2,
    title="Climate of Ljubljana",
    figsize=FIG_SIZE.FULL_MEDIUM,
)
save_figure(figure, "./fig_grid.png", dpi=300)
```

The figure should be saved in the current working directory.

## Real-World Examples

The following examples put the features above to work on realistic data. Each one states what its data is and where it comes from; the data itself lives in a hidden cell. The chart functions they arrange are imported as needed; any chart from the [Charts](https://eriknovak.github.io/datachart/0.8.1/how-to-guides/charts/index.md) guides can take a cell of a grid.

### Example 1: Multi-Site Clinical Trial Dashboard (Nested Rows)

`recruitment` holds the illustrative cumulative number of patients recruited over 12 weeks at four trial sites, `adverse_events` the number of adverse events reported per site, and `retention` the share of recruited patients still enrolled (in %). The recruitment trend is the headline of the dashboard, so nested rows stretch it across the full top row — one multi-series line chart with its own legend — with the two per-site summaries side by side below it.

```
recruitment = LineChart(
    data=recruitment_data,
    subtitle=SITES,
    title="Cumulative recruitment (patients)",
    xlabel="Week",
    show_legend=True,
)
adverse = BarChart(data=adverse_data, title="Adverse events")
retention = BarChart(data=retention_data, title="Retention (%)")

Grid(
    [
        # the headline chart stretches across the full top row
        [recruitment],
        [adverse, retention],
    ],
    title="Multi-site clinical trial",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Example 2: Lab Sensor Monitoring (Shared Axes)

`sensors` holds 48 hours of illustrative temperature readings from six sensors — three lab rooms kept at 21 °C, two incubators at 37 °C, and a cold room at 4 °C — drawn from a seeded generator around each setpoint. All six measure the same quantity, so `sharex` and `sharey` put them on one scale: the three regimes separate at a glance, and any sensor drifting from its band would stand out immediately.

```
Grid(
    [LineChart(data=data, title=location) for location, data in sensors.items()],
    max_cols=3,
    # one scale for all sensors: the three temperature regimes separate
    sharex=True,
    sharey=True,
    title="Temperature sensors (°C, 48 h)",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Example 3: Chromatography Run Report (Irregular Layout)

`chromatogram` holds an illustrative chromatogram — the detector absorbance over 30 minutes with three seeded peaks, `calibration` the peak area of five standards of known concentration, and `peak_areas` the integrated area of the three sample peaks. The chromatogram is the record of the run, so a `"layout_spec"` spans it across both rows of the left column, with the calibration line and the quantification stacked to its right.

```
from datachart.charts import ScatterChart

Grid(
    [
        # the chromatogram spans both rows of the left column
        {
            "figure": LineChart(
                data=chromatogram,
                title="Chromatogram",
                xlabel="Retention time (min)",
                ylabel="Absorbance (AU)",
            ),
            "layout_spec": {"row": 0, "col": 0, "rowspan": 2, "colspan": 2},
        },
        {
            "figure": ScatterChart(
                data=calibration,
                title="Calibration",
                xlabel="Concentration (μM)",
                ylabel="Peak area",
            ),
            "layout_spec": {"row": 0, "col": 2, "rowspan": 1, "colspan": 1},
        },
        {
            "figure": BarChart(data=peak_areas, title="Peak areas"),
            "layout_spec": {"row": 1, "col": 2, "rowspan": 1, "colspan": 1},
        },
    ],
    title="Chromatography run report",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Example 4: City Climate Small Multiples

`city_temperatures` holds the mean monthly temperature (in °C) of eight European cities, rounded from the published climate normals. Small multiples — one small cell per group, identical axes everywhere — let the eye sweep across many groups and compare shapes rather than read single values; `sharex` and `sharey` are what make the cells comparable. Here the shape is the climate: maritime cities (Reykjavík, London, Lisbon) draw flat curves, continental ones (Helsinki, Moscow) wide seasonal swings, and Mediterranean ones (Madrid, Athens) sit high on the shared scale — all visible at a glance, from cells far too small to read a single degree off.

```
Grid(
    [LineChart(data=data, title=city) for city, data in city_data.items()],
    max_cols=4,
    # identical axes make the eight cells comparable
    sharex=True,
    sharey=True,
    title="Mean monthly temperature (°C)",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```
