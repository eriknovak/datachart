"""Tests for the deprecated setting payload names (ADR 0043)."""

import unittest

import datachart.typings as typings

RENAMED = {
    "VLinePlotAttrs": "VLineSettingAttrs",
    "HLinePlotAttrs": "HLineSettingAttrs",
    "TextAttrs": "TextSettingAttrs",
    "HeatmapColorbarAttrs": "ColorbarSettingAttrs",
}


class TestDeprecatedSettingNames(unittest.TestCase):
    def test_old_names_resolve_with_a_warning(self):
        for old, new in RENAMED.items():
            with self.subTest(old=old):
                with self.assertWarns(DeprecationWarning) as cm:
                    resolved = getattr(typings, old)
                self.assertIs(resolved, getattr(typings, new))
                self.assertIn(new, str(cm.warning))

    def test_from_import_warns(self):
        with self.assertWarns(DeprecationWarning):
            from datachart.typings import VLinePlotAttrs  # noqa: F401

    def test_unreleased_span_names_are_gone(self):
        for old in ("VSpanPlotAttrs", "HSpanPlotAttrs"):
            with self.subTest(old=old):
                self.assertFalse(hasattr(typings, old))

    def test_unknown_name_raises(self):
        with self.assertRaises(AttributeError):
            typings.NoSuchAttrs


if __name__ == "__main__":
    unittest.main()
