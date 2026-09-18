import unittest
import warnings

from matplotlib.colors import to_hex

from datachart.utils._internal.colors import (
    get_color_scale,
    get_discrete_colors,
    get_colormap,
    create_colormap,
)
from datachart.constants import COLORS

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
            ["#0C2C84", "#7FCDBB", "#1D91C0", "#C7E9B4", "#225EA8", "#41B6C4"],
        )
        self.assertEqual(get_color_scale(COLORS.PaperAccent), ["#5B84C4", "#C85450"])

    def test_custom_palettes_cycle_not_interpolate(self):
        """Test that custom palettes cycle like explicit color lists."""
        colors = get_discrete_colors(COLORS.PaperAccent, 3)
        self.assertEqual(colors, ["#5B84C4", "#C85450", "#5B84C4"])
        colors = get_discrete_colors(COLORS.PaperYlGnBu, 2)
        self.assertEqual(colors, ["#0C2C84", "#7FCDBB"])

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


if __name__ == "__main__":
    unittest.main()
