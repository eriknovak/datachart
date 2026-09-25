import unittest
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

from datachart.charts import (
    BarChart,
    Histogram,
    LineChart,
    ScatterChart,
    StackedAreaChart,
)
from datachart.config import config
from datachart.utils import Panel
from datachart.utils._internal.colors import (
    cycling_colors,
    get_color_scale,
    get_discrete_colors,
    get_colormap,
    create_colormap,
    warn_palette_overflow,
)
from datachart.constants import COLORS, THEME

# Use a pypalettes palette for testing
TEST_COLOR_SCALE = COLORS.Blues


# =====================================
# Test Colors
# =====================================


class TestColors(unittest.TestCase):
    def test_get_color_scale(self):
        """Test that get_color_scale returns a list of colors."""
        color_scale = get_color_scale(TEST_COLOR_SCALE)
        self.assertIsInstance(color_scale, list, "The color scale is not a list.")
        self.assertGreater(len(color_scale), 0, "The color scale is empty.")
        # Check that colors are strings (hex codes)
        for color in color_scale:
            self.assertIsInstance(color, str, "Color is not a string.")

    def test_get_color_scale_invalid_name(self):
        """Test that invalid palette names fallback to default."""
        # Should not raise, should return default palette with warning
        color_scale = get_color_scale("invalid_palette_name_12345")
        self.assertIsInstance(color_scale, list, "Fallback color scale is not a list.")
        self.assertGreater(len(color_scale), 0, "Fallback color scale is empty.")

    def test_get_discrete_colors(self):
        """Test that get_discrete_colors returns the correct number of colors."""
        test_cases = [1, 5, 10, 20]

        for max_colors in test_cases:
            color_scale = get_discrete_colors(TEST_COLOR_SCALE, max_colors)
            self.assertEqual(
                len(color_scale),
                max_colors,
                f"The number of discrete colors is incorrect for max_colors={max_colors}.",
            )
            # Check that all colors are hex strings
            for color in color_scale:
                self.assertIsInstance(color, str, "Discrete color is not a string.")
                self.assertTrue(
                    color.startswith("#"), f"Color {color} is not a hex color."
                )

    def test_get_colormap(self):
        """Test that get_colormap returns a valid colormap object."""
        cmap = get_colormap(TEST_COLOR_SCALE)
        # Check that it's callable (colormap interface)
        self.assertTrue(callable(cmap), "Colormap is not callable.")

    def test_create_colormap(self):
        """Test that create_colormap creates a colormap from a list of colors."""
        colors = ["#FF0000", "#00FF00", "#0000FF"]
        cmap = create_colormap(colors, "test_cmap")
        self.assertTrue(callable(cmap), "Created colormap is not callable.")

    def test_various_palettes(self):
        """Test that every COLORS palette resolves without the fallback warning."""
        palettes_to_test = [
            value
            for name, value in vars(COLORS).items()
            if isinstance(value, str) and not name.startswith("_")
        ]

        for palette_name in palettes_to_test:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                color_scale = get_color_scale(palette_name)
            self.assertIsInstance(
                color_scale, list, f"Palette {palette_name} did not return a list."
            )
            self.assertGreater(
                len(color_scale), 0, f"Palette {palette_name} returned empty list."
            )

    def test_custom_palettes(self):
        """Test that the datachart-registered palettes resolve before pypalettes."""
        self.assertEqual(
            get_color_scale(COLORS.PaperYlGnBu),
            ["#1E2E85", "#EAF7B1", "#2165AB", "#85CFBA", "#299DC1"],
        )
        self.assertEqual(get_color_scale(COLORS.PaperAccent), ["#5B84C4", "#C85450"])
        # the derived themes' leads cycle exactly and pass the palette gate
        for name, first in (
            (COLORS.Harbor, "#1F4E79"),
            (COLORS.TolMuted, "#332288"),
            (COLORS.Contrast, "#1F4E79"),
            (COLORS.Rust, "#B5563A"),
            (COLORS.Slate, "#4F6D8F"),
        ):
            with self.subTest(palette=name):
                scale = get_color_scale(name)
                self.assertEqual(scale[0], first)
                self.assertEqual(get_discrete_colors(name, len(scale) + 1)[-1], first)

    def test_custom_palettes_cycle_not_interpolate(self):
        """Test that custom palettes cycle like explicit color lists."""
        colors = get_discrete_colors(COLORS.PaperAccent, 3)
        self.assertEqual(colors, ["#5B84C4", "#C85450", "#5B84C4"])
        colors = get_discrete_colors(COLORS.PaperYlGnBu, 2)
        self.assertEqual(colors, ["#1E2E85", "#EAF7B1"])

    def test_custom_palettes_colormap(self):
        """Test that custom palettes produce a usable colormap."""
        cmap = get_colormap(COLORS.PaperYlGnBu)
        self.assertTrue(callable(cmap), "Custom palette colormap is not callable.")

    def test_plain_color_is_a_one_color_palette(self):
        """Test that a plain color resolves to itself, not to the fallback."""
        for color in ["#B5651D", "tab:blue", "rebeccapurple"]:
            self.assertEqual(get_color_scale(color), [color])
            self.assertEqual(get_discrete_colors(color, 1), [color])

    def test_plain_color_cycles_not_interpolates(self):
        """Test that a plain color repeats when more colors are asked for."""
        self.assertEqual(get_discrete_colors("#B5651D", 3), ["#B5651D"] * 3)

    def test_plain_color_colormap(self):
        """Test that a plain color maps to itself at both ends of the ramp."""
        cmap = get_colormap("#B5651D")
        for position in (0.0, 0.5, 1.0):
            self.assertEqual(to_hex(cmap(position)), "#b5651d")

    def test_single_color_list_colormap(self):
        """Test that a one-color list produces a usable colormap."""
        cmap = create_colormap(["#B5651D"])
        self.assertEqual(to_hex(cmap(0.0)), "#b5651d")

    def test_palette_name_wins_over_color_name(self):
        """Test that names that are both a palette and a color stay palettes."""
        for name in ["Red", "Gold", "pink", "chocolate", "grey"]:
            self.assertGreater(
                len(get_color_scale(name)),
                1,
                f"'{name}' resolved as a plain color instead of a palette.",
            )


