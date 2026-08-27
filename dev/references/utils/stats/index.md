# Stats Module

## datachart.utils.stats

The module containing the `stats` methods.

The `stats` module provides methods for calculating statistics.

| FUNCTION         | DESCRIPTION                                                       |
| ---------------- | ----------------------------------------------------------------- |
| `count`          | Counts the number of elements in the list.                        |
| `sum_values`     | Calculates the sum of the values.                                 |
| `mean`           | Calculates the mean of the values.                                |
| `median`         | Calculates the median of the values.                              |
| `stdev`          | Calculates the standard deviation of the values.                  |
| `variance`       | Calculates the variance of the values.                            |
| `quantile`       | Calculates the quantile of the values.                            |
| `iqr`            | Calculates the interquartile range (Q3 - Q1).                     |
| `minimum`        | Gets the minimum of the values.                                   |
| `maximum`        | Gets the maximum of the values.                                   |
| `correlation`    | Calculates the Pearson correlation coefficient between two lists. |
| `contour_levels` | Picks the contour levels of a 2-D grid by a rule of thumb.        |

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

### datachart.utils.stats.contour_levels

```
contour_levels(
    z: List[List[Union[int, float]]],
    rule: Union[str, int, List[float], None],
) -> Union[List[float], int, None]
```

Picks the contour levels of a 2-D grid by a rule of thumb.

The rules of `CONTOUR_LEVELS` are evaluated on the per-axis resolution of the grid, `n = sqrt(cells)`: `"rice"` targets `2 * n ** (1/3)` levels and `"fd"` the value range over `2 * IQR * n ** (-1/3)`. The count is clamped to the 4–20 range and snapped to round values across the range of `z`. `"auto"` (or `None`) returns `None`, leaving the choice to matplotlib; an integer or a list of level values passes through.

Added in Unreleased

Examples:

```
>>> import numpy as np
>>> from datachart.utils.stats import contour_levels
>>> x = np.linspace(-5, 5, 120)
>>> X, Y = np.meshgrid(x, x)
>>> contour_levels(X**2 + Y**2, "rice")
[0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0]
```

| PARAMETER | DESCRIPTION                                                                                                                         |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `z`       | The 2-D grid of values. **TYPE:** `List[List[Union[int, float]]]`                                                                   |
| `rule`    | A rule of CONTOUR_LEVELS, a target level count, or an explicit list of level values. **TYPE:** `Union[str, int, List[float], None]` |

| RETURNS                         | DESCRIPTION                                                         |
| ------------------------------- | ------------------------------------------------------------------- |
| `Union[List[float], int, None]` | The level values, the target count, or None for the automatic rule. |

| RAISES       | DESCRIPTION                               |
| ------------ | ----------------------------------------- |
| `ValueError` | If the rule is not one of CONTOUR_LEVELS. |
