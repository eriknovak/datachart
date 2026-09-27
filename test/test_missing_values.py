"""A missing value (None, NaN, inf) is not drawn, on every front (#325)."""

import unittest
import warnings
from datetime import date, timedelta

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

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
    ImageChart,
    LineChart,
    ParallelCoords,
    PyramidChart,
    RadialChart,
    RaincloudPlot,
    RidgelinePlot,
    ScatterChart,
    ScatterMatrix,
    StackedAreaChart,
    SwarmPlot,
    ViolinPlot,
)

MISSING = {"None": None, "NaN": float("nan"), "inf": float("inf")}
# the index of the record each case makes missing
HOLE = 2
DAY = date(2024, 1, 1)


def series(n=5):
    return [{"x": i, "y": float(i % 3 + 1)} for i in range(n)]


def bars():
    return [{"label": c, "y": float(i + 1)} for i, c in enumerate("abcde")]


def groups():
    return [
        {"label": label, "value": float(v)}
        for label in "ab"
        for v in (1, 2, 3, 5, 8, 4, 6)
    ]


def tasks():
    return [
        {
            "task": f"t{i}",
            "start": DAY + timedelta(days=i),
            "end": DAY + timedelta(days=i + 3),
        }
        for i in range(5)
    ]


def dumbbells():
    return [{"label": c, "start": i, "end": i + 2} for i, c in enumerate("abcde")]


def observations():
    return [{"x": float(v)} for v in (1, 2, 2, 3, 3, 3, 4, 5)]


def points():
    return [{"x": float(i), "y": float(i * 7 % 5)} for i in range(6)]


def rows():
    return [{"a": float(i), "b": float(5 - i), "c": float(i % 2)} for i in range(5)]


def holed(records, key, missing):
    records = [dict(record) for record in records]
    records[HOLE][key] = missing
    return records


def dropped(records):
    return records[:HOLE] + records[HOLE + 1 :]


def finite(values):
    values = np.asarray(values, dtype=float)
    return values[np.isfinite(values).all(axis=-1)] if values.ndim > 1 else values


def drawn(figure):
    """What the figure draws: its marks' finite geometry, texts, and ticks."""

    figure.canvas.draw()
    signature = []
    for ax in figure.axes:
        signature.append(
            (
                sorted(
                    tuple(np.round(p.get_bbox().bounds, 6))
                    for p in ax.patches
                    if isinstance(p, Rectangle)
                ),
                [np.round(finite(l.get_xydata()), 6).tolist() for l in ax.lines],
                [np.round(finite(c.get_offsets()), 6).tolist() for c in ax.collections],
                [t.get_text() for t in ax.texts],
                [t.get_text() for t in ax.get_xticklabels() + ax.get_yticklabels()],
            )
        )
    return signature


def line_has_a_break(figure):
    figure.canvas.draw()
    return any(
        np.isnan(np.asarray(line.get_ydata(), dtype=float)).any()
        for ax in figure.axes
        for line in ax.lines
    )


def area_has_a_break(figure):
    figure.canvas.draw()
    return any(len(c.get_paths()) > 1 for ax in figure.axes for c in ax.collections)


def drawn_bars(figure):
    figure.canvas.draw()
    return sum(
        np.isfinite([p.get_width(), p.get_height()]).all() and p.get_height() != 0
        for ax in figure.axes
        for p in ax.patches
        if isinstance(p, Rectangle)
    )


# front -> (records, value keys, position keys, value-hole check)
RECORD_FRONTS = {
    "LineChart": (LineChart, series, ["y"], ["x"], line_has_a_break),
    "StackedAreaChart": (StackedAreaChart, series, ["y"], ["x"], area_has_a_break),
    "BumpChart": (BumpChart, series, ["y"], ["x"], line_has_a_break),
    "BarChart": (BarChart, bars, ["y"], ["label"], lambda f: drawn_bars(f) == 4),
    "RadialChart": (RadialChart, bars, ["y"], ["label"], line_has_a_break),
    "GanttChart": (GanttChart, tasks, [], ["start", "end"], None),
    "DumbbellChart": (DumbbellChart, dumbbells, [], ["label", "start", "end"], None),
    "Histogram": (Histogram, observations, [], ["x"], None),
    "BoxPlot": (BoxPlot, groups, ["value"], ["label"], "dropped"),
    "ViolinPlot": (ViolinPlot, groups, ["value"], ["label"], "dropped"),
    "SwarmPlot": (SwarmPlot, groups, ["value"], ["label"], "dropped"),
    "RaincloudPlot": (RaincloudPlot, groups, ["value"], ["label"], "dropped"),
    "RidgelinePlot": (RidgelinePlot, groups, ["value"], ["label"], "dropped"),
    "ScatterChart": (ScatterChart, points, ["y"], ["x"], "dropped"),
    "ParallelCoords": (ParallelCoords, rows, ["b"], [], line_has_a_break),
    "ScatterMatrix": (ScatterMatrix, rows, ["b"], [], None),
}


