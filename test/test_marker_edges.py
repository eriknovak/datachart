"""Tiny markers drop their theme edge; a highlight edge always stays."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from datachart.charts import NetworkChart, RadialChart, ScatterChart, SwarmPlot
from datachart.config import config
from datachart.constants import EMPHASIS, RADIAL_TYPE
from datachart.utils._internal.layers import (
    MARKER_EDGE_MAX_SHARE,
    _marker_edge_widths,
)

POINTS = [{"x": i, "y": i} for i in range(4)]
GROUPS = [{"label": "a", "value": float(i)} for i in range(4)]
SPOKES = [{"label": str(i), "y": i + 1} for i in range(4)]
EDGE = config["plot_scatter_edge_width"]
# the largest area whose diameter is too small for the default stroke
TINY = (EDGE / MARKER_EDGE_MAX_SHARE) ** 2 * 0.9


def _points(ax):
    return [c for c in ax.collections if len(c.get_offsets())]


class TestMarkerEdgeWidths(unittest.TestCase):
    def tearDown(self):
        plt.close("all")
        config.reset_config()

    def test_helper_scalar_and_per_marker(self):
        self.assertEqual(_marker_edge_widths(0.5, 36), 0.5)
        self.assertEqual(_marker_edge_widths(0.5, TINY), 0.0)
        self.assertIsNone(_marker_edge_widths(None, 36))
        np.testing.assert_array_equal(
            _marker_edge_widths(0.5, np.array([36.0, TINY])), [0.5, 0.0]
        )

    def test_default_sizes_keep_their_edge(self):
        for fig in (ScatterChart(POINTS), SwarmPlot(GROUPS)):
            widths = _points(fig.axes[0])[0].get_linewidths()
            self.assertTrue(all(w > 0 for w in widths))

    def test_tiny_scatter_drops_its_edge(self):
        fig = ScatterChart(POINTS, style={"plot_scatter_size": TINY})
        self.assertEqual(list(_points(fig.axes[0])[0].get_linewidths()), [0.0])

    def test_bubble_sizes_drop_the_edge_per_point(self):
        data = [dict(p, size=p["x"]) for p in POINTS]
        fig = ScatterChart(data, size="size", size_range=(TINY, 400))
        widths = _points(fig.axes[0])[0].get_linewidths()
        self.assertEqual(widths[0], 0.0)
        self.assertEqual(widths[-1], EDGE)

    def test_tiny_swarm_drops_its_edge(self):
        fig = SwarmPlot(GROUPS, style={"plot_swarm_size": TINY})
        self.assertEqual(list(_points(fig.axes[0])[0].get_linewidths()), [0.0])

    def test_tiny_radial_drops_its_edge(self):
        fig = RadialChart(
            SPOKES, type=RADIAL_TYPE.SCATTER, style={"plot_scatter_size": TINY}
        )
        self.assertEqual(list(_points(fig.axes[0])[0].get_linewidths()), [0.0])

    def test_highlight_keeps_its_edge(self):
        fig = ScatterChart(
            POINTS, emphasis=EMPHASIS.HIGHLIGHT, style={"plot_scatter_size": TINY}
        )
        self.assertGreater(_points(fig.axes[0])[0].get_linewidths()[0], 0)

    def test_network_nodes_drop_the_edge_per_node(self):
        fig = NetworkChart(
            {
                "nodes": [{"id": "a", "size": 1}, {"id": "b", "size": 100}],
                "edges": [{"source": "a", "target": "b"}],
            },
            style={"plot_network_node_size_min": TINY},
        )
        nodes = [c for c in fig.axes[0].collections if c.get_gid() == "nodes"][0]
        small, large = nodes.get_linewidths()
        self.assertEqual(small, 0.0)
        self.assertEqual(large, config["plot_network_node_edge_width"])


if __name__ == "__main__":
    unittest.main()
