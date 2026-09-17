"""Tests for histogram bar_mode stacking and STEP edge defaults."""

import unittest

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from datachart.charts import Histogram
from datachart.config import config
from datachart.constants import HISTOGRAM_TYPE, ORIENTATION, SCALE
from datachart.utils import Panel
from datachart.utils._internal.layers import build_chart_panel_settings

# deterministic series: combined range 0.5-2.5, num_bins=3 puts the values
# 0.5 / 1.5 / 2.5 into bins 0 / 1 / 2 with counts A=[4,2,0], B=[1,0,3]
HIST_A = [{"x": v} for v in [0.5] * 4 + [1.5] * 2]
HIST_B = [{"x": v} for v in [0.5] * 1 + [2.5] * 3]
# num_bins=3 leaves the middle bin empty: counts [100, 0, 2] over two decades
HIST_GAP = [{"x": v} for v in [0.5] * 100 + [2.5] * 2]


def container_bottoms(figure, index):
    return [p.get_y() for p in figure.axes[0].containers[index].patches]


def outline_vertices(figure):
    return np.asarray(figure.axes[0].patches[0].get_xy(), dtype=float)


class TestHistogramBarMode(unittest.TestCase):
    def setUp(self):
        config.reset_config()

    def tearDown(self):
        config.reset_config()
        plt.close("all")

    def test_panel_settings_default_stack_for_histograms(self):
        settings = build_chart_panel_settings("histogram", {}, "single", {})
        self.assertEqual(settings["bar_mode"], "stack")

    def test_panel_settings_default_group_for_bars(self):
        settings = build_chart_panel_settings("barchart", {}, "single", {})
        self.assertEqual(settings["bar_mode"], "group")

    def test_panel_settings_explicit_bar_mode_passes_through(self):
        settings = build_chart_panel_settings(
            "histogram", {"bar_mode": "overlay"}, "single", {}
        )
        self.assertEqual(settings["bar_mode"], "overlay")

    def test_default_stacks_multiple_series(self):
        figure = Histogram([HIST_A, HIST_B], num_bins=3)
        self.assertEqual(container_bottoms(figure, 0), [0, 0, 0])
        self.assertEqual(container_bottoms(figure, 1), [4, 2, 0])

    def test_overlay_draws_each_series_from_zero(self):
        figure = Histogram([HIST_A, HIST_B], num_bins=3, bar_mode="overlay")
        self.assertEqual(container_bottoms(figure, 0), [0, 0, 0])
        self.assertEqual(container_bottoms(figure, 1), [0, 0, 0])

    def test_group_behaves_as_overlay_for_histograms(self):
        figure = Histogram([HIST_A, HIST_B], num_bins=3, bar_mode="group")
        self.assertEqual(container_bottoms(figure, 1), [0, 0, 0])

    def test_stacked_density_normalizes_the_whole_stack(self):
        figure = Histogram([HIST_A, HIST_B], num_bins=3, show_density=True)
        area = sum(
            p.get_height() * p.get_width()
            for c in figure.axes[0].containers
            for p in c.patches
        )
        self.assertAlmostEqual(area, 1.0)

    def test_stacked_cumulative_accumulates_per_series_counts(self):
        figure = Histogram([HIST_A, HIST_B], num_bins=3, show_cumulative=True)
        heights_a = [p.get_height() for p in figure.axes[0].containers[0].patches]
        bottoms_b = container_bottoms(figure, 1)
        self.assertEqual(heights_a, [4, 6, 6])
        self.assertEqual(bottoms_b, [4, 6, 6])

    def test_single_series_needs_no_stack(self):
        figure = Histogram(HIST_A, num_bins=3)
        heights = [p.get_height() for p in figure.axes[0].containers[0].patches]
        self.assertEqual(sum(heights), 6)

    def test_panel_composition_stacks_histograms(self):
        f1 = Histogram(HIST_A, num_bins=3, subtitle="a")
        f2 = Histogram(HIST_B, num_bins=3, subtitle="b")
        panel = Panel([{"figure": f1}, {"figure": f2}], bar_mode="stack")
        bottoms = [p.get_y() for p in panel.axes[0].containers[1].patches]
        self.assertEqual(bottoms, [4, 2, 0])

    def test_panel_composition_default_overlays(self):
        f1 = Histogram(HIST_A, num_bins=3, subtitle="a")
        f2 = Histogram(HIST_B, num_bins=3, subtitle="b")
        panel = Panel([{"figure": f1}, {"figure": f2}])
        bottoms = [p.get_y() for p in panel.axes[0].containers[1].patches]
        self.assertEqual(bottoms, [0, 0, 0])


