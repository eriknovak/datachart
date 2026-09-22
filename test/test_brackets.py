"""Tests for pairwise comparison brackets (ADR 0059): `brackets` on the reference seam."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from datachart import typings
from datachart.charts import (
    BarChart,
    BoxPlot,
    BumpChart,
    ContourChart,
    DumbbellChart,
    HexbinChart,
    Histogram,
    LineChart,
    PyramidChart,
    RadialChart,
    RaincloudPlot,
    RidgelinePlot,
    ScatterChart,
    StackedAreaChart,
    SwarmPlot,
    ViolinPlot,
)
from datachart.config import config
from datachart import themes
from datachart.utils import Grid, Panel
from datachart.utils._internal.config_helpers import get_bracket_style, get_bracket_tick
from datachart.utils._internal.layers import (
    BRACKET_GAP,
    BRACKET_STEP,
    REF_LINE_ZORDER,
)

LINE = [{"x": i, "y": i * 2} for i in range(6)]
BAR = [{"label": c, "y": v} for c, v in zip("ABCD", [3, 5, 4, 6])]
WIND = [{"label": d, "y": v} for d, v in zip(["N", "E", "S", "W"], [3, 5, 4, 6])]
GROUPS = [{"label": g, "value": float(v)} for g in "AB" for v in range(6)]
SPANS = [{"label": "A", "start": 1, "end": 3}, {"label": "B", "start": 2, "end": 5}]
# every group tops out at 10 and bottoms at 0: one data range for the stack
EVEN = [{"label": g, "value": float(v)} for g in "ABCD" for v in (0, 2, 4, 6, 8, 10)]
# B tops the A-B span at 20, C alone reaches 100
UNEVEN = [
    {"label": g, "value": float(v)}
    for g, top in (("A", 10), ("B", 20), ("C", 100))
    for v in (0, top / 2, top)
]
BRACKET_KEYS = ("color", "width", "tick", "alpha")
LINE_KEYS = ("color", "width", "alpha")
PREDEFINED_THEMES = {
    name: getattr(themes, name) for name in themes.__all__ if name.endswith("_THEME")
}
# the even data: range 10, so the gap and the stack step in data units
EVEN_GAP = 10 * BRACKET_GAP
EVEN_STEP = 10 * BRACKET_STEP


def bracket_lines(ax):
    """The bracket paths of an axes: a tick, the span, a tick, on the reference rung."""

    return [
        line
        for line in ax.lines
        if line.get_zorder() == REF_LINE_ZORDER and len(line.get_xdata()) == 4
    ]


def span_of(line, horizontal=False):
    """The (start, end) category positions a bracket spans."""

    data = line.get_ydata() if horizontal else line.get_xdata()
    return (data[1], data[2])


def value_of(line, horizontal=False):
    """The value-axis position of a bracket's span."""

    data = line.get_xdata() if horizontal else line.get_ydata()
    return data[1]


def tick_points(line, ax, horizontal=False):
    """The length of a bracket's end tick, in points."""

    points = ax.transData.transform(list(zip(line.get_xdata(), line.get_ydata())))
    axis = 0 if horizontal else 1
    return abs(points[1][axis] - points[0][axis]) / (ax.figure.dpi / 72)


def bracket_texts(ax):
    return [text for text in ax.texts if text.get_zorder() == REF_LINE_ZORDER]


class TestTypingsAndThemes(unittest.TestCase):
    def test_typings_exported(self):
        for name in ("BracketSettingAttrs", "BracketStyleAttrs"):
            self.assertTrue(hasattr(typings, name))
        self.assertEqual(
            set(typings.BracketSettingAttrs.__annotations__),
            {"from", "to", "text", "y", "style"},
        )
        self.assertEqual(
            set(typings.BracketStyleAttrs.__annotations__),
            {f"plot_bracket_{key}" for key in BRACKET_KEYS},
        )

    def test_theme_keys_in_every_theme(self):
        for theme_name, theme in PREDEFINED_THEMES.items():
            for key in BRACKET_KEYS:
                self.assertIn(f"plot_bracket_{key}", theme, theme_name)

    def test_every_theme_styles_the_bracket_as_its_horizontal_line(self):
        for theme_name, theme in PREDEFINED_THEMES.items():
            for key in LINE_KEYS:
                self.assertEqual(
                    theme[f"plot_bracket_{key}"], theme[f"plot_hline_{key}"], theme_name
                )

    def test_a_derived_theme_carries_the_keys(self):
        derived = themes.derive_theme(themes.MINIMAL_THEME, lead="Greens")
        for key in BRACKET_KEYS:
            self.assertIn(f"plot_bracket_{key}", derived)


