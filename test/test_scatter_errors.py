"""Tests for scatter error bars (ADR 0057): validation, style, drawing, and hover."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np
from matplotlib.collections import PathCollection
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyArrowPatch

from datachart.charts import BarChart, ScatterChart
from datachart.config import config
from datachart.config.configuration import THEMES
from datachart.constants import EMPHASIS, ORIENTATION, THEME
from datachart.utils import Panel
from datachart.utils._internal.config_helpers import get_scatter_error_style
from datachart.utils._internal.validate import validate_error_distances

ERROR_KEYS = (
    "plot_scatter_error_color",
    "plot_scatter_error_width",
    "plot_scatter_error_capsize",
)


def _bars(ax) -> list:
    """Every error bar drawn into `ax`, in drawing order; one per point per side."""

    return [patch for patch in ax.patches if isinstance(patch, FancyArrowPatch)]


def _ends(ax) -> list:
    """Each bar's far end, in data coordinates: where its distance reaches."""

    ax.figure.canvas.draw()
    return [tuple(round(float(v), 6) for v in _shaft(bar)[-1]) for bar in _bars(ax)]


def _shaft(bar) -> np.ndarray:
    """A bar's own vertices, from the marker's edge to its far end, without the cap."""

    return bar.get_path().vertices[:3]


def _bar_colors(ax) -> list:
    return [
        tuple(float(channel) for channel in bar.get_edgecolor()) for bar in _bars(ax)
    ]


POINTS = [
    {"x": 1, "y": 10, "xerr": 0.2, "yerr": 1.0},
    {"x": 2, "y": 12, "xerr": 0.3, "yerr": [0.5, 2.0]},
    {"x": 3, "y": 11},
]


