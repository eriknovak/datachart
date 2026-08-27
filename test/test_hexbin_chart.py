"""Tests for the hexbin chart: input shapes, aggregation, style, and composition."""

import unittest

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

from datachart.charts import HexbinChart, ScatterChart, LineChart
from datachart.config import config
from datachart.constants import HEXBIN_REDUCE, NORMALIZE, COLORS, THEME
from datachart.utils import Panel, Grid
from datachart.utils._internal.config_helpers import get_hexbin_style
from datachart.utils._internal.layers import build_layers, HEXBIN_REDUCERS


def points(n=500, seed=0, center=(0.0, 0.0)):
    rng = np.random.default_rng(seed)
    xy = rng.normal(center, 1.0, (n, 2))
    return {"x": xy[:, 0].tolist(), "y": xy[:, 1].tolist()}


def points_with_c(n=500, seed=0):
    data = points(n, seed)
    data["c"] = [x + y for x, y in zip(data["x"], data["y"])]
    return data


def _hexbins(ax):
    return [c for c in ax.collections if isinstance(c, PolyCollection)]


class TestHexbinStyle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)

    def test_style_falls_back_to_heatmap_cmap(self):
        style = get_hexbin_style({})
        self.assertEqual(style["cmap"], config["plot_heatmap_cmap"])
        self.assertEqual(style["alpha"], config["plot_hexbin_alpha"])
        self.assertEqual(style["linewidths"], config["plot_hexbin_edge_width"])
        self.assertEqual(style["edgecolors"], config["plot_hexbin_edge_color"])

    def test_chart_style_overrides(self):
        style = get_hexbin_style(
            {"plot_hexbin_cmap": COLORS.Reds, "plot_hexbin_edge_width": 1.5}
        )
        self.assertEqual(style["cmap"], COLORS.Reds)
        self.assertEqual(style["linewidths"], 1.5)

    def test_every_theme_sets_the_hexbin_keys(self):
        keys = [
            "plot_hexbin_cmap",
            "plot_hexbin_alpha",
            "plot_hexbin_edge_width",
            "plot_hexbin_edge_color",
            "plot_hexbin_gridsize",
        ]
        themes = [
            THEME.DEFAULT,
            THEME.GREYSCALE,
            THEME.INK,
            THEME.HATCH,
            THEME.MINIMAL,
            THEME.MATERIAL,
        ]
        for theme in themes:
            config.set_theme(theme)
            for key in keys:
                self.assertIn(key, config.config, f"{theme} lacks {key}")


class TestHexbinLayer(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)

    def test_gridsize_defaults_to_config(self):
        layer = build_layers("hexbinchart", [{"data": points()}], {})[0]
        self.assertEqual(layer.gridsize, config["plot_hexbin_gridsize"])
        layer = build_layers("hexbinchart", [{"data": points(), "gridsize": 12}], {})[0]
        self.assertEqual(layer.gridsize, 12)
        layer = build_layers(
            "hexbinchart",
            [{"data": points(), "style": {"plot_hexbin_gridsize": 8}}],
            {},
        )[0]
        self.assertEqual(layer.gridsize, 8)

    def test_reduce_defaults_to_mean_with_c_only(self):
        layer = build_layers("hexbinchart", [{"data": points()}], {})[0]
        self.assertIsNone(layer.c)
        self.assertIsNone(layer.reduce)
        layer = build_layers("hexbinchart", [{"data": points_with_c()}], {})[0]
        self.assertEqual(len(layer.c), 500)
        self.assertIs(layer.reduce, HEXBIN_REDUCERS[HEXBIN_REDUCE.MEAN])

    def test_reduce_is_ignored_without_c(self):
        layer = build_layers(
            "hexbinchart", [{"data": points(), "reduce": HEXBIN_REDUCE.SUM}], {}
        )[0]
        self.assertIsNone(layer.reduce)

    def test_reduce_mapping(self):
        expected = {
            HEXBIN_REDUCE.MEAN: np.mean,
            HEXBIN_REDUCE.SUM: np.sum,
            HEXBIN_REDUCE.MEDIAN: np.median,
            HEXBIN_REDUCE.MIN: np.min,
            HEXBIN_REDUCE.MAX: np.max,
        }
        for name, fn in expected.items():
            layer = build_layers(
                "hexbinchart", [{"data": points_with_c(), "reduce": name}], {}
            )[0]
            self.assertIs(layer.reduce, fn)

    def test_invalid_reduce_raises(self):
        with self.assertRaises(ValueError):
            build_layers(
                "hexbinchart", [{"data": points_with_c(), "reduce": "mode"}], {}
            )

    def test_missing_columns_raise(self):
        with self.assertRaises(ValueError):
            build_layers("hexbinchart", [{"data": {"x": [1, 2, 3]}}], {})
        with self.assertRaises(ValueError):
            build_layers("hexbinchart", [{"data": {"x": [1, 2, 3], "y": [1, 2]}}], {})
        with self.assertRaises(ValueError):
            build_layers(
                "hexbinchart",
                [{"data": {"x": [1, 2, 3], "y": [1, 2, 3], "c": [1]}}],
                {},
            )

    def test_y_range(self):
        layer = build_layers(
            "hexbinchart", [{"data": {"x": [0, 1, 2], "y": [3, -1, 5]}}], {}
        )[0]
        self.assertEqual(layer.y_range(), (-1.0, 5.0))


