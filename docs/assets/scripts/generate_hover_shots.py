"""Generates docs/assets/imgs/hover-*.png — one screenshot per chart type of
the figure shown with `show(interactive=True)` and a mark hovered, for the
support table of the interactive figures guide (ADR 0031).

The hover is synthesised: the figure is shown on the Agg canvas, a pointer
motion event is fired over a mark, and the figure is saved with the
annotation mplcursors placed. No window or widget is needed.

Run from the repo root: python docs/assets/scripts/generate_hover_shots.py
"""

import pathlib
import sys
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseEvent

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.charts import (
    BarChart,
    BoxPlot,
    ContourChart,
    Heatmap,
    HexbinChart,
    Histogram,
    LineChart,
    NetworkChart,
    ParallelCoords,
    PyramidChart,
    RadialChart,
    RaincloudPlot,
    SankeyChart,
    ScatterChart,
    StackedAreaChart,
    SwarmPlot,
    Treemap,
    ViolinPlot,
)

OUT = pathlib.Path(__file__).resolve().parents[1] / "imgs"
FIGSIZE = (5.0, 3.4)
DPI = 110

rng = np.random.default_rng(7)
GROUPS = {
    "Control": rng.normal(50, 8, 40),
    "Treatment": rng.normal(58, 10, 40),
    "Placebo": rng.normal(52, 6, 40),
}
GROUP_DATA = [
    {"label": name, "value": round(float(v), 1)}
    for name, values in GROUPS.items()
    for v in values
]


def _hover(figure, ax, x, y):
    """Show the figure interactively and move the pointer over data point (x, y)."""

    with warnings.catch_warnings():
        # Agg opens no window; plt.show() warns instead
        warnings.simplefilter("ignore")
        figure.show(interactive=True)
    figure.canvas.draw()
    px, py = ax.transData.transform((x, y))
    event = MouseEvent("motion_notify_event", figure.canvas, px, py)
    figure.canvas.callbacks.process("motion_notify_event", event)
    if not figure._hover_cursor.selections:
        raise RuntimeError(f"no mark under the pointer at {(x, y)}")


def _save(figure, name):
    figure.savefig(OUT / f"hover-{name}.png", dpi=DPI, bbox_inches="tight")
    plt.close("all")


def _target(figure, kind):
    """The first registered hover target whose artist is a `kind`."""

    return next((a, r) for a, r in figure._hover_targets if isinstance(a, kind))


def line():
    years = list(range(2019, 2025))
    figure = LineChart(
        data=[
            [{"x": y, "y": v} for y, v in zip(years, [12, 15, 14, 19, 23, 21])],
            [{"x": y, "y": v} for y, v in zip(years, [8, 9, 13, 12, 15, 18])],
        ],
        subtitle=["Web", "Mobile"],
        xlabel="Year",
        ylabel="Signups (k)",
        figsize=FIGSIZE,
    )
    _hover(figure, figure.axes[0], 2023, 23)
    _save(figure, "line")


def stackedarea():
    figure = StackedAreaChart(
        data=[
            [{"x": i, "y": v} for i, v in enumerate([3, 4, 5, 6, 6, 7])],
            [{"x": i, "y": v} for i, v in enumerate([2, 3, 3, 5, 6, 8])],
        ],
        subtitle=["Desktop", "Mobile"],
        xlabel="Year",
        ylabel="Visits (M)",
        figsize=FIGSIZE,
    )
    _hover(figure, figure.axes[0], 3.9, 9)
    _save(figure, "stackedarea")


def bar():
    figure = BarChart(
        data=[
            [
                {"label": r, "y": v}
                for r, v in zip(["North", "South", "East"], [42, 31, 55])
            ],
            [
                {"label": r, "y": v}
                for r, v in zip(["North", "South", "East"], [38, 44, 47])
            ],
        ],
        subtitle=["2024", "2025"],
        xlabel="Region",
        ylabel="Revenue (M)",
        figsize=FIGSIZE,
    )
    _hover(figure, figure.axes[0], 2.2, 20)
    _save(figure, "bar")


