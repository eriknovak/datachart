"""Tests for the typing names (ADRs 0043, 0072)."""

import ast
import inspect
import unittest
from typing import List, Union

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
    "LineDataPointAttrs",
    "LineSingleChartAttrs",
)


class TestRetiredSettingNames(unittest.TestCase):
    def test_retired_names_are_gone(self):
        for old in RETIRED:
            with self.subTest(old=old):
                self.assertFalse(hasattr(typings, old))

    def test_no_private_chart_attrs_remain(self):
        leftovers = [
            name
            for name in vars(typings)
            if name.startswith("_") and name.endswith(("ChartAttrs", "PlotAttrs"))
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


class TestRecordTypings(unittest.TestCase):
    def test_stacked_area_and_bump_records_carry_no_yerr(self):
        for record in ("StackedAreaRecordAttrs", "BumpRecordAttrs"):
            with self.subTest(record=record):
                attrs = getattr(typings, record)
                self.assertEqual(set(attrs.__annotations__), {"x", "y"})


class TestThemeConformance(unittest.TestCase):
    """Every theme key is declared by exactly one style group, and back."""

    @staticmethod
    def classes() -> dict:
        """Each class in the typings source: its base names and own keys."""

        # read from source: before Python 3.12 a TypedDict keeps neither its
        # bases nor its own annotations apart from inherited ones
        tree = ast.parse(inspect.getsource(typings))
        return {
            node.name: (
                [base.id for base in node.bases if isinstance(base, ast.Name)],
                [
                    item.target.id
                    for item in node.body
                    if isinstance(item, ast.AnnAssign)
                ],
            )
            for node in tree.body
            if isinstance(node, ast.ClassDef)
        }

    def declared(self) -> dict:
        classes = self.classes()
        keys = {}
        for group in classes["StyleAttrs"][0]:
            for key in classes[group][1]:
                keys.setdefault(key, []).append(group)
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
        self.assertIn("OverlayStyleAttrs", self.classes()["StyleAttrs"][0])
        self.assertEqual(len(typings.OverlayStyleAttrs.__annotations__), 11)

    def test_linestyle_cycle_accepts_a_dash_pattern(self):
        hint = typings.ThemeDefaultAttrs.__annotations__["plot_linestyle_cycle"]
        entry = hint.__args__[0].__args__[0]
        self.assertIn(List[Union[float, List[float]]], entry.__args__)

    def test_subtitle_font_accepts_str(self):
        hints = typings.FontStyleAttrs.__annotations__
        for key in ("font_subtitle_style", "font_subtitle_weight"):
            with self.subTest(key=key):
                self.assertIn(str, hints[key].__args__)


if __name__ == "__main__":
    unittest.main()
