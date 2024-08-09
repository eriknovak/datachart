"""The module containing the `colors` utlity.

The `colors` module contains the utility functions for getting color
scales and colormaps.

Methods:
    get_color_scale(name):
        Get a color scale by name.
    create_colormap(color_list, name):
        Create a color map from a list of colors.
    get_colormap(name):
        Get a color map by name.
    get_discrete_colors(name, max_colors):
        Get a list of discrete colors.
    create_color_cycle(name, max_colors):
        Create a color cycle.

"""

import warnings
from cycler import cycler
from itertools import cycle
from collections import defaultdict
from typing import List

import numpy as np
import matplotlib.colors as colors

from ..constants import COLORS


# ===============================================
# Constants
# ===============================================

DEFAULT_COLOR = COLORS.Spectral
DEFAULT_MAX_COLOR = 5

# ===============================================
# Main Function
# ===============================================


def get_color_scale(name: str = DEFAULT_COLOR) -> List[str]:
    """Get a color scale by name.

    Args:
        name: The name of the color scale.

    Returns:
        The color scale corresponding to the given name.

    """

    assert isinstance(name, str), "The name is not a string."

    if name not in COLOR_SCALE_MAPPING:
        warnings.warn(
            f"Warning: {name} is not a valid color scale. Reverting to default name='{DEFAULT_COLOR}'."
        )
        return COLOR_SCALE_MAPPING[DEFAULT_COLOR]

    return COLOR_SCALE_MAPPING[name]


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


def get_colormap(name: str = DEFAULT_COLOR) -> colors.LinearSegmentedColormap:
    """Get a color map by name.

    Args:
        name: The name of the color map.

    Returns:
        The color map.

    """

    return create_colormap(get_color_scale(name), name)


def get_discrete_colors(
    name: str = DEFAULT_COLOR, max_colors: int = DEFAULT_MAX_COLOR
) -> list:
    """Get a list of discrete colors.

    Args:
        name: The name of the color scale.
        max_colors: The maximum number of colors.

    Returns:
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

    Args:
        name: The name of the color scale.
        max_colors: The maximum number of colors.

    Returns:
        The color cycle.

    """

    color_cycler = cycler(color=get_discrete_colors(name, max_colors))
    color_cycler = color_cycler()
    return defaultdict(lambda: next(color_cycler))


# ===============================================
# Color definitions and cycles
# Taken from: https://colorbrewer2.org/
# ===============================================

# ===============================================
# Scale definitions
# ===============================================

# -------------------------------------
# Sequential
# -------------------------------------

# ---------------------------
# Single-hue
# ---------------------------

# Blue
color_scale_blue = ["#eff3ff", "#bdd7e7", "#6baed6", "#3182bd", "#08519c"]
color_scale_green = ["#edf8e9", "#bae4b3", "#74c476", "#31a354", "#006d2c"]
color_scale_orange = ["#feedde", "#fdbe85", "#fd8d3c", "#e6550d", "#a63603"]
color_scale_purple = ["#f2f0f7", "#cbc9e2", "#9e9ac8", "#756bb1", "#54278f"]
color_scale_grey = ["#f7f7f7", "#cccccc", "#969696", "#636363", "#252525"]


# ---------------------------
# Multi-hue
# ---------------------------

color_scale_ylgnbu = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]
color_scale_ylgn = ["#ffffcc", "#c2e699", "#78c679", "#31a354", "#006837"]
color_scale_bugn = ["#edf8fb", "#b2e2e2", "#66c2a4", "#2ca25f", "#006d2c"]
color_scale_gnbu = ["#f0f9e8", "#bae4bc", "#7bccc4", "#43a2ca", "#0868ac"]
color_scale_pubu = ["#f1eef6", "#bdc9e1", "#74a9cf", "#2b8cbe", "#045a8d"]

# -------------------------------------
# Diverging
# -------------------------------------

color_scale_rdbn = ["#ca0020", "#f4a582", "#f7f7f7", "#92c5de", "#0571b0"]
color_scale_rdylbu = ["#d7191c", "#fdae61", "#ffffbf", "#abd9e9", "#2c7bb6"]
color_scale_brgn = ["#a6611a", "#dfc27d", "#f5f5f5", "#80cdc1", "#018571"]
color_scale_pugn = ["#7b3294", "#c2a5cf", "#f7f7f7", "#a6dba0", "#008837"]
color_scale_orpu = ["#e66101", "#fdb863", "#f7f7f7", "#b2abd2", "#5e3c99"]
color_scale_rdgy = ["#ca0020", "#f4a582", "#ffffff", "#bababa", "#404040"]
color_scale_rdylgn = ["#d7191c", "#fdae61", "#ffffbf", "#a6d96a", "#1a9641"]
color_scale_spectral = ["#d7191c", "#fdae61", "#ffffbf", "#abdda4", "#2b83ba"]


# -------------------------------------
# Quantitative
# -------------------------------------

# mixed light
color_scale_mixed_light = [
    "#a6cee3",
    "#1f78b4",
    "#b2df8a",
    "#33a02c",
    "#fb9a99",
    "#e31a1c",
    "#fdbf6f",
    "#ff7f00",
    "#cab2d6",
    "#6a3d9a",
]

# mixed dark
color_scale_mixed_dark = [
    "#e41a1c",
    "#377eb8",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#ffff33",
    "#a65628",
    "#f781bf",
    "#999999",
]


# ===============================================
# Color Scale Mapping
# ===============================================

COLOR_SCALE_MAPPING = {
    "blue": color_scale_blue,
    "green": color_scale_green,
    "orange": color_scale_orange,
    "purple": color_scale_purple,
    "grey": color_scale_grey,
    "ylgnbu": color_scale_ylgnbu,
    "ylgn": color_scale_ylgn,
    "bugn": color_scale_bugn,
    "gnbu": color_scale_gnbu,
    "pubu": color_scale_pubu,
    "rdbn": color_scale_rdbn,
    "rdylbu": color_scale_rdylbu,
    "brgn": color_scale_brgn,
    "pugn": color_scale_pugn,
    "orpu": color_scale_orpu,
    "rdgy": color_scale_rdgy,
    "rdylgn": color_scale_rdylgn,
    "spectral": color_scale_spectral,
    "mixed_light": color_scale_mixed_light,
    "mixed_dark": color_scale_mixed_dark,
}

# ===============================================
# Color Definitions
# ===============================================

COLOR_MAPPING = {}
