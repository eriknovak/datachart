"""Tests for the heatmap chart: the `{x, y, z}` data shape and axis labels."""

import unittest
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors

from datachart.charts import Heatmap
from datachart.config import config
from datachart.constants import NORMALIZE, THEME

Z = [[1, 2, 3], [4, 5, 6]]
SIGNED = [[-3, -1, 0], [1, 2, 3]]


def _tick_labels(ax, axis):
    return [t.get_text() for t in getattr(ax, f"get_{axis}ticklabels")()]


class TestHeatmapData(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_bare_list_raises(self):
        with self.assertRaises(ValueError) as cm:
            Heatmap(Z)
        self.assertIn("a dict with `z`", str(cm.exception))

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
        # cells are categories: one tick per cell, at its centre, by index
        self.assertEqual(_tick_labels(ax, "x"), [str(i) for i in range(len(Z[0]))])
        self.assertEqual(_tick_labels(ax, "y"), [str(i) for i in range(len(Z))])
        self.assertEqual(list(ax.get_xticks()), list(range(len(Z[0]))))

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


class TestMarksOutsideUserLimits(unittest.TestCase):
    """A cropped cell's value is skipped (issue #174)."""

    def tearDown(self):
        plt.close("all")

    def test_cell_values_past_xmax_are_hidden(self):
        figure = Heatmap({"z": Z}, show_values=True, xmax=0.5)
        shown = [t.get_text() for t in figure.axes[0].texts if t.get_visible()]
        self.assertEqual(sorted(shown), ["1", "4"])


class TestCenteredNorm(unittest.TestCase):
    """A centred norm fixes `vcenter` in the middle of a diverging map (ADR 0056)."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_centered_norm_builds_a_centered_norm(self):
        image = Heatmap({"z": SIGNED}, norm=NORMALIZE.CENTERED).axes[0].images[0]
        self.assertIsInstance(image.norm, colors.CenteredNorm)
        self.assertEqual(image.norm.vcenter, 0)

    def test_vcenter_moves_the_centre(self):
        image = (
            Heatmap({"z": SIGNED}, norm=NORMALIZE.CENTERED, vcenter=2).axes[0].images[0]
        )
        self.assertEqual(image.norm.vcenter, 2)

    def test_autoscaled_halfrange_is_symmetric_about_the_centre(self):
        image = Heatmap({"z": SIGNED}, norm=NORMALIZE.CENTERED).axes[0].images[0]
        self.assertEqual((image.norm.vmin, image.norm.vmax), (-3, 3))

    def test_bounds_fold_into_the_larger_half_range(self):
        image = (
            Heatmap({"z": SIGNED}, norm=NORMALIZE.CENTERED, vmin=-1, vmax=4)
            .axes[0]
            .images[0]
        )
        self.assertEqual(image.norm.halfrange, 4)

    def test_twoslope_norm_keeps_the_bounds_apart(self):
        image = (
            Heatmap({"z": SIGNED}, norm=NORMALIZE.TWOSLOPE, vmin=-1, vmax=4)
            .axes[0]
            .images[0]
        )
        self.assertIsInstance(image.norm, colors.TwoSlopeNorm)
        self.assertEqual(
            (image.norm.vmin, image.norm.vcenter, image.norm.vmax), (-1, 0, 4)
        )

    def test_other_norms_still_pass_through_with_their_bounds(self):
        image = Heatmap({"z": Z}, norm=NORMALIZE.LOG, vmin=1, vmax=6).axes[0].images[0]
        self.assertIsInstance(image.norm, colors.LogNorm)
        self.assertEqual((image.norm.vmin, image.norm.vmax), (1, 6))

    def test_twoslope_bounds_missing_the_centre_raise(self):
        with self.assertRaises(ValueError) as cm:
            Heatmap({"z": Z}, norm=NORMALIZE.TWOSLOPE, vmin=1, vmax=6)
        self.assertIn("vcenter", str(cm.exception))


class TestDivergingColormap(unittest.TestCase):
    """A centred norm takes the theme's diverging colormap (ADR 0056)."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def _cmap(self, **kwargs):
        return Heatmap({"z": SIGNED}, **kwargs).axes[0].images[0].cmap.name

    def test_sequential_norm_keeps_the_theme_colormap(self):
        self.assertEqual(self._cmap(), config["plot_heatmap_cmap"])

    def test_centered_norm_takes_the_theme_diverging_colormap(self):
        self.assertEqual(
            self._cmap(norm=NORMALIZE.CENTERED), config["plot_heatmap_cmap_diverging"]
        )

    def test_twoslope_norm_takes_the_theme_diverging_colormap(self):
        self.assertEqual(
            self._cmap(norm=NORMALIZE.TWOSLOPE), config["plot_heatmap_cmap_diverging"]
        )

    def test_chart_colormap_wins_over_the_theme_diverging_one(self):
        self.assertEqual(
            self._cmap(norm=NORMALIZE.CENTERED, style={"plot_heatmap_cmap": "Greens"}),
            "Greens",
        )

    def test_chart_diverging_colormap_wins_over_the_theme(self):
        self.assertEqual(
            self._cmap(
                norm=NORMALIZE.CENTERED,
                style={"plot_heatmap_cmap_diverging": "Spectral"},
            ),
            "Spectral",
        )

    def test_theme_sequential_colormap_never_applies_under_a_centred_norm(self):
        config.update_config({"plot_heatmap_cmap": "Greens"})
        self.assertNotEqual(self._cmap(norm=NORMALIZE.CENTERED), "Greens")

    def test_a_config_without_a_diverging_map_falls_back_to_the_sequential_one(self):
        config.update_config(
            {"plot_heatmap_cmap": "Greens", "plot_heatmap_cmap_diverging": None}
        )
        self.assertEqual(self._cmap(norm=NORMALIZE.CENTERED), "Greens")


class TestCenteredColorbar(unittest.TestCase):
    """The colorbar marks the centre a centred norm holds fixed."""

    def tearDown(self):
        plt.close("all")

    def _bar_ticks(self, **kwargs):
        figure = Heatmap({"z": SIGNED}, show_colorbars=True, **kwargs)
        figure.canvas.draw()
        bar = [ax for ax in figure.axes if ax is not figure.axes[0]][0]
        return [float(t) for t in bar.get_yticks()]

    def test_user_ticks_replace_the_centre_tick(self):
        ticks = self._bar_ticks(
            norm=NORMALIZE.CENTERED, vcenter=1, colorbar={"ticks": [-2, 2]}
        )
        self.assertEqual(ticks, [-2.0, 2.0])

    def test_colorbar_ticks_include_the_centre(self):
        figure = Heatmap(
            {"z": SIGNED}, norm=NORMALIZE.CENTERED, vcenter=1, show_colorbars=True
        )
        figure.canvas.draw()
        bar = [ax for ax in figure.axes if ax is not figure.axes[0]][0]
        self.assertIn(1.0, [float(t) for t in bar.get_yticks()])


class TestCenteredValueSteps(unittest.TestCase):
    """An etched value scale breaks a step on the centre, never across it."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def _step_ranges(self, **kwargs):
        config.set_theme(THEME.QUILL)
        figure = Heatmap({"z": SIGNED}, show_colorbars=True, **kwargs)
        legend = figure.axes[0].get_children()
        (legend,) = [c for c in legend if hasattr(c, "get_texts")]
        return [t.get_text() for t in legend.get_texts()]

    def test_a_step_edge_lands_on_the_centre(self):
        ranges = self._step_ranges(norm=NORMALIZE.CENTERED)
        self.assertTrue(any(r.startswith("0 ") for r in ranges), ranges)

    def test_even_steps_stay_even_without_a_centre(self):
        ranges = self._step_ranges()
        self.assertFalse(any(r.startswith("0 ") for r in ranges[1:]), ranges)


if __name__ == "__main__":
    unittest.main()
