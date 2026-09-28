"""The single drawing seam: Layer, LayerGroup, Panel, DrawContext.

A Layer is one drawable unit that puts its marks on a matplotlib Axes. Its style
is resolved from the global config when the layer is built — never at draw time.
A Panel owns every cross-layer concern: color assignment, bar slotting, shared
histogram bins, axis scales and limits, grid, legend assembly, and twin-axis
(left/right) assignment. Layers are sibling-blind; a Panel hands each layer a
frozen DrawContext with its per-layer instructions.
"""

from .base import (
    DEFAULT_ORIENTATION,
    DrawContext,
    Etch,
    HOLLOW_MARKER_EDGE_WIDTH,
    InkStroke,
    Layer,
    MARKER_EDGE_MAX_SHARE,
    MarkClipBox,
    NumpyEncoder,
    TEXT_LINE_HEIGHT,
    _marker_edge_widths,
    _rule_summary,
    emphasis_rule_roles,
    get_chart_hash,
    is_temporal,
    resolve_show_values,
    series_units,
    theme_default,
    value_axis_grid,
    value_label_font,
)
from .ticks import ScheduleTicks, _column_tz, to_date_numbers
from .line import (
    BumpLayer,
    LineLayer,
    StackedAreaLayer,
    _stack_slots,
    rank_bump_charts,
    rank_series,
    stack_first_line,
)
from .bar import (
    BarLayer,
    GanttLayer,
    HistogramLayer,
    KdeLayer,
    bar_units,
    gantt_units,
    sort_bar_charts,
    sort_gantt_charts,
)
from .scatter import ScatterLayer
from .group import (
    BoxLayer,
    DumbbellLayer,
    RAINCLOUD_BOX_WIDTH,
    RAINCLOUD_CLOUD_OFFSET,
    RAINCLOUD_CLOUD_WIDTH,
    RAINCLOUD_RAIN_OFFSET,
    RAINCLOUD_RAIN_SIZE,
    RAINCLOUD_RAIN_SPREAD,
    RidgelineLayer,
    SWARM_MAX_OFFSET,
    SwarmLayer,
    ViolinLayer,
    beeswarm_offsets,
    build_raincloud_layers,
    dumbbell_units,
    group_units,
    sort_dumbbell_charts,
    strip_offsets,
)
from .grid import (
    CalendarHeatmapLayer,
    ContourLayer,
    HEXBIN_REDUCERS,
    HeatmapLayer,
    HexbinLayer,
    contour_levels,
    heatmap_units,
)
from .position import BasemapLayer, DRAW_ZORDER, ImageLayer, draw_zorder_key
from .parallel import ParallelCoordsLayer, parallel_units
from .radial import RADIAL_LAYER_TYPES, RadialLayer
from .relational import (
    NETWORK_PULL_MAX,
    NETWORK_PULL_MIN,
    NetworkLayer,
    SankeyLayer,
    TreemapLayer,
    _fit_text,
    _overlap_area,
    _squarify,
    _text_box,
    _wrap_label,
    circular_layout,
    edge_strengths,
    grouped_layout,
    network_units,
    spring_layout,
    treemap_units,
)
from .text import TextLayer
from .panel import (
    BRACKET_GAP,
    BRACKET_STEP,
    DLINE_CURVE_SAMPLES,
    LayerGroup,
    Panel,
    REF_LINE_ZORDER,
    determine_axis_assignment,
    group_from_chart,
    layers_per_chart,
)
