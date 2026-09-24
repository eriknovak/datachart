# Statistics

A statistics report asks the same questions in the same order: do these groups really differ, how large is the difference and how sure can we be of it, which measurements move together, and does the line fitted through them hold up. This page walks one dataset through those questions and names the figure that answers each, so the chart to reach for arrives with the question rather than the other way round. Every figure links to the chart guide that covers it in full.

The dataset is the **Palmer penguins** (Gorman et al. 2014, [CC0](https://creativecommons.org/publicdomain/zero/1.0/)): the bill length, bill depth, flipper length, body mass, species and sex of 344 penguins measured on the Palmer Archipelago, Antarctica. Two birds were never measured and are dropped, leaving 342. The hypothesis tests are `scipy.stats` calls written out in the open, and the intervals are bootstrap resamples; datachart draws what they produce and the [statistics utilities](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/stats/index.md) supply the rest.

```
import numpy as np
from scipy import stats as scipy_stats

from datachart.charts import (
    Heatmap,
    Histogram,
    LineChart,
    RaincloudPlot,
    ScatterChart,
    ScatterMatrix,
)
from datachart.constants import (
    ASPECT_RATIO,
    FIG_SIZE,
    LINE_DRAW_STYLE,
    NORMALIZE,
    SCATTER_MATRIX_DIAGONAL,
    SHOW_GRID,
    VALUE_FORMAT,
)
from datachart.utils import Grid
from datachart.utils.stats import correlation, linear_fit, spearman
```

The hidden cell below holds the measurements themselves. `PENGUIN_ROWS` is the table as published, one tuple per bird per species; `MEASUREMENTS` names the four numeric columns in order and `SEXES` spells the sex codes out; `penguins` is the list of records the whole page works from, one dict per bird. Every section that follows starts from those four names.

## Comparing the groups

### Do the three species differ in body mass?

The first figure of a comparison shows the distributions themselves, not their summaries: a test says whether a difference exists, and only the shapes say whether the question was sensible to ask. A [raincloud plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/raincloudplot/index.md) draws all three readings at once (the density of each species, its box, and every bird as a point), so a bimodal group or a stray outlier cannot hide behind a median.

The test beside it is the Kruskal-Wallis H, a rank-based one-way test that asks whether any group sits higher than the others. It is used here in place of a one-way ANOVA because nothing yet says these distributions are normal; the last section of this page asks that question directly. A significant omnibus result says only *some* pair differs, so each pair gets its own Mann-Whitney U test, and the three p-values are corrected for having been asked together with the Holm step-down rule.

```
SPECIES = ["Adelie", "Chinstrap", "Gentoo"]
PAIRS = [("Adelie", "Chinstrap"), ("Chinstrap", "Gentoo"), ("Adelie", "Gentoo")]


def values(name, species=None):
    """One measurement of every bird, or of one species."""
    return [
        penguin[name]
        for penguin in penguins
        if species is None or penguin["species"] == species
    ]


mass = {species: np.array(values("body mass", species)) for species in SPECIES}

omnibus = scipy_stats.kruskal(*mass.values())
pairwise = [scipy_stats.mannwhitneyu(mass[a], mass[b]).pvalue for a, b in PAIRS]


def holm(pvalues):
    """The Holm step-down adjusted p-values of a family of tests, in input order."""
    order = np.argsort(pvalues)
    multipliers = np.arange(len(pvalues), 0, -1)
    running = np.maximum.accumulate(np.asarray(pvalues)[order] * multipliers)
    adjusted = np.empty(len(pvalues))
    adjusted[order] = np.clip(running, 0, 1)
    return adjusted


adjusted = holm(pairwise)
{f"{a} vs {b}": float(f"{p:.3g}") for (a, b), p in zip(PAIRS, adjusted)}
```

Each pairwise result becomes a `brackets` entry: the two species by name and the adjusted p-value as its text. The chart places each bracket above the clouds it spans, stacks the ones that overlap, and grows the value axis to fit them, so no position is computed here. The omnibus result is a `texts` note pinned to the axes with `coords="axes"` rather than to a data position.

```
NOTE_STYLE = {"plot_text_size": 9}
REFERENCE_HLINE = {"plot_hline_color": "#666666", "plot_hline_width": 1}


def as_p(pvalue):
    return "p < 0.001" if pvalue < 0.001 else f"p = {pvalue:.2f}"


omnibus_note = f"Kruskal-Wallis H = {omnibus.statistic:.0f}, {as_p(omnibus.pvalue)}"

mass_figure = RaincloudPlot(
    [
        {"label": species, "value": float(value)}
        for species in SPECIES
        for value in mass[species]
    ],
    title="Gentoo stands apart; Adelie and Chinstrap weigh the same",
    ylabel="Body mass (g)",
    ymin=2400,
    # one bracket per pairwise test, named by the species it compares
    brackets=[
        {"from": a, "to": b, "text": as_p(pvalue)}
        for (a, b), pvalue in zip(PAIRS, adjusted)
    ],
    texts={
        "text": omnibus_note,
        "x": 0.02,
        "y": 0.97,
        "coords": "axes",
    },
    figsize=FIG_SIZE.FULL_MEDIUM,
)
mass_figure.show()
```

The omnibus test is significant, and the brackets say where that came from: Gentoo against either of the others, and nothing between Adelie and Chinstrap, whose clouds sit on top of each other. A table of three p-values would have said the same, but the figure also shows that the Chinstrap cloud is the narrowest and the Gentoo box the highest, which no test reports.

### How large is each difference, and how sure can we be of it?

A p-value says a difference is unlikely to be an accident; it never says how large the difference is. The size belongs in its own figure, with an interval attached, and the interval here comes from a bootstrap: both groups are resampled with replacement a few thousand times, the difference of means is recorded each time, and the middle 95% of those recordings is the interval. `bootstrap_ci`, in the [statistics utilities](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/stats/index.md), does this in one call for a statistic of **one** sample (a mean, a median, an IQR); a difference needs both groups resampled, so the helper below does that and keeps the draws, which the next figure needs anyway.

Each pair is one row, so the differences go on the x-axis of a [scatter chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md) and the pairs on the y-axis. `xerr` takes the interval as *distances* from the point rather than as endpoints, which is the subtraction the chart cannot do for you, and `show_xerr` draws it. The `vlines` zero is the reference every row is read against: a bar that crosses it is a difference the data does not establish.

```
REFERENCE_VLINE = {"plot_vline_color": "#666666", "plot_vline_width": 1}
RESAMPLES = 4000


def bootstrap_difference(a, b, resamples=RESAMPLES, seed=20260922):
    """The resampled differences between the means of two groups."""
    rng = np.random.default_rng(seed)
    return np.array(
        [
            rng.choice(b, b.size).mean() - rng.choice(a, a.size).mean()
            for _ in range(resamples)
        ]
    )


draws = {pair: bootstrap_difference(mass[pair[0]], mass[pair[1]]) for pair in PAIRS}

effects = [
    {
        "label": f"{b} - {a}",
        "observed": float(mass[b].mean() - mass[a].mean()),
        "low": float(np.quantile(draws[(a, b)], 0.025)),
        "high": float(np.quantile(draws[(a, b)], 0.975)),
    }
    for a, b in PAIRS
]
effects.sort(key=lambda row: row["observed"])
effects
```

```
effect_figure = ScatterChart(
    [
        {
            "x": row["observed"],
            "y": position,
            # the bar reaches from the point to each bound, not to the axis
            "xerr": [row["observed"] - row["low"], row["high"] - row["observed"]],
        }
        for position, row in enumerate(effects)
    ],
    title="Gentoo outweighs both by about 1.4 kg; Adelie and Chinstrap tie",
    xlabel="Difference in mean body mass (g)",
    show_xerr=True,
    yticks=list(range(len(effects))),
    yticklabels=[row["label"] for row in effects],
    ymin=-0.6,
    ymax=len(effects) - 0.4,
    # zero: the value a pair that weighs the same would land on
    vlines={"x": 0, "style": REFERENCE_VLINE},
    show_grid=SHOW_GRID.X,
    figsize=FIG_SIZE.FULL_SHORT,
)
effect_figure.show()
```

The bottom row straddles zero, so the 32 g the sample happens to show is not a difference the data establishes. The other two sit around 1.35 kg with intervals 230 to 260 g wide, under a fifth of the effect. The figure exists for that comparison: the bar and the point share one axis, so the size of the uncertainty is read against the size of the finding instead of being quoted beside it.

### What is the interval actually made of?

An interval is two numbers, and two numbers hide the shape they came from. Drawing the resampled differences as a [histogram](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/histogram/index.md) shows that shape and makes the percentile rule visible: the observed difference is one `vlines` mark, the two bounds are two more, and the bars between them are the 95% the interval claims.

This is worth one figure in a report when the interval is the result: a bootstrap that comes out skewed or multi-peaked says the statistic is unstable, and a symmetric hill like this one says a normal-theory interval would have given the same answer more cheaply.

```
OBSERVED_VLINE = {"plot_vline_color": "#111111", "plot_vline_width": 1.6}

BIGGEST_GAP = ("Adelie", "Gentoo")
gap_draws = draws[BIGGEST_GAP]
low, high = np.quantile(gap_draws, [0.025, 0.975])
observed = mass[BIGGEST_GAP[1]].mean() - mass[BIGGEST_GAP[0]].mean()

Histogram(
    [{"x": float(value)} for value in gap_draws],
    title=f"{RESAMPLES:,} resampled differences, and the 95% they leave in the middle",
    xlabel="Gentoo - Adelie difference in mean body mass (g)",
    ylabel="Resamples",
    num_bins=40,
    vlines=[
        {
            "x": float(observed),
            "label": f"Observed ({observed:.0f} g)",
            "style": OBSERVED_VLINE,
        },
        {
            "x": float(low),
            "label": f"95% interval ({low:.0f} to {high:.0f} g)",
            "style": REFERENCE_VLINE,
        },
        {"x": float(high), "style": REFERENCE_VLINE},
    ],
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

The observed difference sits in the middle of the hill, as it must, since the bootstrap is centered on the sample. The figure adds the width: the resamples spread over a couple of hundred grams, a sixth of the difference itself, so the finding survives any reasonable redraw of the sample.

## Relating the measurements

### Which measurements move together?

With four measurements there are six pairs, and reading six numbers out of a paragraph is what a correlation matrix exists to prevent. The matrix is a square grid of values, so it is a [heatmap](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/heatmap/index.md). A correlation is signed, though, and a sequential colormap run from the smallest value would put zero on an arbitrary shade. `norm=NORMALIZE.CENTERED` pins zero to the middle of the theme's diverging colormap and runs the same distance to each side, so a cell's hue is its sign and its depth is its strength.

A correlation matrix is also symmetric, which means half of it is decoration. A `None` in `z` leaves a cell blank, so the upper triangle goes; the diagonal of ones goes with the first row and the last column, which hold nothing once it does, and the six numbers that carry information remain.

```
columns = {name: values(name) for name in MEASUREMENTS}

# the lower triangle only: the upper half repeats it and the diagonal is 1,
# so the first row and the last column of the square hold nothing
ROW_NAMES, COLUMN_NAMES = MEASUREMENTS[1:], MEASUREMENTS[:-1]

correlations = [
    [
        round(correlation(columns[row], columns[column]), 2)
        if column_index <= row_index
        else None
        for column_index, column in enumerate(COLUMN_NAMES)
    ]
    for row_index, row in enumerate(ROW_NAMES)
]

correlation_figure = Heatmap(
    {"x": COLUMN_NAMES, "y": ROW_NAMES, "z": correlations},
    title="Flipper length and body mass are near-interchangeable",
    # zero in the middle of the diverging colormap, equal reach each way
    norm=NORMALIZE.CENTERED,
    show_values=True,
    show_colorbars=True,
    value_format=VALUE_FORMAT.DECIMAL_2,
    aspect_ratio=ASPECT_RATIO.EQUAL,
    colorbar={"label": "Pearson correlation"},
    xtickrotate=20,
    figsize=FIG_SIZE.FULL_MEDIUM,
)
correlation_figure.show()
```

Flipper length and body mass at 0.87 are close to the same measurement taken twice, which matters later: a model given both learns little from the second. The surprise is bill depth, which runs *against* all three others: deeper bills on lighter, shorter-flippered birds. That is the finding of this figure, and the next two figures explain it.

### What is a single correlation hiding?

A correlation over the whole table is a correlation over a mixture of three species, and a mixture can invert the relationship inside every group it contains. The figure that shows this is a [scatter matrix](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scattermatrix/index.md): every pair of measurements as its own scatter, colored by species with `hue`, so the pooled cloud and the three clouds inside it are visible at once. `lower_only` drops the mirrored half, matching the heatmap above, and a `KDE` diagonal shows each measurement's distribution per species where a histogram of three overlapping groups would be a mess.

```
ScatterMatrix(
    penguins,
    title="Palmer penguins by species (mm, g)",
    dimensions=MEASUREMENTS,
    # color the points by species, and one density curve per species
    hue="species",
    diagonal=SCATTER_MATRIX_DIAGONAL.KDE,
    lower_only=True,
    show_legend=True,
    figsize=(7.0, 7.0),
).show()
```

The bill depth row is the one to read. Every cell in it slopes downward as a whole, and inside every cluster the same cell slopes *upward*: the three species sit on a diagonal staircase that the pooled cloud follows instead. This is Simpson's paradox, and it is the reason a correlation matrix should never be the last figure of an association section.

### Is it the mixture, or is it the outliers?

One pair deserves the close-up, and it comes with a second question: a Pearson correlation measures how close the points lie to a straight line and is pulled hard by a few extreme ones, while a Spearman correlation measures only whether the ranks move together and barely notices them. When the two disagree the culprit is usually an outlier or a curve; when they agree, as here, neither is the explanation and the mixture is.

Both coefficients come from the [statistics utilities](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/stats/index.md) (`correlation` and `spearman`) and go into a `texts` note. The [scatter chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md) fits the pooled line itself with `show_regression`, and `hue` colors the points by species so the pooled line can be read against the groups it was fitted through.

```
PAIR = ("flipper length", "bill depth")
pearson = correlation(columns[PAIR[0]], columns[PAIR[1]])
rank = spearman(columns[PAIR[0]], columns[PAIR[1]])
within = {
    species: correlation(values(PAIR[0], species), values(PAIR[1], species))
    for species in SPECIES
}
within
```

```
ScatterChart(
    [
        {"x": penguin[PAIR[0]], "y": penguin[PAIR[1]], "hue": penguin["species"]}
        for penguin in penguins
    ],
    title="One line down through three clouds that each point up",
    xlabel="Flipper length (mm)",
    ylabel="Bill depth (mm)",
    # the pooled fit, through all three species at once
    show_regression=True,
    texts=[
        {
            "text": f"Pooled: Pearson r = {pearson:.2f}, Spearman ρ = {rank:.2f}",
            "x": 0.03,
            "y": 0.11,
            "coords": "axes",
            "style": {**NOTE_STYLE, "plot_text_valign": "bottom"},
        },
        {
            "text": "Within species: "
            + ", ".join(f"{name} {value:+.2f}" for name, value in within.items()),
            "x": 0.03,
            "y": 0.04,
            "coords": "axes",
            "style": {**NOTE_STYLE, "plot_text_valign": "bottom"},
        },
    ],
    show_legend=True,
    show_grid=SHOW_GRID.BOTH,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

Pearson and Spearman land about 0.06 apart, so the negative pooled figure is not the work of a handful of stray birds. Every species on its own gives a positive coefficient, and the largest of them is stronger than the pooled one is negative. For the report: flipper length and bill depth rise together within a species, and the species differ enough in both to reverse the sign when they are pooled.

## Checking the model

### Does the straight line hold, and where does it fail?

Flipper length and body mass were the strongest pair in the matrix, so a straight line through them is the obvious model. Two figures check it, and they belong together: the fit itself, which says whether the line is plausible at all, and its residuals against the values it predicted, which say where it is wrong.

`linear_fit` returns the slope, the intercept and the r², so the residuals can be computed in the open rather than read off the chart. The [scatter chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md) draws the same fit with `show_regression` and shades its confidence band with `show_ci`. In the residual plot the reference is the zero line, an `hlines` mark, and the shape to look for is no shape: a horizontal band of even width. A [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md) stacks the two, one above the other. The cells keep their own x-axes rather than sharing one, because the residuals are plotted against *fitted* values, not against flipper length.

```
flipper = np.array(values("flipper length"), dtype=float)
body_mass = np.array(values("body mass"), dtype=float)

slope, intercept, r2 = linear_fit(flipper, body_mass)
fitted = slope * flipper + intercept
residuals = body_mass - fitted
round(slope, 1), round(intercept, 1), round(r2, 3)
```

```
fit_figure = ScatterChart(
    [{"x": float(x), "y": float(y)} for x, y in zip(flipper, body_mass)],
    title="Body mass on flipper length",
    xlabel="Flipper length (mm)",
    ylabel="Body mass (g)",
    show_regression=True,
    show_ci=True,
    texts={
        "text": f"{slope:.0f} g per mm, r² = {r2:.2f}",
        "x": 0.03,
        "y": 0.95,
        "coords": "axes",
        "style": NOTE_STYLE,
    },
    show_grid=SHOW_GRID.BOTH,
)

residual_figure = ScatterChart(
    [{"x": float(x), "y": float(y)} for x, y in zip(fitted, residuals)],
    title="Residuals against fitted values",
    xlabel="Fitted body mass (g)",
    ylabel="Residual (g)",
    # the line a perfect prediction would sit on
    hlines={"y": 0, "style": REFERENCE_HLINE},
    show_grid=SHOW_GRID.BOTH,
)

Grid(
    [[fit_figure], [residual_figure]],
    title="A good line, with one species sitting under it",
    figsize=(7.0, 7.4),
).show()
```

The line explains about three quarters of the variation in body mass, and the residual band is flat and of even width: no curve the line missed, and no fan opening towards the heavy end. The one structure left is a dip in the middle of the range, where Chinstrap birds sit on average 216 g below the line: the species mixture the correlation figures found, showing up again as the thing a single line cannot absorb.

### Are the residuals normal enough to quote an interval?

Every interval and p-value a least-squares fit reports assumes its residuals are roughly normal. A Q-Q plot tests that by eye: sort the residuals, divide them by their standard deviation, and plot each against the value a standard normal distribution would have put in that position. If the assumption holds the points fall on the parity line, which is a `dlines` diagonal, the one reference mark a [scatter chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md) draws without a data series behind it.

The Shapiro-Wilk test answers the same question with one number, and the two belong together: the test says whether to reject, the figure says *where* the deviation is, and on 342 points a test will flag departures too small to matter.

```
# ddof=2: the slope and the intercept were both estimated from these points
standardized = np.sort(residuals / residuals.std(ddof=2))
# Blom plotting positions: where a standard normal would put each rank
ranks = (np.arange(1, standardized.size + 1) - 0.375) / (standardized.size + 0.25)
theoretical = scipy_stats.norm.ppf(ranks)
shapiro = scipy_stats.shapiro(residuals)

qq_figure = ScatterChart(
    [{"x": float(x), "y": float(y)} for x, y in zip(theoretical, standardized)],
    title="The residuals lean right, not enough to reject normality",
    xlabel="Standard normal quantile",
    ylabel="Standardized residual",
    # the parity line the points would follow if they were normal
    dlines={"slope": 1, "intercept": 0, "label": "Normal"},
    texts={
        "text": f"Shapiro-Wilk W = {shapiro.statistic:.3f}, {as_p(shapiro.pvalue)}",
        "x": 0.03,
        "y": 0.95,
        "coords": "axes",
        "style": NOTE_STYLE,
    },
    aspect_ratio=ASPECT_RATIO.EQUAL,
    show_legend=True,
    show_grid=SHOW_GRID.BOTH,
    figsize=FIG_SIZE.FULL_MEDIUM,
)
qq_figure.show()
```

The middle of the distribution lies on the line and both ends sit above it: the heaviest birds are further from the fit than a normal distribution allows, and the lightest are closer to it. That is a mild right skew rather than a heavy tail on both sides. Shapiro-Wilk does not reject at the 5% level, so the intervals the fit reports are usable, and the skew is worth a sentence rather than a different model.

### What do the distributions say with no model at all?

The first figure of this page drew densities, which means it drew a bandwidth choice. The last one draws none: an empirical cumulative distribution puts each observation at its own rank, so the curve is the data and nothing else. Any quantile can be read straight off it (the median is where the curve crosses 0.5), and two curves that never touch are two distributions that do not overlap at all.

A [line chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/linechart/index.md) draws it once the points are sorted, with `plot_line_drawstyle` set to a stepped style so the curve rises at the observations instead of sloping between them, which is what a smooth line would falsely imply.

```
LineChart(
    [
        [
            {"x": float(value), "y": (rank + 1) / mass[species].size}
            for rank, value in enumerate(np.sort(mass[species]))
        ]
        for species in SPECIES
    ],
    title="Above 4.8 kg, every bird is a Gentoo",
    xlabel="Body mass (g)",
    ylabel="Share of birds at or below",
    subtitle=SPECIES,
    # the curve steps up at each bird instead of sloping between them
    style={"plot_line_drawstyle": LINE_DRAW_STYLE.STEPS_POST},
    # the level the median is read off
    hlines={"y": 0.5, "style": REFERENCE_HLINE},
    show_legend=True,
    show_grid=SHOW_GRID.BOTH,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

The Adelie and Chinstrap curves run through each other for their whole length, which is the non-significant pair of the first figure seen without any test. The Gentoo curve only starts where the other two are already seven tenths of the way up, and the horizontal 0.5 line crosses it about 1.3 kg further right: the same effect the second figure measured, read straight off the data.

## The report figure

A paper has room for one figure, not nine. The four that carry the argument (the groups differ, here is what moves with what, here is the model, and here is why its intervals can be trusted) go into one panel with [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md), which takes the figures already drawn above and redraws them into its cells. Nested lists are the layout: one inner list per row.

```
Grid(
    [
        [mass_figure, correlation_figure],
        [fit_figure, qq_figure],
    ],
    title="Palmer penguins: groups, associations, the fit, and its residuals",
    figsize=(11.0, 8.5),
).show()
```

Every figure on this page is one call to a chart function over a list of dicts, and every number in them comes from a `scipy.stats` call or a [statistics utility](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/stats/index.md) written out in the cell above it. To adapt any of them, open the guide it links to and read the parameter that does the job. The charts index lists them all: [Charts](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/index.md).
