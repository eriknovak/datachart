"""Golden-image regression harness for the Layer/Panel drawing seam (ADR 0001).

Usage:
    python test/golden/golden.py baseline   # render all cases into baseline/
    python test/golden/golden.py candidate  # render into candidate/ and diff vs baseline/
"""

import sys
import os
import hashlib
import warnings

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))

from datachart.charts import (
    LineChart,
    BarChart,
    Histogram,
    ScatterChart,
    Heatmap,
    BoxPlot,
    ParallelCoords,
    PyramidChart,
    RadialChart,
)
from datachart.utils import OverlayChart, FigureGridLayout, Panel, Grid
from datachart.config import config
from datachart.constants import THEME

# Cases whose output intentionally changed since the last published baseline.
EXPECTED_CHANGES = {
    # theme renames: PUBLICATION -> INK (same style, new case name)
    "theme_ink_line",
    # new emphasis cases (ADR 0009)
    "emphasis_line_walks",
    "emphasis_line_walks_material",
    "emphasis_scatter_cohort",
    "emphasis_parallel_rows",
    "emphasis_parallel_composed",
    "emphasis_hist_reference",
    "emphasis_box_labels",
    "emphasis_panel_cross_type",
    # show_area now fills down to the axis floor instead of y=0
    "line_area_styled",
    # new horizontal panel cases (ADR 0012)
    "overlay_horizontal_bar_line_dual",
    "overlay_horizontal_bar_bar_line",
    # new radial chart cases (ADR 0015)
    "radial_line",
    "radial_line_area_donut",
    "radial_bar",
    "radial_bar_stacked",
    "radial_scatter",
    "radial_hist_rose",
    "radial_panel_two",
    "radial_grid_mixed",
    "radial_bar_tip_labels",
    "radial_line_values",
    # new pyramid chart cases (ADR 0017)
    "pyramid_basic",
    "pyramid_values_xmax",
    "pyramid_styled_ticks",
    "pyramid_grid_pair",
}


def _reset():
    np.random.seed(42)
    config.set_theme(THEME.DEFAULT)


LINE1 = [{"x": i, "y": i**2} for i in range(10)]
LINE2 = [{"x": i, "y": 5 * i + 3} for i in range(10)]
BAR1 = [{"label": c, "y": v} for c, v in zip("ABCDE", [10, 24, 17, 30, 22])]
BAR2 = [{"label": c, "y": v} for c, v in zip("ABCDE", [14, 18, 25, 12, 28])]
SCAT1 = [{"x": i, "y": 2 * i + ((i * 7) % 5) - 2} for i in range(20)]


def hist_data(n=200, mu=0.0, sigma=1.0):
    rng = np.random.RandomState(7)
    return [{"x": float(v)} for v in rng.randn(n) * sigma + mu]


CASES = {}


def case(fn):
    CASES[fn.__name__] = fn
    return fn


# ----- single charts -----


@case
def line_single():
    return LineChart(data=LINE1, title="Line", xlabel="x", ylabel="y")


@case
def line_multi():
    return LineChart(
        data=[LINE1, LINE2],
        subtitle=["sq", "lin"],
        show_legend=True,
        show_grid="both",
        title="Lines",
    )


@case
def line_multi_subplots():
    return LineChart(
        data=[LINE1, LINE2],
        subtitle=["sq", "lin"],
        subplots=True,
        max_cols=2,
        title="Line subplots",
    )


@case
def line_yerr():
    data = [{"x": i, "y": i * 2, "yerr": 1 + 0.3 * i} for i in range(10)]
    return LineChart(data=data, show_yerr=True)


@case
def line_area_styled():
    style = {"plot_line_color": "#aa3355", "plot_line_style": "--"}
    return LineChart(data=LINE1, show_area=True, style=style)


@case
def line_vlines_hlines():
    return LineChart(
        data=LINE1,
        vlines={"x": 4, "label": "v"},
        hlines={"y": 40, "label": "h"},
        show_legend=True,
    )


