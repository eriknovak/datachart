"""Module containing the `charts`.

The `charts` module contains the functions that create the figures, one per
chart type, grouped by the question they answer. Every function takes the data
as a list of records, keyword settings, and an optional `style` dictionary, and
returns a matplotlib figure.

"""

# trends and comparisons
from .line_chart import LineChart
from .stacked_area_chart import StackedAreaChart
from .bump_chart import BumpChart
from .bar_chart import BarChart
from .pyramid_chart import PyramidChart
from .radial_chart import RadialChart
from .calendar_heatmap import CalendarHeatmap
from .gantt_chart import GanttChart
from .dumbbell_chart import DumbbellChart

# distributions
from .histogram import Histogram
from .box_plot import BoxPlot
from .violin_plot import ViolinPlot
from .swarm_plot import SwarmPlot
from .raincloud_plot import RaincloudPlot
from .ridgeline_plot import RidgelinePlot

# relationships
from .scatter_chart import ScatterChart
from .heatmap import Heatmap
from .contour_chart import ContourChart
from .hexbin_chart import HexbinChart
from .parallel_coords import ParallelCoords
from .network_chart import NetworkChart
from .scatter_matrix import ScatterMatrix

# flows
from .sankey_chart import SankeyChart

# part of a whole
from .treemap import Treemap

__all__ = [
    # trends and comparisons
    "LineChart",
    "StackedAreaChart",
    "BumpChart",
    "BarChart",
    "PyramidChart",
    "RadialChart",
    "CalendarHeatmap",
    "GanttChart",
    "DumbbellChart",
    # distributions
    "Histogram",
    "BoxPlot",
    "ViolinPlot",
    "SwarmPlot",
    "RaincloudPlot",
    "RidgelinePlot",
    # relationships
    "ScatterChart",
    "Heatmap",
    "ContourChart",
    "HexbinChart",
    "ParallelCoords",
    "NetworkChart",
    "ScatterMatrix",
    # flows
    "SankeyChart",
    # part of a whole
    "Treemap",
]
