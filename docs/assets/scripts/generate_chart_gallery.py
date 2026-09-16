"""Generates docs/assets/imgs/gallery-*.png — one figure per chart type for
the gallery cards of the charts index, and one per composition utility for
the cards of the utilities index.

Each figure is a small but realistic chart, with several series, a legend
where the chart has one, and the axes labelled, so a reader can tell from the
card alone what the chart is for.

Run from the repo root: python docs/assets/scripts/generate_chart_gallery.py
"""

import pathlib
import sys
from datetime import date, timedelta

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.utils import Annotate, Grid, Panel
from datachart.charts import (
    BarChart,
    BoxPlot,
    BumpChart,
    CalendarHeatmap,
    ContourChart,
    DumbbellChart,
    GanttChart,
    Heatmap,
    HexbinChart,
    Histogram,
    LineChart,
    NetworkChart,
    ParallelCoords,
    PyramidChart,
    RadialChart,
    RaincloudPlot,
    RidgelinePlot,
    SankeyChart,
    ScatterChart,
    ScatterMatrix,
    StackedAreaChart,
    SwarmPlot,
    Treemap,
    ViolinPlot,
)

OUT = pathlib.Path(__file__).resolve().parents[1] / "imgs"
FIGSIZE = (4.8, 3.2)
DPI = 150

rng = np.random.default_rng(11)
YEARS = list(range(2016, 2025))
GROUPS = {
    "Control": rng.normal(50, 8, 60),
    "Low dose": rng.normal(55, 9, 60),
    "High dose": rng.normal(63, 11, 60),
}
GROUP_DATA = [
    {"label": name, "value": round(float(v), 1)}
    for name, values in GROUPS.items()
    for v in values
]


def _series(x, ys):
    return [[{"x": i, "y": v} for i, v in zip(x, y)] for y in ys]


def line():
    return LineChart(
        data=_series(
            YEARS,
            [
                [12, 15, 14, 19, 23, 21, 26, 30, 29],
                [8, 9, 13, 12, 15, 18, 17, 21, 24],
                [5, 6, 6, 8, 9, 12, 14, 13, 17],
            ],
        ),
        subtitle=["Web", "Mobile", "API"],
        show_legend=True,
        xlabel="Year",
        ylabel="Signups (k)",
        figsize=FIGSIZE,
    )


def stackedarea():
    return StackedAreaChart(
        data=_series(
            YEARS,
            [
                [30, 31, 29, 27, 24, 22, 20, 18, 16],
                [10, 12, 15, 19, 24, 28, 31, 35, 38],
                [2, 3, 4, 6, 8, 10, 13, 15, 18],
            ],
        ),
        subtitle=["Desktop", "Mobile", "Tablet"],
        show_legend=True,
        xlabel="Year",
        ylabel="Visits (M)",
        figsize=FIGSIZE,
    )


def bump():
    seasons = list(range(2020, 2025))
    return BumpChart(
        data=_series(
            seasons,
            [
                [71, 64, 80, 78, 69],
                [68, 75, 77, 81, 84],
                [59, 70, 62, 66, 72],
                [63, 61, 58, 70, 66],
            ],
        ),
        subtitle=["Ljubljana", "Maribor", "Celje", "Koper"],
        xlabel="Season",
        ylabel="Rank",
        figsize=FIGSIZE,
    )


def bar():
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    return BarChart(
        data=[
            [{"label": q, "y": y} for q, y in zip(quarters, ys)]
            for ys in ([12, 19, 15, 22], [9, 14, 18, 16], [7, 11, 13, 20])
        ],
        subtitle=["North", "South", "West"],
        show_legend=True,
        xlabel="Quarter",
        ylabel="Revenue (M€)",
        figsize=FIGSIZE,
    )


def pyramid():
    ages = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"]
    return PyramidChart(
        data=[
            [{"label": a, "y": v} for a, v in zip(ages, ys)]
            for ys in ([9, 10, 12, 14, 13, 12, 9, 7], [8, 9, 11, 13, 13, 12, 10, 10])
        ],
        subtitle=["Men", "Women"],
        show_legend=True,
        xlabel="Population (%)",
        figsize=FIGSIZE,
    )


