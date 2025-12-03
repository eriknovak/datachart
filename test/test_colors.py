import unittest

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
        """Test that various pypalettes palettes can be loaded."""
        palettes_to_test = [
            COLORS.Blues,
            COLORS.Greens,
            COLORS.Spectral,
            COLORS.Viridis,
            COLORS.Greys,
            COLORS.Set2,
        ]

        for palette_name in palettes_to_test:
            color_scale = get_color_scale(palette_name)
            self.assertIsInstance(
                color_scale, list, f"Palette {palette_name} did not return a list."
            )
            self.assertGreater(
                len(color_scale), 0, f"Palette {palette_name} returned empty list."
            )


if __name__ == "__main__":
    unittest.main()
