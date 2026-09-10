"""Tests for reference bands (ADR 0036): `vspans` / `hspans` on the reference-line seam."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.collections import PolyCollection
from matplotlib.artist import Artist

from datachart import typings
from datachart.charts import (
    BarChart,
    BoxPlot,
    ContourChart,
    HexbinChart,
    Histogram,
    LineChart,
    PyramidChart,
    RadialChart,
    RaincloudPlot,
    ScatterChart,
    StackedAreaChart,
    SwarmPlot,
    ViolinPlot,
)
from datachart.config import config
from datachart.constants import THEME
from datachart import themes
from datachart.utils import Grid, Panel
from datachart.utils._internal.config_helpers import get_hspan_style, get_vspan_style

LINE = [{"x": i, "y": i * 2} for i in range(6)]
BAR = [{"label": c, "y": v} for c, v in zip("ABCD", [3, 5, 4, 6])]
WIND = [{"label": d, "y": v} for d, v in zip(["N", "E", "S", "W"], [3, 5, 4, 6])]
SPAN_KEYS = ("color", "alpha", "hatch", "edge_color", "edge_width", "zorder")


def band_patches(ax):
    """The band patches of an axes: spans ride the blended axis transforms."""

    spans = (
        ax.get_xaxis_transform(which="grid"),
        ax.get_yaxis_transform(which="grid"),
    )
    return [p for p in ax.patches if Artist.get_transform(p) in spans]


class TestTypingsAndThemes(unittest.TestCase):
    def test_typings_exported_and_tagged(self):
        for name in (
            "VSpanPlotAttrs",
            "HSpanPlotAttrs",
            "VSpanStyleAttrs",
            "HSpanStyleAttrs",
        ):
            cls = getattr(typings, name)
            self.assertIn("Added in Unreleased", cls.__doc__)
        self.assertEqual(
            set(typings.VSpanPlotAttrs.__annotations__),
            {"xmin", "xmax", "style", "label"},
        )
        self.assertEqual(
            set(typings.HSpanPlotAttrs.__annotations__),
            {"ymin", "ymax", "style", "label"},
        )

    def test_theme_keys_in_every_theme(self):
        for theme_name in themes.__all__:
            theme = getattr(themes, theme_name)
            for side in ("vspan", "hspan"):
                for key in SPAN_KEYS:
                    self.assertIn(f"plot_{side}_{key}", theme, theme_name)

    def test_base_defaults(self):
        config.reset_config()
        self.assertIsNone(config["plot_vspan_color"])
        self.assertEqual(config["plot_vspan_alpha"], 0.25)
        self.assertEqual(config["plot_vspan_zorder"], 1.75)
        self.assertEqual(config["plot_hspan_zorder"], 1.75)


class TestStyleResolvers(unittest.TestCase):
    def tearDown(self):
        config.reset_config()

    def test_defaults(self):
        style = get_vspan_style({})
        self.assertNotIn("facecolor", style)
        self.assertEqual(style["alpha"], 0.25)
        self.assertEqual(style["zorder"], 1.75)
        self.assertNotIn("hatch", style)
        self.assertNotIn("edgecolor", style)

    def test_overrides(self):
        style = get_hspan_style(
            {
                "plot_hspan_color": "#FF0000",
                "plot_hspan_hatch": "//",
                "plot_hspan_edge_color": "#000000",
                "plot_hspan_edge_width": 2,
                "plot_hspan_zorder": 5,
            }
        )
        self.assertEqual(style["facecolor"], "#FF0000")
        self.assertEqual(style["hatch"], "//")
        self.assertEqual(style["edgecolor"], "#000000")
        self.assertEqual(style["linewidth"], 2)
        self.assertEqual(style["zorder"], 5)


class TestBounds(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_neither_bound_raises(self):
        with pytest.raises(ValueError, match="xmin"):
            LineChart(data=LINE, vspans={"label": "x"})
        with pytest.raises(ValueError, match="ymin"):
            LineChart(data=LINE, hspans={})

    def test_open_upper_bound_runs_to_axis_limit(self):
        figure = LineChart(data=LINE, vspans={"xmin": 2})
        ax = figure.axes[0]
        (band,) = band_patches(ax)
        self.assertEqual(band.get_x(), 2)
        self.assertAlmostEqual(band.get_x() + band.get_width(), ax.get_xlim()[1])

    def test_open_lower_bound_runs_to_axis_limit(self):
        figure = LineChart(data=LINE, hspans={"ymax": 4})
        ax = figure.axes[0]
        (band,) = band_patches(ax)
        self.assertAlmostEqual(band.get_y(), ax.get_ylim()[0])
        self.assertAlmostEqual(band.get_y() + band.get_height(), 4)

    def test_closed_band(self):
        figure = LineChart(data=LINE, vspans={"xmin": 1, "xmax": 3})
        (band,) = band_patches(figure.axes[0])
        self.assertEqual((band.get_x(), band.get_width()), (1, 2))

    def test_list_of_bands(self):
        figure = LineChart(
            data=LINE,
            vspans=[{"xmin": 1, "xmax": 2}, {"xmin": 3, "xmax": 4}],
            hspans={"ymin": 2, "ymax": 4},
        )
        self.assertEqual(len(band_patches(figure.axes[0])), 3)


class TestStacking(unittest.TestCase):
    def tearDown(self):
        config.reset_config()
        plt.close("all")

    def test_default_zorder_between_grid_and_marks(self):
        figure = LineChart(data=LINE, vspans={"xmin": 1, "xmax": 3}, show_grid="both")
        ax = figure.axes[0]
        (band,) = band_patches(ax)
        self.assertEqual(band.get_zorder(), 1.75)
        self.assertLess(ax.xaxis.get_zorder(), band.get_zorder())
        self.assertLess(band.get_zorder(), ax.lines[0].get_zorder())

    def test_theme_zorder_moves_band(self):
        config.update_config({"plot_hspan_zorder": 10})
        figure = LineChart(data=LINE, hspans={"ymin": 1, "ymax": 3})
        (band,) = band_patches(figure.axes[0])
        self.assertEqual(band.get_zorder(), 10)

    def test_default_color_is_muted_grey(self):
        figure = LineChart(data=LINE, vspans={"xmin": 1, "xmax": 3})
        (band,) = band_patches(figure.axes[0])
        self.assertEqual(
            band.get_facecolor(),
            matplotlib.colors.to_rgba(config["muted_color"], 0.25),
        )

    def test_hatch_draws_in_edge_color(self):
        figure = LineChart(
            data=LINE,
            vspans={
                "xmin": 1,
                "xmax": 3,
                "style": {"plot_vspan_hatch": "//", "plot_vspan_edge_color": "#123456"},
            },
        )
        (band,) = band_patches(figure.axes[0])
        self.assertEqual(band.get_hatch(), "//")
        self.assertEqual(
            band.get_hatchcolor(), matplotlib.colors.to_rgba("#123456", 0.25)
        )


class TestLegend(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_label_adds_one_entry(self):
        figure = LineChart(
            data=LINE, vspans={"xmin": 1, "xmax": 3, "label": "band"}, show_legend=True
        )
        legend = figure.axes[0].get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["band"])

    def test_no_label_adds_no_entry(self):
        figure = LineChart(
            data=LINE,
            subtitle="series",
            vspans={"xmin": 1, "xmax": 3},
            show_legend=True,
        )
        legend = figure.axes[0].get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["series"])


class TestFronts(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_every_reference_line_front_accepts_bands(self):
        span = {"vspans": {"xmin": 0, "xmax": 1}, "hspans": {"ymin": 0, "ymax": 1}}
        rng = np.random.RandomState(0)
        sample = [{"x": float(v)} for v in rng.randn(30)]
        boxes = [{"label": c, "y": float(v)} for c, v in zip("AABB", rng.randn(4))]
        scat = [{"x": i, "y": i} for i in range(5)]
        grid = {
            "x": [0, 1, 2],
            "y": [0, 1, 2],
            "z": [[0, 1, 2], [1, 2, 3], [2, 3, 4]],
        }
        pyramid = [[{"label": c, "y": v} for c, v in zip("AB", [1, 2])]] * 2
        calls = [
            (LineChart, LINE),
            (BarChart, BAR),
            (Histogram, sample),
            (ScatterChart, scat),
            (BoxPlot, boxes),
            (SwarmPlot, boxes),
            (ViolinPlot, boxes),
            (RaincloudPlot, boxes),
            (HexbinChart, {"x": [0, 1, 2, 3], "y": [1, 0, 2, 3]}),
            (PyramidChart, pyramid),
            (StackedAreaChart, [LINE, LINE]),
            (ContourChart, grid),
        ]
        for front, data in calls:
            figure = front(data=data, **span)
            ax = figure.axes[0]
            self.assertEqual(len(band_patches(ax)) >= 2, True, front.__name__)

    def test_shared_band_draws_once_per_panel(self):
        figure = LineChart(
            data=[LINE, LINE],
            vspans={"xmin": 1, "xmax": 2, "label": "band"},
            show_legend=True,
        )
        ax = figure.axes[0]
        self.assertEqual(len(band_patches(ax)), 1)
        self.assertEqual(
            [t.get_text() for t in ax.get_legend().get_texts()].count("band"), 1
        )

    def test_subplots_take_per_chart_bands(self):
        figure = LineChart(
            data=[LINE, LINE],
            subplots=True,
            vspans=[{"xmin": 1, "xmax": 2}, None],
        )
        self.assertEqual(len(band_patches(figure.axes[0])), 1)
        self.assertEqual(len(band_patches(figure.axes[1])), 0)


class TestRadial(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_reference_lines_still_raise(self):
        with pytest.raises(ValueError, match="vlines"):
            RadialChart(data=WIND, vlines={"x": 1})
        with pytest.raises(ValueError, match="hlines"):
            RadialChart(data=WIND, hlines={"y": 1})

    def test_wedge_spans_theta_over_full_radius(self):
        figure = RadialChart(data=WIND, vspans={"xmin": 0, "xmax": 90})
        ax = figure.axes[0]
        (wedge,) = [c for c in ax.collections if isinstance(c, PolyCollection)]
        verts = wedge.get_paths()[0].vertices
        theta, r = verts[:, 0], verts[:, 1]
        self.assertAlmostEqual(theta.min(), 0)
        self.assertAlmostEqual(theta.max(), np.pi / 2)
        rmin, rmax = ax.get_ylim()
        self.assertAlmostEqual(r.min(), rmin)
        self.assertAlmostEqual(r.max(), rmax)

    def test_annulus_spans_full_circle_between_radii(self):
        figure = RadialChart(data=WIND, hspans={"ymin": 2, "ymax": 4})
        ax = figure.axes[0]
        (ring,) = [c for c in ax.collections if isinstance(c, PolyCollection)]
        verts = ring.get_paths()[0].vertices
        theta, r = verts[:, 0], verts[:, 1]
        self.assertAlmostEqual(theta.min(), 0)
        self.assertAlmostEqual(theta.max(), 2 * np.pi)
        self.assertAlmostEqual(r.min(), 2)
        self.assertAlmostEqual(r.max(), 4)

    def test_radial_half_open_bounds(self):
        figure = RadialChart(data=WIND, vspans={"xmin": 270}, hspans={"ymax": 2})
        ax = figure.axes[0]
        wedge, ring = [c for c in ax.collections if isinstance(c, PolyCollection)]
        self.assertAlmostEqual(wedge.get_paths()[0].vertices[:, 0].max(), 2 * np.pi)
        self.assertAlmostEqual(
            ring.get_paths()[0].vertices[:, 1].min(), ax.get_ylim()[0]
        )

    def test_radial_label_in_legend(self):
        figure = RadialChart(
            data=WIND,
            vspans={"xmin": 0, "xmax": 90, "label": "wedge"},
            show_legend=True,
        )
        legend = figure.axes[0].get_legend()
        self.assertIn("wedge", [t.get_text() for t in legend.get_texts()])


class TestComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_keeps_bands(self):
        banded = LineChart(data=LINE, vspans={"xmin": 1, "xmax": 3, "label": "band"})
        other = BarChart(data=BAR, hspans={"ymin": 1, "ymax": 2})
        figure = Panel([banded, other], show_legend=True)
        ax = figure.axes[0]
        bands = band_patches(ax)
        self.assertEqual(len(bands), 2)
        self.assertIn("band", [p.get_label() for p in bands])

    def test_grid_keeps_bands(self):
        banded = LineChart(data=LINE, vspans={"xmin": 1, "xmax": 3})
        figure = Grid([banded, LineChart(data=LINE)])
        counts = [len(band_patches(ax)) for ax in figure.axes]
        self.assertEqual(counts, [1, 0])

    def test_radial_in_grid_keeps_wedge(self):
        wedge = RadialChart(data=WIND, vspans={"xmin": 0, "xmax": 90})
        figure = Grid([wedge, LineChart(data=LINE)])
        polar_ax = [ax for ax in figure.axes if ax.name == "polar"][0]
        self.assertEqual(
            len([c for c in polar_ax.collections if isinstance(c, PolyCollection)]), 1
        )
