"""Tests for the dumbbell chart: validation, sort, marks, labels, composition."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.colors import to_hex

from datachart.charts import BoxPlot, DumbbellChart
from datachart.config import config
from datachart.constants import (
    DUMBBELL_SORT_KEY,
    DUMBBELL_VALUE,
    EMPHASIS,
    LINE_STYLE,
    ORIENTATION,
    SORT,
    THEME,
)
from datachart.utils import Grid, Panel

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

PAPER_ACCENT = ["#5b84c4", "#c85450"]


def records():
    return [
        {"label": "A", "start": 3.0, "end": 7.0},
        {"label": "B", "start": 5.0, "end": 4.0},
        {"label": "C", "start": 1.0, "end": 9.0},
    ]


def dots(ax):
    return [c for c in ax.collections if isinstance(c, PathCollection)]


def connectors(ax):
    return [c for c in ax.collections if isinstance(c, LineCollection)]


def category_labels(ax, horizontal=True):
    ticks = ax.get_yticklabels() if horizontal else ax.get_xticklabels()
    return [t.get_text() for t in ticks]


def texts(ax):
    return [t.get_text() for t in ax.texts]


class TestDumbbellValidation(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def assertRaisesWith(self, fragment, **kwargs):
        data = kwargs.pop("data")
        with self.assertRaises(ValueError) as cm:
            DumbbellChart(data, **kwargs)
        self.assertIn(fragment, str(cm.exception))

    def test_empty_data_raises(self):
        self.assertRaisesWith("non-empty list", data=[])

    def test_missing_label_raises(self):
        self.assertRaisesWith("has no `label` key", data=[{"start": 1, "end": 2}])

    def test_non_numeric_endpoint_raises(self):
        self.assertRaisesWith("`start`", data=[{"label": "A", "start": "1", "end": 2}])

    def test_bool_endpoint_raises(self):
        self.assertRaisesWith("`end`", data=[{"label": "A", "start": 1, "end": True}])

    def test_nan_endpoint_raises(self):
        self.assertRaisesWith(
            "`end`", data=[{"label": "A", "start": 1, "end": float("nan")}]
        )

    def test_duplicate_label_raises(self):
        self.assertRaisesWith(
            "Duplicate label 'A'",
            data=[
                {"label": "A", "start": 1, "end": 2},
                {"label": "A", "start": 3, "end": 4},
            ],
        )

    def test_invalid_record_emphasis_raises(self):
        self.assertRaisesWith(
            "emphasis", data=[{"label": "A", "start": 1, "end": 2, "emphasis": "x"}]
        )

    def test_sort_by_without_sort_raises(self):
        self.assertRaisesWith(
            "pass `sort` as well", data=records(), sort_by=DUMBBELL_SORT_KEY.DELTA
        )

    def test_invalid_sort_by_raises(self):
        self.assertRaisesWith(
            "`sort_by`", data=records(), sort=SORT.ASCENDING, sort_by="group"
        )

    def test_invalid_value_kind_raises(self):
        self.assertRaisesWith(
            "value_kind", data=records(), show_values=True, value_kind="ratio"
        )

    def test_kind_in_both_names_raises(self):
        with self.assertWarns(DeprecationWarning):
            self.assertRaisesWith(
                "value_kind", data=records(), show_values="delta", value_kind="delta"
            )

    def test_invalid_marker_pair_raises(self):
        self.assertRaisesWith("`marker`", data=records(), marker="o")

    def test_single_dict_raises(self):
        self.assertRaisesWith(
            "non-empty list", data={"label": "A", "start": 1, "end": 2}
        )

    def test_numpy_numbers_accepted(self):
        figure = DumbbellChart(
            [{"label": "A", "start": np.float64(1.5), "end": np.int64(3)}]
        )
        self.assertEqual(len(dots(figure.axes[0])), 2)


class TestDumbbellSort(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def order(self, **kwargs):
        return category_labels(DumbbellChart(records(), **kwargs).axes[0])

    def test_input_order_by_default(self):
        self.assertEqual(self.order(), ["A", "B", "C"])

    def test_sort_by_start_default(self):
        self.assertEqual(self.order(sort=SORT.ASCENDING), ["C", "A", "B"])

    def test_sort_by_end_descending(self):
        self.assertEqual(
            self.order(sort=SORT.DESCENDING, sort_by=DUMBBELL_SORT_KEY.END),
            ["C", "A", "B"],
        )

    def test_sort_by_delta(self):
        self.assertEqual(
            self.order(sort=SORT.ASCENDING, sort_by=DUMBBELL_SORT_KEY.DELTA),
            ["B", "A", "C"],
        )

    def test_ties_keep_input_order(self):
        data = [
            {"label": "X", "start": 1, "end": 2},
            {"label": "Y", "start": 1, "end": 5},
        ]
        figure = DumbbellChart(data, sort=SORT.DESCENDING)
        self.assertEqual(category_labels(figure.axes[0]), ["X", "Y"])

    def test_first_row_at_top_when_horizontal(self):
        ax = DumbbellChart(records()).axes[0]
        self.assertTrue(ax.yaxis_inverted())

    def test_vertical_rows_left_to_right(self):
        ax = DumbbellChart(
            records(), orientation=ORIENTATION.VERTICAL, sort=SORT.ASCENDING
        ).axes[0]
        self.assertEqual(category_labels(ax, horizontal=False), ["C", "A", "B"])
        self.assertFalse(ax.xaxis_inverted())


class TestDumbbellMarks(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_dot_positions_horizontal(self):
        ax = DumbbellChart(records()).axes[0]
        start, end = dots(ax)
        np.testing.assert_allclose(start.get_offsets(), [[3, 0], [5, 1], [1, 2]])
        np.testing.assert_allclose(end.get_offsets(), [[7, 0], [4, 1], [9, 2]])

    def test_vertical_flips_axes(self):
        ax = DumbbellChart(records(), orientation=ORIENTATION.VERTICAL).axes[0]
        start, _ = dots(ax)
        np.testing.assert_allclose(start.get_offsets(), [[0, 3], [1, 5], [2, 1]])

    def test_scaley_addresses_the_value_axis(self):
        ax = DumbbellChart(records(), scaley="log").axes[0]
        self.assertEqual(ax.get_xscale(), "log")
        self.assertEqual(ax.get_yscale(), "linear")

    def test_connector_under_dots(self):
        ax = DumbbellChart(records()).axes[0]
        (connector,) = connectors(ax)
        self.assertEqual(len(connector.get_segments()), 3)
        self.assertLess(connector.get_zorder(), min(c.get_zorder() for c in dots(ax)))

    def test_default_endpoint_colors_are_paper_accent(self):
        start, end = dots(DumbbellChart(records()).axes[0])
        self.assertEqual(to_hex(start.get_facecolor()[0]), PAPER_ACCENT[0])
        self.assertEqual(to_hex(end.get_facecolor()[0]), PAPER_ACCENT[1])

    def test_style_colors_override_the_pair(self):
        figure = DumbbellChart(
            records(),
            style={
                "plot_dumbbell_start_color": "#111111",
                "plot_dumbbell_end_color": "#222222",
            },
        )
        start, end = dots(figure.axes[0])
        self.assertEqual(to_hex(start.get_facecolor()[0]), "#111111")
        self.assertEqual(to_hex(end.get_facecolor()[0]), "#222222")

    def test_show_values_prints_the_default_kind(self):
        ax = DumbbellChart(records(), show_values=True).axes[0]
        expected = DumbbellChart(
            records(), show_values=True, value_kind=DUMBBELL_VALUE.ENDPOINTS
        ).axes[0]
        self.assertTrue(texts(ax))
        self.assertEqual(texts(ax), texts(expected))

    def test_kind_as_show_values_warns_and_maps(self):
        with self.assertWarnsRegex(DeprecationWarning, "value_kind") as caught:
            ax = DumbbellChart(records(), show_values=DUMBBELL_VALUE.DELTA).axes[0]
        self.assertEqual(caught.filename, __file__)
        expected = DumbbellChart(
            records(), show_values=True, value_kind=DUMBBELL_VALUE.DELTA
        ).axes[0]
        self.assertEqual(texts(ax), texts(expected))

    def test_coincident_endpoints_draw_one_dot_no_connector(self):
        data = [
            {"label": "A", "start": 2, "end": 2},
            {"label": "B", "start": 1, "end": 3},
        ]
        ax = DumbbellChart(
            data, show_values=True, value_kind=DUMBBELL_VALUE.DELTA
        ).axes[0]
        start, end = dots(ax)
        self.assertEqual(len(start.get_offsets()), 1)
        self.assertEqual(len(end.get_offsets()), 2)
        self.assertEqual(len(connectors(ax)[0].get_segments()), 1)
        self.assertIn("0", texts(ax))

    def test_marker_and_connector_style_override_theme(self):
        ax = DumbbellChart(
            records(), marker=("s", "D"), connector_style=LINE_STYLE.DASHED
        ).axes[0]
        start, end = dots(ax)
        self.assertFalse(
            np.allclose(start.get_paths()[0].vertices, end.get_paths()[0].vertices)
        )
        _, dashes = connectors(ax)[0].get_linestyle()[0]
        self.assertIsNotNone(dashes)

    def test_chart_style_marker_wins_over_setting(self):
        ax = DumbbellChart(
            records(),
            marker=("s", "s"),
            style={
                "plot_dumbbell_start_marker": "o",
                "plot_dumbbell_end_marker": "o",
            },
        ).axes[0]
        start, end = dots(ax)
        np.testing.assert_allclose(
            start.get_paths()[0].vertices, end.get_paths()[0].vertices
        )

    def test_every_theme_renders(self):
        for theme in THEMES:
            with self.subTest(theme=theme):
                config.set_theme(theme)
                figure = DumbbellChart(
                    records(),
                    start_name="Before",
                    end_name="After",
                    show_values=True,
                    value_kind=DUMBBELL_VALUE.ENDPOINTS,
                )
                figure.canvas.draw()
                self.assertEqual(len(dots(figure.axes[0])), 2)
                plt.close(figure)


def gridlines(ax, axis):
    lines = ax.xaxis.get_gridlines() if axis == "x" else ax.yaxis.get_gridlines()
    return any(line.get_visible() for line in lines)


def arrows(ax):
    return [t for t in ax.texts if t.arrow_patch is not None and not t.get_text()]


class TestDumbbellGrid(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_horizontal_grid_runs_along_the_values(self):
        ax = DumbbellChart(records()).axes[0]
        self.assertTrue(gridlines(ax, "x"))
        self.assertFalse(gridlines(ax, "y"))

    def test_vertical_grid_runs_along_the_values(self):
        ax = DumbbellChart(records(), orientation=ORIENTATION.VERTICAL).axes[0]
        self.assertTrue(gridlines(ax, "y"))
        self.assertFalse(gridlines(ax, "x"))

    def test_explicit_grid_is_literal(self):
        ax = DumbbellChart(records(), show_grid="y").axes[0]
        self.assertTrue(gridlines(ax, "y"))
        self.assertFalse(gridlines(ax, "x"))

    def test_minor_gridlines_split_each_value_step(self):
        ax = DumbbellChart(records()).axes[0]
        ax.figure.canvas.draw()
        majors = ax.xaxis.get_majorticklocs()
        minors = ax.xaxis.get_minorticklocs()
        step = majors[1] - majors[0]
        # one fainter line halfway between each pair of labelled values
        self.assertAlmostEqual((minors[0] - majors[0]) % step, step / 2)
        self.assertTrue(ax.xaxis.get_minor_ticks()[0].gridline.get_visible())
        self.assertEqual(ax.yaxis.get_minorticklocs().size, 0)

    def test_minor_gridlines_off_by_style(self):
        ax = DumbbellChart(records(), style={"plot_dumbbell_grid_minor": 0}).axes[0]
        self.assertEqual(ax.xaxis.get_minorticklocs().size, 0)

    def test_no_minor_gridlines_without_the_value_grid(self):
        ax = DumbbellChart(records(), show_grid="y").axes[0]
        self.assertEqual(ax.xaxis.get_minorticklocs().size, 0)

    def test_panel_grid_runs_along_the_values(self):
        ax = Panel([DumbbellChart(records())]).axes[0]
        self.assertTrue(gridlines(ax, "x"))
        self.assertFalse(gridlines(ax, "y"))


class TestDumbbellDirection(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_no_arrows_by_default(self):
        self.assertEqual(arrows(DumbbellChart(records()).axes[0]), [])

    def test_one_arrow_per_distinct_record_pointing_to_the_end(self):
        data = records() + [{"label": "D", "start": 2, "end": 2}]
        ax = DumbbellChart(data, show_direction=True).axes[0]
        found = arrows(ax)
        self.assertEqual(len(found), 3)
        # B falls: its arrow points from 5 down to 4
        self.assertEqual(found[1].xy[0], 4.0)
        self.assertEqual(found[1].xyann[0], 5.0)

    def test_arrow_is_thinner_than_the_connector(self):
        ax = DumbbellChart(records(), show_direction=True).axes[0]
        connector = connectors(ax)[0]
        self.assertLess(
            arrows(ax)[0].arrow_patch.get_linewidth(), connector.get_linewidth()[0]
        )

    def test_vertical_arrows_follow_the_values(self):
        ax = DumbbellChart(
            records(), show_direction=True, orientation=ORIENTATION.VERTICAL
        ).axes[0]
        first = arrows(ax)[0]
        self.assertEqual((first.xyann[1], first.xy[1]), (3.0, 7.0))

    def test_arrow_style_override(self):
        ax = DumbbellChart(
            records(),
            show_direction=True,
            style={"plot_dumbbell_arrow_color": "#123456"},
        ).axes[0]
        self.assertEqual(to_hex(arrows(ax)[0].arrow_patch.get_edgecolor()), "#123456")


class TestDumbbellLabelsAndLegend(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_endpoint_values(self):
        ax = DumbbellChart(
            records(),
            show_values=True,
            value_kind=DUMBBELL_VALUE.ENDPOINTS,
            value_format="{:.0f}",
        ).axes[0]
        self.assertEqual(sorted(texts(ax)), sorted(["3", "7", "5", "4", "1", "9"]))

    def test_endpoint_labels_point_away_from_connector(self):
        ax = DumbbellChart(
            [{"label": "A", "start": 3, "end": 7}],
            show_values=True,
            value_kind=DUMBBELL_VALUE.ENDPOINTS,
            value_format="{:.0f}",
        ).axes[0]
        by_text = {t.get_text(): t for t in ax.texts}
        self.assertEqual(by_text["3"].get_ha(), "right")
        self.assertEqual(by_text["7"].get_ha(), "left")

    def test_delta_values(self):
        ax = DumbbellChart(
            records(),
            show_values=True,
            value_kind=DUMBBELL_VALUE.DELTA,
            value_format="{:+.0f}",
        ).axes[0]
        self.assertEqual(texts(ax), ["+4", "-1", "+8"])

    def test_no_values_by_default(self):
        self.assertEqual(texts(DumbbellChart(records()).axes[0]), [])

    def test_legend_names_the_endpoints(self):
        ax = DumbbellChart(records(), start_name="2010", end_name="2020").axes[0]
        legend = ax.get_legend()
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["2010", "2020"])

    def test_unnamed_dots_hover_under_the_series(self):
        figure = DumbbellChart(records(), subtitle="Life")
        labels = [resolve(0)["label"] for _, resolve in figure._hover_targets]
        self.assertEqual(labels, ["Life", "Life"])

    def test_no_legend_without_names(self):
        self.assertIsNone(DumbbellChart(records()).axes[0].get_legend())


class TestDumbbellEmphasis(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_record_emphasis_mutes_its_dots(self):
        data = records()
        data[1]["emphasis"] = EMPHASIS.BACKGROUND
        ax = DumbbellChart(data, start_name="a", end_name="b").axes[0]
        muted = [c for c in dots(ax) if len(c.get_offsets()) == 1]
        self.assertEqual(len(muted), 2)
        muted_color = to_hex(config.get("muted_color"))
        for collection in muted:
            self.assertEqual(to_hex(collection.get_facecolor()[0]), muted_color)
        # muted dots add no legend entries
        self.assertEqual(len(ax.get_legend().get_texts()), 2)

    def test_emphasis_rule_reads_the_delta(self):
        ax = DumbbellChart(records(), emphasis_rule={"top": 1}).axes[0]
        highlighted = [c for c in dots(ax) if len(c.get_offsets()) == 1]
        # C (delta 8) is highlighted; A and B are muted together
        self.assertEqual(len(highlighted), 2)
        np.testing.assert_allclose(highlighted[0].get_offsets(), [[1, 2]])

    def test_record_role_wins_over_rule(self):
        data = records()
        data[0]["emphasis"] = EMPHASIS.HIGHLIGHT
        ax = DumbbellChart(data, emphasis_rule={"top": 1}).axes[0]
        highlighted = [c for c in dots(ax) if len(c.get_offsets()) == 2]
        self.assertEqual(len(highlighted), 2)

    def test_background_chart_draws_muted(self):
        ax = DumbbellChart(records(), emphasis=EMPHASIS.BACKGROUND).axes[0]
        muted_color = to_hex(config.get("muted_color"))
        for collection in dots(ax):
            self.assertEqual(to_hex(collection.get_facecolor()[0]), muted_color)


class TestDumbbellComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_metadata_transport(self):
        figure = DumbbellChart(records())
        self.assertEqual(figure._chart_metadata["type"], "dumbbellchart")

    def test_two_layers_overlay_in_cycle_colors(self):
        other = [
            {"label": "C", "start": 2, "end": 6},
            {"label": "D", "start": 0, "end": 1},
        ]
        figure = DumbbellChart([records(), other], subtitle=["one", "two"])
        ax = figure.axes[0]
        self.assertEqual(category_labels(ax), ["A", "B", "C", "D"])
        ends = dots(ax)[1::2]
        self.assertNotEqual(
            to_hex(ends[0].get_facecolor()[0]), to_hex(ends[1].get_facecolor()[0])
        )

    def test_subplots(self):
        figure = DumbbellChart([records(), records()], subplots=True)
        self.assertEqual(len([ax for ax in figure.axes if ax.axison]), 2)

    def test_panel_of_two_dumbbells(self):
        other = [
            {"label": "C", "start": 2, "end": 6},
            {"label": "D", "start": 0, "end": 1},
        ]
        figure = Panel(
            [
                DumbbellChart(records(), subtitle="one"),
                DumbbellChart(other, subtitle="two"),
            ]
        )
        ax = figure.axes[0]
        self.assertEqual(category_labels(ax), ["A", "B", "C", "D"])
        self.assertEqual(len(dots(ax)), 4)

    def test_panel_with_box_plot_shares_categories(self):
        boxes = [{"label": lbl, "value": v} for lbl in "AB" for v in (1, 2, 3, 4)]
        figure = Panel(
            [
                BoxPlot(boxes, orientation=ORIENTATION.HORIZONTAL),
                DumbbellChart(records()),
            ]
        )
        self.assertEqual(category_labels(figure.axes[0]), ["A", "B", "C"])

    def test_grid_cell(self):
        figure = Grid([[DumbbellChart(records()), DumbbellChart(records())]])
        drawn = [ax for ax in figure.axes if dots(ax)]
        self.assertEqual(len(drawn), 2)


if __name__ == "__main__":
    unittest.main()


class TestSharedSortOrder(unittest.TestCase):
    """Subplots sharing the category axis take the first one's order (#187)."""

    def tearDown(self):
        plt.close("all")

    def test_sharey_sort_follows_the_first_subplot(self):
        second = [
            {"label": "A", "start": 0.0, "end": 1.0},
            {"label": "B", "start": 0.0, "end": 9.0},
            {"label": "C", "start": 0.0, "end": 5.0},
        ]
        figure = DumbbellChart(
            data=[records(), second],
            subplots=True,
            sharey=True,
            sort="descending",
            sort_by="end",
        )
        figure.canvas.draw()
        # the first subplot sorts C (9), A (7), B (4); the shared labels are its
        self.assertEqual(category_labels(figure.axes[0]), ["C", "A", "B"])
        # the second subplot draws its rows in that order: C, A, B
        offsets = dots(figure.axes[1])[-1].get_offsets()
        self.assertEqual(offsets[:, 0].tolist(), [5.0, 1.0, 9.0])
        self.assertEqual(offsets[:, 1].tolist(), [0.0, 1.0, 2.0])
