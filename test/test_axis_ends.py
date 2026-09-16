"""An axis end whose data sits on a tick stops on that tick, and the marks there draw whole."""

import unittest

from datachart.charts import LineChart, ScatterChart
from datachart.utils import Panel
from datachart.utils._internal.layers import MarkClipBox

POINTS = [{"x": x, "y": x / 2} for x in range(0, 101, 10)]


class TestAxisEndsOnData(unittest.TestCase):
    def test_scatter_data_on_a_tick_ends_there(self):
        """The autoscale margin past 100 rounds to 100, not to 120."""
        fig = ScatterChart(data=POINTS)
        self.assertEqual(fig.axes[0].get_xlim(), (0.0, 100.0))
        self.assertEqual(fig.axes[0].get_ylim(), (0.0, 50.0))

    def test_data_off_a_tick_keeps_the_outward_snap(self):
        fig = ScatterChart(data=[{"x": x, "y": x} for x in (0, 50, 97)])
        self.assertEqual(fig.axes[0].get_xlim(), (0.0, 120.0))

    def test_line_value_axis_on_a_tick_ends_there(self):
        fig = LineChart(data=POINTS)
        self.assertEqual(fig.axes[0].get_ylim(), (0.0, 50.0))

    def test_panel_of_scatter_and_line_shares_the_data_end(self):
        fig = Panel([ScatterChart(data=POINTS), LineChart(data=POINTS)])
        self.assertEqual(fig.axes[0].get_xlim(), (0.0, 100.0))

    def test_scatter_edge_marks_draw_whole(self):
        fig = ScatterChart(data=POINTS)
        fig.canvas.draw()
        self.assertIsInstance(fig.axes[0].collections[0].get_clip_box(), MarkClipBox)

    def test_user_limit_keeps_the_clip(self):
        """A user limit may cut the data on purpose."""
        fig = ScatterChart(data=POINTS, xmax=100)
        fig.canvas.draw()
        self.assertNotIsInstance(fig.axes[0].collections[0].get_clip_box(), MarkClipBox)


if __name__ == "__main__":
    unittest.main()
