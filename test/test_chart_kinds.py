import unittest
from dataclasses import FrozenInstanceError

import datachart.charts
from datachart.utils._internal.chart_kinds import CHART_KINDS, ChartKind, chart_kind
from datachart.utils._internal.layers import Layer


class TestChartKinds(unittest.TestCase):
    def test_every_front_has_a_row(self):
        for front in datachart.charts.__all__:
            with self.subTest(front=front):
                kind = chart_kind(front.lower())
                self.assertIsInstance(kind, ChartKind)
                self.assertEqual(kind.name, front.lower())

    def test_every_row_names_a_layer_class(self):
        for name, kind in CHART_KINDS.items():
            with self.subTest(kind=name):
                self.assertTrue(issubclass(kind.layer, Layer))

    def test_unknown_name_raises_naming_it(self):
        with self.assertRaisesRegex(ValueError, "'piechart'"):
            chart_kind("piechart")

    def test_rows_are_frozen(self):
        with self.assertRaises(FrozenInstanceError):
            chart_kind("linechart").multiplot = False

    def test_front_without_row_fails_before_drawing(self):
        from datachart.utils._internal.plot_engine import render_chart

        with self.assertRaisesRegex(ValueError, "'piechart'"):
            render_chart("piechart", [{"data": [{"x": 1, "y": 1}]}], {})


if __name__ == "__main__":
    unittest.main()
