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
)
from datachart.utils import OverlayChart, FigureGridLayout, Panel, Grid
from datachart.config import config
from datachart.constants import THEME

# Cases whose output intentionally changed since the last published baseline.
EXPECTED_CHANGES = set()


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
def theme_publication_line():
    config.set_theme(THEME.PUBLICATION)
    return LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True)


@case
def theme_greyscale_bar():
    config.set_theme(THEME.GREYSCALE)
    return BarChart(data=[BAR1, BAR2], show_legend=True)


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
    config.set_theme(THEME.PUBLICATION)
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
                changed.append((name, "missing file"))
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
