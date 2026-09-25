"""Derive a theme variant from a base theme and a lead colormap."""

import copy
from typing import Any, List, Optional, Sequence, Union

import numpy as np
import matplotlib.colors as mcolors

from ._base import TRAITS, canonical_style, warn_aliases
from .default import DEFAULT_THEME
from ..constants import TRAIT
from ..typings import StyleAttrs
from ..utils._internal.colors import get_color_scale, get_colormap, oklab_lightness

Lead = Union[str, List[str]]

# the series palette samples the lead at these positions, measured from its
# dark end; the trimmed quarter is the end that would vanish into the page
LIGHT_PAGE_STOPS = np.linspace(0.0, 0.75, 6)
DARK_PAGE_STOPS = np.linspace(0.25, 1.0, 6)
# darkest, lightest, then inward: neighbours in the cycle stay far apart
INTERLEAVED = (0, 5, 1, 4, 2, 3)
# a lightness step smaller than this is colormap noise, not a turn
SEQUENTIAL_TOLERANCE = 0.01


def _is_sequential(cmap: mcolors.Colormap) -> bool:
    """Whether a colormap's lightness runs one way along it.

    A categorical palette bounces; a diverging map turns in the middle, so it
    reads as categorical too and is never a lead.
    """

    steps = np.diff([oklab_lightness(c) for c in cmap(np.linspace(0, 1, 12))])
    return bool(
        np.all(steps >= -SEQUENTIAL_TOLERANCE) or np.all(steps <= SEQUENTIAL_TOLERANCE)
    )


def _is_dark_page(theme: StyleAttrs) -> bool:
    page = theme.get("figure_facecolor")
    if page is None or mcolors.to_rgba(page)[3] == 0:
        return False
    return oklab_lightness(page) < 0.5


def _resolve_base(base: Union[str, StyleAttrs]) -> StyleAttrs:
    if isinstance(base, dict):
        return {**copy.deepcopy(DEFAULT_THEME), **copy.deepcopy(base)}
    # for a name only: the config module imports this package while loading
    from ..config.configuration import THEMES

    if base not in THEMES:
        raise ValueError(f"Unknown theme: {base!r}. Must be one of {list(THEMES)}")
    return copy.deepcopy(THEMES[base])


def derive_theme(
    base: Union[str, StyleAttrs],
    lead: Lead,
    traits: Optional[Sequence[Union[TRAIT, str]]] = None,
    **overrides: Any,
) -> StyleAttrs:
    """Build a theme variant: the base's furniture with palettes rebuilt from the lead.

    A sequential lead becomes the value scale (`color_general_singular`,
    `plot_heatmap_cmap`); the series palette is six of its colors in lightness
    steps, interleaved dark and light, the parallel coords ramp four of them
    from light to dark, and the dumbbell pair its lightest and darkest sample.
    A categorical lead becomes the series palette, its first color the singular
    one, and the base keeps its value scale, ramp, and dumbbell pair. Each
    trait then sets its mark keys, in the order given, so a later trait wins a
    shared key; fonts, spines and rendering attributes are never touched. The
    result is a plain theme dictionary: apply it with `register_theme` or
    `override`; `TRAIT` lists the traits and the predefined themes built
    this way.

    Examples:
        >>> from datachart.config import config
        >>> from datachart.constants import COLORS, THEME
        >>> from datachart.themes import derive_theme
        >>> forest = derive_theme(THEME.MINIMAL, lead=COLORS.Greens)
        >>> config.register_theme("forest", forest)
        >>> config.set_theme("forest")

    Args:
        base: A `THEME` constant, a registered theme name, or a theme dictionary;
            a partial dictionary is completed from the default theme, as
            `register_theme` completes it.
        lead: A `COLORS` constant, a pypalettes palette name, or a list of colors.
            A diverging map is not a lead; it is read as categorical.
        traits: `TRAIT` members applied in order after the lead; an unknown
            name raises.
        **overrides: Style attributes set on the result; an unknown name raises.

    Returns:
        The derived theme.

    """

    theme = _resolve_base(base)
    swatches = get_color_scale(lead) if isinstance(lead, str) else list(lead)
    if len(swatches) < 2:
        raise ValueError("The lead must hold at least two colors.")
    cmap = get_colormap(lead)
    sequential = _is_sequential(cmap)

    if sequential:
        # positions run from the lead's dark end whichever way it is written
        dark_first = oklab_lightness(cmap(0.0)) < oklab_lightness(cmap(1.0))
        stops = DARK_PAGE_STOPS if _is_dark_page(theme) else LIGHT_PAGE_STOPS
        samples = [
            mcolors.to_hex(cmap(t)) for t in (stops if dark_first else 1 - stops)
        ]
        ramp = [mcolors.to_hex(cmap(t)) for t in np.linspace(0, 1, 4)]
        theme.update(
            {
                "color_general_singular": lead,
                "color_general_multiple": [samples[i] for i in INTERLEAVED],
                "color_parallel_hue_continuous": ramp[::-1] if dark_first else ramp,
                "plot_heatmap_cmap": lead,
                "plot_dumbbell_start_color": samples[-1],
                "plot_dumbbell_end_color": samples[0],
            }
        )
    else:
        # the colors themselves: a palette name would be resampled as a ramp
        theme.update(
            {
                "color_general_singular": swatches[0],
                "color_general_multiple": swatches,
            }
        )

    for trait in traits or ():
        if TRAIT.check(trait, "traits") is not None:
            theme.update(copy.deepcopy(TRAITS[trait]))

    warn_aliases(overrides)
    overrides = canonical_style(overrides)
    unknown = set(overrides) - set(theme)
    if unknown:
        raise ValueError(f"Unknown theme attributes: {sorted(unknown)}")
    theme.update(copy.deepcopy(overrides))
    return theme