@case
def line_log():
    data = [{"x": i, "y": 10**i} for i in range(1, 6)]
    return LineChart(data=data, scaley="log")


@case
def line_ticks():
    return LineChart(
        data=LINE1,
        xticks=[0, 3, 6, 9],
        xticklabels=["a", "b", "c", "d"],
        xtickrotate=45,
    )


@case
def bar_single():
    return BarChart(data=BAR1, title="Bar", show_grid="y")


@case
def bar_multi_grouped():
    return BarChart(
        data=[BAR1, BAR2], subtitle=["s1", "s2"], show_legend=True, title="Grouped"
    )


@case
def bar_multi_subplots():
    return BarChart(data=[BAR1, BAR2], subtitle=["s1", "s2"], subplots=True, max_cols=2)


@case
def bar_horizontal():
    return BarChart(data=BAR1, orientation="horizontal")


@case
def bar_values():
    return BarChart(data=BAR1, show_values=True, value_format="{:.0f}")


@case
def bar_yerr_limits():
    data = [{"label": c, "y": v, "yerr": 2} for c, v in zip("ABC", [5, 9, 7])]
    return BarChart(data=data, show_yerr=True, ymin=0, ymax=12)


@case
def hist_single():
    return Histogram(data=hist_data(), num_bins=15)


@case
def hist_multi_stacked():
    return Histogram(
        data=[hist_data(150, 0.0), hist_data(150, 2.5)],
        subtitle=["a", "b"],
        num_bins=12,
        show_legend=True,
    )


@case
def hist_multi_subplots():
    return Histogram(
        data=[hist_data(150, 0.0), hist_data(150, 2.5)],
        subplots=True,
        max_cols=2,
        num_bins=12,
    )


@case
def hist_horizontal_density():
    return Histogram(
        data=hist_data(), orientation="horizontal", show_density=True, num_bins=10
    )


@case
def scatter_single():
    return ScatterChart(data=SCAT1, title="Scatter")


@case
def scatter_hue_size():
    data = [
        {"x": i, "y": (i * 3) % 11, "size": 10 + i, "hue": "grp" + str(i % 3)}
        for i in range(30)
    ]
    return ScatterChart(data=data, show_legend=True)


@case
def scatter_regression():
    return ScatterChart(
        data=SCAT1, show_regression=True, show_ci=True, show_correlation=True
    )


@case
def scatter_multi_subplots():
    return ScatterChart(data=[SCAT1, LINE1], subplots=True, max_cols=2)


@case
def heatmap_basic():
    data = [[(i * j) % 7 for j in range(5)] for i in range(4)]
    return Heatmap(data=data, show_heatmap_values=True, show_colorbars=True)


@case
def heatmap_multi():
    d1 = [[(i + j) % 4 for j in range(4)] for i in range(4)]
    d2 = [[(i * j) % 5 for j in range(4)] for i in range(4)]
    return Heatmap(data=[d1, d2], subtitle=["m1", "m2"], max_cols=2)


@case
def box_basic():
    rng = np.random.RandomState(3)
    data = [
        {"label": lab, "value": float(v)}
        for lab in ["A", "B", "C"]
        for v in rng.randn(30) + {"A": 0, "B": 2, "C": 1}[lab]
    ]
    return BoxPlot(data=data, show_outliers=True)


@case
def box_horizontal_notch():
    rng = np.random.RandomState(4)
    data = [
        {"label": lab, "value": float(v)}
        for lab in ["A", "B"]
        for v in rng.randn(40) + {"A": 0, "B": 3}[lab]
    ]
    return BoxPlot(data=data, orientation="horizontal", show_notch=True)


