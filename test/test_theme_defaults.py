"""Tests for theme-driven defaults and cycles (ADR 0004) and the value-label fixes."""

import unittest
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from datachart.charts import BarChart, Heatmap, LineChart, RadialChart, RidgelinePlot
from datachart.config import config
from datachart.constants import THEME
from datachart.config.configuration import THEMES
from datachart.utils import Grid, Panel

BAR = [{"label": label, "y": y} for label, y in zip("ABC", [3.0, 5.0, 4.0])]
BAR2 = [{"label": label, "y": y} for label, y in zip("ABC", [2.0, 6.0, 1.0])]
HEAT = {"z": [[0.0, 0.5], [0.8, 1.0]]}
LINE = [{"x": x, "y": x * x} for x in range(5)]
RADIAL = [{"label": d, "y": y} for d, y in zip("NESW", [4.0, 7.0, 3.0, 6.0])]


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

    def test_false_draws_no_grid_over_a_theme_default(self):
        """`show_grid=False` is the off switch, whatever the theme asks for."""
        for front, data in ((BarChart, BAR), (LineChart, LINE)):
            with self.subTest(front=front.__name__):
                ax = front(data, show_grid=False).axes[0]
                self.assertFalse(grid_visible(ax, "x"))
                self.assertFalse(grid_visible(ax, "y"))

    def test_false_draws_no_grid_in_a_panel(self):
        """A `Panel` takes the same off switch as a chart front."""
        ax = Panel([LineChart(LINE)], show_grid=False).axes[0]
        self.assertFalse(grid_visible(ax, "x"))
        self.assertFalse(grid_visible(ax, "y"))

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

    def test_predefined_themes_leave_values_off(self):
        """No predefined theme turns value labels on by default."""
        for theme in [
            THEME.DEFAULT,
            THEME.GREYSCALE,
            THEME.INK,
            THEME.HATCH,
            THEME.MINIMAL,
            THEME.MATERIAL,
            THEME.SKETCH,
            THEME.QUILL,
        ]:
            config.set_theme(theme)
            figure = BarChart(BAR)
            self.assertEqual(list(figure.axes[0].texts), [], theme)

    def test_theme_show_values_default_applies(self):
        """A theme shipping `chart_default_show_values` labels bars by default."""
        config.update_config({"chart_default_show_values": True})
        figure = BarChart(BAR)
        labels = [text.get_text() for text in figure.axes[0].texts]
        self.assertEqual(labels, ["3", "5", "4"])

    def test_explicit_show_values_wins(self):
        """`show_values=False` beats the theme's on-by-default."""
        config.update_config({"chart_default_show_values": True})
        figure = BarChart(BAR, show_values=False)
        self.assertEqual(list(figure.axes[0].texts), [])

    def test_show_values_without_format_does_not_crash(self):
        """`show_values=True` with no `value_format` defaults the format."""
        figure = BarChart(BAR, show_values=True)
        labels = [text.get_text() for text in figure.axes[0].texts]
        self.assertEqual(labels, ["3", "5", "4"])

    def test_value_headroom_expands_axis(self):
        """Value labels expand the value-axis limits so they stay inside."""
        figure = BarChart(BAR, show_values=True)
        figure.canvas.draw()
        ax = figure.axes[0]
        top = max(t.get_window_extent().y1 for t in ax.texts)
        self.assertLessEqual(top, ax.get_window_extent().y1)
        self.assertGreater(ax.get_ylim()[1], max(point["y"] for point in BAR))

    def test_heatmap_contrast_skips_light_colormaps(self):
        """Light colormaps never flip value text to white."""
        figure = Heatmap(
            {"z": [[0.0, 1.0]]},
            show_values=True,
            style={"plot_heatmap_cmap": ["#F7F7F7", "#B0B0B0"]},
        )
        colors = {text.get_color() for text in figure.axes[0].texts}
        self.assertNotIn("#FFFFFF", colors)

    def test_heatmap_cell_borders_off_by_default(self):
        """Without an edge width the heatmap draws no lines between cells."""
        figure = Heatmap(HEAT)
        self.assertEqual(len(figure.axes[0].collections), 0)

    def test_heatmap_cell_borders_follow_edge_style(self):
        """The edge style draws one line along every interior cell boundary."""
        figure = Heatmap(
            {"z": [[1, 2, 3], [4, 5, 6]]},
            style={
                "plot_heatmap_edge_width": 2.0,
                "plot_heatmap_edge_color": "#FF0000",
            },
        )
        ax = figure.axes[0]
        self.assertEqual(len(ax.collections), 1)
        borders = ax.collections[0]
        # one horizontal boundary between 2 rows, two vertical between 3 columns
        self.assertEqual(len(borders.get_segments()), 3)
        self.assertEqual(list(borders.get_linewidths()), [2.0])
        self.assertEqual(matplotlib.colors.to_hex(borders.get_colors()[0]), "#ff0000")
        # the borders never widen the axes beyond the image
        self.assertEqual(ax.get_xlim(), (-0.5, 2.5))

    def test_theme_constants_are_valid(self):
        """Every THEME constant applies without warnings."""
        for theme in [
            THEME.MINIMAL,
            THEME.MATERIAL,
            THEME.INK,
            THEME.HATCH,
            THEME.SKETCH,
            THEME.QUILL,
        ]:
            config.set_theme(theme)
            self.assertEqual(config.theme, theme)

    def test_every_theme_defines_the_text_family(self):
        """Every theme carries the complete plot_text_* family (ADR 0018)."""
        from datachart.typings import TextStyleAttrs

        for theme in [
            THEME.DEFAULT,
            THEME.GREYSCALE,
            THEME.INK,
            THEME.HATCH,
            THEME.MINIMAL,
            THEME.MATERIAL,
            THEME.SKETCH,
            THEME.QUILL,
        ]:
            config.set_theme(theme)
            for key in TextStyleAttrs.__annotations__:
                self.assertIn(key, config.config, f"{theme}: missing {key}")
            # the connector must stay visible when the theme changes
            self.assertIsNotNone(
                config["plot_text_arrow_color"], f"{theme}: arrow color unset"
            )


