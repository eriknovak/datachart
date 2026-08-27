# Bar Chart

This section showcases the bar chart. It contains examples of how to create the bar chart using the [datachart.charts.BarChart](https://eriknovak.github.io/datachart/references/charts/#datachart.charts.BarChart) function.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-bar-chart), which maps common tasks to the parameter or style attribute that does the job.

As mentioned above, the bar charts are created using the `BarChart` function found in the [datachart.charts](https://eriknovak.github.io/datachart/references/charts/index.md) module. Let's import it:

```
from datachart.charts import BarChart
```

## Bar Chart Input Attributes

The `BarChart` function accepts keyword arguments for chart configuration. The main argument is `data`, which contains the data points. For a single bar chart, `data` is a list of dictionaries. For multiple bar charts, `data` is a list of lists.

```
BarChart(
    data=[{                                             # A list of bar data points (or list of lists for multiple charts)
        "label": str,                                   # The x-axis value
        "y":     Union[int, float],                     # The y-axis value
        "yerr":  Optional[Union[int, float]]            # The y-axis error value
    }],
    style={                                             # The style of the bar (optional)
        "plot_bar_color":       Union[str, None],       # The color of the bar
        "plot_bar_alpha":       Union[float, None],     # The alpha of the bar
        "plot_bar_width":       Union[int, float, None], # The width of the bar
        "plot_bar_zorder":      Union[int, float, None], # The z-order of the bar
        "plot_bar_hatch":       Union[HATCH_STYLE, None], # The hatch style of the bar
        "plot_bar_edge_width":  Union[int, float, None], # The edge line width of the edge
        "plot_bar_edge_color":  Union[str, None],       # The edge line color
        "plot_bar_error_color": Union[str, None],       # The error line color
        "plot_bar_value_fontsize": Union[int, float, None], # The font size of bar value labels
        "plot_bar_value_color": Union[str, None],       # The color of bar value labels
        "plot_bar_value_padding": Union[int, float, None], # The padding between bar and value label
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
    orientation=Optional[str],                          # "vertical" (default) or "horizontal"
    bar_mode=Optional[str],                             # How multiple series share the axis ("group", "stack", "overlay")

    show_yerr=Optional[bool],                           # Whether to show the error bars
    show_values=Optional[bool],                         # Whether to show bar value labels
    value_format=Optional[str],                         # Format of the value labels (VALUE_FORMAT constant or e.g. "{:.1f}%")

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
)
```

For more details, see the [datachart.charts.BarChart](https://eriknovak.github.io/datachart/references/charts/#datachart.charts.BarChart) function.

## Basics

The examples in this guide share one dataset: the monthly unit sales of a product in 2025, broken down by sales region. The data is hard-coded in a hidden cell; `sales_total` holds the company-wide monthly totals, `sales_by_region` holds one series per region (with the day-to-day standard deviation of daily sales as `yerr`), and `SALES_GOAL` is the monthly target.

Each data point is a dictionary with a `label` (the category) and a `y` value:

```
sales_total[:3]
```

**Basic example.** Only the `data` argument is required to draw the bar chart.

```
BarChart(
    # add the data to the chart
    data=sales_total
).show()
```

## Customizing the Bar Chart

Every customization is either a keyword argument of `BarChart` or a `plot_bar_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                          | Use                                                                                                  | See                                                           |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| add a title and axis labels         | `title`, `xlabel`, `ylabel`                                                                          | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| rotate the tick labels              | `xtickrotate`, `ytickrotate`                                                                         | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| fix the axis range                  | `xmin`, `xmax`, `ymin`, `ymax`                                                                       | [Title, axis labels and ticks](#title-axis-labels-and-ticks)  |
| resize the figure                   | `figsize`                                                                                            | [Figure size and grid](#figure-size-and-grid)                 |
| show grid lines                     | `show_grid`                                                                                          | [Figure size and grid](#figure-size-and-grid)                 |
| fix the aspect ratio of the axes    | `aspect_ratio`                                                                                       | [Figure size and grid](#figure-size-and-grid)                 |
| change the bar color                | `style={"plot_bar_color": ...}`                                                                      | [Bar style](#bar-style)                                       |
| change the bar width                | `style={"plot_bar_width": ...}`                                                                      | [Bar style](#bar-style)                                       |
| make the bars (semi-)transparent    | `style={"plot_bar_alpha": ...}`                                                                      | [Bar style](#bar-style)                                       |
| add a hatch pattern                 | `style={"plot_bar_hatch": ...}`                                                                      | [Bar style](#bar-style)                                       |
| outline the bars                    | `style={"plot_bar_edge_color": ..., "plot_bar_edge_width": ...}`                                     | [Bar style](#bar-style)                                       |
| draw horizontal bars                | `orientation`                                                                                        | [Bar orientation](#bar-orientation)                           |
| highlight one series, mute the rest | `emphasis`                                                                                           | [Emphasis](#emphasis)                                         |
| mark a goal, threshold or event     | `hlines`, `vlines`                                                                                   | [Reference lines](#reference-lines)                           |
| compare several series side by side | `data` as a list of lists, `subtitle`, `show_legend`                                                 | [Multiple Bar Charts](#multiple-bar-charts)                   |
| stack or overlay the series         | `bar_mode`                                                                                           | [Bar mode](#bar-mode)                                         |
| draw each series in its own subplot | `subplots`, `sharex`, `sharey`, `max_cols`                                                           | [Subplots](#subplots)                                         |
| add error bars                      | `yerr` in `data`, `show_yerr`, `style={"plot_bar_error_color": ...}`                                 | [Error bars](#error-bars)                                     |
| print the value on each bar         | `show_values`                                                                                        | [Bar value labels](#bar-value-labels)                         |
| format the printed values           | `value_format` (a `VALUE_FORMAT` constant or a format string)                                        | [Bar value labels](#bar-value-labels)                         |
| style the value labels              | `style={"plot_bar_value_fontsize": ..., "plot_bar_value_color": ..., "plot_bar_value_padding": ...}` | [Bar value labels](#bar-value-labels)                         |
| use a logarithmic axis              | `scaley`, `scalex`                                                                                   | [Axis scales](#axis-scales)                                   |
| save the chart to a file            | `save_figure`                                                                                        | [Saving the Chart as an Image](#saving-the-chart-as-an-image) |

The full list of style attributes is in the [datachart.typings.BarStyleAttrs](https://eriknovak.github.io/datachart/references/typings/#datachart.typings.BarStyleAttrs) type; the full list of parameters is in the [datachart.charts.BarChart](https://eriknovak.github.io/datachart/references/charts/#datachart.charts.BarChart) reference.

### Title, axis labels and ticks

To add the chart title and axis labels, add the `title`, `xlabel` and `ylabel` attributes. Tick labels can be rotated with `xtickrotate` (or `ytickrotate`), and the axis range can be fixed with `xmin`, `xmax`, `ymin` and `ymax` — here the y-axis is pinned to start at zero so the bar heights stay comparable.

```
BarChart(
    data=sales_total,
    # add the title
    title="Monthly unit sales (2025)",
    # add the x and y axis labels
    xlabel="Month",
    ylabel="Units sold",
    # rotate the x-axis tick labels
    xtickrotate=45,
    # fix the y-axis range
    ymin=0,
    ymax=2000,
).show()
```

### Figure size and grid

To change the figure size, add the `figsize` attribute. The `figsize` attribute can be a tuple (width, height), values are in inches. The `datachart` package provides a [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/references/constants/#datachart.constants.FIG_SIZE) constant, which contains some of the predefined figure sizes.

To add the grid, add the `show_grid` attribute. The possible options are:

| Option   | Description                                     |
| -------- | ----------------------------------------------- |
| `"both"` | shows both the x-axis and the y-axis gridlines. |
| `"x"`    | shows only the x-axis grid lines.               |
| `"y"`    | shows only the y-axis grid lines.               |

Again, `datachart` provides a [datachart.constants.SHOW_GRID](https://eriknovak.github.io/datachart/references/constants/#datachart.constants.SHOW_GRID) constant, which contains the supported options.

Related is the `aspect_ratio` attribute, which fixes the aspect ratio of the axes rather than of the figure: `"auto"` (the default) lets the axes fill the figure, `"equal"` keeps one data unit the same length on both axes. The supported values are in the [datachart.constants.ASPECT_RATIO](https://eriknovak.github.io/datachart/references/constants/#datachart.constants.ASPECT_RATIO) constant. Bar charts rarely need it, so the examples leave it at the default.

```
from datachart.constants import FIG_SIZE, SHOW_GRID
```

```
BarChart(
    data=sales_total,
    title="Monthly unit sales (2025)",
    xlabel="Month",
    ylabel="Units sold",
    # add to determine the figure size
    figsize=FIG_SIZE.FULL_SHORT,
    # add to show the grid lines
    show_grid=SHOW_GRID.Y,
).show()
```

### Bar style

To change the bar style, add the `style` attribute with the corresponding attributes. The supported attributes are shown in the [datachart.typings.BarStyleAttrs](https://eriknovak.github.io/datachart/references/typings/#datachart.typings.BarStyleAttrs) type, which contains the following attributes:

| Attribute                   | Description                                                                   |
| --------------------------- | ----------------------------------------------------------------------------- |
| `"plot_bar_color"`          | The color of the bar (hex color code).                                        |
| `"plot_bar_alpha"`          | The alpha of the bar (how visible the bar is).                                |
| `"plot_bar_width"`          | The width of the bar (as a fraction of the category width, `0.8` by default). |
| `"plot_bar_zorder"`         | The zorder of the bar.                                                        |
| `"plot_bar_hatch"`          | The hatch style of the bar.                                                   |
| `"plot_bar_edge_width"`     | The edge line width of the edge.                                              |
| `"plot_bar_edge_color"`     | The edge line color (hex color code).                                         |
| `"plot_bar_error_color"`    | The error line color (hex color code).                                        |
| `"plot_bar_value_fontsize"` | The font size of bar value labels.                                            |
| `"plot_bar_value_color"`    | The color of bar value labels (hex color code).                               |
| `"plot_bar_value_padding"`  | The padding between bar edge and value label.                                 |

Again, to help with the style settings, the [datachart.constants](https://eriknovak.github.io/datachart/references/constants/index.md) module contains the following constants:

| Constant                                                                                                                       | Description                 |
| ------------------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| [datachart.constants.HATCH_STYLE](https://eriknovak.github.io/datachart/references/constants/#datachart.constants.HATCH_STYLE) | The hatch style of the bar. |

The example below changes the color, alpha, width, hatch pattern and outline of the bars in one go. Any attribute you leave out keeps the value of the active theme.

```
from datachart.constants import HATCH_STYLE
```

```
BarChart(
    data=sales_total,
    # define the style of the bars
    style={
        "plot_bar_color": "#2a9d8f",
        "plot_bar_alpha": 0.8,
        "plot_bar_width": 0.6,
        "plot_bar_hatch": HATCH_STYLE.DIAGONAL,
        "plot_bar_edge_width": 1.0,
        "plot_bar_edge_color": "#264653",
    },
    title="Monthly unit sales (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Bar orientation

To change the orientation of the bars, add the `orientation` attribute, which supports the following values:

| Value          | Description              |
| -------------- | ------------------------ |
| `"horizontal"` | The bars are horizontal. |
| `"vertical"`   | The bars are vertical.   |

Again, to help with the style settings, the [datachart.constants](https://eriknovak.github.io/datachart/references/constants/index.md) module contains the following constants:

| Constant                                                                                                                       | Description                  |
| ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------- |
| [datachart.constants.ORIENTATION](https://eriknovak.github.io/datachart/references/constants/#datachart.constants.ORIENTATION) | The orientation of the bars. |

With horizontal bars the categories run along the y-axis, so swap the axis labels and the grid accordingly.

```
from datachart.constants import ORIENTATION
```

```
BarChart(
    data=sales_total,
    title="Monthly unit sales (2025)",
    # swap the axis labels to match the orientation
    xlabel="Units sold",
    ylabel="Month",
    figsize=FIG_SIZE.FULL_MEDIUM,
    # change the grid to match the change in orientation
    show_grid=SHOW_GRID.X,
    # change the orientation of the bars
    orientation=ORIENTATION.HORIZONTAL,
).show()
```

### Emphasis

When a chart carries several series, the story is often about one of them. The `emphasis` attribute expresses that directly: `"highlight"` bolds a series' edges and brings it to the front, `"background"` mutes a series (the theme's muted color at a lower alpha, drawn behind the others and left out of the legend), and `None` leaves a series unchanged. For multiple charts, `emphasis` is a list aligned with `data`, just like `subtitle` and `style`. The role strings are also available as the [datachart.constants.EMPHASIS](https://eriknovak.github.io/datachart/references/constants/#datachart.constants.EMPHASIS) constants.

The example highlights the Asia-Pacific region against the other two. See the [Highlighting](https://eriknovak.github.io/datachart/how-to-guides/styling/highlighting/index.md) guide for how emphasis works across all chart types and themes.

```
BarChart(
    data=sales_by_region,
    subtitle=REGIONS,
    # highlight one region, mute the rest
    emphasis=["background", "background", "highlight"],
    title="Monthly unit sales by region (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Reference lines

Reference lines mark a threshold or an event on the chart.

**Horizontal lines.** Use the `hlines` argument with the [datachart.typings.HLinePlotAttrs](https://eriknovak.github.io/datachart/references/typings/#datachart.typings.HLinePlotAttrs) typing, which is either a `dict` or a `List[dict]` where each dictionary contains some of the following attributes:

```
{
  "y":    Union[int, float],                 # The y-axis value
  "xmin": Optional[Union[int, float]],       # The minimum x-axis value  (values are bar indices, e.g. 0, 1, 2, etc.)
  "xmax": Optional[Union[int, float]],       # The maximum x-axis value  (values are bar indices, e.g. 0, 1, 2, etc.)
  "style": {                                 # The style of the line (optional)
    "plot_hline_color": Optional[str],       # The color of the line (hex color code)
    "plot_hline_style": Optional[LineStyle], # The line style (solid, dashed, etc.)
    "plot_hline_width": Optional[float],     # The width of the line
    "plot_hline_alpha": Optional[float],     # The alpha of the line (how visible the line is)
  },
  "label": Optional[str],                    # The label of the line (shown in the legend)
}
```

**Vertical lines.** Use the `vlines` argument with the [datachart.typings.VLinePlotAttrs](https://eriknovak.github.io/datachart/references/typings/#datachart.typings.VLinePlotAttrs) typing, which has the same shape with `x`, `ymin`, `ymax` and `plot_vline_*` style attributes. The `x` value is a bar index (`0`, `1`, `2`, …), so a line *between* two bars sits at a half-integer position.

The example marks the monthly sales goal with a dashed horizontal line and the July price cut with a vertical line between June and July. The line labels appear in the legend.

```
from datachart.constants import LINE_STYLE
```

```
BarChart(
    data=sales_total,
    # add a horizontal line at the sales goal
    hlines={
        "y": SALES_GOAL,
        "label": "monthly goal",
        "style": {
            "plot_hline_color": "#c1121f",
            "plot_hline_style": LINE_STYLE.DASHED,
            "plot_hline_width": 1.5,
        },
    },
    # add a vertical line between the June and July bars
    vlines={
        "x": 5.5,
        "label": "price cut",
        "style": {
            "plot_vline_color": "#555555",
            "plot_vline_style": LINE_STYLE.DOTTED,
            "plot_vline_width": 1.5,
        },
    },
    title="Monthly unit sales (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

## Multiple Bar Charts

To create multiple bar charts, pass a list of lists to the `data` argument. Each inner list represents the data for one chart. Per-chart attributes like `subtitle`, `style` and `emphasis` can be passed as lists, where each element corresponds to a chart.

Multiple charts pattern

For multiple charts, `data` becomes a list of lists, and per-chart attributes like `subtitle` and `style` become lists where each element applies to the corresponding chart.

The `sales_by_region` dataset is such a list of lists, one series per region. Series that share a label are grouped side by side.

```
BarChart(
    # use a list of lists to define multiple bar charts
    data=sales_by_region,
    title="Monthly unit sales by region (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Sub-chart subtitles

We can name each chart by passing a list of subtitles to the `subtitle` argument. In addition, to help with discerning which chart is which, use the `show_legend` argument to show the legend of the charts.

```
BarChart(
    data=sales_by_region,
    # add a subtitle to each chart
    subtitle=REGIONS,
    title="Monthly unit sales by region (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # show the legend
    show_legend=True,
).show()
```

### Bar mode

The `bar_mode` attribute controls how the series share the axis:

| Value       | Description                                                     |
| ----------- | --------------------------------------------------------------- |
| `"group"`   | The series are drawn side by side (default).                    |
| `"stack"`   | The series are stacked on top of each other.                    |
| `"overlay"` | The series are drawn on top of each other at the same position. |

Again, `datachart` provides a [datachart.constants.BAR_MODE](https://eriknovak.github.io/datachart/references/constants/#datachart.constants.BAR_MODE) constant, which contains the supported options.

Stacking the regions shows both the regional split and the company-wide total in one chart.

```
from datachart.constants import BAR_MODE
```

```
BarChart(
    data=sales_by_region,
    subtitle=REGIONS,
    # stack the series
    bar_mode=BAR_MODE.STACK,
    title="Monthly unit sales by region (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Subplots

To draw each chart in its own subplot, add the `subplots` attribute. The chart's `subtitle` are then added at the top of each subplot, while the `title`, `xlabel` and `ylabel` are positioned to be global for all charts. The `max_cols` attribute limits the number of subplots per row.

```
BarChart(
    data=sales_by_region,
    subtitle=REGIONS,
    title="Monthly unit sales by region (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
    # show each chart in its own subplot
    subplots=True,
    # at most two subplots per row
    max_cols=2,
).show()
```

### Sharing the x-axis and/or y-axis across subplots

To share the x-axis and/or y-axis across subplots, add the `sharex` and/or `sharey` attributes, which are boolean values that specify whether to share the axis across all subplots. With a shared y-axis, the regions become directly comparable.

```
BarChart(
    data=sales_by_region,
    subtitle=REGIONS,
    title="Monthly unit sales by region (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
    subplots=True,
    max_cols=2,
    # share the x-axis across subplots
    sharex=True,
    # share the y-axis across subplots
    sharey=True,
).show()
```

### Subplot orientation

The `orientation` attribute can be used to change the orientation of all subplots.

```
BarChart(
    data=sales_by_region,
    subtitle=REGIONS,
    title="Monthly unit sales by region (2025)",
    xlabel="Units sold",
    ylabel="Month",
    figsize=FIG_SIZE.FULL_TALL,
    subplots=True,
    max_cols=2,
    sharex=True,
    sharey=True,
    # change the grid to match the change in orientation
    show_grid=SHOW_GRID.X,
    # change the orientation of the bars
    orientation=ORIENTATION.HORIZONTAL,
).show()
```

## Additional Features

### Error bars

To add error bars, first define the `yerr` value of each data point in `data`, then add the `show_yerr` attribute. The `sales_by_region` data points carry the standard deviation of daily sales as `yerr`. The color of the error lines is set with the `plot_bar_error_color` style attribute.

```
BarChart(
    data=sales_by_region,
    subtitle=REGIONS,
    # set the error bar color (a single style applies to every chart)
    style={"plot_bar_error_color": "#000000"},
    title="Monthly unit sales by region (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
    subplots=True,
    max_cols=2,
    sharex=True,
    sharey=True,
    # show the error bars
    show_yerr=True,
    # make sure the y-axis starts at 0
    ymin=0,
).show()
```

### Bar value labels

To display the actual value at the edge of each bar, use the `show_values` parameter. The `value_format` parameter controls how the values are formatted. It accepts a Python format string in which the value is named `x` (e.g., `"{x:.1f}"` for one decimal place, `"{x:.0%}"` to show a fraction as a percentage) — the [datachart.constants.VALUE_FORMAT](https://eriknovak.github.io/datachart/references/constants/#datachart.constants.VALUE_FORMAT) constant collects the common ones:

| Constant                  | Format       | Description                                                                 |
| ------------------------- | ------------ | --------------------------------------------------------------------------- |
| `VALUE_FORMAT.DEFAULT`    | `"{x}"`      | The value as is.                                                            |
| `VALUE_FORMAT.INTEGER`    | `"{x:.0f}"`  | Rounded to an integer.                                                      |
| `VALUE_FORMAT.DECIMAL`    | `"{x:.1f}"`  | One decimal place (`DECIMAL_2` and `DECIMAL_3` for two and three).          |
| `VALUE_FORMAT.PERCENT`    | `"{x:.1%}"`  | A fraction as a percentage with one decimal place (`PERCENT_INT` for none). |
| `VALUE_FORMAT.SCIENTIFIC` | `"{x:.2e}"`  | Scientific notation.                                                        |
| `VALUE_FORMAT.THOUSANDS`  | `"{x:,.0f}"` | With a thousands separator.                                                 |

Positional format strings (`"{:.1f}%"`) and printf-style ones (`"%g"`) work too, which is handy when the value already is a percentage.

```
from datachart.constants import VALUE_FORMAT
```

```
BarChart(
    data=sales_total,
    title="Monthly unit sales (2025)",
    xlabel="Month",
    ylabel="Units sold",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    ymin=0,
    ymax=2000,
    # show bar value labels
    show_values=True,
    # format the values with a thousands separator
    value_format=VALUE_FORMAT.THOUSANDS,
).show()
```

Bar value labels also work with horizontal bar charts. You can customize the label appearance using style attributes like `plot_bar_value_fontsize`, `plot_bar_value_color`, and `plot_bar_value_padding`.

```
BarChart(
    data=sales_total,
    style={
        "plot_bar_value_fontsize": 9,
        "plot_bar_value_color": "#333333",
        "plot_bar_value_padding": 5,
    },
    title="Monthly unit sales (2025)",
    xlabel="Units sold",
    ylabel="Month",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.X,
    xmin=0,
    xmax=2000,
    # horizontal orientation
    orientation=ORIENTATION.HORIZONTAL,
    # show bar value labels
    show_values=True,
    value_format=VALUE_FORMAT.INTEGER,
).show()
```

### Axis scales

The user can change the axis scale using the `scaley` attribute (`scalex` for horizontal bars). The supported scale options are:

| Options    | Description              |
| ---------- | ------------------------ |
| `"linear"` | The linear scale.        |
| `"log"`    | The log scale.           |
| `"symlog"` | The symmetric log scale. |
| `"asinh"`  | The asinh scale.         |

Again, to help with the options settings, the [datachart.constants](https://eriknovak.github.io/datachart/references/constants/index.md) module contains the following constants:

| Constant                                                                                                           | Description       |
| ------------------------------------------------------------------------------------------------------------------ | ----------------- |
| [datachart.constants.SCALE](https://eriknovak.github.io/datachart/references/constants/#datachart.constants.SCALE) | The axis options. |

A logarithmic scale pays off when the values span several orders of magnitude. The hidden cell below defines `populations`, the approximate mid-2024 populations of seven countries in thousands (UN World Population Prospects 2024, rounded) — from about 1.45 billion down to about 10 thousand.

```
from datachart.constants import SCALE
```

On a linear scale the small countries vanish; on a log scale every bar is readable.

```
for scale in [SCALE.LINEAR, SCALE.LOG]:
    figure = BarChart(
        data=populations,
        title=f"Population on the '{scale}' scale",
        xlabel="Country",
        ylabel="Population (thousands)",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
        # set the scale of the y axis
        scaley=scale,
    )
    figure.show()
```

## Saving the Chart as an Image

To save the chart as an image, use the [datachart.utils.save_figure](https://eriknovak.github.io/datachart/references/utils#datachart.utils.save_figure) function.

```
from datachart.utils import save_figure
```

```
save_figure(figure, "./fig_bar_chart.png", dpi=300)
```

The figure should be saved in the current working directory.

## Real-World Examples

The following examples put the features above to work on real or realistic data. Each one states what its data is and where it comes from; the data itself lives in a hidden cell.

### Example 1: Olympic Medal Table (Grouped Bars with Legend)

`medals` holds the gold, silver and bronze medal counts of the six countries that topped the Paris 2024 Olympic medal table (ranked by gold medals; source: the official Paris 2024 medal table). One series per medal type gives a grouped bar chart, colored to match the metals.

```
BarChart(
    data=medals,
    subtitle=["Gold", "Silver", "Bronze"],
    style=[
        {"plot_bar_color": "#d4af37"},  # gold
        {"plot_bar_color": "#a8a9ad"},  # silver
        {"plot_bar_color": "#cd7f32"},  # bronze
    ],
    title="Paris 2024 Olympic medal table",
    xlabel="Country",
    ylabel="Medals",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    ymin=0,
).show()
```

### Example 2: Quarterly Revenue by Region (Emphasis)

`revenue` holds the illustrative quarterly revenue (in million USD) of a company across four sales regions over eight quarters, 2024–2025. The question is how the fastest-growing region compares with the rest, so `emphasis` highlights it and mutes the other three. Muted regions drop out of the legend automatically.

```
BarChart(
    data=revenue,
    subtitle=list(REVENUE),
    # highlight Asia-Pacific, mute the other regions
    emphasis=["background", "background", "highlight", "background"],
    title="Quarterly revenue by region",
    xlabel="Quarter",
    ylabel="Revenue (million USD)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    ymin=0,
).show()
```

### Example 3: Survey Results (Horizontal Bars with Value Labels)

`languages` holds the share of respondents who worked with each programming language in the past year, for the ten most-used languages in the Stack Overflow Developer Survey 2024 (all respondents). Horizontal bars keep the long labels readable, and value labels print the exact share on each bar — the values already are percentages, so a positional `"{:.1f}%"` format appends the sign instead of `VALUE_FORMAT.PERCENT` (which would multiply by 100). The data is ordered from least to most used so the most-used language ends up at the top.

```
BarChart(
    data=languages,
    style={
        "plot_bar_color": "#f48024",
        "plot_bar_value_fontsize": 9,
        "plot_bar_value_padding": 4,
    },
    title="Most used programming languages, 2024",
    xlabel="Share of respondents",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.X,
    orientation=ORIENTATION.HORIZONTAL,
    xmin=0,
    xmax=75,
    show_values=True,
    value_format="{:.1f}%",
).show()
```

### Example 4: Monthly Trade Balance (Diverging Bars)

`trade_balance` holds two years of illustrative monthly trade balance figures (exports minus imports, in billion EUR) — a run of deficits in the first year turning into surpluses in the second. Since `BarChart` applies a single color per series, the data is split into a positive and a negative series (see the tip below).

```
BarChart(
    data=trade_balance,
    style=[
        {"plot_bar_color": "#2a9d8f"},  # surplus
        {"plot_bar_color": "#e76f51"},  # deficit
    ],
    # draw both series at the same positions
    bar_mode=BAR_MODE.OVERLAY,
    # mark the zero line
    hlines={
        "y": 0,
        "style": {
            "plot_hline_color": "black",
            "plot_hline_style": LINE_STYLE.SOLID,
            "plot_hline_width": 1,
        },
    },
    title="Monthly trade balance",
    ylabel="Billion EUR",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    xtickrotate=90,
).show()
```

Tip: Diverging Bar Charts

Each month is zero in one of the two series (positive values in one, negative in the other). Drawing them with `bar_mode=BAR_MODE.OVERLAY` puts both series at the same x-positions, so only one bar is visible per month — the visual effect of a single diverging bar chart with two colors.
