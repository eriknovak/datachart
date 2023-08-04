from typing import Union


# ================================================
# Number Statistics
# ================================================


def get_min_max_values(data: list[Union[int, float]]):
    """Gets the min and max values of a list of data points"

    Args:
        data (list[Union[int, float]]): The data points.

    Returns: The min and max values.
    """
    min_val = min(data)
    max_val = max(data)
    return min_val, max_val
