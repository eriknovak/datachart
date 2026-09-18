# Line Chart

A line chart connects ordered points to show how a value moves along a continuous axis, usually time: trends, growth, seasons, and how the trajectories of several series compare. This guide shows how to create line charts with the [datachart.charts.LineChart](https://eriknovak.github.io/datachart/0.10.1/references/charts/linechart/#datachart.charts.LineChart) function, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-line-chart), which maps common tasks to the parameter or style attribute that does the job.

```
from datachart.charts import LineChart
```

## Basics

The examples in this guide share one dataset: the global mean surface temperature anomaly, the difference of each year's global average from the 1951–1980 mean in °C, from 1880 to 2024 (source: NASA GISS Surface Temperature Analysis, GISTEMP v4, rounded to two decimals). The data lives in a hidden cell. `warming` holds the yearly anomaly as one data point per year, and `warming_by_hemisphere` holds one series each for the Northern and Southern Hemisphere over the same years, with the year-to-year spread of each five-year window as `yerr`. The series is famous for a reason: it starts flat, wobbles for a century, and then climbs, and every customization below helps to read that.

Each data point is a dictionary with an `x` value (here the year) and a `y` value:

```
warming[:3]
```

**Basic example.** Only the `data` argument is required to draw the line chart:

```
LineChart(
    # add the data to the chart
    data=warming
).show()
```

## Customizing the Line Chart

Every customization is either a keyword argument of `LineChart` or a `plot_line_*` / `plot_area_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                              | Use                                                                   | See                                                                                                        |
| --------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| add a title and axis labels             | `title`, `xlabel`, `ylabel`                                           | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| set custom tick positions and labels    | `xticks`, `xticklabels`, `yticks`, `yticklabels`                      | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| format the tick labels                  | `xticks_format`, `yticks_format`                                      | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| fix the axis range                      | `xmin`, `xmax`, `ymin`, `ymax`                                        | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| resize the figure                       | `figsize`                                                             | [Figure size and grid](#figure-size-and-grid)                                                              |
| show grid lines                         | `show_grid`                                                           | [Figure size and grid](#figure-size-and-grid)                                                              |
| fix the aspect ratio of the axes        | `aspect_ratio`                                                        | [Figure size and grid](#figure-size-and-grid)                                                              |
| change the line color, width, or dashes | `style={"plot_line_color": ..., "plot_line_style": ...}`              | [Line style](#line-style)                                                                                  |
| mark the data points                    | `style={"plot_line_marker": ...}`                                     | [Line style](#line-style)                                                                                  |
| draw the line as steps                  | `style={"plot_line_drawstyle": ...}`                                  | [Line style](#line-style)                                                                                  |
| fill the area under the line            | `show_area`, `style={"plot_area_color": ..., "plot_area_alpha": ...}` | [Area under the line](#area-under-the-line)                                                                |
| print the value beside the points       | `show_values`, `value_format`, `value_step`                           | [Value labels](#value-labels)                                                                              |
| mark a threshold or an event            | `hlines`, `vlines`                                                    | [Reference lines](#reference-lines)                                                                        |
| shade a period or a range               | `hspans`, `vspans`                                                    | [Reference bands](#reference-bands)                                                                        |
| put a note on the chart                 | `texts`                                                               | [Text annotations](#text-annotations)                                                                      |
| compare several series in one chart     | `data` as a list of lists, `subtitle`, `show_legend`                  | [Multiple Line Charts](#multiple-line-charts)                                                              |
| highlight one series, mute the rest     | `emphasis`, `emphasis_rule`                                           | [Emphasis](#emphasis)                                                                                      |
| title and place the legend              | `legend`                                                              | [Legend](#legend)                                                                                          |
| draw a confidence band                  | `yerr` in `data`, `show_yerr`                                         | [Confidence interval](#confidence-interval)                                                                |
| draw each series in its own subplot     | `subplots`, `sharex`, `sharey`, `max_cols`                            | [Subplots](#subplots)                                                                                      |
| plot against real dates                 | `datetime` objects as `x`, `xticks_format`                            | [Datetime axis](#datetime-axis)                                                                            |
| use a logarithmic axis                  | `scaley`, `scalex`                                                    | [Axis scales](#axis-scales)                                                                                |
| plot data with other key names          | `x`, `y`, `yerr`                                                      | [Custom data keys](#custom-data-keys)                                                                      |
| save the chart to a file                | `save_figure`                                                         | [Saving Figures](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/utility/saving/index.md) guide |

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.1/references/constants/index.md) that lists its values:

| Parameter                                    | Constant                                                                                                                                                                                                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                      |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                      |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                    |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                              |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                              |
| `scalex`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.DATE_FORMAT)         |

The full list of style attributes is in the [datachart.typings.LineStyleAttrs](https://eriknovak.github.io/datachart/0.10.1/references/charts/linechart/#datachart.typings.LineStyleAttrs) and [datachart.typings.AreaStyleAttrs](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.AreaStyleAttrs) types; the full list of parameters is in the [datachart.charts.LineChart](https://eriknovak.github.io/datachart/0.10.1/references/charts/linechart/#datachart.charts.LineChart) reference.

### Title, axis labels and ticks

A line without a title and axis labels is a shape, not a statement; `title`, `xlabel` and `ylabel` say what moves and in what unit. The ticks are the reader's ruler: `xticks` and `yticks` set their positions (`xticklabels` and `yticklabels` replace the labels), `xticks_format` and `yticks_format` format them (a [VALUE_FORMAT](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT) member or a `"{x:.1f}"` style string on a value axis), and `xtickrotate` and `ytickrotate` tilt them. `xmin`, `xmax`, `ymin` and `ymax` fix the axis range, so the chart shows the span you mean rather than the span of the data. Here the years tick every twenty years, the anomaly prints with a sign, and the range is symmetric around zero, where the anomaly is defined.

```
LineChart(
    data=warming,
    # add the title
    title="Global mean surface temperature anomaly",
    # add the x and y axis labels
    xlabel="Year",
    ylabel="Anomaly (°C, vs. 1951–1980)",
    # a tick every twenty years, values printed with a sign
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    # a range symmetric around zero
    ymin=-0.6,
    ymax=1.4,
    xmin=1880,
    xmax=2025,
).show()
```

### Figure size and grid

A long time series wants a wide, short figure, so the years have room and the slope stays honest. `figsize` takes a `(width, height)` tuple in inches or one of the presets in [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.FIG_SIZE), sized for a full or half page width. Grid lines let the eye carry a point across to the axis; `show_grid` draws them with a [SHOW_GRID](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SHOW_GRID) member, `Y` for the value axis alone, `X` for the time axis, `BOTH` for both. `aspect_ratio` fixes the ratio of the axes rather than of the figure, one data unit the same length on both axes with [ASPECT_RATIO.EQUAL](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.ASPECT_RATIO); a time series never needs it, but the [ROC curve](#example-1-a-roc-curve-custom-data-keys-and-an-equal-aspect-ratio) below does.

```
from datachart.constants import FIG_SIZE, SHOW_GRID

LineChart(
    data=warming,
    title="Global mean surface temperature anomaly",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    # a wide, short figure
    figsize=FIG_SIZE.FULL_SHORT,
    # grid lines along both axes
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Line style

The `style` dictionary sets the look of the line: its color and alpha, its width, its dash pattern from [LINE_STYLE](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LINE_STYLE), a marker at each point from [LINE_MARKER](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LINE_MARKER), and the draw style from [LINE_DRAW_STYLE](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LINE_DRAW_STYLE); the attributes are listed in [datachart.typings.LineStyleAttrs](https://eriknovak.github.io/datachart/0.10.1/references/charts/linechart/#datachart.typings.LineStyleAttrs), and any attribute left out keeps the value of the active theme. The look should follow the data. A hundred and forty-five yearly values are a dense series, so a thin line without markers reads best; the example draws it thin and in a warm color, and the [next section](#area-under-the-line) shows where markers and steps earn their place.

```
from datachart.constants import LINE_STYLE, LINE_MARKER, LINE_DRAW_STYLE

LineChart(
    data=warming,
    # a thin line in a warm color
    style={
        "plot_line_color": "#c1121f",
        "plot_line_width": 1.2,
    },
    title="Global mean surface temperature anomaly",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
).show()
```

Averages over a period are one value per period rather than a continuous curve, and a step line says so. `decades`, the mean anomaly of each decade, is sparse enough for markers and better drawn as steps: `LINE_DRAW_STYLE.STEPS_MID` centers each step on its point, and a dashed pattern marks the series as derived.

```
# the mean anomaly of each full decade, placed at the middle of the decade
decades = [
    {"x": start + 5, "y": round(sum(ANOMALY[i : i + 10]) / 10, 2)}
    for i, start in enumerate(YEARS)
    if start % 10 == 0 and i + 10 <= len(ANOMALY)
]

LineChart(
    data=decades,
    style={
        # one value per decade: steps centered on the points, marked and dashed
        "plot_line_drawstyle": LINE_DRAW_STYLE.STEPS_MID,
        "plot_line_marker": LINE_MARKER.CIRCLE,
        "plot_line_style": LINE_STYLE.DASHED,
    },
    title="Mean temperature anomaly by decade",
    xlabel="Decade",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Area under the line

Filling the area under a line turns a trajectory into a quantity: the fill draws the eye to how much has accumulated, not only where the line is. `show_area` fills between the line and the bottom of the axes in the color of the line at a lower alpha; `plot_area_color`, `plot_area_alpha` and `plot_area_hatch` from [datachart.typings.AreaStyleAttrs](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.AreaStyleAttrs) override that. A fill measures from the bottom of the axes, so the axes must start where the measure starts: the anomaly has not been below zero since 1976, so `warming_recent`, the series from 1977 on, sits on a value axis pinned at zero and the fill measures the warming above the reference period.

```
# the years since the anomaly was last below zero
warming_recent = [point for point in warming if point["x"] >= 1977]

LineChart(
    data=warming_recent,
    style={
        "plot_line_color": "#c1121f",
        # a stronger fill than the theme default
        "plot_area_alpha": 0.3,
    },
    title="Global mean surface temperature anomaly since 1977",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1980, 2025, 10)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    # fill down to the zero line
    show_area=True,
    ymin=0,
    xmin=1977,
    xmax=2024,
).show()
```

### Value labels

Where the exact values matter, `show_values` prints the value beside each point; `value_format` formats it (a [VALUE_FORMAT](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.VALUE_FORMAT) member or any `"{x:.1f}"`, `"{:.1f}%"` or `"%g"` style string) and `value_step` labels every Nth point when the series is too dense to label them all; by default the step is chosen so that neighbouring labels stay apart. Each label sits above or below its point, wherever it overlaps least, and takes the `plot_value_*` style of the active theme ([ValueLabelStyleAttrs](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.ValueLabelStyleAttrs)). Labeling every yearly value would be noise; labeling the decade means, with the sign, states the trend in numbers.

```
from datachart.constants import VALUE_FORMAT

LineChart(
    data=decades,
    style={"plot_line_marker": LINE_MARKER.CIRCLE},
    title="Mean temperature anomaly by decade",
    xlabel="Decade",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # print every decade's value, with its sign
    show_values=True,
    value_format="{x:+.2f}",
    value_step=1,
    ymin=-0.6,
    ymax=1.4,
).show()
```

### Reference lines

A reference line gives the reader something to measure the line against: a threshold it must not cross, or the moment something happened. `hlines` draws a horizontal line at a value and `vlines` a vertical one at an x position, each a dictionary or a list of them with the position, an optional `label` for the legend and a `style`; the keys are listed in [HLineSettingAttrs](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.HLineSettingAttrs) and [VLineSettingAttrs](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.VLineSettingAttrs). The x position is in data coordinates, so a line can sit anywhere along the axis. The example marks the 1.5 °C of the Paris Agreement, which is measured against pre-industrial levels and lands near 1.2 °C on this 1951–1980 baseline, and the year the Agreement was adopted.

```
# 1.5 °C above pre-industrial, about 0.3 °C below the 1951-1980 mean used here
PARIS_LIMIT = 1.2
PARIS_YEAR = 2015

LineChart(
    data=warming,
    subtitle="anomaly",
    # a dashed line at the limit
    hlines={
        "y": PARIS_LIMIT,
        "label": "1.5 °C above pre-industrial",
        "style": {"plot_hline_color": "#c1121f", "plot_hline_style": LINE_STYLE.DASHED},
    },
    # a dotted line at the year of the Agreement
    vlines={
        "x": PARIS_YEAR,
        "label": "Paris Agreement",
        "style": {"plot_vline_color": "#555555", "plot_vline_style": LINE_STYLE.DOTTED},
    },
    title="Global mean surface temperature anomaly",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Reference bands

Where a line marks a value, a band marks a range: a period, a tolerance, an interval the line should stay in. `hspans` shades between two values and `vspans` between two x positions, each a dictionary or a list of them with the bounds, an optional `label` and a `style`; the keys are listed in [HSpanSettingAttrs](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.HSpanSettingAttrs) and [VSpanSettingAttrs](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.VSpanSettingAttrs). At least one bound is required and an omitted bound runs to the axis edge, so `{"xmin": 2000}` shades everything from 2000 to the right. The band sits over the grid and under the line, so the data stays readable through it. The example shades the reference period the anomaly is measured against and the range of the anomaly within it.

```
BASELINE = (1951, 1980)
baseline_values = [a for y, a in zip(YEARS, ANOMALY) if BASELINE[0] <= y <= BASELINE[1]]

LineChart(
    data=warming,
    subtitle="anomaly",
    # shade the reference period
    vspans={"xmin": BASELINE[0], "xmax": BASELINE[1], "label": "reference period"},
    # and the range of the anomaly within it
    hspans={
        "ymin": min(baseline_values),
        "ymax": max(baseline_values),
        "label": "reference range",
        "style": {"plot_hspan_color": "#2a9d8f"},
    },
    title="Global mean surface temperature anomaly",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Text annotations

A line has moments worth naming: a record, a turn, an outlier. `texts` places a note on the chart, with an optional `target` to draw a connector to a data point; the position is in data coordinates by default or in axes fractions with `"coords": "axes"`, which keeps the note in place whatever the axis limits. The [Text Annotations](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/utility/annotations/index.md) guide covers placement, connector looks and styling. The example names the warmest year on record and the last year below the reference mean.

```
RECORD = max(warming, key=lambda point: point["y"])
LAST_BELOW = max((point for point in warming if point["y"] < 0), key=lambda point: point["x"])

LineChart(
    data=warming,
    texts=[
        {
            "text": f"{RECORD['x']}: warmest year on record",
            "x": 0.55,
            "y": 0.85,
            "coords": "axes",
            "target": (RECORD["x"], RECORD["y"]),
        },
        {
            "text": f"{LAST_BELOW['x']}: last year below the reference mean",
            "x": 0.05,
            "y": 0.62,
            "coords": "axes",
            "target": (LAST_BELOW["x"], LAST_BELOW["y"]),
        },
    ],
    title="Global mean surface temperature anomaly",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
).show()
```

## Multiple Line Charts

To compare several series, pass a list of lists to `data`: each inner list is one line, and the per-series attributes (`subtitle`, `style`, `emphasis`) become lists aligned with it. `warming_by_hemisphere` is such a list, one series per hemisphere, and `subtitle` names them for the legend. A single `style` dictionary applies to every line; a list styles each line separately, with `None` keeping the theme style for that line. The two hemispheres move together for a century and then part, the north warming faster; on one chart the gap is the message.

```
LineChart(
    # one series per hemisphere
    data=warming_by_hemisphere,
    # named for the legend
    subtitle=HEMISPHERES,
    # one style per line
    style=[
        {"plot_line_color": "#c1121f"},
        {"plot_line_color": "#1d3557"},
    ],
    title="Temperature anomaly by hemisphere",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Emphasis

When a chart carries several series, the story is usually about one of them, and emphasis makes it visible. `emphasis` takes one role per series, aligned with `data`: `"highlight"` thickens a line and brings it to the front, `"background"` mutes it (the theme's muted color at a lower alpha, thinner, behind the others, and out of the legend), and `None` leaves it as it is. The roles are also available as the [EMPHASIS](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.EMPHASIS) constants, and the [Highlighting](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/styling/highlighting/index.md) guide covers emphasis across every chart type and theme. With the global series added as context, the example highlights the Northern Hemisphere against the other two.

```
LineChart(
    data=[warming] + warming_by_hemisphere,
    subtitle=["Global"] + HEMISPHERES,
    # highlight the north, mute the rest
    emphasis=["background", "highlight", "background"],
    title="Temperature anomaly, the Northern Hemisphere against the rest",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

`emphasis_rule` picks the lines from the data instead of naming them. It is a one-key dictionary, `{"top": n}`, `{"bottom": n}`, `{"above": v}`, `{"below": v}` (strict) or `{"between": (lo, hi)}` (inclusive), read against a summary of each line's own `y` values: the mean by default, or the `"median"`, `"min"`, `"max"` or `"sum"` named by an extra `"by"` key. The lines that match are highlighted and the rest muted, and an explicit `emphasis` role wins over the rule. Asking for the line that warmed least, the lowest mean, needs no knowledge of which one it is:

```
LineChart(
    data=[warming] + warming_by_hemisphere,
    subtitle=["Global"] + HEMISPHERES,
    # the one line with the lowest mean
    emphasis_rule={"bottom": 1},
    title="Temperature anomaly, the series that warmed least",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Legend

`show_legend` lists the series; `legend` says where and how, with a `title`, a `location` from [LEGEND_LOCATION](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LEGEND_LOCATION), the number of columns `ncols`, and the `alignment` of the entries from [LEGEND_ALIGN](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.LEGEND_ALIGN); a field left out falls back to the theme ([LegendSettingAttrs](https://eriknovak.github.io/datachart/0.10.1/references/typings/#datachart.typings.LegendSettingAttrs)). A rising series leaves its empty corner at the top left, which is where the legend goes.

```
from datachart.constants import LEGEND_LOCATION

LineChart(
    data=warming_by_hemisphere,
    subtitle=HEMISPHERES,
    title="Temperature anomaly by hemisphere",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # a titled legend in the empty corner
    legend={"title": "Hemisphere", "location": LEGEND_LOCATION.UPPER_LEFT},
).show()
```

### Confidence interval

A mean without its spread overstates what is known. When each data point carries a `yerr`, `show_yerr` draws a band from `y - yerr` to `y + yerr` around the line, styled with the same `plot_area_*` attributes as the area under the line. The hemisphere series carry the spread of each five-year window as `yerr`, and the bands show that the two hemispheres are indistinguishable until the late twentieth century, when the bands part.

```
LineChart(
    data=warming_by_hemisphere,
    subtitle=HEMISPHERES,
    style=[
        {"plot_line_color": "#c1121f"},
        {"plot_line_color": "#1d3557"},
    ],
    title="Temperature anomaly by hemisphere, with the five-year spread",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # draw the spread as a band around each line
    show_yerr=True,
).show()
```

### Subplots

Lines that cross and overlap hide each other, and when the question is the shape of each series rather than the gap between them, `subplots=True` draws each in its own panel: `subtitle` titles the panels, `title`, `xlabel` and `ylabel` stay global, and `max_cols` limits the panels per row. `sharex=True` and `sharey=True` put the panels on common axes, so a slope in one panel is the same slope in the next; without them each panel scales to its own data, and the slower-warming south would look as steep as the north.

```
LineChart(
    data=warming_by_hemisphere,
    subtitle=HEMISPHERES,
    style=[
        {"plot_line_color": "#c1121f"},
        {"plot_line_color": "#1d3557"},
    ],
    title="Temperature anomaly by hemisphere",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 50)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # one panel per hemisphere, side by side, on common axes
    subplots=True,
    max_cols=2,
    sharex=True,
    sharey=True,
).show()
```

## Additional Features

### Datetime axis

Yearly data sits fine on a numeric axis, but daily or monthly data wants a real time axis, where points land at their elapsed time and the ticks label themselves sensibly. An `x` value that is a real temporal object (a `datetime`, a `date`, a `numpy.datetime64` or a pandas `Timestamp`) does exactly that: the ticks pick a concise, non-repeating label for the visible span, with the part every label shares (such as `2024-Apr`) as an offset. Date strings such as `"2024-03-01"` are **not** parsed; they draw as unordered categories, like any other string. `daily_index` holds sixty days of an illustrative index level.

```
from datetime import date, timedelta

# daily closing level of an index over one spring (illustrative)
start = date(2024, 3, 1)
daily_index = [
    {"x": start + timedelta(days=i), "y": 100 + round(2.5 * i - 0.05 * i * i, 1)}
    for i in range(60)
]

LineChart(
    data=daily_index,
    title="Daily index level",
    xlabel="Date",
    ylabel="Level",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

On a time axis everything that takes an x position takes a date: `xticks`, `xmin` and `xmax`, reference lines and bands, and annotation targets. `xticks_format` labels the ticks with a [DATE_FORMAT](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.DATE_FORMAT) member or any `strftime` pattern instead of the automatic labels. The example fixes the ticks to the first and the fifteenth of each month, marks a rebalancing date, and shades an earnings season.

```
from datachart.constants import DATE_FORMAT

LineChart(
    data=daily_index,
    title="Daily index level",
    xlabel="Date",
    ylabel="Level",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # ticks, limits, lines and bands all take dates
    xticks_format=DATE_FORMAT.MONTH_DAY,
    xticks=[date(2024, 3, 1), date(2024, 3, 15), date(2024, 4, 1), date(2024, 4, 15)],
    xmin=date(2024, 3, 1),
    xmax=date(2024, 4, 20),
    vlines={"x": date(2024, 3, 20), "label": "rebalance"},
    vspans={"xmin": date(2024, 4, 1), "xmax": date(2024, 4, 10), "label": "earnings season"},
    yticks_format=VALUE_FORMAT.INTEGER,
    show_legend=True,
).show()
```

### Axis scales

A quantity that grows by a constant factor looks like a hockey stick on a linear axis and like a straight line on a logarithmic one, and only the second lets the reader judge whether the growth rate changed. `scaley` and `scalex` take a [SCALE](https://eriknovak.github.io/datachart/0.10.1/references/constants/#datachart.constants.SCALE) member: `LINEAR`, `LOG`, `SYMLOG` (log on both sides of zero) or `ASINH`. `transistors`, defined in a hidden cell, holds the transistor count of a representative microprocessor per year from the Intel 4004 (1971) to the Apple M1 Ultra (2022), Moore's law in sixteen data points rounded from the manufacturers' figures. On a linear scale the first forty years collapse onto the x-axis; on a log scale the doubling every two years becomes the straight line it is famous for.

```
from datachart.constants import SCALE

for scale in [SCALE.LINEAR, SCALE.LOG]:
    LineChart(
        data=transistors,
        style={"plot_line_marker": LINE_MARKER.CIRCLE},
        title=f"Transistors per microprocessor on the '{scale}' scale",
        xlabel="Year",
        ylabel="Transistors",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.BOTH,
        # the scale of the value axis
        scaley=scale,
    ).show()
```

### Custom data keys

Data that comes from a file or an API rarely uses the `x`, `y` and `yerr` keys, and renaming every record just to plot it is a chore. Instead, tell `LineChart` which keys to read with the `x`, `y` and `yerr` arguments. `readings` stores the Northern Hemisphere series the way a data export might, under `year`, `anomaly` and `spread`:

```
readings = [
    {"year": point["x"], "anomaly": point["y"], "spread": point["yerr"]}
    for point in warming_by_hemisphere[0]
]
readings[:3]
```

```
LineChart(
    data=readings,
    # the keys that hold the x, y and error values
    x="year",
    y="anomaly",
    yerr="spread",
    title="Northern Hemisphere temperature anomaly",
    xlabel="Year",
    ylabel="Anomaly (°C)",
    xticks=list(range(1880, 2025, 20)),
    yticks_format="{x:+.1f}",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_yerr=True,
).show()
```

## Real-World Examples

The examples below put the features above to work on real or realistic data, each one answering a question. The data lives in hidden cells; each example says what its data is and where it comes from.

### Example 1: A ROC Curve (Custom Data Keys and an Equal Aspect Ratio)

`roc_curves` holds the receiver operating characteristic of two illustrative binary classifiers: each point is the false positive rate (`fp`) and the true positive rate (`tp`) at one decision threshold, so the keys are mapped with the `x` and `y` arguments. The question is which classifier separates the classes better, and the answer is the area under each curve. A ROC curve is read against the diagonal of chance, so the axes keep an equal aspect ratio, and the area under each curve is filled with a hatch and its size printed in the subtitle; the subplots share both axes so the two areas compare.

```
from datachart.constants import ASPECT_RATIO, HATCH_STYLE

LineChart(
    data=roc_curves,
    # name each curve by its area
    subtitle=[f"{name} (AUC {auc(points):.2f})" for name, points in ROC_POINTS.items()],
    # the points are stored as "fp" and "tp", instead of "x" and "y"
    x="fp",
    y="tp",
    # hatch the area under each curve (a single style applies to every chart)
    style={"plot_area_hatch": HATCH_STYLE.DIAGONAL},
    title="ROC curves",
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
    # one unit the same length on both axes
    aspect_ratio=ASPECT_RATIO.EQUAL,
).show()
```

### Example 2: Training Runs (A Confidence Band on a Log Scale, and the Best Run Picked by a Rule)

`training_loss` holds the validation loss of three illustrative training methods, evaluated every five steps over 200 steps and averaged over several runs, with the standard deviation across the runs as `spread`. The question is which method converges lowest, and whether the runs agree. The loss decays toward a floor, so a log value axis keeps the late-training differences readable; `show_yerr` draws the run-to-run spread as a band around each mean; and `emphasis_rule` highlights the method with the lowest final loss without naming it, so the same cell keeps working when the methods change.

```
LineChart(
    data=training_loss,
    subtitle=list(LOSS_CURVES),
    # the points are stored as "step", "loss" and "spread"
    x="step",
    y="loss",
    yerr="spread",
    # the method with the lowest final loss
    emphasis_rule={"bottom": 1, "by": "min"},
    title="Validation loss during training",
    xlabel="Training step",
    ylabel="Validation loss",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # draw the run-to-run spread as a band
    show_yerr=True,
    # a log value axis
    scaley=SCALE.LOG,
).show()
```

### Example 3: Did the Campaign Work? (Reference Lines, a Band, a Note, and a Panel)

`weekly_visitors` holds sixteen weeks of illustrative weekly unique visitors of a website, and `weekly_signups` the sign-ups of the same weeks. A marketing campaign ran from week 7 to week 10, and the hosting plan is sized for 60,000 weekly visitors. The chart has to answer two questions at once, whether the campaign moved the numbers and when the plan needs upgrading: a band shades the campaign weeks, a line marks the capacity, and a note names the week it was first exceeded. Visitors and sign-ups live on different scales, so [Panel](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/utility/panel/index.md) overlays the two line charts with the sign-ups on a second value axis; the reference marks, declared on the visitor chart, travel with it.

```
from datachart.utils import Panel

visitors = LineChart(
    data=weekly_visitors,
    subtitle="unique visitors (thousands)",
    style={"plot_line_marker": LINE_MARKER.CIRCLE},
    # shade the campaign weeks
    vspans={"xmin": CAMPAIGN[0], "xmax": CAMPAIGN[1], "label": "campaign"},
    # mark the hosting capacity
    hlines={
        "y": CAPACITY,
        "label": "hosting capacity",
        "style": {"plot_hline_color": "#c1121f", "plot_hline_style": LINE_STYLE.DASHED},
    },
    # name the week the capacity was first exceeded
    texts={
        "text": f"over capacity in week {OVER_CAPACITY['x']}",
        "x": 0.05,
        "y": 0.85,
        "coords": "axes",
        "target": (OVER_CAPACITY["x"], OVER_CAPACITY["y"]),
    },
)
signups = LineChart(
    data=weekly_signups,
    subtitle="sign-ups",
    style={"plot_line_color": "#2a9d8f", "plot_line_style": LINE_STYLE.DASHED},
)

Panel(
    [
        {"figure": visitors, "y_axis": "left"},
        {"figure": signups, "y_axis": "right"},
    ],
    title="Weekly website traffic around the campaign",
    xlabel="Week",
    ylabel_left="Visitors (thousands)",
    ylabel_right="Sign-ups",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    ymin=0,
    ymin_right=0,
).show()
```
