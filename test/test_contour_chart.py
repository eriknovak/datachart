"""Tests for the contour chart: grid validation, lines vs fills, levels, and composition."""

import unittest

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.contour import ContourSet
from matplotlib.lines import Line2D

from datachart.charts import ContourChart, ScatterChart, LineChart
from datachart.config import config
from datachart.constants import CONTOUR_LEVELS, COLORS, THEME
from datachart.utils import Panel, Grid
from datachart.utils._internal.colors import create_color_cycle
from datachart.utils._internal.config_helpers import (
    get_contour_style,
    get_contour_label_style,
)
from datachart.utils._internal.layers import build_layers


def surface(n=40, lo=-5, hi=5):
    x = np.linspace(lo, hi, n)
    X, Y = np.meshgrid(x, x)
    z = (X**2 + Y - 11) ** 2 + (X + Y**2 - 7) ** 2
    return {"x": x.tolist(), "y": x.tolist(), "z": z.tolist()}


def bump(mx, my, n=40):
    x = np.linspace(-5, 5, n)
    X, Y = np.meshgrid(x, x)
    z = np.exp(-((X - mx) ** 2 + (Y - my) ** 2) / 2)
    return {"x": x.tolist(), "y": x.tolist(), "z": z.tolist()}


def _contour_sets(ax):
    return [c for c in ax.collections if isinstance(c, ContourSet)]


def _proxies(ax):
    return [l for l in ax.lines if isinstance(l, Line2D) and len(l.get_xdata()) == 0]


class TestContourStyle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)

    def test_style_falls_back_to_heatmap_cmap_and_line_width(self):
        style = get_contour_style({})
        self.assertEqual(style["cmap"], config["plot_heatmap_cmap"])
        self.assertEqual(style["linewidths"], config["plot_line_width"])
        self.assertNotIn("color", style)

    def test_chart_style_overrides(self):
        style = get_contour_style(
            {"plot_contour_cmap": COLORS.Reds, "plot_contour_line_width": 3}
        )
        self.assertEqual(style["cmap"], COLORS.Reds)
        self.assertEqual(style["linewidths"], 3)

    def test_label_style_derives_font_size(self):
        style = get_contour_label_style({})
        self.assertEqual(style["fontsize"], config["font_general_size"] - 2)
        self.assertNotIn("colors", style)
        style = get_contour_label_style({"plot_contour_label_font_color": "#123456"})
        self.assertEqual(style["colors"], "#123456")


