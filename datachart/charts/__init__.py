"""Module containing the `charts`.

The `charts` module contains the methods to create the plots and figures.

Methods:
    BarChart(attrs):
        Creates the bar chart.
    BoxPlot(attrs):
        Creates the box plot.
    Heatmap(attrs):
        Creates the heatmap.
    Histogram(attrs):
        Creates the histogram.
    LineChart(attrs):
        Creates the line chart.
    ParallelCoords(attrs):
        Creates the parallel coordinates chart.
    ScatterChart(attrs):
        Creates the scatter chart.

"""

from .bar_chart import BarChart
from .box_plot import BoxPlot
from .heatmap import Heatmap
from .histogram import Histogram
from .line_chart import LineChart
from .parallel_coords import ParallelCoords
from .scatter_chart import ScatterChart

__all__ = [
    "BarChart",
    "BoxPlot",
    "Heatmap",
    "Histogram",
    "LineChart",
    "ParallelCoords",
    "ScatterChart",
]
