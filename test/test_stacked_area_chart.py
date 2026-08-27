"""Tests for the stacked area chart: baselines, style, limits, and composition."""

import unittest

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

from datachart.charts import StackedAreaChart, LineChart
from datachart.config import config
from datachart.constants import BASELINE, THEME
from datachart.utils import Panel, Grid
from datachart.utils._internal.config_helpers import get_stackedarea_style
from datachart.utils._internal.layers import (
    build_layers,
    stack_first_line,
    _stack_slots,
)

THEMES = [
    THEME.DEFAULT,
    THEME.GREYSCALE,
    THEME.INK,
    THEME.HATCH,
    THEME.MINIMAL,
    THEME.MATERIAL,
]


def series(values, x=None):
    x = range(len(values)) if x is None else x
    return [{"x": i, "y": v} for i, v in zip(x, values)]


DATA = [series([1, 2, 3, 4]), series([2, 1, 2, 1]), series([1, 1, 1, 1])]
Y = np.array([[1, 2, 3, 4], [2, 1, 2, 1], [1, 1, 1, 1]], dtype=float)


def _bands(ax):
    return [c for c in ax.collections if isinstance(c, PolyCollection)]


class TestStackedAreaStyle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)

    def test_style_resolves_from_area_and_own_keys(self):
        style = get_stackedarea_style({})
        self.assertEqual(style["alpha"], config["plot_stackedarea_alpha"])
        self.assertEqual(style["zorder"], config["plot_area_zorder"])
        self.assertIs(style["outline"], False)
        self.assertNotIn("color", style)

    def test_chart_style_overrides(self):
        style = get_stackedarea_style(
            {"plot_stackedarea_alpha": 0.3, "plot_area_color": "#123456"}
        )
        self.assertEqual(style["alpha"], 0.3)
        self.assertEqual(style["color"], "#123456")

    def test_every_theme_sets_the_stackedarea_keys(self):
        for theme in THEMES:
            config.set_theme(theme)
            for key in ("plot_stackedarea_alpha", "plot_stackedarea_outline"):
                self.assertIn(key, config.config, f"{theme} lacks {key}")


class TestStackOffsets(unittest.TestCase):
    def test_zero_starts_at_zero(self):
        np.testing.assert_array_equal(stack_first_line(Y, BASELINE.ZERO), 0)

    def test_percent_columns_sum_to_100(self):
        layers = build_layers("stackedareachart", _charts(DATA), {})
        slots = _stack_slots(layers, BASELINE.PERCENT)
        top = slots[id(layers[-1])].top
        np.testing.assert_allclose(top, 100.0)
        np.testing.assert_array_equal(slots[id(layers[0])].bottom, 0)

    def test_sym_is_symmetric_about_zero(self):
        first = stack_first_line(Y, BASELINE.SYM)
        np.testing.assert_allclose(first, -Y.sum(0) / 2)
        np.testing.assert_allclose(first + Y.sum(0), -first)

    def test_wiggle_matches_stackplot(self):
        m = Y.shape[0]
        expected = (Y * (m - 0.5 - np.arange(m)[:, None])).sum(0) / -m
        np.testing.assert_allclose(stack_first_line(Y, BASELINE.WIGGLE), expected)

    def test_weighted_wiggle_matches_stackplot(self):
        fig, ax = plt.subplots()
        polys = ax.stackplot(np.arange(4), Y, baseline="weighted_wiggle")
        vertices = polys[0].get_paths()[0].vertices
        # the first polygon's lower edge is the baseline
        lower = [vertices[vertices[:, 0] == x, 1].min() for x in range(4)]
        first = stack_first_line(Y, BASELINE.WEIGHTED_WIGGLE)
        np.testing.assert_allclose(lower, first)
        plt.close(fig)

    def test_series_order_is_stack_order(self):
        layers = build_layers("stackedareachart", _charts(DATA), {})
        slots = _stack_slots(layers, BASELINE.ZERO)
        np.testing.assert_array_equal(slots[id(layers[0])].top, Y[0])
        np.testing.assert_array_equal(slots[id(layers[1])].bottom, Y[0])
        np.testing.assert_array_equal(slots[id(layers[2])].top, Y.sum(0))

    def test_invalid_baseline_raises(self):
        with self.assertRaises(ValueError):
            StackedAreaChart(data=DATA, baseline="nope")

    def test_ragged_x_raises(self):
        with self.assertRaises(ValueError):
            StackedAreaChart(data=[DATA[0], series([1, 2, 3])])
        with self.assertRaises(ValueError):
            StackedAreaChart(data=[DATA[0], series([1, 2, 3, 4], x=[3, 2, 1, 0])])


