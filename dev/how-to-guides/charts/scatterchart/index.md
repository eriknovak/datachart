# Scatter Chart

A scatter chart places each observation by two numeric values, so it answers *do these two quantities move together, and which points break the pattern*. This guide shows how to create scatter charts with the [datachart.charts.ScatterChart](https://eriknovak.github.io/datachart/dev/references/charts/scatterchart/#datachart.charts.ScatterChart) function, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-scatter-chart), which maps common tasks to the parameter or style attribute that does the job.

```
from datachart.charts import ScatterChart
```

## Basics

The examples in this guide share one dataset: the GDP per capita and the life expectancy at birth of 49 countries in 2019, the last year before the COVID-19 pandemic. GDP per capita is in current US dollars, rounded to the nearest hundred, and population is in millions (source: World Bank, World Development Indicators); life expectancy is in years for both sexes, and the region is the country's WHO region (source: WHO Global Health Observatory). The data lives in a hidden cell. `countries` holds one data point per country, with the GDP per capita as `x`, the life expectancy as `y`, and the `country`, `region` and `population` as extra keys; `countries_by_region` holds one list per WHO region, in the order of `REGIONS`. The pattern is well known, richer countries live longer, and the interesting part is the countries that break it.

Each data point is a dictionary with an `x` and a `y` value; the other keys are ignored until a parameter asks for them:

```
countries[:3]
```

**Basic example.** Only the `data` argument is required. Even without labels the shape is visible: life expectancy climbs steeply at low incomes and flattens out above them:

```
ScatterChart(
    # add the data to the chart
    data=countries
).show()
```

## Customizing the Scatter Chart

Every customization is either a keyword argument of `ScatterChart` or a `plot_scatter_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                    | Use                                                             | See                                                                                                     |
| --------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| add a title and axis labels                   | `title`, `xlabel`, `ylabel`                                     | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                            |
| set the tick positions and labels             | `xticks`, `xticklabels`, `yticks`, `yticklabels`                | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                            |
| format or rotate the tick labels              | `xticks_format`, `yticks_format`, `xtickrotate`, `ytickrotate`  | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                            |
| fix the axis range                            | `xmin`, `xmax`, `ymin`, `ymax`                                  | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                            |
| resize the figure                             | `figsize`                                                       | [Figure size and grid](#figure-size-and-grid)                                                           |
| show grid lines                               | `show_grid`                                                     | [Figure size and grid](#figure-size-and-grid)                                                           |
| change the marker color, shape, size, or edge | `style={"plot_scatter_color": ..., "plot_scatter_marker": ...}` | [Scatter style](#scatter-style)                                                                         |
| color the points by a category                | `hue`, `show_legend`                                            | [Hue grouping](#hue-grouping)                                                                           |
| scale the markers by a third value            | `size`, `size_range`                                            | [Bubble chart](#bubble-chart)                                                                           |
| name some or all of the points                | `annotation`, the `"annotation"` key of a data point            | [Point annotations](#point-annotations)                                                                 |
| print the value beside each point             | `show_values`, `value_format`, `value_step`                     | [Value labels](#value-labels)                                                                           |
| show the uncertainty of each point            | `xerr`, `yerr`, `show_xerr`, `show_yerr`                        | [Error bars](#error-bars)                                                                               |
| fit a trend line and measure the correlation  | `show_regression`, `show_ci`, `ci_level`, `show_correlation`    | [Regression line](#regression-line)                                                                     |
| keep one unit the same length on both axes    | `aspect_ratio`                                                  | [Aspect ratio](#aspect-ratio)                                                                           |
| highlight some series, mute the rest          | `emphasis`, `emphasis_rule`                                     | [Emphasis](#emphasis)                                                                                   |
| mark a threshold or a reference value         | `hlines`, `vlines`, `dlines`                                    | [Reference lines and bands](#reference-lines-and-bands)                                                 |
| shade a range of values                       | `hspans`, `vspans`                                              | [Reference lines and bands](#reference-lines-and-bands)                                                 |
| put a note on the chart                       | `texts`                                                         | [Text annotations](#text-annotations)                                                                   |
| compare several series in one chart           | `data` as a list of lists, `subtitle`, `show_legend`            | [Multiple Scatter Charts](#multiple-scatter-charts)                                                     |
| title and place the legend                    | `legend`                                                        | [Legend](#legend)                                                                                       |
| draw each series in its own subplot           | `subplots`, `sharex`, `sharey`, `max_cols`                      | [Subplots](#subplots)                                                                                   |
| use a logarithmic axis                        | `scalex`, `scaley`                                              | [Axis scales](#axis-scales)                                                                             |
| plot dates on the x-axis                      | `date` or `datetime` values as `x`, `xticks_format`             | [Datetime axis](#datetime-axis)                                                                         |
| plot data with other key names                | `x`, `y`, `size`, `hue`, `annotation`                           | [Custom data keys](#custom-data-keys)                                                                   |
| save the chart to a file                      | `save_figure`                                                   | [Saving Figures](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/saving/index.md) guide |

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values:

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                   |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                           |
| `scalex`                                     | [`AXIS_SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.AXIS_SCALE)                                                                                                                               |
| `scaley`                                     | [`AXIS_SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.AXIS_SCALE)                                                                                                                               |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |

The full list of style attributes is in the [datachart.typings.ScatterStyleAttrs](https://eriknovak.github.io/datachart/dev/references/charts/scatterchart/#datachart.typings.ScatterStyleAttrs) type; the full list of parameters is in the [datachart.charts.ScatterChart](https://eriknovak.github.io/datachart/dev/references/charts/scatterchart/#datachart.charts.ScatterChart) reference.

### Title, axis labels and ticks

A chart without a title and axis labels leaves the reader guessing what the axes measure; `title`, `xlabel` and `ylabel` say it. GDP per capita runs from about 500 to 86,000 dollars, and on a linear axis the poorer half of the countries piles up against the left edge. `scalex=AXIS_SCALE.LOG` ([AXIS_SCALE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.AXIS_SCALE)) spreads them out, so the examples below use it; the [Axis scales](#axis-scales) section compares the two. A log axis labels its ticks as powers of ten, so `xticks` places a tick at 1,000, 10,000 and 100,000 dollars and `xticklabels` names them. `xticks_format` (and `yticks_format`) is the alternative when the labels follow a pattern: a [VALUE_FORMAT](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT) member or a `"{x:,.0f}"` style string. `xtickrotate` and `ytickrotate` tilt crowded labels, and `xmin`, `xmax`, `ymin` and `ymax` fix the axis range.

```
from datachart.constants import AXIS_SCALE

GDP_TICKS = [1_000, 10_000, 100_000]
GDP_TICK_LABELS = ["$1k", "$10k", "$100k"]

ScatterChart(
    data=countries,
    # add the title
    title="Life expectancy and income, 2019",
    # add the x and y axis labels
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    # a logarithmic income axis
    scalex=AXIS_SCALE.LOG,
    # one labeled tick per power of ten
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    # fix the y-axis range
    ymin=55,
    ymax=90,
).show()
```

### Figure size and grid

The default figure is 6.4 by 4.8 inches, a little wider than the text column of an A4 page. `figsize` takes a `(width, height)` tuple in inches or one of the presets in [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE), sized for a full or half page width; `FIG_SIZE.FULL_MEDIUM` fits the full width. The default grid draws only horizontal lines, but a scatter chart has no baseline to read from, so grid lines in both directions help the eye carry a point to either axis: `show_grid=SHOW_GRID.BOTH` ([SHOW_GRID](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)); `SHOW_GRID.X` and `SHOW_GRID.Y` draw one set only.

```
from datachart.constants import FIG_SIZE, SHOW_GRID

ScatterChart(
    data=countries,
    title="Life expectancy and income, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    # a figure as wide as the page
    figsize=FIG_SIZE.FULL_MEDIUM,
    # grid lines in both directions
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Scatter style

The `style` dictionary sets the look of the markers: the color and alpha, the size (the marker area in points squared), the shape from [LINE_MARKER](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LINE_MARKER), and the edge; the attributes are listed in [datachart.typings.ScatterStyleAttrs](https://eriknovak.github.io/datachart/dev/references/charts/scatterchart/#datachart.typings.ScatterStyleAttrs), and any attribute left out keeps the value of the active theme. Where points overlap, as in the crowded top right corner of this chart, a lower alpha and a thin dark edge keep each marker visible.

```
from datachart.constants import LINE_MARKER

ScatterChart(
    data=countries,
    # translucent diamonds with a thin dark edge
    style={
        "plot_scatter_color": "#e76f51",
        "plot_scatter_alpha": 0.7,
        "plot_scatter_size": 60,
        "plot_scatter_marker": LINE_MARKER.DIAMOND,
        "plot_scatter_edge_width": 0.8,
        "plot_scatter_edge_color": "#1d3557",
    },
    title="Life expectancy and income, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Hue grouping

Is the pattern the same everywhere, or do regions sit apart? `hue` names the key that holds a category, here the `region` of each country; each category gets its own color from the theme's palette and its own legend entry, which `show_legend` shows. The colors show that the bottom left corner, low income and short lives, is mostly African, while Europe and the Western Pacific share the top right.

```
ScatterChart(
    data=countries,
    # color the points by WHO region
    hue="region",
    title="Life expectancy and income, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    # name the regions
    show_legend=True,
).show()
```

### Bubble chart

A point for China and a point for Slovenia look the same, though one stands for 700 times as many people. `size` names the key whose value scales the marker, here `population`, which turns the chart into a bubble chart. The values map linearly onto the marker areas in `size_range` (the default is `(20, 200)`): the smallest value gets the smallest marker, the largest the largest. With populations from 1.7 million to 1.4 billion, a wide range keeps the difference visible, and a low alpha with an edge keeps overlapping bubbles readable. The two largest bubbles, China and India, show that most of the people in this chart live in the middle of the income range.

`hue` and `size` combine, but the sizes are scaled within each hue group, so the largest country of every region would get the largest bubble; for sizes that compare across the whole chart, keep the points in one group.

```
ScatterChart(
    data=countries,
    # scale the markers by population
    size="population",
    # a wide range of marker areas
    size_range=(10, 1500),
    style={
        "plot_scatter_alpha": 0.5,
        "plot_scatter_edge_width": 0.6,
        "plot_scatter_edge_color": "#1d3557",
    },
    title="Life expectancy and income, sized by population, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Point annotations

A scatter chart invites the question *which one is that?* `annotation` names the key that holds each point's annotation, here `country`. Each annotation is placed beside its marker at the spot with the least overlap with the other markers, the annotations already placed, and the axes edge, so a chart of a dozen points stays readable without hand-placed notes; the annotations use the `plot_text_*` font of the theme. The Americas alone show the spread within one region, from Haiti to the United States.

```
americas = [point for point in countries if point["region"] == "Americas"]

ScatterChart(
    data=americas,
    # name each point after its country
    annotation="country",
    title="Life expectancy and income in the Americas, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

Fifty annotations would bury the chart, so annotate only the points the reader needs. Points without the annotation key stay unannotated, and `"annotation"` is the default key, so adding it to a few records is enough. Here it names the five most populous countries in the chart:

```
most_populous = sorted(countries, key=lambda point: point["population"])[-5:]
most_populous_names = {point["country"] for point in most_populous}

populous_marked = [
    {**point, "annotation": point["country"]} if point["country"] in most_populous_names else point
    for point in countries
]

ScatterChart(
    # only the five most populous countries carry an "annotation" key
    data=populous_marked,
    hue="region",
    title="Life expectancy and income, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

### Value labels

When the exact values matter more than the names, `show_values` prints each point's `y` value beside it, placed like the point labels. `value_format` formats it: a [VALUE_FORMAT](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT) member or any `"{x:.1f}"`, `"{:.1f}%"` or `"%g"` style string. On a crowded chart the default prints only every Nth value, choosing the step that keeps neighboring labels apart; `value_step` sets the step, and `1` prints them all. A point carries either its name or its value, so combining `label` with `show_values` raises a `ValueError`.

```
ScatterChart(
    data=americas,
    # print the life expectancy beside every point
    show_values=True,
    value_format="{x:.1f}",
    value_step=1,
    title="Life expectancy and income in the Americas, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Error bars

A point drawn on its own claims the measurement is exact. When it is a mean over runs, an estimate from a sample, or anything else with a margin, the reader cannot tell a real gap between two points from the noise. `xerr` and `yerr` name the keys that hold that margin, and every point carrying one gets a bar, drawn in the point's own color. Each bar starts at the edge of its marker, so a translucent or a large marker stays clean.

A value is a *distance* from the point, not a bound: one number reaches the same distance both ways, so a margin of 0.6 points is `0.6`, and a point without the key draws no bar. `benchmarks`, defined in a hidden cell, holds eight illustrative model checkpoints, each evaluated five times on one test set: `x` is the median inference latency in milliseconds and `xerr` its spread across the runs, `y` the mean accuracy in percent and `yerr` the standard error of that mean. Both are the default key names, so the bars need no argument at all.

```
ScatterChart(
    # every point carries an "xerr" and a "yerr" key
    data=benchmarks,
    title="Accuracy and latency of eight checkpoints",
    xlabel="Inference latency (ms)",
    ylabel="Accuracy (%)",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

An interval that is not symmetric about the point is a `[low, high]` pair, again as distances: `low` reaches below the point and `high` above it. A bootstrap interval of the same evaluations is such a pair, stored here under `accuracy_ci`, which `yerr` names; `show_xerr=False` drops the latency bars so the comparison is only about accuracy. The look of the bars is styleable: `plot_scatter_error_width` sets their thickness, `plot_scatter_error_capsize` the half-width of the cap at each end (`0` draws none), and `plot_scatter_error_color` pins one color for all of them, where the default follows each point.

```
ScatterChart(
    data=benchmarks,
    # the bootstrap interval: a low and a high distance from the mean
    yerr="accuracy_ci",
    # the latency bars stay out of this one
    show_xerr=False,
    style={"plot_scatter_error_width": 1.5, "plot_scatter_error_capsize": 4},
    title="Accuracy of eight checkpoints, with bootstrap intervals",
    xlabel="Inference latency (ms)",
    ylabel="Accuracy (%)",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Regression line

How strong is the link, and what does it predict? `show_regression` fits a straight line through the points by least squares, `show_ci` shades the confidence band of that line and `ci_level` sets its level (the default is 0.95), and `show_correlation` prints the Pearson correlation coefficient `r` in the top left corner. With `hue`, one line is fitted to all groups together.

The line is fitted to the values as they are in the data, whatever the axis scale, so on a log axis it would be a straight-line fit to raw dollars. Life expectancy grows with the *order of magnitude* of income, so the example plots `log10` of the GDP per capita and labels the ticks with the dollar amounts they stand for. The fit is tight, and the countries far below the band are the ones worth a closer look.

```
import math

countries_log_gdp = [{**point, "x": math.log10(point["x"])} for point in countries]

ScatterChart(
    data=countries_log_gdp,
    # fit a straight line through the points
    show_regression=True,
    # shade its 95% confidence band
    show_ci=True,
    ci_level=0.95,
    # print the correlation coefficient
    show_correlation=True,
    title="Life expectancy and income, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    # the x values are log10(GDP); label them with the dollar amounts
    xticks=[3, 4, 5],
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Aspect ratio

Dollars and years have nothing in common, so the axes of the charts above can stretch freely. When both axes share a unit (coordinates, distances, a prediction against a measurement), stretching distorts the picture. `aspect_ratio=ASPECT_RATIO.EQUAL` ([ASPECT_RATIO](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)) keeps one data unit the same length on both axes, while the default `ASPECT_RATIO.AUTO` lets the axes fill the figure. `cities`, defined in a hidden cell, holds the longitude and latitude of 16 European capitals, rounded to two decimals; with an equal aspect ratio they draw a recognizable map (a plain longitude-latitude grid, without a map projection).

```
from datachart.constants import ASPECT_RATIO

ScatterChart(
    data=cities,
    annotation="city",
    title="European capitals",
    xlabel="Longitude (°E)",
    ylabel="Latitude (°N)",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    # one degree is the same length on both axes
    aspect_ratio=ASPECT_RATIO.EQUAL,
).show()
```

### Emphasis

A chart usually makes one point, and emphasis makes it visible. With the data split into several series (the [Multiple Scatter Charts](#multiple-scatter-charts) section covers the list-of-lists form), `emphasis` takes one role per series: `"highlight"` gives the markers a contrasting edge and brings them to the front, `"background"` mutes a series (the theme's muted color at a lower alpha, behind the others, without a legend entry), and `None` leaves it as it is. The roles are also available as the [EMPHASIS](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS) constants, and the [Highlighting](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/highlighting/index.md) guide covers emphasis across every chart type and theme.

`annotation` also takes one entry per series, with `None` for a series left unannotated, so highlighting and naming go together. Which countries break the pattern? Four sit well below the trend (Nigeria, South Africa, Equatorial Guinea, and the United States among the rich), and three well above it (Cuba, Costa Rica and Sri Lanka).

```
OUTLIERS = {"Nigeria", "South Africa", "Equatorial Guinea", "United States", "Cuba", "Costa Rica", "Sri Lanka"}
outliers = [point for point in countries if point["country"] in OUTLIERS]
others = [point for point in countries if point["country"] not in OUTLIERS]

ScatterChart(
    data=[others, outliers],
    subtitle=["other countries", "far from the trend"],
    # mute the rest, highlight the outliers
    emphasis=["background", "highlight"],
    # name the outliers only
    annotation=[None, "country"],
    title="Countries that break the pattern, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

`emphasis_rule` picks the series from the data instead. It is a one-key dictionary read against a summary of each series's `y` values: `{"above": v}` or `{"below": v}` (strict), `{"between": (lo, hi)}` (inclusive), or `{"top": n}` or `{"bottom": n}` by rank. The summary is the mean by default; a `"by"` key picks `"median"`, `"min"`, `"max"` or `"sum"` instead. The series that match are highlighted and the rest muted, and an explicit `emphasis` role wins over the rule. Asking which regions have a country with a life expectancy below 65 years is `{"below": 65, "by": "min"}`, and the answer is three regions, not only Africa:

```
ScatterChart(
    data=countries_by_region,
    subtitle=REGIONS,
    # highlight the regions whose lowest life expectancy is below 65
    emphasis_rule={"below": 65, "by": "min"},
    title="Regions with a life expectancy below 65 years, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

### Reference lines and bands

Is a country above or below the world as a whole? Reference lines answer by marking a value: `hlines` draws a horizontal line at a `y` value and `vlines` a vertical one at an `x` value. `hspans` and `vspans` shade a range instead; a band needs at least one bound, and a missing bound runs to the axis edge. Each takes a dictionary or a list of them, with the position, an optional `label` for the legend and a `style`; the keys are listed in [HLineSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineSettingAttrs), [VLineSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineSettingAttrs), [HSpanSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanSettingAttrs) and [VSpanSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanSettingAttrs), and the line patterns in [LINE_STYLE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LINE_STYLE). The lines below split the chart into quadrants: the world life expectancy in 2019 (73.1 years, WHO) and the median GDP per capita of the countries shown.

`dlines` completes the trio. Where `vlines` fixes an x and `hlines` a y, a diagonal is fixed by a `slope` and an `intercept`, so it runs through the data space instead of across it; `dlines={}` on its own draws the parity line `y = x`. It spans the axes unless `xmin` and `xmax` clip it to a segment, and takes the same optional `label` and `style`; the keys are listed in [DLineSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineSettingAttrs). The line is straight in data coordinates, which means straight on a linear axis only: on a logarithmic one it draws as a curve. The chart above uses a logarithmic income axis for that reason; this one drops it and keeps to the poorest countries, where the diagonal reads as what it is — the years of life a thousand dollars buys at the bottom of the income scale. Above it the gain flattens, which is why the full range wants the log axis.

```
from statistics import median

from datachart.constants import LINE_STYLE

median_gdp = median(point["x"] for point in countries)

ScatterChart(
    data=countries,
    hue="region",
    # the world life expectancy
    hlines={
        "y": WORLD_LIFE_EXPECTANCY,
        "label": "world life expectancy",
        "style": {"plot_hline_color": "#1d3557", "plot_hline_style": LINE_STYLE.DASHED},
    },
    # the median income of the countries shown
    vlines={
        "x": median_gdp,
        "label": "median GDP per capita",
        "style": {"plot_vline_color": "#9d0208", "plot_vline_style": LINE_STYLE.DOTTED},
    },
    title="Life expectancy and income, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    # a fixed income range, so the horizontal line spans it
    xmin=400,
    xmax=100_000,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

```
POOREST = 10_000
poorest = [point for point in countries if point["x"] <= POOREST]
lowest = min(poorest, key=lambda point: point["x"])
highest = max(poorest, key=lambda point: point["x"])
# years of life expectancy per dollar, across the poorest countries
per_dollar = (highest["y"] - lowest["y"]) / (highest["x"] - lowest["x"])

ScatterChart(
    data=poorest,
    hue="region",
    # the gradient across the bottom of the income scale
    dlines={
        "slope": per_dollar,
        "intercept": lowest["y"] - per_dollar * lowest["x"],
        "label": f"{per_dollar * 1000:.1f} years per $1,000",
        "style": {"plot_dline_color": "#1d3557", "plot_dline_style": LINE_STYLE.DASHED},
    },
    title="Life expectancy and income below $10,000 per head, 2019",
    xlabel="GDP per capita (USD)",
    ylabel="Life expectancy (years)",
    xmin=0,
    xmax=POOREST,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

Bands work the same way. The chart below shades the countries with a life expectancy of 80 years or more, a band with no upper bound, and those with a GDP per capita under 1,000 dollars, a band with no lower bound. Costa Rica and Chile make it into the top band on a fraction of the income of the other countries in it.

```
ScatterChart(
    data=countries,
    hue="region",
    # no upper bound: the band runs to the top edge
    hspans={"ymin": 80, "label": "80 years or more"},
    # no lower bound: the band runs to the left edge
    vspans={
        "xmax": 1_000,
        "label": "under $1,000 per person",
        "style": {"plot_vspan_color": "#e9c46a"},
    },
    title="Life expectancy and income, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

### Text annotations

Where a label names a point, a note explains it. `texts` places text on the chart, with an optional `target` to draw a connector to a data point; the position is in data coordinates by default, or in axes fractions with `"coords": "axes"`, which keeps the note in place whatever the axis range and scale. The [Text Annotations](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/annotations/index.md) guide covers placement, connector looks and styling. The note below points at the United States, the richest large country in the chart and one of the shortest-lived among the rich.

```
US_GDP, US_LIFE = COUNTRIES["United States"][1:3]

ScatterChart(
    data=countries,
    # a note pinned to the axes, pointing at the United States
    texts={
        "text": "United States: $65k per person,\nyet shorter lives than Chile",
        "x": 0.6,
        "y": 0.2,
        "coords": "axes",
        "target": (US_GDP, US_LIFE),
    },
    title="Life expectancy and income, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

## Multiple Scatter Charts

To compare several groups as separate series, pass a list of lists to `data`: each inner list is one series, and the per-series attributes (`subtitle`, `style`, `emphasis`, `label`, and the data keys) become lists aligned with it. `subtitle` names each series and `show_legend` lists them. `countries_by_region` is such a list, one series per WHO region. Unlike `hue`, which colors the groups of one series, separate series take separate styles: a list of `style` dictionaries gives each region its own marker shape, which keeps the groups apart in greyscale too (`None` in the list keeps the theme style for a series).

```
REGION_MARKERS = [
    {"plot_scatter_marker": marker}
    for marker in [
        LINE_MARKER.CIRCLE,
        LINE_MARKER.SQUARE,
        LINE_MARKER.TRIANGLE,
        LINE_MARKER.DIAMOND,
        LINE_MARKER.PENTAGON,
        LINE_MARKER.HEXAGON,
    ]
]

ScatterChart(
    # one series per region
    data=countries_by_region,
    # named for the legend
    subtitle=REGIONS,
    # one marker shape per region
    style=REGION_MARKERS,
    title="Life expectancy and income by WHO region, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

### Legend

`show_legend` lists the series; `legend` says where and how, with a `title`, a `location` from [LEGEND_LOCATION](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), the number of columns `ncols`, and the `alignment` of the entries from [LEGEND_ALIGN](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN); a field left out falls back to the theme ([LegendSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.LegendSettingAttrs)). No country in the chart is rich and short-lived, so the bottom right corner is empty and holds the legend without covering a point.

```
from datachart.constants import LEGEND_LOCATION

ScatterChart(
    data=countries_by_region,
    subtitle=REGIONS,
    style=REGION_MARKERS,
    title="Life expectancy and income by WHO region, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
    # a titled legend in the empty corner
    legend={"title": "WHO region", "location": LEGEND_LOCATION.LOWER_RIGHT},
).show()
```

### Subplots

Six overlapping groups are hard to tell apart, however they are styled. `subplots=True` draws each series in its own panel: `subtitle` titles the panels, `title`, `xlabel` and `ylabel` stay global, and `max_cols` limits the panels per row. `sharex=True` and `sharey=True` put every panel on the same axes, so a position means the same in each panel; without them each panel zooms to its own points, and the African countries would fill their panel just like the European ones.

```
ScatterChart(
    data=countries_by_region,
    subtitle=REGIONS,
    title="Life expectancy and income by WHO region, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    # one panel per region, three per row
    subplots=True,
    max_cols=3,
    # the same axes in every panel
    sharex=True,
    sharey=True,
    # a y range that holds every region
    ymin=55,
    ymax=90,
).show()
```

## Additional Features

### Axis scales

A linear axis suits values of one order of magnitude; values that span several read better on a logarithmic one, where equal distances stand for equal ratios. `scalex` and `scaley` take a [AXIS_SCALE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.AXIS_SCALE) member: `AXIS_SCALE.LINEAR` (the default), `AXIS_SCALE.LOG`, and `AXIS_SCALE.SYMLOG` and `AXIS_SCALE.ASINH` for data that also crosses zero. On the linear scale the countries under 10,000 dollars crowd into the left edge and the relationship looks like a sharp bend; on the log scale they spread out and the relationship is close to a straight line.

```
for scale in [AXIS_SCALE.LINEAR, AXIS_SCALE.LOG]:
    ScatterChart(
        data=countries,
        title=f"Life expectancy and income on the '{scale}' scale",
        xlabel="GDP per capita (USD)",
        ylabel="Life expectancy (years)",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.BOTH,
        # the scale of the income axis
        scalex=scale,
    ).show()
```

### Datetime axis

When `x` is a date, the question becomes how a value changes over time, and whether the change is steady. An `x` value that is a real temporal object (`datetime`, `date`, `numpy.datetime64` or a pandas `Timestamp`) puts the chart on a time axis: points sit at their elapsed time, and the ticks choose concise labels for the visible span; date strings are not parsed. `xticks_format` takes a [DATE_FORMAT](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT) member or any `strftime` pattern, and explicit `xticks`, `xmin` and `xmax`, reference lines and bands take dates as well. `records`, defined in a hidden cell, holds the progression of the men's marathon world record since 2003: the date of each record race, the finishing time in minutes, and the record holder as the label (source: World Athletics). The regression line shows a steady pace, about 13 seconds off the record per year.

```
from datachart.constants import DATE_FORMAT

ScatterChart(
    data=records,
    title="Men's marathon world record",
    xlabel="Race date",
    ylabel="Finishing time (minutes)",
    # a tick every five years, labeled with the year
    xticks=[date(year, 1, 1) for year in range(2005, 2025, 5)],
    xticks_format=DATE_FORMAT.YEAR,
    show_regression=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Custom data keys

Data that comes from a file or an API rarely uses the `x` and `y` keys, and renaming every record just to plot it is a chore. The `x` and `y` arguments name the keys to read instead, just as `size`, `hue` and `annotation` name the keys of the bubble size, the category and the point annotation. `country_records` stores the countries the way a CSV export would:

```
country_records = [
    {"country": name, "region": region, "gdp_per_capita": gdp, "life_expectancy": life, "population": population}
    for name, (region, gdp, life, population) in COUNTRIES.items()
]
country_records[:2]
```

```
ScatterChart(
    data=country_records,
    # the keys that hold the x and y values
    x="gdp_per_capita",
    y="life_expectancy",
    # and the category
    hue="region",
    title="Life expectancy and income, 2019",
    xlabel="GDP per capita (USD, log scale)",
    ylabel="Life expectancy (years)",
    scalex=AXIS_SCALE.LOG,
    xticks=GDP_TICKS,
    xticklabels=GDP_TICK_LABELS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

## Real-World Examples

The examples below put the features above to work on real or realistic data, each one answering a question. The data lives in hidden cells; each example says what its data is and where it comes from.

### Example 1: Does Accuracy Keep Growing with Model Size? (Log-Transformed Regression with a Confidence Band)

`model_accuracy` holds the benchmark accuracy, in percent, of 24 illustrative language models with 0.1 to 100 billion parameters, drawn from a seeded random generator around a trend of 12 points per tenfold increase in size. Accuracy grows with the logarithm of the size, so the points are plotted against `log10` of the parameter count with the ticks labeled in billions; `show_regression` fits the trend, `show_ci` shades its 90% confidence band, and `show_correlation` reports how tight the trend is. The band is narrowest in the middle of the range, where the fit has data on both sides.

```
ScatterChart(
    data=model_accuracy,
    style={"plot_scatter_alpha": 0.8},
    # the trend, its 90% confidence band, and its strength
    show_regression=True,
    show_ci=True,
    ci_level=0.9,
    show_correlation=True,
    title="Benchmark accuracy and model size",
    xlabel="Parameters (log scale)",
    ylabel="Accuracy (%)",
    # the x values are log10(billions of parameters)
    xticks=[-1, 0, 1, 2],
    xticklabels=["0.1B", "1B", "10B", "100B"],
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Example 2: Heavier Penguins Have Longer Flippers, Within Each Species Too (Per-Series Regression and Custom Data Keys)

`penguins` holds the flipper length in millimeters and the body mass in grams of the 342 penguins with both measurements in the [Palmer penguins](https://allisonhorst.github.io/palmerpenguins/) dataset (Gorman, Williams and Fraser, 2014; released under CC0), one list per species, stored under the keys `flipper_length_mm` and `body_mass_g`. Across all penguins the link is strong, but part of it only says that Gentoo penguins are bigger than the other two species. Does it hold within a species? One series per species answers it: `x` and `y` read the stored keys, and `show_regression` fits one line per series, in the series' color. All three lines rise.

```
ScatterChart(
    data=penguins,
    # the keys that hold the measurements
    x="flipper_length_mm",
    y="body_mass_g",
    subtitle=SPECIES,
    style={"plot_scatter_alpha": 0.5, "plot_scatter_size": 16},
    # one regression line per species
    show_regression=True,
    title="Body mass and flipper length of Palmer penguins",
    xlabel="Flipper length (mm)",
    ylabel="Body mass (g)",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
    legend={"title": "Species", "location": LEGEND_LOCATION.UPPER_LEFT},
).show()
```

### Example 3: Did the Final Sweep Beat the Search? (Emphasis, a Frontier Line with Panel, and a Note)

`tuning_runs` holds two sets of illustrative hyperparameter tuning runs, each run a point of training time in minutes against validation accuracy in percent: 150 runs of a broad random search and the 12 runs of a final, narrowed-down sweep, both drawn from seeded random generators. The question is whether the sweep found anything the search had not. `emphasis` mutes the search into a background cloud and highlights the sweep. `search_frontier` holds the best accuracy the search reached within each training time, drawn as a dashed [LineChart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/linechart/index.md) that runs flat to the longest run, and [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) puts the frontier over the runs in one axes; a note points at the best run of the sweep, above the frontier.

```
from datachart.charts import LineChart
from datachart.utils import Panel

runs = ScatterChart(
    data=tuning_runs,
    subtitle=["random search", "final sweep"],
    # mute the search, highlight the sweep
    emphasis=["background", "highlight"],
    # point at the best run of the sweep
    texts={
        "text": f"best sweep run: {BEST_SWEEP['y']:.1f}%",
        "x": 0.1,
        "y": 0.9,
        "coords": "axes",
        "target": (BEST_SWEEP["x"], BEST_SWEEP["y"]),
    },
)
frontier = LineChart(
    data=search_frontier,
    subtitle="best of the search so far",
    style={"plot_line_color": "#6c757d", "plot_line_style": LINE_STYLE.DASHED},
)

Panel(
    [runs, frontier],
    title="Validation accuracy of the tuning runs",
    xlabel="Training time (minutes)",
    ylabel_left="Validation accuracy (%)",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
    legend={"title": "Tuning runs", "location": LEGEND_LOCATION.LOWER_RIGHT},
).show()
```