@case
def parallel_basic():
    rng = np.random.RandomState(5)
    data = [
        {
            "alpha": float(rng.rand() * 10),
            "beta": float(rng.rand() * 100),
            "cat": ["low", "mid", "high"][i % 3],
            "hue": "g" + str(i % 2),
        }
        for i in range(20)
    ]
    return ParallelCoords(
        data=data, dimensions=["alpha", "beta", "cat"], hue="hue", show_legend=True
    )


# ----- themes -----


@case
def theme_ink_line():
    config.set_theme(THEME.INK)
    return LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True)


@case
def theme_greyscale_bar():
    config.set_theme(THEME.GREYSCALE)
    return BarChart(data=[BAR1, BAR2], show_legend=True)


# ----- emphasis (ADR 0009) -----


def walk_data(seed, n=40):
    rng = np.random.RandomState(seed)
    return [{"x": i, "y": float(v)} for i, v in enumerate(np.cumsum(rng.randn(n)))]


def _emphasis_walks():
    walks = [walk_data(seed) for seed in range(6)]
    return LineChart(
        data=walks,
        subtitle=[f"run {i}" for i in range(6)],
        emphasis=["background"] * 3 + [None, "highlight", "background"],
        show_legend=True,
        title="One walk among many",
    )


@case
def emphasis_line_walks():
    return _emphasis_walks()


@case
def emphasis_line_walks_material():
    config.set_theme(THEME.MATERIAL)
    return _emphasis_walks()


@case
def emphasis_scatter_cohort():
    cohort = [{"x": i, "y": 2 * i + (i * 3) % 5} for i in range(25)]
    rest = [{"x": i, "y": i + (i * 7) % 9} for i in range(25)]
    return ScatterChart(
        data=[rest, cohort],
        subtitle=["all points", "cohort"],
        emphasis=["background", "highlight"],
        show_legend=True,
    )


@case
def emphasis_parallel_rows():
    rng = np.random.RandomState(11)
    data = [
        {
            "speed": float(rng.rand() * 10),
            "cost": float(rng.rand() * 100),
            "score": float(rng.rand()),
        }
        for _ in range(15)
    ]
    best = [2, 7]
    return ParallelCoords(
        data=data,
        dimensions=["speed", "cost", "score"],
        emphasis=["highlight" if i in best else "background" for i in range(len(data))],
        title="Best runs",
    )


@case
def emphasis_parallel_composed():
    rng = np.random.RandomState(13)
    ctx = [{"a": float(rng.rand() * 5), "b": float(rng.rand() * 20)} for _ in range(12)]
    runs = [{"a": float(2 + i), "b": float(60 + 5 * i)} for i in range(3)]
    f1 = ParallelCoords(data=ctx, dimensions=["a", "b"])
    f2 = ParallelCoords(data=runs, dimensions=["a", "b"])
    return Panel(
        [{"figure": f1, "emphasis": "background"}, {"figure": f2}],
        title="Composed parallel",
    )


@case
def emphasis_hist_reference():
    return Histogram(
        data=[hist_data(300, 0.5, 1.4), hist_data(150, 2.0, 0.8)],
        subtitle=["reference", "cohort"],
        emphasis=["background", None],
        num_bins=18,
        show_legend=True,
    )


@case
def emphasis_box_labels():
    rng = np.random.RandomState(9)
    data = [
        {"label": lab, "value": float(v)}
        for lab in "ABCD"
        for v in rng.randn(30) + {"A": 0, "B": 2, "C": 1, "D": 3}[lab]
    ]
    return BoxPlot(data=data, emphasis=["background", None, "highlight", "background"])


@case
def emphasis_panel_cross_type():
    fh = Histogram(data=hist_data(), num_bins=20, subtitle="observations")
    xs = np.linspace(-3, 3, 50)
    fl = LineChart(
        data=[{"x": float(x), "y": float(30 * np.exp(-x * x / 2))} for x in xs],
        subtitle="trend",
    )
    return Panel(
        [
            {"figure": fh, "emphasis": "background"},
            {"figure": fl, "emphasis": "highlight"},
        ],
        title="Trend over observations",
        show_legend=True,
    )