class TestContourValidation(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_z_must_be_2d(self):
        with self.assertRaises(ValueError):
            ContourChart(data={"z": [1, 2, 3]})

    def test_x_length_must_match_columns(self):
        data = surface()
        data["x"] = data["x"][:-1]
        with self.assertRaisesRegex(ValueError, "per column"):
            ContourChart(data=data)

    def test_y_length_must_match_rows(self):
        data = surface()
        data["y"] = data["y"] + [1.0]
        with self.assertRaisesRegex(ValueError, "per row"):
            ContourChart(data=data)

    def test_missing_z(self):
        with self.assertRaises(ValueError):
            ContourChart(data={"x": [0, 1]})

    def test_emphasis_rejected_when_filled(self):
        with self.assertRaises(ValueError):
            ContourChart(data=surface(), filled=True, emphasis="highlight")

    def test_invalid_levels_rule(self):
        with self.assertRaises(ValueError):
            ContourChart(data=surface(), levels="sturges")


class TestContourDraw(unittest.TestCase):
    def tearDown(self):
        plt.close("all")
        config.set_theme(THEME.DEFAULT)

    def test_indices_default_axes(self):
        z = [[0, 1, 2], [1, 2, 3]]
        layers = build_layers("contourchart", [{"data": {"z": z}}], {})
        np.testing.assert_array_equal(layers[0].x, [0, 1, 2])
        np.testing.assert_array_equal(layers[0].y, [0, 1])
        self.assertEqual(layers[0].y_range(), (0.0, 1.0))

    def test_lines_take_cycle_color_and_grid(self):
        figure = ContourChart(data=surface())
        ax = figure.axes[0]
        sets = _contour_sets(ax)
        self.assertEqual(len(sets), 1)
        expected = matplotlib.colors.to_rgb(
            create_color_cycle(config["color_general_multiple"], 1)[0]["color"]
        )
        self.assertEqual(tuple(sets[0].get_edgecolor()[0][:3]), expected)
        self.assertFalse(sets[0].filled)
        self.assertTrue(ax.yaxis.get_gridlines()[0].get_visible())

    def test_filled_uses_cmap_no_grid_and_colorbar(self):
        figure = ContourChart(data=surface(), filled=True, show_colorbars=True)
        ax = figure.axes[0]
        sets = _contour_sets(ax)
        self.assertTrue(sets[0].filled)
        self.assertEqual(sets[0].get_cmap().name, config["plot_heatmap_cmap"])
        self.assertFalse(ax.yaxis.get_gridlines()[0].get_visible())
        # the colorbar is a second, layout-managed axes of the figure
        self.assertEqual(len(figure.axes), 2)

    def test_lines_without_colorbar(self):
        figure = ContourChart(data=surface(), show_colorbars=True)
        self.assertEqual(len(figure.axes), 1)

    def test_line_cmap_truncated_when_pinned(self):
        figure = ContourChart(
            data=surface(), style={"plot_contour_cmap": COLORS.Blues}, levels=6
        )
        cs = _contour_sets(figure.axes[0])[0]
        cmap = cs.get_cmap()
        self.assertTrue(cmap.name.endswith("_lines"))
        # the truncated cmap starts at Blues(0.3), not near white
        self.assertLess(sum(cmap(0.0)[:3]), 2.7)

    def test_line_style_keys_apply(self):
        figure = ContourChart(
            data=surface(),
            style={
                "plot_contour_color": "#FF0000",
                "plot_contour_line_width": 3,
                "plot_contour_line_style": "--",
            },
        )
        cs = _contour_sets(figure.axes[0])[0]
        self.assertEqual(tuple(cs.get_edgecolor()[0][:3]), (1.0, 0.0, 0.0))
        self.assertEqual(cs.get_linewidth()[0], 3)

    def test_labels_drawn_with_valfmt(self):
        figure = ContourChart(
            data=surface(), show_labels=True, valfmt="{x:.0f}", levels=[50, 100, 200]
        )
        ax = figure.axes[0]
        texts = [t.get_text() for t in ax.texts]
        self.assertTrue(texts)
        self.assertTrue(set(texts) <= {"50", "100", "200"})
        self.assertEqual(ax.texts[0].get_fontsize(), config["font_general_size"] - 2)

    def test_levels_variants(self):
        explicit = ContourChart(data=surface(), levels=[50, 100, 200])
        np.testing.assert_array_equal(
            _contour_sets(explicit.axes[0])[0].levels, [50, 100, 200]
        )
        rice = ContourChart(data=surface(), levels=CONTOUR_LEVELS.RICE)
        rice_levels = _contour_sets(rice.axes[0])[0].levels
        self.assertTrue(4 <= len(rice_levels) <= 21)
        auto = ContourChart(data=surface())
        self.assertTrue(len(_contour_sets(auto.axes[0])[0].levels) > 1)
        count = ContourChart(data=surface(), levels=4)
        self.assertTrue(len(_contour_sets(count.axes[0])[0].levels) >= 3)

    def test_explicit_none_cmap_is_not_pinned(self):
        figure = ContourChart(data=surface(), style={"plot_contour_cmap": None})
        cs = _contour_sets(figure.axes[0])[0]
        self.assertFalse(cs.get_cmap().name.endswith("_lines"))

    def test_background_mutes_cmap_colored_lines(self):
        figure = ContourChart(
            data=[bump(-2, -1), bump(2, 1)],
            style={"plot_contour_cmap": COLORS.Blues},
            emphasis=["background", None],
        )
        sets = _contour_sets(figure.axes[0])
        muted = matplotlib.colors.to_rgb(config["muted_color"])
        self.assertEqual(tuple(sets[0].get_edgecolor()[0][:3]), muted)
        self.assertTrue(sets[1].get_cmap().name.endswith("_lines"))

    def test_all_none_emphasis_allowed_when_filled(self):
        figure = ContourChart(
            data=[bump(-2, -1), bump(2, 1)], filled=True, emphasis=[None, None]
        )
        self.assertEqual(len(_contour_sets(figure.axes[0])), 2)

    def test_overlay_legend_entries(self):
        figure = ContourChart(
            data=[bump(-2, -1), bump(2, 1)],
            subtitle=["A", "B"],
            show_legend=True,
            levels=5,
        )
        ax = figure.axes[0]
        self.assertEqual(len(_contour_sets(ax)), 2)
        legend = ax.get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["A", "B"])
        colors = [tuple(c.get_edgecolor()[0][:3]) for c in _contour_sets(ax)]
        self.assertNotEqual(colors[0], colors[1])
        handles = legend.legend_handles
        self.assertEqual(matplotlib.colors.to_rgb(handles[0].get_color()), colors[0])

    def test_filled_legend_swatch(self):
        figure = ContourChart(
            data=bump(0, 0), subtitle="density", filled=True, show_legend=True
        )
        legend = figure.axes[0].get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["density"])

    def test_subplots(self):
        figure = ContourChart(
            data=[bump(-2, -1), bump(2, 1)], subtitle=["A", "B"], subplots=True
        )
        self.assertEqual(len(figure.axes), 2)
        for ax in figure.axes:
            self.assertEqual(len(_contour_sets(ax)), 1)
        self.assertEqual(figure.axes[0].get_title(), "A")

    def test_emphasis_on_lines(self):
        figure = ContourChart(
            data=[bump(-2, -1), bump(2, 1)],
            subtitle=["A", "B"],
            emphasis=["background", "highlight"],
            show_legend=True,
        )
        ax = figure.axes[0]
        sets = _contour_sets(ax)
        muted = matplotlib.colors.to_rgb(config["muted_color"])
        self.assertEqual(tuple(sets[0].get_edgecolor()[0][:3]), muted)
        self.assertEqual(sets[0].get_alpha(), config["muted_alpha"])
        self.assertEqual(sets[1].get_linewidth()[0], config["plot_line_width"] * 2)
        legend = ax.get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["B"])

    def test_norm_and_vmin_vmax(self):
        figure = ContourChart(data=surface(), filled=True, vmin=0, vmax=500)
        cs = _contour_sets(figure.axes[0])[0]
        self.assertEqual((cs.norm.vmin, cs.norm.vmax), (0, 500))


