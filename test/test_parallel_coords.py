"""Tests for the parallel coordinates chart: dimensions, hue scale, and axis ticks."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import ParallelCoords

SET_A = [{"a": 1, "b": 2, "c": 3, "d": 9}, {"a": 2, "b": 1, "c": 4, "d": 8}]
SET_B = [{"a": 3, "b": 5, "c": 1, "d": 7}, {"a": 4, "b": 3, "c": 2, "d": 6}]


HUE_ROWS = [
    {"p": 1.0, "q": 2.0, "mass": 2725.0},
    {"p": 2.0, "q": 1.0, "mass": 4000.0},
    {"p": 3.0, "q": 3.0, "mass": 5708.0},
    {"p": 4.0, "q": 4.0, "mass": 6169.0},
]


def dimension_labels(figure):
    return [t.get_text() for t in figure.axes[0].get_xticklabels()]


def parallel_layer(figure):
    return figure._chart_metadata["panel"].layers[0]


class TestDimensions(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_single_set_uses_the_given_order(self):
        figure = ParallelCoords(SET_A, dimensions=["c", "a"])
        self.assertEqual(dimension_labels(figure), ["c", "a"])

    def test_flat_list_applies_to_every_set(self):
        figure = ParallelCoords([SET_A, SET_B], dimensions=["c", "a", "b"])
        self.assertEqual(dimension_labels(figure), ["c", "a", "b"])

    def test_equal_list_of_lists_applies_per_set(self):
        figure = ParallelCoords(
            [SET_A, SET_B], dimensions=[["b", "a", "c"], ["b", "a", "c"]]
        )
        self.assertEqual(dimension_labels(figure), ["b", "a", "c"])

    def test_list_of_lists_with_a_missing_entry_detects_that_set(self):
        figure = ParallelCoords([SET_A, SET_B], dimensions=[None, ["a", "b", "c", "d"]])
        self.assertEqual(dimension_labels(figure), ["a", "b", "c", "d"])

    def test_different_list_of_lists_raises(self):
        with self.assertRaisesRegex(ValueError, "must share the same dimensions"):
            ParallelCoords([SET_A, SET_B], dimensions=[["a", "b"], ["b", "a"]])

    def test_sets_without_dimensions_detect_every_column(self):
        figure = ParallelCoords([SET_A, SET_B])
        self.assertEqual(dimension_labels(figure), ["a", "b", "c", "d"])


class TestHueScale(unittest.TestCase):
    """A numeric hue ramp spans every record: the emphasis rule mutes, it does not rescale."""

    def tearDown(self):
        plt.close("all")

    def test_emphasis_rule_keeps_the_full_hue_range(self):
        figure = ParallelCoords(HUE_ROWS, hue="mass", emphasis_rule={"top": 2})
        layer = parallel_layer(figure)
        self.assertEqual((layer.hue_min, layer.hue_max), (2725.0, 6169.0))

    def test_background_rows_keep_the_full_hue_range(self):
        figure = ParallelCoords(
            HUE_ROWS,
            hue="mass",
            emphasis=["background", "background", "highlight", "highlight"],
        )
        layer = parallel_layer(figure)
        self.assertEqual((layer.hue_min, layer.hue_max), (2725.0, 6169.0))

    def test_a_background_only_numeric_hue_still_reads_as_continuous(self):
        figure = ParallelCoords(
            HUE_ROWS, hue="mass", emphasis=["background"] * len(HUE_ROWS)
        )
        self.assertTrue(parallel_layer(figure).continuous_hue)

    def test_a_categorical_hue_skips_background_rows_in_the_legend(self):
        rows = [dict(row, kind=kind) for row, kind in zip(HUE_ROWS, "aabb")]
        figure = ParallelCoords(
            rows,
            hue="kind",
            dimensions=["p", "q"],
            emphasis=["background", "background", "highlight", "highlight"],
        )
        self.assertEqual(parallel_layer(figure).unique_hues, ["b"])


if __name__ == "__main__":
    unittest.main()
