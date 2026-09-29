"""Generates docs/assets/imgs/fig-sizes.svg — every FIG_SIZE drawn to scale
on an A4 page (paper sizes) or as a standalone frame (slide sizes).

Run from the repo root: python docs/assets/scripts/generate_fig_sizes.py
"""

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.constants import FIG_SIZE
from datachart.themes import DEFAULT_THEME
from datachart.utils._internal.colors import create_color_cycle

A4_W, A4_H = 8.27, 11.69
MARGIN = 2.5 / 2.54  # the 2.5 cm print margin the paper sizes are anchored to
COLUMN_GAP = 0.3

# colors come from the DEFAULT theme: its singular Blues cycle and font color
_cycle = create_color_cycle(DEFAULT_THEME["color_general_singular"], 3)
_, _MID, _DARK = (_cycle[key]["color"] for key in ("a", "b", "c"))
PAGE_COLOR = "#ffffff"
PAGE_EDGE = "#000000"
MARGIN_EDGE = DEFAULT_THEME["muted_color"]
BOX_FACE = to_rgba(_MID, 0.45)
BOX_EDGE = _DARK
GHOST_EDGE = _MID
LABEL_COLOR = DEFAULT_THEME["font_general_color"]

# (name, size, ghost twin for side-by-side half-width figures);
# rows of at most four pages keep the image narrow enough for the docs column
PAPER_ROWS = [
    [
        ("FULL_SHORT", FIG_SIZE.FULL_SHORT, False),
        ("FULL_MEDIUM", FIG_SIZE.FULL_MEDIUM, False),
        ("FULL_TALL", FIG_SIZE.FULL_TALL, False),
        ("A4_PORTRAIT", FIG_SIZE.A4_PORTRAIT, False),
    ],
    [
        ("HALF_SHORT", FIG_SIZE.HALF_SHORT, True),
        ("HALF_MEDIUM", FIG_SIZE.HALF_MEDIUM, True),
        ("HALF_TALL", FIG_SIZE.HALF_TALL, True),
        ("HALF_SQUARE", FIG_SIZE.HALF_SQUARE, True),
    ],
    [
        ("A4_LANDSCAPE", FIG_SIZE.A4_LANDSCAPE, False),
        ("SQUARE", FIG_SIZE.SQUARE, False),
        ("DEFAULT", FIG_SIZE.DEFAULT, False),
    ],
]

SLIDE_SIZES = [
    ("SLIDE_16_9", FIG_SIZE.SLIDE_16_9),
    ("SLIDE_4_3", FIG_SIZE.SLIDE_4_3),
    ("BEAMER_16_9", FIG_SIZE.BEAMER_16_9),
    ("BEAMER_4_3", FIG_SIZE.BEAMER_4_3),
]


def size_label(name, size):
    w, h = size
    return f"{name}\n{w} × {h} in\n({w * 2.54:.1f} × {h * 2.54:.1f} cm)"


def draw_page_with_box(ax, x0, y0, name, size, ghost):
    w, h = size
    page_w, page_h = (A4_H, A4_W) if name == "A4_LANDSCAPE" else (A4_W, A4_H)
    ax.add_patch(
        Rectangle(
            (x0, y0), page_w, page_h, facecolor=PAGE_COLOR, edgecolor=PAGE_EDGE, lw=1
        )
    )
    ax.add_patch(
        Rectangle(
            (x0 + MARGIN, y0 + MARGIN),
            page_w - 2 * MARGIN,
            page_h - 2 * MARGIN,
            facecolor="none",
            edgecolor=MARGIN_EDGE,
            lw=0.8,
            linestyle=":",
        )
    )
    # figures hang from the top of the text block
    box_y = y0 + page_h - MARGIN - h
    box_x = (
        x0 + (page_w - w) / 2 if not ghost else x0 + (page_w - 2 * w - COLUMN_GAP) / 2
    )
    ax.add_patch(
        Rectangle((box_x, box_y), w, h, facecolor=BOX_FACE, edgecolor=BOX_EDGE, lw=1.2)
    )
    if ghost:
        ax.add_patch(
            Rectangle(
                (box_x + w + COLUMN_GAP, box_y),
                w,
                h,
                facecolor="none",
                edgecolor=GHOST_EDGE,
                lw=1.2,
                linestyle="--",
            )
        )
    ax.text(
        x0 + page_w / 2,
        y0 - 0.6,
        size_label(name, size),
        ha="center",
        va="top",
        fontsize=9,
        color=LABEL_COLOR,
        linespacing=1.5,
    )


def draw_slide(ax, x0, y0, name, size):
    w, h = size
    ax.add_patch(
        Rectangle((x0, y0), w, h, facecolor=BOX_FACE, edgecolor=BOX_EDGE, lw=1.2)
    )
    ax.text(
        x0 + w / 2,
        y0 - 0.6,
        size_label(name, size),
        ha="center",
        va="top",
        fontsize=9,
        color=LABEL_COLOR,
        linespacing=1.5,
    )


def main():
    out = pathlib.Path(__file__).resolve().parents[1] / "imgs" / "fig-sizes.svg"
    gap = 1.0
    label_h = 4.2
    row_step = A4_H + label_h
    n_rows = len(PAPER_ROWS)

    # one axes with equal aspect keeps every mockup at the same physical scale
    # width matches the other constants images so on-page text sizes agree
    fig, ax = plt.subplots(figsize=(7, 14))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    max_x = 0.0
    for i, row in enumerate(PAPER_ROWS):
        y0 = (n_rows - i) * row_step
        x0 = 0.0
        for name, size, ghost in row:
            draw_page_with_box(ax, x0, y0, name, size, ghost)
            page_w = A4_H if name == "A4_LANDSCAPE" else A4_W
            x0 += page_w + gap
        max_x = max(max_x, x0 - gap)

    x0 = 0.0
    slide_h = max(h for _, (_, h) in SLIDE_SIZES)
    for name, size in SLIDE_SIZES:
        draw_slide(ax, x0, 0.0, name, size)
        x0 += size[0] + gap
    max_x = max(max_x, x0 - gap)

    ax.text(
        max_x / 2,
        n_rows * row_step + A4_H + 1.0,
        "FIG_SIZE on an A4 page\ndotted: the 2.5 cm print margins; dashed: a second half-width figure beside",
        ha="center",
        fontsize=11,
        color=LABEL_COLOR,
        linespacing=1.6,
    )
    ax.text(
        max_x / 2,
        slide_h + 1.0,
        "Presentation sizes, at the same scale as the pages above",
        ha="center",
        fontsize=11,
        color=LABEL_COLOR,
    )
    ax.set_xlim(-0.4, max_x + 0.4)
    ax.set_ylim(-label_h, n_rows * row_step + A4_H + 4.4)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(out, format="svg", bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
