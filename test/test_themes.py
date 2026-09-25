"""Tests for `derive_theme`: a theme variant built from a base and a lead (#245)."""

import copy
import unittest
import warnings

from datachart import themes
from datachart.config import config
from datachart.config.configuration import THEMES
from datachart.constants import COLORS, LINE_STYLE, THEME, TRAIT
from datachart.themes import (
    DARK_THEME,
    DEFAULT_THEME,
    HATCH_THEME,
    MINIMAL_THEME,
    MUTED_THEME,
    MUTEDHATCH_THEME,
    SLATEHATCH_THEME,
    PaletteScore,
    derive_theme,
    score_palette,
)
from datachart.themes._base import TRAITS
from datachart.themes.score import palette_colors, theme_palette_score
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


class TestTraits(unittest.TestCase):
    """Traits compose in order on top of the lead (ADR 0074)."""

    def test_trait_sets_its_mark_keys_only(self):
        plain = derive_theme(THEME.DEFAULT, lead=COLORS.TolMuted)
        flat = derive_theme(THEME.DEFAULT, lead=COLORS.TolMuted, traits=[TRAIT.FLAT])
        changed = {k for k in flat if flat[k] != plain[k]}
        self.assertEqual(changed, set(TRAITS[TRAIT.FLAT]))
        self.assertEqual(flat["plot_bar_edge_width"], 0)
        self.assertEqual(flat["font_general_family"], plain["font_general_family"])

    def test_later_trait_wins_a_shared_key(self):
        flat_then_hatched = derive_theme(
            THEME.DEFAULT, lead=COLORS.TolMuted, traits=[TRAIT.FLAT, TRAIT.HATCHED]
        )
        hatched_then_flat = derive_theme(
            THEME.DEFAULT, lead=COLORS.TolMuted, traits=[TRAIT.HATCHED, TRAIT.FLAT]
        )
        self.assertEqual(flat_then_hatched["plot_bar_edge_width"], 0.8)
        self.assertEqual(hatched_then_flat["plot_bar_edge_width"], 0)
        # an override still wins everything
        theme = derive_theme(
            THEME.DEFAULT,
            lead=COLORS.TolMuted,
            traits=[TRAIT.HATCHED],
            plot_bar_edge_width=2,
        )
        self.assertEqual(theme["plot_bar_edge_width"], 2)

    def test_plain_strings_and_unknown_names(self):
        by_string = derive_theme(THEME.DEFAULT, lead=COLORS.TolMuted, traits=["flat"])
        by_member = derive_theme(
            THEME.DEFAULT, lead=COLORS.TolMuted, traits=[TRAIT.FLAT]
        )
        self.assertEqual(by_string, by_member)
        with self.assertRaises(ValueError):
            derive_theme(THEME.DEFAULT, lead=COLORS.TolMuted, traits=["glossy"])
        # the domain's DEFAULT is no trait at all
        plain = derive_theme(THEME.DEFAULT, lead=COLORS.TolMuted)
        self.assertEqual(
            derive_theme(THEME.DEFAULT, lead=COLORS.TolMuted, traits=[TRAIT.DEFAULT]),
            plain,
        )

    def test_bundle_themes_are_derivations(self):
        """The hatched sibling of a theme is that theme plus the trait and its scale."""
        mutedhatch = derive_theme(
            MUTED_THEME,
            lead=COLORS.TolMuted,
            traits=[TRAIT.HATCHED],
            color_general_singular=COLORS.BuPu,
            color_parallel_hue_continuous=MUTEDHATCH_THEME[
                "color_parallel_hue_continuous"
            ],
            plot_heatmap_cmap=COLORS.BuPu,
            plot_heatmap_cmap_diverging=COLORS.BrBG,
        )
        self.assertEqual(mutedhatch, MUTEDHATCH_THEME)
        slatehatch = derive_theme(
            HATCH_THEME,
            lead=COLORS.Slate,
            color_general_singular=COLORS.PuBu,
            color_parallel_hue_continuous=SLATEHATCH_THEME[
                "color_parallel_hue_continuous"
            ],
            plot_dumbbell_start_color="#4F6D8F",
            plot_dumbbell_end_color="#743538",
            plot_heatmap_cmap=COLORS.PuBu,
            plot_heatmap_cmap_diverging=COLORS.BrBG,
        )
        self.assertEqual(slatehatch, SLATEHATCH_THEME)

    def test_trait_keys_are_marks_never_furniture(self):
        for name, trait in TRAITS.items():
            with self.subTest(trait=name):
                self.assertTrue(all(k.startswith("plot_") for k in trait))
                self.assertFalse(
                    any("color_general" in k or "cmap" in k for k in trait)
                )


