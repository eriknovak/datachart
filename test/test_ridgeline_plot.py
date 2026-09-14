"""Tests for the ridgeline plot (ADR 0047)."""

import unittest
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection, PolyCollection
import numpy as np

from datachart.charts import RidgelinePlot, SwarmPlot
from datachart.config import config
from datachart.constants import RIDGELINE_SCALE, SORT, THEME
from datachart.themes import _base
from datachart.utils import Grid, Panel

THEMES = [
    THEME.DEFAULT,
    THEME.GREYSCALE,
    THEME.INK,
    THEME.HATCH,
    THEME.MINIMAL,
    THEME.MATERIAL,
    THEME.SKETCH,
]
RIDGELINE_KEYS = (
    "plot_ridgeline_color",
    "plot_ridgeline_alpha",
    "plot_ridgeline_linewidth",
    "plot_ridgeline_edgecolor",
    "plot_ridgeline_overlap",
    "plot_ridgeline_inner_color",
    "plot_ridgeline_inner_linewidth",
)


def ridge_data(centres=(0.0, 1.0, 2.0), labels="ABC", n=40, scales=None):
    rng = np.random.RandomState(4)
    scales = scales or [1.0] * len(labels)
    return [
        {"label": lab, "value": float(v)}
        for lab, centre, scale in zip(labels, centres, scales)
        for v in rng.randn(n) * scale + centre
    ]


def fills(ax):
    return [c for c in ax.collections if isinstance(c, PolyCollection)]


def rise(fill, position, horizontal=True):
    """How far a ridge fill reaches from its row edge, in category slots."""

    vertices = fill.get_paths()[0].vertices[:, 1 if horizontal else 0]
    if horizontal:
        return position - vertices.min()
    return vertices.max() - position