class TestTickLabelRotation(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def rotations(self, figure):
        ax = figure.axes[0]
        return (
            {label.get_rotation() for label in ax.get_xticklabels()},
            {label.get_rotation() for label in ax.get_yticklabels()},
        )

    def test_unset_rotation_leaves_labels_level(self):
        self.assertEqual(self.rotations(LineChart(data=LINE)), ({0.0}, {0.0}))

    def test_set_rotation_turns_the_labels(self):
        config.update_config(
            {"axes_xticks_label_rotate": 45, "axes_yticks_label_rotate": 30}
        )
        self.assertEqual(self.rotations(LineChart(data=LINE)), ({45.0}, {30.0}))

    def test_chart_rotation_wins_over_the_theme(self):
        config.update_config({"axes_xticks_label_rotate": 45})
        figure = BarChart(data=BAR, xtickrotate=10)
        self.assertEqual(self.rotations(figure)[0], {10.0})

    def test_old_key_warns_and_applies(self):
        with self.assertWarns(DeprecationWarning):
            config.update_config({"plot_xticks_label_rotate": 60})
        self.assertEqual(self.rotations(BarChart(data=BAR))[0], {60.0})


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


class TestColourSafeThemes(unittest.TestCase):
    """The colour-blind-safe themes keep their series apart by more than hue."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_palettes_have_distinct_colors(self):
        for theme in (
            THEME.HARBOR,
            THEME.MUTED,
            THEME.CONTRAST,
            THEME.MUTEDHATCH,
            THEME.SLATEHATCH,
            THEME.DARK,
        ):
            with self.subTest(theme=theme):
                config.set_theme(theme)
                colors = config["color_general_multiple"]
                self.assertEqual(len(colors), len(set(colors)))
                self.assertGreaterEqual(len(colors), 5)

    def test_print_themes_carry_a_second_cue(self):
        """MUTED and CONTRAST tell series apart without colour too."""
        for theme in (THEME.MUTED, THEME.CONTRAST):
            with self.subTest(theme=theme):
                config.set_theme(theme)
                n = len(config["color_general_multiple"])
                self.assertEqual(len(config["plot_linestyle_cycle"]), n)
                self.assertEqual(len(config["plot_marker_cycle"]), n)
        config.set_theme(THEME.CONTRAST)
        self.assertEqual(len(config["plot_hatch_cycle"]), 5)

    def test_mutedhatch_pairs_muted_colours_with_contrast_hatches(self):
        config.set_theme(THEME.MUTED)
        muted = config["color_general_multiple"]
        config.set_theme(THEME.CONTRAST)
        hatches = config["plot_hatch_cycle"]
        config.set_theme(THEME.MUTEDHATCH)
        self.assertEqual(config["color_general_multiple"], muted)
        self.assertEqual(config["plot_hatch_cycle"], hatches)
        self.assertEqual(config["plot_heatmap_cmap"], "BuPu")
        series = [[{**p, "y": p["y"] + k} for p in BAR] for k in range(5)]
        figure = BarChart(series, show_values=False)
        drawn = [str(c.patches[0].get_hatch() or "") for c in figure.axes[0].containers]
        self.assertEqual(drawn, ["", "//", "..", "xx", "\\"])

    def test_slatehatch_drops_rust_from_hatch(self):
        config.set_theme(THEME.HATCH)
        hatch = config.config
        rust = "#B5563A"
        self.assertIn(rust, hatch["color_general_multiple"])
        config.set_theme(THEME.SLATEHATCH)
        slate = config.config
        self.assertNotIn(rust, slate["color_general_multiple"])
        self.assertEqual(slate["color_general_multiple"][0], "#4F6D8F")
        self.assertEqual(slate["plot_heatmap_cmap"], "PuBu")
        self.assertEqual(slate["plot_hatch_cycle"], hatch["plot_hatch_cycle"])

    def test_muted_line_styles_differ_per_series(self):
        config.set_theme(THEME.MUTED)
        series = [[{"x": x, "y": x * k} for x in range(5)] for k in (1, 2, 3)]
        figure = LineChart(series)
        styles = [line.get_linestyle() for line in figure.axes[0].get_lines()[:3]]
        self.assertEqual(len(set(styles)), 3)


class TestDarkTheme(unittest.TestCase):
    """DARK inverts the furniture and leaves the marks alone (ADR 0058)."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def luminance(self, color):
        r, g, b = mcolors.to_rgb(color)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def test_the_theme_is_registered(self):
        self.assertIn(THEME.DARK, THEMES)
        config.set_theme(THEME.DARK)
        self.assertEqual(config.theme, THEME.DARK)

    def test_the_theme_is_complete(self):
        """Every base attribute survives the overrides."""
        config.set_theme(THEME.DEFAULT)
        base_keys = set(config.config)
        config.set_theme(THEME.DARK)
        self.assertEqual(set(config.config), base_keys)

    def test_the_background_is_two_tone_and_dark(self):
        config.set_theme(THEME.DARK)
        figure_face = self.luminance(config["figure_facecolor"])
        axes_face = self.luminance(config["axes_facecolor"])
        self.assertLess(figure_face, 0.2)
        self.assertLess(axes_face, 0.2)
        self.assertGreater(axes_face, figure_face)

    def test_every_furniture_colour_reads_on_the_dark_face(self):
        """No furniture attribute is left at its light-theme black."""
        config.set_theme(THEME.DARK)
        for key in (
            "font_general_color",
            "font_title_color",
            "font_subtitle_color",
            "font_xlabel_color",
            "font_ylabel_color",
            "plot_legend_label_color",
            "plot_value_color",
            "plot_text_color",
            "plot_bar_error_color",
            "plot_heatmap_frame_color",
            "plot_calendar_heatmap_month_line_color",
            "plot_parallel_axis_color",
            "plot_parallel_tick_color",
            "plot_parallel_tick_label_color",
            "plot_parallel_dim_label_color",
            "plot_box_edgecolor",
            "plot_box_median_color",
            "plot_box_whisker_color",
            "plot_box_cap_color",
        ):
            with self.subTest(key=key):
                self.assertGreater(self.luminance(config[key]), 0.5)

    def test_the_drawn_furniture_follows_the_theme(self):
        config.set_theme(THEME.DARK)
        figure = LineChart(LINE, title="Dark")
        ax = figure.axes[0]
        self.assertEqual(
            mcolors.to_hex(figure.get_facecolor()).upper(),
            config["figure_facecolor"].upper(),
        )
        self.assertEqual(
            mcolors.to_hex(ax.get_facecolor()).upper(), config["axes_facecolor"].upper()
        )
        self.assertEqual(
            mcolors.to_hex(ax.spines["bottom"].get_edgecolor()).upper(),
            config["axes_spines_color"].upper(),
        )
        label = ax.get_xticklabels()[0]
        self.assertEqual(
            mcolors.to_hex(label.get_color()).upper(),
            config["font_general_color"].upper(),
        )

    def test_the_colorbar_labels_follow_the_theme(self):
        """A colorbar's ticks and outline are furniture too (ADR 0058)."""
        config.set_theme(THEME.DARK)
        figure = Heatmap(HEAT, show_colorbars=True)
        bar_axes = [ax for ax in figure.axes if ax is not figure.axes[0]]
        self.assertTrue(bar_axes)
        labels = bar_axes[0].get_yticklabels() or bar_axes[0].get_xticklabels()
        self.assertTrue(labels)
        for label in labels:
            self.assertGreater(self.luminance(label.get_color()), 0.5)

    def test_a_light_heatmap_cell_keeps_dark_text(self):
        """The cell label follows the cell, not the figure face (ADR 0058)."""
        config.set_theme(THEME.DARK)
        figure = Heatmap(HEAT, show_values=True)
        texts = [t for t in figure.axes[0].texts if t.get_text()]
        self.assertTrue(texts)
        by_value = {t.get_text(): t for t in texts}
        self.assertLess(self.luminance(by_value["1.0"].get_color()), 0.5)

    def test_the_marks_keep_their_own_colours(self):
        """The palette is the theme's own, not a furniture colour."""
        config.set_theme(THEME.DARK)
        colors = config["color_general_multiple"]
        self.assertEqual(len(colors), len(set(colors)))
        face = config["axes_facecolor"]
        for color in colors:
            with self.subTest(color=color):
                self.assertGreater(self.luminance(color) - self.luminance(face), 0.15)


class TestFurnitureFollowsEveryTheme(unittest.TestCase):
    """A colorbar and a polar radius wear the theme's tick color, not black.

    Both were hard-wired to black until DARK needed them light, so every
    theme whose `font_general_color` is not black moved with the fix.
    """

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_the_colorbar_tick_labels_take_the_theme_color(self):
        for theme in THEMES:
            with self.subTest(theme=theme):
                config.set_theme(theme)
                expected = config["font_general_color"]
                figure = Heatmap(HEAT, show_colorbars=True)
                bars = [ax for ax in figure.axes if ax is not figure.axes[0]]
                if not bars:
                    # a value-etch theme draws a stepped legend, not a bar
                    self.assertIsNotNone(config["plot_value_etch"])
                    continue
                labels = bars[0].get_yticklabels() or bars[0].get_xticklabels()
                self.assertTrue(labels)
                for label in labels:
                    self.assertEqual(
                        mcolors.to_hex(label.get_color()).upper(),
                        mcolors.to_hex(expected).upper(),
                    )
                plt.close("all")

    def test_the_radius_labels_take_the_theme_color(self):
        for theme in THEMES:
            with self.subTest(theme=theme):
                config.set_theme(theme)
                expected = config["font_general_color"]
                figure = RadialChart(RADIAL, mark="bar")
                texts = [t for t in figure.axes[0].texts if t.get_text()]
                self.assertTrue(texts)
                for text in texts:
                    self.assertEqual(
                        mcolors.to_hex(text.get_color()).upper(),
                        mcolors.to_hex(expected).upper(),
                    )
                plt.close("all")


class TestDivergingColormapDefaults(unittest.TestCase):
    """Every theme names a diverging heatmap colormap of its own (ADR 0056)."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_every_theme_sets_a_diverging_colormap(self):
        for theme in THEMES:
            with self.subTest(theme=theme):
                config.set_theme(theme)
                self.assertTrue(config["plot_heatmap_cmap_diverging"])

    def test_the_diverging_colormap_differs_from_the_sequential_one(self):
        for theme in THEMES:
            with self.subTest(theme=theme):
                config.set_theme(theme)
                self.assertNotEqual(
                    config["plot_heatmap_cmap_diverging"], config["plot_heatmap_cmap"]
                )

    def test_the_calendar_diverging_colormap_derives_from_the_heatmap_one(self):
        self.assertIsNone(config["plot_calendar_heatmap_cmap_diverging"])


class TestThemeDefaultAliases(unittest.TestCase):
    """The renamed theme-default keys still work for one release, with a warning."""

    RENAMED = {
        "plot_calendar_heatmap_week_start": "chart_default_calendar_heatmap_week_start",
        "plot_ridgeline_overlap": "chart_default_ridgeline_overlap",
        "chart_default_node_label_position": "chart_default_network_label_position",
    }

    def tearDown(self):
        config.reset_config()

    def test_reset_config_carries_the_new_keys_only(self):
        config.reset_config()
        self.assertEqual(
            config.get("chart_default_calendar_heatmap_week_start"), "monday"
        )
        self.assertEqual(config.get("chart_default_ridgeline_overlap"), 0.5)
        self.assertIsNone(config.get("chart_default_network_label_position", "unset"))
        for theme in THEMES.values():
            self.assertFalse(set(self.RENAMED) & set(theme))

    def test_write_warns_and_the_value_round_trips(self):
        with self.assertWarns(DeprecationWarning) as caught:
            config.update_config({"plot_ridgeline_overlap": 0.3})
        self.assertIn("chart_default_ridgeline_overlap", str(caught.warning))
        self.assertEqual(config.get("chart_default_ridgeline_overlap"), 0.3)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            self.assertEqual(config.get("plot_ridgeline_overlap"), 0.3)
            self.assertEqual(config["plot_ridgeline_overlap"], 0.3)

    def test_old_key_in_a_chart_style_still_sets_the_default(self):
        data = [{"label": "a", "value": float(v)} for v in range(10)]
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            figure = RidgelinePlot(data, style={"plot_ridgeline_overlap": 0.0})
        self.assertEqual(
            [str(w.message) for w in caught if w.category is DeprecationWarning],
            [
                "Style key 'plot_ridgeline_overlap' is deprecated; "
                "use 'chart_default_ridgeline_overlap'."
            ],
        )
        self.assertEqual(caught[0].filename, __file__)
        layer = figure._chart_metadata["panel"].groups[0].layers[0]
        self.assertEqual(layer.overlap, 0.0)

    def test_every_alias_warns_naming_its_replacement(self):
        for alias, key in self.RENAMED.items():
            with self.subTest(alias=alias):
                with self.assertWarnsRegex(DeprecationWarning, key):
                    config.update_config({alias: config.get(key)})


if __name__ == "__main__":
    unittest.main()
