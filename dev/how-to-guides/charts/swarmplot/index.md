# Swarm Plot

A swarm plot draws every observation as its own point, grouped by category and spread sideways so no point hides another. Where a box plot summarizes a sample, a swarm shows it whole, which matters when the sample is small or when single points are the story: an outlier with a name, a cluster, a gap. This guide shows how to create swarm plots with the [datachart.charts.SwarmPlot](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/#datachart.charts.SwarmPlot) function, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-swarm-plot), which maps common tasks to the parameter or style attribute that does the job.

```
from datachart.charts import SwarmPlot
```

## Basics

The examples in this guide share one small dataset: the 47 presidencies of the United States in their official numbering (Grover Cleveland and Donald Trump each count twice), with the age of each president on the day he took office. The ages are computed from the birth and inauguration dates published in the White House presidential biographies. The data lives in a hidden cell. `PRESIDENCIES` holds one row per presidency (name, party, birth date, first day and last day in office), and `inauguration_ages` holds one data point per presidency, labeled with its era: the presidencies that began in 1789–1897, in 1901–1993, and in 2001–2025. With 47 points, every point is a person, and the extremes have names: the youngest president, Theodore Roosevelt, and the two oldest, both sworn in during the last era.

Each data point is a dictionary with a `label` (the group) and a `value`. The points that share a `label` form one swarm, so three eras give three swarms:

```
inauguration_ages[:3]
```

**Basic example.** Only the `data` argument is required. Each presidency is one point above its era, and points with the same or a close age spread sideways instead of stacking, so the width of a swarm at any height shows how many presidents took office at that age:

```
SwarmPlot(
    # add the data to the chart
    data=inauguration_ages
).show()
```

## Customizing the Swarm Plot

Every customization is either a keyword argument of `SwarmPlot` or a `plot_swarm_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                    | Use                                                       | See                                                                                                     |
| --------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| add a title and axis labels                   | `title`, `xlabel`, `ylabel`                               | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                            |
| fix the axis range or the ticks               | `ymin`, `ymax`, `yticks`, `xtickrotate`                   | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                            |
| resize the figure                             | `figsize`                                                 | [Figure size and grid](#figure-size-and-grid)                                                           |
| show grid lines                               | `show_grid`                                               | [Figure size and grid](#figure-size-and-grid)                                                           |
| change the point color, size, marker, or edge | `style={"plot_swarm_color": ..., "plot_swarm_size": ...}` | [Point style](#point-style)                                                                             |
| jitter the points instead of packing them     | `mode`, `jitter`                                          | [Swarm and strip modes](#swarm-and-strip-modes)                                                         |
| draw the swarms horizontally                  | `orientation`                                             | [Horizontal swarms](#horizontal-swarms)                                                                 |
| change the order of the groups                | the order of `data`                                       | [Horizontal swarms](#horizontal-swarms)                                                                 |
| print each group's min, median, and max       | `show_values`, `value_format`                             | [Value labels](#value-labels)                                                                           |
| highlight some groups, mute the rest          | `emphasis`, `emphasis_rule`                               | [Emphasis](#emphasis)                                                                                   |
| highlight single points                       | a series of their own, `emphasis`                         | [Emphasis](#emphasis)                                                                                   |
| mark a threshold or shade a range             | `hlines`, `dlines`, `vlines`, `hspans`, `vspans`          | [Reference lines and bands](#reference-lines-and-bands)                                                 |
| name a point on the chart                     | `texts`                                                   | [Text annotations](#text-annotations)                                                                   |
| use dates as group labels                     | `date` objects as `label`, `xticks_format`                | [Date labels](#date-labels)                                                                             |
| put the points over a box or violin plot      | `Panel`                                                   | [Swarms over boxes and violins](#swarms-over-boxes-and-violins)                                         |
| compare several datasets in one chart         | `data` as a list of lists, `subtitle`, `show_legend`      | [Multiple Swarm Plots](#multiple-swarm-plots)                                                           |
| title and place the legend                    | `legend`                                                  | [Legend](#legend)                                                                                       |
| draw each dataset in its own subplot          | `subplots`, `sharex`, `sharey`, `max_cols`                | [Subplots](#subplots)                                                                                   |
| use a logarithmic value axis                  | `scaley`                                                  | [Logarithmic scale](#logarithmic-scale)                                                                 |
| plot data with other key names                | `label`, `value`                                          | [Custom data keys](#custom-data-keys)                                                                   |
| save the chart to a file                      | `save_figure`                                             | [Saving Figures](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/saving/index.md) guide |

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values:

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                   |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |
| `mode`                                       | [`SWARM_MODE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SWARM_MODE)                                                                                                                               |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                           |
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION)                                                                                                                             |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE)                                                                                                                                         |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |

