"""Tests for the typing names (ADRs 0043, 0072)."""

import unittest
import warnings

import datachart.typings as typings
from datachart.themes._base import BASE_THEME

ROLE_SUFFIXES = ("RecordAttrs", "DataAttrs", "StyleAttrs", "SettingAttrs")
SINGLE_CHARTS = {
    "SankeySingleChartAttrs",
    "TreemapSingleChartAttrs",
    "NetworkSingleChartAttrs",
}

RETIRED = (
    "VLinePlotAttrs",
    "HLinePlotAttrs",
    "VSpanPlotAttrs",
    "HSpanPlotAttrs",
    "TextAttrs",
    "HeatmapColorbarAttrs",
    "ChartCommonAttrs",
)


class TestRetiredSettingNames(unittest.TestCase):
    def test_retired_names_are_gone(self):
        for old in RETIRED:
            with self.subTest(old=old):
                self.assertFalse(hasattr(typings, old))

    def test_private_chart_attrs_only_back_an_alias(self):
        backing = {
            f"_{old}" for old, new in typings._DEPRECATED_ALIASES.items() if new is None
        }
        leftovers = [
            name
            for name in vars(typings)
            if name.startswith("_")
            and name.endswith(("ChartAttrs", "PlotAttrs"))
            and name not in backing
        ]
        self.assertEqual(leftovers, [])

    def test_unknown_name_raises(self):
        with self.assertRaises(AttributeError):
            typings.NoSuchAttrs


class TestTypingRoles(unittest.TestCase):
    def test_public_names_carry_a_role_suffix(self):
        # the brief leaves these two outside the rule (ADR 0072)
        exempt = SINGLE_CHARTS | {"ThemeDefaultAttrs", "EmphasisRuleAttrs"}
        stray = [
            name
            for name in dir(typings)
            if name.endswith("Attrs")
            and not name.startswith("_")
            and not name.endswith(ROLE_SUFFIXES)
            and name not in exempt
        ]
        self.assertEqual(stray, [])

    def test_single_chart_types_are_the_reachable_three(self):
        public = {
            name
            for name in dir(typings)
            if name.endswith("SingleChartAttrs") and not name.startswith("_")
        }
        self.assertEqual(public, SINGLE_CHARTS)

    def test_renamed_record_type_warns_and_resolves(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            resolved = typings.LineDataPointAttrs
        self.assertIs(resolved, typings.LineRecordAttrs)
        self.assertEqual(len(caught), 1)
        self.assertIs(caught[0].category, DeprecationWarning)
        self.assertIn("LineRecordAttrs", str(caught[0].message))

    def test_removed_single_chart_type_warns_and_resolves(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            resolved = typings.LineSingleChartAttrs
        self.assertIs(resolved, typings._LineSingleChartAttrs)
        self.assertEqual(len(caught), 1)
        self.assertIn("no replacement", str(caught[0].message))

    def test_every_alias_resolves(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for old in typings._DEPRECATED_ALIASES:
                with self.subTest(old=old):
                    self.assertTrue(hasattr(typings, old))


class TestThemeConformance(unittest.TestCase):
    """Every theme key is declared by exactly one style group, and back."""

    def declared(self) -> dict:
        # a TypedDict's annotations include inherited keys; the union's
        # direct bases each declare only their own
        keys = {}
        for group in typings.StyleAttrs.__orig_bases__:
            for key in group.__annotations__:
                keys.setdefault(key, []).append(group.__name__)
        return keys

    def test_every_key_is_declared_once(self):
        twice = {
            key: groups for key, groups in self.declared().items() if len(groups) > 1
        }
        self.assertEqual(twice, {})

    def test_theme_keys_match_declared_keys(self):
        declared = set(self.declared())
        self.assertEqual(sorted(set(BASE_THEME) - declared), [])
        self.assertEqual(sorted(declared - set(BASE_THEME)), [])

    def test_overlay_group_is_in_the_union(self):
        self.assertIn(typings.OverlayStyleAttrs, typings.StyleAttrs.__orig_bases__)
        self.assertEqual(len(typings.OverlayStyleAttrs.__annotations__), 11)

    def test_subtitle_font_accepts_str(self):
        hints = typings.FontStyleAttrs.__annotations__
        for key in ("font_subtitle_style", "font_subtitle_weight"):
            with self.subTest(key=key):
                self.assertIn(str, hints[key].__args__)


if __name__ == "__main__":
    unittest.main()
