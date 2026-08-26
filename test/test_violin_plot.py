"""Tests for the violin plot (ADR 0019)."""

import unittest
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import numpy as np

from datachart.charts import BoxPlot, ViolinPlot
from datachart.config import config
from datachart.constants import THEME, VIOLIN_INNER
from datachart.utils import Panel


def violin_data(labels="ABC", n=30, split=False):
    rng = np.random.RandomState(3)
    data = []
    for i, lab in enumerate(labels):
        for j, v in enumerate(rng.randn(n) + i):
            point = {"label": lab, "value": float(v)}
            if split:
                point["sex"] = "F" if j % 2 else "M"
            data.append(point)
    return data


def bodies(ax):
    return [c for c in ax.collections if isinstance(c, PolyCollection)]


class TestViolinPlot(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_groups_by_label_in_first_seen_order(self):
        figure = ViolinPlot(violin_data("CAB"))
        ax = figure.axes[0]
        self.assertEqual(len(bodies(ax)), 3)
        self.assertEqual([t.get_text() for t in ax.get_xticklabels()], list("CAB"))
        self.assertEqual(list(ax.get_xticks()), [1, 2, 3])

    def test_inner_modes_draw_expected_marks(self):
        base = len(ViolinPlot(violin_data(), inner=None).axes[0].lines)
        self.assertEqual(base, 0)
        # box: whisker + quartile bar + median dot per violin
        self.assertEqual(len(ViolinPlot(violin_data(), inner="box").axes[0].lines), 9)
        # quartiles: three lines per violin
        self.assertEqual(
            len(ViolinPlot(violin_data(), inner=VIOLIN_INNER.QUARTILES).axes[0].lines),
            9,
        )
        self.assertEqual(
            len(ViolinPlot(violin_data(), inner="median").axes[0].lines), 3
        )

    def test_invalid_inner_raises(self):
        with self.assertRaises(ValueError):
            ViolinPlot(violin_data(), inner="mean")

    def test_split_requires_exactly_two_values(self):
        data = violin_data(split=True)
        for point in data[:3]:
            point["sex"] = "X"
        with self.assertRaises(ValueError):
            ViolinPlot(data, split="sex")
        with self.assertRaises(ValueError):
            ViolinPlot(violin_data(), split="sex")

    def test_split_draws_two_halves_with_legend(self):
        figure = ViolinPlot(violin_data(split=True), split="sex", show_legend=True)
        ax = figure.axes[0]
        halves = bodies(ax)
        self.assertEqual(len(halves), 6)
        # left halves never cross the centre, right halves never go left of it
        left, right = halves[0], halves[1]
        self.assertLessEqual(left.get_paths()[0].vertices[:, 0].max(), 1.0 + 1e-9)
        self.assertGreaterEqual(right.get_paths()[0].vertices[:, 0].min(), 1.0 - 1e-9)
        self.assertNotEqual(
            tuple(left.get_facecolor()[0]), tuple(right.get_facecolor()[0])
        )
        legend = ax.get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["M", "F"])

    def test_bandwidth_passthrough(self):
        data = violin_data("A")
        narrow = bodies(ViolinPlot(data, bandwidth=0.1).axes[0])[0]
        wide = bodies(ViolinPlot(data, bandwidth=1.0).axes[0])[0]
        # a wider kernel spreads the density: the peak half-width shrinks
        self.assertGreater(
            np.abs(narrow.get_paths()[0].vertices[:, 0] - 1).max(),
            np.abs(wide.get_paths()[0].vertices[:, 0] - 1).max() * 0.99,
        )
        with self.assertRaises(ValueError):
            ViolinPlot(data, bandwidth="gaussian")

    def test_horizontal_puts_labels_on_y(self):
        figure = ViolinPlot(violin_data(), orientation="horizontal")
        ax = figure.axes[0]
        self.assertEqual([t.get_text() for t in ax.get_yticklabels()], list("ABC"))
        body = bodies(ax)[0].get_paths()[0].vertices
        self.assertLess(np.ptp(body[:, 1]), np.ptp(body[:, 0]))

    def test_empty_data_warns(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            ViolinPlot([])
        self.assertTrue(any("No data points" in str(w.message) for w in caught))

    def test_emphasis_mutes_background_violin(self):
        figure = ViolinPlot(violin_data(), emphasis=["background", None, "highlight"])
        ax = figure.axes[0]
        muted = bodies(ax)[0]
        self.assertEqual(muted.get_alpha(), config["muted_alpha"])
        self.assertEqual(
            matplotlib.colors.to_hex(muted.get_facecolor()[0]).upper(),
            config["muted_color"],
        )
        with self.assertRaises(ValueError):
            ViolinPlot(violin_data(), emphasis=["background"])

    def test_label_value_remap(self):
        data = [{"g": g, "v": v} for g in "AB" for v in (1.0, 2.0, 3.0)]
        figure = ViolinPlot(data, label="g", value="v")
        self.assertEqual(len(bodies(figure.axes[0])), 2)

    def test_single_value_label_raises(self):
        with self.assertRaises(ValueError):
            ViolinPlot([{"label": "A", "value": 1.0}])

    def test_panel_with_box_plot(self):
        data = violin_data()
        figure = Panel(
            [ViolinPlot(data, inner=None), BoxPlot(data, show_outliers=False)]
        )
        ax = figure.axes[0]
        self.assertEqual(len(bodies(ax)), 3)
        self.assertEqual(len([p for p in ax.patches if hasattr(p, "get_path")]), 3)

    def test_subplots(self):
        figure = ViolinPlot([violin_data(), violin_data("DE")], subplots=True)
        self.assertEqual(len(figure.axes), 2)

    def test_every_theme_declares_violin_keys(self):
        from datachart.themes import (
            DEFAULT_THEME,
            GREYSCALE_THEME,
            INK_THEME,
            HATCH_THEME,
            MINIMAL_THEME,
            MATERIAL_THEME,
        )

        for theme in (
            DEFAULT_THEME,
            GREYSCALE_THEME,
            INK_THEME,
            HATCH_THEME,
            MINIMAL_THEME,
            MATERIAL_THEME,
        ):
            for key in (
                "plot_violin_color",
                "plot_violin_alpha",
                "plot_violin_linewidth",
                "plot_violin_edgecolor",
                "plot_violin_width",
                "plot_violin_inner_color",
                "plot_violin_inner_linewidth",
                "plot_violin_median_color",
                "plot_violin_median_size",
            ):
                self.assertIn(key, theme)


if __name__ == "__main__":
    unittest.main()
