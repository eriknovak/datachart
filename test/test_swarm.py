"""Tests for the swarm chart and the panel category index."""

import unittest
import warnings

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import BoxPlot, SwarmChart
from datachart.config import config
from datachart.constants import SWARM_MODE, THEME
from datachart.utils import Panel
from datachart.utils._internal.layers import (
    SWARM_MAX_OFFSET,
    Panel as _Panel,
    beeswarm_offsets,
    strip_offsets,
)


def group_data(seed=3, n=40):
    rng = np.random.default_rng(seed)
    return [
        {"label": lab, "value": float(v)}
        for lab, mu in [("A", 10), ("B", 12), ("C", 16)]
        for v in rng.normal(mu, 2, n)
    ]


def _swarm_collections(ax):
    return [c for c in ax.collections if len(c.get_offsets())]


class TestBeeswarmOffsets(unittest.TestCase):
    def test_no_pair_overlaps(self):
        rng = np.random.default_rng(0)
        values = rng.normal(0, 10, 150)
        diameter = 6.0
        offsets = beeswarm_offsets(values, diameter)
        pts = np.column_stack([offsets, values])
        dist = np.sqrt(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1))
        dist[np.diag_indices_from(dist)] = np.inf
        self.assertGreaterEqual(dist.min(), diameter * 0.99)

    def test_offsets_stay_near_center(self):
        # candidates nearest zero win, so a sparse column stays a column
        offsets = beeswarm_offsets(np.arange(0, 100, 10.0), 6.0)
        np.testing.assert_array_equal(offsets, 0.0)

    def test_deterministic(self):
        values = np.random.default_rng(1).normal(0, 5, 80)
        np.testing.assert_array_equal(
            beeswarm_offsets(values, 5.0), beeswarm_offsets(values, 5.0)
        )


class TestStripOffsets(unittest.TestCase):
    def test_deterministic_and_bounded(self):
        a, b = strip_offsets(50, 0.4), strip_offsets(50, 0.4)
        np.testing.assert_array_equal(a, b)
        self.assertLessEqual(np.abs(a).max(), 0.2)


class TestSwarmChart(unittest.TestCase):
    def tearDown(self):
        plt.close("all")
        config.set_theme(THEME.DEFAULT)

    def test_category_ticks_and_limits(self):
        figure = SwarmChart(group_data())
        ax = figure.axes[0]
        np.testing.assert_array_equal(ax.get_xticks(), [1, 2, 3])
        self.assertEqual([t.get_text() for t in ax.get_xticklabels()], ["A", "B", "C"])
        self.assertEqual(ax.get_xlim(), (0.5, 3.5))

    def test_swarm_clamps_to_category_width(self):
        # 400 identical values pack into one row wider than the category
        data = [{"label": "A", "value": 1.0} for _ in range(400)]
        ax = SwarmChart(data).axes[0]
        xs = np.concatenate([c.get_offsets()[:, 0] for c in _swarm_collections(ax)])
        self.assertLessEqual(np.abs(xs - 1).max(), SWARM_MAX_OFFSET + 1e-9)
        self.assertGreater(np.abs(xs - 1).max(), SWARM_MAX_OFFSET * 0.9)

    def test_swarm_points_do_not_overlap_in_pixels(self):
        figure = SwarmChart(group_data(n=60))
        ax = figure.axes[0]
        size = config["plot_swarm_size"]
        diameter = np.sqrt(size) / 72 * figure.dpi
        for collection in _swarm_collections(ax):
            xy = np.asarray(collection.get_offsets())
            for pos in (1, 2, 3):
                group = xy[np.abs(xy[:, 0] - pos) <= 0.5]
                px = ax.transData.transform(group)
                dist = np.sqrt(((px[:, None, :] - px[None, :, :]) ** 2).sum(-1))
                dist[np.diag_indices_from(dist)] = np.inf
                self.assertGreaterEqual(dist.min(), diameter * 0.99)

    def test_strip_is_deterministic(self):
        first = SwarmChart(group_data(), mode=SWARM_MODE.STRIP).axes[0]
        second = SwarmChart(group_data(), mode="strip").axes[0]
        np.testing.assert_array_equal(
            _swarm_collections(first)[0].get_offsets(),
            _swarm_collections(second)[0].get_offsets(),
        )

    def test_strip_jitter_width(self):
        ax = SwarmChart(group_data(), mode="strip", jitter=0.2).axes[0]
        xs = _swarm_collections(ax)[0].get_offsets()[:, 0]
        self.assertLessEqual(np.abs(xs - np.round(xs)).max(), 0.1)

    def test_invalid_mode_raises(self):
        with self.assertRaises(ValueError):
            SwarmChart(group_data(), mode="dodge")

    def test_horizontal_orientation(self):
        ax = SwarmChart(group_data(), orientation="horizontal").axes[0]
        np.testing.assert_array_equal(ax.get_yticks(), [1, 2, 3])
        self.assertEqual(ax.get_ylim(), (0.5, 3.5))

    def test_log_scale_packs_in_display_space(self):
        data = [{"label": "A", "value": float(v)} for v in np.logspace(0, 3, 120)]
        figure = SwarmChart(data, scaley="log")
        ax = figure.axes[0]
        self.assertEqual(ax.get_yscale(), "log")
        diameter = np.sqrt(config["plot_swarm_size"]) / 72 * figure.dpi
        px = ax.transData.transform(_swarm_collections(ax)[0].get_offsets())
        dist = np.sqrt(((px[:, None, :] - px[None, :, :]) ** 2).sum(-1))
        dist[np.diag_indices_from(dist)] = np.inf
        self.assertGreaterEqual(dist.min(), diameter * 0.99)

    def test_emphasis_per_group(self):
        figure = SwarmChart(
            group_data(), emphasis=["background", None, "highlight"], subtitle="s"
        )
        ax = figure.axes[0]
        collections = _swarm_collections(ax)
        # plain, highlight, background collections
        self.assertEqual(len(collections), 3)
        by_label = {c.get_label(): c for c in collections}
        self.assertIn("s", by_label)
        background = [c for c in collections if c.get_alpha() == config["muted_alpha"]]
        self.assertEqual(len(background), 1)
        self.assertEqual(len(background[0].get_offsets()), 40)
        # one legend entry per layer
        self.assertEqual(sum(1 for c in collections if c.get_label() == "s"), 1)

    def test_emphasis_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            SwarmChart(group_data(), emphasis=["background", None])

    def test_style_keys_in_every_theme(self):
        for theme in [
            THEME.DEFAULT,
            THEME.GREYSCALE,
            THEME.INK,
            THEME.HATCH,
            THEME.MINIMAL,
            THEME.MATERIAL,
        ]:
            config.set_theme(theme)
            self.assertEqual(config["plot_swarm_zorder"], 3)
            self.assertIsNotNone(config["plot_swarm_edge_color"])

    def test_multiple_layers_overlay_at_the_center(self):
        first = group_data(seed=1)
        second = [{"label": "D", "value": 1.0}, {"label": "A", "value": 2.0}]
        ax = SwarmChart([first, second], subtitle=["one", "two"]).axes[0]
        np.testing.assert_array_equal(ax.get_xticks(), [1, 2, 3, 4])
        self.assertEqual(
            [t.get_text() for t in ax.get_xticklabels()], ["A", "B", "C", "D"]
        )
        xs = _swarm_collections(ax)[1].get_offsets()[:, 0]
        np.testing.assert_allclose(np.round(xs), [4, 1])

    def test_subplots(self):
        figure = SwarmChart([group_data(), group_data(seed=5)], subplots=True)
        self.assertEqual(len(figure.axes), 2)


