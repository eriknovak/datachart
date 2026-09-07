import os

from matplotlib import font_manager

from ._base import make_theme
from ..typings import StyleAttrs
from ..constants import COLORS, FONT_WEIGHT

# Comic Neue Regular + Bold (SIL OFL, licence alongside) ship with the package
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_fonts")
_FONT_FILES = ("ComicNeue-Regular.ttf", "ComicNeue-Bold.ttf")


def _register_bundled_fonts() -> None:
    """Register the bundled faces with matplotlib once, so the theme's font
    stack resolves on every machine."""

    known = {entry.fname for entry in font_manager.fontManager.ttflist}
    for name in _FONT_FILES:
        path = os.path.join(_FONT_DIR, name)
        # a face missing from the install leaves the stack to its fallbacks
        if path not in known and os.path.isfile(path):
            font_manager.fontManager.addfont(path)


_register_bundled_fonts()

SKETCH_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": [
            "#2E86AB",
            "#E4572E",
            "#76B041",
            "#F5B700",
            "#7E5AAB",
        ],
        "font_general_family": "sans-serif",
        # the fallbacks only apply when the bundled face fails to register
        "font_general_sansserif": ["Comic Neue", "Humor Sans", "Comic Sans MS"],
        "font_general_size": 11,
        "font_general_color": "#222222",
        "font_title_size": 15,
        "font_title_color": "#222222",
        "font_title_weight": FONT_WEIGHT.BOLD,
        "axes_spines_width": 1.6,
        "axes_ticks_length": 5,
        "chart_default_show_grid": None,
        "plot_line_width": 2.5,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 1.6,
        "plot_hist_edge_width": 1.6,
        "plot_scatter_edge_color": "#222222",
        "plot_heatmap_cmap": COLORS.Blues,
        # a wobbled box around wobbled tiles reads as a second drawing; the
        # band and the pad already mark the group
        "plot_treemap_group_edge_width": 0,
        # half the amplitude of matplotlib's xkcd mode (1, 100, 2), plus a halo
        "plot_sketch_params": (0.5, 100, 2),
        "plot_sketch_halo_width": 4,
    }
)
"""The sketch theme: hand-drawn, xkcd-style wobble and halo, Comic Neue font.

Paths wobble, lines carry a white halo, spines and lines are thick, the grid is
off, and text is set in Comic Neue, which ships with the package; Humor Sans
and Comic Sans MS are the fallbacks should the bundled face fail to register.

!!! info "Added in v0.9.1"
"""
