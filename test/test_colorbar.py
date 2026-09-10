"""Tests for the per-figure colorbar setting (ADR 0035)."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

from datachart.charts import ContourChart, Heatmap, HexbinChart
from datachart.config import config
from datachart.constants import COLORBAR_LOCATION, ORIENTATION, THEME
from datachart.typings import ColorbarSettingAttrs, HeatmapColorbarAttrs
from datachart.utils import Grid
from datachart.utils._internal.config_helpers import (
    get_colorbar_setting,
    get_text_style,
)

Z = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]


def surface(n=20):
    xs = np.linspace(-2, 2, n)
    z = [[float(np.exp(-(x * x + y * y))) for x in xs] for y in xs]
    return {"x": xs.tolist(), "y": xs.tolist(), "z": z}


def points(n=300, seed=0):
    rng = np.random.RandomState(seed)
    pts = rng.normal(0, 1, (n, 2))
    return {"x": pts[:, 0].tolist(), "y": pts[:, 1].tolist()}


FRONTS = {
    "heatmap": lambda **kw: Heatmap(data={"z": Z}, show_colorbars=True, **kw),
    "contour": lambda **kw: ContourChart(
        data=surface(), filled=True, show_colorbars=True, **kw
    ),
    "hexbin": lambda **kw: HexbinChart(data=points(), gridsize=8, **kw),
}


def colorbar_of(figure):
    """The one colorbar drawn on a figure, after a draw so positions are final."""
    figure.canvas.draw()
    bars = colorbars_of(figure)
    assert len(bars) == 1, bars
    return bars[0]


def colorbars_of(figure):
    """Every colorbar on a figure, whether a figure axes or a child axes."""
    axes = list(figure.axes) + [c for ax in figure.axes for c in ax.child_axes]
    return [ax._colorbar for ax in axes if hasattr(ax, "_colorbar")]


def edge_of(figure, colorbar):
    """Which edge of the chart axes the colorbar sits on."""
    ax = figure.axes[0].get_position()
    cax = colorbar.ax.get_position()
    if colorbar.orientation == "vertical":
        return "right" if cax.x0 >= ax.x1 else "left"
    return "top" if cax.y0 >= ax.y1 else "bottom"


def pixels(figure):
    figure.canvas.draw()
    return np.asarray(figure.canvas.buffer_rgba()).copy()


class TestColorbarSetting(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_defaults(self):
        setting = get_colorbar_setting(None)
        self.assertEqual(setting["location"], COLORBAR_LOCATION.RIGHT)
        self.assertEqual(setting["orientation"], ORIENTATION.VERTICAL)
        self.assertIsNone(setting["label"])
        self.assertIsNone(setting["format"])
        self.assertIsNone(setting["ticks"])

    def test_orientation_alone_derives_the_edge(self):
        vertical = get_colorbar_setting({"orientation": ORIENTATION.VERTICAL})
        horizontal = get_colorbar_setting({"orientation": ORIENTATION.HORIZONTAL})
        self.assertEqual(vertical["location"], COLORBAR_LOCATION.RIGHT)
        self.assertEqual(horizontal["location"], COLORBAR_LOCATION.TOP)
        self.assertEqual(horizontal["orientation"], ORIENTATION.HORIZONTAL)

    def test_location_derives_the_orientation(self):
        for location, orientation in [
            (COLORBAR_LOCATION.LEFT, ORIENTATION.VERTICAL),
            (COLORBAR_LOCATION.BOTTOM, ORIENTATION.HORIZONTAL),
        ]:
            setting = get_colorbar_setting({"location": location})
            self.assertEqual(setting["location"], location)
            self.assertEqual(setting["orientation"], orientation)

    def test_location_wins_over_orientation(self):
        setting = get_colorbar_setting(
            {"location": COLORBAR_LOCATION.BOTTOM, "orientation": ORIENTATION.VERTICAL}
        )
        self.assertEqual(setting["location"], COLORBAR_LOCATION.BOTTOM)
        self.assertEqual(setting["orientation"], ORIENTATION.HORIZONTAL)

    def test_none_fields_fall_back(self):
        setting = get_colorbar_setting({"location": None, "orientation": None})
        self.assertEqual(setting["location"], COLORBAR_LOCATION.RIGHT)

    def test_format_falls_back_to_valfmt(self):
        self.assertEqual(get_colorbar_setting({}, "{x:.0f}")["format"], "{x:.0f}")
        setting = get_colorbar_setting({"format": "{x:.2f}"}, "{x:.0f}")
        self.assertEqual(setting["format"], "{x:.2f}")

    def test_invalid_location_raises(self):
        with self.assertRaises(ValueError) as cm:
            get_colorbar_setting({"location": "middle"})
        self.assertIn("location", str(cm.exception))

    def test_label_style_is_the_ylabel_font(self):
        config.update_config({"font_ylabel_size": 17})
        setting = get_colorbar_setting({"label": "count"})
        self.assertEqual(setting["label_style"], get_text_style("ylabel"))
        self.assertEqual(setting["label_style"]["fontsize"], 17)

    def test_alias_still_resolves(self):
        self.assertIs(HeatmapColorbarAttrs, ColorbarSettingAttrs)


class TestColorbarRendering(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_four_locations_on_every_front(self):
        for name, front in FRONTS.items():
            for aspect in (None, "equal"):
                for location in ("right", "left", "top", "bottom"):
                    with self.subTest(front=name, aspect=aspect, location=location):
                        figure = front(
                            colorbar={"location": location}, aspect_ratio=aspect
                        )
                        colorbar = colorbar_of(figure)
                        self.assertEqual(edge_of(figure, colorbar), location)
                        plt.close(figure)

    def test_orientation_alone_matches_the_derived_location(self):
        for name, front in FRONTS.items():
            for orientation, location in [("vertical", "right"), ("horizontal", "top")]:
                with self.subTest(front=name, orientation=orientation):
                    by_orientation = pixels(
                        front(colorbar={"orientation": orientation})
                    )
                    by_location = pixels(front(colorbar={"location": location}))
                    self.assertTrue(np.array_equal(by_orientation, by_location))
                    plt.close("all")

    def test_location_wins_when_both_given(self):
        figure = FRONTS["heatmap"](
            colorbar={"location": "left", "orientation": "horizontal"}
        )
        colorbar = colorbar_of(figure)
        self.assertEqual(colorbar.orientation, "vertical")
        self.assertEqual(edge_of(figure, colorbar), "left")

    def test_label_renders_in_the_ylabel_font(self):
        config.update_config({"font_ylabel_size": 17, "font_ylabel_color": "#FF0000"})
        for name, front in FRONTS.items():
            with self.subTest(front=name):
                figure = front(colorbar={"label": "Count"})
                label = colorbar_of(figure).ax.yaxis.label
                self.assertEqual(label.get_text(), "Count")
                self.assertEqual(label.get_fontsize(), 17)
                self.assertEqual(label.get_color(), "#FF0000")
                plt.close(figure)

    def test_horizontal_label_reads_along_the_bar(self):
        figure = FRONTS["heatmap"](colorbar={"label": "Count", "location": "bottom"})
        colorbar = colorbar_of(figure)
        self.assertEqual(colorbar.ax.xaxis.label.get_text(), "Count")
        self.assertEqual(colorbar.ax.yaxis.label.get_text(), "")

    def test_format_controls_the_tick_labels(self):
        for name, front in FRONTS.items():
            with self.subTest(front=name):
                figure = front(colorbar={"format": "{x:.3f}"})
                colorbar = colorbar_of(figure)
                labels = [t.get_text() for t in colorbar.ax.yaxis.get_ticklabels()]
                self.assertTrue(labels)
                self.assertTrue(all(len(l.split(".")[-1]) == 3 for l in labels))
                plt.close(figure)

    def test_hexbin_valfmt_is_the_format_fallback(self):
        figure = HexbinChart(data=points(), gridsize=8, valfmt="{x:.2f}")
        colorbar = colorbar_of(figure)
        self.assertIsInstance(colorbar.formatter, mticker.StrMethodFormatter)
        self.assertEqual(colorbar.formatter.fmt, "{x:.2f}")

        figure = HexbinChart(
            data=points(), gridsize=8, valfmt="{x:.2f}", colorbar={"format": "{x:.1f}"}
        )
        self.assertEqual(colorbar_of(figure).formatter.fmt, "{x:.1f}")

    def test_heatmap_valfmt_still_formats_cells(self):
        figure = Heatmap(
            data={"z": Z},
            show_colorbars=True,
            show_heatmap_values=True,
            valfmt="{x:.1f}",
            colorbar={"format": "{x:.3f}"},
        )
        colorbar = colorbar_of(figure)
        cells = [t.get_text() for t in figure.axes[0].texts]
        self.assertIn("1.0", cells)
        ticks = [t.get_text() for t in colorbar.ax.yaxis.get_ticklabels()]
        self.assertTrue(all(len(t.split(".")[-1]) == 3 for t in ticks))

    def test_ticks_place_explicit_ticks(self):
        for name, front in FRONTS.items():
            with self.subTest(front=name):
                figure = front(colorbar={"ticks": [1, 2, 5]})
                colorbar = colorbar_of(figure)
                self.assertEqual(list(colorbar.get_ticks()), [1, 2, 5])
                plt.close(figure)

    def test_locked_bar_clears_the_axis_tick_labels(self):
        for location, axis in [("left", "yaxis"), ("bottom", "xaxis")]:
            with self.subTest(location=location):
                figure = FRONTS["heatmap"](
                    colorbar={"location": location}, aspect_ratio="equal"
                )
                colorbar = colorbar_of(figure)
                renderer = figure.canvas.get_renderer()
                ticks = getattr(figure.axes[0], axis).get_tightbbox(renderer)
                bar = colorbar.ax.get_window_extent(renderer)
                self.assertFalse(bar.overlaps(ticks))
                plt.close(figure)

    def test_grid_cell_keeps_label_and_edge(self):
        source = FRONTS["heatmap"](
            colorbar={"label": "Count", "location": "bottom", "format": "{x:.2f}"}
        )
        grid = Grid([[source, FRONTS["hexbin"](show_colorbars=False)]])
        grid.canvas.draw()
        bars = colorbars_of(grid)
        self.assertEqual(len(bars), 1)
        self.assertEqual(bars[0].orientation, "horizontal")
        self.assertEqual(bars[0].ax.xaxis.label.get_text(), "Count")
        self.assertEqual(bars[0].formatter.fmt, "{x:.2f}")


if __name__ == "__main__":
    unittest.main()
