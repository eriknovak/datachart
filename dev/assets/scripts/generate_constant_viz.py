"""Generates docs/assets/imgs/const-*.svg — one at-a-glance visualization per
constants class. Text-like constants (fonts, lines, hatches, legends, value
and date formats, colorbars) are drawn with raw matplotlib; chart-setting
constants (bar modes, histogram types, orientation, grid, scales, norms,
emphasis, aspect ratios, annotation connectors, sort orders, label positions,
gantt and dumbbell settings, the scatter matrix diagonal) render through the
chart fronts (ADR 0013).

Run from the repo root: python docs/assets/scripts/generate_constant_viz.py
"""

import pathlib
import sys
from datetime import date, datetime, timedelta

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.charts import (
    BarChart,
    BumpChart,
    CalendarHeatmap,
    ContourChart,
    DumbbellChart,
    GanttChart,
    Heatmap,
    HexbinChart,
    Histogram,
    ImageChart,
    BasemapChart,
    LineChart,
    NetworkChart,
    RadialChart,
    RidgelinePlot,
    ScatterChart,
    ScatterMatrix,
    StackedAreaChart,
    SwarmPlot,
    ViolinPlot,
)
from datachart.config import config
from datachart.constants import (
    ARROW_STYLE,
    ASPECT_RATIO,
    BANDWIDTH,
    BAR_MODE,
    LINE_LABEL_POSITION,
    BUMP_RANK,
    CALENDAR_WEEKDAY,
    COLORBAR_LOCATION,
    CONTOUR_LEVELS,
    DATE_FORMAT,
    DUMBBELL_SORT_KEY,
    DUMBBELL_VALUE,
    EMPHASIS,
    FONT_STYLE,
    FONT_WEIGHT,
    GANTT_ARROW_ENTRY,
    GANTT_DATE_PERIOD,
    GANTT_SORT_KEY,
    GANTT_VALUE,
    HATCH_STYLE,
    HEXBIN_REDUCE,
    HISTOGRAM_TYPE,
    DRAW_POSITION,
    BASEMAP_FEATURE,
    BASEMAP_RESOLUTION,
    LEGEND_ALIGN,
    LINE_DRAW_STYLE,
    LINE_MARKER,
    LINE_STYLE,
    NETWORK_LAYOUT,
    NETWORK_LABEL_POSITION,
    COLOR_NORM,
    ORIENTATION,
    RADIAL_DIRECTION,
    RADIAL_TYPE,
    RIDGELINE_SCALE,
    AXIS_SCALE,
    SCATTER_MATRIX_DIAGONAL,
    SHOW_GRID,
    SORT,
    STACKED_AREA_BASELINE,
    SWARM_MODE,
    VALUE_FORMAT,
    VIOLIN_INNER,
)
from datachart.themes import DEFAULT_THEME
from datachart.utils import Grid, Panel
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
        ("NO_MARKER", LINE_MARKER.NO_MARKER),
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
        ("NO_LINE", LINE_STYLE.NO_LINE),
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
        ("STRAIGHT", ARROW_STYLE.STRAIGHT),
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
        "side and depth against the data, TOUCHING starts flush at the box border. "
        "Network edges take the headless CURVE and STRAIGHT only.",
    )


