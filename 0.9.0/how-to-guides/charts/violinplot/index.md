# Violin Plot

This section showcases the violin plot. It contains examples of how to create violin plots using the [datachart.charts.ViolinPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.ViolinPlot) function.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-violin-chart), which maps common tasks to the parameter or style attribute that does the job.

As mentioned above, the violin plots are created using the `ViolinPlot` function found in the [datachart.charts](https://eriknovak.github.io/datachart/0.9.0/references/charts/index.md) module. Let's import it:

```
from datachart.charts import ViolinPlot
```

## Violin Plot Input Attributes

The `ViolinPlot` function accepts keyword arguments for chart configuration. The main argument is `data`, which contains the data points. For a single violin plot, `data` is a list of dictionaries; the points that share a `label` form one violin. For multiple violin plots, `data` is a list of lists.

```
ViolinPlot(
    data=[{                                             # A list of violin data points (or list of lists for multiple charts)
        "label": str,                                   # The category label
        "value": Union[int, float],                     # The numeric value
    }],
    style={                                             # The style of the violin (optional)
        "plot_violin_color":           Union[str, None],        # The fill color of the body
        "plot_violin_alpha":           Union[float, None],      # The alpha of the body
        "plot_violin_linewidth":       Union[int, float, None], # The line width of the body edge
        "plot_violin_edgecolor":       Union[str, None],        # The edge color of the body (default: the fill)
        "plot_violin_width":           Union[int, float, None], # The maximum width of the body
        "plot_violin_inner_color":     Union[str, None],        # The color of the inner marks (default: the font color)
        "plot_violin_inner_linewidth": Union[int, float, None], # The line width of the inner marks
        "plot_violin_median_color":    Union[str, None],        # The color of the median dot
        "plot_violin_median_size":     Union[int, float, None], # The size of the median dot
    },
    subtitle=Optional[str],                             # The subtitle of the chart (or list for multiple charts)
    title=Optional[str],                                # The title of the chart
    xlabel=Optional[str],                               # The x-axis label
    ylabel=Optional[str],                               # The y-axis label
    emphasis=Optional[Union[str, List[Optional[str]]]], # The emphasis role per violin label ("background", "highlight", None)

    inner=Optional[str],                                # The inner marks ("box", "quartiles", "median", None; default: "box")
    bandwidth=Optional[Union[str, float]],              # The KDE bandwidth ("scott", "silverman", or a number; default: "scott")
    split=Optional[str],                                # The key in data whose two values split each violin in half

    figsize=Optional[Tuple[float, float]],              # The figure size in inches
    show_grid=Optional[str],                            # Which grid lines to show ("both", "x", "y")
    show_legend=Optional[bool],                         # Whether to show the legend (the split values)
    orientation=Optional[ORIENTATION],                  # The orientation of the violins
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

For more details, see the [datachart.charts.ViolinPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.ViolinPlot) function.

## Basics

The examples in this guide share one dataset: the body mass of the 342 penguins of the [Palmer penguins](https://allisonhorst.github.io/palmerpenguins/) dataset (CC0), three species measured on the islands of the Palmer Archipelago in Antarctica — the same data the [Box Plot](https://eriknovak.github.io/datachart/0.9.0/how-to-guides/charts/boxplot/index.md) guide uses. The data is hard-coded in a hidden cell, which keeps the flipper length of every penguin alongside its species. `chart_data` holds the body mass (in g) of every penguin, labeled with its species and carrying its sex.

The data is a flat list of dictionaries, one per data point, each with a `label` and a `value`; extra keys like `sex` are ignored until a section asks for them. The points that share a `label` are grouped into one violin, so three species give three violins:

```
chart_data[:3]
```

**Basic example.** Only the `data` argument is required to draw the violin plot. Each body is a kernel density estimate of its values, mirrored around the category position and scaled to the same maximum width; inside it, a thin bar spans the middle half of the values (the first to the third quartile), the line through it reaches the furthest values within 1.5 times the bar height, and the dot is the median. Where a box plot draws these summaries alone, the violin shows the shape of the distribution around them: the Gentoo are the heaviest species, and the Adelie have a wider spread than their box would suggest.

```
ViolinPlot(
    # add the data to the chart
    data=chart_data
).show()
```

## Customizing the Violin Plot

Every customization is either a keyword argument of `ViolinPlot` or a `plot_violin_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                             | Use                                                                                        | See                                                             |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| add a title and axis labels                            | `title`, `xlabel`, `ylabel`                                                                | [Title and axis labels](#title-and-axis-labels)                 |
| resize the figure                                      | `figsize`                                                                                  | [Figure size and grid](#figure-size-and-grid)                   |
| show the grid lines                                    | `show_grid`                                                                                | [Figure size and grid](#figure-size-and-grid)                   |
| change the body fill, edge or transparency             | `style={"plot_violin_color": ..., "plot_violin_edgecolor": ..., "plot_violin_alpha": ...}` | [Violin style](#violin-style)                                   |
| style the inner marks and the median dot               | `style={"plot_violin_inner_color": ..., "plot_violin_median_color": ..., ...}`             | [Violin style](#violin-style)                                   |
| change what is drawn inside the body                   | `inner`                                                                                    | [Inner marks](#inner-marks)                                     |
| smooth or sharpen the body                             | `bandwidth`                                                                                | [Bandwidth](#bandwidth)                                         |
| compare two groups within each category                | `split`, `show_legend`                                                                     | [Split violins](#split-violins)                                 |
| draw the violins horizontally                          | `orientation`                                                                              | [Violin orientation](#violin-orientation)                       |
| highlight one violin, mute the rest                    | `emphasis`                                                                                 | [Emphasis](#emphasis)                                           |
| draw a threshold or reference line                     | `hlines`, `vlines`                                                                         | [Reference lines](#reference-lines)                             |
| draw a box plot or the observations inside the violins | `Panel`                                                                                    | [Violins with boxes and swarms](#violins-with-boxes-and-swarms) |
| compare several datasets side by side                  | `data` as a list of lists, `subtitle`, `subplots`                                          | [Multiple Violin Plots](#multiple-violin-charts)                |
| arrange the subplots                                   | `max_cols`, `sharex`, `sharey`                                                             | [Shared axes across subplots](#shared-axes-across-subplots)     |
| save the chart to a file                               | `save_figure`                                                                              | [Saving the Chart as an Image](#saving-the-chart-as-an-image)   |

The full list of style attributes is in the [datachart.typings.ViolinStyleAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.ViolinStyleAttrs) type; the full list of parameters is in the [datachart.charts.ViolinPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.ViolinPlot) reference.

### Title and axis labels

To add the chart title and axis labels, add the `title`, `xlabel` and `ylabel` attributes.

```
ViolinPlot(
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

Again, `datachart` provides a [datachart.constants.SHOW_GRID](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.SHOW_GRID) constant, which contains the supported options. The values of a vertical violin are read off the y-axis, so the y-axis grid lines are the ones that help.

```
from datachart.constants import FIG_SIZE, SHOW_GRID
```

```
ViolinPlot(
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

### Violin style

To change the violin style, add the `style` attribute with the corresponding attributes. The supported attributes are shown in the [datachart.typings.ViolinStyleAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.ViolinStyleAttrs) type: the `plot_violin_color`, `plot_violin_edgecolor`, `plot_violin_alpha`, `plot_violin_linewidth` and `plot_violin_width` attributes style the body, the `plot_violin_inner_*` attributes the marks inside it, and the `plot_violin_median_*` attributes the median dot.

The `style` applies to every violin of the chart. The body fill defaults to the theme's color cycle and the edge to the fill; the inner marks default to the theme's font color, so they read on any fill, and the median dot is white to stand out on the dark quartile bar. Any attribute you leave out keeps the value of the active theme.

```
ViolinPlot(
    data=chart_data,
    # define the style of the violins
    style={
        "plot_violin_color": "#6baed6",
        "plot_violin_edgecolor": "#08519c",
        "plot_violin_linewidth": 1.5,
        "plot_violin_alpha": 0.6,
        "plot_violin_width": 0.6,
        "plot_violin_inner_color": "#08519c",
        "plot_violin_inner_linewidth": 1.5,
        "plot_violin_median_color": "#d62728",
        "plot_violin_median_size": 6,
    },
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Inner marks

To change what is drawn inside each body, add the `inner` attribute, which supports the following values:

| Value         | Description                                                                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"box"`       | A thin bar from the first to the third quartile, a line reaching the furthest values within 1.5 times the bar height, and a median dot (the default). |
| `"quartiles"` | A dashed median line and dotted first and third quartile lines, each as wide as the body at that value.                                               |
| `"median"`    | A single solid median line, as wide as the body at that value.                                                                                        |
| `None`        | The body only.                                                                                                                                        |

Again, `datachart` provides a [datachart.constants.VIOLIN_INNER](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.VIOLIN_INNER) constant, which contains the supported options. The `"box"` marks summarize the values the way a box plot does; the `"quartiles"` lines show the same quartiles without hiding the shape behind them, and are the better choice when the bodies are narrow or the figure is small.

```
from datachart.constants import VIOLIN_INNER
```

```
for inner in [VIOLIN_INNER.BOX, VIOLIN_INNER.QUARTILES, VIOLIN_INNER.MEDIAN, None]:
    ViolinPlot(
        data=chart_data,
        # change the marks drawn inside the bodies
        inner=inner,
        title=f"Body mass of Palmer penguins (inner={inner!r})",
        xlabel="Species",
        ylabel="Body mass (g)",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
    ).show()
```

### Bandwidth

The body is a Gaussian kernel density estimate, and the `bandwidth` attribute sets how wide its kernel is. It takes one of the following values:

| Value         | Description                                                                                       |
| ------------- | ------------------------------------------------------------------------------------------------- |
| `"scott"`     | Scott's rule of thumb, scaled to the number of values (the default).                              |
| `"silverman"` | Silverman's rule of thumb, about 6% wider than Scott's — the two look nearly the same.            |
| a number      | A factor applied to the standard deviation of the values; smaller is sharper, larger is smoother. |

Again, `datachart` provides a [datachart.constants.BANDWIDTH](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.BANDWIDTH) constant, which contains the supported rules. A small factor follows every bump of the data and a large one smooths the body into a single hump; the two rules of thumb sit in between and shrink the kernel as the number of values grows. The shape can change more than the summary marks, which are computed from the values and never from the estimate.

```
from datachart.constants import BANDWIDTH

for bandwidth in [0.15, BANDWIDTH.SCOTT, 0.6]:
    ViolinPlot(
        data=chart_data,
        # sharpen or smooth the bodies
        bandwidth=bandwidth,
        title=f"Body mass of Palmer penguins (bandwidth={bandwidth!r})",
        xlabel="Species",
        ylabel="Body mass (g)",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
    ).show()
```

### Split violins

To compare two groups within each category, add the `split` attribute with the name of the key in `data` that holds the group of each point. The key must take **exactly two** distinct values across the data; each violin is then cut in half, the left half drawn from the points with the first value and the right half from the points with the second, in the order the values first appear. The halves take the first two colors of the theme's multiple-series palette, each keeps its own inner marks, and `show_legend` lists the two values.

The penguins carry their sex, so `split="sex"` puts the female penguins of each species on the left and the males on the right. A handful of penguins have no recorded sex, which would be a third value, so they are filtered out first.

```
sexed_data = [penguin for penguin in chart_data if penguin["sex"] is not None]

ViolinPlot(
    data=sexed_data,
    # split every violin by the sex of the penguins
    split="sex",
    # list the two split values in the legend
    show_legend=True,
    title="Body mass of Palmer penguins by sex",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

The `inner` attribute applies to both halves; with `"quartiles"` each half gets its own quartile lines, which makes the difference between the medians easy to read across the centre line.

```
ViolinPlot(
    data=sexed_data,
    split="sex",
    # quartile lines in each half
    inner=VIOLIN_INNER.QUARTILES,
    show_legend=True,
    title="Body mass of Palmer penguins by sex",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Violin orientation

To change the orientation of the violins, add the `orientation` attribute, which supports the following values:

| Value          | Description                                                                |
| -------------- | -------------------------------------------------------------------------- |
| `"vertical"`   | The violins are vertical, one per category along the x-axis (the default). |
| `"horizontal"` | The violins are horizontal, one per category along the y-axis.             |

Again, `datachart` provides a [datachart.constants.ORIENTATION](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.ORIENTATION) constant, which contains the supported options. Horizontal violins swap the roles of the axes: the categories move to the y-axis and the values to the x-axis, so the axis labels and the grid follow.

```
from datachart.constants import ORIENTATION
```

```
ViolinPlot(
    data=chart_data,
    # change the orientation of the violins
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

### Emphasis

To draw attention to one violin, add the `emphasis` attribute. As with box plots, the `emphasis` list aligns with the violin **labels** of one call, in the order the labels first appear in the data — here Adelie, Chinstrap, Gentoo. Each entry is one of the following roles:

| Role           | Description                                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------------------- |
| `"background"` | Mutes the violin: the body takes the muted color of the active theme, and its inner marks mute together with it. |
| `"highlight"`  | Bolds the body edge.                                                                                             |
| `None`         | Leaves the violin unchanged.                                                                                     |

A single value instead of a list applies the role to every violin. Again, `datachart` provides a [datachart.constants.EMPHASIS](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.EMPHASIS) constant, which contains the supported roles. The example puts the Gentoo violin under scrutiny and pushes the other two species into the background. See the [Highlighting](https://eriknovak.github.io/datachart/0.9.0/how-to-guides/styling/highlighting/index.md) guide for the full picture.

```
from datachart.constants import EMPHASIS
```

```
ViolinPlot(
    data=chart_data,
    # one role per violin label: Adelie, Chinstrap, Gentoo
    emphasis=[EMPHASIS.BACKGROUND, EMPHASIS.BACKGROUND, EMPHASIS.HIGHLIGHT],
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Reference lines

A reference line puts a threshold or a summary value next to the violins. To add horizontal lines, add the `hlines` attribute with the [datachart.typings.HLinePlotAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.HLinePlotAttrs) typing, which is either a `dict` or a `List[dict]`; vertical lines work the same way through the `vlines` attribute and the [datachart.typings.VLinePlotAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.VLinePlotAttrs) typing. The [Box Plot](https://eriknovak.github.io/datachart/0.9.0/how-to-guides/charts/boxplot/#reference-lines) guide lists every attribute of a line. The example marks the mean body mass of all penguins.

```
from datachart.constants import LINE_STYLE
```

```
mean_mass = sum(penguin["value"] for penguin in chart_data) / len(chart_data)

ViolinPlot(
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

### Violins with boxes and swarms

A violin and a box plot over the same labels draw at the same positions, so the two compose with [datachart.utils.Panel](https://eriknovak.github.io/datachart/0.9.0/references/utils#datachart.utils.Panel): the violin with `inner=None` supplies the shape, and the [datachart.charts.BoxPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.BoxPlot) drawn over it supplies the full box with its whiskers, caps and outliers. Both charts must group the same labels in the same order; one violin plot and one box plot per panel.

```
from datachart.charts import BoxPlot, SwarmPlot
from datachart.utils import Panel
```

```
Panel(
    [
        # the body only; the box plot supplies the summaries
        ViolinPlot(data=chart_data, inner=None),
        BoxPlot(
            data=chart_data,
            style={"plot_box_color": "#FFFFFF", "plot_box_alpha": 0.9},
        ),
    ],
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel_left="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

A [datachart.charts.SwarmPlot](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.SwarmPlot) puts every observation inside the body instead: the points draw above the violin, so lower the body's alpha to keep them legible. The two also compose with the box in one panel — the violin outlines the distribution, the box summarizes it, and the swarm shows the data.

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

```
Panel(
    [
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

## Multiple Violin Plots

To create multiple violin plots, pass a list of lists to the `data` argument. Each inner list holds the data points of one chart, which is drawn in its own subplot with the `subtitle` at the top and the `title`, `xlabel` and `ylabel` positioned to be global for all charts. Per-chart attributes like `subtitle` and `style` can be passed as lists, where each element corresponds to a chart; a single value applies to every chart.

Subplots required for multiple datasets

When using multiple datasets (list of lists), you **must** set `subplots=True`. Violin plots do not support overlaying multiple datasets on a single axis; to compare two groups within each category, use `split` instead.

The example draws the body mass and the flipper length of the three species side by side. The two charts hold different quantities, so each gets its own subtitle with its unit and there is no global `ylabel`.

```
ViolinPlot(
    # use a list of lists to define multiple violin plots
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

To share the x-axis and/or y-axis across subplots, add the `sharex` and/or `sharey` attributes, which are boolean values that specify whether to share the axis across all subplots; a shared axis is labeled once, on the outer subplots only. The `max_cols` attribute limits the number of subplots per row — with `max_cols=1` the charts stack vertically. The `orientation` attribute changes the orientation of every subplot at once: horizontal violins move the species to the y-axis, so side by side it is `sharey` that labels them once, next to the left chart.

```
figure = ViolinPlot(
    data=[chart_data, flipper_data],
    subtitle=["Body mass (g)", "Flipper length (mm)"],
    # change the orientation of the violins in every subplot
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
save_figure(figure, "./fig_violin_plot.png", dpi=300)
```

The figure should be saved in the current working directory.

## Real-World Examples

The following examples put the features above to work on real or realistic data. Each one states what its data is and where it comes from; the data itself lives in a hidden cell.

### Example 1: Service Response Times (Bimodal Data and a Box Comparison)

`response_times` holds the illustrative response time (in ms) of 300 requests to each of three services, drawn from a seeded generator. Two of the services answer some requests from a cache and the rest from the database, so their response times have two modes — fast cache hits and slow misses — with nothing in between. A box plot reduces each service to one median and one spread, which puts the median of the cached services in a gap where no request actually lands; the violin shows the two humps, and its `"quartiles"` lines make the same point without hiding them. The `Panel` on the right draws the two charts over each other for the comparison.

```
from datachart.utils import Grid

violins = ViolinPlot(
    data=response_times,
    # quartile lines keep the two humps visible
    inner=VIOLIN_INNER.QUARTILES,
    title="Violin plot",
    xlabel="Service",
    ylabel="Response time (ms)",
    show_grid=SHOW_GRID.Y,
)
boxes = Panel(
    [
        ViolinPlot(data=response_times, inner=None, style={"plot_violin_alpha": 0.3}),
        BoxPlot(data=response_times, show_outliers=False),
    ],
    title="Box plot over the body",
    xlabel="Service",
    show_grid=SHOW_GRID.Y,
)

Grid(
    [[violins, boxes]],
    title=f"Response time of {N_REQUESTS} requests per service",
    figsize=FIG_SIZE.FULL_SHORT,
    sharey=True,
).show()
```

### Example 2: Model Benchmark Across Seeds (Split by Evaluation Split)

`benchmark` holds the illustrative accuracy of four models, each trained with 20 random seeds and evaluated on both the validation and the test split, drawn from a seeded generator. One violin per model split by the evaluation split shows two things at once: how much of the difference between models is seed noise, and whether a model that looks best on validation holds up on test. The `emphasis` mutes the models that are out of the running so the comparison of the two contenders stands out.

```
CONTENDERS = {"Deep", "Deep + aug."}

ViolinPlot(
    data=benchmark,
    # the left half is the validation split, the right half the test split
    split="split",
    inner=VIOLIN_INNER.QUARTILES,
    show_legend=True,
    # mute the models that are out of the running
    emphasis=[None if model in CONTENDERS else EMPHASIS.BACKGROUND for model in MODELS],
    title=f"Accuracy across {N_SEEDS} seeds",
    xlabel="Model",
    ylabel="Accuracy",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```
