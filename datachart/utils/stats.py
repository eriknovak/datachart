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
"""

from typing import List, Tuple, Union

import numpy as np

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
    return float(np.std(values))


def variance(values: List[Union[int, float]]) -> float:
    """Calculates the variance of the values.

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

    return float(np.percentile(values, q))


def iqr(values: List[Union[int, float]]) -> float:
    """Calculates the interquartile range (Q3 - Q1).

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
    return float(np.max(values))


def correlation(x: List[Union[int, float]], y: List[Union[int, float]]) -> float:
    """Calculates the Pearson correlation coefficient between two lists.

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
    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")
    return float(np.corrcoef(x, y)[0, 1])
