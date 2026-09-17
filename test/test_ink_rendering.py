"""Tests for the ink rendering attributes (ADR 0048)."""

import copy
import io
import os
import tempfile
import unittest
import warnings

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import to_hex
from matplotlib.legend import Legend

from datachart.charts import (
    BarChart,
    BoxPlot,
    CalendarHeatmap,
    ContourChart,
    Heatmap,
    HexbinChart,
    RidgelinePlot,
    ViolinPlot,
    Histogram,
    LineChart,
    NetworkChart,
    ParallelCoords,
    RadialChart,
    Treemap,
    SankeyChart,
    ScatterChart,
    StackedAreaChart,
)
from datachart.config import config
from datachart.constants import THEME
from datachart.themes import QUILL_THEME
from datachart.utils import Grid
from datachart.utils._internal.config_helpers import _font_available
from datachart.utils._internal.layers import Etch, InkStroke

LINE = [{"x": x, "y": y} for x, y in enumerate([1.0, 3.0, 2.0, 4.0, 3.5])]
LINE_2 = [{"x": x, "y": y} for x, y in enumerate([2.0, 1.0, 3.0, 2.5, 1.5])]
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

    def test_contour_lines_take_the_stroke(self):
        config.update_config({"plot_ink_stroke": STROKE})
        figure = ContourChart(GRID)
        self.assertTrue(any(ink_effects(c) for c in figure.axes[0].collections))

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
        stacked = StackedAreaChart([LINE, LINE_2])
        self.assertTrue(etch_effects(stacked.axes[0].collections[0]))
        self.assertEqual(hatched_draws(line), 0)

    def test_etching_repeats(self):
        config.update_config({"plot_etch": ETCH})
        first = png(BarChart(BAR, style={"plot_bar_hatch": "x."}))
        second = png(BarChart(BAR, style={"plot_bar_hatch": "x."}))
        self.assertEqual(first, second)


PARCHMENT = "#F3E7CB"
INK = "#1A120A"
GROUND = {
    "figure_facecolor": PARCHMENT,
    "axes_facecolor": PARCHMENT,
    "axes_spines_color": INK,
    "axes_ticks_color": INK,
    "plot_legend_edge_color": INK,
    "plot_legend_face_color": PARCHMENT,
}


