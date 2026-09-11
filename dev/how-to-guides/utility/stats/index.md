# Statistics

This section showcases the utility functions found in the [datachart.utils.stats](https://eriknovak.github.io/datachart/dev/references/utils/stats) module.

Let us start by importing the supporting libraries:

```
import math
import random
```

## Statistics Submodule

The [dataset.utils.stats](https://eriknovak.github.io/datachart/dev/references/utils/stats) submodule contains functions for calculating statistics. To showcase its use, let us create a list of random numbers:

```
random_values = random.sample(range(1, 100), 10)
random_values
```

Let us now showcase the functions in the `stats` module.

### Count

The `count` function returns the number of elements in the list.

```
from datachart.utils.stats import count
```

```
count(random_values)
```

### Sum

The `sum_values` function returns the sum of all values in the list.

```
from datachart.utils.stats import sum_values
```

```
sum_values(random_values)
```

### Mean

The `mean` function returns the mean of the values.

```
from datachart.utils.stats import mean
```

```
mean(random_values)
```

### Median

The `median` function returns the median of the values.

```
from datachart.utils.stats import median
```

```
median(random_values)
```

### Standard Deviation

The `stdev` function returns the standard deviation of the values.

```
from datachart.utils.stats import stdev
```

```
stdev(random_values)
```

### Variance

The `variance` function returns the variance of the values. Variance is the square of the standard deviation.

```
from datachart.utils.stats import variance
```

```
variance(random_values)
```

### Quantile

The `quantile` function returns the quantile of the values.

```
from datachart.utils.stats import quantile
```

Show the 25th quantile:

```
quantile(random_values, 25)
```

Show the 75th quantile:

```
quantile(random_values, 75)
```

### Interquartile Range (IQR)

The `iqr` function returns the interquartile range, which is the difference between the 75th percentile (Q3) and 25th percentile (Q1). It is useful for identifying outliers and understanding the spread of the middle 50% of the data.

```
from datachart.utils.stats import iqr
```

```
iqr(random_values)
```

### Minimum

The `minimum` function returns the minimum of the values.

```
from datachart.utils.stats import minimum
```

```
minimum(random_values)
```

### Maximum

The `maximum` function returns the maximum of the values.

```
from datachart.utils.stats import maximum
```

```
maximum(random_values)
```

### Correlation

The `correlation` function calculates the Pearson correlation coefficient between two lists of values. It measures the linear relationship between the datasets, ranging from -1 (perfect negative correlation) to 1 (perfect positive correlation).

```
from datachart.utils.stats import correlation
```

Create a second list of random values to compare:

```
random_values_2 = random.sample(range(1, 100), 10)
random_values_2
```

```
correlation(random_values, random_values_2)
```

### Spearman correlation

The `spearman` function calculates the Spearman rank correlation between two lists of values. It is the Pearson correlation of the ranks, so it captures any monotone relationship (not only a linear one) and is robust to outliers.

```
from datachart.utils.stats import spearman
```

```
spearman(random_values, random_values_2)
```

### Mode

The `mode` function returns the most frequent value. It is meant for discrete data, where values repeat; ties are broken by taking the smallest of the most frequent values.

```
from datachart.utils.stats import mode
```

```
mode([3, 1, 2, 3, 1])
```

### Skewness

The `skewness` function measures the asymmetry of the values: positive when the tail extends to the right of the bulk, negative when it extends to the left, and zero for a symmetric distribution.

```
from datachart.utils.stats import skewness
```

```
skewness(random_values)
```

### Kurtosis

The `kurtosis` function measures how heavy the tails are compared to a normal distribution, which scores zero: positive for heavier tails and sharper peaks, negative for lighter tails and flatter shapes.

```
from datachart.utils.stats import kurtosis
```

```
kurtosis(random_values)
```

Shape statistics are easiest to read against the distribution they describe. A right-skewed sample drawn on a [datachart.charts.Histogram](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.Histogram) with its mean and median as `vlines` shows why the skewness is positive: the tail pulls the mean past the median.

```
from datachart.charts import Histogram
from datachart.constants import FIG_SIZE, SHOW_GRID

random.seed(5)
skewed_values = [random.lognormvariate(3, 0.5) for _ in range(300)]

Histogram(
    data=[{"x": value} for value in skewed_values],
    vlines=[
        {"x": mean(skewed_values), "label": "mean"},
        {"x": median(skewed_values), "label": "median", "style": {"plot_vline_style": "--"}},
    ],
    title=f"Skewness {skewness(skewed_values):.2f}, excess kurtosis {kurtosis(skewed_values):.2f}",
    xlabel="Value",
    ylabel="Count",
    show_legend=True,
    show_grid=SHOW_GRID.Y,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Linear fit

The `linear_fit` function fits a straight line `y = slope * x + intercept` to two lists of values and returns `(slope, intercept, r2)`, where `r2` says how much of the variation in `y` the line explains (1 is a perfect fit).

```
from datachart.utils.stats import linear_fit
```

```
slope, intercept, r2 = linear_fit(random_values, random_values_2)
slope, intercept, r2
```

The fit is a trend line: evaluate `slope * x + intercept` at the two ends of the x range and draw it as a [datachart.charts.LineChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.LineChart) over the [datachart.charts.ScatterChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.ScatterChart) of the points with [datachart.utils.Panel](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel). The `r2` goes in the title.

```
from datachart.charts import LineChart, ScatterChart
from datachart.utils import Panel

random.seed(11)
hours = [random.uniform(0, 10) for _ in range(40)]
scores = [40 + 5 * hour + random.gauss(0, 8) for hour in hours]
slope, intercept, r2 = linear_fit(hours, scores)

Panel(
    [
        ScatterChart(data=[{"x": x, "y": y} for x, y in zip(hours, scores)], subtitle="students"),
        LineChart(
            data=[{"x": x, "y": slope * x + intercept} for x in (min(hours), max(hours))],
            subtitle=f"fit: {slope:.1f} x + {intercept:.1f}",
        ),
    ],
    title=f"Test score against study hours (r² = {r2:.2f})",
    xlabel="Study hours",
    ylabel_left="Score",
    show_legend=True,
    show_grid=SHOW_GRID.Y,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Bootstrap confidence interval

The `bootstrap_ci` function estimates a confidence interval of a statistic (the `mean` by default) by resampling the values with replacement `n_resamples` times and taking the central `level` share of the results. Pass a `seed` to make the interval reproducible.

```
from datachart.utils.stats import bootstrap_ci
```

```
low, high = bootstrap_ci(random_values, level=0.95, seed=42)
low, high
```

The interval is a ready-made error bar. To show the uncertainty of each group's mean on a [datachart.charts.BarChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.BarChart), set each bar's `y` to the group mean and its `yerr` to the half-width of the interval, then turn on `show_yerr`:

```
from datachart.charts import BarChart

random.seed(7)
groups = {
    "Group A": [random.gauss(50, 10) for _ in range(30)],
    "Group B": [random.gauss(60, 20) for _ in range(30)],
    "Group C": [random.gauss(55, 5) for _ in range(30)],
}

data = []
for label, values in groups.items():
    low, high = bootstrap_ci(values, seed=42)
    data.append({"label": label, "y": mean(values), "yerr": (high - low) / 2})

BarChart(
    data=data,
    title="Group means with 95% bootstrap confidence intervals",
    xlabel="Group",
    ylabel="Mean",
    show_yerr=True,
).show()
```

### Histogram

The `histogram` function bins the values and returns the `(counts, edges)` lists, with one more edge than counts. The `bins` argument is passed straight to `numpy.histogram_bin_edges`: a rule name such as `"auto"`, `"fd"`, or `"rice"` picks the edges from the data, an integer sets the number of equal-width bins, and a list gives the edges explicitly.

```
from datachart.utils.stats import histogram
```

```
counts, edges = histogram(random_values, bins=4)
counts, edges
```

The counts and edges are a bar chart in waiting: label each bar with its lower edge and draw the counts with a [datachart.charts.BarChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.BarChart). Unlike the [datachart.charts.Histogram](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.Histogram) front, which takes an integer `num_bins`, the bin rule picks the number of bins from the data — here Freedman–Diaconis on the skewed sample above.

```
counts, edges = histogram(skewed_values, bins="fd")

BarChart(
    data=[{"label": f"{low:.0f}", "y": count} for count, low in zip(counts, edges)],
    title=f"Freedman–Diaconis rule: {len(counts)} bins",
    xlabel="Bin lower edge",
    ylabel="Count",
    show_grid=SHOW_GRID.Y,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Rolling mean

The `rolling_mean` function smooths a series with a trailing moving average. Each output is the mean of the `window` values ending at that index, so the result lines up with the input and is `nan` until the window fills. Let us create a noisy series to smooth:

```
from datachart.utils.stats import rolling_mean
```

```
random.seed(3)
noisy_series = [value + random.gauss(0, 10) for value in range(0, 120, 10)]
noisy_series
```

```
rolling_mean(noisy_series, window=3)
```

### Exponentially weighted moving average

The `ewma` function smooths a series by blending each value with the previous output, `alpha * value + (1 - alpha) * previous`. A larger `alpha` follows the data more closely; a smaller one smooths harder.

```
from datachart.utils.stats import ewma
```

```
ewma(noisy_series, alpha=0.3)
```

Both smoothers line up with the input, so they draw as extra series of one [datachart.charts.LineChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.LineChart) over the raw values. The rolling mean starts once its window fills (the leading `nan` values leave a gap); the EWMA starts at once but lags behind turns.

```
random.seed(3)
daily_sales = [50 + 0.5 * day + 8 * math.sin(day / 5) + random.gauss(0, 6) for day in range(90)]

series = {
    "daily sales": daily_sales,
    "rolling mean (7 days)": rolling_mean(daily_sales, window=7),
    "EWMA (alpha 0.2)": ewma(daily_sales, alpha=0.2),
}

LineChart(
    data=[[{"x": day, "y": value} for day, value in enumerate(values)] for values in series.values()],
    subtitle=list(series),
    title="Daily sales with two smoothers",
    xlabel="Day",
    ylabel="Units",
    show_legend=True,
    show_grid=SHOW_GRID.Y,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

When the raw series is context rather than the message, mute it instead of giving it an equal color: `emphasis` (see the [emphasis guide](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/styling/highlighting)) greys the raw line and drops it from the legend, and [datachart.utils.Panel](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) draws the smoothed series over it in the palette color.

```
from datachart.constants import EMPHASIS

Panel(
    [
        LineChart(
            data=[{"x": day, "y": value} for day, value in enumerate(daily_sales)],
            emphasis=EMPHASIS.BACKGROUND,
        ),
        LineChart(
            data=[
                {"x": day, "y": value}
                for day, value in enumerate(rolling_mean(daily_sales, window=7))
            ],
            subtitle="rolling mean (7 days)",
        ),
    ],
    title="Daily sales behind its 7-day mean",
    xlabel="Day",
    ylabel_left="Units",
    show_legend=True,
    show_grid=SHOW_GRID.Y,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### LOESS

The `loess` function smooths `(x, y)` points with a locally weighted linear fit: at each `x` a line is fitted to the nearest `frac` share of the points, weighted so closer points count more. It returns `{x, y}` points sorted by `x`, ready to draw as a [datachart.charts.LineChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.LineChart) over the raw points. The fit runs on numbers, so a datetime `x` goes through `matplotlib.dates.date2num` on the way in and `num2date` on the way back.

```
from datachart.utils.stats import loess
```

```
loess(list(range(len(noisy_series))), noisy_series, frac=0.5)
```

Because `loess` returns `{x, y}` points, the smoothed curve overlays the [datachart.charts.ScatterChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.ScatterChart) of the raw points through [datachart.utils.Panel](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) — a non-linear trend a straight `linear_fit` would miss.

```
random.seed(8)
x_points = [random.uniform(0, 10) for _ in range(80)]
y_points = [math.sin(x) + random.gauss(0, 0.3) for x in x_points]

Panel(
    [
        ScatterChart(data=[{"x": x, "y": y} for x, y in zip(x_points, y_points)], subtitle="points"),
        LineChart(data=loess(x_points, y_points, frac=0.3), subtitle="loess (frac 0.3)"),
    ],
    title="LOESS through noisy points",
    xlabel="x",
    ylabel_left="y",
    show_legend=True,
    show_grid=SHOW_GRID.Y,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Kernel density estimate

The `kde1d` function estimates the density of a list of values with a Gaussian kernel and returns it as `{x, y}` points, ready to draw as a [datachart.charts.LineChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.LineChart) — over a density [datachart.charts.Histogram](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.Histogram) of the same values, for instance. The `bandwidth` is a rule of [datachart.constants.BANDWIDTH](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.BANDWIDTH) or a scalar factor, `gridsize` the number of points, and `cut` how many bandwidths the curve extends past the extremes (`xlim` fixes the range instead).

```
from datachart.utils.stats import kde1d
```

```
curve = kde1d(random_values, gridsize=5)
curve
```

Drawn as a [datachart.charts.LineChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.LineChart) with `show_area`, the curve is the density chart of the skewed sample; the [Histogram guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/histogram/#density-curve) overlays it on a density histogram.

```
LineChart(
    data=kde1d(skewed_values),
    title="Kernel density of the skewed sample",
    xlabel="Value",
    ylabel="Density",
    show_area=True,
    show_grid=SHOW_GRID.Y,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

The `kde2d` function does the same for `(x, y)` points and returns the `{x, y, z}` surface a [datachart.charts.ContourChart](https://eriknovak.github.io/datachart/dev/references/charts/#datachart.charts.ContourChart) draws — the density contours of a scattered dataset. The `gridsize` can be one number or an `(x, y)` pair of column and row counts, and `xlim`/`ylim` fix the grid so several surfaces share it.

```
from datachart.utils.stats import kde2d
```

```
surface = kde2d(random_values, random_values_2, gridsize=3)
surface
```
