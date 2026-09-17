"""An axis end whose data sits on a tick stops on that tick, and the marks there draw whole."""

import unittest

from matplotlib.collections import PathCollection

from datachart.charts import (
    BumpChart,
    DumbbellChart,
    LineChart,
    ScatterChart,
    SwarmPlot,
)
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

    def test_user_limit_keeps_the_clip_on_its_axis(self):
        """A user limit may cut the data on purpose; the other axis still unclips."""
        fig = ScatterChart(data=POINTS, xmax=100)
        fig.canvas.draw()
        box = fig.axes[0].collections[0].get_clip_box()
        self.assertIsInstance(box, MarkClipBox)
        self.assertEqual(box._dims, ("y",))

    def test_dumbbell_dots_on_the_data_end_draw_whole(self):
        """A value axis that stops on the last dot leaves the dots unclipped."""
        rows = [
            {"label": "A", "start": 30, "end": 40},
            {"label": "B", "start": 45, "end": 60},
        ]
        fig = DumbbellChart(data=rows)
        fig.canvas.draw()
        self.assertEqual(fig.axes[0].get_xlim(), (30.0, 60.0))
        dots = [c for c in fig.axes[0].collections if isinstance(c, PathCollection)]
        self.assertEqual(len(dots), 2)
        for collection in dots:
            self.assertIsInstance(collection.get_clip_box(), MarkClipBox)

    def test_swarm_points_on_the_data_end_draw_whole(self):
        points = [{"label": "A", "value": v} for v in (0, 25, 50, 75, 100)]
        fig = SwarmPlot(data=points)
        fig.canvas.draw()
        self.assertEqual(fig.axes[0].get_ylim(), (0.0, 100.0))
        self.assertIsInstance(fig.axes[0].collections[0].get_clip_box(), MarkClipBox)

    def test_bump_end_markers_draw_whole_under_rank_limits(self):
        """Limits on the rank axis leave the period ends unclipped."""
        ranks = ([1, 2, 3], [2, 1, 1], [3, 3, 2])
        data = [[{"x": 2016 + i, "y": r} for i, r in enumerate(rs)] for rs in ranks]
        fig = BumpChart(data=data, ymin=0.5, ymax=5.5)
        fig.canvas.draw()
        box = fig.axes[0].lines[0].get_clip_box()
        self.assertIsInstance(box, MarkClipBox)
        self.assertIn("x", box._dims)
        self.assertNotIn("y", box._dims)


if __name__ == "__main__":
    unittest.main()
