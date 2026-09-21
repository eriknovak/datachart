"""Tests for scatter error bars (ADR 0057): validation, style, drawing, and hover."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matplotlib.collections import PathCollection
from matplotlib.colors import to_rgba
from matplotlib.container import ErrorbarContainer

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


def _bar_collections(ax) -> list:
    """Every error bar line collection drawn into `ax`, in drawing order."""

    return [
        collection
        for container in ax.containers
        if isinstance(container, ErrorbarContainer)
        for collection in container.lines[2]
    ]


def _segments(ax) -> list:
    return [
        segment
        for collection in _bar_collections(ax)
        for segment in collection.get_segments()
    ]


def _bar_colors(ax) -> list:
    return [
        tuple(float(channel) for channel in color)
        for collection in _bar_collections(ax)
        for color in collection.get_colors()
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
        (segment,) = _segments(ax)
        self.assertEqual([tuple(point) for point in segment], [(1.0, 8.0), (1.0, 12.0)])

    def test_a_pair_reaches_low_below_and_high_above(self):
        ax = ScatterChart(data=[{"x": 1, "y": 10, "yerr": [1, 4]}]).axes[0]
        (segment,) = _segments(ax)
        self.assertEqual([tuple(point) for point in segment], [(1.0, 9.0), (1.0, 14.0)])

    def test_an_x_error_runs_along_the_x_axis(self):
        ax = ScatterChart(data=[{"x": 5, "y": 10, "xerr": [1, 2]}]).axes[0]
        (segment,) = _segments(ax)
        self.assertEqual(
            [tuple(point) for point in segment], [(4.0, 10.0), (7.0, 10.0)]
        )

    def test_both_axes_draw_their_own_bar(self):
        ax = ScatterChart(data=[{"x": 5, "y": 10, "xerr": 1, "yerr": 2}]).axes[0]
        self.assertEqual(len(_segments(ax)), 2)

    def test_a_point_without_an_error_draws_no_bar(self):
        ax = ScatterChart(data=POINTS).axes[0]
        along_y = [s for s in _segments(ax) if s[0][0] == s[1][0]]
        self.assertEqual([float(segment[0][0]) for segment in along_y], [1.0, 2.0])

    def test_no_error_key_draws_nothing(self):
        ax = ScatterChart(data=[{"x": 1, "y": 1}, {"x": 2, "y": 2}]).axes[0]
        self.assertEqual(_segments(ax), [])

    def test_the_show_flags_switch_the_bars_off(self):
        ax = ScatterChart(data=POINTS, show_xerr=False, show_yerr=False).axes[0]
        self.assertEqual(_segments(ax), [])
        ax = ScatterChart(data=POINTS, show_xerr=False).axes[0]
        self.assertTrue(all(s[0][0] == s[1][0] for s in _segments(ax)))

    def test_the_parameters_name_the_keys(self):
        data = [{"x": 1, "y": 10, "ci": 0.5, "sd": 2}]
        ax = ScatterChart(data=data, xerr="sd", yerr="ci").axes[0]
        along_x = [s for s in _segments(ax) if s[0][1] == s[1][1]]
        self.assertEqual(
            [tuple(point) for point in along_x[0]], [(-1.0, 10.0), (3.0, 10.0)]
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
        figure = ScatterChart(data=data, hue="hue")
        ax = figure.axes[0]
        marker_colors = [
            tuple(collection.get_facecolor()[0][:3])
            for collection in ax.collections
            if isinstance(collection, PathCollection)
        ]
        bar_colors = [color[:3] for color in _bar_colors(ax)]
        self.assertEqual(len(bar_colors), 2)
        self.assertEqual(bar_colors, marker_colors)

    def test_a_bar_takes_the_series_color(self):
        ax = ScatterChart(
            data=[{"x": 1, "y": 1, "yerr": 1}],
            style={"plot_scatter_color": "#123456"},
        ).axes[0]
        alpha = config["plot_scatter_alpha"]
        self.assertEqual(_bar_colors(ax), [to_rgba("#123456", alpha)])

    def test_the_style_color_overrides_the_point_color(self):
        ax = ScatterChart(
            data=[{"x": 1, "y": 1, "yerr": 1}],
            style={
                "plot_scatter_color": "#123456",
                "plot_scatter_error_color": "#000000",
            },
        ).axes[0]
        alpha = config["plot_scatter_alpha"]
        self.assertEqual(_bar_colors(ax), [to_rgba("#000000", alpha)])

    def test_a_muted_series_dims_its_bars(self):
        ax = ScatterChart(
            data=[[{"x": 1, "y": 1, "yerr": 1}], [{"x": 2, "y": 2, "yerr": 1}]],
            emphasis=["background", None],
        ).axes[0]
        muted = to_rgba(config["muted_color"], config["muted_alpha"])
        self.assertIn(muted, [tuple(color) for color in _bar_colors(ax)])

    def test_a_muted_point_keeps_its_bar(self):
        data = [
            {"x": 1, "y": 1, "yerr": 1, "emphasis": EMPHASIS.BACKGROUND},
            {"x": 2, "y": 2, "yerr": 1},
        ]
        ax = ScatterChart(data=data).axes[0]
        self.assertEqual(len(_segments(ax)), 2)

    def test_a_transposed_panel_swaps_the_bars(self):
        bars = BarChart(
            data=[{"label": "a", "y": 1}], orientation=ORIENTATION.HORIZONTAL
        )
        points = ScatterChart(data=[{"x": 1, "y": 10, "yerr": 2}])
        ax = Panel([bars, points]).axes[0]
        # the y error runs along the drawn x axis, where the y values sit
        (segment,) = _segments(ax)
        self.assertEqual([tuple(point) for point in segment], [(8.0, 1.0), (12.0, 1.0)])

    def test_the_bars_draw_under_their_markers(self):
        figure = ScatterChart(data=[{"x": 1, "y": 1, "yerr": 1}])
        ax = figure.axes[0]
        marks = [c for c in ax.collections if isinstance(c, PathCollection)]
        bars = _bar_collections(ax)
        self.assertLess(bars[0].get_zorder(), marks[0].get_zorder())


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