def pyramid(data):
    return PyramidChart([data, bars()])


def grid(missing):
    return [[1, 2, 3], [4, missing, 6], [7, 8, 9]]


def calendar(missing):
    days = [DAY + timedelta(days=i) for i in range(5)]
    return {"date": days, "value": [1, 2, missing, 4, 5]}


def hexbin(missing):
    return {"x": [0, 1, missing, 3, 4], "y": [0, 1, 2, 1, 0]}


def masked_cell(figure, row, column):
    image = figure.axes[0].images[0].get_array()
    return bool(np.ma.getmaskarray(image)[row, column])


# front -> (data with one missing cell, check)
GRID_FRONTS = {
    "Heatmap": (
        lambda m: Heatmap({"z": grid(m)}, show_values=True),
        lambda f: masked_cell(f, 1, 1) and len(f.axes[0].texts) == 8,
    ),
    "ContourChart": (
        lambda m: ContourChart({"z": grid(m)}),
        lambda f: max(f.axes[0].collections[0].levels) <= 10,
    ),
    "HexbinChart": (
        lambda m: HexbinChart(hexbin(m), gridsize=3),
        lambda f: f.axes[0].collections[0].get_array().sum() == 4,
    ),
    "CalendarHeatmap": (
        lambda m: CalendarHeatmap(calendar(m)),
        lambda f: np.ma.count(f.axes[0].images[0].get_array()) == 4,
    ),
    "ImageChart": (
        lambda m: ImageChart({"image": grid(m), "extent": (0, 3, 0, 3)}),
        lambda f: masked_cell(f, 1, 1),
    ),
}


