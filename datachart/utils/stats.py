from typing import List, Union

import numpy as np

# ================================================
# Number Statistics
# ================================================


def get_min_max_values(data: List[Union[int, float]]):
    """Gets the min and max values of a list of data points"

    Parameters
    ----------
    data: List[Union[int, float]]
        The data points.

    Returns
    -------
    min_val: Union[int, float]
        The min value.
    max_val: Union[int, float]
        The max value.

    """
    assert isinstance(data, (list, np.ndarray)), "The data variable is not a list."
    min_val = min(data)
    max_val = max(data)
    return min_val, max_val