def radial():
    metrics = ["Speed", "Range", "Comfort", "Safety", "Price", "Space"]
    return RadialChart(
        data=[
            [{"label": m, "y": v} for m, v in zip(metrics, ys)]
            for ys in ([8, 6, 7, 9, 4, 6], [5, 9, 8, 7, 8, 9])
        ],
        type="line",
        show_area=True,
        subtitle=["Sport", "Family"],
        show_legend=True,
        legend={"location": "outside right"},
        figsize=FIGSIZE,
    )


def calendarheatmap():
    days = [date(2024, 1, 1) + timedelta(days=i) for i in range(105)]
    weekday_load = np.array([6, 7, 7, 6, 5, 1, 1])
    values = [int(rng.poisson(weekday_load[d.weekday()])) for d in days]
    return CalendarHeatmap(
        data={"date": days, "value": values}, subtitle="Commits", figsize=FIGSIZE
    )


def gantt():
    d = date(2024, 1, 1)
    return GanttChart(
        data=[
            {
                "task": "Research",
                "start": d,
                "end": d + timedelta(14),
                "group": "Plan",
                "progress": 1.0,
            },
            {
                "task": "Design",
                "start": d + timedelta(10),
                "end": d + timedelta(28),
                "group": "Plan",
                "progress": 0.8,
            },
            {
                "task": "Build",
                "start": d + timedelta(28),
                "end": d + timedelta(63),
                "group": "Make",
                "progress": 0.4,
                "depends_on": ["Design"],
            },
            {
                "task": "Test",
                "start": d + timedelta(56),
                "end": d + timedelta(77),
                "group": "Make",
                "depends_on": ["Build"],
            },
            {
                "task": "Release",
                "start": d + timedelta(77),
                "end": d + timedelta(77),
                "group": "Make",
            },
        ],
        show_dependencies=True,
        figsize=FIGSIZE,
    )


def dumbbell():
    return DumbbellChart(
        data=[
            {"label": "Norway", "start": 79.8, "end": 83.2},
            {"label": "Chile", "start": 77.1, "end": 81.2},
            {"label": "Brazil", "start": 70.2, "end": 75.9},
            {"label": "India", "start": 62.5, "end": 70.9},
            {"label": "Nigeria", "start": 46.3, "end": 54.7},
        ],
        start_name="2000",
        end_name="2019",
        show_legend=True,
        xlabel="Life expectancy (years)",
        figsize=FIGSIZE,
    )


def histogram():
    return Histogram(
        data=[
            [{"x": round(float(v), 1)} for v in rng.normal(68, 10, 400)],
            [{"x": round(float(v), 1)} for v in rng.normal(76, 8, 400)],
        ],
        subtitle=["Before", "After"],
        show_legend=True,
        num_bins=24,
        xlabel="Score",
        ylabel="Students",
        figsize=FIGSIZE,
    )


def box():
    return BoxPlot(data=GROUP_DATA, xlabel="Group", ylabel="Response", figsize=FIGSIZE)


def violin():
    return ViolinPlot(
        data=GROUP_DATA, xlabel="Group", ylabel="Response", figsize=FIGSIZE
    )


def swarm():
    return SwarmPlot(
        data=GROUP_DATA, xlabel="Group", ylabel="Response", figsize=FIGSIZE
    )


def raincloud():
    return RaincloudPlot(
        data=GROUP_DATA, xlabel="Group", ylabel="Response", figsize=FIGSIZE
    )


def ridgeline():
    months = ["Jan", "Mar", "May", "Jul", "Sep", "Nov"]
    means = [2, 6, 13, 21, 15, 6]
    return RidgelinePlot(
        data=[
            {"label": m, "value": round(float(v), 1)}
            for m, mu in zip(months, means)
            for v in rng.normal(mu, 3.5, 80)
        ],
        xlabel="Temperature (°C)",
        figsize=FIGSIZE,
    )


