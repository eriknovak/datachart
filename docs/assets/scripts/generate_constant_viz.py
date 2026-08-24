"""Generates docs/assets/imgs/const-*.svg — one at-a-glance visualization per
constants class. Text-like constants (fonts, lines, hatches, legends, value
formats, colorbars) are drawn with raw matplotlib; chart-setting constants
(bar modes, histogram types, orientation, grid, scales, norms, emphasis,
aspect ratios, annotation connectors) render through the chart fronts
(ADR 0013).

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
from datachart.charts import (
    BarChart,
    Heatmap,
    Histogram,
    LineChart,
    RadialChart,
    ScatterChart,
)
from datachart.config import config
from datachart.constants import (
    ARROW_STYLE,
    ASPECT_RATIO,
    BAR_MODE,
    COLORBAR_LOCATION,
    DIRECTION,
    EMPHASIS,
    FONT_STYLE,
    FONT_WEIGHT,
    HATCH_STYLE,
    HISTOGRAM_TYPE,
    LEGEND_ALIGN,
    LINE_DRAW_STYLE,
    LINE_MARKER,
    LINE_STYLE,
    NORMALIZE,
    ORIENTATION,
    RADIAL_TYPE,
    SCALE,
    SHOW_GRID,
    VALUE_FORMAT,
)
from datachart.themes import DEFAULT_THEME
from datachart.utils import Grid
from datachart.utils._internal.colors import create_color_cycle

IMGS = pathlib.Path(__file__).resolve().parents[1] / "imgs"

_cycle = create_color_cycle(DEFAULT_THEME["color_general_singular"], 3)
_, MID, DARK = (_cycle[key]["color"] for key in ("a", "b", "c"))
FACE = to_rgba(MID, 0.45)
MUTED = DEFAULT_THEME["muted_color"]
INK = DEFAULT_THEME["font_general_color"]
SAMPLE = "The quick brown fox jumps over the lazy dog"

# one scheme across all images: equal pt at equal 7 in content width renders equal
FS_LABEL = 9
FS_BODY = 10
FS_NOTE = 8.5


def full_width(fig):
    """Axes flush to the figure edges, so every SVG crops to the same width."""
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)


def save(fig, name):
    fig.savefig(IMGS / name, format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {IMGS / name}")


def text_rows(rows, name, sample_kw, sample_family=None, footnote=None):
    """One row per member: constant name on the left, styled sample text right."""
    fig, ax = plt.subplots(figsize=(7, 0.32 * len(rows) + (0.3 if footnote else 0.05)))
    full_width(fig)
    family = sample_family or plt.rcParams["font.family"]
    for i, (label, value) in enumerate(rows):
        y = 1 - (i + 0.5) / len(rows)
        ax.text(
            0.0, y, label, va="center", fontsize=FS_LABEL, color=INK, family="monospace"
        )
        ax.text(
            0.36,
            y,
            SAMPLE,
            va="center",
            fontsize=FS_BODY,
            color=INK,
            family=family,
            **{sample_kw: value},
        )
    if footnote:
        pad = 0.8 / len(rows)
        ax.text(
            0.0,
            -pad,
            footnote,
            va="center",
            fontsize=FS_NOTE,
            color=INK,
            style="italic",
        )
        ax.set_ylim(-2 * pad / 1.6, 1)
    else:
        ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    ax.axis("off")
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
    # a family with many weight cuts; DejaVu would collapse them to two
    text_rows(
        rows,
        "const-font-weight.svg",
        "fontweight",
        sample_family=["Avenir Next", "Helvetica Neue", "DejaVu Sans"],
        footnote="The visible steps depend on the weights the active font family provides.",
    )


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
    full_width(fig)
    for i, (label, value) in enumerate(members):
        cx, cy = i % cols + 0.5, rows - (i // cols) - 0.5
        if value:
            ax.plot([cx], [cy], marker=value, markersize=11, color=DARK, linestyle="")
        ax.text(
            cx,
            cy - 0.38,
            label,
            ha="center",
            fontsize=FS_LABEL,
            color=INK,
            family="monospace",
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
    full_width(fig)
    for i, (label, value) in enumerate(members):
        y = 1 - (i + 0.5) / len(members)
        ax.text(
            0.0,
            y,
            f"LINE_STYLE.{label}",
            va="center",
            fontsize=FS_LABEL,
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
    fig, axs = plt.subplots(2, 2, figsize=(7, 4.6), sharex=True, sharey=True)
    fig.subplots_adjust(
        left=0, right=1, top=0.93, bottom=0.01, wspace=0.06, hspace=0.22
    )
    for ax, (label, value) in zip(axs.flat, members):
        ax.plot(x, y, drawstyle=value, color=DARK, lw=1.8)
        ax.plot(x, y, linestyle="", marker="o", markersize=4, color=MID)
        ax.set_title(
            f"LINE_DRAW_STYLE.{label}", fontsize=FS_LABEL, color=INK, family="monospace"
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
    full_width(fig)
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
            fontsize=FS_LABEL,
            color=INK,
            family="monospace",
        )
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis("off")
    save(fig, "const-hatch-style.svg")


def arrow_style():
    members = [
        ("CURVE", ARROW_STYLE.CURVE),
        ("CURVE_ARROW", ARROW_STYLE.CURVE_ARROW),
        ("TOUCHING", ARROW_STYLE.TOUCHING),
        ("ARROW", ARROW_STYLE.ARROW),
    ]
    data = [
        {"x": x, "y": y} for x, y in zip(range(10), [1, 3, 5, 8, 10, 11, 10, 8, 5, 3])
    ]
    figs = [
        LineChart(
            data=data,
            title=f"ARROW_STYLE.{label}",
            texts={
                "text": "note",
                "x": 0.78,
                "y": 0.25,
                "coords": "axes",
                "target": (5, 11),
                "style": {"plot_text_arrow_style": value},
            },
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-arrow-style.svg",
        3.4,
        cols=2,
        footnote="Same annotation under each look; curved looks pick their bow "
        "side and depth against the data, TOUCHING starts flush at the box border.",
    )


def legend_align():
    members = [
        ("LEFT", LEGEND_ALIGN.LEFT),
        ("CENTER", LEGEND_ALIGN.CENTER),
        ("RIGHT", LEGEND_ALIGN.RIGHT),
    ]
    fig, axs = plt.subplots(1, 3, figsize=(7, 1.05))
    fig.subplots_adjust(left=0, right=1, top=0.78, bottom=0.02, wspace=0.06)
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
            fontsize=FS_LABEL,
            title_fontsize=FS_LABEL,
        )
        legend.get_frame().set_edgecolor(MUTED)
        ax.set_title(
            f"LEGEND_ALIGN.{label}", fontsize=FS_LABEL, color=INK, family="monospace"
        )
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
    fig.subplots_adjust(left=0.002, right=0.998, top=0.995, bottom=0.12)
    for label, (x, y, ha, va) in spots.items():
        ax.text(
            x,
            y,
            label,
            ha=ha,
            va=va,
            fontsize=FS_LABEL,
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
        fontsize=FS_NOTE,
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
    full_width(fig)
    n = len(members) + 1
    header_y = 1 - 0.5 / n
    for x, text in (
        (0.0, "constant"),
        (0.42, "format"),
        (0.62, "1234.5678 (0.4321 for %) →"),
    ):
        ax.text(
            x,
            header_y,
            text,
            va="center",
            fontsize=FS_LABEL,
            color=INK,
            fontweight="bold",
        )
    for i, (label, value) in enumerate(members):
        y = 1 - (i + 1.5) / n
        sample = 0.4321 if "%" in value else 1234.5678
        ax.text(
            0.0,
            y,
            f"VALUE_FORMAT.{label}",
            va="center",
            fontsize=FS_LABEL,
            color=INK,
            family="monospace",
        )
        ax.text(
            0.42,
            y,
            f'"{value}"',
            va="center",
            fontsize=FS_LABEL,
            color=INK,
            family="monospace",
        )
        ax.text(
            0.62,
            y,
            value.format(x=sample),
            va="center",
            fontsize=FS_LABEL,
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
    fig = plt.figure(figsize=(7, 6.2), layout="constrained")
    # subfigures keep each title above its own colorbar, whatever its location
    for subfig, (label, value) in zip(fig.subfigures(2, 2).flat, members):
        ax = subfig.subplots()
        image = ax.imshow(data, cmap="Blues")
        colorbar = subfig.colorbar(
            image, ax=ax, location=value, fraction=0.15, pad=0.06
        )
        colorbar.ax.tick_params(labelsize=FS_LABEL)
        subfig.suptitle(
            f"COLORBAR_LOCATION.{label}",
            fontsize=FS_LABEL,
            color=INK,
            family="monospace",
        )
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, "const-colorbar-location.svg")


def chart_grid(figs, name, height, cols=None, footnote=None):
    """Compose chart-front figures with Grid, restyled to the const-* look.

    Chart-setting constants are rendered through the datachart fronts, so the
    figures show the package's actual behavior (ADR 0013).
    """
    fig = Grid(figs, max_cols=cols or len(figs), figsize=(7, height))
    for ax in fig.axes:
        ax.title.set_fontfamily("monospace")
        ax.title.set_fontsize(FS_LABEL)
    if footnote:
        # centered so a note wider than the grid cannot push it off-center,
        # with a fixed 0.22 in gap whatever the figure height
        fig.text(
            0.5,
            -0.22 / height,
            footnote,
            ha="center",
            fontsize=FS_NOTE,
            color=INK,
            style="italic",
        )
    save(fig, name)


BAR_SERIES = [
    [{"label": label, "y": y} for label, y in zip("wxyz", ys)]
    for ys in ([4, 6, 3, 5], [2, 3, 5, 2], [3, 1, 2, 4])
]


def bar_mode():
    members = [
        ("GROUP", BAR_MODE.GROUP),
        ("STACK", BAR_MODE.STACK),
        ("OVERLAY", BAR_MODE.OVERLAY),
    ]
    figs = [
        BarChart(data=BAR_SERIES, bar_mode=value, title=f"BAR_MODE.{label}")
        for label, value in members
    ]
    chart_grid(figs, "const-bar-mode.svg", 2.2)


def histogram_type():
    members = [
        ("BAR", HISTOGRAM_TYPE.BAR),
        ("STEP", HISTOGRAM_TYPE.STEP),
        ("STEP_FILLED", HISTOGRAM_TYPE.STEP_FILLED),
    ]
    rng = np.random.default_rng(42)
    values = rng.normal(0, 1, 400)
    figs = [
        Histogram(
            data=[{"x": x} for x in values],
            style={"plot_hist_type": value},
            title=f"HISTOGRAM_TYPE.{label}",
        )
        for label, value in members
    ]
    # the fourth panel shows the orthogonal axis: series sharing via bar_mode
    figs.append(
        Histogram(
            data=[
                [{"x": x} for x in values],
                [{"x": x} for x in rng.normal(2.5, 0.8, 250)],
            ],
            bar_mode="stack",
            title='bar_mode="stack"',
        )
    )
    chart_grid(
        figs,
        "const-histogram-type.svg",
        3.8,
        cols=2,
        footnote="The type renders one series; how several series share the "
        "axis is bar_mode's job.",
    )


def orientation():
    members = [
        ("VERTICAL", ORIENTATION.VERTICAL),
        ("HORIZONTAL", ORIENTATION.HORIZONTAL),
    ]
    figs = [
        BarChart(
            data=BAR_SERIES[0],
            orientation=value,
            title=f"ORIENTATION.{label}",
        )
        for label, value in members
    ]
    chart_grid(figs, "const-orientation.svg", 2.6)


def radial_type():
    members = [
        ("LINE", RADIAL_TYPE.LINE),
        ("BAR", RADIAL_TYPE.BAR),
        ("SCATTER", RADIAL_TYPE.SCATTER),
        ("HISTOGRAM", RADIAL_TYPE.HISTOGRAM),
    ]
    compass = [
        {"label": d, "y": y}
        for d, y in zip("N NE E SE S SW W NW".split(), [4, 7, 6, 3, 5, 8, 2, 6])
    ]
    degrees = [
        {"x": float(v % 360)}
        for v in np.random.default_rng(11).vonmises(0.8, 2, 200) * 180 / np.pi
    ]
    figs = [
        RadialChart(
            data=degrees if value == RADIAL_TYPE.HISTOGRAM else compass,
            type=value,
            num_bins=16,
            title=f"RADIAL_TYPE.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-radial-type.svg",
        2.2,
        footnote="LINE, BAR, and SCATTER place labels evenly around the circle; "
        "HISTOGRAM bins numeric degrees over [0, 360).",
    )


def direction():
    members = [
        ("CLOCKWISE", DIRECTION.CLOCKWISE),
        ("COUNTERCLOCKWISE", DIRECTION.COUNTERCLOCKWISE),
    ]
    months = [
        {"label": m, "y": y}
        for m, y in zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [3, 5, 7, 6, 4, 2])
    ]
    figs = [
        RadialChart(
            data=months,
            type=RADIAL_TYPE.BAR,
            direction=value,
            title=f"DIRECTION.{label}",
        )
        for label, value in members
    ]
    chart_grid(figs, "const-direction.svg", 2.6)


def show_grid():
    members = [
        ("NONE", SHOW_GRID.NONE),
        ("X", SHOW_GRID.X),
        ("Y", SHOW_GRID.Y),
        ("BOTH", SHOW_GRID.BOTH),
    ]
    data = [{"x": x, "y": y} for x, y in zip(range(6), [1, 3, 2, 5, 4, 6])]
    # mute the theme's grid opinion so NONE means no grid, and darken the
    # grid lines so the panels differ at thumbnail size
    config.update_config(
        {
            "chart_default_show_grid": None,
            "plot_grid_color": "#9A9A9A",
            "plot_grid_linewidth": 0.8,
            "plot_grid_alpha": 0.8,
        }
    )
    try:
        figs = [
            LineChart(data=data, show_grid=value, title=f"SHOW_GRID.{label}")
            for label, value in members
        ]
    finally:
        config.reset_config()
    chart_grid(
        figs,
        "const-show-grid.svg",
        1.9,
        footnote="Grid lines darkened for visibility; when show_grid is unset "
        "or NONE, the theme's chart_default_show_grid fills in.",
    )


def scale():
    members = [
        ("LINEAR", SCALE.LINEAR),
        ("LOG", SCALE.LOG),
        ("SYMLOG", SCALE.SYMLOG),
        ("ASINH", SCALE.ASINH),
    ]
    data = [{"x": x, "y": 10**x} for x in range(6)]
    figs = [
        LineChart(data=data, scaley=value, title=f"SCALE.{label}")
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-scale.svg",
        1.9,
        footnote="Same growth data on each value axis; "
        "SYMLOG and ASINH also accept zero and negative values.",
    )


def normalize():
    members = [
        ("LINEAR", NORMALIZE.LINEAR),
        ("LOG", NORMALIZE.LOG),
        ("SYMLOG", NORMALIZE.SYMLOG),
        ("ASINH", NORMALIZE.ASINH),
        ("LOGIT", NORMALIZE.LOGIT),
    ]
    # values in (0, 1) with a wide dynamic range, legal for every norm
    data = np.geomspace(0.001, 0.95, 16).reshape(4, 4).tolist()
    figs = [
        Heatmap(
            data=data,
            norm=value,
            show_colorbars=False,
            title=f"NORMALIZE.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-normalize.svg",
        1.7,
        footnote="Same cell values under each norm; "
        "SYMLOG and ASINH also accept zero and negative values.",
    )


def emphasis():
    members = [
        ("BACKGROUND", EMPHASIS.BACKGROUND),
        ("HIGHLIGHT", EMPHASIS.HIGHLIGHT),
    ]
    series = [
        [{"x": x, "y": y + offset} for x, y in zip(range(6), [1, 3, 2, 5, 4, 6])]
        for offset in (0, 1.5, 3)
    ]
    figs = [
        LineChart(
            data=series,
            subtitle=["alpha", "beta", "gamma"],
            emphasis=[None, value, None],
            show_legend=True,
            title=f"EMPHASIS.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-emphasis.svg",
        2.4,
        footnote='The "beta" series carries the emphasis role; '
        "BACKGROUND also drops its legend entry.",
    )


def aspect_ratio():
    members = [
        ("AUTO", ASPECT_RATIO.AUTO),
        ("EQUAL", ASPECT_RATIO.EQUAL),
    ]
    rng = np.random.default_rng(7)
    points = rng.uniform(0, 1, size=(40, 2)) * (2, 4)
    figs = [
        ScatterChart(
            data=[{"x": x, "y": y} for x, y in points],
            aspect_ratio=value,
            title=f"ASPECT_RATIO.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-aspect-ratio.svg",
        2.6,
        footnote="The y range is twice the x range; AUTO stretches the data to "
        "fill the box, EQUAL keeps one unit equal on both axes.",
    )


def main():
    font_style()
    font_weight()
    line_marker()
    line_style()
    line_draw_style()
    hatch_style()
    arrow_style()
    legend_align()
    legend_location()
    value_format()
    colorbar_location()
    bar_mode()
    histogram_type()
    orientation()
    radial_type()
    direction()
    show_grid()
    scale()
    normalize()
    emphasis()
    aspect_ratio()


if __name__ == "__main__":
    main()