# ----- overlays -----


@case
def overlay_line_line():
    f1 = LineChart(data=LINE1, subtitle="sq")
    f2 = LineChart(data=LINE2, subtitle="lin")
    return OverlayChart(
        charts=[{"figure": f1}, {"figure": f2}], title="Two lines", show_legend=True
    )


@case
def overlay_line_bar_dual():
    fb = BarChart(
        data=[{"label": c, "y": v * 100} for c, v in zip("ABCD", [1, 2, 3, 2])]
    )
    fl = LineChart(data=[{"x": i, "y": i * 2} for i in range(4)])
    return OverlayChart(
        charts=[
            {"figure": fb, "y_axis": "left"},
            {"figure": fl, "y_axis": "right", "legend_label": "trend"},
        ],
        title="Dual",
        xlabel="cat",
        ylabel_left="count",
        ylabel_right="value",
        show_legend=True,
    )


@case
def overlay_auto_assign():
    fb = BarChart(data=[{"label": str(i), "y": i * 1000} for i in range(5)])
    fl = LineChart(data=[{"x": i, "y": i * 2} for i in range(5)])
    return OverlayChart(
        charts=[{"figure": fb}, {"figure": fl}], auto_secondary_axis=3.0
    )


@case
def overlay_nested_panel():
    fb = BarChart(
        data=[{"label": c, "y": v * 100} for c, v in zip("ABCD", [1, 2, 3, 2])]
    )
    fl = LineChart(data=[{"x": i, "y": i * 2} for i in range(4)])
    inner = Panel(
        [
            {"figure": fb, "y_axis": "left"},
            {"figure": fl, "y_axis": "right", "legend_label": "trend"},
        ]
    )
    f2 = LineChart(data=[{"x": i, "y": i * 3} for i in range(4)], subtitle="extra")
    return Panel(
        [inner, f2],
        title="Nested",
        ylabel_left="count",
        ylabel_right="value",
        show_legend=True,
    )


@case
def overlay_hist_line():
    fh = Histogram(data=hist_data(), num_bins=20)
    xs = np.linspace(-3, 3, 50)
    fl = LineChart(
        data=[{"x": float(x), "y": float(30 * np.exp(-x * x / 2))} for x in xs]
    )
    return OverlayChart(
        charts=[{"figure": fh, "y_axis": "left"}, {"figure": fl, "y_axis": "left"}],
        show_legend=True,
    )


@case
def overlay_zorder_grid():
    f1 = LineChart(data=LINE2, subtitle="l")
    f2 = ScatterChart(data=SCAT1, subtitle="s")
    return OverlayChart(
        charts=[{"figure": f1, "z_order": 3}, {"figure": f2, "z_order": 2}],
        show_grid="both",
        show_legend=True,
        ymin=0,
        ymax=60,
    )


@case
def overlay_theme_snapshot():
    config.set_theme(THEME.INK)
    f1 = LineChart(data=LINE1, subtitle="pub")
    config.set_theme(THEME.DEFAULT)
    f2 = LineChart(data=LINE2, subtitle="def")
    return OverlayChart(charts=[{"figure": f1}, {"figure": f2}], show_legend=True)


@case
def overlay_bar_bar():
    f1 = BarChart(data=BAR1, subtitle="s1")
    f2 = BarChart(data=BAR2, subtitle="s2")
    return OverlayChart(charts=[{"figure": f1}, {"figure": f2}], show_legend=True)


@case
def overlay_bar_bar_line():
    f1 = BarChart(data=BAR1, subtitle="s1")
    f2 = BarChart(data=BAR2, subtitle="s2")
    f3 = LineChart(data=[{"x": i, "y": 20} for i in range(5)], subtitle="ref")
    return OverlayChart(
        charts=[{"figure": f1}, {"figure": f2}, {"figure": f3}],
        bar_mode="stack",
        show_legend=True,
    )


