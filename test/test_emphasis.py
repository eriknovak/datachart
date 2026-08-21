"""Tests for the per-chart emphasis mechanism (ADR 0009) and theme renames."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import (
    BarChart,
    BoxPlot,
    Heatmap,
    Histogram,
    LineChart,
    ParallelCoords,
    ScatterChart,
)
from datachart.config import config
from datachart.constants import THEME
from datachart.utils import Panel

LINE1 = [{"x": i, "y": i} for i in range(5)]
LINE2 = [{"x": i, "y": 2 * i} for i in range(5)]
LINE3 = [{"x": i, "y": 2.5 * i} for i in range(5)]
BAR1 = [{"label": c, "y": v} for c, v in zip("ABC", [3.0, 5.0, 4.0])]
BAR2 = [{"label": c, "y": v} for c, v in zip("ABC", [2.0, 6.0, 1.0])]
HIST1 = [{"x": float(v)} for v in [0, 1, 1, 2, 2, 2, 3, 3, 4]]
HIST2 = [{"x": float(v)} for v in [2, 3, 3, 4, 4, 4, 5, 5, 6]]
SCAT1 = [{"x": i, "y": i} for i in range(8)]
SCAT2 = [{"x": i, "y": 2 * i} for i in range(8)]


def data_lines(ax):
    """The axes' data lines (legend proxies excluded)."""
    return list(ax.lines)


