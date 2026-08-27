# Stats Module

## datachart.utils.stats

The module containing the `stats` methods.

The `stats` module provides methods for calculating statistics.

| FUNCTION      | DESCRIPTION                                                       |
| ------------- | ----------------------------------------------------------------- |
| `count`       | Counts the number of elements in the list.                        |
| `sum_values`  | Calculates the sum of the values.                                 |
| `mean`        | Calculates the mean of the values.                                |
| `median`      | Calculates the median of the values.                              |
| `stdev`       | Calculates the standard deviation of the values.                  |
| `variance`    | Calculates the variance of the values.                            |
| `quantile`    | Calculates the quantile of the values.                            |
| `iqr`         | Calculates the interquartile range (Q3 - Q1).                     |
| `minimum`     | Gets the minimum of the values.                                   |
| `maximum`     | Gets the maximum of the values.                                   |
| `correlation` | Calculates the Pearson correlation coefficient between two lists. |
| `kde1d`       | Estimates the density of the values as a curve.                   |
| `kde2d`       | Estimates the density of the (x, y) points as a gridded surface.  |

## Functions

### datachart.utils.stats.count

```
count(values: List[Union[int, float]]) -> int
```

Counts the number of elements in a list.

Examples:

```
>>> from datachart.utils.stats import count
>>> count([1, 2, 3, 4, 5])
5
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION                         |
| ------- | ----------------------------------- |
| `int`   | The number of elements in the list. |

### datachart.utils.stats.sum_values

```
sum_values(values: List[Union[int, float]]) -> float
```

Calculates the sum of all values.

Added in v0.7.0

Examples:

```
>>> from datachart.utils.stats import sum_values
>>> sum_values([1, 2, 3, 4, 5])
15.0
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION            |
| ------- | ---------------------- |
| `float` | The sum of all values. |

### datachart.utils.stats.mean

```
mean(values: List[Union[int, float]]) -> float
```

Calculates the mean of the values.

Examples:

```
>>> from datachart.utils.stats import mean
>>> mean([1, 2, 3, 4, 5])
3.0
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION             |
| ------- | ----------------------- |
| `float` | The mean of the values. |

### datachart.utils.stats.median

```
median(values: List[Union[int, float]]) -> float
```

Calculates the median of the values.

Examples:

```
>>> from datachart.utils.stats import median
>>> median([1, 2, 3, 4, 5])
3.0
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION               |
| ------- | ------------------------- |
| `float` | The median of the values. |

### datachart.utils.stats.stdev

```
stdev(values: List[Union[int, float]]) -> float
```

Calculates the standard deviation of the values.

Examples:

```
>>> from datachart.utils.stats import stdev
>>> stdev([1, 2, 3, 4, 5])
1.4142135623730951
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION                           |
| ------- | ------------------------------------- |
| `float` | The standard deviation of the values. |

### datachart.utils.stats.variance

```
variance(values: List[Union[int, float]]) -> float
```

Calculates the variance of the values.

Added in v0.7.0

Examples:

```
>>> from datachart.utils.stats import variance
>>> variance([1, 2, 3, 4, 5])
2.0
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION                 |
| ------- | --------------------------- |
| `float` | The variance of the values. |

### datachart.utils.stats.quantile

```
quantile(
    values: List[Union[int, float]], q: float
) -> float
```

Calculates the quantile of the values.

Examples:

```
>>> from datachart.utils.stats import quantile
>>> quantile([1, 2, 3, 4, 5], 25)
2.0
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |
| `q`       | The quantile to calculate (0-100). **TYPE:** `float`    |

| RETURNS | DESCRIPTION                 |
| ------- | --------------------------- |
| `float` | The quantile of the values. |

### datachart.utils.stats.iqr

```
iqr(values: List[Union[int, float]]) -> float
```

Calculates the interquartile range (Q3 - Q1).

Added in v0.7.0

The interquartile range is the difference between the 75th percentile (Q3) and the 25th percentile (Q1). It is a measure of statistical dispersion and is useful for identifying outliers.

Examples:

```
>>> from datachart.utils.stats import iqr
>>> iqr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
4.5
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION                            |
| ------- | -------------------------------------- |
| `float` | The interquartile range of the values. |

### datachart.utils.stats.minimum

```
minimum(values: List[Union[int, float]]) -> float
```

Gets the minimum of the values.

Examples:

