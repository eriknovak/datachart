"""Derive a theme variant from a base theme and a lead colormap."""

import copy
from typing import List, Union

import numpy as np
import matplotlib.colors as mcolors

from ._base import canonical_style
from ..typings import StyleAttrs
from ..utils._internal.colors import get_color_scale, get_colormap

Lead = Union[str, List[str]]

# the series palette samples the lead at these positions, measured from its
# dark end; the trimmed quarter is the end that would vanish into the page
LIGHT_PAGE_STOPS = np.linspace(0.0, 0.75, 6)
DARK_PAGE_STOPS = np.linspace(0.25, 1.0, 6)
# darkest, lightest, then inward: neighbours in the cycle stay far apart
INTERLEAVED = (0, 5, 1, 4, 2, 3)


def lightness(color: str) -> float:
    """The OKLab lightness of a color, 0 (black) to 1 (white)."""

    rgb = [
        c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        for c in mcolors.to_rgb(color)
    ]
    l = 0.4122214708 * rgb[0] + 0.5363325363 * rgb[1] + 0.0514459929 * rgb[2]
    m = 0.2119034982 * rgb[0] + 0.6806995451 * rgb[1] + 0.1073969566 * rgb[2]
    s = 0.0883024619 * rgb[0] + 0.2817188376 * rgb[1] + 0.6299787005 * rgb[2]
    return (
        0.2104542553 * l ** (1 / 3)
        + 0.7936177850 * m ** (1 / 3)
        - 0.0040720468 * s ** (1 / 3)
    )


def is_sequential(lead: Lead) -> bool:
    """Whether a lead's lightness runs one way along it.

    A categorical palette bounces; a diverging map turns in the middle, so it
    reads as categorical too and is never a lead.
    """

    cmap = get_colormap(lead)
    steps = np.diff([lightness(c) for c in cmap(np.linspace(0, 1, 12))])
    return bool(np.all(steps >= -0.01) or np.all(steps <= 0.01))


def _resolve_base(base: Union[str, StyleAttrs]) -> StyleAttrs:
    # imported here: the configuration module imports the themes package
    from ..config.configuration import THEMES
    from .default import DEFAULT_THEME

    if isinstance(base, dict):
        return {**copy.deepcopy(DEFAULT_THEME), **copy.deepcopy(base)}
    if base not in THEMES:
        raise ValueError(f"Unknown theme: {base!r}. Must be one of {list(THEMES)}")
    return copy.deepcopy(THEMES[base])


def derive_theme(base: Union[str, StyleAttrs], lead: Lead, **overrides) -> StyleAttrs:
    """Build a theme variant: the base's furniture with palettes rebuilt from the lead.

    A sequential lead becomes the value scale (`color_general_singular`,
    `plot_heatmap_cmap`); the series palette is six of its colors in lightness
    steps, interleaved dark and light, the parallel coords ramp four of them
    from light to dark, and the dumbbell pair its lightest and darkest sample.
    A categorical lead becomes the series palette, its first color the singular
    one, and the base keeps its value scale, ramp, and dumbbell pair. Fonts,
    spines, hatches, and rendering attributes are never touched. The result is
    a plain theme dictionary: apply it with `register_theme` or `override`.

    Examples:
        >>> from datachart.config import config
        >>> from datachart.constants import COLORS, THEME
        >>> from datachart.themes import derive_theme
        >>> forest = derive_theme(THEME.MINIMAL, lead=COLORS.Greens)
        >>> config.register_theme("forest", forest)
        >>> config.set_theme("forest")

    Args:
        base: A `THEME` constant, a registered theme name, or a theme dictionary.
        lead: A `COLORS` constant, a pypalettes palette name, or a list of colors.
            A diverging map is not a lead; it is read as categorical.
        **overrides: Style attributes set on the result; an unknown name raises.

    Returns:
        The derived theme.

    """

    theme = _resolve_base(base)
    if len(get_color_scale(lead) if isinstance(lead, str) else lead) < 2:
        raise ValueError("The lead must hold at least two colors.")

    if is_sequential(lead):
        cmap = get_colormap(lead)
        # positions run from the lead's dark end whichever way it is written
        dark_first = lightness(cmap(0.0)) < lightness(cmap(1.0))
        page = theme.get("figure_facecolor")
        stops = DARK_PAGE_STOPS if page and lightness(page) < 0.5 else LIGHT_PAGE_STOPS
        oriented = stops if dark_first else 1 - stops
        samples = [mcolors.to_hex(cmap(t)) for t in oriented]
        ramp = [mcolors.to_hex(cmap(t)) for t in np.linspace(0, 1, 4)]
        theme.update(
            {
                "color_general_singular": lead,
                "color_general_multiple": [samples[i] for i in INTERLEAVED],
                "color_parallel_hue_continuous": ramp if not dark_first else ramp[::-1],
                "plot_heatmap_cmap": lead,
                "plot_dumbbell_start_color": samples[-1],
                "plot_dumbbell_end_color": samples[0],
            }
        )
    else:
        theme.update(
            {
                "color_general_singular": (
                    get_color_scale(lead)[0] if isinstance(lead, str) else lead[0]
                ),
                "color_general_multiple": lead,
            }
        )

    overrides = canonical_style(overrides)
    unknown = set(overrides) - set(theme)
    if unknown:
        raise ValueError(f"Unknown theme attributes: {sorted(unknown)}")
    theme.update(copy.deepcopy(overrides))
    return theme