class TestThemeRenames(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_new_theme_constants(self):
        self.assertEqual(THEME.INK, "ink")
        self.assertEqual(THEME.HATCH, "hatch")
        for name in ("PUBLICATION", "ACADEMIC", "BACKGROUND"):
            self.assertFalse(hasattr(THEME, name))

    def test_emphasis_constants(self):
        from datachart.constants import EMPHASIS

        self.assertEqual(EMPHASIS.BACKGROUND, "background")
        self.assertEqual(EMPHASIS.HIGHLIGHT, "highlight")

    def test_new_themes_apply(self):
        for theme in (THEME.INK, THEME.HATCH):
            config.set_theme(theme)
            self.assertEqual(config.theme, theme)

    def test_theme_exports(self):
        from datachart import themes

        self.assertTrue(hasattr(themes, "INK_THEME"))
        self.assertTrue(hasattr(themes, "HATCH_THEME"))
        for name in ("PUBLICATION_THEME", "ACADEMIC_THEME", "BACKGROUND_THEME"):
            self.assertFalse(hasattr(themes, name))

    def test_hatch_uses_ink_sans_stack(self):
        from datachart.themes import HATCH_THEME, INK_THEME

        self.assertEqual(HATCH_THEME["font_general_family"], "sans-serif")
        self.assertEqual(
            HATCH_THEME["font_general_sansserif"],
            INK_THEME["font_general_sansserif"],
        )
        self.assertIsNone(HATCH_THEME["font_general_serif"])
        # the hatch identity stays
        self.assertEqual(HATCH_THEME["plot_hatch_cycle"], ["", "//", ".."])

    def test_muted_attrs_in_every_theme(self):
        from datachart.themes import (
            DEFAULT_THEME,
            GREYSCALE_THEME,
            HATCH_THEME,
            INK_THEME,
            MATERIAL_THEME,
            MINIMAL_THEME,
        )

        for theme in (
            DEFAULT_THEME,
            GREYSCALE_THEME,
            INK_THEME,
            HATCH_THEME,
            MINIMAL_THEME,
            MATERIAL_THEME,
        ):
            self.assertIn("muted_color", theme)
            self.assertIn("muted_alpha", theme)
        self.assertEqual(DEFAULT_THEME["muted_color"], "#CFCFCF")


class TestEmphasisValidation(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_invalid_value_raises(self):
        with self.assertRaises(ValueError):
            LineChart([LINE1, LINE2], emphasis=["background", "bold"])

    def test_heatmap_rejects_emphasis(self):
        with self.assertRaises(ValueError):
            Heatmap([[1.0, 2.0], [3.0, 4.0]], emphasis="background")

    def test_panel_rejects_invalid_emphasis(self):
        fig = LineChart(LINE1)
        with self.assertRaises(ValueError):
            Panel([{"figure": fig, "emphasis": "bold"}])


class TestMutedTransform(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_background_line_is_muted(self):
        figure = LineChart(
            [LINE1, LINE2],
            subtitle=["ctx", "main"],
            emphasis=["background", None],
        )
        bg, fg = data_lines(figure.axes[0])
        self.assertEqual(bg.get_color(), config["muted_color"])
        self.assertEqual(bg.get_alpha(), config["muted_alpha"])
        self.assertLess(bg.get_linewidth(), fg.get_linewidth())
        self.assertLess(bg.get_zorder(), fg.get_zorder())

    def test_muted_overrides_explicit_style_color(self):
        figure = LineChart(
            [LINE1, LINE2],
            emphasis=["background", None],
            style=[{"plot_line_color": "#FF0000"}, None],
        )
        bg = data_lines(figure.axes[0])[0]
        self.assertEqual(bg.get_color(), config["muted_color"])

    def test_muted_color_follows_theme(self):
        config.update_config({"muted_color": "#ABCDEF"})
        figure = LineChart([LINE1, LINE2], emphasis=["background", None])
        bg = data_lines(figure.axes[0])[0]
        self.assertEqual(bg.get_color(), "#ABCDEF")

    def test_highlight_line_is_bolder_and_in_front(self):
        figure = LineChart([LINE1, LINE2], emphasis=[None, "highlight"])
        base, hi = data_lines(figure.axes[0])
        self.assertAlmostEqual(hi.get_linewidth(), base.get_linewidth() * 2)
        self.assertGreater(hi.get_zorder(), base.get_zorder())

    def test_highlight_keeps_cycle_color_and_legend(self):
        plain = LineChart([LINE1, LINE2], show_legend=True)
        emphasized = LineChart(
            [LINE1, LINE2], emphasis=[None, "highlight"], show_legend=True
        )
        plain_colors = [l.get_color() for l in data_lines(plain.axes[0])]
        emph_colors = [l.get_color() for l in data_lines(emphasized.axes[0])]
        self.assertEqual(plain_colors, emph_colors)

    def test_no_emphasis_matches_current_output(self):
        with_kwarg = LineChart([LINE1, LINE2], emphasis=None)
        without = LineChart([LINE1, LINE2])
        for a, b in zip(data_lines(with_kwarg.axes[0]), data_lines(without.axes[0])):
            self.assertEqual(a.get_color(), b.get_color())
            self.assertEqual(a.get_linewidth(), b.get_linewidth())
            self.assertEqual(a.get_zorder(), b.get_zorder())

    def test_background_bar_is_muted(self):
        figure = BarChart([BAR1, BAR2], emphasis=["background", None])
        bg_patch = figure.axes[0].containers[0].patches[0]
        self.assertEqual(bg_patch.get_alpha(), config["muted_alpha"])

    def test_background_scatter_is_muted(self):
        figure = ScatterChart([SCAT1, SCAT2], emphasis=["background", None])
        bg = figure.axes[0].collections[0]
        self.assertEqual(bg.get_alpha(), config["muted_alpha"])


class TestLegendAndCycle(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_background_excluded_from_legend(self):
        figure = LineChart(
            [LINE1, LINE2],
            subtitle=["ctx", "main"],
            emphasis=["background", None],
            show_legend=True,
        )
        legend = figure.axes[0].get_legend()
        labels = [t.get_text() for t in legend.get_texts()]
        self.assertEqual(labels, ["main"])

    def test_background_skips_color_cycle_slot(self):
        """The remaining series get the same colors as if drawn alone."""
        emphasized = LineChart(
            [LINE1, LINE2, LINE3], emphasis=["background", None, None]
        )
        plain = LineChart([LINE2, LINE3])
        emph_colors = [l.get_color() for l in data_lines(emphasized.axes[0])][1:]
        plain_colors = [l.get_color() for l in data_lines(plain.axes[0])]
        self.assertEqual(emph_colors, plain_colors)


class TestBoxEmphasis(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    @staticmethod
    def _box_data():
        return [
            {"label": lab, "value": float(v + off)}
            for lab, off in [("A", 0), ("B", 2), ("C", 4)]
            for v in [1, 2, 3, 4, 5]
        ]

    def test_per_label_box_emphasis(self):
        figure = BoxPlot(self._box_data(), emphasis=["background", None, "highlight"])
        ax = figure.axes[0]
        boxes = [p for p in ax.patches if hasattr(p, "get_path")]
        self.assertEqual(len(boxes), 3)
        self.assertEqual(boxes[0].get_alpha(), config["muted_alpha"])
        # background box whiskers mute with the box (whiskers 0,1 belong to box A)
        whisker = ax.lines[0]
        self.assertEqual(
            matplotlib.colors.to_hex(whisker.get_color()).upper(),
            config["muted_color"],
        )

    def test_box_emphasis_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            BoxPlot(self._box_data(), emphasis=["background", None])

    def test_box_single_value_applies_to_all(self):
        figure = BoxPlot(self._box_data(), emphasis="background")
        boxes = [p for p in figure.axes[0].patches if hasattr(p, "get_path")]
        for box in boxes:
            self.assertEqual(box.get_alpha(), config["muted_alpha"])


class TestParallelEmphasis(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    @staticmethod
    def _rows(scale=1.0, n=4):
        return [{"a": float(i * scale), "b": float((n - i) * scale)} for i in range(n)]

    def test_per_row_emphasis(self):
        rows = self._rows()
        figure = ParallelCoords(
            rows,
            dimensions=["a", "b"],
            emphasis=["highlight"] + ["background"] * (len(rows) - 1),
        )
        ax = figure.axes[0]
        # data rows draw first; axis/tick furniture lines come after
        row_lines = ax.lines[: len(rows)]
        hi, bg = row_lines[0], row_lines[1]
        self.assertEqual(bg.get_color(), config["muted_color"])
        self.assertAlmostEqual(hi.get_linewidth(), bg.get_linewidth() / 0.75 * 2)
        # highlight stays below the parallel axis furniture (zorder 2)
        self.assertLess(hi.get_zorder(), 2)
        self.assertGreater(hi.get_zorder(), bg.get_zorder())

    def test_shared_normalization_across_panel_layers(self):
        """Two composed parallel figures share per-dimension ranges."""
        f1 = ParallelCoords(self._rows(scale=1.0), dimensions=["a", "b"])
        f2 = ParallelCoords(self._rows(scale=10.0), dimensions=["a", "b"])
        panel = Panel([f1, f2])
        ax = panel.axes[0]
        rows = ax.lines[:8]
        # under shared ranges the small-scale rows compress toward the bottom
        small_max = max(max(l.get_ydata()) for l in rows[:4])
        large_max = max(max(l.get_ydata()) for l in rows[4:])
        self.assertLess(small_max, 0.2)
        self.assertAlmostEqual(large_max, 1.0)
        # axis furniture draws once, with the combined range labels
        texts = [t.get_text() for t in ax.texts]
        self.assertIn("30", [t.replace(".0", "") for t in texts])

    def test_single_layer_normalization_unchanged(self):
        """A single parallel figure keeps today's own-range normalization."""
        figure = ParallelCoords(self._rows(), dimensions=["a", "b"])
        rows = figure.axes[0].lines[:4]
        ymax = max(max(l.get_ydata()) for l in rows)
        self.assertAlmostEqual(ymax, 1.0)


class TestHistogramEmphasis(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_stacked_hist_honors_per_layer_colors(self):
        """Per-series explicit hist colors are honored in the stacked draw."""
        figure = Histogram(
            [HIST1, HIST2],
            style=[{"plot_hist_color": "#112233"}, {"plot_hist_color": "#445566"}],
            num_bins=5,
        )
        ax = figure.axes[0]
        colors = [
            matplotlib.colors.to_hex(c.patches[0].get_facecolor())
            for c in ax.containers
        ]
        self.assertEqual(colors, ["#112233", "#445566"])

    def test_emphasis_switches_stack_to_overlay(self):
        """A muted background makes no sense inside a stack: draw individually."""
        stacked = Histogram([HIST1, HIST2], num_bins=5)
        emphasized = Histogram(
            [HIST1, HIST2], num_bins=5, emphasis=["background", None]
        )
        # stacked bars sit on top of each other; individual draws both start at 0
        stack_bottom = stacked.axes[0].containers[1].patches[2].get_y()
        emph_bottom = emphasized.axes[0].containers[1].patches[2].get_y()
        self.assertGreater(stack_bottom, 0)
        self.assertEqual(emph_bottom, 0)
        bg_patch = emphasized.axes[0].containers[0].patches[0]
        self.assertEqual(bg_patch.get_alpha(), config["muted_alpha"])


class TestPanelEmphasis(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_per_figure_emphasis(self):
        f1 = LineChart(LINE1, subtitle="ctx")
        f2 = LineChart(LINE2, subtitle="main")
        panel = Panel(
            [{"figure": f1, "emphasis": "background"}, {"figure": f2}],
            show_legend=True,
        )
        bg, fg = data_lines(panel.axes[0])
        self.assertEqual(bg.get_color(), config["muted_color"])
        labels = [t.get_text() for t in panel.axes[0].get_legend().get_texts()]
        self.assertEqual(labels, ["main"])

    def test_nested_panel_keeps_emphasis(self):
        f1 = LineChart(LINE1, subtitle="ctx")
        f2 = LineChart(LINE2, subtitle="main")
        inner = Panel([{"figure": f1, "emphasis": "background"}, {"figure": f2}])
        f3 = LineChart(LINE3, subtitle="extra")
        outer = Panel([inner, f3], show_legend=True)
        bg = data_lines(outer.axes[0])[0]
        self.assertEqual(bg.get_color(), config["muted_color"])
        labels = [t.get_text() for t in outer.axes[0].get_legend().get_texts()]
        self.assertEqual(labels, ["main", "extra"])


if __name__ == "__main__":
    unittest.main()
