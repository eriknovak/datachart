"""The module containing the `stats` methods.

The `stats` module provides methods for calculating statistics.

Methods:
    count(values):
        Counts the number of elements in the list.
    sum_values(values):
        Calculates the sum of the values.
    mean(values):
        Calculates the mean of the values.
    median(values):
        Calculates the median of the values.
    stdev(values):
        Calculates the standard deviation of the values.
    variance(values):
        Calculates the variance of the values.
    quantile(values, q):
        Calculates the quantile of the values.
    iqr(values):
        Calculates the interquartile range (Q3 - Q1).
    minimum(values):
        Gets the minimum of the values.
    maximum(values):
        Gets the maximum of the values.
    correlation(x, y):
        Calculates the Pearson correlation coefficient between two lists.
    contour_levels(z, rule):
        Picks the contour levels of a 2-D grid by a rule of thumb.
"""

import math
from typing import List, Optional, Tuple, Union

import numpy as np
from matplotlib.ticker import MaxNLocator

from ..constants import CONTOUR_LEVELS

# rule-of-thumb level counts stay readable in this range (ADR 0022)
CONTOUR_LEVELS_MIN = 4
CONTOUR_LEVELS_MAX = 20
# the fd rule on a flat surface (IQR 0) has no bin width; match auto's density
CONTOUR_LEVELS_FLAT = 8

# ================================================
# Statistical values
# ================================================


def count(values: List[Union[int, float]]) -> int:
    """Counts the number of elements in a list.

    Examples:
        >>> from datachart.utils.stats import count
        >>> count([1, 2, 3, 4, 5])
        5

    Args:
        values: The list of values.

    Returns:
        The number of elements in the list.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    return len(values)


def sum_values(values: List[Union[int, float]]) -> float:
    """Calculates the sum of all values.

    !!! info "Added in v0.7.0"

    Examples:
        >>> from datachart.utils.stats import sum_values
        >>> sum_values([1, 2, 3, 4, 5])
        15.0

    Args:
        values: The list of values.

    Returns:
        The sum of all values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    return float(np.sum(values))


def mean(values: List[Union[int, float]]) -> float:
    """Calculates the mean of the values.

    Examples:
        >>> from datachart.utils.stats import mean
        >>> mean([1, 2, 3, 4, 5])
        3.0

    Args:
        values: The list of values.

    Returns:
        The mean of the values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.mean(values))


def median(values: List[Union[int, float]]) -> float:
    """Calculates the median of the values.

    Examples:
        >>> from datachart.utils.stats import median
        >>> median([1, 2, 3, 4, 5])
        3.0

    Args:
        values: The list of values.

    Returns:
        The median of the values.
    """

    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.median(values))


def stdev(values: List[Union[int, float]]) -> float:
    """Calculates the standard deviation of the values.

    Examples:
        >>> from datachart.utils.stats import stdev
        >>> stdev([1, 2, 3, 4, 5])
        1.4142135623730951

    Args:
        values: The list of values.

    Returns:
        The standard deviation of the values.
    """

    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.std(values))


def variance(values: List[Union[int, float]]) -> float:
    """Calculates the variance of the values.

    !!! info "Added in v0.7.0"

    Examples:
        >>> from datachart.utils.stats import variance
        >>> variance([1, 2, 3, 4, 5])
        2.0

    Args:
        values: The list of values.

    Returns:
        The variance of the values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.var(values))


def quantile(values: List[Union[int, float]], q: float) -> float:
    """Calculates the quantile of the values.

    Examples:
        >>> from datachart.utils.stats import quantile
        >>> quantile([1, 2, 3, 4, 5], 25)
        2.0

    Args:
        values: The list of values.
        q: The quantile to calculate (0-100).

    Returns:
        The quantile of the values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.percentile(values, q))


def iqr(values: List[Union[int, float]]) -> float:
    """Calculates the interquartile range (Q3 - Q1).

    !!! info "Added in v0.7.0"

    The interquartile range is the difference between the 75th percentile
    (Q3) and the 25th percentile (Q1). It is a measure of statistical
    dispersion and is useful for identifying outliers.

    Examples:
        >>> from datachart.utils.stats import iqr
        >>> iqr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        4.5

    Args:
        values: The list of values.

    Returns:
        The interquartile range of the values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.percentile(values, 75) - np.percentile(values, 25))


