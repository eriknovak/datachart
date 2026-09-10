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

from datachart.charts import (
    BarChart,
    BoxPlot,
    ContourChart,
    Heatmap,
    HexbinChart,
    LineChart,
    ParallelCoords,
    PyramidChart,
    ScatterChart,
    StackedAreaChart,
    SwarmPlot,
    ViolinPlot,
)
from datachart.constants import DATE_FORMAT, ORIENTATION, VALUE_FORMAT
from datachart.utils import Grid, Panel
from datachart.utils._internal.layers import NumpyEncoder, get_chart_hash
from datachart.utils.stats import maximum, minimum

DAYS = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(10)]
LINE_DAYS = [{"x": d, "y": i} for i, d in enumerate(DAYS)]
LINE_NUMS = [{"x": i, "y": i} for i in range(10)]
ISO_DAYS = [{"x": d.strftime("%Y-%m-%d"), "y": i} for i, d in enumerate(DAYS)]
MONTHS = [date(2024, m, 1) for m in (1, 2, 3, 4)]
BAR_MONTHS = [{"label": m, "y": v} for m, v in zip(MONTHS, [3, 5, 4, 6])]
GROUPS = [{"label": m, "value": v} for m in MONTHS for v in (1.0, 2.0, 3.5)]


class Stamp(datetime):
    """A datetime subclass, standing in for a pandas Timestamp."""


def date_locator(axis) -> bool:
    return isinstance(axis.get_major_locator(), mdates.AutoDateLocator)


def concise(axis) -> bool:
    return isinstance(axis.get_major_formatter(), mdates.ConciseDateFormatter)


def tick_labels(axis) -> list:
    axis.axes.figure.canvas.draw()
    return [t.get_text() for t in axis.get_ticklabels()]


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


