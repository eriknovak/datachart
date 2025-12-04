"""Module containing the `charts`.

The `charts` module contains the methods to create the plots and figures.

Methods:
    LineChart(attrs):
        Creates the line chart.
    BarChart(attrs):
        Creates the bar chart.
    Histogram(attrs):
        Creates the histogram.
    Heatmap(attrs):
        Creates the heatmap.
    ScatterChart(attrs):
        Creates the scatter chart.
    BoxPlot(attrs):
        Creates the box plot.
    ParallelCoords(attrs):
        Creates the parallel coordinates chart.

"""

from .line_chart import LineChart
from .bar_chart import BarChart
from .histogram import Histogram
from .heatmap import Heatmap
from .scatter_chart import ScatterChart
from .box_plot import BoxPlot
from .parallel_coords import ParallelCoords


__all__ = ["LineChart", "BarChart", "Histogram", "Heatmap", "ScatterChart", "BoxPlot", "ParallelCoords"]