class TestHexbinChart(unittest.TestCase):
    def tearDown(self):
        plt.close("all")
        config.set_theme(THEME.DEFAULT)

    def test_basic_counts(self):
        figure = HexbinChart(data=points(), title="Hexbin")
        ax = figure.axes[0]
        hexes = _hexbins(ax)
        self.assertEqual(len(hexes), 1)
        self.assertTrue(hexes[0].get_array().max() > 1)
        self.assertEqual(figure._suptitle.get_text(), "Hexbin")

    def test_colorbar_drawn_by_default(self):
        figure = HexbinChart(data=points())
        self.assertEqual(len(figure.axes), 2)
        figure = HexbinChart(data=points(), show_colorbars=False)
        self.assertEqual(len(figure.axes), 1)

    def test_grid_off_by_default(self):
        figure = HexbinChart(data=points())
        ax = figure.axes[0]
        self.assertFalse(any(l.get_visible() for l in ax.get_xgridlines()))
        figure = HexbinChart(data=points(), show_grid="both")
        ax = figure.axes[0]
        self.assertTrue(any(l.get_visible() for l in ax.get_xgridlines()))

    def test_log_norm(self):
        figure = HexbinChart(data=points(), norm=NORMALIZE.LOG)
        hexes = _hexbins(figure.axes[0])[0]
        self.assertIsInstance(hexes.norm, matplotlib.colors.LogNorm)

    def test_vmin_vmax(self):
        figure = HexbinChart(data=points(), vmin=0, vmax=10)
        hexes = _hexbins(figure.axes[0])[0]
        self.assertEqual((hexes.norm.vmin, hexes.norm.vmax), (0, 10))

    def test_c_aggregation_changes_values(self):
        counts = _hexbins(HexbinChart(data=points()).axes[0])[0].get_array()
        means = _hexbins(HexbinChart(data=points_with_c()).axes[0])[0].get_array()
        self.assertTrue(np.all(counts >= 0))
        self.assertTrue(np.any(means < 0))
        sums = _hexbins(
            HexbinChart(data=points_with_c(), reduce=HEXBIN_REDUCE.SUM).axes[0]
        )[0].get_array()
        self.assertFalse(np.allclose(sums, means))

    def test_mincnt_drops_sparse_cells(self):
        every = _hexbins(HexbinChart(data=points()).axes[0])[0]
        dense = _hexbins(HexbinChart(data=points(), mincnt=5).axes[0])[0]
        self.assertLess(len(dense.get_offsets()), len(every.get_offsets()))
        self.assertTrue(dense.get_array().min() >= 5)

    def test_gridsize_controls_cell_count(self):
        coarse = _hexbins(HexbinChart(data=points(), gridsize=5).axes[0])[0]
        fine = _hexbins(HexbinChart(data=points(), gridsize=30).axes[0])[0]
        self.assertLess(len(coarse.get_offsets()), len(fine.get_offsets()))

    def test_edge_style(self):
        figure = HexbinChart(
            data=points(),
            style={"plot_hexbin_edge_width": 1.0, "plot_hexbin_edge_color": "#FF0000"},
        )
        hexes = _hexbins(figure.axes[0])[0]
        self.assertEqual(hexes.get_linewidth()[0], 1.0)
        self.assertEqual(tuple(hexes.get_edgecolor()[0][:3]), (1.0, 0.0, 0.0))

    def test_cmap_override(self):
        figure = HexbinChart(data=points(), style={"plot_hexbin_cmap": COLORS.Reds})
        hexes = _hexbins(figure.axes[0])[0]
        self.assertNotEqual(hexes.get_cmap().name, config["plot_heatmap_cmap"])

    def test_emphasis_rejected(self):
        with self.assertRaises(ValueError):
            HexbinChart(data=points(), emphasis="highlight")

    def test_subplots(self):
        figure = HexbinChart(
            data=[points(seed=1), points(seed=2)],
            subtitle=["A", "B"],
            subplots=True,
        )
        # two chart axes plus a colorbar each
        self.assertEqual(len(figure.axes), 4)
        chart_axes = [ax for ax in figure.axes if _hexbins(ax)]
        self.assertEqual(len(chart_axes), 2)
        self.assertEqual(chart_axes[0].get_title(), "A")

    def test_per_chart_attrs_in_subplots(self):
        figure = HexbinChart(
            data=[points(seed=1), points_with_c(seed=2)],
            subplots=True,
            gridsize=[5, 20],
            reduce=[None, HEXBIN_REDUCE.MAX],
            show_colorbars=False,
        )
        a, b = [_hexbins(ax)[0] for ax in figure.axes]
        self.assertLess(len(a.get_offsets()), len(b.get_offsets()))

    def test_overlay_draws_every_chart(self):
        figure = HexbinChart(
            data=[points(seed=1, center=(-3, 0)), points(seed=2, center=(3, 0))],
            show_colorbars=False,
        )
        self.assertEqual(len(_hexbins(figure.axes[0])), 2)