```
>>> from datachart.utils.stats import minimum
>>> minimum([1, 2, 3, 4, 5])
1
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION                |
| ------- | -------------------------- |
| `float` | The minimum of the values. |

### datachart.utils.stats.maximum

```
maximum(values: List[Union[int, float]]) -> float
```

Gets the maximum of the values.

Examples:

```
>>> from datachart.utils.stats import maximum
>>> maximum([1, 2, 3, 4, 5])
5
```

| PARAMETER | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `values`  | The list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION                |
| ------- | -------------------------- |
| `float` | The maximum of the values. |

### datachart.utils.stats.correlation

```
correlation(
    x: List[Union[int, float]], y: List[Union[int, float]]
) -> float
```

Calculates the Pearson correlation coefficient between two lists.

Added in v0.7.0

The Pearson correlation coefficient measures the linear relationship between two datasets. It ranges from -1 (perfect negative correlation) to 1 (perfect positive correlation), with 0 indicating no linear correlation.

Examples:

```
>>> from datachart.utils.stats import correlation
>>> correlation([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
1.0
>>> correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
-1.0
```

| PARAMETER | DESCRIPTION                                                    |
| --------- | -------------------------------------------------------------- |
| `x`       | The first list of values. **TYPE:** `List[Union[int, float]]`  |
| `y`       | The second list of values. **TYPE:** `List[Union[int, float]]` |

| RETURNS | DESCRIPTION                          |
| ------- | ------------------------------------ |
| `float` | The Pearson correlation coefficient. |

| RAISES       | DESCRIPTION                             |
| ------------ | --------------------------------------- |
| `TypeError`  | If x or y is not a list or numpy array. |
| `ValueError` | If x and y have different lengths.      |

### datachart.utils.stats.kde1d

```
kde1d(
    values: List[Union[int, float]],
    *,
    bandwidth: Optional[
        Union[BANDWIDTH, str, float]
    ] = None,
    gridsize: int = 100,
    cut: float = 3,
    xlim: Optional[Tuple[float, float]] = None
) -> List[Dict[str, float]]
```

Estimates the density of the values as a curve.

A Gaussian kernel density estimate evaluated on `gridsize` evenly spaced points over the range of the values, extended by `cut` bandwidths on each side so the curve tails off instead of being clipped at the extremes, or over an explicit `xlim` so several curves share one grid. The result is a list of `{x, y}` points ready for `LineChart`; the curve integrates to 1, so it overlays a density `Histogram` of the same values.

Added in Unreleased

Examples:

```
>>> from datachart.utils.stats import kde1d
>>> curve = kde1d([1, 2, 2, 3, 3, 3, 4, 4, 5], gridsize=5, cut=0)
>>> [round(point["x"], 2) for point in curve]
[1.0, 2.0, 3.0, 4.0, 5.0]
>>> round(sum(point["y"] for point in curve), 2)
0.94
```

| PARAMETER   | DESCRIPTION                                                                                                                                                                  |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `values`    | The values to estimate the density of. **TYPE:** `List[Union[int, float]]`                                                                                                   |
| `bandwidth` | The kernel bandwidth: None or "scott" (Scott's rule), "silverman", or a scalar factor. See BANDWIDTH. **TYPE:** `Optional[Union[BANDWIDTH, str, float]]` **DEFAULT:** `None` |
| `gridsize`  | The number of points the curve is evaluated on. **TYPE:** `int` **DEFAULT:** `100`                                                                                           |
| `cut`       | How many bandwidths to extend the grid past the extremes. **TYPE:** `float` **DEFAULT:** `3`                                                                                 |
| `xlim`      | The (min, max) range of the grid; overrides the padded range. **TYPE:** `Optional[Tuple[float, float]]` **DEFAULT:** `None`                                                  |

| RETURNS                  | DESCRIPTION                             |
| ------------------------ | --------------------------------------- |
| `List[Dict[str, float]]` | The {x, y} points of the density curve. |

| RAISES       | DESCRIPTION                                                                             |
| ------------ | --------------------------------------------------------------------------------------- |
| `ValueError` | If the bandwidth is invalid, there are fewer than two values, or a value is not finite. |

### datachart.utils.stats.kde2d

```
kde2d(
    x: List[Union[int, float]],
    y: List[Union[int, float]],
    *,
    bandwidth: Optional[
        Union[BANDWIDTH, str, float]
    ] = None,
    gridsize: Union[int, Tuple[int, int]] = 100,
    cut: float = 3,
    xlim: Optional[Tuple[float, float]] = None,
    ylim: Optional[Tuple[float, float]] = None
) -> Dict[str, List]
```

Estimates the density of the (x, y) points as a gridded surface.

A Gaussian kernel density estimate evaluated on a `gridsize` × `gridsize` grid over the range of the points, extended by `cut` bandwidths on each side so the outer contours close instead of being clipped, or over explicit `xlim`/`ylim` so several surfaces share one grid. The result is an `{x, y, z}` chart dict ready for `ContourChart` — the density chart of a scattered dataset is `ContourChart(kde2d(x, y))`.

Added in Unreleased

Examples:

```
>>> from datachart.utils.stats import kde2d
>>> surface = kde2d([1, 2, 3, 4], [1, 3, 2, 4], gridsize=(3, 2), cut=0)
>>> surface["x"], surface["y"]
([1.0, 2.5, 4.0], [1.0, 4.0])
>>> [[round(z, 3) for z in row] for row in surface["z"]]
[[0.075, 0.038, 0.001], [0.001, 0.038, 0.075]]
```

| PARAMETER   | DESCRIPTION                                                                                                                                                                  |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `x`         | The x values of the points. **TYPE:** `List[Union[int, float]]`                                                                                                              |
| `y`         | The y values of the points, one per x value. **TYPE:** `List[Union[int, float]]`                                                                                             |
| `bandwidth` | The kernel bandwidth: None or "scott" (Scott's rule), "silverman", or a scalar factor. See BANDWIDTH. **TYPE:** `Optional[Union[BANDWIDTH, str, float]]` **DEFAULT:** `None` |
| `gridsize`  | The number of grid columns and rows, as one number or an (x, y) pair. **TYPE:** `Union[int, Tuple[int, int]]` **DEFAULT:** `100`                                             |
| `cut`       | How many bandwidths to extend the grid past the extremes. **TYPE:** `float` **DEFAULT:** `3`                                                                                 |
| `xlim`      | The (min, max) x range of the grid; overrides the padded range. **TYPE:** `Optional[Tuple[float, float]]` **DEFAULT:** `None`                                                |
| `ylim`      | The (min, max) y range of the grid; overrides the padded range. **TYPE:** `Optional[Tuple[float, float]]` **DEFAULT:** `None`                                                |

| RETURNS           | DESCRIPTION                                      |
| ----------------- | ------------------------------------------------ |
| `Dict[str, List]` | The {x, y, z} chart dict of the density surface. |

| RAISES       | DESCRIPTION                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If the bandwidth is invalid, x and y differ in length, there are fewer than two points, or a value is not finite. |
