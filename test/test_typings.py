"""Tests for the retired setting payload names (ADR 0043)."""

import unittest

import datachart.typings as typings

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

    def test_retired_chart_attrs_are_gone(self):
        leftovers = [
            name
            for name in vars(typings)
            if name.startswith("_") and name.endswith(("ChartAttrs", "PlotAttrs"))
        ]
        self.assertEqual(leftovers, [])

    def test_unknown_name_raises(self):
        with self.assertRaises(AttributeError):
            typings.NoSuchAttrs


if __name__ == "__main__":
    unittest.main()