def scatter():
    engine = rng.uniform(1, 5, 60)
    mpg = 48 - 6 * engine + rng.normal(0, 3, 60)
    return ScatterChart(
        data=[
            {
                "x": round(float(x), 2),
                "y": round(float(y), 1),
                "hue": "SUV" if x > 3 else "Sedan",
            }
            for x, y in zip(engine, mpg)
        ],
        show_regression=True,
        show_legend=True,
        xlabel="Engine (L)",
        ylabel="Efficiency (mpg)",
        figsize=FIGSIZE,
    )


def heatmap():
    features = ["Age", "Income", "Spend", "Visits", "Tenure"]
    corr = np.corrcoef(rng.normal(size=(5, 200)) + np.arange(5)[:, None] * 0.0)
    corr = np.round((corr + rng.uniform(-0.3, 0.9, (5, 5))).clip(-1, 1), 2)
    corr = np.triu(corr) + np.triu(corr, 1).T
    np.fill_diagonal(corr, 1.0)
    return Heatmap(
        data={"x": features, "y": features, "z": corr.tolist()},
        show_heatmap_values=True,
        figsize=FIGSIZE,
    )


def contour():
    x = y = np.linspace(-3, 3, 60)
    xx, yy = np.meshgrid(x, y)
    z = np.exp(-((xx - 1) ** 2 + yy**2)) + 0.7 * np.exp(
        -((xx + 1.2) ** 2 + (yy - 0.8) ** 2) / 1.5
    )
    return ContourChart(
        data={"x": x.tolist(), "y": y.tolist(), "z": z.tolist()},
        filled=True,
        xlabel="x",
        ylabel="y",
        figsize=FIGSIZE,
    )


def hexbin():
    a = rng.multivariate_normal([0, 0], [[1, 0.6], [0.6, 1]], 2500)
    b = rng.multivariate_normal([2.5, -1.5], [[0.4, 0], [0, 0.4]], 800)
    xy = np.vstack([a, b])
    return HexbinChart(
        data={"x": xy[:, 0].tolist(), "y": xy[:, 1].tolist()},
        gridsize=22,
        xlabel="x",
        ylabel="y",
        figsize=FIGSIZE,
    )


def parallelcoords():
    classes = ["Compact", "Sedan", "SUV", "Sport"]
    base = {
        "Compact": (22, 430, 5, 6.2),
        "Sedan": (34, 520, 5, 7.1),
        "SUV": (47, 470, 7, 9.4),
        "Sport": (65, 590, 4, 4.8),
    }
    return ParallelCoords(
        data=[
            {
                "Price": round(p + rng.normal(0, 3), 1),
                "Range": round(r + rng.normal(0, 25)),
                "Seats": s,
                "0-100": round(a + rng.normal(0, 0.4), 1),
                "Class": c,
            }
            for c in classes
            for _ in range(4)
            for p, r, s, a in [base[c]]
        ],
        dimensions=["Price", "Range", "Seats", "0-100"],
        hue="Class",
        figsize=FIGSIZE,
    )


def network():
    nodes = {
        "core": "Platform",
        "auth": "Platform",
        "db": "Platform",
        "web": "Clients",
        "ios": "Clients",
        "android": "Clients",
        "billing": "Services",
        "mail": "Services",
        "search": "Services",
    }
    edges = [
        ("web", "core", 5),
        ("ios", "core", 3),
        ("android", "core", 3),
        ("core", "auth", 4),
        ("core", "db", 6),
        ("auth", "db", 2),
        ("core", "billing", 2),
        ("billing", "mail", 1),
        ("core", "search", 3),
        ("search", "db", 2),
        ("web", "search", 1),
    ]
    return NetworkChart(
        data={
            "nodes": [{"id": n, "group": g} for n, g in nodes.items()],
            "edges": [{"source": s, "target": t, "weight": w} for s, t, w in edges],
        },
        show_legend=True,
        seed=4,
        figsize=FIGSIZE,
    )