def pyramid():
    ages = ["0-19", "20-39", "40-59", "60+"]
    figure = PyramidChart(
        data=[
            [{"label": a, "y": v} for a, v in zip(ages, [22, 31, 27, 18])],
            [{"label": a, "y": v} for a, v in zip(ages, [21, 30, 28, 23])],
        ],
        subtitle=["Men", "Women"],
        xlabel="Population (%)",
        figsize=FIGSIZE,
    )
    _hover(figure, figure.axes[0], 15, 1)
    _save(figure, "pyramid")


def radial():
    figure = RadialChart(
        data=[
            {"label": d, "y": v}
            for d, v in zip(
                ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], [5, 8, 12, 9, 6, 4, 7, 10]
            )
        ],
        type="bar",
        subtitle="Wind hours",
        figsize=FIGSIZE,
    )
    _hover(figure, figure.axes[0], 2 * np.pi / 8 * 2, 6)
    _save(figure, "radial")


def histogram():
    figure = Histogram(
        data=[{"x": round(float(v), 1)} for v in rng.normal(70, 12, 300)],
        num_bins=12,
        subtitle="Exam scores",
        xlabel="Score",
        ylabel="Students",
        figsize=FIGSIZE,
    )
    bars, _ = _target(figure, matplotlib.container.BarContainer)
    tallest = max(bars.patches, key=lambda p: p.get_height())
    _hover(
        figure,
        figure.axes[0],
        tallest.get_x() + tallest.get_width() / 2,
        tallest.get_height() / 2,
    )
    _save(figure, "histogram")


def box():
    figure = BoxPlot(data=GROUP_DATA, xlabel="Group", ylabel="Score", figsize=FIGSIZE)
    _hover(figure, figure.axes[0], 2, float(np.median(GROUPS["Treatment"])))
    _save(figure, "box")


def violin():
    figure = ViolinPlot(
        data=GROUP_DATA, xlabel="Group", ylabel="Score", figsize=FIGSIZE
    )
    _hover(figure, figure.axes[0], 2.05, float(np.median(GROUPS["Treatment"])))
    _save(figure, "violin")


def swarm():
    figure = SwarmPlot(data=GROUP_DATA, xlabel="Group", ylabel="Score", figsize=FIGSIZE)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        figure.show(interactive=True)
    figure.canvas.draw()
    points, _ = _target(figure, matplotlib.collections.PathCollection)
    x, y = points.get_offsets()[45]
    _hover(figure, figure.axes[0], x, y)
    _save(figure, "swarm")


def raincloud():
    figure = RaincloudPlot(
        data=GROUP_DATA, xlabel="Group", ylabel="Score", figsize=FIGSIZE
    )
    _hover(figure, figure.axes[0], 2.2, float(np.median(GROUPS["Treatment"])))
    _save(figure, "raincloud")


def scatter():
    figure = ScatterChart(
        data=[
            {
                "x": round(float(x), 2),
                "y": round(float(y), 2),
                "hue": ["Sedan", "SUV"][i % 2],
            }
            for i, (x, y) in enumerate(
                zip(rng.uniform(1, 4, 40), rng.uniform(20, 45, 40))
            )
        ],
        xlabel="Engine (L)",
        ylabel="Efficiency (mpg)",
        figsize=FIGSIZE,
    )
    points, _ = _target(figure, matplotlib.collections.PathCollection)
    x, y = points.get_offsets()[3]
    _hover(figure, figure.axes[0], x, y)
    _save(figure, "scatter")


def heatmap():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    slots = ["Morning", "Noon", "Evening"]
    figure = Heatmap(
        data={"x": days, "y": slots, "z": rng.integers(10, 90, (3, 5)).tolist()},
        xlabel="Day",
        ylabel="Slot",
        figsize=FIGSIZE,
    )
    _hover(figure, figure.axes[0], 2, 1)
    _save(figure, "heatmap")


def contour():
    x = y = np.linspace(-2, 2, 30)
    xx, yy = np.meshgrid(x, y)
    z = np.exp(-(xx**2 + yy**2)) + 0.6 * np.exp(-((xx - 1) ** 2 + (yy + 1) ** 2))
    figure = ContourChart(
        data={"x": x.tolist(), "y": y.tolist(), "z": z.tolist()},
        xlabel="x",
        ylabel="y",
        subtitle="Density",
        figsize=FIGSIZE,
    )
    contours, _ = _target(figure, matplotlib.contour.ContourSet)
    vertex = contours.get_paths()[3].vertices[10]
    _hover(figure, figure.axes[0], *vertex)
    _save(figure, "contour")