class TestContourCompose(unittest.TestCase):
    def tearDown(self):
        plt.close("all")
        config.set_theme(THEME.DEFAULT)

    def test_metadata_type(self):
        figure = ContourChart(data=surface())
        self.assertEqual(figure._chart_metadata["type"], "contourchart")

    def test_panel_with_scatter(self):
        rng = np.random.default_rng(1)
        points = [{"x": float(x), "y": float(y)} for x, y in rng.normal(0, 1, (30, 2))]
        panel = Panel(
            [
                ScatterChart(data=points, subtitle="points"),
                ContourChart(data=bump(0, 0), subtitle="density", levels=5),
            ],
            show_legend=True,
        )
        ax = panel.axes[0]
        self.assertEqual(len(_contour_sets(ax)), 1)
        self.assertEqual(len(ax.collections), 2)
        legend = ax.get_legend()
        self.assertEqual(
            [t.get_text() for t in legend.get_texts()], ["points", "density"]
        )
        # the contour keeps a distinct cycle color from the scatter
        scatter_color = tuple(ax.collections[0].get_facecolor()[0][:3])
        contour_color = tuple(_contour_sets(ax)[0].get_edgecolor()[0][:3])
        self.assertNotEqual(scatter_color, contour_color)

    def test_panel_filled_with_scatter(self):
        rng = np.random.default_rng(1)
        points = [{"x": float(x), "y": float(y)} for x, y in rng.normal(0, 1, (30, 2))]
        panel = Panel(
            [
                ContourChart(data=bump(0, 0), filled=True),
                ScatterChart(data=points),
            ],
        )
        ax = panel.axes[0]
        self.assertTrue(_contour_sets(ax)[0].filled)

    def test_grid_nesting(self):
        fig = Grid(
            [
                [ContourChart(data=surface(), filled=True, title="fill")],
                [
                    LineChart(data=[{"x": i, "y": i} for i in range(5)]),
                    ContourChart(data=surface(), show_labels=True, title="lines"),
                ],
            ]
        )
        self.assertEqual(len(fig.axes), 3)
        self.assertTrue(_contour_sets(fig.axes[0])[0].filled)
        self.assertEqual(len(_contour_sets(fig.axes[2])), 1)
        self.assertTrue(fig.axes[2].texts)

    def test_grid_of_subplot_figure(self):
        inner = ContourChart(
            data=[bump(-2, -1), bump(2, 1)], subtitle=["A", "B"], subplots=True
        )
        fig = Grid([inner, LineChart(data=[{"x": i, "y": i} for i in range(5)])])
        self.assertEqual(len(fig.axes), 3)


if __name__ == "__main__":
    unittest.main()
