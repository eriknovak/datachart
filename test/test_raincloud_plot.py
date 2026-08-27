"""Tests for the raincloud plot: layer offsets, per-group colors, and composition."""

import unittest

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.patches import PathPatch

from datachart.charts import RaincloudPlot, LineChart
from datachart.config import config
from datachart.constants import THEME
from datachart.utils import Panel, Grid
from datachart.utils._internal.colors import create_color_cycle
from datachart.utils._internal.layers import (
    RAINCLOUD_RAIN_OFFSET,
    RAINCLOUD_RAIN_SPREAD,
    RAINCLOUD_BOX_WIDTH,
    build_layers,
)


def group_data(seed=3, n=40):
    rng = np.random.default_rng(seed)
    return [
        {"label": lab, "value": float(v)}
        for lab, mu in [("A", 10), ("B", 12), ("C", 16)]
        for v in rng.normal(mu, 2, n)
    ]


def _swarm_collections(ax):
    return [c for c in ax.collections if isinstance(c, PathCollection)]


def _violin_bodies(ax):
    return [c for c in ax.collections if isinstance(c, PolyCollection)]


def _box_patches(ax):
    return [p for p in ax.patches if isinstance(p, PathPatch)]


class TestRaincloudLayers(unittest.TestCase):
    def tearDown(self):
        plt.close("all")
        config.set_theme(THEME.DEFAULT)

    def test_build_layers_yields_cloud_rain_box_per_dataset(self):
        charts = [{"data": group_data()}, {"data": group_data(seed=4)}]
        layers = build_layers("raincloudplot", charts, {"orientation": "vertical"})
        self.assertEqual([l.kind for l in layers], ["violin", "swarm", "box"] * 2)
        self.assertIs(layers[0].chart, layers[2].chart)

    def test_vertical_cloud_left_rain_and_box_right(self):
        figure = RaincloudPlot(group_data())
        ax = figure.axes[0]
        # cloud: every body vertex stays at or left of its category position
        for pos, body in enumerate(_violin_bodies(ax), start=1):
            xs = np.concatenate([p.vertices[:, 0] for p in body.get_paths()])
            self.assertLessEqual(xs.max(), pos + 1e-9)
            self.assertLess(xs.min(), pos - 0.1)
        # rain: one-sided, packed outward from p + offset over the spread
        xy = np.concatenate([c.get_offsets() for c in _swarm_collections(ax)])
        for pos in (1, 2, 3):
            xs = xy[np.abs(xy[:, 0] - pos) <= 0.5][:, 0] - pos
            self.assertTrue(len(xs))
            self.assertGreaterEqual(xs.min(), RAINCLOUD_RAIN_OFFSET - 1e-9)
            self.assertLessEqual(
                xs.max(), RAINCLOUD_RAIN_OFFSET + RAINCLOUD_RAIN_SPREAD + 1e-9
            )
            self.assertGreater(xs.max() - xs.min(), 0.05)
        # box: the rain-side half on the cloud's seam, an outline
        boxes = _box_patches(ax)
        self.assertEqual(len(boxes), 3)
        for pos, box in enumerate(boxes, start=1):
            xs = box.get_path().vertices[:, 0]
            self.assertAlmostEqual(xs.min(), pos)
            self.assertAlmostEqual(xs.max() - xs.min(), RAINCLOUD_BOX_WIDTH / 2)
            self.assertEqual(box.get_facecolor()[3], 0.0)

    def test_horizontal_cloud_above_rain_below(self):
        figure = RaincloudPlot(group_data(), orientation="horizontal")
        ax = figure.axes[0]
        for pos, body in enumerate(_violin_bodies(ax), start=1):
            ys = np.concatenate([p.vertices[:, 1] for p in body.get_paths()])
            self.assertGreaterEqual(ys.min(), pos - 1e-9)
        xy = np.concatenate([c.get_offsets() for c in _swarm_collections(ax)])
        self.assertLessEqual(xy[:, 1].max(), 3 - RAINCLOUD_RAIN_OFFSET + 1e-9)
        for pos, box in enumerate(_box_patches(ax), start=1):
            ys = box.get_path().vertices[:, 1]
            self.assertAlmostEqual(ys.max(), pos)
            self.assertAlmostEqual(ys.max() - ys.min(), RAINCLOUD_BOX_WIDTH / 2)

    def test_strip_rain_stays_inside_spread(self):
        figure = RaincloudPlot(group_data(), mode="strip")
        xy = np.concatenate(
            [c.get_offsets() for c in _swarm_collections(figure.axes[0])]
        )
        off = (
            xy[:, 0]
            - np.round(xy[:, 0] - RAINCLOUD_RAIN_OFFSET)
            - RAINCLOUD_RAIN_OFFSET
        )
        self.assertLessEqual(np.abs(off).max(), RAINCLOUD_RAIN_SPREAD + 1e-9)

    def test_cloud_and_rain_share_group_color(self):
        figure = RaincloudPlot(group_data(), show_legend=True)
        ax = figure.axes[0]
        cycle = create_color_cycle(config["color_general_multiple"], 3)
        expected = [matplotlib.colors.to_rgb(cycle[i]["color"]) for i in range(3)]
        bodies = _violin_bodies(ax)
        rain = _swarm_collections(ax)
        self.assertEqual(len(rain), 3)
        for i in range(3):
            self.assertEqual(tuple(bodies[i].get_facecolor()[0][:3]), expected[i])
            self.assertEqual(tuple(rain[i].get_facecolor()[0][:3]), expected[i])
        legend = ax.get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["A", "B", "C"])

    def test_box_outline_uses_font_color(self):
        figure = RaincloudPlot(group_data())
        ax = figure.axes[0]
        font = matplotlib.colors.to_rgb(config["font_general_color"])
        box = _box_patches(ax)[0]
        self.assertEqual(tuple(box.get_edgecolor()[:3]), font)
        medians = [l for l in ax.lines if len(l.get_xdata()) == 2]
        self.assertTrue(medians)
        self.assertEqual(matplotlib.colors.to_rgb(medians[0].get_color()), font)

    def test_emphasis_applies_to_all_three_parts(self):
        figure = RaincloudPlot(group_data(), emphasis=["background", None, None])
        ax = figure.axes[0]
        muted = matplotlib.colors.to_rgb(config["muted_color"])
        self.assertEqual(tuple(_violin_bodies(ax)[0].get_facecolor()[0][:3]), muted)
        self.assertEqual(tuple(_swarm_collections(ax)[0].get_facecolor()[0][:3]), muted)
        self.assertEqual(tuple(_box_patches(ax)[0].get_edgecolor()[:3]), muted)

    def test_rain_point_size_default_and_override(self):
        figure = RaincloudPlot(group_data())
        self.assertEqual(_swarm_collections(figure.axes[0])[0].get_sizes()[0], 6)
        figure = RaincloudPlot(group_data(), style={"plot_swarm_size": 20})
        self.assertEqual(_swarm_collections(figure.axes[0])[0].get_sizes()[0], 20)

    def test_invalid_bandwidth_raises(self):
        with self.assertRaises(ValueError):
            RaincloudPlot(group_data(), bandwidth="nope")

    def test_subplots_group_the_three_layers_per_axes(self):
        figure = RaincloudPlot([group_data(), group_data(seed=4)], subplots=True)
        axes = [ax for ax in figure.axes if ax.axison]
        self.assertEqual(len(axes), 2)
        for ax in axes:
            self.assertEqual(len(_violin_bodies(ax)), 3)
            self.assertEqual(len(_swarm_collections(ax)), 3)
            self.assertEqual(len(_box_patches(ax)), 3)
        self.assertEqual(figure._chart_metadata["type"], "raincloudplot")
        self.assertEqual(len(figure._chart_metadata["panels"]), 2)

    def test_composes_in_panel_and_grid(self):
        rc = RaincloudPlot(group_data())
        line = LineChart([{"x": i, "y": 10 + i} for i in range(1, 4)])
        panel = Panel([rc, line])
        ax = panel.axes[0]
        self.assertEqual(len(_violin_bodies(ax)), 3)
        self.assertEqual(len(_box_patches(ax)), 3)
        grid = Grid([[RaincloudPlot(group_data()), line]])
        self.assertGreaterEqual(len(grid.axes), 2)


if __name__ == "__main__":
    unittest.main()