def hexbin():
    figure = HexbinChart(
        data={"x": rng.normal(0, 1, 800).tolist(), "y": rng.normal(0, 1, 800).tolist()},
        gridsize=12,
        xlabel="x",
        ylabel="y",
        figsize=FIGSIZE,
    )
    tiles, _ = _target(figure, matplotlib.collections.PolyCollection)
    densest = int(np.argmax(tiles.get_array()))
    _hover(figure, figure.axes[0], *tiles.get_offsets()[densest])
    _save(figure, "hexbin")


def parallelcoords():
    figure = ParallelCoords(
        data=[
            {"Price": 21, "Range": 420, "Seats": 5, "Class": "Compact"},
            {"Price": 35, "Range": 510, "Seats": 5, "Class": "Sedan"},
            {"Price": 48, "Range": 480, "Seats": 7, "Class": "SUV"},
            {"Price": 62, "Range": 600, "Seats": 4, "Class": "Sport"},
        ],
        dimensions=["Price", "Range", "Seats"],
        hue="Class",
        figsize=FIGSIZE,
    )
    line, _ = _target(figure, matplotlib.lines.Line2D)
    x, y = line.get_xydata()[1]
    _hover(figure, figure.axes[0], x, y)
    _save(figure, "parallelcoords")


def network():
    figure = NetworkChart(
        data={
            "nodes": [{"id": n, "group": g} for n, g in zip("abcdef", "xxxyyy")],
            "edges": [
                {"source": "a", "target": "b", "weight": 3},
                {"source": "a", "target": "c", "weight": 1},
                {"source": "b", "target": "d", "weight": 2},
                {"source": "d", "target": "e", "weight": 4},
                {"source": "e", "target": "f", "weight": 2},
                {"source": "c", "target": "f", "weight": 1},
            ],
        },
        seed=3,
        figsize=FIGSIZE,
    )
    nodes, _ = _target(figure, matplotlib.collections.PathCollection)
    _hover(figure, figure.axes[0], *nodes.get_offsets()[3])
    _save(figure, "network")


def sankey():
    figure = SankeyChart(
        data={
            "links": [
                {"source": "Visited", "target": "Signed up", "value": 300},
                {"source": "Visited", "target": "Bounced", "value": 700},
                {"source": "Signed up", "target": "Paid", "value": 90},
                {"source": "Signed up", "target": "Churned", "value": 210},
            ]
        },
        figsize=FIGSIZE,
    )
    links, _ = _target(figure, matplotlib.container.BarContainer)
    # the second container holds the ribbons; hover the widest at its middle
    ribbons = [a for a, _ in figure._hover_targets][1]
    widest = max(ribbons.patches, key=lambda p: p.get_path().get_extents().height)
    box = widest.get_path().get_extents()
    _hover(figure, figure.axes[0], (box.x0 + box.x1) / 2, (box.y0 + box.y1) / 2)
    _save(figure, "sankey")


def treemap():
    figure = Treemap(
        data={
            "data": [
                {
                    "label": "Asia",
                    "children": [
                        {"label": "India", "value": 1429},
                        {"label": "China", "value": 1426},
                        {"label": "Indonesia", "value": 278},
                    ],
                },
                {"label": "Africa", "value": 1460},
                {"label": "Europe", "value": 742},
                {"label": "Americas", "value": 1040},
            ]
        },
        show_values=True,
        figsize=FIGSIZE,
    )
    tiles, _ = _target(figure, matplotlib.container.BarContainer)
    tile = next(p for p in tiles.patches if p.get_gid() == "tile:India")
    _hover(
        figure,
        figure.axes[0],
        tile.get_x() + tile.get_width() / 2,
        tile.get_y() + tile.get_height() / 2,
    )
    _save(figure, "treemap")


def main():
    for shot in (
        line,
        stackedarea,
        bar,
        pyramid,
        radial,
        histogram,
        box,
        violin,
        swarm,
        raincloud,
        scatter,
        heatmap,
        contour,
        hexbin,
        parallelcoords,
        network,
        sankey,
        treemap,
    ):
        shot()
        print(f"hover-{shot.__name__}.png")


if __name__ == "__main__":
    main()
