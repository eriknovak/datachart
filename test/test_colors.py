import unittest

from datachart.themes.colors import COLOR_SCALE_MAPPING
from datachart.utils.colors import (
    get_color_scale,
    get_discrete_colors,
)
from datachart.constants import COLORS

TEST_COLOR_SCALE = COLORS.Blue
COLOR_SCALE_BLUE = COLOR_SCALE_MAPPING[TEST_COLOR_SCALE]


class TestColors(unittest.TestCase):
    def test_color_amount(self):
        self.assertEqual(
            len(COLOR_SCALE_MAPPING.keys()),
            20,
            "The number of color scales is incorrect.",
        )

    def test_get_color_scale(self):
        color_scale = get_color_scale(TEST_COLOR_SCALE)
        self.assertEqual(
            isinstance(color_scale, list), True, "The color scale is not a list."
        )
        self.assertEqual(color_scale, COLOR_SCALE_BLUE, "The color scale is incorrect.")

    def test_get_discrete_colors(self):
        test_cases = [
            {"max_colors": 1, "scale": [COLOR_SCALE_BLUE[-1], COLOR_SCALE_BLUE[-1]]},
            {"max_colors": 5, "scale": [COLOR_SCALE_BLUE[0], COLOR_SCALE_BLUE[-1]]},
            {"max_colors": 20, "scale": [COLOR_SCALE_BLUE[0], COLOR_SCALE_BLUE[-1]]},
        ]

        for test_case in test_cases:
            max_colors = test_case["max_colors"]

            color_scale = get_discrete_colors(TEST_COLOR_SCALE, max_colors)
            self.assertEqual(
                len(color_scale),
                max_colors,
                "The number of discrete colors is incorrect.",
            )
            self.assertEqual(
                [color_scale[0], color_scale[-1]],
                test_case["scale"],
                f"The discrete colors does not return the correct colors for max_colors=${max_colors}.",
            )


if __name__ == "__main__":
    unittest.main()
