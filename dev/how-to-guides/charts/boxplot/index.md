# Box Plot

A box plot compares the center, the spread and the outliers of several groups at a glance: each group gets a box, and the boxes answer *which group is higher, which varies more, and which has unusual values*. This guide shows how to create box plots with the [datachart.charts.BoxPlot](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/#datachart.charts.BoxPlot) function, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-box-plot), which maps common tasks to the parameter or style attribute that does the job.

```
from datachart.charts import BoxPlot
```

## Basics

The examples in this guide share one dataset: the [Palmer penguins](https://allisonhorst.github.io/palmerpenguins/) (Gorman, Williams and Fraser, 2014; released under CC0), measurements of the penguins of three species on the islands of the Palmer Archipelago in Antarctica. The hidden cell holds the 342 penguins with a recorded body mass, grouped by species and sex, with the flipper length of each. `body_mass` holds one data point per penguin, its body mass in grams labeled with its species, and `flipper_length` the same for the flipper length in millimeters. The question running through the guide is how the three species differ in size: Adelie and Chinstrap penguins weigh about the same, Gentoo penguins are much heavier, and the boxes show by how much.

Each data point is a dictionary with a `label` (the group) and a `value`. The points that share a `label` form one box, so the three species give three boxes:

```
body_mass[:3]
```

**Basic example.** Only the `data` argument is required. Each box spans the middle half of its group (from the first to the third quartile), the line inside it is the median, the whiskers reach the furthest values within 1.5 box heights of the box, and the values beyond the whiskers are drawn as outliers. The boxes follow the order in which the labels first appear in the data:

```
BoxPlot(
    # add the data to the chart
    data=body_mass
).show()
```

## Customizing the Box Plot

Every customization is either a keyword argument of `BoxPlot` or a `plot_box_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                    | Use                                                           | See                                                                                                     |
| --------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| add a title and axis labels                   | `title`, `xlabel`, `ylabel`                                   | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                            |
| set the axis range, ticks and tick format     | `ymin`, `ymax`, `yticks`, `yticks_format`                     | [Title, axis labels and ticks](#title-axis-labels-and-ticks)                                            |
| resize the figure                             | `figsize`                                                     | [Figure size and grid](#figure-size-and-grid)                                                           |
| show grid lines                               | `show_grid`                                                   | [Figure size and grid](#figure-size-and-grid)                                                           |
| order the boxes by their median               | `sort`                                                        | [Box order](#box-order)                                                                                 |
| change the box fill, edge, median or outliers | `style={"plot_box_color": ..., "plot_box_median_color": ...}` | [Box style](#box-style)                                                                                 |
| draw the boxes horizontally                   | `orientation`                                                 | [Horizontal boxes](#horizontal-boxes)                                                                   |
| hide the outliers                             | `show_outliers`                                               | [Showing and hiding outliers](#showing-and-hiding-outliers)                                             |
| check whether two medians differ              | `show_notch`                                                  | [Notched boxes](#notched-boxes)                                                                         |
| print the median of each box                  | `show_values`, `value_format`                                 | [Value labels](#value-labels)                                                                           |
| highlight some boxes, mute the rest           | `emphasis`, `emphasis_rule`                                   | [Emphasis](#emphasis)                                                                                   |
| mark a threshold or a summary value           | `hlines`, `vlines`, `dlines`                                  | [Reference lines](#reference-lines)                                                                     |
| compare two groups with a bracket             | `brackets`                                                    | [Brackets](#brackets)                                                                                   |
| shade a range of values                       | `hspans`, `vspans`                                            | [Reference bands](#reference-bands)                                                                     |
| title and place the legend                    | `show_legend`, `legend`                                       | [Reference bands](#reference-bands)                                                                     |
| put a note on the chart                       | `texts`                                                       | [Text annotations](#text-annotations)                                                                   |
| use dates as group labels                     | `date` objects as `label`, `xticks_format`                    | [Date labels](#date-labels)                                                                             |
| draw the observations or a violin with boxes  | `Panel` with `SwarmPlot`, `ViolinPlot`                        | [Boxes with swarms and violins](#boxes-with-swarms-and-violins)                                         |
| compare several datasets side by side         | `data` as a list of lists, `subtitle`, `subplots`             | [Multiple Box Plots](#multiple-box-plots)                                                               |
| arrange the subplots and share their axes     | `max_cols`, `sharex`, `sharey`                                | [Shared axes across subplots](#shared-axes-across-subplots)                                             |
| draw every subplot horizontally               | `orientation`                                                 | [Subplot orientation](#subplot-orientation)                                                             |
| use a logarithmic value axis                  | `scaley`                                                      | [Axis scales](#axis-scales)                                                                             |
| plot data with other key names                | `label`, `value`                                              | [Custom data keys](#custom-data-keys)                                                                   |
| save the chart to a file                      | `save_figure`                                                 | [Saving Figures](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/saving/index.md) guide |

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values:

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `emphasis`                                   | [`EMPHASIS`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS)                                                                                                                                   |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                 |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `aspect_ratio`                               | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                           |
| `orientation`                                | [`ORIENTATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION)                                                                                                                             |
| `sort`                                       | [`SORT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SORT)                                                                                                                                           |
| `scaley`                                     | [`SCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE)                                                                                                                                         |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT)         |

