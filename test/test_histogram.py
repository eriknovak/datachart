"""Tests for histogram bar_mode stacking and STEP edge defaults."""

import unittest

import matplotlib
import matplotlib.pyplot as plt

from datachart.charts import Histogram
from datachart.config import config
from datachart.utils import Panel
from datachart.utils._internal.layers import build_chart_panel_settings

# deterministic series: combined range 0.5-2.5, num_bins=3 puts the values
# 0.5 / 1.5 / 2.5 into bins 0 / 1 / 2 with counts A=[4,2,0], B=[1,0,3]
HIST_A = [{"x": v} for v in [0.5] * 4 + [1.5] * 2]
HIST_B = [{"x": v} for v in [0.5] * 1 + [2.5] * 3]


def container_bottoms(figure, index):
    return [p.get_y() for p in figure.axes[0].containers[index].patches]


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


if __name__ == "__main__":
    unittest.main()
