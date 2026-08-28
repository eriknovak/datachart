"""Module containing the `charts`.

The `charts` module contains the methods to create the plots and figures,
grouped by the question they answer.

Methods:
    LineChart(attrs):
        Creates the line chart.
    StackedAreaChart(attrs):
        Creates the stacked area chart.
    BarChart(attrs):
        Creates the bar chart.
    PyramidChart(attrs):
        Creates the pyramid chart.
    RadialChart(attrs):
        Creates the radial chart.
    Histogram(attrs):
        Creates the histogram.
    BoxPlot(attrs):
        Creates the box plot.
    ViolinPlot(attrs):
        Creates the violin plot.
    SwarmPlot(attrs):
        Creates the swarm plot.
    RaincloudPlot(attrs):
        Creates the raincloud plot.
    ScatterChart(attrs):
        Creates the scatter chart.
    Heatmap(attrs):
        Creates the heatmap.
    ContourChart(attrs):
        Creates the contour chart.
    HexbinChart(attrs):
        Creates the hexbin chart.
    ParallelCoords(attrs):
        Creates the parallel coordinates chart.
    SankeyChart(attrs):
        Creates the Sankey chart.

"""

# trends and comparisons
from .line_chart import LineChart
from .stacked_area_chart import StackedAreaChart
from .bar_chart import BarChart
from .pyramid_chart import PyramidChart
from .radial_chart import RadialChart

# distributions
from .histogram import Histogram
from .box_plot import BoxPlot
from .violin_plot import ViolinPlot
from .swarm_plot import SwarmPlot
from .raincloud_plot import RaincloudPlot

# relationships
from .scatter_chart import ScatterChart
from .heatmap import Heatmap
from .contour_chart import ContourChart
from .hexbin_chart import HexbinChart
from .parallel_coords import ParallelCoords

# flows
from .sankey_chart import SankeyChart

__all__ = [
    # trends and comparisons
    "LineChart",
    "StackedAreaChart",
    "BarChart",
    "PyramidChart",
    "RadialChart",
    # distributions
    "Histogram",
    "BoxPlot",
    "ViolinPlot",
    "SwarmPlot",
    "RaincloudPlot",
    # relationships
    "ScatterChart",
    "Heatmap",
    "ContourChart",
    "HexbinChart",
    "ParallelCoords",
    # flows
    "SankeyChart",
]
