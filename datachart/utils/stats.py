"""The module containing the `stats` methods.

The `stats` module provides methods for calculating statistics.

Methods:
    count(values):
        Counts the number of elements in the list.
    mean(values):
        Calculatest the mean of the values.
    median(values):
        Calculates the median of the values.
    stdev(values):
        Calculates the standard deviation of the values.
    quantile(values, q):
        Calculates the quantile of the values.
    minimum(values):
        Gets the minimum of the values.
    maximum(values):
        Gets the maximum of the values.
"""


from typing import List, Tuple, Union

import numpy as np

# ================================================
# Statistical values
# ================================================


def count(values: List[Union[int, float]]) -> int:
    """Counts the number of elements in a list

    Args:
        values: The list of values.

    Returns:
        The number of elements in the list.
    """
    assert isinstance(values, (list, np.ndarray)), "The values variable is not a list."
    return len(values)


def mean(values: List[Union[int, float]]) -> float:
    """Calculates the mean of the values

    Args:
        values: The list of values.

    Returns:
        The mean of the values.
    """
    assert isinstance(values, (list, np.ndarray)), "The values variable is not a list."
    return sum(values) / len(values)


def median(values: List[Union[int, float]]) -> float:
    """Calculates the median of the values

    Args:
        values: The list of values.

    Returns:
        The median of the values.
    """

    assert isinstance(values, (list, np.ndarray)), "The values variable is not a list."
    values.sort()
    if len(values) % 2 == 0:
        return (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2
    else:
        return values[len(values) // 2]


def stdev(values: List[Union[int, float]]) -> float:
    """Calculates the standard deviation of the values

    Args:
        values: The list of values.

    Returns:
        The standard deviation of the values.
    """

    assert isinstance(values, (list, np.ndarray)), "The values variable is not a list."
    return (sum([(x - mean(values)) ** 2 for x in values]) / len(values)) ** 0.5


def quantile(values: List[Union[int, float]], q: float) -> float:
    """Calculates the quantile of the values

    Args:
        values: The list of values.
        q: The quantile to calculate.

    Returns:
        The quantile of the values.
    """
    assert isinstance(values, (list, np.ndarray)), "The values variable is not a list."

    values.sort()
    return values[len(values) * q // 100]


def minimum(values: List[Union[int, float]]) -> Tuple[float, float]:
    """Gets the minimum of the values

    Args:
        values: The list of values.

    Returns:
        The minimum of the values.

    """
    assert isinstance(values, (list, np.ndarray)), "The values variable is not a list."
    return min(values)

def maximum(values: List[Union[int, float]]) -> Union[int, float]:
    """Gets the maximum of the values

    Args:
        values: The list of values.

    Returns:
        The maximum of the values.

    """
    assert isinstance(values, (list, np.ndarray)), "The values variable is not a list."
    return max(values)