class TestRidgelineLayout(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_rows_read_top_to_bottom_in_input_order(self):
        ax = RidgelinePlot(ridge_data(labels="CAB")).axes[0]
        self.assertEqual(len(fills(ax)), 3)
        self.assertEqual([t.get_text() for t in ax.get_yticklabels()], list("CAB"))
        self.assertEqual(list(ax.get_yticks()), [1, 2, 3])
        self.assertTrue(ax.yaxis_inverted())

    def test_later_rows_draw_above_earlier_ones(self):
        zorders = [f.get_zorder() for f in fills(RidgelinePlot(ridge_data()).axes[0])]
        self.assertEqual(zorders, sorted(zorders))
        self.assertEqual(len(set(zorders)), 3)

    def test_sort_orders_rows_by_median(self):
        data = ridge_data(centres=(2.0, 0.0, 1.0))
        ascending = RidgelinePlot(data, sort=SORT.ASCENDING).axes[0]
        self.assertEqual(
            [t.get_text() for t in ascending.get_yticklabels()], ["B", "C", "A"]
        )
        descending = RidgelinePlot(data, sort="descending").axes[0]
        self.assertEqual(
            [t.get_text() for t in descending.get_yticklabels()], ["A", "C", "B"]
        )

    def test_sort_ties_keep_input_order(self):
        data = [{"label": lab, "value": v} for lab in "BA" for v in (1.0, 2.0, 3.0)]
        ax = RidgelinePlot(data, sort="ascending").axes[0]
        self.assertEqual([t.get_text() for t in ax.get_yticklabels()], ["B", "A"])

    def test_overlap_sets_the_peak_height(self):
        for overlap in (0.0, 0.5, 1.0):
            ax = RidgelinePlot(ridge_data(), overlap=overlap).axes[0]
            for position, fill in enumerate(fills(ax), start=1):
                self.assertAlmostEqual(rise(fill, position), 1 + overlap)

    def test_theme_overlap_default(self):
        ax = RidgelinePlot(ridge_data()).axes[0]
        self.assertAlmostEqual(
            rise(fills(ax)[0], 1), 1 + config["plot_ridgeline_overlap"]
        )

    def test_per_row_scales_every_ridge_to_the_same_peak(self):
        data = ridge_data(scales=[0.5, 1.0, 3.0])
        ax = RidgelinePlot(data, overlap=0.5, normalize=RIDGELINE_SCALE.PER_ROW).axes[0]
        rises = [rise(f, p) for p, f in enumerate(fills(ax), start=1)]
        np.testing.assert_allclose(rises, [1.5, 1.5, 1.5])

    def test_common_keeps_one_density_scale(self):
        data = ridge_data(scales=[0.5, 1.0, 3.0])
        ax = RidgelinePlot(data, overlap=0.5, normalize="common").axes[0]
        rises = [rise(f, p) for p, f in enumerate(fills(ax), start=1)]
        self.assertAlmostEqual(max(rises), 1.5)
        # the narrowest spread is the densest row, the widest the flattest
        self.assertEqual(int(np.argmax(rises)), 0)
        self.assertLess(rises[2], rises[1])

    def test_ridges_share_one_grid(self):
        ax = RidgelinePlot(ridge_data(centres=(0, 5, 10)), inner=None).axes[0]
        grids = [line.get_xdata() for line in ax.lines]
        self.assertEqual(len(grids), 3)
        for grid in grids[1:]:
            np.testing.assert_array_equal(grid, grids[0])

    def test_value_limits_bound_the_grid(self):
        ax = RidgelinePlot(ridge_data(), xmin=-1.0, xmax=3.0).axes[0]
        grid = ax.lines[0].get_xdata()
        self.assertAlmostEqual(grid[0], -1.0)
        self.assertAlmostEqual(grid[-1], 3.0)

    def test_vertical_transposes(self):
        ax = RidgelinePlot(ridge_data(), orientation="vertical").axes[0]
        self.assertEqual([t.get_text() for t in ax.get_xticklabels()], list("ABC"))
        self.assertFalse(ax.xaxis_inverted())
        self.assertFalse(ax.yaxis_inverted())
        self.assertAlmostEqual(rise(fills(ax)[0], 1, horizontal=False), 1.5, places=6)
        # each vertical ridge rises from its own tick
        for position, fill in enumerate(fills(ax), start=1):
            self.assertAlmostEqual(fill.get_paths()[0].vertices[:, 0].min(), position)
        # rows rise rightward, so earlier rows draw over the later ones they reach
        zorders = [f.get_zorder() for f in fills(ax)]
        self.assertEqual(zorders, sorted(zorders, reverse=True))


class TestRidgelineMarks(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_fill_and_outline_toggle_independently(self):
        both = RidgelinePlot(ridge_data()).axes[0]
        self.assertEqual((len(fills(both)), len(both.lines)), (3, 3))
        no_fill = RidgelinePlot(ridge_data(), fill=False).axes[0]
        self.assertEqual((len(fills(no_fill)), len(no_fill.lines)), (0, 3))
        no_outline = RidgelinePlot(ridge_data(), show_outline=False).axes[0]
        self.assertEqual((len(fills(no_outline)), len(no_outline.lines)), (3, 0))

    def test_inner_marks_stop_at_the_ridge(self):
        ax = RidgelinePlot(ridge_data(), inner="median", show_outline=False).axes[0]
        self.assertEqual(len(ax.lines), 3)
        for position, (fill, mark) in enumerate(zip(fills(ax), ax.lines), start=1):
            ys = mark.get_ydata()
            self.assertAlmostEqual(max(ys), position)
            self.assertGreater(min(ys), position - rise(fill, position) - 1e-9)
        quartiles = RidgelinePlot(
            ridge_data(), inner="quartiles", show_outline=False
        ).axes[0]
        self.assertEqual(len(quartiles.lines), 9)

    def test_fill_takes_the_palette_color_and_style(self):
        ax = RidgelinePlot(
            ridge_data(), style={"plot_ridgeline_color": "#FF0000"}
        ).axes[0]
        self.assertEqual(
            matplotlib.colors.to_hex(fills(ax)[0].get_facecolor()[0]).upper(),
            "#FF0000",
        )

    def test_emphasis_mutes_and_highlights_rows(self):
        ax = RidgelinePlot(
            ridge_data(), emphasis=["background", None, "highlight"]
        ).axes[0]
        muted = fills(ax)[0]
        self.assertEqual(muted.get_alpha(), config["muted_alpha"])
        self.assertEqual(
            matplotlib.colors.to_hex(muted.get_facecolor()[0]).upper(),
            config["muted_color"],
        )
        widths = [line.get_linewidth() for line in ax.lines]
        self.assertGreater(widths[2], widths[1])
        self.assertLess(widths[0], widths[1])

    def test_emphasis_rule_reads_row_medians(self):
        ax = RidgelinePlot(ridge_data(), emphasis_rule={"top": 1}).axes[0]
        self.assertEqual(fills(ax)[0].get_alpha(), config["muted_alpha"])
        self.assertNotEqual(fills(ax)[2].get_alpha(), config["muted_alpha"])

    def test_emphasis_follows_labels_through_sort(self):
        data = ridge_data(centres=(2.0, 0.0, 1.0))
        ax = RidgelinePlot(
            data, sort="ascending", emphasis=["background", None, None]
        ).axes[0]
        # "A" has the largest median, so it is drawn last
        self.assertEqual(fills(ax)[2].get_alpha(), config["muted_alpha"])

    def test_no_legend_entries(self):
        ax = RidgelinePlot(ridge_data(), subtitle="Rows", show_legend=True).axes[0]
        self.assertEqual(ax.get_legend_handles_labels()[0], [])

    def test_label_value_remap_and_subplots(self):
        data = [{"g": g, "v": v} for g in "AB" for v in (1.0, 2.0, 4.0)]
        ax = RidgelinePlot(data, label="g", value="v").axes[0]
        self.assertEqual(len(fills(ax)), 2)
        figure = RidgelinePlot([ridge_data(), ridge_data(labels="DE")], subplots=True)
        self.assertEqual(len(figure.axes), 2)

    def test_multiple_datasets_draw_one_axes_each(self):
        figure = RidgelinePlot([ridge_data(), ridge_data()])
        self.assertEqual(len(figure.axes), 2)

    def test_single_value_row_raises(self):
        with self.assertRaises(ValueError):
            RidgelinePlot([{"label": "A", "value": 1.0}])

    def test_empty_data_warns(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            RidgelinePlot([])
        self.assertTrue(any("No data points" in str(w.message) for w in caught))


class TestRidgelineValidation(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_overlap_outside_unit_range_raises(self):
        for overlap in (-0.1, 1.5):
            with self.assertRaisesRegex(ValueError, "overlap"):
                RidgelinePlot(ridge_data(), overlap=overlap)

    def test_box_inner_raises(self):
        with self.assertRaisesRegex(ValueError, "inner"):
            RidgelinePlot(ridge_data(), inner="box")

    def test_nothing_to_draw_raises(self):
        with self.assertRaisesRegex(ValueError, "fill"):
            RidgelinePlot(ridge_data(), fill=False, show_outline=False)

    def test_invalid_normalize_and_sort_raise(self):
        with self.assertRaisesRegex(ValueError, "normalize"):
            RidgelinePlot(ridge_data(), normalize="global")
        with self.assertRaisesRegex(ValueError, "sort"):
            RidgelinePlot(ridge_data(), sort="median")
        with self.assertRaises(ValueError):
            RidgelinePlot(ridge_data(), bandwidth="gaussian")


class TestRidgelineComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_swarm_overlay_lines_up_with_the_rows(self):
        data = ridge_data()
        figure = Panel([RidgelinePlot(data), SwarmPlot(data, orientation="horizontal")])
        ax = figure.axes[0]
        self.assertEqual(len(fills(ax)), 3)
        self.assertTrue(ax.yaxis_inverted())
        swarms = [c for c in ax.collections if isinstance(c, PathCollection)]
        rows = np.concatenate([c.get_offsets()[:, 1] for c in swarms])
        # ridges rise from their tick and the points pack upward, inside them
        for position, fill in enumerate(fills(ax), start=1):
            base = fill.get_paths()[0].vertices[:, 1].max()
            self.assertAlmostEqual(base, position)
        offsets = rows - np.round(rows + 0.2)
        self.assertTrue(np.all((offsets <= 1e-9) & (offsets >= -0.4 - 1e-9)))
        self.assertLess(offsets.min(), -0.05)

    def test_swarm_without_ridges_packs_both_sides(self):
        ax = SwarmPlot(ridge_data(), orientation="horizontal").axes[0]
        rows = np.concatenate([c.get_offsets()[:, 1] for c in ax.collections])
        self.assertTrue(np.any(rows > np.round(rows) + 1e-6))
        self.assertTrue(np.any(rows < np.round(rows) - 1e-6))

    def test_panel_without_ridges_keeps_its_axis(self):
        data = ridge_data()
        ax = Panel([SwarmPlot(data, orientation="horizontal")]).axes[0]
        self.assertFalse(ax.yaxis_inverted())

    def test_grid_accepts_the_figure(self):
        figure = Grid([[RidgelinePlot(ridge_data()), RidgelinePlot(ridge_data())]])
        self.assertTrue(all(len(fills(ax)) == 3 for ax in figure.axes[:2]))


class TestRidgelineDeclarations(unittest.TestCase):
    def test_every_theme_declares_every_key(self):
        for theme in THEMES:
            config.set_theme(theme)
            for key in RIDGELINE_KEYS:
                self.assertIn(key, config.config)
        config.set_theme(THEME.DEFAULT)
        self.assertEqual(
            set(RIDGELINE_KEYS),
            {k for k in _base.BASE_THEME if k.startswith("plot_ridgeline_")},
        )

    def test_typings_and_export(self):
        from datachart import typings
        import datachart.charts as charts

        self.assertEqual(
            set(typings.RidgelineStyleAttrs.__annotations__), set(RIDGELINE_KEYS)
        )
        for key in RIDGELINE_KEYS:
            self.assertIn(key, typings.StyleAttrs.__annotations__)
        self.assertIn("value", typings.RidgelineDataPointAttrs.__annotations__)
        self.assertIn("RidgelinePlot", charts.__all__)
        self.assertEqual(
            (RIDGELINE_SCALE.PER_ROW, RIDGELINE_SCALE.COMMON), ("per_row", "common")
        )
        self.assertEqual(RIDGELINE_SCALE.DEFAULT, RIDGELINE_SCALE.PER_ROW)


if __name__ == "__main__":
    unittest.main()
