"""Tests for the parallel coordinates chart: the `dimensions` broadcast."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import ParallelCoords

SET_A = [{"a": 1, "b": 2, "c": 3, "d": 9}, {"a": 2, "b": 1, "c": 4, "d": 8}]
SET_B = [{"a": 3, "b": 5, "c": 1, "d": 7}, {"a": 4, "b": 3, "c": 2, "d": 6}]


def dimension_labels(figure):
    return [t.get_text() for t in figure.axes[0].get_xticklabels()]


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


if __name__ == "__main__":
    unittest.main()
