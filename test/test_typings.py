"""Tests for the deprecated chart-attrs typings (ADR 0003)."""

import warnings

import pytest

DEPRECATED_NAMES = [
    "ChartAttrs",
    "LineChartAttrs",
    "BarChartAttrs",
    "HistogramChartAttrs",
    "HeatmapChartAttrs",
    "ScatterChartAttrs",
    "BoxChartAttrs",
    "ParallelCoordsChartAttrs",
]


class TestDeprecatedChartAttrs:
    """The retired chart-attrs typings warn but still resolve."""

    @pytest.mark.parametrize("name", DEPRECATED_NAMES)
    def test_access_warns_and_returns_type(self, name):
        import datachart.typings as typings

        with pytest.warns(DeprecationWarning, match="datachart.charts"):
            attr = getattr(typings, name)
        assert attr is not None

    def test_single_chart_attrs_stay_public(self):
        import datachart.typings as typings

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            assert typings.LineSingleChartAttrs is not None
            assert typings.BarSingleChartAttrs is not None

    def test_unknown_name_raises_attribute_error(self):
        import datachart.typings as typings

        with pytest.raises(AttributeError):
            typings.DoesNotExist