class TestCategoryIndex(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_unions_labels_in_first_seen_order(self):
        box = BoxPlot([{"label": l, "value": 1.0} for l in ["B", "A"]])
        swarm = SwarmChart([{"label": l, "value": 1.0} for l in ["C", "A", "D"]])
        layers = [
            l
            for fig in (box, swarm)
            for g in fig._chart_metadata["panel"].groups
            for l in g.layers
        ]
        self.assertEqual(
            _Panel.category_index(layers), {"B": 1, "A": 2, "C": 3, "D": 4}
        )

    def test_box_swarm_overlay_shares_positions(self):
        data = group_data()
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            figure = Panel([BoxPlot(data), SwarmChart(data)], show_legend=True)
        ax = figure.axes[0]
        np.testing.assert_array_equal(ax.get_xticks(), [1, 2, 3])
        self.assertEqual([t.get_text() for t in ax.get_xticklabels()], ["A", "B", "C"])
        boxes = [p for p in ax.patches if hasattr(p, "get_path")]
        centers = [np.mean(b.get_path().vertices[:4, 0]) for b in boxes]
        np.testing.assert_allclose(centers, [1, 2, 3])
        xs = _swarm_collections(ax)[0].get_offsets()[:, 0]
        np.testing.assert_allclose(np.round(xs), np.repeat([1, 2, 3], 40))
        self.assertLessEqual(np.abs(xs - np.round(xs)).max(), SWARM_MAX_OFFSET + 1e-9)

    def test_overlay_horizontal(self):
        data = group_data()
        figure = Panel(
            [
                BoxPlot(data, orientation="horizontal"),
                SwarmChart(data, orientation="horizontal"),
            ]
        )
        ax = figure.axes[0]
        np.testing.assert_array_equal(ax.get_yticks(), [1, 2, 3])

    def test_packing_reads_panel_limits_and_later_layers(self):
        data = group_data(n=60)
        figure = Panel([SwarmChart(data), BoxPlot(data)], ymin=0, ymax=40)
        ax = figure.axes[0]
        self.assertEqual(ax.get_ylim(), (0.0, 40.0))
        diameter = np.sqrt(config["plot_swarm_size"]) / 72 * figure.dpi
        xy = np.asarray(_swarm_collections(ax)[0].get_offsets())
        for pos in (1, 2, 3):
            px = ax.transData.transform(xy[np.abs(xy[:, 0] - pos) <= 0.5])
            dist = np.sqrt(((px[:, None, :] - px[None, :, :]) ** 2).sum(-1))
            dist[np.diag_indices_from(dist)] = np.inf
            self.assertGreaterEqual(dist.min(), diameter * 0.99)

    def test_panel_role_mutes_box_and_swarm(self):
        data = group_data()
        figure = Panel(
            [
                {"figure": BoxPlot(data), "emphasis": "background"},
                {"figure": SwarmChart(data), "emphasis": "background"},
            ]
        )
        ax = figure.axes[0]
        boxes = [p for p in ax.patches if hasattr(p, "get_path")]
        for box in boxes:
            self.assertEqual(box.get_alpha(), config["muted_alpha"])
        for collection in _swarm_collections(ax):
            self.assertEqual(collection.get_alpha(), config["muted_alpha"])

    def test_multiple_boxes_still_require_subplots(self):
        data = group_data()
        with self.assertRaises(ValueError):
            Panel([BoxPlot(data), BoxPlot(data)])

    def test_box_alone_unchanged(self):
        ax = BoxPlot(group_data()).axes[0]
        np.testing.assert_array_equal(ax.get_xticks(), [1, 2, 3])
        self.assertEqual([t.get_text() for t in ax.get_xticklabels()], ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()
