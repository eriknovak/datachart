"""Tests for the gantt chart: validation, row order, marks, axes, composition."""

import unittest
from datetime import date, datetime, timedelta

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import to_hex
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

from datachart.charts import BarChart, GanttChart, LineChart
from datachart.config import config
from datachart.constants import (
    DATE_FORMAT,
    DATE_PERIOD,
    GANTT_ARROW_ENTRY,
    EMPHASIS,
    GANTT_SORT_KEY,
    GANTT_VALUE,
    SORT,
    THEME,
)
from datachart.themes import _base
from datachart.utils import Grid, Panel
from datachart.utils._internal.layers import GanttLayer, Layer, ScheduleTicks

D0 = date(2024, 1, 1)
THEMES = [
    THEME.DEFAULT,
    THEME.GREYSCALE,
    THEME.INK,
    THEME.HATCH,
    THEME.MINIMAL,
    THEME.MATERIAL,
    THEME.SKETCH,
    THEME.QUILL,
]


def task(name, start, days, **extra):
    """A task starting `start` days after D0 and lasting `days` days."""
    begin = D0 + timedelta(days=start)
    return {"task": name, "start": begin, "end": begin + timedelta(days=days), **extra}


def schedule():
    return [
        task("Design", 0, 10, group="Plan", progress=1.0),
        task("Build", 8, 30, group="Make", progress=0.5, depends_on=["Design"]),
        task("Docs", 5, 12, group="Plan"),
        task("Test", 35, 14, group="Make", depends_on=["Build"]),
    ]


def row_labels(ax):
    return [t.get_text() for t in ax.get_yticklabels()]


def task_bars(ax, n):
    """The first `n` bar patches: the task bars, drawn before the progress bars."""
    return [p for p in ax.patches if not isinstance(p, FancyArrowPatch)][:n]