class TestHexbinCompose(unittest.TestCase):
    def tearDown(self):
        plt.close("all")
        config.set_theme(THEME.DEFAULT)

    def test_metadata_type(self):
        figure = HexbinChart(data=points())
        self.assertEqual(figure._chart_metadata["type"], "hexbinchart")
        layers = figure._chart_metadata["panel"].layers
        self.assertEqual([layer.kind for layer in layers], ["hexbin"])

    def test_panel_with_scatter(self):
        data = points(n=100)
        scatter_points = [{"x": x, "y": y} for x, y in zip(data["x"], data["y"])]
        panel = Panel(
            [
                HexbinChart(data=data, show_colorbars=False),
                ScatterChart(data=scatter_points, subtitle="points"),
            ],
            show_legend=True,
        )
        ax = panel.axes[0]
        self.assertEqual(len(_hexbins(ax)), 1)
        self.assertEqual(len(ax.collections), 2)

    def test_grid_nesting(self):
        fig = Grid(
            [
                [HexbinChart(data=points(), title="hex")],
                [
                    LineChart(data=[{"x": i, "y": i} for i in range(5)]),
                    HexbinChart(data=points_with_c(), show_colorbars=False),
                ],
            ]
        )
        chart_axes = [ax for ax in fig.axes if _hexbins(ax)]
        self.assertEqual(len(chart_axes), 2)

    def test_grid_of_subplot_figure(self):
        inner = HexbinChart(
            data=[points(seed=1), points(seed=2)],
            subtitle=["A", "B"],
            subplots=True,
            show_colorbars=False,
        )
        fig = Grid([inner, LineChart(data=[{"x": i, "y": i} for i in range(5)])])
        self.assertEqual(len(fig.axes), 3)


if __name__ == "__main__":
    unittest.main()
