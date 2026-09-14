"""Tests for the bump chart: validation, per-period ranking, drawing, and composition."""

import math
import unittest

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import BumpChart
from datachart.config import config
from datachart.constants import RANK, LABEL_POSITION, THEME
from datachart.utils import Panel, Grid
from datachart.utils._internal.layers import BumpLayer, rank_series
from datachart.utils._internal.validate import (
    validate_rank_by,
    validate_label_position,
    validate_line_curve,
    validate_given_ranks,
)


def series(values, x=None):
    x = range(len(values)) if x is None else x
    return [{"x": i, "y": v} for i, v in zip(x, values)]


def _nan_list(values):
    return [None if math.isnan(v) else v for v in values]


class TestBumpValidation(unittest.TestCase):
    def test_rank_by_defaults_to_descending(self):
        self.assertEqual(validate_rank_by(None), RANK.VALUE_DESCENDING)
        for member in (RANK.VALUE_ASCENDING, RANK.GIVEN):
            self.assertEqual(validate_rank_by(member), member)

    def test_rank_by_rejects_unknown(self):
        with self.assertRaisesRegex(ValueError, "rank_by"):
            validate_rank_by("value")

    def test_label_position_defaults_to_end(self):
        self.assertEqual(validate_label_position(None), LABEL_POSITION.END)
        self.assertEqual(
            validate_label_position(LABEL_POSITION.BOTH), LABEL_POSITION.BOTH
        )

    def test_label_position_rejects_unknown(self):
        with self.assertRaisesRegex(ValueError, "label_position"):
            validate_label_position("middle")

    def test_line_curve_defaults_to_straight(self):
        self.assertEqual(validate_line_curve(None), 0.0)
        self.assertEqual(validate_line_curve(1), 1.0)

    def test_line_curve_rejects_out_of_range_and_non_numbers(self):
        for bad in (-0.1, 1.5, "0.5", True):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, "line_curve"):
                    validate_line_curve(bad)

    def test_given_ranks_accept_positive_whole_numbers(self):
        validate_given_ranks([1, 2, 3.0, float("nan")])

    def test_given_ranks_reject_non_integer_and_non_positive(self):
        for bad in ([1, 2.5], [0, 1], [-1], [True]):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    validate_given_ranks(bad)


class TestRankSeries(unittest.TestCase):
    def test_descending_ranks_highest_first(self):
        periods, ranks = rank_series(
            [[1, 2], [1, 2], [1, 2]], [[10, 1], [5, 7], [1, 9]], RANK.VALUE_DESCENDING
        )
        self.assertEqual(list(periods), [1, 2])
        self.assertEqual([list(r) for r in ranks], [[1, 3], [2, 2], [3, 1]])

    def test_ascending_ranks_lowest_first(self):
        _, ranks = rank_series([[1], [1]], [[10], [5]], RANK.VALUE_ASCENDING)
        self.assertEqual([list(r) for r in ranks], [[2], [1]])

    def test_ties_keep_input_order(self):
        for rank_by in (RANK.VALUE_DESCENDING, RANK.VALUE_ASCENDING):
            with self.subTest(rank_by=rank_by):
                _, ranks = rank_series([[0], [0], [0]], [[4], [4], [4]], rank_by)
                self.assertEqual([list(r) for r in ranks], [[1], [2], [3]])

    def test_missing_period_leaves_a_gap_and_takes_no_rank(self):
        periods, ranks = rank_series(
            [[1, 2, 3], [1, 3], [1, 2, 3]],
            [[1, 5, 1], [9, 9], [2, 3, 2]],
            RANK.VALUE_DESCENDING,
        )
        self.assertEqual(list(periods), [1, 2, 3])
        self.assertEqual(
            [_nan_list(r) for r in ranks],
            [[3, 1, 3], [1, None, 1], [2, 2, 2]],
        )

    def test_missing_value_is_a_gap(self):
        _, ranks = rank_series(
            [[1, 2], [1, 2]], [[1, None], [2, 2]], RANK.VALUE_DESCENDING
        )
        self.assertEqual([_nan_list(r) for r in ranks], [[2, None], [1, 1]])

    def test_given_ranks_pass_through_with_gaps(self):
        _, ranks = rank_series([[1, 2], [2]], [[2, 1], [2]], RANK.GIVEN)
        self.assertEqual([_nan_list(r) for r in ranks], [[2, 1], [None, 2]])

    def test_given_ranks_are_validated(self):
        with self.assertRaisesRegex(ValueError, "positive integer"):
            rank_series([[1]], [[0.5]], RANK.GIVEN)

    def test_numeric_periods_sort_and_labels_keep_first_seen_order(self):
        periods, _ = rank_series([[3, 1], [2]], [[1, 1], [1]], RANK.GIVEN)
        self.assertEqual(list(periods), [1, 2, 3])
        periods, _ = rank_series([["b", "a"], ["c"]], [[1, 1], [1]], RANK.GIVEN)
        self.assertEqual(list(periods), ["b", "a", "c"])

    def test_repeated_period_in_one_series_raises(self):
        with self.assertRaisesRegex(ValueError, "period"):
            rank_series([[1, 1]], [[1, 2]], RANK.VALUE_DESCENDING)