class TestGanttValidation(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def assertRaisesWith(self, fragment, **kwargs):
        data = kwargs.pop("data")
        with self.assertRaises(ValueError) as cm:
            GanttChart(data, **kwargs)
        self.assertIn(fragment, str(cm.exception))

    def test_string_dates_raise(self):
        self.assertRaisesWith(
            "date strings are never parsed",
            data=[{"task": "A", "start": "2024-01-01", "end": date(2024, 1, 2)}],
        )

    def test_end_before_start_raises(self):
        self.assertRaisesWith("ends before it starts", data=[task("A", 5, -2)])

    def test_duplicate_task_raises(self):
        self.assertRaisesWith(
            "Duplicate task name 'A'", data=[task("A", 0, 1), task("A", 2, 1)]
        )

    def test_unknown_dependency_raises(self):
        self.assertRaisesWith(
            "unknown task 'Z'", data=[task("A", 0, 1, depends_on=["Z"])]
        )

    def test_dependency_string_raises(self):
        self.assertRaisesWith(
            "must be a list", data=[task("A", 0, 1), task("B", 1, 1, depends_on="A")]
        )

    def test_progress_out_of_range_raises(self):
        self.assertRaisesWith("[0, 1]", data=[task("A", 0, 1, progress=1.5)])

    def test_group_sort_without_groups_raises(self):
        self.assertRaisesWith(
            "no task carries a `group`",
            data=[task("A", 0, 1)],
            sort=SORT.ASCENDING,
            sort_by=GANTT_SORT_KEY.GROUP,
        )

    def test_sort_by_without_sort_raises(self):
        self.assertRaisesWith(
            "pass `sort` as well", data=schedule(), sort_by=GANTT_SORT_KEY.START
        )

    def test_invalid_show_values_raises(self):
        self.assertRaisesWith("show_values", data=schedule(), show_values=True)

    def test_invalid_record_emphasis_raises(self):
        self.assertRaisesWith("emphasis", data=[task("A", 0, 1, emphasis="loud")])

    def test_empty_data_raises(self):
        self.assertRaisesWith("non-empty list", data=[])

    def test_value_format_ticks_raise(self):
        self.assertRaisesWith("holds dates", data=schedule(), xticks_format="{x:.1f}")

    def test_temporal_types_accepted(self):
        records = [
            {"task": "A", "start": datetime(2024, 1, 1, 8), "end": date(2024, 1, 3)},
            {
                "task": "B",
                "start": np.datetime64("2024-01-02"),
                "end": np.datetime64("2024-01-05"),
            },
        ]
        GanttChart(records)


class TestGanttRowOrder(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_input_order_top_down(self):
        ax = GanttChart(schedule()).axes[0]
        self.assertTrue(ax.yaxis_inverted())
        self.assertEqual(row_labels(ax), ["Design", "Build", "Docs", "Test"])

    def test_sort_by_start(self):
        ax = GanttChart(schedule(), sort=SORT.ASCENDING).axes[0]
        self.assertEqual(row_labels(ax), ["Design", "Docs", "Build", "Test"])
        ax = GanttChart(schedule(), sort=SORT.DESCENDING).axes[0]
        self.assertEqual(row_labels(ax), ["Test", "Build", "Docs", "Design"])

    def test_sort_by_group(self):
        ax = GanttChart(
            schedule(), sort=SORT.ASCENDING, sort_by=GANTT_SORT_KEY.GROUP
        ).axes[0]
        self.assertEqual(row_labels(ax), ["Design", "Docs", "Build", "Test"])
        ax = GanttChart(
            schedule(), sort=SORT.DESCENDING, sort_by=GANTT_SORT_KEY.GROUP
        ).axes[0]
        self.assertEqual(row_labels(ax), ["Test", "Build", "Docs", "Design"])

    def test_missing_and_none_group_sort_alike(self):
        records = [
            task("A", 0, 3, group="g"),
            task("B", 1, 3, group=None),
            task("C", 2, 3),
            task("D", 3, 3, group="g"),
        ]
        ax = GanttChart(
            records, sort=SORT.ASCENDING, sort_by=GANTT_SORT_KEY.GROUP
        ).axes[0]
        self.assertEqual(row_labels(ax), ["A", "D", "B", "C"])

    def test_groups_stay_contiguous(self):
        records = [
            task("A1", 0, 3, group="A"),
            task("B1", 0, 3, group="B"),
            task("A2", 1, 3, group="A"),
            task("B2", 1, 3, group="B"),
        ]
        ax = GanttChart(
            records, sort=SORT.ASCENDING, sort_by=GANTT_SORT_KEY.GROUP
        ).axes[0]
        self.assertEqual(row_labels(ax), ["A1", "A2", "B1", "B2"])


class TestGanttMarks(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_bars_span_start_to_end(self):
        ax = GanttChart(schedule()).axes[0]
        bars = task_bars(ax, 4)
        for bar, record in zip(bars, schedule()):
            self.assertAlmostEqual(bar.get_x(), mdates.date2num(record["start"]))
            self.assertAlmostEqual(
                bar.get_x() + bar.get_width(), mdates.date2num(record["end"])
            )

    def test_time_on_the_x_axis(self):
        ax = GanttChart(schedule()).axes[0]
        self.assertIsInstance(ax.xaxis.get_major_locator(), ScheduleTicks)
        self.assertIsInstance(
            ax.xaxis.get_major_formatter(), mdates.ConciseDateFormatter
        )

    def test_date_format_applies(self):
        ax = GanttChart(schedule(), xticks_format=DATE_FORMAT.ISO).axes[0]
        formatter = ax.xaxis.get_major_formatter()
        self.assertIsInstance(formatter, mdates.DateFormatter)
        self.assertEqual(formatter(mdates.date2num(D0)), "2024-01-01")

    def test_date_window(self):
        ax = GanttChart(
            schedule(), xmin=date(2023, 12, 25), xmax=datetime(2024, 3, 1)
        ).axes[0]
        self.assertEqual(
            ax.get_xlim(),
            (mdates.date2num(date(2023, 12, 25)), mdates.date2num(date(2024, 3, 1))),
        )

    def test_date_tick_rotation(self):
        figure = GanttChart(schedule(), xtickrotate=30)
        figure.canvas.draw()
        rotations = {t.get_rotation() for t in figure.axes[0].get_xticklabels()}
        self.assertEqual(rotations, {30.0})

    def test_group_colours_and_legend(self):
        ax = GanttChart(schedule()).axes[0]
        bars = task_bars(ax, 4)
        colors = [to_hex(bar.get_facecolor()) for bar in bars]
        self.assertEqual(colors[0], colors[2])
        self.assertEqual(colors[1], colors[3])
        self.assertNotEqual(colors[0], colors[1])
        legend = ax.get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["Plan", "Make"])

    def test_no_groups_one_colour_no_legend(self):
        records = [task("A", 0, 3), task("B", 2, 3)]
        ax = GanttChart(records).axes[0]
        bars = task_bars(ax, 2)
        self.assertEqual(
            to_hex(bars[0].get_facecolor()), to_hex(bars[1].get_facecolor())
        )
        self.assertIsNone(ax.get_legend())

    def test_progress_bars(self):
        ax = GanttChart(schedule()).axes[0]
        bars = task_bars(ax, 6)
        progress = bars[4:]
        self.assertEqual(len(progress), 2)
        self.assertAlmostEqual(progress[0].get_width(), 10.0)
        self.assertAlmostEqual(progress[1].get_width(), 15.0)
        self.assertLess(progress[0].get_height(), bars[0].get_height())

    def test_duration_and_progress_values(self):
        ax = GanttChart(schedule(), show_values=GANTT_VALUE.DURATION).axes[0]
        self.assertEqual([t.get_text() for t in ax.texts], ["10d", "30d", "12d", "14d"])
        ax = GanttChart(schedule(), show_values=GANTT_VALUE.PROGRESS).axes[0]
        self.assertEqual([t.get_text() for t in ax.texts], ["100%", "50%", "", ""])
        ax = GanttChart(
            schedule(), show_values=GANTT_VALUE.DURATION, value_format="{x:.1f} days"
        ).axes[0]
        self.assertEqual(ax.texts[0].get_text(), "10.0 days")

    def test_dependencies(self):
        ax = GanttChart(schedule()).axes[0]
        self.assertEqual([p for p in ax.patches if isinstance(p, FancyArrowPatch)], [])
        ax = GanttChart(schedule(), show_dependencies=True).axes[0]
        arrows = [p for p in ax.patches if isinstance(p, FancyArrowPatch)]
        self.assertEqual(len(arrows), 2)

    def test_today_line(self):
        ax = GanttChart(schedule(), show_today=True, today=date(2024, 1, 20)).axes[0]
        (line,) = [c for c in ax.collections if isinstance(c, LineCollection)]
        x = line.get_segments()[0][0][0]
        self.assertAlmostEqual(x, mdates.date2num(date(2024, 1, 20)))
        self.assertEqual(
            to_hex(line.get_color()[0]), to_hex(config["plot_gantt_today_color"])
        )

    def test_today_defaults_to_the_current_date(self):
        ax = GanttChart(schedule(), show_today=True).axes[0]
        (line,) = [c for c in ax.collections if isinstance(c, LineCollection)]
        self.assertAlmostEqual(
            line.get_segments()[0][0][0], mdates.date2num(date.today())
        )

    def test_record_emphasis_mutes_the_bar(self):
        records = schedule()
        records[1]["emphasis"] = EMPHASIS.BACKGROUND
        ax = GanttChart(records).axes[0]
        bars = task_bars(ax, 4)
        self.assertEqual(to_hex(bars[1].get_facecolor()), to_hex(config["muted_color"]))

    def test_emphasis_rule_reads_duration(self):
        ax = GanttChart(schedule(), emphasis_rule={"above": 12}).axes[0]
        bars = task_bars(ax, 4)
        muted = [
            to_hex(b.get_facecolor()) == to_hex(config["muted_color"]) for b in bars
        ]
        self.assertEqual(muted, [True, False, True, False])

    def test_emphasis_rule_rejects_by(self):
        with self.assertRaises(ValueError):
            GanttChart(schedule(), emphasis_rule={"top": 1, "by": "mean"})

    def test_figure_emphasis(self):
        ax = GanttChart(schedule(), emphasis=EMPHASIS.BACKGROUND).axes[0]
        bars = task_bars(ax, 4)
        self.assertTrue(
            all(
                to_hex(b.get_facecolor()) == to_hex(config["muted_color"]) for b in bars
            )
        )

    def test_several_schedules_draw_subplots(self):
        figure = GanttChart([schedule(), schedule()[:2]], subtitle=["One", "Two"])
        axes = [ax for ax in figure.axes if ax.axison]
        self.assertEqual(len(axes), 2)
        self.assertEqual(row_labels(axes[1]), ["Design", "Build"])

    def test_every_theme_renders(self):
        for theme in THEMES:
            with self.subTest(theme=theme):
                config.set_theme(theme)
                GanttChart(
                    schedule() + [task("Release", 49, 0, group="Make")],
                    show_dependencies=True,
                    show_today=True,
                    today_label="Today",
                    show_values=GANTT_VALUE.DURATION,
                    show_group_headers=True,
                    period=DATE_PERIOD.WEEK,
                ).savefig(__import__("io").BytesIO(), format="png")
                plt.close("all")

    def test_base_theme_carries_the_keys(self):
        keys = [k for k in _base.BASE_THEME if k.startswith("plot_gantt_")]
        self.assertGreaterEqual(len(keys), 10)


def period_labels(figure):
    """The period row and the parent row labels of a gantt figure, after a draw."""
    figure.canvas.draw()
    ax = figure.axes[0]
    parent = [t.get_text() for c in ax.child_axes for t in c.get_xticklabels()]
    return [t.get_text() for t in ax.get_xticklabels()], parent


class TestGanttPeriods(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def span(self, start, end):
        return [{"task": "A", "start": start, "end": end}]

    def test_date_ticks_run_from_the_first_start_to_the_last_end(self):
        figure = GanttChart(self.span(date(2024, 3, 4), date(2024, 3, 24)))
        figure.canvas.draw()
        ticks = [
            mdates.num2date(t).date() for t in figure.axes[0].xaxis.get_majorticklocs()
        ]
        self.assertEqual(ticks[0], date(2024, 3, 4))
        self.assertEqual(ticks[-1], date(2024, 3, 24))
        self.assertEqual({(b - a).days for a, b in zip(ticks, ticks[1:])}, {4})
        long = GanttChart(self.span(date(2024, 1, 15), date(2026, 1, 15)))
        long.canvas.draw()
        ticks = [
            mdates.num2date(t).date() for t in long.axes[0].xaxis.get_majorticklocs()
        ]
        self.assertEqual(ticks[0], date(2024, 1, 15))
        self.assertEqual(ticks[-1], date(2026, 1, 15))
        self.assertTrue(all(t.day == 15 for t in ticks))

    def test_period_view_covers_whole_periods(self):
        ax = GanttChart(
            self.span(date(2024, 2, 20), date(2025, 8, 10)), period="quarter"
        ).axes[0]
        lo, hi = (mdates.num2date(v).date() for v in ax.get_xlim())
        self.assertEqual((lo, hi), (date(2024, 1, 1), date(2025, 10, 1)))
        ax.figure.canvas.draw()
        self.assertEqual(len(ax.get_xticklabels()), 7)
        fixed = GanttChart(
            self.span(date(2024, 2, 20), date(2025, 8, 10)),
            period="quarter",
            xmax=date(2025, 9, 1),
        ).axes[0]
        self.assertEqual(mdates.num2date(fixed.get_xlim()[1]).date(), date(2025, 9, 1))

    def test_month_period(self):
        figure = GanttChart(
            self.span(date(2023, 11, 20), date(2024, 5, 1)), period=DATE_PERIOD.MONTH
        )
        months, years = period_labels(figure)
        # the task ends at the start of May, so the view ends there too
        self.assertEqual(months, ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr"])
        self.assertEqual(years, ["2023", "2024"])

    def test_project_month_period_counts_from_the_start(self):
        months, years = period_labels(
            GanttChart(
                self.span(date(2024, 3, 15), date(2025, 9, 1)), period="project_month"
            )
        )
        self.assertEqual(months, [f"M{i}" for i in range(1, len(months) + 1)])
        self.assertGreaterEqual(len(months), 18)
        self.assertEqual(years, ["Y1", "Y2"])
        figure = GanttChart(
            self.span(date(2024, 3, 15), date(2024, 6, 1)),
            period="project_month",
            xmin=date(2024, 3, 1),
        )
        self.assertIn(
            mdates.date2num(date(2024, 4, 1)), figure.axes[0].xaxis.get_minorticklocs()
        )
        self.assertEqual(period_labels(figure)[0][:2], ["M1", "M2"])

    def test_period_edges_carry_the_grid(self):
        ax = GanttChart(
            self.span(date(2024, 1, 10), date(2024, 4, 20)), period=DATE_PERIOD.MONTH
        ).axes[0]
        edges = ax.xaxis.get_minorticklocs()
        self.assertIn(mdates.date2num(date(2024, 2, 1)), edges)
        ax.figure.canvas.draw()
        minor = [t.gridline for t in ax.xaxis.get_minor_ticks()]
        self.assertTrue(any(line.get_visible() for line in minor))
        self.assertFalse(any(l.get_visible() for l in ax.xaxis.get_gridlines()))

    def test_week_quarter_day_year_labels(self):
        weeks, months = period_labels(
            GanttChart(self.span(date(2024, 1, 1), date(2024, 1, 29)), period="week")
        )
        self.assertEqual(weeks[:2], ["W01", "W02"])
        self.assertEqual(months, ["Jan 2024"])
        quarters, _ = period_labels(
            GanttChart(
                self.span(date(2024, 1, 1), date(2024, 12, 20)), period="quarter"
            )
        )
        self.assertEqual(quarters, ["Q1", "Q2", "Q3", "Q4"])
        days, _ = period_labels(
            GanttChart(self.span(date(2024, 3, 1), date(2024, 3, 4)), period="day")
        )
        self.assertEqual(days[:3], ["01", "02", "03"])
        years, parent = period_labels(
            GanttChart(self.span(date(2022, 3, 1), date(2024, 10, 1)), period="year")
        )
        self.assertEqual(years, ["2022", "2023", "2024"])
        self.assertEqual(parent, [])

    def test_xticks_format_sets_the_period_labels(self):
        months, _ = period_labels(
            GanttChart(
                self.span(date(2024, 1, 10), date(2024, 3, 20)),
                period="month",
                xticks_format="%B",
            )
        )
        self.assertEqual(months, ["January", "February", "March"])

    def test_invalid_period_raises(self):
        with self.assertRaises(ValueError):
            GanttChart(schedule(), period="fortnight")


class TestGanttGroupHeaders(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_header_rows_cluster_groups(self):
        ax = GanttChart(schedule(), show_group_headers=True).axes[0]
        self.assertEqual(
            row_labels(ax), ["Plan", "Design", "Docs", "Make", "Build", "Test"]
        )
        bold = [
            t.get_text() for t in ax.get_yticklabels() if t.get_fontweight() == "bold"
        ]
        self.assertEqual(bold, ["Plan", "Make"])
        ticks = list(ax.get_yticks())
        self.assertAlmostEqual(ticks[3] - ticks[2], 1 + config["plot_gantt_group_gap"])

    def test_summary_bars_span_their_groups(self):
        ax = GanttChart(schedule(), show_group_headers=True).axes[0]
        make = [
            p
            for p in ax.patches
            if not isinstance(p, FancyArrowPatch)
            and abs(p.get_y() + p.get_height() / 2 - ax.get_yticks()[3]) < 1e-9
        ]
        self.assertEqual(len(make), 1)
        self.assertAlmostEqual(make[0].get_x(), mdates.date2num(D0 + timedelta(days=8)))
        self.assertAlmostEqual(
            make[0].get_x() + make[0].get_width(),
            mdates.date2num(D0 + timedelta(days=49)),
        )

    def test_headers_turn_the_legend_off(self):
        ax = GanttChart(schedule(), show_group_headers=True).axes[0]
        self.assertIsNone(ax.get_legend())

    def test_headers_without_groups_raise(self):
        with self.assertRaises(ValueError) as cm:
            GanttChart([task("A", 0, 1)], show_group_headers=True)
        self.assertIn("show_group_headers", str(cm.exception))


class TestGanttMilestonesAndArrows(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def records(self):
        records = schedule()
        records.append(task("Release", 49, 0, group="Make", depends_on=["Test"]))
        return records

    def test_milestone_draws_a_marker(self):
        ax = GanttChart(self.records()).axes[0]
        (marker,) = [
            l
            for l in ax.lines
            if l.get_marker() == config["plot_gantt_milestone_marker"]
        ]
        self.assertAlmostEqual(
            marker.get_xdata()[0], mdates.date2num(D0 + timedelta(days=49))
        )
        self.assertFalse(task_bars(ax, 5)[4].get_visible())

    def test_milestone_prints_its_date(self):
        ax = GanttChart(self.records(), show_values=GANTT_VALUE.DURATION).axes[0]
        texts = [t.get_text() for t in ax.texts]
        self.assertIn("19 Feb", texts)
        self.assertNotIn("0d", texts)

    def test_left_entry_arrives_at_the_start(self):
        records = [task("A", 0, 3), task("B", 5, 3, depends_on=["A"])]
        ax = GanttChart(
            records,
            show_dependencies=True,
            style={"plot_gantt_dependency_entry": GANTT_ARROW_ENTRY.LEFT},
        ).axes[0]
        (arrow,) = [p for p in ax.patches if isinstance(p, FancyArrowPatch)]
        self.assertEqual(
            arrow._posA_posB[1], (mdates.date2num(D0 + timedelta(days=5)), 1.0)
        )

    def test_left_entry_without_room_enters_from_the_top(self):
        records = [task("A", 0, 3), task("B", 1, 3, depends_on=["A"])]
        ax = GanttChart(
            records,
            show_dependencies=True,
            style={"plot_gantt_dependency_entry": GANTT_ARROW_ENTRY.LEFT},
        ).axes[0]
        (arrow,) = [p for p in ax.patches if isinstance(p, FancyArrowPatch)]
        self.assertLess(arrow._posA_posB[1][1], 1.0)

    def test_invalid_arrow_entry_raises(self):
        with self.assertRaises(ValueError):
            GanttChart(schedule(), style={"plot_gantt_dependency_entry": "right"})

    def test_today_label(self):
        ax = GanttChart(
            schedule(), show_today=True, today=date(2024, 1, 20), today_label="Today"
        ).axes[0]
        self.assertIn("Today", [t.get_text() for t in ax.texts])
        ax = GanttChart(schedule(), show_today=True, today=date(2024, 1, 20)).axes[0]
        self.assertEqual(len(ax.texts), 0)


class TestGanttComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_rejects(self):
        with self.assertRaises(ValueError) as cm:
            Panel([GanttChart(schedule()), LineChart([{"x": 1, "y": 2}])])
        self.assertIn("gantt", str(cm.exception))

    def test_grid_cell(self):
        figure = Grid([[GanttChart(schedule()), GanttChart(schedule()[:2])]])
        axes = [ax for ax in figure.axes if ax.axison]
        self.assertEqual(len(axes), 2)
        self.assertEqual(row_labels(axes[0]), ["Design", "Build", "Docs", "Test"])
        self.assertIsInstance(
            axes[0].xaxis.get_major_formatter(), mdates.ConciseDateFormatter
        )


class TestValueAxisKind(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_default_hook_is_none(self):
        self.assertIsNone(Layer.value_kind(object.__new__(Layer)))

    def test_existing_fronts_keep_their_axes(self):
        ax = BarChart([{"label": "a", "y": 1}, {"label": "b", "y": 2}]).axes[0]
        self.assertNotIsInstance(
            ax.yaxis.get_major_formatter(), mdates.ConciseDateFormatter
        )
        ax = LineChart([{"x": D0, "y": 1}, {"x": D0 + timedelta(days=3), "y": 2}]).axes[
            0
        ]
        self.assertIsInstance(
            ax.xaxis.get_major_formatter(), mdates.ConciseDateFormatter
        )
        self.assertNotIsInstance(
            ax.yaxis.get_major_formatter(), mdates.ConciseDateFormatter
        )

    def test_gantt_layer_reports_temporal_value(self):
        figure = GanttChart(schedule())
        (layer,) = figure._chart_metadata["panel"].layers
        self.assertIsInstance(layer, GanttLayer)
        self.assertEqual(layer.value_kind(), "temporal")
        self.assertEqual(figure._chart_metadata["panel"].temporal_axis, "x")


if __name__ == "__main__":
    unittest.main()
