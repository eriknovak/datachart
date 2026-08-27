# Scatter Chart

This section showcases the scatter chart. It contains examples of how to create scatter charts using the [datachart.charts.ScatterChart](https://eriknovak.github.io/datachart/0.8.0/references/charts/#datachart.charts.ScatterChart) function.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-scatter-chart), which maps common tasks to the parameter or style attribute that does the job.

As mentioned above, the scatter charts are created using the `ScatterChart` function found in the [datachart.charts](https://eriknovak.github.io/datachart/0.8.0/references/charts/index.md) module. Let's import it:

```
from datachart.charts import ScatterChart
```

## Scatter Chart Input Attributes

The `ScatterChart` function accepts keyword arguments for chart configuration. The main argument is `data`, which contains the data points. For a single scatter chart, `data` is a list of dictionaries. For multiple scatter charts, `data` is a list of lists.

```
ScatterChart(
    data=[{                                             # A list of scatter data points (or list of lists for multiple charts)
        "x":    Union[int, float],                      # The x-axis value
        "y":    Union[int, float],                      # The y-axis value
        "size": Optional[Union[int, float]],            # The marker size value (for bubble charts)
        "hue":  Optional[str],                          # The category for color grouping
    }],
    style={                                             # The style of the scatter markers (optional)
        "plot_scatter_color":      Optional[str],       # The color of the markers (hex color code)
        "plot_scatter_alpha":      Optional[float],     # The alpha of the markers (how visible they are)
        "plot_scatter_size":       Optional[float],     # The size of the markers
        "plot_scatter_marker":     Optional[LINE_MARKER], # The marker shape (circle, square, etc.)
        "plot_scatter_zorder":     Optional[int],       # The zorder of the markers
        "plot_scatter_edge_width": Optional[float],     # The edge width of the markers
        "plot_scatter_edge_color": Optional[str],       # The edge color of the markers (hex color code)
    },
    subtitle=Optional[str],                             # The subtitle of the chart (or list for multiple charts)
    emphasis=Optional[str],                             # "highlight" or "background" (or list for multiple charts)
    title=Optional[str],                                # The title of the chart
    xlabel=Optional[str],                               # The x-axis label
    ylabel=Optional[str],                               # The y-axis label

    figsize=Optional[Tuple[float, float]],              # The figure size in inches
    show_grid=Optional[str],                            # Which grid lines to show ("both", "x", "y")
    aspect_ratio=Optional[str],                         # The aspect ratio of the axes ("auto", "equal")
    show_legend=Optional[bool],                         # Whether to show the legend
    show_regression=Optional[bool],                     # Whether to show the regression line
    show_ci=Optional[bool],                             # Whether to show the confidence interval around the regression line
    ci_level=Optional[float],                           # The confidence interval level (default: 0.95)
    show_correlation=Optional[bool],                    # Whether to annotate the Pearson correlation coefficient

    subplots=Optional[bool],                            # Whether to draw each chart in its own subplot
    max_cols=Optional[int],                             # Maximum number of subplots per row
    sharex=Optional[bool],                              # Whether subplots share the x-axis
    sharey=Optional[bool],                              # Whether subplots share the y-axis
    scalex=Optional[str],                               # The x-axis scale ("linear", "log", "symlog", "asinh")
    scaley=Optional[str],                               # The y-axis scale ("linear", "log", "symlog", "asinh")
    xmin=Optional[Union[int, float]],                   # The x-axis range
    xmax=Optional[Union[int, float]],
    ymin=Optional[Union[int, float]],                   # The y-axis range
    ymax=Optional[Union[int, float]],

    xticks=Optional[List[Union[int, float]]],           # the x-axis ticks
    xticklabels=Optional[List[str]],                    # the x-axis tick labels (must be same length as xticks)
    xtickrotate=Optional[int],                          # the x-axis tick labels rotation
    yticks=Optional[List[Union[int, float]]],           # the y-axis ticks
    yticklabels=Optional[List[str]],                    # the y-axis tick labels (must be same length as yticks)
    ytickrotate=Optional[int],                          # the y-axis tick labels rotation

    vlines=Optional[Union[dict, List[dict]]],           # the vertical lines
    hlines=Optional[Union[dict, List[dict]]],           # the horizontal lines

    x=Optional[str],                                    # the key holding the x-axis value (default: "x")
    y=Optional[str],                                    # the key holding the y-axis value (default: "y")
    size=Optional[str],                                 # the key holding the marker size value (bubble charts)
    hue=Optional[str],                                  # the key holding the category for color grouping
    size_range=Optional[Tuple[float, float]],           # the (min_size, max_size) range for bubble charts (default: (20, 200))
)
```

For more details, see the [datachart.charts.ScatterChart](https://eriknovak.github.io/datachart/0.8.0/references/charts/#datachart.charts.ScatterChart) function.

## Basics

The examples in this guide share one dataset: the GDP per capita (in US dollars) and life expectancy (in years) of 36 countries, with their continent and population. The data is hard-coded in a hidden cell; `countries` holds one point per country, and `countries_by_continent` holds one list per continent — Africa, the Americas, Asia and Europe — in the order of `CONTINENTS`. The figures are rounded recent public statistics.

Each data point is a dictionary with an `x` value (here the GDP per capita) and a `y` value (the life expectancy). The other keys are ignored until a later example asks for them:

```
countries[:3]
```

**Basic example.** Only the `data` argument is required to draw the scatter chart.

```
ScatterChart(
    # add the data to the chart
    data=countries
).show()
```

## Customizing the Scatter Chart

Every customization is either a keyword argument of `ScatterChart` or a `plot_scatter_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                             | Use                                                                      | See                                                           |
| -------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------- |
| add a title and axis labels            | `title`, `xlabel`, `ylabel`                                              | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| set custom tick positions and labels   | `xticks`, `xticklabels`, `yticks`, `yticklabels`                         | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| rotate the tick labels                 | `xtickrotate`, `ytickrotate`                                             | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| fix the axis range                     | `xmin`, `xmax`, `ymin`, `ymax`                                           | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| resize the figure                      | `figsize`                                                                | [Figure size and grid](#figure-size-and-grid)                 |
| show grid lines                        | `show_grid`                                                              | [Figure size and grid](#figure-size-and-grid)                 |
| change the marker color or shape       | `style={"plot_scatter_color": ..., "plot_scatter_marker": ...}`          | [Scatter style](#scatter-style)                               |
| change the marker size or transparency | `style={"plot_scatter_size": ..., "plot_scatter_alpha": ...}`            | [Scatter style](#scatter-style)                               |
| outline the markers                    | `style={"plot_scatter_edge_width": ..., "plot_scatter_edge_color": ...}` | [Scatter style](#scatter-style)                               |
| color the points by a category         | `hue`, `show_legend`                                                     | [Hue grouping](#hue-grouping)                                 |
| scale the markers by a value           | `size`, `size_range`                                                     | [Bubble chart](#bubble-chart)                                 |
| fit a regression line                  | `show_regression`, `show_ci`, `ci_level`, `show_correlation`             | [Regression line](#regression-line)                           |
| fix the aspect ratio of the axes       | `aspect_ratio`                                                           | [Aspect ratio](#aspect-ratio)                                 |
| highlight one series, mute the rest    | `emphasis`                                                               | [Emphasis](#emphasis)                                         |
| mark a threshold or a reference value  | `hlines`, `vlines`                                                       | [Reference lines](#reference-lines)                           |
| compare several series in one chart    | `data` as a list of lists, `subtitle`, `show_legend`                     | [Multiple Scatter Charts](#multiple-scatter-charts)           |
| draw each series in its own subplot    | `subplots`, `sharex`, `sharey`, `max_cols`                               | [Subplots](#subplots)                                         |
| use a logarithmic axis                 | `scalex`, `scaley`                                                       | [Axis scales](#axis-scales)                                   |
| plot data with other key names         | `x`, `y`, `size`, `hue`                                                  | [Custom data keys](#custom-data-keys)                         |
| save the chart to a file               | `save_figure`                                                            | [Saving the Chart as an Image](#saving-the-chart-as-an-image) |

The full list of style attributes is in the [datachart.typings.ScatterStyleAttrs](https://eriknovak.github.io/datachart/0.8.0/references/typings/#datachart.typings.ScatterStyleAttrs) type; the full list of parameters is in the [datachart.charts.ScatterChart](https://eriknovak.github.io/datachart/0.8.0/references/charts/#datachart.charts.ScatterChart) reference.

### Title, axis labels and ticks

To add the chart title and axis labels, add the `title`, `xlabel` and `ylabel` attributes. The tick positions and their labels can be set with `xticks` and `xticklabels` (or `yticks` and `yticklabels`) — here the GDP per capita ticks are labeled in thousands of dollars. Tick labels can be rotated with `xtickrotate` (or `ytickrotate`), and the axis range can be fixed with `xmin`, `xmax`, `ymin` and `ymax`.

```
GDP_TICKS = [0, 25_000, 50_000, 75_000, 100_000]
GDP_TICK_LABELS = ["$0", "$25k", "$50k", "$75k", "$100k"]

ScatterChart(
    data=countries,
    # add the title
    title="Life expectancy vs. GDP per capita",
    # add the x and y axis labels
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    # label the GDP ticks in thousands of dollars
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    # fix the y-axis range
    ymin=50,
    ymax=90,
).show()
```

### Figure size and grid

To change the figure size, add the `figsize` attribute. The `figsize` attribute can be a tuple (width, height), values are in inches. The `datachart` package provides a [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.FIG_SIZE) constant, which contains some of the predefined figure sizes.

To add the grid, add the `show_grid` attribute. The possible options are:

| Option   | Description                                     |
| -------- | ----------------------------------------------- |
| `"both"` | shows both the x-axis and the y-axis gridlines. |
| `"x"`    | shows only the x-axis grid lines.               |
| `"y"`    | shows only the y-axis grid lines.               |

Again, `datachart` provides a [datachart.constants.SHOW_GRID](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.SHOW_GRID) constant, which contains the supported options.

```
from datachart.constants import FIG_SIZE, SHOW_GRID
```

```
ScatterChart(
    data=countries,
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    # add to determine the figure size
    figsize=FIG_SIZE.FULL_SHORT,
    # add to show the grid lines
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Scatter style

To change the marker style, add the `style` attribute with the corresponding attributes. The supported attributes are shown in the [datachart.typings.ScatterStyleAttrs](https://eriknovak.github.io/datachart/0.8.0/references/typings/#datachart.typings.ScatterStyleAttrs) type, which contains the following attributes:

| Attribute                   | Description                                      |
| --------------------------- | ------------------------------------------------ |
| `"plot_scatter_color"`      | The color of the markers (hex color code).       |
| `"plot_scatter_alpha"`      | The alpha of the markers (how visible they are). |
| `"plot_scatter_size"`       | The size of the markers.                         |
| `"plot_scatter_marker"`     | The marker shape (circle, square, etc.).         |
| `"plot_scatter_zorder"`     | The zorder of the markers.                       |
| `"plot_scatter_edge_width"` | The edge width of the markers.                   |
| `"plot_scatter_edge_color"` | The edge color of the markers (hex color code).  |

Again, to help with the style settings, the [datachart.constants](https://eriknovak.github.io/datachart/0.8.0/references/constants/index.md) module contains the following constants:

| Constant                                                                                                                             | Description                             |
| ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------- |
| [datachart.constants.LINE_MARKER](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.LINE_MARKER) | The marker shape (circle, square, etc.) |

The example below changes the color, transparency, size, shape and outline of the markers in one go. Any attribute you leave out keeps the value of the active theme.

```
from datachart.constants import LINE_MARKER
```

```
ScatterChart(
    data=countries,
    # define the style of the markers
    style={
        "plot_scatter_color": "#e76f51",
        "plot_scatter_alpha": 0.7,
        "plot_scatter_size": 80,
        "plot_scatter_marker": LINE_MARKER.DIAMOND,
        "plot_scatter_edge_width": 1,
        "plot_scatter_edge_color": "#1d3557",
    },
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Hue grouping

To color the points by a categorical variable, add the `hue` attribute with the name of the key that holds the category — here the `continent` key of each country. Each category gets its own color from the theme's palette and its own legend entry, so `show_legend` tells the continents apart.

```
ScatterChart(
    data=countries,
    # color the points by continent
    hue="continent",
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    # show the legend with the continent names
    show_legend=True,
).show()
```

### Bubble chart

To scale the markers by a third variable, add the `size` attribute with the name of the key that holds the value — here the `population` key. The values are mapped linearly onto the marker area range given by `size_range` (the default is `(20, 200)`): the smallest value gets the smallest marker, the largest the largest. With populations from 2 million to 1.4 billion, the upper end is raised so that the gap between the two is visible. An outline and a lower alpha keep overlapping bubbles readable.

`hue` and `size` combine freely. Note that the sizes are scaled within each hue group, so the largest country of every continent gets the largest bubble.

```
ScatterChart(
    data=countries,
    hue="continent",
    # scale the markers by population
    size="population",
    # widen the range of marker areas
    size_range=(20, 800),
    style={
        "plot_scatter_alpha": 0.6,
        "plot_scatter_edge_width": 0.5,
        "plot_scatter_edge_color": "#1d3557",
    },
    title="Life expectancy vs. GDP per capita, sized by population",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

### Regression line

To fit a straight line through the points, add the `show_regression` attribute. `show_ci` draws the confidence band around the line and `ci_level` sets its level (the default is 0.95); `show_correlation` annotates the chart with the Pearson correlation coefficient.

The line is fitted to the plotted values. Life expectancy grows with the *order of magnitude* of GDP per capita rather than with GDP itself, so the example plots `log10` of the GDP per capita and labels the ticks with the dollar amounts they stand for. With `hue` the regression is fitted to all groups together.

```
import math

countries_log_gdp = [{**point, "x": math.log10(point["x"])} for point in countries]

ScatterChart(
    data=countries_log_gdp,
    # fit a regression line through the points
    show_regression=True,
    # draw the 95% confidence band around the line
    show_ci=True,
    ci_level=0.95,
    # annotate the correlation coefficient
    show_correlation=True,
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    # the x values are log10(GDP); label them with the dollar amounts
    xticks=[3, 4, 5],
    xticklabels=["$1k", "$10k", "$100k"],
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Aspect ratio

The `aspect_ratio` attribute fixes the aspect ratio of the axes rather than of the figure: `"auto"` (the default) lets the axes fill the figure, `"equal"` keeps one data unit the same length on both axes. It makes sense when both axes share a unit — distances, coordinates, a predicted value against a measured one — which dollars and years do not. The supported values are in the [datachart.constants.ASPECT_RATIO](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.ASPECT_RATIO) constant; the [European cities example](#example-4-european-cities-bubble-chart-with-an-equal-aspect-ratio) below draws a map with it.

### Emphasis

When a chart carries several series, the story is often about one of them. The `emphasis` attribute expresses that directly: `"highlight"` gives the markers a contrasting edge and brings them to the front, `"background"` mutes a series (the theme's muted color at a lower alpha, drawn behind the others), and `None` leaves a series unchanged. For multiple charts, `emphasis` is a list aligned with `data`, just like `subtitle` and `style`. Only emphasized-or-unset series appear in the legend — background series drop out of it. The role strings are also available as the [datachart.constants.EMPHASIS](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.EMPHASIS) constants.

The example highlights the European countries against the rest of the world, passed as two series. See the [Highlighting](https://eriknovak.github.io/datachart/0.8.0/how-to-guides/styling/highlighting/index.md) guide for how emphasis works across all chart types and themes.

```
europe = [point for point in countries if point["continent"] == "Europe"]
rest_of_world = [point for point in countries if point["continent"] != "Europe"]

ScatterChart(
    data=[rest_of_world, europe],
    subtitle=["other continents", "Europe"],
    # mute the rest of the world, highlight Europe
    emphasis=["background", "highlight"],
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

### Reference lines

Reference lines mark a threshold or a reference value on the chart.

**Horizontal lines.** Use the `hlines` argument with the [datachart.typings.HLinePlotAttrs](https://eriknovak.github.io/datachart/0.8.0/references/typings/#datachart.typings.HLinePlotAttrs) typing, which is either a `dict` or a `List[dict]` where each dictionary contains some of the following attributes:

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
  "label": Optional[str],                    # The label of the line (shown in the legend)
}
```

**Vertical lines.** Use the `vlines` argument with the [datachart.typings.VLinePlotAttrs](https://eriknovak.github.io/datachart/0.8.0/references/typings/#datachart.typings.VLinePlotAttrs) typing, which has the same shape with `x`, `ymin`, `ymax` and `plot_vline_*` style attributes.

The example marks the world averages — a life expectancy of 73 years and a GDP per capita of $13,000 — so the lines split the countries into four quadrants. The line labels appear in the legend.

```
from datachart.constants import LINE_STYLE
```

```
ScatterChart(
    data=countries,
    hue="continent",
    # add a horizontal line at the world average life expectancy
    hlines={
        "y": 73,
        "label": "world average life expectancy",
        "style": {
            "plot_hline_color": "#1d3557",
            "plot_hline_style": LINE_STYLE.DASHED,
            "plot_hline_width": 1.5,
        },
    },
    # add a vertical line at the world average GDP per capita
    vlines={
        "x": 13_000,
        "label": "world average GDP per capita",
        "style": {
            "plot_vline_color": "#e9a03b",
            "plot_vline_style": LINE_STYLE.DOTTED,
            "plot_vline_width": 1.5,
        },
    },
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

## Multiple Scatter Charts

To create multiple scatter charts, pass a list of lists to the `data` argument. Each inner list represents the data for one chart. Per-chart attributes like `subtitle`, `style` and `emphasis` can be passed as lists, where each element corresponds to a chart.

Multiple charts pattern

For multiple charts, `data` becomes a list of lists, and per-chart attributes like `subtitle` and `style` become lists where each element applies to the corresponding chart.

The `countries_by_continent` dataset is such a list of lists, one series per continent. Unlike `hue`, which colors the groups of one series, separate series can also be styled separately: a single `style` dictionary applies to every chart, while a list of dictionaries styles each chart on its own (`None` keeps the theme style for that chart).

```
ScatterChart(
    # use a list of lists to define multiple scatter charts
    data=countries_by_continent,
    # style can be a list (one per chart) or a single dict (applies to all)
    style=[
        {"plot_scatter_marker": LINE_MARKER.CIRCLE},
        {"plot_scatter_marker": LINE_MARKER.SQUARE},
        {"plot_scatter_marker": LINE_MARKER.TRIANGLE},
        None,  # keep the theme style for the fourth chart
    ],
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Sub-chart subtitles

We can name each chart by passing a list of subtitles to the `subtitle` argument. In addition, to help with discerning which chart is which, use the `show_legend` argument to show the legend of the charts.

```
ScatterChart(
    data=countries_by_continent,
    # add a subtitle to each chart
    subtitle=CONTINENTS,
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    # show the legend
    show_legend=True,
).show()
```

### Subplots

To draw each chart in its own subplot, add the `subplots` attribute. The chart's `subtitle` are then added at the top of each subplot, while the `title`, `xlabel` and `ylabel` are positioned to be global for all charts. The `max_cols` attribute limits the number of subplots per row.

```
ScatterChart(
    data=countries_by_continent,
    subtitle=CONTINENTS,
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    # show each chart in its own subplot
    subplots=True,
    # at most two subplots per row
    max_cols=2,
).show()
```

### Sharing the x-axis and/or y-axis across subplots

To share the x-axis and/or y-axis across subplots, add the `sharex` and/or `sharey` attributes, which are boolean values that specify whether to share the axis across all subplots. With shared axes the continents become directly comparable — Africa's cluster no longer fills its subplot.

```
ScatterChart(
    data=countries_by_continent,
    subtitle=CONTINENTS,
    title="Life expectancy vs. GDP per capita",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    subplots=True,
    max_cols=2,
    # share the x-axis across subplots
    sharex=True,
    # share the y-axis across subplots
    sharey=True,
).show()
```

## Additional Features

### Axis scales

The user can change the axis scale using the `scalex` and `scaley` attributes. The supported scale options are:

| Options    | Description              |
| ---------- | ------------------------ |
| `"linear"` | The linear scale.        |
| `"log"`    | The log scale.           |
| `"symlog"` | The symmetric log scale. |
| `"asinh"`  | The asinh scale.         |

Again, to help with the options settings, the [datachart.constants](https://eriknovak.github.io/datachart/0.8.0/references/constants/index.md) module contains the following constants:

| Constant                                                                                                                 | Description       |
| ------------------------------------------------------------------------------------------------------------------------ | ----------------- |
| [datachart.constants.SCALE](https://eriknovak.github.io/datachart/0.8.0/references/constants/#datachart.constants.SCALE) | The axis options. |

A logarithmic scale pays off when the values span several orders of magnitude. GDP per capita runs from $1,000 to over $100,000: on a linear scale the poorer half of the countries piles up against the y-axis, on a log scale the relationship with life expectancy straightens out and every country gets room.

```
from datachart.constants import SCALE
```

```
for scale in [SCALE.LINEAR, SCALE.LOG]:
    figure = ScatterChart(
        data=countries,
        hue="continent",
        title=f"Life expectancy vs. GDP per capita on the '{scale}' scale",
        xlabel="GDP per capita (USD)",
        ylabel="Life expectancy (years)",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.BOTH,
        show_legend=True,
        # set the scale of the x axis
        scalex=scale,
    )
    figure.show()
```

### Custom data keys

By default, the `data` items are dictionaries with the keys `x` and `y`, and `size` and `hue` name whichever keys hold the bubble size and the category. Data that comes from elsewhere rarely calls its columns `x` and `y`, and renaming every key just to plot it is a chore. Instead, tell `ScatterChart` which keys to read with the `x` and `y` arguments. The `country_records` list below stores the same countries under their natural names.

```
country_records = [
    {
        "country": name,
        "continent": continent,
        "gdp_per_capita": gdp,
        "life_expectancy": life,
        "population": population,
    }
    for name, (continent, gdp, life, population) in COUNTRIES.items()
]
country_records[:3]
```

```
figure = ScatterChart(
    data=country_records,
    # specify which keys hold the x and y values
    x="gdp_per_capita",
    y="life_expectancy",
    # and which hold the bubble size and the category
    size="population",
    hue="continent",
    size_range=(20, 800),
    style={
        "plot_scatter_alpha": 0.6,
        "plot_scatter_edge_width": 0.5,
        "plot_scatter_edge_color": "#1d3557",
    },
    title="Life expectancy vs. GDP per capita, sized by population",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
    scalex=SCALE.LOG,
)
figure.show()
```

## Saving the Chart as an Image

To save the chart as an image, use the [datachart.utils.save_figure](https://eriknovak.github.io/datachart/0.8.0/references/utils#datachart.utils.save_figure) function.

```
from datachart.utils import save_figure
```

```
save_figure(figure, "./fig_scatter_chart.png", dpi=300)
```

The figure should be saved in the current working directory.

## Real-World Examples

The following examples put the features above to work on real or realistic data. Each one states what its data is and where it comes from; the data itself lives in a hidden cell.

### Example 1: Model Accuracy vs. Parameter Count (Regression Line and Confidence Interval)

`model_accuracy` holds the benchmark accuracy of 24 illustrative language models with 0.1 to 100 billion parameters. Accuracy grows with the logarithm of the model size, so the points are plotted against `log10` of the parameter count (with the ticks labeled in billions) and `show_regression` fits the scaling trend, `show_ci` draws its 90% confidence band and `show_correlation` reports how tight the trend is. The run-to-run noise comes from a seeded random generator.

```
ScatterChart(
    data=model_accuracy,
    style={"plot_scatter_alpha": 0.8},
    # fit the scaling trend and its 90% confidence band
    show_regression=True,
    show_ci=True,
    ci_level=0.9,
    # report the correlation coefficient
    show_correlation=True,
    title="Benchmark accuracy vs. model size",
    xlabel="Parameters",
    ylabel="Accuracy (%)",
    # the x values are log10(parameters); label them in billions
    xticks=[-1, 0, 1, 2],
    xticklabels=["0.1B", "1B", "10B", "100B"],
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Example 2: Penguin Morphometrics (Hue Grouping and Custom Data Keys)

`penguins` holds the bill length and flipper length of 120 illustrative penguins of three species, 40 per species, drawn from a seeded Gaussian around the species means of the Palmer penguins dataset. The measurements are stored under `bill_length` and `flipper_length`, so the keys are mapped with the `x` and `y` arguments, and `hue` colors each species so the three clusters — and the overlap between Adelie and Chinstrap flippers — stand out.

```
ScatterChart(
    data=penguins,
    # the points are stored as "bill_length" and "flipper_length"
    x="bill_length",
    y="flipper_length",
    # color the points by species
    hue="species",
    style={
        "plot_scatter_alpha": 0.7,
        "plot_scatter_edge_width": 0.5,
        "plot_scatter_edge_color": "#1d3557",
    },
    title="Penguin flipper length vs. bill length",
    xlabel="Bill length (mm)",
    ylabel="Flipper length (mm)",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

### Example 3: One Sweep Among Many (Emphasis)

`tuning_runs` holds two series of illustrative hyperparameter tuning runs, each run a point of training time against validation accuracy: 150 runs of a broad random search and the 12 runs of a final, narrowed-down sweep. The question is whether the final sweep actually beat the search, so `emphasis` mutes the random search into a background cloud and highlights the sweep. Muted series drop out of the legend automatically; both series are drawn from seeded random generators.

```
ScatterChart(
    data=tuning_runs,
    subtitle=["random search", "final sweep"],
    # mute the random search, highlight the final sweep
    emphasis=["background", "highlight"],
    title="Validation accuracy of the tuning runs",
    xlabel="Training time (minutes)",
    ylabel="Validation accuracy (%)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

### Example 4: European Cities (Bubble Chart with an Equal Aspect Ratio)

`cities` holds the longitude, latitude and metropolitan population (in millions, rounded) of 21 European cities. Plotting longitude against latitude turns the scatter chart into a map, which only keeps its shape if a degree is the same length on both axes — hence `aspect_ratio`. `size` scales each bubble by population and `size_range` is widened so that the capitals dominate the map the way they dominate the continent.

```
from datachart.constants import ASPECT_RATIO
```

```
ScatterChart(
    data=cities,
    # scale the bubbles by population
    size="population",
    size_range=(30, 900),
    style={
        "plot_scatter_alpha": 0.5,
        "plot_scatter_edge_width": 0.8,
        "plot_scatter_edge_color": "#1d3557",
    },
    title="Metropolitan population of European cities",
    xlabel="Longitude (°E)",
    ylabel="Latitude (°N)",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    # keep one degree the same length on both axes
    aspect_ratio=ASPECT_RATIO.EQUAL,
).show()
```
