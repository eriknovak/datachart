"""The module containing the `colors` utility.

The `colors` module contains the utility functions for getting color
scales and colormaps using pypalettes (https://y-sunflower.github.io/pypalettes/).

Methods:
    get_color_scale(name):
        Get a color scale by name using pypalettes.
    create_colormap(color_list, name):
        Create a color map from a list of colors.
    get_colormap(name):
        Get a color map by name using pypalettes.
    get_discrete_colors(name, max_colors):
        Get a list of discrete colors.
    create_color_cycle(name, max_colors):
        Create a color cycle.

"""

import warnings
from cycler import cycler
from itertools import cycle
from collections import defaultdict
from typing import List, Union

import numpy as np
import matplotlib.colors as colors

from pypalettes import load_palette, load_cmap

from ...constants import COLORS


# ===============================================
# Constants
# ===============================================

DEFAULT_COLOR = COLORS.Spectral
DEFAULT_MAX_COLOR = 5

# ===============================================
# Main Function
# ===============================================


def get_color_scale(name: str = DEFAULT_COLOR) -> List[str]:
    """Get a color scale by name using pypalettes.

    Args:
        name: The name of the color scale (any valid pypalettes palette name).

    Returns:
        The color scale corresponding to the given name.

    """

    assert isinstance(name, str), "The name is not a string."

    try:
        palette = load_palette(name)
        return list(palette)
    except Exception:
        warnings.warn(
            f"Warning: '{name}' is not a valid pypalettes palette. "
            f"Reverting to default name='{DEFAULT_COLOR}'. "
            f"See https://y-sunflower.github.io/pypalettes/ for available palettes."
        )
        try:
            palette = load_palette(DEFAULT_COLOR)
            return list(palette)
        except Exception:
            # Ultimate fallback to a simple color list
            return ["#d7191c", "#fdae61", "#ffffbf", "#abdda4", "#2b83ba"]


def create_colormap(
    color_list: List[str], name: str = ""
) -> colors.LinearSegmentedColormap:
    """Create a color map from a list of colors.

    Args:
        color_list: The list of colors.
        name: The name of the color map.

    Returns:
        The color map.

    """

    assert isinstance(color_list, list), "The color_list is not a list."
    assert all(
        isinstance(c, str) for c in color_list
    ), "The color_list items are not strings."

    return colors.LinearSegmentedColormap.from_list(name, color_list)


def get_colormap(
    name: str = DEFAULT_COLOR, cmap_type: str = "continuous"
) -> colors.LinearSegmentedColormap:
    """Get a color map by name using pypalettes.

    Args:
        name: The name of the color map (any valid pypalettes palette name).
        cmap_type: The type of colormap ("continuous" or "discrete").

    Returns:
        The color map.

    """

    try:
        return load_cmap(name, cmap_type=cmap_type)
    except Exception:
        # Fallback to creating colormap from color scale
        return create_colormap(get_color_scale(name), name)


def get_discrete_colors(
    name: Union[str, List[str]] = DEFAULT_COLOR, max_colors: int = DEFAULT_MAX_COLOR
) -> list:
    """Get a list of discrete colors.

    Args:
        name: The name of the color scale (any valid pypalettes palette name) or a list of hex color strings.
        max_colors: The maximum number of colors.

    Returns:
        The list of discrete colors.

    """

    assert isinstance(name, (str, list)), "The name must be a string or a list."
    assert isinstance(max_colors, int), "The max_colors is not an integer."
    assert max_colors > 0, "The max_colors must be greater than 0."

    # If name is a list of colors, use them directly
    if isinstance(name, list):
        assert all(isinstance(c, str) for c in name), "All color list items must be strings."
        # Cycle through the provided colors if more colors are needed
        if max_colors <= len(name):
            return name[:max_colors]
        else:
            # Repeat the color list to get enough colors
            return (name * ((max_colors // len(name)) + 1))[:max_colors]

    # Otherwise use pypalettes
    color_scale = get_color_scale(name)
    if max_colors == 1:
        # the color scale is long enough
        return [color_scale[-1]]
    # otherwise create a continuous colormap and retrieve the discrete colors
    cmap = get_colormap(name)
    return [colors.to_hex(c) for c in cmap(np.linspace(0, 1, max_colors))]


def create_color_cycle(
    name: Union[str, List[str]] = DEFAULT_COLOR, max_colors: int = DEFAULT_MAX_COLOR
) -> cycle:
    """Create a color cycle.

    Args:
        name: The name of the color scale (any valid pypalettes palette name) or a list of hex color strings.
        max_colors: The maximum number of colors.

    Returns:
        The color cycle.

    """

    color_cycler = cycler(color=get_discrete_colors(name, max_colors))
    color_cycler = color_cycler()
    return defaultdict(lambda: next(color_cycler))