class TestGroundColors(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_off_by_default(self):
        for key in GROUND:
            self.assertIsNone(config[key], key)

    def test_panel_applies_ground_and_furniture(self):
        config.update_config(GROUND)
        figure = LineChart(LINE, subtitle="Run", show_legend=True)
        ax = figure.axes[0]
        self.assertEqual(to_hex(figure.get_facecolor()), PARCHMENT.lower())
        self.assertEqual(to_hex(ax.get_facecolor()), PARCHMENT.lower())
        self.assertEqual(to_hex(ax.spines["left"].get_edgecolor()), INK.lower())
        tick = ax.xaxis.get_major_ticks()[0]
        self.assertEqual(to_hex(tick.tick1line.get_color()), INK.lower())
        frame = ax.get_legend().get_frame()
        self.assertEqual(to_hex(frame.get_edgecolor()), INK.lower())
        self.assertEqual(to_hex(frame.get_facecolor()), PARCHMENT.lower())

    def test_bare_panel_takes_the_ground(self):
        config.update_config(GROUND)
        figure = SankeyChart({"links": [{"source": "a", "target": "b", "value": 1.0}]})
        self.assertEqual(to_hex(figure.get_facecolor()), PARCHMENT.lower())

    def test_halo_follows_the_ground(self):
        config.update_config({**GROUND, "plot_sketch_halo_width": 2})
        figure = BarChart(BAR, show_values=True)
        (effect,) = figure.axes[0].texts[0].get_path_effects()
        self.assertEqual(to_hex(effect._gc["foreground"]), PARCHMENT.lower())
        (halo,) = data_lines(LineChart(LINE))[0].get_path_effects()
        self.assertEqual(to_hex(halo._gc["foreground"]), PARCHMENT.lower())


class TestAreaAndBodyEtching(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_hatch_cycle_skips_areas_without_etch(self):
        config.update_config({"plot_hatch_cycle": ["/", "x"]})
        figure = StackedAreaChart([LINE, LINE_2])
        self.assertEqual(
            [c.get_hatch() for c in figure.axes[0].collections], [None, None]
        )

    def test_each_area_takes_its_own_pattern(self):
        config.update_config({"plot_etch": ETCH, "plot_hatch_cycle": ["/", "x"]})
        stacked = StackedAreaChart([LINE, LINE_2])
        self.assertEqual(
            [c.get_hatch() for c in stacked.axes[0].collections], ["/", "x"]
        )
        lines = LineChart([LINE, LINE_2], show_area=True)
        self.assertEqual([c.get_hatch() for c in lines.axes[0].collections], ["/", "x"])

    def test_chart_area_hatch_beats_the_cycle(self):
        config.update_config({"plot_etch": ETCH, "plot_hatch_cycle": ["/", "x"]})
        figure = LineChart(LINE, show_area=True, style={"plot_area_hatch": "."})
        self.assertEqual(figure.axes[0].collections[0].get_hatch(), ".")

    def test_area_legend_swatch_carries_the_etch(self):
        config.update_config({"plot_etch": ETCH, "plot_hatch_cycle": ["/", "x"]})
        figure = StackedAreaChart([LINE, LINE_2], subtitle=["a", "b"], show_legend=True)
        swatch = figure.axes[0].get_legend().get_patches()[0]
        self.assertTrue(etch_effects(swatch))

    def test_bodies_take_their_hatch_and_etch(self):
        config.update_config(
            {
                "plot_etch": ETCH,
                "plot_box_hatch": "/",
                "plot_violin_hatch": "\\",
                "plot_ridgeline_hatch": "/",
            }
        )
        points = [{"label": l, "value": float(v)} for l in "AB" for v in range(8)]
        box = BoxPlot(points).axes[0].patches[0]
        self.assertEqual(box.get_hatch(), "/")
        self.assertTrue(etch_effects(box))
        violin = ViolinPlot(points).axes[0].collections[0]
        self.assertEqual(violin.get_hatch(), "\\")
        self.assertTrue(etch_effects(violin))
        ridge = RidgelinePlot(points).axes[0].collections[0]
        self.assertEqual(ridge.get_hatch(), "/")
        self.assertTrue(etch_effects(ridge))


class TestStyleCycles(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_off_by_default(self):
        self.assertIsNone(config["plot_linestyle_cycle"])
        self.assertIsNone(config["plot_marker_cycle"])

    def test_line_styles_cycle_per_series(self):
        config.update_config({"plot_linestyle_cycle": ["-", "--", ":"]})
        figure = LineChart([LINE, LINE_2])
        styles = [line.get_linestyle() for line in data_lines(figure)]
        self.assertEqual(styles, ["-", "--"])

    def test_chart_line_style_wins(self):
        config.update_config({"plot_linestyle_cycle": ["--"]})
        figure = LineChart(LINE, style={"plot_line_style": ":"})
        self.assertEqual(data_lines(figure)[0].get_linestyle(), ":")

    def test_markers_cycle_filled_and_hollow(self):
        config.update_config(
            {"plot_marker_cycle": ["o", {"marker": "s", "hollow": True}]}
        )
        points = [{"x": float(i), "y": float(i)} for i in range(4)]
        shifted = [{"x": float(i), "y": float(i) + 1} for i in range(4)]
        figure = ScatterChart([points, shifted])
        filled, hollow = figure.axes[0].collections
        self.assertEqual(filled.get_facecolor()[0][3], 0.75)
        self.assertEqual(len(hollow.get_facecolor()), 0)
        self.assertGreater(hollow.get_linewidths()[0], 0)
        self.assertFalse(
            np.array_equal(
                filled.get_paths()[0].vertices, hollow.get_paths()[0].vertices
            )
        )

    def test_chart_marker_wins(self):
        config.update_config({"plot_marker_cycle": [{"marker": "s", "hollow": True}]})
        points = [{"x": float(i), "y": float(i)} for i in range(4)]
        figure = ScatterChart(points, style={"plot_scatter_marker": "^"})
        self.assertEqual(len(figure.axes[0].collections[0].get_facecolor()), 1)


class TestQuillTheme(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_theme_registered(self):
        config.set_theme(THEME.QUILL)
        self.assertEqual(config.config, QUILL_THEME)
        self.assertEqual(config["color_general_multiple"], [INK])

    def test_bundled_fonts_registered(self):
        self.assertTrue(_font_available("IM FELL English"))
        styles = {
            entry.style
            for entry in font_manager.fontManager.ttflist
            if entry.name == "IM FELL English"
        }
        self.assertEqual(styles, {"normal", "italic"})
        self.assertTrue(_font_available("IM FELL English SC"))

    def test_series_draw_in_ink_with_their_own_marks(self):
        config.set_theme(THEME.QUILL)
        figure = LineChart([LINE, LINE_2], title="Runs")
        first, second = data_lines(figure)
        self.assertEqual(to_hex(first.get_color()), INK.lower())
        self.assertNotEqual(first.get_linestyle(), second.get_linestyle())
        self.assertTrue(ink_effects(first))
        self.assertEqual(figure._suptitle.get_fontstyle(), "italic")
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            png(figure)

    def test_value_texts_take_the_theme_font(self):
        config.set_theme(THEME.QUILL)
        heatmap = Heatmap(GRID, show_heatmap_values=True)
        self.assertEqual(heatmap.axes[0].texts[0].get_fontname(), "IM FELL English")
        contour = ContourChart(GRID, show_labels=True)
        self.assertEqual(contour.axes[0].texts[0].get_fontname(), "IM FELL English")
        parallel = ParallelCoords(
            [{"a": 1.0, "b": 2.0}, {"a": 2.0, "b": 1.0}], dimensions=["a", "b"]
        )
        self.assertEqual(parallel.axes[0].texts[0].get_fontname(), "IM FELL English")

    def test_theme_file_round_trip_renders_the_same(self):
        config.set_theme(THEME.QUILL)
        bars = [BAR, [{"label": l, "y": y} for l, y in zip("ABC", [2.0, 4.0, 1.0])]]
        native = png(LineChart([LINE, LINE_2])) + png(BarChart(bars))
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "quill_copy.json")
            config.save_theme(path, name=THEME.QUILL)
            config.set_theme(config.load_theme(path))
        loaded = png(LineChart([LINE, LINE_2])) + png(BarChart(bars))
        self.assertEqual(native, loaded)


VALUE_ETCH = {
    "washes": ["#F3E7CB", "#E2D1A6", "#D3BF90", "#C1A874", "#A88C52"],
    "hatches": ["", ".", "..", "//", "xx"],
}
GRID = {"z": [[0.0, 1.0, 2.0], [3.0, 4.0, 5.0], [6.0, 7.0, 8.0]]}


def step_collections(ax):
    return [c for c in ax.collections if c.get_gid() == "value-step"]


class TestValueEtch(unittest.TestCase):
    def setUp(self):
        config.update_config({"plot_etch": ETCH, "plot_value_etch": VALUE_ETCH})

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_off_by_default(self):
        config.set_theme(THEME.DEFAULT)
        self.assertIsNone(config["plot_value_etch"])
        figure = Heatmap(GRID, show_colorbars=True)
        self.assertFalse(step_collections(figure.axes[0]))
        self.assertEqual(len(figure.axes), 2)

    def test_needs_the_etch(self):
        config.update_config({"plot_etch": None})
        figure = Heatmap(GRID, show_colorbars=True)
        self.assertFalse(step_collections(figure.axes[0]))

    def test_heatmap_cells_draw_as_steps_with_a_step_legend(self):
        figure = Heatmap(GRID, show_colorbars=True, colorbar={"label": "Score"})
        ax = figure.axes[0]
        self.assertEqual(len(figure.axes), 1)
        steps = step_collections(ax)
        self.assertEqual(len(steps), 5)
        self.assertEqual(sum(len(c.get_paths()) for c in steps), 9)
        self.assertEqual([c.get_hatch() for c in steps], [None, ".", "..", "//", "xx"])
        legends = [a for a in ax.artists if isinstance(a, Legend)]
        (legend,) = legends
        self.assertEqual(legend.get_title().get_text(), "Score")
        self.assertEqual(len(legend.get_texts()), 5)
        self.assertEqual(legend.get_texts()[0].get_text(), "0 – 1.6")
        self.assertFalse(legend.get_clip_on())
        png(figure)

    def test_hexbin_steps_keep_the_emphasis_fade(self):
        rng = np.random.default_rng(1)
        figure = HexbinChart(
            {"x": list(rng.normal(size=300)), "y": list(rng.normal(size=300))},
            emphasis_rule={"top": 3},
        )
        alphas = np.concatenate(
            [np.atleast_1d(c.get_alpha()) for c in step_collections(figure.axes[0])]
        )
        self.assertLess(alphas.min(), 1.0)
        self.assertEqual(alphas.max(), 1.0)

    def test_empty_hexbin_bins_draw_nothing(self):
        figure = HexbinChart({"x": [0.0, 0.1, 5.0], "y": [0.0, 0.1, 5.0]}, gridsize=5)
        tiles = figure.axes[0].collections[0]
        values = [c for c in figure.axes[0].collections if c.get_gid() != "value-step"]
        drawn = sum(len(c.get_offsets()) for c in step_collections(figure.axes[0]))
        self.assertEqual(drawn, int((tiles.get_edgecolor()[:, 3] > 0).sum()))
        self.assertLess(drawn, len(tiles.get_offsets()))

    def test_no_legend_without_colorbars(self):
        figure = Heatmap(GRID, show_colorbars=False)
        self.assertTrue(step_collections(figure.axes[0]))
        self.assertFalse([a for a in figure.axes[0].artists if isinstance(a, Legend)])

    def test_values_read_through_a_ground_halo(self):
        config.update_config(GROUND)
        text = Heatmap(GRID, show_heatmap_values=True).axes[0].texts[-1]
        self.assertIsNone(text.get_bbox_patch())
        (halo,) = text.get_path_effects()
        self.assertEqual(to_hex(halo._gc["foreground"]), PARCHMENT.lower())
        x = np.linspace(-2, 2, 20)
        z = [[float(np.exp(-(a * a + b * b))) for a in x] for b in x]
        relief = ContourChart({"x": list(x), "y": list(x), "z": z}, filled=True)
        self.assertTrue(all(t.get_path_effects() for t in relief.axes[0].texts))

    def test_boxless_parallel_labels_take_the_halo(self):
        rows = [{"a": 1.0, "b": 2.0}, {"a": 2.0, "b": 1.0}]
        boxed = ParallelCoords(rows, dimensions=["a", "b"]).axes[0].texts[0]
        self.assertIsNotNone(boxed.get_bbox_patch())
        self.assertFalse(boxed.get_path_effects())
        config.update_config({"plot_parallel_tick_label_bg_color": None})
        halo = ParallelCoords(rows, dimensions=["a", "b"]).axes[0].texts[0]
        self.assertIsNone(halo.get_bbox_patch())
        self.assertTrue(halo.get_path_effects())

    def test_calendar_and_hexbin_draw_steps(self):
        from datetime import date, timedelta

        days = [date(2024, 1, 1) + timedelta(days=i) for i in range(40)]
        calendar = CalendarHeatmap(
            {"date": days, "value": list(range(40))},
            show_colorbars=True,
        )
        self.assertTrue(step_collections(calendar.axes[0]))
        rng = np.random.default_rng(1)
        hexbin = HexbinChart(
            {"x": list(rng.normal(size=300)), "y": list(rng.normal(size=300))},
            show_colorbars=True,
        )
        self.assertTrue(step_collections(hexbin.axes[0]))
        self.assertEqual(len(hexbin.axes), 1)
        png(calendar)
        png(hexbin)

    def test_filled_contour_is_a_relief_map(self):
        x = np.linspace(-2, 2, 30)
        z = [[float(np.exp(-(a * a + b * b))) for a in x] for b in x]
        figure = ContourChart(
            {"x": list(x), "y": list(x), "z": z}, filled=True, show_colorbars=True
        )
        ax = figure.axes[0]
        self.assertTrue(step_collections(ax))
        self.assertEqual(len(figure.axes), 1)
        self.assertTrue(ax.texts, "level labels")
        (legend,) = [a for a in ax.artists if isinstance(a, Legend)]
        self.assertLessEqual(len(legend.get_texts()), 5)
        png(figure)


TREE = {
    "data": [
        {
            "label": "Asia",
            "children": [
                {"label": "China", "value": 14.0},
                {"label": "India", "value": 13.0},
            ],
        },
        {"label": "Africa", "value": 12.0},
    ]
}
NETWORK = {
    "nodes": [
        {"id": "a", "group": "g1"},
        {"id": "b", "group": "g1"},
        {"id": "c", "group": "g2"},
    ],
    "edges": [
        {"source": "a", "target": "b", "weight": 2.0},
        {"source": "b", "target": "c", "weight": 1.0},
    ],
}


class TestChartInkLooks(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_sankey_nodes_as_outlines(self):
        links = {"links": [{"source": "a", "target": "b", "value": 1.0}]}
        filled = SankeyChart(links).axes[0].patches[0]
        self.assertEqual(filled.get_facecolor()[3], 1.0)
        config.update_config({"plot_sankey_node_fill": False})
        outline = SankeyChart(links).axes[0].patches[0]
        self.assertEqual(outline.get_facecolor()[3], 0.0)

    def test_treemap_etching_thins_with_depth(self):
        config.update_config(
            {
                "plot_etch": ETCH,
                "plot_hatch_cycle": ["/", "."],
                "plot_treemap_etch_density": [3, 1, 0],
                **GROUND,
            }
        )
        figure = Treemap(TREE, show_legend=True)
        patches = {p.get_gid(): p for p in figure.axes[0].patches}
        self.assertEqual(patches["fill:Asia"].get_hatch(), "///")
        self.assertEqual(patches["tile:China"].get_hatch(), "/")
        self.assertEqual(patches["tile:Africa"].get_hatch(), "...")
        self.assertEqual(
            to_hex(patches["tile:China"].get_facecolor()), PARCHMENT.lower()
        )
        self.assertTrue(etch_effects(patches["tile:China"]))
        swatch = figure.axes[0].get_legend().get_patches()[0]
        self.assertEqual(swatch.get_hatch(), "/")
        self.assertTrue(etch_effects(swatch))
        png(figure)

    def test_treemap_unchanged_without_density(self):
        config.update_config({"plot_etch": ETCH, "plot_hatch_cycle": ["/", "."]})
        patches = Treemap(TREE).axes[0].patches
        self.assertTrue(all(p.get_hatch() is None for p in patches))

    def test_network_ink_roads_shapes_and_rings(self):
        config.update_config(
            {
                "plot_network_edge_ink_stroke": {
                    "width_scale": 1.4,
                    "nib_floor": 1.0,
                    "wobble": 0.0,
                    "swell": 0.5,
                    "noise": 0.12,
                },
                "plot_marker_cycle": ["o", {"marker": "s", "hollow": True}],
                "plot_network_group_linestyle": ":",
            }
        )
        figure = NetworkChart(
            NETWORK, directed=True, layout="grouped", show_legend=True
        )
        ax = figure.axes[0]
        edges = [p for p in ax.patches if (p.get_gid() or "").startswith("edge:")]
        self.assertTrue(all(ink_effects(edge) for edge in edges))
        self.assertTrue(all(edge.get_linewidth() > 0 for edge in edges))
        rings = [p for p in ax.patches if (p.get_gid() or "").startswith("group:")]
        self.assertTrue(rings)
        self.assertEqual(rings[0].get_facecolor()[3], 0.0)
        self.assertEqual(rings[0].get_linestyle(), ":")
        nodes = [c for c in ax.collections if c.get_gid() == "nodes"]
        self.assertEqual([len(c.get_offsets()) for c in nodes], [2, 1])
        self.assertEqual(len(nodes[1].get_facecolors()), 0)
        handle = ax.get_legend().legend_handles[1]
        self.assertEqual(handle.get_marker(), "s")
        self.assertEqual(handle.get_markerfacecolor(), "none")
        png(figure)

    def test_node_label_position(self):
        centred = NetworkChart(NETWORK).axes[0].texts[0]
        self.assertEqual(centred.get_va(), "center")
        above = NetworkChart(NETWORK, label_position="above").axes[0].texts[0]
        self.assertEqual(above.get_va(), "bottom")
        config.update_config({"chart_default_node_label_position": "above"})
        self.assertEqual(NetworkChart(NETWORK).axes[0].texts[0].get_va(), "bottom")
        explicit = NetworkChart(NETWORK, label_position="center").axes[0].texts[0]
        self.assertEqual(explicit.get_va(), "center")
        with self.assertRaises(ValueError):
            NetworkChart(NETWORK, label_position="below")


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