@case
def overlay_horizontal_bar_line_dual():
    fb = BarChart(
        data=[{"label": c, "y": v * 100} for c, v in zip("ABCD", [1, 2, 3, 2])],
        orientation="horizontal",
        subtitle="count",
    )
    fl = LineChart(data=[{"x": i, "y": i * 2} for i in range(4)], subtitle="trend")
    return Panel(
        [{"figure": fb, "y_axis": "left"}, {"figure": fl, "y_axis": "right"}],
        title="Horizontal dual",
        xlabel="cat",
        ylabel_left="count",
        ylabel_right="value",
        ymin=0,
        ymin_right=0,
        show_legend=True,
    )


@case
def overlay_horizontal_bar_bar_line():
    f1 = BarChart(data=BAR1, orientation="horizontal", subtitle="s1")
    f2 = BarChart(data=BAR2, orientation="horizontal", subtitle="s2")
    f3 = LineChart(data=[{"x": i, "y": 20} for i in range(5)], subtitle="ref")
    return Panel([f1, f2, f3], bar_mode="stack", show_legend=True, show_grid="x")


@case
def overlay_hist_hist():
    f1 = Histogram(data=hist_data(150, 0.0), subtitle="a", num_bins=12)
    f2 = Histogram(data=hist_data(150, 2.0), subtitle="b", num_bins=12)
    return OverlayChart(charts=[{"figure": f1}, {"figure": f2}], show_legend=True)


# ----- grids -----


@case
def grid_uniform_mixed():
    f1 = LineChart(data=LINE1, subtitle="line")
    f2 = BarChart(data=BAR1, subtitle="bar")
    f3 = ScatterChart(data=SCAT1, subtitle="scatter")
    f4 = Histogram(data=hist_data(), subtitle="hist", num_bins=10)
    return FigureGridLayout(
        charts=[{"figure": f} for f in (f1, f2, f3, f4)],
        title="Grid",
        max_cols=2,
        figsize=(10, 8),
    )


@case
def grid_custom_layout():
    f1 = LineChart(data=LINE1)
    f2 = BarChart(data=BAR1)
    f3 = ScatterChart(data=SCAT1)
    return FigureGridLayout(
        charts=[
            {
                "figure": f1,
                "layout_spec": {"row": 0, "col": 0, "rowspan": 1, "colspan": 2},
            },
            {
                "figure": f2,
                "layout_spec": {"row": 1, "col": 0, "rowspan": 1, "colspan": 1},
            },
            {
                "figure": f3,
                "layout_spec": {"row": 1, "col": 1, "rowspan": 1, "colspan": 1},
            },
        ],
        title="Custom",
        figsize=(10, 8),
    )


@case
def grid_with_overlay():
    fb = BarChart(data=BAR1, title="Bar")
    fl = LineChart(data=LINE2, title="Line")
    fo = OverlayChart(
        charts=[{"figure": fb, "y_axis": "left"}, {"figure": fl, "y_axis": "right"}],
        title="Overlay",
        show_legend=True,
    )
    return FigureGridLayout(
        charts=[{"figure": fb}, {"figure": fl}, {"figure": fo}],
        title="Grid+Overlay",
        max_cols=2,
        figsize=(10, 8),
    )


@case
def grid_subplot_figure():
    f = LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], subplots=True, max_cols=2)
    g = BarChart(data=BAR1)
    return FigureGridLayout(
        charts=[{"figure": f}, {"figure": g}], max_cols=2, figsize=(10, 4)
    )


@case
def grid_nested_grid():
    f1 = LineChart(data=LINE1, subtitle="line")
    f2 = BarChart(data=BAR1, subtitle="bar")
    f3 = ScatterChart(data=SCAT1, subtitle="scatter")
    f4 = Histogram(data=hist_data(), subtitle="hist", num_bins=10)
    inner = Grid([[f1, f2], [f3]], title="Inner", sharex=True)
    return Grid([inner, f4], title="Nested", figsize=(12, 5))


