"""Valid or near-valid inputs render or raise the library's ValueError (#305)."""

import datetime
import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from datachart.charts import (
    BoxPlot,
    CalendarHeatmap,
    ContourChart,
    Heatmap,
    HexbinChart,
    Histogram,
    LineChart,
    NetworkChart,
    RaincloudPlot,
    RidgelinePlot,
    SankeyChart,
    ScatterChart,
    SwarmPlot,
    Treemap,
    ViolinPlot,
)
from datachart.config import config
from datachart.constants import THEME

NAN = float("nan")
Z = {"z": [[1, 2], [3, 4]]}
RECORDS = [{"a": 1, "b": 2, "c": "u"}, {"a": 2, "b": 3, "c": "v"}]


def group(values, label="a"):
    return [{"label": label, "value": v} for v in values]


def texts(figure):
    return [t.get_text() for ax in figure.axes for t in ax.texts]


class ValidInputCase(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")


class TestQuillHeatmapEmphasis(ValidInputCase):
    def test_rule_renders_under_quill(self):
        with config.using_theme(THEME.QUILL):
            figure = Heatmap(Z, emphasis_rule={"above": 2})
            figure.canvas.draw()


class TestNanValues(ValidInputCase):
    def test_violin_drops_nan(self):
        figure = ViolinPlot(group([1, 2, NAN, 3, 4]), inner="box")
        figure.canvas.draw()

    def test_histogram_drops_nan(self):
        with_nan = Histogram([{"x": [1, 2, NAN, 3]}])
        without = Histogram([{"x": [1, 2, 3]}])
        heights = [
            [p.get_height() for p in f.axes[0].patches] for f in (with_nan, without)
        ]
        self.assertEqual(heights[0], heights[1])

    def test_histogram_of_nan_alone_raises(self):
        with self.assertRaisesRegex(ValueError, "histogram `s` has no finite"):
            Histogram([{"x": [NAN, NAN]}], subtitle="s")

    def test_scatter_fit_leaves_out_a_nan_point(self):
        points = [
            {"x": 1, "y": 1},
            {"x": 2, "y": NAN},
            {"x": 3, "y": 2},
            {"x": 4, "y": 5},
        ]
        kept = [p for p in points if not np.isnan(p["y"])]
        figures = [
            ScatterChart(d, show_regression=True, show_correlation=True)
            for d in (points, kept)
        ]
        self.assertEqual(texts(figures[0]), texts(figures[1]))
        self.assertTrue(texts(figures[0])[0].startswith("r = "))
        self.assertNotIn("nan", texts(figures[0])[0])

    def test_value_labels_skip_nan(self):
        for front in (BoxPlot, SwarmPlot, RaincloudPlot):
            with self.subTest(front=front.__name__):
                with_nan = front(group([1, 2, NAN, 3, 4]), show_values=True)
                without = front(group([1, 2, 3, 4]), show_values=True)
                labels = texts(with_nan)
                self.assertTrue(labels)
                self.assertFalse(any("nan" in t for t in labels))
                self.assertEqual(labels, texts(without))
                lines = [
                    [line.get_xydata().tolist() for line in f.axes[0].lines]
                    for f in (with_nan, without)
                ]
                self.assertEqual(lines[0], lines[1])

    def test_group_of_nan_alone_raises(self):
        data = group([NAN, NAN], "b") + group([1, 2, 3])
        for front in (BoxPlot, ViolinPlot, SwarmPlot, RaincloudPlot, RidgelinePlot):
            with self.subTest(front=front.__name__):
                with self.assertRaisesRegex(ValueError, "group `b` has no finite"):
                    front(data)

    def test_contour_of_nan_alone_raises(self):
        for levels in ("rice", "fd", "auto", 5):
            with self.subTest(levels=levels):
                with self.assertRaisesRegex(ValueError, "`z` grid has no finite"):
                    ContourChart({"z": [[NAN, NAN], [NAN, NAN]]}, levels=levels)


class TestConstantGroups(ValidInputCase):
    def test_violin_draws_a_flat_line(self):
        figure = ViolinPlot(group([2, 2, 2, 2]), inner="quartiles")
        ax = figure.axes[0]
        (body,) = ax.collections
        ys = body.get_paths()[0].vertices[:, 1]
        self.assertTrue(np.allclose(ys, 2))
        # the quartile marks collapse onto the value
        self.assertTrue(all(np.allclose(line.get_ydata(), 2) for line in ax.lines))

    def test_ridge_draws_a_line_at_the_value(self):
        figure = RidgelinePlot(group([2, 2, 2, 2]) + group([1, 2, 3, 4], "b"))
        spikes = [
            line
            for line in figure.axes[0].lines
            if np.allclose(line.get_xdata(), 2) and len(line.get_xdata()) == 2
        ]
        self.assertEqual(len(spikes), 1)


class TestOneElementLists(ValidInputCase):
    def test_unwraps_with_one_dataset(self):
        cases = {
            "vmin": lambda: Heatmap(Z, vmin=[0]),
            "norm": lambda: Heatmap(Z, norm=["log"]),
            "value_format": lambda: Heatmap(
                Z, show_values=True, value_format=["{x:.1f}"]
            ),
            "grid_size": lambda: HexbinChart(
                {"x": list(range(20)), "y": [i % 3 for i in range(20)]},
                grid_size=[5],
            ),
            "x": lambda: LineChart(RECORDS, x=["a"], y="b"),
            "hue": lambda: ScatterChart(RECORDS, x="a", y="b", hue=["c"]),
        }
        for name, draw in cases.items():
            with self.subTest(setting=name):
                draw()

    def test_unwrapped_value_applies(self):
        figure = Heatmap(Z, show_values=True, value_format=["{x:.1f}"])
        self.assertIn("1.0", texts(figure))


class TestEmptyData(ValidInputCase):
    def test_renders_an_empty_panel(self):
        for front in (CalendarHeatmap, NetworkChart, SankeyChart, Treemap):
            with self.subTest(front=front.__name__):
                figure = front([])
                figure.canvas.draw()
                self.assertEqual(len(figure.axes), 1)
                self.assertFalse(figure.axes[0].has_data())

    def test_calendar_takes_a_flat_list_of_records(self):
        days = [datetime.date(2024, 1, 1), datetime.date(2024, 1, 2)]
        records = [{"date": d, "value": v} for d, v in zip(days, (1, 2))]
        columns = {"date": days, "value": [1, 2]}
        figures = [CalendarHeatmap(d) for d in (records, columns)]
        self.assertEqual(len(figures[0].axes), len(figures[1].axes))


if __name__ == "__main__":
    unittest.main()