class TestStyleResolver(unittest.TestCase):
    def tearDown(self):
        config.reset_config()

    def test_defaults(self):
        style = get_bracket_style({})
        # an unset color falls to the reference color the diagonal takes
        self.assertNotIn("color", style)
        self.assertEqual(style["alpha"], config["plot_hline_alpha"])
        self.assertEqual(style["linewidth"], config["plot_hline_width"])
        self.assertEqual(get_bracket_tick({}), config["plot_bracket_tick"])

    def test_overrides(self):
        style = {
            "plot_bracket_color": "#FF0000",
            "plot_bracket_width": 3,
            "plot_bracket_alpha": 0.2,
            "plot_bracket_tick": 9,
        }
        resolved = get_bracket_style(style)
        self.assertEqual(resolved["color"], "#FF0000")
        self.assertEqual(resolved["linewidth"], 3)
        self.assertEqual(resolved["alpha"], 0.2)
        self.assertEqual(get_bracket_tick(style), 9)


class TestValidation(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_an_empty_bracket_names_both_endpoints(self):
        with pytest.raises(ValueError) as error:
            BoxPlot(data=GROUPS, brackets={})
        self.assertIn("`from`", str(error.value))
        self.assertIn("`to`", str(error.value))

    def test_a_half_declared_bracket_raises(self):
        with pytest.raises(ValueError, match="`to`"):
            BoxPlot(data=GROUPS, brackets={"from": "A"})

    def test_an_unknown_label_names_the_chart_labels(self):
        with pytest.raises(ValueError) as error:
            BoxPlot(data=GROUPS, brackets={"from": "A", "to": "Z"})
        self.assertIn("'Z'", str(error.value))
        self.assertIn("'B'", str(error.value))


class TestGeometry(unittest.TestCase):
    def tearDown(self):
        config.reset_config()
        plt.close("all")

    def test_the_path_is_a_tick_the_span_and_a_tick(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "C"})
        ax = figure.axes[0]
        (line,) = bracket_lines(ax)
        self.assertEqual(span_of(line), (0, 2))
        xs, ys = list(line.get_xdata()), list(line.get_ydata())
        self.assertEqual(xs, [0, 0, 2, 2])
        # the ticks point down, toward the data they bracket
        self.assertLess(ys[0], ys[1])
        self.assertEqual(ys[1], ys[2])
        self.assertLess(ys[3], ys[2])

    def test_the_tick_is_the_theme_length_in_points(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B"})
        ax = figure.axes[0]
        (line,) = bracket_lines(ax)
        self.assertAlmostEqual(
            tick_points(line, ax), config["plot_bracket_tick"], places=4
        )

    def test_the_tick_holds_its_length_on_a_log_axis(self):
        figure = BoxPlot(
            data=[
                {"label": g, "value": float(v)}
                for g, top in (("A", 10), ("B", 10000))
                for v in (1, top)
            ],
            scaley="log",
            brackets={"from": "A", "to": "B"},
        )
        ax = figure.axes[0]
        (line,) = bracket_lines(ax)
        self.assertAlmostEqual(
            tick_points(line, ax), config["plot_bracket_tick"], places=4
        )

    def test_a_per_bracket_tick_length_overrides_the_theme(self):
        figure = BoxPlot(
            data=EVEN,
            brackets={"from": "A", "to": "B", "style": {"plot_bracket_tick": 12}},
        )
        ax = figure.axes[0]
        (line,) = bracket_lines(ax)
        self.assertAlmostEqual(tick_points(line, ax), 12, places=4)

    def test_the_line_sits_above_the_marks(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B"})
        ax = figure.axes[0]
        (line,) = bracket_lines(ax)
        self.assertEqual(line.get_zorder(), REF_LINE_ZORDER)

    def test_a_bracket_takes_no_legend_entry(self):
        figure = BoxPlot(
            data=EVEN,
            subtitle="series",
            brackets={"from": "A", "to": "B", "text": "p < .05"},
            show_legend=True,
        )
        labels = [t.get_text() for t in figure.axes[0].get_legend().get_texts()]
        self.assertEqual(labels, ["series"])

    def test_a_bracket_registers_no_hover_target(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B", "text": "ns"})
        plain = BoxPlot(data=EVEN)
        self.assertEqual(
            len(figure._hover_targets or []), len(plain._hover_targets or [])
        )

    def test_per_bracket_style_overrides_the_theme(self):
        figure = BoxPlot(
            data=EVEN,
            brackets={
                "from": "A",
                "to": "B",
                "style": {"plot_bracket_color": "#123456", "plot_bracket_width": 4},
            },
        )
        (line,) = bracket_lines(figure.axes[0])
        self.assertEqual(line.get_color(), "#123456")
        self.assertEqual(line.get_linewidth(), 4)

    def test_a_null_style_falls_back_to_the_theme(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B", "style": None})
        (line,) = bracket_lines(figure.axes[0])
        self.assertEqual(line.get_alpha(), config["plot_bracket_alpha"])

    def test_a_list_of_brackets(self):
        figure = BoxPlot(
            data=EVEN,
            brackets=[{"from": "A", "to": "B"}, {"from": "C", "to": "D"}],
        )
        self.assertEqual(len(bracket_lines(figure.axes[0])), 2)


class TestText(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_the_text_sits_centred_above_the_span(self):
        figure = BoxPlot(
            data=EVEN, brackets={"from": "A", "to": "C", "text": "p = .01"}
        )
        ax = figure.axes[0]
        (line,) = bracket_lines(ax)
        (text,) = bracket_texts(ax)
        self.assertEqual(text.get_text(), "p = .01")
        self.assertEqual(text.xy, (1.0, value_of(line)))
        self.assertEqual(text.get_ha(), "center")
        self.assertEqual(text.get_va(), "bottom")

    def test_the_text_takes_the_bracket_color(self):
        figure = BoxPlot(
            data=EVEN,
            brackets={
                "from": "A",
                "to": "B",
                "text": "*",
                "style": {"plot_bracket_color": "#AA0000"},
            },
        )
        (text,) = bracket_texts(figure.axes[0])
        self.assertEqual(text.get_color(), "#AA0000")

    def test_the_text_takes_the_text_font_size(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B", "text": "*"})
        (text,) = bracket_texts(figure.axes[0])
        self.assertEqual(text.get_fontsize(), config["plot_text_size"])

    def test_a_bracket_without_text_draws_the_line_alone(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B"})
        ax = figure.axes[0]
        self.assertEqual(len(bracket_lines(ax)), 1)
        self.assertEqual(bracket_texts(ax), [])


class TestPlacement(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_an_explicit_value_pins_the_bracket(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B", "y": 42})
        (line,) = bracket_lines(figure.axes[0])
        self.assertEqual(value_of(line), 42)

    def test_a_bracket_sits_a_gap_above_the_data_in_its_span(self):
        figure = BoxPlot(data=UNEVEN, brackets={"from": "A", "to": "B"})
        (line,) = bracket_lines(figure.axes[0])
        # the span tops out at B's 20, and the data range is C's 100
        self.assertAlmostEqual(value_of(line), 20 + 100 * BRACKET_GAP)

    def test_overlapping_brackets_stack_one_step_apart(self):
        figure = BoxPlot(
            data=EVEN,
            brackets=[
                {"from": "A", "to": "B"},
                {"from": "B", "to": "C"},
                {"from": "A", "to": "C"},
            ],
        )
        values = [value_of(line) for line in bracket_lines(figure.axes[0])]
        self.assertAlmostEqual(values[0], 10 + EVEN_GAP)
        self.assertAlmostEqual(values[1], 10 + EVEN_GAP + EVEN_STEP)
        self.assertAlmostEqual(values[2], 10 + EVEN_GAP + 2 * EVEN_STEP)

    def test_brackets_over_separate_spans_share_a_row(self):
        figure = BoxPlot(
            data=EVEN,
            brackets=[{"from": "A", "to": "B"}, {"from": "C", "to": "D"}],
        )
        values = [value_of(line) for line in bracket_lines(figure.axes[0])]
        self.assertAlmostEqual(values[0], values[1])

    def test_the_value_axis_grows_to_fit_the_stack(self):
        figure = BoxPlot(
            data=EVEN,
            brackets=[
                {"from": "A", "to": "B", "text": "p < .001"},
                {"from": "A", "to": "C", "text": "p < .01"},
            ],
        )
        ax = figure.axes[0]
        top = max(value_of(line) for line in bracket_lines(ax))
        self.assertGreater(ax.get_ylim()[1], top)

    def test_a_user_limit_wins_over_the_growth(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B"}, ymax=11)
        self.assertEqual(figure.axes[0].get_ylim()[1], 11)

    def test_a_pinned_bracket_above_the_data_grows_the_axis(self):
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B", "y": 42})
        self.assertGreater(figure.axes[0].get_ylim()[1], 42)

    def test_a_bracket_leaves_the_category_axis_alone(self):
        plain = BoxPlot(data=EVEN)
        limits = plain.axes[0].get_xlim()
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "D", "text": "*"})
        self.assertEqual(figure.axes[0].get_xlim(), limits)

    def test_a_span_clears_only_the_data_inside_it(self):
        # the whole chart reaches 100, the span only 16
        figure = LineChart(
            data=[{"x": i, "y": float(i * i)} for i in range(11)],
            brackets={"from": 1, "to": 4},
        )
        (line,) = bracket_lines(figure.axes[0])
        self.assertAlmostEqual(value_of(line), 16 + 100 * BRACKET_GAP)

    def test_a_pyramid_keeps_the_user_limit_and_its_mirror(self):
        figure = PyramidChart(
            data=[BAR, BAR], xmax=12, brackets={"from": "A", "to": "C"}
        )
        self.assertEqual(figure.axes[0].get_xlim(), (-12, 12))

    def test_a_pyramid_grows_both_ends_of_its_mirror(self):
        figure = PyramidChart(data=[BAR, BAR], brackets={"from": "A", "to": "C"})
        low, high = figure.axes[0].get_xlim()
        self.assertAlmostEqual(low, -high)

    def test_a_pinned_bracket_does_not_shrink_the_axis(self):
        plain = BoxPlot(data=EVEN)
        limit = plain.axes[0].get_ylim()[1]
        figure = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B", "y": 1})
        self.assertGreaterEqual(figure.axes[0].get_ylim()[1], limit)


class TestOrientation(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_a_horizontal_chart_spans_the_vertical_category_axis(self):
        figure = BoxPlot(
            data=EVEN,
            orientation="horizontal",
            brackets={"from": "A", "to": "C", "text": "p = .04"},
        )
        ax = figure.axes[0]
        (line,) = bracket_lines(ax)
        self.assertEqual(span_of(line, horizontal=True), (0, 2))
        xs = list(line.get_xdata())
        # the ticks point left, toward the data they bracket
        self.assertLess(xs[0], xs[1])
        self.assertEqual(xs[1], xs[2])
        (text,) = bracket_texts(ax)
        self.assertEqual(text.xy, (value_of(line, horizontal=True), 1.0))
        self.assertEqual(text.get_ha(), "left")
        self.assertEqual(text.get_va(), "center")

    def test_a_horizontal_chart_grows_the_x_axis(self):
        figure = BoxPlot(
            data=EVEN, orientation="horizontal", brackets={"from": "A", "to": "B"}
        )
        ax = figure.axes[0]
        (line,) = bracket_lines(ax)
        self.assertGreater(ax.get_xlim()[1], value_of(line, horizontal=True))

    def test_a_horizontal_user_limit_wins(self):
        figure = BoxPlot(
            data=EVEN,
            orientation="horizontal",
            brackets={"from": "A", "to": "B"},
            xmax=11,
        )
        self.assertEqual(figure.axes[0].get_xlim()[1], 11)


class TestEndpoints(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_a_bar_chart_resolves_its_labels(self):
        figure = BarChart(data=BAR, brackets={"from": "B", "to": "D", "text": "*"})
        (line,) = bracket_lines(figure.axes[0])
        self.assertEqual(span_of(line), (1, 3))

    def test_a_swarm_plot_resolves_its_labels(self):
        figure = SwarmPlot(data=EVEN, brackets={"from": "B", "to": "D"})
        (line,) = bracket_lines(figure.axes[0])
        self.assertEqual(span_of(line), (1, 3))

    def test_a_ridgeline_plot_resolves_its_labels(self):
        figure = RidgelinePlot(data=EVEN, brackets={"from": "A", "to": "C"})
        (line,) = bracket_lines(figure.axes[0])
        self.assertEqual(span_of(line, horizontal=True), (0, 2))

    def test_numeric_endpoints_are_axis_positions(self):
        figure = LineChart(data=LINE, brackets={"from": 1, "to": 4, "y": 8})
        (line,) = bracket_lines(figure.axes[0])
        self.assertEqual(span_of(line), (1, 4))
        self.assertEqual(value_of(line), 8)

    def test_a_reversed_span_draws_left_to_right(self):
        figure = BarChart(data=BAR, brackets={"from": "D", "to": "B"})
        (line,) = bracket_lines(figure.axes[0])
        self.assertEqual(span_of(line), (1, 3))

    def test_a_sorted_box_plot_follows_the_drawn_order(self):
        figure = BoxPlot(
            data=UNEVEN, sort="descending", brackets={"from": "C", "to": "A"}
        )
        (line,) = bracket_lines(figure.axes[0])
        # descending by median puts C first and A last
        self.assertEqual(span_of(line), (0, 2))


class TestComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_keeps_both_sources_brackets(self):
        first = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B", "text": "one"})
        second = SwarmPlot(data=EVEN, brackets={"from": "C", "to": "D", "text": "two"})
        figure = Panel([first, second])
        ax = figure.axes[0]
        self.assertEqual(len(bracket_lines(ax)), 2)
        self.assertEqual(
            sorted(text.get_text() for text in bracket_texts(ax)), ["one", "two"]
        )

    def test_panel_draws_a_shared_bracket_once(self):
        first = BoxPlot(data=EVEN, brackets={"from": "A", "to": "B"})
        second = SwarmPlot(data=EVEN, brackets={"from": "A", "to": "B"})
        figure = Panel([first, second])
        self.assertEqual(len(bracket_lines(figure.axes[0])), 1)

    def test_grid_redraws_the_bracket_in_its_cell(self):
        figure = Grid(
            [
                [
                    BoxPlot(data=EVEN, brackets={"from": "A", "to": "B"}),
                    BoxPlot(data=EVEN),
                ]
            ]
        )
        self.assertEqual(len(bracket_lines(figure.axes[0])), 1)
        self.assertEqual(len(bracket_lines(figure.axes[1])), 0)


class TestFrontCoverage(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_every_cartesian_front_takes_brackets(self):
        grid = {
            "x": [0, 1, 2],
            "y": [0, 1, 2],
            "z": [[0, 1, 2], [1, 2, 3], [2, 3, 4]],
        }
        cloud = {"x": [float(i) for i in range(12)], "y": [float(i) for i in range(12)]}
        calls = [
            (BarChart, {"data": BAR}),
            (BoxPlot, {"data": GROUPS}),
            (BumpChart, {"data": [[{"x": 0, "y": 1}, {"x": 1, "y": 3}]]}),
            (ContourChart, {"data": grid}),
            (DumbbellChart, {"data": SPANS}),
            (HexbinChart, {"data": cloud}),
            (Histogram, {"data": [{"x": [1, 2, 2, 3, 4]}]}),
            (LineChart, {"data": LINE}),
            (PyramidChart, {"data": [BAR, BAR]}),
            (RaincloudPlot, {"data": GROUPS}),
            (RidgelinePlot, {"data": GROUPS}),
            (ScatterChart, {"data": LINE}),
            (StackedAreaChart, {"data": [LINE, LINE]}),
            (SwarmPlot, {"data": GROUPS}),
            (ViolinPlot, {"data": GROUPS}),
        ]
        self.assertEqual(len(calls), 15)
        for front, kwargs in calls:
            figure = front(brackets={"from": 0, "to": 1, "text": "*"}, **kwargs)
            self.assertTrue(
                any(bracket_lines(ax) for ax in figure.axes), front.__name__
            )
            plt.close(figure)

    def test_radial_rejects_brackets(self):
        with pytest.raises(ValueError, match="brackets"):
            RadialChart(data=WIND, brackets={"from": 0, "to": 1})


if __name__ == "__main__":
    unittest.main()
