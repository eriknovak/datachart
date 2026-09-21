"""Tests for scatter error bars (ADR 0057): validation, style, drawing, and hover."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.config import config
from datachart.config.configuration import THEMES
from datachart.constants import THEME
from datachart.utils._internal.config_helpers import get_scatter_error_style
from datachart.utils._internal.validate import validate_error_distances

ERROR_KEYS = (
    "plot_scatter_error_color",
    "plot_scatter_error_width",
    "plot_scatter_error_capsize",
)

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


class TestErrorFrontParameters(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_the_front_takes_the_error_parameters(self):
        from datachart.charts import ScatterChart

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
