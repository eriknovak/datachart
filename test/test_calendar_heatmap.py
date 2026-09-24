"""Tests for the calendar heatmap: validation, year panels, cell layout, composition."""

import unittest
from datetime import date, datetime, timedelta

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

from datachart.charts import CalendarHeatmap, LineChart
from datachart.config import config
from datachart.constants import (
    COLORBAR_LOCATION,
    COLOR_NORM,
    THEME,
    VALUE_FORMAT,
    CALENDAR_WEEKDAY,
)
from datachart.themes import _base
from datachart.utils import Grid, Panel
from datachart.utils._internal.layers import DrawContext
from datachart.utils._internal.validate import (
    validate_calendar_dates,
    validate_calendar_year,
    validate_unique_dates,
)

THEMES = [
    THEME.DEFAULT,
    THEME.GREYSCALE,
    THEME.INK,
    THEME.HATCH,
    THEME.MINIMAL,
    THEME.MATERIAL,
    THEME.SKETCH,
]
CALENDAR_KEYS = tuple(
    key for key in _base.BASE_THEME if key.startswith("plot_calendar_heatmap_")
)


def days(start, n):
    return [start + timedelta(days=i) for i in range(n)]


def calendar(start, n, **kwargs):
    """A calendar of `n` days from `start`, valued 1..n."""
    dates = days(start, n)
    return CalendarHeatmap({"date": dates, "value": list(range(1, n + 1))}, **kwargs)


def year_calendar(year, **kwargs):
    """A full year valued by the day of the year."""
    n = (date(year + 1, 1, 1) - date(year, 1, 1)).days
    return calendar(date(year, 1, 1), n, **kwargs)


def _image(ax):
    (image,) = ax.images
    return np.ma.filled(np.asarray(image.get_array(), dtype=float), np.nan)


def _tick_labels(ax, axis):
    ax.figure.canvas.draw()
    return [t.get_text() for t in getattr(ax, f"get_{axis}ticklabels")()]


def _all_axes(figure):
    """The figure's axes and the colorbar axes a locked aspect parents to them."""
    return list(figure.axes) + [c for ax in figure.axes for c in ax.child_axes]


def _month_lines(ax):
    return [
        c
        for c in ax.collections
        if isinstance(c, LineCollection) and c.get_gid() == "month-separators"
    ]


class TestWeekdayConstant(unittest.TestCase):
    def test_members(self):
        self.assertEqual(CALENDAR_WEEKDAY.MONDAY, "monday")
        self.assertEqual(CALENDAR_WEEKDAY.SUNDAY, "sunday")


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