class TestStepEdgeDefaults(unittest.TestCase):
    def setUp(self):
        config.reset_config()

    def tearDown(self):
        config.reset_config()
        plt.close("all")

    def test_step_edge_follows_series_color(self):
        figure = Histogram(HIST_A, num_bins=3, style={"plot_hist_type": "step"})
        patch = figure.axes[0].patches[0]
        edge = matplotlib.colors.to_hex(patch.get_edgecolor())
        self.assertNotEqual(edge.lower(), "#ffffff")
        # the outline is the series mark: it carries the series color
        face = matplotlib.colors.to_hex(patch.get_facecolor())
        self.assertEqual(edge, face)

    def test_step_edge_width_defaults_to_line_width(self):
        figure = Histogram(HIST_A, num_bins=3, style={"plot_hist_type": "step"})
        patch = figure.axes[0].patches[0]
        self.assertEqual(patch.get_linewidth(), config["plot_line_width"])

    def test_explicit_edge_style_wins_over_step_defaults(self):
        figure = Histogram(
            HIST_A,
            num_bins=3,
            style={
                "plot_hist_type": "step",
                "plot_hist_edge_color": "#000000",
                "plot_hist_edge_width": 3.0,
            },
        )
        patch = figure.axes[0].patches[0]
        self.assertEqual(matplotlib.colors.to_hex(patch.get_edgecolor()), "#000000")
        self.assertEqual(patch.get_linewidth(), 3.0)

    def test_filled_types_keep_theme_edges(self):
        figure = Histogram(HIST_A, num_bins=3)
        patch = figure.axes[0].containers[0].patches[0]
        self.assertEqual(
            matplotlib.colors.to_hex(patch.get_edgecolor()),
            config["plot_hist_edge_color"].lower(),
        )
        self.assertEqual(patch.get_linewidth(), config["plot_hist_edge_width"])

    def test_multi_series_step_stacks_as_filled(self):
        figure = Histogram(
            [HIST_A, HIST_B], num_bins=3, style={"plot_hist_type": "step"}
        )
        patches = figure.axes[0].patches
        self.assertTrue(all(p.get_fill() for p in patches))

    def test_multi_series_step_overlay_keeps_outlines(self):
        figure = Histogram(
            [HIST_A, HIST_B],
            num_bins=3,
            bar_mode="overlay",
            style={"plot_hist_type": "step"},
        )
        patches = figure.axes[0].patches
        self.assertTrue(all(not p.get_fill() for p in patches))
        edges = {matplotlib.colors.to_hex(p.get_edgecolor()) for p in patches}
        self.assertEqual(len(edges), 2)


class TestCumulativeStepEnd(unittest.TestCase):
    """A cumulative step outline ends at its total, with no drop back to zero."""

    def setUp(self):
        config.reset_config()

    def tearDown(self):
        config.reset_config()
        plt.close("all")

    def test_cumulative_step_ends_at_its_total(self):
        figure = Histogram(
            HIST_A,
            num_bins=3,
            show_cumulative=True,
            style={"plot_hist_type": HISTOGRAM_TYPE.STEP},
        )
        vertices = outline_vertices(figure)
        self.assertEqual(vertices[-1][1], 6)
        # only the closing drop goes: the initial rise from zero stays
        self.assertEqual(vertices[0][1], 0)
        self.assertEqual(len(vertices), 2 * 3 + 1)

    def test_horizontal_cumulative_step_ends_at_its_total(self):
        figure = Histogram(
            HIST_A,
            num_bins=3,
            show_cumulative=True,
            orientation=ORIENTATION.HORIZONTAL,
            style={"plot_hist_type": HISTOGRAM_TYPE.STEP},
        )
        vertices = outline_vertices(figure)
        self.assertEqual(vertices[-1][0], 6)
        self.assertEqual(vertices[0][0], 0)

    def test_plain_step_keeps_its_closing_drop(self):
        figure = Histogram(
            HIST_A, num_bins=3, style={"plot_hist_type": HISTOGRAM_TYPE.STEP}
        )
        vertices = outline_vertices(figure)
        # a plain histogram's fall to zero is a true count
        self.assertEqual(vertices[-1][1], 0)
        self.assertEqual(len(vertices), 2 * 3 + 2)

    def test_cumulative_step_filled_keeps_its_closing_drop(self):
        figure = Histogram(
            HIST_A,
            num_bins=3,
            show_cumulative=True,
            style={"plot_hist_type": HISTOGRAM_TYPE.STEP_FILLED},
        )
        vertices = outline_vertices(figure)
        # a filled step is an area: it needs the closing edge
        self.assertEqual(vertices[-1][1], 0)

    def test_stacked_cumulative_step_keeps_its_closing_drop(self):
        figure = Histogram(
            [HIST_A, HIST_B],
            num_bins=3,
            show_cumulative=True,
            style={"plot_hist_type": HISTOGRAM_TYPE.STEP},
        )
        for patch in figure.axes[0].patches:
            # a stacked slot draws as a filled step: it closes on its bottom
            vertices = np.asarray(patch.get_xy(), dtype=float)
            self.assertEqual(vertices[-1].tolist(), vertices[0].tolist())


