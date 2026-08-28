# Box Plot

This section showcases the box plot. It contains examples of how to create box plots using the [datachart.charts.BoxPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.BoxPlot) function.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-box-plot), which maps common tasks to the parameter or style attribute that does the job.

As mentioned above, the box plots are created using the `BoxPlot` function found in the [datachart.charts](https://eriknovak.github.io/datachart/0.9.0/references/charts/index.md) module. Let's import it:

```
from datachart.charts import BoxPlot
```

## Box Plot Input Attributes

The `BoxPlot` function accepts keyword arguments for chart configuration. The main argument is `data`, which contains the data points. For a single box plot, `data` is a list of dictionaries; the points that share a `label` form one box. For multiple box plots, `data` is a list of lists.

```
BoxPlot(
    data=[{                                             # A list of box data points (or list of lists for multiple charts)
        "label": str,                                   # The category label
        "value": Union[int, float],                     # The numeric value
    }],
    style={                                             # The style of the box (optional)
        "plot_box_color":           Union[str, None],       # The fill color of the box
        "plot_box_alpha":           Union[float, None],     # The alpha of the box
        "plot_box_linewidth":       Union[int, float, None], # The line width of the box
        "plot_box_edgecolor":       Union[str, None],       # The edge color of the box
        "plot_box_outlier_marker":  Union[str, None],       # The outlier marker style
        "plot_box_outlier_size":    Union[int, float, None], # The outlier marker size
        "plot_box_outlier_color":   Union[str, None],       # The outlier marker color
        "plot_box_outlier_edge_color": Union[str, None],    # The outlier marker edge color
        "plot_box_median_color":    Union[str, None],       # The median line color
        "plot_box_median_linewidth": Union[int, float, None], # The median line width
        "plot_box_whisker_color":   Union[str, None],       # The whisker line color
        "plot_box_whisker_linewidth": Union[int, float, None], # The whisker line width
        "plot_box_cap_color":       Union[str, None],       # The cap line color
        "plot_box_cap_linewidth":   Union[int, float, None], # The cap line width
    },
    subtitle=Optional[str],                             # The subtitle of the chart (or list for multiple charts)
    title=Optional[str],                                # The title of the chart
    xlabel=Optional[str],                               # The x-axis label
    ylabel=Optional[str],                               # The y-axis label
    emphasis=Optional[Union[str, List[Optional[str]]]], # The emphasis role per box label ("background", "highlight", None)

    figsize=Optional[Tuple[float, float]],              # The figure size in inches
    show_grid=Optional[str],                            # Which grid lines to show ("both", "x", "y")
    show_outliers=Optional[bool],                       # Whether to show outliers (default: True)
    show_notch=Optional[bool],                          # Whether to show notched boxes (default: False)
    orientation=Optional[ORIENTATION],                  # The orientation of the boxes
    scaley=Optional[str],                               # The y-axis scale ("linear", "log", ...)
    xmin=Optional[Union[int, float]],                   # The x-axis range
    xmax=Optional[Union[int, float]],
    ymin=Optional[Union[int, float]],                   # The y-axis range
    ymax=Optional[Union[int, float]],

    subplots=Optional[bool],                            # Whether to draw each chart in its own subplot (required for multiple charts)
    max_cols=Optional[int],                             # Maximum number of subplots per row
    sharex=Optional[bool],                              # Whether subplots share the x-axis
    sharey=Optional[bool],                              # Whether subplots share the y-axis

    xticks=Optional[List[Union[int, float]]],           # the x-axis ticks
    xticklabels=Optional[List[str]],                    # the x-axis tick labels (must be same length as xticks)
    xtickrotate=Optional[int],                          # the x-axis tick labels rotation
    yticks=Optional[List[Union[int, float]]],           # the y-axis ticks
    yticklabels=Optional[List[str]],                    # the y-axis tick labels (must be same length as yticks)
    ytickrotate=Optional[int],                          # the y-axis tick labels rotation

    vlines=Optional[Union[dict, List[dict]]],           # the vertical lines
    hlines=Optional[Union[dict, List[dict]]],           # the horizontal lines

    label=Optional[str],                                # The key in data holding the category label (default: "label")
    value=Optional[str],                                # The key in data holding the numeric value (default: "value")
)
```

For more details, see the [datachart.charts.BoxPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.BoxPlot) function.

## Basics

The examples in this guide share one dataset: the body mass of the 342 penguins of the [Palmer penguins](https://allisonhorst.github.io/palmerpenguins/) dataset (CC0), three species measured on the islands of the Palmer Archipelago in Antarctica. The data is hard-coded in a hidden cell, which keeps the sex and the flipper length of every penguin alongside its species — the later sections and examples reuse them. `chart_data` holds the body mass (in g) of every penguin, labeled with its species.

The data is a flat list of dictionaries, one per data point, each with a `label` and a `value`. The points that share a `label` are grouped into one box, so three species give three boxes:

```
chart_data[:3]
```

**Basic example.** Only the `data` argument is required to draw the box plot. Each box spans the middle half of its values (the first to the third quartile), the line inside it is the median, the whiskers reach the furthest values within 1.5 times the box height, and the values beyond the whiskers are drawn as outliers.

```
BoxPlot(
    # add the data to the chart
    data=chart_data
).show()
```

## Customizing the Box Plot

Every customization is either a keyword argument of `BoxPlot` or a `plot_box_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                       | Use                                                                               | See                                                             |
| ------------------------------------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| add a title and axis labels                      | `title`, `xlabel`, `ylabel`                                                       | [Title and axis labels](#title-and-axis-labels)                 |
| resize the figure                                | `figsize`                                                                         | [Figure size and grid](#figure-size-and-grid)                   |
| show the grid lines                              | `show_grid`                                                                       | [Figure size and grid](#figure-size-and-grid)                   |
| change the box fill, edge or transparency        | `style={"plot_box_color": ..., "plot_box_edgecolor": ..., "plot_box_alpha": ...}` | [Box style](#box-style)                                         |
| style the median, whiskers and caps              | `style={"plot_box_median_color": ..., "plot_box_whisker_color": ..., ...}`        | [Box style](#box-style)                                         |
| style the outlier markers                        | `style={"plot_box_outlier_marker": ..., "plot_box_outlier_size": ..., ...}`       | [Box style](#box-style)                                         |
| draw the boxes horizontally                      | `orientation`                                                                     | [Box orientation](#box-orientation)                             |
| hide the outliers                                | `show_outliers`                                                                   | [Showing and hiding outliers](#showing-and-hiding-outliers)     |
| show the confidence interval of the median       | `show_notch`                                                                      | [Notched box plots](#notched-box-plots)                         |
| highlight one box, mute the rest                 | `emphasis`                                                                        | [Emphasis](#emphasis)                                           |
| draw a threshold or reference line               | `hlines`, `vlines`                                                                | [Reference lines](#reference-lines)                             |
| draw the observations or a violin with the boxes | `Panel`                                                                           | [Boxes with swarms and violins](#boxes-with-swarms-and-violins) |
| compare several datasets side by side            | `data` as a list of lists, `subtitle`, `subplots`                                 | [Multiple Box Plots](#multiple-box-plots)                       |
| arrange the subplots                             | `max_cols`, `sharex`, `sharey`                                                    | [Shared axes across subplots](#shared-axes-across-subplots)     |
| draw every subplot horizontally                  | `orientation`                                                                     | [Subplot orientation](#subplot-orientation)                     |
| save the chart to a file                         | `save_figure`                                                                     | [Saving the Chart as an Image](#saving-the-chart-as-an-image)   |

The full list of style attributes is in the [datachart.typings.BoxStyleAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.BoxStyleAttrs) type; the full list of parameters is in the [datachart.charts.BoxPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.BoxPlot) reference.

### Title and axis labels

To add the chart title and axis labels, add the `title`, `xlabel` and `ylabel` attributes.

```
BoxPlot(
    data=chart_data,
    # add the title
    title="Body mass of Palmer penguins",
    # add the x and y axis labels
    xlabel="Species",
    ylabel="Body mass (g)",
).show()
```

### Figure size and grid

To change the figure size, add the `figsize` attribute. The `figsize` attribute can be a tuple (width, height), values are in inches. The `datachart` package provides a [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.FIG_SIZE) constant, which contains some of the predefined figure sizes.

To add the grid, add the `show_grid` attribute. The possible options are:

| Option   | Description                                     |
| -------- | ----------------------------------------------- |
| `"both"` | shows both the x-axis and the y-axis gridlines. |
| `"x"`    | shows only the x-axis grid lines.               |
| `"y"`    | shows only the y-axis grid lines.               |

Again, `datachart` provides a [datachart.constants.SHOW_GRID](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.SHOW_GRID) constant, which contains the supported options. The values of a vertical box plot are read off the y-axis, so the y-axis grid lines are the ones that help.

```
from datachart.constants import FIG_SIZE, SHOW_GRID
```

```
BoxPlot(
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

### Box style

To change the box style, add the `style` attribute with the corresponding attributes. The supported attributes are shown in the [datachart.typings.BoxStyleAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.BoxStyleAttrs) type, which contains the following attributes:

| Attribute                       | Description                                     |
| ------------------------------- | ----------------------------------------------- |
| `"plot_box_color"`              | The fill color of the box (hex color code).     |
| `"plot_box_alpha"`              | The alpha of the box (how visible the box is).  |
| `"plot_box_linewidth"`          | The line width of the box border.               |
| `"plot_box_edgecolor"`          | The edge color of the box (hex color code).     |
| `"plot_box_outlier_marker"`     | The outlier marker style.                       |
| `"plot_box_outlier_size"`       | The outlier marker size.                        |
| `"plot_box_outlier_color"`      | The outlier marker color (hex color code).      |
| `"plot_box_outlier_edge_color"` | The outlier marker edge color (hex color code). |
| `"plot_box_median_color"`       | The median line color (hex color code).         |
| `"plot_box_median_linewidth"`   | The median line width.                          |
| `"plot_box_whisker_color"`      | The whisker line color (hex color code).        |
| `"plot_box_whisker_linewidth"`  | The whisker line width.                         |
| `"plot_box_cap_color"`          | The cap line color (hex color code).            |
| `"plot_box_cap_linewidth"`      | The cap line width.                             |

Again, to help with the style settings, the [datachart.constants](https://eriknovak.github.io/datachart/0.9.0/references/constants/index.md) module contains the following constants:

| Constant                                                                                                                             | Description               |
| ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------- |
| [datachart.constants.LINE_MARKER](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.LINE_MARKER) | The outlier marker style. |

The `style` applies to every box of the chart. The median is the one line every reader looks for, so it earns a contrasting color and a heavier width; the outlier attributes style the two Chinstrap outliers. Any attribute you leave out keeps the value of the active theme.

```
from datachart.constants import LINE_MARKER
```

```
BoxPlot(
    data=chart_data,
    # define the style of the boxes
    style={
        "plot_box_color": "#6baed6",
        "plot_box_edgecolor": "#08519c",
        "plot_box_linewidth": 1.5,
        "plot_box_median_color": "#d62728",
        "plot_box_median_linewidth": 2,
        "plot_box_outlier_marker": LINE_MARKER.DIAMOND,
        "plot_box_outlier_size": 5,
        "plot_box_outlier_color": "#08519c",
    },
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Box orientation

To change the orientation of the boxes, add the `orientation` attribute, which supports the following values:

| Value          | Description                                                              |
| -------------- | ------------------------------------------------------------------------ |
| `"vertical"`   | The boxes are vertical, one per category along the x-axis (the default). |
| `"horizontal"` | The boxes are horizontal, one per category along the y-axis.             |

Again, `datachart` provides a [datachart.constants.ORIENTATION](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.ORIENTATION) constant, which contains the supported options. Horizontal boxes swap the roles of the axes: the categories move to the y-axis and the values to the x-axis, so the axis labels and the grid follow.

```
from datachart.constants import ORIENTATION
```

```
BoxPlot(
    data=chart_data,
    # change the orientation of the boxes
    orientation=ORIENTATION.HORIZONTAL,
    title="Body mass of Palmer penguins",
    # swap the axis labels to match the orientation
    xlabel="Body mass (g)",
    ylabel="Species",
    figsize=FIG_SIZE.FULL_SHORT,
    # the values are now read off the x-axis
    show_grid=SHOW_GRID.X,
).show()
```

### Showing and hiding outliers

By default, the values beyond the whiskers are drawn as outliers. To hide them, add the `show_outliers` attribute set to `False`. The Chinstrap penguins have two: one of 2,700 g and one of 4,800 g, far from the 3,700 g median. With the outliers hidden the whiskers stay where they are — they still end at the furthest values within 1.5 times the box height — so hiding outliers changes what is drawn, not what the boxes summarize.

```
for show_outliers in [True, False]:
    BoxPlot(
        data=chart_data,
        # show or hide the values beyond the whiskers
        show_outliers=show_outliers,
        title=f"Body mass of Palmer penguins (outliers {'shown' if show_outliers else 'hidden'})",
        xlabel="Species",
        ylabel="Body mass (g)",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
    ).show()
```

### Notched box plots

To draw notched boxes, add the `show_notch` attribute set to `True`. The notch marks a confidence interval around the median: if the notches of two boxes do not overlap, their medians differ with some confidence. The notch narrows with the number of values — the 68 Chinstrap penguins get a wider notch than the 151 Adelie — and the Adelie and Chinstrap notches overlap, so their medians cannot be told apart, while the Gentoo are heavier beyond doubt.

```
BoxPlot(
    data=chart_data,
    # draw the confidence interval of the median as a notch
    show_notch=True,
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Emphasis

To draw attention to one box, add the `emphasis` attribute. Box plots never overlay, so the `emphasis` list aligns with the box **labels** of one call, in the order the labels first appear in the data — here Adelie, Chinstrap, Gentoo. Each entry is one of the following roles:

| Role           | Description                                                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `"background"` | Mutes the box: it takes the muted color of the active theme, and its whiskers, caps, median and outliers mute together with it. |
| `"highlight"`  | Bolds the box edges and the median line.                                                                                        |
| `None`         | Leaves the box unchanged.                                                                                                       |

A single value instead of a list applies the role to every box. Again, `datachart` provides a [datachart.constants.EMPHASIS](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.EMPHASIS) constant, which contains the supported roles. The example puts the Gentoo box under scrutiny and pushes the other two species into the background. See the [Highlighting](https://eriknovak.github.io/datachart/0.9.0/how-to-guides/styling/highlighting/index.md) guide for the full model — how the muted color follows the theme and how emphasis works across the other charts.

```
from datachart.constants import EMPHASIS
```

```
BoxPlot(
    data=chart_data,
    # one role per box label: Adelie, Chinstrap, Gentoo
    emphasis=[EMPHASIS.BACKGROUND, EMPHASIS.BACKGROUND, EMPHASIS.HIGHLIGHT],
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Reference lines

A reference line puts a threshold or a summary value next to the boxes. To add horizontal lines, add the `hlines` attribute with the [datachart.typings.HLinePlotAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.HLinePlotAttrs) typing, which is either a `dict` or a `List[dict]` where each dictionary contains some of the following attributes:

```
{
  "y":    Union[int, float],                 # The y-axis value
  "xmin": Optional[Union[int, float]],       # The minimum x-axis value
  "xmax": Optional[Union[int, float]],       # The maximum x-axis value
  "style": {                                 # The style of the line (optional)
    "plot_hline_color": Optional[str],       # The color of the line (hex color code)
    "plot_hline_style": Optional[LineStyle], # The line style (solid, dashed, etc.)
    "plot_hline_width": Optional[float],     # The width of the line
    "plot_hline_alpha": Optional[float],     # The alpha of the line (how visible the line is)
  },
  "label": Optional[str],                    # The label of the line
}
```

Vertical lines work the same way through the `vlines` attribute and the [datachart.typings.VLinePlotAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.VLinePlotAttrs) typing, with `x`, `ymin`, `ymax` and `plot_vline_*` style attributes in place of their horizontal counterparts. The line style takes a [datachart.constants.LINE_STYLE](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.LINE_STYLE) value. The example marks the mean body mass of all 342 penguins, which shows at a glance that the whole Gentoo box sits above it.

```
from datachart.constants import LINE_STYLE
```

```
mean_mass = sum(penguin["value"] for penguin in chart_data) / len(chart_data)

BoxPlot(
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

### Boxes with swarms and violins

A box summarizes its group; a [datachart.charts.SwarmPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.SwarmPlot) shows every observation and a [datachart.charts.ViolinPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.ViolinPlot) the shape of the distribution. Over the same labels the three draw at the same positions, so they compose with [datachart.utils.Panel](https://eriknovak.github.io/datachart/0.9.0/references/utils/#datachart.utils.Panel). The points draw above the boxes; hide the outliers, which the swarm already shows.

```
from datachart.charts import SwarmPlot, ViolinPlot
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

A violin body behind the boxes adds the distribution shape: draw it with `inner=None`, since the box supplies the summaries, and give the box a white fill so it reads over the body. One box plot and one violin plot per panel; swarms may repeat.

```
Panel(
    [
        # the body only; the box plot supplies the summaries
        ViolinPlot(data=chart_data, inner=None, style={"plot_violin_alpha": 0.3}),
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

## Multiple Box Plots

To create multiple box plots, pass a list of lists to the `data` argument. Each inner list holds the data points of one chart, which is drawn in its own subplot with the `subtitle` at the top and the `title`, `xlabel` and `ylabel` positioned to be global for all charts. Per-chart attributes like `subtitle` and `style` can be passed as lists, where each element corresponds to a chart; a single value applies to every chart.

Subplots required for multiple datasets

When using multiple datasets (list of lists), you **must** set `subplots=True`. Box plots do not support overlaying multiple datasets on a single axis.

The example draws the body mass and the flipper length of the three species side by side. The two charts hold different quantities, so each gets its own subtitle with its unit and there is no global `ylabel`.

```
BoxPlot(
    # use a list of lists to define multiple box plots
    data=[chart_data, flipper_data],
    # add a subtitle to each chart
    subtitle=["Body mass (g)", "Flipper length (mm)"],
    title="Palmer penguins",
    xlabel="Species",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # draw each chart in its own subplot
    subplots=True,
).show()
```

### Shared axes across subplots

To share the x-axis and/or y-axis across subplots, add the `sharex` and/or `sharey` attributes, which are boolean values that specify whether to share the axis across all subplots; a shared axis is labeled once, on the outer subplots only. The `max_cols` attribute limits the number of subplots per row — with `max_cols=1` the charts stack vertically. Which axis to share follows from the orientation: the two vertical charts have the species on the x-axis, so stacked with `sharex` the species are labeled once, under the bottom chart, while the values are different quantities and keep their own y-axis.

```
BoxPlot(
    data=[chart_data, flipper_data],
    subtitle=["Body mass (g)", "Flipper length (mm)"],
    title="Palmer penguins",
    xlabel="Species",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
    subplots=True,
    # stack the charts in one column
    max_cols=1,
    # share the x-axis across subplots
    sharex=True,
).show()
```

### Subplot orientation

The `orientation` attribute changes the orientation of every subplot at once. Horizontal boxes move the species to the y-axis, so side by side it is now `sharey` that labels them once, next to the left chart.

```
figure = BoxPlot(
    data=[chart_data, flipper_data],
    subtitle=["Body mass (g)", "Flipper length (mm)"],
    # change the orientation of the boxes in every subplot
    orientation=ORIENTATION.HORIZONTAL,
    title="Palmer penguins",
    ylabel="Species",
    figsize=FIG_SIZE.FULL_SHORT,
    # the values are now read off the x-axis
    show_grid=SHOW_GRID.X,
    subplots=True,
    # the species are now on the y-axis
    sharey=True,
)
figure.show()
```

## Saving the Chart as an Image

To save the chart as an image, use the [datachart.utils.save_figure](https://eriknovak.github.io/datachart/0.9.0/references/utils#datachart.utils.save_figure) function.

```
from datachart.utils import save_figure
```

```
save_figure(figure, "./fig_box_plot.png", dpi=300)
```

The figure should be saved in the current working directory.

## Real-World Examples

The following examples put the features above to work on real or realistic data. Each one states what its data is and where it comes from; the data itself lives in a hidden cell.

### Example 1: Model Benchmark Across Seeds (Emphasis)

`benchmark` holds the illustrative test accuracy of five models, each trained and evaluated with 20 random seeds, drawn from a seeded generator. Reporting one number per model hides how much of the difference between them is seed noise; one box per model shows the spread and the median together. The question is which model to ship, so `emphasis` highlights the model with the best median accuracy and pushes the other four into the background — the highlighted box keeps its color and gets bold edges, the muted ones become context. A short figure and the y-axis grid make the small differences in accuracy readable.

```
BEST_MODEL = "Deep + aug."

BoxPlot(
    data=benchmark,
    # highlight the best model, mute the rest
    emphasis=[
        EMPHASIS.HIGHLIGHT if model == BEST_MODEL else EMPHASIS.BACKGROUND
        for model in MODELS
    ],
    title=f"Test accuracy across {N_SEEDS} seeds",
    xlabel="Model",
    ylabel="Accuracy",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Example 2: Daily Temperatures by Month (Horizontal Boxes and Many Categories)

`daily_temperatures` holds one year of daily mean temperatures (in °C) in Ljubljana, drawn from a seeded generator around the published 1991–2020 monthly climate normals of the city's weather station, with the larger day-to-day swings of winter. Twelve boxes are the case for horizontal boxes: the months stack from January at the bottom to December at the top, every label stays legible, and the temperature axis gets the full figure width, which a taller figure makes room for. The outliers are kept — an unusually cold or warm day is exactly what a reader of this chart looks for — and a dashed `vlines` reference marks the freezing point, so the months with days below zero are the boxes that cross it.

```
BoxPlot(
    data=daily_temperatures,
    # twelve labeled boxes read best top to bottom
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
    title="Daily mean temperature in Ljubljana",
    xlabel="Temperature (°C)",
    ylabel="Month",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.X,
).show()
```

### Example 3: Service Response Times (Skewed Data, Outliers and an SLA Line)

`response_times` holds the illustrative response time (in ms) of 200 requests to each of four services, drawn from a seeded log-normal generator: most requests are fast and a long tail of slow ones stretches each distribution upwards, as in most latency data. A dashed `hlines` reference marks the 500 ms service level agreement. Drawn twice, once with and once without outliers, the two charts show why the default keeps them on skewed data: the slow requests are the outliers, so hiding them hides exactly the requests that breach the agreement — without them Search looks safely below the line, with them its slowest requests cross it and the Reports tail stretches to well over a second.

```
for show_outliers in [True, False]:
    BoxPlot(
        data=response_times,
        # the slow requests are the outliers; hiding them hides the SLA breaches
        show_outliers=show_outliers,
        # mark the service level agreement
        hlines={
            "y": SLA_MS,
            "style": {
                "plot_hline_color": "#d62728",
                "plot_hline_style": LINE_STYLE.DASHED,
                "plot_hline_width": 1.5,
            },
        },
        title=f"Response time of {N_REQUESTS} requests per service (outliers {'shown' if show_outliers else 'hidden'})",
        xlabel="Service",
        ylabel="Response time (ms)",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
    ).show()
```

### Example 4: Penguin Body Mass by Sex (Multiple Box Plots and a Shared Value Axis)

`body_mass_by_sex` splits the body mass of the Palmer penguins from the hidden cell of the [Basics](#basics) section into the 165 female and the 168 male penguins (the 9 penguins without a recorded sex are left out). Each sex gets its own chart, named with a list of `subtitle`, and `sharey` puts both on the same mass axis, so the boxes are comparable across the two subplots: the males of every species are heavier than the females, and the gap is largest for the Gentoo. The `xlabel` and `ylabel` label the species and the unit once for both.

```
BoxPlot(
    data=body_mass_by_sex,
    # one subtitle per chart
    subtitle=SEXES,
    title="Body mass of Palmer penguins by sex",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    subplots=True,
    # the same mass axis for both charts, so the boxes are comparable
    sharey=True,
).show()
```
