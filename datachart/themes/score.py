"""Score a series palette for colour-blind readers."""

# the gate, its thresholds and the simulation model are fixed by ADR 0073

import itertools
import warnings
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from ..typings import StyleAttrs
from ..utils._internal.colors import (
    CUSTOM_PALETTES,
    delta_e,
    get_discrete_colors,
    oklab_lightness,
    wcag_contrast,
)

# worst deutan or protan pair (OKLab ΔE ×100): the target, and the floor a
# theme ships at only with a pattern cycle carrying identity
CVD_TARGET = 8.0
CVD_FLOOR = 6.0
# the worst pair under normal vision, so every reader tells neighbours apart
NORMAL_FLOOR = 15.0
# WCAG 2 non-text contrast of a mark against the face it sits on
CONTRAST_FLOOR = 3.0
# how many colours a named palette contributes, as the six-series default
PALETTE_SERIES = 6

VISION_KINDS = ("deutan", "protan", "tritan", "normal")


@dataclass(frozen=True)
class PaletteScore:
    """How far apart a palette's two closest colours are, per kind of vision.

    Every distance is the palette's worst pair in OKLab ΔE ×100, `grey_gap`
    the smallest lightness step between two colours once printed without
    colour, `low_contrast` how many colours sit under 3:1 against the face,
    `worst_kind` whichever of deutan and protan scores lower and `worst_pair`
    the pair behind it. `verdict` is `"pass"` when deutan and protan reach 8
    and normal reaches 15, `"weak"` when deutan and protan stay between 6
    and 8 with normal at 15, and `"fail"` otherwise.
    """

    deutan: float
    protan: float
    tritan: float
    normal: float
    grey_gap: float
    low_contrast: int
    worst_kind: str
    worst_pair: Tuple[str, str]
    verdict: str

    def __str__(self) -> str:
        return (
            f"deutan {self.deutan:.1f} · protan {self.protan:.1f} · "
            f"tritan {self.tritan:.1f} · normal {self.normal:.1f} · "
            f"greyscale gap {self.grey_gap:.0f} · {self.verdict} "
            f"({self.worst_pair[0]} vs {self.worst_pair[1]}, {self.worst_kind} "
            f"ΔE {getattr(self, self.worst_kind):.1f})"
        )


def palette_colors(palette: Union[str, List[str]]) -> List[str]:
    """The colours a series palette holds, whatever form a theme keeps it in.

    A list is its own colours; a name is datachart's own palette of that name,
    else six colours of the pypalettes palette.
    """

    if isinstance(palette, str):
        return list(
            CUSTOM_PALETTES.get(palette) or get_discrete_colors(palette, PALETTE_SERIES)
        )
    return list(palette)


def score_palette(
    colors: Union[str, List[str]], face: Optional[str] = None
) -> PaletteScore:
    """Score a series palette for colour-blind readers.

    Every pair of colours is compared, since any two series may sit side by
    side; each colour is passed through the Machado, Oliveira and Fernandes
    (2009) simulation of deuteranopia, protanopia and tritanopia at full
    severity and the distance measured in OKLab (ΔE ×100).

    Examples:
        >>> from datachart.themes import DEFAULT_THEME, score_palette
        >>> score = score_palette(DEFAULT_THEME["color_general_multiple"])
        >>> score.verdict
        'pass'

    Args:
        colors: The palette: a list of colours, a `COLORS` constant, or a
            pypalettes palette name.
        face: The colour the marks sit on, for the contrast count; `None`
            counts nothing.

    Returns:
        The score.

    Raises:
        ValueError: When the palette holds fewer than two colours.

    """

    swatches = palette_colors(colors)
    if len(swatches) < 2:
        raise ValueError("A palette needs at least two colours to score.")
    pairs = list(itertools.combinations(swatches, 2))
    worst = {}
    for kind in VISION_KINDS:
        deficiency = None if kind == "normal" else kind
        pair = min(pairs, key=lambda p: delta_e(p[0], p[1], deficiency))
        worst[kind] = (delta_e(pair[0], pair[1], deficiency), pair)
    lightness = sorted(100 * oklab_lightness(c) for c in swatches)
    grey_gap = min(b - a for a, b in zip(lightness, lightness[1:]))
    low_contrast = (
        0
        if face is None
        else sum(wcag_contrast(c, face) < CONTRAST_FLOOR for c in swatches)
    )
    worst_kind = min(("deutan", "protan"), key=lambda k: worst[k][0])
    cvd = worst[worst_kind][0]
    if cvd >= CVD_TARGET and worst["normal"][0] >= NORMAL_FLOOR:
        verdict = "pass"
    elif cvd >= CVD_FLOOR and worst["normal"][0] >= NORMAL_FLOOR:
        verdict = "weak"
    else:
        verdict = "fail"
    return PaletteScore(
        deutan=worst["deutan"][0],
        protan=worst["protan"][0],
        tritan=worst["tritan"][0],
        normal=worst["normal"][0],
        grey_gap=grey_gap,
        low_contrast=low_contrast,
        worst_kind=worst_kind,
        worst_pair=worst[worst_kind][1],
        verdict=verdict,
    )


def theme_palette_score(theme: StyleAttrs) -> Optional[PaletteScore]:
    """A theme's series palette scored against its face, `None` for one ink.

    The face is the axes face, else the figure face, else white.
    """

    colors = palette_colors(theme["color_general_multiple"])
    if len(colors) < 2:
        return None
    face = theme.get("axes_facecolor") or theme.get("figure_facecolor") or "#FFFFFF"
    return score_palette(colors, face)


def warn_failing_palette(theme: StyleAttrs) -> None:
    """Warn, at the caller of the caller, when a theme's palette fails the gate."""

    score = theme_palette_score(theme)
    if score is not None and score.verdict == "fail":
        warnings.warn(
            f"The theme's series palette fails the colour-blindness gate: {score}",
            UserWarning,
            stacklevel=3,
        )