def scattermatrix():
    n = 40
    species = [["setosa", "virginica"][i % 2] for i in range(n)]
    shift = np.array([0 if s == "setosa" else 1.5 for s in species])
    return ScatterMatrix(
        data={
            "length": (rng.normal(5, 0.4, n) + shift).round(1).tolist(),
            "width": (rng.normal(3.4, 0.3, n) - shift / 3).round(1).tolist(),
            "petal": (rng.normal(1.5, 0.3, n) + 2.5 * shift).round(1).tolist(),
            "species": species,
        },
        hue="species",
        figsize=(4.8, 4.2),
    )


def sankey():
    return SankeyChart(
        data={
            "links": [
                {"source": "Ads", "target": "Visited", "value": 420},
                {"source": "Search", "target": "Visited", "value": 380},
                {"source": "Referral", "target": "Visited", "value": 200},
                {"source": "Visited", "target": "Signed up", "value": 310},
                {"source": "Visited", "target": "Bounced", "value": 690},
                {"source": "Signed up", "target": "Paid", "value": 95},
                {"source": "Signed up", "target": "Free tier", "value": 215},
            ]
        },
        figsize=FIGSIZE,
    )


def treemap():
    return Treemap(
        data={
            "data": [
                {
                    "label": "Asia",
                    "children": [
                        {"label": "India", "value": 1429},
                        {"label": "China", "value": 1426},
                        {"label": "Indonesia", "value": 278},
                        {"label": "Pakistan", "value": 240},
                    ],
                },
                {
                    "label": "Africa",
                    "children": [
                        {"label": "Nigeria", "value": 224},
                        {"label": "Ethiopia", "value": 127},
                        {"label": "Other", "value": 1109},
                    ],
                },
                {"label": "Europe", "value": 742},
                {
                    "label": "Americas",
                    "children": [
                        {"label": "USA", "value": 340},
                        {"label": "Brazil", "value": 216},
                        {"label": "Other", "value": 484},
                    ],
                },
            ]
        },
        show_values=True,
        figsize=FIGSIZE,
    )


def panel():
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    revenue = BarChart(
        data=[{"label": q, "y": y} for q, y in zip(quarters, [12, 19, 15, 22])],
        subtitle="Revenue (M€)",
    )
    margin = LineChart(
        data=[{"x": q, "y": y} for q, y in zip(quarters, [18, 24, 21, 27])],
        subtitle="Margin (%)",
    )
    return Panel(
        [revenue, {"figure": margin, "y_axis": "right"}],
        xlabel="Quarter",
        ylabel_left="Revenue (M€)",
        ylabel_right="Margin (%)",
        show_legend=True,
        figsize=FIGSIZE,
    )


def grid():
    return Grid(
        [[line(), bar()], [scatter(), box()]],
        figsize=(FIGSIZE[0], FIGSIZE[1] * 1.15),
    )


def annotate():
    years = list(range(2016, 2025))
    values = [12, 15, 14, 19, 23, 21, 26, 30, 29]
    figure = LineChart(
        data=_series(years, [values]),
        xlabel="Year",
        ylabel="Signups (k)",
        figsize=FIGSIZE,
    )
    return Annotate(
        figure,
        [
            {"text": "Record year", "x": 2020.4, "y": 31.5, "target": (2023, 30)},
            {"text": "Pricing change", "x": 2017.2, "y": 25, "target": (2019, 19)},
        ],
    )


UTILITIES = (panel, grid, annotate)

CHARTS = (
    line,
    stackedarea,
    bump,
    bar,
    pyramid,
    radial,
    calendarheatmap,
    gantt,
    dumbbell,
    histogram,
    box,
    violin,
    swarm,
    raincloud,
    ridgeline,
    scatter,
    heatmap,
    contour,
    hexbin,
    parallelcoords,
    network,
    scattermatrix,
    sankey,
    treemap,
)


def main():
    for chart in CHARTS + UTILITIES:
        figure = chart()
        path = OUT / f"gallery-{chart.__name__}.png"
        figure.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
        plt.close("all")
        print(path.name)


if __name__ == "__main__":
    main()