class TestErrorValidation(unittest.TestCase):
    def test_a_number_is_a_symmetric_distance(self):
        self.assertEqual(validate_error_distances([2], "yerr"), [(2.0, 2.0)])

    def test_a_pair_is_a_low_and_a_high_distance(self):
        self.assertEqual(validate_error_distances([[1, 3]], "yerr"), [(1.0, 3.0)])
        self.assertEqual(validate_error_distances([(1, 3)], "yerr"), [(1.0, 3.0)])

    def test_a_missing_error_is_no_bar(self):
        self.assertEqual(
            validate_error_distances([None, 1], "xerr"), [None, (1.0, 1.0)]
        )

    def test_a_negative_distance_raises(self):
        with self.assertRaises(ValueError) as caught:
            validate_error_distances([1, -0.5], "yerr")
        self.assertIn("`yerr`", str(caught.exception))
        self.assertIn("point 1", str(caught.exception))

    def test_a_pair_of_the_wrong_length_raises(self):
        for value in ([1], [1, 2, 3], []):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_error_distances([value], "xerr")

    def test_a_none_inside_a_pair_raises(self):
        with self.assertRaises(ValueError) as caught:
            validate_error_distances([[None, 2]], "yerr")
        self.assertIn("`yerr`", str(caught.exception))

    def test_a_non_number_raises(self):
        for value in ("1", True, float("nan"), float("inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_error_distances([value], "yerr")


class TestErrorStyle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)

    def test_every_theme_carries_the_error_keys(self):
        for name, theme in THEMES.items():
            for key in ERROR_KEYS:
                with self.subTest(theme=name, key=key):
                    self.assertIn(key, theme)

    def test_the_default_color_follows_the_point(self):
        self.assertNotIn("ecolor", get_scatter_error_style({}))

    def test_the_style_resolves_the_theme_keys(self):
        style = get_scatter_error_style({})
        self.assertEqual(style["elinewidth"], config["plot_scatter_error_width"])
        self.assertEqual(style["capsize"], config["plot_scatter_error_capsize"])

    def test_a_chart_style_wins_over_the_theme(self):
        style = get_scatter_error_style(
            {
                "plot_scatter_error_color": "#123456",
                "plot_scatter_error_width": 3.0,
                "plot_scatter_error_capsize": 5,
            }
        )
        self.assertEqual(style, {"ecolor": "#123456", "elinewidth": 3.0, "capsize": 5})


class TestErrorDrawing(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_a_symmetric_error_reaches_the_same_distance_both_ways(self):
        ax = ScatterChart(data=[{"x": 1, "y": 10, "yerr": 2}]).axes[0]
        self.assertEqual(_ends(ax), [(1.0, 8.0), (1.0, 12.0)])

    def test_a_pair_reaches_low_below_and_high_above(self):
        ax = ScatterChart(data=[{"x": 1, "y": 10, "yerr": [1, 4]}]).axes[0]
        self.assertEqual(_ends(ax), [(1.0, 9.0), (1.0, 14.0)])

    def test_an_x_error_runs_along_the_x_axis(self):
        ax = ScatterChart(data=[{"x": 5, "y": 10, "xerr": [1, 2]}]).axes[0]
        self.assertEqual(_ends(ax), [(4.0, 10.0), (7.0, 10.0)])

    def test_both_axes_draw_their_own_bars(self):
        ax = ScatterChart(data=[{"x": 5, "y": 10, "xerr": 1, "yerr": 2}]).axes[0]
        self.assertEqual(_ends(ax), [(4.0, 10.0), (6.0, 10.0), (5.0, 8.0), (5.0, 12.0)])

    def test_a_bar_stops_at_the_edge_of_its_marker(self):
        size = 400
        figure = ScatterChart(
            data=[{"x": 1, "y": 10, "yerr": 2}], style={"plot_scatter_size": size}
        )
        ax = figure.axes[0]
        ax.figure.canvas.draw()
        for bar in _bars(ax):
            near = ax.transData.transform(_shaft(bar)[0])
            point = ax.transData.transform((1.0, 10.0))
            gap = np.hypot(*(near - point)) * 72 / figure.dpi
            self.assertAlmostEqual(gap, np.sqrt(size) / 2, places=2)

    def test_a_zero_distance_draws_no_bar(self):
        ax = ScatterChart(data=[{"x": 1, "y": 10, "yerr": [0, 2]}]).axes[0]
        self.assertEqual(_ends(ax), [(1.0, 12.0)])

    def test_a_point_without_an_error_draws_no_bar(self):
        ax = ScatterChart(data=POINTS).axes[0]
        along_y = [end for end in _ends(ax) if end[0] in (1.0, 2.0) and end[1] != 10.0]
        self.assertEqual(along_y, [(1.0, 9.0), (1.0, 11.0), (2.0, 11.5), (2.0, 14.0)])

    def test_no_error_key_draws_nothing(self):
        ax = ScatterChart(data=[{"x": 1, "y": 1}, {"x": 2, "y": 2}]).axes[0]
        self.assertEqual(_bars(ax), [])

    def test_the_show_flags_switch_the_bars_off(self):
        ax = ScatterChart(data=POINTS, show_xerr=False, show_yerr=False).axes[0]
        self.assertEqual(_bars(ax), [])
        ax = ScatterChart(data=POINTS, show_xerr=False).axes[0]
        # only the y errors are left, so every bar ends over its own point
        self.assertEqual([end[0] for end in _ends(ax)], [1.0, 1.0, 2.0, 2.0])

    def test_the_parameters_name_the_keys(self):
        data = [{"x": 1, "y": 10, "ci": 0.5, "sd": 2}]
        ax = ScatterChart(data=data, xerr="sd", yerr="ci").axes[0]
        self.assertEqual(
            _ends(ax), [(-1.0, 10.0), (3.0, 10.0), (1.0, 9.5), (1.0, 10.5)]
        )

    def test_a_bad_error_raises_from_the_front(self):
        with self.assertRaises(ValueError) as caught:
            ScatterChart(data=[{"x": 1, "y": 1, "yerr": [1, 2, 3]}])
        self.assertIn("`yerr`", str(caught.exception))

    def test_a_bar_takes_the_color_of_its_hue_group(self):
        data = [
            {"x": i, "y": i, "yerr": 1, "hue": group}
            for i, group in enumerate(["a", "b", "a"])
        ]
        ax = ScatterChart(data=data, hue="hue").axes[0]
        marker_colors = [
            tuple(collection.get_facecolor()[0][:3])
            for collection in ax.collections
            if isinstance(collection, PathCollection)
        ]
        bar_colors = {color[:3] for color in _bar_colors(ax)}
        self.assertEqual(bar_colors, set(marker_colors))

    def test_a_bar_takes_the_series_color(self):
        ax = ScatterChart(
            data=[{"x": 1, "y": 1, "yerr": 1}],
            style={"plot_scatter_color": "#123456"},
        ).axes[0]
        alpha = config["plot_scatter_alpha"]
        self.assertEqual(set(_bar_colors(ax)), {to_rgba("#123456", alpha)})

    def test_the_style_color_overrides_the_point_color(self):
        ax = ScatterChart(
            data=[{"x": 1, "y": 1, "yerr": 1}],
            style={
                "plot_scatter_color": "#123456",
                "plot_scatter_error_color": "#000000",
            },
        ).axes[0]
        alpha = config["plot_scatter_alpha"]
        self.assertEqual(set(_bar_colors(ax)), {to_rgba("#000000", alpha)})

    def test_a_muted_series_dims_its_bars(self):
        ax = ScatterChart(
            data=[[{"x": 1, "y": 1, "yerr": 1}], [{"x": 2, "y": 2, "yerr": 1}]],
            emphasis=["background", None],
        ).axes[0]
        muted = to_rgba(config["muted_color"], config["muted_alpha"])
        self.assertIn(muted, _bar_colors(ax))

    def test_a_muted_point_keeps_its_bar(self):
        data = [
            {"x": 1, "y": 1, "yerr": 1, "emphasis": EMPHASIS.BACKGROUND},
            {"x": 2, "y": 2, "yerr": 1},
        ]
        ax = ScatterChart(data=data).axes[0]
        self.assertEqual(len(_bars(ax)), 4)

    def test_a_transposed_panel_swaps_the_bars(self):
        bars = BarChart(
            data=[{"label": "a", "y": 1}], orientation=ORIENTATION.HORIZONTAL
        )
        points = ScatterChart(data=[{"x": 1, "y": 10, "yerr": 2}])
        ax = Panel([bars, points]).axes[0]
        # the y error runs along the drawn x axis, where the y values sit
        self.assertEqual(_ends(ax), [(8.0, 1.0), (12.0, 1.0)])

    def test_the_bars_draw_under_their_markers(self):
        ax = ScatterChart(data=[{"x": 1, "y": 1, "yerr": 1}]).axes[0]
        marks = [c for c in ax.collections if isinstance(c, PathCollection)]
        self.assertLess(_bars(ax)[0].get_zorder(), marks[0].get_zorder())

    def test_the_axes_reach_the_ends_of_the_bars(self):
        ax = ScatterChart(data=[{"x": 1, "y": 10, "yerr": 5}]).axes[0]
        low, high = ax.get_ylim()
        self.assertLessEqual(low, 5.0)
        self.assertGreaterEqual(high, 15.0)


class TestErrorHover(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_a_symmetric_error_reports_its_distance(self):
        figure = ScatterChart(data=[{"x": 1, "y": 10, "yerr": 2}])
        ((_, resolve),) = figure._hover_targets
        self.assertEqual(resolve(0), {"label": None, "x": 1, "y": 10, "yerr": 2.0})

    def test_an_asymmetric_error_reports_both_distances(self):
        figure = ScatterChart(data=[{"x": 1, "y": 10, "xerr": [0.5, 1.5]}])
        ((_, resolve),) = figure._hover_targets
        self.assertEqual(resolve(0)["xerr"], "-0.5/+1.5")

    def test_a_point_without_an_error_reports_none(self):
        figure = ScatterChart(data=POINTS)
        ((_, resolve),) = figure._hover_targets
        self.assertEqual(list(resolve(0)), ["label", "x", "y", "xerr", "yerr"])
        self.assertEqual(list(resolve(2)), ["label", "x", "y"])

    def test_a_transposed_panel_swaps_the_error_fields(self):
        bars = BarChart(
            data=[{"label": "a", "y": 1}], orientation=ORIENTATION.HORIZONTAL
        )
        points = ScatterChart(data=[{"x": 1, "y": 10, "yerr": 2}])
        figure = Panel([bars, points])
        _, resolve = figure._hover_targets[-1]
        self.assertEqual(resolve(0), {"label": None, "x": 10, "y": 1, "xerr": 2.0})


class TestErrorFrontParameters(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_the_front_takes_the_error_parameters(self):
        figure = ScatterChart(
            data=[{"x": 1, "y": 10, "ci": 0.5}],
            xerr="ci",
            yerr="ci",
            show_xerr=False,
            show_yerr=True,
        )
        self.assertEqual(len(figure.axes), 1)


if __name__ == "__main__":
    unittest.main()