The full list of style attributes is in the [datachart.typings.SwarmStyleAttrs](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/#datachart.typings.SwarmStyleAttrs) type; the full list of parameters is in the [datachart.charts.SwarmPlot](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/#datachart.charts.SwarmPlot) reference.

### Title, axis labels and ticks

The basic chart does not say what the points measure; `title`, `xlabel` and `ylabel` do. `ymin` and `ymax` fix the value range, and `yticks` picks the tick positions: a round range from 40 to 80 frames every age, and a tick every five years makes the ages easy to read off. Long group names can be tilted with `xtickrotate` (or `ytickrotate`); three short eras do not need it.

```
SwarmPlot(
    data=inauguration_ages,
    # add the title
    title="Age of US presidents at inauguration",
    # add the x and y axis labels
    xlabel="Took office in",
    ylabel="Age (years)",
    # fix the value range and the ticks
    ymin=40,
    ymax=80,
    yticks=[40, 45, 50, 55, 60, 65, 70, 75, 80],
).show()
```

### Figure size and grid

Three swarms do not need a square figure; a wide, short one fits a page better. `figsize` takes a `(width, height)` tuple in inches or one of the presets in [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE). Grid lines let the eye carry a point across to the value axis: `show_grid` takes a [SHOW_GRID](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID) member, and `SHOW_GRID.Y` draws them along the value axis only. `aspect_ratio` fixes the ratio of the axes ([ASPECT_RATIO](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)); a swarm has no reason to, so the examples leave it at the default.

```
from datachart.constants import FIG_SIZE, SHOW_GRID

SwarmPlot(
    data=inauguration_ages,
    title="Age of US presidents at inauguration",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    # a wide, short figure
    figsize=FIG_SIZE.FULL_SHORT,
    # grid lines along the value axis only
    show_grid=SHOW_GRID.Y,
).show()
```

### Point style

The `style` dictionary sets the look of the points: color, alpha, size, marker, edge and z-order; the attributes are listed in [datachart.typings.SwarmStyleAttrs](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/#datachart.typings.SwarmStyleAttrs), and any attribute left out keeps the value of the active theme. With few points, larger markers make each one count, and a white edge keeps neighbors apart where the swarm packs them tightly. The swarm packs from the marker size, so larger points spread wider. The marker shapes are listed in [LINE_MARKER](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LINE_MARKER).

```
from datachart.constants import LINE_MARKER

SwarmPlot(
    data=inauguration_ages,
    # large diamonds with a white edge
    style={
        "plot_swarm_color": "#1d3557",
        "plot_swarm_size": 40,
        "plot_swarm_alpha": 0.9,
        "plot_swarm_marker": LINE_MARKER.DIAMOND,
        "plot_swarm_edge_color": "#ffffff",
        "plot_swarm_edge_width": 0.8,
    },
    title="Age of US presidents at inauguration",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Swarm and strip modes

A swarm computes a place for every point so none overlap, which is what makes single points readable. With thousands of points that placement adds nothing: the swarm fills its whole width anyway, and grows wider than the category. `mode` picks the placement from [SWARM_MODE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SWARM_MODE): `SWARM_MODE.SWARM` packs the points from the marker size at the moment the chart is drawn (the default; axis limits changed on the figure afterwards can shift the spacing), and `SWARM_MODE.STRIP` scatters them at random across the category, a *strip plot*. `jitter` sets the width of the strip as a fraction of the category width (0.4 by default), and the jitter is seeded, so the same data draws the same chart. On the presidents the strip lets points overlap, so the swarm is the better choice for a sample this small; the strip earns its place in [Example 1](#example-1-which-services-breach-the-sla-strip-mode-log-scale-and-an-sla-line), with 1,200 points.

```
from datachart.constants import SWARM_MODE

SwarmPlot(
    data=inauguration_ages,
    # scatter the points at random instead of packing them
    mode=SWARM_MODE.STRIP,
    # a strip a quarter of the category wide
    jitter=0.25,
    title="Age of US presidents at inauguration, strip mode",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Horizontal swarms

Long group names read best unrotated, and many groups read best top to bottom. `orientation=ORIENTATION.HORIZONTAL` ([ORIENTATION](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION)) puts the groups on the y-axis and the values on the x-axis, so the axis labels, the value range and the grid swap with it. The groups follow the order in which their labels first appear in `data`, and the first group is drawn at the bottom; `SwarmPlot` has no sorting parameter, so the order is set by ordering the data. Reversing it puts the first era on top, and the eras read as a timeline from top to bottom.

```
from datachart.constants import ORIENTATION

SwarmPlot(
    # reversed, so the first era ends up at the top
    data=inauguration_ages[::-1],
    title="Age of US presidents at inauguration",
    # the axis labels, the range and the grid swap with the orientation
    xlabel="Age (years)",
    ylabel="Took office in",
    xmin=40,
    xmax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.X,
    # draw the swarms horizontally
    orientation=ORIENTATION.HORIZONTAL,
).show()
```

### Value labels

A reader who wants the numbers behind a swarm usually asks three things: the youngest, the oldest, and the typical age. `show_values` prints each group's minimum, median and maximum beside the points that hold them (the median beside the point nearest it), and `value_format` formats the labels: a [VALUE_FORMAT](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT) constant or any `"{x:.1f}"`, `"{:.1f}%"` or `"%g"` style string. The label font size, color and padding are the `plot_value_*` style attributes ([ValueLabelStyleAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)). The median age barely moves across the eras; the range is what grows.

```
from datachart.constants import VALUE_FORMAT

SwarmPlot(
    data=inauguration_ages,
    style={"plot_value_fontsize": 9},
    title="Age of US presidents at inauguration",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # print the min, median and max of every era
    show_values=True,
    value_format=VALUE_FORMAT.INTEGER,
).show()
```

### Emphasis

A chart usually makes one point, and emphasis makes it visible. `emphasis` takes one role per group, aligned with the group labels in the order they first appear: `"highlight"` bolds the edges of a group's points, `"background"` mutes them into the theme's muted color, and `None` leaves them as they are; a single value applies to every group. The roles are also available as the [EMPHASIS](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS) constants, and the [Highlighting](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/highlighting/index.md) guide covers emphasis across every chart type and theme. Highlighting the last era and muting the others asks the question of the chart: are recent presidents older?

```
from datachart.constants import EMPHASIS

SwarmPlot(
    data=inauguration_ages,
    # one role per era, in the order the eras appear
    emphasis=[EMPHASIS.BACKGROUND, EMPHASIS.BACKGROUND, EMPHASIS.HIGHLIGHT],
    title="Age of US presidents at inauguration, the last era",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

`emphasis_rule` picks the groups from the data instead of naming them. It is a dictionary with one condition, `{"top": n}` or `{"bottom": n}` by rank, `{"above": v}` or `{"below": v}` (strict), or `{"between": (lo, hi)}` (inclusive), read against a summary of each group: the median by default, or the `"mean"`, `"min"`, `"max"` or `"sum"` named by a `"by"` key. The groups that match are highlighted, the rest muted, and an explicit `emphasis` role wins over the rule. Asking which era swore in a president older than 70 highlights the last one, through its maximum:

```
SwarmPlot(
    data=inauguration_ages,
    # the eras whose oldest president was over 70
    emphasis_rule={"above": 70, "by": "max"},
    title="Age of US presidents at inauguration, eras with a president over 70",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

Emphasis works on whole groups, and a data point has no emphasis of its own. To single out a few points, move them into a series of their own (the [Multiple Swarm Plots](#multiple-swarm-plots) section covers the list-of-lists form) and give each series a role: the rest in the background, the chosen points highlighted. The two series are packed separately, so this suits points that stand apart from their group, like the two presidents who took office at 78:

```
# the two oldest presidents in a series of their own
oldest = [point for point in inauguration_ages if point["value"] >= 78]
others = [point for point in inauguration_ages if point["value"] < 78]

SwarmPlot(
    data=[others, oldest],
    # one role per series: mute the others, highlight the oldest
    emphasis=[EMPHASIS.BACKGROUND, EMPHASIS.HIGHLIGHT],
    title="Age of US presidents at inauguration, the two oldest",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Reference lines and bands

Reference lines and bands put the points in context. `hlines` draws a horizontal line at a value, such as a limit or the overall median, and `vlines` a vertical one; `hspans` and `vspans` shade a range instead. The groups sit at positions `1`, `2`, `3`, … along the category axis, so a vertical line at `1.5` falls between the first two groups. Each takes a dictionary or a list of them, with the position, an optional `label` for the legend and a `style`; the keys are listed in [HLineSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineSettingAttrs), [VLineSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineSettingAttrs), [HSpanSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanSettingAttrs) and [VSpanSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanSettingAttrs), and the line styles in [LINE_STYLE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LINE_STYLE). The US Constitution requires a president to be at least 35: a band shades the ages below it, and a dashed line marks the median age of all 47 presidencies. Nobody came close to the limit.

`dlines` completes the trio. Where `vlines` fixes an x and `hlines` a y, a diagonal is fixed by a `slope` and an `intercept`, so it runs through the data space instead of across it; `dlines={}` on its own draws the parity line `y = x`. It spans the axes unless `xmin` and `xmax` clip it to a segment, and takes the same optional `label` and `style`; the keys are listed in [DLineSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineSettingAttrs). The groups sit at `0`, `1`, `2`, … along the category axis, so a diagonal asks whether the ages drift across them: the line runs from the first group's median to the last, and the swarms standing above it took office older than that drift would have them.

```
from statistics import median

from datachart.constants import LEGEND_LOCATION, LINE_STYLE

SwarmPlot(
    data=inauguration_ages,
    # a dashed line at the median age of all presidencies
    hlines={
        "y": median(point["value"] for point in inauguration_ages),
        "label": "median age",
        "style": {"plot_hline_color": "#c1121f", "plot_hline_style": LINE_STYLE.DASHED},
    },
    # shade the ages below the constitutional minimum
    hspans={
        "ymax": 35,
        "label": "below the minimum age",
        "style": {"plot_hspan_color": "#6c757d", "plot_hspan_alpha": 0.2},
    },
    title="Age of US presidents at inauguration",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=30,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # outside the axes, clear of the points
    legend={"location": LEGEND_LOCATION.OUTSIDE_RIGHT},
).show()
```

```
from statistics import median

periods = list(dict.fromkeys(point["label"] for point in inauguration_ages))
medians = [
    median(point["value"] for point in inauguration_ages if point["label"] == name)
    for name in periods
]
# the even drift from the first group to the last, in years per group
drift = (medians[-1] - medians[0]) / (len(periods) - 1)

SwarmPlot(
    data=inauguration_ages,
    # the line the medians would sit on if the age drifted evenly
    dlines={
        "slope": drift,
        "intercept": medians[0],
        "label": "even drift",
        "style": {"plot_dline_color": "#1d3557", "plot_dline_style": LINE_STYLE.DASHED},
    },
    title="Age of US presidents at inauguration against an even drift",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=30,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    legend={"location": LEGEND_LOCATION.OUTSIDE_RIGHT},
).show()
```

### Text annotations

When the story is a single point, a note says whose it is. `texts` places text on the chart, with an optional `target` that draws a connector to a point; the position is in data coordinates by default (group position, value), or in axes fractions with `"coords": "axes"`, which keeps the note in place whatever the axis limits. The target is a group position and a value, so the connector lands on a point that sits on its group's center line, as a lone extreme usually does. The keys are listed in [TextSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextSettingAttrs), and the [Text Annotations](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/annotations/index.md) guide covers placement, connectors and styling.

```
SwarmPlot(
    data=inauguration_ages,
    # name the youngest and the oldest presidents
    texts=[
        {
            "text": "Theodore Roosevelt, 42",
            "x": 0.22,
            "y": 0.07,
            "coords": "axes",
            "target": (1, 42),
        },
        {
            "text": "Joe Biden and\nDonald Trump, 78",
            "x": 0.62,
            "y": 0.85,
            "coords": "axes",
            "target": (2, 78),
        },
    ],
    title="Age of US presidents at inauguration",
    xlabel="Took office in",
    ylabel="Age (years)",
    # room below the youngest for the note
    ymin=35,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Date labels

Groups are often dates: race days, releases, sampling rounds. A `label` that is a real temporal object (`datetime`, `date`, `numpy.datetime64` or a pandas `Timestamp`) keeps its group position but prints through `xticks_format` (or `yticks_format` for horizontal swarms), a [DATE_FORMAT](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT) member or any `strftime` pattern. `race_times`, defined in a hidden cell, holds the illustrative finishing times (in minutes) of a weekly 5 km community run on six Saturdays, labeled by the date of each run; the day and month are enough to tell the runs apart.

```
SwarmPlot(
    data=race_times,
    title="Finishing times of a weekly 5 km run",
    xlabel="Run",
    ylabel="Time (minutes)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # print the date labels as day and month
    xticks_format="%d %b",
).show()
```

### Swarms over boxes and violins

A swarm shows every observation but leaves the reader to estimate the median and the spread; a box plot draws them but hides the observations. [Panel](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) overlays the two: a [BoxPlot](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/#datachart.charts.BoxPlot) and a `SwarmPlot` of the same data share their group positions, so the points sit on the boxes, and the points draw above them. The box plot's outliers are already in the swarm, so `show_outliers=False` hides them, and muting the box figure with the per-figure `"emphasis"` option lets the points carry the color. The [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) guide covers the per-figure options.

```
from datachart.charts import BoxPlot, ViolinPlot
from datachart.utils import Panel

Panel(
    [
        # the boxes in the background; the swarm already draws the outliers
        {"figure": BoxPlot(data=inauguration_ages, show_outliers=False), "emphasis": EMPHASIS.BACKGROUND},
        SwarmPlot(data=inauguration_ages),
    ],
    title="Age of US presidents at inauguration",
    xlabel="Took office in",
    ylabel_left="Age (years)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

A [ViolinPlot](https://eriknovak.github.io/datachart/dev/references/charts/violinplot/#datachart.charts.ViolinPlot) outlines the shape of each distribution instead. `inner=None` draws the body only, since the swarm already shows where the values sit, and a low alpha keeps the points legible. With five points in the last era the outline is a guess, which is exactly what the points on top reveal.

```
Panel(
    [
        # the body only, faded behind the points
        ViolinPlot(data=inauguration_ages, inner=None, style={"plot_violin_alpha": 0.3}),
        SwarmPlot(data=inauguration_ages),
    ],
    title="Age of US presidents at inauguration",
    xlabel="Took office in",
    ylabel_left="Age (years)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

## Multiple Swarm Plots

To compare datasets over the same groups, pass a list of lists to `data`: each inner list is one series, and the per-series attributes (`subtitle`, `style`, `emphasis`) become lists aligned with it. The series share one category axis, and the swarms of the same group overlay at the same position in distinct colors; `show_legend` names them by their subtitles. `ages_by_party`, defined in a hidden cell, splits the presidencies into the 16 Democratic and the 20 Republican ones (the 11 presidencies of other parties, all in the first era, are left out), and a style per series colors each party in its customary color. The two series are packed separately, so a Democrat and a Republican of the same age land on the same spot; large, translucent points for one series and small, solid points for the other keep both visible.

```
# large, translucent Democrats under small, solid Republicans
PARTY_STYLE = [
    {"plot_swarm_color": PARTY_COLORS[0], "plot_swarm_size": 70, "plot_swarm_alpha": 0.35, "plot_swarm_edge_width": 0},
    {"plot_swarm_color": PARTY_COLORS[1], "plot_swarm_size": 14},
]

SwarmPlot(
    # one series per party
    data=ages_by_party,
    # named for the legend
    subtitle=PARTIES,
    # and colored like the party
    style=PARTY_STYLE,
    title="Age of US presidents at inauguration, by party",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Legend

`show_legend` lists the series; `legend` says where and how, with a `title`, a `location` from [LEGEND_LOCATION](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), the number of columns `ncols`, and the `alignment` of the entries from [LEGEND_ALIGN](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN); a field left out falls back to the theme ([LegendSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.LegendSettingAttrs)). The swarms reach the top corners of the chart, so the legend moves above the axes, titled and with both entries in one row.

```
SwarmPlot(
    data=ages_by_party,
    subtitle=PARTIES,
    style=PARTY_STYLE,
    title="Age of US presidents at inauguration, by party",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # a titled legend above the axes, in one row
    legend={"title": "Party", "location": LEGEND_LOCATION.OUTSIDE_TOP, "ncols": 2},
).show()
```

### Subplots

Overlaid swarms pack separately, so two series at the same group can cover each other, and the size trick above only goes so far. `subplots=True` draws each series in its own panel instead: `subtitle` titles the panels, `title`, `xlabel` and `ylabel` stay global, and `max_cols` limits the panels per row. `sharey=True` puts the panels on one value axis, so an age in one panel compares with an age in the next, and `sharex=True` keeps one category axis for both.

```
SwarmPlot(
    data=ages_by_party,
    subtitle=PARTIES,
    # one color per party, the same point size in both panels
    style=[{"plot_swarm_color": color} for color in PARTY_COLORS],
    title="Age of US presidents at inauguration, by party",
    xlabel="Took office in",
    ylabel="Age (years)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # one panel per party, side by side
    subplots=True,
    # one value axis and one category axis for both panels
    sharex=True,
    sharey=True,
).show()
```

## Additional Features

### Logarithmic scale

Some values span orders of magnitude, and on a linear axis the small ones pile up at the bottom. `scaley` takes a [SCALE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE) member, and the swarm packs the points on the scaled axis, so they stay apart. `days_in_office`, defined in a hidden cell, holds the length of each completed presidency in days, from William Henry Harrison's 31 days to Franklin D. Roosevelt's 4,422 (the current presidency is left out). The log axis spreads the short presidencies, cut short by death or resignation, as clearly as the long ones, and the value labels name the extremes of each era.

```
from datachart.constants import SCALE

SwarmPlot(
    data=days_in_office,
    title="Length of US presidencies",
    xlabel="Took office in",
    ylabel="Days in office",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
    show_values=True,
    # draw the value axis on a logarithmic scale
    scaley=SCALE.LOG,
    # ticks at readable round numbers
    yticks=[30, 100, 300, 1000, 3000],
    ymin=20,
).show()
```

### Custom data keys

Data that comes from a file or an API rarely uses the `label` and `value` keys, and renaming every record just to plot it is a chore. Instead, tell `SwarmPlot` which keys to read with the `label` and `value` arguments. `president_records` stores the presidencies the way a CSV export would, one record per presidency with a `name`, an `era` and an `age` key:

```
president_records = [
    {"name": name, "era": era(took), "age": age_on(born, took)}
    for name, _, born, took, _ in PRESIDENCIES
]
president_records[:2]
```

```
SwarmPlot(
    data=president_records,
    # the keys that hold the group and the value
    label="era",
    value="age",
    title="Age of US presidents at inauguration",
    xlabel="Took office in",
    ylabel="Age (years)",
    ymin=40,
    ymax=80,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

## Real-World Examples

The examples below put the features above to work on realistic data, each one answering a question. The data lives in hidden cells; each example says what its data is and where it comes from.

### Example 1: Which Services Breach the SLA? (Strip Mode, Log Scale and an SLA Line)

`response_times` holds the illustrative response times (in ms) of 300 requests to each of four services, drawn from a seeded log-normal generator: most requests are fast, and a long tail of slow ones stretches each distribution. The question is which services break the 500 ms service level agreement (SLA), and how often. With 1,200 points a swarm would overflow its category, so the strip mode scatters them instead, with small, translucent points so the dense regions read darker. On a log axis the tail reads at the same resolution as the bulk, and a shaded band above the SLA line holds the requests that breach it.

```
SwarmPlot(
    data=response_times,
    # scatter the many points across the category width
    mode=SWARM_MODE.STRIP,
    # small, translucent points
    style={"plot_swarm_size": 6, "plot_swarm_alpha": 0.4, "plot_swarm_edge_width": 0},
    # the long tail reads at the same resolution as the bulk
    scaley=SCALE.LOG,
    # the SLA, and the requests that breach it
    hlines={
        "y": SLA_MS,
        "label": f"SLA ({SLA_MS} ms)",
        "style": {"plot_hline_color": "#c1121f", "plot_hline_style": LINE_STYLE.DASHED},
    },
    hspans={
        "ymin": SLA_MS,
        "style": {"plot_hspan_color": "#c1121f", "plot_hspan_alpha": 0.08},
    },
    title=f"Response time of {N_REQUESTS} requests per service",
    xlabel="Service",
    ylabel="Response time (ms)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    legend={"location": LEGEND_LOCATION.UPPER_LEFT},
).show()
```

### Example 2: Which Months Bring Frost? (Horizontal Swarms, a Rule and a Frost Band)

`daily_temperatures` holds one year of illustrative daily mean temperatures (in °C) in Ljubljana, drawn from a seeded generator around the city's published 1991–2020 monthly climate normals, with larger day-to-day swings in winter. The question is which months bring freezing days. Twelve labeled swarms read best top to bottom, so the swarms are horizontal and the data is reversed to put January on top. A band shades the temperatures below zero, so the frost days are the points inside it, and `emphasis_rule` highlights the months whose coldest day fell below freezing, through the `"min"` summary.

```
SwarmPlot(
    # reversed, so January ends up at the top
    data=daily_temperatures[::-1],
    orientation=ORIENTATION.HORIZONTAL,
    style={"plot_swarm_size": 8},
    # the months whose coldest day was below zero
    emphasis_rule={"below": 0, "by": "min"},
    # shade the freezing temperatures
    vspans={
        "xmax": 0,
        "label": "below freezing",
        "style": {"plot_vspan_color": "#4c72b0", "plot_vspan_alpha": 0.12},
    },
    title="Daily mean temperature in Ljubljana",
    xlabel="Temperature (°C)",
    ylabel="Month",
    figsize=FIG_SIZE.FULL_TALL,
    show_grid=SHOW_GRID.X,
    show_legend=True,
    legend={"location": LEGEND_LOCATION.LOWER_RIGHT},
).show()
```

### Example 3: Is the Best Model Better, or Just Luckier? (Box Overlay, Emphasis and a Note)

`benchmark` holds the illustrative test accuracy of five models, each trained with 10 random seeds, drawn from a seeded generator. Ten runs per model is a small sample, and the question is whether the model with the best single run is also the most reliable. A box plot alone hides the runs; the swarm on top shows every one, so a tight cluster reads apart from a wide one. [Panel](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) overlays the two, the same `emphasis` roles on both figures highlight the two leading models and mute the rest, and [Annotate](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Annotate) adds a note to the finished panel, pointing at the single best run.

```
from datachart.utils import Annotate

LEADERS = ["Deep", "Deep + aug."]
roles = [EMPHASIS.HIGHLIGHT if model in LEADERS else EMPHASIS.BACKGROUND for model in MODELS]

panel = Panel(
    [
        BoxPlot(data=benchmark, show_outliers=False, emphasis=roles),
        # the same roles align with the same models in both figures
        SwarmPlot(data=benchmark, emphasis=roles),
    ],
    title=f"Test accuracy across {N_SEEDS} seeds",
    xlabel="Model",
    ylabel_left="Test accuracy",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
)

# point at the single best run; groups sit at positions 0, 1, 2, ...
position = list(MODELS).index(BEST_RUN["label"])
Annotate(
    panel,
    texts={
        "text": f"best single run ({BEST_RUN['value']:.3f}),\nbut the widest spread",
        "x": 0.2,
        "y": 0.9,
        "coords": "axes",
        "target": (position, BEST_RUN["value"]),
    },
).show()
```
