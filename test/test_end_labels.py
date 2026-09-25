"""End labels on the line family: text colour, a halo, and a spread (ADR 0076)."""

import unittest
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import BumpChart, LineChart, StackedAreaChart
from datachart.config import config
from datachart.constants import LINE_LABEL_POSITION
from datachart.utils import Panel
from datachart.utils._internal.layers import TEXT_LINE_HEIGHT


def series(values, x=None):
    x = range(len(values)) if x is None else x
    return [{"x": i, "y": v} for i, v in zip(x, values)]


# three series over a wide range that all end on the same value
CONVERGING = [series([0, 50]), series([100, 50]), series([30, 50])]
NAMES = ["A", "B", "C"]


def _labels(ax):
    return {t.get_text(): t for t in ax.texts if t.get_text() in NAMES}


class TestLineEndLabels(unittest.TestCase):
    def setUp(self):
        config.reset_config()

    def tearDown(self):
        plt.close("all")

    def test_off_by_default(self):
        self.assertEqual(_labels(LineChart(CONVERGING, subtitle=NAMES).axes[0]), {})

    def test_one_label_per_series_at_its_last_point(self):
        ax = LineChart(CONVERGING, subtitle=NAMES, show_labels=True).axes[0]
        labels = _labels(ax)
        self.assertEqual(set(labels), set(NAMES))
        for line, name in zip(ax.get_lines(), NAMES):
            label = labels[name]
            self.assertEqual(label.xy, (line.get_xdata()[-1], line.get_ydata()[-1]))
            self.assertEqual(label.get_ha(), "left")

    def test_labels_wear_the_text_color_and_a_halo(self):
        ax = LineChart(CONVERGING, subtitle=NAMES, show_labels=True).axes[0]
        for label in _labels(ax).values():
            self.assertEqual(label.get_color(), config.get("font_general_color"))
            (halo,) = label.get_path_effects()
            self.assertEqual(halo._gc["linewidth"], config.get("plot_value_halo_width"))
            self.assertEqual(
                halo._gc["foreground"], config.get("axes_facecolor") or "#FFFFFF"
            )

    def test_background_series_takes_the_muted_color(self):
        ax = LineChart(
            CONVERGING,
            subtitle=NAMES,
            show_labels=True,
            emphasis=["highlight", "background", "background"],
        ).axes[0]
        labels = _labels(ax)
        self.assertEqual(labels["B"].get_color(), config.get("muted_color"))
        self.assertEqual(labels["A"].get_color(), config.get("font_general_color"))

    def test_legend_is_unchanged(self):
        plain = LineChart(CONVERGING, subtitle=NAMES).axes[0]
        labelled = LineChart(CONVERGING, subtitle=NAMES, show_labels=True).axes[0]
        self.assertEqual(plain.get_legend() is None, labelled.get_legend() is None)
        with_legend = LineChart(
            CONVERGING, subtitle=NAMES, show_labels=True, show_legend=True
        ).axes[0]
        self.assertIsNotNone(with_legend.get_legend())

    def test_label_position_start_and_both(self):
        start = LineChart(
            CONVERGING,
            subtitle=NAMES,
            show_labels=True,
            label_position=LINE_LABEL_POSITION.START,
        ).axes[0]
        self.assertEqual({t.xy[0] for t in start.texts}, {0})
        self.assertEqual({t.get_ha() for t in start.texts}, {"right"})
        both = LineChart(
            CONVERGING, subtitle=NAMES, show_labels=True, label_position="both"
        ).axes[0]
        self.assertEqual(sorted(t.xy[0] for t in both.texts), [0, 0, 0, 1, 1, 1])

    def test_invalid_label_position_raises(self):
        with self.assertRaises(ValueError):
            LineChart(
                CONVERGING, subtitle=NAMES, show_labels=True, label_position="mid"
            )

    def test_converging_labels_spread_along_the_value_axis(self):
        ax = LineChart(CONVERGING, subtitle=NAMES, show_labels=True).axes[0]
        labels = list(_labels(ax).values())
        height = TEXT_LINE_HEIGHT * labels[0].get_fontsize()
        offsets = sorted(label.xyann[1] for label in labels)
        for below, above in zip(offsets, offsets[1:]):
            self.assertGreaterEqual(above - below, height - 1e-6)
        # the spread is symmetric about the shared end
        self.assertAlmostEqual(sum(offsets), 0)
        # a label never leaves its end along the category axis
        self.assertEqual(len({label.xyann[0] for label in labels}), 1)

    def test_distinct_ends_stay_put(self):
        data = [series([0, 0]), series([100, 100]), series([50, 50])]
        ax = LineChart(data, subtitle=NAMES, show_labels=True).axes[0]
        self.assertEqual({t.xyann[1] for t in _labels(ax).values()}, {0})

    def test_labels_past_a_user_limit_are_hidden(self):
        ax = LineChart(CONVERGING, subtitle=NAMES, show_labels=True, xmax=0.5).axes[0]
        self.assertFalse(any(t.get_visible() for t in _labels(ax).values()))

    def test_date_axis_labels_the_last_date(self):
        dates = [datetime(2024, 1, 1), datetime(2024, 2, 1)]
        data = [series([1, 2], dates), series([3, 2], dates)]
        ax = LineChart(data, subtitle=NAMES[:2], show_labels=True).axes[0]
        labels = _labels(ax)
        self.assertEqual(len(labels), 2)
        self.assertEqual(labels["A"].xy[0], ax.xaxis.convert_units(dates[-1]))

    def test_a_panel_spreads_labels_across_its_sources(self):
        left = LineChart(series([0, 50]), subtitle="A", show_labels=True)
        right = LineChart(series([100, 50]), subtitle="B", show_labels=True)
        ax = Panel([left, right]).axes[0]
        labels = _labels(ax)
        self.assertEqual(set(labels), {"A", "B"})
        height = TEXT_LINE_HEIGHT * labels["A"].get_fontsize()
        gap = abs(labels["A"].xyann[1] - labels["B"].xyann[1])
        self.assertGreaterEqual(gap, height - 1e-6)


class TestStackedAreaEndLabels(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_band_is_named_at_its_midpoint(self):
        data = [series([1, 2]), series([1, 4]), series([1, 6])]
        ax = StackedAreaChart(data, subtitle=NAMES, show_labels=True).axes[0]
        labels = _labels(ax)
        # bands stack 0-2, 2-6, 6-12 at the last x
        self.assertEqual([labels[n].xy for n in NAMES], [(1, 1), (1, 4), (1, 9)])
        self.assertEqual({t.get_ha() for t in labels.values()}, {"left"})

    def test_off_by_default(self):
        data = [series([1, 2]), series([1, 4])]
        self.assertEqual(_labels(StackedAreaChart(data, subtitle=NAMES).axes[0]), {})


class TestBumpEndLabels(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_whole_ranks_need_no_spread(self):
        data = [series([10, 1]), series([5, 7]), series([1, 9])]
        ax = BumpChart(data, subtitle=NAMES).axes[0]
        self.assertEqual({t.xyann[1] for t in _labels(ax).values()}, {0})


if __name__ == "__main__":
    unittest.main()