def _charts(data):
    return [{"data": d} for d in data]


class TestStackedAreaChart(unittest.TestCase):
    def tearDown(self):
        plt.close("all")
        config.set_theme(THEME.DEFAULT)

    def test_draws_one_band_per_series(self):
        fig = StackedAreaChart(data=DATA, subtitle=list("ABC"), show_legend=True)
        ax = fig.axes[0]
        self.assertEqual(len(_bands(ax)), 3)
        self.assertEqual(len(ax.lines), 0)
        self.assertEqual(
            [t.get_text() for t in ax.get_legend().get_texts()], list("ABC")
        )

    def test_outline_adds_lines(self):
        fig = StackedAreaChart(data=DATA, style={"plot_stackedarea_outline": True})
        self.assertEqual(len(fig.axes[0].lines), 3)

    def test_zero_and_percent_pin_the_bottom(self):
        for baseline in (BASELINE.ZERO, BASELINE.PERCENT):
            fig = StackedAreaChart(data=DATA, baseline=baseline)
            self.assertEqual(fig.axes[0].get_ylim()[0], 0.0)

    def test_sym_keeps_the_margin(self):
        fig = StackedAreaChart(data=DATA, baseline=BASELINE.SYM)
        lo, hi = fig.axes[0].get_ylim()
        self.assertLess(lo, -3.0)
        self.assertAlmostEqual(lo, -hi)

    def test_x_is_tightened(self):
        fig = StackedAreaChart(data=DATA)
        self.assertEqual(fig.axes[0].get_xlim(), (0.0, 3.0))

    def test_user_ymin_overrides_the_pin(self):
        fig = StackedAreaChart(data=DATA, ymin=-1)
        self.assertEqual(fig.axes[0].get_ylim()[0], -1.0)

    def test_subplots_unstack(self):
        fig = StackedAreaChart(data=DATA, subplots=True)
        self.assertEqual(len(fig.axes), 3)
        for ax, y in zip(fig.axes, Y):
            self.assertEqual(len(_bands(ax)), 1)
            self.assertEqual(ax.get_ylim()[0], 0.0)
            top = _bands(ax)[0].get_paths()[0].vertices[:, 1].max()
            self.assertAlmostEqual(top, y.max())

    def test_emphasis_mutes_a_band(self):
        fig = StackedAreaChart(data=DATA, emphasis=["background", None, None])
        band = _bands(fig.axes[0])[0]
        self.assertEqual(band.get_alpha(), config["muted_alpha"])

    def test_alpha_uses_the_stackedarea_key(self):
        fig = StackedAreaChart(data=DATA)
        band = _bands(fig.axes[0])[0]
        self.assertEqual(band.get_alpha(), config["plot_stackedarea_alpha"])

    def test_panel_with_line_keeps_the_stack(self):
        stack = StackedAreaChart(data=DATA, baseline=BASELINE.SYM)
        line = LineChart(data=DATA[0])
        fig = Panel([stack, line])
        ax = fig.axes[0]
        self.assertEqual(len(_bands(ax)), 3)
        self.assertEqual(len(ax.lines), 1)
        self.assertEqual(fig._chart_metadata["panel"].settings["baseline"], "sym")

    def test_panel_zero_pins_the_bottom(self):
        fig = Panel([StackedAreaChart(data=DATA), LineChart(data=DATA[0])])
        self.assertEqual(fig.axes[0].get_ylim()[0], 0.0)

    def test_grid_nests(self):
        fig = Grid([[StackedAreaChart(data=DATA), LineChart(data=DATA[0])]])
        self.assertEqual(len(_bands(fig.axes[0])), 3)


if __name__ == "__main__":
    unittest.main()