def minimum(values: List[Union[int, float]]) -> float:
    """Gets the minimum of the values.

    Examples:
        >>> from datachart.utils.stats import minimum
        >>> minimum([1, 2, 3, 4, 5])
        1

    Args:
        values: The list of values.

    Returns:
        The minimum of the values.

    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.min(values))


def maximum(values: List[Union[int, float]]) -> float:
    """Gets the maximum of the values.

    Examples:
        >>> from datachart.utils.stats import maximum
        >>> maximum([1, 2, 3, 4, 5])
        5

    Args:
        values: The list of values.

    Returns:
        The maximum of the values.

    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.max(values))


def correlation(x: List[Union[int, float]], y: List[Union[int, float]]) -> float:
    """Calculates the Pearson correlation coefficient between two lists.

    !!! info "Added in v0.7.0"

    The Pearson correlation coefficient measures the linear relationship
    between two datasets. It ranges from -1 (perfect negative correlation)
    to 1 (perfect positive correlation), with 0 indicating no linear
    correlation.

    Examples:
        >>> from datachart.utils.stats import correlation
        >>> correlation([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
        1.0
        >>> correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
        -1.0

    Args:
        x: The first list of values.
        y: The second list of values.

    Returns:
        The Pearson correlation coefficient.

    Raises:
        TypeError: If x or y is not a list or numpy array.
        ValueError: If x and y have different lengths.
    """
    if not isinstance(x, (list, np.ndarray)):
        raise TypeError("The x variable must be a list or numpy array.")
    if not isinstance(y, (list, np.ndarray)):
        raise TypeError("The y variable must be a list or numpy array.")
    if len(x) == 0 or len(y) == 0:
        raise ValueError("x and y must have at least one value.")
    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")
    return float(np.corrcoef(x, y)[0, 1])


def contour_levels(
    z: List[List[Union[int, float]]], rule: Union[str, int, List[float], None]
) -> Union[List[float], int, None]:
    """Picks the contour levels of a 2-D grid by a rule of thumb.

    The rules of `CONTOUR_LEVELS` are evaluated on the per-axis resolution
    of the grid, `n = sqrt(cells)`: `"rice"` targets `2 * n ** (1/3)` levels
    and `"fd"` the value range over `2 * IQR * n ** (-1/3)`. The count is
    clamped to the 4–20 range and snapped to round values across the range of
    `z`. `"auto"` (or `None`) returns `None`, leaving the choice to
    matplotlib; an integer or a list of level values passes through.

    !!! info "Added in Unreleased"

    Examples:
        >>> import numpy as np
        >>> from datachart.utils.stats import contour_levels
        >>> x = np.linspace(-5, 5, 120)
        >>> X, Y = np.meshgrid(x, x)
        >>> contour_levels(X**2 + Y**2, "rice")
        [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0]

    Args:
        z: The 2-D grid of values.
        rule: A rule of `CONTOUR_LEVELS`, a target level count, or an explicit
            list of level values.

    Returns:
        The level values, the target count, or `None` for the automatic rule.

    Raises:
        ValueError: If the rule is not one of `CONTOUR_LEVELS`.
    """
    if rule is None or rule == CONTOUR_LEVELS.AUTO:
        return None
    if not isinstance(rule, str):
        return rule
    if rule not in (CONTOUR_LEVELS.RICE, CONTOUR_LEVELS.FD):
        raise ValueError(
            f"Invalid contour `levels` rule {rule!r}. Must be one of "
            f"{[CONTOUR_LEVELS.AUTO, CONTOUR_LEVELS.RICE, CONTOUR_LEVELS.FD]}, "
            "an integer, or a list of level values."
        )

    values = np.asarray(z, dtype=float).ravel()
    values = values[np.isfinite(values)]
    n = math.sqrt(values.size)
    if rule == CONTOUR_LEVELS.RICE:
        k = math.ceil(2 * n ** (1 / 3))
    else:
        h = 2 * iqr(values) * n ** (-1 / 3)
        k = math.ceil(np.ptp(values) / h) if h > 0 else CONTOUR_LEVELS_FLAT
    k = int(np.clip(k, CONTOUR_LEVELS_MIN, CONTOUR_LEVELS_MAX))
    ticks = MaxNLocator(nbins=k).tick_values(values.min(), values.max())
    return [float(t) for t in ticks]
