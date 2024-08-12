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

"""

from .line_chart import LineChart
from .bar_chart import BarChart
from .histogram import Histogram
from .heatmap import Heatmap


__all__ = ["LineChart", "BarChart", "Histogram", "Heatmap"]
