"""Tests for diagonal reference lines (ADR 0055): `dlines` on the reference-line seam."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
from matplotlib.lines import AxLine

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
from datachart.utils._internal.config_helpers import get_dline_style
from datachart.utils._internal.layers import REF_LINE_ZORDER

LINE = [{"x": i, "y": i * 2} for i in range(6)]
BAR = [{"label": c, "y": v} for c, v in zip("ABCD", [3, 5, 4, 6])]
WIND = [{"label": d, "y": v} for d, v in zip(["N", "E", "S", "W"], [3, 5, 4, 6])]
GROUPS = [{"label": g, "value": float(v)} for g in "AB" for v in range(6)]
SPANS = [{"label": "A", "start": 1, "end": 3}, {"label": "B", "start": 2, "end": 5}]
DLINE_KEYS = ("color", "style", "width", "alpha")


def ref_lines(ax):
    """The reference lines of an axes: they sit on the reference-line rung."""

    return [line for line in ax.lines if line.get_zorder() == REF_LINE_ZORDER]


class TestTypingsAndThemes(unittest.TestCase):
    def test_typings_exported(self):
        for name in ("DLineSettingAttrs", "DLineStyleAttrs"):
            self.assertTrue(hasattr(typings, name))
        self.assertEqual(
            set(typings.DLineSettingAttrs.__annotations__),
            {"slope", "intercept", "xmin", "xmax", "style", "label"},
        )
        self.assertEqual(
            set(typings.DLineStyleAttrs.__annotations__),
            {f"plot_dline_{key}" for key in DLINE_KEYS},
        )

    def test_theme_keys_in_every_theme(self):
        for theme_name in themes.__all__:
            theme = getattr(themes, theme_name)
            for key in DLINE_KEYS:
                self.assertIn(f"plot_dline_{key}", theme, theme_name)

    def test_base_defaults_follow_the_horizontal_line(self):
        config.reset_config()
        for key in DLINE_KEYS:
            self.assertEqual(config[f"plot_dline_{key}"], config[f"plot_hline_{key}"])


class TestStyleResolver(unittest.TestCase):
    def tearDown(self):
        config.reset_config()

    def test_defaults(self):
        style = get_dline_style({})
        # an unset color falls to matplotlib's own, as the hline's does
        self.assertNotIn("color", style)
        self.assertEqual(style["alpha"], 0.7)
        self.assertEqual(style["linewidth"], 1)

    def test_overrides(self):
        style = get_dline_style(
            {
                "plot_dline_color": "#FF0000",
                "plot_dline_style": "dashed",
                "plot_dline_width": 3,
                "plot_dline_alpha": 0.2,
            }
        )
        self.assertEqual(style["color"], "#FF0000")
        self.assertEqual(style["linestyle"], "dashed")
        self.assertEqual(style["linewidth"], 3)
        self.assertEqual(style["alpha"], 0.2)


class TestGeometry(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_empty_setting_draws_the_parity_line(self):
        figure = LineChart(data=LINE, dlines={})
        (line,) = ref_lines(figure.axes[0])
        self.assertIsInstance(line, AxLine)
        self.assertEqual(line.get_slope(), 1)
        self.assertEqual(line.get_xy1(), (0, 0))

    def test_unbounded_line_is_an_axline(self):
        figure = LineChart(data=LINE, dlines={"slope": 2, "intercept": 1})
        (line,) = ref_lines(figure.axes[0])
        self.assertIsInstance(line, AxLine)
        self.assertEqual(line.get_slope(), 2)
        self.assertEqual(line.get_xy1(), (0, 1))

    def test_bounded_line_is_a_segment(self):
        figure = LineChart(
            data=LINE, dlines={"slope": 2, "intercept": 1, "xmin": 1, "xmax": 3}
        )
        (line,) = ref_lines(figure.axes[0])
        self.assertNotIsInstance(line, AxLine)
        self.assertEqual(list(line.get_xdata()), [1, 3])
        self.assertEqual(list(line.get_ydata()), [3, 7])

    def test_open_upper_bound_runs_to_the_axis_limit(self):
        figure = LineChart(data=LINE, dlines={"xmin": 2})
        ax = figure.axes[0]
        (line,) = ref_lines(ax)
        xdata = list(line.get_xdata())
        self.assertEqual(xdata[0], 2)
        self.assertAlmostEqual(xdata[1], ax.get_xlim()[1])
        self.assertAlmostEqual(list(line.get_ydata())[1], xdata[1])

    def test_open_lower_bound_runs_to_the_axis_limit(self):
        figure = LineChart(data=LINE, dlines={"xmax": 3, "slope": 0.5, "intercept": 2})
        ax = figure.axes[0]
        (line,) = ref_lines(ax)
        xdata = list(line.get_xdata())
        self.assertAlmostEqual(xdata[0], ax.get_xlim()[0])
        self.assertEqual(xdata[1], 3)
        self.assertAlmostEqual(list(line.get_ydata())[0], 0.5 * xdata[0] + 2)

    def test_a_segment_does_not_widen_the_axes(self):
        plain = LineChart(data=LINE)
        limits = (plain.axes[0].get_xlim(), plain.axes[0].get_ylim())
        figure = LineChart(data=LINE, dlines={"intercept": 40, "xmin": 0, "xmax": 50})
        ax = figure.axes[0]
        self.assertEqual((ax.get_xlim(), ax.get_ylim()), limits)

    def test_list_of_lines(self):
        figure = LineChart(data=LINE, dlines=[{}, {"slope": -1, "intercept": 10}])
        self.assertEqual(len(ref_lines(figure.axes[0])), 2)


class TestStyleAndLegend(unittest.TestCase):
    def tearDown(self):
        config.reset_config()
        plt.close("all")

    def test_label_reaches_the_legend(self):
        figure = LineChart(data=LINE, dlines={"label": "parity"}, show_legend=True)
        ax = figure.axes[0]
        self.assertIn("parity", [t.get_text() for t in ax.get_legend().get_texts()])

    def test_an_unlabelled_line_takes_no_legend_entry(self):
        figure = LineChart(data=LINE, subtitle="series", dlines={}, show_legend=True)
        ax = figure.axes[0]
        labels = [t.get_text() for t in ax.get_legend().get_texts()]
        self.assertEqual(labels, ["series"])

    def test_per_line_style_overrides_the_theme(self):
        figure = LineChart(
            data=LINE,
            dlines={"style": {"plot_dline_color": "#123456", "plot_dline_width": 4}},
        )
        (line,) = ref_lines(figure.axes[0])
        self.assertEqual(line.get_color(), "#123456")
        self.assertEqual(line.get_linewidth(), 4)

    def test_line_sits_above_the_marks(self):
        figure = LineChart(data=LINE, dlines={})
        ax = figure.axes[0]
        (line,) = ref_lines(ax)
        series = [l for l in ax.lines if l is not line]
        self.assertGreater(line.get_zorder(), max(s.get_zorder() for s in series))


class TestComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_draws_a_shared_line_once(self):
        first = ScatterChart(data=LINE, dlines={"label": "parity"})
        second = ScatterChart(data=LINE, dlines={"label": "parity"})
        figure = Panel([first, second])
        self.assertEqual(len(ref_lines(figure.axes[0])), 1)

    def test_panel_keeps_both_sources_lines(self):
        first = ScatterChart(data=LINE, dlines={"slope": 1})
        second = ScatterChart(data=LINE, dlines={"slope": 2})
        figure = Panel([first, second])
        self.assertEqual(len(ref_lines(figure.axes[0])), 2)

    def test_grid_redraws_the_line_in_its_cell(self):
        figure = Grid([[LineChart(data=LINE, dlines={}), LineChart(data=LINE)]])
        self.assertEqual(len(ref_lines(figure.axes[0])), 1)
        self.assertEqual(len(ref_lines(figure.axes[1])), 0)


class TestFrontCoverage(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_every_cartesian_front_takes_dlines(self):
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
            figure = front(dlines={}, **kwargs)
            self.assertTrue(any(ref_lines(ax) for ax in figure.axes), front.__name__)
            plt.close(figure)

    def test_radial_rejects_dlines(self):
        with pytest.raises(ValueError, match="dlines"):
            RadialChart(data=WIND, dlines={})


if __name__ == "__main__":
    unittest.main()