@case
def grid_mixed_panel_and_grid():
    fb = BarChart(data=BAR1, title="Bar")
    fl = LineChart(data=LINE2, title="Line")
    panel = Panel([fb, fl], title="Panel", show_legend=True)
    grid_fig = Grid([LineChart(data=LINE1), ScatterChart(data=SCAT1)], title="Sub")
    return Grid([panel, grid_fig], figsize=(12, 5))


COMPASS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
RAD1 = [{"label": d, "y": v} for d, v in zip(COMPASS, [4, 7, 6, 3, 5, 8, 2, 6])]
RAD2 = [{"label": d, "y": v} for d, v in zip(COMPASS, [6, 3, 5, 7, 2, 4, 8, 3])]


def wind_directions(n=200):
    rng = np.random.RandomState(11)
    return [{"x": float(v % 360)} for v in rng.vonmises(np.pi / 4, 2, n) * 180 / np.pi]


@case
def radial_line():
    return RadialChart(
        data=[RAD1, RAD2], subtitle=["a", "b"], show_legend=True, title="Radar"
    )


@case
def radial_line_area_donut():
    return RadialChart(data=RAD1, show_area=True, innerradius=0.25, startangle="E")


@case
def radial_bar():
    return RadialChart(data=RAD1, type="bar", title="Circular bars", show_grid="both")


@case
def radial_bar_stacked():
    return RadialChart(
        data=[RAD1, RAD2],
        type="bar",
        bar_mode="stack",
        subtitle=["a", "b"],
        show_legend=True,
    )


@case
def radial_scatter():
    return RadialChart(data=RAD1, type="scatter", direction="counterclockwise")


@case
def radial_hist_rose():
    return RadialChart(data=wind_directions(), type="histogram", num_bins=16)


@case
def radial_bar_tip_labels():
    labels = [f"Set {i + 1}" for i in range(16)]
    rng = np.random.RandomState(5)
    s1 = [{"label": l, "y": int(v)} for l, v in zip(labels, rng.randint(20, 80, 16))]
    s2 = [{"label": l, "y": int(v)} for l, v in zip(labels, rng.randint(10, 60, 16))]
    return RadialChart(
        data=[s1, s2],
        type="bar",
        bar_mode="stack",
        show_tip_labels=True,
        show_border=False,
        innerradius=0.3,
        figsize=(7, 7),
    )


@case
def radial_line_values():
    return RadialChart(data=RAD1, show_values=True, value_format="%.0f")


@case
def radial_panel_two():
    f1 = RadialChart(data=RAD1, subtitle="a")
    f2 = RadialChart(data=RAD2, type="bar", subtitle="b")
    return Panel([f2, f1], title="Radial panel", show_legend=True)


@case
def radial_grid_mixed():
    fr = RadialChart(data=RAD1, type="bar", title="Rose")
    fl = LineChart(data=LINE1, title="Line")
    return Grid([fr, fl], max_cols=2, figsize=(10, 4))


def pyr_side(base, boom_age, boom_size, taper, phase):
    """A deterministic single-year age distribution: 80 bands per side."""
    return [
        {
            "label": str(age),
            "y": round(
                max(
                    base
                    - age * taper
                    + boom_size * np.exp(-((age - boom_age) ** 2) / 120)
                    + 55 * np.sin(age / 5.5 + phase),
                    40.0,
                ),
                1,
            ),
        }
        for age in range(80)
    ]


def pyr_bands(side, width=2):
    """Aggregate a single-year side into `width`-year bands."""
    return [
        {
            "label": f"{lo}-{lo + width - 1}",
            "y": round(sum(p["y"] for p in side[lo : lo + width]), 1),
        }
        for lo in range(0, len(side), width)
    ]


PYR1 = pyr_side(base=920, boom_age=31, boom_size=380, taper=6.5, phase=0.4)
PYR2 = pyr_side(base=860, boom_age=42, boom_size=430, taper=5.8, phase=2.1)


