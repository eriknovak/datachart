"""Tests for theme-driven defaults and cycles (ADR 0004) and the value-label fixes."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import BarChart, Heatmap, LineChart
from datachart.config import config
from datachart.constants import THEME
from datachart.utils import Grid, Panel

BAR = [{"label": label, "y": y} for label, y in zip("ABC", [3.0, 5.0, 4.0])]
BAR2 = [{"label": label, "y": y} for label, y in zip("ABC", [2.0, 6.0, 1.0])]
HEAT = [[0.0, 0.5], [0.8, 1.0]]


def grid_visible(ax, axis):
    lines = ax.yaxis.get_gridlines() if axis == "y" else ax.xaxis.get_gridlines()
    return any(line.get_visible() for line in lines)


class TestThemeDefaults(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_theme_grid_default_applies(self):
        """A theme's grid default applies when the chart call leaves it unset."""
        figure = BarChart(BAR)
        self.assertTrue(grid_visible(figure.axes[0], "y"))

    def test_explicit_show_grid_wins(self):
        """An explicit chart setting always wins over the theme default."""
        figure = BarChart(BAR, show_grid="x")
        self.assertTrue(grid_visible(figure.axes[0], "x"))
        self.assertFalse(grid_visible(figure.axes[0], "y"))

    def test_none_theme_default_leaves_grid_off(self):
        """A `None` theme default preserves the no-grid behavior."""
        config.update_config({"chart_default_show_grid": None})
        figure = BarChart(BAR)
        self.assertFalse(grid_visible(figure.axes[0], "y"))
        self.assertFalse(grid_visible(figure.axes[0], "x"))

    def test_grid_default_skips_heatmaps(self):
        """The theme grid default never applies to heatmaps."""
        figure = Heatmap(HEAT)
        self.assertFalse(grid_visible(figure.axes[0], "y"))

    def test_theme_show_values_default_applies(self):
        """Themes shipping `chart_default_show_values` label bars by default."""
        config.set_theme(THEME.MINIMAL)
        figure = BarChart(BAR)
        labels = [text.get_text() for text in figure.axes[0].texts]
        self.assertEqual(labels, ["3", "5", "4"])

    def test_explicit_show_values_wins(self):
        """`show_values=False` beats the theme's on-by-default."""
        config.set_theme(THEME.MINIMAL)
        figure = BarChart(BAR, show_values=False)
        self.assertEqual(list(figure.axes[0].texts), [])

    def test_show_values_without_format_does_not_crash(self):
        """`show_values=True` with no `value_format` defaults the format."""
        figure = BarChart(BAR, show_values=True)
        labels = [text.get_text() for text in figure.axes[0].texts]
        self.assertEqual(labels, ["3", "5", "4"])

    def test_value_headroom_expands_axis(self):
        """Value labels expand the value-axis limits so they stay inside."""
        plain = BarChart(BAR)
        labeled = BarChart(BAR, show_values=True)
        self.assertGreater(labeled.axes[0].get_ylim()[1], plain.axes[0].get_ylim()[1])

    def test_heatmap_contrast_skips_light_colormaps(self):
        """Light colormaps never flip value text to white."""
        figure = Heatmap(
            [[0.0, 1.0]],
            show_heatmap_values=True,
            style={"plot_heatmap_cmap": ["#F7F7F7", "#B0B0B0"]},
        )
        colors = {text.get_color() for text in figure.axes[0].texts}
        self.assertNotIn("#FFFFFF", colors)

    def test_theme_constants_are_valid(self):
        """Every THEME constant applies without warnings."""
        for theme in [THEME.MINIMAL, THEME.MATERIAL, THEME.INK, THEME.HATCH]:
            config.set_theme(theme)
            self.assertEqual(config.theme, theme)


