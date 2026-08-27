"""Tests for the heatmap chart: the `{x, y, z}` data shape and axis labels."""

import unittest
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import Heatmap

Z = [[1, 2, 3], [4, 5, 6]]


def _tick_labels(ax, axis):
    return [t.get_text() for t in getattr(ax, f"get_{axis}ticklabels")()]


class TestHeatmapData(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_bare_list_raises(self):
        with self.assertRaises(ValueError) as cm:
            Heatmap(Z)
        self.assertIn('{"z": ', str(cm.exception))

    def test_bare_list_of_lists_raises(self):
        with self.assertRaises(ValueError):
            Heatmap([Z, Z])

    def test_missing_z_raises(self):
        with self.assertRaises(ValueError):
            Heatmap({"x": [1, 2, 3]})

    def test_x_length_mismatch_raises(self):
        with self.assertRaises(ValueError) as cm:
            Heatmap({"x": ["a", "b"], "z": Z})
        self.assertIn("column", str(cm.exception))

    def test_y_length_mismatch_raises(self):
        with self.assertRaises(ValueError) as cm:
            Heatmap({"y": ["r"], "z": Z})
        self.assertIn("row", str(cm.exception))

    def test_non_2d_z_raises(self):
        with self.assertRaises(ValueError):
            Heatmap({"z": [1, 2, 3]})

    def test_none_cells_render(self):
        figure = Heatmap({"z": [[1, None], [3, 4]]})
        self.assertEqual(len(figure.axes[0].images), 1)


class TestHeatmapLabels(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_x_y_become_tick_labels(self):
        figure = Heatmap({"x": ["a", "b", "c"], "y": ["r1", "r2"], "z": Z})
        figure.canvas.draw()
        ax = figure.axes[0]
        self.assertEqual(_tick_labels(ax, "x"), ["a", "b", "c"])
        self.assertEqual(_tick_labels(ax, "y"), ["r1", "r2"])
        self.assertEqual(list(ax.get_xticks()), [0, 1, 2])
        self.assertEqual(list(ax.get_yticks()), [0, 1])

    def test_numeric_labels_stay_labels(self):
        figure = Heatmap({"x": [0, 1, 5], "z": Z})
        figure.canvas.draw()
        ax = figure.axes[0]
        self.assertEqual(_tick_labels(ax, "x"), ["0", "1", "5"])
        self.assertEqual(list(ax.get_xticks()), [0, 1, 2])

    def test_explicit_xticklabels_win_over_x(self):
        figure = Heatmap(
            {"x": ["a", "b", "c"], "z": Z},
            xticks=[0, 2],
            xticklabels=["first", "last"],
        )
        figure.canvas.draw()
        ax = figure.axes[0]
        self.assertEqual(_tick_labels(ax, "x"), ["first", "last"])

    def test_xticklabels_alone_replace_x_at_cell_positions(self):
        figure = Heatmap({"x": ["a", "b", "c"], "z": Z}, xticklabels=["A", "B", "C"])
        figure.canvas.draw()
        ax = figure.axes[0]
        self.assertEqual(_tick_labels(ax, "x"), ["A", "B", "C"])
        self.assertEqual(list(ax.get_xticks()), [0, 1, 2])

    def test_absent_x_y_gives_index_labels(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            figure = Heatmap({"z": Z})
        figure.canvas.draw()
        ax = figure.axes[0]
        plain = plt.figure().add_subplot()
        plain.imshow(Z)
        plain.figure.canvas.draw()
        self.assertEqual(_tick_labels(ax, "x"), _tick_labels(plain, "x"))
        self.assertEqual(_tick_labels(ax, "y"), _tick_labels(plain, "y"))

    def test_tick_rotation_applies_to_x_labels(self):
        figure = Heatmap({"x": ["a", "b", "c"], "z": Z}, xtickrotate=45)
        figure.canvas.draw()
        ax = figure.axes[0]
        self.assertEqual(ax.get_xticklabels()[0].get_rotation(), 45)

    def test_multi_chart_labels_per_subplot(self):
        figure = Heatmap(
            [{"x": ["a", "b", "c"], "z": Z}, {"y": ["p", "q"], "z": Z}],
            subplots=True,
        )
        figure.canvas.draw()
        self.assertEqual(_tick_labels(figure.axes[0], "x"), ["a", "b", "c"])
        self.assertEqual(_tick_labels(figure.axes[1], "y"), ["p", "q"])


if __name__ == "__main__":
    unittest.main()
