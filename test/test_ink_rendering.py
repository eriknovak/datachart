"""Tests for the ink rendering attributes (ADR 0048)."""

import copy
import io
import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import (
    BarChart,
    Histogram,
    LineChart,
    RadialChart,
    ScatterChart,
    StackedAreaChart,
)
from datachart.config import config
from datachart.constants import THEME
from datachart.utils import Grid
from datachart.utils._internal.layers import Etch, InkStroke

LINE = [{"x": x, "y": y} for x, y in enumerate([1.0, 3.0, 2.0, 4.0, 3.5])]
STROKE = {
    "width_scale": 1.6,
    "nib_angle": 32,
    "nib_floor": 0.35,
    "wobble": 0.22,
    "taper": 7,
}
ETCH = {
    "spacing": 4.2,
    "jitter": 0.3,
    "angle_jitter": 2.5,
    "line_width": 0.6,
    "wash": 0.1,
    "color": "#1A120A",
}
BAR = [{"label": label, "y": y} for label, y in zip("ABC", [3.0, 5.0, 4.0])]


def data_lines(figure):
    return [
        line for ax in figure.axes for line in ax.get_lines() if line.get_xydata().size
    ]


def ink_effects(artist):
    return [e for e in artist.get_path_effects() if isinstance(e, InkStroke)]


def png(figure) -> bytes:
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png")
    return buffer.getvalue()


class TestInkStroke(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_off_by_default(self):
        self.assertIsNone(config["plot_ink_stroke"])
        self.assertFalse(data_lines(LineChart(LINE))[0].get_path_effects())

    def test_series_line_takes_the_stroke(self):
        config.update_config({"plot_ink_stroke": STROKE})
        figure = LineChart(LINE)
        (effect,) = ink_effects(data_lines(figure)[0])
        self.assertAlmostEqual(effect.width_scale, 1.6)
        png(figure)

    def test_regression_line_takes_the_stroke(self):
        config.update_config({"plot_ink_stroke": STROKE})
        figure = ScatterChart(
            [{"x": float(i), "y": float(i % 3)} for i in range(6)],
            show_regression=True,
        )
        self.assertTrue(any(ink_effects(line) for line in data_lines(figure)))

    def test_chart_style_turns_the_stroke_off(self):
        config.update_config({"plot_ink_stroke": STROKE})
        figure = LineChart(LINE, style={"plot_ink_stroke": None})
        self.assertFalse(ink_effects(data_lines(figure)[0]))

    def test_stroke_changes_the_pixels_and_repeats(self):
        plain = png(LineChart(LINE))
        config.update_config({"plot_ink_stroke": STROKE})
        first, second = png(LineChart(LINE)), png(LineChart(LINE))
        self.assertNotEqual(plain, first)
        self.assertEqual(first, second)

    def test_dashed_line_draws_one_ribbon_per_dash(self):
        effect = InkStroke(**STROKE)
        renderer = _RecordingRenderer()
        figure = LineChart(LINE, style={"plot_line_style": "--"})
        line = data_lines(figure)[0]
        figure.canvas.draw()
        line.set_path_effects([effect])
        line.draw(renderer)
        self.assertGreater(renderer.fills, 3)

    def test_grid_keeps_the_stroke(self):
        config.update_config({"plot_ink_stroke": STROKE})
        source = LineChart(LINE)
        config.set_theme(THEME.DEFAULT)
        grid = Grid([source, LineChart(LINE)])
        strokes = [bool(ink_effects(line)) for line in data_lines(grid)]
        self.assertEqual(strokes, [True, False])

    def test_no_rc_leakage(self):
        before = copy.deepcopy(matplotlib.rcParams["path.effects"])
        config.update_config({"plot_ink_stroke": STROKE})
        png(LineChart(LINE))
        self.assertEqual(matplotlib.rcParams["path.effects"], before)


def etch_effects(artist):
    return [e for e in artist.get_path_effects() if isinstance(e, Etch)]


def hatched_draws(figure) -> int:
    """How many paths the figure draws with a matplotlib hatch tile."""

    renderer = _RecordingRenderer()
    figure.canvas.draw()
    figure.draw(renderer)
    return renderer.hatched


class TestEtch(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_off_by_default(self):
        self.assertIsNone(config["plot_etch"])
        bars = BarChart(BAR, style={"plot_bar_hatch": "/"})
        self.assertFalse(bars.axes[0].patches[0].get_path_effects())
        self.assertGreater(hatched_draws(bars), 0)

    def test_hatched_bars_are_etched_not_tiled(self):
        config.update_config({"plot_etch": ETCH})
        bars = BarChart(BAR, style={"plot_bar_hatch": "/"})
        patch = bars.axes[0].patches[0]
        (effect,) = etch_effects(patch)
        self.assertAlmostEqual(effect.wash, 0.1)
        self.assertEqual(hatched_draws(bars), 0)

    def test_unhatched_bars_draw_as_they_are(self):
        plain = png(BarChart(BAR))
        config.update_config({"plot_etch": ETCH})
        self.assertEqual(png(BarChart(BAR)), plain)

    def test_histogram_and_radial_bars_are_etched(self):
        config.update_config({"plot_etch": ETCH, "plot_hatch_cycle": ["/", "x"]})
        hist = Histogram({"x": [1.0, 2.0, 2.0, 3.0, 3.0, 3.0]})
        self.assertTrue(etch_effects(hist.axes[0].patches[0]))
        radial = RadialChart(BAR, type="bar")
        self.assertTrue(etch_effects(radial.axes[0].patches[0]))
        self.assertEqual(hatched_draws(hist) + hatched_draws(radial), 0)

    def test_area_fills_etch_without_wash(self):
        config.update_config({"plot_etch": ETCH, "plot_area_hatch": "/"})
        line = LineChart(LINE, show_area=True)
        (effect,) = etch_effects(line.axes[0].collections[0])
        self.assertIsNone(effect.wash)
        stacked = StackedAreaChart([LINE, LINE])
        self.assertTrue(etch_effects(stacked.axes[0].collections[0]))
        self.assertEqual(hatched_draws(line), 0)

    def test_etching_repeats(self):
        config.update_config({"plot_etch": ETCH})
        first = png(BarChart(BAR, style={"plot_bar_hatch": "x."}))
        second = png(BarChart(BAR, style={"plot_bar_hatch": "x."}))
        self.assertEqual(first, second)


class _RecordingRenderer:
    """Wraps an Agg renderer and counts the filled paths drawn through it."""

    def __init__(self):
        from matplotlib.backends.backend_agg import RendererAgg

        self._agg = RendererAgg(400, 300, 100)
        self.fills = 0
        self.hatched = 0

    def draw_path(self, gc, path, transform, rgbFace=None):
        if rgbFace is not None:
            self.fills += 1
        if gc.get_hatch():
            self.hatched += 1
        self._agg.draw_path(gc, path, transform, rgbFace)

    def __getattr__(self, name):
        return getattr(self._agg, name)


if __name__ == "__main__":
    unittest.main()
