"""Tests for text annotations and the Annotate front (ADR 0018)."""

import unittest
from datetime import date, timedelta

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import (
    BarChart,
    CalendarHeatmap,
    Heatmap,
    LineChart,
    RadialChart,
    ScatterChart,
)
from datachart.config import config
from datachart.constants import THEME
from datachart.utils import Annotate, Grid, Panel
from datachart.utils._internal.chart_builder import build_charts_structure
from datachart.utils._internal.config_helpers import TEXT_ARROW_TARGET_GAP

LINE1 = [{"x": i, "y": i**2} for i in range(10)]
LINE2 = [{"x": i, "y": 3 * i} for i in range(10)]
LINE3 = [{"x": i, "y": 50 - 2 * i} for i in range(10)]
BAR1 = [{"label": c, "y": v} for c, v in zip("ABC", [3.0, 5.0, 4.0])]
NOTE = {"text": "note", "x": 2, "y": 40, "target": (5, 25)}


def annotation_texts(figure, content):
    return [t for ax in figure.axes for t in ax.texts if t.get_text() == content]


def annotation_texts_on(ax, content):
    return [t for t in ax.texts if t.get_text() == content]


class TestTextsParameter(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_single_chart_draws_text(self):
        figure = LineChart(LINE1, texts=NOTE)
        (text,) = annotation_texts(figure, "note")
        self.assertEqual(text.get_fontsize(), config["plot_text_size"])
        self.assertIsNotNone(text.get_bbox_patch())

    def test_text_requires_position(self):
        with self.assertWarns(UserWarning):
            figure = LineChart(LINE1, texts={"text": "nowhere"})
        self.assertEqual(annotation_texts(figure, "nowhere"), [])

    def test_invalid_coords_raises(self):
        with self.assertRaises(ValueError):
            LineChart(LINE1, texts={"text": "bad", "x": 1, "y": 1, "coords": "figure"})

    def test_axes_coords_place_by_fraction(self):
        figure = LineChart(
            LINE1, texts={"text": "corner", "x": 0.5, "y": 0.5, "coords": "axes"}
        )
        (text,) = annotation_texts(figure, "corner")
        self.assertEqual(text.get_position(), (0.5, 0.5))

    def test_per_text_style_override(self):
        figure = LineChart(
            LINE1,
            texts={
                "text": "styled",
                "x": 2,
                "y": 40,
                "style": {"plot_text_color": "#FF0000", "plot_text_box_visible": False},
            },
        )
        (text,) = annotation_texts(figure, "styled")
        self.assertEqual(text.get_color(), "#FF0000")
        self.assertIsNone(text.get_bbox_patch())

    def test_builder_list_of_lists_indexes_per_chart(self):
        charts = build_charts_structure(
            "linechart",
            [LINE1, LINE2],
            texts=[
                [NOTE, {"text": "b", "x": 1, "y": 1}],
                {"text": "c", "x": 0, "y": 0},
            ],
        )
        self.assertEqual([t["text"] for t in charts[0]["texts"]], ["note", "b"])
        self.assertEqual(charts[1]["texts"]["text"], "c")

    def test_builder_single_chart_passthrough(self):
        charts = build_charts_structure(
            "linechart", LINE1, texts=[NOTE, {"text": "b", "x": 1, "y": 1}]
        )
        self.assertEqual(len(charts["texts"]), 2)

    def test_texts_index_per_subplot_chart(self):
        figure = LineChart(
            [LINE1, LINE2],
            subplots=True,
            texts=[
                {"text": "first", "x": 1, "y": 1},
                {"text": "second", "x": 1, "y": 1},
            ],
        )
        self.assertEqual(len(annotation_texts(figure, "first")), 1)
        self.assertEqual(len(annotation_texts(figure, "second")), 1)

    def test_texts_survive_panel_and_grid(self):
        figure = LineChart(LINE1, texts=NOTE)
        other = LineChart(LINE2)
        panel = Panel([figure, other])
        self.assertEqual(len(annotation_texts(panel, "note")), 1)
        grid = Grid([figure, other])
        self.assertEqual(len(annotation_texts(grid, "note")), 1)

    def test_bow_side_follows_open_space(self):
        """The default curve flips its bow away from the data when needed."""
        hump = [0.8, 2.4, 6.8, 11.5, 16.2, 20.1, 22.0, 21.4, 16.6, 11.5, 5.9, 1.3]
        data = [{"x": i, "y": v} for i, v in enumerate(hump)]
        # the default clockwise bow would cut through the rising slope here
        figure = LineChart(
            data, texts={"text": "n", "x": 1.2, "y": 14.7, "target": (6, 22.0)}
        )
        (text,) = annotation_texts(figure, "n")
        self.assertLess(text.arrow_patch.get_connectionstyle().rad, 0)

    def test_bow_keeps_the_flattest_clear_arc(self):
        """With open space on both sides, the flattest default bow wins."""
        flat = [{"x": x, "y": 5} for x in range(11)]
        figure = LineChart(flat, texts={"text": "n", "x": 2, "y": 1, "target": (8, 5)})
        (text,) = annotation_texts(figure, "n")
        self.assertEqual(text.arrow_patch.get_connectionstyle().rad, 0.2)

    def test_pinned_curve_opts_out_of_the_bow_choice(self):
        """An explicit plot_text_arrow_curve pins the bow exactly."""
        flat = [{"x": x, "y": 5} for x in range(11)]
        figure = LineChart(
            flat,
            texts={
                "text": "n",
                "x": 2,
                "y": 9,
                "target": (8, 5),
                "style": {"plot_text_arrow_curve": 0.4},
            },
        )
        (text,) = annotation_texts(figure, "n")
        self.assertEqual(text.arrow_patch.get_connectionstyle().rad, 0.4)

    def test_connector_exits_the_facing_side(self):
        """The connector leaves the box from the side facing the target."""
        figure = LineChart(
            LINE1, texts={"text": "n", "x": 1, "y": 60, "target": (8, 64)}
        )
        (text,) = annotation_texts(figure, "n")
        # target to the right: the exit point sits on the right box edge
        self.assertEqual(text.arrowprops["relpos"][0], 1.0)

    def test_short_connector_is_dropped(self):
        """A text sitting on its target draws no connector at all."""
        figure = LineChart(
            LINE1, texts={"text": "n", "x": 5.2, "y": 26, "target": (5, 25)}
        )
        (text,) = annotation_texts(figure, "n")
        self.assertIsNone(text.arrow_patch)

    def test_close_target_keeps_a_straight_stub(self):
        """A target just past the text box still gets a short straight line."""
        figure = LineChart(
            LINE1, texts={"text": "n", "x": 5, "y": 25, "target": (5, 31.5)}
        )
        (text,) = annotation_texts(figure, "n")
        self.assertIsNotNone(text.arrow_patch)
        self.assertEqual(text.arrow_patch.get_connectionstyle().rad, 0.0)

    def test_target_inside_the_box_draws_no_connector(self):
        """A target the text box already covers leaves no room for a line."""
        figure = LineChart(
            LINE1, texts={"text": "n", "x": 5, "y": 25, "target": (5, 30)}
        )
        (text,) = annotation_texts(figure, "n")
        self.assertIsNone(text.arrow_patch)

    def test_texts_render_on_the_topmost_axes(self):
        """In a twin-axis panel, texts land on the twin so nothing covers them."""
        left = LineChart(
            [{"x": x, "y": x} for x in range(5)],
            texts={"text": "note", "x": 1, "y": 2, "target": (3, 3)},
        )
        right = LineChart([{"x": x, "y": x * 100} for x in range(5)])
        panel = Panel(
            [
                {"figure": left, "y_axis": "left"},
                {"figure": right, "y_axis": "right"},
            ]
        )
        ax_left, ax_right = panel.axes[0], panel.axes[1]
        self.assertEqual(annotation_texts_on(ax_left, "note"), [])
        (text,) = annotation_texts_on(ax_right, "note")
        # the position still reads the owning (left) axis data coordinates
        self.assertEqual(text.get_position(), (1, 2))
        self.assertIs(text.xycoords, ax_left.transData)

    def test_theme_styles_the_connector(self):
        config.set_theme(THEME.INK)
        figure = LineChart(LINE1, texts=NOTE)
        (text,) = annotation_texts(figure, "note")
        self.assertEqual(
            matplotlib.colors.to_hex(text.arrow_patch.get_edgecolor()),
            config["plot_text_arrow_color"].lower(),
        )


class TestAnnotate(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_annotate_adds_text(self):
        figure = LineChart(LINE1, texts=NOTE)
        annotated = Annotate(
            figure, {"text": "post", "x": 0.1, "y": 0.9, "coords": "axes"}
        )
        self.assertEqual(len(annotation_texts(annotated, "post")), 1)
        # the source figure's own annotations ride along
        self.assertEqual(len(annotation_texts(annotated, "note")), 1)

    def test_annotate_leaves_the_source_untouched(self):
        figure = LineChart(LINE1)
        panel = figure._chart_metadata["panel"]
        groups_before = list(panel.groups)
        layers_before = list(panel.layers)
        Annotate(figure, NOTE)
        self.assertEqual(panel.groups, groups_before)
        self.assertEqual(panel.layers, layers_before)
        self.assertEqual(annotation_texts(figure, "note"), [])

    def test_annotate_preserves_colors(self):
        """Appending the carrier keeps the chart-hash -> color assignment."""
        figure = LineChart([LINE1, LINE2])
        colors = [line.get_color() for ax in figure.axes for line in ax.lines]
        annotated = Annotate(
            figure, {"text": "n", "x": 0.5, "y": 0.5, "coords": "axes"}
        )
        recolors = [line.get_color() for ax in annotated.axes for line in ax.lines]
        self.assertEqual(colors, recolors)

    def test_annotate_panel_output(self):
        panel = Panel([LineChart(LINE1), BarChart(BAR1)])
        annotated = Annotate(panel, {"text": "p", "x": 0.5, "y": 0.5, "coords": "axes"})
        self.assertEqual(len(annotation_texts(annotated, "p")), 1)

    def test_annotate_output_composes(self):
        annotated = Annotate(LineChart(LINE1), NOTE)
        panel = Panel([annotated, LineChart(LINE2)])
        self.assertEqual(len(annotation_texts(panel, "note")), 1)
        grid = Grid([annotated, LineChart(LINE2)])
        self.assertEqual(len(annotation_texts(grid, "note")), 1)

    def test_carrier_claims_no_color_in_composition(self):
        """A composed annotated figure keeps the unannotated panel's colors."""
        plain = Panel([LineChart(LINE1), LineChart(LINE2)])
        baseline = [line.get_color() for ax in plain.axes for line in ax.lines]
        annotated = Annotate(LineChart(LINE1), NOTE)
        panel = Panel([annotated, LineChart(LINE2)])
        colors = [line.get_color() for ax in panel.axes for line in ax.lines]
        self.assertEqual(colors, baseline)

    def test_annotate_radial_figure(self):
        radial = RadialChart(
            [{"label": c, "y": v} for c, v in zip("NESW", [1, 2, 3, 4])]
        )
        annotated = Annotate(
            radial, {"text": "r", "x": 0.5, "y": 0.5, "coords": "axes"}
        )
        self.assertEqual(len(annotation_texts(annotated, "r")), 1)

    def test_annotate_rejects_grid_figures(self):
        grid = Grid([LineChart(LINE1), LineChart(LINE2)])
        with self.assertRaises(ValueError):
            Annotate(grid, NOTE)

    def test_annotate_rejects_subplot_key_on_single_panel_figure(self):
        with self.assertRaises(ValueError):
            Annotate(LineChart(LINE1), {**NOTE, "subplot": 0})

    def test_annotate_rejects_foreign_figures(self):
        figure = plt.figure()
        with self.assertRaises(ValueError):
            Annotate(figure, NOTE)


class TestAnnotateSubplots(unittest.TestCase):
    """`Annotate` on a multi-subplot figure targets subplots by index (#125)."""

    def setUp(self):
        self.figure = LineChart(
            [LINE1, LINE2, LINE3],
            subplots=True,
            title="Three",
            xlabel="x",
            ylabel="y",
        )

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_text_lands_in_the_targeted_subplot_only(self):
        annotated = Annotate(self.figure, {**NOTE, "subplot": 2})
        self.assertEqual(len(annotated.axes), 3)
        per_axes = [len(annotation_texts_on(ax, "note")) for ax in annotated.axes]
        self.assertEqual(per_axes, [0, 0, 1])

    def test_texts_group_by_subplot(self):
        annotated = Annotate(
            self.figure,
            [
                {**NOTE, "subplot": 0},
                {**NOTE, "text": "other", "subplot": 2},
                {**NOTE, "text": "second", "subplot": 2},
            ],
        )
        first, _, third = annotated.axes
        self.assertEqual(len(annotation_texts_on(first, "note")), 1)
        self.assertEqual(len(annotation_texts_on(third, "other")), 1)
        self.assertEqual(len(annotation_texts_on(third, "second")), 1)

    def test_layout_and_figure_labels_follow_the_source(self):
        annotated = Annotate(self.figure, {**NOTE, "subplot": 1})
        self.assertEqual(annotated.get_suptitle(), "Three")
        self.assertEqual(annotated.get_supxlabel(), "x")
        self.assertEqual(annotated.get_supylabel(), "y")
        self.assertEqual(
            annotated._chart_metadata["shape"], self.figure._chart_metadata["shape"]
        )
        self.assertEqual(
            [ax.get_subplotspec().get_geometry()[:2] for ax in annotated.axes],
            [ax.get_subplotspec().get_geometry()[:2] for ax in self.figure.axes],
        )

    def test_combined_panel_carries_no_subplot_texts(self):
        annotated = Annotate(self.figure, {**NOTE, "subplot": 2})
        metadata = annotated._chart_metadata
        self.assertEqual(metadata["type"], "linechart")
        self.assertFalse(
            any(layer.kind == "text" for layer in metadata["panel"].layers)
        )
        text_layers = [
            [layer for layer in panel.layers if layer.kind == "text"]
            for panel in metadata["panels"]
        ]
        self.assertEqual([len(t) for t in text_layers], [0, 0, 1])

    def test_source_is_untouched(self):
        panels_before = [list(p.layers) for p in self.figure._chart_metadata["panels"]]
        Annotate(self.figure, {**NOTE, "subplot": 2})
        self.assertEqual(
            [list(p.layers) for p in self.figure._chart_metadata["panels"]],
            panels_before,
        )
        self.assertEqual(annotation_texts(self.figure, "note"), [])

    def test_annotated_subplots_survive_grid(self):
        annotated = Annotate(self.figure, {**NOTE, "subplot": 2})
        grid = Grid([annotated, LineChart(LINE2)])
        # the cell rebuilds the three sub-axes plus one for the plain figure
        data_axes = [ax for ax in grid.axes if ax.lines]
        self.assertEqual(len(data_axes), 4)
        (host,) = [ax for ax in grid.axes if annotation_texts_on(ax, "note")]
        # the third sub-axes of the cell draws the third series
        self.assertEqual(
            list(host.lines[0].get_ydata()), [point["y"] for point in LINE3]
        )
        # the source's title and axis labels frame the rebuilt subplots
        texts = [t.get_text() for ax in grid.axes for t in ax.texts]
        for label in ("Three", "x", "y"):
            self.assertIn(label, texts)

    def test_missing_subplot_raises(self):
        with self.assertRaisesRegex(ValueError, "subplot"):
            Annotate(self.figure, NOTE)
        with self.assertRaisesRegex(ValueError, "subplot"):
            Annotate(self.figure, [{**NOTE, "subplot": 0}, NOTE])

    def test_out_of_range_subplot_raises(self):
        for index in (-1, 3):
            with self.subTest(index=index):
                with self.assertRaisesRegex(ValueError, "out of range"):
                    Annotate(self.figure, {**NOTE, "subplot": index})

    def test_non_integer_subplot_raises(self):
        for index in (1.5, True, "2"):
            with self.subTest(index=index):
                with self.assertRaisesRegex(ValueError, "integer index"):
                    Annotate(self.figure, {**NOTE, "subplot": index})


class TestConnectorTargetGap(unittest.TestCase):
    """The connector stops short of its target, but never off the mark (#184)."""

    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    @staticmethod
    def tip_in_data(figure, content):
        figure.canvas.draw()
        ax = figure.axes[0]
        (text,) = annotation_texts_on(ax, content)
        vertices = text.arrow_patch.get_path().vertices
        return ax.transData.inverted().transform(vertices[-1])

    def test_gap_stays_inside_a_small_heatmap_cell(self):
        cells = [[(row * col) % 7 for col in range(40)] for row in range(40)]
        figure = Heatmap(
            {"z": cells},
            texts={
                "text": "n",
                "x": 0.1,
                "y": 0.1,
                "coords": "axes",
                "target": (20, 20),
            },
        )
        x, y = self.tip_in_data(figure, "n")
        # imshow centers cell (20, 20) on (20, 20); its borders sit half a unit out
        self.assertLessEqual(abs(x - 20), 0.5)
        self.assertLessEqual(abs(y - 20), 0.5)

    def test_gap_is_unchanged_without_a_mark_under_the_target(self):
        figure = LineChart(LINE1, texts=NOTE)
        (text,) = annotation_texts(figure, "note")
        self.assertEqual(text.arrowprops["shrinkB"], TEXT_ARROW_TARGET_GAP)

    def test_gap_stays_inside_a_calendar_cell(self):
        days = [date(2024, 1, 1) + timedelta(days=i) for i in range(366)]
        figure = CalendarHeatmap(
            {"date": days, "value": [i % 9 for i in range(366)]},
            year=2024,
            texts={"text": "n", "x": 5, "y": -1.6, "target": (30, 3)},
        )
        x, y = self.tip_in_data(figure, "n")
        self.assertLessEqual(abs(x - 30), 0.5)
        self.assertLessEqual(abs(y - 3), 0.5)

    def test_gap_stops_on_the_scatter_marker_it_names(self):
        data = [{"x": i, "y": i % 5} for i in range(10)]
        figure = ScatterChart(
            data,
            texts={"text": "n", "x": 2, "y": 4, "target": (5, 0)},
            style={"plot_scatter_size": 16},
        )
        (text,) = annotation_texts(figure, "n")
        # a 16 pt² marker is 2 pt across its radius, under the 5 pt gap
        self.assertEqual(text.arrowprops["shrinkB"], 2.0)


if __name__ == "__main__":
    unittest.main()
