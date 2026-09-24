import unittest
from dataclasses import FrozenInstanceError

import datachart.charts
from datachart.utils._internal.chart_kinds import (
    CHART_KINDS,
    ChartKind,
    DatasetPolicy,
    chart_kind,
    splits_datasets,
)
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
            chart_kind("linechart").subplots = False

    def test_front_without_row_fails_before_drawing(self):
        from datachart.utils._internal.plot_engine import render_chart

        with self.assertRaisesRegex(ValueError, "'piechart'"):
            render_chart("piechart", [{"data": [{"x": 1, "y": 1}]}], {})


class TestDatasetPolicy(unittest.TestCase):
    def test_policy_per_group_front_is_unchanged(self):
        expected = {
            "boxplot": DatasetPolicy.RAISE,
            "violinplot": DatasetPolicy.RAISE,
            "raincloudplot": DatasetPolicy.SUBPLOT,
            "ridgelineplot": DatasetPolicy.SUBPLOT,
            "swarmplot": DatasetPolicy.OVERLAY,
        }
        for name, policy in expected.items():
            with self.subTest(kind=name):
                self.assertIs(chart_kind(name).datasets, policy)

    def test_overlay_splits_only_when_asked(self):
        kind = chart_kind("swarmplot")
        self.assertFalse(splits_datasets(kind, 2, None))
        self.assertTrue(splits_datasets(kind, 2, True))

    def test_subplot_splits_unasked(self):
        self.assertTrue(splits_datasets(chart_kind("raincloudplot"), 2, None))

    def test_raise_has_one_message(self):
        messages = set()
        for name in ("boxplot", "violinplot"):
            kind = chart_kind(name)
            with self.assertRaises(ValueError) as caught:
                splits_datasets(kind, 2, None)
            messages.add(str(caught.exception).lower().replace(kind.label, "<front>"))
            self.assertTrue(splits_datasets(kind, 2, True))
            self.assertTrue(splits_datasets(kind, 1, None))
        self.assertEqual(len(messages), 1)

    def test_front_without_subplots_warns_and_overlays(self):
        with self.assertWarnsRegex(UserWarning, "does not support subplots"):
            self.assertFalse(splits_datasets(chart_kind("pyramidchart"), 2, True))


if __name__ == "__main__":
    unittest.main()