class TestCalendarFront(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_exported_under_trends(self):
        import datachart.charts as charts

        self.assertIn("CalendarHeatmap", charts.__all__)

    def test_bad_data_shape_raises(self):
        with self.assertRaises(ValueError) as cm:
            CalendarHeatmap([date(2024, 1, 1)])
        self.assertIn("a dict with `date` and `value`", str(cm.exception))
        with self.assertRaises(ValueError):
            CalendarHeatmap({"date": [date(2024, 1, 1)]})

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError) as cm:
            CalendarHeatmap({"date": days(date(2024, 1, 1), 3), "value": [1, 2]})
        self.assertIn("one value per date", str(cm.exception))

    def test_empty_data_raises(self):
        with self.assertRaises(ValueError):
            CalendarHeatmap({"date": [], "value": []})

    def test_string_date_raises_at_the_front(self):
        with self.assertRaises(ValueError) as cm:
            CalendarHeatmap({"date": ["2024-01-01"], "value": [1]})
        self.assertIn("datetime64", str(cm.exception))

    def test_duplicate_date_raises_at_the_front(self):
        dates = [date(2024, 3, 5), date(2024, 3, 6), date(2024, 3, 5)]
        with self.assertRaises(ValueError) as cm:
            CalendarHeatmap({"date": dates, "value": [1, 2, 3]})
        self.assertIn("2024-03-05", str(cm.exception))

    def test_emphasis_raises(self):
        with self.assertRaises(ValueError):
            calendar(date(2024, 1, 1), 5, emphasis="highlight")

    def test_invalid_week_start_raises(self):
        with self.assertRaises(ValueError):
            calendar(date(2024, 1, 1), 5, week_start="tuesday")

    def test_single_year_draws_one_axes_with_a_seven_row_grid(self):
        figure = year_calendar(2024)
        self.assertEqual(len(figure.axes), 1)
        # 2024 starts on a Monday and has 366 days: 53 week columns
        self.assertEqual(_image(figure.axes[0]).shape, (7, 53))
        self.assertEqual(figure._chart_metadata["type"], "calendarheatmap")

    def test_drawn_range_spans_the_months_with_data(self):
        figure = calendar(date(2024, 10, 15), 20)
        ax = figure.axes[0]
        # 20 days from mid-October reach November: nine weeks from Tue Oct 1
        z = _image(ax)
        self.assertEqual(z.shape, (7, 9))
        self.assertEqual(_tick_labels(ax, "x"), ["Oct", "Nov"])
        (lines,) = _month_lines(ax)
        self.assertEqual(len(lines.get_paths()), 1)
        self.assertTrue(np.isnan(z[0, 0]))  # Mon Sep 30: off the range
        self.assertEqual(z[1, 2], 1)  # Tue Oct 15
        self.assertTrue(np.isnan(z[1, 0]))  # Tue Oct 1: missing

    def test_monday_start_places_each_date(self):
        figure = calendar(date(2024, 1, 1), 10)
        z = _image(figure.axes[0])
        self.assertEqual(z[0, 0], 1)  # Mon Jan 1
        self.assertEqual(z[6, 0], 7)  # Sun Jan 7
        self.assertEqual(z[0, 1], 8)  # Mon Jan 8
        self.assertEqual(z[2, 1], 10)  # Wed Jan 10

    def test_sunday_start_places_each_date(self):
        figure = calendar(date(2024, 1, 1), 10, week_start=CALENDAR_WEEKDAY.SUNDAY)
        z = _image(figure.axes[0])
        self.assertTrue(np.isnan(z[0, 0]))  # Sun Dec 31 2023: outside the year
        self.assertEqual(z[1, 0], 1)  # Mon Jan 1
        self.assertEqual(z[0, 1], 7)  # Sun Jan 7
        self.assertEqual(z[6, 0], 6)  # Sat Jan 6
        self.assertEqual(
            _image(
                year_calendar(2024, week_start=CALENDAR_WEEKDAY.SUNDAY).axes[0]
            ).shape,
            (7, 53),
        )

    def test_theme_week_start_is_the_default(self):
        config.update_config(
            {"plot_calendar_heatmap_week_start": CALENDAR_WEEKDAY.SUNDAY}
        )
        figure = calendar(date(2024, 1, 1), 3)
        self.assertEqual(_image(figure.axes[0])[1, 0], 1)
        self.assertEqual(_tick_labels(figure.axes[0], "y")[0], "Sun")

    def test_missing_days_and_none_values_are_blank(self):
        dates = [date(2023, 1, 1), date(2023, 1, 3)]
        figure = CalendarHeatmap({"date": dates, "value": [5, None]})
        z = _image(figure.axes[0])
        # 2023 starts on a Sunday: the six cells above it are outside the year
        self.assertTrue(np.isnan(z[:6, 0]).all())
        self.assertEqual(z[6, 0], 5)
        self.assertTrue(np.isnan(z[0, 1]))  # Mon Jan 2: missing
        self.assertTrue(np.isnan(z[1, 1]))  # Tue Jan 3: None
        self.assertEqual(np.count_nonzero(~np.isnan(z)), 1)

    def test_month_and_weekday_labels(self):
        figure = year_calendar(2024)
        ax = figure.axes[0]
        self.assertEqual(
            _tick_labels(ax, "x"),
            [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
        )
        self.assertEqual(_tick_labels(ax, "y"), ["Mon", "Wed", "Fri", "Sun"])
        self.assertEqual(list(ax.get_yticks()), [0, 2, 4, 6])
        sunday = calendar(date(2024, 1, 1), 3, week_start=CALENDAR_WEEKDAY.SUNDAY)
        self.assertEqual(
            _tick_labels(sunday.axes[0], "y"), ["Sun", "Tue", "Thu", "Sat"]
        )

    def test_label_toggles(self):
        figure = calendar(
            date(2024, 1, 1), 3, show_month_labels=False, show_weekday_labels=False
        )
        ax = figure.axes[0]
        self.assertEqual(_tick_labels(ax, "x"), [])
        self.assertEqual(_tick_labels(ax, "y"), [])
        self.assertFalse(any(spine.get_visible() for spine in ax.spines.values()))

    def test_month_separators_sit_between_months(self):
        figure = year_calendar(2024)
        (lines,) = _month_lines(figure.axes[0])
        self.assertEqual(len(lines.get_paths()), 11)
        # a zero width draws none
        bare = calendar(
            date(2024, 1, 1), 3, style={"plot_calendar_heatmap_month_line_width": 0}
        )
        self.assertEqual(_month_lines(bare.axes[0]), [])

    def test_values_print_only_on_dated_cells(self):
        figure = calendar(date(2024, 1, 1), 4, show_values=True)
        texts = [t.get_text() for t in figure.axes[0].texts]
        self.assertEqual(texts, ["1", "2", "3", "4"])
        fmt = calendar(
            date(2024, 1, 1), 2, show_values=True, value_format=VALUE_FORMAT.DECIMAL
        )
        self.assertEqual([t.get_text() for t in fmt.axes[0].texts], ["1.0", "2.0"])

    def test_theme_value_default_applies(self):
        config.update_config({"chart_default_show_values": True})
        figure = calendar(date(2024, 1, 1), 2)
        self.assertEqual(len(figure.axes[0].texts), 2)

    def test_colorbar_matches_heatmap(self):
        figure = calendar(
            date(2024, 1, 1),
            5,
            show_colorbars=True,
            colorbar={"label": "Steps", "location": COLORBAR_LOCATION.BOTTOM},
        )
        bars = [ax for ax in _all_axes(figure) if ax.get_xlabel() == "Steps"]
        self.assertEqual(len(bars), 1)
        self.assertEqual(len(_all_axes(calendar(date(2024, 1, 1), 5))), 1)

    def test_norm_and_range_apply(self):
        figure = calendar(date(2024, 1, 1), 5, vmin=0, vmax=10, norm="log")
        (image,) = figure.axes[0].images
        self.assertEqual((image.norm.vmin, image.norm.vmax), (0, 10))
        self.assertEqual(type(image.norm).__name__, "LogNorm")

    def test_cmap_derives_from_the_heatmap_colormap(self):
        config.set_theme(THEME.INK)
        figure = calendar(date(2024, 1, 1), 5)
        (image,) = figure.axes[0].images
        self.assertIn("YlGnBu", image.get_cmap().name)
        own = calendar(
            date(2024, 1, 1), 5, style={"plot_calendar_heatmap_cmap": "Greys"}
        )
        self.assertIn("Greys", own.axes[0].images[0].get_cmap().name)

    def test_every_theme_carries_the_calendar_keys(self):
        self.assertIn("plot_calendar_heatmap_week_start", CALENDAR_KEYS)
        for theme in THEMES:
            config.set_theme(theme)
            for key in CALENDAR_KEYS:
                self.assertIn(key, config.config, f"{theme}: {key}")
            figure = calendar(date(2024, 1, 1), 40, show_values=True)
            self.assertEqual(len(figure.axes[0].images), 1)
            plt.close(figure)

    def test_hover_reports_the_date(self):
        figure = calendar(date(2024, 1, 1), 3, subtitle="steps")
        panel = figure._chart_metadata["panel"]
        (layer,) = panel.layers
        fig, ax = plt.subplots()
        layer.draw(ax, DrawContext())
        ((image, resolver),) = layer.take_hover_targets()
        self.assertEqual(
            resolver((1, 0)), {"label": "steps", "date": "2024-01-02", "value": 2}
        )
        self.assertEqual(
            resolver((6, 4)), {"label": "steps", "date": None, "value": None}
        )


class TestYearPanels(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_multi_year_draws_one_panel_per_year_in_order(self):
        dates = days(date(2024, 12, 30), 5) + days(date(2022, 6, 1), 3)
        figure = CalendarHeatmap({"date": dates, "value": list(range(8))})
        self.assertEqual(len(figure.axes), 3)
        self.assertEqual(
            [ax.get_title() for ax in figure.axes], ["2022", "2024", "2025"]
        )
        self.assertEqual(figure._chart_metadata["shape"], (3, 1))
        self.assertEqual(_tick_labels(figure.axes[1], "x"), ["Dec"])
        self.assertEqual(_image(figure.axes[2])[2, 0], 2)  # Wed Jan 1 2025

    def test_subtitle_prefixes_the_year(self):
        dates = days(date(2023, 12, 31), 2)
        figure = CalendarHeatmap({"date": dates, "value": [1, 2]}, subtitle="steps")
        self.assertEqual(
            [ax.get_title() for ax in figure.axes], ["steps 2023", "steps 2024"]
        )
        single = calendar(date(2024, 1, 1), 2, subtitle="steps")
        self.assertEqual(single.axes[0].get_title(), "")

    def test_years_share_one_value_range(self):
        dates = days(date(2023, 12, 31), 2)
        figure = CalendarHeatmap({"date": dates, "value": [1, 9]})
        norms = [ax.images[0].norm for ax in figure.axes]
        self.assertEqual([(n.vmin, n.vmax) for n in norms], [(1, 9), (1, 9)])
        pinned = CalendarHeatmap({"date": dates, "value": [1, 9]}, vmin=0, vmax=10)
        norms = [ax.images[0].norm for ax in pinned.axes]
        self.assertEqual([(n.vmin, n.vmax) for n in norms], [(0, 10), (0, 10)])

    def test_log_norm_shares_the_positive_range(self):
        dates = days(date(2023, 12, 30), 6)
        figure = CalendarHeatmap(
            {"date": dates, "value": [0, 1, 0, 5, 2, 0]}, norm="log"
        )
        figure.canvas.draw()
        norms = [ax.images[0].norm for ax in figure.axes]
        self.assertEqual([(n.vmin, n.vmax) for n in norms], [(1, 5), (1, 5)])

    def test_month_line_is_black_in_every_theme(self):
        for theme in THEMES:
            config.set_theme(theme)
            (lines,) = _month_lines(year_calendar(2024).axes[0])
            self.assertEqual(
                lines.get_edgecolor()[0].tolist(), [0.0, 0.0, 0.0, 1.0], theme
            )
            self.assertEqual(list(lines.get_linewidths()), [1.0], theme)

    def test_month_line_color_none_follows_the_theme_frame(self):
        config.set_theme(THEME.INK)
        config.update_config({"plot_calendar_heatmap_month_line_color": None})
        (lines,) = _month_lines(year_calendar(2024).axes[0])
        self.assertEqual(
            lines.get_edgecolor()[0].tolist(),
            list(matplotlib.colors.to_rgba(config["plot_heatmap_frame_color"])),
        )

    def test_year_filter_keeps_one_panel(self):
        dates = days(date(2023, 12, 30), 4)
        figure = CalendarHeatmap({"date": dates, "value": [1, 2, 3, 4]}, year=2024)
        self.assertEqual(len(figure.axes), 1)
        z = _image(figure.axes[0])
        self.assertEqual(z[0, 0], 3)  # Mon Jan 1 2024
        self.assertEqual(np.count_nonzero(~np.isnan(z)), 2)
        self.assertNotIn("panels", figure._chart_metadata)

    def test_missing_year_raises(self):
        with self.assertRaises(ValueError) as cm:
            calendar(date(2024, 1, 1), 3, year=2020)
        self.assertIn("2020", str(cm.exception))

    def test_datasets_each_split_into_their_years(self):
        one = {"date": days(date(2023, 12, 31), 2), "value": [1, 2]}
        two = {"date": days(date(2024, 5, 1), 2), "value": [3, 4]}
        figure = CalendarHeatmap([one, two], subtitle=["a", "b"], max_cols=3)
        self.assertEqual(
            [ax.get_title() for ax in figure.axes], ["a 2023", "a 2024", "b"]
        )
        self.assertEqual(figure._chart_metadata["shape"], (1, 3))

    def test_default_figure_is_wide_and_grows_per_calendar(self):
        single = calendar(date(2024, 1, 1), 2)
        double = CalendarHeatmap({"date": days(date(2023, 12, 31), 2), "value": [1, 2]})
        w1, h1 = single.get_size_inches()
        w2, h2 = double.get_size_inches()
        self.assertEqual(w1, w2)
        self.assertGreater(w1, h1)
        self.assertGreater(h2, h1)


class TestComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_rejects(self):
        line = LineChart([{"x": 0, "y": 1}, {"x": 1, "y": 2}])
        with self.assertRaisesRegex(ValueError, "Grid"):
            Panel([calendar(date(2024, 1, 1), 3), line])

    def test_grid_accepts_single_and_multi_year(self):
        line = LineChart([{"x": 0, "y": 1}, {"x": 1, "y": 2}])
        single = calendar(date(2024, 1, 1), 3, title="one")
        multi = CalendarHeatmap({"date": days(date(2023, 12, 31), 2), "value": [1, 2]})
        grid = Grid([[single, line], [multi]])
        self.assertEqual(len(grid.axes), 4)
        self.assertEqual(_image(grid.axes[0])[0, 0], 1)
        self.assertEqual(grid.axes[0].get_title(), "one")
        self.assertEqual(len(_month_lines(grid.axes[0])), 1)
        titles = sorted(ax.get_title() for ax in grid.axes[2:])
        self.assertEqual(titles, ["2023", "2024"])
        self.assertFalse(any(s.get_visible() for s in grid.axes[0].spines.values()))


class TestCalendarCenteredNorm(unittest.TestCase):
    """A centred norm on the calendar takes the derived diverging map (ADR 0056)."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def _anomaly(self, **kwargs):
        dates = days(date(2024, 1, 1), 60)
        values = [(i % 7) - 3 for i in range(60)]
        return CalendarHeatmap({"date": dates, "value": values}, **kwargs)

    def test_centered_norm_builds_a_centered_norm(self):
        image = self._anomaly(norm=COLOR_NORM.CENTERED).axes[0].images[0]
        self.assertIsInstance(image.norm, matplotlib.colors.CenteredNorm)

    def test_vcenter_moves_the_centre(self):
        image = self._anomaly(norm=COLOR_NORM.CENTERED, vcenter=-1).axes[0].images[0]
        self.assertEqual(image.norm.vcenter, -1)

    def test_diverging_colormap_derives_from_the_heatmap_key(self):
        image = self._anomaly(norm=COLOR_NORM.CENTERED).axes[0].images[0]
        self.assertEqual(image.cmap.name, config["plot_heatmap_cmap_diverging"])

    def test_calendar_diverging_style_wins_over_the_heatmap_one(self):
        image = (
            self._anomaly(
                norm=COLOR_NORM.CENTERED,
                style={"plot_calendar_heatmap_cmap_diverging": "Spectral"},
            )
            .axes[0]
            .images[0]
        )
        self.assertEqual(image.cmap.name, "Spectral")

    def test_years_share_one_half_range(self):
        dates = days(date(2023, 12, 1), 70)
        values = [i - 35 for i in range(70)]
        figure = CalendarHeatmap(
            {"date": dates, "value": values}, norm=COLOR_NORM.CENTERED
        )
        halfranges = {ax.images[0].norm.halfrange for ax in figure.axes if ax.images}
        self.assertEqual(len(halfranges), 1)


if __name__ == "__main__":
    unittest.main()
