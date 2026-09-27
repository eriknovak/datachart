"""Tests for the nested-grid layout engine and its fallback."""

import threading
import unittest
import warnings
from unittest import mock

import matplotlib

matplotlib.use("Agg", force=True)

import matplotlib._constrained_layout as _constrained_layout
from matplotlib.gridspec import GridSpecFromSubplotSpec
from matplotlib.layout_engine import ConstrainedLayoutEngine

from datachart.charts import BarChart, LineChart
from datachart.utils import Grid
from datachart.utils._internal import figures


def _line_fig():
    return LineChart(data=[{"x": i, "y": i * 2} for i in range(5)])


def _bar_fig():
    return BarChart(data=[{"label": c, "y": v} for c, v in zip("ABCD", [3, 1, 4, 2])])


def _nested_grid():
    """A two-row host grid whose second row holds only a nested grid."""
    inner = Grid([[_line_fig(), _bar_fig()]])
    return Grid([[_line_fig(), _bar_fig()], [inner]])


def _split_heights(fig):
    """Axes heights of the host row's charts and of the nested grid's charts."""
    fig.canvas.draw()
    host, nested = [], []
    for ax in fig.axes:
        if not ax.axison:
            continue
        gs = ax.get_subplotspec().get_gridspec()
        target = nested if isinstance(gs, GridSpecFromSubplotSpec) else host
        target.append(ax.get_position().height)
    return host, nested


class TestNestedGridLayout(unittest.TestCase):

    def test_nested_grid_alone_in_row_keeps_sibling_height(self):
        """A nested grid alone in a host row does not shrink (issue #86)."""
        host, nested = _split_heights(_nested_grid())
        self.assertEqual((len(host), len(nested)), (2, 2))
        for height in nested:
            self.assertAlmostEqual(height, host[0], delta=1e-3)

    def test_missing_margin_hook_is_detected(self):
        with mock.patch.dict(_constrained_layout.__dict__):
            del _constrained_layout.make_layout_margins
            self.assertFalse(figures._margin_hook_available())
        self.assertTrue(figures._margin_hook_available())

    def test_missing_margin_hook_falls_back_to_plain_engine(self):
        """Without the private hook the figure lays out plainly and warns once."""
        original = _constrained_layout.make_layout_margins
        # matplotlib's own layout still needs a margin step: one it can call
        # whose signature the guard rejects
        with (
            mock.patch.object(
                _constrained_layout,
                "make_layout_margins",
                lambda *args, **kwargs: original(*args, **kwargs),
            ),
            mock.patch.object(
                figures, "_MARGIN_HOOK", figures._margin_hook_available()
            ),
            mock.patch.object(figures, "_fallback_warned", False),
            warnings.catch_warnings(record=True) as caught,
        ):
            warnings.simplefilter("always")
            figure = figures.new_figure()
            fig = _nested_grid()
            fig.canvas.draw()
        self.assertIs(type(figure.get_layout_engine()), ConstrainedLayoutEngine)
        self.assertIs(type(fig.get_layout_engine()), ConstrainedLayoutEngine)
        fallback = [w for w in caught if "nested grid" in str(w.message)]
        self.assertEqual(len(fallback), 1)
        self.assertTrue(issubclass(fallback[0].category, UserWarning))
        self.assertEqual(len(fig.axes), 4)

    def test_concurrent_layouts_restore_margin_hook(self):
        """Two threads laying out nested grids leave the private hook untouched."""
        original = _constrained_layout.make_layout_margins
        errors = []

        def render():
            try:
                for _ in range(3):
                    _nested_grid().canvas.draw()
            except Exception as error:  # a thread swallows it; surfaced below
                errors.append(error)

        threads = [threading.Thread(target=render) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(errors, [])
        self.assertIs(_constrained_layout.make_layout_margins, original)


if __name__ == "__main__":
    unittest.main()
