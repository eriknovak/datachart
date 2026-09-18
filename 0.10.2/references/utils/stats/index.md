# Stats Module

## datachart.utils.stats

The module containing the `stats` methods.

The `stats` module provides the statistics behind the charts: centers and spreads, shape, correlation, a linear fit, bootstrap intervals, histogram bins, smoothers, and density estimates. Every function takes plain Python lists.

## Choosing a Function

Every function takes plain Python lists and returns a number, a pair, or lists ready to feed back into a chart. The groups below match the [Statistics guide](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/utility/stats/index.md), which shows each one on a chart.

| I want to…                      | Use                                                                                                                                                                                                                                                                  |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| a center, count, or total       | [`mean`](#datachart.utils.stats.mean), [`median`](#datachart.utils.stats.median), [`mode`](#datachart.utils.stats.mode), [`count`](#datachart.utils.stats.count), [`sum_values`](#datachart.utils.stats.sum_values)                                                  |
| how far the values spread       | [`stdev`](#datachart.utils.stats.stdev), [`variance`](#datachart.utils.stats.variance), [`quantile`](#datachart.utils.stats.quantile), [`iqr`](#datachart.utils.stats.iqr), [`minimum`](#datachart.utils.stats.minimum), [`maximum`](#datachart.utils.stats.maximum) |
| the shape of a distribution     | [`skewness`](#datachart.utils.stats.skewness), [`kurtosis`](#datachart.utils.stats.kurtosis)                                                                                                                                                                         |
| how two variables move together | [`correlation`](#datachart.utils.stats.correlation), [`spearman`](#datachart.utils.stats.spearman)                                                                                                                                                                   |
| a trend line                    | [`linear_fit`](#datachart.utils.stats.linear_fit)                                                                                                                                                                                                                    |
| an interval around a statistic  | [`bootstrap_ci`](#datachart.utils.stats.bootstrap_ci)                                                                                                                                                                                                                |
| bins for a histogram            | [`histogram`](#datachart.utils.stats.histogram)                                                                                                                                                                                                                      |
| a smoothed series               | [`rolling_mean`](#datachart.utils.stats.rolling_mean), [`ewma`](#datachart.utils.stats.ewma), [`loess`](#datachart.utils.stats.loess)                                                                                                                                |
| a density curve or surface      | [`kde1d`](#datachart.utils.stats.kde1d), [`kde2d`](#datachart.utils.stats.kde2d)                                                                                                                                                                                     |

## Center

### datachart.utils.stats.count

```
count(values: list[int | float]) -> int
```

Counts the number of elements in a list.

Examples:

```
>>> from datachart.utils.stats import count
>>> count([1, 2, 3, 4, 5])
5
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION                         |
| ------- | ----------------------------------- |
| `int`   | The number of elements in the list. |

### datachart.utils.stats.sum_values

```
sum_values(values: list[int | float]) -> float
```

Calculates the sum of all values.

Examples:

```
>>> from datachart.utils.stats import sum_values
>>> sum_values([1, 2, 3, 4, 5])
15.0
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION            |
| ------- | ---------------------- |
| `float` | The sum of all values. |

### datachart.utils.stats.mean

```
mean(values: list[int | float]) -> float
```

Calculates the mean of the values.

Examples:

```
>>> from datachart.utils.stats import mean
>>> mean([1, 2, 3, 4, 5])
3.0
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION             |
| ------- | ----------------------- |
| `float` | The mean of the values. |

### datachart.utils.stats.median

```
median(values: list[int | float]) -> float
```

Calculates the median of the values.

Examples:

```
>>> from datachart.utils.stats import median
>>> median([1, 2, 3, 4, 5])
3.0
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION               |
| ------- | ------------------------- |
| `float` | The median of the values. |

### datachart.utils.stats.mode

```
mode(values: list[int | float]) -> float
```

Gets the most frequent value.

Meant for discrete data, where values repeat; on continuous data every value tends to be unique and the mode is just the smallest one. Ties are broken by taking the smallest of the most frequent values.

Examples:

```
>>> from datachart.utils.stats import mode
>>> mode([3, 1, 2, 3, 1])
1.0
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION                                              |
| ------- | -------------------------------------------------------- |
| `float` | The smallest most frequent value; nan for an empty list. |

| RAISES      | DESCRIPTION                             |
| ----------- | --------------------------------------- |
| `TypeError` | If values is not a list or numpy array. |

## Spread

### datachart.utils.stats.stdev

```
stdev(values: list[int | float]) -> float
```

Calculates the standard deviation of the values.

Examples:

```
>>> from datachart.utils.stats import stdev
>>> stdev([1, 2, 3, 4, 5])
1.4142135623730951
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION                           |
| ------- | ------------------------------------- |
| `float` | The standard deviation of the values. |

### datachart.utils.stats.variance

```
variance(values: list[int | float]) -> float
```

Calculates the variance of the values.

Examples:

```
>>> from datachart.utils.stats import variance
>>> variance([1, 2, 3, 4, 5])
2.0
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION                 |
| ------- | --------------------------- |
| `float` | The variance of the values. |

### datachart.utils.stats.quantile

```
quantile(values: list[int | float], q: float) -> float
```

Calculates the quantile of the values.

Examples:

```
>>> from datachart.utils.stats import quantile
>>> quantile([1, 2, 3, 4, 5], 25)
2.0
```

| PARAMETER | DESCRIPTION                                          |
| --------- | ---------------------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int            |
| `q`       | The quantile to calculate (0-100). **TYPE:** `float` |

| RETURNS | DESCRIPTION                 |
| ------- | --------------------------- |
| `float` | The quantile of the values. |

### datachart.utils.stats.iqr

```
iqr(values: list[int | float]) -> float
```

Calculates the interquartile range (Q3 - Q1).

The interquartile range is the difference between the 75th percentile (Q3) and the 25th percentile (Q1). It is a measure of statistical dispersion and is useful for identifying outliers.

Examples:

```
>>> from datachart.utils.stats import iqr
>>> iqr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
4.5
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION                            |
| ------- | -------------------------------------- |
| `float` | The interquartile range of the values. |

### datachart.utils.stats.minimum

```
minimum(values: list[Any]) -> Any
```

Gets the minimum of the values.

Numeric values return a float; any other ordered values, such as datetimes, return their minimum unchanged.

Examples:

```
>>> from datachart.utils.stats import minimum
>>> minimum([1, 2, 3, 4, 5])
1
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** `list[Any]` |

| RETURNS | DESCRIPTION                                                            |
| ------- | ---------------------------------------------------------------------- |
| `Any`   | The minimum of the values: a float for numbers, else the value itself. |

### datachart.utils.stats.maximum

```
maximum(values: list[Any]) -> Any
```

Gets the maximum of the values.

Numeric values return a float; any other ordered values, such as datetimes, return their maximum unchanged.

Examples:

```
>>> from datachart.utils.stats import maximum
>>> maximum([1, 2, 3, 4, 5])
5
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** `list[Any]` |

| RETURNS | DESCRIPTION                                                            |
| ------- | ---------------------------------------------------------------------- |
| `Any`   | The maximum of the values: a float for numbers, else the value itself. |

## Shape

### datachart.utils.stats.skewness

```
skewness(values: list[int | float]) -> float
```

Calculates the skewness of the values.

Skewness measures the asymmetry of the distribution: positive when the tail extends to the right of the bulk, negative when it extends to the left, and zero for a symmetric distribution.

Examples:

```
>>> from datachart.utils.stats import skewness
>>> skewness([1, 2, 3, 4, 5])
0.0
>>> round(skewness([1, 1, 1, 2, 10]), 3)
1.457
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION                                                    |
| ------- | -------------------------------------------------------------- |
| `float` | The skewness of the values; nan for fewer than two values or a |
| `float` | constant list.                                                 |

| RAISES      | DESCRIPTION                             |
| ----------- | --------------------------------------- |
| `TypeError` | If values is not a list or numpy array. |

### datachart.utils.stats.kurtosis

```
kurtosis(values: list[int | float]) -> float
```

Calculates the excess kurtosis of the values.

Kurtosis measures how heavy the tails of the distribution are compared to a normal distribution, which scores zero: positive for heavier tails and sharper peaks, negative for lighter tails and flatter shapes.

Examples:

```
>>> from datachart.utils.stats import kurtosis
>>> kurtosis([1, 2, 3, 4, 5])
-1.3
```

| PARAMETER | DESCRIPTION                               |
| --------- | ----------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int |

| RETURNS | DESCRIPTION                                                         |
| ------- | ------------------------------------------------------------------- |
| `float` | The excess kurtosis of the values; nan for fewer than two values or |
| `float` | a constant list.                                                    |

| RAISES      | DESCRIPTION                             |
| ----------- | --------------------------------------- |
| `TypeError` | If values is not a list or numpy array. |

## Association

### datachart.utils.stats.correlation

```
correlation(
    x: list[int | float], y: list[int | float]
) -> float
```

Calculates the Pearson correlation coefficient between two lists.

The Pearson correlation coefficient measures the linear relationship between two datasets. It ranges from -1 (perfect negative correlation) to 1 (perfect positive correlation), with 0 indicating no linear correlation. A temporal `x` (dates, datetimes, or `datetime64`) is correlated as matplotlib date numbers.

Examples:

```
>>> from datachart.utils.stats import correlation
>>> correlation([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
1.0
>>> correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
-1.0
```

| PARAMETER | DESCRIPTION                                                          |
| --------- | -------------------------------------------------------------------- |
| `x`       | The first list of values, numeric or temporal. **TYPE:** \`list\[int |
| `y`       | The second list of values. **TYPE:** \`list\[int                     |

| RETURNS | DESCRIPTION                          |
| ------- | ------------------------------------ |
| `float` | The Pearson correlation coefficient. |

| RAISES       | DESCRIPTION                                                                     |
| ------------ | ------------------------------------------------------------------------------- |
| `TypeError`  | If x or y is not a list or numpy array, or x mixes temporal and numeric values. |
| `ValueError` | If x and y have different lengths.                                              |

### datachart.utils.stats.spearman

```
spearman(
    x: list[int | float], y: list[int | float]
) -> float
```

Calculates the Spearman rank correlation between two lists.

The Spearman coefficient is the Pearson correlation of the ranks, so it measures any monotone relationship, not only a linear one, and is robust to outliers. It ranges from -1 to 1 like `correlation`, and likewise accepts a temporal `x`.

Examples:

```
>>> from datachart.utils.stats import spearman
>>> round(spearman([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]), 6)
1.0
>>> round(spearman([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]), 6)
-1.0
```

| PARAMETER | DESCRIPTION                                                          |
| --------- | -------------------------------------------------------------------- |
| `x`       | The first list of values, numeric or temporal. **TYPE:** \`list\[int |
| `y`       | The second list of values. **TYPE:** \`list\[int                     |

| RETURNS | DESCRIPTION                                                       |
| ------- | ----------------------------------------------------------------- |
| `float` | The Spearman rank correlation; nan for fewer than two points or a |
| `float` | constant list.                                                    |

| RAISES       | DESCRIPTION                                                                     |
| ------------ | ------------------------------------------------------------------------------- |
| `TypeError`  | If x or y is not a list or numpy array, or x mixes temporal and numeric values. |
| `ValueError` | If x and y have different lengths.                                              |

## Trend Line

### datachart.utils.stats.linear_fit

```
linear_fit(
    x: list[int | float], y: list[int | float]
) -> tuple[float, float, float]
```

Fits a straight line to the (x, y) points.

An ordinary least-squares fit of `y = slope * x + intercept`, with the coefficient of determination `r2` saying how much of the variation in `y` the line explains (1 is a perfect fit). A temporal `x` (dates, datetimes, or `datetime64`) is fitted as matplotlib date numbers, so the slope is per day and the intercept is relative to matplotlib's date epoch.

Examples:

```
>>> from datachart.utils.stats import linear_fit
>>> slope, intercept, r2 = linear_fit([0, 1, 2, 3], [1, 3, 5, 7])
>>> round(slope, 6), round(intercept, 6), round(r2, 6)
(2.0, 1.0, 1.0)
```

| PARAMETER | DESCRIPTION                                                            |
| --------- | ---------------------------------------------------------------------- |
| `x`       | The x values of the points, numeric or temporal. **TYPE:** \`list\[int |
| `y`       | The y values of the points, one per x value. **TYPE:** \`list\[int     |

| RETURNS                      | DESCRIPTION                                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| `float`                      | The (slope, intercept, r2) of the fitted line, the slope per day  |
| `float`                      | for a temporal x; all nan for fewer than two points or a constant |
| `float`                      | x, and r2 alone nan for a constant y, which leaves no             |
| `tuple[float, float, float]` | variation to explain.                                             |

| RAISES       | DESCRIPTION                                                                     |
| ------------ | ------------------------------------------------------------------------------- |
| `TypeError`  | If x or y is not a list or numpy array, or x mixes temporal and numeric values. |
| `ValueError` | If x and y have different lengths.                                              |

## Confidence Intervals

### datachart.utils.stats.bootstrap_ci

```
bootstrap_ci(
    values: list[int | float],
    statistic: Callable[
        [List[Union[int, float]]], float
    ] = mean,
    level: float = 0.95,
    n_resamples: int = 1000,
    seed: int | np.random.Generator | None = None,
) -> tuple[float, float]
```

Estimates a confidence interval of a statistic by bootstrapping.

The values are resampled with replacement `n_resamples` times, the statistic is computed on each resample, and the interval is the central `level` share of those results (the percentile bootstrap). The half-width of the interval is a ready-made error bar for a `BarChart`.

Examples:

```
>>> from datachart.utils.stats import bootstrap_ci, median
>>> low, high = bootstrap_ci([1, 2, 3, 4, 5, 6, 7, 8], seed=0)
>>> low < 4.5 < high
True
>>> bootstrap_ci([1, 2, 3, 4, 100], statistic=median, seed=0)[1] <= 100
True
```

| PARAMETER     | DESCRIPTION                                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `values`      | The list of values. **TYPE:** \`list\[int                                                                                           |
| `statistic`   | The function of the values to estimate, mean by default. **TYPE:** `Callable[[List[Union[int, float]]], float]` **DEFAULT:** `mean` |
| `level`       | The confidence level, strictly between 0 and 1. **TYPE:** `float` **DEFAULT:** `0.95`                                               |
| `n_resamples` | The number of resamples to draw. **TYPE:** `int` **DEFAULT:** `1000`                                                                |
| `seed`        | An integer or numpy.random.Generator that makes the resamples reproducible. **TYPE:** \`int                                         |

| RETURNS | DESCRIPTION                                                     |
| ------- | --------------------------------------------------------------- |
| `float` | The (low, high) bounds of the interval; both nan for fewer than |
| `float` | two values.                                                     |

| RAISES       | DESCRIPTION                                                     |
| ------------ | --------------------------------------------------------------- |
| `TypeError`  | If values is not a list or numpy array.                         |
| `ValueError` | If level is not between 0 and 1 or n_resamples is not positive. |

## Binning

### datachart.utils.stats.histogram

```
histogram(
    values: list[int | float],
    bins: str | int | list[int | float] = "auto",
) -> tuple[list[int], list[float]]
```

Bins the values into histogram counts and edges.

The `bins` are passed straight to `numpy.histogram_bin_edges`: a rule name such as `"auto"`, `"fd"`, `"rice"`, or `"sturges"` picks the edges from the data, an integer sets the number of equal-width bins, and a list gives the edges explicitly. These rules are unrelated to the `CONTOUR_LEVELS` rules that share their names.

Examples:

```
>>> from datachart.utils.stats import histogram
>>> histogram([1, 2, 2, 3, 3, 3, 4], bins=3)
([1, 2, 4], [1.0, 2.0, 3.0, 4.0])
```

| PARAMETER | DESCRIPTION                                                                |
| --------- | -------------------------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int                                  |
| `bins`    | A bin rule name, a number of bins, or a list of bin edges. **TYPE:** \`str |

| RETURNS       | DESCRIPTION                                                     |
| ------------- | --------------------------------------------------------------- |
| `list[int]`   | The (counts, edges) lists, with one more edge than counts; both |
| `list[float]` | empty for an empty list.                                        |

| RAISES       | DESCRIPTION                             |
| ------------ | --------------------------------------- |
| `TypeError`  | If values is not a list or numpy array. |
| `ValueError` | If the bin rule is unknown.             |

## Smoothing

### datachart.utils.stats.rolling_mean

```
rolling_mean(
    values: list[int | float], window: int
) -> list[float]
```

Smooths the values with a trailing moving average.

Each output is the mean of the `window` values ending at that index, so the result lines up with the input and is `nan` until the window fills.

Examples:

```
>>> from datachart.utils.stats import rolling_mean
>>> rolling_mean([1, 2, 3, 4, 5], 3)
[nan, nan, 2.0, 3.0, 4.0]
```

| PARAMETER | DESCRIPTION                                                |
| --------- | ---------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int                  |
| `window`  | The number of values averaged, at least 1. **TYPE:** `int` |

| RETURNS       | DESCRIPTION                               |
| ------------- | ----------------------------------------- |
| `list[float]` | The smoothed values, one per input value. |

| RAISES       | DESCRIPTION                                                              |
| ------------ | ------------------------------------------------------------------------ |
| `TypeError`  | If values is not a list or numpy array, or the window is not an integer. |
| `ValueError` | If the window is not positive.                                           |

### datachart.utils.stats.ewma

```
ewma(
    values: list[int | float], alpha: float
) -> list[float]
```

Smooths the values with an exponentially weighted moving average.

Each output blends the current value with the previous output, `alpha * value + (1 - alpha) * previous`, starting from the first value. A larger `alpha` follows the data more closely; a smaller one smooths harder.

Examples:

```
>>> from datachart.utils.stats import ewma
>>> ewma([1, 2, 3], 0.5)
[1.0, 1.5, 2.25]
```

| PARAMETER | DESCRIPTION                                                    |
| --------- | -------------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** \`list\[int                      |
| `alpha`   | The weight of the current value, in (0, 1\]. **TYPE:** `float` |

| RETURNS       | DESCRIPTION                               |
| ------------- | ----------------------------------------- |
| `list[float]` | The smoothed values, one per input value. |

| RAISES       | DESCRIPTION                             |
| ------------ | --------------------------------------- |
| `TypeError`  | If values is not a list or numpy array. |
| `ValueError` | If alpha is not in (0, 1\].             |

### datachart.utils.stats.loess

```
loess(
    x: list[int | float],
    y: list[int | float],
    frac: float = 0.3,
) -> list[dict[str, float]]
```

Smooths the (x, y) points with a locally weighted linear fit.

At each `x` a straight line is fitted to the nearest `frac` share of the points, weighted by a tricube kernel so closer points count more, and the smoothed `y` is that line's value there (LOESS/LOWESS). The result is a list of `{x, y}` points sorted by `x`, ready for `LineChart`, as `kde1d` returns. A smaller `frac` follows the data more closely. A temporal `x` (dates, datetimes, or `datetime64`) is smoothed as date numbers and the curve's `x` values come back as datetimes, in the input's zone.

Examples:

```
>>> from datachart.utils.stats import loess
>>> curve = loess([5, 1, 3, 2, 4], [11, 3, 7, 5, 9], frac=0.6)
>>> [(point["x"], round(point["y"], 6)) for point in curve]
[(1.0, 3.0), (2.0, 5.0), (3.0, 7.0), (4.0, 9.0), (5.0, 11.0)]
```

| PARAMETER | DESCRIPTION                                                                                   |
| --------- | --------------------------------------------------------------------------------------------- |
| `x`       | The x values of the points, numeric or temporal. **TYPE:** \`list\[int                        |
| `y`       | The y values of the points, one per x value. **TYPE:** \`list\[int                            |
| `frac`    | The share of the points each local fit uses, in (0, 1\]. **TYPE:** `float` **DEFAULT:** `0.3` |

| RETURNS                  | DESCRIPTION                                                    |
| ------------------------ | -------------------------------------------------------------- |
| `list[dict[str, float]]` | The {x, y} points of the smoothed curve, sorted by x; the y is |
| `list[dict[str, float]]` | nan for fewer than two points.                                 |

| RAISES       | DESCRIPTION                                                                     |
| ------------ | ------------------------------------------------------------------------------- |
| `TypeError`  | If x or y is not a list or numpy array, or x mixes temporal and numeric values. |
| `ValueError` | If x and y have different lengths or frac is not in (0, 1\].                    |

## Density Estimates

### datachart.utils.stats.kde1d

```
kde1d(
    values: list[int | float],
    *,
    bandwidth: BANDWIDTH | str | float | None = None,
    gridsize: int = 100,
    cut: float = 3,
    xlim: tuple[float, float] | None = None
) -> list[dict[str, float]]
```

Estimates the density of the values as a curve.

A Gaussian kernel density estimate evaluated on `gridsize` evenly spaced points over the range of the values, extended by `cut` bandwidths on each side so the curve tails off instead of being clipped at the extremes, or over an explicit `xlim` so several curves share one grid. The result is a list of `{x, y}` points ready for `LineChart`; the curve integrates to 1, so it overlays a density `Histogram` of the same values.

Examples:

```
>>> from datachart.utils.stats import kde1d
>>> curve = kde1d([1, 2, 2, 3, 3, 3, 4, 4, 5], gridsize=5, cut=0)
>>> [round(point["x"], 2) for point in curve]
[1.0, 2.0, 3.0, 4.0, 5.0]
>>> round(sum(point["y"] for point in curve), 2)
0.94
```

| PARAMETER   | DESCRIPTION                                                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- |
| `values`    | The values to estimate the density of. **TYPE:** \`list\[int                                                                |
| `bandwidth` | The kernel bandwidth: None or "scott" (Scott's rule), "silverman", or a scalar factor. See BANDWIDTH. **TYPE:** \`BANDWIDTH |
| `gridsize`  | The number of points the curve is evaluated on. **TYPE:** `int` **DEFAULT:** `100`                                          |
| `cut`       | How many bandwidths to extend the grid past the extremes. **TYPE:** `float` **DEFAULT:** `3`                                |
| `xlim`      | The (min, max) range of the grid; overrides the padded range. **TYPE:** \`tuple[float, float]                               |

| RETURNS                  | DESCRIPTION                             |
| ------------------------ | --------------------------------------- |
| `list[dict[str, float]]` | The {x, y} points of the density curve. |

| RAISES       | DESCRIPTION                                                                             |
| ------------ | --------------------------------------------------------------------------------------- |
| `ValueError` | If the bandwidth is invalid, there are fewer than two values, or a value is not finite. |

### datachart.utils.stats.kde2d

```
kde2d(
    x: list[int | float],
    y: list[int | float],
    *,
    bandwidth: BANDWIDTH | str | float | None = None,
    gridsize: int | tuple[int, int] = 100,
    cut: float = 3,
    xlim: tuple[Any, Any] | None = None,
    ylim: tuple[float, float] | None = None
) -> dict[str, list]
```

Estimates the density of the (x, y) points as a gridded surface.

A Gaussian kernel density estimate evaluated on a `gridsize` × `gridsize` grid over the range of the points, extended by `cut` bandwidths on each side so the outer contours close instead of being clipped, or over explicit `xlim`/`ylim` so several surfaces share one grid. The result is an `{x, y, z}` chart dict ready for `ContourChart` — the density chart of a scattered dataset is `ContourChart(kde2d(x, y))`. A temporal `x` (dates, datetimes, or `datetime64`) gives a grid of datetime `x` values, in the input's zone, and `xlim` may then be a pair of datetimes.

Examples:

```
>>> from datachart.utils.stats import kde2d
>>> surface = kde2d([1, 2, 3, 4], [1, 3, 2, 4], gridsize=(3, 2), cut=0)
>>> surface["x"], surface["y"]
([1.0, 2.5, 4.0], [1.0, 4.0])
>>> [[round(z, 3) for z in row] for row in surface["z"]]
[[0.075, 0.038, 0.001], [0.001, 0.038, 0.075]]
```

| PARAMETER   | DESCRIPTION                                                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- |
| `x`         | The x values of the points, numeric or temporal. **TYPE:** \`list\[int                                                      |
| `y`         | The y values of the points, one per x value. **TYPE:** \`list\[int                                                          |
| `bandwidth` | The kernel bandwidth: None or "scott" (Scott's rule), "silverman", or a scalar factor. See BANDWIDTH. **TYPE:** \`BANDWIDTH |
| `gridsize`  | The number of grid columns and rows, as one number or an (x, y) pair. **TYPE:** \`int                                       |
| `cut`       | How many bandwidths to extend the grid past the extremes. **TYPE:** `float` **DEFAULT:** `3`                                |
| `xlim`      | The (min, max) x range of the grid; overrides the padded range. **TYPE:** \`tuple[Any, Any]                                 |
| `ylim`      | The (min, max) y range of the grid; overrides the padded range. **TYPE:** \`tuple[float, float]                             |

| RETURNS           | DESCRIPTION                                      |
| ----------------- | ------------------------------------------------ |
| `dict[str, list]` | The {x, y, z} chart dict of the density surface. |

| RAISES       | DESCRIPTION                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------- |
| `TypeError`  | If x or xlim mixes temporal and numeric values, or xlim is temporal while x is not, or the other way around.      |
| `ValueError` | If the bandwidth is invalid, x and y differ in length, there are fewer than two points, or a value is not finite. |