@case
def pyramid_basic():
    return PyramidChart(
        data=[PYR1, PYR2],
        subtitle=["Group A", "Group B"],
        title="Pyramid",
        xlabel="Residents",
        ylabel="Age",
        show_legend=True,
        yticks=list(range(0, 80, 10)),
    )


@case
def pyramid_values_xmax():
    return PyramidChart(
        data=[pyr_bands(PYR1), pyr_bands(PYR2)],
        show_values=True,
        value_format="%.0f",
        style={"plot_bar_value_fontsize": 6},
        xmax=2600,
        show_grid="x",
        figsize=(10, 8),
    )


@case
def pyramid_styled_ticks():
    styles = [{"plot_bar_hatch": "//"}, {"plot_bar_edge_color": "#222222"}]
    return PyramidChart(
        data=[pyr_bands(PYR1), pyr_bands(PYR2)],
        style=styles,
        xticks=[0, 1000, 2000],
        xticklabels=["0", "1k", "2k"],
    )


@case
def pyramid_grid_pair():
    fa = PyramidChart(
        data=[PYR1, PYR2],
        subtitle=["A", "B"],
        title="2010",
        yticks=list(range(0, 80, 10)),
    )
    fb = PyramidChart(
        data=[PYR2, PYR1],
        subtitle=["A", "B"],
        title="2020",
        yticks=list(range(0, 80, 10)),
    )
    return Grid([fa, fb], max_cols=2, figsize=(10, 4))


@case
def grid_theme_mutation():
    f1 = LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True)
    config.set_theme(THEME.GREYSCALE)
    grid = FigureGridLayout(charts=[{"figure": f1}], figsize=(6, 4))
    config.set_theme(THEME.DEFAULT)
    return grid


# ----- runner -----


def render_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    results = {}
    for name, fn in CASES.items():
        _reset()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                fig = fn()
                path = os.path.join(outdir, name + ".png")
                fig.savefig(path, dpi=100)
                results[name] = "ok"
            except Exception as e:  # keep going; report at the end
                results[name] = f"ERROR: {type(e).__name__}: {e}"
            finally:
                plt.close("all")
        _reset()
    return results


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def pixel_diff(p1, p2):
    a = plt.imread(p1)
    b = plt.imread(p2)
    if a.shape != b.shape:
        return -1.0
    return float((np.abs(a - b) > 1 / 255).any(axis=-1).mean())


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    outdir = os.path.join(HERE, mode)
    results = render_all(outdir)
    errors = {k: v for k, v in results.items() if v != "ok"}
    print(f"rendered {len(results) - len(errors)}/{len(results)} cases into {mode}/")
    for k, v in errors.items():
        print(f"  RENDER {k}: {v}")

    if mode == "candidate":
        base = os.path.join(HERE, "baseline")
        same, changed, expected = [], [], []
        for name in CASES:
            bp, cp = (os.path.join(d, name + ".png") for d in (base, outdir))
            if not (os.path.exists(bp) and os.path.exists(cp)):
                (expected if name in EXPECTED_CHANGES else changed).append(
                    (name, "missing file")
                )
                continue
            if sha(bp) == sha(cp):
                same.append(name)
            else:
                frac = pixel_diff(bp, cp)
                tag = f"{frac:.4%} px differ" if frac >= 0 else "size mismatch"
                (expected if name in EXPECTED_CHANGES else changed).append((name, tag))
        print(f"\nIDENTICAL: {len(same)}")
        print(f"EXPECTED CHANGES ({len(expected)}):")
        for n, t in expected:
            print(f"  ~ {n}: {t}")
        print(f"UNEXPECTED CHANGES ({len(changed)}):")
        for n, t in changed:
            print(f"  ! {n}: {t}")
        sys.exit(1 if changed or errors else 0)


if __name__ == "__main__":
    main()