def network_layout():
    members = [
        ("SPRING", NETWORK_LAYOUT.SPRING),
        ("WEIGHTED", NETWORK_LAYOUT.WEIGHTED),
        ("GROUPED", NETWORK_LAYOUT.GROUPED),
        ("CIRCULAR", NETWORK_LAYOUT.CIRCULAR),
        ("FIXED", NETWORK_LAYOUT.FIXED),
    ]
    # six modules in two packages; the weights are the imported names, FIXED
    # reads the hand-placed x/y from the nodes
    placed = {
        "core": ("lib", 0.5, 0.5),
        "utils": ("lib", 0.5, 0.12),
        "tests": ("lib", 0.12, 0.35),
        "cli": ("app", 0.15, 0.85),
        "api": ("app", 0.85, 0.85),
        "web": ("app", 0.88, 0.4),
    }
    edges = [
        {"source": s, "target": t, "weight": w}
        for s, t, w in (
            ("core", "utils", 9),
            ("cli", "core", 2),
            ("api", "core", 1),
            ("web", "api", 8),
            ("tests", "core", 6),
            ("tests", "api", 1),
        )
    ]
    figs = [
        NetworkChart(
            data={
                "nodes": [
                    {"id": k, "group": g, "x": x, "y": y}
                    for k, (g, x, y) in placed.items()
                ],
                "edges": edges,
            },
            layout=value,
            directed=True,
            title=f"NETWORK_LAYOUT.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-network-layout.svg",
        10.0,
        cols=2,
        footnote="The same six modules; SPRING is seeded so it repeats, WEIGHTED "
        "pulls heavy edges short,\nGROUPED clusters by group, CIRCULAR keeps the "
        "input order, FIXED reads each node's x and y.",
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
        # beside the axes: the side placements hang from the top edge
        "OUTSIDE_RIGHT": (1.02, 1.0, "left", "top"),
        "OUTSIDE_LEFT": (-0.02, 1.0, "right", "top"),
        "OUTSIDE_TOP": (0.5, 1.03, "center", "bottom"),
        "OUTSIDE_BOTTOM": (0.5, -0.03, "center", "top"),
    }
    fig, ax = plt.subplots(figsize=(7, 4.2))
    fig.subplots_adjust(left=0.2, right=0.8, top=0.88, bottom=0.24)
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
            transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.35", facecolor=FACE, edgecolor=DARK, lw=1),
        )
    ax.text(
        0.5,
        -0.2,
        "BEST picks the least-crowded spot automatically; RIGHT is an alias of "
        "CENTER_RIGHT;\nOUTSIDE_* sits beside the axes, clear of the tick labels",
        ha="center",
        va="top",
        fontsize=FS_NOTE,
        color=INK,
        transform=ax.transAxes,
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


def chart_grid(figs, name, height, cols=None, footnote=None, rasterize=False):
    """Compose chart-front figures with Grid, restyled to the const-* look.

    Chart-setting constants are rendered through the datachart fronts, so the
    figures show the package's actual behavior (ADR 0013).
    """
    fig = Grid(figs, max_cols=cols or len(figs), figsize=(7, height))
    for ax in fig.axes:
        ax.title.set_fontfamily("monospace")
        ax.title.set_fontsize(FS_LABEL)
        if rasterize:
            # an SVG keeps every vertex, even off view: a world outline is MBs
            for artist in ax.collections + ax.patches:
                artist.set_rasterized(True)
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


AREA_SERIES = [
    [{"x": x, "y": y} for x, y in enumerate(ys)]
    for ys in ([2, 3, 4, 4, 5, 6], [3, 2, 3, 4, 3, 2], [1, 2, 2, 3, 4, 5])
]


def baseline():
    members = [
        ("ZERO", STACKED_AREA_BASELINE.ZERO),
        ("PERCENT", STACKED_AREA_BASELINE.PERCENT),
        ("SYM", STACKED_AREA_BASELINE.SYM),
        ("WIGGLE", STACKED_AREA_BASELINE.WIGGLE),
        ("WEIGHTED_WIGGLE", STACKED_AREA_BASELINE.WEIGHTED_WIGGLE),
    ]
    figs = [
        StackedAreaChart(
            data=AREA_SERIES, baseline=value, title=f"STACKED_AREA_BASELINE.{label}"
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-baseline.svg",
        4.0,
        cols=3,
        footnote="The same three series; the baseline moves where the first one starts.",
    )


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


def weekday():
    members = [("MONDAY", CALENDAR_WEEKDAY.MONDAY), ("SUNDAY", CALENDAR_WEEKDAY.SUNDAY)]
    days = [date(2024, 1, 1) + timedelta(days=i) for i in range(91)]
    values = [(i % 7) * (i % 5) for i in range(len(days))]
    figs = [
        CalendarHeatmap(
            data={"date": days, "value": values},
            week_start=value,
            title=f"CALENDAR_WEEKDAY.{label}",
        )
        for label, value in members
    ]
    # stacked: side by side the cells are too small to read
    chart_grid(
        figs,
        "const-weekday.svg",
        3.6,
        cols=1,
        footnote="The first quarter of 2024; the week start is the top row.",
    )


def _violin_data():
    rng = np.random.default_rng(7)
    return [
        {"label": label, "value": float(v)}
        for label, (mu, sd) in zip("abc", ((0, 1), (2, 1.5), (1, 0.6)))
        for v in rng.normal(mu, sd, 60)
    ]


def violin_inner():
    members = [
        ("BOX", VIOLIN_INNER.BOX),
        ("QUARTILES", VIOLIN_INNER.QUARTILES),
        ("MEDIAN", VIOLIN_INNER.MEDIAN),
        ("None", None),
    ]
    figs = [
        ViolinPlot(
            data=_violin_data(),
            inner=value,
            title=f"VIOLIN_INNER.{label}" if value else "None",
        )
        for label, value in members
    ]
    chart_grid(figs, "const-violin-inner.svg", 2.2)


def bandwidth():
    members = [
        ("BANDWIDTH.SCOTT", BANDWIDTH.SCOTT),
        ("BANDWIDTH.SILVERMAN", BANDWIDTH.SILVERMAN),
        ("0.25", 0.25),
        ("1.0", 1.0),
    ]
    figs = [
        ViolinPlot(data=_violin_data(), bandwidth=value, inner=None, title=label)
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-bandwidth.svg",
        2.2,
        footnote="The two rules differ by a constant 6%; a number is a factor on "
        "the standard deviation of the values.",
    )


def contour_levels():
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    # the "peaks" surface: a few hills and hollows of different heights
    z = (
        3 * (1 - X) ** 2 * np.exp(-(X**2) - (Y + 1) ** 2)
        - 10 * (X / 5 - X**3 - Y**5) * np.exp(-(X**2) - Y**2)
        - np.exp(-((X + 1) ** 2) - Y**2) / 3
    )
    members = [
        ("AUTO", CONTOUR_LEVELS.AUTO),
        ("RICE", CONTOUR_LEVELS.RICE),
        ("FD", CONTOUR_LEVELS.FD),
    ]
    figs = [
        ContourChart(
            data={"x": x, "y": x, "z": z},
            levels=value,
            title=f"CONTOUR_LEVELS.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-contour-levels.svg",
        2.4,
        footnote="The same 120×120 surface; the rules count levels from the "
        "per-axis resolution, so a finer grid draws more of them.",
    )


def hexbin_reduce():
    rng = np.random.RandomState(4)
    pts = rng.normal(0, 1, (3000, 2))
    # a per-point value that rises along the diagonal, so the reducers differ
    data = {
        "x": pts[:, 0].tolist(),
        "y": pts[:, 1].tolist(),
        "c": (pts[:, 0] + pts[:, 1] + rng.normal(0, 0.5, 3000)).tolist(),
    }
    members = [
        ("MEAN", HEXBIN_REDUCE.MEAN),
        ("SUM", HEXBIN_REDUCE.SUM),
        ("MEDIAN", HEXBIN_REDUCE.MEDIAN),
        ("MIN", HEXBIN_REDUCE.MIN),
        ("MAX", HEXBIN_REDUCE.MAX),
    ]
    figs = [
        HexbinChart(
            data=data,
            reduce=value,
            gridsize=12,
            show_colorbars=False,
            title=f"HEXBIN_REDUCE.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-hexbin-reduce.svg",
        3.6,
        cols=3,
        footnote="The same 3,000 points and c values; each hexagon shows the "
        "aggregate of the c of its points.",
    )


def draw_position():
    # a translucent square over the middle of a line, grid on
    square = np.zeros((10, 10, 4))
    square[..., :3] = to_rgba(DARK)[:3]
    square[..., 3] = 0.55
    line = LineChart(
        data=[{"x": x, "y": (x - 4) ** 2} for x in range(9)], show_grid="both"
    )
    figs = [
        Panel(
            [
                line,
                ImageChart({"image": square, "extent": (2, 6, 1, 12)}, position=value),
            ],
            title=f"DRAW_POSITION.{label}",
            show_grid="both",
        )
        for label, value in [
            ("BELOW", DRAW_POSITION.BELOW),
            ("ABOVE", DRAW_POSITION.ABOVE),
        ]
    ]
    chart_grid(figs, "const-draw-position.svg", 2.2)


def basemap_feature():
    # each feature alone, over the Baltic, where all of them show
    members = [
        ("COASTLINE", BASEMAP_FEATURE.COASTLINE),
        ("LAND", BASEMAP_FEATURE.LAND),
        ("COUNTRIES", BASEMAP_FEATURE.COUNTRIES),
        ("BORDERS", BASEMAP_FEATURE.BORDERS),
        ("LAKES", BASEMAP_FEATURE.LAKES),
        ("RIVERS", BASEMAP_FEATURE.RIVERS),
        ("ROADS", BASEMAP_FEATURE.ROADS),
    ]
    # the lines read at a finer scale, and roads exist at 1:10m alone
    resolutions = {
        "RIVERS": BASEMAP_RESOLUTION.MEDIUM,
        "ROADS": BASEMAP_RESOLUTION.HIGH,
    }
    figs = [
        BasemapChart(
            value,
            resolution=resolutions.get(label),
            # countries are one area each; highlight picks the Baltic states
            highlight=["EST", "LVA", "LTU"] if label == "COUNTRIES" else None,
            title=f"BASEMAP_FEATURE.{label}",
            xmin=5,
            xmax=40,
            ymin=50,
            ymax=66,
            style={"plot_basemap_lake_color": "#9ecae1"},
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-basemap-feature.svg",
        8.5,
        cols=2,
        rasterize=True,
        footnote="COUNTRIES highlights the Baltic states; the lakes are blue "
        "here. RIVERS is drawn at 1:50m, ROADS at 1:10m, its only scale.",
    )


def basemap_resolution():
    # the same stretch of coast at each scale, where the detail shows
    figs = [
        BasemapChart(
            [BASEMAP_FEATURE.LAND, BASEMAP_FEATURE.BORDERS],
            resolution=value,
            title=f"BASEMAP_RESOLUTION.{label}",
            xmin=12.5,
            xmax=16,
            ymin=44.5,
            ymax=46.5,
            aspect_ratio=ASPECT_RATIO.GEOGRAPHIC,
        )
        for label, value in [
            ("LOW", BASEMAP_RESOLUTION.LOW),
            ("MEDIUM", BASEMAP_RESOLUTION.MEDIUM),
            ("HIGH", BASEMAP_RESOLUTION.HIGH),
        ]
    ]
    chart_grid(
        figs,
        "const-basemap-resolution.svg",
        2.4,
        rasterize=True,
        footnote="The head of the Adriatic, Slovenia's coast and borders: "
        "1:110m, 1:50m and 1:10m.",
    )


def swarm_mode():
    members = [("SWARM", SWARM_MODE.SWARM), ("STRIP", SWARM_MODE.STRIP)]
    figs = [
        SwarmPlot(data=_violin_data(), mode=value, title=f"SWARM_MODE.{label}")
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-swarm-mode.svg",
        2.2,
        footnote="A swarm packs the points from their size; a strip jitters them "
        "uniformly across the jitter fraction of the category width.",
    )


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
            mark=value,
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
        ("CLOCKWISE", RADIAL_DIRECTION.CLOCKWISE),
        ("COUNTERCLOCKWISE", RADIAL_DIRECTION.COUNTERCLOCKWISE),
    ]
    months = [
        {"label": m, "y": y}
        for m, y in zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [3, 5, 7, 6, 4, 2])
    ]
    figs = [
        RadialChart(
            data=months,
            mark=RADIAL_TYPE.BAR,
            direction=value,
            title=f"RADIAL_DIRECTION.{label}",
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
        ("LINEAR", AXIS_SCALE.LINEAR),
        ("LOG", AXIS_SCALE.LOG),
        ("SYMLOG", AXIS_SCALE.SYMLOG),
        ("ASINH", AXIS_SCALE.ASINH),
    ]
    data = [{"x": x, "y": 10**x} for x in range(6)]
    figs = [
        LineChart(data=data, scaley=value, title=f"AXIS_SCALE.{label}")
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
        ("LINEAR", COLOR_NORM.LINEAR),
        ("LOG", COLOR_NORM.LOG),
        ("SYMLOG", COLOR_NORM.SYMLOG),
        ("ASINH", COLOR_NORM.ASINH),
        ("LOGIT", COLOR_NORM.LOGIT),
    ]
    # values in (0, 1) with a wide dynamic range, legal for every norm
    data = {"z": np.geomspace(0.001, 0.95, 16).reshape(4, 4).tolist()}
    figs = [
        Heatmap(
            data=data,
            norm=value,
            show_colorbars=False,
            title=f"COLOR_NORM.{label}",
        )
        for label, value in members
    ]
    # the centred norms need signed values and draw in the diverging cmap
    signed = {"z": np.linspace(-0.6, 0.95, 16).reshape(4, 4).round(2).tolist()}
    figs += [
        Heatmap(
            data=signed,
            norm=value,
            vmin=-0.6,
            vmax=0.95,
            show_colorbars=False,
            title=f"COLOR_NORM.{label}",
        )
        for label, value in (
            ("CENTERED", COLOR_NORM.CENTERED),
            ("TWOSLOPE", COLOR_NORM.TWOSLOPE),
        )
    ]
    chart_grid(
        figs,
        "const-normalize.svg",
        3.4,
        cols=4,
        footnote="The first five norms share one grid of positive values; "
        "CENTERED and TWOSLOPE hold zero in the middle of a signed one.",
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


def date_format():
    members = [
        ("AUTO", DATE_FORMAT.AUTO),
        ("ISO", DATE_FORMAT.ISO),
        ("YEAR", DATE_FORMAT.YEAR),
        ("YEAR_MONTH", DATE_FORMAT.YEAR_MONTH),
        ("MONTH_DAY", DATE_FORMAT.MONTH_DAY),
        ("DAY", DATE_FORMAT.DAY),
        ("TIME", DATE_FORMAT.TIME),
    ]
    sample = datetime(2024, 3, 7, 14, 5)
    fig, ax = plt.subplots(figsize=(7, 0.4 * (len(members) + 1) + 0.3))
    full_width(fig)
    n = len(members) + 1
    header_y = 1 - 0.5 / n
    for x, text in (
        (0.0, "constant"),
        (0.42, "pattern"),
        (0.62, "2024-03-07 14:05 →"),
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
        rendered = (
            "picked from the visible span"
            if value == DATE_FORMAT.AUTO
            else sample.strftime(value)
        )
        ax.text(
            0.0,
            y,
            f"DATE_FORMAT.{label}",
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
            rendered,
            va="center",
            fontsize=FS_LABEL,
            color=DARK,
            family="monospace",
            style="italic" if value == DATE_FORMAT.AUTO else "normal",
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    save(fig, "const-date-format.svg")


def sort():
    members = [
        ("NONE", SORT.NONE),
        ("ASCENDING", SORT.ASCENDING),
        ("DESCENDING", SORT.DESCENDING),
    ]
    figs = [
        BarChart(data=BAR_SERIES[0], sort=value, title=f"SORT.{label}")
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-sort.svg",
        2.2,
        footnote="The same four categories; NONE keeps the input order.",
    )


def ridgeline_scale():
    members = [
        ("PER_ROW", RIDGELINE_SCALE.PER_ROW),
        ("COMMON", RIDGELINE_SCALE.COMMON),
    ]
    figs = [
        RidgelinePlot(
            data=_violin_data(), ridge_scale=value, title=f"RIDGELINE_SCALE.{label}"
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-ridgeline-scale.svg",
        2.6,
        footnote="The same three ridges; the narrow one peaks highest, so under "
        "COMMON the wide ones flatten.",
    )


BUMP_SERIES = [
    [{"x": x, "y": y} for x, y in enumerate(ys, start=1)]
    for ys in ([30, 45, 20, 50], [40, 25, 35, 30], [20, 35, 45, 10])
]


def rank():
    members = [
        ("VALUE_DESCENDING", BUMP_RANK.VALUE_DESCENDING),
        ("VALUE_ASCENDING", BUMP_RANK.VALUE_ASCENDING),
        ("GIVEN", BUMP_RANK.GIVEN),
    ]
    given = [
        [{"x": x, "y": y} for x, y in enumerate(ys, start=1)]
        for ys in ([2, 1, 3, 1], [1, 3, 2, 2], [3, 2, 1, 3])
    ]
    figs = [
        BumpChart(
            data=given if value == BUMP_RANK.GIVEN else BUMP_SERIES,
            rank_by=value,
            subtitle=["alpha", "beta", "gamma"],
            show_values=True,
            title=f"BUMP_RANK.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-rank.svg",
        2.4,
        footnote="The value rules rank the same series per period; GIVEN "
        "reads y as the rank itself.",
    )


def label_position():
    members = [
        ("START", LINE_LABEL_POSITION.START),
        ("END", LINE_LABEL_POSITION.END),
        ("BOTH", LINE_LABEL_POSITION.BOTH),
    ]
    figs = [
        BumpChart(
            data=BUMP_SERIES,
            label_position=value,
            subtitle=["alpha", "beta", "gamma"],
            xticks=[1, 2, 3, 4],
            title=f"LINE_LABEL_POSITION.{label}",
        )
        for label, value in members
    ]
    chart_grid(figs, "const-label-position.svg", 4.4, cols=2)


def network_label_position():
    members = [
        ("CENTER", NETWORK_LABEL_POSITION.CENTER),
        ("ABOVE", NETWORK_LABEL_POSITION.ABOVE),
        ("BEST", NETWORK_LABEL_POSITION.BEST),
    ]
    data = {
        "nodes": [{"id": n} for n in ("core", "utils", "cli", "api", "web")],
        "edges": [
            {"source": s, "target": t}
            for s, t in (
                ("core", "utils"),
                ("cli", "core"),
                ("api", "core"),
                ("web", "api"),
            )
        ],
    }
    figs = [
        NetworkChart(
            data=data,
            layout=NETWORK_LAYOUT.CIRCULAR,
            label_position=value,
            title=f"NETWORK_LABEL_POSITION.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-network-label-position.svg",
        2.6,
        footnote="BEST tries the spots around each marker in turn and keeps the "
        "one clear of nodes, edges, and other labels.",
    )


def _gantt_tasks():
    d = date(2024, 3, 4)
    rows = [
        ("plan", "design", 0, 5, 1.0, []),
        ("mockups", "design", 5, 12, 0.6, ["plan"]),
        ("backend", "build", 3, 15, 0.4, ["plan"]),
        ("frontend", "build", 12, 20, 0.1, ["mockups"]),
        ("release", "build", 20, 20, 0.0, ["backend", "frontend"]),
    ]
    return [
        {
            "task": task,
            "group": group,
            "start": d + timedelta(days=a),
            "end": d + timedelta(days=b),
            "progress": progress,
            "depends_on": deps,
        }
        for task, group, a, b, progress, deps in rows
    ]


def gantt_value():
    members = [
        ("NONE", GANTT_VALUE.NONE),
        ("DURATION", GANTT_VALUE.DURATION),
        ("PROGRESS", GANTT_VALUE.PROGRESS),
    ]
    figs = [
        GanttChart(
            data=_gantt_tasks(),
            show_values=value,
            show_legend=False,
            title=f"GANTT_VALUE.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-gantt-value.svg",
        2.4,
        footnote="The same five tasks; the label prints past each bar's end.",
    )


def gantt_sort_key():
    members = [
        ("START", GANTT_SORT_KEY.START),
        ("GROUP", GANTT_SORT_KEY.GROUP),
    ]
    figs = [
        GanttChart(
            data=_gantt_tasks(),
            sort=SORT.ASCENDING,
            sort_by=value,
            title=f"GANTT_SORT_KEY.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-gantt-sort-key.svg",
        2.6,
        footnote="Both with sort=SORT.ASCENDING; GROUP keeps each group's "
        "tasks together.",
    )


def gantt_arrow_entry():
    members = [
        ("TOP", GANTT_ARROW_ENTRY.TOP),
        ("LEFT", GANTT_ARROW_ENTRY.LEFT),
    ]
    figs = [
        GanttChart(
            data=_gantt_tasks(),
            show_dependencies=True,
            show_legend=False,
            style={"plot_gantt_dependency_entry": value},
            title=f"GANTT_ARROW_ENTRY.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-gantt-arrow-entry.svg",
        2.6,
        footnote="The same dependencies; the entry is where the arrow meets "
        "the dependent bar.",
    )


def date_period():
    members = [
        ("NONE", GANTT_DATE_PERIOD.NONE),
        ("DAY", GANTT_DATE_PERIOD.DAY),
        ("WEEK", GANTT_DATE_PERIOD.WEEK),
        ("MONTH", GANTT_DATE_PERIOD.MONTH),
        ("QUARTER", GANTT_DATE_PERIOD.QUARTER),
        ("YEAR", GANTT_DATE_PERIOD.YEAR),
        ("PROJECT_MONTH", GANTT_DATE_PERIOD.PROJECT_MONTH),
    ]
    # each period needs a span that shows a handful of its edges: the three
    # week schedule as is, and stretched to seven and twenty months
    short = _gantt_tasks()
    origin = short[0]["start"]

    def stretched(factor):
        return [
            {
                **task,
                "start": origin + (task["start"] - origin) * factor,
                "end": origin + (task["end"] - origin) * factor,
            }
            for task in short
        ]

    spans = {
        "MONTH": stretched(10),
        "QUARTER": stretched(30),
        "YEAR": stretched(30),
        "PROJECT_MONTH": stretched(10),
    }
    figs = [
        GanttChart(
            data=spans.get(label, short),
            period=value,
            show_legend=False,
            title=f"GANTT_DATE_PERIOD.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-date-period.svg",
        8.0,
        cols=2,
        footnote="The same five tasks over three weeks (NONE, DAY, WEEK), seven "
        "months (MONTH, PROJECT_MONTH), and twenty months (QUARTER, YEAR);\nthe "
        "first label row names the period, the second its enclosing one.",
    )


DUMBBELL_RECORDS = [
    {"label": label, "start": start, "end": end}
    for label, start, end in (
        ("w", 20, 35),
        ("x", 40, 30),
        ("y", 15, 45),
        ("z", 30, 32),
    )
]


def dumbbell_value():
    members = [
        ("NONE", DUMBBELL_VALUE.NONE),
        ("ENDPOINTS", DUMBBELL_VALUE.ENDPOINTS),
        ("DELTA", DUMBBELL_VALUE.DELTA),
    ]
    figs = [
        DumbbellChart(
            data=DUMBBELL_RECORDS,
            show_values=value,
            show_legend=False,
            title=f"DUMBBELL_VALUE.{label}",
        )
        for label, value in members
    ]
    chart_grid(figs, "const-dumbbell-value.svg", 2.2)


def dumbbell_sort_key():
    members = [
        ("START", DUMBBELL_SORT_KEY.START),
        ("END", DUMBBELL_SORT_KEY.END),
        ("DELTA", DUMBBELL_SORT_KEY.DELTA),
    ]
    figs = [
        DumbbellChart(
            data=DUMBBELL_RECORDS,
            sort=SORT.ASCENDING,
            sort_by=value,
            show_legend=False,
            title=f"DUMBBELL_SORT_KEY.{label}",
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-dumbbell-sort-key.svg",
        2.2,
        footnote="All with sort=SORT.ASCENDING; DELTA orders by end - start, "
        "so a shrinking record comes first.",
    )


def diagonal():
    members = [
        ("HIST", SCATTER_MATRIX_DIAGONAL.HIST),
        ("KDE", SCATTER_MATRIX_DIAGONAL.KDE),
        ("BLANK", SCATTER_MATRIX_DIAGONAL.BLANK),
    ]
    rng = np.random.default_rng(3)
    a = rng.normal(0, 1, 120)
    data = {"a": a.tolist(), "b": (0.7 * a + rng.normal(0, 0.6, 120)).tolist()}
    figs = [
        ScatterMatrix(
            data=data, diagonal=value, title=f"SCATTER_MATRIX_DIAGONAL.{label}"
        )
        for label, value in members
    ]
    chart_grid(
        figs,
        "const-diagonal.svg",
        6.4,
        cols=2,
        footnote="The same two dimensions; only the cells on the diagonal change.",
    )


def main():
    font_style()
    font_weight()
    line_marker()
    line_style()
    line_draw_style()
    hatch_style()
    arrow_style()
    network_layout()
    legend_align()
    legend_location()
    value_format()
    colorbar_location()
    bar_mode()
    baseline()
    histogram_type()
    orientation()
    weekday()
    violin_inner()
    bandwidth()
    contour_levels()
    hexbin_reduce()
    draw_position()
    basemap_feature()
    basemap_resolution()
    swarm_mode()
    radial_type()
    direction()
    show_grid()
    scale()
    normalize()
    emphasis()
    aspect_ratio()
    date_format()
    sort()
    ridgeline_scale()
    rank()
    label_position()
    network_label_position()
    gantt_value()
    gantt_sort_key()
    gantt_arrow_entry()
    date_period()
    dumbbell_value()
    dumbbell_sort_key()
    diagonal()


if __name__ == "__main__":
    main()