# rank descending: A 1,3  B 2,2  C 3,1
DATA = [series([10, 1]), series([5, 7]), series([1, 9])]
NAMES = ["A", "B", "C"]


def _texts(ax):
    return {t.get_text(): t for t in ax.texts}


class TestBumpChartDrawing(unittest.TestCase):
    def tearDown(self):
        plt.close("all")
        config.set_theme(THEME.DEFAULT)

    def test_lines_draw_ranks_on_an_inverted_integer_axis(self):
        fig = BumpChart(DATA, subtitle=NAMES)
        ax = fig.axes[0]
        ranks = [list(line.get_ydata()) for line in ax.get_lines()]
        self.assertEqual(ranks, [[1, 3], [2, 2], [3, 1]])
        bottom, top = ax.get_ylim()
        self.assertEqual((bottom, top), (3.5, 0.5))
        self.assertTrue(all(t == int(t) for t in ax.get_yticks()))

    def test_periods_span_the_x_axis_with_whole_end_markers(self):
        ax = BumpChart(DATA, subtitle=NAMES).axes[0]
        self.assertEqual(ax.get_xlim(), (0, 1))
        self.assertFalse(ax.get_lines()[0].get_clip_on())
        cropped = BumpChart(DATA, subtitle=NAMES, xmax=0.5).axes[0]
        self.assertTrue(cropped.get_lines()[0].get_clip_on())

    def test_user_rank_limits_keep_rank_one_on_top(self):
        fig = BumpChart(DATA, subtitle=NAMES, ymin=1, ymax=2)
        self.assertEqual(fig.axes[0].get_ylim(), (2, 1))

    def test_markers_on_by_default_and_switchable(self):
        fig = BumpChart(DATA, subtitle=NAMES)
        self.assertEqual(fig.axes[0].get_lines()[0].get_marker(), "o")
        fig = BumpChart(DATA, subtitle=NAMES, show_markers=False)
        self.assertIn(fig.axes[0].get_lines()[0].get_marker(), ("None", "", None))

    def test_style_keys_reach_the_line(self):
        fig = BumpChart(
            DATA, style={"plot_bump_line_width": 4, "plot_bump_marker": "s"}
        )
        line = fig.axes[0].get_lines()[0]
        self.assertEqual(line.get_linewidth(), 4)
        self.assertEqual(line.get_marker(), "s")

    def test_end_labels_sit_at_the_last_point_in_series_color(self):
        fig = BumpChart(DATA, subtitle=NAMES)
        ax = fig.axes[0]
        texts = _texts(ax)
        self.assertEqual(set(texts), set(NAMES))
        for line, name in zip(ax.get_lines(), NAMES):
            text = texts[name]
            self.assertEqual(text.xy, (line.get_xdata()[-1], line.get_ydata()[-1]))
            self.assertEqual(text.get_ha(), "left")
            self.assertEqual(text.get_color(), line.get_color())

    def test_label_position_both_labels_each_end(self):
        fig = BumpChart(DATA, subtitle=NAMES, label_position=LABEL_POSITION.BOTH)
        ax = fig.axes[0]
        self.assertEqual(len(ax.texts), 6)
        starts = [t for t in ax.texts if t.get_ha() == "right"]
        self.assertEqual({t.xy[0] for t in starts}, {0})

    def test_start_labels_push_the_rank_ticks_out(self):
        plain = BumpChart(DATA, subtitle=NAMES)
        start = BumpChart(DATA, subtitle=NAMES, label_position=LABEL_POSITION.START)
        pad = lambda fig: fig.axes[0].yaxis.get_major_ticks()[0].get_pad()
        self.assertGreater(pad(start), pad(plain))

    def test_legend_off_with_labels_and_on_without(self):
        self.assertIsNone(BumpChart(DATA, subtitle=NAMES).axes[0].get_legend())
        fig = BumpChart(DATA, subtitle=NAMES, show_labels=False)
        self.assertEqual(len(fig.axes[0].texts), 0)
        self.assertIsNotNone(fig.axes[0].get_legend())

    def test_show_values_prints_the_original_values(self):
        fig = BumpChart(DATA, subtitle=NAMES, show_values=True, value_step=1)
        fig.canvas.draw()
        printed = {t.get_text() for t in fig.axes[0].texts} - set(NAMES)
        self.assertEqual(printed, {"10", "1", "5", "7", "9"})

    def test_missing_period_breaks_the_line(self):
        data = [series([1, 2, 3]), series([3, 1], x=[0, 2])]
        fig = BumpChart(data, subtitle=["A", "B"])
        ydata = fig.axes[0].get_lines()[1].get_ydata()
        self.assertTrue(math.isnan(ydata[1]))

    def test_line_curve_passes_through_every_point(self):
        fig = BumpChart(DATA, subtitle=NAMES, line_curve=1)
        line = fig.axes[0].get_lines()[0]
        x, y = line.get_xdata(), line.get_ydata()
        self.assertGreater(len(x), 2)
        self.assertEqual((x[0], y[0]), (0, 1))
        self.assertEqual((x[-1], y[-1]), (1, 3))
        self.assertTrue(np.all(np.diff(y) >= 0))
        self.assertLess(y[len(y) // 4], 1 + 2 * 0.25)

    def test_emphasis_rule_top_highlights_best_mean_ranks(self):
        data = [series([9, 9]), series([5, 5]), series([1, 1])]
        fig = BumpChart(data, subtitle=NAMES, emphasis_rule={"top": 1})
        panel = fig._chart_metadata["panel"]
        roles = [layer.emphasis for layer in panel.layers]
        self.assertEqual(roles, ["highlight", "background", "background"])

    def test_hover_reports_period_rank_and_value(self):
        fig = BumpChart(DATA, subtitle=NAMES, line_curve=1)
        line, resolve = fig._hover_targets[0]
        last = len(line.get_xdata()) - 1
        self.assertEqual(resolve(0), {"label": "A", "x": 0, "y": 1.0, "value": 10.0})
        self.assertEqual(resolve(last), {"label": "A", "x": 1, "y": 3.0, "value": 1.0})

    def test_invalid_settings_raise(self):
        for kwargs in (
            {"rank_by": "value"},
            {"label_position": "middle"},
            {"line_curve": 2},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    BumpChart(DATA, **kwargs)

    def test_rank_given_draws_y_as_rank(self):
        fig = BumpChart([series([2, 1]), series([1, 2])], rank_by=RANK.GIVEN)
        ranks = [list(l.get_ydata()) for l in fig.axes[0].get_lines()]
        self.assertEqual(ranks, [[2, 1], [1, 2]])

    def test_temporal_periods_draw_on_a_date_axis(self):
        from datetime import date

        data = [
            [{"x": date(2024, m, 1), "y": v} for m, v in zip((1, 2), (1, 2))],
            [{"x": date(2024, m, 1), "y": v} for m, v in zip((1, 2), (2, 1))],
        ]
        fig = BumpChart(data, subtitle=["A", "B"], line_curve=0.5)
        fig.canvas.draw()
        labels = [t.get_text() for t in fig.axes[0].get_xticklabels()]
        self.assertTrue(any("Jan" in l or "Feb" in l for l in labels), labels)

    def test_every_theme_renders(self):
        for theme in (THEME.DEFAULT, THEME.SKETCH, THEME.HATCH, THEME.INK):
            with self.subTest(theme=theme):
                config.set_theme(theme)
                BumpChart(DATA, subtitle=NAMES, line_curve=0.5).canvas.draw()


class TestBumpChartComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_overlay_keeps_bump_layers_and_rank_axis(self):
        fig = Panel(
            [
                BumpChart(DATA, subtitle=NAMES),
                BumpChart([series([3, 2])], subtitle="D", rank_by=RANK.GIVEN),
            ]
        )
        ax = fig.axes[0]
        layers = fig._chart_metadata["panel"].layers
        self.assertEqual(len(layers), 4)
        self.assertTrue(all(isinstance(l, BumpLayer) for l in layers))
        self.assertTrue(ax.yaxis_inverted())
        self.assertEqual({"A", "B", "C", "D"}, set(_texts(ax)))

    def test_grid_cell_renders_the_bump_panel(self):
        fig = Grid([BumpChart(DATA, subtitle=NAMES), BumpChart(DATA, subtitle=NAMES)])
        drawn = [ax for ax in fig.axes if ax.get_lines()]
        self.assertEqual(len(drawn), 2)
        for ax in drawn:
            self.assertTrue(ax.yaxis_inverted())
            self.assertEqual(len(ax.texts), 3)

    def test_subplots_rank_across_every_series(self):
        fig = BumpChart(DATA, subtitle=NAMES, subplots=True)
        ranks = [list(ax.get_lines()[0].get_ydata()) for ax in fig.axes[:3]]
        self.assertEqual(ranks, [[1, 3], [2, 2], [3, 1]])


if __name__ == "__main__":
    unittest.main()
