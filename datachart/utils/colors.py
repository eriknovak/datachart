import warnings
from cycler import cycler
from itertools import cycle
from collections import defaultdict

import numpy as np
import matplotlib.colors as colors

from ..constants import COLORS
from ..themes.colors import COLOR_SCALE_MAPPING


# ===============================================
# Constants
# ===============================================

DEFAULT_COLOR = COLORS.Spectral
DEFAULT_MAX_COLOR = 5

# ===============================================
# Main Function
# ===============================================


def get_color_scale(name: str = DEFAULT_COLOR) -> list:
    """Get a color scale by name.

    Parameters
    ----------
    name : str, optional (default=COLORS.Spectral)
        The name of the color scale.

    Returns
    -------
    list
        The color scale corresponding to the given name.
    """

    assert isinstance(name, str), "The name is not a string."

    if name not in COLOR_SCALE_MAPPING:
        warnings.warn(
            f"Warning: {name} is not a valid color scale. Reverting to default name='{DEFAULT_COLOR}'."
        )
        return COLOR_SCALE_MAPPING[DEFAULT_COLOR]

    return COLOR_SCALE_MAPPING[name]


def create_colormap(color_list: list, name: str = "") -> colors.LinearSegmentedColormap:
    """Create a color map from a list of colors.

    Parameters
    ----------
    color_list : list
        The list of colors.

    name : str, optional (default="")
        The name of the color map.

    Returns
    -------
    colors.LinearSegmentedColormap
        The color map.
    """

    assert isinstance(color_list, list), "The color_list is not a list."
    assert all(
        isinstance(c, str) for c in color_list
    ), "The color_list items are not strings."

    return colors.LinearSegmentedColormap.from_list(name, color_list)


def get_colormap(name: str = DEFAULT_COLOR) -> colors.LinearSegmentedColormap:
    """Get a color map by name.

    Parameters
    ----------
    name : str, optional (default=COLORS.Spectral)
        The name of the color map.

    Returns
    -------
    colors.LinearSegmentedColormap
        The color map.
    """

    return create_colormap(get_color_scale(name), name)


def get_discrete_colors(
    name: str = DEFAULT_COLOR, max_colors: int = DEFAULT_MAX_COLOR
) -> list:
    """Get a list of discrete colors.

    Parameters
    ----------
    name : str, optional (default=COLORS.Spectral)
        The name of the color scale.
    max_colors : int, optional (default=5)
        The maximum number of colors.

    Returns
    -------
    list
        The list of discrete colors.
    """

    assert isinstance(name, str), "The name is not a string."
    assert isinstance(max_colors, int), "The max_colors is not an integer."
    assert max_colors > 0, "The max_colors must be greater than 0."

    color_scale = get_color_scale(name)
    if max_colors == 1:
        # the color scale is long enough
        return [color_scale[-1]]
    # otherwise create a continuous colormap and retrieve the discrete colors
    cmap = get_colormap(name)
    return [colors.to_hex(c) for c in cmap(np.linspace(0, 1, max_colors))]


def create_color_cycle(
    name: list = DEFAULT_COLOR, max_colors: int = DEFAULT_MAX_COLOR
) -> cycle:
    """Create a color cycle.

    Parameters
    ----------
    name : list, optional (default=COLORS.Spectral)
        The name of the color scale.
    max_colors : int, optional (default=5)
        The maximum number of colors.

    Returns
    -------
    cycle
        The color cycle.
    """

    color_cycler = cycler(color=get_discrete_colors(name, max_colors))
    color_cycler = color_cycler()
    return defaultdict(lambda: next(color_cycler))
