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
    RaincloudPlot,
    ScatterChart,
    StackedAreaChart,
    SwarmPlot,
    ViolinPlot,
)
from datachart.config import config
from datachart.constants import ORIENTATION, SWARM_MODE, VALUE_FORMAT
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
# 200 normal draws in one group
DENSE = [
    {"label": "A", "value": float(v)}
    for v in np.random.default_rng(0).normal(10, 2, 200)
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

    def test_theme_spread_with_alias_override(self):
        config.register_theme(
            "spread", {**DEFAULT_THEME, "plot_bar_value_fontsize": 12}
        )
        config.set_theme("spread")
        self.assertEqual(config["plot_value_fontsize"], 12)

    def test_every_value_label_wears_the_halo(self):
        for figure in (
            LineChart(LINE, show_values=True),
            BarChart(BAR, show_values=True),
            StackedAreaChart(STACK, show_values=True),
            BoxPlot(GROUPS, show_values=True),
        ):
            self.assertTrue(labels(figure.axes[0])[0].get_path_effects())
        bare = LineChart(LINE, show_values=True, style={"plot_value_halo_width": 0})
        self.assertEqual(labels(bare.axes[0])[0].get_path_effects(), [])

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

    def test_thin_band_stays_bare(self):
        thin = [{"x": i, "y": 0.001} for i in range(3)]
        figure = StackedAreaChart([STACK[0], thin, STACK[1]], show_values=True)
        self.assertEqual(texts(figure.axes[0]), ["1", "2", "3", "4", "5", "6"])

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
        figure = LineChart(LINE, show_values=True)
        figure.canvas.draw()
        ax = figure.axes[0]
        top = max(t.get_window_extent().y1 for t in labels(ax))
        self.assertLessEqual(top, ax.get_window_extent().y1)

    def test_background_emphasis_carries_no_labels(self):
        figure = LineChart(
            [LINE, LINE], emphasis=["background", None], show_values=True
        )
        self.assertEqual(len(labels(figure.axes[0])), len(LINE))


def packed_points(ax):
    """Every swarm point's final (x, y), from the drawn collections."""

    return {tuple(xy) for c in ax.collections for xy in np.asarray(c.get_offsets())}


class TestSwarm(ValueLabelCase):
    def test_labels_min_median_max_per_group(self):
        figure = SwarmPlot(GROUPS, show_values=True)
        self.assertEqual(
            sorted(texts(figure.axes[0]), key=float), ["1", "3", "5", "10", "20", "30"]
        )

    def test_labels_sit_at_packed_points(self):
        figure = SwarmPlot(GROUPS, show_values=True)
        ax = figure.axes[0]
        points = packed_points(ax)
        for label in labels(ax):
            self.assertIn(tuple(label.xy), points)

    def test_dense_group_still_prints_three_values(self):
        figure = SwarmPlot(DENSE, show_values=True)
        values = [p["value"] for p in DENSE]
        expected = [f"{v:g}" for v in (min(values), np.median(values), max(values))]
        self.assertEqual(sorted(texts(figure.axes[0]), key=float), expected)

    def test_even_group_median_sits_on_the_nearest_point(self):
        even = [{"label": "A", "value": float(v)} for v in (1, 2, 3, 4)]
        figure = SwarmPlot(even, show_values=True)
        placed = {t.get_text(): t.xy for t in labels(figure.axes[0])}
        self.assertEqual(sorted(placed, key=float), ["1", "2.5", "4"])
        self.assertEqual(placed["2.5"][1], 2.0)

    def test_small_groups_do_not_repeat_a_point(self):
        pair = [{"label": "A", "value": 1.0}, {"label": "A", "value": 3.0}]
        single = [{"label": "B", "value": 7.0}]
        figure = SwarmPlot(pair + single, show_values=True)
        self.assertEqual(sorted(texts(figure.axes[0]), key=float), ["1", "3", "7"])

    def test_value_format_applies(self):
        figure = SwarmPlot(GROUPS, show_values=True, value_format=VALUE_FORMAT.DECIMAL)
        self.assertIn("3.0", texts(figure.axes[0]))

    def test_strip_and_horizontal(self):
        for kwargs in (
            {"mode": SWARM_MODE.STRIP},
            {"orientation": ORIENTATION.HORIZONTAL},
            {"mode": SWARM_MODE.STRIP, "orientation": ORIENTATION.HORIZONTAL},
        ):
            figure = SwarmPlot(GROUPS, show_values=True, **kwargs)
            ax = figure.axes[0]
            self.assertEqual(len(labels(ax)), 6, kwargs)
            points = packed_points(ax)
            for label in labels(ax):
                self.assertIn(tuple(label.xy), points)

    def test_horizontal_labels_carry_the_value_on_x(self):
        figure = SwarmPlot(GROUPS, show_values=True, orientation=ORIENTATION.HORIZONTAL)
        for label in labels(figure.axes[0]):
            self.assertEqual(f"{label.xy[0]:g}", label.get_text())

    def test_headroom_keeps_labels_inside(self):
        figure = SwarmPlot(GROUPS, show_values=True)
        figure.canvas.draw()
        ax = figure.axes[0]
        top = max(t.get_window_extent().y1 for t in labels(ax))
        self.assertLessEqual(top, ax.get_window_extent().y1)

    def test_background_group_carries_no_labels(self):
        figure = SwarmPlot(GROUPS, show_values=True, emphasis=["background", None])
        self.assertEqual(sorted(texts(figure.axes[0]), key=float), ["10", "20", "30"])


class TestRaincloud(ValueLabelCase):
    def test_box_labels_the_median(self):
        figure = RaincloudPlot(GROUPS, show_values=True)
        ax = figure.axes[0]
        medians = [t for t in labels(ax) if t.get_text() in ("3", "20")]
        self.assertEqual([tuple(t.xy) for t in medians], [(1.0, 3.0), (2.0, 20.0)])

    def test_rain_labels_min_and_max_only(self):
        figure = RaincloudPlot(GROUPS, show_values=True)
        ax = figure.axes[0]
        self.assertEqual(
            sorted(texts(ax), key=float), ["1", "3", "5", "10", "20", "30"]
        )
        points = packed_points(ax)
        for label in labels(ax):
            if label.get_text() not in ("3", "20"):
                self.assertIn(tuple(label.xy), points)

    def test_horizontal_and_format(self):
        figure = RaincloudPlot(
            GROUPS,
            show_values=True,
            value_format=VALUE_FORMAT.DECIMAL,
            orientation=ORIENTATION.HORIZONTAL,
        )
        ax = figure.axes[0]
        self.assertEqual(
            sorted(texts(ax), key=float), ["1.0", "3.0", "5.0", "10.0", "20.0", "30.0"]
        )
        median = next(t for t in labels(ax) if t.get_text() == "20.0")
        self.assertEqual(tuple(median.xy), (20.0, 2.0))


class TestThemeDefault(ValueLabelCase):
    FRONTS = (
        lambda **kw: LineChart(LINE, **kw),
        lambda **kw: ScatterChart(SCATTER, **kw),
        lambda **kw: Histogram(HIST, num_bins=3, **kw),
        lambda **kw: StackedAreaChart(STACK, **kw),
        lambda **kw: BoxPlot(GROUPS, **kw),
        lambda **kw: ViolinPlot(GROUPS, **kw),
        lambda **kw: SwarmPlot(GROUPS, **kw),
        lambda **kw: RaincloudPlot(GROUPS, **kw),
    )

    def test_labelling_theme_labels_every_front(self):
        config.update_config({"chart_default_show_values": True})
        for front in self.FRONTS:
            self.assertTrue(labels(front().axes[0]))
            self.assertFalse(labels(front(show_values=False).axes[0]))

    def test_none_theme_default_leaves_labels_off(self):
        for front in self.FRONTS:
            self.assertFalse(labels(front().axes[0]))

    def test_labelling_theme_labels_a_raincloud_range(self):
        config.update_config({"chart_default_show_values": True})
        self.assertEqual(len(texts(RaincloudPlot(GROUPS).axes[0])), 6)

    def test_point_labels_win_over_the_theme_default(self):
        config.update_config({"chart_default_show_values": True})
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

    def test_swarm_and_raincloud_labels_survive_composition(self):
        swarm = SwarmPlot(GROUPS, show_values=True)
        box = BoxPlot(GROUPS)
        self.assertEqual(len(labels(Panel([box, swarm]).axes[0])), 6)
        rain = RaincloudPlot(GROUPS, show_values=True)
        figure = Grid([[swarm, rain]])
        self.assertEqual(len(labels(figure.axes[0])), 6)
        self.assertEqual(len(texts(figure.axes[1])), 6)


if __name__ == "__main__":
    unittest.main()
