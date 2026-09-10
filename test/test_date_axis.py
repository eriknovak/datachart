"""Tests for the temporal x axis: detection, tick formatting, and composition."""

import json
import unittest
from datetime import date, datetime, timedelta, timezone

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

from datachart.constants import DATE_FORMAT, VALUE_FORMAT
from datachart.utils._internal.layers import NumpyEncoder, get_chart_hash
from datachart.utils.stats import maximum, minimum

DAYS = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(10)]
LINE_DAYS = [{"x": d, "y": i} for i, d in enumerate(DAYS)]


class TestEncoder(unittest.TestCase):
    def test_datetime_and_date_encode_to_iso(self):
        payload = {"a": datetime(2024, 1, 2, 3, 4), "b": date(2024, 1, 2)}
        self.assertEqual(
            json.loads(json.dumps(payload, cls=NumpyEncoder)),
            {"a": "2024-01-02T03:04:00", "b": "2024-01-02"},
        )

    def test_numpy_datetime64_encodes(self):
        payload = {"a": np.datetime64("2024-01-02")}
        self.assertEqual(
            json.loads(json.dumps(payload, cls=NumpyEncoder)), {"a": "2024-01-02"}
        )

    def test_chart_hash_is_stable_for_temporal_data(self):
        chart = {"data": LINE_DAYS}
        self.assertEqual(get_chart_hash(chart), get_chart_hash(dict(chart)))


class TestStatsPassThrough(unittest.TestCase):
    def test_numeric_input_still_returns_floats(self):
        self.assertEqual(minimum([3, 1, 2]), 1)
        self.assertIsInstance(minimum([3, 1, 2]), float)
        self.assertEqual(maximum(np.array([3.5, 1.0])), 3.5)

    def test_temporal_input_passes_through(self):
        self.assertEqual(minimum(DAYS), DAYS[0])
        self.assertEqual(maximum(DAYS), DAYS[-1])
        stamps = np.array(["2024-01-05", "2024-01-01"], dtype="datetime64[D]")
        self.assertEqual(minimum(stamps), np.datetime64("2024-01-01"))


class TestDateFormatConstant(unittest.TestCase):
    def test_members(self):
        self.assertEqual(DATE_FORMAT.AUTO, "auto")
        self.assertEqual(DATE_FORMAT.ISO, "%Y-%m-%d")
        self.assertEqual(DATE_FORMAT.YEAR, "%Y")
        self.assertEqual(DATE_FORMAT.YEAR_MONTH, "%Y-%m")
        self.assertEqual(DATE_FORMAT.MONTH_DAY, "%m-%d")
        self.assertEqual(DATE_FORMAT.DAY, "%d")
        self.assertEqual(DATE_FORMAT.TIME, "%H:%M")

    def test_added_in_admonition(self):
        self.assertIn('!!! info "Added in Unreleased"', DATE_FORMAT.__doc__)


if __name__ == "__main__":
    unittest.main()