class TestHatchCycle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_hatch_cycle_assigns_per_series(self):
        """The theme's hatch cycle assigns one pattern per bar series."""
        config.set_theme(THEME.HATCH)
        figure = BarChart([BAR, BAR2], show_values=False)
        hatches = [
            container.patches[0].get_hatch() for container in figure.axes[0].containers
        ]
        self.assertEqual(hatches, [None, "//"])

    def test_explicit_hatch_style_wins(self):
        """An explicit per-chart hatch beats the cycle."""
        config.set_theme(THEME.HATCH)
        figure = BarChart(
            [BAR, BAR2],
            style=[{"plot_bar_hatch": "xx"}, {"plot_bar_hatch": "oo"}],
            show_values=False,
        )
        hatches = [
            container.patches[0].get_hatch() for container in figure.axes[0].containers
        ]
        self.assertEqual(hatches, ["xx", "oo"])

    def test_no_cycle_means_no_hatches(self):
        """Themes without a hatch cycle draw unhatched bars."""
        figure = BarChart([BAR, BAR2])
        hatches = [
            container.patches[0].get_hatch() for container in figure.axes[0].containers
        ]
        self.assertEqual(hatches, [None, None])


class TestFurnitureConsistency(unittest.TestCase):
    """Composed figures carry the same themed label/tick furniture as fronts."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    @staticmethod
    def _twin_panel():
        left = LineChart([{"x": x, "y": x} for x in range(5)])
        right = LineChart([{"x": x, "y": x * 100} for x in range(5)])
        panel = Panel(
            [
                {"figure": left, "y_axis": "left"},
                {"figure": right, "y_axis": "right"},
            ],
            title="Twin",
            xlabel="X",
            ylabel_left="L",
            ylabel_right="R",
        )
        plt.close(left)
        plt.close(right)
        return panel

    def test_panel_axis_labels_take_theme_fonts(self):
        panel = self._twin_panel()
        ax_left, ax_right = panel.axes[0], panel.axes[1]
        self.assertEqual(ax_left.xaxis.label.get_fontsize(), config["font_xlabel_size"])
        self.assertEqual(ax_left.yaxis.label.get_fontsize(), config["font_ylabel_size"])
        self.assertEqual(
            ax_right.yaxis.label.get_fontsize(), config["font_ylabel_size"]
        )

    def test_standalone_panel_title_stays_suptitle(self):
        """A standalone Panel keeps its title as a title-styled suptitle."""
        panel = self._twin_panel()
        self.assertEqual(panel._suptitle.get_text(), "Twin")
        self.assertEqual(panel._suptitle.get_fontsize(), config["font_title_size"])
        self.assertEqual(panel.axes[0].get_title(), "")

    def test_grid_cell_titles_share_subtitle_style(self):
        """Plain-chart and Panel cells title at the same (subtitle) size."""
        bar = BarChart(BAR, title="Bar")
        panel = self._twin_panel()
        grid = Grid([bar, panel])
        titles = {
            ax.get_title(): ax.title.get_fontsize()
            for ax in grid.axes
            if ax.get_title()
        }
        self.assertEqual(
            titles,
            {
                "Bar": config["font_subtitle_size"],
                "Twin": config["font_subtitle_size"],
            },
        )
        plt.close(bar)
        plt.close(panel)

    def test_tick_labels_take_theme_font_color(self):
        config.set_theme(THEME.MINIMAL)
        figure = BarChart(BAR)
        label = figure.axes[0].yaxis.get_ticklabels()[0]
        self.assertEqual(label.get_color(), config["font_general_color"])
        panel = self._twin_panel()
        for ax in panel.axes:
            for tick_label in ax.yaxis.get_ticklabels():
                self.assertEqual(tick_label.get_color(), config["font_general_color"])

    def test_grayscale_keeps_base_parallel_label_sizes(self):
        """GREYSCALE inherits the base parallel-coords label sizes unchanged."""
        config.set_theme(THEME.DEFAULT)
        base_sizes = {
            key: config[key]
            for key in (
                "plot_parallel_tick_label_size",
                "plot_parallel_dim_label_size",
            )
        }
        config.set_theme(THEME.GREYSCALE)
        for key, value in base_sizes.items():
            self.assertEqual(config[key], value)


if __name__ == "__main__":
    unittest.main()
