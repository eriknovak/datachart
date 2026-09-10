"""Value labels are one cross-chart feature with per-geometry placement (ADR 0033)."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.text import Annotation

from datachart.charts import (
    BarChart,
    BoxPlot,
    Histogram,
    LineChart,
    ScatterChart,
    StackedAreaChart,
    ViolinPlot,
)
from datachart.config import config
from datachart.constants import ORIENTATION, THEME, VALUE_FORMAT
from datachart.themes import DEFAULT_THEME
from datachart.utils import Grid, Panel

LINE = [{"x": i, "y": float(v)} for i, v in enumerate([1, 3, 2, 5, 4])]
LONG_LINE = [{"x": i, "y": float(i % 7)} for i in range(200)]
SCATTER = [{"x": 1, "y": 2.0}, {"x": 4, "y": 6.0}, {"x": 9, "y": 3.0}]
NAMED = [{"x": p["x"], "y": p["y"], "name": f"p{i}"} for i, p in enumerate(SCATTER)]
BAR = [{"label": c, "y": v} for c, v in zip("ABC", [3.0, 5.0, 4.0])]
# num_bins=3 over 0.5-2.5 gives counts [4, 0, 2]: the middle bin is empty
HIST = [{"x": v} for v in [0.5] * 4 + [2.5] * 2]
STACK = [
    [{"x": i, "y": float(v)} for i, v in enumerate([1, 2, 3])],
    [{"x": i, "y": float(v)} for i, v in enumerate([4, 5, 6])],
]
GROUPS = [
    {"label": lab, "value": float(v)}
    for lab, values in {"A": [1, 2, 3, 4, 5], "B": [10, 20, 30]}.items()
    for v in values
]


def labels(ax):
    """The value labels drawn into `ax`, in draw order."""

    return [t for t in ax.texts if isinstance(t, Annotation) and t.get_text()]


def texts(ax):
    return [t.get_text() for t in labels(ax)]


class ValueLabelCase(unittest.TestCase):
    def setUp(self):
        config.reset_config()

    def tearDown(self):
        config.reset_config()
        plt.close("all")


class TestStyleFamily(ValueLabelCase):
    def test_theme_base_defines_the_shared_family(self):
        for key in ("plot_value_fontsize", "plot_value_color", "plot_value_padding"):
            self.assertIn(key, DEFAULT_THEME)
        self.assertNotIn("plot_bar_value_fontsize", DEFAULT_THEME)

    def test_bar_value_keys_alias_the_family_in_config(self):
        config.update_config({"plot_bar_value_fontsize": 13})
        self.assertEqual(config["plot_value_fontsize"], 13)
        self.assertEqual(config["plot_bar_value_fontsize"], 13)
        self.assertEqual(config.get("plot_bar_value_fontsize"), 13)

    def test_registered_theme_with_alias_keys(self):
        config.register_theme("aliased", {"plot_bar_value_color": "#123456"})
        config.set_theme("aliased")
        self.assertEqual(config["plot_value_color"], "#123456")
        figure = BarChart(BAR, show_values=True)
        self.assertEqual(labels(figure.axes[0])[0].get_color(), "#123456")

    def test_chart_style_accepts_both_names(self):
        old = BarChart(BAR, show_values=True, style={"plot_bar_value_fontsize": 15})
        new = LineChart(LINE, show_values=True, style={"plot_value_fontsize": 15})
        self.assertEqual(labels(old.axes[0])[0].get_fontsize(), 15)
        self.assertEqual(labels(new.axes[0])[0].get_fontsize(), 15)


class TestFronts(ValueLabelCase):
    def test_line_labels_every_point_with_its_value(self):
        figure = LineChart(LINE, show_values=True)
        self.assertEqual(texts(figure.axes[0]), ["1", "3", "2", "5", "4"])

    def test_value_format_applies(self):
        figure = LineChart(LINE, show_values=True, value_format=VALUE_FORMAT.DECIMAL)
        self.assertEqual(texts(figure.axes[0])[0], "1.0")
        figure = LineChart(LINE, show_values=True, value_format="{:.0f}%")
        self.assertEqual(texts(figure.axes[0])[0], "1%")

    def test_line_labels_sit_above_or_below_only(self):
        figure = LineChart(LINE, show_values=True)
        placed = labels(figure.axes[0])
        for label in placed:
            self.assertEqual(label.xyann[0], 0.0)
            self.assertNotEqual(label.xyann[1], 0.0)
        # only the end labels hang inward from the axes edge
        for label in placed[1:-1]:
            self.assertEqual(label.get_ha(), "center")

    def test_scatter_labels_the_y_value(self):
        figure = ScatterChart(SCATTER, show_values=True)
        self.assertEqual(texts(figure.axes[0]), ["2", "6", "3"])

    def test_scatter_label_and_show_values_are_exclusive(self):
        with self.assertRaises(ValueError):
            ScatterChart(NAMED, label="name", show_values=True)

    def test_value_step_labels_every_nth_point(self):
        figure = LineChart(LONG_LINE, show_values=True, value_step=50)
        self.assertEqual(texts(figure.axes[0]), ["0", "1", "2", "3"])
        figure = ScatterChart(LONG_LINE, show_values=True, value_step=100)
        self.assertEqual(len(labels(figure.axes[0])), 2)

    def test_default_step_keeps_a_dense_series_readable(self):
        figure = LineChart(LONG_LINE, show_values=True)
        self.assertLess(len(labels(figure.axes[0])), 60)
        self.assertGreater(len(labels(figure.axes[0])), 5)

    def test_histogram_labels_bin_counts(self):
        figure = Histogram(HIST, num_bins=3, show_values=True)
        self.assertEqual(texts(figure.axes[0]), ["4", "2"])

    def test_histogram_step_and_horizontal(self):
        step = Histogram(
            HIST, num_bins=3, show_values=True, style={"plot_hist_type": "step"}
        )
        self.assertEqual(texts(step.axes[0]), ["4", "2"])
        horizontal = Histogram(
            HIST, num_bins=3, show_values=True, orientation=ORIENTATION.HORIZONTAL
        )
        self.assertEqual(texts(horizontal.axes[0]), ["4", "2"])

    def test_stacked_area_labels_band_midpoints(self):
        figure = StackedAreaChart(STACK, show_values=True)
        ax = figure.axes[0]
        self.assertEqual(texts(ax), ["1", "2", "3", "4", "5", "6"])
        # the second band spans 1-5 at x=0: its label sits at the midpoint
        self.assertEqual(tuple(labels(ax)[3].xy), (0.0, 3.0))

    def test_box_labels_the_median(self):
        figure = BoxPlot(GROUPS, show_values=True)
        ax = figure.axes[0]
        self.assertEqual(texts(ax), ["3", "20"])
        self.assertEqual(tuple(labels(ax)[1].xy), (2.0, 20.0))

    def test_violin_labels_the_median(self):
        figure = ViolinPlot(GROUPS, show_values=True)
        self.assertEqual(texts(figure.axes[0]), ["3", "20"])
        horizontal = ViolinPlot(
            GROUPS, show_values=True, orientation=ORIENTATION.HORIZONTAL
        )
        self.assertEqual(tuple(labels(horizontal.axes[0])[1].xy), (20.0, 2.0))

    def test_headroom_keeps_labels_inside(self):
        bare = LineChart(LINE).axes[0].get_ylim()[1]
        labelled = LineChart(LINE, show_values=True).axes[0].get_ylim()[1]
        self.assertGreater(labelled, bare)

    def test_background_emphasis_carries_no_labels(self):
        figure = LineChart(
            [LINE, LINE], emphasis=["background", None], show_values=True
        )
        self.assertEqual(len(labels(figure.axes[0])), len(LINE))


class TestThemeDefault(ValueLabelCase):
    FRONTS = (
        lambda **kw: LineChart(LINE, **kw),
        lambda **kw: ScatterChart(SCATTER, **kw),
        lambda **kw: Histogram(HIST, num_bins=3, **kw),
        lambda **kw: StackedAreaChart(STACK, **kw),
        lambda **kw: BoxPlot(GROUPS, **kw),
        lambda **kw: ViolinPlot(GROUPS, **kw),
    )

    def test_labelling_theme_labels_every_front(self):
        config.set_theme(THEME.MINIMAL)
        for front in self.FRONTS:
            self.assertTrue(labels(front().axes[0]))
            self.assertFalse(labels(front(show_values=False).axes[0]))

    def test_none_theme_default_leaves_labels_off(self):
        for front in self.FRONTS:
            self.assertFalse(labels(front().axes[0]))

    def test_point_labels_win_over_the_theme_default(self):
        config.set_theme(THEME.MINIMAL)
        figure = ScatterChart(NAMED, label="name")
        self.assertEqual(texts(figure.axes[0]), ["p0", "p1", "p2"])


class TestComposition(ValueLabelCase):
    def test_panel_keeps_the_labels(self):
        line = LineChart(LINE, show_values=True)
        scatter = ScatterChart(SCATTER, show_values=True)
        figure = Panel([line, scatter])
        self.assertEqual(
            texts(figure.axes[0]), ["1", "3", "2", "5", "4", "2", "6", "3"]
        )

    def test_grid_keeps_the_labels(self):
        box = BoxPlot(GROUPS, show_values=True)
        stack = StackedAreaChart(STACK, show_values=True)
        figure = Grid([[box, stack]])
        self.assertEqual(texts(figure.axes[0]), ["3", "20"])
        self.assertEqual(len(labels(figure.axes[1])), 6)


if __name__ == "__main__":
    unittest.main()
