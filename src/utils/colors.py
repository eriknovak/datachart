import warnings

import numpy as np
import matplotlib.colors as colors

from cycler import cycler
from itertools import cycle
from collections import defaultdict

from schema.constants import Colors
from config.themes.colors import COLOR_SCALE_MAPPING

# ===============================================
# Constants
# ===============================================

DEFAULT_COLOR = Colors.Spectral
DEFAULT_MAX_COLOR = 5

# ===============================================
# Main Function
# ===============================================


def get_color_scale(name: str = DEFAULT_COLOR) -> list:
    """Get a color scale by name."""
    if name not in COLOR_SCALE_MAPPING:
        warnings.warn(
            f"Warning: {name} is not a valid color scale. Reverting to default name='{DEFAULT_COLOR}'."
        )
        return COLOR_SCALE_MAPPING[DEFAULT_COLOR]
    return COLOR_SCALE_MAPPING[name]


def create_colormap(color_list: list, name: str = "") -> colors.LinearSegmentedColormap:
    """Create a color map from a list of colors."""
    return colors.LinearSegmentedColormap.from_list(name, color_list)


def get_colormap(name: str = DEFAULT_COLOR) -> colors.LinearSegmentedColormap:
    """Get a color map by name."""
    return create_colormap(get_color_scale(name), name)


def get_discrete_colors(
    name: str = DEFAULT_COLOR, max_colors: int = DEFAULT_MAX_COLOR
) -> list:
    """Get a list of discrete colors."""
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
    """Create a color cycle."""
    color_cycler = cycler(color=get_discrete_colors(name, max_colors))
    color_cycler = color_cycler()
    return defaultdict(lambda: next(color_cycler))
