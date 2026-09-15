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
from matplotlib.patches import FancyArrowPatch

from datachart.charts import BarChart, GanttChart, LineChart
from datachart.config import config
from datachart.constants import (
    DATE_FORMAT,
    EMPHASIS,
    GANTT_SORT_KEY,
    GANTT_VALUE,
    SORT,
    THEME,
)
from datachart.themes import _base
from datachart.utils import Grid, Panel
from datachart.utils._internal.layers import GanttLayer, Layer

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
        self.assertIsInstance(ax.xaxis.get_major_locator(), mdates.AutoDateLocator)
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
        self.assertEqual(
            [t.get_text() for t in ax.texts], ["10d", "30d", "12d", "14d"]
        )
        ax = GanttChart(schedule(), show_values=GANTT_VALUE.PROGRESS).axes[0]
        self.assertEqual([t.get_text() for t in ax.texts], ["100%", "50%", "", ""])
        ax = GanttChart(
            schedule(), show_values=GANTT_VALUE.DURATION, value_format="{x:.1f} days"
        ).axes[0]
        self.assertEqual(ax.texts[0].get_text(), "10.0 days")

    def test_dependencies(self):
        ax = GanttChart(schedule()).axes[0]
        self.assertEqual(
            [p for p in ax.patches if isinstance(p, FancyArrowPatch)], []
        )
        ax = GanttChart(schedule(), show_dependencies=True).axes[0]
        arrows = [p for p in ax.patches if isinstance(p, FancyArrowPatch)]
        self.assertEqual(len(arrows), 2)

    def test_today_line(self):
        ax = GanttChart(schedule(), show_today=True, today=date(2024, 1, 20)).axes[0]
        (line,) = [c for c in ax.collections if isinstance(c, LineCollection)]
        x = line.get_segments()[0][0][0]
        self.assertAlmostEqual(x, mdates.date2num(date(2024, 1, 20)))
        self.assertEqual(to_hex(line.get_color()[0]), to_hex(config["plot_gantt_today_color"]))

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
        muted = [to_hex(b.get_facecolor()) == to_hex(config["muted_color"]) for b in bars]
        self.assertEqual(muted, [True, False, True, False])

    def test_emphasis_rule_rejects_by(self):
        with self.assertRaises(ValueError):
            GanttChart(schedule(), emphasis_rule={"top": 1, "by": "mean"})

    def test_figure_emphasis(self):
        ax = GanttChart(schedule(), emphasis=EMPHASIS.BACKGROUND).axes[0]
        bars = task_bars(ax, 4)
        self.assertTrue(
            all(to_hex(b.get_facecolor()) == to_hex(config["muted_color"]) for b in bars)
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
                    schedule(),
                    show_dependencies=True,
                    show_today=True,
                    show_values=GANTT_VALUE.DURATION,
                ).savefig(__import__("io").BytesIO(), format="png")
                plt.close("all")

    def test_base_theme_carries_the_keys(self):
        keys = [k for k in _base.BASE_THEME if k.startswith("plot_gantt_")]
        self.assertGreaterEqual(len(keys), 10)


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
        ax = LineChart([{"x": D0, "y": 1}, {"x": D0 + timedelta(days=3), "y": 2}]).axes[0]
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
