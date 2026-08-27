# Swarm Plot

This section showcases the swarm plot. It contains examples of how to create swarm plots using the [datachart.charts.SwarmPlot](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.SwarmPlot) function.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-swarm-chart), which maps common tasks to the parameter or style attribute that does the job.

As mentioned above, the swarm plots are created using the `SwarmPlot` function found in the [datachart.charts](https://eriknovak.github.io/datachart/dev/references/charts/index.md) module. Let's import it:

```
from datachart.charts import SwarmPlot
```

## Swarm Plot Input Attributes

The `SwarmPlot` function accepts keyword arguments for chart configuration. The main argument is `data`, which contains the data points. For a single swarm plot, `data` is a list of dictionaries; the points that share a `label` form one group. For multiple swarm plots, `data` is a list of lists.

```
SwarmPlot(
    data=[{                                             # A list of data points (or list of lists for multiple charts)
        "label": str,                                   # The category label
        "value": Union[int, float],                     # The numeric value
    }],
    style={                                             # The style of the points (optional)
        "plot_swarm_color":         Union[str, None],       # The point color
        "plot_swarm_alpha":         Union[float, None],     # The alpha of the points
        "plot_swarm_size":          Union[int, float, None], # The point size
        "plot_swarm_marker":        Union[str, None],       # The point marker shape
        "plot_swarm_edge_width":    Union[int, float, None], # The edge width of the points
        "plot_swarm_edge_color":    Union[str, None],       # The edge color of the points
        "plot_swarm_zorder":        Union[int, float, None], # The zorder of the points
    },
    title: Union[str, None],                            # The chart title (optional)
    xlabel: Union[str, None],                           # The x-axis label (optional)
    ylabel: Union[str, None],                           # The y-axis label (optional)
    subtitle: Union[str, List[str], None],              # The subtitle(s), used as legend labels (optional)
    emphasis: Union[str, List[str], None],              # The emphasis role(s), aligned with the group labels (optional)
    mode: Union[str, None],                             # "swarm" (the default) or "strip" (optional)
    jitter: Union[float, None],                         # The strip jitter width, a fraction of the category width (optional)
    orientation: Union[str, None],                      # "vertical" (the default) or "horizontal" (optional)
    scaley: Union[str, None],                           # The value axis scale (optional)
    figsize: Union[Tuple[float, float], None],          # The figure size (optional)
    show_legend: Union[bool, None],                     # Whether to show the legend (optional)
    show_grid: Union[str, None],                        # Which grid lines to show (optional)
    subplots: Union[bool, None],                        # Whether to draw each chart in its own subplot (optional)
    max_cols: Union[int, None],                         # The maximum number of subplot columns (optional)
    sharex: Union[bool, None],                          # Whether the subplots share the x-axis (optional)
    sharey: Union[bool, None],                          # Whether the subplots share the y-axis (optional)
    hlines: Union[dict, List[dict], None],              # The horizontal reference lines (optional)
    vlines: Union[dict, List[dict], None],              # The vertical reference lines (optional)
    label: Union[str, None],                            # The key name in `data` holding the label (optional)
    value: Union[str, None],                            # The key name in `data` holding the value (optional)
)
```

For more details, see the [datachart.charts.SwarmPlot](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.SwarmPlot) function.

## Basics

The examples in this guide share one dataset: the body mass of the 342 penguins of the [Palmer penguins](https://allisonhorst.github.io/palmerpenguins/) dataset (CC0), three species measured on the islands of the Palmer Archipelago in Antarctica. The data is hard-coded in a hidden cell, which keeps the sex and the flipper length of every penguin alongside its species — the later sections and examples reuse them. `chart_data` holds the body mass (in g) of every penguin, labeled with its species.

The data is a flat list of dictionaries, one per data point, each with a `label` and a `value`. The points that share a `label` are grouped into one swarm, so three species give three swarms:

```
chart_data[:3]
```

**Basic example.** Only the `data` argument is required to draw the swarm plot. Every penguin is one point at its species' position, and the points spread sideways just far enough not to cover each other, so the width of a swarm at any height shows how many penguins weigh that much.

```
SwarmPlot(
    # add the data to the chart
    data=chart_data
).show()
```

## Customizing the Swarm Plot

Every customization is either a keyword argument of `SwarmPlot` or a `plot_swarm_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                    | Use                                                                                | See                                                             |
| --------------------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| add a title and axis labels                   | `title`, `xlabel`, `ylabel`                                                        | [Title and axis labels](#title-and-axis-labels)                 |
| resize the figure                             | `figsize`                                                                          | [Figure size and grid](#figure-size-and-grid)                   |
| show the grid lines                           | `show_grid`                                                                        | [Figure size and grid](#figure-size-and-grid)                   |
| change the point color, size or transparency  | `style={"plot_swarm_color": ..., "plot_swarm_size": ..., "plot_swarm_alpha": ...}` | [Point style](#point-style)                                     |
| change the point marker or edge               | `style={"plot_swarm_marker": ..., "plot_swarm_edge_color": ..., ...}`              | [Point style](#point-style)                                     |
| jitter the points instead of packing them     | `mode`, `jitter`                                                                   | [Swarm and strip modes](#swarm-and-strip-modes)                 |
| draw the swarms horizontally                  | `orientation`                                                                      | [Swarm orientation](#swarm-orientation)                         |
| highlight one group, mute the rest            | `emphasis`                                                                         | [Emphasis](#emphasis)                                           |
| draw a threshold or reference line            | `hlines`, `vlines`                                                                 | [Reference lines](#reference-lines)                             |
| put the points on top of a box or violin plot | `Panel`                                                                            | [Swarms over boxes and violins](#swarms-over-boxes-and-violins) |
| draw several datasets on one chart            | `data` as a list of lists, `subtitle`                                              | [Multiple Swarm Plots](#multiple-swarm-plots)                   |
| draw each dataset in its own subplot          | `subplots`, `max_cols`, `sharex`, `sharey`                                         | [Subplots](#subplots)                                           |
| use a logarithmic value axis                  | `scaley`                                                                           | [Logarithmic scale](#logarithmic-scale)                         |
| save the chart to a file                      | `save_figure`                                                                      | [Saving the Chart as an Image](#saving-the-chart-as-an-image)   |

The full list of style attributes is in the [datachart.typings.SwarmStyleAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.SwarmStyleAttrs) type; the full list of parameters is in the [datachart.charts.SwarmPlot](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.SwarmPlot) reference.

### Title and axis labels

To add the chart title and axis labels, add the `title`, `xlabel` and `ylabel` attributes.

```
SwarmPlot(
    data=chart_data,
    # add the title
    title="Body mass of Palmer penguins",
    # add the x and y axis labels
    xlabel="Species",
    ylabel="Body mass (g)",
).show()
```

### Figure size and grid

To change the figure size, add the `figsize` attribute. The `figsize` attribute can be a tuple (width, height), values are in inches. The `datachart` package provides a [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE) constant, which contains predefined figure sizes. To show the grid lines, add the `show_grid` attribute, which supports the values of the [datachart.constants.SHOW_GRID](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID) constant.

```
from datachart.constants import FIG_SIZE, SHOW_GRID
```

```
SwarmPlot(
    data=chart_data,
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    # add to determine the figure size
    figsize=FIG_SIZE.FULL_SHORT,
    # add to show the grid lines
    show_grid=SHOW_GRID.Y,
).show()
```

### Point style

To change the point style, add the `style` attribute with the corresponding attributes. The supported attributes are shown in the [datachart.typings.SwarmStyleAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.SwarmStyleAttrs) type, which contains the following attributes:

| Attribute               | Description                                                                                                                                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_swarm_color`      | The point color.                                                                                                                                                |
| `plot_swarm_alpha`      | The alpha of the points.                                                                                                                                        |
| `plot_swarm_size`       | The point size, in points squared. The swarm packs the points from this size, so larger points spread wider.                                                    |
| `plot_swarm_marker`     | The point marker shape; see [datachart.constants.LINE_MARKER](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LINE_MARKER). |
| `plot_swarm_edge_width` | The edge width of the points.                                                                                                                                   |
| `plot_swarm_edge_color` | The edge color of the points.                                                                                                                                   |
| `plot_swarm_zorder`     | The zorder of the points.                                                                                                                                       |

```
from datachart.constants import LINE_MARKER
```

```
SwarmPlot(
    data=chart_data,
    # define the style of the points
    style={
        "plot_swarm_color": "#08519c",
        "plot_swarm_size": 12,
        "plot_swarm_alpha": 0.6,
        "plot_swarm_marker": LINE_MARKER.SQUARE,
        "plot_swarm_edge_color": "#08519c",
        "plot_swarm_edge_width": 0,
    },
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Swarm and strip modes

The `mode` attribute chooses how the points of a group spread across the category width. It supports the values of the [datachart.constants.SWARM_MODE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SWARM_MODE) constant:

| Value     | Description                                                                                                                                                                                                         |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"swarm"` | The points are packed so none overlap, from the point size at the moment the chart is drawn (the default). Axis limits changed on the figure afterwards can shift the spacing.                                      |
| `"strip"` | The points are jittered uniformly across the category width; `jitter` sets the width of the band as a fraction of the category width (0.4 by default). The jitter is seeded, so the same data draws the same chart. |

The strip mode is the faster choice for many thousands of points, where a swarm would fill its whole width anyway.

```
from datachart.constants import SWARM_MODE
```

```
SwarmPlot(
    data=chart_data,
    # jitter the points instead of packing them
    mode=SWARM_MODE.STRIP,
    # narrow the jitter band to a quarter of the category width
    jitter=0.25,
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Swarm orientation

To change the orientation of the swarms, add the `orientation` attribute, which supports the following values:

| Value          | Description                                                               |
| -------------- | ------------------------------------------------------------------------- |
| `"vertical"`   | The swarms are vertical, one per category along the x-axis (the default). |
| `"horizontal"` | The swarms are horizontal, one per category along the y-axis.             |

The `datachart` package provides the [datachart.constants.ORIENTATION](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION) constant with these values.

```
from datachart.constants import ORIENTATION
```

```
SwarmPlot(
    data=chart_data,
    # change the orientation of the swarms
    orientation=ORIENTATION.HORIZONTAL,
    title="Body mass of Palmer penguins",
    # swap the axis labels to match the orientation
    xlabel="Body mass (g)",
    ylabel="Species",
    figsize=FIG_SIZE.FULL_SHORT,
    # the value axis is now the x-axis
    show_grid=SHOW_GRID.X,
).show()
```

### Emphasis

To draw attention to one group, add the `emphasis` attribute. The `emphasis` list aligns with the group **labels** of one call, in the order the labels first appear in the data — here Adelie, Chinstrap, Gentoo. Each entry is one of the following roles:

| Role           | Description                                                      |
| -------------- | ---------------------------------------------------------------- |
| `"background"` | Mutes the group's points into the theme's muted color and alpha. |
| `"highlight"`  | Bolds the edges of the group's points.                           |
| `None`         | Leaves the group unchanged.                                      |

A single value applies to every group. The [datachart.constants.EMPHASIS](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS) constant holds the roles; the [highlighting guide](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/highlighting.ipynb) covers emphasis across chart types and themes.

```
from datachart.constants import EMPHASIS
```

```
SwarmPlot(
    data=chart_data,
    # one role per group label: Adelie, Chinstrap, Gentoo
    emphasis=[EMPHASIS.BACKGROUND, EMPHASIS.BACKGROUND, EMPHASIS.HIGHLIGHT],
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Reference lines

A reference line puts a threshold or a summary value next to the swarms. To add horizontal lines, add the `hlines` attribute with the [datachart.typings.HLinePlotAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLinePlotAttrs) typing, which is either a `dict` or a `List[dict]`; vertical lines use `vlines` and the [datachart.typings.VLinePlotAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLinePlotAttrs) typing.

```
from datachart.constants import LINE_STYLE
```

```
mean_mass = sum(penguin["value"] for penguin in chart_data) / len(chart_data)

SwarmPlot(
    data=chart_data,
    # add a horizontal line at the mean body mass of all penguins
    hlines={
        "y": mean_mass,
        "style": {
            "plot_hline_color": "#d62728",
            "plot_hline_style": LINE_STYLE.DASHED,
            "plot_hline_width": 1.5,
            "plot_hline_alpha": 0.8,
        },
    },
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Swarms over boxes and violins

A swarm shows every observation; a box plot summarizes them. To get both, compose a [datachart.charts.BoxPlot](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.BoxPlot) and a `SwarmPlot` of the same data with [datachart.utils.Panel](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel): the groups share their positions, so the points sit on the box centers, and the points draw above the boxes. The box plot's outliers are already in the swarm, so hide them with `show_outliers=False`.

```
from datachart.charts import BoxPlot, ViolinPlot
from datachart.utils import Panel
```

```
Panel(
    [
        # the boxes summarize the groups; the swarm already draws the outliers
        BoxPlot(data=chart_data, show_outliers=False),
        SwarmPlot(data=chart_data),
    ],
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel_left="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

To keep the boxes in the background, mute the box plot figure with `emphasis` and let the points carry the color.

```
Panel(
    [
        # mute the boxes into context
        {"figure": BoxPlot(data=chart_data, show_outliers=False), "emphasis": EMPHASIS.BACKGROUND},
        SwarmPlot(data=chart_data),
    ],
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel_left="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

A [datachart.charts.ViolinPlot](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.ViolinPlot) gives the same context as a smooth outline of the distribution. Draw the body only with `inner=None` — the swarm already shows where the values sit — and lower its alpha so the points stay legible.

```
Panel(
    [
        # the body only, faded behind the points
        ViolinPlot(data=chart_data, inner=None, style={"plot_violin_alpha": 0.3}),
        SwarmPlot(data=chart_data),
    ],
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel_left="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

All three compose at once: the violin body outlines the distribution, the box summarizes it, and the swarm shows every observation. One box plot and one violin plot per panel; swarms may repeat.

```
Panel(
    [
        ViolinPlot(data=chart_data, inner=None, style={"plot_violin_alpha": 0.3}),
        # a white box reads over the body; its outliers are in the swarm
        BoxPlot(
            data=chart_data,
            show_outliers=False,
            style={"plot_box_color": "#FFFFFF", "plot_box_alpha": 0.9},
        ),
        SwarmPlot(data=chart_data, style={"plot_swarm_size": 12}),
    ],
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel_left="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

## Multiple Swarm Plots

To create multiple swarm plots, pass a list of lists to the `data` argument. Each inner list holds the data points of one chart; the charts share one category axis, which lists every label in the order it first appears, and the swarms of the same label overlay at the same position in distinct colors. Per-chart attributes like `subtitle` and `style` can be passed as lists, where each element corresponds to a chart; a single value applies to every chart. The `subtitle` labels the legend.

`body_mass_by_sex` splits the penguins of the hidden cell into the 165 female and the 168 male penguins (the 9 penguins without a recorded sex are left out), one list of data points per sex.

```
SEXES = ["Female", "Male"]

# one list of data points per sex; the penguins without a recorded sex are left out
body_mass_by_sex = [
    [
        {"label": penguin["species"], "value": mass}
        for penguin in PENGUINS
        if penguin["sex"] == sex
        for mass in penguin["body_mass"]
    ]
    for sex in SEXES
]
```

```
SwarmPlot(
    # use a list of lists to define multiple swarm plots
    data=body_mass_by_sex,
    # one legend entry per chart
    subtitle=SEXES,
    title="Body mass of Palmer penguins by sex",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Subplots

To draw each chart in its own subplot, add the `subplots` attribute set to `True`. The `subtitle` becomes the subplot title and the `title`, `xlabel` and `ylabel` are positioned to be global for all charts. The `max_cols` attribute limits the number of columns, and `sharex` and `sharey` share an axis across the subplots; a shared axis is labeled once, on the outer subplots only.

```
SwarmPlot(
    data=body_mass_by_sex,
    subtitle=SEXES,
    title="Body mass of Palmer penguins by sex",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # draw each chart in its own subplot
    subplots=True,
    # the same mass axis for both charts
    sharey=True,
).show()
```

## Additional Features

### Logarithmic scale

To draw the value axis on a logarithmic scale, add the `scaley` attribute with a value of the [datachart.constants.SCALE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE) constant. The swarm packs the points in the scaled space, so they stay apart on the log axis as well. `flipper_data` from the hidden cell holds the flipper length (in mm) of every penguin; the span is narrow, so the log axis mostly shows that the packing follows it.

```
from datachart.constants import SCALE
```

```
SwarmPlot(
    data=flipper_data,
    # draw the value axis on a logarithmic scale
    scaley=SCALE.LOG,
    title="Flipper length of Palmer penguins",
    xlabel="Species",
    ylabel="Flipper length (mm)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Custom data keys

If the data points hold the label and the value under other keys, add the `label` and `value` attributes with the key names, so the data need not be reshaped.

```
flipper_records = [
    {"species": penguin["species"], "flipper_mm": length}
    for penguin in PENGUINS
    for length in penguin["flipper_length"]
]

SwarmPlot(
    data=flipper_records,
    # the keys holding the label and the value
    label="species",
    value="flipper_mm",
    title="Flipper length of Palmer penguins",
    xlabel="Species",
    ylabel="Flipper length (mm)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

## Saving the Chart as an Image

To save the chart as an image, use the [datachart.utils.save_figure](https://eriknovak.github.io/datachart/dev/references/utils#datachart.utils.save_figure) function.

```
from datachart.utils import save_figure
```

```
figure = SwarmPlot(
    data=chart_data,
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
)
save_figure(figure, "./fig_swarm_plot.png", dpi=300)
```

The figure should be saved in the current working directory.

## Real-World Examples

The following examples put the features above to work on real or realistic data. Each one states what its data is and where it comes from; the data itself lives in a hidden cell.

### Example 1: Model Benchmark Across Seeds (Box Overlay and Emphasis)

`benchmark` holds the illustrative test accuracy of five models, each trained and evaluated with 20 random seeds, drawn from a seeded generator. A box plot alone hides that 20 seeds is a small sample; the swarm on top shows every run, so a reader can tell a tight cluster from a wide one that happens to share a median. The best model is highlighted in both layers, the rest muted.

```
BEST_MODEL = "Deep + aug."
roles = [EMPHASIS.HIGHLIGHT if model == BEST_MODEL else EMPHASIS.BACKGROUND for model in MODELS]

Panel(
    [
        BoxPlot(data=benchmark, show_outliers=False, emphasis=roles),
        # the same roles align with the same labels in both layers
        SwarmPlot(data=benchmark, emphasis=roles),
    ],
    title=f"Test accuracy across {N_SEEDS} seeds",
    xlabel="Model",
    ylabel_left="Test accuracy",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Example 2: Service Response Times (Strip Mode, Log Scale and an SLA Line)

`response_times` holds the illustrative response time (in ms) of 300 requests to each of four services, drawn from a seeded log-normal generator: most requests are fast and a long tail of slow ones stretches each distribution. On a log axis the tail reads at the same resolution as the bulk, and with 1,200 points the strip mode spreads them evenly instead of packing a swarm that would fill its width anyway. The horizontal line marks the service level agreement, so the requests that breach it are the points above it.

```
SwarmPlot(
    data=response_times,
    # jitter the many points evenly across the category width
    mode=SWARM_MODE.STRIP,
    # the long tail reads at the same resolution as the bulk
    scaley=SCALE.LOG,
    # mark the service level agreement
    hlines={
        "y": SLA_MS,
        "style": {
            "plot_hline_color": "#d62728",
            "plot_hline_style": LINE_STYLE.DASHED,
            "plot_hline_width": 1.5,
        },
    },
    style={"plot_swarm_size": 8, "plot_swarm_alpha": 0.5, "plot_swarm_edge_width": 0},
    title=f"Response time of {N_REQUESTS} requests per service",
    xlabel="Service",
    ylabel="Response time (ms)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Example 3: Daily Temperatures by Month (Horizontal Swarms and Many Categories)

`daily_temperatures` holds one year of daily mean temperatures (in °C) in Ljubljana, drawn from a seeded generator around the published 1991–2020 monthly climate normals of the city's weather station, with the larger day-to-day swings of the winter months. Twelve labeled swarms read best top to bottom, and a vertical line marks the freezing point, so the days below zero are the points to its left.

```
SwarmPlot(
    data=daily_temperatures,
    # twelve labeled swarms read best top to bottom
    orientation=ORIENTATION.HORIZONTAL,
    # mark the freezing point
    vlines={
        "x": 0,
        "style": {
            "plot_vline_color": "#4c72b0",
            "plot_vline_style": LINE_STYLE.DASHED,
            "plot_vline_width": 1.5,
        },
    },
    style={"plot_swarm_size": 10},
    title="Daily mean temperature in Ljubljana",
    xlabel="Temperature (°C)",
    ylabel="Month",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.X,
).show()
```
