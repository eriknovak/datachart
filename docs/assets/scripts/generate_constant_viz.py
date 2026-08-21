"""Generates docs/assets/imgs/const-*.svg — one at-a-glance visualization per
constants class (fonts, lines, hatches, legends, value formats, colorbars).

Run from the repo root: python docs/assets/scripts/generate_constant_viz.py
"""

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.constants import (
    COLORBAR_LOCATION,
    FONT_STYLE,
    FONT_WEIGHT,
    HATCH_STYLE,
    LEGEND_ALIGN,
    LINE_DRAW_STYLE,
    LINE_MARKER,
    LINE_STYLE,
    VALUE_FORMAT,
)
from datachart.themes import DEFAULT_THEME
from datachart.utils._internal.colors import create_color_cycle

IMGS = pathlib.Path(__file__).resolve().parents[1] / "imgs"

_cycle = create_color_cycle(DEFAULT_THEME["color_general_singular"], 3)
_, MID, DARK = (_cycle[key]["color"] for key in ("a", "b", "c"))
FACE = to_rgba(MID, 0.45)
MUTED = DEFAULT_THEME["muted_color"]
INK = DEFAULT_THEME["font_general_color"]
SAMPLE = "The quick brown fox jumps over the lazy dog"


def save(fig, name):
    fig.savefig(IMGS / name, format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {IMGS / name}")


def text_rows(rows, name, sample_kw):
    """One row per member: constant name on the left, styled sample text right.

    Saves when a name is given; otherwise returns the figure for annotation.
    """
    fig, ax = plt.subplots(figsize=(7, 0.4 * len(rows) + 0.3))
    for i, (label, value) in enumerate(rows):
        y = 1 - (i + 0.5) / len(rows)
        ax.text(0.0, y, label, va="center", fontsize=10, color=INK, family="monospace")
        ax.text(
            0.38, y, SAMPLE, va="center", fontsize=11, color=INK, **{sample_kw: value}
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    if name is None:
        return fig
    save(fig, name)


def font_style():
    rows = [
        ("FONT_STYLE.NORMAL", FONT_STYLE.NORMAL),
        ("FONT_STYLE.ITALIC", FONT_STYLE.ITALIC),
        ("FONT_STYLE.OBLIQUE", FONT_STYLE.OBLIQUE),
    ]
    text_rows(rows, "const-font-style.svg", "fontstyle")


def font_weight():
    rows = [
        ("FONT_WEIGHT.ULTRA_LIGHT", FONT_WEIGHT.ULTRA_LIGHT),
        ("FONT_WEIGHT.LIGHT", FONT_WEIGHT.LIGHT),
        ("FONT_WEIGHT.NORMAL", FONT_WEIGHT.NORMAL),
        ("FONT_WEIGHT.MEDIUM", FONT_WEIGHT.MEDIUM),
        ("FONT_WEIGHT.SEMIBOLD", FONT_WEIGHT.SEMIBOLD),
        ("FONT_WEIGHT.BOLD", FONT_WEIGHT.BOLD),
        ("FONT_WEIGHT.EXTRA_BOLD", FONT_WEIGHT.EXTRA_BOLD),
        ("FONT_WEIGHT.HEAVY", FONT_WEIGHT.HEAVY),
        ("FONT_WEIGHT.BLACK", FONT_WEIGHT.BLACK),
    ]
    fig = text_rows(rows, None, "fontweight")
    fig.text(
        0.0,
        -0.04,
        "Rendered weight depends on the font family; the default provides regular and bold only.",
        fontsize=8.5,
        color=INK,
        style="italic",
    )
    save(fig, "const-font-weight.svg")


def line_marker():
    members = [
        ("NONE", LINE_MARKER.NONE),
        ("PIXEL", LINE_MARKER.PIXEL),
        ("POINT", LINE_MARKER.POINT),
        ("CIRCLE", LINE_MARKER.CIRCLE),
        ("DIAMOND", LINE_MARKER.DIAMOND),
        ("THIN_DIAMOND", LINE_MARKER.THIN_DIAMOND),
        ("TRIANGLE", LINE_MARKER.TRIANGLE),
        ("TRIANGLE_DOWN", LINE_MARKER.TRIANGLE_DOWN),
        ("TRIANGLE_LEFT", LINE_MARKER.TRIANGLE_LEFT),
        ("TRIANGLE_RIGHT", LINE_MARKER.TRIANGLE_RIGHT),
        ("SQUARE", LINE_MARKER.SQUARE),
        ("PENTAGON", LINE_MARKER.PENTAGON),
        ("HEXAGON", LINE_MARKER.HEXAGON),
        ("STAR", LINE_MARKER.STAR),
        ("CROSS", LINE_MARKER.CROSS),
        ("PLUS", LINE_MARKER.PLUS),
        ("VLINE", LINE_MARKER.VLINE),
        ("HLINE", LINE_MARKER.HLINE),
    ]
    cols = 6
    rows = -(-len(members) // cols)
    fig, ax = plt.subplots(figsize=(7, 1.5 * rows))
    for i, (label, value) in enumerate(members):
        cx, cy = i % cols + 0.5, rows - (i // cols) - 0.5
        if value:
            ax.plot([cx], [cy], marker=value, markersize=11, color=DARK, linestyle="")
        ax.text(
            cx, cy - 0.38, label, ha="center", fontsize=8, color=INK, family="monospace"
        )
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis("off")
    save(fig, "const-line-marker.svg")


def line_style():
    members = [
        ("NONE", LINE_STYLE.NONE),
        ("SOLID", LINE_STYLE.SOLID),
        ("DASHED", LINE_STYLE.DASHED),
        ("DASHDOT", LINE_STYLE.DASHDOT),
        ("DOTTED", LINE_STYLE.DOTTED),
    ]
    fig, ax = plt.subplots(figsize=(7, 0.4 * len(members) + 0.3))
    for i, (label, value) in enumerate(members):
        y = 1 - (i + 0.5) / len(members)
        ax.text(
            0.0,
            y,
            f"LINE_STYLE.{label}",
            va="center",
            fontsize=10,
            color=INK,
            family="monospace",
        )
        if value:
            ax.plot([0.38, 1.0], [y, y], linestyle=value, color=DARK, lw=2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    save(fig, "const-line-style.svg")


def line_draw_style():
    members = [
        ("DEFAULT", LINE_DRAW_STYLE.DEFAULT),
        ("STEPS_PRE", LINE_DRAW_STYLE.STEPS_PRE),
        ("STEPS_MID", LINE_DRAW_STYLE.STEPS_MID),
        ("STEPS_POST", LINE_DRAW_STYLE.STEPS_POST),
    ]
    x, y = [0, 1, 2, 3], [1, 3, 2, 4]
    fig, axs = plt.subplots(1, 4, figsize=(7, 1.9), sharey=True)
    for ax, (label, value) in zip(axs, members):
        ax.plot(x, y, drawstyle=value, color=DARK, lw=1.8)
        ax.plot(x, y, linestyle="", marker="o", markersize=4, color=MID)
        ax.set_title(
            f"LINE_DRAW_STYLE.\n{label}", fontsize=8, color=INK, family="monospace"
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(MUTED)
    save(fig, "const-line-draw-style.svg")


def hatch_style():
    members = [
        ("DEFAULT", HATCH_STYLE.DEFAULT),
        ("DIAGONAL", HATCH_STYLE.DIAGONAL),
        ("BACK_DIAGONAL", HATCH_STYLE.BACK_DIAGONAL),
        ("VERTICAL", HATCH_STYLE.VERTICAL),
        ("HORIZONTAL", HATCH_STYLE.HORIZONTAL),
        ("CROSSED", HATCH_STYLE.CROSSED),
        ("CROSSED_DIAGONAL", HATCH_STYLE.CROSSED_DIAGONAL),
        ("DOTS", HATCH_STYLE.DOTS),
        ("CIRCLES", HATCH_STYLE.CIRCLES),
        ("STARS", HATCH_STYLE.STARS),
    ]
    cols = 5
    rows = -(-len(members) // cols)
    fig, ax = plt.subplots(figsize=(7, 1.7 * rows))
    for i, (label, value) in enumerate(members):
        cx, cy = i % cols, rows - (i // cols) - 1
        ax.add_patch(
            Rectangle(
                (cx + 0.12, cy + 0.32),
                0.76,
                0.55,
                facecolor="white",
                edgecolor=DARK,
                hatch=(value * 2) if value else None,
                lw=1,
            )
        )
        ax.text(
            cx + 0.5,
            cy + 0.14,
            label,
            ha="center",
            fontsize=8,
            color=INK,
            family="monospace",
        )
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis("off")
    save(fig, "const-hatch-style.svg")


def legend_align():
    members = [
        ("LEFT", LEGEND_ALIGN.LEFT),
        ("CENTER", LEGEND_ALIGN.CENTER),
        ("RIGHT", LEGEND_ALIGN.RIGHT),
    ]
    fig, axs = plt.subplots(1, 3, figsize=(7, 1.7))
    for ax, (label, value) in zip(axs, members):
        handles = [
            plt.Line2D([], [], color=DARK, lw=2, label="alpha"),
            plt.Line2D([], [], color=MID, lw=2, label="beta"),
        ]
        legend = ax.legend(
            handles=handles,
            title="A wide legend title",
            alignment=value,
            loc="center",
            fontsize=8,
            title_fontsize=8,
        )
        legend.get_frame().set_edgecolor(MUTED)
        ax.set_title(f"LEGEND_ALIGN.{label}", fontsize=9, color=INK, family="monospace")
        ax.axis("off")
    save(fig, "const-legend-align.svg")


def legend_location():
    spots = {
        "UPPER_LEFT": (0.04, 0.93, "left", "top"),
        "UPPER_CENTER": (0.5, 0.93, "center", "top"),
        "UPPER_RIGHT": (0.96, 0.93, "right", "top"),
        "CENTER_LEFT": (0.04, 0.5, "left", "center"),
        "CENTER": (0.5, 0.5, "center", "center"),
        "CENTER_RIGHT": (0.96, 0.5, "right", "center"),
        "LOWER_LEFT": (0.04, 0.07, "left", "bottom"),
        "LOWER_CENTER": (0.5, 0.07, "center", "bottom"),
        "LOWER_RIGHT": (0.96, 0.07, "right", "bottom"),
    }
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for label, (x, y, ha, va) in spots.items():
        ax.text(
            x,
            y,
            label,
            ha=ha,
            va=va,
            fontsize=9,
            color=INK,
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.35", facecolor=FACE, edgecolor=DARK, lw=1),
        )
    ax.text(
        0.5,
        -0.08,
        "BEST picks the least-crowded spot automatically; RIGHT is an alias of CENTER_RIGHT",
        ha="center",
        va="top",
        fontsize=9,
        color=INK,
    )
    for spine in ax.spines.values():
        spine.set_color(INK)
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, "const-legend-location.svg")


def value_format():
    members = [
        ("DEFAULT", VALUE_FORMAT.DEFAULT),
        ("INTEGER", VALUE_FORMAT.INTEGER),
        ("DECIMAL", VALUE_FORMAT.DECIMAL),
        ("DECIMAL_2", VALUE_FORMAT.DECIMAL_2),
        ("DECIMAL_3", VALUE_FORMAT.DECIMAL_3),
        ("PERCENT", VALUE_FORMAT.PERCENT),
        ("PERCENT_INT", VALUE_FORMAT.PERCENT_INT),
        ("SCIENTIFIC", VALUE_FORMAT.SCIENTIFIC),
        ("THOUSANDS", VALUE_FORMAT.THOUSANDS),
    ]
    fig, ax = plt.subplots(figsize=(7, 0.4 * (len(members) + 1) + 0.3))
    n = len(members) + 1
    header_y = 1 - 0.5 / n
    for x, text in (
        (0.0, "constant"),
        (0.42, "format"),
        (0.62, "1234.5678 (0.4321 for %) →"),
    ):
        ax.text(
            x, header_y, text, va="center", fontsize=9, color=INK, fontweight="bold"
        )
    for i, (label, value) in enumerate(members):
        y = 1 - (i + 1.5) / n
        sample = 0.4321 if "%" in value else 1234.5678
        ax.text(
            0.0,
            y,
            f"VALUE_FORMAT.{label}",
            va="center",
            fontsize=9.5,
            color=INK,
            family="monospace",
        )
        ax.text(
            0.42,
            y,
            f'"{value}"',
            va="center",
            fontsize=9.5,
            color=INK,
            family="monospace",
        )
        ax.text(
            0.62,
            y,
            value.format(x=sample),
            va="center",
            fontsize=9.5,
            color=DARK,
            family="monospace",
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    save(fig, "const-value-format.svg")


def colorbar_location():
    members = [
        ("RIGHT", COLORBAR_LOCATION.RIGHT),
        ("LEFT", COLORBAR_LOCATION.LEFT),
        ("TOP", COLORBAR_LOCATION.TOP),
        ("BOTTOM", COLORBAR_LOCATION.BOTTOM),
    ]
    data = np.linspace(0, 1, 16).reshape(4, 4)
    fig = plt.figure(figsize=(7, 2.6), layout="constrained")
    # subfigures keep each title above its own colorbar, whatever its location
    for subfig, (label, value) in zip(fig.subfigures(1, 4), members):
        ax = subfig.subplots()
        image = ax.imshow(data, cmap="Blues")
        subfig.colorbar(image, ax=ax, location=value, fraction=0.15, pad=0.06)
        subfig.suptitle(
            f"COLORBAR_LOCATION.\n{label}", fontsize=8, color=INK, family="monospace"
        )
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, "const-colorbar-location.svg")


def main():
    font_style()
    font_weight()
    line_marker()
    line_style()
    line_draw_style()
    hatch_style()
    legend_align()
    legend_location()
    value_format()
    colorbar_location()


if __name__ == "__main__":
    main()