The full list of style attributes is in the [datachart.typings.BoxStyleAttrs](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/#datachart.typings.BoxStyleAttrs) type; the full list of parameters is in the [datachart.charts.BoxPlot](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/#datachart.charts.BoxPlot) reference.

### Title, axis labels and ticks

A box plot without labels leaves the reader guessing what is measured and in which unit; `title`, `xlabel` and `ylabel` say it. `ymin` and `ymax` fix the value range, which matters when several charts should be read against each other, and `yticks` picks the tick positions. Body masses run into the thousands, so `yticks_format` prints them with a thousands separator through [VALUE_FORMAT.THOUSANDS](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT); `xtickrotate` and `ytickrotate` tilt long tick labels.

```
from datachart.constants import VALUE_FORMAT

BoxPlot(
    data=body_mass,
    # add the title
    title="Body mass of Palmer penguins",
    # add the x and y axis labels
    xlabel="Species",
    ylabel="Body mass (g)",
    # fix the value range and its ticks
    ymin=2500,
    ymax=6500,
    yticks=[3000, 4000, 5000, 6000],
    # print the ticks with a thousands separator
    yticks_format=VALUE_FORMAT.THOUSANDS,
).show()
```

### Figure size and grid

Three boxes do not need a square figure, and a wide, short one fits a page better. `figsize` takes a `(width, height)` tuple in inches or one of the presets in [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE), sized for a full or half page width.

The values of a vertical box plot are read off the y-axis, so grid lines along it help the eye carry a median or a quartile across to the scale. `show_grid` draws them with [SHOW_GRID.Y](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID) (`SHOW_GRID.X` and `SHOW_GRID.BOTH` are the other options). `aspect_ratio` fixes the ratio of the axes rather than of the figure ([ASPECT_RATIO](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)); box plots rarely need it, so the examples leave it at the default.

```
from datachart.constants import FIG_SIZE, SHOW_GRID

BoxPlot(
    data=body_mass,
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    # a wide, short figure
    figsize=FIG_SIZE.FULL_SHORT,
    # grid lines along the value axis only
    show_grid=SHOW_GRID.Y,
).show()
```

### Box order

The boxes follow the order in which their labels first appear in the data, which is often an accident of how the file was written. Ordered by their median, the boxes read as a ranking. `sort` orders the boxes by their median, `"ascending"` or `"descending"`, also available as the [SORT](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SORT) constants: here by the median body mass of each species, heaviest first. Adelie and Chinstrap penguins share a median of 3,700 g, and ties keep their input order. An `emphasis` list stays aligned with the input order, whatever the sort.

```
from datachart.constants import SORT

BoxPlot(
    data=body_mass,
    # heaviest species first
    sort=SORT.DESCENDING,
    title="Body mass of Palmer penguins, heaviest species first",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Box style

The `style` dictionary sets the look of the boxes: the fill and its alpha, the edge, the hatch, the median line, the whiskers and caps, and the outlier markers; the attributes are listed in [datachart.typings.BoxStyleAttrs](https://eriknovak.github.io/datachart/dev/references/charts/boxplot/#datachart.typings.BoxStyleAttrs), and any attribute left out keeps the value of the active theme. The median is the one line every reader looks for, so it earns a contrasting color and a heavier width. The outlier marker takes a [LINE_MARKER](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LINE_MARKER) value; the diamonds below make the two Chinstrap outliers stand out from the whisker ends.

```
from datachart.constants import LINE_MARKER

BoxPlot(
    data=body_mass,
    # a light box, a strong median, and diamond outliers
    style={
        "plot_box_color": "#c6dbef",
        "plot_box_alpha": 1.0,
        "plot_box_edgecolor": "#08519c",
        "plot_box_linewidth": 1.2,
        "plot_box_median_color": "#d62728",
        "plot_box_median_linewidth": 2.5,
        "plot_box_whisker_color": "#08519c",
        "plot_box_cap_color": "#08519c",
        "plot_box_outlier_marker": LINE_MARKER.DIAMOND,
        "plot_box_outlier_size": 6,
        "plot_box_outlier_color": "#d62728",
    },
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Horizontal boxes

Long group names and many groups read best down the page. `orientation=ORIENTATION.HORIZONTAL` ([ORIENTATION](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION)) puts the groups on the y-axis and the values on the x-axis, so the axis labels, the tick format and the grid swap with it. The first group is drawn at the bottom.

```
from datachart.constants import ORIENTATION

BoxPlot(
    data=body_mass,
    # draw the boxes horizontally
    orientation=ORIENTATION.HORIZONTAL,
    title="Body mass of Palmer penguins",
    # the axis labels, the tick format and the grid swap with the orientation
    xlabel="Body mass (g)",
    ylabel="Species",
    xticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.X,
).show()
```

### Showing and hiding outliers

Outliers are the values beyond the whiskers, and whether to draw them depends on the question. When they are measurement errors or a distraction, `show_outliers=False` hides them; when they are the story, keep them (the default). The Chinstrap penguins have two: one of 2,700 g and one of 4,800 g. Hiding them does not move the whiskers, which still end at the furthest values within 1.5 box heights, so hiding outliers changes what is drawn, not what the boxes summarize.

```
for show_outliers in [True, False]:
    BoxPlot(
        data=body_mass,
        # show or hide the values beyond the whiskers
        show_outliers=show_outliers,
        title=f"Body mass of Palmer penguins, outliers {'shown' if show_outliers else 'hidden'}",
        xlabel="Species",
        ylabel="Body mass (g)",
        yticks_format=VALUE_FORMAT.THOUSANDS,
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
    ).show()
```

### Notched boxes

Two medians that look different may still be the same up to sampling noise, and a notch shows which. `show_notch=True` cuts a notch around each median that spans an approximate 95% confidence interval of it. When the notches of two boxes do not overlap, that is good evidence that their medians differ; when they overlap, the data cannot tell the medians apart. The notch narrows as the group grows, so the 68 Chinstrap penguins get a wider notch than the 151 Adelie. Here the Adelie and Chinstrap notches overlap (both medians are 3,700 g), while the Gentoo notch sits far above both: Gentoo penguins are heavier, beyond doubt.

```
BoxPlot(
    data=body_mass,
    # cut a confidence-interval notch around each median
    show_notch=True,
    title="Body mass of Palmer penguins, with median notches",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Value labels

The median is the number readers take away from a box, and reading it off the axis is imprecise. `show_values` prints each box's median beside its median line, and `value_format` formats it: a [VALUE_FORMAT](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT) constant or any `"{x:.1f}"`, `"{:.1f} g"` or `"%g"` style string. The label font size, color and padding are the `plot_value_*` style attributes ([ValueLabelStyleAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)).

```
BoxPlot(
    data=body_mass,
    # print the median of every box, with its unit
    show_values=True,
    value_format="{x:,.0f} g",
    title="Body mass of Palmer penguins, with the medians",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Emphasis

A chart usually makes one point, and emphasis makes it visible. `emphasis` takes one role per box, in the order the labels first appear in the data (here Adelie, Chinstrap, Gentoo): `"highlight"` bolds the box edges and the median, `"background"` mutes the box together with its whiskers, caps, median and outliers, and `None` leaves it as it is; a single value applies to every box. The roles are also available as the [EMPHASIS](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.EMPHASIS) constants, and the [Highlighting](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/highlighting/index.md) guide covers emphasis across every chart type and theme. The example puts the heavy Gentoo penguins in front.

```
from datachart.constants import EMPHASIS

BoxPlot(
    data=body_mass,
    # one role per box: Adelie, Chinstrap, Gentoo
    emphasis=[EMPHASIS.BACKGROUND, EMPHASIS.BACKGROUND, EMPHASIS.HIGHLIGHT],
    title="Body mass of Palmer penguins, the Gentoo stand apart",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

`emphasis_rule` picks the boxes from the data instead of naming them. It is a one-key dictionary read against a summary of each box: `{"top": n}` or `{"bottom": n}` by rank, `{"above": v}` or `{"below": v}` (strict), or `{"between": (lo, hi)}` (inclusive). The summary is the median by default, what the box already draws; a `"by"` key picks `"mean"`, `"min"`, `"max"` or `"sum"` instead. The boxes that match are highlighted, the rest muted, and an explicit `emphasis` role wins over the rule. Asking which species has penguins lighter than 3 kg picks the boxes by their minimum:

```
BoxPlot(
    data=body_mass,
    # the species whose lightest penguin is under 3,000 g
    emphasis_rule={"below": 3000, "by": "min"},
    title="Species with penguins under 3 kg",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Reference lines

A box on its own says little about whether its values are high or low; a reference line gives it something to be compared with, such as a threshold or the overall mean. `hlines` draws a horizontal line at a value and `vlines` a vertical one; positions along the group axis are box positions, and the first box sits at `0`, as the first bar does, so a half-integer sits between two boxes. Each takes a dictionary or a list of them, with the position, an optional `label` for the legend and a `style` whose line style is a [LINE_STYLE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LINE_STYLE) value; the keys are listed in [HLineSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HLineSettingAttrs) and [VLineSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VLineSettingAttrs). The dashed line marks the mean body mass of all 342 penguins: the whole Gentoo box sits above it, and the Adelie and Chinstrap boxes below it. A dotted vertical line separates the two small species from the Gentoo.

`dlines` completes the trio. Where `vlines` fixes an x and `hlines` a y, a diagonal is fixed by a `slope` and an `intercept`, so it runs through the data space instead of across it; `dlines={}` on its own draws the parity line `y = x`. It spans the axes unless `xmin` and `xmax` clip it to a segment, and takes the same optional `label` and `style`; the keys are listed in [DLineSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.DLineSettingAttrs). The boxes sit at `0`, `1`, `2`, so a diagonal asks whether the species step up evenly: the line runs from the first median to the last, and the middle box sits below it.

```
from datachart.constants import LINE_STYLE

masses = [point["value"] for point in body_mass]
mean_mass = sum(masses) / len(masses)

BoxPlot(
    data=body_mass,
    # a dashed line at the mean of all penguins
    hlines={
        "y": mean_mass,
        "style": {"plot_hline_color": "#d62728", "plot_hline_style": LINE_STYLE.DASHED, "plot_hline_width": 1.5},
    },
    # a dotted line between the second and the third box
    vlines={"x": 1.5, "style": {"plot_vline_color": "#888888", "plot_vline_style": LINE_STYLE.DOTTED}},
    title="Body mass of Palmer penguins against the overall mean",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

```
from statistics import median

# the species in the order the boxes are drawn, and their medians
species = list(dict.fromkeys(point["label"] for point in body_mass))
medians = [
    median(point["value"] for point in body_mass if point["label"] == name)
    for name in species
]
# an even step from the first species to the last
even_step = (medians[-1] - medians[0]) / (len(species) - 1)

BoxPlot(
    data=body_mass,
    # the line the medians would sit on if the species stepped up evenly
    dlines={
        "slope": even_step,
        "intercept": medians[0],
        "label": "even step between species",
        "style": {"plot_dline_color": "#1d3557", "plot_dline_style": LINE_STYLE.DASHED},
    },
    title="Body mass of Palmer penguins against an even step",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_legend=True,
).show()
```

### Brackets

A reference line marks a value; a bracket marks a comparison. `brackets` draws a line spanning two groups, with a tick at each end pointing at them and a text above it — the conventional way to write “these two differ” on a figure. Each bracket names its ends by their labels, so no group positions are computed, and `text` is whatever you worked out elsewhere: datachart draws the result and runs no test of its own. A bracket without a `y` places itself above the data inside its span, and any two that overlap stack a step apart, so several comparisons need no hand-picked heights; the value axis grows to fit them unless the chart sets its own limit. `y` pins a bracket where the figure needs it, and `style` takes the `plot_bracket_*` attributes: the colour (which the text takes too), the line width, the alpha, and `plot_bracket_tick`, the length of the end ticks in points. On a horizontal chart the bracket spans vertically, its ticks point left and its text sits to the right. The keys are listed in [BracketSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.BracketSettingAttrs).

The brackets below carry a Mann–Whitney U test of every pair of species. Two of the three pairs separate cleanly; Adelie and Chinstrap do not, and the bracket says so rather than leaving the reader to guess from two overlapping boxes.

```
from scipy.stats import mannwhitneyu


def mass_of(name):
    return [point["value"] for point in body_mass if point["label"] == name]


def p_text(first, second):
    """The two-sided Mann-Whitney U result, as the bracket prints it."""
    p = mannwhitneyu(mass_of(first), mass_of(second)).pvalue
    return "p < 0.001" if p < 0.001 else f"p = {p:.2f}"


BoxPlot(
    data=body_mass,
    # every pair of species; the chart stacks the three brackets
    brackets=[
        {"from": "Adelie", "to": "Chinstrap", "text": p_text("Adelie", "Chinstrap")},
        {"from": "Chinstrap", "to": "Gentoo", "text": p_text("Chinstrap", "Gentoo")},
        {"from": "Adelie", "to": "Gentoo", "text": p_text("Adelie", "Gentoo")},
    ],
    title="Body mass of Palmer penguins, compared pair by pair",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Reference bands

A line marks one value; a band shades a range, such as a normal range or a tolerance around a value. `hspans` shades between `ymin` and `ymax` and `vspans` between `xmin` and `xmax`; at least one bound is required, and an omitted bound runs to the axis edge. Each takes a dictionary or a list of them, with an optional `label` and a `style` of `plot_hspan_*` or `plot_vspan_*` attributes ([HSpanSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.HSpanSettingAttrs), [VSpanSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.VSpanSettingAttrs)).

Labeled lines and bands are what the legend of a box plot lists: `show_legend` turns it on, and `legend` gives it a `title`, a `location` from [LEGEND_LOCATION](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), the number of columns `ncols` and the `alignment` of the entries ([LegendSettingAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.LegendSettingAttrs)). The example shades one standard deviation around the overall mean: the Adelie and Chinstrap boxes sit inside the band, the Gentoo box mostly above it. The legend goes outside the axes, where it covers no box.

```
from datachart.constants import LEGEND_LOCATION

std_mass = (sum((mass - mean_mass) ** 2 for mass in masses) / len(masses)) ** 0.5

BoxPlot(
    data=body_mass,
    # shade one standard deviation around the mean
    hspans={
        "ymin": mean_mass - std_mass,
        "ymax": mean_mass + std_mass,
        "label": "mean ± 1 SD",
        "style": {"plot_hspan_color": "#d62728", "plot_hspan_alpha": 0.12},
    },
    # and keep the mean itself as a line
    hlines={
        "y": mean_mass,
        "label": "mean",
        "style": {"plot_hline_color": "#d62728", "plot_hline_style": LINE_STYLE.DASHED},
    },
    title="Body mass of Palmer penguins against the overall spread",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # a titled legend outside the axes
    show_legend=True,
    legend={"title": "All penguins", "location": LEGEND_LOCATION.OUTSIDE_RIGHT},
).show()
```

### Text annotations

Where a reference line marks a value, a note explains it. `texts` places text on the chart, with an optional `target` to draw a connector to a point; the position is in data coordinates by default (box position, value) or in axes fractions with `"coords": "axes"`, which keeps the note in place whatever the axis limits. The [Text Annotations](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/annotations/index.md) guide covers placement, connector looks and styling. The note below points at the lightest Chinstrap penguin, the lowest outlier of the dataset.

```
lightest = min(point["value"] for point in body_mass if point["label"] == "Chinstrap")

BoxPlot(
    data=body_mass,
    # a note pinned to the axes, pointing at the Chinstrap outlier
    texts={
        "text": f"the lightest penguin\nof the dataset: {lightest:,} g",
        "x": 0.6,
        "y": 0.2,
        "coords": "axes",
        "target": (1, lightest),
    },
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

### Date labels

Groups are often days, weeks or months: one box per day of measurements. A `label` that is a real temporal object (`datetime`, `date`, `numpy.datetime64` or a pandas `Timestamp`) keeps its categorical position but prints through `xticks_format`, a [DATE_FORMAT](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DATE_FORMAT) member or any `strftime` pattern. `daily_latency`, defined in a hidden cell, holds illustrative response times (in ms) of 100 requests per day to a web service over two weeks, drawn from a seeded log-normal generator, with a slow release on the ninth day that was rolled back two days later. One box per day shows the release as a jump in the median and a longer upper whisker.

```
from datachart.constants import DATE_FORMAT

BoxPlot(
    data=daily_latency,
    title="Daily response times, a slow release on 9 March",
    xlabel="Day (2024)",
    ylabel="Response time (ms)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    show_outliers=False,
    # print the date labels as month and day
    xticks_format=DATE_FORMAT.MONTH_DAY,
    xtickrotate=45,
).show()
```

### Boxes with swarms and violins

A box summarizes its group but hides how many values it holds and how they are spread inside it. A [datachart.charts.SwarmPlot](https://eriknovak.github.io/datachart/dev/references/charts/swarmplot/#datachart.charts.SwarmPlot) shows every observation and a [datachart.charts.ViolinPlot](https://eriknovak.github.io/datachart/dev/references/charts/violinplot/#datachart.charts.ViolinPlot) the shape of the distribution. Over the same labels they draw at the same positions as the boxes, so [datachart.utils.Panel](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) overlays them. A panel holds one box plot dataset, and it overlays with other kinds of chart; the [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) guide covers the rest. The swarm already draws every penguin, so the boxes hide their outliers. The swarm shows what the boxes cannot: there are fewer than half as many Chinstrap penguins as Adelie.

```
from datachart.charts import SwarmPlot, ViolinPlot
from datachart.utils import Panel

Panel(
    [
        # the boxes summarize; the swarm draws every penguin, outliers included
        BoxPlot(data=body_mass, show_outliers=False, style={"plot_box_alpha": 0.4}),
        SwarmPlot(data=body_mass, style={"plot_swarm_size": 6}),
    ],
    title="Body mass of Palmer penguins, every penguin",
    xlabel="Species",
    ylabel_left="Body mass (g)",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
).show()
```

A violin body behind the box adds the shape of the distribution: draw the violin with `inner=None`, since the box supplies the summaries, and give the box a white fill so it reads over the body. The Gentoo violin stays wide across its whole box instead of peaking at the median, a hint of two groups of different size inside the species: the two sexes, which the [Multiple Box Plots](#multiple-box-plots) section splits apart.

```
Panel(
    [
        # the body only; the box supplies the summaries
        ViolinPlot(data=body_mass, inner=None, style={"plot_violin_alpha": 0.3}),
        BoxPlot(
            data=body_mass,
            show_outliers=False,
            style={"plot_box_color": "#FFFFFF", "plot_box_alpha": 0.9},
        ),
    ],
    title="Body mass of Palmer penguins, with the distribution shape",
    xlabel="Species",
    ylabel_left="Body mass (g)",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

## Multiple Box Plots

To compare several datasets over the same groups, pass a list of lists to `data`: each inner list is one dataset, and the per-dataset attributes (`subtitle`, `style`, `hlines` and the other reference settings) become lists aligned with it. Boxes never overlay each other, so each dataset is drawn in its own subplot, which `subplots=True` requires; `subtitle` titles the subplots, while `title`, `xlabel` and `ylabel` stay global. The hidden cell splits the penguins by sex into `body_mass_by_sex`, the 165 female and the 168 male penguins (the 9 penguins without a recorded sex are left out). A style per subplot colors each sex.

```
SEX_STYLE = [{"plot_box_color": "#e07a5f"}, {"plot_box_color": "#3d85c6"}]

BoxPlot(
    # one dataset per sex
    data=body_mass_by_sex,
    # a subtitle and a color per subplot
    subtitle=SEXES,
    style=SEX_STYLE,
    title="Body mass of Palmer penguins by sex",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    # each dataset in its own subplot
    subplots=True,
).show()
```

The two subplots above scale their value axes separately, so the female Gentoo box looks as high as the male one although it is 800 g lighter. The next section fixes that.

### Shared axes across subplots

Boxes in two subplots only compare when they share a scale. `sharey=True` puts every subplot on one value axis and `sharex=True` on one group axis; a shared axis is labeled once, on the outer subplots. `ymin` and `ymax` set the shared range so that it covers the boxes of every subplot. `max_cols` limits the subplots per row, so `max_cols=1` stacks them. Side by side and on a shared mass axis, the males of every species are heavier than the females, and the gap is largest for the Gentoo.

```
BoxPlot(
    data=body_mass_by_sex,
    subtitle=SEXES,
    style=SEX_STYLE,
    title="Body mass of Palmer penguins by sex",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
    subplots=True,
    # one mass axis for both sexes, covering both
    sharey=True,
    ymin=2500,
    ymax=6500,
).show()
```

When the subplots hold different quantities, only the group axis can be shared. Body mass and flipper length stacked in one column share the species axis, labeled once under the bottom subplot, and each keeps its own value axis; the subtitles carry the units.

```
BoxPlot(
    data=[body_mass, flipper_length],
    subtitle=["Body mass (g)", "Flipper length (mm)"],
    title="Size of Palmer penguins",
    xlabel="Species",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
    subplots=True,
    # stack the subplots and share the species axis
    max_cols=1,
    sharex=True,
).show()
```

### Subplot orientation

`orientation` turns every subplot at once. Horizontal boxes move the species to the y-axis, so side by side it is `sharey` that labels them once, next to the left subplot, and the grid follows the values to the x-axis.

```
BoxPlot(
    data=[body_mass, flipper_length],
    subtitle=["Body mass (g)", "Flipper length (mm)"],
    # every subplot horizontal
    orientation=ORIENTATION.HORIZONTAL,
    title="Size of Palmer penguins",
    ylabel="Species",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.X,
    subplots=True,
    # the species are now on the y-axis
    sharey=True,
).show()
```

## Additional Features

### Axis scales

Response times, incomes and file sizes are skewed: most values are small and a long tail runs far above them. On a linear axis the tail squeezes the boxes into a thin strip at the bottom. `scaley` takes a [SCALE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SCALE) member, and a logarithmic scale spreads the boxes out so that their medians and quartiles can be compared. `response_times`, defined in a hidden cell, holds illustrative response times (in ms) of 200 requests to each of four services, drawn from a seeded log-normal generator.

```
from datachart.constants import SCALE

for scale in [SCALE.LINEAR, SCALE.LOG]:
    BoxPlot(
        data=response_times,
        title=f"Response times on the '{scale}' scale",
        xlabel="Service",
        ylabel="Response time (ms)",
        figsize=FIG_SIZE.FULL_SHORT,
        show_grid=SHOW_GRID.Y,
        # the scale of the value axis
        scaley=scale,
    ).show()
```

### Custom data keys

Data from a file or an API rarely uses the `label` and `value` keys, and renaming every record just to plot it is a chore. The `label` and `value` arguments name the keys to read instead. `penguin_records` stores the penguins the way the published CSV file does, one record per penguin with a `species` and a `body_mass_g` key:

```
penguin_records = [
    {"species": group["species"], "sex": group["sex"], "body_mass_g": mass}
    for group in PENGUINS
    for mass in group["body_mass"]
]
penguin_records[:2]
```

```
BoxPlot(
    data=penguin_records,
    # the keys that hold the group and the value
    label="species",
    value="body_mass_g",
    title="Body mass of Palmer penguins",
    xlabel="Species",
    ylabel="Body mass (g)",
    yticks_format=VALUE_FORMAT.THOUSANDS,
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.Y,
).show()
```

## Real-World Examples

The examples below put the features above to work, each one answering a question. The data lives in hidden cells; each example says what its data is and where it comes from.

### Example 1: Which Model Should Ship? (Seed Spread, Notches, Median Labels, and a Rule-Picked Winner)

`benchmark` holds the illustrative test accuracy of five models, each trained with 20 random seeds, drawn from a seeded generator. A single accuracy per model hides how much of the difference between models is seed noise; one box per model shows the spread, and the notches say whether two medians really differ. `emphasis_rule={"top": 1}` highlights the model with the best median accuracy and value labels print its median. The notches temper the verdict: the Ensemble notch overlaps the winner's, so the data cannot say the Ensemble is worse, while Baseline and Wide are behind beyond doubt. A notch that folds back past its box, as for Wide, means the confidence interval is wider than the box itself, a sign that 20 seeds are too few to pin that median down.

```
BoxPlot(
    data=benchmark,
    # highlight the model with the best median, mute the rest
    emphasis_rule={"top": 1},
    # do the medians really differ?
    show_notch=True,
    # print the medians as percentages
    show_values=True,
    value_format=VALUE_FORMAT.PERCENT,
    title=f"Test accuracy across {N_SEEDS} seeds",
    xlabel="Model",
    ylabel="Accuracy",
    yticks_format=VALUE_FORMAT.PERCENT_INT,
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.Y,
).show()
```

### Example 2: How Cold Does Each Month Get? (Horizontal Boxes, a Freezing Line, and a Band)

`daily_temperatures` holds one illustrative year of daily mean temperatures (in °C) in a central European city, drawn from a seeded generator around approximate monthly means, with larger day-to-day swings in winter. Twelve boxes read best as horizontal boxes, with January at the top; since the first box is drawn at the bottom, the data is ordered from December to January. A dashed `vlines` line marks the freezing point, so the months with frosty days are the boxes that reach left of it, and a `vspans` band shades the 18 to 24 °C range of warm days, where only the summer boxes sit. The outliers stay: an unusually cold or warm day is what a reader of this chart looks for.

```
BoxPlot(
    data=daily_temperatures,
    # twelve labeled boxes read best top to bottom
    orientation=ORIENTATION.HORIZONTAL,
    # the freezing point
    vlines={
        "x": 0,
        "label": "freezing point",
        "style": {"plot_vline_color": "#4c72b0", "plot_vline_style": LINE_STYLE.DASHED, "plot_vline_width": 1.5},
    },
    # the range of warm days
    vspans={
        "xmin": 18,
        "xmax": 24,
        "label": "warm days",
        "style": {"plot_vspan_color": "#f4a261", "plot_vspan_alpha": 0.2},
    },
    title="Daily mean temperature by month",
    xlabel="Temperature (°C)",
    ylabel="Month",
    figsize=FIG_SIZE.FULL_MEDIUM,
    show_grid=SHOW_GRID.X,
    show_legend=True,
    legend={"title": "Reference", "location": LEGEND_LOCATION.OUTSIDE_RIGHT},
).show()
```

### Example 3: Do the Services Meet Their SLA? (A Log Scale, an SLA Line, a Note, and a Grid with Swarm Panels)

A service level agreement (SLA) promises that requests finish within 500 ms, and the `response_times` of the [Axis scales](#axis-scales) section show which of the four services keeps the promise. The top chart draws all four services on a log scale with the SLA as a dashed line; `emphasis_rule={"above": 500, "by": "max"}` highlights the services whose slowest request breaks the SLA, and a note points at Reports, whose median alone is above the line. Search is highlighted although its whole box sits below the line. The bottom row zooms into Search and Checkout on one linear range: a [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) per service overlays the box on a swarm of every request, so the breaches are counted, not guessed. Search breaks the SLA with a handful of slow requests, Checkout never. [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md) puts the three charts in one figure.

```
from datachart.utils import Grid

SLA_MS = 500
SLA_LINE = {
    "y": SLA_MS,
    "style": {"plot_hline_color": "#d62728", "plot_hline_style": LINE_STYLE.DASHED, "plot_hline_width": 1.5},
}

overview = BoxPlot(
    data=response_times,
    scaley=SCALE.LOG,
    hlines=SLA_LINE,
    # the services whose slowest request breaks the SLA
    emphasis_rule={"above": SLA_MS, "by": "max"},
    texts={
        "text": "median above the SLA",
        "x": 0.55,
        "y": 0.9,
        "coords": "axes",
        "target": (3, 700),
    },
    title="All services, log scale",
    ylabel="Response time (ms)",
    show_grid=SHOW_GRID.Y,
)


def service_zoom(service):
    # one service: a box over every request, with the SLA line
    requests = [point for point in response_times if point["label"] == service]
    breaches = sum(point["value"] > SLA_MS for point in requests)
    return Panel(
        [
            BoxPlot(data=requests, show_outliers=False, style={"plot_box_alpha": 0.4}, hlines=SLA_LINE),
            SwarmPlot(data=requests, style={"plot_swarm_size": 4}),
        ],
        title=f"{service}: {breaches} of {N_REQUESTS} over {SLA_MS} ms",
        ylabel_left="Response time (ms)",
        show_grid=SHOW_GRID.Y,
        # the same range for both services, the SLA line included
        ymin=0,
        ymax=700,
    )


Grid(
    [
        [overview],
        [service_zoom("Search"), service_zoom("Checkout")],
    ],
    title="Response times against a 500 ms SLA",
    figsize=FIG_SIZE.FULL_TALL,
).show()
```
