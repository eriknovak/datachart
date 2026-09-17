"""Shared axes hold the data of every axes that shares them."""

import unittest

from datachart.charts import BarChart, BoxPlot, LineChart, ScatterChart
from datachart.utils import Grid

LOW = [1, 2, 5]
WIDE = [-5, 20, 50]


def _points(values, start=0):
    return [{"x": start + i, "y": v} for i, v in enumerate(values)]


def _assert_holds_data(case, figure):
    figure.canvas.draw()
    for ax in figure.axes:
        if not ax.axison or not ax.has_data():
            continue
        for lim, data in (
            (ax.get_xlim(), ax.dataLim.intervalx),
            (ax.get_ylim(), ax.dataLim.intervaly),
        ):
            lo, hi = sorted(lim)
            case.assertLess(lo, hi)
            case.assertLessEqual(lo, data[0] + 1e-9)
            case.assertGreaterEqual(hi, data[1] - 1e-9)


class TestSharedSubplots(unittest.TestCase):
    def test_sharey_spans_every_subplot(self):
        fig = LineChart(data=[_points(LOW), _points(WIDE)], subplots=True, sharey=True)
        _assert_holds_data(self, fig)
        self.assertEqual(fig.axes[0].get_ylim(), fig.axes[1].get_ylim())

    def test_sharey_crosses_zero_when_one_subplot_does(self):
        """One subplot all positive, one all negative: one axis holds both."""
        fig = LineChart(
            data=[_points([1, 5]), _points([-5, -2])], subplots=True, sharey=True
        )
        lo, hi = fig.axes[0].get_ylim()
        self.assertLessEqual(lo, -5)
        self.assertGreaterEqual(hi, 5)

    def test_sharex_spans_every_line_subplot(self):
        fig = LineChart(
            data=[_points(LOW), _points(WIDE, start=10)], subplots=True, sharex=True
        )
        self.assertEqual(fig.axes[0].get_xlim(), (0.0, 12.0))

    def test_other_kinds_hold_every_subplot(self):
        groups = [
            [{"label": "g", "value": v} for v in values] for values in (LOW, WIDE)
        ]
        bars = [
            [{"label": f"c{i}", "y": v} for i, v in enumerate(values)]
            for values in (LOW, WIDE)
        ]
        for fig in (
            ScatterChart(
                data=[_points(LOW), _points(WIDE, start=10)],
                subplots=True,
                sharex=True,
                sharey=True,
            ),
            BarChart(data=bars, subplots=True, sharey=True),
            BoxPlot(data=groups, subplots=True, sharey=True),
        ):
            with self.subTest(figure=fig._chart_metadata["type"]):
                _assert_holds_data(self, fig)


class TestSharedGrid(unittest.TestCase):
    def test_grid_sharey_spans_every_cell(self):
        small = LineChart(data=_points([0, 1]))
        large = LineChart(data=_points([0, 10]))
        fig = Grid([small, large], sharey=True)
        _assert_holds_data(self, fig)
        self.assertGreaterEqual(fig.axes[1].get_ylim()[1], 10)

    def test_nested_grid_sharey_spans_its_cells(self):
        small = LineChart(data=_points([0, 1]))
        large = LineChart(data=_points([0, 10]))
        other = ScatterChart(data=_points([40, 60], start=-2))
        _assert_holds_data(self, Grid([Grid([small, large], sharey=True), other]))


if __name__ == "__main__":
    unittest.main()
