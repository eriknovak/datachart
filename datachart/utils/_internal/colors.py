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
    cycling_colors(name):
        The colors a palette cycles through, or None when it interpolates.
    warn_palette_overflow(name, count, what):
        Warn when more units than colors draw from a cycling palette.
    is_plain_color(name):
        Tell a plain color apart from a palette name.
    oklab_lightness(color):
        The perceptual lightness of a color.

"""

import warnings
from cycler import cycler
from collections import defaultdict
from typing import List, Union, Dict, Literal

import numpy as np
import matplotlib.colors as colors

from pypalettes import load_palette, load_cmap

from ...constants import COLORS

# ===============================================
# Constants
# ===============================================

DEFAULT_COLOR = COLORS.Spectral
DEFAULT_MAX_COLOR = 5

# datachart-defined palettes, consulted before pypalettes
CUSTOM_PALETTES: Dict[str, List[str]] = {
    # five YlGnBu samples 0.15 apart in lightness, darkest and lightest first
    COLORS.PaperYlGnBu: [
        "#1E2E85",
        "#EAF7B1",
        "#2165AB",
        "#85CFBA",
        "#299DC1",
    ],
    COLORS.PaperAccent: ["#5B84C4", "#C85450"],
    # the tuned categorical leads of the derived themes (ADR 0074)
    COLORS.Harbor: ["#1F4E79", "#D08C3A", "#6FA3D3", "#EFC98C", "#8C6D5A", "#1A1A1A"],
    COLORS.TolMuted: ["#332288", "#88CCEE", "#DDCC77", "#CC6677", "#882255"],
    COLORS.Contrast: ["#1F4E79", "#D4B24C", "#B45C6A", "#2B2B2B", "#9A9A9A"],
    COLORS.Rust: ["#B5563A", "#5A6F86", "#EBBC63", "#2C4A34", "#9F9A8D", "#966AD5"],
    COLORS.Slate: ["#4F6D8F", "#D4D389", "#743538", "#67A652", "#C06AC9", "#8EB2D2"],
}

# ===============================================
# Helper Functions
# ===============================================


def is_plain_color(name: str) -> bool:
    """Whether a name is a plain color rather than a palette.

    Callers resolve `CUSTOM_PALETTES` before asking.

    Args:
        name: The name to inspect.

    Returns:
        `True` for a color that names no palette, `False` otherwise.

    """

    if not colors.is_color_like(name):
        return False
    # palettes win the ambiguous names ("Red", "Gold", "pink", "grey", ...)
    try:
        load_palette(name)
    except Exception:
        return True
    return False


# Machado, Oliveira and Fernandes (2009) at full severity, linear RGB (ADR 0073)
_CVD_TRANSFORMS: Dict[str, np.ndarray] = {
    "deutan": np.array(
        [
            [0.367322, 0.860646, -0.227968],
            [0.280085, 0.672501, 0.047413],
            [-0.011820, 0.042940, 0.968881],
        ]
    ),
    "protan": np.array(
        [
            [0.152286, 1.052583, -0.204868],
            [0.114503, 0.786281, 0.099216],
            [-0.003882, -0.048116, 1.051998],
        ]
    ),
    "tritan": np.array(
        [
            [1.255528, -0.076749, -0.178779],
            [-0.078411, 0.930809, 0.147602],
            [0.004733, 0.691367, 0.303900],
        ]
    ),
}
_RGB_TO_LMS = np.array(
    [
        [0.4122214708, 0.5363325363, 0.0514459929],
        [0.2119034982, 0.6806995451, 0.1073969566],
        [0.0883024619, 0.2817188376, 0.6299787005],
    ]
)
_LMS_TO_OKLAB = np.array(
    [
        [0.2104542553, 0.7936177850, -0.0040720468],
        [1.9779984951, -2.4285922050, 0.4505937099],
        [0.0259040371, 0.7827717662, -0.8086757660],
    ]
)


def linear_rgb(color) -> np.ndarray:
    """A color as linear (gamma-expanded) RGB, each channel 0 to 1."""

    return np.array(
        [
            c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
            for c in colors.to_rgb(color)
        ]
    )


def oklab(color, deficiency: Union[str, None] = None) -> np.ndarray:
    """A color in OKLab, as seen with a color-vision deficiency when named.

    Args:
        color: Any matplotlib color.
        deficiency: `"deutan"`, `"protan"`, `"tritan"`, or `None` for normal
            vision.

    Returns:
        The `(L, a, b)` triple, lightness 0 (black) to 1 (white).

    """

    linear = linear_rgb(color)
    if deficiency is not None:
        linear = np.clip(_CVD_TRANSFORMS[deficiency] @ linear, 0.0, 1.0)
    return _LMS_TO_OKLAB @ np.cbrt(_RGB_TO_LMS @ linear)


def oklab_lightness(color) -> float:
    """The OKLab lightness of a color, 0 (black) to 1 (white).

    Args:
        color: Any matplotlib color.

    Returns:
        The lightness.

    """

    return float(oklab(color)[0])


def delta_e(a, b, deficiency: Union[str, None] = None) -> float:
    """The distance between two colors in OKLab ×100, under a deficiency when named."""

    return float(100 * np.linalg.norm(oklab(a, deficiency) - oklab(b, deficiency)))


def wcag_contrast(a, b) -> float:
    """The WCAG 2 contrast ratio of two colors, 1 (equal) to 21 (black on white)."""

    weights = np.array([0.2126, 0.7152, 0.0722])
    la, lb = (float(weights @ linear_rgb(c)) for c in (a, b))
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# ===============================================
# Main Function
# ===============================================


def get_color_scale(name: str = DEFAULT_COLOR) -> List[str]:
    """Get a color scale by name using pypalettes.

    Args:
        name: The name of the color scale (any valid pypalettes palette name),
            or a single color, which is a color scale of one.

    Returns:
        The color scale corresponding to the given name.

    """

    if not isinstance(name, str):
        raise TypeError("The name must be a string.")

    if name in CUSTOM_PALETTES:
        return list(CUSTOM_PALETTES[name])

    if is_plain_color(name):
        return [name]

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

    if not isinstance(color_list, list):
        raise TypeError("The color_list is not a list.")
    if not all(isinstance(c, str) for c in color_list):
        raise TypeError("The color_list items are not strings.")

    # a ramp needs both ends; one color ramps from itself to itself
    if len(color_list) == 1:
        color_list = color_list * 2

    return colors.LinearSegmentedColormap.from_list(name, color_list)


def get_colormap(
    name: str = DEFAULT_COLOR, cmap_type: str = "continuous"
) -> colors.LinearSegmentedColormap:
    """Get a color map by name using pypalettes.

    Args:
        name: The name of the color map (any valid pypalettes palette name),
            or a single color, which is a color map of one.
        cmap_type: The type of colormap ("continuous" or "discrete").

    Returns:
        The color map.

    """

    if isinstance(name, list):
        return create_colormap(name)

    if isinstance(name, str) and name in CUSTOM_PALETTES:
        return create_colormap(CUSTOM_PALETTES[name], name)

    if isinstance(name, str) and is_plain_color(name):
        return create_colormap([name], name)

    try:
        return load_cmap(name, cmap_type=cmap_type)
    except Exception:
        # Fallback to creating colormap from color scale
        return create_colormap(get_color_scale(name), name)


def cycling_colors(name: Union[str, List[str]]) -> Union[List[str], None]:
    """The colors a palette cycles through, or None when it interpolates.

    A color list, a custom palette and a plain color repeat their colors past
    the end; a pypalettes name samples its colormap instead.
    """

    if isinstance(name, str):
        if name in CUSTOM_PALETTES:
            return list(CUSTOM_PALETTES[name])
        if is_plain_color(name):
            return [name]
        return None
    if not all(isinstance(c, str) for c in name):
        raise TypeError("All color list items must be strings.")
    return list(name)


def warn_palette_overflow(
    name: Union[str, List[str]], count: int, what: str = "series"
) -> None:
    """Warn when `count` units outrun a cycling palette, so colors repeat.

    A one-color palette is monochrome by design, its patterns carry identity,
    so it never warns.

    Args:
        name: The palette the units draw from.
        count: How many units take a color.
        what: What the units are, for the message.

    """

    cycling = cycling_colors(name)
    if cycling is None or len(cycling) < 2 or count <= len(cycling):
        return
    palette = f"the `{name}` palette" if isinstance(name, str) else "the palette"
    warnings.warn(
        f"{count} {what}, but {palette} has {len(cycling)} colors, so colors "
        "repeat. Mute the rest with `emphasis`, split them into subplots, or "
        "set a longer palette.",
        stacklevel=3,
    )


def get_discrete_colors(
    name: Union[str, List[str]] = DEFAULT_COLOR, max_colors: int = DEFAULT_MAX_COLOR
) -> list:
    """Get a list of discrete colors.

    Args:
        name: The name of the color scale (any valid pypalettes palette name), a single
            color, or a list of hex color strings.
        max_colors: The maximum number of colors.

    Returns:
        The list of discrete colors.

    """

    if not isinstance(name, (str, list)):
        raise TypeError("The name must be a string or a list.")
    if not isinstance(max_colors, int):
        raise TypeError("The max_colors is not an integer.")
    if max_colors <= 0:
        raise ValueError("The max_colors must be greater than 0.")

    cycling = cycling_colors(name)
    if cycling is not None:
        if max_colors <= len(cycling):
            return cycling[:max_colors]
        return (cycling * ((max_colors // len(cycling)) + 1))[:max_colors]

    # Otherwise use pypalettes
    color_scale = get_color_scale(name)
    if max_colors == 1:
        # the color scale is long enough
        return [color_scale[-1]]
    # otherwise create a continuous colormap and retrieve the discrete colors
    cmap = get_colormap(name)
    return [colors.to_hex(c) for c in cmap(np.linspace(0, 1, max_colors))]


def create_color_cycle(
    name: Union[str, List[str]] = DEFAULT_COLOR,
    max_colors: int = DEFAULT_MAX_COLOR,
    what: Union[str, None] = None,
) -> Dict[int, Dict[Literal["color"], str]]:
    """Create a color cycle.

    Args:
        name: The name of the color scale (any valid pypalettes palette name), a single
            color, or a list of hex color strings.
        max_colors: The maximum number of colors.
        what: What the colors are for (series, hue levels, groups); when given,
            more of them than the palette has colors warns.

    Returns:
        The color cycle.

    """

    if what is not None:
        warn_palette_overflow(name, max_colors, what)
    color_cycler = cycler(color=get_discrete_colors(name, max_colors))
    color_cycler = color_cycler()
    return defaultdict(lambda: next(color_cycler))
