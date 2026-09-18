# Histogram

A histogram sorts the values of one numeric variable into bins and counts them, so it answers *what shape does this distribution have*: where the values pile up, how widely they spread, whether they lean to one side, have two peaks, or trail off into outliers. This guide shows how to create histograms with the [datachart.charts.Histogram](https://eriknovak.github.io/datachart/0.10.0/references/charts/histogram/#datachart.charts.Histogram) function, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-histogram), which maps common tasks to the parameter or style attribute that does the job.

```
from datachart.charts import Histogram
```

## Basics

The examples in this guide share one dataset: the flipper length, in millimeters, of the 342 penguins measured on three islands of the Palmer Archipelago, Antarctica (source: the [Palmer penguins](https://allisonhorst.github.io/palmerpenguins/) dataset, Gorman, Williams and Fraser 2014, released under CC0). The data lives in a hidden cell. `penguins` holds one data point per penguin, and `penguins_by_species` holds one list per species (Adelie, Chinstrap and Gentoo, in the order of `SPECIES`). The pooled flipper lengths hide a story: they come from three species of different build, and the histogram shows it as two peaks that the customizations below bring out.

Each data point is a dictionary with an `x` value, here the flipper length, which the histogram bins and counts. Other keys, such as the species, are carried along and ignored:

```
penguins[:3]
```

**Basic example.** Only the `data` argument is required. The values are split into 20 equal-width bins by default, and the two peaks are already visible:

```
Histogram(
    # add the data to the chart
    data=penguins
).show()
```

## Customizing the Histogram

Every customization is either a keyword argument of `Histogram` or a `plot_hist_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                   | Use                                                           | See                                                                                                        |
| -------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| add a title and axis labels                  | `title`, `xlabel`, `ylabel`                                   | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| set tick positions, labels, and rotation     | `xticks`, `xticklabels`, `xtickrotate` (and the `y` versions) | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| fix the axis range                           | `xmin`, `xmax`, `ymin`, `ymax`                                | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                               |
| resize the figure                            | `figsize`                                                     | [Figure size and grid](#figure-size-and-grid)                                                              |
| show grid lines                              | `show_grid`                                                   | [Figure size and grid](#figure-size-and-grid)                                                              |
| fix the aspect ratio of the axes             | `aspect_ratio`                                                | [Figure size and grid](#figure-size-and-grid)                                                              |
| change how finely the values are binned      | `num_bins`                                                    | [Number of bins](#number-of-bins)                                                                          |
| draw the bins as bars or a step outline      | `style={"plot_hist_type": ...}`                               | [Histogram style](#histogram-style)                                                                        |
| change the color, hatch, or edge of the bins | `style={"plot_hist_color": ..., "plot_hist_hatch": ...}`      | [Histogram style](#histogram-style)                                                                        |
| draw the bars horizontally                   | `orientation`                                                 | [Orientation](#orientation)                                                                                |
| print the count at the top of each bin       | `show_values`, `value_format`                                 | [Value labels](#value-labels)                                                                              |
| mark a mean, a median, or a cut-off          | `vlines`, `hlines`                                            | [Reference lines and bands](#reference-lines-and-bands)                                                    |
| shade a range of values                      | `vspans`, `hspans`                                            | [Reference lines and bands](#reference-lines-and-bands)                                                    |
| put a note on the chart                      | `texts`                                                       | [Text annotations](#text-annotations)                                                                      |
| compare several distributions in one chart   | `data` as a list of lists, `subtitle`, `style`, `show_legend` | [Multiple Histograms](#multiple-histograms)                                                                |
| stack or overlay the series                  | `bar_mode`                                                    | [Bar mode](#bar-mode)                                                                                      |
| highlight one series, mute the rest          | `emphasis`, `emphasis_rule`                                   | [Emphasis](#emphasis)                                                                                      |
| title and place the legend                   | `legend`                                                      | [Legend](#legend)                                                                                          |
| draw each series in its own subplot          | `subplots`, `sharex`, `sharey`, `max_cols`                    | [Subplots](#subplots)                                                                                      |
| compare samples of different sizes           | `show_density`                                                | [Density view](#density-view)                                                                              |
| overlay a smooth density curve               | `stats.kde1d`, `LineChart`, `Panel`                           | [Density curve](#density-curve)                                                                            |
| read off how many values fall below a value  | `show_cumulative`                                             | [Cumulative view](#cumulative-view)                                                                        |
| use a logarithmic axis                       | `scaley`, `scalex`                                            | [Axis scales](#axis-scales)                                                                                |
| plot data with other key names               | `x`                                                           | [Custom data keys](#custom-data-keys)                                                                      |
| save the chart to a file                     | `save_figure`                                                 | [Saving Figures](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/utility/saving/index.md) guide |

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.0/references/constants/index.md) that lists its values:

| Parameter                                    | Constant                                                                                                                                                                                                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `style={"plot_hist_type": ...}`              | [`HISTOGRAM_TYPE`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.HISTOGRAM_TYPE)                                                                                                                          |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                      |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                      |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                    |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                              |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                              |
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.ORIENTATION)                                                                                                                                |
| `bar_mode`                                   | [`BAR_MODE`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.BAR_MODE)                                                                                                                                      |
| `scalex`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.SCALE)                                                                                                                                            |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.SCALE)                                                                                                                                            |

The full list of style attributes is in the [datachart.typings.HistStyleAttrs](https://eriknovak.github.io/datachart/0.10.0/references/charts/histogram/#datachart.typings.HistStyleAttrs) type; the full list of parameters is in the [datachart.charts.Histogram](https://eriknovak.github.io/datachart/0.10.0/references/charts/histogram/#datachart.charts.Histogram) reference.

### Title, axis labels and ticks

Without a title and axis labels the reader cannot tell what was measured or what the bars count; `title`, `xlabel` and `ylabel` say it. The automatic ticks rarely land on values people think in, so `xticks` places them every 10 mm (`xticklabels` would rename them, and `xtickrotate` would tilt them). `xmin` and `xmax` fix the range of the binned axis, which keeps several charts of the same variable aligned.

```
Histogram(
    data=penguins,
    # add the title
    title="Flipper length of Palmer penguins",
    # add the x and y axis labels
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    # tick the flipper length every 10 mm
    xticks=FLIPPER_TICKS,
    # fix the range of the binned axis
    xmin=165,
    xmax=235,
).show()
```

### Figure size and grid

A distribution is wider than it is tall, so a wide, short figure suits it. `figsize` takes a `(width, height)` tuple in inches or one of the presets in [FIG_SIZE](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.FIG_SIZE), sized for a full or half page width.

The counts are read off the y-axis, so [SHOW_GRID.Y](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.SHOW_GRID) is the grid a vertical histogram needs; `SHOW_GRID.X` and `SHOW_GRID.BOTH` are the other options. `aspect_ratio` ([ASPECT_RATIO](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.ASPECT_RATIO)) fixes the ratio of the axes rather than of the figure; a histogram has counts on one axis and values on the other, so the examples leave it at the default.

```
from datachart.constants import FIG_SIZE, SHOW_GRID

Histogram(
    data=penguins,
    title="Flipper length of Palmer penguins",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    # a wide, short figure
    figsize=FIG_SIZE.FULL_SHORT,
    # grid lines along the count axis only
    show_grid=SHOW_GRID.Y,
).show()
```

### Number of bins

The bin count decides which story the histogram tells, so it is worth choosing on purpose. `num_bins` sets it (20 by default). The flipper lengths span 172 to 231 mm. With 4 bins, each about 15 mm wide, the two peaks merge into one, and the distribution looks like a single peak with a long right tail. With 20 bins the dip between the peaks shows. With 120 bins each bin is half a millimeter wide, narrower than the whole millimeters the lengths were recorded in, so every other bin is empty and the chart is mostly noise.

```
for num_bins in [4, 20, 120]:
    Histogram(
        data=penguins,
        title=f"Flipper length in {num_bins} bins",
        xlabel="Flipper length (mm)",
        ylabel="Number of penguins",
        xticks=FLIPPER_TICKS,
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
        # the number of equal-width bins
        num_bins=num_bins,
    ).show()
```

### Histogram style

The `style` dictionary sets the look of the bins; the attributes are listed in [datachart.typings.HistStyleAttrs](https://eriknovak.github.io/datachart/0.10.0/references/charts/histogram/#datachart.typings.HistStyleAttrs), and any attribute left out keeps the value of the active theme. `plot_hist_type` takes a [HISTOGRAM_TYPE](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.HISTOGRAM_TYPE): `BAR` draws one bar per bin (the default), `STEP` an unfilled outline, and `STEP_FILLED` a filled outline with no lines between the bins, which reads as one shape rather than a row of bars. For `STEP` the outline is the mark itself and takes the series color; `plot_hist_edge_color` and `plot_hist_edge_width` override it. A hatch from [HATCH_STYLE](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.HATCH_STYLE) and a dark edge keep the shape readable when printed in greyscale.

```
from datachart.constants import HATCH_STYLE, HISTOGRAM_TYPE

Histogram(
    data=penguins,
    # one filled shape with a hatch and a dark outline
    style={
        "plot_hist_type": HISTOGRAM_TYPE.STEP_FILLED,
        "plot_hist_color": "#a8dadc",
        "plot_hist_alpha": 0.8,
        "plot_hist_hatch": HATCH_STYLE.DIAGONAL,
        "plot_hist_edge_width": 1.5,
        "plot_hist_edge_color": "#1d3557",
    },
    title="Flipper length of Palmer penguins",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Orientation

A horizontal histogram puts the values on the y-axis, which suits a variable people read top to bottom (depth, altitude, age) or a histogram placed beside another chart that shares that axis. `orientation=ORIENTATION.HORIZONTAL` ([ORIENTATION](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.ORIENTATION)) draws the bars from the y-axis; the axis labels, the ticks and the grid swap with it.

```
from datachart.constants import ORIENTATION

Histogram(
    data=penguins,
    title="Flipper length of Palmer penguins",
    # the axis labels swap with the orientation
    xlabel="Number of penguins",
    ylabel="Flipper length (mm)",
    yticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    # and so does the grid
    show_grid=SHOW_GRID.X,
    # draw the bars from the y-axis
    orientation=ORIENTATION.HORIZONTAL,
).show()
```

### Value labels

When the reader needs the exact counts, say to check how many penguins fall in the dip between the peaks, `show_values` prints each bin's count at its top, and `value_format` formats it: a [VALUE_FORMAT](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.VALUE_FORMAT) constant or any `"{x:.1f}"`, `"{:.1f}%"` or `"%g"` style string. Empty bins stay bare. Labels need room, so the example uses fewer bins and extends the count axis a little.

```
from datachart.constants import VALUE_FORMAT

Histogram(
    data=penguins,
    title="Flipper length of Palmer penguins",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    num_bins=12,
    ymax=75,
    # print the count of every bin
    show_values=True,
    value_format=VALUE_FORMAT.INTEGER,
).show()
```

### Reference lines and bands

A summary statistic means more when it sits on the distribution it summarizes. `vlines` draws a vertical line at a value of the binned variable (a mean, a median, a cut-off) and `hlines` a horizontal one at a count. `vspans` and `hspans` shade a range instead. Each takes a dictionary or a list of them, with the position, an optional `label` for the legend, and a `style`; the keys are listed in [VLineSettingAttrs](https://eriknovak.github.io/datachart/0.10.0/references/typings/#datachart.typings.VLineSettingAttrs), [HLineSettingAttrs](https://eriknovak.github.io/datachart/0.10.0/references/typings/#datachart.typings.HLineSettingAttrs), [VSpanSettingAttrs](https://eriknovak.github.io/datachart/0.10.0/references/typings/#datachart.typings.VSpanSettingAttrs) and [HSpanSettingAttrs](https://eriknovak.github.io/datachart/0.10.0/references/typings/#datachart.typings.HSpanSettingAttrs).

The example marks the mean (201 mm) and the median (197 mm) and shades one standard deviation around the mean. The mean sits right of the median because the long-flippered Gentoo penguins pull it, and it lands on the slope down into the dip between the peaks: for a two-peaked distribution the "typical" value describes few of the penguins. The taller figure and `ymax` leave the legend room above the bars.

```
from datachart.constants import LINE_STYLE

flippers = [point["x"] for point in penguins]
mean_flipper = sum(flippers) / len(flippers)
median_flipper = sorted(flippers)[len(flippers) // 2]
std_flipper = (sum((f - mean_flipper) ** 2 for f in flippers) / len(flippers)) ** 0.5

Histogram(
    data=penguins,
    subtitle="penguins",
    # the mean and the median as lines
    vlines=[
        {
            "x": mean_flipper,
            "label": "mean",
            "style": {"plot_vline_color": "#1d3557", "plot_vline_style": LINE_STYLE.DASHED},
        },
        {
            "x": median_flipper,
            "label": "median",
            "style": {"plot_vline_color": "#e76f51", "plot_vline_style": LINE_STYLE.DOTTED},
        },
    ],
    # one standard deviation around the mean as a band
    vspans={
        "xmin": mean_flipper - std_flipper,
        "xmax": mean_flipper + std_flipper,
        "label": "mean ± 1 SD",
    },
    title="Flipper length of Palmer penguins",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    ymax=60,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Text annotations

A peak that has an explanation deserves one. `texts` places text on the chart, with an optional `target` to draw a connector to a point; the position is in data coordinates by default (value, count) or in axes fractions with `"coords": "axes"`. The keys are listed in [TextSettingAttrs](https://eriknovak.github.io/datachart/0.10.0/references/typings/#datachart.typings.TextSettingAttrs), and the [Text Annotations](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/utility/annotations/index.md) guide covers placement and styling. The notes below name the species behind each peak.

```
Histogram(
    data=penguins,
    # one note per peak, each pointing at the top of its peak
    texts=[
        {"text": "Adelie and Chinstrap", "x": 172, "y": 40, "target": (191, 38)},
        {"text": "Gentoo", "x": 224, "y": 36, "target": (216, 27)},
    ],
    title="Flipper length of Palmer penguins",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    ymax=50,
).show()
```

## Multiple Histograms

To compare distributions, pass a list of lists to `data`: each inner list is one series, and the per-series attributes (`subtitle`, `style`, `emphasis`, `x`) become lists aligned with it. A single `style` dictionary applies to every series, while a list styles each one (`None` keeps the theme style). `penguins_by_species` is such a list, and splitting the pooled data by species explains the two peaks. By default the series share one set of bins and are **stacked**, so the outline of the stack is the pooled histogram from the Basics section and the colors show which species fills each bin: the Adelie and Chinstrap penguins make the left peak, the Gentoo penguins the right one.

```
Histogram(
    # one series per species
    data=penguins_by_species,
    # named for the legend
    subtitle=SPECIES,
    # one style per series; None keeps the theme color
    style=[{"plot_hist_color": "#e76f51"}, {"plot_hist_color": "#e9c46a"}, None],
    title="Flipper length of Palmer penguins by species",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Bar mode

A stack answers *what makes up each bin*, but hides the shape of every series except the bottom one. `bar_mode` ([BAR_MODE](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.BAR_MODE)) changes that: `BAR_MODE.OVERLAY` draws every series from zero on the shared bins, one over the other, so each species shows its own shape and the overlap between Adelie and Chinstrap becomes visible. `BAR_MODE.STACK` is the default, and `BAR_MODE.GROUP` behaves like overlay. A step outline keeps the overlaid series from hiding each other.

```
from datachart.constants import BAR_MODE

Histogram(
    data=penguins_by_species,
    subtitle=SPECIES,
    # outlines, so no series hides another
    style={"plot_hist_type": HISTOGRAM_TYPE.STEP, "plot_hist_edge_width": 2},
    title="Flipper length of Palmer penguins by species",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # every series from zero, on the shared bins
    bar_mode=BAR_MODE.OVERLAY,
).show()
```

### Emphasis

When the question is about one of the series, `emphasis` takes one role per series, aligned with `data`: `"highlight"` bolds a series and brings it to the front, `"background"` mutes it and drops it from the legend, `None` leaves it as it is ([EMPHASIS](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.EMPHASIS)). As soon as any series carries a role, the histograms are overlaid rather than stacked, since a muted series stacked under a highlighted one would lift it off the axis. Asking *how do the Gentoo penguins differ* turns the other two species into context. The [Highlighting](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/styling/highlighting/index.md) guide covers emphasis across every chart type and theme.

```
Histogram(
    data=penguins_by_species,
    subtitle=SPECIES,
    # the Gentoo penguins are the question, the rest the context
    emphasis=["background", "background", "highlight"],
    title="Gentoo penguins against the other species",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

`emphasis_rule` picks the series from the data instead. It is a one-key rule, `{"top": n}` or `{"bottom": n}` by rank, `{"above": v}` or `{"below": v}` (strict), or `{"between": (lo, hi)}` (inclusive), read against a summary of each series' own values: the mean by default, or the `"median"`, `"min"`, `"max"` or `"sum"` named by a `"by"` key. An explicit `emphasis` role wins over the rule. The rule below highlights the species whose median flipper is shortest:

```
Histogram(
    data=penguins_by_species,
    subtitle=SPECIES,
    # the series with the smallest median
    emphasis_rule={"bottom": 1, "by": "median"},
    title="The species with the shortest flippers",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Legend

`show_legend` lists the series; `legend` says where and how, with a `title`, a `location` from [LEGEND_LOCATION](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LEGEND_LOCATION), the number of columns `ncols`, and the `alignment` of the entries from [LEGEND_ALIGN](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.LEGEND_ALIGN); a field left out falls back to the theme ([LegendSettingAttrs](https://eriknovak.github.io/datachart/0.10.0/references/typings/#datachart.typings.LegendSettingAttrs)). The two peaks leave little room at the top of the axes, so the legend moves above them, in one row.

```
from datachart.constants import LEGEND_LOCATION

Histogram(
    data=penguins_by_species,
    subtitle=SPECIES,
    style=[{"plot_hist_color": "#e76f51"}, {"plot_hist_color": "#e9c46a"}, None],
    title="Flipper length of Palmer penguins by species",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # a titled, one-row legend above the axes
    legend={"title": "Species", "location": LEGEND_LOCATION.OUTSIDE_TOP, "ncols": 3},
).show()
```

### Subplots

Overlaid series get hard to read once their shapes cross. `subplots=True` draws each series in its own panel: `subtitle` titles the panels, `title`, `xlabel` and `ylabel` stay global, and `max_cols` limits the panels per row. On their own, the panels bin and scale independently, so a bar in one panel does not compare with a bar in the next. `sharex=True` puts the panels on one value axis with shared bins, so the species line up bin for bin, and `sharey=True` puts them on one count axis, so the smaller Chinstrap sample (68 penguins against 151 Adelie) no longer fills its panel.

```
Histogram(
    data=penguins_by_species,
    subtitle=SPECIES,
    title="Flipper length of Palmer penguins by species",
    xlabel="Flipper length (mm)",
    ylabel="Number of penguins",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_TALL,
    show_grid=SHOW_GRID.Y,
    # one panel per species, stacked in a column
    subplots=True,
    max_cols=1,
    # one set of bins and one count axis for all panels
    sharex=True,
    sharey=True,
).show()
```

## Additional Features

### Density view

Counts depend on the sample size: in the panels above the Chinstrap histogram is small because fewer Chinstrap penguins were measured, not because their flippers are unusual. `show_density=True` rescales the bars so that the total area of each series is 1, which makes samples of different sizes comparable. Per density, the Adelie and Chinstrap distributions have about the same height and width, with the Chinstrap one shifted about 6 mm to the right.

```
Histogram(
    data=penguins_by_species,
    subtitle=SPECIES,
    title="Flipper length of Palmer penguins by species",
    xlabel="Flipper length (mm)",
    ylabel="Density",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_TALL,
    show_grid=SHOW_GRID.Y,
    subplots=True,
    max_cols=1,
    sharex=True,
    sharey=True,
    # the density instead of the count
    show_density=True,
).show()
```

### Density curve

A histogram's shape depends on where its bin edges fall; a kernel density estimate smooths the same values into a curve that does not. [datachart.utils.stats.kde1d](https://eriknovak.github.io/datachart/0.10.0/references/utils/stats/#datachart.utils.stats.kde1d) computes the curve and returns `{x, y}` points that a [LineChart](https://eriknovak.github.io/datachart/0.10.0/references/charts/linechart/#datachart.charts.LineChart) draws, and [Panel](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/utility/panel/index.md) lays the curve over a density histogram; both integrate to 1, so they share the y-axis. The `bandwidth` argument of `kde1d` sets how smooth the curve is: a [BANDWIDTH](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.BANDWIDTH) rule (Scott's by default) or a number, where smaller values follow the data more closely. The [Statistics](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/utility/stats/index.md) guide covers the estimate in more depth.

```
from datachart.charts import LineChart
from datachart.utils import Panel
from datachart.utils.stats import kde1d

# the default bandwidth and a narrower one
smooth = kde1d(flippers)
detailed = kde1d(flippers, bandwidth=0.15)

Panel(
    [
        Histogram(data=penguins, subtitle="binned", show_density=True),
        LineChart(data=smooth, subtitle="kernel density (Scott)"),
        LineChart(data=detailed, subtitle="kernel density (bandwidth 0.15)"),
    ],
    title="Flipper length of Palmer penguins",
    xlabel="Flipper length (mm)",
    ylabel_left="Density",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    # the curves run past the data, so the range is fixed
    xmin=165,
    xmax=240,
).show()
```

### Cumulative view

Some questions are about thresholds, not shapes: *how many penguins have flippers of 200 mm or less?* `show_cumulative=True` makes each bar hold the count of all values up to and including its bin, so the bars climb to the sample size. Combined with `show_density=True`, the bars hold the share of values instead and every series climbs to 1, which is the empirical cumulative distribution. At 200 mm, 95% of the Adelie penguins and 74% of the Chinstrap penguins are counted, and not a single Gentoo penguin. A `STEP` outline ends at its final level here: a running total never falls back, so a cumulative outline has no closing drop to zero.

```
Histogram(
    data=penguins_by_species,
    subtitle=SPECIES,
    style={"plot_hist_type": HISTOGRAM_TYPE.STEP, "plot_hist_edge_width": 2},
    bar_mode=BAR_MODE.OVERLAY,
    # the 200 mm threshold
    vlines={"x": 200, "style": {"plot_vline_style": LINE_STYLE.DASHED}},
    title="Share of penguins up to each flipper length",
    xlabel="Flipper length (mm)",
    ylabel="Cumulative share",
    xticks=FLIPPER_TICKS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
    legend={"location": LEGEND_LOCATION.UPPER_LEFT},
    num_bins=59,
    xmax=231,
    # the running share of each species
    show_cumulative=True,
    show_density=True,
).show()
```

### Axis scales

On a linear count axis the bins in the tail of a distribution hold a handful of values and vanish next to the peak. `scaley` (or `scalex` for a horizontal histogram) takes a [SCALE](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.SCALE) member, and a logarithmic count axis gives every occupied bin a visible bar. The bins stay equal-width on the data scale whichever axis scale is applied, so a log scale on the binned axis stretches them unevenly and is rarely what you want. A log axis has no zero, so a `STEP` outline breaks over the empty bins instead of dropping to the axis floor.

Flipper lengths have no long tail, so this example switches dataset. `quakes`, defined in a hidden cell, holds 5,000 illustrative earthquake magnitudes from a seeded generator that follows the Gutenberg-Richter law: every step of one magnitude up makes earthquakes about ten times rarer. On a linear axis the strong earthquakes are invisible; on a log axis the counts fall along a straight line, which is how seismologists read the law.

```
from datachart.constants import SCALE

for scale in [SCALE.LINEAR, SCALE.LOG]:
    Histogram(
        data=quakes,
        title=f"Earthquake magnitudes on a '{scale}' count axis",
        xlabel="Magnitude",
        ylabel="Number of earthquakes",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
        num_bins=30,
        # the scale of the count axis
        scaley=scale,
    ).show()
```

### Custom data keys

Data from a file or an API rarely calls its column `x`, and renaming every record just to plot it is a chore. The `x` argument names the key that holds the value to bin (a list of keys for several series). `penguin_records` stores the penguins the way the published dataset names its columns, so the same records can be binned by body mass instead of flipper length:

```
penguin_records = [
    {"species": species, "flipper_length_mm": flipper, "body_mass_g": mass}
    for species in SPECIES
    for flipper, mass in PENGUINS[species]
]
penguin_records[:2]
```

```
Histogram(
    data=penguin_records,
    # the key that holds the value to bin
    x="body_mass_g",
    title="Body mass of Palmer penguins",
    xlabel="Body mass (g)",
    ylabel="Number of penguins",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    num_bins=30,
).show()
```

## Real-World Examples

The examples below put the features above to work, each one answering a question. The data lives in hidden cells; each example says what its data is and where it comes from.

### Example 1: Do Marathoners Race the Clock? (Fine Bins, Hour Ticks, and Reference Lines)

A study of millions of marathon results found that finish times bunch up just before round-number goals such as four hours, as runners push to beat them (Allen, Dechow, Pope and Wu, *Management Science*, 2017). `finish_times` holds 20,000 illustrative finish times in minutes from a seeded generator that reproduces the effect: a broad spread of times, where some runners heading for just over 3:00, 3:30, 4:00, 4:30 or 5:00 are pulled in under the mark, most strongly at the full hours. With the default 20 bins each bin is 12 minutes wide and the bunching disappears into a smooth hump, so the example uses one-minute bins. `xticks` and `xticklabels` print the axis in hours and minutes, and `vlines` mark the goals, so each spike can be seen to sit just left of its line.

```
Histogram(
    data=finish_times,
    style={"plot_hist_type": HISTOGRAM_TYPE.STEP_FILLED},
    # the round-number goals
    vlines=[
        {
            "x": goal,
            "style": {"plot_vline_color": "#1d3557", "plot_vline_style": LINE_STYLE.DASHED, "plot_vline_width": 0.8},
        }
        for goal in GOALS
    ],
    title="Marathon finish times, in one-minute bins",
    xlabel="Finish time (h:mm)",
    ylabel="Number of runners",
    # the axis in hours and minutes
    xticks=HOUR_TICKS,
    xticklabels=HOUR_LABELS,
    xmin=150,
    xmax=390,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # one bin per minute
    num_bins=240,
).show()
```

### Example 2: Did the New Onboarding Lengthen Sessions? (Emphasis, Density View, and Medians)

`session_durations` holds illustrative session durations, in minutes, from an A/B test of a redesigned onboarding flow: 5,000 sessions of the control group and 600 of the new variant, drawn from seeded log-normal generators. The groups differ eightfold in size, so `show_density` compares their shapes rather than their counts. `emphasis` mutes the control group into a reference and highlights the variant, which also overlays the two instead of stacking them, and `vlines` mark each group's median, the robust summary for a right-skewed duration.

```
Histogram(
    data=session_durations,
    subtitle=["control", "variant"],
    # the control group is the reference, the variant the question
    emphasis=["background", "highlight"],
    # each group's median
    vlines=[
        {
            "x": median,
            "label": f"{group} median ({median:.1f} min)",
            "style": {"plot_vline_color": color, "plot_vline_style": LINE_STYLE.DASHED},
        }
        for (group, median), color in zip(MEDIANS.items(), ["#6c757d", "#c1121f"])
    ],
    title="Session duration with the redesigned onboarding",
    xlabel="Session duration (minutes)",
    ylabel="Density",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    num_bins=60,
    xmin=0,
    xmax=25,
    # compare the shapes, not the sample sizes
    show_density=True,
    show_legend=True,
).show()
```

### Example 3: Did the Release Fatten the Latency Tail? (Log Counts, the Cumulative View, and a Grid)

`latency` holds the response times, in milliseconds, of 20,000 illustrative requests to a web service in the week before and the week after a release, from seeded log-normal generators; after the release, about 3% of requests take a slow path. The service promises that 99% of requests answer within 200 ms. The typical request did not change, so the peaks overlap, and the question lives in the tail. The left chart overlays both weeks as outlines on a log count axis, where the new bump of slow requests shows up. The right chart shows the cumulative share of requests, zoomed to the top 10% with `ymin`, with the 99% promise as a horizontal line and the 200 ms limit as a vertical one: before the release the curve reaches 99% left of the limit, after it only to the right. [Grid](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/utility/grid/index.md) puts the two views side by side.

```
from datachart.utils import Grid

LIMIT = {"x": 200, "style": {"plot_vline_color": "#1d3557", "plot_vline_style": LINE_STYLE.DASHED}}

counts = Histogram(
    data=latency,
    subtitle=WEEKS,
    style=WEEK_STYLE,
    bar_mode=BAR_MODE.OVERLAY,
    vlines=LIMIT,
    title="Requests per bin",
    xlabel="Response time (ms)",
    ylabel="Requests",
    show_grid=SHOW_GRID.Y,
    num_bins=80,
    # the tail shows on a log count axis
    scaley=SCALE.LOG,
    show_legend=True,
)

cumulative = Histogram(
    data=latency,
    subtitle=WEEKS,
    style=WEEK_STYLE,
    bar_mode=BAR_MODE.OVERLAY,
    vlines=LIMIT,
    # the 99% promise
    hlines={"y": 0.99, "style": {"plot_hline_color": "#1d3557", "plot_hline_style": LINE_STYLE.DOTTED}},
    title="Share of requests answered",
    xlabel="Response time (ms)",
    ylabel="Cumulative share",
    show_grid=SHOW_GRID.Y,
    num_bins=400,
    show_cumulative=True,
    show_density=True,
    # zoom into the top 10%, and past the slowest requests
    xmax=700,
    ymin=0.9,
    ymax=1.0,
)

Grid(
    [[counts, cumulative]],
    title="Latency before and after the release",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```