class TestPaletteOverflow(unittest.TestCase):
    """More units than a cycling palette has colors warns once (ADR 0075)."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def caught(self, fn):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            fn()
        return [w for w in caught if issubclass(w.category, UserWarning)]

    def test_cycling_palettes_warn_past_their_length(self):
        for palette in (["#111111", "#222222"], COLORS.PaperAccent):
            with self.subTest(palette=palette):
                n = len(cycling_colors(palette))
                self.assertEqual(
                    self.caught(lambda: warn_palette_overflow(palette, n)), []
                )
                (warning,) = self.caught(lambda: warn_palette_overflow(palette, n + 1))
                self.assertIn(f"{n + 1} series", str(warning.message))
                self.assertIn(f"{n} colors", str(warning.message))

    def test_one_color_palette_is_monochrome_by_design(self):
        for palette in ("#B5651D", ["#B5651D"]):
            with self.subTest(palette=palette):
                self.assertEqual(
                    self.caught(lambda: warn_palette_overflow(palette, 3)), []
                )

    def test_interpolating_palette_stays_silent(self):
        self.assertIsNone(cycling_colors(TEST_COLOR_SCALE))
        self.assertEqual(
            self.caught(lambda: warn_palette_overflow(TEST_COLOR_SCALE, 40)), []
        )

    def test_chart_warns_once_when_series_outrun_the_palette(self):
        n = len(config["color_general_multiple"])
        series = [[{"x": 0, "y": i}, {"x": 1, "y": i + 1}] for i in range(n + 1)]
        self.assertEqual(self.caught(lambda: LineChart(data=series[:n])), [])
        caught = self.caught(lambda: LineChart(data=series))
        self.assertEqual(len(caught), 1)
        self.assertIn(f"{n + 1} series", str(caught[0].message))

    def test_scatter_hue_levels_outrun_the_palette(self):
        n = len(config["color_general_multiple"])
        data = [{"x": i, "y": i, "group": f"g{i}"} for i in range(n + 1)]
        (warning,) = self.caught(lambda: ScatterChart(data=data, hue="group"))
        self.assertIn(f"{n + 1} hue levels", str(warning.message))

    def test_own_colored_series_take_no_palette_slot(self):
        """A series coloured in its style draws nothing from the palette (ADR 0077)."""
        n = len(config["color_general_multiple"])
        series = [[{"x": 0, "y": i}, {"x": 1, "y": i + 1}] for i in range(n + 1)]
        colors = [f"#{20 * i + 30:02x}4040" for i in range(n + 1)]
        self.assertEqual(
            self.caught(
                lambda: LineChart(
                    data=series, style=[{"plot_line_color": c} for c in colors]
                )
            ),
            [],
        )
        self.assertEqual(
            self.caught(
                lambda: StackedAreaChart(
                    data=series, style=[{"plot_area_color": c} for c in colors]
                )
            ),
            [],
        )
        figures = [
            LineChart(data=[s], style={"plot_line_color": c})
            for s, c in zip(series, colors)
        ]
        self.assertEqual(self.caught(lambda: Panel(figures)), [])
        bars = [[{"label": "a", "y": i}] for i in range(n + 1)]
        self.assertEqual(
            self.caught(
                lambda: BarChart(
                    data=bars, style=[{"plot_bar_color": c} for c in colors]
                )
            ),
            [],
        )
        samples = [[{"x": i}, {"x": i + 1}] for i in range(n + 1)]
        self.assertEqual(
            self.caught(
                lambda: Histogram(
                    data=samples, style=[{"plot_hist_color": c} for c in colors]
                )
            ),
            [],
        )

    def test_own_colored_series_do_not_advance_the_cycle(self):
        palette = config["color_general_multiple"]
        series = [[{"x": 0, "y": i}, {"x": 1, "y": i + 1}] for i in range(2)]
        figure = LineChart(data=series, style=[{"plot_line_color": "#123456"}, {}])
        first, second = figure.axes[0].get_lines()[:2]
        self.assertEqual(to_hex(first.get_color()), "#123456")
        self.assertEqual(to_hex(second.get_color()), to_hex(palette[0]))


if __name__ == "__main__":
    unittest.main()