class TestLogStepGaps(unittest.TestCase):
    """A log value axis has no zero: the step outline breaks over the drops to it."""

    def setUp(self):
        config.reset_config()

    def tearDown(self):
        config.reset_config()
        plt.close("all")

    def step(self, data=HIST_GAP, **kwargs):
        kwargs.setdefault("num_bins", 3)
        kwargs.setdefault("style", {"plot_hist_type": HISTOGRAM_TYPE.STEP})
        return outline_vertices(Histogram(data, **kwargs))

    def test_log_step_breaks_over_an_empty_bin(self):
        values = self.step(scaley=SCALE.LOG)[:, 1]
        self.assertTrue(np.isnan(values[[0, 3, 4, 7]]).all())
        self.assertEqual(values[np.isfinite(values)].tolist(), [100, 100, 2, 2])

    def test_log_step_gaps_count_the_empty_bins_and_the_ends(self):
        values = self.step(scaley=SCALE.LOG)[:, 1]
        # two vertices per empty bin, plus the rise in and the drop out
        self.assertEqual(int(np.isnan(values).sum()), 2 * 1 + 2)

    def test_linear_step_keeps_its_zeros(self):
        values = self.step()[:, 1]
        self.assertFalse(np.isnan(values).any())
        self.assertEqual(int((values == 0).sum()), 4)

    def test_horizontal_log_step_breaks_on_the_value_axis(self):
        vertices = self.step(scalex=SCALE.LOG, orientation=ORIENTATION.HORIZONTAL)
        # the counts run along x when the histogram lies down
        self.assertEqual(int(np.isnan(vertices[:, 0]).sum()), 4)
        self.assertFalse(np.isnan(vertices[:, 1]).any())

    def test_panel_log_breaks_an_inherited_step_outline(self):
        figure = Histogram(
            HIST_GAP, num_bins=3, style={"plot_hist_type": HISTOGRAM_TYPE.STEP}
        )
        panel = Panel([{"figure": figure}], scaley=SCALE.LOG)
        self.assertEqual(int(np.isnan(outline_vertices(panel)[:, 1]).sum()), 4)

    def test_cumulative_log_step_keeps_only_its_opening_gap(self):
        values = self.step(scaley=SCALE.LOG, show_cumulative=True)[:, 1]
        # the closing drop is already gone; the rise from zero becomes the gap
        self.assertTrue(np.isnan(values[0]))
        self.assertEqual(int(np.isnan(values).sum()), 1)
        self.assertEqual(values[-1], 102)

    def test_log_step_filled_keeps_its_zeros(self):
        values = self.step(
            scaley=SCALE.LOG, style={"plot_hist_type": HISTOGRAM_TYPE.STEP_FILLED}
        )[:, 1]
        # a filled step needs its baseline to have an area at all
        self.assertFalse(np.isnan(values).any())

    def test_log_step_draws_no_spike_into_the_gap(self):
        def inked_rows(scale):
            figure = Histogram(
                HIST_GAP,
                num_bins=3,
                scaley=scale,
                style={"plot_hist_type": HISTOGRAM_TYPE.STEP},
            )
            figure.canvas.draw()
            image = np.asarray(figure.canvas.buffer_rgba())[:, :, :3]
            ink = (image != image[0, 0]).any(axis=2)
            # the column where the outline falls into the empty bin
            edge = outline_vertices(figure)[3][0]
            column = int(round(figure.axes[0].transData.transform((edge, 1))[0]))
            return int(ink[:, column].sum())

        # the renderer breaks the path where the linear outline drops
        self.assertLess(inked_rows(SCALE.LOG) * 5, inked_rows(SCALE.LINEAR))


if __name__ == "__main__":
    unittest.main()


class TestListValuedPoints(unittest.TestCase):
    """A point may carry one observation or a list of them (issue #233)."""

    def tearDown(self):
        plt.close("all")

    def bin_counts(self, figure, index=0):
        return [p.get_height() for p in figure.axes[0].containers[index].patches]

    def test_one_point_holding_every_observation(self):
        values = [v["x"] for v in HIST_A]
        listed = Histogram([{"x": values}], num_bins=3)
        scalars = Histogram(HIST_A, num_bins=3)
        self.assertEqual(self.bin_counts(listed), self.bin_counts(scalars))

    def test_several_points_pool_their_observations(self):
        split = [{"x": [0.5] * 4}, {"x": [1.5] * 2}]
        self.assertEqual(
            self.bin_counts(Histogram(split, num_bins=3)),
            self.bin_counts(Histogram(HIST_A, num_bins=3)),
        )

    def test_points_of_unequal_length_pool_too(self):
        ragged = [{"x": [0.5, 0.5, 0.5]}, {"x": [0.5, 1.5]}, {"x": [1.5]}]
        self.assertEqual(
            self.bin_counts(Histogram(ragged, num_bins=3)),
            self.bin_counts(Histogram(HIST_A, num_bins=3)),
        )

    def test_a_step_histogram_draws_one_outline(self):
        figure = Histogram(
            [{"x": [v["x"] for v in HIST_A]}],
            num_bins=3,
            style={"plot_hist_type": HISTOGRAM_TYPE.STEP},
        )
        self.assertEqual(len(figure.axes[0].patches), 1)

    def test_a_mixed_series_keeps_its_own_bins(self):
        figure = Histogram([[{"x": [v["x"] for v in HIST_A]}], HIST_B], num_bins=3)
        self.assertEqual(len(figure.axes[0].containers), 2)