class TestScorePalette(unittest.TestCase):
    """`score_palette` scores the worst pair of a series palette (ADR 0073)."""

    def test_default_theme_passes(self):
        score = score_palette(DEFAULT_THEME["color_general_multiple"], face="#FFFFFF")
        self.assertIsInstance(score, PaletteScore)
        self.assertEqual(score.verdict, "pass")
        self.assertGreaterEqual(min(score.deutan, score.protan), 8)
        self.assertGreaterEqual(score.normal, 15)

    def test_red_green_fails_under_deutan(self):
        score = score_palette(["#D93025", "#1E8E3E", "#1A73E8"])
        self.assertEqual(score.verdict, "fail")
        self.assertLess(score.deutan, 6)
        self.assertEqual(set(score.worst_pair), {"#D93025", "#1E8E3E"})
        self.assertIn("#D93025 vs #1E8E3E", str(score))

    def test_greys_score_by_lightness_alone(self):
        score = score_palette(["#202020", "#606060", "#A0A0A0", "#E0E0E0"])
        self.assertAlmostEqual(score.deutan, score.normal, places=3)
        self.assertGreater(score.grey_gap, 15)

    def test_contrast_count_needs_a_face(self):
        pale = ["#F0F0F0", "#101010"]
        self.assertEqual(score_palette(pale).low_contrast, 0)
        self.assertEqual(score_palette(pale, face="#FFFFFF").low_contrast, 1)
        self.assertEqual(score_palette(pale, face="#000000").low_contrast, 1)

    def test_named_palette_scores_its_colours(self):
        by_name = score_palette(COLORS.PaperYlGnBu)
        by_list = score_palette(palette_colors(COLORS.PaperYlGnBu))
        self.assertEqual(by_name, by_list)

    def test_one_colour_raises(self):
        with self.assertRaises(ValueError):
            score_palette(["#000000"])


class TestPredefinedThemesPassTheGate(unittest.TestCase):
    """Every predefined theme's series palette passes, with no allowlist."""

    def test_every_theme_passes(self):
        predefined = [name for name in themes.__all__ if name.endswith("_THEME")]
        for name in predefined:
            score = theme_palette_score(getattr(themes, name))
            if score is None:
                continue  # one ink: series differ by pattern, not colour
            with self.subTest(theme=name):
                self.assertEqual(score.verdict, "pass", str(score))


class TestFurnitureDefaults(unittest.TestCase):
    """Every predefined theme keeps its furniture recessive (ADR 0075)."""

    def test_solid_grid_and_no_legend_title(self):
        predefined = [name for name in themes.__all__ if name.endswith("_THEME")]
        for name in predefined:
            theme = getattr(themes, name)
            with self.subTest(theme=name):
                self.assertEqual(theme["plot_grid_linestyle"], LINE_STYLE.SOLID)
                self.assertIsNone(theme["plot_legend_title"])


class TestFailingPaletteWarns(unittest.TestCase):
    """`register_theme` and `derive_theme` warn once on a failing palette."""

    RED_GREEN = ["#D93025", "#1E8E3E", "#1A73E8"]
    # amber and green sit at deutan ΔE 7.8: weak, not a fail
    NEON = ["#00E5FF", "#FF2D95", "#FFB000", "#7DFF5A", "#B26BFF"]

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        for name in ("redgreen", "fine", "neon"):
            THEMES.pop(name, None)

    def test_register_theme_warns_once_at_the_caller(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            config.register_theme(
                "redgreen", {"color_general_multiple": self.RED_GREEN}
            )
        self.assertEqual(len(caught), 1)
        self.assertIs(caught[0].category, UserWarning)
        self.assertIn("#D93025 vs #1E8E3E", str(caught[0].message))
        self.assertEqual(caught[0].filename, __file__)

    def test_derive_theme_warns_once_at_the_caller(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            derive_theme(THEME.DEFAULT, lead=self.RED_GREEN)
        self.assertEqual(len(caught), 1)
        self.assertEqual(caught[0].filename, __file__)

    def test_weak_passing_and_ramp_palettes_stay_silent(self):
        self.assertEqual(score_palette(self.NEON, face="#000000").verdict, "weak")
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            config.register_theme("neon", {"color_general_multiple": self.NEON})
            # a sequential lead's samples are a ramp by design, never gated
            derive_theme(THEME.DEFAULT, lead=COLORS.Greens)
            derive_theme(THEME.INK, lead=list(DEFAULT_THEME["color_general_multiple"]))
            config.register_theme(
                "fine", {"color_general_multiple": ["#000000", "#FFFFFF"]}
            )


if __name__ == "__main__":
    unittest.main()
