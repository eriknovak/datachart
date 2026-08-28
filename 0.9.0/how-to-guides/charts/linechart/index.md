# Line Chart

This section showcases the line chart. It contains examples of how to create line charts using the [datachart.charts.LineChart](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.LineChart) function.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-line-chart), which maps common tasks to the parameter or style attribute that does the job.

As mentioned above, the line charts are created using the `LineChart` function found in the [datachart.charts](https://eriknovak.github.io/datachart/0.9.0/references/charts/index.md) module. Let's import it:

```
from datachart.charts import LineChart
```

## Line Chart Input Attributes

The `LineChart` function accepts keyword arguments for chart configuration. The main argument is `data`, which contains the data points. For a single line chart, `data` is a list of dictionaries. For multiple line charts, `data` is a list of lists.

```
LineChart(
    data=[{                                             # A list of line data points (or list of lists for multiple charts)
        "x":    Union[int, float],                      # The x-axis value
        "y":    Union[int, float],                      # The y-axis value
        "yerr": Optional[Union[int, float]]             # The y-axis error value (to plot the confidence interval)
    }],
    style={                                             # The style of the line (optional)
        "plot_line_color":     Optional[str],           # The color of the line (hex color code)
        "plot_line_style":     Optional[LINE_STYLE],    # The line style (solid, dashed, etc.)
        "plot_line_marker":    Optional[LINE_MARKER],   # The marker style of the line (circle, square, etc.)
        "plot_line_width":     Optional[float],         # The width of the line
        "plot_line_alpha":     Optional[float],         # The alpha of the line (how visible the line is)
        "plot_line_drawstyle": Optional[LINE_DRAW_STYLE], # The drawstyle of the line (step, steps-mid, etc.)
        "plot_line_zorder":    Optional[int],           # The zorder of the line
        "plot_area_color":     Optional[str],           # The color of the area under the line / confidence band
        "plot_area_alpha":     Optional[float],         # The alpha of the area
        "plot_area_hatch":     Optional[HATCH_STYLE],   # The hatch style of the area
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
    show_area=Optional[bool],                           # Whether to fill the area under the line
    show_yerr=Optional[bool],                           # Whether to show the confidence interval (from "yerr")

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
    yerr=Optional[str],                                 # the key holding the y-axis error value (default: "yerr")
)
```

For more details, see the [datachart.charts.LineChart](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.LineChart) function.

## Basics

The examples in this guide share one dataset: the average monthly temperature (in °C) of three European cities, based on their 1991–2020 climate normals. The data is hard-coded in a hidden cell; `temperature_ljubljana` holds the twelve monthly values of Ljubljana, and `temperature_by_city` holds one series per city — Ljubljana, Reykjavik and Lisbon — with the year-to-year standard deviation of each monthly mean as `yerr`. `MONTHS` holds the month names used as tick labels.

Each data point is a dictionary with an `x` value (here the month number) and a `y` value:

```
temperature_ljubljana[:3]
```

**Basic example.** Only the `data` argument is required to draw the line chart.

```
LineChart(
    # add the data to the chart
    data=temperature_ljubljana
).show()
```

## Customizing the Line Chart

Every customization is either a keyword argument of `LineChart` or a `plot_line_*` / `plot_area_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                            | Use                                                                   | See                                                           |
| ------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------- |
| add a title and axis labels           | `title`, `xlabel`, `ylabel`                                           | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| set custom tick positions and labels  | `xticks`, `xticklabels`, `yticks`, `yticklabels`                      | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| rotate the tick labels                | `xtickrotate`, `ytickrotate`                                          | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| fix the axis range                    | `xmin`, `xmax`, `ymin`, `ymax`                                        | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| resize the figure                     | `figsize`                                                             | [Figure size and grid](#figure-size-and-grid)                 |
| show grid lines                       | `show_grid`                                                           | [Figure size and grid](#figure-size-and-grid)                 |
| fix the aspect ratio of the axes      | `aspect_ratio`                                                        | [Figure size and grid](#figure-size-and-grid)                 |
| change the line color                 | `style={"plot_line_color": ...}`                                      | [Line style](#line-style)                                     |
| dash or dot the line                  | `style={"plot_line_style": ...}`                                      | [Line style](#line-style)                                     |
| mark the data points                  | `style={"plot_line_marker": ...}`                                     | [Line style](#line-style)                                     |
| draw the line as steps                | `style={"plot_line_drawstyle": ...}`                                  | [Line style](#line-style)                                     |
| change the line width or transparency | `style={"plot_line_width": ..., "plot_line_alpha": ...}`              | [Line style](#line-style)                                     |
| fill the area under the line          | `show_area`, `style={"plot_area_color": ..., "plot_area_alpha": ...}` | [Area under the line](#area-under-the-line)                   |
| highlight one series, mute the rest   | `emphasis`                                                            | [Emphasis](#emphasis)                                         |
| mark a threshold or an event          | `hlines`, `vlines`                                                    | [Reference lines](#reference-lines)                           |
| compare several series in one chart   | `data` as a list of lists, `subtitle`, `show_legend`                  | [Multiple Line Charts](#multiple-line-charts)                 |
| draw each series in its own subplot   | `subplots`, `sharex`, `sharey`, `max_cols`                            | [Subplots](#subplots)                                         |
| draw a confidence interval            | `yerr` in `data`, `show_yerr`                                         | [Confidence interval](#confidence-interval)                   |
| use a logarithmic axis                | `scaley`, `scalex`                                                    | [Axis scales](#axis-scales)                                   |
| plot data with other key names        | `x`, `y`, `yerr`                                                      | [Custom data keys](#custom-data-keys)                         |
| save the chart to a file              | `save_figure`                                                         | [Saving the Chart as an Image](#saving-the-chart-as-an-image) |

The full list of style attributes is in the [datachart.typings.LineStyleAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.LineStyleAttrs) and [datachart.typings.AreaStyleAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.AreaStyleAttrs) types; the full list of parameters is in the [datachart.charts.LineChart](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.LineChart) reference.

### Title, axis labels and ticks

To add the chart title and axis labels, add the `title`, `xlabel` and `ylabel` attributes. The tick positions and their labels can be set with `xticks` and `xticklabels` (or `yticks` and `yticklabels`) — here the month numbers on the x-axis are replaced by month names. Tick labels can be rotated with `xtickrotate` (or `ytickrotate`), and the axis range can be fixed with `xmin`, `xmax`, `ymin` and `ymax`.

```
LineChart(
    data=temperature_ljubljana,
    # add the title
    title="Average monthly temperature in Ljubljana",
    # add the x and y axis labels
    xlabel="Month",
    ylabel="Temperature (°C)",
    # show the month names instead of the month numbers
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    # rotate the x-axis tick labels
    xtickrotate=45,
    # fix the y-axis range
    ymin=-5,
    ymax=25,
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

Again, `datachart` provides a [datachart.constants.SHOW_GRID](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.SHOW_GRID) constant, which contains the supported options.

Related is the `aspect_ratio` attribute, which fixes the aspect ratio of the axes rather than of the figure: `"auto"` (the default) lets the axes fill the figure, `"equal"` keeps one data unit the same length on both axes. The supported values are in the [datachart.constants.ASPECT_RATIO](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.ASPECT_RATIO) constant; the [ROC curve example](#example-1-roc-curve-custom-data-keys-and-equal-aspect-ratio) below uses it.

```
from datachart.constants import FIG_SIZE, SHOW_GRID
```

```
LineChart(
    data=temperature_ljubljana,
    title="Average monthly temperature in Ljubljana",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    # add to determine the figure size
    figsize=FIG_SIZE.FULL_SHORT,
    # add to show the grid lines
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Line style

To change the line style, add the `style` attribute with the corresponding attributes. The supported attributes are shown in the [datachart.typings.LineStyleAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.LineStyleAttrs) type, which contains the following attributes:

| Attribute                    | Description                                          |
| ---------------------------- | ---------------------------------------------------- |
| `"plot_line_color"`          | The color of the line (hex color code).              |
| `"plot_line_alpha"`          | The alpha of the line (how visible the line is).     |
| `"plot_line_width"`          | The width of the line.                               |
| `"plot_line_style"`          | The line style (solid, dashed, etc.).                |
| `"plot_line_marker"`         | The marker style of the line (circle, square, etc.). |
| `"plot_line_drawstyle"`      | The drawstyle of the line (step, steps-mid, etc.).   |
| `"plot_line_zorder"`         | The zorder of the line.                              |
| `"plot_xticks_label_rotate"` | The rotation of the x-axis tick labels.              |
| `"plot_yticks_label_rotate"` | The rotation of the y-axis tick labels.              |

Again, to help with the style settings, the [datachart.constants](https://eriknovak.github.io/datachart/0.9.0/references/constants/index.md) module contains the following constants:

| Constant                                                                                                                                     | Description                                         |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| [datachart.constants.LINE_STYLE](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.LINE_STYLE)           | The line style (solid, dashed, etc.)                |
| [datachart.constants.LINE_MARKER](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.LINE_MARKER)         | The marker style of the line (circle, square, etc.) |
| [datachart.constants.LINE_DRAW_STYLE](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.LINE_DRAW_STYLE) | The drawstyle of the line (step, steps-mid, etc.)   |

The example below changes the color, width, dash pattern and marker of the line in one go. Any attribute you leave out keeps the value of the active theme.

```
from datachart.constants import LINE_STYLE, LINE_MARKER, LINE_DRAW_STYLE
```

```
LineChart(
    data=temperature_ljubljana,
    # define the style of the line
    style={
        "plot_line_color": "#e76f51",
        "plot_line_width": 2,
        "plot_line_style": LINE_STYLE.DASHED,
        "plot_line_marker": LINE_MARKER.CIRCLE,
    },
    title="Average monthly temperature in Ljubljana",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
).show()
```

Monthly averages are one value per month rather than a continuous curve. The `plot_line_drawstyle` attribute draws the line as steps instead — `LINE_DRAW_STYLE.STEPS_MID` centers each step on its data point.

```
LineChart(
    data=temperature_ljubljana,
    style={
        # draw the line as steps centered on the data points
        "plot_line_drawstyle": LINE_DRAW_STYLE.STEPS_MID,
        "plot_line_marker": LINE_MARKER.POINT,
    },
    title="Average monthly temperature in Ljubljana",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Area under the line

To fill the area between the line and the bottom of the axes, add the `show_area` attribute. The fill takes the color of the line at a lower alpha; the `plot_area_color`, `plot_area_alpha` and `plot_area_hatch` style attributes from the [datachart.typings.AreaStyleAttrs](https://eriknovak.github.io/datachart/0.9.0/how-to-guides/charts/linechart/%7BREF%7D/typings/#datachart.typings.AreaStyleAttrs) type override that. With the step draw style the fill follows the steps.

```
LineChart(
    data=temperature_ljubljana,
    style={
        "plot_line_drawstyle": LINE_DRAW_STYLE.STEPS_MID,
        # make the fill a bit stronger than the theme default
        "plot_area_alpha": 0.35,
    },
    title="Average monthly temperature in Ljubljana",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    # fill the area under the line
    show_area=True,
).show()
```

### Emphasis

When a chart carries several series, the story is often about one of them. The `emphasis` attribute expresses that directly: `"highlight"` thickens a line and brings it to the front, `"background"` mutes a line (the theme's muted color at a lower alpha, thinner and drawn behind the others), and `None` leaves a line unchanged. For multiple charts, `emphasis` is a list aligned with `data`, just like `subtitle` and `style`. Only emphasized-or-unset series appear in the legend — background lines drop out of it. The role strings are also available as the [datachart.constants.EMPHASIS](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.EMPHASIS) constants.

The example highlights Ljubljana against the other two cities. See the [Highlighting](https://eriknovak.github.io/datachart/0.9.0/how-to-guides/styling/highlighting/index.md) guide for how emphasis works across all chart types and themes.

```
LineChart(
    data=temperature_by_city,
    subtitle=CITIES,
    # highlight Ljubljana, mute the other cities
    emphasis=["highlight", "background", "background"],
    title="Average monthly temperature",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

### Reference lines

Reference lines mark a threshold or an event on the chart.

**Horizontal lines.** Use the `hlines` argument with the [datachart.typings.HLinePlotAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.HLinePlotAttrs) typing, which is either a `dict` or a `List[dict]` where each dictionary contains some of the following attributes:

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

**Vertical lines.** Use the `vlines` argument with the [datachart.typings.VLinePlotAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.VLinePlotAttrs) typing, which has the same shape with `x`, `ymin`, `ymax` and `plot_vline_*` style attributes. The `x` value is in data coordinates, so a line can sit anywhere along the axis — here between two months.

The example marks the freezing point with a dashed horizontal line and the summer solstice (21 June) with a vertical line. The line labels appear in the legend.

```
LineChart(
    data=temperature_ljubljana,
    subtitle="Ljubljana",
    # add a horizontal line at the freezing point
    hlines={
        "y": 0,
        "label": "freezing point",
        "style": {
            "plot_hline_color": "#1d3557",
            "plot_hline_style": LINE_STYLE.DASHED,
            "plot_hline_width": 1.5,
        },
    },
    # add a vertical line at the summer solstice
    vlines={
        "x": 6.7,
        "label": "summer solstice",
        "style": {
            "plot_vline_color": "#e9a03b",
            "plot_vline_style": LINE_STYLE.DOTTED,
            "plot_vline_width": 1.5,
        },
    },
    title="Average monthly temperature in Ljubljana",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

## Multiple Line Charts

To create multiple line charts, pass a list of lists to the `data` argument. Each inner list represents the data for one line. Per-chart attributes like `subtitle`, `style` and `emphasis` can be passed as lists, where each element corresponds to a chart.

Multiple charts pattern

For multiple charts, `data` becomes a list of lists, and per-chart attributes like `subtitle` and `style` become lists where each element applies to the corresponding chart.

The `temperature_by_city` dataset is such a list of lists, one series per city. A single `style` dictionary applies to every line; a list of dictionaries styles each line separately (`None` keeps the theme style for that line).

```
LineChart(
    # use a list of lists to define multiple lines
    data=temperature_by_city,
    # style can be a list (one per chart) or a single dict (applies to all)
    style=[
        {"plot_line_marker": LINE_MARKER.CIRCLE},
        {"plot_line_marker": LINE_MARKER.SQUARE},
        None,  # keep the theme style for the third line
    ],
    title="Average monthly temperature",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Sub-chart subtitles

We can name each chart by passing a list of subtitles to the `subtitle` argument. In addition, to help with discerning which chart is which, use the `show_legend` argument to show the legend of the charts.

```
LineChart(
    data=temperature_by_city,
    # add a subtitle to each line
    subtitle=CITIES,
    title="Average monthly temperature",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    # show the legend
    show_legend=True,
).show()
```

### Subplots

To draw each chart in its own subplot, add the `subplots` attribute. The chart's `subtitle` are then added at the top of each subplot, while the `title`, `xlabel` and `ylabel` are positioned to be global for all charts. The `max_cols` attribute limits the number of subplots per row.

```
LineChart(
    data=temperature_by_city,
    subtitle=CITIES,
    title="Average monthly temperature",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    # show each chart in its own subplot
    subplots=True,
    # at most two subplots per row
    max_cols=2,
).show()
```

### Sharing the x-axis and/or y-axis across subplots

To share the x-axis and/or y-axis across subplots, add the `sharex` and/or `sharey` attributes, which are boolean values that specify whether to share the axis across all subplots. With a shared y-axis, the cities become directly comparable — Reykjavik's flat curve no longer fills its subplot.

```
LineChart(
    data=temperature_by_city,
    subtitle=CITIES,
    title="Average monthly temperature",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
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

### Area under the lines

Specifying the `show_area` attribute fills the area under each line. In a single chart the fills overlap, so the attribute is at its best with subplots.

```
LineChart(
    data=temperature_by_city,
    subtitle=CITIES,
    title="Average monthly temperature",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    subplots=True,
    max_cols=2,
    sharex=True,
    sharey=True,
    # fill the area under the line in all subplots
    show_area=True,
).show()
```

### Confidence interval

If a line chart has a confidence interval, it can be added by adding the `yerr` attribute to the chart's `data` attribute. Afterwards, the `show_yerr` attribute can be set to `True` to draw the band between `y - yerr` and `y + yerr`. The `temperature_by_city` data points carry the year-to-year standard deviation of each monthly mean as `yerr`. The band is styled with the same `plot_area_*` attributes as the area under the line.

```
LineChart(
    data=temperature_by_city,
    subtitle=CITIES,
    title="Average monthly temperature",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
    # draw the confidence interval using the error values
    show_yerr=True,
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

Again, to help with the options settings, the [datachart.constants](https://eriknovak.github.io/datachart/0.9.0/references/constants/index.md) module contains the following constants:

| Constant                                                                                                                 | Description       |
| ------------------------------------------------------------------------------------------------------------------------ | ----------------- |
| [datachart.constants.SCALE](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.SCALE) | The axis options. |

A logarithmic scale pays off when the values span several orders of magnitude. The hidden cell below defines `transistors`, the transistor count of a representative microprocessor per year from the Intel 4004 (1971) to the Apple M1 Ultra (2022) — Moore's law in sixteen data points, rounded from the manufacturers' figures.

```
from datachart.constants import SCALE
```

On a linear scale the first forty years collapse onto the x-axis; on a log scale the exponential growth becomes the straight line it is famous for.

```
for scale in [SCALE.LINEAR, SCALE.LOG]:
    figure = LineChart(
        data=transistors,
        style={"plot_line_marker": LINE_MARKER.CIRCLE},
        title=f"Transistors per microprocessor on the '{scale}' scale",
        xlabel="Year",
        ylabel="Transistors",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.BOTH,
        # set the scale of the y axis
        scaley=scale,
    )
    figure.show()
```

### Custom data keys

By default, the `data` items are dictionaries with the keys `x`, `y` and, optionally, `yerr`. Data that comes from elsewhere rarely uses those names, and renaming every key just to plot it is a chore. Instead, tell `LineChart` which keys to read with the `x`, `y` and `yerr` arguments. The `readings` list below stores the Ljubljana temperatures under `month` and `temperature`, with the deviation under `spread`.

```
readings = [
    {"month": month, "temperature": temp, "spread": std}
    for month, temp, std in zip(MONTH_TICKS, TEMPERATURE["Ljubljana"], TEMPERATURE_STD["Ljubljana"])
]
readings[:3]
```

```
figure = LineChart(
    data=readings,
    # specify which keys hold the x, y and error values
    x="month",
    y="temperature",
    yerr="spread",
    title="Average monthly temperature in Ljubljana",
    xlabel="Month",
    ylabel="Temperature (°C)",
    xticks=MONTH_TICKS,
    xticklabels=MONTHS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    show_yerr=True,
)
figure.show()
```

## Saving the Chart as an Image

To save the chart as an image, use the [datachart.utils.save_figure](https://eriknovak.github.io/datachart/0.9.0/references/utils#datachart.utils.save_figure) function.

```
from datachart.utils import save_figure
```

```
save_figure(figure, "./fig_line_chart.png", dpi=300)
```

The figure should be saved in the current working directory.

## Real-World Examples

The following examples put the features above to work on real or realistic data. Each one states what its data is and where it comes from; the data itself lives in a hidden cell.

### Example 1: ROC Curve (Custom Data Keys and Equal Aspect Ratio)

`roc_curves` holds the receiver operating characteristic of two illustrative binary classifiers: each point is the false positive rate (`fp`) and true positive rate (`tp`) at one decision threshold, so the keys are mapped with the `x` and `y` arguments. A ROC curve is read against the diagonal, so the subplots share an equal aspect ratio (`aspect_ratio`) and the area under each curve — the AUC — is filled with a hatch pattern.

```
from datachart.constants import ASPECT_RATIO, HATCH_STYLE
```

```
LineChart(
    data=roc_curves,
    subtitle=list(ROC_POINTS),
    # the points are stored as "fp" and "tp", instead of "x" and "y"
    x="fp",
    y="tp",
    # hatch the area under each curve (a single style applies to every chart)
    style={"plot_area_hatch": HATCH_STYLE.DIAGONAL},
    title="ROC curve",
    xlabel="False positive rate",
    ylabel="True positive rate",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    xmin=0,
    xmax=1,
    ymin=0,
    ymax=1,
    show_area=True,
    subplots=True,
    sharex=True,
    sharey=True,
    # keep one unit the same length on both axes
    aspect_ratio=ASPECT_RATIO.EQUAL,
).show()
```

### Example 2: Training Loss (Confidence Interval on a Log Scale)

`training_loss` holds the validation loss of three illustrative training methods, evaluated every five steps over 200 steps and averaged over several runs; `spread` is the standard deviation across the runs. The loss decays exponentially toward a floor, so the y-axis uses a log scale to keep the late-training differences readable, and `show_yerr` draws the run-to-run spread as a band around each mean.

```
LineChart(
    data=training_loss,
    subtitle=list(LOSS_CURVES),
    # the points are stored as "step", "loss" and "spread"
    x="step",
    y="loss",
    yerr="spread",
    title="Validation loss during training",
    xlabel="Training step",
    ylabel="Validation loss",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # draw the run-to-run spread as a band
    show_yerr=True,
    # depict the y-axis as a log scale
    scaley=SCALE.LOG,
).show()
```

### Example 3: One Index Among Many (Emphasis)

`sector_indices` holds the illustrative performance of five stock market sector indices over three years, sampled quarterly and rebased to 100 at the end of 2022. The question is how the technology sector did against the market, so `emphasis` highlights it and mutes the other four. Muted indices drop out of the legend automatically.

```
LineChart(
    data=sector_indices,
    subtitle=list(SECTOR_INDEX),
    # highlight Technology, mute the other sectors
    emphasis=["highlight", "background", "background", "background", "background"],
    title="Sector indices, rebased to 100",
    xlabel="Quarter",
    ylabel="Index level",
    # the x values are quarter offsets; label them with the quarter names
    xticks=list(range(len(QUARTERS))),
    xticklabels=QUARTERS,
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Example 4: Website Traffic (Reference Lines)

`weekly_visitors` holds the illustrative weekly unique visitors of a website over sixteen weeks. A marketing campaign launched in week 7, and the hosting plan is sized for 60,000 weekly visitors. A vertical line marks the launch and a horizontal line the capacity, so the chart answers both "did the campaign work" and "when do we need to upgrade" at a glance.

```
LineChart(
    data=weekly_visitors,
    subtitle="unique visitors",
    style={"plot_line_marker": LINE_MARKER.CIRCLE},
    # mark the campaign launch
    vlines={
        "x": CAMPAIGN_WEEK,
        "label": "campaign launch",
        "style": {
            "plot_vline_color": "#2a9d8f",
            "plot_vline_style": LINE_STYLE.DASHED,
            "plot_vline_width": 1.5,
        },
    },
    # mark the hosting capacity
    hlines={
        "y": CAPACITY,
        "label": "hosting capacity",
        "style": {
            "plot_hline_color": "#c1121f",
            "plot_hline_style": LINE_STYLE.DOTTED,
            "plot_hline_width": 1.5,
        },
    },
    title="Weekly website visitors",
    xlabel="Week",
    ylabel="Visitors (thousands)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    ymin=0,
).show()
```
