"""Tests for `derive_theme`: a theme variant built from a base and a lead (#245)."""

import copy
import unittest

from datachart.config import config
from datachart.constants import COLORS, THEME
from datachart.themes import DARK_THEME, MINIMAL_THEME, derive_theme
from datachart.utils._internal.colors import (
    get_color_scale,
    oklab_lightness as lightness,
)

LEAD_KEYS = (
    "color_general_singular",
    "color_general_multiple",
    "color_parallel_hue_continuous",
    "plot_heatmap_cmap",
    "plot_dumbbell_start_color",
    "plot_dumbbell_end_color",
)


class TestDeriveTheme(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)

    def test_sequential_lead_rebuilds_the_lead_keys(self):
        theme = derive_theme(THEME.MINIMAL, lead=COLORS.Greens)
        self.assertEqual(theme["color_general_singular"], COLORS.Greens)
        self.assertEqual(theme["plot_heatmap_cmap"], COLORS.Greens)
        self.assertEqual(len(theme["color_general_multiple"]), 6)
        self.assertEqual(len(theme["color_parallel_hue_continuous"]), 4)
        self.assertEqual(
            len(set(theme["color_general_multiple"])), 6, "samples are distinct"
        )
        # the ramp runs light to dark, as every predefined theme's does
        ramp = [lightness(c) for c in theme["color_parallel_hue_continuous"]]
        self.assertEqual(ramp, sorted(ramp, reverse=True))
        # the dumbbell pair spans the palette, light start to dark end
        self.assertGreater(
            lightness(theme["plot_dumbbell_start_color"]),
            lightness(theme["plot_dumbbell_end_color"]),
        )

    def test_furniture_and_diverging_map_are_untouched(self):
        theme = derive_theme(THEME.MINIMAL, lead=COLORS.Greens)
        for key, value in MINIMAL_THEME.items():
            if key not in LEAD_KEYS:
                self.assertEqual(theme[key], value, key)

    def test_result_registers_as_a_theme(self):
        config.register_theme("forest", derive_theme(THEME.MINIMAL, lead=COLORS.Greens))
        config.set_theme("forest")
        self.assertEqual(config.theme, "forest")
        self.assertEqual(config["plot_heatmap_cmap"], COLORS.Greens)

    def test_base_is_not_mutated(self):
        before = copy.deepcopy(MINIMAL_THEME)
        derived = derive_theme(MINIMAL_THEME, lead=COLORS.Reds)
        derived["color_general_multiple"].append("#000000")
        self.assertEqual(MINIMAL_THEME, before)

    def test_categorical_lead_keeps_the_base_value_scale(self):
        theme = derive_theme(THEME.MINIMAL, lead=COLORS.Tab10)
        # the colors themselves, so a series never draws a blend of two of them
        self.assertEqual(theme["color_general_multiple"], get_color_scale(COLORS.Tab10))
        self.assertEqual(theme["color_general_singular"], "#1f77b4")
        for key in LEAD_KEYS[2:]:
            self.assertEqual(theme[key], MINIMAL_THEME[key], key)

    def test_list_leads_infer_their_kind(self):
        ramp = derive_theme(THEME.DEFAULT, lead=["#F7FBFF", "#6BAED6", "#08306B"])
        self.assertEqual(len(ramp["color_general_multiple"]), 6)
        swatches = ["#0B3954", "#E0FF4F", "#FF6663"]
        flat = derive_theme(THEME.DEFAULT, lead=swatches)
        self.assertEqual(flat["color_general_multiple"], swatches)
        self.assertEqual(flat["color_general_singular"], "#0B3954")

    def test_dark_base_keeps_the_palette_off_the_page(self):
        light = derive_theme(THEME.MINIMAL, lead=COLORS.Greens)
        dark = derive_theme(THEME.DARK, lead=COLORS.Greens)
        self.assertGreater(
            min(lightness(c) for c in dark["color_general_multiple"]),
            min(lightness(c) for c in light["color_general_multiple"]),
        )
        self.assertGreater(
            max(lightness(c) for c in dark["color_general_multiple"]),
            max(lightness(c) for c in light["color_general_multiple"]),
        )
        self.assertEqual(dark["figure_facecolor"], DARK_THEME["figure_facecolor"])
        # a transparent page is not a dark page
        clear = derive_theme({"figure_facecolor": "none"}, lead=COLORS.Greens)
        self.assertEqual(
            clear["color_general_multiple"], light["color_general_multiple"]
        )

    def test_overrides_apply_and_unknown_keys_raise(self):
        theme = derive_theme(THEME.INK, lead=COLORS.Reds, font_general_family="serif")
        self.assertEqual(theme["font_general_family"], "serif")
        with self.assertRaises(ValueError):
            derive_theme(THEME.INK, lead=COLORS.Reds, font_family="serif")

    def test_unknown_base_raises(self):
        with self.assertRaises(ValueError):
            derive_theme("no-such-theme", lead=COLORS.Reds)

    def test_single_color_lead_raises(self):
        with self.assertRaises(ValueError):
            derive_theme(THEME.DEFAULT, lead="#B5651D")


if __name__ == "__main__":
    unittest.main()
