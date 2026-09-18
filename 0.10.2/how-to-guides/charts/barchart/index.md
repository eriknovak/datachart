# Bar Chart

A bar chart compares a numeric value across a few categories: each category gets a bar, and the bar lengths answer *which is bigger, and by how much*. This guide shows how to create bar charts with the [datachart.charts.BarChart](https://eriknovak.github.io/datachart/0.10.2/references/charts/barchart/#datachart.charts.BarChart) function, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-bar-chart), which maps common tasks to the parameter or style attribute that does the job.

```
from datachart.charts import BarChart
```

## Basics

The examples in this guide share one dataset: the top ten countries of the Paris 2024 Olympic medal table, ranked by gold medals (source: the official Paris 2024 medal table). The data lives in a hidden cell. `medals_total` holds the total medals of each country, one data point per country, and `medals_by_metal` holds one series per metal (gold, silver, bronze) over the same countries. The table has stories in it, and the customizations below tell them: two countries tied on gold, a host nation, and a ranking that changes with the way it is counted.

Each data point is a dictionary with a `label` (the category) and a `y` value:

```
medals_total[:3]
```

**Basic example.** Only the `data` argument is required. The bars follow the input order, which here is the official gold-medal ranking:

```
BarChart(
    # add the data to the chart
    data=medals_total
).show()
```

## Customizing the Bar Chart

Every customization is either a keyword argument of `BarChart` or a `plot_bar_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                  | Use                                                    | See                                                                                                        |
| ------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| add a title and axis labels                 | `title`, `xlabel`, `ylabel`                            | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| rotate the tick labels                      | `xtickrotate`, `ytickrotate`                           | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| fix the axis range                          | `xmin`, `xmax`, `ymin`, `ymax`                         | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| resize the figure                           | `figsize`                                              | [Figure size and grid](#figure-size-and-grid)                                                              |
| show grid lines                             | `show_grid`                                            | [Figure size and grid](#figure-size-and-grid)                                                              |
| fix the aspect ratio of the axes            | `aspect_ratio`                                         | [Figure size and grid](#figure-size-and-grid)                                                              |
| draw the bars horizontally                  | `orientation`                                          | [Horizontal bars](#horizontal-bars)                                                                        |
| order the categories by value               | `sort`, `sort_by`                                      | [Sorting](#sorting)                                                                                        |
| print the value on each bar                 | `show_values`, `value_format`                          | [Value labels](#value-labels)                                                                              |
| change the bar color, width, hatch, or edge | `style={"plot_bar_color": ..., "plot_bar_hatch": ...}` | [Bar style](#bar-style)                                                                                    |
| highlight some bars, mute the rest          | `emphasis_rule`, the `"emphasis"` key of a data point  | [Emphasis](#emphasis)                                                                                      |
| mark a threshold or a boundary              | `hlines`, `vlines`                                     | [Reference lines and bands](#reference-lines-and-bands)                                                    |
| shade a range or a group of bars            | `hspans`, `vspans`                                     | [Reference lines and bands](#reference-lines-and-bands)                                                    |
| put a note on the chart                     | `texts`                                                | [Text annotations](#text-annotations)                                                                      |
| use dates as category labels                | `date` objects as `label`, `xticks_format`             | [Date labels](#date-labels)                                                                                |
| compare several series in one chart         | `data` as a list of lists, `subtitle`, `show_legend`   | [Multiple Bar Charts](#multiple-bar-charts)                                                                |
| group, stack, or overlay the series         | `bar_mode`                                             | [Bar mode](#bar-mode)                                                                                      |
| highlight one series, mute the rest         | `emphasis`                                             | [Multiple Bar Charts](#multiple-bar-charts)                                                                |
| title and place the legend                  | `legend`                                               | [Legend](#legend)                                                                                          |
| draw each series in its own subplot         | `subplots`, `sharex`, `sharey`, `max_cols`             | [Subplots](#subplots)                                                                                      |
| show the uncertainty of each bar            | `yerr` in `data`, `show_yerr`                          | [Error bars](#error-bars)                                                                                  |
| use a logarithmic axis                      | `scaley`, `scalex`                                     | [Axis scales](#axis-scales)                                                                                |
| plot data with other key names              | `label`, `y`, `yerr`                                   | [Custom data keys](#custom-data-keys)                                                                      |
| save the chart to a file                    | `save_figure`                                          | [Saving Figures](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/utility/saving/index.md) guide |

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.2/references/constants/index.md) that lists its values:

| Parameter                                    | Constant                                                                                                                                                                                                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                      |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                      |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                    |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                              |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                              |
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.ORIENTATION)                                                                                                                                |
| `bar_mode`                                   | [`BAR_MODE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.BAR_MODE)                                                                                                                                      |
| `sort`                                       | [`SORT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SORT)                                                                                                                                              |
| `scalex`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.DATE_FORMAT)         |

The full list of style attributes is in the [datachart.typings.BarStyleAttrs](https://eriknovak.github.io/datachart/0.10.2/references/charts/barchart/#datachart.typings.BarStyleAttrs) type; the full list of parameters is in the [datachart.charts.BarChart](https://eriknovak.github.io/datachart/0.10.2/references/charts/barchart/#datachart.charts.BarChart) reference.

### Title, axis labels and ticks

A chart without a title and axis labels leaves the reader guessing what the bars measure; `title`, `xlabel` and `ylabel` say it. Ten country names crowd the category axis, so `xtickrotate` (or `ytickrotate`) tilts them out of each other's way. `xmin`, `xmax`, `ymin` and `ymax` fix the axis range: bars encode value by length, so the value axis should start at zero, and a little headroom leaves space for labels added later.

```
BarChart(
    data=medals_total,
    # add the title
    title="Paris 2024 medal table",
    # add the x and y axis labels
    xlabel="Country",
    ylabel="Medals",
    # rotate the x-axis tick labels
    xtickrotate=45,
    # fix the y-axis range
    ymin=0,
    ymax=140,
).show()
```

### Figure size and grid

The default figure is nearly square, while a bar chart with many categories reads best wide and short. `figsize` takes a `(width, height)` tuple in inches or one of the presets in [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.FIG_SIZE), sized for a full or half page width.

Grid lines let the eye carry the top of a bar across to the axis. `show_grid` draws them along the value axis with [SHOW_GRID.Y](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SHOW_GRID), the reading aid a bar chart needs, without cluttering the category axis (`SHOW_GRID.X` and `SHOW_GRID.BOTH` are the other options). `aspect_ratio` fixes the ratio of the axes rather than of the figure ([ASPECT_RATIO](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.ASPECT_RATIO)); bar charts rarely need it, so the examples leave it at the default.

```
from datachart.constants import FIG_SIZE, SHOW_GRID

BarChart(
    data=medals_total,
    title="Paris 2024 medal table",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    ymin=0,
    ymax=140,
    # a wide, short figure
    figsize=FIG_SIZE.FULL_SHORT,
    # grid lines along the value axis only
    show_grid=SHOW_GRID.Y,
).show()
```

### Horizontal bars

A ranking reads best top to bottom, and long category names read best unrotated. Horizontal bars give both: `orientation=ORIENTATION.HORIZONTAL` ([ORIENTATION](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.ORIENTATION)) puts the categories on the y-axis and the values on the x-axis, so the axis labels and the grid swap with it. The first data point is drawn at the bottom, so the data is reversed to keep the ranking top-down.

```
from datachart.constants import ORIENTATION

BarChart(
    # reversed, so the first country ends up at the top
    data=medals_total[::-1],
    title="Paris 2024 medal table",
    # the axis labels swap with the orientation
    xlabel="Medals",
    ylabel="Country",
    figsize=FIG_SIZE.FULL_MEDIUM,
    # and so does the grid
    show_grid=SHOW_GRID.X,
    # draw the bars horizontally
    orientation=ORIENTATION.HORIZONTAL,
    xmin=0,
).show()
```

### Sorting

The medal table ranks by gold, but that is a convention, and the same numbers tell a different story ranked by total medals. `sort` orders the categories by value: `SORT.DESCENDING` puts the largest bar first, `SORT.ASCENDING` the smallest, and `None` keeps the input order ([SORT](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SORT)). Ranked by total, Great Britain climbs from seventh to third and France moves above Japan and Australia.

```
from datachart.constants import SORT

BarChart(
    data=medals_total,
    title="Paris 2024 medal table, ranked by total medals",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # largest total first
    sort=SORT.DESCENDING,
    ymin=0,
).show()
```

With several series in one chart, one order serves all of them, keyed by the total across the series; `sort_by` names the series (by its `subtitle`) that keys the order instead. `medals_by_metal` holds one series per metal (the [Multiple Bar Charts](#multiple-bar-charts) section covers the list-of-lists form), and ranking it by silver medals moves France to third:

```
BarChart(
    data=medals_by_metal,
    subtitle=METALS,
    title="Paris 2024 medal table, ranked by silver medals",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # one order for every series, keyed by one of them
    sort=SORT.DESCENDING,
    sort_by="Silver",
).show()
```

### Value labels

When the exact numbers matter, as they do in a medal table, `show_values` prints each bar's value at its edge, and `value_format` formats it: a [VALUE_FORMAT](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT) constant or any `"{x:.1f}"`, `"{:.1f}%"` or `"%g"` style string. The label font size, color and padding are the `plot_value_*` style attributes ([ValueLabelStyleAttrs](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.ValueLabelStyleAttrs)), shared by every chart that prints values. Value labels need headroom, so the value axis is extended a little past the longest bar.

```
from datachart.constants import VALUE_FORMAT

BarChart(
    data=medals_total[::-1],
    style={"plot_value_fontsize": 9, "plot_value_padding": 4},
    title="Paris 2024 medal table",
    xlabel="Medals",
    ylabel="Country",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.X,
    orientation=ORIENTATION.HORIZONTAL,
    # room for the labels past the longest bar
    xmin=0,
    xmax=145,
    # print the value of each bar
    show_values=True,
    value_format=VALUE_FORMAT.INTEGER,
).show()
```

### Bar style

The `style` dictionary sets the look of the bars: the color and alpha, the width as a fraction of the category width, the hatch pattern, and the edge; the attributes are listed in [datachart.typings.BarStyleAttrs](https://eriknovak.github.io/datachart/0.10.2/references/charts/barchart/#datachart.typings.BarStyleAttrs), and any attribute left out keeps the value of the active theme. A chart that will be printed or photocopied has to survive without color: a hatch pattern from [HATCH_STYLE](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.HATCH_STYLE) and a dark edge keep the bars distinct in greyscale.

```
from datachart.constants import HATCH_STYLE

BarChart(
    data=medals_total,
    # a print-safe look: hatched bars with a dark edge
    style={
        "plot_bar_color": "#f4f1de",
        "plot_bar_width": 0.6,
        "plot_bar_hatch": HATCH_STYLE.DIAGONAL,
        "plot_bar_edge_width": 1.0,
        "plot_bar_edge_color": "#3d405b",
    },
    title="Paris 2024 medal table",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    ymin=0,
).show()
```

### Emphasis

A chart usually makes one point, and emphasis makes it visible. A data point can carry its own `"emphasis"` key: `"highlight"` bolds the bar's edges and brings it to the front, `"background"` mutes it (the theme's muted color at a lower alpha), so marking the host nation is a matter of tagging one record and muting the rest. The roles are also available as the [EMPHASIS](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.EMPHASIS) constants, and the [Highlighting](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/styling/highlighting/index.md) guide covers emphasis across every chart type and theme.

```
# tag the host nation, mute the rest
host_marked = [
    {**point, "emphasis": "highlight" if point["label"] == HOST else "background"}
    for point in medals_total
]

BarChart(
    data=host_marked,
    title="Paris 2024 medal table, the host nation",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    ymin=0,
).show()
```

`emphasis_rule` picks the bars from the data instead of tagging them by hand. It is a one-key dictionary: `{"top": n}` or `{"bottom": n}` by rank, `{"above": v}` or `{"below": v}` (strict), or `{"between": (lo, hi)}` (inclusive); the bars that match are highlighted, the rest muted. A data point's own `"emphasis"` key wins over the rule, so tagging the host alone and letting the rule handle the rest says *the podium, and also the host*:

```
# tag the host only; the rule decides the rest
host_tagged = [
    {**point, "emphasis": "highlight"} if point["label"] == HOST else point
    for point in medals_total
]

BarChart(
    data=host_tagged,
    title="Paris 2024 medal table, the podium and the host",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    sort=SORT.DESCENDING,
    # the three largest bars; France's own key keeps it highlighted
    emphasis_rule={"top": 3},
    ymin=0,
).show()
```

### Reference lines and bands

Reference lines and bands put the bars in context. `hlines` draws a horizontal line at a value, such as the mean of the table, and `vlines` a vertical one at a bar position; positions along the category axis are bar indices (`0`, `1`, `2`, …), so a half-integer sits between two bars. `hspans` and `vspans` shade a range instead of marking a value: a band of acceptable values, or a group of bars. Each takes a dictionary or a list of them, with the position, an optional `label` for the legend and a `style`; the keys are listed in [HLineSettingAttrs](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.HLineSettingAttrs), [VLineSettingAttrs](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.VLineSettingAttrs), [HSpanSettingAttrs](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.HSpanSettingAttrs) and [VSpanSettingAttrs](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.VSpanSettingAttrs). The example marks the mean of the top ten with a dashed line and shades the three podium positions.

```
from datachart.constants import LINE_STYLE

mean_medals = sum(point["y"] for point in medals_total) / len(medals_total)

BarChart(
    data=medals_total,
    # a dashed line at the mean of the top ten
    hlines={
        "y": mean_medals,
        "label": "top-ten mean",
        "style": {"plot_hline_color": "#c1121f", "plot_hline_style": LINE_STYLE.DASHED},
    },
    # shade the first three bars
    vspans={"xmin": -0.5, "xmax": 2.5, "label": "podium"},
    title="Paris 2024 medal table, ranked by total medals",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    sort=SORT.DESCENDING,
    ymin=0,
).show()
```

### Text annotations

Where a reference line marks a value, a note explains it. `texts` places text on the chart, with an optional `target` to draw a connector to a data point; the position is in data coordinates by default (bar index, value) or in axes fractions with `"coords": "axes"`, which keeps the note in place whatever the axis limits. The [Text Annotations](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/utility/annotations/index.md) guide covers placement, connector looks and styling. The note below explains the tie at the top of the table.

```
BarChart(
    data=medals_total,
    # a note pinned to the axes, pointing at China's bar
    texts={
        "text": "tied on 40 golds; the United States\nleads on silver and bronze",
        "x": 0.5,
        "y": 0.8,
        "coords": "axes",
        "target": (1, MEDAL_TABLE["China"][0]),
    },
    title="Paris 2024 medal table",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    ymin=0,
    ymax=140,
).show()
```

### Date labels

Categories are often dates: quarters, months, editions of an event. A `label` that is a real temporal object (`datetime`, `date`, `numpy.datetime64` or a pandas `Timestamp`) keeps its categorical position but prints through `xticks_format`, a [DATE_FORMAT](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.DATE_FORMAT) member or any `strftime` pattern, so the tick labels come out tidy without hand-writing them. `france_golds`, defined in a hidden cell, holds France's gold medals at the last five Summer Games, labeled by the opening day of each Games (Tokyo 2020 was held in 2021, and the year format shows it).

```
from datachart.constants import DATE_FORMAT

BarChart(
    data=france_golds,
    title="France's gold medals by Summer Games",
    xlabel="Games",
    ylabel="Gold medals",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # print the date labels as years
    xticks_format=DATE_FORMAT.YEAR,
    yticks=[0, 5, 10, 15],
    ymin=0,
).show()
```

## Multiple Bar Charts

To compare several series, pass a list of lists to `data`: each inner list is one series, and the per-series attributes (`subtitle`, `style`, `emphasis`) become lists aligned with it. Series that share a label are drawn side by side in one group, and `show_legend` names them by their subtitles. `medals_by_metal` is such a list, one series per metal, and a style per series colors the bars like the metals they stand for.

```
METAL_STYLE = [
    {"plot_bar_color": "#d4af37"},  # gold
    {"plot_bar_color": "#a8a9ad"},  # silver
    {"plot_bar_color": "#cd7f32"},  # bronze
]

BarChart(
    # one series per metal
    data=medals_by_metal,
    # named for the legend
    subtitle=METALS,
    # and colored like the metal
    style=METAL_STYLE,
    title="Paris 2024 medal table by metal",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

When the question is about one of the series, `emphasis` takes one role per series, aligned with `data` like `subtitle` and `style`: `"highlight"` bolds a series, `"background"` mutes it and drops it from the legend, `None` leaves it as it is. Asking only about gold turns the silver and bronze bars into context:

```
BarChart(
    data=medals_by_metal,
    subtitle=METALS,
    style=METAL_STYLE,
    # gold is the question, silver and bronze the context
    emphasis=["highlight", "background", "background"],
    title="Paris 2024 medal table, gold against the rest",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Bar mode

Grouped bars compare the series within each category, but hide the totals. `bar_mode` changes how the series share a category ([BAR_MODE](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.BAR_MODE)): `BAR_MODE.STACK` stacks them, so the height of each stack is the total and the segments are its split; `BAR_MODE.OVERLAY` draws them at the same position, one over the other, which suits a before-and-after pair; `BAR_MODE.GROUP` is the default. Stacked and sorted, the chart shows the ranking by total medals and what each total is made of.

```
from datachart.constants import BAR_MODE

BarChart(
    data=medals_by_metal,
    subtitle=METALS,
    style=METAL_STYLE,
    title="Paris 2024 medal table by metal, ranked by total medals",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # stack the metals; the sort keys on the total across them
    bar_mode=BAR_MODE.STACK,
    sort=SORT.DESCENDING,
).show()
```

An overlay pairs each country's Paris result with its Tokyo result. `golds_2020`, defined in a hidden cell, holds the same ten countries' gold medals at Tokyo 2020 (source: the official Tokyo 2020 medal table). The Tokyo series is drawn first, in grey, and the Paris series over it in gold, so a grey bar showing above a gold one is a country that won fewer golds in Paris than in Tokyo: Japan, the previous host, and Great Britain.

```
BarChart(
    data=[golds_2020, golds_2024],
    subtitle=["Tokyo 2020", "Paris 2024"],
    # the earlier Games in grey, the later ones in gold over them
    style=GAMES_STYLE,
    title="Gold medals, Tokyo 2020 and Paris 2024",
    xlabel="Country",
    ylabel="Gold medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # both series at the same positions
    bar_mode=BAR_MODE.OVERLAY,
).show()
```

### Legend

`show_legend` lists the series; `legend` says where and how, with a `title`, a `location` from [LEGEND_LOCATION](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_LOCATION), the number of columns `ncols`, and the `alignment` of the entries from [LEGEND_ALIGN](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_ALIGN); a field left out falls back to the theme ([LegendSettingAttrs](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.LegendSettingAttrs)). Ten groups of three bars leave no empty corner inside the axes, so the legend goes outside them.

```
from datachart.constants import LEGEND_LOCATION

BarChart(
    data=medals_by_metal,
    subtitle=METALS,
    style=METAL_STYLE,
    title="Paris 2024 medal table by metal",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # a titled legend outside the axes, to the right
    legend={"title": "Medal", "location": LEGEND_LOCATION.OUTSIDE_RIGHT},
).show()
```

### Subplots

When the series are many, or the question is about the shape of each rather than the comparison within a category, `subplots=True` draws each series in its own panel. `subtitle` titles the panels; `title`, `xlabel` and `ylabel` stay global; `max_cols` limits the panels per row. `sharey=True` puts the panels on one value axis, so a bar in one panel is comparable with a bar in the next; without it each panel scales to its own maximum and the bronze counts would look as large as the golds. `sharex=True` keeps one category axis for all of them.

```
BarChart(
    data=medals_by_metal,
    subtitle=METALS,
    style=METAL_STYLE,
    title="Paris 2024 medal table by metal",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_TALL,
    show_grid=SHOW_GRID.Y,
    # one panel per metal, stacked in a column
    subplots=True,
    max_cols=1,
    # one value axis and one category axis for all panels
    sharex=True,
    sharey=True,
).show()
```

## Additional Features

### Error bars

A bar shows an estimate; an error bar shows how sure the estimate is. Each data point carries its uncertainty as `yerr`, `show_yerr` draws it, and the `plot_bar_error_color` style attribute colors the whiskers. Medal counts are exact, so this example switches dataset: `poll`, defined in a hidden cell, is an illustrative pre-election poll, the support for five parties with the survey's margin of error. Two parties whose error bars overlap are not shown to be apart, which is what the error bars are there to say.

```
BarChart(
    data=poll,
    # the color of the whiskers
    style={"plot_bar_error_color": "#333333"},
    title="Voting intention, with the margin of error",
    xlabel="Party",
    ylabel="Support (%)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # draw the error bars
    show_yerr=True,
    ymin=0,
).show()
```

### Axis scales

Bars encode value by length, so a linear axis is the honest default, and a logarithmic one is the exception for values that span orders of magnitude. `scaley` (or `scalex` for horizontal bars) takes a [SCALE](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SCALE) member. `populations`, defined in a hidden cell, holds the approximate mid-2024 population of seven countries in thousands (UN World Population Prospects 2024, rounded), from about 1.45 billion down to about 10 thousand. On a linear scale the small countries vanish; on a log scale every bar is readable, at the price that bar lengths no longer compare.

```
from datachart.constants import SCALE

for scale in [SCALE.LINEAR, SCALE.LOG]:
    BarChart(
        data=populations,
        title=f"Population on the '{scale}' scale",
        xlabel="Country",
        ylabel="Population (thousands)",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
        # the scale of the value axis
        scaley=scale,
    ).show()
```

### Custom data keys

Data that comes from a file or an API rarely uses the `label`, `y` and `yerr` keys, and renaming every record just to plot it is a chore. Instead, tell `BarChart` which keys to read with the `label`, `y` and `yerr` arguments. `medal_records` stores the table the way a CSV export would, one record per country with a `country` and a `total` key:

```
medal_records = [
    {"country": country, "gold": gold, "silver": silver, "bronze": bronze, "total": gold + silver + bronze}
    for country, (gold, silver, bronze) in MEDAL_TABLE.items()
]
medal_records[:2]
```

```
BarChart(
    data=medal_records,
    # the keys that hold the label and the value
    label="country",
    y="total",
    title="Paris 2024 medal table",
    xlabel="Country",
    ylabel="Medals",
    xtickrotate=45,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    ymin=0,
).show()
```

## Real-World Examples

The examples below put the features above to work on real or realistic data, each one answering a question. The data lives in hidden cells; each example says what its data is and where it comes from.

### Example 1: Where Python Stands (Ranked Horizontal Bars with Value Labels)

`languages` holds the share of respondents who worked with each of the ten most-used programming languages in the past year, from the Stack Overflow Developer Survey 2024 (all respondents). The question is where Python stands among them. Horizontal bars keep the names readable and `sort` ranks them, value labels print the exact share (the values already are percentages, so a positional `"{:.1f}%"` format appends the sign; `VALUE_FORMAT.PERCENT` would multiply by 100), and Python's record carries its own `"emphasis"` key while the rest are muted.

```
BarChart(
    data=languages,
    style={"plot_value_fontsize": 9, "plot_value_padding": 4},
    title="Most used programming languages, 2024",
    xlabel="Share of respondents",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.X,
    orientation=ORIENTATION.HORIZONTAL,
    # smallest first, so the most used ends up at the top
    sort=SORT.ASCENDING,
    xmin=0,
    xmax=75,
    show_values=True,
    value_format="{:.1f}%",
).show()
```

### Example 2: A Trade Balance Turns Around (Diverging Bars with a Note)

`trade_balance` holds two years of illustrative monthly trade balance figures (exports minus imports, in billion EUR): a run of deficits in the first year turning into surpluses in the second. Positive and negative months want different colors, and `BarChart` applies one color per series, so the data is split into a surplus series and a deficit series drawn at the same positions with `bar_mode=BAR_MODE.OVERLAY` (see the tip below). The months are `date` labels printed as year and month, a solid line marks zero, and a note points at the first month in surplus.

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
        "style": {"plot_hline_color": "black", "plot_hline_style": LINE_STYLE.SOLID, "plot_hline_width": 1},
    },
    # point at the first month in surplus
    texts={
        "text": "first surplus",
        "x": 0.3,
        "y": 0.85,
        "coords": "axes",
        "target": (FIRST_SURPLUS, BALANCE[FIRST_SURPLUS]),
    },
    title="Monthly trade balance",
    ylabel="Billion EUR",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    xticks_format=DATE_FORMAT.YEAR_MONTH,
    xtickrotate=90,
).show()
```

Tip: Diverging Bar Charts

Each month is zero in one of the two series (positive values in one, negative in the other). Drawing them with `bar_mode=BAR_MODE.OVERLAY` puts both series at the same positions, so only one bar is visible per month: the visual effect of a single diverging bar chart with two colors.

### Example 3: The Host Effect (Overlaid Games, Highlighted Home Games, and a Grid)

Hosting the Games is said to lift a country's medal haul, and the medal tables of the last five Summer Games let us check. The top chart overlays each country's gold medals at Tokyo 2020 and Paris 2024 for the ten countries of the shared dataset, ranked by the Paris result with `sort_by`. The two charts below it follow the two most recent hosts, France and Japan, across five Games: `japan_golds`, defined in a hidden cell, holds Japan's gold medals (source: the official medal tables), and `emphasis_rule={"top": 1}` highlights each country's best Games, which in both cases is the one it hosted; a note on each says so. [Grid](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/utility/grid/index.md) puts the three charts in one figure, the comparison across the full top row and the two histories side by side below it, and the notes travel with their charts.

```
from datachart.utils import Grid

games = BarChart(
    data=[golds_2020, golds_2024],
    subtitle=["Tokyo 2020", "Paris 2024"],
    style=GAMES_STYLE,
    title="Gold medals at the last two Games",
    ylabel="Gold medals",
    xtickrotate=45,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    bar_mode=BAR_MODE.OVERLAY,
    # ranked by the Paris result
    sort=SORT.DESCENDING,
    sort_by="Paris 2024",
)


def host_history(data, country, host_index):
    # a country's golds over five Games, its best Games highlighted and annotated
    return BarChart(
        data=data,
        title=f"{country}'s gold medals by Games",
        ylabel="Gold medals",
        show_grid=SHOW_GRID.Y,
        xticks_format=DATE_FORMAT.YEAR,
        emphasis_rule={"top": 1},
        texts={
            "text": "home Games",
            "x": 0.08 if host_index == 4 else 0.62,
            "y": 0.9,
            "coords": "axes",
            "target": (host_index, data[host_index]["y"]),
        },
        # the same value axis for both countries
        yticks=[0, 10, 20, 30],
        ymin=0,
        ymax=30,
    )


Grid(
    [
        [games],
        [host_history(france_golds, "France", 4), host_history(japan_golds, "Japan", 3)],
    ],
    title="The host effect",
    figsize=FIG_SIZE.FULL_TALL,
).show()
```