class MissingCase(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def quietly(self, draw):
        """The figure `draw` returns, drawn with every warning an error."""

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            figure = draw()
            figure.canvas.draw()
        return figure


class TestRecordFronts(MissingCase):
    def cases(self):
        for name, (front, records, values, positions, check) in RECORD_FRONTS.items():
            yield name, front, records(), values, positions, check
        yield "PyramidChart", pyramid, bars(), ["y"], ["label"], None

    def test_a_missing_value_is_not_drawn(self):
        for name, front, records, values, _, check in self.cases():
            for key in values:
                for label, missing in MISSING.items():
                    with self.subTest(front=name, key=key, missing=label):
                        figure = self.quietly(
                            lambda: front(holed(records, key, missing))
                        )
                        if check == "dropped":
                            self.assertEqual(
                                drawn(figure), drawn(front(dropped(records)))
                            )
                        elif check is not None:
                            self.assertTrue(check(figure))

    def test_a_missing_position_drops_the_record(self):
        for name, front, records, _, positions, _ in self.cases():
            for key in positions:
                for label, missing in MISSING.items():
                    with self.subTest(front=name, key=key, missing=label):
                        figure = self.quietly(
                            lambda: front(holed(records, key, missing))
                        )
                        self.assertEqual(drawn(figure), drawn(front(dropped(records))))

    def test_a_pyramid_side_draws_without_the_missing_bar(self):
        figure = self.quietly(lambda: pyramid(holed(bars(), "y", None)))
        self.assertEqual(drawn_bars(figure), 9)

    def test_a_missing_scatter_size_or_error_is_not_drawn(self):
        for key in ("size", "xerr", "yerr"):
            for label, missing in MISSING.items():
                with self.subTest(key=key, missing=label):
                    records = [
                        {**p, "size": 1.0, "xerr": 0.1, "yerr": 0.1} for p in points()
                    ]
                    self.quietly(lambda: ScatterChart(holed(records, key, missing)))

    def test_a_missing_value_has_no_value_label(self):
        figure = self.quietly(
            lambda: LineChart(holed(series(), "y", None), show_values=True)
        )
        self.assertEqual(len(figure.axes[0].texts), 4)

    def test_an_absent_key_still_raises(self):
        with self.assertRaisesRegex(ValueError, "record `data\\[0\\]` has no `y` key"):
            LineChart([{"x": 1}])


class TestGridFronts(MissingCase):
    def test_a_missing_cell_is_not_drawn(self):
        for name, (draw, check) in GRID_FRONTS.items():
            for label, missing in MISSING.items():
                with self.subTest(front=name, missing=label):
                    figure = self.quietly(lambda: draw(missing))
                    self.assertTrue(check(figure))


class TestEmptySeries(MissingCase):
    def test_every_value_missing_raises(self):
        cases = {
            "line": lambda: LineChart([{"x": 1, "y": None}, {"x": 2, "y": np.nan}]),
            "bar": lambda: BarChart([{"label": "a", "y": np.inf}]),
            "histogram": lambda: Histogram([{"x": None}, {"x": np.nan}]),
            "heatmap": lambda: Heatmap({"z": [[None, np.nan]]}),
            "subplots": lambda: LineChart(
                [[{"x": None, "y": 1}], [{"x": 1, "y": None}]], subplots=True
            ),
        }
        for name, draw in cases.items():
            with self.subTest(case=name):
                with self.assertRaisesRegex(ValueError, "has nothing to draw"):
                    draw()

    def test_an_empty_subplot_renders(self):
        cases = {
            "LineChart": (LineChart, series(), "y"),
            "StackedAreaChart": (StackedAreaChart, series(), "y"),
            "BarChart": (BarChart, bars(), "y"),
            "Histogram": (Histogram, observations(), "x"),
            "ScatterChart": (ScatterChart, points(), "y"),
            "SwarmPlot": (SwarmPlot, groups(), "value"),
            "RadialChart": (RadialChart, bars(), "y"),
            "DumbbellChart": (DumbbellChart, dumbbells(), "start"),
        }
        for name, (front, records, key) in cases.items():
            with self.subTest(front=name):
                empty = [{**record, key: None} for record in records]
                figure = self.quietly(lambda: front([empty, records], subplots=True))
                self.assertEqual(len(figure.axes), 2)
        for front in (Heatmap, ContourChart):
            with self.subTest(front=front.__name__):
                grids = [{"z": [[None, None], [None, None]]}, {"z": [[1, 2], [3, 4]]}]
                figure = self.quietly(lambda: front(grids, subplots=True))
                ax = figure.axes[0]
                drawn_cells = sum(np.ma.count(image.get_array()) for image in ax.images)
                self.assertEqual(drawn_cells + len(ax.collections), 0)

    def test_a_missing_bar_adds_nothing_to_a_stack(self):
        below = [{"label": "a", "y": None}, {"label": "b", "y": 1}]
        above = [{"label": "a", "y": 2}, {"label": "b", "y": 1}]
        figure = self.quietly(lambda: BarChart([below, above], bar_mode="stack"))
        bottoms = [p.get_y() for p in figure.axes[0].patches]
        self.assertEqual(bottoms, [0, 0, 0, 1])

    def test_an_empty_series_keeps_its_legend_entry(self):
        empty = [{**record, "y": None} for record in series()]
        figure = self.quietly(
            lambda: LineChart(
                [empty, series()], subtitle=["empty", "full"], show_legend=True
            )
        )
        legend = figure.axes[0].get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["empty", "full"])


class TestAxes(MissingCase):
    def test_a_column_mixing_dates_and_numbers_raises(self):
        with self.assertRaisesRegex(ValueError, "Cannot mix temporal and numeric"):
            LineChart([{"x": 1, "y": 1}, {"x": date(2020, 1, 1), "y": 2}])

    def test_a_single_point_draws_without_a_warning(self):
        cases = {
            "line": (lambda: LineChart([{"x": 1, "y": 1}]), "x", (0.95, 1.05)),
            "zero": (lambda: ScatterChart([{"x": 0, "y": 3}]), "x", (-0.5, 0.5)),
            "bar": (lambda: BarChart([{"label": "a", "y": 0}]), "y", (-0.5, 0.5)),
            "date": (lambda: LineChart([{"x": DAY, "y": 3}]), "x", None),
        }
        for name, (draw, axis, limits) in cases.items():
            with self.subTest(case=name):
                ax = self.quietly(draw).axes[0]
                lo, hi = ax.get_xlim() if axis == "x" else ax.get_ylim()
                self.assertLess(lo, hi)
                if limits is not None:
                    self.assertLessEqual(lo, limits[0])
                    self.assertGreaterEqual(hi, limits[1])

    def test_a_single_date_pads_a_day(self):
        ax = self.quietly(lambda: LineChart([{"x": DAY, "y": 3}])).axes[0]
        lo, hi = ax.get_xlim()
        self.assertAlmostEqual(hi - lo, 2.0)


if __name__ == "__main__":
    unittest.main()
