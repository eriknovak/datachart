"""Tests for the sketch theme and its render-scoped rc attributes (ADR 0027)."""

import copy
import io
import unittest
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

from datachart.charts import BarChart, LineChart
from datachart.config import config
from datachart.constants import THEME
from datachart.themes import SKETCH_THEME
from datachart.utils import Grid, Panel
from datachart.utils._internal.config_helpers import _font_available

LINE = [{"x": x, "y": y} for x, y in enumerate([1.0, 3.0, 2.0, 4.0])]
NEGATIVE = [{"x": x, "y": y} for x, y in enumerate([-3.0, -1.0, -2.0, 0.0])]
BAR = [{"label": label, "y": y} for label, y in zip("ABC", [3.0, 5.0, 4.0])]


def data_lines(figure):
    return [
        line for ax in figure.axes for line in ax.get_lines() if line.get_xydata().size
    ]


class TestSketchTheme(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_theme_registered(self):
        config.set_theme(THEME.SKETCH)
        self.assertEqual(config.config, SKETCH_THEME)
        self.assertEqual(SKETCH_THEME["plot_sketch_params"], (1, 100, 2))
        self.assertEqual(SKETCH_THEME["plot_sketch_halo_width"], 4)

    def test_default_theme_has_no_sketch(self):
        """Existing themes keep both rc attributes off, so their output is unchanged."""
        self.assertIsNone(config["plot_sketch_params"])
        self.assertIsNone(config["plot_sketch_halo_width"])
        figure = LineChart(LINE)
        line = data_lines(figure)[0]
        self.assertIsNone(line.get_sketch_params())
        self.assertFalse(line.get_path_effects())

    def test_sketch_applies_to_artists(self):
        config.set_theme(THEME.SKETCH)
        figure = LineChart(LINE)
        line = data_lines(figure)[0]
        self.assertEqual(line.get_sketch_params(), (1, 100, 2))
        self.assertEqual(len(line.get_path_effects()), 1)
        spine = figure.axes[0].spines["bottom"]
        self.assertEqual(spine.get_sketch_params(), (1, 100, 2))
        self.assertEqual(len(spine.get_path_effects()), 1)

    def test_sketch_applies_to_bars(self):
        config.set_theme(THEME.SKETCH)
        figure = BarChart(BAR)
        patch = figure.axes[0].patches[0]
        self.assertEqual(patch.get_sketch_params(), (1, 100, 2))
        self.assertEqual(len(patch.get_path_effects()), 1)

    def test_area_floor_fill_skips_sketch(self):
        """The floor fill's off-screen edge stays unsketched; the line wobbles."""
        config.set_theme(THEME.SKETCH)
        figure = LineChart(LINE, show_area=True)
        fill = figure.axes[0].collections[0]
        self.assertIsNone(fill.get_sketch_params())
        self.assertEqual(data_lines(figure)[0].get_sketch_params(), (1, 100, 2))

    def test_no_rc_leakage(self):
        before = {
            key: copy.deepcopy(matplotlib.rcParams[key])
            for key in ("path.sketch", "path.effects")
        }
        config.set_theme(THEME.SKETCH)
        figure = LineChart(LINE)
        figure.savefig(io.BytesIO(), format="png")
        for key, value in before.items():
            self.assertEqual(matplotlib.rcParams[key], value)

    def test_grid_keeps_build_time_sketch(self):
        """A grid of sketch figures renders sketched after the theme changes."""
        config.set_theme(THEME.SKETCH)
        first, second = LineChart(LINE), BarChart(BAR)
        config.set_theme(THEME.DEFAULT)
        grid = Grid([[first, second]])
        lines = data_lines(grid)
        self.assertTrue(lines)
        self.assertEqual(lines[0].get_sketch_params(), (1, 100, 2))
        patches = [p for ax in grid.axes for p in ax.patches]
        self.assertEqual(patches[0].get_sketch_params(), (1, 100, 2))

    def test_panel_twin_axis_sketched(self):
        config.set_theme(THEME.SKETCH)
        bars = BarChart(BAR)
        line = LineChart([{"x": x, "y": y * 100} for x, y in enumerate([1, 2, 3])])
        panel = Panel([bars, line], auto_secondary_axis=1)
        self.assertEqual(len(panel.axes), 2)
        for ax in panel.axes:
            for spine in ax.spines.values():
                self.assertEqual(spine.get_sketch_params(), (1, 100, 2))

    def test_explicit_show_grid_wins(self):
        config.set_theme(THEME.SKETCH)
        off = BarChart(BAR)
        on = BarChart(BAR, show_grid="y")
        self.assertFalse(
            any(l.get_visible() for l in off.axes[0].yaxis.get_gridlines())
        )
        self.assertTrue(any(l.get_visible() for l in on.axes[0].yaxis.get_gridlines()))

    def test_bundled_font_registered(self):
        self.assertTrue(_font_available("Comic Neue"))
        paths = [
            entry.fname
            for entry in font_manager.fontManager.ttflist
            if entry.name == "Comic Neue"
        ]
        # registration is idempotent: one entry per bundled face
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(
            {
                entry.weight
                for entry in font_manager.fontManager.ttflist
                if entry.name == "Comic Neue"
            },
            {400, 700},
        )

    def test_font_resolves_without_warning(self):
        config.set_theme(THEME.SKETCH)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            figure = LineChart(NEGATIVE, title="Bold title")
            figure.savefig(io.BytesIO(), format="png")
        label = figure.axes[0].get_yticklabels()[0]
        self.assertEqual(label.get_fontfamily()[0], "Comic Neue")
        self.assertIn("−", label.get_text())


if __name__ == "__main__":
    unittest.main()
