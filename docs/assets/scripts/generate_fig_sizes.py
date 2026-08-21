"""Generates docs/assets/imgs/fig-sizes.svg — every FIG_SIZE drawn to scale
on an A4 page (paper sizes) or as a standalone frame (slide sizes).

Run from the repo root: python docs/assets/scripts/generate_fig_sizes.py
"""

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.constants import FIG_SIZE

A4_W, A4_H = 8.27, 11.69
TOP_MARGIN = 1.0

PAGE_COLOR = "#ffffff"
PAGE_EDGE = "#9e9e9e"
BOX_FACE = "#aecbe8"
BOX_EDGE = "#3d6f9e"
GHOST_EDGE = "#8fb2d4"
LABEL_COLOR = "#333333"

# (name, size, ghost twin for side-by-side half-width figures)
PAPER_SIZES = [
    ("FULL_SHORT", FIG_SIZE.FULL_SHORT, False),
    ("FULL_MEDIUM", FIG_SIZE.FULL_MEDIUM, False),
    ("FULL_TALL", FIG_SIZE.FULL_TALL, False),
    ("HALF_SHORT", FIG_SIZE.HALF_SHORT, True),
    ("HALF_MEDIUM", FIG_SIZE.HALF_MEDIUM, True),
    ("HALF_TALL", FIG_SIZE.HALF_TALL, True),
    ("A4_PORTRAIT", FIG_SIZE.A4_PORTRAIT, False),
    ("A4_LANDSCAPE", FIG_SIZE.A4_LANDSCAPE, False),
    ("SQUARE", FIG_SIZE.SQUARE, False),
    ("DEFAULT", FIG_SIZE.DEFAULT, False),
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
    # full-page sizes sit centered; figures hang from a 1 in top margin
    box_y = y0 + max(page_h - TOP_MARGIN - h, (page_h - h) / 2)
    box_x = x0 + (page_w - w) / 2 if not ghost else x0 + (page_w - 2 * w - 0.2) / 2
    ax.add_patch(
        Rectangle((box_x, box_y), w, h, facecolor=BOX_FACE, edgecolor=BOX_EDGE, lw=1.2)
    )
    if ghost:
        ax.add_patch(
            Rectangle(
                (box_x + w + 0.2, box_y),
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
    gap = 1.2
    label_h = 4.2
    row_step = A4_H + label_h

    # one axes with equal aspect keeps every mockup at the same physical scale
    fig, ax = plt.subplots(figsize=(13.5, 12))
    row_specs = [(PAPER_SIZES[:5], 2 * row_step), (PAPER_SIZES[5:], row_step)]

    max_x = 0.0
    for row, y0 in row_specs:
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
        2 * row_step + A4_H + 1.0,
        "FIG_SIZE on an A4 page (dashed: a second half-width figure placed beside)",
        ha="center",
        fontsize=13,
        color=LABEL_COLOR,
    )
    ax.text(
        max_x / 2,
        slide_h + 1.0,
        "Presentation sizes, at the same scale as the pages above",
        ha="center",
        fontsize=13,
        color=LABEL_COLOR,
    )
    ax.set_xlim(-0.4, max_x + 0.4)
    ax.set_ylim(-label_h, 2 * row_step + A4_H + 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, format="svg", bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
