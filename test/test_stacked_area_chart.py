"""Tests for the stacked area chart: baselines, style, limits, and composition."""

import unittest

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

from datachart.charts import StackedAreaChart, LineChart
from datachart.config import config
from datachart.constants import STACKED_AREA_BASELINE, THEME
from datachart.utils import Panel, Grid
from datachart.utils._internal.config_helpers import get_stackedarea_style
from datachart.utils._internal.layers import (
    MarkClipBox,
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
            for key in (
                "plot_stackedarea_alpha",
                "plot_stackedarea_outline",
                "plot_stackedarea_edge_color",
                "plot_stackedarea_edge_width",
            ):
                self.assertIn(key, config.config, f"{theme} lacks {key}")


def _charts(data):
    return [{"data": d} for d in data]


class TestStackOffsets(unittest.TestCase):
    def test_zero_starts_at_zero(self):
        np.testing.assert_array_equal(
            stack_first_line(Y, STACKED_AREA_BASELINE.ZERO), 0
        )

    def test_percent_columns_sum_to_100(self):
        layers = build_layers("stackedareachart", _charts(DATA), {})
        slots = _stack_slots(layers, STACKED_AREA_BASELINE.PERCENT)
        top = slots[id(layers[-1])].top
        np.testing.assert_allclose(top, 100.0)
        np.testing.assert_array_equal(slots[id(layers[0])].bottom, 0)

    def test_sym_is_symmetric_about_zero(self):
        first = stack_first_line(Y, STACKED_AREA_BASELINE.SYM)
        np.testing.assert_allclose(first, -Y.sum(0) / 2)
        np.testing.assert_allclose(first + Y.sum(0), -first)

    def test_wiggle_matches_stackplot(self):
        m = Y.shape[0]
        expected = (Y * (m - 0.5 - np.arange(m)[:, None])).sum(0) / -m
        np.testing.assert_allclose(
            stack_first_line(Y, STACKED_AREA_BASELINE.WIGGLE), expected
        )

    def test_weighted_wiggle_matches_stackplot(self):
        fig, ax = plt.subplots()
        polys = ax.stackplot(np.arange(4), Y, baseline="weighted_wiggle")
        vertices = polys[0].get_paths()[0].vertices
        # the first polygon's lower edge is the baseline
        lower = [vertices[vertices[:, 0] == x, 1].min() for x in range(4)]
        first = stack_first_line(Y, STACKED_AREA_BASELINE.WEIGHTED_WIGGLE)
        np.testing.assert_allclose(lower, first)
        plt.close(fig)

    def test_series_order_is_stack_order(self):
        layers = build_layers("stackedareachart", _charts(DATA), {})
        slots = _stack_slots(layers, STACKED_AREA_BASELINE.ZERO)
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
        for baseline in (STACKED_AREA_BASELINE.ZERO, STACKED_AREA_BASELINE.PERCENT):
            fig = StackedAreaChart(data=DATA, baseline=baseline)
            self.assertEqual(fig.axes[0].get_ylim()[0], 0.0)

    def test_sym_ends_on_the_stack(self):
        fig = StackedAreaChart(data=DATA, baseline=STACKED_AREA_BASELINE.SYM)
        lo, hi = fig.axes[0].get_ylim()
        self.assertEqual((lo, hi), (-3.0, 3.0))

    def test_percent_ends_at_one_hundred(self):
        fig = StackedAreaChart(data=DATA, baseline=STACKED_AREA_BASELINE.PERCENT)
        lo, hi = fig.axes[0].get_ylim()
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 100.0)

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
        stack = StackedAreaChart(data=DATA, baseline=STACKED_AREA_BASELINE.SYM)
        line = LineChart(data=DATA[0])
        fig = Panel([stack, line])
        ax = fig.axes[0]
        self.assertEqual(len(_bands(ax)), 3)
        self.assertEqual(len(ax.lines), 1)
        self.assertEqual(fig._chart_metadata["panel"].settings["baseline"], "sym")

    def test_panel_of_line_layers_tightens_x(self):
        fig = Panel([StackedAreaChart(data=DATA), LineChart(data=DATA[0])])
        self.assertEqual(fig.axes[0].get_xlim(), (0.0, 3.0))

    def test_tightened_x_never_snaps_to_a_tick(self):
        """The data range wins over the tick grid: no empty step before 1."""
        line = LineChart(data=[{"x": x, "y": x} for x in range(1, 17)])
        self.assertEqual(line.axes[0].get_xlim(), (1.0, 16.0))
        stack = StackedAreaChart(data=[series([1, 2, 3]) for _ in range(2)])
        self.assertEqual(stack.axes[0].get_xlim(), (0.0, 2.0))

    def test_line_end_markers_draw_whole(self):
        """Markers on the pinned x ends clip to the axes grown by their radius."""
        fig = LineChart(
            data=[{"x": x, "y": x} for x in range(1, 17)],
            style={"plot_line_marker": "o"},
        )
        fig.canvas.draw()
        ax = fig.axes[0]
        line = ax.lines[0]
        box = line.get_clip_box()
        self.assertIsInstance(box, MarkClipBox)
        radius = line.get_markersize() / 2 * fig.dpi / 72
        self.assertGreaterEqual(box.x0, ax.bbox.x0 - radius - 2)
        self.assertLess(box.x0, ax.bbox.x0 - radius + 1e-6)
        self.assertGreater(box.x1, ax.bbox.x1 + radius - 1e-6)
        # a user limit may cut the line on purpose: the clip stays on that axis
        cropped = LineChart(data=[{"x": x, "y": x} for x in range(1, 17)], xmax=8)
        box = cropped.axes[0].lines[0].get_clip_box()
        self.assertFalse(isinstance(box, MarkClipBox) and "x" in box._dims)

    def test_legend_adds_no_headroom_over_a_pinned_stack(self):
        fig = StackedAreaChart(
            data=DATA,
            baseline=STACKED_AREA_BASELINE.PERCENT,
            subtitle=list("abc"),
            show_legend=True,
        )
        fig.canvas.draw()
        lo, hi = fig.axes[0].get_ylim()
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 100.0)

    def test_log_scale_keeps_its_own_floor(self):
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            fig = StackedAreaChart(data=DATA, scaley="log")
        self.assertGreater(fig.axes[0].get_ylim()[0], 0.0)

    def test_panel_first_stacked_figure_baseline_wins(self):
        fig = Panel(
            [StackedAreaChart(data=DATA), StackedAreaChart(data=DATA, baseline="sym")]
        )
        self.assertEqual(fig._chart_metadata["panel"].settings["baseline"], "zero")
        self.assertEqual(fig.axes[0].get_ylim()[0], 0.0)
        fig = Panel(
            [LineChart(data=DATA[0]), StackedAreaChart(data=DATA, baseline="sym")]
        )
        self.assertEqual(fig._chart_metadata["panel"].settings["baseline"], "sym")

    def test_panel_zero_pins_the_bottom(self):
        fig = Panel([StackedAreaChart(data=DATA), LineChart(data=DATA[0])])
        self.assertEqual(fig.axes[0].get_ylim()[0], 0.0)

    def test_grid_nests(self):
        fig = Grid([[StackedAreaChart(data=DATA), LineChart(data=DATA[0])]])
        self.assertEqual(len(_bands(fig.axes[0])), 3)


if __name__ == "__main__":
    unittest.main()


class TestSharedReferences(unittest.TestCase):
    """One reference dict draws once per axes (issue #171)."""

    def tearDown(self):
        plt.close("all")

    def test_single_hline_is_one_legend_entry(self):
        fig = StackedAreaChart(
            data=DATA,
            subtitle=["a", "b", "c"],
            hlines={"y": 3, "label": "cap"},
            texts={"x": 1, "y": 5, "text": "note"},
            show_legend=True,
        )
        ax = fig.axes[0]
        labels = [t.get_text() for t in ax.get_legend().get_texts()]
        self.assertEqual(labels.count("cap"), 1)
        self.assertEqual([t.get_text() for t in ax.texts].count("note"), 1)

    def test_per_series_list_draws_per_series(self):
        fig = StackedAreaChart(
            data=DATA,
            hlines=[{"y": 1, "label": "a"}, {"y": 2, "label": "b"}, {"y": 3}],
        )
        lines = [c for c in fig.axes[0].collections if c.get_label() in "ab"]
        self.assertEqual(len(lines), 2)
