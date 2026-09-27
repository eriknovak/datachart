"""Invalid inputs raise the library's ValueError at the entry point (#306)."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from datachart.charts import BarChart, LineChart, RadialChart, ViolinPlot
from datachart.utils import Grid, Panel
from datachart.utils.stats import histogram, kde1d, loess

NAN = float("nan")
INF = float("inf")
VALUES = [1, 2, 2, 3, 3, 3, 4, 4, 5.0]


def line_fig(**kwargs):
    return LineChart(data=[{"x": i, "y": i} for i in range(5)], **kwargs)


def bar_fig(**kwargs):
    data = [{"label": "a", "y": 100}, {"label": "b", "y": 200}]
    return BarChart(data=data, **kwargs)


def spec(row, col, rowspan=1, colspan=1):
    return {"row": row, "col": col, "rowspan": rowspan, "colspan": colspan}


class InvalidInputCase(unittest.TestCase):
    def tearDown(self):
        plt.close("all")


class TestBandwidth(InvalidInputCase):
    BAD = (0, -0.5, NAN, INF)

    def test_kde1d_rejects_a_non_positive_or_non_finite_bandwidth(self):
        for bandwidth in self.BAD:
            with self.subTest(bandwidth=bandwidth):
                with self.assertRaisesRegex(ValueError, "`bandwidth`"):
                    kde1d(VALUES, bandwidth=bandwidth)

    def test_violin_rejects_a_non_positive_or_non_finite_bandwidth(self):
        data = [{"label": "g", "value": v} for v in VALUES]
        for bandwidth in self.BAD:
            with self.subTest(bandwidth=bandwidth):
                with self.assertRaisesRegex(ValueError, "`bandwidth`"):
                    ViolinPlot(data, bandwidth=bandwidth)

    def test_a_positive_number_passes(self):
        self.assertEqual(len(kde1d(VALUES, bandwidth=0.5, gridsize=10)), 10)


class TestPanelDicts(InvalidInputCase):
    def test_an_unknown_key_raises_naming_it(self):
        with self.assertRaisesRegex(ValueError, r"'yaxis'.*charts\[0\].*'y_axis'"):
            Panel([{"figure": line_fig(), "yaxis": "right"}, bar_fig()])

    def test_y_axis_outside_left_right_auto_raises(self):
        with self.assertRaisesRegex(ValueError, r"y_axis.*'top'.*'left'"):
            Panel([{"figure": line_fig(), "y_axis": "top"}, bar_fig()])

    def test_a_non_integer_z_order_raises(self):
        for z_order in ("hi", 1.5, True):
            with self.subTest(z_order=z_order):
                with self.assertRaisesRegex(ValueError, r"z_order"):
                    Panel([{"figure": line_fig(), "z_order": z_order}, bar_fig()])

    def test_valid_options_pass(self):
        Panel(
            [
                {"figure": line_fig(), "y_axis": "right", "z_order": np.int64(3)},
                {"figure": bar_fig(), "y_axis": "auto", "legend_label": "bars"},
            ]
        )

    def test_a_non_figure_raises(self):
        with self.assertRaisesRegex(ValueError, r"charts\[0\]\['figure'\]"):
            Panel([{"figure": "x"}])


class TestGridDicts(InvalidInputCase):
    def test_an_unknown_key_raises_naming_it(self):
        with self.assertRaisesRegex(ValueError, r"'row'.*charts\[0\].*'layout_spec'"):
            Grid([{"figure": line_fig(), "row": 0, "col": 0}])

    def test_overlapping_cells_raise_naming_both_indices(self):
        charts = [
            {"figure": line_fig(), "layout_spec": spec(0, 0, colspan=2)},
            {"figure": bar_fig(), "layout_spec": spec(0, 1)},
        ]
        with self.assertRaisesRegex(ValueError, r"charts\[0\].*charts\[1\].*overlap"):
            Grid(charts)

    def test_out_of_range_positions_and_spans_raise(self):
        for key, bad in (("row", -1), ("col", -1), ("rowspan", 0), ("colspan", -2)):
            with self.subTest(key=key):
                layout = {**spec(0, 0), key: bad}
                with self.assertRaisesRegex(ValueError, rf"'{key}'"):
                    Grid([{"figure": line_fig(), "layout_spec": layout}])

    def test_a_non_positive_max_cols_raises(self):
        for max_cols in (0, -1, 1.5):
            with self.subTest(max_cols=max_cols):
                with self.assertRaisesRegex(ValueError, "`max_cols`"):
                    Grid([line_fig(), bar_fig()], max_cols=max_cols)

    def test_a_non_figure_raises(self):
        with self.assertRaisesRegex(ValueError, r"charts\[0\]\['figure'\]"):
            Grid([{"figure": "x", "layout_spec": spec(0, 0)}])

    def test_a_valid_layout_passes(self):
        Grid(
            [
                {"figure": line_fig(), "layout_spec": spec(0, 0, rowspan=2)},
                {"figure": bar_fig(), "layout_spec": spec(0, 1)},
                {"figure": bar_fig(), "layout_spec": spec(1, 1)},
            ]
        )


class TestLegendLocation(InvalidInputCase):
    def test_panel_and_grid_raise_the_same_error(self):
        messages = []
        for front in (Panel, Grid):
            with self.subTest(front=front.__name__):
                with self.assertRaisesRegex(ValueError, "'nowhere'") as caught:
                    front([line_fig(), bar_fig()], legend={"location": "nowhere"})
                messages.append(str(caught.exception))
        self.assertEqual(messages[0], messages[1])


class TestGridLegendSideTags(InvalidInputCase):
    def test_a_twin_axis_cell_tags_its_entries(self):
        panel = Panel(
            [
                {"figure": bar_fig(subtitle="bars"), "y_axis": "left"},
                {"figure": line_fig(subtitle="line"), "y_axis": "right"},
            ]
        )
        figure = Grid([panel, line_fig(subtitle="other")], show_legend=True)
        legends = [ax.get_legend() for ax in figure.axes if ax.get_legend()]
        labels = [t.get_text() for t in legends[-1].get_texts()]
        self.assertEqual(labels, ["bars (L)", "line (R)"])


class TestRadialRequiredY(InvalidInputCase):
    def test_a_record_missing_y_raises_like_bar_chart(self):
        data = [{"label": "a"}, {"label": "b"}]
        with self.assertRaisesRegex(ValueError, r"`data\[0\]` has no `y` key"):
            BarChart(data)
        for mark in ("bar", "line"):
            with self.subTest(mark=mark):
                with self.assertRaisesRegex(ValueError, r"`data\[0\]` has no `y` key"):
                    RadialChart(data, mark=mark)
        with self.assertRaisesRegex(ValueError, r"`data\[1\]\[0\]` has no `y` key"):
            RadialChart([[{"label": "a", "y": 1}], [{"label": "a"}]], show_area=True)

    def test_the_histogram_mark_reads_x(self):
        RadialChart([{"x": v} for v in VALUES], mark="histogram")


class TestStatsNan(unittest.TestCase):
    def test_histogram_raises_on_nan(self):
        with self.assertRaisesRegex(ValueError, "NaN"):
            histogram([1, 2, NAN, 4])

    def test_loess_passes_nan_through(self):
        curve = loess([1, 2, 3, 4, 5, 6], [1, 2, NAN, 4, 5, 6])
        self.assertTrue(all(np.isnan(point["y"]) for point in curve))


if __name__ == "__main__":
    unittest.main()