class TestTemporalAxis(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_continuous_fronts_take_datetimes(self):
        figures = [
            LineChart(data=LINE_DAYS),
            StackedAreaChart(data=[LINE_DAYS, LINE_DAYS]),
            ScatterChart(data=LINE_DAYS),
        ]
        first, last = mdates.date2num([DAYS[0], DAYS[-1]])
        for fig in figures:
            ax = fig.axes[0]
            self.assertTrue(date_locator(ax.xaxis))
            self.assertTrue(concise(ax.xaxis))
            lo, hi = ax.get_xlim()
            self.assertLessEqual(lo, first)
            self.assertGreaterEqual(hi, last)
        # line and stacked area charts hug their data
        for fig in figures[:2]:
            self.assertEqual(fig.axes[0].get_xlim(), (first, last))

    def test_tick_spacing_follows_elapsed_time(self):
        gaps = [DAYS[0], DAYS[1], DAYS[9]]
        fig = LineChart(data=[{"x": d, "y": 1} for d in gaps])
        line = fig.axes[0].lines[0]
        x = line.get_xdata(orig=False)
        self.assertAlmostEqual((x[2] - x[1]) / (x[1] - x[0]), 8.0)

    def test_numpy_and_timestamp_like_inputs(self):
        stamps = np.array([d.date() for d in DAYS], dtype="datetime64[D]")
        as_numpy = [{"x": s, "y": i} for i, s in enumerate(stamps)]
        as_stamp = [
            {"x": Stamp(d.year, d.month, d.day), "y": i} for i, d in enumerate(DAYS)
        ]
        as_dict = {"x": stamps, "y": np.arange(len(stamps))}
        for data in (as_numpy, as_stamp, as_dict):
            ax = LineChart(data=data).axes[0]
            self.assertTrue(concise(ax.xaxis))
            self.assertAlmostEqual(ax.get_xlim()[0], mdates.date2num(DAYS[0]), places=6)

    def test_gridded_fronts_take_datetimes(self):
        z = np.arange(12.0).reshape(3, 4)
        contour = ContourChart(data={"x": DAYS[:4], "y": [1, 2, 3], "z": z})
        self.assertTrue(concise(contour.axes[0].xaxis))
        self.assertFalse(date_locator(contour.axes[0].yaxis))
        hexbin = HexbinChart(data={"x": DAYS, "y": list(range(10))})
        self.assertTrue(concise(hexbin.axes[0].xaxis))
        heat = Heatmap(data={"x": MONTHS, "y": ["a", "b"], "z": [[1, 2, 3, 4]] * 2})
        self.assertEqual(
            tick_labels(heat.axes[0].xaxis), [m.strftime("%Y-%m-%d") for m in MONTHS]
        )

    def test_iso_strings_stay_categorical(self):
        ax = LineChart(data=ISO_DAYS).axes[0]
        self.assertFalse(date_locator(ax.xaxis))
        self.assertEqual(tick_labels(ax.xaxis), [d["x"] for d in ISO_DAYS])
        # one category per string, in input order, on an integer index
        self.assertEqual(list(ax.get_xticks()), list(range(10)))

    def test_timezone_aware_passes_through(self):
        tz = timezone(timedelta(hours=2))
        aware = [{"x": d.replace(tzinfo=tz), "y": i} for i, d in enumerate(DAYS)]
        ax = LineChart(data=aware).axes[0]
        self.assertTrue(concise(ax.xaxis))
        self.assertEqual(ax.xaxis.get_units(), tz)
        self.assertAlmostEqual(
            ax.get_xlim()[0], mdates.date2num(DAYS[0].replace(tzinfo=tz)), places=6
        )

    def test_mixed_temporal_and_numeric_raises(self):
        with self.assertRaisesRegex(ValueError, "temporal"):
            LineChart(data=[LINE_DAYS, LINE_NUMS])
        with self.assertRaisesRegex(ValueError, "temporal"):
            Panel([LineChart(data=LINE_DAYS), ScatterChart(data=LINE_NUMS)])

    def test_horizontal_orientation_keeps_the_time_axis(self):
        ax = BarChart(data=BAR_MONTHS, orientation=ORIENTATION.HORIZONTAL).axes[0]
        self.assertEqual(tick_labels(ax.yaxis), [m.isoformat() for m in MONTHS])


class TestGroupLabels(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_group_fronts_format_date_labels(self):
        cases = [
            BarChart(data=BAR_MONTHS),
            BoxPlot(data=GROUPS),
            ViolinPlot(data=GROUPS),
            SwarmPlot(data=GROUPS),
        ]
        for fig in cases:
            ax = fig.axes[0]
            self.assertEqual(tick_labels(ax.xaxis), [m.isoformat() for m in MONTHS])
            self.assertFalse(date_locator(ax.xaxis))
            ticks = ax.get_xticks()
            self.assertEqual(list(ticks), sorted(ticks))
            self.assertLess(max(ticks), 10)

    def test_group_labels_take_a_date_format(self):
        ax = BarChart(data=BAR_MONTHS, xticks_format=DATE_FORMAT.YEAR_MONTH).axes[0]
        self.assertEqual(
            tick_labels(ax.xaxis), ["2024-01", "2024-02", "2024-03", "2024-04"]
        )
        ax = BoxPlot(
            data=GROUPS,
            orientation=ORIENTATION.HORIZONTAL,
            yticks_format=DATE_FORMAT.YEAR_MONTH,
        ).axes[0]
        self.assertEqual(
            tick_labels(ax.yaxis), ["2024-01", "2024-02", "2024-03", "2024-04"]
        )

    def test_datetime_labels_with_a_time_component(self):
        stamps = [datetime(2024, 1, 1, h) for h in (8, 12, 16)]
        ax = BarChart(data=[{"label": s, "y": 1} for s in stamps]).axes[0]
        self.assertEqual(
            tick_labels(ax.xaxis),
            ["2024-01-01 08:00", "2024-01-01 12:00", "2024-01-01 16:00"],
        )

    def test_pyramid_and_parallel_coords(self):
        left = [{"label": m, "y": v} for m, v in zip(MONTHS, [1, 2, 3, 4])]
        right = [{"label": m, "y": v} for m, v in zip(MONTHS, [2, 3, 4, 5])]
        ax = PyramidChart(data=[left, right]).axes[0]
        self.assertEqual(tick_labels(ax.yaxis), [m.isoformat() for m in MONTHS])
        rows = [{"when": m, "v": i} for i, m in enumerate(MONTHS)]
        fig = ParallelCoords(data=rows)
        texts = [t.get_text() for t in fig.axes[0].texts]
        for m in MONTHS:
            self.assertIn(m.isoformat(), texts)


class TestTicksFormat(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_date_format_on_a_temporal_axis(self):
        ax = LineChart(data=LINE_DAYS, xticks_format=DATE_FORMAT.MONTH_DAY).axes[0]
        fmt = ax.xaxis.get_major_formatter()
        self.assertIsInstance(fmt, mdates.DateFormatter)
        self.assertEqual(fmt(mdates.date2num(DAYS[0])), "01-01")

    def test_value_format_on_a_numeric_axis(self):
        ax = LineChart(data=LINE_DAYS, yticks_format=VALUE_FORMAT.PERCENT).axes[0]
        self.assertEqual(ax.yaxis.get_major_formatter()(0.5), "50.0%")
        ax = ScatterChart(data=LINE_NUMS, xticks_format="{x:.2f}").axes[0]
        self.assertEqual(ax.xaxis.get_major_formatter()(1), "1.00")
        ax = ScatterChart(data=LINE_NUMS, xticks_format="%.1f").axes[0]
        self.assertEqual(ax.xaxis.get_major_formatter()(1), "1.0")

    def test_auto_leaves_a_numeric_axis_alone(self):
        plain = LineChart(data=LINE_NUMS).axes[0]
        auto = LineChart(data=LINE_NUMS, xticks_format=DATE_FORMAT.AUTO).axes[0]
        self.assertEqual(
            type(plain.xaxis.get_major_formatter()),
            type(auto.xaxis.get_major_formatter()),
        )

    def test_bad_format_raises(self):
        with self.assertRaisesRegex(ValueError, "ticks_format"):
            LineChart(data=LINE_NUMS, xticks_format="%Y")


class TestExplicitPositions(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_ticks_limits_and_references_take_datetimes(self):
        ticks = [DAYS[0], DAYS[5], DAYS[9]]
        fig = LineChart(
            data=LINE_DAYS,
            xticks=ticks,
            xmin=DAYS[1],
            xmax=DAYS[8],
            vlines={"x": DAYS[4]},
            vspans={"xmin": DAYS[2], "xmax": DAYS[3]},
            hlines={"y": 3, "xmin": DAYS[2], "xmax": DAYS[6]},
        )
        ax = fig.axes[0]
        self.assertEqual(list(ax.get_xticks()), list(mdates.date2num(ticks)))
        self.assertEqual(
            tick_labels(ax.xaxis), ["2024-01-01", "2024-01-06", "2024-01-10"]
        )
        self.assertEqual(ax.get_xlim(), tuple(mdates.date2num([DAYS[1], DAYS[8]])))
        self.assertGreater(len(ax.collections), 0)
        self.assertGreater(len(ax.patches), 0)

    def test_explicit_ticks_take_a_date_format(self):
        ax = LineChart(
            data=LINE_DAYS, xticks=[DAYS[0], DAYS[9]], xticks_format=DATE_FORMAT.DAY
        ).axes[0]
        self.assertEqual(tick_labels(ax.xaxis), ["01", "10"])


class TestComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_keeps_the_axis_kind(self):
        fig = Panel(
            [
                LineChart(data=LINE_DAYS, xticks_format=DATE_FORMAT.MONTH_DAY),
                ScatterChart(data=LINE_DAYS),
            ]
        )
        ax = fig.axes[0]
        self.assertTrue(date_locator(ax.xaxis))
        self.assertIsInstance(ax.xaxis.get_major_formatter(), mdates.DateFormatter)
        self.assertEqual(
            ax.xaxis.get_major_formatter()(mdates.date2num(DAYS[0])), "01-01"
        )

    def test_grid_keeps_the_axis_kind(self):
        fig = Grid([LineChart(data=LINE_DAYS), BarChart(data=BAR_MONTHS)])
        line_ax, bar_ax = fig.axes[:2]
        self.assertTrue(concise(line_ax.xaxis))
        self.assertEqual(tick_labels(bar_ax.xaxis), [m.isoformat() for m in MONTHS])

    def test_subplots_keep_the_axis_kind(self):
        fig = LineChart(data=[LINE_DAYS, LINE_DAYS], subplots=True)
        for ax in fig.axes:
            self.assertTrue(concise(ax.xaxis))


if __name__ == "__main__":
    unittest.main()
