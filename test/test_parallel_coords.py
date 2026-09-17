"""Tests for the parallel coordinates chart: dimensions, hue scale, and axis ticks."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import ParallelCoords
from datachart.utils import Panel

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


TICK_ROWS = [
    {"a": 3.0, "b": 2.2, "c": 5.0},
    {"a": 9.0, "b": 5.0, "c": 5.0},
    {"a": 18.0, "b": 8.7, "c": 5.0},
]


def axis_ticks(figure, index):
    """One dimension axis's tick labels, as (normalized position, text) pairs."""
    pairs = [
        (round(text.get_position()[1], 6), text.get_text())
        for text in figure.axes[0].texts
        if abs(text.get_position()[0] - index) < 0.5
    ]
    return sorted(pairs)


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


class TestNumericAxisTicks(unittest.TestCase):
    """A numeric dimension snaps outward to the enclosing nice ticks."""

    def tearDown(self):
        plt.close("all")

    def test_tick_labels_are_round_values(self):
        figure = ParallelCoords(TICK_ROWS, dimensions=["a", "b"])
        self.assertEqual(
            axis_ticks(figure, 0),
            [(0.0, "0"), (0.25, "5.00"), (0.5, "10.0"), (0.75, "15.0"), (1.0, "20.0")],
        )
        self.assertEqual(
            [text for _, text in axis_ticks(figure, 1)],
            ["2.00", "4.00", "6.00", "8.00", "10.0"],
        )

    def test_the_axis_ends_on_a_tick(self):
        figure = ParallelCoords(TICK_ROWS, dimensions=["a", "b"])
        for index in (0, 1):
            positions = [position for position, _ in axis_ticks(figure, index)]
            self.assertEqual((positions[0], positions[-1]), (0.0, 1.0))

    def test_values_normalize_against_the_snapped_span(self):
        figure = ParallelCoords(TICK_ROWS, dimensions=["a", "b"])
        rows = figure.axes[0].lines[: len(TICK_ROWS)]
        # the "a" span snaps to 0-20, so 3.0 sits at 0.15 and 18.0 at 0.9
        self.assertAlmostEqual(rows[0].get_ydata()[0], 0.15)
        self.assertAlmostEqual(rows[2].get_ydata()[0], 0.9)

    def test_composed_layers_share_the_snapped_span(self):
        small = ParallelCoords([{"a": 1.0, "b": 1.0}, {"a": 3.0, "b": 2.0}])
        large = ParallelCoords([{"a": 1.0, "b": 1.0}, {"a": 18.0, "b": 2.0}])
        panel = Panel([small, large])
        # both layers read the combined 1-18 range, snapped outward to 0-20
        rows = panel.axes[0].lines[:4]
        self.assertAlmostEqual(rows[1].get_ydata()[0], 0.15)
        self.assertAlmostEqual(rows[3].get_ydata()[0], 0.9)
        self.assertEqual(axis_ticks(panel, 0)[-1], (1.0, "20.0"))

    def test_a_constant_dimension_keeps_one_tick(self):
        figure = ParallelCoords(TICK_ROWS, dimensions=["a", "c"])
        self.assertEqual(axis_ticks(figure, 1), [(0.5, "5.00")])


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
