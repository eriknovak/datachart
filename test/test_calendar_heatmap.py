"""Tests for the calendar heatmap: validation, year panels, cell layout, composition."""

import unittest
from datetime import date, datetime, timedelta

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from datachart.constants import WEEKDAY
from datachart.utils._internal.validate import (
    validate_calendar_dates,
    validate_calendar_year,
    validate_unique_dates,
)


def days(start, n):
    return [start + timedelta(days=i) for i in range(n)]


class TestWeekdayConstant(unittest.TestCase):
    def test_members(self):
        self.assertEqual(WEEKDAY.MONDAY, "monday")
        self.assertEqual(WEEKDAY.SUNDAY, "sunday")


class TestCalendarValidators(unittest.TestCase):
    def test_temporal_objects_normalize_to_dates(self):
        dates = validate_calendar_dates(
            [
                date(2024, 1, 1),
                datetime(2024, 1, 2, 13, 30),
                np.datetime64("2024-01-03"),
                np.datetime64("2024-01-04T08:00"),
            ]
        )
        self.assertEqual(dates, [date(2024, 1, d) for d in range(1, 5)])

    def test_string_date_raises_naming_the_types(self):
        with self.assertRaises(ValueError) as cm:
            validate_calendar_dates([date(2024, 1, 1), "2024-01-02"])
        message = str(cm.exception)
        self.assertIn("'2024-01-02'", message)
        for name in ("date", "datetime", "datetime64", "Timestamp"):
            self.assertIn(name, message)

    def test_number_raises(self):
        with self.assertRaises(ValueError):
            validate_calendar_dates([20240101])

    def test_duplicate_raises_naming_the_first_duplicate(self):
        dates = [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 2), date(2024, 1, 1)]
        with self.assertRaises(ValueError) as cm:
            validate_unique_dates(dates)
        self.assertIn("2024-01-02", str(cm.exception))
        self.assertNotIn("2024-01-01", str(cm.exception))

    def test_unique_dates_pass(self):
        validate_unique_dates(days(date(2024, 1, 1), 10))

    def test_year_filter_accepts_a_present_year_or_none(self):
        validate_calendar_year(None, {2023, 2024})
        validate_calendar_year(2024, {2023, 2024})

    def test_missing_year_raises_naming_the_span(self):
        with self.assertRaises(ValueError) as cm:
            validate_calendar_year(2022, {2023, 2024})
        self.assertIn("2022", str(cm.exception))
        self.assertIn("2023", str(cm.exception))
        self.assertIn("2024", str(cm.exception))

    def test_non_integer_year_raises(self):
        with self.assertRaises(ValueError):
            validate_calendar_year("2024", {2024})
        with self.assertRaises(ValueError):
            validate_calendar_year(True, {2024})


class TestTypings(unittest.TestCase):
    def test_calendar_typings_exist(self):
        from datachart import typings

        self.assertIn("date", typings.CalendarHeatmapDataAttrs.__annotations__)
        self.assertIn("value", typings.CalendarHeatmapDataAttrs.__annotations__)
        self.assertIn("data", typings.CalendarHeatmapSingleChartAttrs.__annotations__)
        keys = typings.CalendarHeatmapStyleAttrs.__annotations__
        self.assertTrue(all(k.startswith("plot_calendar_heatmap_") for k in keys))
        self.assertIn("plot_calendar_heatmap_week_start", keys)
        self.assertIn(
            "plot_calendar_heatmap_week_start", typings.StyleAttrs.__annotations__
        )


if __name__ == "__main__":
    unittest.main()
