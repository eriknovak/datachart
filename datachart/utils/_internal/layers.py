"""The single drawing seam: Layer, LayerGroup, Panel, DrawContext.

A Layer is one drawable unit that puts its marks on a matplotlib Axes. Its style
is resolved from the global config when the layer is built — never at draw time.
A Panel owns every cross-layer concern: color assignment, bar slotting, shared
histogram bins, axis scales and limits, grid, legend assembly, and twin-axis
(left/right) assignment. Layers are sibling-blind; a Panel hands each layer a
frozen DrawContext with its per-layer instructions.
"""

import hashlib
from contextlib import contextmanager
import json
import math
import warnings
from collections import defaultdict
from datetime import date, datetime, time, timedelta, tzinfo
from numbers import Real
from dataclasses import dataclass, replace
from itertools import cycle as iter_cycle
from typing import Callable, List, NamedTuple, Optional, Union

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.font_manager import FontProperties
from matplotlib import cbook, rc_context
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator
from matplotlib.collections import LineCollection, PathCollection, PolyCollection
from matplotlib.container import BarContainer
from matplotlib.colors import (
    LinearSegmentedColormap,
    to_hex,
    to_rgb,
    to_rgba,
    to_rgba_array,
)
from matplotlib.mlab import GaussianKDE
from matplotlib.lines import Line2D
from matplotlib.markers import MarkerStyle
from matplotlib.patches import Circle, FancyArrowPatch, Patch, PathPatch, Rectangle
from matplotlib.path import Path
from matplotlib.text import Text
from matplotlib.transforms import (
    offset_copy,
    Bbox,
    IdentityTransform,
    ScaledTranslation,
    TransformedBbox,
    TransformedPath,
    blended_transform_factory,
)
import matplotlib.patheffects as patheffects
from matplotlib.legend import Legend
from matplotlib.legend_handler import (
    HandlerPatch,
    HandlerPathCollection,
    HandlerPolyCollection,
)

from .colors import (
    create_color_cycle,
    create_colormap,
    get_colormap,
    get_discrete_colors,
)
from .validate import (
    AXIS_CATEGORICAL,
    AXIS_NUMERIC,
    AXIS_TEMPORAL,
    infer_network_nodes,
    first_seen_nodes,
    infer_sankey_columns,
    treemap_record_total,
    validate_baseline,
    validate_contour_levels,
    validate_filled_levels,
    validate_emphasis,
    validate_given_ranks,
    validate_label_position,
    validate_node_label_position,
    validate_line_curve,
    validate_rank_by,
    validate_emphasis_rule,
    validate_date_period,
    validate_dumbbell_show_values,
    validate_dumbbell_sort_by,
    validate_marker_pair,
    validate_gantt_arrow_entry,
    validate_gantt_show_values,
    validate_gantt_sort_by,
    validate_log_values,
    validate_overlap,
    validate_ridge_marks,
    validate_ridgeline_inner,
    validate_ridgeline_scale,
    validate_single_dataset,
    validate_sort,
    validate_sort_by,
    validate_network_edge_style,
    validate_sankey_link_color,
    validate_axis_kinds,
    validate_shared_x,
    validate_span_bounds,
    validate_ticks_format,
    validate_value_step,
    validate_week_start,
)
from .config_helpers import (
    get_attr_value,
    resolve_font_family,
    get_area_style,
    get_bump_style,
    get_etch,
    get_ink_stroke,
    get_legend_style,
    get_value_etch,
    get_sketch_halo,
    get_stackedarea_style,
    get_sankey_style,
    get_treemap_style,
    get_network_style,
    get_grid_style,
    get_line_style,
    get_bar_style,
    get_gantt_style,
    get_dumbbell_style,
    get_hist_style,
    get_kde_style,
    get_legend_panel_settings,
    expand_legend_location,
    get_vline_style,
    get_hline_style,
    get_vspan_style,
    get_hspan_style,
    get_heatmap_style,
    get_heatmap_font_style,
    get_heatmap_edge_style,
    get_calendar_month_line_style,
    get_contour_style,
    get_contour_label_style,
    get_hexbin_style,
    get_colorbar_setting,
    get_scatter_style,
    get_regression_style,
    get_box_style,
    get_box_outlier_style,
    get_box_median_style,
    get_box_whisker_style,
    get_box_cap_style,
    get_swarm_style,
    get_violin_style,
    get_violin_inner_style,
    get_ridgeline_style,
    get_parallel_coords_style,
    get_parallel_axis_style,
    get_parallel_tick_style,
    get_parallel_tick_length,
    get_parallel_tick_label_style,
    get_parallel_tick_label_bbox,
    get_parallel_dim_label_style,
    get_parallel_dim_label_rotation,
    get_parallel_dim_label_pad,
    get_text_style,
    get_plot_text_style,
    get_value_label_style,
    get_plot_text_box_style,
    get_plot_text_arrow_style,
    configure_axis_ticks_position,
    configure_axis_limits,
)
from ..stats import minimum, maximum, iqr, kde1d
from ...constants import (
    ARROW_STYLE,
    ASPECT_RATIO,
    BUMP_LABEL_POSITION,
    BUMP_RANK,
    CALENDAR_WEEKDAY,
    COLORBAR_LOCATION,
    COLORS,
    CONTOUR_LEVELS,
    DATE_FORMAT,
    DUMBBELL_SORT_KEY,
    DUMBBELL_VALUE,
    EMPHASIS,
    FONT_WEIGHT,
    GANTT_ARROW_ENTRY,
    GANTT_DATE_PERIOD,
    GANTT_SORT_KEY,
    GANTT_VALUE,
    HEXBIN_REDUCE,
    HISTOGRAM_TYPE,
    LEGEND_LOCATION,
    NETWORK_LAYOUT,
    NETWORK_LABEL_POSITION,
    ORIENTATION,
    RADIAL_DIRECTION,
    RADIAL_TYPE,
    RIDGELINE_SCALE,
    SCALE,
    SORT,
    STACKED_AREA_BASELINE,
    SWARM_MODE,
    VALUE_FORMAT,
    VIOLIN_INNER,
)
from ...config import config

DEFAULT_NUM_BINS = 20
DEFAULT_ORIENTATION = ORIENTATION.VERTICAL
DEFAULT_VALUE_FORMAT = VALUE_FORMAT.DEFAULT
DEFAULT_CI_LEVEL = 0.95
DEFAULT_SIZE_RANGE = (20, 200)
DEFAULT_SWARM_MODE = SWARM_MODE.SWARM
DEFAULT_SWARM_JITTER = 0.4
# swarm offsets stay inside the category cell, clear of its neighbors
SWARM_MAX_OFFSET = 0.4
DEFAULT_VALUE_LABEL_FORMAT = "%g"
# show_area fills this many data magnitudes below the line; the axes clip it,
# so the fill meets the floor whatever limits sharey, ymin or a re-render set
AREA_FLOOR_FACTOR = 1e6
# emphasis roles (ADR 0009): background mutes, highlight bolds, None is today
EMPHASIS_BACKGROUND = EMPHASIS.BACKGROUND
EMPHASIS_HIGHLIGHT = EMPHASIS.HIGHLIGHT
# offsets keep emphasized layers among the data layers, below panel furniture
EMPHASIS_Z_OFFSET = {EMPHASIS_BACKGROUND: -0.5, EMPHASIS_HIGHLIGHT: 0.5}
MUTED_WIDTH_SCALE = 0.75
HIGHLIGHT_WIDTH_SCALE = 2.0
DEFAULT_MUTED_COLOR = "#CFCFCF"
DEFAULT_MUTED_ALPHA = 0.5
# sankey labels: room past the outer columns, the gap to the node bar
SANKEY_LABEL_MARGIN = 0.2
SANKEY_LABEL_PAD = 0.01
# column headings sit this far above the tallest column
SANKEY_COLUMN_LABEL_PAD = 0.03
SANKEY_COLUMN_LABEL_HEADROOM = 0.1
# a ribbon value sits at the ribbon's end, before the node it enters, where no
# label lives; thin ribbons fall back to spots along the centreline
SANKEY_VALUE_POSITIONS = (0.8, 0.65, 0.5, 0.35, 0.2)
# estimated glyph width and line height as multiples of the font size
TEXT_WIDTH_PER_CHAR = 0.55
TEXT_LINE_HEIGHT = 1.2
# point labels: the gap between a marker's edge and its label, in points, and
# the candidate spots around the marker in preference order (ha, va, dx, dy)
POINT_LABEL_PAD = 3.0
# an overlap below this many square pixels counts as a clear spot
POINT_LABEL_CLEAR = 1e-6
POINT_LABEL_SPOTS = (
    ("left", "center", 1, 0),
    ("right", "center", -1, 0),
    ("center", "bottom", 0, 1),
    ("center", "top", 0, -1),
    ("left", "bottom", 1, 1),
    ("right", "bottom", -1, 1),
    ("left", "top", 1, -1),
    ("right", "top", -1, -1),
)
# a line's value labels sit above or below the mark only: a side spot falls
# on the line itself, between two points, and reads as either (ADR 0033);
# the edge-anchored spots keep the first and last labels inside the axes
POINT_LABEL_SPOTS_VERTICAL = (
    ("center", "bottom", 0, 1),
    ("center", "top", 0, -1),
    ("left", "bottom", 0, 1),
    ("right", "bottom", 0, 1),
    ("left", "top", 0, -1),
    ("right", "top", 0, -1),
)
# a raincloud's extremes sit past their points along the value axis, clear of
# the box whiskers beside the rain (ADR 0033)
POINT_LABEL_SPOTS_HORIZONTAL = POINT_LABEL_SPOTS[:2]
# the widest correlation readout, for reserving its corner box
CORRELATION_BOX_TEXT = "r = -0.000"
# the correlation readout's corner, in axes fractions
CORRELATION_BOX_CORNER = (0.05, 0.95)
CORRELATION_BOX_PAD = 0.3
SANKEY_GREY = "#9E9E9E"
# treemap header band: its height in font heights, and the group height in
# bands below which the group goes unlabelled (ADR 0028)
TREEMAP_BAND_HEIGHT = 1.6
TREEMAP_BAND_MIN_ROWS = 2.2
# points kept clear inside a tile around its label, and before a band label
TREEMAP_LABEL_PAD = 4
# the font shrinks in these steps before a label is dropped
TREEMAP_FONT_STEP = 0.5
# network layouts keep this much of the 0–1 space clear on every side, room
# for the largest marker and its label (ADR 0029)
NETWORK_LAYOUT_MARGIN = 0.1
# fixed positions stay the user's; the view widens by this much on every
# side, so 0–1 lands inside the same margin (ADR 0029)
NETWORK_FIXED_PAD = NETWORK_LAYOUT_MARGIN / (1 - 2 * NETWORK_LAYOUT_MARGIN)
# spring layout: iterations and the initial step, cooled geometrically
NETWORK_SPRING_ITERATIONS = 300
NETWORK_SPRING_STEP = 0.1
NETWORK_SPRING_COOLING = 0.985
# weighted pull: the lightest edge pulls at PULL_MIN times the plain spring
# pull, the heaviest at PULL_MAX, the rest linearly between (ADR 0030)
NETWORK_PULL_MIN = 0.1
NETWORK_PULL_MAX = 3.0
# grouped layout: a cluster's radius scales sqrt(n_g / n); centres are pushed
# apart to GAP times the summed radii; a cluster fills FILL of its share of
# the gap to its nearest neighbour (ADR 0030)
NETWORK_CLUSTER_RADIUS = 0.3
NETWORK_CLUSTER_GAP = 2.0
NETWORK_CLUSTER_FILL = 0.8
NETWORK_CLUSTER_PUSH_ITERATIONS = 100
# a disconnected spring packs its components like clusters, closer: they
# carry no halo (ADR 0029)
NETWORK_COMPONENT_GAP = 1.25
# the cluster halo reaches this far past the rim nodes' markers, room for
# their labels
NETWORK_CLUSTER_HALO_PAD = 0.03
# the grouped solvers pull every node toward the centre in proportion to its
# distance: a node with no link inside its network cannot drift away and
# squeeze the linked ones together, and a chain of groups folds into a
# compact shape instead of a line across the square
NETWORK_CLUSTER_GRAVITY = 3.0
# an arrowhead grows with its shaft, from this base in points
NETWORK_ARROW_HEAD_BASE = 6.0
NETWORK_ARROW_HEAD_PER_WIDTH = 1.5
# an inked directed edge: its head's width as a share of its length (ADR 0048)
NETWORK_INKED_HEAD_WIDTH = 0.6
# a cluster ring's stroke, in points
NETWORK_RING_WIDTH = 0.9
# the gap between a node's marker and a name printed above it, in points
NETWORK_LABEL_GAP = 2.0
# the spacing, in pixels, of the boxes an edge is sampled into for BEST labels
NETWORK_OBSTACLE_STEP = 6.0
# matplotlib skips underscore-prefixed labels when assembling the legend
NO_LEGEND = "_nolegend_"
# radial furniture defaults: compass and calendar conventions (ADR 0015)
DEFAULT_STARTANGLE = "N"
DEFAULT_DIRECTION = RADIAL_DIRECTION.CLOCKWISE
COMPASS_LOCATIONS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
# the polar border circle crosses the plot area, so the r-value labels and
# the legend stack above the spine zorder, not just above the marks
RADIAL_LABEL_Z_OVER_SPINE = 1
RADIAL_LEGEND_Z_OVER_SPINE = 2
DEFAULT_SPINE_ZORDER = 100
# axis labels on a polar axes pad past the category labels around the circle
RADIAL_XLABEL_PAD = 15
RADIAL_YLABEL_PAD = 30
# tip texts sit just past the mark along its spoke, as fractions of the r span
RADIAL_TIP_VALUE_PAD = 0.03
RADIAL_TIP_LABEL_PAD = 0.06
# a soft box keeps polar tip texts legible over the grid spokes and the border
# a radius label hangs this many points inside its ring, plus half its height
RADIAL_RLABEL_INSET = 3.0
# extra radial room so tip labels stay inside the border circle
RADIAL_TIP_LABEL_HEADROOM = 0.25


def _scatter_legend_handle(legend_handle, orig_handle):
    legend_handle.update_from(orig_handle)
    size = getattr(orig_handle, "datachart_legend_size", None)
    if size is not None:
        legend_handle.set_sizes([size])


# a marker keeps its theme edge only while the stroke stays under this share of
# the marker diameter (sqrt of the area in points): on a tiny circle a light
# rim reads as a gap and a dark one swallows the fill
MARKER_EDGE_MAX_SHARE = 1 / 6


def _marker_edge_widths(width, sizes):
    """`width` for markers of area `sizes` the stroke fits, 0 for the rest.

    Scalar in, scalar out; per-marker areas give per-marker widths. A highlight
    edge never passes through here — it is the emphasis cue, not a rim.
    """

    if not width or sizes is None:
        return width
    fits = width <= MARKER_EDGE_MAX_SHARE * np.sqrt(np.asarray(sizes, dtype=float))
    if fits.all():
        return width
    if not fits.any():
        return 0.0
    return np.where(fits, width, 0.0)


# a hollow marker's outline is the mark: never thinner than this, in points
HOLLOW_MARKER_EDGE_WIDTH = 1.2


def _hollow_marker(style: dict) -> dict:
    """A scatter style whose cycle marker is hollow: the color strokes the outline."""

    if not style.pop("hollow", False):
        return style
    color = style.pop("c", None)
    style["facecolors"] = "none"
    if color is not None:
        style["edgecolors"] = color
    width = np.max(style.get("linewidths") or 0)
    style["linewidths"] = max(float(width), HOLLOW_MARKER_EDGE_WIDTH)
    return style


# marker collections draw plain, highlighted, then muted
MARKER_ROLE_ORDER = (None, EMPHASIS_HIGHLIGHT, EMPHASIS_BACKGROUND)


def _draw_scatter_marks(scatter, x, y, sizes, style: dict, label, highlighted: bool):
    """One marker collection; the edge fits its markers unless it is the highlight cue.

    An unfilled marker (`"x"`, `"+"`) is all stroke: matplotlib strokes it in
    the face color, so it keeps the series color and a visible width.
    """

    style = dict(style)
    marker = style.get("marker") or mpl.rcParams["scatter.marker"]
    if not MarkerStyle(marker).is_filled():
        style.pop("hollow", None)
        # matplotlib ignores, with a warning, an edge color on these markers
        style.pop("edgecolors", None)
        width = np.max(style.get("linewidths") or 0)
        style["linewidths"] = max(float(width), HOLLOW_MARKER_EDGE_WIDTH)
    elif not highlighted:
        style["linewidths"] = _marker_edge_widths(style.get("linewidths"), sizes)
    return scatter(x, y, s=sizes, label=label, **_hollow_marker(style))


class HandlerBarSeries(HandlerPatch):
    """Draws a bar series' legend swatch from a representative bar.

    A container's swatch is its first bar, which per-record emphasis may have
    muted (ADR 0042); the series then reads as grey in the legend. The layer
    names an unmuted bar to stand for it, and without one nothing changes.
    """

    def create_artists(self, legend, orig_handle, *args, **kwargs):
        representative = getattr(orig_handle, "legend_patch", None)
        if representative is None:
            patches = getattr(orig_handle, "patches", None)
            representative = patches[0] if patches else orig_handle
        return super().create_artists(legend, representative, *args, **kwargs)


class HandlerEtchedFill(HandlerPolyCollection):
    """Draws a fill's legend swatch with the fill's etching (ADR 0048)."""

    def _update_prop(self, legend_handle, orig_handle):
        super()._update_prop(legend_handle, orig_handle)
        legend_handle.set_path_effects(orig_handle.get_path_effects())


# bubble charts size markers by data; their legend entries keep the base size
LEGEND_HANDLER_MAP = {
    PathCollection: HandlerPathCollection(update_func=_scatter_legend_handle),
    BarContainer: HandlerBarSeries(),
    PolyCollection: HandlerEtchedFill(),
}
# fraction of the value-axis span added so bar value labels stay inside
VALUE_HEADROOM_VERTICAL = 0.08
VALUE_HEADROOM_HORIZONTAL = 0.12
# a legend that would cover marks gets a clear slot at the value-axis end;
# the marks give up at most this fraction of the axes for it, padded in points
LEGEND_HEADROOM_MAX = 0.35
LEGEND_HEADROOM_PAD_PT = 4.0
# normalized cell value above which heatmap value text switches to white
HEATMAP_TEXT_CONTRAST_THRESHOLD = 0.55
# the low end of a sequential cmap vanishes on white: iso-lines sample from here
CONTOUR_LINE_CMAP_START = 0.3
# the cmap sample that stands in for a cmap-colored contour in the legend
CONTOUR_SWATCH = 0.7
# value steps (ADR 0048): the legend swatch outline
STEP_LEGEND_EDGE_WIDTH = 0.8


# ================================================
# Data Helpers
# ================================================


def get_chart_data(attr: str, chart: dict) -> Optional[np.ndarray]:
    """Extract a data column from a chart dictionary as a numpy array."""

    attr_label = get_attr_value(attr, chart, attr)

    if isinstance(chart["data"], dict):
        return chart["data"][attr_label] if attr_label in chart["data"] else None

    if isinstance(chart["data"], list):
        filtered = [d[attr_label] for d in chart["data"] if attr_label in d]
        if not filtered:
            return None
        return np.array(filtered)

    return None


def get_chart_grid(chart: dict, kind: str, dtype=float) -> tuple:
    """The validated (x, y, z) of a gridded chart; x and y are None when absent."""

    z = get_chart_data("z", chart)
    if z is None:
        raise ValueError(f"A {kind} chart requires the `z` grid in `data`.")
    z = np.asarray(z, dtype=dtype)
    if z.ndim != 2:
        raise ValueError(
            f"The {kind} `z` attribute must be a 2-D grid, got {z.ndim} dimension(s)."
        )
    n_rows, n_cols = z.shape
    axes = []
    for attr, extent, name in (("x", n_cols, "column"), ("y", n_rows, "row")):
        values = get_chart_data(attr, chart)
        if values is not None:
            values = np.asarray(values)
            if values.ndim != 1 or len(values) != extent:
                raise ValueError(
                    f"The {kind} `{attr}` attribute must hold one value per {name} "
                    f"of `z` ({extent}), got {values.shape}."
                )
        axes.append(values)
    return axes[0], axes[1], z


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles numpy arrays and types."""

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        if is_temporal(obj):
            return obj.isoformat() if isinstance(obj, date) else str(obj)
        return super().default(obj)


def get_chart_hash(chart: dict) -> int:
    """Stable hash of a chart dictionary, used to key color assignment."""

    return hash(json.dumps(chart, sort_keys=True, cls=NumpyEncoder))


# an AUTO date label carries the time only when one of the labels has one
DATE_LABEL_WITH_TIME = "%Y-%m-%d %H:%M"


def is_temporal(value) -> bool:
    """Whether `value` is a real temporal object; date strings never are (ADR 0037)."""

    # a datetime is a date; pandas Timestamps are datetimes
    return isinstance(value, (date, np.datetime64))


def axis_kind(values) -> Optional[str]:
    """The kind of axis a data column asks for; None when it holds nothing."""

    if values is None:
        return None
    if isinstance(values, np.ndarray) and values.dtype.kind == "M":
        return AXIS_TEMPORAL
    for value in values:
        if value is None:
            continue
        if is_temporal(value):
            return AXIS_TEMPORAL
        return AXIS_CATEGORICAL if isinstance(value, str) else AXIS_NUMERIC
    return None


def _as_datetime(value):
    """A value with `strftime`; numpy scalars convert at microsecond precision."""

    if isinstance(value, np.datetime64):
        return value.astype("datetime64[us]").item()
    return value


def _auto_format(fmt) -> bool:
    """Whether a tick format leaves the labels to the axis."""

    return fmt in (None, DATE_FORMAT.AUTO)


def _column_tz(values) -> Optional[tzinfo]:
    """The zone of the first zone-aware value in a temporal column, else None."""

    return next((v.tzinfo for v in values if getattr(v, "tzinfo", None)), None)


def date_labels(values, fmt=None) -> List[str]:
    """Temporal values as tick text; AUTO prints the date, plus the time when any has one."""

    values = [_as_datetime(v) for v in values]
    if _auto_format(fmt):
        has_time = any(
            isinstance(v, datetime) and (v.hour or v.minute or v.second) for v in values
        )
        fmt = DATE_LABEL_WITH_TIME if has_time else DATE_FORMAT.ISO
    return [v.strftime(fmt) for v in values]


def to_date_numbers(values) -> np.ndarray:
    """Temporal values as matplotlib date numbers, for layers that draw floats."""

    return np.asarray(mdates.date2num(list(values)), dtype=float)


def _tick_formatter(fmt, temporal: bool, locator=None, tz=None):
    """The major formatter a tick format resolves to; None keeps the axis default.

    On a temporal axis the format is a `strftime` pattern, AUTO the concise
    formatter over `locator`. Elsewhere any value-label style string (`{x}`,
    `{}`, or `%`) formats each tick, like the heatmap's `valfmt`.
    """

    if temporal:
        if _auto_format(fmt):
            if isinstance(locator, ScheduleTicks):
                return ScheduleDateFormatter(locator, tz=tz)
            return mdates.ConciseDateFormatter(locator, tz=tz)
        return mdates.DateFormatter(fmt, tz=tz)
    if _auto_format(fmt):
        return None
    return mticker.FuncFormatter(lambda value, _pos: _format_value(fmt, value))


# a period's labels, and the enclosing period named in the row beneath
DATE_PERIOD_LABELS = {
    GANTT_DATE_PERIOD.DAY: "%d",
    GANTT_DATE_PERIOD.WEEK: "W%V",
    GANTT_DATE_PERIOD.MONTH: "%b",
    GANTT_DATE_PERIOD.QUARTER: None,
    GANTT_DATE_PERIOD.YEAR: "%Y",
    GANTT_DATE_PERIOD.PROJECT_MONTH: None,
}
# the project year, the row beneath project months; never a period of its own
PROJECT_YEAR = "project_year"
DATE_PERIOD_PARENT = {
    GANTT_DATE_PERIOD.DAY: GANTT_DATE_PERIOD.MONTH,
    GANTT_DATE_PERIOD.WEEK: GANTT_DATE_PERIOD.MONTH,
    GANTT_DATE_PERIOD.MONTH: GANTT_DATE_PERIOD.YEAR,
    GANTT_DATE_PERIOD.QUARTER: GANTT_DATE_PERIOD.YEAR,
    GANTT_DATE_PERIOD.YEAR: None,
    GANTT_DATE_PERIOD.PROJECT_MONTH: PROJECT_YEAR,
}
DATE_PARENT_LABELS = {GANTT_DATE_PERIOD.MONTH: "%b %Y", GANTT_DATE_PERIOD.YEAR: "%Y"}
# the longest period of each kind in days, to reach the edges beyond the view
DATE_PERIOD_SPAN = {
    GANTT_DATE_PERIOD.DAY: 1,
    GANTT_DATE_PERIOD.WEEK: 7,
    GANTT_DATE_PERIOD.MONTH: 31,
    GANTT_DATE_PERIOD.QUARTER: 92,
    GANTT_DATE_PERIOD.YEAR: 366,
    GANTT_DATE_PERIOD.PROJECT_MONTH: 31,
    PROJECT_YEAR: 366,
}
# a period cut to under this share of the widest visible one is unlabelled
DATE_PERIOD_MIN_SHARE = 0.2
# the parent row sits this many label heights below the period row
DATE_PARENT_ROW_SPACING = 1.6


def _months_since(origin, moment) -> int:
    """The whole months from the project origin to `moment`; negative before it."""

    months = (moment.year - origin.year) * 12 + moment.month - origin.month
    if (moment.day, moment.hour, moment.minute) < (
        origin.day,
        origin.hour,
        origin.minute,
    ):
        months -= 1
    return months


class ProjectPeriodEdges(mticker.Locator):
    """Edges every `months` months from the project origin, M1 starting there."""

    def __init__(self, origin, months: int):
        self.origin = origin
        self.months = months

    def tick_values(self, vmin, vmax):
        lo, hi = (
            v if isinstance(v, (int, float)) else mdates.date2num(v)
            for v in (vmin, vmax)
        )
        first = _months_since(self.origin, mdates.num2date(lo, tz=self.origin.tzinfo))
        # no edge before the origin: the time before M1 is no project period
        k = max(first // self.months - 1, 0)
        edges = []
        while True:
            edge = mdates.date2num(self.origin + relativedelta(months=self.months * k))
            if edge > hi:
                return edges
            edges.append(edge)
            k += 1

    def __call__(self):
        return self.tick_values(*sorted(self.axis.get_view_interval()))


# a schedule's date ticks: at most this many regular steps from the first start
SCHEDULE_TICKS_MAX = 8
# sub-day steps in days: 1, 2, 5, 10, 15, 30 minutes; 1, 2, 3, 4, 6, 12 hours
SCHEDULE_TICK_SUBDAY = tuple(m / 1440 for m in (1, 2, 5, 10, 15, 30)) + tuple(
    h / 24 for h in (1, 2, 3, 4, 6, 12)
)
SCHEDULE_TICK_DAYS = (1, 2, 3, 4, 5, 7, 14, 21, 28)
SCHEDULE_TICK_MONTHS = (1, 2, 3, 4, 6, 12, 24, 60)


class ScheduleTicks(mticker.Locator):
    """Date ticks from a schedule's first start to its last end (ADR 0049).

    Minute, hour, and day steps run regularly from the first start; minutes
    and hours only when the schedule carries times. Month steps fall on the
    first of the calendar months the step divides (quarters, years). The
    first start and the last end are always ticks; a regular tick within
    half a step of either gives way, so they never crowd.
    """

    def __init__(self, start: float, end: float, tz=None, timed: bool = False):
        self.start, self.end, self.tz, self.timed = start, end, tz, timed
        # the month step of the last ticks; None when they step in days or less
        self.months = None

    def tick_values(self, vmin, vmax):
        span = self.end - self.start
        if span <= 0:
            return [self.start]
        steps = (SCHEDULE_TICK_SUBDAY if self.timed else ()) + SCHEDULE_TICK_DAYS
        # the finest step that keeps the count, preferring one that divides
        # the span so the last interval is no shorter than the rest
        fitting = [d for d in steps if span / d <= SCHEDULE_TICKS_MAX]
        even = [d for d in fitting if np.isclose(span / d, round(span / d))]
        step = (even or fitting or [None])[0]
        self.months = None
        if step is not None:
            regular = (self.start + k * step for k in range(1, round(span / step)))
        else:
            months = next(
                (
                    m
                    for m in SCHEDULE_TICK_MONTHS
                    if span / (m * 30.4) <= SCHEDULE_TICKS_MAX
                ),
                SCHEDULE_TICK_MONTHS[-1],
            )
            self.months, step = months, months * 30.4
            regular = self._month_starts(months)
        ticks = [self.start]
        for tick in regular:
            if tick >= self.end - step / 2:
                break
            if tick - self.start >= step / 2:
                ticks.append(tick)
        return ticks + [self.end]

    def _month_starts(self, months: int):
        """The 1sts of every `months`-th calendar month from the start's on."""

        start = mdates.num2date(self.start, tz=self.tz)
        # counted from year 0, so 3 months lands on quarters and 12 on Januaries
        index = -(-(start.year * 12 + start.month - 1) // months) * months
        while True:
            year, month = divmod(index, 12)
            yield mdates.date2num(
                start.replace(
                    year=year,
                    month=month + 1,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
            )
            index += months

    def __call__(self):
        return self.tick_values(*sorted(self.axis.get_view_interval()))


class ScheduleDateFormatter(mdates.ConciseDateFormatter):
    """Concise schedule labels where month-step ticks on January 1 read the year.

    The concise formatter labels at the level the first start and last end
    differ in (days), so it would print every January as "Jan"; the offset
    then names one year only when all ticks fall in it.
    """

    def __init__(self, locator: ScheduleTicks, tz=None):
        super().__init__(locator, tz=tz)
        self.schedule = locator
        self.year_offset = None

    def format_ticks(self, values):
        labels = super().format_ticks(values)
        self.year_offset = None
        if self.schedule.months is None or len(values) < 3:
            return labels
        dates = mdates.num2date(values, tz=self._tz)
        for i in range(1, len(dates) - 1):
            if (dates[i].month, dates[i].day) == (1, 1):
                labels[i] = str(dates[i].year)
        years = {d.year for d in dates}
        self.year_offset = "" if len(years) > 1 else str(dates[0].year)
        return labels

    def get_offset(self):
        if self.year_offset is None:
            return super().get_offset()
        return self.year_offset


def _period_edges(period: str, tz=None, origin=None) -> mticker.Locator:
    """The locator of a period's first instants: its edges on the axis."""

    if period == GANTT_DATE_PERIOD.PROJECT_MONTH:
        return ProjectPeriodEdges(origin, 1)
    if period == PROJECT_YEAR:
        return ProjectPeriodEdges(origin, 12)
    if period == GANTT_DATE_PERIOD.DAY:
        return mdates.DayLocator(tz=tz)
    if period == GANTT_DATE_PERIOD.WEEK:
        return mdates.WeekdayLocator(byweekday=mdates.MO, tz=tz)
    if period == GANTT_DATE_PERIOD.MONTH:
        return mdates.MonthLocator(tz=tz)
    if period == GANTT_DATE_PERIOD.QUARTER:
        return mdates.MonthLocator(bymonth=(1, 4, 7, 10), tz=tz)
    return mdates.YearLocator(tz=tz)


class PeriodCentres(mticker.Locator):
    """Ticks at the centre of each period's visible part, one per period.

    A period cut by the view is centred on what remains of it, so a wide
    period (a year over a few months) keeps its label.
    """

    def __init__(self, edges: mdates.DateLocator, span: float):
        self.edges = edges
        self.span = span

    def __call__(self):
        low, high = sorted(self.axis.get_view_interval())
        self.edges.set_axis(self.axis)
        edges = self.edges.tick_values(
            mdates.num2date(low - self.span), mdates.num2date(high + self.span)
        )
        edges = np.unique(np.clip(np.asarray(edges, dtype=float), low, high))
        widths = np.diff(edges)
        # a sliver of a period at the view's edge has no room for its label
        keep = widths >= widths.max() * DATE_PERIOD_MIN_SHARE if len(widths) else []
        return list(((edges[:-1] + edges[1:]) / 2)[keep])


def _project_label(period: str, moment, origin) -> str:
    """M1, M2, … or Y1, Y2, … counted from the project origin."""

    months = _months_since(origin, moment)
    if period == GANTT_DATE_PERIOD.PROJECT_MONTH:
        return f"M{months + 1}"
    return f"Y{months // 12 + 1}"


def _period_formatter(period: str, fmt, tz=None, origin=None) -> mticker.FuncFormatter:
    """A period's label at its centre: the format given, else the period's own."""

    def label(value, _pos=None):
        moment = mdates.num2date(value, tz=tz)
        if not _auto_format(fmt):
            return moment.strftime(fmt)
        if period == GANTT_DATE_PERIOD.QUARTER:
            return f"Q{(moment.month - 1) // 3 + 1}"
        if period == GANTT_DATE_PERIOD.PROJECT_MONTH:
            return _project_label(period, moment, origin)
        return moment.strftime(DATE_PERIOD_LABELS[period])

    return mticker.FuncFormatter(label)


def _apply_date_period(
    ax, axis_name: str, period: str, fmt, tz=None, origin=None, bounds=None
) -> None:
    """Divide a date axis into calendar periods (ADR 0049).

    Minor ticks mark the period edges and carry the grid lines; major ticks
    label each period at its centre. The enclosing period names its span in
    a row beneath, drawn on a secondary axis offset by one label row. Project
    months count from `origin`, the project start, under their project year.
    `bounds`, the schedule's (start, end) with a fixed limit as None, snaps
    the free ends of the view to the enclosing period edges, so every period
    shows whole and the labels sit evenly.
    """

    axis = getattr(ax, f"{axis_name}axis")
    if bounds is not None:
        _snap_to_periods(ax, axis_name, period, tz, origin, bounds)
    axis.set_minor_locator(_period_edges(period, tz, origin))
    axis.set_minor_formatter(mticker.NullFormatter())
    axis.set_major_locator(
        PeriodCentres(_period_edges(period, tz, origin), DATE_PERIOD_SPAN[period])
    )
    axis.set_major_formatter(_period_formatter(period, fmt, tz, origin))
    params = axis.get_tick_params(which="major")
    # the edge marks take the major tick look the furniture gave the axis
    edge_marks = {k: params[k] for k in ("length", "width", "color") if k in params}
    edge_marks.setdefault("length", mpl.rcParams[f"{axis_name}tick.major.size"])
    axis.set_tick_params(which="minor", **edge_marks)
    axis.set_tick_params(which="major", length=0)

    parent = DATE_PERIOD_PARENT[period]
    if parent is None:
        return
    size = params.get("labelsize", mpl.rcParams[f"{axis_name}tick.labelsize"])
    size = FontProperties(size=size).get_size_in_points()
    location = "bottom" if axis_name == "x" else "left"
    secondary = (
        ax.secondary_xaxis(location)
        if axis_name == "x"
        else ax.secondary_yaxis(location)
    )
    other = getattr(secondary, f"{axis_name}axis")
    other.set_major_locator(
        PeriodCentres(_period_edges(parent, tz, origin), DATE_PERIOD_SPAN[parent])
    )

    def parent_label(value, _pos=None):
        moment = mdates.num2date(value, tz=tz)
        if parent == PROJECT_YEAR:
            return _project_label(parent, moment, origin)
        return moment.strftime(DATE_PARENT_LABELS[parent])

    other.set_major_formatter(mticker.FuncFormatter(parent_label))
    other.set_tick_params(
        length=0,
        pad=params.get("pad", mpl.rcParams[f"{axis_name}tick.major.pad"])
        + size * DATE_PARENT_ROW_SPACING,
        labelsize=size,
        **({"labelcolor": params["labelcolor"]} if "labelcolor" in params else {}),
    )
    for spine in secondary.spines.values():
        spine.set_visible(False)


def _shared_data_interval(ax, axis_name: str) -> tuple:
    """The data range of an axis, across every axes that shares it."""

    intervals = [
        getattr(a.dataLim, f"interval{axis_name}")
        for a in ax._shared_axes[axis_name].get_siblings(ax)
    ]
    intervals = [i for i in intervals if np.isfinite(i).all()]
    if not intervals:
        return tuple(sorted(getattr(ax, f"{axis_name}axis").get_data_interval()))
    return min(min(i) for i in intervals), max(max(i) for i in intervals)


def _snap_limits_to_ticks(
    ax, axis_name: str, fixed=(False, False), data_ends: bool = True
) -> bool:
    """Move an axis's free view ends outward to its locator's ticks.

    A continuous axis then starts and ends on a tick. Only an automatic
    locator on a linear scale qualifies: a fixed tick set (a category axis,
    user ticks) or a log-family scale keeps its view, as does a user limit.
    With `data_ends`, an end whose data already sits on a tick and is
    overshot by the autoscale margin alone stops on that tick: the margin
    never adds a whole step, while headroom added on purpose still does.
    Returns whether a free end now lands on the data, so the marks there
    can draw whole.
    """

    axis = getattr(ax, f"{axis_name}axis")
    if all(fixed) or axis.get_scale() != "linear":
        return False
    # a polar r axis wraps its locator
    locator = getattr(axis.get_major_locator(), "base", axis.get_major_locator())
    if not isinstance(locator, (mticker.MaxNLocator, mdates.AutoDateLocator)):
        return False
    lo, hi = sorted(axis.get_view_interval())
    if not np.isfinite([lo, hi]).all() or hi <= lo:
        return False
    dated = isinstance(locator, mdates.AutoDateLocator)
    data_lo, data_hi = _shared_data_interval(ax, axis_name)
    # the overshoot the autoscale margin alone accounts for at each end
    margin = (
        (ax.get_xmargin() if axis_name == "x" else ax.get_ymargin())
        * (data_hi - data_lo)
        * (1 + 1e-6)
    )
    lo_by_margin = data_ends and data_lo - lo <= margin
    hi_by_margin = data_ends and hi - data_hi <= margin

    def tick_values(vmin, vmax):
        if dated:
            vmin, vmax = (mdates.num2date(v, tz=locator.tz) for v in (vmin, vmax))
        return np.asarray(locator.tick_values(vmin, vmax), dtype=float)

    # a number locator's ticks enclose the view; a date locator's stop inside
    # it, so the grid is stepped outward and the ticks re-read until both
    # ends land on one
    new_lo, new_hi = lo, hi
    for _ in range(3):
        ticks = tick_values(new_lo, new_hi)
        if len(ticks) < 2:
            return False
        step = float(np.min(np.diff(ticks)))
        tol = step * 1e-6
        below, above = ticks[ticks <= new_lo + tol], ticks[ticks >= new_hi - tol]
        # the tick the data edge itself sits on, when there is one
        lo_on_data = ticks[np.isclose(ticks, data_lo, rtol=0, atol=tol)]
        hi_on_data = ticks[np.isclose(ticks, data_hi, rtol=0, atol=tol)]
        if not lo_by_margin:
            lo_on_data = lo_on_data[:0]
        if not hi_by_margin:
            hi_on_data = hi_on_data[:0]
        lo_next = (
            new_lo
            if fixed[0]
            else (
                float(lo_on_data[0])
                if len(lo_on_data)
                else (
                    float(below.max())
                    if len(below)
                    else ticks[0] - step * math.ceil((ticks[0] - new_lo - tol) / step)
                )
            )
        )
        hi_next = (
            new_hi
            if fixed[1]
            else (
                float(hi_on_data[0])
                if len(hi_on_data)
                else (
                    float(above.min())
                    if len(above)
                    else ticks[-1] + step * math.ceil((new_hi - ticks[-1] - tol) / step)
                )
            )
        )
        if (lo_next, hi_next) == (new_lo, new_hi):
            break
        new_lo, new_hi = lo_next, hi_next
    # the snap never crosses zero when the data does not: a margin dipping
    # below all-positive values rounds to zero, not a whole step under it
    if not fixed[0] and new_lo < 0 <= data_lo:
        new_lo = 0.0
    if not fixed[1] and new_hi > 0 >= data_hi:
        new_hi = 0.0
    on_data = data_ends and (
        (not fixed[0] and math.isclose(new_lo, data_lo, abs_tol=tol))
        or (not fixed[1] and math.isclose(new_hi, data_hi, abs_tol=tol))
    )
    if (new_lo, new_hi) == (lo, hi):
        return on_data
    bounds = (new_hi, new_lo) if axis.get_inverted() else (new_lo, new_hi)
    (ax.set_xlim if axis_name == "x" else ax.set_ylim)(*bounds)
    return on_data


def _snap_to_periods(ax, axis_name, period, tz, origin, bounds) -> None:
    """Extend the free view ends to the period edges enclosing the schedule."""

    axis = getattr(ax, f"{axis_name}axis")
    lo, hi = sorted(axis.get_view_interval())
    start, end = bounds
    edges = _period_edges(period, tz, origin)
    edges.set_axis(axis)
    span = DATE_PERIOD_SPAN[period]
    reach = (start if start is not None else lo, end if end is not None else hi)
    ticks = np.asarray(
        edges.tick_values(
            mdates.num2date(reach[0] - span, tz=tz),
            mdates.num2date(reach[1] + span, tz=tz),
        ),
        dtype=float,
    )
    if start is not None:
        below = ticks[ticks <= start]
        lo = below.max() if len(below) else start
    if end is not None:
        above = ticks[ticks >= end]
        hi = above.min() if len(above) else end
    (ax.set_xlim if axis_name == "x" else ax.set_ylim)(lo, hi)


def _normalize_sizes(
    sizes: np.ndarray, size_range: tuple, extent: Optional[tuple] = None
) -> np.ndarray:
    """Map size values from `extent` (default: their own) onto the (min, max) range."""

    min_size, max_size = size_range
    lo, hi = extent if extent is not None else (sizes.min(), sizes.max())
    if hi == lo:
        return np.full_like(sizes, (min_size + max_size) / 2, dtype=float)
    normalized = (sizes - lo) / (hi - lo)
    return normalized * (max_size - min_size) + min_size


def _size_extents(layers_on_axes) -> dict:
    """The (min, max) of every scatter layer's size data, pooled per axes.

    One bubble scale per axes, so an equal size draws equal in every hue
    group and every composed figure.
    """

    extents = {}
    for layer, owner_ax in layers_on_axes:
        if not isinstance(layer, ScatterLayer):
            continue
        sizes = get_chart_data("size", layer.chart)
        if sizes is None or len(sizes) == 0:
            continue
        lo, hi = float(np.min(sizes)), float(np.max(sizes))
        if owner_ax in extents:
            lo, hi = min(lo, extents[owner_ax][0]), max(hi, extents[owner_ax][1])
        extents[owner_ax] = (lo, hi)
    return extents


def _resolve_ref_lines(chart: dict, key: str) -> List[tuple]:
    """Resolve v/h reference-line styles at build time."""

    lines = chart.get(key)
    if lines is None:
        return []
    lines = lines if isinstance(lines, list) else [lines]
    get_style = get_vline_style if key == "vlines" else get_hline_style
    return [(line, get_style(line.get("style", {}))) for line in lines]


# per side: the bound keys and the style resolver; on polar a vspan is
# bounded in degrees, an hspan in radius
SPAN_SIDES = {
    "vspans": ("xmin", "xmax", get_vspan_style),
    "hspans": ("ymin", "ymax", get_hspan_style),
}
# the layer attributes holding pre-resolved references, pooled per axes
REF_KEYS = ("vlines", "hlines", "vspans", "hspans", "texts")
# polar wedge outline samples per degree: enough for the chord error to vanish
SPAN_SAMPLES_PER_DEGREE = 2


def _resolve_ref_spans(chart: dict, key: str, muted_color: str) -> List[tuple]:
    """Resolve v/h reference-band styles at build time (ADR 0036)."""

    spans = chart.get(key)
    if spans is None:
        return []
    spans = spans if isinstance(spans, list) else [spans]
    lo_key, hi_key, get_style = SPAN_SIDES[key]
    resolved = []
    for span in spans:
        validate_span_bounds(span, lo_key, hi_key)
        style = get_style(span.get("style") or {})
        # an unset color sits behind the data without competing with the cycle
        style.setdefault("facecolor", muted_color)
        if style.get("hatch") and "edgecolor" not in style:
            # a hatch draws in the edge color, and an unset edge is transparent
            style["edgecolor"] = style["facecolor"]
        resolved.append((span, style))
    return resolved


def _span_bounds(span: dict, key: str, limits: tuple) -> tuple:
    """A band's (lower, upper) bounds, an omitted one falling back to the limit."""

    lo_key, hi_key, _ = SPAN_SIDES[key]
    lo = span.get(lo_key)
    hi = span.get(hi_key)
    return (limits[0] if lo is None else lo, limits[1] if hi is None else hi)


TEXT_COORDS = ("data", "axes")
# annotations sit above the data marks (zorder 3), below the panel furniture
TEXT_ANNOTATION_ZORDER = 5
# reference lines sit above every mark (zorder 3), below annotations (ADR 0054)
REF_LINE_ZORDER = 3.5
# connector placement (ADR 0018): the bow side and depth are chosen at draw
# time against the panel's data, unless plot_text_arrow_curve pins them
TEXT_BOW_CANDIDATES = (0.2, -0.2, 0.35, -0.35, 0.5, -0.5)
# beyond this clearance (px) an arc is "clear of the data"; flatter wins
TEXT_BOW_CLEARANCE_CAP = 14.0
# the final approach always meets the data at the target: score the body only
TEXT_BOW_BODY = 0.75
# approximate half-extent of the text box (px), for connector-length checks
TEXT_BOX_PAD = 18.0
# short connectors (px past the box) straighten with tiny gaps, then vanish
TEXT_SHORT_STRAIGHT = 40.0
TEXT_SHORT_NONE = 14.0
TEXT_SHORT_GAP = 1.5


def _facing_relpos(start: np.ndarray, target: np.ndarray) -> tuple:
    """The point on the text box border facing the target, as box fractions."""

    dx, dy = target - start
    if dx == 0 and dy == 0:
        return (0.5, 0.5)
    if abs(dx) >= abs(dy):
        return (1.0 if dx > 0 else 0.0, min(max(0.5 + 0.5 * dy / abs(dx), 0.0), 1.0))
    return (min(max(0.5 + 0.5 * dx / abs(dy), 0.0), 1.0), 1.0 if dy > 0 else 0.0)


def _arc_points(start: np.ndarray, target: np.ndarray, rad: float) -> np.ndarray:
    """Sample the arc3 connector path; positive rad bulges clockwise."""

    span = target - start
    length = np.hypot(*span)
    if length == 0:
        return start[None, :]
    perp = np.array([-span[1], span[0]]) / length
    control = (start + target) / 2 - rad * length * perp
    t = np.linspace(0.0, TEXT_BOW_BODY, 24)[:, None]
    return (1 - t) ** 2 * start + 2 * t * (1 - t) * control + t**2 * target


def _bow_rad(start: np.ndarray, target: np.ndarray, clearance_pts, bbox) -> float:
    """The candidate bow with the most open space; flatter wins past the cap.

    An arc that leaves the axes loses to any arc that stays inside.
    """

    def score(rad):
        pts = _arc_points(start, target, rad)
        inside = (
            (pts[:, 0] >= bbox.x0)
            & (pts[:, 0] <= bbox.x1)
            & (pts[:, 1] >= bbox.y0)
            & (pts[:, 1] <= bbox.y1)
        )
        clearance = TEXT_BOW_CLEARANCE_CAP
        if clearance_pts is not None and len(clearance_pts):
            gaps = np.hypot(
                pts[:, None, 0] - clearance_pts[None, :, 0],
                pts[:, None, 1] - clearance_pts[None, :, 1],
            )
            clearance = min(float(gaps.min()), TEXT_BOW_CLEARANCE_CAP)
        return (float(inside.mean()), clearance, -abs(rad))

    return max(TEXT_BOW_CANDIDATES, key=score)


def _densify(pts: np.ndarray, k: int = 4) -> np.ndarray:
    """Add interior samples along each polyline segment."""

    if len(pts) < 2:
        return pts
    t = np.linspace(0.0, 1.0, k, endpoint=False)[1:]
    segments = pts[1:] - pts[:-1]
    extra = (pts[:-1, None, :] + t[None, :, None] * segments[:, None, :]).reshape(-1, 2)
    return np.vstack([pts, extra])


def _layer_clearance_xy(layer: "Layer", transpose: bool):
    """The layer's data as (x, y) pairs in its drawing orientation, or None."""

    if layer.kind == "bar":
        y = get_chart_data("y", layer.chart)
        if y is None:
            return None
        xy = np.column_stack([np.arange(len(y), dtype=float), y])
        return xy[:, ::-1] if layer.is_horizontal else xy
    if layer.kind not in ("line", "scatter"):
        return None
    x = get_chart_data("x", layer.chart)
    y = get_chart_data("y", layer.chart)
    if x is None or y is None or len(x) != len(y):
        return None
    xy = np.column_stack([x, y]).astype(float)
    if transpose and layer.is_horizontal is None:
        xy = xy[:, ::-1]
    return _densify(xy) if layer.kind == "line" else xy


# build-time resolution keeps texts on the reference-line seam (ADR 0018)
def _resolve_texts(chart: dict) -> List[tuple]:
    """Resolve text annotation styles at build time."""

    texts = chart.get("texts")
    if texts is None:
        return []
    texts = texts if isinstance(texts, list) else [texts]
    resolved = []
    for text in texts:
        style = text.get("style") or {}
        resolved.append(
            (
                text,
                {
                    "font": get_plot_text_style(style),
                    "bbox": get_plot_text_box_style(style),
                    "arrowprops": get_plot_text_arrow_style(style),
                },
            )
        )
    return resolved


def _data_point(ax: plt.Axes, point) -> tuple:
    """A data position in axis units, so dates and categories can transform.

    An axis without units keeps the raw value: converting would install a
    converter that disagrees with the positions its marks already use.
    """

    return tuple(
        axis.convert_units(value) if axis.have_units() else value
        for axis, value in zip((ax.xaxis, ax.yaxis), point)
    )


def _draw_texts(
    ax: plt.Axes, texts: List[tuple], data_ax: plt.Axes = None, clearance=None
) -> None:
    """Draw the pre-resolved text annotations.

    The artists land on `ax` — the panel's topmost axes, so they cover
    twin-axis marks — while data coordinates read from `data_ax`, the
    owning layer's axes. `clearance` holds the panel's data in display
    coordinates; a curved connector left on its default bows toward the
    side with the most open space.
    """

    data_ax = data_ax if data_ax is not None else ax
    for text, style in texts:
        content = text.get("text")
        x, y = text.get("x"), text.get("y")
        if content is None or x is None or y is None:
            warnings.warn(
                "A text annotation requires the `text`, `x`, and `y` "
                "attributes. Skipping it..."
            )
            continue
        coords = text.get("coords") or "data"
        if coords not in TEXT_COORDS:
            raise ValueError(
                f"Invalid text `coords` value {coords!r}. "
                f"Must be one of {list(TEXT_COORDS)}."
            )
        # the host and its twin share the axes rectangle, so axes fractions
        # need no owner transform
        textcoords = data_ax.transData if coords == "data" else "axes fraction"
        if coords == "data":
            x, y = _data_point(data_ax, (x, y))

        kwargs = dict(style["font"])
        kwargs["zorder"] = TEXT_ANNOTATION_ZORDER
        if style["bbox"] is not None:
            kwargs["bbox"] = dict(style["bbox"])

        target = text.get("target")
        if target is None:
            ax.annotate(content, xy=(x, y), xycoords=textcoords, **kwargs)
            continue
        target = _data_point(data_ax, target)

        text_tr = data_ax.transData if coords == "data" else ax.transAxes
        start = np.asarray(text_tr.transform((x, y)), dtype=float)
        end = np.asarray(data_ax.transData.transform(target), dtype=float)
        length = np.hypot(*(end - start)) - TEXT_BOX_PAD

        # a connector shorter than the gaps that frame it is pure noise
        if length < TEXT_SHORT_NONE:
            ax.annotate(content, xy=(x, y), xycoords=textcoords, **kwargs)
            continue

        arrowprops = dict(style["arrowprops"])
        curve = arrowprops.pop("curve")
        pinned = arrowprops.pop("curve_pinned")
        if length < TEXT_SHORT_STRAIGHT:
            rad = 0.0
            arrowprops["shrinkA"] = min(arrowprops["shrinkA"], TEXT_SHORT_GAP)
            arrowprops["shrinkB"] = min(arrowprops["shrinkB"], TEXT_SHORT_GAP)
        elif curve and not pinned:
            rad = _bow_rad(start, end, clearance, ax.bbox)
        else:
            rad = curve
        arrowprops["connectionstyle"] = f"arc3,rad={rad}"
        # leave the box from the side facing the target, never under the text
        arrowprops["relpos"] = _facing_relpos(start, end)
        arrowprops["zorder"] = TEXT_ANNOTATION_ZORDER
        # the text bbox becomes patchA, so the connector never crosses the
        # box border (flush at gap 0, the TOUCHING look)
        ax.annotate(
            content,
            xy=target,
            xycoords=data_ax.transData,
            xytext=(x, y),
            textcoords=textcoords,
            arrowprops=arrowprops,
            **kwargs,
        )


def _draw_ref_lines(ax: plt.Axes, vlines: List[tuple], hlines: List[tuple]) -> None:
    """Draw the pre-resolved vertical and horizontal reference lines."""

    default_ymin, default_ymax = ax.get_ylim()
    for vline, style in vlines:
        x = vline.get("x")
        if x is None:
            warnings.warn(
                "The attribute `x` is not specified. Please provide the `x` value."
            )
            continue
        ax.vlines(
            x=x,
            ymin=vline.get("ymin", default_ymin),
            ymax=vline.get("ymax", default_ymax),
            label=vline.get("label", ""),
            **{"zorder": REF_LINE_ZORDER, **style},
        )
    # a line running to the limits must not widen them under autoscale
    if any(v.get("ymin") is None or v.get("ymax") is None for v, _ in vlines):
        ax.set_ylim(default_ymin, default_ymax)

    default_xmin, default_xmax = ax.get_xlim()
    for hline, style in hlines:
        y = hline.get("y")
        if y is None:
            warnings.warn(
                "The attribute `y` is not specified. Please provide the `y` value."
            )
            continue
        ax.hlines(
            y=y,
            xmin=hline.get("xmin", default_xmin),
            xmax=hline.get("xmax", default_xmax),
            label=hline.get("label", ""),
            **{"zorder": REF_LINE_ZORDER, **style},
        )
    if any(h.get("xmin") is None or h.get("xmax") is None for h, _ in hlines):
        ax.set_xlim(default_xmin, default_xmax)


def _draw_ref_spans(
    ax: plt.Axes,
    vspans: List[tuple],
    hspans: List[tuple],
    polar: bool,
    value_ax: Optional[plt.Axes] = None,
) -> None:
    """Draw the pre-resolved reference bands on the host axes (ADR 0036).

    Cartesian bands are `axvspan` / `axhspan`; on a polar axes a vertical
    band is a wedge over the full radius and a horizontal one an annulus over
    the full circle, both via `fill_between` because the span helpers measure
    their perpendicular extent in axes fractions. An omitted bound falls back
    to the axis limit, and that limit is then pinned so the band meets the
    axes edge instead of the autoscale margin pushing the edge away from it.
    The polar r limits are always pinned: the radial furniture already read
    them, so a band never moves the ring the donut hole was cut from.
    A band of a twin's figure passes the twin as `value_ax`: its bounds are
    measured there while it still draws on the host, under both axes' marks.
    """

    if not (vspans or hspans):
        return

    if polar:
        rlim = ax.get_ylim()
        for vspan, style in vspans:
            lo, hi = _span_bounds(vspan, "vspans", (0.0, 360.0))
            if hi < lo:
                # a wedge through the start angle wraps the long way round
                hi += 360.0
            samples = max(2, int(SPAN_SAMPLES_PER_DEGREE * (hi - lo)) + 1)
            theta = np.deg2rad(np.linspace(lo, hi, samples))
            ax.fill_between(theta, *rlim, label=vspan.get("label", ""), **style)
        theta = np.linspace(0, 2 * np.pi, SPAN_SAMPLES_PER_DEGREE * 360 + 1)
        for hspan, style in hspans:
            lo, hi = _span_bounds(hspan, "hspans", rlim)
            ax.fill_between(theta, lo, hi, label=hspan.get("label", ""), **style)
        ax.set_ylim(rlim)
        return

    data_ax = ax if value_ax is None else value_ax
    for key, spans in (("vspans", vspans), ("hspans", hspans)):
        along_x = key == "vspans"
        lo_key, hi_key, _ = SPAN_SIDES[key]
        limits = data_ax.get_xlim() if along_x else data_ax.get_ylim()
        for span, style in spans:
            lo, hi = _span_bounds(span, key, limits)
            label = span.get("label", "")
            if data_ax is ax:
                (ax.axvspan if along_x else ax.axhspan)(lo, hi, label=label, **style)
                continue
            # the band spans the host's frame but is measured on the twin
            if along_x:
                trans = blended_transform_factory(data_ax.transData, ax.transAxes)
                rect = Rectangle((lo, 0), hi - lo, 1, label=label, **style)
            else:
                trans = blended_transform_factory(ax.transAxes, data_ax.transData)
                rect = Rectangle((0, lo), 1, hi - lo, label=label, **style)
            rect.set_transform(trans)
            ax.add_patch(rect)
        if any(sp.get(lo_key) is None or sp.get(hi_key) is None for sp, _ in spans):
            (data_ax.set_xlim if along_x else data_ax.set_ylim)(limits)


def _hide_marks_past_limits(ax: plt.Axes, limits: dict, marks: list) -> None:
    """Hide the unclipped marks anchored past a limit the user set.

    Auto limits keep a mark overflowing the axes edge on purpose; a user
    limit crops the data, and a mark left beside the axes names nothing.
    """

    ends = {"x": sorted(ax.get_xlim()), "y": sorted(ax.get_ylim())}
    for artist, anchor in marks:
        for name, value in zip("xy", anchor):
            lo, hi = ends[name]
            if (limits[f"{name}min"] is not None and value < lo) or (
                limits[f"{name}max"] is not None and value > hi
            ):
                artist.set_visible(False)


def _draw_legend(
    ax: plt.Axes,
    ax_right: Optional[plt.Axes],
    legend_style: dict,
    handles: list,
    labels: Optional[list] = None,
) -> Legend:
    """Draw the legend on the panel's topmost axes.

    A twin axes renders entirely above its host, so a legend on the host would
    sit under every right-axis mark. matplotlib scores ``loc="best"`` against
    the legend's own axes only; with a twin, the scoring is widened to both
    through its private ``_auto_legend_data`` hook.
    """

    top_ax = ax if ax_right is None else ax_right
    entries = (
        {"handles": handles}
        if labels is None
        else {"handles": handles, "labels": labels}
    )
    legend = top_ax.legend(**entries, **legend_style)
    # matplotlib leaves the title in rc text.color; the label color covers it
    if isinstance(legend_style.get("labelcolor"), str):
        legend.get_title().set_color(legend_style["labelcolor"])
    if ax_right is None:
        return legend

    own_axes_data = legend._auto_legend_data

    def both_axes_data(*args):
        bboxes, lines, offsets = [], [], []
        try:
            for axes in (ax, ax_right):
                legend.parent = axes
                b, l, o = own_axes_data(*args)
                bboxes += b
                lines += l
                offsets += list(o)
        finally:
            legend.parent = top_ax
        return bboxes, lines, offsets

    legend._auto_legend_data = both_axes_data
    return legend


def _legend_obstacles(legend, axes, renderer):
    """The marks and texts a legend must clear, in display coordinates."""

    bboxes, lines, offsets = legend._auto_legend_data(renderer)
    texts = [
        t.get_window_extent(renderer)
        for a in axes
        for t in a.texts
        if t.get_visible() and t.get_text()
    ]
    return list(bboxes) + texts, list(lines), np.asarray(offsets).reshape(-1, 2)


def _legend_overlaps(box, bboxes, lines, offsets) -> bool:
    return bool(
        any(box.overlaps(b) for b in bboxes)
        or any(
            box.count_contains(l.vertices) or l.intersects_bbox(box, filled=False)
            for l in lines
        )
        or box.count_contains(offsets)
    )


def _marks_reach(slot, dim, bboxes, lines, offsets):
    """How far the marks under a slot extend along the value axis `dim`.

    Only marks within the slot's span across the other axis count: bar boxes
    and texts by their far edge, polylines by their vertices and by where a
    segment crosses the span's edges, markers by their centre.
    """

    cross = 1 - dim
    lo, hi = slot.get_points()[:, cross]
    reach = []
    for b in bboxes:
        pts = b.get_points()
        if pts[1, cross] > lo and pts[0, cross] < hi:
            reach.append(pts[1, dim])
    for line in lines:
        v = line.vertices
        if len(v) == 0:
            continue
        inside = (v[:, cross] >= lo) & (v[:, cross] <= hi)
        if inside.any():
            reach.append(v[inside, dim].max())
        a, b = v[:-1], v[1:]
        for edge in (lo, hi):
            straddle = (a[:, cross] - edge) * (b[:, cross] - edge) < 0
            if straddle.any():
                t = (edge - a[straddle, cross]) / (
                    b[straddle, cross] - a[straddle, cross]
                )
                reach.append(
                    (a[straddle, dim] + t * (b[straddle, dim] - a[straddle, dim])).max()
                )
    if len(offsets):
        inside = (offsets[:, cross] >= lo) & (offsets[:, cross] <= hi)
        if inside.any():
            reach.append(offsets[inside, dim].max())
    return max(reach) if reach else None


def _fit_legend(legend: Legend, axes: list, dim: int, renderer) -> None:
    """Give a best-placed legend a clear slot at the end of the value axis.

    matplotlib picks the least-covered slot, which still hides marks when they
    fill the axes. The legend then moves to the slot along the value-axis end
    (top for a vertical panel, right for a horizontal one) whose marks reach
    least far, and every axes extends its value range so those marks end below
    the legend. Runs at draw time, once constrained layout has sized the axes.
    A fit that would squeeze the marks past LEGEND_HEADROOM_MAX keeps
    matplotlib's slot; the translucent frame still shows what it covers.
    """

    if legend._loc != 0:
        return
    bboxes, lines, offsets = _legend_obstacles(legend, axes, renderer)
    box = legend.get_window_extent(renderer)
    if not _legend_overlaps(box, bboxes, lines, offsets):
        return

    pad = _legend_pad_px(legend.figure)
    size = Bbox.from_bounds(0, 0, box.width, box.height)
    anchor = legend.get_bbox_to_anchor()
    names = (
        ("upper left", "upper right", "upper center")
        if dim == 1
        else ("upper right", "lower right", "center right")
    )
    a0, a1 = legend.axes.bbox.get_points()[:, dim]
    best = None
    for name in names:
        code = Legend.codes[name]
        l, b = legend._get_anchored_bbox(code, size, anchor, renderer)
        slot = Bbox.from_bounds(l, b, box.width, box.height)
        reach = _marks_reach(slot, dim, bboxes, lines, offsets)
        reach = a0 if reach is None else min(reach, a1)
        floor = slot.get_points()[0, dim] - pad
        if floor <= a0:
            continue
        # scale the value range so the marks' reach maps just below the legend
        factor = max(1.0, (reach - a0) / (floor - a0))
        if best is None or factor < best[0]:
            best = (factor, code)
    if best is None or best[0] - 1 > LEGEND_HEADROOM_MAX:
        return
    factor, code = best
    for a in axes:
        axis = a.yaxis if dim == 1 else a.xaxis
        trans = axis.get_transform()
        lo, hi = trans.transform(a.get_ylim() if dim == 1 else a.get_xlim())
        lo, hi = trans.inverted().transform([lo, lo + (hi - lo) * factor])
        (a.set_ylim if dim == 1 else a.set_xlim)(lo, hi)
    legend._set_loc(code)


def _fit_outside_legend(legend: Legend, axes: list, renderer) -> None:
    """Move an outside legend past the tick labels and axis labels on its side.

    An outside location anchors to the axes edge, where the axis furniture
    lives. Once layout has sized the axes, the legend shifts outward by the
    furniture's overhang on that side, as a fixed offset in inches so the
    re-layout that makes room for it keeps the gap.
    """

    box = legend.get_window_extent(renderer)
    ax_box = legend.axes.bbox
    legend.set_in_layout(False)
    try:
        furniture = Bbox.union([ax.get_tightbbox(renderer) for ax in axes])
    finally:
        legend.set_in_layout(True)
    if box.x0 >= ax_box.x1:
        shift, direction = furniture.x1 - ax_box.x1, (1, 0)
    elif box.x1 <= ax_box.x0:
        shift, direction = ax_box.x0 - furniture.x0, (-1, 0)
    elif box.y0 >= ax_box.y1:
        shift, direction = furniture.y1 - ax_box.y1, (0, 1)
    elif box.y1 <= ax_box.y0:
        shift, direction = ax_box.y0 - furniture.y0, (0, -1)
    else:
        return
    if shift <= 0:
        return
    inches = (shift + _legend_pad_px(legend.figure)) / legend.figure.dpi
    offset = ScaledTranslation(
        direction[0] * inches, direction[1] * inches, legend.figure.dpi_scale_trans
    )
    # the anchor reads back in display space; the offset hangs off its
    # axes-fraction position so the re-layout keeps the gap
    anchor = legend.axes.transAxes.inverted().transform(legend.get_bbox_to_anchor().p0)
    legend.set_bbox_to_anchor(tuple(anchor), transform=legend.axes.transAxes + offset)


def _legend_pad_px(figure) -> float:
    return LEGEND_HEADROOM_PAD_PT * figure.dpi / 72.0


def _defer_legend_fit(ax: plt.Axes, fit) -> None:
    """Queue a legend fit for the figure's first draw, once layout has run."""

    ax.figure.__dict__.setdefault("_legend_fits", []).append(fit)


# ================================================
# DrawContext
# ================================================


@dataclass(frozen=True)
class BarSlot:
    """A bar layer's placement within the panel-wide bar arrangement."""

    offset: float = 0.0
    width: Optional[float] = None
    bottom: Optional[np.ndarray] = None
    show_yerr: bool = True


@dataclass(frozen=True)
class HistSlot:
    """A histogram layer's precomputed heights and offset within the panel stack."""

    bins: np.ndarray
    heights: np.ndarray
    bottom: np.ndarray


@dataclass(frozen=True)
class StackSlot:
    """A stacked area layer's band within the panel-wide stack (ADR 0025)."""

    bottom: np.ndarray
    top: np.ndarray


@dataclass(frozen=True)
class DrawContext:
    """Frozen per-layer instructions a Panel hands to a Layer at draw time."""

    color: Optional[str] = None
    z_order: Optional[float] = None
    legend_label: Optional[str] = None
    alpha: Optional[float] = None
    bar_slot: Optional[BarSlot] = None
    hist_slot: Optional[HistSlot] = None
    stack_slot: Optional[StackSlot] = None
    bins: Optional[np.ndarray] = None
    hatch: Optional[str] = None
    linestyle: Optional[Union[str, tuple]] = None
    # (marker, hollow) from the panel's marker cycle
    marker: Optional[tuple] = None
    emphasis: Optional[str] = None
    # the role a composition sets on the layer's figure; beats record roles
    panel_emphasis: Optional[str] = None
    parallel_stats: Optional[dict] = None
    parallel_axes: bool = True
    transpose: bool = False
    # label -> position of the panel's category axis (ADR 0020)
    category_index: Optional[dict] = None
    # the panel's only dumbbell layer wears the style's pair colors (ADR 0050)
    sole_dumbbell: bool = False
    # the panel pins its aspect ratio, so colorbars size to the axes box
    aspect_locked: bool = False
    # the resolved scales of the axes the layer draws on (ADR 0041)
    value_scale: Optional[str] = None
    category_scale: Optional[str] = None
    # the (min, max) size data every bubble on the axes maps from
    size_extent: Optional[tuple] = None


# ================================================
# Layers
# ================================================


def _oriented(ax: plt.Axes, transpose: bool) -> tuple:
    """The plot, fill and scatter calls of `ax`; x and y swapped when transposed."""

    if not transpose:
        return ax.plot, ax.fill_between, ax.scatter
    return (
        lambda x, y, **kw: ax.plot(y, x, **kw),
        ax.fill_betweenx,
        lambda x, y, **kw: ax.scatter(y, x, **kw),
    )


def _resolve_show_values(settings: dict) -> bool:
    """`show_values` as set, else the theme default for a front that takes it (ADR 0033)."""

    value = settings.get("show_values")
    if value is None and "show_values" in settings:
        value = config.get("chart_default_show_values")
    return bool(value)


class Layer:
    """One drawable unit; owns its resolved style, knows nothing about siblings."""

    # a continuous axis ends on a tick; a layer filling its whole field
    # (a heatmap, contour, or hexbin) keeps the axis tight to the field
    ticks_at_axis_ends = True

    kind: str = ""
    # None for layers without an orientation; they follow the panel
    is_horizontal: Optional[bool] = None
    # the coordinate space the layer draws in; a panel property (ADR 0015)
    projection: str = "cartesian"
    # a bare layer owns its axes: fixed limits, axis off, no panel furniture
    bare: bool = False
    # value labels sit past the mark on the value axis and need headroom there
    labels_past_mark: bool = False
    # value labels also sit below the value range, so the low end needs room
    labels_below_range: bool = False
    # one emphasis role per drawn record, on the layers whose records carry one
    record_roles: list = ()
    # marker records outrank the layer's own role; bar records yield to it
    record_roles_beat_layer = False
    # the zone of a temporal x column a layer draws as date numbers
    x_tz: Optional[tzinfo] = None
    # a filled background layer; a Panel overlay draws it under marks (ADR 0054)
    surface: bool = False
    # the edge the layer's drawn colorbar takes; None when it draws none
    colorbar_edge: Optional[str] = None

    def __init__(self, chart: dict, settings: dict):
        self.chart = chart
        # (artist, resolver) pairs registered by the draw in progress (ADR 0031)
        self._hover_targets = []
        # (artist, (x, y)) marks drawn past the axes, hidden past a user limit
        self._limit_marks = []
        self.settings = settings
        self.subtitle = chart.get("subtitle", None)
        self.style = chart.get("style", {}) or {}
        self.chart_hash = get_chart_hash(chart)
        self.vlines = _resolve_ref_lines(chart, "vlines")
        self.hlines = _resolve_ref_lines(chart, "hlines")
        self.texts = _resolve_texts(chart)
        self.emphasis = self._resolve_emphasis(chart.get("emphasis"))
        # snapshot at build so muting harmonizes with the layer's own theme
        muted_alpha = config.get("muted_alpha")
        self.muted_color = config.get("muted_color") or DEFAULT_MUTED_COLOR
        self.vspans = _resolve_ref_spans(chart, "vspans", self.muted_color)
        self.hspans = _resolve_ref_spans(chart, "hspans", self.muted_color)
        self.muted_alpha = DEFAULT_MUTED_ALPHA if muted_alpha is None else muted_alpha
        # the sketch halo around a series line (ADR 0027); None means off
        self.halo = get_sketch_halo(self.style)
        # the ink stroke on the same series lines (ADR 0048); None means off
        self.ink_stroke = get_ink_stroke(self.style)
        self.etch = get_etch(self.style)
        # a bare layer turns its axes off, so the figure is what lies behind it
        ground_key = "figure_facecolor" if self.bare else "axes_facecolor"
        self.ground = config.get(ground_key) or "#FFFFFF"
        # a value scale drawn in etched steps; only with the etch on
        self.value_etch_steps = get_value_etch(self.style) if self.etch else None
        # the ground halo of a value over value steps, as value labels take it
        self.value_halo = _halo_effects(
            get_value_label_style(self.style)["halo_width"], self.ground
        )
        self.step_legend_style = None
        if self.value_etch_steps:
            self.step_legend_style = {
                **get_legend_style({"location": LEGEND_LOCATION.OUTSIDE_RIGHT}),
                "family": resolve_font_family(),
            }
        self._resolve_style()

    def _resolve_emphasis(self, value):
        return validate_emphasis(value)

    def _colorbar_edge(self, shown) -> Optional[str]:
        """The resolved colorbar's edge, when shown; etched steps draw none."""
        if shown and not self.value_etch_steps:
            return self.colorbar["location"]
        return None

    def _resolve_style(self) -> None:
        """Collapse config → theme → chart style into concrete style dicts."""

    def _resolve_value_labels(self) -> None:
        """The `show_values` flag, value format, step, and label font (ADR 0033).

        One resolution serves every chart that prints values; only the
        placement differs per geometry.
        """

        self.show_values = _resolve_show_values(self.settings)
        value_format = self.settings.get("value_format")
        self.value_format = (
            DEFAULT_VALUE_LABEL_FORMAT if value_format is None else value_format
        )
        self.value_step = validate_value_step(self.settings.get("value_step"))
        style = get_value_label_style(self.style)
        self.value_padding = style["padding"]
        self.value_font = _value_label_font(style)

    def _label_bars(self, ax, bars, stacked: bool, **bar_label_kwargs) -> None:
        """Label a bar container past each bar's edge; inside it when stacked.

        A stacked segment's edge is the next segment's base, so an edge label
        would sit on the mark above it. `bar_label_kwargs` name the texts:
        `fmt` or `labels`, as `ax.bar_label` takes them.
        """

        ax.bar_label(
            bars,
            label_type="center" if stacked else "edge",
            padding=0 if stacked else self.value_padding,
            zorder=TEXT_ANNOTATION_ZORDER,
            **bar_label_kwargs,
            **self.value_font,
        )

    def _resolve_bare_labels(self) -> None:
        """The bare layers' label font and value labels.

        Their labels are drawn text in the general font; their values print
        as passed, so a whole number stays a whole number.
        """

        self._resolve_value_labels()
        self.label_style = get_text_style("general")
        if self.settings.get("value_format") is None:
            self.value_format = VALUE_FORMAT.DEFAULT
        # a bare layer strokes its values with its own label halo
        self.value_font.pop("path_effects")

    def _value_texts(self, ax, values, along_y: bool = False) -> np.ndarray:
        """One formatted value per mark, `None` where the step skips it.

        Without a `value_step` the step keeps the widest label from meeting
        its neighbours along the series axis, so a dense series stays legible.
        """

        texts = [_format_value(self.value_format, v) for v in values]
        step = self.value_step or _default_value_step(
            ax, texts, self.value_font["fontsize"], along_y
        )
        return np.array(
            [t if i % step == 0 else None for i, t in enumerate(texts)], dtype=object
        )

    def label(self, ctx: DrawContext) -> Optional[str]:
        return ctx.legend_label if ctx.legend_label is not None else self.subtitle

    def draw(self, ax: plt.Axes, ctx: DrawContext) -> None:
        raise NotImplementedError

    def register_hover(self, artist, resolver: Callable[[int], dict]) -> None:
        """Make `artist` a hover target: `resolver(i)` is the datum behind its i-th element.

        The datum is an ordered dict: the series' legend `label`, then the
        fields the mark stands for — `x`/`y` are the drawn axes' coordinates,
        any other key is shown as is — so `show(interactive=True)` annotates
        it without knowing the chart type. Called from `draw`; the panel
        collects the pairs right after.
        """

        self._hover_targets.append((artist, resolver))

    def register_patch_hover(self, marks: list) -> None:
        """Make loose `(patch, datum)` pairs one hover target picked by containment.

        mplcursors picks a lone patch by the distance to its outline, but a
        container's patches by containment — what a filled mark wants.
        """

        self.register_hover(
            BarContainer([patch for patch, _ in marks]), lambda i: marks[i][1]
        )

    def register_limit_mark(self, artist, x, y) -> None:
        """Hide an unclipped mark whose data anchor lies past a user limit."""

        self._limit_marks.append((artist, (x, y)))

    def take_limit_marks(self) -> list:
        """Hand over the marks registered by the last draw and forget them."""

        marks, self._limit_marks = self._limit_marks, []
        return marks

    def take_hover_targets(self) -> list:
        """Hand over the pairs registered by the last draw and forget them."""

        targets, self._hover_targets = self._hover_targets, []
        return targets

    def y_range(self) -> Optional[tuple]:
        """The (min, max) of the layer's y data, used for axis clustering."""
        return None

    def x_values(self):
        """The layer's x data column; None when it has none."""
        return None

    def value_data(self):
        """The raw values the layer plots on the value axis (issue #147).

        None when the layer plots none, or only derived ones (counts,
        densities, stacked tops), which a log scale never rejects.
        """
        return None

    def category_data(self):
        """The raw values the layer plots on the category axis; None without."""
        return self.x_values()

    def labels(self):
        """The layer's category labels; None for a layer without groups."""
        return None

    def x_kind(self) -> Optional[str]:
        """The kind of axis the layer's x data asks for (ADR 0037); None without x.

        Labelled groups sit on category positions whatever their labels hold.
        """

        if self.labels() is not None:
            return AXIS_CATEGORICAL
        return axis_kind(self.x_values())

    def value_kind(self) -> Optional[str]:
        """The kind of axis the layer's value column asks for; None by default.

        Only a layer that plots time along its value axis reports one (ADR 0049).
        """

        return None

    def date_label_axes(self) -> set:
        """The drawn axes ("x", "y") whose category labels are dates."""

        if axis_kind(self.labels()) != AXIS_TEMPORAL:
            return set()
        return {"y" if self.is_horizontal else "x"}

    def apply_scales(self, ax: plt.Axes, scalex, scaley) -> None:
        if scalex:
            ax.set_xscale(scalex)
        if scaley:
            ax.set_yscale(scaley)

    def _stroke_halo(self, line_style: dict) -> None:
        """Stroke the sketch halo under a series line, sized to its width."""

        halo = []
        if self.halo is not None:
            width = (line_style.get("linewidth") or 0) + self.halo
            # a line's halo wobbles with the line it cuts out
            halo = [patheffects.withStroke(linewidth=width, foreground=self.ground)]
        if self.ink_stroke is not None and halo:
            # the ribbon replaces the plain line withStroke redraws on top
            halo = [patheffects.Stroke(linewidth=width, foreground=self.ground)]
        if self.ink_stroke is not None:
            halo = halo + [InkStroke(**self.ink_stroke)]
        if halo:
            line_style["path_effects"] = halo

    def _apply_cycle_linestyle(self, line_style: dict, ctx: DrawContext) -> None:
        """Take the panel's cycle line style unless the chart style sets one."""

        if ctx.linestyle is not None and "plot_line_style" not in self.style:
            line_style["linestyle"] = ctx.linestyle

    def _apply_cycle_marker(self, scatter_style: dict, ctx: DrawContext) -> None:
        """Take the panel's cycle marker unless the chart style sets one.

        A hollow entry is drawn as an outline by `_hollow_marker`.
        """

        if ctx.marker is None or "plot_scatter_marker" in self.style:
            return
        marker, hollow = ctx.marker
        scatter_style["marker"] = marker
        if hollow:
            scatter_style["hollow"] = True

    def _etch(self, artists, wash: bool = True) -> None:
        """Etch the hatched fills among `artists` (ADR 0048); nothing when off.

        A fill under a line takes no wash, so what sits beneath stays visible.
        """

        if self.etch is None:
            return
        effect = self._etch_effect(self.etch.get("wash") if wash else None)
        for artist in artists:
            if artist is not None:
                artist.set_path_effects([effect])

    def _etch_effect(self, wash: Optional[float]) -> "Etch":
        return Etch(**{**self.etch, "wash": wash, "ground": self.ground})

    def _draw_value_steps(
        self,
        ax,
        steps: np.ndarray,
        collection_for: Callable,
        zorder: float,
        alphas: Optional[np.ndarray] = None,
    ) -> None:
        """One etched collection per value step, built for the marks at `steps == k`.

        `alphas`, one per mark, carries the emphasis fade over to the steps.
        """

        effect = self._etch_effect(1.0)
        for k, (wash, hatch) in enumerate(self.value_etch_steps):
            mask = steps == k
            if not mask.any():
                continue
            collection = collection_for(mask)
            collection.set(
                facecolor=wash,
                edgecolor="none",
                linewidth=0,
                hatch=hatch or None,
                zorder=zorder,
                gid="value-step",
                path_effects=[effect],
            )
            if alphas is not None:
                collection.set_alpha(alphas[mask])
            ax.add_collection(collection, autolim=False)

    def _draw_step_legend(self, ax, entries: list, title: Optional[str]) -> None:
        """A legend of `(step, label)` entries beside the axes, in place of a colorbar.

        Added as an artist, so a panel legend on the same axes keeps it.
        """

        effect = self._etch_effect(1.0)
        handles = [
            Patch(
                facecolor=self.value_etch_steps[k][0],
                edgecolor=self.etch["color"],
                linewidth=STEP_LEGEND_EDGE_WIDTH,
                hatch=self.value_etch_steps[k][1] or None,
                path_effects=[effect],
            )
            for k, _ in entries
        ]
        style = dict(self.step_legend_style)
        family = style.pop("family")
        style["title"] = title or None
        legend = Legend(ax, handles, [label for _, label in entries], **style)
        for text in legend.get_texts() + [legend.get_title()]:
            text.set_fontfamily(family)
        ax.add_artist(legend)
        # add_artist clips to the axes patch; the legend sits outside it
        legend.set_clip_on(False)
        _defer_legend_fit(
            ax, lambda renderer: _fit_outside_legend(legend, [ax], renderer)
        )

    def _draw_even_step_legend(self, ax, norm, title: Optional[str]) -> None:
        """The step legend of a normalized value scale: one entry per even step."""

        n = len(self.value_etch_steps)
        edges = norm.inverse(np.linspace(0, 1, n + 1))
        entries = [(k, _step_label(edges[k], edges[k + 1])) for k in range(n)]
        self._draw_step_legend(ax, entries, title)

    @staticmethod
    def _merge_color(color_key: str, ctx_color: Optional[str], style: dict) -> dict:
        """Cycle color first, resolved style overrides — same precedence as before."""
        merged = {color_key: ctx_color} if ctx_color is not None else {}
        merged.update(style)
        return merged

    def _apply_emphasis(
        self,
        style: dict,
        role: Optional[str],
        width_key: str = "linewidth",
        color_key: Optional[str] = "color",
    ) -> None:
        """Apply an emphasis role's color/stroke/alpha/z transform to a style dict."""

        if role is None:
            return
        style["zorder"] = style.get("zorder", 0) + EMPHASIS_Z_OFFSET[role]
        width = style.get(width_key)
        if role == EMPHASIS_BACKGROUND:
            style["alpha"] = self.muted_alpha
            if color_key is not None:
                style[color_key] = self.muted_color
            if width is not None:
                style[width_key] = width * MUTED_WIDTH_SCALE
        elif width is not None:
            style[width_key] = width * HIGHLIGHT_WIDTH_SCALE

    def draws_all_muted(self, role: Optional[str], panel_role: Optional[str]) -> bool:
        """Whether every mark draws muted, so the layer takes no color or legend."""

        if role != EMPHASIS_BACKGROUND:
            return False
        if panel_role is not None or not self.record_roles_beat_layer:
            return True
        return all(r in (None, EMPHASIS_BACKGROUND) for r in self.record_roles)

    def _marker_roles(self, unit_roles: list, ctx: DrawContext) -> list:
        """Each mark's role: the panel's, else its record's, else its unit's.

        `unit_roles` are the series' or group's roles, one per mark in record
        order; columnar data carries no records and keeps them.
        """

        if ctx.panel_emphasis is not None:
            return [ctx.panel_emphasis] * len(unit_roles)
        if len(self.record_roles) != len(unit_roles):
            return list(unit_roles)
        return [own or unit for own, unit in zip(self.record_roles, unit_roles)]

    def _record_roles(self, panel_role: Optional[str], n: int) -> list:
        """One role per drawn record; a layer-level role covers them all instead.

        Columnar data carries no records, so it draws `n` unset roles.
        """

        if panel_role is not None or len(self.record_roles) != n:
            return [None] * n
        return self.record_roles

    @staticmethod
    def _name_legend_patch(bars, roles: list) -> None:
        """Let the series' first unmuted bar stand for it in the legend."""

        unmuted = next(
            (p for p, role in zip(bars.patches, roles) if role != EMPHASIS_BACKGROUND),
            None,
        )
        if unmuted is not None:
            bars.legend_patch = unmuted

    def _apply_patch_emphasis(self, patches, roles: list) -> None:
        """Apply per-record roles to drawn patches (ADR 0042).

        The patches were drawn in the layer's style; a muted one takes the
        muted color, alpha, and stroke, a highlighted one the bolder stroke,
        and both step in z like a whole layer would.
        """

        for patch, role in zip(patches, roles):
            if role is None:
                continue
            patch.set_zorder(patch.get_zorder() + EMPHASIS_Z_OFFSET[role])
            if role == EMPHASIS_BACKGROUND:
                patch.set_facecolor(self.muted_color)
                patch.set_alpha(self.muted_alpha)
                patch.set_linewidth(patch.get_linewidth() * MUTED_WIDTH_SCALE)
            else:
                patch.set_linewidth(patch.get_linewidth() * HIGHLIGHT_WIDTH_SCALE)


def _is_bar_record(record, y_key: str) -> bool:
    """Whether a data entry is a dict carrying the `y_key` column, as a bar is."""

    return isinstance(record, dict) and y_key in record


def _keyed_records(chart: dict, column: str) -> list:
    """The chart's records carrying the `column` key; empty for columnar data."""

    key = get_attr_value(column, chart, column)
    data = chart.get("data")
    if not isinstance(data, list):
        return []
    return [record for record in data if _is_bar_record(record, key)]


def _bar_records(chart: dict) -> list:
    """The chart's drawn bar records; empty for columnar data."""

    return _keyed_records(chart, "y")


def _record_emphasis(chart: dict) -> list:
    """The validated per-record emphasis roles of a bar chart, one per drawn bar."""

    return _validated_record_roles(_bar_records(chart), "bar")


def _validated_record_roles(records: list, kind: str) -> list:
    """The validated `emphasis` of each record; None where it sets none."""

    return [
        validate_emphasis(record.get("emphasis"), f"{kind} record {i} `emphasis`")
        for i, record in enumerate(records)
    ]


def _axis_numbers(ax, transpose: bool, x) -> np.ndarray:
    """The drawn x data in axis units, so fits run on numbers when x is temporal."""

    axis = ax.yaxis if transpose else ax.xaxis
    return np.asarray(axis.convert_units(x), dtype=float)


def _point_resolver(label, x, y, transpose: bool) -> Callable[[int], dict]:
    """The hover resolver of a point series drawn from `x` and `y` arrays.

    The datum names the *drawn* axes: a transposed series (horizontal panel
    or bars) reports its `x` values under `y` and vice versa, so the axis
    labels on the artist's axes always describe the values.
    """

    def resolve(index: int) -> dict:
        x_val, y_val = _scalar(x[index]), _scalar(y[index])
        if transpose:
            x_val, y_val = y_val, x_val
        return {"label": label, "x": x_val, "y": y_val}

    return resolve


def _scalar(value):
    """A plain Python scalar for a numpy element; anything else as is."""

    return value.item() if isinstance(value, np.generic) else value


def _span_text(low, high, fmt=lambda value: f"{value:g}") -> str:
    """A `low – high` span, each end formatted by `fmt`."""

    return f"{fmt(low).strip()} – {fmt(high).strip()}"


def _axis_formatter(ax: plt.Axes, which: str) -> Callable:
    """The formatter the axis uses for its own coordinates."""

    return getattr(ax, f"format_{which}data")


def _nearest(positions, coordinate) -> int:
    """The index of the position closest to `coordinate`."""

    return int(np.nanargmin(np.abs(np.asarray(positions, dtype=float) - coordinate)))


def _vertex_coordinate(vertices: np.ndarray, index, axis: int) -> float:
    """The coordinate along `axis` of a picked outline vertex.

    A polygon collection picks `(polygon, vertex)`, a patch outline the
    vertex alone; either wraps around the closing vertex.
    """

    vertex = index[-1] if isinstance(index, tuple) else index
    return float(vertices[vertex % len(vertices)][axis])


def _column_range(chart: dict, attr: str) -> Optional[tuple]:
    """The (min, max) of a chart's data column; None when the column is absent."""

    values = get_chart_data(attr, chart)
    if values is None or len(values) == 0 or axis_kind(values) == AXIS_CATEGORICAL:
        return None
    return (minimum(values), maximum(values))


class PointLabelMixin:
    """Marks whose labels the panel places together, once every mark is drawn.

    A layer records its drawn points; the panel's collision-avoiding placer
    reads them back through `pending_labels` and tries `label_spots` around
    each mark in preference order.
    """

    label_spots = POINT_LABEL_SPOTS
    labels_past_mark = True
    # only the scatter layer reserves a correlation box among the obstacles
    show_correlation = False

    def _init_point_labels(self) -> None:
        # point labels wear the text font; alignment comes from their spot
        self.label_font = {
            k: v for k, v in get_plot_text_style({}).items() if k not in ("ha", "va")
        }
        # drawn points per axes, consumed by the panel's label placement
        self._pending_labels = {}

    def _record_points(
        self, ax, ctx, x, y, sizes, labels=None, font=None, pad=POINT_LABEL_PAD
    ) -> None:
        """Remember the drawn points so the panel can place their labels.

        `sizes` are marker areas in points squared; `pad` is the gap between
        a mark's edge and its label, in points.
        """

        if ctx.transpose:
            x, y = y, x
        font = dict(self.label_font if font is None else font)
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            font["color"] = self.muted_color
        self._pending_labels.setdefault(id(ax), []).append(
            (
                np.asarray(ax.xaxis.convert_units(x), dtype=float),
                np.asarray(ax.yaxis.convert_units(y), dtype=float),
                sizes,
                labels,
                font,
                pad,
            )
        )

    def pending_labels(self, ax) -> list:
        """The points drawn into `ax` as (x, y, sizes, labels, font, pad) tuples."""

        return self._pending_labels.pop(id(ax), [])

    def label_obstacles(self, ax) -> list:
        """Display-space boxes of the layer's other marks in `ax` the labels avoid."""

        return []


def _apply_cycle_hatch(style: dict, ctx: DrawContext) -> None:
    """Take the panel's cycle hatch unless the resolved style sets one."""

    if ctx.hatch is not None and "hatch" not in style:
        style["hatch"] = ctx.hatch or None


class AreaFillMixin:
    """The fill under a series line: cycle color and hatch, muted or not."""

    def _resolved_area_style(self, ctx):
        area_style = self._merge_color("color", ctx.color, self.area_style)
        if ctx.z_order is not None:
            area_style["zorder"] = ctx.z_order - 0.1
        _apply_cycle_hatch(area_style, ctx)
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            area_style["color"] = self.muted_color
        return area_style


class MarkClipBox(TransformedBbox):
    """The axes box grown by `pad` points along `dims`, read live with the layout."""

    def __init__(self, ax, pad: float, dims=("x", "y")):
        super().__init__(Bbox.unit(), ax.transAxes)
        self._figure, self._pad, self._dims = ax.figure, pad, tuple(dims)

    def get_points(self):
        pad = self._pad * self._figure.dpi / 72.0
        grow = [pad if "x" in self._dims else 0.0, pad if "y" in self._dims else 0.0]
        return super().get_points() + [[-grow[0], -grow[1]], grow]


def _mark_radius(line_style: dict) -> float:
    """Half the marker size of a line's points, or half its stroke when unmarked."""

    marker = line_style.get("marker")
    if marker in (None, "", "None", "none", " "):
        return (line_style.get("linewidth") or 1.0) / 2
    return (line_style.get("markersize") or plt.rcParams["lines.markersize"]) / 2


class LineLayer(PointLabelMixin, AreaFillMixin, Layer):
    kind = "line"
    label_spots = POINT_LABEL_SPOTS_VERTICAL

    def __init__(self, chart: dict, settings: dict):
        # the lines drawn per axes, so the panel can unclip their end markers
        self._lines = {}
        super().__init__(chart, settings)

    def _resolve_style(self):
        self.line_style = get_line_style(self.style)
        self.area_style = get_area_style(self.style)
        self.show_yerr = self.settings.get("show_yerr")
        self.show_area = self.settings.get("show_area")
        self._resolve_value_labels()
        self._init_point_labels()

    def y_range(self):
        return _column_range(self.chart, "y")

    def x_range(self):
        return _column_range(self.chart, "x")

    def x_values(self):
        return get_chart_data("x", self.chart)

    def value_data(self):
        return get_chart_data("y", self.chart)

    def unclip_marks(self, ax, dims=("x", "y")) -> None:
        """Let the markers on the `dims` edges draw whole, past the frame."""

        for line in self._lines.get(id(ax), ()):
            pad = line.get_markersize() / 2 + line.get_markeredgewidth()
            line.set_clip_path(None)
            line.set_clip_box(MarkClipBox(ax, pad, dims))

    def draw(self, ax, ctx):
        x = get_chart_data("x", self.chart)
        y = get_chart_data("y", self.chart)
        yerr = get_chart_data("yerr", self.chart)

        if x is None or y is None:
            return

        line_style = self._merge_color("color", ctx.color, self.line_style)
        if ctx.z_order is not None:
            line_style["zorder"] = ctx.z_order
        self._apply_cycle_linestyle(line_style, ctx)
        self._apply_emphasis(line_style, ctx.emphasis)
        self._stroke_halo(line_style)

        draw_yerr = (
            self.show_yerr and isinstance(yerr, np.ndarray) and len(yerr) == len(y)
        )

        plot, fill, _ = _oriented(ax, ctx.transpose)

        if draw_yerr:
            band = fill(x, y - yerr, y + yerr, **self._resolved_area_style(ctx))
            self._etch([band], wash=False)

        (line,) = plot(x, y, **line_style, label=self.label(ctx))
        self._lines.setdefault(id(ax), []).append(line)
        self.register_hover(line, _point_resolver(self.label(ctx), x, y, ctx.transpose))

        if self.show_values and ctx.emphasis != EMPHASIS_BACKGROUND:
            self._record_points(
                ax,
                ctx,
                x,
                y,
                (2 * _mark_radius(line_style)) ** 2,
                self._value_texts(ax, y, ctx.transpose),
                self.value_font,
                self.value_padding,
            )

        if self.show_area:
            drawstyle = line_style.get("drawstyle", "")
            step = drawstyle.split("-")[1] if "steps-" in drawstyle else None
            area = self._fill_to_floor(
                fill, ax, x, y, step, self._resolved_area_style(ctx)
            )
            self._etch([area], wash=False)

    @staticmethod
    def _fill_to_floor(fill, ax, x, y, step, area_style):
        """Fill under the line past any plausible axis floor, outside the autoscale.

        Returns the fill, or None when the line has no finite value.
        """

        values = np.asarray(y, dtype=float)
        values = values[np.isfinite(values)]
        if values.size == 0:
            return None
        floor = values.min() - AREA_FLOOR_FACTOR * max(np.abs(values).max(), 1.0)
        data_lim = ax.dataLim.frozen()
        collection = fill(x, y, floor, step=step, **area_style)
        ax.dataLim.set(data_lim)
        # the sketch filter would split the off-screen floor edge into millions
        # of wobble segments; the top edge sits under the line and its halo
        collection.set_sketch_params()
        return collection


# vertices per segment of a curved bump line
BUMP_CURVE_SAMPLES = 24
# the least gap between two period tick labels, in font sizes
PERIOD_LABEL_GAP = 0.5


class PeriodTicks(mticker.Locator):
    """One tick per period, thinned so the labels never touch.

    Every period is a tick when its labels fit along the axis; otherwise
    the first and last periods stay and a period drops out when its label
    would run into the previous kept one. Measured from the axis length at
    draw time, so a narrow subplot keeps fewer ticks than a wide figure.
    """

    def __init__(self, periods):
        self.periods = np.unique(np.asarray(periods, dtype=float))

    def __call__(self):
        return self.tick_values(*self.axis.get_view_interval())

    def tick_values(self, vmin, vmax):
        periods, axis = self.periods, self.axis
        span = abs(vmax - vmin)
        if axis is None or len(periods) < 3 or span <= 0:
            return periods
        along_x = axis.axis_name == "x"
        length = axis.axes.bbox.width if along_x else axis.axes.bbox.height
        if length <= 0:
            return periods
        size = FontProperties(
            size=axis.get_tick_params(which="major").get(
                "labelsize", mpl.rcParams[f"{axis.axis_name}tick.labelsize"]
            )
        ).get_size_in_points()
        px = axis.figure.dpi / 72.0
        labels = axis.get_major_formatter().format_ticks(periods)
        extents = [
            _text_size(size, label)[0 if along_x else 1] * px for label in labels
        ]
        centres = (periods - min(vmin, vmax)) / span * length
        gap = PERIOD_LABEL_GAP * size * px

        def fits(i, j):
            return centres[j] - extents[j] / 2 >= centres[i] + extents[i] / 2 + gap

        kept = [0]
        for j in range(1, len(periods) - 1):
            if fits(kept[-1], j):
                kept.append(j)
        last = len(periods) - 1
        while len(kept) > 1 and not fits(kept[-1], last):
            kept.pop()
        kept.append(last)
        return periods[kept]


def _series_periods(xs: list) -> list:
    """The union of the series' periods: sorted, or first-seen when categorical."""

    periods = []
    seen = set()
    for x in xs:
        for period in x:
            if period not in seen:
                seen.add(period)
                periods.append(period)
    if axis_kind(periods) == AXIS_CATEGORICAL:
        return periods
    return sorted(periods)


def _align_to_periods(x, y, periods: list, index: int) -> np.ndarray:
    """A series' `y` at each period as floats; NaN where it has no value."""

    position = {period: i for i, period in enumerate(periods)}
    aligned = np.full(len(periods), np.nan)
    seen = set()
    for period, value in zip(x, y):
        if period in seen:
            raise ValueError(
                f"Bump chart series {index} has period {period!r} more than once; "
                "a series takes one value per period."
            )
        seen.add(period)
        if value is None:
            continue
        if not isinstance(value, Real) or isinstance(value, bool):
            raise ValueError(
                f"Bump chart series {index} has a non-numeric `y` {value!r} at "
                f"period {period!r}; `y` must be a number."
            )
        aligned[position[period]] = float(value)
    return aligned


def rank_series(xs: list, ys: list, rank_by: str) -> tuple:
    """The periods and each series' rank at them (ADR 0046).

    Values rank per period over the series present there, ties in input
    order; `GIVEN` takes `y` as the rank. A series without a value at a
    period holds NaN there: a gap in its line.
    """

    periods = _series_periods(xs)
    values = [
        _align_to_periods(x, y, periods, i) for i, (x, y) in enumerate(zip(xs, ys))
    ]
    if rank_by == BUMP_RANK.GIVEN:
        for column in values:
            validate_given_ranks(column)
        return periods, values
    ranks = [np.full(len(periods), np.nan) for _ in values]
    sign = -1 if rank_by == BUMP_RANK.VALUE_DESCENDING else 1
    for p in range(len(periods)):
        present = [i for i, column in enumerate(values) if not np.isnan(column[p])]
        for rank, i in enumerate(sorted(present, key=lambda i: sign * values[i][p])):
            ranks[i][p] = rank + 1
    return periods, ranks


def rank_bump_charts(charts: List[dict], settings: dict) -> List[dict]:
    """The charts with their data as periods, ranks and the original values.

    Ranking reads every series of the figure at once, so the layers draw
    ranks without knowing their siblings.
    """

    rank_by = validate_rank_by(settings.get("rank_by"))
    xs, ys = [], []
    for chart in charts:
        x, y = get_chart_data("x", chart), get_chart_data("y", chart)
        if x is None or y is None or len(x) != len(y):
            raise ValueError(
                "A bump chart requires the `x` and `y` columns, one `y` per `x`."
            )
        xs.append(list(x))
        ys.append(list(y))
    periods, ranks = rank_series(xs, ys, rank_by)
    return [
        {
            **{k: v for k, v in chart.items() if k not in ("x", "y", "yerr")},
            "data": {
                "x": periods,
                "y": rank,
                "value": _align_to_periods(x, y, periods, i),
            },
        }
        for i, (chart, x, y, rank) in enumerate(zip(charts, xs, ys, ranks))
    ]


def _bump_path(x: np.ndarray, y: np.ndarray, curve: float) -> tuple:
    """The drawn vertices through every point and the indices of the points.

    Between two present points the rank eases along a sigmoid blended with
    the straight segment by `curve`; the points themselves never move. A
    gap stays a NaN vertex, so the line breaks there.
    """

    if curve == 0:
        return x, y, None
    t = np.linspace(0, 1, BUMP_CURVE_SAMPLES + 1)[1:]
    ease = (1 - curve) * t + curve * t**3 * (t * (6 * t - 15) + 10)
    px, py, marks = [x[0]], [y[0]], [0]
    for i in range(1, len(x)):
        if not (np.isnan(y[i - 1]) or np.isnan(y[i])):
            px.extend(x[i - 1] + (x[i] - x[i - 1]) * t[:-1])
            py.extend(y[i - 1] + (y[i] - y[i - 1]) * ease[:-1])
        marks.append(len(px))
        px.append(x[i])
        py.append(y[i])
    return np.asarray(px), np.asarray(py), marks


class BumpLayer(LineLayer):
    """One series of a bump chart, drawn on its per-period ranks (ADR 0046)."""

    kind = "bump"
    # value labels sit beside the marks inside the half-rank margin
    labels_past_mark = False

    def _resolve_style(self):
        style = get_bump_style(self.style)
        self.label_padding = style.pop("label_padding", 0)
        if self.settings.get("show_markers") is False:
            style.pop("marker", None)
        self.line_style = style
        self.area_style = get_area_style(self.style)
        self.show_yerr = False
        self.show_area = False
        self.line_curve = validate_line_curve(self.settings.get("line_curve"))
        self.show_labels = self.settings.get("show_labels") is not False
        self.label_position = validate_label_position(
            self.settings.get("label_position")
        )
        self._resolve_value_labels()
        self._init_point_labels()

    def ranks(self) -> np.ndarray:
        return np.asarray(get_chart_data("y", self.chart), dtype=float)

    def y_range(self):
        ranks = self.ranks()
        if np.isnan(ranks).all():
            return None
        return (float(np.nanmin(ranks)), float(np.nanmax(ranks)))

    def value_data(self):
        return None

    def draw(self, ax, ctx):
        periods = self.x_values()
        ranks = self.ranks()
        values = np.asarray(get_chart_data("value", self.chart), dtype=float)

        line_style = self._merge_color("color", ctx.color, self.line_style)
        if ctx.z_order is not None:
            line_style["zorder"] = ctx.z_order
        self._apply_cycle_linestyle(line_style, ctx)
        self._apply_emphasis(line_style, ctx.emphasis)
        self._stroke_halo(line_style)

        # periods draw as axis numbers so a curve can interpolate between them
        axis = ax.yaxis if ctx.transpose else ax.xaxis
        axis.update_units(periods)
        x = np.asarray(axis.convert_units(periods), dtype=float)
        px, py, marks = _bump_path(x, ranks, self.line_curve)

        plot, _, _ = _oriented(ax, ctx.transpose)
        label = self.label(ctx)
        (line,) = plot(px, py, **line_style, markevery=marks, label=label)
        # the period axis ends on the first and last period: the panel lets
        # the end markers overhang the spines there
        self._lines.setdefault(id(ax), []).append(line)

        def resolve(index: int) -> dict:
            i = _nearest(x, px[index])
            datum = {"label": label, "x": _scalar(periods[i]), "y": _scalar(ranks[i])}
            if ctx.transpose:
                datum["x"], datum["y"] = datum["y"], datum["x"]
            datum["value"] = _scalar(values[i])
            return datum

        self.register_hover(line, resolve)

        present = ~np.isnan(ranks)
        if self.show_values and ctx.emphasis != EMPHASIS_BACKGROUND and present.any():
            self._record_points(
                ax,
                ctx,
                x[present],
                ranks[present],
                (2 * _mark_radius(line_style)) ** 2,
                self._value_texts(ax, values[present], ctx.transpose),
                self.value_font,
                self.value_padding,
            )

        if present.any():
            color = (
                self.muted_color
                if ctx.emphasis == EMPHASIS_BACKGROUND
                else line.get_color()
            )
            self._draw_end_labels(ax, ctx, x, ranks, present, line_style, color)

    def _labels_at(self, end: str) -> bool:
        """Whether an end label prints at the `BUMP_LABEL_POSITION.START` or `END`."""

        return bool(self.show_labels and self.subtitle) and self.label_position in (
            end,
            BUMP_LABEL_POSITION.BOTH,
        )

    def _draw_end_labels(self, ax, ctx, x, ranks, present, line_style, color):
        """Print the series name beside its first and/or last present point."""

        indices = np.flatnonzero(present)
        ends = []
        if self._labels_at(BUMP_LABEL_POSITION.START):
            ends.append((indices[0], -1))
        if self._labels_at(BUMP_LABEL_POSITION.END):
            ends.append((indices[-1], 1))
        gap = _mark_radius(line_style) + self.label_padding
        font = {k: v for k, v in self.label_font.items() if k != "color"}
        for i, side in ends:
            xy = (ranks[i], x[i]) if ctx.transpose else (x[i], ranks[i])
            offset = (0, -side * gap) if ctx.transpose else (side * gap, 0)
            label = ax.annotate(
                self.subtitle,
                xy=xy,
                xytext=offset,
                textcoords="offset points",
                ha=("center" if ctx.transpose else "left" if side > 0 else "right"),
                va=("top" if side > 0 else "bottom") if ctx.transpose else "center",
                color=color,
                annotation_clip=False,
                zorder=TEXT_ANNOTATION_ZORDER,
                **font,
            )
            self.register_limit_mark(label, *xy)


class StackedAreaLayer(Layer):
    """One series of a stack; the panel computes its band (ADR 0025)."""

    kind = "stackedarea"
    surface = True
    # the stack fills its frame: both axes end on the data, not on a tick
    ticks_at_axis_ends = False

    def _resolve_style(self):
        style = get_stackedarea_style(self.style)
        self.outline = bool(style.pop("outline", False))
        self.fill_style = style
        self.line_style = get_line_style(self.style)
        self._resolve_value_labels()

    def x_values(self):
        return get_chart_data("x", self.chart)

    def y_values(self):
        y = get_chart_data("y", self.chart)
        return None if y is None else np.asarray(y, dtype=float)

    def x_range(self):
        return _column_range(self.chart, "x")

    def y_range(self):
        return _column_range(self.chart, "y")

    def draw(self, ax, ctx):
        x = self.x_values()
        if x is None or ctx.stack_slot is None:
            return

        fill_style = self._merge_color("color", ctx.color, self.fill_style)
        if ctx.z_order is not None:
            fill_style["zorder"] = ctx.z_order
        _apply_cycle_hatch(fill_style, ctx)
        self._apply_emphasis(fill_style, ctx.emphasis)

        plot, fill, _ = _oriented(ax, ctx.transpose)
        band = fill(
            x,
            ctx.stack_slot.bottom,
            ctx.stack_slot.top,
            **fill_style,
            label=self.label(ctx),
        )
        self._etch([band], wash=False)
        # the band picks by containment and reports the point nearest the
        # picked vertex, under its own value, never the stack total
        y = get_chart_data("y", self.chart)
        point = _point_resolver(self.label(ctx), x, y, ctx.transpose)
        axis = ax.yaxis if ctx.transpose else ax.xaxis

        def resolve(index):
            vertices = band.get_paths()[index[0]].vertices
            coordinate = _vertex_coordinate(vertices, index, 1 if ctx.transpose else 0)
            return point(_nearest(axis.convert_units(x), coordinate))

        self.register_hover(band, resolve)

        if self.outline:
            line_style = self._merge_color("color", ctx.color, self.line_style)
            line_style["zorder"] = fill_style.get("zorder", 0) + 0.1
            self._apply_emphasis(line_style, ctx.emphasis)
            plot(x, ctx.stack_slot.top, **line_style)

        if self.show_values and ctx.emphasis != EMPHASIS_BACKGROUND:
            self._label_band(ax, ctx, x)

    def _label_band(self, ax, ctx, x) -> None:
        """Print each value at the midpoint of its band; a thin band stays bare."""

        heights = ctx.stack_slot.top - ctx.stack_slot.bottom
        mids = (ctx.stack_slot.top + ctx.stack_slot.bottom) / 2
        texts = self._value_texts(ax, heights, ctx.transpose)
        # a band thinner than its label cannot hold it; the axes autoscale
        # first so the display transform sees the final limits
        axis = 0 if ctx.transpose else 1
        ax.autoscale_view()
        per_unit = abs(
            ax.transData.transform([[1, 1]])[0][axis]
            - ax.transData.transform([[0, 0]])[0][axis]
        )
        text_px = TEXT_LINE_HEIGHT * self.value_font["fontsize"] * ax.figure.dpi / 72
        last = len(x) - 1
        for i, (xi, mid, height, text) in enumerate(zip(x, mids, heights, texts)):
            if text is None or height * per_unit < text_px:
                continue
            # the band ends at the axes edge: the end labels hang inward
            edge = "left" if i == 0 else "right" if i == last else "center"
            ax.annotate(
                text,
                xy=(mid, xi) if ctx.transpose else (xi, mid),
                ha="center" if ctx.transpose else edge,
                va=(
                    {"left": "bottom", "right": "top"}.get(edge, "center")
                    if ctx.transpose
                    else "center"
                ),
                zorder=TEXT_ANNOTATION_ZORDER,
                **self.value_font,
            )


def stack_first_line(y: np.ndarray, baseline: str) -> np.ndarray:
    """Where the stack starts at each x; matplotlib's `stackplot` baselines."""

    if baseline in (STACKED_AREA_BASELINE.ZERO, STACKED_AREA_BASELINE.PERCENT):
        return np.zeros(y.shape[1])
    if baseline == STACKED_AREA_BASELINE.SYM:
        return -0.5 * np.sum(y, 0)
    m = y.shape[0]
    if baseline == STACKED_AREA_BASELINE.WIGGLE:
        return (y * (m - 0.5 - np.arange(m)[:, None])).sum(0) / -m
    validate_baseline(baseline)
    total = np.sum(y, 0)
    inv_total = np.zeros_like(total)
    mask = total > 0
    inv_total[mask] = 1.0 / total[mask]
    increase = np.hstack((y[:, 0:1], np.diff(y)))
    below_size = total - np.cumsum(y, 0) + 0.5 * y
    move_up = below_size * inv_total
    move_up[:, 0] = 0.5
    center = np.cumsum(((move_up - 0.5) * increase).sum(0))
    return center - 0.5 * total


def _stack_slots(layers: List[StackedAreaLayer], baseline: str) -> dict:
    """Per-layer (bottom, top) bands of the stack; series order is stack order."""

    validate_shared_x([l.x_values() for l in layers])
    y = np.vstack([l.y_values() for l in layers])
    if baseline == STACKED_AREA_BASELINE.PERCENT:
        total = y.sum(0)
        y = np.divide(y * 100.0, total, out=np.zeros_like(y), where=total != 0)
    first_line = stack_first_line(y, baseline)
    tops = np.cumsum(y, 0) + first_line
    slots = {}
    bottom = first_line
    for layer, top in zip(layers, tops):
        slots[id(layer)] = StackSlot(bottom=bottom, top=top)
        bottom = top
    return slots


class BarLayer(Layer):
    kind = "bar"
    labels_past_mark = True

    def _resolve_style(self):
        orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.is_horizontal = orientation == ORIENTATION.HORIZONTAL
        self.is_pyramid = bool(self.settings.get("pyramid"))
        self.bar_style = get_bar_style(self.style, self.is_horizontal)
        self.show_yerr = self.settings.get("show_yerr")
        self.record_roles = _record_emphasis(self.chart)
        self._resolve_value_labels()
        self.log_offset = 1 if self.settings.get("scaley") == "log" else 0

    def labels(self) -> Optional[np.ndarray]:
        return get_chart_data("label", self.chart)

    def y_values(self) -> Optional[np.ndarray]:
        return get_chart_data("y", self.chart)

    def value_data(self):
        return self.y_values()

    def y_range(self):
        y = self.y_values()
        if y is None or len(y) == 0:
            return None
        return (float(np.min(y)), float(np.max(y)))

    @property
    def bar_width(self) -> float:
        """The layer's resolved `plot_bar_width`, as a fraction of the category width."""
        key = "height" if self.is_horizontal else "width"
        return self.bar_style.get(key, config["plot_bar_width"])

    def draw(self, ax, ctx):
        y = self.y_values()
        labels = self.labels()
        if y is None or labels is None:
            return

        yerr = get_chart_data("yerr", self.chart) if self.show_yerr else None
        x = np.arange(len(labels))

        bar_style = self._merge_color("color", ctx.color, self.bar_style)
        if ctx.z_order is not None:
            bar_style["zorder"] = ctx.z_order
        if ctx.alpha is not None:
            bar_style["alpha"] = ctx.alpha
        _apply_cycle_hatch(bar_style, ctx)
        self._apply_emphasis(bar_style, ctx.emphasis)

        slot = ctx.bar_slot
        x_offset = 0.0
        if slot is not None:
            bar_style["height" if self.is_horizontal else "width"] = slot.width
            x_offset = slot.offset
            if slot.bottom is not None:
                bar_style["left" if self.is_horizontal else "bottom"] = slot.bottom
            if not slot.show_yerr:
                yerr = None

        error_range = {("xerr" if self.is_horizontal else "yerr"): yerr}

        draw_func = ax.barh if self.is_horizontal else ax.bar
        bars = draw_func(
            x + x_offset,
            y + self.log_offset,
            label=self.label(ctx),
            **error_range,
            **bar_style,
        )
        self._etch(bars.patches)
        roles = self._record_roles(ctx.emphasis, len(bars))
        self._apply_patch_emphasis(bars.patches, roles)
        self._name_legend_patch(bars, roles)
        # each bar reports its category position (the axis names it) and its
        # own value, never the stack total; a pyramid side draws negative
        # values, so they read as passed, like the labels
        self.register_hover(
            bars,
            _point_resolver(
                self.label(ctx),
                x,
                np.abs(y) if self.is_pyramid else y,
                self.is_horizontal,
            ),
        )

        if self.show_values and ctx.emphasis != EMPHASIS_BACKGROUND:
            # pyramid sides draw as signed data but display positive
            # magnitudes (ADR 0017); a muted bar prints no value
            magnitude = abs if self.is_pyramid else (lambda v: v)
            self._label_bars(
                ax,
                bars,
                labels=[
                    (
                        ""
                        if role == EMPHASIS_BACKGROUND
                        else _format_value(self.value_format, magnitude(v))
                    )
                    for v, role in zip(y + self.log_offset, roles)
                ],
                stacked=slot is not None and slot.bottom is not None,
            )


# the gantt value labels print whole days and whole percents by default
GANTT_DURATION_FORMAT = "{x:.0f}d"
GANTT_PROGRESS_FORMAT = VALUE_FORMAT.PERCENT_INT
# the dependency arrow head, in points, and the elbow it bends through
GANTT_ARROW_SCALE = 8
GANTT_ARROW_CONNECTION = "angle,angleA=0,angleB=90,rad=0"
GANTT_ARROW_FROM_LEFT = "angle,angleA=90,angleB=0,rad=0"
# a milestone prints its date as the day and month unless a format is set
GANTT_MILESTONE_FORMAT = "%d %b"
GANTT_MILESTONE_Z_OFFSET = 0.2
# the today label sits this many points off the foot of its line
GANTT_TODAY_LABEL_OFFSET = 3
# the progress bar darkens the task color by this much toward black
GANTT_PROGRESS_DARKEN = 0.35
# the progress bar sits just above its task bar
GANTT_PROGRESS_Z_OFFSET = 0.1


def _darken(color, amount: float) -> str:
    """The color moved `amount` (0–1) of the way to black."""

    return to_hex(tuple(c * (1 - amount) for c in to_rgb(color)))


def gantt_tasks(chart: dict) -> list:
    """The chart's task records, in drawing order."""

    data = chart.get("data")
    if not isinstance(data, list):
        return []
    return [record for record in data if isinstance(record, dict)]


def gantt_durations(tasks: list) -> np.ndarray:
    """Each task's duration in days, from its temporal `start` and `end`."""

    if not tasks:
        return np.array([], dtype=float)
    starts = to_date_numbers([task["start"] for task in tasks])
    ends = to_date_numbers([task["end"] for task in tasks])
    return ends - starts


def _gantt_cluster(tasks: list, index: int):
    """The row cluster of a task: its group, or the task alone without one."""

    group = tasks[index].get("group")
    return ("task", index) if group is None else group


def sort_gantt_charts(charts: List[dict], settings: dict) -> List[dict]:
    """The charts with their task rows in `sort` order by `sort_by` (ADR 0049).

    By start, every row orders by its start; by group, rows cluster by group,
    groups ordered by their earliest start and tasks within a group by start.
    A task without a group forms its own cluster. Ties keep input order.
    """

    sort = validate_sort(settings.get("sort"))
    sort_by = validate_gantt_sort_by(sort, settings.get("sort_by"))
    if sort is None:
        return charts

    sign = -1 if sort == SORT.DESCENDING else 1
    sorted_charts = []
    for chart in charts:
        tasks = gantt_tasks(chart)
        if not tasks:
            sorted_charts.append(chart)
            continue
        starts = to_date_numbers([task["start"] for task in tasks])
        if sort_by == GANTT_SORT_KEY.GROUP:
            earliest = {}
            for index in range(len(tasks)):
                key = _gantt_cluster(tasks, index)
                earliest[key] = min(earliest.get(key, starts[index]), starts[index])
            order = sorted(
                range(len(tasks)),
                key=lambda i: (
                    sign * earliest[_gantt_cluster(tasks, i)],
                    sign * starts[i],
                ),
            )
            # a group's rows stay contiguous even when two groups start together
            clusters = {}
            for i in order:
                clusters.setdefault(_gantt_cluster(tasks, i), []).append(i)
            order = [i for cluster in clusters.values() for i in cluster]
        else:
            order = sorted(range(len(tasks)), key=lambda i: sign * starts[i])
        sorted_charts.append(
            {
                **chart,
                "data": [tasks[i] for i in order],
                # colors follow the input order, so a sort never recolors
                "group_order": gantt_groups(tasks),
            }
        )
    return sorted_charts


def gantt_groups(tasks: list) -> list:
    """The task groups in first-seen order; ungrouped tasks name none."""

    groups = []
    for task in tasks:
        if task.get("group") is not None and task["group"] not in groups:
            groups.append(task["group"])
    return groups


class GanttLayer(BarLayer):
    """One range bar per task over a temporal value axis (ADR 0049).

    Draws on the bar layer's geometry: `barh` with each bar's left edge at
    the task start and its width the duration, through the panel's slotting.
    """

    kind = "gantt"

    def _resolve_style(self):
        self.is_horizontal = True
        self.is_pyramid = False
        self.show_yerr = False
        self.log_offset = 0
        self.gantt_style = get_gantt_style(self.style)
        bar_keys = ("color", "alpha", "hatch", "linewidth", "edgecolor", "zorder")
        self.bar_style = {k: v for k, v in self.gantt_style.items() if k in bar_keys}
        self.arrow_entry = validate_gantt_arrow_entry(
            self.gantt_style.get("dependency_entry")
        )
        self.show_headers = bool(self.settings.get("show_group_headers"))
        tasks = gantt_tasks(self.chart)
        if self.show_headers:
            # a header stands over its whole group, so the group's rows cluster
            clusters = {}
            for index in range(len(tasks)):
                clusters.setdefault(_gantt_cluster(tasks, index), []).append(index)
            tasks = [tasks[i] for cluster in clusters.values() for i in cluster]
        self.tasks = tasks
        times = [t["start"] for t in tasks] + [t["end"] for t in tasks]
        self.x_tz = _column_tz(times)
        self.starts = (
            to_date_numbers([t["start"] for t in tasks])
            if tasks
            else np.array([], dtype=float)
        )
        self.durations = gantt_durations(tasks)
        self.milestones = self.durations == 0
        # the front validated the task records, their roles included
        self.record_roles = [t.get("emphasis") for t in tasks]
        self.value_mode = validate_gantt_show_values(self.settings.get("show_values"))
        self._resolve_value_labels()
        self.show_values = self.value_mode is not None
        if self.settings.get("value_format") is None:
            self.value_format = (
                GANTT_PROGRESS_FORMAT
                if self.value_mode == GANTT_VALUE.PROGRESS
                else GANTT_DURATION_FORMAT
            )
        self.milestone_format = self.settings.get("xticks_format")
        if _auto_format(self.milestone_format):
            self.milestone_format = GANTT_MILESTONE_FORMAT
        self.show_dependencies = bool(self.settings.get("show_dependencies"))
        # the bars of the last draw stand for their groups in the legend
        self._task_patches = []

        # the legend lists the groups in row order; one color and hatch per
        # group in input order, so sorting the rows never recolors a group
        self.groups = gantt_groups(tasks)
        groups = self.chart.get("group_order") or self.groups
        cycle = (
            create_color_cycle(config["color_general_multiple"], len(groups))
            if groups
            else None
        )
        hatches = config.get("plot_hatch_cycle") or []
        self.group_colors = {g: cycle[i]["color"] for i, g in enumerate(groups)}
        self.group_hatches = {
            g: hatches[i % len(hatches)] or None
            for i, g in enumerate(groups)
            if hatches
        }
        self._layout_rows()

        self.today = None
        self.today_label = None
        if self.settings.get("show_today"):
            today = self.settings.get("today") or date.today()
            self.today = float(to_date_numbers([today])[0])
            self.today_label = self.settings.get("today_label")
            line_style = get_vline_style(
                {
                    "plot_vline_color": self.gantt_style.get("today_color"),
                    "plot_vline_style": self.gantt_style.get("today_style"),
                    "plot_vline_width": self.gantt_style.get("today_width"),
                    "plot_vline_alpha": self.gantt_style.get("today_alpha"),
                }
            )
            self.vlines = [({"x": today}, line_style)] + self.vlines

    def _layout_rows(self) -> None:
        """Place the task rows, and under headers each group's header row.

        A header row sits over its group's tasks and a gap of
        `plot_gantt_group_gap` rows opens before every header but the first.
        """

        self.rows = np.arange(len(self.tasks), dtype=float)
        self.header_rows = []
        self.tick_rows = list(self.rows)
        self.tick_labels = [t["task"] for t in self.tasks]
        if not self.show_headers:
            return
        gap = self.gantt_style.get("group_gap", 0.0)
        position = 0.0
        ticks, labels, current = [], [], object()
        for index, task in enumerate(self.tasks):
            group = task.get("group")
            if group is not None and group != current:
                if index > 0:
                    position += gap
                self.header_rows.append((group, position))
                ticks.append(position)
                labels.append(str(group))
                position += 1
            current = group
            self.rows[index] = position
            ticks.append(position)
            labels.append(task["task"])
            position += 1
        self.tick_rows, self.tick_labels = ticks, labels

    def apply_row_ticks(self, ax) -> None:
        """Label the task rows; group header labels print bold."""

        ax.set_yticks(self.tick_rows, self.tick_labels)
        ax.yaxis.set_major_locator(mticker.FixedLocator(self.tick_rows))
        ax.set_yticklabels(self.tick_labels, rotation=self.chart.get("ytickrotate", 0))
        headers = {position for _, position in self.header_rows}
        for position, label in zip(self.tick_rows, ax.get_yticklabels()):
            if position in headers:
                label.set_fontweight(FONT_WEIGHT.BOLD)

    def labels(self) -> Optional[np.ndarray]:
        if not self.tasks:
            return None
        return np.array([t["task"] for t in self.tasks], dtype=object)

    def y_values(self) -> Optional[np.ndarray]:
        return self.durations if self.tasks else None

    def value_data(self):
        # time is never on a log scale; durations are derived
        return None

    def value_kind(self) -> Optional[str]:
        return AXIS_TEMPORAL if self.tasks else None

    def y_range(self):
        if not self.tasks:
            return None
        return (
            float(np.min(self.starts)),
            float(np.max(self.starts + self.durations)),
        )

    @property
    def bar_width(self) -> float:
        return self.gantt_style.get("height", config["plot_gantt_bar_height"])

    def task_color(self, task: dict, ctx_color: Optional[str]) -> Optional[str]:
        """The task's fill: an explicit bar color, its group's, or the layer's."""

        if "color" in self.bar_style:
            return self.bar_style["color"]
        return self.group_colors.get(task.get("group"), ctx_color)

    def legend_handles(self):
        """One key per task group; a group whose every task is muted stays out."""

        if not self.groups:
            return None
        handles = []
        for group in self.groups:
            members = [
                (role, patch, milestone)
                for task, role, patch, milestone in zip(
                    self.tasks, self.record_roles, self._task_patches, self.milestones
                )
                if task.get("group") == group
            ]
            if all(role == EMPHASIS_BACKGROUND for role, _, _ in members):
                continue
            # the group's first unmuted bar, so the key shows its hatch and etch
            patch = next(
                (
                    patch
                    for role, patch, milestone in members
                    if role != EMPHASIS_BACKGROUND and not milestone
                ),
                None,
            )
            handle = Patch(facecolor=self.task_color({"group": group}, None))
            if patch is not None:
                handle.update_from(patch)
            handle.set_label(str(group))
            handles.append(handle)
        return handles

    def draw(self, ax, ctx):
        if not self.tasks:
            return

        bar_style = dict(self.bar_style)
        bar_style.pop("color", None)
        if ctx.z_order is not None:
            bar_style["zorder"] = ctx.z_order
        if ctx.alpha is not None:
            bar_style["alpha"] = ctx.alpha
        if not self.groups:
            _apply_cycle_hatch(bar_style, ctx)
        colors = [self.task_color(task, ctx.color) for task in self.tasks]
        self._apply_emphasis(bar_style, ctx.emphasis)
        if "color" in bar_style:
            colors = [bar_style.pop("color")] * len(self.tasks)

        rows = self.rows
        slot = ctx.bar_slot
        height = self.bar_width
        if slot is not None:
            rows = rows + slot.offset
            height = slot.width if slot.width is not None else height

        bars = ax.barh(
            rows,
            self.durations,
            left=self.starts,
            height=height,
            color=colors,
            label=NO_LEGEND if self.groups else self.label(ctx),
            **bar_style,
        )
        for patch, task, milestone in zip(bars.patches, self.tasks, self.milestones):
            hatch = self.group_hatches.get(task.get("group"))
            if hatch and "hatch" not in bar_style:
                patch.set_hatch(hatch)
            # a milestone is a marker, not a bar; a bar's start pins the axis
            # to it, which would cut a marker at the schedule's end in half
            patch.set_visible(not milestone)
            if milestone:
                patch.sticky_edges.x.clear()
        roles = self._record_roles(ctx.emphasis, len(bars))
        self._task_patches = bars.patches
        self._draw_progress(ax, rows, height, colors, bar_style, roles)
        self._draw_summaries(ax, bar_style, ctx)
        self._draw_milestones(ax, rows, colors, bar_style, roles)
        self._etch(bars.patches)
        self._apply_patch_emphasis(bars.patches, roles)
        self._name_legend_patch(bars, roles)
        self.register_hover(bars, self._task_resolver(self.label(ctx)))

        # date ticks come from the locator, so the rotation applies to the axis
        rotation = self.chart.get("xtickrotate")
        if rotation:
            ax.xaxis.set_tick_params(labelrotation=rotation)

        if self.show_dependencies:
            self._draw_dependencies(ax, rows, height, ctx)
        if self.today_label:
            self._draw_today_label(ax)

        if self.show_values and ctx.emphasis != EMPHASIS_BACKGROUND:
            self._label_bars(
                ax,
                bars,
                labels=[
                    (
                        ""
                        if role == EMPHASIS_BACKGROUND or milestone
                        else self._value_text(i)
                    )
                    for i, (role, milestone) in enumerate(zip(roles, self.milestones))
                ],
                stacked=False,
            )

    def _draw_progress(self, ax, rows, height, colors, bar_style, roles):
        """The inner bars over each task's done fraction."""

        indices = [
            i
            for i, t in enumerate(self.tasks)
            if t.get("progress") is not None and not self.milestones[i]
        ]
        if not indices:
            return
        style = self.gantt_style
        fraction = np.array([self.tasks[i]["progress"] for i in indices], dtype=float)
        progress_color = style.get("progress_color")
        bars = ax.barh(
            rows[indices],
            self.durations[indices] * fraction,
            left=self.starts[indices],
            height=height
            * style.get("progress_height", config["plot_gantt_progress_height"]),
            color=[
                progress_color or _darken(colors[i], GANTT_PROGRESS_DARKEN)
                for i in indices
            ],
            alpha=style.get("progress_alpha"),
            linewidth=0,
            zorder=bar_style.get("zorder", 0) + GANTT_PROGRESS_Z_OFFSET,
            label=NO_LEGEND,
        )
        # the bar's edge is stroked half inside its outline: the progress
        # starts and ends half a stroke in, flush with the visible border
        for patch, i in zip(bars.patches, indices):
            task = self._task_patches[i]
            inset = task.get_linewidth() / 2 / 72
            shift = lambda dx: ScaledTranslation(dx, 0, ax.figure.dpi_scale_trans)
            patch.set_transform(ax.transData + shift(inset))
            patch.set_clip_path(task.get_path(), task.get_transform() + shift(-inset))
        self._etch(bars.patches)
        self._apply_patch_emphasis(bars.patches, [roles[i] for i in indices])

    def _draw_summaries(self, ax, bar_style, ctx) -> None:
        """A bar over each group header, from the group's first start to its last end."""

        style = self.gantt_style
        for group, position in self.header_rows:
            members = [i for i, t in enumerate(self.tasks) if t.get("group") == group]
            start = float(np.min(self.starts[members]))
            end = float(np.max(self.starts[members] + self.durations[members]))
            muted = ctx.emphasis == EMPHASIS_BACKGROUND or all(
                self.record_roles[i] == EMPHASIS_BACKGROUND for i in members
            )
            color = style.get("summary_color") or self.task_color(
                {"group": group}, None
            )
            ax.barh(
                position,
                end - start,
                left=start,
                height=style.get("summary_height"),
                color=self.muted_color if muted else color,
                alpha=self.muted_alpha if muted else None,
                linewidth=0,
                zorder=bar_style.get("zorder", 0),
                label=NO_LEGEND,
            )

    def _draw_milestones(self, ax, rows, colors, bar_style, roles) -> None:
        """A marker at each milestone; under value labels, its date beside it."""

        style = self.gantt_style
        size = style.get("milestone_size")
        for i in np.flatnonzero(self.milestones):
            muted = roles[i] == EMPHASIS_BACKGROUND
            anchor = (self.starts[i], rows[i])
            (marker,) = ax.plot(
                [self.starts[i]],
                [rows[i]],
                linestyle="none",
                marker=style.get("milestone_marker"),
                markersize=size,
                color=self.muted_color if muted else colors[i],
                markeredgecolor=bar_style.get("edgecolor"),
                markeredgewidth=bar_style.get("linewidth"),
                alpha=self.muted_alpha if muted else None,
                zorder=bar_style.get("zorder", 0) + GANTT_MILESTONE_Z_OFFSET,
                label=NO_LEGEND,
                # a milestone on the view's edge shows whole, over the spine
                clip_on=False,
            )
            self.register_limit_mark(marker, *anchor)
            if self.show_values and not muted:
                label = ax.annotate(
                    date_labels([self.tasks[i]["start"]], self.milestone_format)[0],
                    anchor,
                    xytext=(size / 2 + self.value_padding, 0),
                    textcoords="offset points",
                    ha="left",
                    va="center",
                    zorder=TEXT_ANNOTATION_ZORDER,
                    **self.value_font,
                )
                self.register_limit_mark(label, *anchor)

    def _draw_dependencies(self, ax, rows, height, ctx) -> None:
        """An elbow arrow from each dependency's end to the dependent's start.

        Entering from the top, the arrow runs along the dependency's row and
        turns onto the dependent bar; from the left, it drops from the
        dependency's end and turns into the dependent bar's start.
        """

        style = self.gantt_style
        color = style.get("dependency_color")
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            color = self.muted_color
        # a milestone's marker, not its row centre, is where an arrow stops
        clearance = style.get("milestone_size", 0) / 2
        position = {task["task"]: i for i, task in enumerate(self.tasks)}
        for j, task in enumerate(self.tasks):
            for name in task.get("depends_on") or []:
                i = position[name]
                # with no room before the dependent's start, it enters from the top
                from_left = (
                    self.arrow_entry == GANTT_ARROW_ENTRY.LEFT
                    and self.starts[j] > self.starts[i] + self.durations[i]
                )
                # the facing edge of a bar, toward the other task's row
                toward = height / 2 if rows[j] > rows[i] else -height / 2
                start_edge = 0.0 if self.milestones[i] or not from_left else toward
                end_edge = 0.0 if self.milestones[j] or from_left else -toward
                ax.add_patch(
                    FancyArrowPatch(
                        (self.starts[i] + self.durations[i], rows[i] + start_edge),
                        (self.starts[j], rows[j] + end_edge),
                        arrowstyle=style.get("dependency_style"),
                        connectionstyle=(
                            GANTT_ARROW_FROM_LEFT
                            if from_left
                            else GANTT_ARROW_CONNECTION
                        ),
                        mutation_scale=GANTT_ARROW_SCALE,
                        color=color,
                        linewidth=style.get("dependency_width"),
                        shrinkA=clearance if self.milestones[i] else 0,
                        shrinkB=clearance if self.milestones[j] else 0,
                        zorder=style.get("dependency_zorder"),
                    )
                )

    def _draw_today_label(self, ax) -> None:
        """The today line's label, at the foot of the line."""

        ax.annotate(
            self.today_label,
            (self.today, 0),
            xycoords=ax.get_xaxis_transform(),
            xytext=(GANTT_TODAY_LABEL_OFFSET, GANTT_TODAY_LABEL_OFFSET),
            textcoords="offset points",
            ha="left",
            va="bottom",
            zorder=TEXT_ANNOTATION_ZORDER,
            **{**self.value_font, "color": self.gantt_style.get("today_color")},
        )

    def _value_text(self, index: int) -> str:
        """The bar's value label: its duration in days or its progress."""

        if self.value_mode == GANTT_VALUE.PROGRESS:
            progress = self.tasks[index].get("progress")
            return (
                "" if progress is None else _format_value(self.value_format, progress)
            )
        return _format_value(self.value_format, float(self.durations[index]))

    def _task_resolver(self, label) -> Callable[[int], dict]:
        """The hover datum of a task bar: its name, span, duration and progress."""

        def resolve(index: int) -> dict:
            task = self.tasks[index]
            datum = {
                "label": label,
                "task": task["task"],
                "start": task["start"],
                "end": task["end"],
                "duration": f"{self.durations[index]:g} days",
            }
            if task.get("progress") is not None:
                datum["progress"] = f"{task['progress']:.0%}"
            return datum

        return resolve


class HistogramLayer(Layer):
    kind = "histogram"
    labels_past_mark = True

    def _resolve_style(self):
        self.hist_style = get_hist_style(self.style)
        self.orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.is_horizontal = self.orientation == ORIENTATION.HORIZONTAL
        self.show_density = self.settings.get("show_density")
        self.show_cumulative = self.settings.get("show_cumulative")
        self.num_bins = self.settings.get("num_bins") or DEFAULT_NUM_BINS
        # step's outline is the series mark: it follows the cycle color and
        # the theme line width unless the chart style pins them (ADR 0014)
        self.step_edge_color_auto = "plot_hist_edge_color" not in self.style
        self.step_edge_width_auto = "plot_hist_edge_width" not in self.style
        self.step_edge_width = config["plot_line_width"]
        self._resolve_value_labels()

    def x_values(self) -> Optional[np.ndarray]:
        return get_chart_data("x", self.chart)

    def y_range(self):
        x = self.x_values()
        if x is None or len(x) == 0:
            return None
        # the view decides the scale: densities and cumulative shares are not counts
        heights, edges = np.histogram(x, bins=self.num_bins, density=self.show_density)
        if self.show_cumulative:
            heights = np.cumsum(
                heights * np.diff(edges) if self.show_density else heights
            )
        return (float(np.min(heights)), float(np.max(heights)))

    def draw(self, ax, ctx):
        x = self.x_values()
        if x is None:
            return

        hist_style = self._merge_color("color", ctx.color, self.hist_style)
        if hist_style.get("histtype") == HISTOGRAM_TYPE.STEP:
            if ctx.hist_slot is not None:
                # a stack needs area: step stacks as its filled equivalent (ADR 0014)
                hist_style["histtype"] = HISTOGRAM_TYPE.STEP_FILLED
            else:
                if self.step_edge_color_auto:
                    # dropping the theme edge lets `color` drive the outline
                    hist_style.pop("edgecolor", None)
                if self.step_edge_width_auto:
                    hist_style["linewidth"] = self.step_edge_width
        if ctx.z_order is not None:
            hist_style["zorder"] = ctx.z_order
        if ctx.alpha is not None:
            hist_style["alpha"] = ctx.alpha
        _apply_cycle_hatch(hist_style, ctx)
        self._apply_emphasis(hist_style, ctx.emphasis)

        if ctx.hist_slot is not None:
            # weighted bin centers reproduce the precomputed stack heights
            # exactly; density/cumulative are already encoded in them
            slot = ctx.hist_slot
            counts, edges, bars = ax.hist(
                (slot.bins[:-1] + slot.bins[1:]) / 2,
                bins=slot.bins,
                weights=slot.heights,
                bottom=slot.bottom,
                label=self.label(ctx),
                orientation=self.orientation,
                **hist_style,
            )
        else:
            bins = ctx.bins if ctx.bins is not None else self.num_bins
            counts, edges, bars = ax.hist(
                x,
                bins=bins,
                label=self.label(ctx),
                density=self.show_density,
                cumulative=self.show_cumulative,
                orientation=self.orientation,
                **hist_style,
            )
        self._etch(bars.patches if isinstance(bars, BarContainer) else bars)
        self._register_bins(ax, ctx, bars, edges, counts)
        if self.show_values and ctx.emphasis != EMPHASIS_BACKGROUND:
            self._label_bins(ax, bars, edges, counts, ctx.hist_slot is not None)

    def _label_bins(self, ax, bars, edges, counts, stacked: bool) -> None:
        """Print each bin's height at its top; an empty bin stays bare."""

        texts = [_format_value(self.value_format, c) if c else "" for c in counts]
        if isinstance(bars, BarContainer):
            self._label_bars(ax, bars, stacked, labels=texts)
            return
        # a step outline has no bars to label: the bin tops are annotated directly
        centres = (edges[:-1] + edges[1:]) / 2
        for centre, height, text in zip(centres, counts, texts):
            if text:
                _annotate_value(
                    ax,
                    centre,
                    height,
                    text,
                    self.is_horizontal,
                    self.value_padding,
                    self.value_font,
                )

    def _register_bins(self, ax, ctx, bars, edges, counts) -> None:
        """Each bin reports its range on the value axis and its own height."""

        label = self.label(ctx)
        value_axis = "y" if self.is_horizontal else "x"

        def datum(i: int) -> dict:
            span = _span_text(edges[i], edges[i + 1], _axis_formatter(ax, value_axis))
            count = _scalar(counts[i])
            # matplotlib bins into floats; a plain count reads as a whole number
            if not self.show_density and float(count).is_integer():
                count = int(count)
            if self.is_horizontal:
                return {"label": label, "x": count, "y": span}
            return {"label": label, "x": span, "y": count}

        if isinstance(bars, BarContainer):
            self.register_hover(bars, datum)
            return
        # a step outline is one polygon; a picked vertex names its bin
        (outline,) = bars
        axis = 1 if self.is_horizontal else 0

        def resolve(index):
            coordinate = _vertex_coordinate(outline.get_xy(), index, axis)
            i = int(np.searchsorted(edges, coordinate, side="right")) - 1
            return datum(min(max(i, 0), len(counts) - 1))

        self.register_hover(outline, resolve)


class KdeLayer(Layer):
    """A density curve of one chart's `x` values, with a soft fill beneath.

    The scatter matrix draws one per hue group on its diagonal (ADR 0051);
    `kde_xlim` pins the evaluation grid to the column's shared limits.
    """

    kind = "kde"

    def _resolve_style(self):
        self.kde_style = get_kde_style(self.style)
        self.xlim = self.settings.get("kde_xlim")

    def x_values(self) -> Optional[np.ndarray]:
        return get_chart_data("x", self.chart)

    def curve(self) -> Optional[tuple]:
        """The (x, density) samples; None when the values have no spread."""

        # the estimate is fixed once built; the range and the draw share it
        if not hasattr(self, "_curve"):
            x = self.x_values()
            self._curve = None
            if x is not None and len(x) > 1 and np.ptp(x) > 0:
                points = kde1d(x, xlim=self.xlim)
                self._curve = (
                    np.array([p["x"] for p in points]),
                    np.array([p["y"] for p in points]),
                )
        return self._curve

    def y_range(self):
        curve = self.curve()
        return None if curve is None else (0.0, float(np.max(curve[1])))

    def draw(self, ax, ctx):
        curve = self.curve()
        if curve is None:
            return
        x, y = curve
        color = self.muted_color if ctx.emphasis == EMPHASIS_BACKGROUND else ctx.color
        line_style = {"color": color, "linewidth": self.kde_style["linewidth"]}
        if ctx.z_order is not None:
            line_style["zorder"] = ctx.z_order
        self._stroke_halo(line_style)
        (line,) = ax.plot(x, y, label=self.label(ctx), **line_style)
        if self.kde_style["alpha"]:
            ax.fill_between(
                x,
                0,
                y,
                color=color,
                alpha=self.kde_style["alpha"],
                linewidth=0,
                zorder=line.get_zorder() - 0.1,
            )
        # a density starts at zero: the autoscale margin stops there
        line.sticky_edges.y.append(0)
        self.register_hover(line, _point_resolver(self.label(ctx), x, y, ctx.transpose))


class UnclippedMarksMixin:
    """A layer whose scatter marks may draw whole over an axis end on the data."""

    def register_marks(self, ax, collection) -> None:
        """Remember a mark collection drawn into `ax`, so the panel can unclip it."""

        self.__dict__.setdefault("_marks", {}).setdefault(id(ax), []).append(collection)

    def unclip_marks(self, ax, dims=("x", "y")) -> None:
        """Let the markers on the `dims` edges draw whole, past the frame."""

        for collection in getattr(self, "_marks", {}).get(id(ax), ()):
            sizes = np.asarray(collection.get_sizes(), dtype=float)
            radius = float(np.sqrt(sizes.max()) / 2) if sizes.size else 0.0
            widths = np.asarray(collection.get_linewidths(), dtype=float)
            pad = radius + (float(widths.max()) if widths.size else 0.0)
            collection.set_clip_path(None)
            collection.set_clip_box(MarkClipBox(ax, pad, dims))


class ScatterLayer(UnclippedMarksMixin, PointLabelMixin, Layer):
    kind = "scatter"
    record_roles_beat_layer = True

    def _resolve_style(self):
        self.scatter_style = get_scatter_style(self.style)
        self.record_roles = _validated_record_roles(
            _keyed_records(self.chart, "x"), self.kind
        )
        self._resolve_value_labels()
        self._init_point_labels()
        # an explicit `show_values` outranks point labels found under the
        # default key; the theme default yields to them
        self.show_values_explicit = self.settings.get("show_values") is not None
        self.size_range = self.settings.get("size_range") or DEFAULT_SIZE_RANGE
        self.show_regression = self.settings.get("show_regression")
        self.show_ci = self.settings.get("show_ci")
        self.ci_level = self.settings.get("ci_level") or DEFAULT_CI_LEVEL
        self.show_correlation = self.settings.get("show_correlation")
        self.default_size = config["plot_scatter_size"]
        # a highlight edge contrasts in the theme's own text color
        self.highlight_edge_color = config.get("font_general_color") or "#000000"
        # a front may restyle the line; a color it pins beats the group's
        regression_style = self.settings.get("regression_style") or {}
        self.regression_style = get_regression_style(regression_style)
        self.regression_color_pinned = (
            regression_style.get("plot_regression_color") is not None
        )
        self.regression_ci_alpha = config["plot_regression_ci_alpha"]
        # the correlation box wears the plot_text_* family (ADR 0018)
        self.correlation_font = get_plot_text_style({})
        self.correlation_bbox = get_plot_text_box_style({})

        hue_data = get_chart_data("hue", self.chart)
        self.hue_colors = None
        if hue_data is not None:
            unique_hues = np.unique(hue_data)
            cycle = create_color_cycle(
                config["color_general_multiple"], len(unique_hues)
            )
            self.hue_colors = [cycle[i]["color"] for i in range(len(unique_hues))]

    def y_range(self):
        y = get_chart_data("y", self.chart)
        if y is None or len(y) == 0:
            return None
        return (float(np.min(y)), float(np.max(y)))

    def x_values(self):
        return get_chart_data("x", self.chart)

    def value_data(self):
        return get_chart_data("y", self.chart)

    def _sizes(self, size_data, extent: Optional[tuple] = None):
        if size_data is not None:
            return _normalize_sizes(size_data, self.size_range, extent)
        return self.scatter_style.get("s", self.default_size)

    def _mark_legend_size(self, collection, size_data):
        if size_data is not None:
            collection.datachart_legend_size = self.scatter_style.get(
                "s", self.default_size
            )

    def _point_labels(self, x_data) -> Optional[np.ndarray]:
        """One label per drawn point (None where the key is absent), or None."""

        label_attr = get_attr_value("label", self.chart, "label")
        labels = [d.get(label_attr) for d in _keyed_records(self.chart, "x")]
        if len(labels) != len(x_data) or all(l is None for l in labels):
            return None
        return np.array([None if l is None else str(l) for l in labels], dtype=object)

    def _mark_labels(self, ax, ctx, x_data, y_data, roles) -> tuple:
        """The (labels, font, pad) each point carries: its value, or its point label.

        A muted point prints no value; a fully muted series keeps its point labels.
        """

        labels = self._point_labels(x_data)
        muted = roles == EMPHASIS_BACKGROUND
        if (
            self.show_values
            and (labels is None or self.show_values_explicit)
            and not muted.all()
        ):
            values = self._value_texts(ax, y_data, ctx.transpose)
            return (
                np.where(muted, None, values),
                self.value_font,
                self.value_padding,
            )
        return labels, self.label_font, POINT_LABEL_PAD

    def _draw_regression(self, ax, ctx, x, y, color):
        from scipy import stats as scipy_stats

        if len(x) == 0 or len(np.unique(x)) <= 1:
            return

        plot, fill, _ = _oriented(ax, ctx.transpose)

        # a log axis fits and samples its data as log10 values
        x_log = ctx.category_scale == SCALE.LOG
        y_log = ctx.value_scale == SCALE.LOG
        x = np.log10(x) if x_log else x
        y = np.log10(y) if y_log else y
        slope, intercept, _, _, _ = scipy_stats.linregress(x, y)
        x_fit = np.linspace(x.min(), x.max(), 100)
        y_fit = slope * x_fit + intercept
        x_line = np.power(10.0, x_fit) if x_log else x_fit
        y_line = np.power(10.0, y_fit) if y_log else y_fit

        reg_style = dict(self.regression_style)
        if color is not None and not self.regression_color_pinned:
            reg_style["color"] = color
        self._stroke_halo(reg_style)
        plot(x_line, y_line, **reg_style)
        # the line's samples keep point labels off it, as markers of its width
        width = reg_style.get("linewidth") or 1.0
        self._record_points(ax, ctx, x_line, y_line, (2 * width) ** 2, None)

        if self.show_ci:
            n = len(x)
            t_val = scipy_stats.t.ppf((1 + self.ci_level) / 2, n - 2)
            y_pred = slope * x + intercept
            residuals = y - y_pred
            s_err = np.sqrt(np.sum(residuals**2) / (n - 2))
            x_mean = np.mean(x)
            ss_x = np.sum((x - x_mean) ** 2)
            se_line = s_err * np.sqrt(1 / n + (x_fit - x_mean) ** 2 / ss_x)
            ci = t_val * se_line
            lower, upper = y_fit - ci, y_fit + ci
            if y_log:
                lower, upper = np.power(10.0, lower), np.power(10.0, upper)
            fill(
                x_line,
                lower,
                upper,
                alpha=self.regression_ci_alpha,
                color=color,
            )

    def _draw_correlation(self, ax, x, y, color):
        from ..stats import correlation

        r = correlation(x, y)
        font = dict(self.correlation_font)
        if color is not None:
            font["color"] = color
        # the corner placement pins the alignment; only the look is styleable
        font["ha"], font["va"] = "left", "top"
        if self.correlation_bbox is not None:
            font["bbox"] = dict(self.correlation_bbox)
        ax.annotate(
            f"r = {r:.3f}",
            xy=CORRELATION_BOX_CORNER,
            xycoords="axes fraction",
            **font,
        )

    def draw(self, ax, ctx):
        x_data = get_chart_data("x", self.chart)
        y_data = get_chart_data("y", self.chart)
        size_data = get_chart_data("size", self.chart)
        hue_data = get_chart_data("hue", self.chart)

        if x_data is None or y_data is None:
            return
        roles = np.array(
            self._marker_roles([ctx.emphasis] * len(x_data), ctx), dtype=object
        )
        labels, font, pad = self._mark_labels(ax, ctx, x_data, y_data, roles)

        scatter_style = dict(self.scatter_style)
        if ctx.z_order is not None:
            scatter_style["zorder"] = ctx.z_order
        self._apply_cycle_marker(scatter_style, ctx)
        scatter_style.pop("s", None)

        _, _, scatter = _oriented(ax, ctx.transpose)

        # one unit per hue group, or the whole series; each keeps one legend entry
        if hue_data is not None:
            units = [
                (hue_data == hue_val, self.hue_colors[i], str(hue_val))
                for i, hue_val in enumerate(np.unique(hue_data))
            ]
        else:
            series_color = scatter_style.get("c")
            if series_color is None:
                series_color = ctx.color
            units = [(np.ones(len(x_data), dtype=bool), series_color, self.label(ctx))]
        for mask, color, label in units:
            sizes = self._sizes(
                size_data[mask] if size_data is not None else None, ctx.size_extent
            )
            self._draw_unit(
                ax,
                ctx,
                scatter,
                scatter_style,
                x_data[mask],
                y_data[mask],
                sizes,
                roles[mask],
                color=color,
                label=label,
                size_data=size_data,
                labels=labels[mask] if labels is not None else None,
                font=font,
                pad=pad,
            )

        x_fit = _axis_numbers(ax, ctx.transpose, x_data)
        if hue_data is not None:
            if self.show_correlation:
                self._draw_correlation(ax, x_fit, y_data, color=None)
            if self.show_regression:
                self._draw_regression(ax, ctx, x_fit, y_data, color=None)
            return
        color = (
            self.muted_color if ctx.emphasis == EMPHASIS_BACKGROUND else series_color
        )
        if self.show_regression:
            self._draw_regression(ax, ctx, x_fit, y_data, color=color)
        if self.show_correlation:
            self._draw_correlation(ax, x_data, y_data, color=color)

    def _draw_unit(
        self,
        ax,
        ctx,
        scatter,
        base_style,
        x,
        y,
        sizes,
        roles,
        *,
        color,
        label,
        size_data,
        labels,
        font,
        pad,
    ) -> None:
        """Draw one hue group or series: one collection per emphasis role.

        The first unmuted collection carries the legend entry.
        """

        legend_label = label
        for role in MARKER_ROLE_ORDER:
            picked = roles == role
            if not picked.any():
                continue
            style = dict(base_style)
            style["c"] = self.muted_color if role == EMPHASIS_BACKGROUND else color
            self._apply_emphasis(style, role, width_key="linewidths", color_key=None)
            if role == EMPHASIS_HIGHLIGHT:
                style["edgecolors"] = self.highlight_edge_color
            role_sizes = sizes[picked] if np.ndim(sizes) else sizes
            collection = _draw_scatter_marks(
                scatter,
                x[picked],
                y[picked],
                role_sizes,
                style,
                NO_LEGEND if role == EMPHASIS_BACKGROUND else legend_label,
                role == EMPHASIS_HIGHLIGHT,
            )
            if role != EMPHASIS_BACKGROUND:
                legend_label = NO_LEGEND
            self.register_marks(ax, collection)
            self._mark_legend_size(collection, size_data)
            self.register_hover(
                collection,
                _point_resolver(label, x[picked], y[picked], ctx.transpose),
            )
            self._record_points(
                ax,
                replace(ctx, emphasis=role),
                x[picked],
                y[picked],
                role_sizes,
                labels[picked] if labels is not None else None,
                font,
                pad,
            )


def grouped_records(chart: dict) -> dict:
    """A group chart's drawn records keyed by label, in first-seen label order."""

    label_attr = get_attr_value("label", chart, "label")
    value_attr = get_attr_value("value", chart, "value")
    grouped = {}
    data = chart.get("data", [])
    if isinstance(data, list):
        for d in data:
            if d.get(label_attr) is not None and d.get(value_attr) is not None:
                grouped.setdefault(d[label_attr], []).append(d)
    return grouped


def grouped_values(chart: dict) -> dict:
    """A group chart's values keyed by label, in first-seen label order."""

    value_attr = get_attr_value("value", chart, "value")
    return {
        label: [d[value_attr] for d in records]
        for label, records in grouped_records(chart).items()
    }


class GroupLayer(Layer):
    """A layer of labeled groups placed on the panel's category index."""

    # box, violin and ridgeline fronts order their groups by median (ADR 0042)
    sorts_by_median = False
    sort = None
    # the first unmuted body and the subtitle, kept for the legend key
    legend_body = None
    legend_label = None

    def _resolve_emphasis(self, value):
        # group layers never dodge; emphasis aligns with the group labels
        if isinstance(value, list):
            for item in value:
                validate_emphasis(item)
            return value
        return validate_emphasis(value)

    def _resolve_style(self):
        if self.sorts_by_median:
            self.sort = validate_sort(self.settings.get("sort"))
        self.orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.is_horizontal = self.orientation == ORIENTATION.HORIZONTAL
        # a raincloud colors its groups from the multiple palette (ADR 0021);
        # the cycle is built once so sibling layers of one chart agree
        self.color_by_group = bool(self.settings.get("color_by_group"))
        self.group_colors = (
            create_color_cycle(
                config["color_general_multiple"], max(len(self.labels()), 1)
            )
            if self.color_by_group
            else None
        )
        if self.color_by_group:
            # a raincloud keeps the colors and legend of a muted group whose
            # rain holds an unmuted point, as its swarm draws it
            self._take_record_roles()

    def _take_record_roles(self) -> None:
        """Let the records' own roles outrank the group roles, in drawing order."""

        self.record_roles_beat_layer = True
        self.record_roles = _validated_record_roles(
            [d for group in grouped_records(self.chart).values() for d in group],
            self.kind,
        )

    def group_color(self, index: int, ctx_color: Optional[str]) -> Optional[str]:
        """The color of the group at `index`: its own palette slot, or the layer's."""

        if self.group_colors is None:
            return ctx_color
        return self.group_colors[index]["color"]

    def group_legend_handles(self, roles: list) -> Optional[list]:
        """One patch per group when coloring by group; background groups stay out."""

        if self.group_colors is None:
            return None
        records = grouped_records(self.chart)
        return [
            Patch(facecolor=self.group_colors[i]["color"], label=str(label))
            for i, (label, role) in enumerate(zip(self.labels(), roles))
            if role != EMPHASIS_BACKGROUND
            or any(
                r.get("emphasis") not in (None, EMPHASIS_BACKGROUND)
                for r in records[label]
            )
        ]

    def keep_legend_body(self, bodies: list, roles: list, ctx: DrawContext) -> None:
        """Remember the first unmuted body to key the subtitle in the legend."""

        # a group-colored layer keys its groups instead
        self.legend_label = None if self.color_by_group else self.label(ctx)
        self.legend_body = next(
            (b for b, role in zip(bodies, roles) if role != EMPHASIS_BACKGROUND),
            None,
        )

    def body_legend_handles(self) -> Optional[list]:
        """One key named by the subtitle, drawn like the body it stands for."""

        body = self.legend_body
        if self.legend_label is None or body is None:
            return None
        if isinstance(body, Patch):
            handle = Patch()
            handle.update_from(body)
        else:
            handle = Patch(
                facecolor=body.get_facecolor()[0],
                edgecolor=body.get_edgecolor()[0],
                linewidth=body.get_linewidth()[0],
                hatch=body.get_hatch(),
            )
            handle.set_path_effects(body.get_path_effects())
        handle.set_label(str(self.legend_label))
        return [handle]

    def grouped_values(self) -> dict:
        """The layer's values keyed by label: input order, or by median."""

        grouped = grouped_values(self.chart)
        if self.sort is None:
            return grouped
        sign = -1 if self.sort == SORT.DESCENDING else 1
        # a stable sort: ties keep input order
        order = sorted(grouped, key=lambda label: sign * np.median(grouped[label]))
        return {label: grouped[label] for label in order}

    def label_roles(self, panel_role: Optional[str] = None) -> dict:
        """Label -> emphasis role; a role list aligns with the input order."""

        labels = list(grouped_values(self.chart))
        return dict(zip(labels, self._group_roles(labels, panel_role)))

    def labels(self) -> list:
        return list(self.grouped_values().keys())

    def value_data(self):
        return [v for vals in self.grouped_values().values() for v in vals]

    def y_range(self):
        values = self.value_data()
        if not values:
            return None
        return (float(np.min(values)), float(np.max(values)))

    def summary_datum(self, label, position, values) -> dict:
        """A group's hover datum: its category position on the drawn axis, then the five-number summary."""

        values = np.asarray(values, dtype=float)
        q1, median, q3 = np.percentile(values, [25, 50, 75])
        return {
            "label": label,
            "y" if self.is_horizontal else "x": position,
            "median": float(median),
            "q1": float(q1),
            "q3": float(q3),
            "min": float(values.min()),
            "max": float(values.max()),
        }

    def _label_median(self, ax, position: float, values) -> None:
        """Print a group's median beside its median line."""

        median = float(np.percentile(np.asarray(values, dtype=float), 50))
        _annotate_value(
            ax,
            position,
            median,
            _format_value(self.value_format, median),
            self.is_horizontal,
            self.value_padding,
            self.value_font,
        )

    def _group_roles(self, labels: list, panel_role: Optional[str] = None) -> list:
        """One emphasis role per label; the panel's role, or a single value, applies to all."""

        roles = panel_role if panel_role is not None else self.emphasis
        if roles is None:
            return [None] * len(labels)
        if isinstance(roles, str):
            return [roles] * len(labels)
        if len(roles) != len(labels):
            raise ValueError(
                f"`emphasis` length ({len(roles)}) must match the number of "
                f"{self.kind} labels ({len(labels)})."
            )
        return list(roles)


class BoxLayer(GroupLayer):
    kind = "box"
    sorts_by_median = True

    def _resolve_style(self):
        super()._resolve_style()
        self.show_outliers = self.settings.get("show_outliers")
        self.show_notch = self.settings.get("show_notch")
        self.offset = self.settings.get("offset") or 0.0
        self.width = self.settings.get("width")
        self.zorder = self.settings.get("zorder")
        # a raincloud keeps one half of the box: -1 the low side, +1 the high
        self.side = self.settings.get("side") or 0
        self.box_style = get_box_style(self.style)
        self.outlier_style = get_box_outlier_style(self.style)
        self.median_style = get_box_median_style(self.style)
        self.whisker_style = get_box_whisker_style(self.style)
        self.cap_style = get_box_cap_style(self.style)
        self._resolve_value_labels()
        if self.settings.get("outline"):
            self._apply_outline()

    def _apply_outline(self) -> None:
        """A raincloud box strokes its edges in the font color (ADR 0021)."""

        stroke = config.get("font_general_color") or "#000000"
        overrides = [
            (self.box_style, "edgecolor", "plot_box_edgecolor", stroke),
            (self.outlier_style, "marker", "plot_box_outlier_marker", "o"),
            (
                self.outlier_style,
                "markersize",
                "plot_box_outlier_size",
                RAINCLOUD_OUTLIER_SIZE,
            ),
            (self.outlier_style, "markerfacecolor", "plot_box_outlier_color", "none"),
            (
                self.outlier_style,
                "markeredgecolor",
                "plot_box_outlier_edge_color",
                stroke,
            ),
            (self.median_style, "color", "plot_box_median_color", stroke),
            (self.whisker_style, "color", "plot_box_whisker_color", stroke),
            (self.cap_style, "color", "plot_box_cap_color", stroke),
        ]
        # an explicit chart style still wins over the outline defaults
        for style, key, style_key, value in overrides:
            if style_key not in self.style:
                style[key] = value

    def draw(self, ax, ctx):
        grouped = self.grouped_values()
        labels = list(grouped.keys())
        values = [grouped[lbl] for lbl in labels]

        if len(values) == 0:
            warnings.warn("No data points found for box plot.")
            return

        positions = [ctx.category_index[lbl] + self.offset for lbl in labels]

        box_style = dict(self.box_style)
        if box_style.get("facecolor") is None:
            box_style["facecolor"] = ctx.color

        boxprops = {k: v for k, v in box_style.items() if v is not None}
        flierprops = {k: v for k, v in self.outlier_style.items() if v is not None}
        medianprops = {k: v for k, v in self.median_style.items() if v is not None}
        whiskerprops = {k: v for k, v in self.whisker_style.items() if v is not None}
        capprops = {k: v for k, v in self.cap_style.items() if v is not None}

        bp = ax.boxplot(
            values,
            positions=positions,
            widths=self.width,
            zorder=self.zorder,
            orientation=self.orientation,
            patch_artist=True,
            showfliers=self.show_outliers if self.show_outliers is not None else True,
            notch=self.show_notch if self.show_notch is not None else False,
            boxprops=boxprops if boxprops else None,
            flierprops=flierprops if flierprops else None,
            medianprops=medianprops if medianprops else None,
            whiskerprops=whiskerprops if whiskerprops else None,
            capprops=capprops if capprops else None,
        )

        alpha = box_style.get("alpha", 1.0)
        for i, patch in enumerate(bp["boxes"]):
            if box_style.get("facecolor"):
                patch.set_facecolor(box_style["facecolor"])
            if self.color_by_group and self.box_style.get("facecolor") is None:
                patch.set_facecolor(self.group_color(i, ctx.color))
            if alpha is not None:
                patch.set_alpha(alpha)

        self._etch(bp["boxes"])
        if self.side:
            self._clip_to_side(bp, positions)
        label_roles = self.label_roles(ctx.emphasis)
        roles = [label_roles[lbl] for lbl in labels]
        self._apply_box_emphasis(bp, roles)
        self.keep_legend_body(bp["boxes"], roles, ctx)
        if self.show_values:
            # the median is the number a reader takes from a box (ADR 0033)
            for position, vals, role in zip(positions, values, roles):
                if role != EMPHASIS_BACKGROUND:
                    self._label_median(ax, position, vals)
        label = self.label(ctx)
        self.register_patch_hover(
            [
                (box, self.summary_datum(label, ctx.category_index[lbl], vals))
                for box, lbl, vals in zip(bp["boxes"], labels, values)
            ]
        )

    def legend_handles(self):
        return self.body_legend_handles()

    def _clip_to_side(self, bp: dict, positions: list) -> None:
        """Keep the box, median, and caps on one side of each box center."""

        axis = 1 if self.is_horizontal else 0
        clip = np.minimum if self.side < 0 else np.maximum
        for i, center in enumerate(positions):
            verts = bp["boxes"][i].get_path().vertices
            verts[:, axis] = clip(verts[:, axis], center)
            for line in [bp["medians"][i]] + bp["caps"][2 * i : 2 * i + 2]:
                data = np.asarray(line.get_xdata() if axis == 0 else line.get_ydata())
                (line.set_xdata if axis == 0 else line.set_ydata)(clip(data, center))

    def _apply_box_emphasis(self, bp: dict, roles: list) -> None:
        """Apply per-label roles; whiskers, caps, medians, and outliers follow the box."""

        for i, role in enumerate(roles):
            if role is None:
                continue
            box = bp["boxes"][i]
            median = bp["medians"][i]
            strokes = bp["whiskers"][2 * i : 2 * i + 2] + bp["caps"][2 * i : 2 * i + 2]
            fliers = bp["fliers"][i : i + 1]
            if role == EMPHASIS_BACKGROUND:
                box.set_facecolor(self.muted_color)
                box.set_edgecolor(self.muted_color)
                box.set_alpha(self.muted_alpha)
                box.set_linewidth(box.get_linewidth() * MUTED_WIDTH_SCALE)
                for line in strokes + [median]:
                    line.set_color(self.muted_color)
                    line.set_linewidth(line.get_linewidth() * MUTED_WIDTH_SCALE)
                for flier in fliers:
                    flier.set_markerfacecolor(self.muted_color)
                    flier.set_markeredgecolor(self.muted_color)
                    flier.set_alpha(self.muted_alpha)
            else:
                box.set_linewidth(box.get_linewidth() * HIGHLIGHT_WIDTH_SCALE)
                median.set_linewidth(median.get_linewidth() * HIGHLIGHT_WIDTH_SCALE)


def beeswarm_offsets(
    values_px: np.ndarray, diameter_px: float, one_sided: bool = False
) -> np.ndarray:
    """Non-overlapping offsets across the category axis, in pixels.

    Greedy placement in sorted-value order: each point takes the candidate
    offset nearest the center that keeps it a diameter away from every point
    already placed within a diameter along the value axis. One-sided packing
    only grows away from the center in the positive direction.
    """

    values_px = np.asarray(values_px, dtype=float)
    order = np.argsort(values_px, kind="stable")
    d2 = diameter_px**2
    placed_off, placed_val = [], []
    offsets = np.zeros(len(values_px))
    for i in order:
        v = values_px[i]
        if placed_val:
            offs = np.asarray(placed_off)
            vals = np.asarray(placed_val)
            near = np.abs(vals - v) < diameter_px
            offs, vals = offs[near], vals[near]
        else:
            offs = vals = np.empty(0)
        dv2 = (vals - v) ** 2
        # candidates: the center, then tangent to each neighbor on either side
        spread = np.sqrt(np.maximum(d2 - dv2, 0.0))
        cands = np.concatenate([[0.0], offs + spread, offs - spread])
        if one_sided:
            cands = cands[cands >= 0]
        cands = cands[np.argsort(np.abs(cands), kind="stable")]
        chosen = 0.0
        for c in cands:
            if np.all((c - offs) ** 2 + dv2 >= d2 * 0.999):
                chosen = c
                break
        offsets[i] = chosen
        placed_off.append(chosen)
        placed_val.append(v)
    return offsets


def strip_offsets(n: int, jitter: float) -> np.ndarray:
    """Seeded uniform jitter across the category axis, in data units."""

    return np.random.default_rng(0).uniform(-jitter / 2, jitter / 2, n)


class SwarmLayer(UnclippedMarksMixin, PointLabelMixin, GroupLayer):
    kind = "swarm"

    def _resolve_style(self):
        super()._resolve_style()
        self._take_record_roles()
        self._resolve_value_labels()
        self._init_point_labels()
        # a raincloud's box prints the median, so its rain labels the extremes
        self.label_median = self.settings.get("label_median", True)
        if not self.label_median:
            self.label_spots = (
                POINT_LABEL_SPOTS_HORIZONTAL
                if self.is_horizontal
                else POINT_LABEL_SPOTS_VERTICAL
            )
        self.mode = self.settings.get("mode") or DEFAULT_SWARM_MODE
        if self.mode not in (SWARM_MODE.SWARM, SWARM_MODE.STRIP):
            raise ValueError(
                f"Invalid swarm mode '{self.mode}'. "
                f"Must be one of ['{SWARM_MODE.SWARM}', '{SWARM_MODE.STRIP}']."
            )
        jitter = self.settings.get("jitter")
        self.jitter = DEFAULT_SWARM_JITTER if jitter is None else float(jitter)
        # a raincloud's rain sits off-center in a narrower cell (ADR 0021)
        self.offset = self.settings.get("offset") or 0.0
        spread = self.settings.get("spread")
        self.max_offset = SWARM_MAX_OFFSET if spread is None else float(spread)
        # a raincloud's rain packs away from the box: -1 the low side, +1 high
        self.side = self.settings.get("side") or 0
        self.swarm_style = get_swarm_style(self.style)
        self.default_size = config["plot_swarm_size"]
        # a front's point size replaces the theme's; a chart style still wins
        size = self.settings.get("size")
        if size is not None and "plot_swarm_size" not in self.style:
            self.swarm_style["s"] = size
        # a highlight edge contrasts in the theme's own text color
        self.highlight_edge_color = config.get("font_general_color") or "#000000"
        # collections drawn per axes, packed by the panel after limits settle
        self._pending = {}

    def diameter_px(self, ax) -> float:
        """The marker diameter in pixels, the spacing the beeswarm keeps."""

        size = self.swarm_style.get("s")
        if size is None:
            size = self.default_size
        return np.sqrt(size) / 72 * ax.figure.dpi

    def jitter_offsets(self, values: np.ndarray, side: int) -> np.ndarray:
        """Per-point jitter from the category center, in data units.

        A nonzero `side` jitters on one side only: -1 toward lower category
        positions, +1 toward higher ones.
        """

        # the jitter width scales with the cell the points may spread over
        offsets = strip_offsets(
            len(values), self.jitter * self.max_offset / SWARM_MAX_OFFSET
        )
        return offsets if not side else (np.abs(offsets) * 2) * side

    def draw(self, ax, ctx):
        grouped = self.grouped_values()
        labels = list(grouped.keys())
        if not labels:
            warnings.warn("No data points found for swarm plot.")
            return

        index = ctx.category_index
        split = self._split_by_role(labels, grouped, ctx)

        base_style = dict(self.swarm_style)
        if ctx.z_order is not None:
            base_style["zorder"] = ctx.z_order
        if base_style.get("c") is None:
            base_style["c"] = ctx.color
        if base_style.get("s") is None:
            base_style["s"] = self.default_size

        # one collection per role with a single legend entry; colored by
        # group, one collection per label and role, and the cloud's legend
        # lists the groups
        positions = list(index.values())
        lo, hi = min(positions) - 0.5, max(positions) + 0.5
        if self.color_by_group:
            batches = [
                ([lbl], role, i)
                for i, lbl in enumerate(labels)
                for role in MARKER_ROLE_ORDER
            ]
        else:
            batches = [(labels, role, None) for role in MARKER_ROLE_ORDER]
        legend_taken = self.color_by_group
        for members, role, group_index in batches:
            members = [lbl for lbl in members if (lbl, role) in split]
            if not members:
                continue
            style = dict(base_style)
            if group_index is not None and self.swarm_style.get("c") is None:
                style["c"] = self.group_color(group_index, ctx.color)
            self._apply_emphasis(style, role, width_key="linewidths", color_key="c")
            if role == EMPHASIS_HIGHLIGHT:
                style["edgecolors"] = self.highlight_edge_color
            label = NO_LEGEND
            if role != EMPHASIS_BACKGROUND and not legend_taken:
                label = self.label(ctx)
                legend_taken = True
            groups = [
                (index[lbl] + self.offset, split[lbl, role][0]) for lbl in members
            ]
            centers = np.concatenate([np.full(len(v), pos) for pos, v in groups])
            values = np.concatenate([v for _, v in groups])
            x, y = (values, centers) if self.is_horizontal else (centers, values)
            sizes = style.pop("s")
            collection = _draw_scatter_marks(
                ax.scatter, x, y, sizes, style, label, role == EMPHASIS_HIGHLIGHT
            )
            self.register_marks(ax, collection)
            positions = np.concatenate(
                [np.full(len(v), index[lbl]) for lbl, (_, v) in zip(members, groups)]
            )
            self.register_hover(
                collection,
                _point_resolver(self.label(ctx), positions, values, self.is_horizontal),
            )
            # the category axis spans every group edge to edge, like a box plot
            edges = (
                collection.sticky_edges.y
                if self.is_horizontal
                else collection.sticky_edges.x
            )
            edges[:] = [lo, hi]
            texts = None
            if self.show_values and role != EMPHASIS_BACKGROUND:
                texts = np.concatenate([split[lbl, role][1] for lbl in members])
            self._pending.setdefault(id(ax), []).append((collection, groups, texts))
        interval = ax.dataLim.intervaly if self.is_horizontal else ax.dataLim.intervalx
        interval[:] = (min(interval[0], lo), max(interval[1], hi))

    def _split_by_role(self, labels: list, grouped: dict, ctx: DrawContext) -> dict:
        """Each group's (values, value texts) keyed by (label, role).

        A point takes the panel's role, else its record's, else its group's;
        value texts come from the whole group, so a split keeps its extremes.
        """

        counts = [len(grouped[lbl]) for lbl in labels]
        unit_roles = [
            role
            for role, n in zip(self._group_roles(labels, ctx.emphasis), counts)
            for _ in range(n)
        ]
        roles = np.array(self._marker_roles(unit_roles, ctx), dtype=object)
        split, start = {}, 0
        for lbl, n in zip(labels, counts):
            values = np.asarray(grouped[lbl], dtype=float)
            texts = self._group_value_texts(values)
            own = roles[start : start + n]
            start += n
            for role in MARKER_ROLE_ORDER:
                picked = own == role
                if picked.any():
                    split[lbl, role] = (values[picked], texts[picked])
        return split

    def _group_value_texts(self, values: np.ndarray) -> np.ndarray:
        """One group's min, median, and max texts, `None` on every other point.

        The median labels the point nearest it; when that point is also the
        min or max, the extreme keeps it, so no point prints twice (ADR 0033).
        """

        labelled = np.full(len(values), None, dtype=object)
        if len(values) == 0:
            return labelled
        lowest, highest = int(np.argmin(values)), int(np.argmax(values))
        marks = [(lowest, values[lowest]), (highest, values[highest])]
        if self.label_median:
            median = float(np.median(values))
            marks.insert(0, (int(np.argmin(np.abs(values - median))), median))
        for index, value in marks:
            labelled[index] = _format_value(self.value_format, value)
        return labelled
        order = np.argsort(values, kind="stable")
        along = 0 if self.is_horizontal else 1
        ends = np.zeros((2, 2))
        ends[:, along] = values[order[[0, -1]]]
        span_px = np.ptp(ax.transData.transform(ends)[:, along])
        labelled[order] = self._value_texts(
            ax, values[order], not self.is_horizontal, span_px * 72.0 / ax.figure.dpi
        )
        return labelled


def _beeswarm_units(
    ax, position: float, values: np.ndarray, horizontal: bool, diameter_px, one_sided
) -> np.ndarray:
    """Unsigned beeswarm offsets of `values` around `position`, in data units."""

    centers = np.full(len(values), position, dtype=float)
    points = (
        np.column_stack([values, centers])
        if horizontal
        else np.column_stack([centers, values])
    )
    px = ax.transData.transform(points)
    value_px = px[:, 0] if horizontal else px[:, 1]
    offsets_px = beeswarm_offsets(value_px, diameter_px, one_sided)
    # pixels per data unit along the category axis; unsigned, so a side
    # stays in data units on an inverted axis
    unit = ax.transData.transform([[0, 1]] if horizontal else [[1, 0]])
    origin = ax.transData.transform([[0, 0]])
    scale = abs((unit - origin)[0][1 if horizontal else 0])
    return offsets_px / scale


def pack_swarms(ax, layers: list, side: int = 0) -> None:
    """Spread the swarm points drawn into `ax`; the panel calls this once its view is final.

    Points at one category position and side pack as one cloud, whichever
    layer or emphasis role drew them, so overlaid series never cover each
    other (ADR 0020). A layer's own side wins over the panel's `side`, and
    each layer keeps its own spread. Strip layers jitter on their own.
    """

    entries = [
        (layer, *entry) for layer in layers for entry in layer._pending.pop(id(ax), [])
    ]
    offsets, clouds = {}, defaultdict(list)
    for i, (layer, _, groups, _) in enumerate(entries):
        layer_side = layer.side or side
        for j, (position, values) in enumerate(groups):
            if layer.mode == SWARM_MODE.STRIP:
                offsets[i, j] = layer.jitter_offsets(values, layer_side)
            else:
                key = (position, layer_side, layer.is_horizontal)
                clouds[key].append((i, j))

    def member(i, j) -> tuple:
        """The layer and values of group `j` in pending entry `i`."""

        layer, _, groups, _ = entries[i]
        return layer, groups[j][1]

    for (position, cloud_side, horizontal), members in clouds.items():
        values = [member(i, j)[1] for i, j in members]
        diameter = max(member(i, j)[0].diameter_px(ax) for i, j in members)
        units = _beeswarm_units(
            ax,
            position,
            np.concatenate(values),
            horizontal,
            diameter,
            bool(cloud_side),
        )
        start = 0
        for (i, j), part in zip(members, values):
            spread = member(i, j)[0].max_offset
            placed = np.clip(units[start : start + len(part)], -spread, spread)
            offsets[i, j] = placed * cloud_side if cloud_side else placed
            start += len(part)

    for i, (layer, collection, groups, texts) in enumerate(entries):
        xy = np.asarray(collection.get_offsets()).copy()
        xy[:, 1 if layer.is_horizontal else 0] += np.concatenate(
            [offsets[i, j] for j in range(len(groups))]
        )
        collection.set_offsets(xy)
        # labels read the packed positions; every point is an obstacle
        layer._pending_labels.setdefault(id(ax), []).append(
            (
                xy[:, 0],
                xy[:, 1],
                collection.get_sizes(),
                texts,
                layer.value_font,
                layer.value_padding,
            )
        )


# keeps the two inner boxes of a split violin off the shared seam
SPLIT_INNER_OFFSET = 0.05
# raincloud geometry (ADR 0021), in category-axis units around the position:
# the box is centered on the position, the cloud's seam sits past it on the
# high side, and the rain starts past it on the low side and packs outward
RAINCLOUD_BOX_WIDTH = 0.1
RAINCLOUD_CLOUD_OFFSET = 0.08
# the full violin width; the cloud draws one half of it
RAINCLOUD_CLOUD_WIDTH = 0.6
RAINCLOUD_RAIN_OFFSET = 0.08
RAINCLOUD_RAIN_SPREAD = 0.28
# the rain is denser than a standalone swarm, so its points are smaller
RAINCLOUD_RAIN_SIZE = 6
# outliers are hollow rings, small enough not to outweigh the rain
RAINCLOUD_OUTLIER_SIZE = 4
INNER_QUARTILE_WIDTH_SCALE = 5.0


def dumbbell_records(chart: dict) -> list:
    """The chart's dumbbell records, in drawing order."""

    data = chart.get("data")
    if not isinstance(data, list):
        return []
    return [record for record in data if isinstance(record, dict)]


DUMBBELL_SORT_KEYS = {
    DUMBBELL_SORT_KEY.START: lambda record: record["start"],
    DUMBBELL_SORT_KEY.END: lambda record: record["end"],
    DUMBBELL_SORT_KEY.DELTA: lambda record: record["end"] - record["start"],
}


def sort_dumbbell_charts(charts: List[dict], settings: dict) -> List[dict]:
    """The charts with their records in `sort` order by `sort_by` (ADR 0050).

    Each chart sorts on its own; overlaid charts share the first one's rows,
    and so do subplots sharing the category axis, whose one set of tick
    labels must name every subplot's rows. Ties keep input order.
    """

    sort = validate_sort(settings.get("sort"))
    key = DUMBBELL_SORT_KEYS[validate_dumbbell_sort_by(sort, settings.get("sort_by"))]
    if sort is None:
        return charts
    sign = -1 if sort == SORT.DESCENDING else 1
    ranked = [
        sorted(dumbbell_records(chart), key=lambda r: sign * key(r)) for chart in charts
    ]
    horizontal = (
        settings.get("orientation") or DEFAULT_ORIENTATION
    ) == ORIENTATION.HORIZONTAL
    if settings.get("subplots") and settings.get("sharey" if horizontal else "sharex"):
        order = {}
        for records in ranked:
            for record in records:
                order.setdefault(record["label"], len(order))
        # a stable sort: a label the first chart lacks keeps its own rank
        ranked = [
            sorted(records, key=lambda r: order[r["label"]]) for records in ranked
        ]
    return [{**chart, "data": records} for chart, records in zip(charts, ranked)]


# how far a composed dumbbell's start dot fades toward white from its end dot
DUMBBELL_START_LIGHTEN = 0.5
# a minor value gridline is this much fainter than a labelled one
MINOR_GRID_ALPHA_SCALE = 0.6
# a composed z-order puts the connectors this far under the dots
DUMBBELL_CONNECTOR_Z_BELOW = 0.5


class DumbbellLayer(UnclippedMarksMixin, GroupLayer):
    """Two dots per category joined by a connector, on the category index (ADR 0050).

    The dots draw through the scatter marks; one role batch at a time, each
    batch its connectors under a start and an end collection.
    """

    kind = "dumbbell"
    labels_past_mark = True

    def _resolve_style(self):
        # the front validated the records, their roles included
        self.records = dumbbell_records(self.chart)
        super()._resolve_style()
        self.starts = np.array([r["start"] for r in self.records], dtype=float)
        self.ends = np.array([r["end"] for r in self.records], dtype=float)
        self.record_roles = [r.get("emphasis") for r in self.records]
        self.dumbbell_style = get_dumbbell_style(self.style)
        # a front's marker pair and connector style yield to the chart style
        overrides = zip(
            ("start_marker", "end_marker"),
            validate_marker_pair(self.settings.get("marker")) or (),
        )
        for key, value in overrides:
            if f"plot_dumbbell_{key}" not in self.style:
                self.dumbbell_style[key] = value
        connector_style = self.settings.get("connector_style")
        if (
            connector_style is not None
            and "plot_dumbbell_connector_style" not in self.style
        ):
            self.dumbbell_style["connector_style"] = connector_style
        accent = get_discrete_colors(COLORS.PaperAccent, 2)
        self.pair_colors = tuple(
            self.dumbbell_style.get(key) or default
            for key, default in zip(("start_color", "end_color"), accent)
        )
        # composed, only the chart's own colors outrank the cycle color
        self.own_colors = tuple(
            self.style.get(f"plot_dumbbell_{key}")
            for key in ("start_color", "end_color")
        )
        self.names = (self.settings.get("start_name"), self.settings.get("end_name"))
        self.value_mode = validate_dumbbell_show_values(
            self.settings.get("show_values")
        )
        self._resolve_value_labels()
        self.show_values = self.value_mode is not None
        self.labels_below_range = self.value_mode == DUMBBELL_VALUE.ENDPOINTS
        self.show_direction = bool(self.settings.get("show_direction"))
        self.grid_minor = int(self.dumbbell_style.get("grid_minor") or 0)
        # a highlight edge contrasts in the theme's own text color
        self.highlight_edge_color = config.get("font_general_color") or "#000000"

    def labels(self) -> list:
        return [record["label"] for record in self.records]

    def value_data(self):
        return list(self.starts) + list(self.ends)

    def _endpoint_colors(self, ctx: DrawContext) -> tuple:
        """The start and end colors: the pair alone, a cycle shade pair composed."""

        if ctx.sole_dumbbell or ctx.color is None:
            return self.pair_colors
        start, end = self.own_colors
        return (
            start or _lighten(ctx.color, DUMBBELL_START_LIGHTEN),
            end or ctx.color,
        )

    def _endpoint_labels(self, ctx: DrawContext) -> tuple:
        """The legend labels of the start and end dots, named after the endpoints.

        Composed, the series label prefixes each name; the end dot alone
        carries it when the endpoints have no names.
        """

        start_name, end_name = self.names
        series = None if ctx.sole_dumbbell else self.label(ctx)
        if series is not None:
            start_name = start_name and f"{series} ({start_name})"
            end_name = f"{series} ({end_name})" if end_name else series
        return tuple(NO_LEGEND if n is None else n for n in (start_name, end_name))

    def draw(self, ax, ctx):
        if not self.records:
            return
        index = ctx.category_index
        positions = np.array([index[label] for label in self.labels()], dtype=float)
        roles = [
            panel_role or record_role
            for panel_role, record_role in zip(
                self._group_roles(self.labels(), ctx.emphasis), self.record_roles
            )
        ]
        style = self.dumbbell_style
        dot_style = {
            k: style[k]
            for k in ("alpha", "linewidths", "edgecolors", "zorder")
            if k in style
        }
        line_style = {
            "color": style.get("connector_color"),
            "linewidth": style.get("connector_width"),
            "linestyle": style.get("connector_style"),
            "zorder": style.get("connector_zorder"),
        }
        if ctx.z_order is not None:
            dot_style["zorder"] = ctx.z_order
            line_style["zorder"] = ctx.z_order - DUMBBELL_CONNECTOR_Z_BELOW
        size = style["s"]
        colors = self._endpoint_colors(ctx)
        names = self._endpoint_labels(ctx)
        distinct = self.starts != self.ends
        lo, hi = positions.min() - 0.5, positions.max() + 0.5

        legend_taken = False
        for role in (None, EMPHASIS_HIGHLIGHT, EMPHASIS_BACKGROUND):
            members = np.array([r == role for r in roles])
            if not members.any():
                continue
            named = role != EMPHASIS_BACKGROUND and not legend_taken
            legend_taken = legend_taken or named
            self._draw_connectors(ax, positions, members & distinct, line_style, role)
            # coincident endpoints draw the end dot alone
            endpoints = (
                (self.starts, members & distinct, "start_marker", 0),
                (self.ends, members, "end_marker", 1),
            )
            for values, mask, marker_key, k in endpoints:
                if not mask.any():
                    continue
                marks = dict(dot_style, c=colors[k], marker=style.get(marker_key))
                self._apply_emphasis(marks, role, width_key="linewidths", color_key="c")
                if role == EMPHASIS_HIGHLIGHT:
                    marks["edgecolors"] = self.highlight_edge_color
                x, y = values[mask], positions[mask]
                if not self.is_horizontal:
                    x, y = y, x
                label = names[k] if named else NO_LEGEND
                # an unnamed or unlisted dot still hovers under its series
                hover_label = self.label(ctx) if label == NO_LEGEND else label
                collection = _draw_scatter_marks(
                    ax.scatter,
                    x,
                    y,
                    size,
                    marks,
                    label,
                    role == EMPHASIS_HIGHLIGHT,
                )
                self.register_marks(ax, collection)
                self.register_hover(
                    collection,
                    _point_resolver(
                        hover_label,
                        positions[mask],
                        values[mask],
                        self.is_horizontal,
                    ),
                )
                # the category axis spans every row edge to edge, like boxes
                edges = (
                    collection.sticky_edges.y
                    if self.is_horizontal
                    else collection.sticky_edges.x
                )
                edges[:] = [lo, hi]
        interval = ax.dataLim.intervaly if self.is_horizontal else ax.dataLim.intervalx
        interval[:] = (min(interval[0], lo), max(interval[1], hi))

        radius = np.sqrt(size) / 2
        if self.show_direction:
            self._draw_arrows(ax, positions, roles, radius)
        if self.show_values:
            self._label_values(ax, positions, roles, radius)

    def _arrow_offset(self, radius: float) -> float:
        """How far off the connector a direction arrow runs, in points."""

        return radius + self.dumbbell_style.get("arrow_gap", 0)

    def _draw_arrows(self, ax, positions, roles, radius: float) -> None:
        """A thin arrow beside each distinct record, from its start to its end.

        It runs above a horizontal dumbbell and right of a vertical one.
        """

        offset = self._arrow_offset(radius)
        shift = {"y": offset} if self.is_horizontal else {"x": offset}
        transform = offset_copy(ax.transData, fig=ax.figure, units="points", **shift)
        style = self.dumbbell_style
        for position, start, end, role in zip(positions, self.starts, self.ends, roles):
            if start == end:
                continue
            props = {
                "arrowstyle": style.get("arrow_style"),
                "color": style.get("arrow_color"),
                "linewidth": style.get("arrow_width"),
                "shrinkA": 0,
                "shrinkB": 0,
            }
            self._apply_emphasis(props, role)
            zorder = props.pop("zorder", 0) + style.get("connector_zorder", 0)
            tail, head = (start, position), (end, position)
            if not self.is_horizontal:
                tail, head = tail[::-1], head[::-1]
            ax.annotate(
                "",
                xy=head,
                xytext=tail,
                xycoords=transform,
                textcoords=transform,
                arrowprops=props,
                zorder=zorder,
                annotation_clip=False,
            )

    def _draw_connectors(self, ax, positions, mask, line_style, role) -> None:
        """One line per masked record from its start to its end."""

        if not mask.any():
            return
        segments = [
            (
                [(start, position), (end, position)]
                if self.is_horizontal
                else [(position, start), (position, end)]
            )
            for position, start, end in zip(
                positions[mask], self.starts[mask], self.ends[mask]
            )
        ]
        style = dict(line_style)
        self._apply_emphasis(style, role)
        ax.add_collection(LineCollection(segments, **style))

    def _label_values(self, ax, positions, roles, radius: float) -> None:
        """Print each unmuted record's endpoints past its dots, or its delta.

        An endpoint label sits away from the connector; the delta sits at the
        connector midpoint, above it (or beside it when vertical).
        """

        pad = radius + self.value_padding
        connector_pad = (
            self.dumbbell_style.get("connector_width", 0) / 2 + self.value_padding
        )
        arrow_pad = (
            self._arrow_offset(radius)
            + self.dumbbell_style.get("arrow_width", 0)
            + self.value_padding
        )
        for position, start, end, role in zip(positions, self.starts, self.ends, roles):
            if role == EMPHASIS_BACKGROUND:
                continue
            if self.value_mode == DUMBBELL_VALUE.DELTA:
                offset = connector_pad if start != end else pad
                if self.show_direction and start != end:
                    # the delta reads past the direction arrow, not over it
                    offset = arrow_pad
                self._annotate(ax, (start + end) / 2, position, end - start, offset, 0)
                continue
            marks = (
                [(end, 1)]
                if start == end
                else [
                    (start, np.sign(start - end)),
                    (end, np.sign(end - start)),
                ]
            )
            for value, side in marks:
                self._annotate(ax, value, position, value, pad, int(side))

    def _annotate(self, ax, value, position, number, pad, side: int) -> None:
        """Print `number` at a record's `value`, `pad` points away from it.

        A `side` of -1 or +1 moves it down or up the value axis; 0 moves it
        off the connector, across the category axis.
        """

        if self.is_horizontal:
            xy = (value, position)
            if side:
                offset, ha, va = (
                    (side * pad, 0),
                    "left" if side > 0 else "right",
                    "center",
                )
            else:
                offset, ha, va = (0, pad), "center", "bottom"
        else:
            xy = (position, value)
            if side:
                offset, ha, va = (
                    (0, side * pad),
                    "center",
                    "bottom" if side > 0 else "top",
                )
            else:
                offset, ha, va = (pad, 0), "left", "center"
        ax.annotate(
            _format_value(self.value_format, number),
            xy=xy,
            xytext=offset,
            textcoords="offset points",
            ha=ha,
            va=va,
            zorder=TEXT_ANNOTATION_ZORDER,
            **self.value_font,
        )


def inner_line_marks(inner: str, values) -> list:
    """The `(value, linestyle)` line marks of a median or quartiles inner."""

    q1, median, q3 = np.percentile(np.asarray(values, dtype=float), [25, 50, 75])
    if inner == VIOLIN_INNER.MEDIAN:
        return [(median, "-")]
    return [(q1, ":"), (median, "--"), (q3, ":")]


class ViolinLayer(GroupLayer):
    """A per-label KDE body with inner marks drawn from the data."""

    kind = "violin"
    sorts_by_median = True

    def _resolve_style(self):
        super()._resolve_style()
        self.inner = self.settings.get("inner")
        self.bandwidth = self.settings.get("bandwidth")
        self.split = self.settings.get("split")
        # a raincloud keeps one half of the body: -1 the low side, +1 the high
        self.side = self.settings.get("side") or 0
        self.offset = self.settings.get("offset") or 0.0
        self._legend_roles = []
        self.violin_style = get_violin_style(self.style)
        # a front's body width replaces the theme's; a chart style still wins
        width = self.settings.get("width")
        if width is not None and "plot_violin_width" not in self.style:
            self.violin_style["width"] = width
        self.inner_style = get_violin_inner_style(self.style)
        self._resolve_value_labels()
        # split halves take the multiple palette; a layer receives one ctx color
        self.split_colors = (
            create_color_cycle(config["color_general_multiple"], 2)
            if self.split
            else None
        )
        self.split_values = []

    def legend_handles(self):
        if self.color_by_group:
            return self.group_legend_handles(self._legend_roles)
        # split values are known once draw() has grouped the data
        if not self.split:
            return self.body_legend_handles()
        if not self.split_values:
            return None
        return [
            Patch(facecolor=self.split_colors[i]["color"], label=str(value))
            for i, value in enumerate(self.split_values)
        ]

    def _group(self) -> tuple:
        """Values per label (and per split value) in first-seen order."""

        label_attr = get_attr_value("label", self.chart, "label")
        value_attr = get_attr_value("value", self.chart, "value")
        data = self.chart.get("data", [])
        grouped, split_values = {}, []
        if isinstance(data, list):
            for d in data:
                lbl, val = d.get(label_attr), d.get(value_attr)
                if lbl is None or val is None:
                    continue
                side = d.get(self.split) if self.split else None
                if self.split and side not in split_values:
                    split_values.append(side)
                grouped.setdefault(lbl, {}).setdefault(side, []).append(val)
        if self.split and grouped and len(split_values) != 2:
            raise ValueError(
                f"`split` key {self.split!r} must take exactly two distinct "
                f"values, found {len(split_values)}."
            )
        self.split_values = split_values
        return self.labels(), grouped

    def draw(self, ax, ctx):
        labels, grouped = self._group()
        if len(labels) == 0:
            warnings.warn("No data points found for violin plot.")
            return

        body_style = dict(self.violin_style)
        width = body_style.pop("width")
        if body_style.get("facecolor") is None:
            body_style["facecolor"] = ctx.color
        label_roles = self.label_roles(ctx.emphasis)
        roles = [label_roles[label] for label in labels]
        # (split value, side): -1 draws the low half, +1 the high half, 0 both
        sides = list(zip(self.split_values, (-1, 1))) or [(None, self.side)]
        self._legend_roles = roles
        drawn_bodies, drawn_roles = [], []

        for i, label in enumerate(labels):
            position = ctx.category_index[label] + self.offset
            for j, (split_value, side) in enumerate(sides):
                values = grouped[label].get(split_value)
                if not values:
                    continue
                if len(values) < 2:
                    raise ValueError(
                        f"Violin {label!r} needs at least two values to estimate "
                        "a density."
                    )
                style = dict(body_style)
                if self.split:
                    style["facecolor"] = self.split_colors[j]["color"]
                elif self.color_by_group and self.violin_style.get("facecolor") is None:
                    style["facecolor"] = self.group_color(i, ctx.color)
                artists = [
                    self._draw_body(
                        ax, values, position, width, style, side, ctx.value_scale
                    )
                ]
                drawn_bodies.append(artists[0])
                drawn_roles.append(roles[i])
                artists += self._draw_inner(ax, values, position, width, side)
                self._apply_violin_emphasis(artists, roles[i])
                if self.show_values and roles[i] != EMPHASIS_BACKGROUND:
                    # a half body carries its label at the middle of its half
                    self._label_median(ax, position + side * width / 4, values)
                # a split half stands for its split value, like its legend entry
                datum = self.summary_datum(
                    str(split_value) if self.split else self.label(ctx),
                    ctx.category_index[label],
                    values,
                )
                self.register_hover(artists[0], lambda _, datum=datum: datum)
        self.keep_legend_body(drawn_bodies, drawn_roles, ctx)

    def _draw_body(self, ax, values, position, width, style, side, scale):
        options = dict(
            positions=[position],
            widths=width,
            orientation=self.orientation,
            showextrema=False,
            showmedians=False,
            showmeans=False,
        )
        if scale == SCALE.LOG:
            parts = ax.violin([self._log_stats(values)], **options)
        else:
            parts = ax.violinplot([values], bw_method=self.bandwidth, **options)
        body = parts["bodies"][0]
        # above the axis gridlines (zorder 1.5), like a box patch
        body.set_zorder(2)
        facecolor = style.get("facecolor")
        if facecolor is not None:
            body.set_facecolor(facecolor)
        edgecolor = style.get("edgecolor")
        body.set_edgecolor(edgecolor if edgecolor is not None else facecolor)
        if style.get("alpha") is not None:
            body.set_alpha(style["alpha"])
        if style.get("linewidth") is not None:
            body.set_linewidth(style["linewidth"])
        if style.get("hatch"):
            body.set_hatch(style["hatch"])
        self._etch([body])
        if side:
            axis = 1 if self.is_horizontal else 0
            clip = np.minimum if side < 0 else np.maximum
            for path in body.get_paths():
                path.vertices[:, axis] = clip(path.vertices[:, axis], position)
        return body

    def _log_stats(self, values) -> dict:
        """The body's density estimated on log10 values, mapped back to values."""

        def kde(data, coords):
            return GaussianKDE(data, self.bandwidth).evaluate(coords)

        (stats,) = cbook.violin_stats([np.log10(values)], kde)
        for key in ("coords", "mean", "median", "min", "max", "quantiles"):
            stats[key] = np.power(10.0, stats[key])
        return stats

    def _draw_inner(self, ax, values, position, width, side) -> list:
        if self.inner is None:
            return []
        values = np.asarray(values, dtype=float)
        q1, median, q3 = np.percentile(values, [25, 50, 75])
        color = self.inner_style["color"]
        linewidth = self.inner_style["linewidth"]
        zorder = 3
        xy = (lambda c, v: (v, c)) if self.is_horizontal else (lambda c, v: (c, v))

        def line(c0, v0, c1, v1, **kwargs):
            (x0, y0), (x1, y1) = xy(c0, v0), xy(c1, v1)
            return ax.plot([x0, x1], [y0, y1], color=color, zorder=zorder, **kwargs)[0]

        if self.inner == VIOLIN_INNER.BOX:
            iqr = q3 - q1
            inside = values[(values >= q1 - 1.5 * iqr) & (values <= q3 + 1.5 * iqr)]
            lo, hi = float(inside.min()), float(inside.max())
            centre = position + side * SPLIT_INNER_OFFSET
            whisker = line(centre, lo, centre, hi, linewidth=linewidth)
            bar = line(
                centre, q1, centre, q3, linewidth=linewidth * INNER_QUARTILE_WIDTH_SCALE
            )
            x, y = xy(centre, median)
            dot = ax.plot(
                [x],
                [y],
                marker="o",
                linestyle="none",
                markersize=self.inner_style["median_size"],
                markerfacecolor=self.inner_style["median_color"],
                markeredgecolor="none",
                zorder=zorder + 1,
            )[0]
            return [whisker, bar, dot]

        # the line marks span the body width at their value
        kde = GaussianKDE(values, self.bandwidth)
        grid = np.linspace(values.min(), values.max(), 100)
        peak = float(kde.evaluate(grid).max()) or 1.0

        def span(value, linestyle):
            h = float(kde.evaluate([value])[0]) / peak * width / 2
            lo_c = position if side > 0 else position - h
            hi_c = position if side < 0 else position + h
            return line(
                lo_c, value, hi_c, value, linewidth=linewidth, linestyle=linestyle
            )

        return [span(v, style) for v, style in inner_line_marks(self.inner, values)]

    def _apply_violin_emphasis(self, artists: list, role: Optional[str]) -> None:
        if role is None:
            return
        body, marks = artists[0], artists[1:]
        if role == EMPHASIS_BACKGROUND:
            body.set_facecolor(self.muted_color)
            body.set_edgecolor(self.muted_color)
            body.set_alpha(self.muted_alpha)
            body.set_linewidth(body.get_linewidth()[0] * MUTED_WIDTH_SCALE)
            for mark in marks:
                mark.set_color(self.muted_color)
                mark.set_markerfacecolor(self.muted_color)
                mark.set_alpha(self.muted_alpha)
                mark.set_linewidth(mark.get_linewidth() * MUTED_WIDTH_SCALE)
        else:
            body.set_linewidth(body.get_linewidth()[0] * HIGHLIGHT_WIDTH_SCALE)


# the points each ridge's density is evaluated on
RIDGE_GRIDSIZE = 200
# rows stack in z from the violin body's level, below an overlaid swarm
RIDGE_ZORDER = 2
RIDGE_ZORDER_SPAN = 0.9


class RidgelineLayer(GroupLayer):
    """Per-label density ridges stacked on the category index (ADR 0047)."""

    kind = "ridge"
    sorts_by_median = True

    def _resolve_style(self):
        super()._resolve_style()
        if self.settings.get("orientation") is None:
            self.orientation = ORIENTATION.HORIZONTAL
            self.is_horizontal = True
        self.bandwidth = self.settings.get("bandwidth")
        self.inner = validate_ridgeline_inner(self.settings.get("inner"))
        self.normalize = validate_ridgeline_scale(self.settings.get("normalize"))
        self.fill = self.settings.get("fill") is not False
        self.show_outline = self.settings.get("show_outline") is not False
        validate_ridge_marks(self.fill, self.show_outline)
        self.ridge_style = get_ridgeline_style(self.style)
        overlap = self.settings.get("overlap")
        self.overlap = validate_overlap(
            self.ridge_style["overlap"] if overlap is None else overlap
        )
        self.show_values = False
        # subplots share one value range, set once every layer is built
        self.shared_range = None

    def padded_range(self, log: Optional[bool] = None) -> Optional[tuple]:
        """The union of the rows' padded density ranges; None without a density.

        On a log value axis the densities, and so their padding, live in
        log10 space; `log` defaults to the front's own value scale.
        """

        if log is None:
            log = self.settings.get("scaley") == SCALE.LOG
        ends = [
            (curve[0]["x"], curve[-1]["x"])
            for curve in (
                kde1d(
                    np.log10(values) if log else values,
                    bandwidth=self.bandwidth,
                    gridsize=2,
                )
                for values in self.grouped_values().values()
                if len(values) > 1
            )
        ]
        if not ends:
            return None
        lo, hi = min(e[0] for e in ends), max(e[1] for e in ends)
        return (10.0**lo, 10.0**hi) if log else (lo, hi)

    def _grid_bounds(self, log: bool) -> tuple:
        """The shared or own padded range, widened to the ticks enclosing it;
        the value-axis limits win.

        The panel ends the value axis on a tick, and the ridges' baselines run
        the length of their grid, so the grid reaches those ticks too.
        """

        lo, hi = self.shared_range or self.padded_range(log)
        locator = mticker.LogLocator() if log else mticker.AutoLocator()
        ticks = np.asarray(locator.tick_values(lo, hi), dtype=float)
        if len(ticks) > 1:
            tol = float(np.min(np.diff(ticks))) * 1e-6
            below, above = ticks[ticks <= lo + tol], ticks[ticks >= hi - tol]
            lo = float(below.max()) if len(below) else lo
            hi = float(above.min()) if len(above) else hi
        axis = "x" if self.is_horizontal else "y"
        low, high = self.settings.get(f"{axis}min"), self.settings.get(f"{axis}max")
        return (lo if low is None else low, hi if high is None else high)

    def draw(self, ax, ctx):
        grouped = self.grouped_values()
        if not grouped:
            warnings.warn("No data points found for ridgeline plot.")
            return
        for label, values in grouped.items():
            if len(values) < 2:
                raise ValueError(
                    f"Ridge {label!r} needs at least two values to estimate a density."
                )

        roles = self.label_roles(ctx.emphasis)

        # on a log value axis the densities are estimated on log10 values
        log = ctx.value_scale == SCALE.LOG
        lo, hi = self._grid_bounds(log)
        if log:
            grouped_fit = {k: np.log10(v) for k, v in grouped.items()}
            lo, hi = np.log10(lo), np.log10(hi)
        else:
            grouped_fit = grouped
        curves = [
            kde1d(
                values, bandwidth=self.bandwidth, gridsize=RIDGE_GRIDSIZE, xlim=(lo, hi)
            )
            for values in grouped_fit.values()
        ]
        grid = np.array([point["x"] for point in curves[0]])
        if log:
            grid = np.power(10.0, grid)
        densities = [np.array([point["y"] for point in curve]) for curve in curves]
        peak = 1 + self.overlap
        common_max = max(float(d.max()) for d in densities)
        step = RIDGE_ZORDER_SPAN / len(grouped)
        # ridges rise from their tick: toward the first row (the top, on the
        # inverted axis) when horizontal, rightward when vertical
        rise = -1 if self.is_horizontal else 1

        style = self.ridge_style
        facecolor = style.get("facecolor")
        if facecolor is None:
            facecolor = ctx.color
        edgecolor = style.get("edgecolor")
        if edgecolor is None:
            edgecolor = facecolor

        for i, (label, values) in enumerate(grouped.items()):
            density = densities[i]
            scale = (
                common_max
                if self.normalize == RIDGELINE_SCALE.COMMON
                else density.max()
            )
            heights = density / (float(scale) or 1.0) * peak
            position = ctx.category_index[label]
            baseline = position
            tops = baseline + rise * heights
            # a ridge draws over the row it rises into, so overlap reads as depth
            depth = i if self.is_horizontal else len(grouped) - 1 - i
            zorder = RIDGE_ZORDER + depth * step
            artists = []
            if self.fill:
                fill_between = (
                    ax.fill_between if self.is_horizontal else ax.fill_betweenx
                )
                body = fill_between(
                    grid,
                    baseline,
                    tops,
                    facecolor=facecolor,
                    edgecolor="none",
                    linewidth=0,
                    alpha=style.get("alpha"),
                    hatch=style.get("hatch"),
                    zorder=zorder,
                )
                self._etch([body])
                # the grid ends on ticks and the ridge runs its length, so the
                # axis ends there too, without a margin past it
                (body.sticky_edges.x if self.is_horizontal else body.sticky_edges.y)[
                    :
                ] = [grid[0], grid[-1]]
                artists.append(("fill", body))
            artists += [
                ("mark", mark)
                for mark in self._draw_inner(
                    ax, values, grid, baseline, tops, zorder + step / 3
                )
            ]
            if self.show_outline:
                xy = (grid, tops) if self.is_horizontal else (tops, grid)
                outline = ax.plot(
                    *xy,
                    color=edgecolor,
                    linewidth=style.get("linewidth"),
                    zorder=zorder + 2 * step / 3,
                )[0]
                (
                    outline.sticky_edges.x
                    if self.is_horizontal
                    else outline.sticky_edges.y
                )[:] = [grid[0], grid[-1]]
                artists.append(("outline", outline))
            self._apply_ridge_emphasis(artists, roles[label])
            datum = self.summary_datum(self.label(ctx), position, values)
            self.register_hover(artists[0][1], lambda _, datum=datum: datum)

    def _draw_inner(self, ax, values, grid, baseline, tops, zorder) -> list:
        """The median or quartile marks, from the baseline up to the ridge."""

        if self.inner is None:
            return []
        lines = []
        for value, linestyle in inner_line_marks(self.inner, values):
            top = float(np.interp(value, grid, tops))
            xs, ys = [value, value], [baseline, top]
            lines.append(
                ax.plot(
                    *((xs, ys) if self.is_horizontal else (ys, xs)),
                    color=self.ridge_style["inner_color"],
                    linewidth=self.ridge_style["inner_linewidth"],
                    linestyle=linestyle,
                    zorder=zorder,
                )[0]
            )
        return lines

    def _apply_ridge_emphasis(self, artists: list, role: Optional[str]) -> None:
        if role is None:
            return
        for part, artist in artists:
            if role == EMPHASIS_HIGHLIGHT:
                if part == "outline":
                    artist.set_linewidth(artist.get_linewidth() * HIGHLIGHT_WIDTH_SCALE)
                continue
            artist.set_alpha(self.muted_alpha)
            if part == "fill":
                artist.set_facecolor(self.muted_color)
            else:
                artist.set_color(self.muted_color)
                artist.set_linewidth(artist.get_linewidth() * MUTED_WIDTH_SCALE)


# the axes fraction a colorbar takes, and its gap from the axes
COLORBAR_FRACTION = 0.05
COLORBAR_PAD = 0.03
COLORBAR_DIVIDER_PAD = 0.1


def _draw_colorbar(
    ax: plt.Axes, mappable, setting: dict, aspect_locked: bool = False
) -> None:
    """Draw a colorbar on the edge the resolved setting names (ADR 0035)."""

    colorbar = _place_colorbar(ax, mappable, setting, aspect_locked)
    fmt = _value_formatter(setting["format"])
    if fmt is not None:
        colorbar.formatter = fmt
        colorbar.update_ticks()
    if setting["ticks"] is not None:
        # set_ticks widens the bar to every tick; keep it to the mapped range
        low, high = colorbar.vmin, colorbar.vmax
        slack = (high - low) * 1e-9
        colorbar.set_ticks(
            [t for t in setting["ticks"] if low - slack <= t <= high + slack]
        )
    if setting["label"]:
        colorbar.set_label(setting["label"], **setting["label_style"])
    # tick labels take no family through tick_params; restyled directly
    family = setting["label_style"]["family"]
    for label in colorbar.ax.get_xticklabels() + colorbar.ax.get_yticklabels():
        label.set_fontfamily(family)


def _place_colorbar(ax: plt.Axes, mappable, setting: dict, aspect_locked: bool):
    """Place the bar on its edge and size it against the axes.

    The layout engine places it clear of titles and neighbouring axes; an
    aspect-locked axes instead carves it from its own box, which the engine
    would size to the grid cell rather than the box.
    """

    location, orientation = setting["location"], setting["orientation"]
    if not aspect_locked:
        # the layout engine keeps a colorbar at its own aspect (20:1 by
        # default), which shortens it beside a narrow axes: size it to the
        # axes slot instead
        bbox = ax.get_position()
        width, height = ax.figure.get_size_inches()
        along, across = bbox.height * height, bbox.width * width
        if orientation == ORIENTATION.HORIZONTAL:
            along, across = across, along
        return ax.figure.colorbar(
            mappable,
            ax=ax,
            location=location,
            fraction=COLORBAR_FRACTION,
            pad=COLORBAR_PAD,
            aspect=along / (across * COLORBAR_FRACTION),
        )
    cax = ax.inset_axes((0, 0, 1, 1))
    cax.set_axes_locator(_LockedBarLocator(ax, location))
    kwargs = {"orientation": orientation}
    if location == COLORBAR_LOCATION.LEFT:
        # a left bar reads outward; the other edges keep matplotlib's tick side
        kwargs["ticklocation"] = location
    return ax.figure.colorbar(mappable, cax=cax, **kwargs)


class _LockedBarLocator:
    """Places a bar beside the axes' drawn box, in display space.

    Display space stays valid while a tight-bbox save swaps the figure box,
    which an inch-based divider does not (#192).
    """

    def __init__(self, ax: plt.Axes, location: str):
        self._ax, self._location = ax, location

    def __call__(self, cax: plt.Axes, renderer) -> Bbox:
        ax, location = self._ax, self._location
        ax.apply_aspect()
        box = ax.get_position(original=False).transformed(ax.figure.transSubfigure)
        pad = COLORBAR_DIVIDER_PAD * ax.figure.dpi
        # a left or bottom bar crosses the chart's tick labels: pad past them
        if location == COLORBAR_LOCATION.LEFT:
            ticks = ax.yaxis.get_tightbbox(renderer)
            pad += max(box.x0 - ticks.x0, 0.0) if ticks else 0.0
        elif location == COLORBAR_LOCATION.BOTTOM:
            ticks = ax.xaxis.get_tightbbox(renderer)
            pad += max(box.y0 - ticks.y0, 0.0) if ticks else 0.0
        x0, y0, width, height = box.bounds
        if location in (COLORBAR_LOCATION.LEFT, COLORBAR_LOCATION.RIGHT):
            size = width * COLORBAR_FRACTION
            x0 = x0 - pad - size if location == COLORBAR_LOCATION.LEFT else box.x1 + pad
            bar = Bbox.from_bounds(x0, y0, size, height)
        else:
            size = height * COLORBAR_FRACTION
            y0 = (
                y0 - pad - size
                if location == COLORBAR_LOCATION.BOTTOM
                else box.y1 + pad
            )
            bar = Bbox.from_bounds(x0, y0, width, size)
        return bar.transformed(ax.figure.transSubfigure.inverted())


def _value_formatter(valfmt):
    """A `{x}`-style format string as a matplotlib formatter; others pass."""

    if isinstance(valfmt, str) and "{x" in valfmt:
        return mticker.StrMethodFormatter(valfmt)
    return valfmt


def heatmap_cell_roles(chart: dict, z: list) -> list:
    """A copy of the heatmap's per-cell `emphasis` grid, aligned to `z`.

    Absent roles read as a grid of None; a grid of another shape, or a cell
    role that is not one, raises.
    """

    roles = chart["data"].get("emphasis") if isinstance(chart["data"], dict) else None
    if roles is None:
        return [[None] * len(row) for row in z]
    shape = [len(row) for row in z]
    if (
        not isinstance(roles, list)
        or [len(row) if isinstance(row, list) else -1 for row in roles] != shape
    ):
        raise ValueError(
            "The heatmap `emphasis` grid must hold one role per cell of `z` "
            f"({len(z)} rows of {shape[0] if shape else 0})."
        )
    return [
        [
            validate_emphasis(role, f"heatmap cell ({i}, {j}) `emphasis`")
            for j, role in enumerate(row)
        ]
        for i, row in enumerate(roles)
    ]


class HeatmapLayer(Layer):
    ticks_at_axis_ends = False
    kind = "heatmap"
    # the theme keys the cells, values, and borders read
    style_prefix = "plot_heatmap"

    def _resolve_style(self):
        self.show_colorbars = self.settings.get("show_colorbars")
        self.colorbar = get_colorbar_setting(self.chart.get("colorbar"))
        self.colorbar_edge = self._colorbar_edge(self.show_colorbars)
        heatmap_style = get_heatmap_style(self.style, self.style_prefix)
        heatmap_style["cmap"] = get_colormap(heatmap_style["cmap"])
        self.heatmap_style = heatmap_style
        self.font_style = get_heatmap_font_style(self.style, self.style_prefix)
        self.edge_style = get_heatmap_edge_style(self.style, self.style_prefix)
        # white value text only helps when the cmap's high end is actually dark
        r, g, b = heatmap_style["cmap"](1.0)[:3]
        self.contrast_values = (0.2126 * r + 0.7152 * g + 0.0722 * b) < 0.5
        self.frame_color = self.style.get(
            "plot_heatmap_frame_color",
            config.get("plot_heatmap_frame_color") or "#000000",
        )
        self.frame_width = config.get("axes_spines_width") or 0.8
        self._resolve_cell_values()
        x, y, self.z = self._grid()
        self.cell_roles = heatmap_cell_roles(self.chart, self.z)
        self.highlight_color = config["font_general_color"]
        self.date_axes = {
            axis
            for axis, labels in (("x", x), ("y", y))
            if axis_kind(labels) == AXIS_TEMPORAL
        }
        self._label_axes(x, y)

    def _resolve_cell_values(self) -> None:
        """The cell value switch and text; the heatmap keeps its own names."""

        self.show_cell_values = bool(self.settings.get("show_heatmap_values"))
        formatter = _value_formatter(self.chart.get("valfmt", DEFAULT_VALUE_FORMAT))
        self.cell_text = lambda value: formatter(value, None)

    def _grid(self) -> tuple:
        """The validated (x, y, z); x and y are None when not given, z lists."""

        x, y, z = get_chart_grid(self.chart, "heatmap", dtype=object)
        z = [[(np.nan if item is None else item) for item in row] for row in z]
        return x, y, z

    def _label_axes(self, x, y):
        # x/y default the tick attrs so the panel applies them like explicit
        # ones; cells are categories, so unnamed ones tick at their index
        chart = dict(self.chart)
        rows, cols = len(self.z), len(self.z[0]) if self.z else 0
        for axis, labels, count in (("x", x, cols), ("y", y, rows)):
            if chart.get(f"{axis}ticks") is not None:
                continue
            if labels is None:
                labels = list(range(count))
            chart[f"{axis}ticks"] = list(range(len(labels)))
            chart[f"{axis}ticklabels"] = chart.get(f"{axis}ticklabels") or (
                date_labels(labels, self.settings.get(f"{axis}ticks_format"))
                if axis_kind(labels) == AXIS_TEMPORAL
                else [str(label) for label in labels]
            )
        self.chart = chart

    def date_label_axes(self):
        return self.date_axes

    def draw(self, ax, ctx):
        data = self.z

        # the panel owns the aspect; imshow's own "equal" would size the
        # colorbar to a box the panel then stretches
        im = ax.imshow(
            data,
            aspect="auto",
            norm=self.chart.get("norm", None),
            vmin=self.chart.get("vmin", None),
            vmax=self.chart.get("vmax", None),
            **self._cell_style(),
        )
        label = self.label(ctx)
        self.register_hover(im, lambda index: self._cell_datum(label, *index))
        if self.value_etch_steps:
            self._draw_cell_steps(ax, im)
        self._draw_cell_emphasis(ax)

        if self.show_cell_values:
            self._draw_cell_values(ax, im)

        if self.edge_style.get("linewidth"):
            self._draw_cell_borders(ax, len(data), len(data[0]))

        if self.show_colorbars and self.value_etch_steps:
            self._draw_even_step_legend(ax, im.norm, self.colorbar["label"])
        elif self.show_colorbars:
            _draw_colorbar(ax, im, self.colorbar, ctx.aspect_locked)

        self._draw_frame(ax)

    def _draw_cell_steps(self, ax, im) -> None:
        """The cells as etched value steps over the image, left clear for hover."""

        im.autoscale_None()
        values = np.asarray(self.z, dtype=float)
        steps = value_steps(
            im.norm(np.ma.masked_invalid(values)), len(self.value_etch_steps)
        )
        rows, cols = np.indices(values.shape)
        squares = np.array([[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5]])

        def cells(mask):
            centres = np.column_stack([cols[mask], rows[mask]])
            return PolyCollection([squares + centre for centre in centres])

        # a muted cell keeps its fade (ADR 0045)
        alpha = self._cell_style().get("alpha")
        alphas = np.broadcast_to(1.0 if alpha is None else alpha, values.shape)
        self._draw_value_steps(ax, steps, cells, im.get_zorder(), alphas)
        im.set_alpha(0)

    def _cell_datum(self, label, row, col) -> dict:
        """The hover datum of a cell: the indices the tick labels name."""

        return {
            "label": label,
            "x": col,
            "y": row,
            "value": _scalar(self.z[row][col]),
        }

    def _draw_cell_values(self, ax, im) -> None:
        """Print each cell's value at its centre; a blank cell stays bare."""

        for i, row in enumerate(self.z):
            for j, value in enumerate(row):
                if np.isnan(value):
                    continue
                font_style = dict(self.font_style)
                # a faded cell is light whatever its value
                if (
                    self.contrast_values
                    and float(im.norm(value)) > HEATMAP_TEXT_CONTRAST_THRESHOLD
                    and self.cell_roles[i][j] != EMPHASIS_BACKGROUND
                ):
                    font_style["color"] = "#FFFFFF"
                if self.value_etch_steps:
                    # a value over the etching reads through a halo of the ground
                    font_style["color"] = self.font_style.get("color")
                    font_style["path_effects"] = self.value_halo
                text = ax.text(
                    j, i, self.cell_text(value), ha="center", va="center", **font_style
                )
                self.register_limit_mark(text, j, i)

    def _cell_style(self) -> dict:
        """The image style; background cells fade to the muted alpha (ADR 0045).

        A fade rather than the muted color keeps a muted cell on the colormap
        and leaves the areas around the picked cells clean.
        """

        style = self.heatmap_style
        roles = self.cell_roles
        if not any(role == EMPHASIS_BACKGROUND for row in roles for role in row):
            return style
        alpha = 1.0 if style.get("alpha") is None else style["alpha"]
        faded = alpha * self.muted_alpha
        return {
            **style,
            "alpha": np.array(
                [
                    [faded if role == EMPHASIS_BACKGROUND else alpha for role in row]
                    for row in roles
                ]
            ),
        }

    def _draw_cell_emphasis(self, ax) -> None:
        """Outline the highlighted cells in the bolder highlight stroke."""

        width = HIGHLIGHT_WIDTH_SCALE * max(
            self.edge_style.get("linewidth") or 0, self.frame_width
        )
        for i, row in enumerate(self.cell_roles):
            for j, role in enumerate(row):
                if role != EMPHASIS_HIGHLIGHT:
                    continue
                ax.add_patch(
                    Rectangle(
                        (j - 0.5, i - 0.5),
                        1,
                        1,
                        facecolor="none",
                        edgecolor=self.highlight_color,
                        linewidth=width,
                        # over the cell borders, under the cell values
                        zorder=2,
                    )
                )

    def _draw_frame(self, ax) -> None:
        # heatmaps always draw a full frame, regardless of theme spine visibility
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(self.frame_color)
            spine.set_linewidth(self.frame_width)

    def _draw_cell_borders(self, ax, n_rows, n_cols):
        # imshow centers cell (i, j) on (j, i), so the boundaries sit at half-integers
        left, right = -0.5, n_cols - 0.5
        top, bottom = -0.5, n_rows - 0.5
        segments = [[(left, i + 0.5), (right, i + 0.5)] for i in range(n_rows - 1)]
        segments += [[(j + 0.5, top), (j + 0.5, bottom)] for j in range(n_cols - 1)]
        # autolim=False keeps the borders from widening the image's tight limits
        ax.add_collection(
            LineCollection(segments, zorder=1, **self.edge_style), autolim=False
        )


# calendar heatmap furniture (ADR 0044): month and weekday labels, in week order
MONTH_LABELS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# every other weekday is labelled: seven labels overlap at the default cell size
WEEKDAY_LABEL_STEP = 2
CALENDAR_MONTH_LINE_ZORDER = 2


def week_row(day: date, week_start: str) -> int:
    """The row of a day in a week column: 0 is the week start, 6 the day before it."""

    offset = 6 if week_start == CALENDAR_WEEKDAY.SUNDAY else 0
    return (day.weekday() - offset) % 7


def calendar_layout(
    year: int, week_start: str, first_month: int, last_month: int
) -> tuple:
    """The cell of every day of the months drawn: `(cells, n_weeks)`, cells as `(row, col)`.

    Columns are weeks, rows weekdays from the week start down; the days of
    the first and last week that fall outside the drawn months hold no cell.
    """

    first = date(year, first_month, 1)
    end = date(year + 1, 1, 1) if last_month == 12 else date(year, last_month + 1, 1)
    n_days = (end - first).days
    first_row = week_row(first, week_start)
    cells = {
        first + timedelta(days=i): divmod(first_row + i, 7)[::-1] for i in range(n_days)
    }
    return cells, (first_row + n_days + 6) // 7


def _resolve_flag(settings: dict, key: str, default: bool = True) -> bool:
    """A boolean setting; None takes the default."""

    value = settings.get(key)
    return default if value is None else bool(value)


class CalendarHeatmapLayer(HeatmapLayer):
    """One year of dated values as a weeks-by-weekdays grid of cells (ADR 0044).

    The cells, value labels, and colorbar are the heatmap's; the layer adds
    the year layout, month separators, and the month and weekday labels.
    The drawn range spans the months holding data, whole months at a time.
    """

    kind = "calendarheatmap"
    style_prefix = "plot_calendar_heatmap"

    def _resolve_style(self):
        week_start = self.settings.get("week_start")
        if week_start is None:
            week_start = get_attr_value(
                "plot_calendar_heatmap_week_start", self.style, config
            )
        self.week_start = validate_week_start(week_start) or CALENDAR_WEEKDAY.MONDAY
        self.month_line_style = get_calendar_month_line_style(self.style)
        self.show_month_labels = _resolve_flag(self.settings, "show_month_labels")
        self.show_weekday_labels = _resolve_flag(self.settings, "show_weekday_labels")
        super()._resolve_style()

    def _resolve_cell_values(self) -> None:
        """The shared `show_values` and `value_format` vocabulary (ADR 0033)."""

        self.show_cell_values = _resolve_show_values(self.settings)
        value_format = self.settings.get("value_format")
        self.value_format = (
            DEFAULT_VALUE_FORMAT if value_format is None else value_format
        )
        self.cell_text = lambda value: _format_value(self.value_format, value)

    def _grid(self) -> tuple:
        """The 7 x n_weeks grid of the months holding data; NaN off them and on missing days."""

        self.year = self.chart["year"]
        months = {day.month for day in self.chart["data"]["date"]}
        self.months = range(min(months), max(months) + 1)
        self.cells, n_weeks = calendar_layout(
            self.year, self.week_start, self.months[0], self.months[-1]
        )
        # python scalars, as the heatmap holds them: a whole number prints whole
        z = [[np.nan] * n_weeks for _ in range(7)]
        self.dates = {}
        data = self.chart["data"]
        for day, value in zip(data["date"], data["value"]):
            row, col = self.cells[day]
            self.dates[(row, col)] = day
            z[row][col] = np.nan if value is None else value
        return None, None, z

    def _label_axes(self, x, y):
        chart = dict(self.chart)
        chart["xticks"], chart["xticklabels"] = [], []
        chart["yticks"], chart["yticklabels"] = [], []
        if self.show_month_labels:
            # a month's label sits over the middle of its weeks
            spans = defaultdict(list)
            for day, (_, col) in self.cells.items():
                spans[day.month].append(col)
            chart["xticks"] = [
                (min(cols) + max(cols)) / 2 for _, cols in sorted(spans.items())
            ]
            chart["xticklabels"] = [MONTH_LABELS[month - 1] for month in self.months]
        if self.show_weekday_labels:
            start = 6 if self.week_start == CALENDAR_WEEKDAY.SUNDAY else 0
            chart["yticks"] = list(range(0, 7, WEEKDAY_LABEL_STEP))
            chart["yticklabels"] = [
                WEEKDAY_LABELS[(start + row) % 7] for row in chart["yticks"]
            ]
        self.chart = chart

    def _cell_datum(self, label, row, col) -> dict:
        day = self.dates.get((row, col))
        value = self.z[row][col]
        return {
            "label": label,
            "date": day.isoformat() if day is not None else None,
            "value": None if np.isnan(value) else _scalar(value),
        }

    def draw(self, ax, ctx):
        super().draw(ax, ctx)
        if self.month_line_style.get("linewidth"):
            self._draw_month_separators(ax)
        # the labels alone name the rows and columns
        ax.tick_params(which="both", length=0)

    def _draw_frame(self, ax) -> None:
        # the month separators and cell borders are the calendar's only lines
        for spine in ax.spines.values():
            spine.set_visible(False)

    def _draw_cell_borders(self, ax, n_rows, n_cols):
        # borders sit between two days of the year, never around the blank
        # cells the first and last week hold off the year
        segments = []
        for day, (row, col) in self.cells.items():
            if row < 6 and day + timedelta(days=1) in self.cells:
                segments.append([(col - 0.5, row + 0.5), (col + 0.5, row + 0.5)])
            if day + timedelta(days=7) in self.cells:
                segments.append([(col + 0.5, row - 0.5), (col + 0.5, row + 0.5)])
        ax.add_collection(
            LineCollection(segments, zorder=1, **self.edge_style), autolim=False
        )

    def _draw_month_separators(self, ax) -> None:
        """A stepped line along the left edge of every month but the first."""

        paths = []
        for month in self.months[1:]:
            row, col = self.cells[date(self.year, month, 1)]
            left, right = col - 0.5, col + 0.5
            if row == 0:
                paths.append([(left, -0.5), (left, 6.5)])
            else:
                paths.append(
                    [(right, -0.5), (right, row - 0.5), (left, row - 0.5), (left, 6.5)]
                )
        lines = LineCollection(
            paths, zorder=CALENDAR_MONTH_LINE_ZORDER, **self.month_line_style
        )
        lines.set_gid("month-separators")
        ax.add_collection(lines, autolim=False)


# rule-of-thumb level counts stay readable in this range (ADR 0022)
CONTOUR_LEVELS_MIN = 4
CONTOUR_LEVELS_MAX = 20
# the fd rule on a flat surface (IQR 0) has no bin width; match auto's density
CONTOUR_LEVELS_FLAT = 8


def contour_levels(
    z: List[List[Union[int, float]]], rule: Union[str, int, List[float], None]
) -> Union[List[float], int, None]:
    """Picks the contour levels of a 2-D grid by a rule of thumb.

    The rules of `CONTOUR_LEVELS` are evaluated on the per-axis resolution
    of the grid, `n = sqrt(cells)`: `"rice"` targets `2 * n ** (1/3)` levels
    and `"fd"` the value range over `2 * IQR * n ** (-1/3)`. The count is
    clamped to the 4–20 range and snapped to round values across the range of
    `z`. `"auto"` (or `None`) returns `None`, leaving the choice to
    matplotlib; an integer passes through and a list of level values comes
    back sorted and deduplicated.

    Args:
        z: The 2-D grid of values.
        rule: A rule of `CONTOUR_LEVELS`, a target level count, or an explicit
            list of level values.

    Returns:
        The level values, the target count, or `None` for the automatic rule.

    Raises:
        ValueError: If the rule is not one of `CONTOUR_LEVELS`, or the list
            is empty or holds a non-finite or non-numeric value.
    """
    if rule is None:
        return None
    if isinstance(rule, (int, np.integer)) and not isinstance(rule, bool):
        return rule
    if not isinstance(rule, str):
        return validate_contour_levels(rule)
    if rule == CONTOUR_LEVELS.AUTO:
        return None
    if rule not in (CONTOUR_LEVELS.RICE, CONTOUR_LEVELS.FD):
        raise ValueError(
            f"Invalid contour `levels` rule {rule!r}. Must be one of "
            f"{[CONTOUR_LEVELS.AUTO, CONTOUR_LEVELS.RICE, CONTOUR_LEVELS.FD]}, "
            "an integer, or a list of level values."
        )

    values = np.asarray(z, dtype=float).ravel()
    values = values[np.isfinite(values)]
    n = math.sqrt(values.size)
    if rule == CONTOUR_LEVELS.RICE:
        k = math.ceil(2 * n ** (1 / 3))
    else:
        h = 2 * iqr(values) * n ** (-1 / 3)
        k = math.ceil(np.ptp(values) / h) if h > 0 else CONTOUR_LEVELS_FLAT
    k = int(np.clip(k, CONTOUR_LEVELS_MIN, CONTOUR_LEVELS_MAX))
    ticks = MaxNLocator(nbins=k).tick_values(values.min(), values.max())
    return [float(t) for t in ticks]


# one layer for lines and fills, also the 2-D density chart (ADR 0022)
class ContourLayer(Layer):
    """A gridded surface drawn as iso-lines or filled bands."""

    ticks_at_axis_ends = False

    kind = "contour"

    def _resolve_style(self):
        self.filled = bool(self.settings.get("filled"))
        self.surface = self.filled
        self.show_labels = self.settings.get("show_labels")
        self.show_colorbars = self.settings.get("show_colorbars")
        self.colorbar = get_colorbar_setting(self.chart.get("colorbar"))
        self.colorbar_edge = self._colorbar_edge(self.filled and self.show_colorbars)
        style = get_contour_style(self.style)
        self.cmap = get_colormap(style.pop("cmap"))
        # lines take a pinned contour cmap only, past its washed-out low end
        self.line_cmap = None
        cmap_pinned = get_attr_value("plot_contour_cmap", self.style, config)
        if not self.filled and cmap_pinned is not None:
            self.line_cmap = LinearSegmentedColormap.from_list(
                f"{self.cmap.name}_lines",
                self.cmap(np.linspace(CONTOUR_LINE_CMAP_START, 1, 256)),
            )
        self.contour_style = style
        self.label_style = get_contour_label_style(self.style)
        # clabel takes no font family; the level labels are restyled after
        self.label_family = resolve_font_family()
        self.x, self.y, self.z = self._grid()
        self.levels = contour_levels(self.z, self.settings.get("levels"))
        if self.filled:
            validate_filled_levels(self.levels)
        self.extend, self.band_edges = self._coverage()

    def _coverage(self) -> tuple:
        """How filled bands reach past explicit levels, and every band's edges.

        A surface beyond the list's ends fills in the end colors; each such
        overflow band spans from the end level to the surface extreme.
        """

        if not isinstance(self.levels, list):
            return "neither", None
        edges = list(self.levels)
        low, high = np.nanmin(self.z), np.nanmax(self.z)
        below, above = low < edges[0], high > edges[-1]
        if below:
            edges.insert(0, float(low))
        if above:
            edges.append(float(high))
        if below and above:
            return "both", edges
        return ("min" if below else "max" if above else "neither"), edges

    def _grid(self) -> tuple:
        """The validated (x, y, z) arrays; x and y default to the indices."""

        x, y, z = get_chart_grid(self.chart, "contour")
        n_rows, n_cols = z.shape
        self._x_kind = axis_kind(x)
        if x is None:
            x = np.arange(n_cols)
        elif self._x_kind == AXIS_TEMPORAL:
            self.x_tz = _column_tz(x)
            x = to_date_numbers(x)
        else:
            x = x.astype(float)
        y = np.arange(n_rows) if y is None else y.astype(float)
        return x, y, z

    def x_kind(self):
        return self._x_kind

    def value_data(self):
        return self.y

    def category_data(self):
        return None if self._x_kind == AXIS_TEMPORAL else self.x

    def y_range(self):
        return (float(self.y.min()), float(self.y.max()))

    def draw(self, ax, ctx):
        style = dict(self.contour_style)
        if ctx.z_order is not None:
            style["zorder"] = ctx.z_order
        scaling = {
            "norm": self.chart.get("norm", None),
            "vmin": self.chart.get("vmin", None),
            "vmax": self.chart.get("vmax", None),
        }
        label = self.label(ctx)

        if self.filled:
            for key in ("color", "linewidths", "linestyles"):
                style.pop(key, None)
            if ctx.emphasis == EMPHASIS_BACKGROUND:
                style["alpha"] = self.muted_alpha
            bands = ax.contourf(
                self.x,
                self.y,
                self.z,
                levels=self.levels,
                extend=self.extend,
                cmap=self.cmap,
                **scaling,
                **style,
            )
            # a legend proxy: the contour set itself carries no legend handle
            proxy = ax.fill_between(
                [], [], [], color=self.cmap(CONTOUR_SWATCH), label=label
            )
            edges = self.band_edges or list(bands.levels)
            self.register_hover(bands, self._level_resolver(bands, label, edges))
            if self.value_etch_steps:
                self._draw_relief(ax, ctx, bands, proxy, edges)
            elif self.show_colorbars:
                _draw_colorbar(ax, bands, self.colorbar, ctx.aspect_locked)
            return
        self._draw_lines(ax, ctx, self.show_labels, legend_proxy=True)

    def _draw_relief(self, ax, ctx, bands, proxy, edges) -> None:
        """Filled bands as a relief map: etched steps, then labelled level lines.

        A band takes the step of its middle value under the bands' norm; the
        legend merges consecutive bands that share a step, and the legend
        proxy wears the middle step. `edges` bound every drawn band.
        """

        levels = np.asarray(edges, dtype=float)
        middles = (levels[:-1] + levels[1:]) / 2
        n = len(self.value_etch_steps)
        bands.autoscale_None()
        steps = value_steps(bands.norm(middles), n)
        wash, hatch = self.value_etch_steps[n // 2]
        proxy.set(facecolor=wash, hatch=hatch or None)
        proxy.set_path_effects([self._etch_effect(1.0)])
        paths = bands.get_paths()

        def band_paths(mask):
            return PathCollection(
                [paths[i] for i in np.flatnonzero(mask)],
                transform=bands.get_transform(),
            )

        self._draw_value_steps(ax, steps, band_paths, bands.get_zorder())
        bands.set_alpha(0)
        self._draw_lines(ax, ctx, True, legend_proxy=False)
        if not self.show_colorbars:
            return
        entries = []
        for k, low, high in zip(steps, levels[:-1], levels[1:]):
            if entries and entries[-1][0] == k:
                entries[-1][2] = high
            else:
                entries.append([k, low, high])
        self._draw_step_legend(
            ax,
            [(k, _step_label(low, high)) for k, low, high in entries],
            self.colorbar["label"],
        )

    def _draw_lines(self, ax, ctx, show_labels, legend_proxy: bool) -> None:
        """The level lines, optionally labelled, with a legend proxy."""

        style = dict(self.contour_style)
        if ctx.z_order is not None:
            style["zorder"] = ctx.z_order
        scaling = {
            "norm": self.chart.get("norm", None),
            "vmin": self.chart.get("vmin", None),
            "vmax": self.chart.get("vmax", None),
        }
        label = self.label(ctx)
        # a pinned line color beats the cmap; a muted background beats both
        by_level = (
            self.line_cmap is not None
            and "color" not in style
            and ctx.emphasis != EMPHASIS_BACKGROUND
        )
        style = self._merge_color("color", ctx.color, style)
        self._apply_emphasis(style, ctx.emphasis, width_key="linewidths")
        color = style.pop("color", None)
        if by_level:
            palette = {"cmap": self.line_cmap, **scaling}
            color = self.line_cmap(CONTOUR_SWATCH)
        else:
            palette = {"colors": [color]}
        lines = ax.contour(
            self.x, self.y, self.z, levels=self.levels, **palette, **style
        )
        if self.ink_stroke is not None:
            lines.set_path_effects([InkStroke(**self.ink_stroke)])
        self.register_hover(lines, self._level_resolver(lines, label))
        if legend_proxy:
            ax.plot(
                [],
                [],
                color=color,
                linewidth=style["linewidths"],
                linestyle=style["linestyles"],
                label=label,
            )
        if show_labels:
            label_style = dict(self.label_style)
            fmt = _value_formatter(self.chart.get("valfmt"))
            if fmt is not None:
                label_style["fmt"] = fmt
            if ctx.emphasis == EMPHASIS_BACKGROUND:
                label_style["colors"] = self.muted_color
            # a relief's labels sit over the etching and read through a halo
            halo = self.value_halo if self.filled and self.value_etch_steps else []
            for text in ax.clabel(lines, **label_style):
                text.set_fontfamily(self.label_family)
                text.set_path_effects(halo)

    @staticmethod
    def _level_resolver(contours, label, edges=None) -> Callable:
        """A level line reports its level; a filled band the two edges it lies between."""

        levels = [_scalar(level) for level in (edges or contours.levels)]

        def resolve(index):
            i = index[0]
            if contours.filled:
                return {"label": label, "level": _span_text(levels[i], levels[i + 1])}
            return {"label": label, "level": levels[i]}

        return resolve


# the `reduce` attr of a hexbin chart, as the numpy reducer of a hexagon's `c`
HEXBIN_REDUCERS = {
    HEXBIN_REDUCE.MEAN: np.mean,
    HEXBIN_REDUCE.SUM: np.sum,
    HEXBIN_REDUCE.MEDIAN: np.median,
    HEXBIN_REDUCE.MIN: np.min,
    HEXBIN_REDUCE.MAX: np.max,
}


class HexbinLayer(Layer):
    """Scattered points binned into hexagons, colored by count or by `c` (ADR 0024)."""

    ticks_at_axis_ends = False

    kind = "hexbin"
    surface = True

    def _resolve_style(self):
        self.show_colorbars = self.settings.get("show_colorbars")
        # valfmt is the tick format the colorbar setting falls back on
        self.colorbar = get_colorbar_setting(
            self.chart.get("colorbar"), self.chart.get("valfmt")
        )
        self.colorbar_edge = self._colorbar_edge(self.show_colorbars)
        style = get_hexbin_style(self.style)
        style["cmap"] = get_colormap(style["cmap"])
        self.hexbin_style = style
        self.x, self.y, self.c = self._columns()
        self.gridsize = self.chart.get("gridsize")
        if self.gridsize is None:
            self.gridsize = get_attr_value("plot_hexbin_gridsize", self.style, config)
        self.mincnt = self.chart.get("mincnt")
        # bins exist only once drawn, so the rule resolves in draw (ADR 0045)
        self.emphasis_rule = validate_emphasis_rule(self.settings.get("emphasis_rule"))
        self.highlight_color = config["font_general_color"]
        self.frame_width = config.get("axes_spines_width") or 0.8
        # counts need no reducer; `c` defaults to the mean
        self.reduce = None
        self.value_name = "count"
        if self.c is not None:
            name = self.chart.get("reduce")
            if name is None:
                name = HEXBIN_REDUCE.DEFAULT
            if name not in HEXBIN_REDUCERS:
                raise ValueError(
                    f"Invalid hexbin `reduce` value {name!r}. "
                    f"Must be one of {sorted(HEXBIN_REDUCERS)}."
                )
            self.reduce = HEXBIN_REDUCERS[name]
            self.value_name = str(name)

    def _columns(self) -> tuple:
        """The validated (x, y, c) columns; c is None when absent."""

        x = get_chart_data("x", self.chart)
        y = get_chart_data("y", self.chart)
        if x is None or y is None:
            raise ValueError(
                "A hexbin chart requires the `x` and `y` columns in `data`."
            )
        self._x_kind = axis_kind(x)
        if self._x_kind == AXIS_TEMPORAL:
            self.x_tz = _column_tz(x)
            x = to_date_numbers(x)
        else:
            x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        c = get_chart_data("c", self.chart)
        c = None if c is None else np.asarray(c, dtype=float)
        for name, column in (("y", y), ("c", c)):
            if column is not None and column.shape != x.shape:
                raise ValueError(
                    f"The hexbin `{name}` column must hold one value per `x` "
                    f"({len(x)}), got {len(column)}."
                )
        return x, y, c

    def x_kind(self):
        return self._x_kind

    def value_data(self):
        return self.y

    def category_data(self):
        return None if self._x_kind == AXIS_TEMPORAL else self.x

    def y_range(self):
        if len(self.y) == 0:
            return None
        return (float(self.y.min()), float(self.y.max()))

    def draw(self, ax, ctx):
        style = dict(self.hexbin_style)
        if ctx.z_order is not None:
            style["zorder"] = ctx.z_order
        tiles = ax.hexbin(
            self.x,
            self.y,
            C=self.c,
            gridsize=self.gridsize,
            # hexagons bin in the axes' scale; a later log scale would warp them
            xscale="log" if ctx.category_scale == SCALE.LOG else "linear",
            yscale="log" if ctx.value_scale == SCALE.LOG else "linear",
            reduce_C_function=self.reduce,
            mincnt=self.mincnt,
            norm=self.chart.get("norm", None),
            vmin=self.chart.get("vmin", None),
            vmax=self.chart.get("vmax", None),
            **style,
        )
        label = self.label(ctx)
        values = tiles.get_array()
        if self.emphasis_rule is not None:
            self._apply_bin_emphasis(ax, tiles, values)
        if self.value_etch_steps:
            self._draw_bin_steps(ax, tiles, values, self.emphasis_rule is not None)

        def resolve(index):
            cx, cy = tiles.get_offsets()[index[0]]
            value = _scalar(values[index[0]])
            return {
                "label": label,
                "x": _scalar(cx),
                "y": _scalar(cy),
                self.value_name: value,
            }

        self.register_hover(tiles, resolve)
        if self.show_colorbars and self.value_etch_steps:
            self._draw_even_step_legend(ax, tiles.norm, self.colorbar["label"])
        elif self.show_colorbars:
            _draw_colorbar(ax, tiles, self.colorbar, ctx.aspect_locked)

    def _draw_bin_steps(self, ax, tiles, values, faded: bool) -> None:
        """The bins as etched value steps under their outlines.

        `faded` bins carry the emphasis fade in their face alphas. A count bin
        holding no point draws nothing, outline included.
        """

        alphas = tiles.get_facecolors()[:, 3] if faded else None
        # the emphasis fade already scaled the norm and dropped the array
        if not faded:
            tiles.autoscale_None()
        steps = value_steps(tiles.norm(values), len(self.value_etch_steps))
        if self.c is None:
            steps = np.where(np.ma.filled(values, 0) == 0, -1, steps)
        empty = steps < 0
        hexagon = tiles.get_paths()[0].vertices
        offsets = tiles.get_offsets()

        def bins(mask):
            collection = PolyCollection(
                [hexagon],
                offsets=offsets[mask],
                offset_transform=tiles.get_offset_transform(),
            )
            collection.set_transform(tiles.get_transform())
            return collection

        self._draw_value_steps(ax, steps, bins, tiles.get_zorder() - 0.01, alphas)
        tiles.set_array(None)
        tiles.set_facecolor("none")
        edges = np.array(to_rgba_array(tiles.get_edgecolor()), dtype=float)
        edges = np.broadcast_to(edges, (len(steps), 4)).copy()
        edges[empty, 3] = 0.0
        # a collection alpha would overwrite the per-bin edge alphas
        tiles.set_alpha(None)
        tiles.set_edgecolor(edges)

    def _apply_bin_emphasis(self, ax, tiles, values) -> None:
        """Fade the bins the rule rejects and outline the ones it picks.

        The bin colors are fixed from the colormap first so the fade holds, as
        a heatmap's muted cells fade; the outlines draw as their own
        collection so no neighbour covers them.
        """

        values = np.asarray(values, dtype=float)
        # an empty count bin holds no points to rank, so it never matches
        ranked = np.where(values == 0, np.nan, values) if self.c is None else values
        roles = emphasis_rule_roles(self.emphasis_rule, ranked)
        background = np.array([role == EMPHASIS_BACKGROUND for role in roles])
        tiles.autoscale_None()
        faces = tiles.to_rgba(values)
        alpha = tiles.get_alpha()
        faces[:, 3] = 1.0 if alpha is None else alpha
        faces[background, 3] *= self.muted_alpha
        tiles.set_array(None)
        tiles.set_alpha(None)
        tiles.set_facecolor(faces)

        picked = ~background
        if not picked.any():
            return
        width = HIGHLIGHT_WIDTH_SCALE * max(
            float(np.max(tiles.get_linewidth())), self.frame_width
        )
        outline = PolyCollection(
            [tiles.get_paths()[0].vertices],
            offsets=tiles.get_offsets()[picked],
            offset_transform=tiles.get_offset_transform(),
            facecolors="none",
            edgecolors=self.highlight_color,
            linewidths=width,
            zorder=tiles.get_zorder() + EMPHASIS_Z_OFFSET[EMPHASIS_HIGHLIGHT],
        )
        outline.set_transform(tiles.get_transform())
        ax.add_collection(outline, autolim=False)


class ParallelCoordsLayer(Layer):
    """One parallel-coords set; holds every chart's data as a single drawable."""

    kind = "parallelcoords"

    def __init__(self, charts: List[dict], settings: dict):
        self.charts = charts
        super().__init__(charts[0], settings)
        # texts pool across the source charts, like the data rows
        self.texts = [t for chart in charts for t in _resolve_texts(chart)]

    def _resolve_emphasis(self, value):
        # emphasis aligns with the data rows of each source chart
        self.row_emphasis = []
        for chart in self.charts:
            roles = chart.get("emphasis")
            n_rows = len(chart.get("data", []) or [])
            if roles is None:
                self.row_emphasis.extend([None] * n_rows)
            elif isinstance(roles, str):
                validate_emphasis(roles)
                self.row_emphasis.extend([roles] * n_rows)
            else:
                for item in roles:
                    validate_emphasis(item)
                if len(roles) != n_rows:
                    raise ValueError(
                        f"`emphasis` length ({len(roles)}) must match the "
                        f"number of data rows ({n_rows})."
                    )
                self.row_emphasis.extend(list(roles))
        return None

    def _resolve_style(self):
        shared_style = self.style
        self.axis_style = get_parallel_axis_style(shared_style)
        self.tick_style = get_parallel_tick_style(shared_style)
        self.tick_length = get_parallel_tick_length(shared_style)
        self.tick_label_style = get_parallel_tick_label_style(shared_style)
        self.tick_label_bbox = get_parallel_tick_label_bbox(shared_style)
        # a label without a box reads over the lines through the value halo
        self.tick_label_halo = (
            []
            if self.tick_label_bbox is not None
            else _halo_effects(
                get_value_label_style(shared_style)["halo_width"], self.ground
            )
        )
        self.dim_label_style = get_parallel_dim_label_style(shared_style)
        self.dim_label_rotation = get_parallel_dim_label_rotation(shared_style)
        self.dim_label_pad = get_parallel_dim_label_pad(shared_style)
        self.hue_palette = config.get("color_parallel_hue", "Set1")

        # per-line styles are shared per source chart
        self.line_styles = [
            get_parallel_coords_style(c.get("style", {}) or {}) for c in self.charts
        ]

        all_hues = []
        for chart in self.charts:
            hue_attr = chart.get("hue", "hue")
            for d in chart.get("data", []):
                all_hues.append(d.get(hue_attr, None))

        # background rows are muted: they claim no hue color and no legend entry
        non_bg_hues = [
            h
            for h, role in zip(all_hues, self.row_emphasis)
            if role != EMPHASIS_BACKGROUND
        ]
        non_null_hues = [h for h in non_bg_hues if h is not None]
        self.continuous_hue = bool(non_null_hues) and all(
            isinstance(h, (int, float)) and not isinstance(h, bool)
            for h in non_null_hues
        )
        if self.continuous_hue:
            ramp = (
                config.get("color_parallel_hue_continuous")
                or config.get("color_general_singular")
                or "Blues"
            )
            self.hue_cmap = (
                create_colormap(list(ramp))
                if isinstance(ramp, list)
                else get_colormap(ramp)
            )
            self.hue_min = float(min(non_null_hues))
            self.hue_max = float(max(non_null_hues))
            self.hue_colors = {}
            self.default_color = self.hue_cmap(0.5)
            self.unique_hues = []
            return

        unique_hues = sorted(set(non_null_hues))

        if len(unique_hues) > 0:
            cycle = create_color_cycle(self.hue_palette, len(unique_hues))
            self.hue_colors = {
                hue: cycle[i]["color"] for i, hue in enumerate(unique_hues)
            }
            self.default_color = cycle[0]["color"]
        else:
            self.hue_colors = {}
            singular = create_color_cycle(self.hue_palette, 1)
            self.default_color = singular[0]["color"]
        self.unique_hues = unique_hues

    def _hue_color(self, hue_val):
        if self.continuous_hue and hue_val is not None:
            span = self.hue_max - self.hue_min
            t = 0.5 if span == 0 else (float(hue_val) - self.hue_min) / span
            return self.hue_cmap(t)
        return self.hue_colors.get(hue_val, self.default_color)

    def legend_handles(self):
        if not self.unique_hues:
            return None
        return [
            plt.Line2D([0], [0], color=self.hue_colors[hue], linewidth=2, label=hue)
            for hue in self.unique_hues
        ]

    def _normalize_value(self, value, dim: str, stats: dict) -> float:
        """Normalize one cell against the panel-shared per-dimension ranges."""

        if stats["is_categorical"][dim]:
            if value is None:
                return np.nan
            return stats["category_map"][dim].get(value, np.nan)
        range_val = stats["dim_max"][dim] - stats["dim_min"][dim]
        if range_val == 0:
            return 0.0
        if value is None or not isinstance(value, (int, float)):
            return np.nan
        return (value - stats["dim_min"][dim]) / range_val

    def draw(self, ax, ctx):
        all_data, all_hues, all_styles = [], [], []
        for chart, line_style in zip(self.charts, self.line_styles):
            hue_attr = chart.get("hue", "hue")
            for d in chart.get("data", []):
                all_data.append(d)
                all_hues.append(d.get(hue_attr, None))
                all_styles.append(line_style)

        if len(all_data) == 0:
            warnings.warn("No data points found for parallel coordinates plot.")
            return

        # the panel always supplies the shared stats (single drawing path)
        stats = ctx.parallel_stats

        dimensions = stats["dimensions"]
        x_positions = np.arange(len(dimensions))

        for data_point, hue_val, line_style, row_role in zip(
            all_data, all_hues, all_styles, self.row_emphasis
        ):
            # the panel-level (per-figure) role wins over per-row roles
            role = ctx.emphasis if ctx.emphasis is not None else row_role
            y_vals = [
                self._normalize_value(data_point.get(dim, None), dim, stats)
                for dim in dimensions
            ]
            line_color = self._hue_color(hue_val)
            style = dict(line_style)
            if style.get("color") is None:
                style["color"] = line_color
            self._apply_emphasis(style, role)
            (line,) = ax.plot(x_positions, y_vals, **style)
            self.register_hover(
                line,
                _row_resolver(
                    self.label(ctx) if hue_val is None else str(hue_val),
                    dimensions,
                    data_point,
                ),
            )

        if ctx.parallel_axes:
            self._draw_axis_furniture(ax, stats)

    def _draw_axis_furniture(self, ax, stats: dict) -> None:
        """Draw the axis lines, ticks, and labels — once per panel."""

        dimensions = stats["dimensions"]
        n_dims = len(dimensions)
        dim_is_categorical = stats["is_categorical"]
        dim_categories = stats["categories"]
        dim_category_map = stats["category_map"]
        dim_min, dim_max = stats["dim_min"], stats["dim_max"]
        x_positions = np.arange(n_dims)

        ax.set_xticks(x_positions)
        ax.set_xlim(-0.1, n_dims - 0.9)
        ax.set_xticklabels(
            dimensions, rotation=self.dim_label_rotation, **self.dim_label_style
        )
        ax.set_ylim(-0.02, 1.02)
        ax.set_yticks([])

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.tick_params(axis="x", length=0, pad=self.dim_label_pad)

        def format_number(value):
            """Format numbers in a human-readable way, avoiding scientific notation."""
            if value == 0:
                return "0"
            abs_val = abs(value)
            if abs_val >= 1000:
                return f"{value:,.0f}"
            elif abs_val >= 1:
                return f"{value:.1f}" if abs_val >= 10 else f"{value:.2f}"
            elif abs_val >= 0.1:
                return f"{value:.2f}"
            else:
                return f"{value:.3f}"

        for i, dim in enumerate(dimensions):
            ax.plot([i, i], [0, 1], **self.axis_style)

            is_first_axis = i == 0
            label_x_offset = -0.05 if is_first_axis else 0.05
            label_ha = "right" if is_first_axis else "left"
            if is_first_axis:
                tick_start, tick_end = i - self.tick_length, i
            else:
                tick_start, tick_end = i, i + self.tick_length

            tick_zorder = self.axis_style.get("zorder", 2) + 1

            if dim_is_categorical[dim]:
                categories = dim_categories[dim]
                texts = (
                    date_labels(categories)
                    if axis_kind(categories) == AXIS_TEMPORAL
                    else [str(cat) for cat in categories]
                )
                for cat, text in zip(categories, texts):
                    tick_pos = dim_category_map[dim][cat]
                    ax.plot(
                        [tick_start, tick_end],
                        [tick_pos, tick_pos],
                        zorder=tick_zorder,
                        **self.tick_style,
                    )
                    ax.text(
                        i + label_x_offset,
                        tick_pos,
                        text,
                        ha=label_ha,
                        va="center",
                        bbox=self.tick_label_bbox,
                        path_effects=self.tick_label_halo,
                        zorder=tick_zorder + 1,
                        **self.tick_label_style,
                    )
            else:
                dim_range = dim_max[dim] - dim_min[dim]
                for tick_pos in [0.0, 0.25, 0.5, 0.75, 1.0]:
                    ax.plot(
                        [tick_start, tick_end],
                        [tick_pos, tick_pos],
                        zorder=tick_zorder,
                        **self.tick_style,
                    )
                    actual = (
                        dim_min[dim] + tick_pos * dim_range
                        if dim_range
                        else dim_min[dim]
                    )
                    ax.text(
                        i + label_x_offset,
                        tick_pos,
                        format_number(actual),
                        ha=label_ha,
                        va="center",
                        bbox=self.tick_label_bbox,
                        path_effects=self.tick_label_halo,
                        zorder=tick_zorder + 1,
                        **self.tick_label_style,
                    )


def _row_resolver(label, dimensions: list, row: dict) -> Callable[[int], dict]:
    """A parallel-coords row reports, under the axis nearest the pointer, its value there."""

    def resolve(index: int) -> dict:
        dim = dimensions[min(max(int(index), 0), len(dimensions) - 1)]
        return {"label": label, dim: row.get(dim)}

    return resolve


def compute_parallel_stats(layers: List["ParallelCoordsLayer"]) -> Optional[dict]:
    """Shared per-dimension ranges across a panel's parallel layers.

    A cross-layer concern (like shared histogram bins): every layer normalizes
    against the combined ranges, so composed parallel charts share axis scales
    and the axis end labels show the combined range.
    """

    all_data = []
    for layer in layers:
        for chart in layer.charts:
            all_data.extend(chart.get("data", []) or [])
    if not all_data:
        return None

    def detected_dimensions(layer):
        hue_attr = layer.charts[0].get("hue", "hue")
        for chart in layer.charts:
            for d in chart.get("data", []) or []:
                return [k for k, v in d.items() if k != hue_attr and v is not None]
        return []

    # every data set on one axes shares one dimension order
    all_dimensions = [
        (
            list(chart["dimensions"])
            if chart.get("dimensions") is not None
            else detected_dimensions(layer)
        )
        for layer in layers
        for chart in layer.charts
    ]
    dimensions = all_dimensions[0]
    for other in all_dimensions[1:]:
        if other != dimensions:
            raise ValueError(
                "Parallel coordinates data sets and composed charts must share "
                f"the same dimensions; got {dimensions} and {other}."
            )

    if len(dimensions) < 2:
        raise ValueError("Parallel coordinates requires at least 2 dimensions.")

    dim_values_raw = {dim: [d.get(dim, None) for d in all_data] for dim in dimensions}
    category_orders = layers[0].charts[0].get("category_orders", None) or {}

    dim_is_categorical = {}
    dim_categories = {}
    dim_category_map = {}

    for dim in dimensions:
        values = dim_values_raw[dim]
        non_none = [v for v in values if v is not None]
        if len(non_none) > 0 and (
            isinstance(non_none[0], str) or is_temporal(non_none[0])
        ):
            dim_is_categorical[dim] = True
            unique_cats = set(v for v in values if v is not None)
            if dim in category_orders:
                ordered = [c for c in category_orders[dim] if c in unique_cats]
                categories = ordered + sorted(unique_cats - set(ordered))
            else:
                categories = sorted(unique_cats)
            dim_categories[dim] = categories
            if len(categories) == 1:
                dim_category_map[dim] = {categories[0]: 0.5}
            else:
                dim_category_map[dim] = {
                    cat: i / (len(categories) - 1) for i, cat in enumerate(categories)
                }
        else:
            dim_is_categorical[dim] = False

    dim_min, dim_max = {}, {}
    for dim in dimensions:
        if dim_is_categorical[dim]:
            dim_min[dim] = 0
            dim_max[dim] = len(dim_categories[dim]) - 1
        else:
            vals = np.array(
                [
                    v if v is not None and isinstance(v, (int, float)) else np.nan
                    for v in dim_values_raw[dim]
                ],
                dtype=float,
            )
            dim_min[dim] = np.nanmin(vals)
            dim_max[dim] = np.nanmax(vals)

    return {
        "dimensions": dimensions,
        "is_categorical": dim_is_categorical,
        "categories": dim_categories,
        "category_map": dim_category_map,
        "dim_min": dim_min,
        "dim_max": dim_max,
    }


# ================================================
# Radial Layers
# ================================================


def _radial_theta(n: int) -> np.ndarray:
    """Evenly spaced angular category positions, in radians."""

    return np.linspace(0, 2 * np.pi, n, endpoint=False)


def _radial_resolver(label, angles, radii) -> Callable[[int], dict]:
    """The hover resolver of radial marks: `angle` and `radius` under their own keys.

    Polar axes carry no axis labels to name the fields off. Indices wrap, for
    a closed line's repeated first point.
    """

    def resolve(index: int) -> dict:
        i = int(index) % len(radii)
        return {
            "label": label,
            "angle": _scalar(angles[i]),
            "radius": _scalar(radii[i]),
        }

    return resolve


class RadialLayer(Layer):
    """A layer drawn on a polar axes; angles are degrees in, radians internally."""

    projection = "polar"
    # categorical layers place their labels evenly around the circle
    is_categorical = True
    # (theta, tip radius, value, category index) per mark, recorded at draw
    # time so the panel can write tip texts with the final orientation
    _tips = ()

    def labels(self) -> Optional[np.ndarray]:
        return get_chart_data("label", self.chart)

    def value_data(self):
        return get_chart_data("y", self.chart)

    def y_range(self):
        y = get_chart_data("y", self.chart)
        if y is None or len(y) == 0:
            return None
        return (float(np.min(y)), float(np.max(y)))

    def apply_scales(self, ax, scalex, scaley):
        # a polar axes rejects set_xscale; only the radial (value) axis scales
        if scaley:
            ax.set_yscale(scaley)


class RadialLineLayer(AreaFillMixin, RadialLayer):
    kind = "radial-line"

    def _resolve_style(self):
        self.line_style = get_line_style(self.style)
        self.area_style = get_area_style(self.style)
        self.show_yerr = self.settings.get("show_yerr")
        self.show_area = self.settings.get("show_area")

    def draw(self, ax, ctx):
        y = get_chart_data("y", self.chart)
        labels = self.labels()
        if y is None or labels is None:
            return

        theta = _radial_theta(len(y))
        self._tips = [
            (float(t), float(v), float(v), i) for i, (t, v) in enumerate(zip(theta, y))
        ]
        # close the polygon: the first point repeats one full turn later, so
        # the closing segment sweeps the short arc forward
        theta = np.append(theta, theta[0] + 2 * np.pi)
        y = np.append(y, y[0])

        line_style = self._merge_color("color", ctx.color, self.line_style)
        if ctx.z_order is not None:
            line_style["zorder"] = ctx.z_order
        self._apply_cycle_linestyle(line_style, ctx)
        self._apply_emphasis(line_style, ctx.emphasis)
        self._stroke_halo(line_style)

        yerr = get_chart_data("yerr", self.chart)
        if self.show_yerr and isinstance(yerr, np.ndarray) and len(yerr) == len(y) - 1:
            yerr = np.append(yerr, yerr[0])
            band = ax.fill_between(
                theta, y - yerr, y + yerr, **self._resolved_area_style(ctx)
            )
            self._etch([band], wash=False)

        (line,) = ax.plot(theta, y, **line_style, label=self.label(ctx))
        self.register_hover(line, _radial_resolver(self.label(ctx), labels, y[:-1]))

        if self.show_area:
            # the fill reaches the center (or the innerradius hole clips it)
            area = ax.fill_between(theta, 0.0, y, **self._resolved_area_style(ctx))
            self._etch([area], wash=False)


class RadialBarLayer(RadialLayer):
    kind = "radial-bar"
    show_values = False

    def _resolve_style(self):
        self.bar_style = get_bar_style(self.style)
        self.show_yerr = self.settings.get("show_yerr")
        self.record_roles = _record_emphasis(self.chart)

    def labels(self) -> Optional[np.ndarray]:
        return get_chart_data("label", self.chart)

    def y_values(self) -> Optional[np.ndarray]:
        return get_chart_data("y", self.chart)

    @property
    def bar_width(self) -> float:
        """The layer's resolved `plot_bar_width`, as a fraction of the sector width."""
        return self.bar_style.get("width", config["plot_bar_width"])

    def draw(self, ax, ctx):
        y = self.y_values()
        labels = self.labels()
        if y is None or labels is None:
            return

        sector = 2 * np.pi / len(labels)
        theta = _radial_theta(len(labels))

        bar_style = self._merge_color("color", ctx.color, self.bar_style)
        if ctx.z_order is not None:
            bar_style["zorder"] = ctx.z_order
        if ctx.alpha is not None:
            bar_style["alpha"] = ctx.alpha
        _apply_cycle_hatch(bar_style, ctx)
        self._apply_emphasis(bar_style, ctx.emphasis, width_key="linewidth")

        yerr = get_chart_data("yerr", self.chart) if self.show_yerr else None

        # panel bar slots are fractions of the category width; here a
        # category is one sector, so the slot scales to radians at draw time
        slot = ctx.bar_slot
        theta_offset = 0.0
        if slot is not None:
            bar_style["width"] = slot.width * sector
            theta_offset = slot.offset * sector
            if slot.bottom is not None:
                bar_style["bottom"] = slot.bottom
            if not slot.show_yerr:
                yerr = None
        else:
            bar_style["width"] = self.bar_width * sector

        bottoms = bar_style.get("bottom")
        tops = np.asarray(y, dtype=float) + (0.0 if bottoms is None else bottoms)
        # a muted bar keeps its tip (the category label hugs it) but no value
        roles = self._record_roles(ctx.emphasis, len(y))
        self._tips = [
            (
                float(t + theta_offset),
                float(r),
                None if role == EMPHASIS_BACKGROUND else float(v),
                i,
            )
            for i, (t, r, v, role) in enumerate(zip(theta, tops, y, roles))
        ]

        bars = ax.bar(
            theta + theta_offset, y, yerr=yerr, label=self.label(ctx), **bar_style
        )
        self._etch(bars.patches)
        self._apply_patch_emphasis(bars.patches, roles)
        self._name_legend_patch(bars, roles)
        self.register_hover(bars, _radial_resolver(self.label(ctx), labels, y))


class RadialScatterLayer(RadialLayer):
    kind = "radial-scatter"

    def _resolve_style(self):
        self.scatter_style = get_scatter_style(self.style)
        # a highlight edge contrasts in the theme's own text color
        self.highlight_edge_color = config.get("font_general_color") or "#000000"

    def draw(self, ax, ctx):
        y = get_chart_data("y", self.chart)
        labels = self.labels()
        if y is None or labels is None:
            return

        scatter_style = dict(self.scatter_style)
        if ctx.z_order is not None:
            scatter_style["zorder"] = ctx.z_order
        self._apply_cycle_marker(scatter_style, ctx)
        self._apply_emphasis(
            scatter_style, ctx.emphasis, width_key="linewidths", color_key=None
        )
        if ctx.emphasis == EMPHASIS_HIGHLIGHT:
            scatter_style["edgecolors"] = self.highlight_edge_color
        else:
            scatter_style["linewidths"] = _marker_edge_widths(
                scatter_style.get("linewidths"), scatter_style.get("s")
            )
        if scatter_style.get("c") is None:
            scatter_style["c"] = ctx.color
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            scatter_style["c"] = self.muted_color

        theta = _radial_theta(len(y))
        self._tips = [
            (float(t), float(v), float(v), i) for i, (t, v) in enumerate(zip(theta, y))
        ]
        points = ax.scatter(
            theta, y, label=self.label(ctx), **_hollow_marker(scatter_style)
        )
        self.register_hover(points, _radial_resolver(self.label(ctx), labels, y))


class RadialHistogramLayer(RadialLayer):
    kind = "radial-histogram"
    is_categorical = False

    def _resolve_style(self):
        hist_style = get_hist_style(self.style)
        # the rose draws through ax.bar; histtype/align are ax.hist-only knobs
        hist_style.pop("histtype", None)
        hist_style.pop("align", None)
        self.hist_style = hist_style
        self.num_bins = self.settings.get("num_bins") or DEFAULT_NUM_BINS

    def x_values(self) -> Optional[np.ndarray]:
        return get_chart_data("x", self.chart)

    def value_data(self):
        return None

    def _counts(self) -> Optional[tuple]:
        x = self.x_values()
        if x is None or len(x) == 0:
            return None
        # observations are degrees; the fixed [0, 360) domain keeps bin edges
        # shared across every radial histogram in a panel
        return np.histogram(
            np.asarray(x, dtype=float) % 360.0, bins=self.num_bins, range=(0.0, 360.0)
        )

    def y_range(self):
        binned = self._counts()
        if binned is None:
            return None
        counts, _ = binned
        return (float(np.min(counts)), float(np.max(counts)))

    def draw(self, ax, ctx):
        binned = self._counts()
        if binned is None:
            return

        hist_style = self._merge_color("color", ctx.color, self.hist_style)
        if ctx.z_order is not None:
            hist_style["zorder"] = ctx.z_order
        if ctx.alpha is not None:
            hist_style["alpha"] = ctx.alpha
        _apply_cycle_hatch(hist_style, ctx)
        self._apply_emphasis(hist_style, ctx.emphasis, width_key="linewidth")

        counts, edges = binned
        theta_edges = np.deg2rad(edges)
        centers = (theta_edges[:-1] + theta_edges[1:]) / 2
        self._tips = [
            (float(c), float(n), float(n), None) for c, n in zip(centers, counts)
        ]
        bars = ax.bar(
            centers,
            counts,
            width=np.diff(theta_edges),
            label=self.label(ctx),
            **hist_style,
        )
        self._etch(bars.patches)
        spans = [
            _span_text(lo, hi, lambda value: f"{value:g}°")
            for lo, hi in zip(edges[:-1], edges[1:])
        ]
        self.register_hover(bars, _radial_resolver(self.label(ctx), spans, counts))


# the carrier keeps post-hoc texts on the layer seam (ADR 0018)
class TextLayer(Layer):
    """A carrier for post-hoc text annotations.

    Appended to a figure's panel by `Annotate`; it draws no marks and claims
    no color-cycle slot, legend entry, hatch, orientation, or projection.
    """

    kind = "text"
    projection = None

    def __init__(self, texts):
        super().__init__({"texts": texts}, {})

    def draw(self, ax, ctx):
        """No marks; the panel draws the texts with the other annotations."""


# ================================================
# Sankey Layer
# ================================================


def _ribbon_centerline(x1, y1, x2, y2, t):
    """The point at `t` on a ribbon's centreline, a cubic Bézier bending at mid-x."""

    cx = (x1 + x2) / 2
    mt = 1 - t
    x = mt**3 * x1 + 3 * mt**2 * t * cx + 3 * mt * t**2 * cx + t**3 * x2
    y = mt**3 * y1 + 3 * mt**2 * t * y1 + 3 * mt * t**2 * y2 + t**3 * y2
    return x, y


class _TextHalo(patheffects.withStroke):
    """A label halo drawn without the sketch wobble, which breaks it into gaps."""

    def draw_path(self, renderer, gc, tpath, affine, rgbFace=None):
        gc.set_sketch_params(None)
        super().draw_path(renderer, gc, tpath, affine, rgbFace)


def _halo_effects(width, ground: Optional[str] = None) -> list:
    """The path effects stroking a text halo of `width` points in the ground color.

    None when the width is 0; a None ground is white.
    """

    if not width or width <= 0:
        return []
    return [_TextHalo(linewidth=width, foreground=ground or "#FFFFFF")]


# ================================================
# Ink Effects (ADR 0048)
# ================================================

# an ink ribbon never grows past this share of the axes height
INK_STROKE_MAX_AXES_SHARE = 0.012
# display pixels between the samples of a resampled path
INK_STROKE_STEP = 1.5
# the most samples one polyline takes, so a huge path stays drawable
INK_STROKE_MAX_SAMPLES = 6000
# the narrowest a pressure stroke gets, as a share of its width
INK_STROKE_PRESSURE_FLOOR = 0.45
# the ink wobble: two sines of these periods in pixels and weights
INK_WOBBLE_WAVES = ((37.0, 0.6), (11.0, 0.4))
# pressure: sine half-waves over the stroke, and the grain's smoothing window
INK_SWELL_HALF_WAVES = 3
INK_GRAIN_WINDOW = 7
# a tapered end keeps this share of the width; a stroke too short to taper
# is drawn at the short share throughout
INK_TAPER_FLOOR = 0.4
INK_SHORT_STROKE_SHARE = 0.85


def _path_seed(*arrays) -> int:
    """A seed from a path's vertices, so a redraw of the same data looks the same."""

    digest = hashlib.md5()
    for array in arrays:
        digest.update(
            np.ascontiguousarray(np.asarray(array, dtype=np.float32)).tobytes()
        )
    return int(digest.hexdigest()[:8], 16)


@contextmanager
def _derived_gc(renderer, gc, **changes):
    """A copy of `gc` without its hatch, with `changes` set through its setters.

    A tuple value spreads over the setter's arguments, as `dashes` takes two.
    """

    derived = renderer.new_gc()
    derived.copy_properties(gc)
    derived.set_hatch(None)
    for name, value in changes.items():
        setter = getattr(derived, f"set_{name}")
        if isinstance(value, tuple):
            setter(*value)
        else:
            setter(value)
    try:
        yield derived
    finally:
        derived.restore()


def _polylines(path: Path):
    """The path split into polylines at every MOVETO and CLOSEPOLY."""

    verts, codes = path.vertices, path.codes
    if codes is None:
        yield verts
        return
    start = 0
    for i, code in enumerate(codes):
        if code == Path.MOVETO and i > start:
            yield verts[start:i]
            start = i
        elif code in (Path.CLOSEPOLY, Path.STOP):
            if i > start:
                yield verts[start:i]
            start = i + 1
    if len(verts) > start:
        yield verts[start:]


def _resample(points: np.ndarray, step: float) -> tuple:
    """The polyline resampled every `step` pixels, with the arclength at each sample.

    `(None, None)` for a polyline shorter than a pixel.
    """

    points = np.asarray(points, dtype=float)
    if len(points) < 2:
        return None, None
    lengths = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(points, axis=0).T))])
    total = lengths[-1]
    if total < 1.0:
        return None, None
    n = int(min(max(total / step, 2), INK_STROKE_MAX_SAMPLES))
    s = np.linspace(0, total, n)
    xy = np.column_stack(
        [np.interp(s, lengths, points[:, 0]), np.interp(s, lengths, points[:, 1])]
    )
    return xy, s


def _dash_runs(s: np.ndarray, offset: float, dashes: list) -> list:
    """The sample index runs that fall on the dashes of `dashes`, in pixels."""

    period = sum(dashes)
    if period <= 0:
        return [np.arange(len(s))]
    on = (
        np.searchsorted(np.cumsum(dashes), np.mod(s + offset, period), "right") % 2 == 0
    )
    edges = np.flatnonzero(np.diff(np.concatenate([[0], on.astype(int), [0]])))
    return [np.arange(a, b) for a, b in zip(edges[::2], edges[1::2]) if b - a >= 2]


class InkStroke(patheffects.AbstractPathEffect):
    """Draws a stroked path as a filled ribbon whose width follows a pen.

    The broad-nib model makes the width the nib projected across the travel
    direction — thick across the nib, a hairline along it — modulated by a
    slow ink wobble and tapered at the ends. With `nib_floor` 1 the nib has
    no direction and `swell` and `noise` model pressure instead: sine swells
    over the stroke and a smoothed grain. Dashes split the ribbon; a filled
    shape (an arrowhead) keeps its fill under the ribbon of its outline.
    """

    def __init__(
        self,
        width_scale: float = 1.6,
        nib_angle: float = 32.0,
        nib_floor: float = 0.35,
        wobble: float = 0.22,
        taper: float = 7.0,
        swell: float = 0.0,
        noise: float = 0.0,
    ):
        super().__init__()
        self.width_scale = width_scale
        angle = np.radians(nib_angle)
        self.nib = np.array([np.cos(angle), np.sin(angle)])
        self.nib_floor = nib_floor
        self.wobble = wobble
        self.taper = taper
        self.swell = swell
        self.noise = noise

    def _profile(self, t: np.ndarray, s: np.ndarray, phases) -> np.ndarray:
        """The width along the stroke as a share of the full nib width."""

        across = np.abs(t[:, 0] * self.nib[1] - t[:, 1] * self.nib[0])
        profile = self.nib_floor + (1 - self.nib_floor) * across
        (long_period, long_weight), (short_period, short_weight) = INK_WOBBLE_WAVES
        profile = profile * (
            1
            + self.wobble
            * (
                long_weight * np.sin(s / long_period + phases[0])
                + short_weight * np.sin(s / short_period + phases[1])
            )
        )
        length = s[-1] - s[0]
        if self.swell and length > 0:
            profile = profile * (
                1
                + self.swell
                * np.sin(INK_SWELL_HALF_WAVES * np.pi * (s - s[0]) / length + phases[0])
            )
        if self.noise:
            grain = np.random.default_rng(int(phases[1] * 1e6)).normal(
                0, self.noise, len(s)
            )
            profile = profile * (
                1
                + np.convolve(
                    grain, np.ones(INK_GRAIN_WINDOW) / INK_GRAIN_WINDOW, "same"
                )
            )
        if self.swell or self.noise:
            profile = np.clip(profile, INK_STROKE_PRESSURE_FLOOR, None)
        edge = np.minimum(s - s[0], s[-1] - s)
        ramp = np.clip(edge / max(self.taper, 1e-6), 0, 1)
        ramp = ramp * ramp * (3 - 2 * ramp)
        if length > 2 * self.taper:
            return profile * (INK_TAPER_FLOOR + (1 - INK_TAPER_FLOOR) * ramp)
        return profile * INK_SHORT_STROKE_SHARE

    def _ribbon(self, xy: np.ndarray, s: np.ndarray, half: float, phases) -> Path:
        d = np.gradient(xy, axis=0)
        norm = np.hypot(d[:, 0], d[:, 1])
        norm[norm == 0] = 1.0
        t = d / norm[:, None]
        n = np.column_stack([-t[:, 1], t[:, 0]])
        h = half * self._profile(t, s, phases)
        left, right = xy + n * h[:, None], xy - n * h[:, None]
        polygon = np.vstack([left, right[::-1], left[:1]])
        codes = np.full(len(polygon), Path.LINETO)
        codes[0], codes[-1] = Path.MOVETO, Path.CLOSEPOLY
        return Path(polygon, codes)

    def draw_path(self, renderer, gc, tpath, affine, rgbFace=None):
        width = gc.get_linewidth()
        if width <= 0:
            return renderer.draw_path(gc, tpath, affine, rgbFace)
        half = 0.5 * renderer.points_to_pixels(width) * self.width_scale
        clip = gc.get_clip_rectangle()
        if clip is not None and clip.height > 0:
            half = min(half, max(INK_STROKE_MAX_AXES_SHARE * clip.height, 0.5))
        phases = np.random.default_rng(_path_seed(tpath.vertices)).uniform(
            0, 2 * np.pi, 2
        )
        offset, dashes = gc.get_dashes()
        dashes = (
            None if dashes is None else [renderer.points_to_pixels(v) for v in dashes]
        )
        offset = renderer.points_to_pixels(offset or 0)
        with _derived_gc(renderer, gc, linewidth=0.0, dashes=(0, None)) as fill:
            if rgbFace is not None:
                renderer.draw_path(fill, tpath, affine, rgbFace)
            path = tpath.cleaned(transform=affine, remove_nans=True, curves=False)
            for points in _polylines(path):
                xy, s = _resample(points, INK_STROKE_STEP)
                if xy is None:
                    continue
                runs = (
                    [np.arange(len(s))]
                    if dashes is None
                    else _dash_runs(s, offset, dashes)
                )
                for run in runs:
                    ribbon = self._ribbon(xy[run], s[run], half, phases)
                    renderer.draw_path(fill, ribbon, IdentityTransform(), gc.get_rgb())


# etch line directions per matplotlib hatch character, in degrees
ETCH_ANGLES = {
    "/": (45,),
    "\\": (135,),
    "|": (90,),
    "-": (0,),
    "x": (45, 135),
    "X": (45, 135),
    "+": (0, 90),
}
# the tightest etch line spacing and stipple spacing, in pixels
ETCH_MIN_SPACING = 2.5
ETCH_MIN_STIPPLE = 3.0
# a stipple is a short tick this long in pixels, scattered this far
ETCH_STIPPLE_TICK = (1.0, 0.6)
ETCH_STIPPLE_SCATTER = 0.8
# stipples sit this much further apart than lines of the same density
ETCH_STIPPLE_SPREAD = 1.3


class Etch(patheffects.AbstractPathEffect):
    """Draws a hatched fill as hand-etched lines clipped to its outline.

    The hatch string still selects the pattern (matplotlib's characters, a
    repeated character is denser), but each line is drawn on its own with a
    small jitter in spacing and angle, so the renderer's sketch wobble reaches
    it; `.` stipples. Under the lines lies a `wash` of the face color over
    the `ground` (`None`: no fill; 1: the face itself). A path without a
    hatch draws as it is.
    """

    def __init__(
        self,
        spacing: float = 4.2,
        jitter: float = 0.3,
        angle_jitter: float = 2.5,
        line_width: float = 0.6,
        wash: Optional[float] = 0.1,
        color: str = "#000000",
        ground: str = "#FFFFFF",
    ):
        super().__init__()
        self.spacing = spacing
        self.jitter = jitter
        self.angle_jitter = angle_jitter
        self.line_width = line_width
        self.wash = wash
        self.color = to_rgb(color)
        self.ground = np.asarray(to_rgb(ground))

    def _stipples(self, bbox, count, rng, spacing_px) -> tuple:
        spacing = max(spacing_px * ETCH_STIPPLE_SPREAD / count, ETCH_MIN_STIPPLE)
        xs = np.arange(bbox.x0, bbox.x1 + spacing, spacing)
        ys = np.arange(bbox.y0, bbox.y1 + spacing, spacing)
        gx, gy = np.meshgrid(xs, ys)
        # every other row shifts half a step, as a hand stipples
        gx = gx + (np.arange(len(ys)) % 2)[:, None] * spacing / 2
        starts = np.column_stack([gx.ravel(), gy.ravel()])
        starts = starts + rng.uniform(
            -ETCH_STIPPLE_SCATTER, ETCH_STIPPLE_SCATTER, starts.shape
        )
        return starts, starts + ETCH_STIPPLE_TICK

    def _strokes(self, bbox, char, count, rng, spacing_px) -> tuple:
        centre = np.array([(bbox.x0 + bbox.x1) / 2, (bbox.y0 + bbox.y1) / 2])
        diagonal = np.hypot(bbox.width, bbox.height) + 4
        spacing = max(spacing_px / count, ETCH_MIN_SPACING)
        starts, ends = [], []
        for angle in ETCH_ANGLES.get(char, (45,)):
            offsets = np.arange(-diagonal / 2, diagonal / 2, spacing)
            offsets = (
                offsets + rng.uniform(-self.jitter, self.jitter, len(offsets)) * spacing
            )
            angles = np.radians(
                angle + rng.uniform(-self.angle_jitter, self.angle_jitter, len(offsets))
            )
            u = np.column_stack([np.cos(angles), np.sin(angles)])
            v = np.column_stack([-np.sin(angles), np.cos(angles)])
            base = centre + v * offsets[:, None]
            starts.append(base - u * diagonal / 2)
            ends.append(base + u * diagonal / 2)
        return np.vstack(starts), np.vstack(ends)

    def _lines(self, bbox, hatch: str, rng, spacing_px: float) -> Optional[Path]:
        starts, ends = [], []
        # sorted, so the random draws follow the same order on every run
        for char in sorted(set(hatch)):
            count = hatch.count(char)
            if char == ".":
                a, b = self._stipples(bbox, count, rng, spacing_px)
            else:
                a, b = self._strokes(bbox, char, count, rng, spacing_px)
            starts.append(a)
            ends.append(b)
        if not starts:
            return None
        starts, ends = np.vstack(starts), np.vstack(ends)
        vertices = np.empty((2 * len(starts), 2))
        vertices[0::2], vertices[1::2] = starts, ends
        codes = np.tile([Path.MOVETO, Path.LINETO], len(starts))
        return Path(vertices, codes)

    def _pattern(self, gc, face) -> tuple:
        """The `(hatch, wash color)` of a path; the hatch is empty when unetched."""

        hatch = gc.get_hatch()
        if not hatch or self.wash is None:
            return hatch, None
        return hatch, (1 - self.wash) * self.ground + self.wash * face

    def draw_path(self, renderer, gc, tpath, affine, rgbFace=None):
        if rgbFace is None:
            return renderer.draw_path(gc, tpath, affine, rgbFace)
        hatch, wash = self._pattern(gc, np.asarray(to_rgb(rgbFace[:3])))
        if not hatch and wash is None:
            return renderer.draw_path(gc, tpath, affine, rgbFace)
        bbox = tpath.transformed(affine).get_extents()
        # an area fill reaches a floor far off-screen: etch the visible part
        clip = gc.get_clip_rectangle()
        if clip is not None:
            bbox = Bbox.intersection(bbox, clip) or Bbox.null()
        if bbox.width <= 0 or bbox.height <= 0:
            return
        # every bar shares the unit-square path: its placement tells them apart
        rng = np.random.default_rng(_path_seed(tpath.vertices, affine.get_matrix()))

        if wash is not None:
            with _derived_gc(renderer, gc, linewidth=0.0) as fill:
                renderer.draw_path(fill, tpath, affine, (*wash, 1.0))

        lines = (
            self._lines(bbox, hatch, rng, renderer.points_to_pixels(self.spacing))
            if hatch
            else None
        )
        if lines is not None:
            with _derived_gc(
                renderer,
                gc,
                linewidth=self.line_width,
                capstyle="round",
                dashes=(0, None),
                clip_path=TransformedPath(tpath, affine),
            ) as stroke:
                stroke.set_foreground((*self.color, 1.0), isRGBA=True)
                renderer.draw_path(stroke, lines, IdentityTransform(), None)

        if gc.get_linewidth() > 0:
            with _derived_gc(renderer, gc) as outline:
                renderer.draw_path(outline, tpath, affine, None)


def value_steps(normed, n: int) -> np.ndarray:
    """The step, 0 to `n - 1`, of each value normalized to [0, 1]; -1 where missing."""

    normed = np.ma.masked_invalid(np.ma.asarray(normed, dtype=float))
    steps = np.clip(np.floor(normed.filled(0.0) * n), 0, n - 1).astype(int)
    return np.where(np.ma.getmaskarray(normed), -1, steps)


def _step_label(low, high) -> str:
    """A value step's range, each end to three significant digits."""

    return " – ".join(f"{float(f'{value:.3g}'):g}" for value in (low, high))


def _value_label_font(style: dict) -> dict:
    """The text kwargs of a value label from its resolved `plot_value_*` style."""

    return {
        "fontsize": style["fontsize"],
        "color": style["color"],
        "family": resolve_font_family(),
        "path_effects": _halo_effects(
            style.get("halo_width"), config.get("axes_facecolor")
        ),
    }


def _text_size(fontsize, text) -> tuple:
    """A text's estimated (width, height) in points."""

    lines = text.split("\n")
    return (
        TEXT_WIDTH_PER_CHAR * fontsize * max(len(line) for line in lines),
        TEXT_LINE_HEIGHT * fontsize * len(lines),
    )


def _text_box(ax, x, y, text, fontsize, ha, pad_points=0.0):
    """A text's estimated (x0, y0, x1, y1) in data units, before any layout pass."""

    fig_w, fig_h = ax.figure.get_size_inches()
    pos = ax.get_position()
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    per_point_x = (xlim[1] - xlim[0]) / (fig_w * pos.width * 72)
    per_point_y = (ylim[1] - ylim[0]) / (fig_h * pos.height * 72)
    text_w, text_h = _text_size(fontsize, text)
    width = (text_w + 2 * pad_points) * per_point_x
    height = (text_h + 2 * pad_points) * per_point_y
    x0 = x - width / 2 if ha == "center" else x - width if ha == "right" else x
    return (x0, y - height / 2, x0 + width, y + height / 2)


def _draw_point_labels(ax, entries, obstacles) -> None:
    """Draw point labels at the spot around each marker with the least overlap.

    `entries` are (owner_ax, x, y, radius_pt, pad_pt, text, font, spots) in
    draw order; `obstacles` are display-space (x0, y0, x1, y1) boxes — every
    marker of the panel and its correlation box. Each label takes the first
    clear spot among its `spots`, or the least-overlapping one when none is
    clear; placed labels join the obstacles, and the space outside the axes
    counts as occupied.
    """

    px_per_pt = ax.figure.dpi / 72.0
    frame = tuple(ax.bbox.extents)
    occupied = list(obstacles)
    for owner_ax, x, y, radius_pt, pad_pt, text, font, spots in entries:
        cx, cy = owner_ax.transData.transform((x, y))
        w, h = (v * px_per_pt for v in _text_size(font["fontsize"], text))
        gap = radius_pt + pad_pt
        best = None
        for ha, va, dx, dy in spots:
            # a diagonal spot keeps the same gap along the diagonal
            step = gap / math.sqrt(2) if dx and dy else gap
            ax0 = cx + dx * step * px_per_pt
            ay0 = cy + dy * step * px_per_pt
            x0 = ax0 - w / 2 if ha == "center" else ax0 - w if ha == "right" else ax0
            y0 = ay0 - h / 2 if va == "center" else ay0 - h if va == "top" else ay0
            box = (x0, y0, x0 + w, y0 + h)
            outside = w * h - _overlap_area(box, frame)
            overlap = outside + sum(_overlap_area(box, other) for other in occupied)
            # sub-pixel residue from the transforms is not an overlap
            overlap = 0.0 if overlap < POINT_LABEL_CLEAR else overlap
            if best is None or overlap < best[0]:
                best = (overlap, ha, va, dx * step, dy * step, box)
            if overlap == 0:
                break
        _, ha, va, dx, dy, box = best
        occupied.append(box)
        ax.annotate(
            text,
            xy=(x, y),
            xycoords=owner_ax.transData,
            xytext=(dx, dy),
            textcoords="offset points",
            ha=ha,
            va=va,
            zorder=TEXT_ANNOTATION_ZORDER,
            **font,
        )


def _overlap_area(a, b) -> float:
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(
        0.0, min(a[3], b[3]) - max(a[1], b[1])
    )


def _format_value(value_format, value) -> str:
    """Render a value with a formatter or callable, a `{x}`, `{}`, or `%` string."""

    if callable(value_format):
        return value_format(value)
    if "{x" in value_format:
        return value_format.format(x=value)
    if "{" in value_format:
        return value_format.format(value)
    return value_format % (value,)


def _default_value_step(ax, texts: list, fontsize, along_y: bool = False) -> int:
    """Every Nth mark, so the widest label fits between neighbours along the axes."""

    fig_w, fig_h = ax.figure.get_size_inches()
    pos = ax.get_position()
    if along_y:
        axis_pt = fig_h * pos.height * 72
        widest = max(_text_size(fontsize, t)[1] for t in texts)
    else:
        axis_pt = fig_w * pos.width * 72
        widest = max(_text_size(fontsize, t)[0] for t in texts)
    fits = max(int(axis_pt // (widest + 2 * POINT_LABEL_PAD)), 1)
    return max(1, math.ceil(len(texts) / fits))


def _annotate_value(ax, position, value, text, horizontal, pad, font) -> None:
    """Print `text` just past `value` at `position` on the category axis."""

    ax.annotate(
        text,
        xy=(value, position) if horizontal else (position, value),
        xytext=(pad, 0) if horizontal else (0, pad),
        textcoords="offset points",
        ha="left" if horizontal else "center",
        va="center" if horizontal else "bottom",
        zorder=TEXT_ANNOTATION_ZORDER,
        **font,
    )


class NodeBox(NamedTuple):
    """One Sankey node bar in the 0–1 data space."""

    x: float
    bottom: float
    height: float

    @property
    def top(self) -> float:
        return self.bottom + self.height


class SankeyLayer(Layer):
    """One Sankey: every link of a chart as node bars and ribbons (ADR 0026).

    The layer owns its axes: a fixed 0–1 data space with the axis off, so the
    panel applies no furniture, scales, or limits around it.
    """

    kind = "sankey"
    bare = True

    def __init__(self, chart: dict, settings: dict):
        self.links = chart["data"]["links"]
        self.columns = settings.get("nodes") or infer_sankey_columns(self.links)
        self.column_labels = settings.get("column_labels")
        if self.column_labels is not None and len(self.column_labels) != len(
            self.columns
        ):
            raise ValueError(
                f"`column_labels` has {len(self.column_labels)} entries but the "
                f"Sankey has {len(self.columns)} columns."
            )
        super().__init__(chart, settings)

    def _resolve_style(self) -> None:
        self.sankey_style = get_sankey_style(self.style)
        self.link_color = validate_sankey_link_color(
            self.sankey_style.get("link_color")
        )
        self._resolve_bare_labels()
        # column headings read as per-column subtitles
        self.column_label_style = get_text_style("subtitle")
        # one color per node in first appearance across the links, so the
        # column order never recolors a node; unlinked nodes follow
        names = first_seen_nodes(self.links)
        names += [n for column in self.columns for n in column if n not in names]
        cycle = create_color_cycle(config["color_general_multiple"], len(names))
        self.node_colors = {name: cycle[i]["color"] for i, name in enumerate(names)}

    def _geometry(self) -> tuple:
        """The (x, bottom, height) of every node, the shared height scale, and the node flows."""

        style = self.sankey_style
        node_width = style["node_width"]
        node_pad = style["node_pad"]

        outflow, inflow = defaultdict(float), defaultdict(float)
        for record in self.links:
            outflow[record["source"]] += record["value"]
            inflow[record["target"]] += record["value"]
        size = {n: max(outflow[n], inflow[n]) for col in self.columns for n in col}

        # one scale for every column: the tallest column fills 1 - node_pad
        max_total = max(sum(size[n] for n in col) for col in self.columns)
        scale = (1 - node_pad) / max_total
        n_cols = len(self.columns)
        x_step = (1 - node_width) / (n_cols - 1) if n_cols > 1 else 0.0

        geometry = {}
        for ci, column in enumerate(self.columns):
            gap = node_pad / (len(column) - 1) if len(column) > 1 else 0.0
            total = sum(size[n] for n in column) * scale + gap * (len(column) - 1)
            # shorter columns center on the tallest one
            y = 1 - (1 - total) / 2
            x = ci * x_step if n_cols > 1 else (1 - node_width) / 2
            for name in column:
                height = size[name] * scale
                geometry[name] = NodeBox(x, y - height, height)
                y -= height + gap
        return geometry, scale, size

    def draw(self, ax: plt.Axes, ctx: DrawContext) -> None:
        style = self.sankey_style
        node_width = style["node_width"]
        geometry, scale, size = self._geometry()
        # the (patch, datum) of every node bar and ribbon, for the hover targets
        node_marks, link_marks = [], []
        halo = style.get("halo_width") or 0
        # the axes limits are fixed before any text so box estimates use them
        ax.set_xlim(-SANKEY_LABEL_MARGIN, 1 + SANKEY_LABEL_MARGIN)
        ax.set_ylim(0, 1 + (SANKEY_COLUMN_LABEL_HEADROOM if self.column_labels else 0))
        # every label and value placed so far, for the ribbon values to avoid
        occupied = []
        effects = _halo_effects(halo, self.ground)

        for ci, column in enumerate(self.columns):
            for name in column:
                box = geometry[name]
                bar = Rectangle(
                    (box.x, box.bottom),
                    node_width,
                    box.height,
                    facecolor=(
                        self.node_colors[name]
                        if style.get("node_fill", True)
                        else "none"
                    ),
                    edgecolor=style.get("edgecolor"),
                    linewidth=style.get("linewidth"),
                    zorder=3,
                    label=name,
                )
                ax.add_patch(bar)
                node_marks.append((bar, {"label": name, "flow": size[name]}))
                # labels sit left of the first column, right of every other
                if ci == 0:
                    tx, ha = box.x - SANKEY_LABEL_PAD, "right"
                else:
                    tx, ha = box.x + node_width + SANKEY_LABEL_PAD, "left"
                ty = box.bottom + box.height / 2
                ax.text(
                    tx,
                    ty,
                    name,
                    ha=ha,
                    va="center",
                    zorder=4,
                    path_effects=effects,
                    **self.label_style,
                )
                occupied.append(
                    _text_box(ax, tx, ty, name, self.label_style["fontsize"], ha, halo)
                )

        if self.column_labels is not None:
            for column, label in zip(self.columns, self.column_labels):
                x = geometry[column[0]].x
                ax.text(
                    x + node_width / 2,
                    1 + SANKEY_COLUMN_LABEL_PAD,
                    label,
                    ha="center",
                    va="bottom",
                    zorder=4,
                    **self.column_label_style,
                )

        # ribbons stack from the top of each node; drawing in order of
        # endpoint height keeps the crossings few
        source_used, target_used = defaultdict(float), defaultdict(float)
        # (height, centreline endpoints, text) of every ribbon value to place
        values = []
        order = sorted(
            self.links,
            key=lambda r: (geometry[r["source"]].top, geometry[r["target"]].top),
            reverse=True,
        )
        for record in order:
            source, target = record["source"], record["target"]
            height = record["value"] * scale
            y_source = geometry[source].top - source_used[source]
            y_target = geometry[target].top - target_used[target]
            source_used[source] += height
            target_used[target] += height

            x1, x2 = geometry[source].x + node_width, geometry[target].x
            cx = (x1 + x2) / 2
            verts = [
                (x1, y_source),
                (cx, y_source),
                (cx, y_target),
                (x2, y_target),
                (x2, y_target - height),
                (cx, y_target - height),
                (cx, y_source - height),
                (x1, y_source - height),
                (x1, y_source),
            ]
            codes = [
                Path.MOVETO,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.LINETO,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CLOSEPOLY,
            ]
            color = {
                "source": self.node_colors[source],
                "target": self.node_colors[target],
                "grey": SANKEY_GREY,
            }[self.link_color]
            ribbon = PathPatch(
                Path(verts, codes),
                facecolor=color,
                edgecolor="none",
                alpha=style.get("link_alpha"),
                zorder=2,
            )
            ax.add_patch(ribbon)
            link_marks.append(
                (
                    ribbon,
                    {
                        "label": None,
                        "source": source,
                        "target": target,
                        "flow": record["value"],
                    },
                )
            )
            if self.show_values:
                values.append(
                    (
                        height,
                        (x1, y_source - height / 2, x2, y_target - height / 2),
                        _format_value(self.value_format, record["value"]),
                    )
                )

        # the widest ribbons claim their midpoints first; the rest slide along
        # their curve to the first spot clear of the labels and earlier values
        for _, line, text in sorted(values, key=lambda v: v[0], reverse=True):
            fontsize = self.value_font["fontsize"]
            x1, y1, x2, y2 = line
            candidates = [(x2 - SANKEY_LABEL_PAD, y2, "right")] + [
                (*_ribbon_centerline(*line, t), "center")
                for t in SANKEY_VALUE_POSITIONS
            ]
            best = None
            for x, y, ha in candidates:
                box = _text_box(ax, x, y, text, fontsize, ha, halo)
                overlap = sum(_overlap_area(box, other) for other in occupied)
                if best is None or overlap < best[0]:
                    best = (overlap, x, y, ha, box)
                if overlap == 0:
                    break
            _, x, y, ha, box = best
            occupied.append(box)
            ax.text(
                x,
                y,
                text,
                ha=ha,
                va="center",
                zorder=4,
                path_effects=effects,
                **self.value_font,
            )

        self.register_patch_hover(node_marks)
        self.register_patch_hover(link_marks)
        ax.axis("off")


# ================================================
# Treemap Layer
# ================================================


def _squarify(values, x, y, w, h) -> list:
    """Squarified tiling (Bruls et al.) of descending `values` into a rectangle.

    Returns one (x, y, w, h) per value with the areas in proportion. Rows fill
    from the top-left, so the first value takes the top-left tile; the input
    is sorted descending by the caller so the rows stay near square.
    """

    scale = (w * h) / sum(values)
    areas = [v * scale for v in values]

    def worst(row, side):
        total = sum(row)
        return max(
            side * side * max(row) / (total * total),
            total * total / (side * side * min(row)),
        )

    rects, i = [], 0
    while i < len(areas):
        side = min(w, h)
        row, j = [areas[i]], i + 1
        while j < len(areas) and worst(row + [areas[j]], side) <= worst(row, side):
            row.append(areas[j])
            j += 1
        row_sum = sum(row)
        if w >= h:
            # a column on the left, filled top down
            rw = row_sum / h
            top = y + h
            for area in row:
                rh = area / rw
                top -= rh
                rects.append((x, top, rw, rh))
            x += rw
            w -= rw
        else:
            # a row along the top, filled left to right
            rh = row_sum / w
            left = x
            for area in row:
                rw = area / rh
                rects.append((left, y + h - rh, rw, rh))
                left += rw
            h -= rh
        i = j
    return rects


def _lighten(color, amount: float) -> str:
    """The color moved `amount` (0–1) of the way to white."""

    return to_hex(tuple(c + (1 - c) * amount for c in to_rgb(color)))


def _wrap_label(text) -> Optional[str]:
    """The label split at the space nearest its middle; None without a space."""

    cuts = [i for i, c in enumerate(text) if c == " "]
    if not cuts:
        return None
    cut = min(cuts, key=lambda i: abs(i - len(text) // 2))
    return text[:cut] + "\n" + text[cut + 1 :]


def _fit_text(label, value, box, size, value_size, min_size) -> Optional[tuple]:
    """Fit a label (and its value) into a (width, height) box in points.

    The ladder runs as is, wrapped, then shrunk in steps to `min_size`; with
    a value it runs first with the value and then without, so the value is
    dropped before the label. Returns (label, value, size, value_size), or
    None when nothing fits.
    """

    width, height = box[0] - TREEMAP_LABEL_PAD, box[1] - TREEMAP_LABEL_PAD
    wrapped = _wrap_label(label)
    candidates = [label] if wrapped is None else [label, wrapped]
    # the value shrinks in proportion to the label, never below the minimum
    value_step = TREEMAP_FONT_STEP * value_size / size
    for with_value in (True, False) if value else (False,):
        s, vs = size, max(value_size, min_size)
        while s >= min_size:
            for text in candidates:
                tw, th = _text_size(s, text)
                if with_value:
                    vw, vh = _text_size(vs, value)
                    tw, th = max(tw, vw), th + vh
                if tw <= width and th <= height:
                    return text, value if with_value else None, s, vs
            s -= TREEMAP_FONT_STEP
            vs = max(vs - value_step, min_size)
    return None


class TileFrame(NamedTuple):
    """What one treemap draw shares with every tile it places."""

    # the axes size in points; tiles are squarified in this aspect
    axes_pt: tuple
    aspect: float
    # the halo path effects behind every label
    effects: list
    # the (patch, datum) of every tile and band placed, for the hover container
    marks: list
    # the top-level group being drawn, whose pattern its boxes etch in
    group: Optional[str] = None


class TreemapLayer(Layer):
    """One treemap: every record of a chart as tiles and group boxes (ADR 0028).

    The layer owns its axes: a fixed 0–1 data space with the axis off, so the
    panel applies no furniture, scales, or limits around it. Tiling and text
    fitting read the axes size at draw time, so tiles are squarified in the
    axes' own aspect wherever the layer is drawn.
    """

    kind = "treemap"
    bare = True

    def __init__(self, chart: dict, settings: dict):
        self.records = chart["data"]["data"]
        super().__init__(chart, settings)

    def _resolve_style(self) -> None:
        self.treemap_style = get_treemap_style(self.style)
        self._resolve_bare_labels()
        # a group's header band reads as its subtitle
        self.band_style = get_text_style("subtitle")
        self.highlight_color = config["font_general_color"]
        # top-level records largest first; one palette color each, keyed by
        # label in input order, so a change in size never recolors a group
        self.groups = sorted(self.records, key=treemap_record_total, reverse=True)
        cycle = create_color_cycle(config["color_general_multiple"], len(self.groups))
        self.group_colors = {
            record["label"]: cycle[i]["color"] for i, record in enumerate(self.records)
        }
        # etching by depth in the group's pattern (ADR 0048); None keeps colors
        density = self.treemap_style.get("etch_density")
        patterns = config.get("plot_hatch_cycle")
        self.group_hatches = None
        if density and patterns and self.etch is not None:
            self.group_hatches = {
                record["label"]: patterns[i % len(patterns)]
                for i, record in enumerate(self.records)
            }

    def legend_handles(self):
        # a muted group is context, and like any background mark it has no entry
        groups = [r for r in self.groups if r.get("emphasis") != EMPHASIS_BACKGROUND]
        if self.group_hatches is not None:
            effect = self._etch_effect(0.0)
            return [
                Patch(
                    facecolor=self.ground,
                    edgecolor=self.treemap_style["edgecolor"],
                    hatch=self.group_hatches[record["label"]] or None,
                    path_effects=[effect],
                    label=record["label"],
                )
                for record in groups
            ]
        return [
            Patch(facecolor=self.group_colors[record["label"]], label=record["label"])
            for record in groups
        ]

    def _etch_box(self, patch, group: str, level: int) -> None:
        """Fill a box with the ground and etch it in its group's pattern for `level`.

        The fill is opaque, so the etching of an outer box never shows through.
        """

        if self.group_hatches is None or patch.get_facecolor()[3] == 0:
            return
        density = self.treemap_style["etch_density"]
        repeat = density[level] if level < len(density) else 0
        patch.set_facecolor(self.ground)
        patch.set_hatch(self.group_hatches[group] * repeat or None)
        patch.set_path_effects([self._etch_effect(0.0)])

    def draw(self, ax: plt.Axes, ctx: DrawContext) -> None:
        style = self.treemap_style
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        # lay the figure out first, so the axes size read below is the drawn one
        engine = ax.figure.get_layout_engine()
        if engine is not None:
            engine.execute(ax.figure)
        fig_w, fig_h = ax.figure.get_size_inches()
        pos = ax.get_position()
        axes_pt = (fig_w * pos.width * 72, fig_h * pos.height * 72)
        frame = TileFrame(
            axes_pt,
            axes_pt[0] / axes_pt[1],
            _halo_effects(style.get("halo_width"), self.ground),
            [],
        )
        aspect = frame.aspect
        pad = style["group_pad"]

        totals = [treemap_record_total(record) for record in self.groups]
        for record, (x, y, w, h) in zip(
            self.groups, _squarify(totals, 0, 0, aspect, 1)
        ):
            box = (x / aspect + pad / 2, y + pad / 2, w / aspect - pad, h - pad)
            color = self.group_colors[record["label"]]
            group_frame = frame._replace(group=record["label"])
            self._draw_record(
                ax, record, box, color, record.get("emphasis"), 0, group_frame
            )
        # tiles and bands never overlap, so one containment pick names one
        self.register_patch_hover(frame.marks)

    def _draw_record(self, ax, record, box, color, role, level, frame):
        """A record in its box: a group when it carries `children`, else a tile."""

        if record.get("children") is None:
            self._draw_tile(ax, record, box, color, role, level, frame)
        else:
            self._draw_group(ax, record, box, color, role, level, frame)

    def _draw_group(self, ax, record, box, color, role, level, frame):
        """A group at any level: band, children, and one border (ADR 0032)."""

        style = self.treemap_style
        axes_pt, aspect, effects, marks, _ = frame
        x, y, w, h = box
        label = record["label"]
        muted = role == EMPHASIS_BACKGROUND
        highlight = role == EMPHASIS_HIGHLIGHT
        box_color = self.muted_color if muted else color
        alpha = self.muted_alpha if muted else None
        # the box is filled in the group's color: the band and the gutter
        # around the children are one surface, under everything drawn inside
        ax.add_patch(
            Rectangle(
                (x, y),
                w,
                h,
                facecolor=box_color,
                edgecolor="none",
                alpha=alpha,
                zorder=1,
                gid=f"fill:{label}",
            )
        )
        if not muted:
            self._etch_box(ax.patches[-1], frame.group, level)

        # the band font scales per level, then shrinks to the minimum before
        # the group goes unlabelled
        band_size = self.band_style["fontsize"] * style["level_font_scale"] ** level
        band = 0.0
        while band_size >= style["min_fontsize"]:
            height = TREEMAP_BAND_HEIGHT * band_size / axes_pt[1]
            if h > TREEMAP_BAND_MIN_ROWS * height:
                band = height
                break
            band_size -= TREEMAP_FONT_STEP

        # children tile the area under the band, inset by the pad as the
        # top-level records are set apart by it; siblings meet at the stroke
        children = sorted(record["children"], key=treemap_record_total, reverse=True)
        child_color = _lighten(color, style["level_shade"])
        totals = [treemap_record_total(child) for child in children]
        gutter = style["group_pad"]
        inner = (x + gutter, y + gutter, w - 2 * gutter, h - band - 2 * gutter)
        for child, (cx, cy, cw, ch) in zip(
            children,
            _squarify(totals, inner[0] * aspect, inner[1], inner[2] * aspect, inner[3]),
        ):
            child_box = (cx / aspect, cy, cw / aspect, ch)
            # a child inherits its group's role unless it carries its own
            child_role = child.get("emphasis") or role
            self._draw_record(
                ax, child, child_box, child_color, child_role, level + 1, frame
            )

        if band:
            header = Rectangle(
                (x, y + h - band),
                w,
                band,
                facecolor=box_color,
                edgecolor="none",
                alpha=alpha,
                zorder=3,
                gid=f"band:{label}",
            )
            ax.add_patch(header)
            if not muted:
                self._etch_box(header, frame.group, level)
            marks.append(
                (header, {"label": label, "value": treemap_record_total(record)})
            )
            # a band label never wraps or shrinks; the legend names what is cut
            if (
                _text_size(band_size, label)[0]
                <= w * axes_pt[0] - 2 * TREEMAP_LABEL_PAD
            ):
                # centred on band + gutter, on the text body (ADR 0032)
                ax.text(
                    x + TREEMAP_LABEL_PAD / axes_pt[0],
                    y + h - (band + gutter) / 2,
                    label,
                    ha="left",
                    va="center_baseline",
                    fontsize=band_size,
                    fontweight=self.band_style["fontweight"],
                    family=self.band_style["family"],
                    color=self.muted_color if muted else self.band_style["color"],
                    path_effects=effects,
                    zorder=6,
                )
        # the group is a box: one border in the tile stroke color encloses
        # the band and the children
        ax.add_patch(
            Rectangle(
                (x, y),
                w,
                h,
                facecolor="none",
                edgecolor=self.highlight_color if highlight else style["edgecolor"],
                linewidth=(
                    style["highlight_linewidth"]
                    if highlight
                    else style["group_linewidth"]
                ),
                alpha=alpha,
                # under highlighted leaves, whose stroke must not be clipped
                zorder=3,
                gid=f"group:{label}",
            )
        )

    def _draw_tile(self, ax, record, box, color, role, level, frame):
        style = self.treemap_style
        axes_pt, _, effects, marks, _ = frame
        x, y, w, h = box
        muted = role == EMPHASIS_BACKGROUND
        highlight = role == EMPHASIS_HIGHLIGHT
        tile = Rectangle(
            (x, y),
            w,
            h,
            facecolor=self.muted_color if muted else color,
            alpha=self.muted_alpha if muted else None,
            edgecolor=self.highlight_color if highlight else style["edgecolor"],
            linewidth=(
                style["highlight_linewidth"] if highlight else style["linewidth"]
            ),
            zorder=4 if highlight else 2,
            gid=f"tile:{record['label']}",
        )
        ax.add_patch(tile)
        if not muted:
            self._etch_box(tile, frame.group, level)
        marks.append((tile, {"label": record["label"], "value": record["value"]}))
        scale = style["level_font_scale"] ** level
        value = (
            _format_value(self.value_format, record["value"])
            if self.show_values
            else None
        )
        fit = _fit_text(
            record["label"],
            value,
            (w * axes_pt[0], h * axes_pt[1]),
            self.label_style["fontsize"] * scale,
            self.value_font["fontsize"] * scale,
            style["min_fontsize"],
        )
        if fit is None:
            return
        text, value, size, value_size = fit
        common = {
            "ha": "center",
            "va": "center",
            "family": self.label_style["family"],
            "path_effects": effects,
            "zorder": 6,
            "linespacing": 1.1,
        }
        cx, cy = x + w / 2, y + h / 2
        text_color = self.muted_color if muted else self.label_style["color"]
        if value is None:
            ax.text(
                cx,
                cy,
                text,
                fontsize=size,
                color=text_color,
                fontweight=self.label_style["fontweight"],
                **common,
            )
            return
        # the label sits above the centre, the value below it
        label_h = _text_size(size, text)[1]
        value_h = _text_size(value_size, value)[1]
        ax.text(
            cx,
            cy + value_h / 2 / axes_pt[1],
            text,
            fontsize=size,
            color=text_color,
            fontweight=self.label_style["fontweight"],
            **common,
        )
        ax.text(
            cx,
            cy - label_h / 2 / axes_pt[1],
            value,
            fontsize=value_size,
            color=self.muted_color if muted else self.value_font["color"],
            **common,
        )


# ================================================
# Network Layer
# ================================================


def _fit_transform(pos: np.ndarray) -> tuple:
    """The uniform scale and offset that centre `pos` inside the layout margin."""

    low, high = pos.min(axis=0), pos.max(axis=0)
    span = (high - low).max()
    inner = 1 - 2 * NETWORK_LAYOUT_MARGIN
    if span == 0:
        return 0.0, np.full(2, 0.5)
    scale = inner / span
    return scale, 0.5 - (low + high) / 2 * scale


def _fit_layout(pos: np.ndarray) -> np.ndarray:
    """Positions scaled uniformly and centred inside the layout margin."""

    scale, offset = _fit_transform(pos)
    return pos * scale + offset


def edge_strengths(weights: list) -> list:
    """Each weight's pull under the weighted layouts (ADR 0030).

    Weights map linearly from the lightest at `NETWORK_PULL_MIN` to the
    heaviest at `NETWORK_PULL_MAX`; a missing weight pulls as the lightest.
    Without weights, or with all equal, every edge pulls at one: the plain
    spring picture.
    """

    given = [w for w in weights if w is not None]
    if not given or max(given) == min(given):
        return [1.0] * len(weights)
    low, span = min(given), max(given) - min(given)
    return [
        NETWORK_PULL_MIN
        + ((low if w is None else w) - low)
        / span
        * (NETWORK_PULL_MAX - NETWORK_PULL_MIN)
        for w in weights
    ]


def spring_layout(
    n: int,
    pairs: list,
    seed: int,
    strengths=None,
    gravity: float = 0.0,
    components: bool = True,
) -> np.ndarray:
    """Fruchterman–Reingold positions of `n` nodes joined by index `pairs`.

    Linked nodes attract in proportion to their distance squared, scaled by
    the pair's strength (one when `strengths` is None); every pair repels in
    inverse proportion to its distance; `gravity` pulls every node toward
    the centre in proportion to its distance; the step length cools
    geometrically. Seeded, so the same input renders the same picture. The
    result fits the 0–1 space inside the layout margin.

    With `components`, a disconnected graph lays out each component on its
    own and packs them by size, the isolated nodes on a ring around the rest
    (ADR 0029).
    """

    strengths = [1.0] * len(pairs) if strengths is None else list(strengths)
    if components and n > 1:
        from scipy.sparse import coo_matrix
        from scipy.sparse.csgraph import connected_components

        rows, cols = np.array(pairs, int).reshape(-1, 2).T
        adjacency = coo_matrix((np.ones(len(pairs)), (rows, cols)), shape=(n, n))
        count, labels = connected_components(adjacency, directed=False)
        if count > 1:
            return _fit_layout(
                _component_layout(labels, pairs, strengths, seed, gravity)
            )
    return _fit_layout(_spring_positions(n, pairs, seed, strengths, gravity))


def _spring_positions(
    n: int, pairs: list, seed: int, strengths: list, gravity: float
) -> np.ndarray:
    """One spring pass over the whole graph, in its own unfitted space."""

    rng = np.random.default_rng(seed)
    pos = rng.random((n, 2))
    if n < 2:
        return pos
    linked = np.zeros((n, n))
    for (i, j), s in zip(pairs, strengths):
        # a reverse pair or a repeated edge keeps the strongest pull
        linked[i, j] = linked[j, i] = max(linked[i, j], s)
    # the ideal edge length for n nodes in a unit square
    k = 1 / math.sqrt(n)
    step = NETWORK_SPRING_STEP
    for _ in range(NETWORK_SPRING_ITERATIONS):
        delta = pos[:, None, :] - pos[None, :, :]
        dist = np.linalg.norm(delta, axis=-1)
        np.fill_diagonal(dist, 1)
        dist = np.maximum(dist, 0.01)
        force = k * k / dist**2 - linked * dist / k
        disp = (delta * force[..., None]).sum(axis=1)
        disp -= gravity * (pos - pos.mean(axis=0))
        length = np.maximum(np.linalg.norm(disp, axis=1), 0.01)
        pos += disp / length[:, None] * np.minimum(length, step)[:, None]
        step *= NETWORK_SPRING_COOLING
    return pos


def _component_layout(
    labels: np.ndarray, pairs: list, strengths: list, seed: int, gravity: float
) -> np.ndarray:
    """Each component's own spring, packed like clusters; isolates ring the rest."""

    n = len(labels)
    members = [np.flatnonzero(labels == c) for c in range(labels.max() + 1)]
    # the largest first, so it takes the centre
    members.sort(key=len, reverse=True)
    linked = [idx for idx in members if len(idx) > 1]
    isolates = [idx[0] for idx in members if len(idx) == 1]
    pos = np.zeros((n, 2))
    reach = 0.0
    if linked:
        local = []
        for idx in linked:
            place = {node: k for k, node in enumerate(idx)}
            inside = [
                ((place[i], place[j]), w)
                for (i, j), w in zip(pairs, strengths)
                if i in place
            ]
            spring = _spring_positions(
                len(idx),
                [pair for pair, _ in inside],
                seed,
                [w for _, w in inside],
                gravity,
            )
            local.append(spring - (spring.min(axis=0) + spring.max(axis=0)) / 2)
        sizes = np.array([len(idx) for idx in linked], float)
        radius = NETWORK_CLUSTER_RADIUS * np.sqrt(sizes / n)
        # the largest at the centre, the rest a golden-angle spiral around it
        turns = np.arange(len(linked)) * np.pi * (3 - np.sqrt(5))
        centers = (
            np.column_stack([np.cos(turns), np.sin(turns)])
            * np.sqrt(np.arange(len(linked)))[:, None]
            * radius[0]
        )
        centers, radius = _pack_clusters(centers, radius, NETWORK_COMPONENT_GAP)
        for idx, spring, centre, r in zip(linked, local, centers, radius):
            pos[idx] = centre + spring / (np.linalg.norm(spring, axis=1).max() or 1) * r
        linked_nodes = np.concatenate(linked)
        middle = (pos[linked_nodes].min(axis=0) + pos[linked_nodes].max(axis=0)) / 2
        pos[linked_nodes] -= middle
        reach = np.linalg.norm(pos[linked_nodes], axis=1).max()
    if isolates:
        # a lone node takes a one-node cluster's diameter of room on the ring
        spacing = 2 * NETWORK_CLUSTER_RADIUS / math.sqrt(n)
        ring = max(reach + spacing, len(isolates) * spacing / (2 * np.pi))
        pos[isolates] = ring * _ring(len(isolates))
    return pos


def _pack_clusters(centers: np.ndarray, radius: np.ndarray, gap: float) -> tuple:
    """Cluster centres pushed `gap` times their summed radii apart, each radius
    shrunk clear of its nearest neighbour."""

    if len(centers) < 2:
        return centers, radius
    min_dist = (radius[:, None] + radius[None, :]) * gap
    for _ in range(NETWORK_CLUSTER_PUSH_ITERATIONS):
        delta, dist = _centre_distances(centers)
        overlap = np.maximum(min_dist - dist, 0)
        if not overlap.any():
            break
        centers = centers + (delta / dist[..., None] * (overlap / 2)[..., None]).sum(
            axis=1
        )
    _, dist = _centre_distances(centers)
    radius_share = radius[:, None] / (radius[:, None] + radius[None, :])
    radius = np.minimum(
        radius, (dist * radius_share).min(axis=1) * NETWORK_CLUSTER_FILL
    )
    return centers, radius


def grouped_layout(groups: list, pairs: list, weights: list, seed: int) -> tuple:
    """Two-level spring positions: clusters by group, arranged by their links (ADR 0030).

    `groups[i]` is node `i`'s group, None for none; an ungrouped node is a
    group of one. Each group runs the plain spring on the edges inside it.
    The groups then run the weighted spring as a smaller network, an edge
    between two groups weighing the sum of the edges joining them (a missing
    weight counts one). Overlapping clusters are pushed apart, each shrinks
    to keep clear of its nearest neighbour, and the whole fits the 0–1 space.

    Returns the positions and the clusters of the named groups as
    `(group, centre, radius)` in the same space, for the halo behind each.
    """

    n = len(groups)
    keys = [
        ("group", g) if g is not None else ("node", i) for i, g in enumerate(groups)
    ]
    names = list(dict.fromkeys(keys))
    index = {name: k for k, name in enumerate(names)}
    group_of = [index[key] for key in keys]
    members = [[i for i in range(n) if group_of[i] == g] for g in range(len(names))]

    # level one: each group's own spring, centred on the origin
    local = np.zeros((n, 2))
    for g, idx in enumerate(members):
        place = {node: k for k, node in enumerate(idx)}
        inside = [
            (place[i], place[j])
            for i, j in pairs
            if group_of[i] == g and group_of[j] == g
        ]
        local[idx] = (
            spring_layout(
                len(idx),
                inside,
                seed,
                gravity=NETWORK_CLUSTER_GRAVITY,
                components=False,
            )
            - 0.5
        )

    # level two: the groups as a weighted network
    between = {}
    for (i, j), w in zip(pairs, weights):
        a, b = sorted((group_of[i], group_of[j]))
        if a != b:
            between[(a, b)] = between.get((a, b), 0) + (1 if w is None else w)
    links = list(between)
    centers = spring_layout(
        len(names),
        links,
        seed,
        edge_strengths([between[k] for k in links]),
        gravity=NETWORK_CLUSTER_GRAVITY,
        components=False,
    )

    sizes = np.array([len(idx) for idx in members], float)
    centers, radius = _pack_clusters(
        centers, NETWORK_CLUSTER_RADIUS * np.sqrt(sizes / n), NETWORK_CLUSTER_GAP
    )

    # a group's local picture fills a square; scale its farthest node onto the
    # cluster radius so every node lies within the disc
    pos = np.zeros((n, 2))
    for g, idx in enumerate(members):
        reach = np.linalg.norm(local[idx], axis=1).max()
        pos[idx] = centers[g] + local[idx] / (reach or 1) * radius[g]
    named = [g for g, name in enumerate(names) if name[0] == "group"]
    # the fit keeps the named clusters' discs inside the margin, not only the nodes
    rim = radius[named, None]
    scale, offset = _fit_transform(
        np.vstack([pos, centers[named] - rim, centers[named] + rim])
    )
    clusters = [
        (names[g][1], centers[g] * scale + offset, radius[g] * scale) for g in named
    ]
    return pos * scale + offset, clusters


def _centre_distances(centers: np.ndarray):
    """Pairwise offsets and distances between cluster centres, the diagonal infinite."""

    delta = centers[:, None] - centers[None]
    dist = np.linalg.norm(delta, axis=-1)
    np.fill_diagonal(dist, np.inf)
    return delta, dist


def circular_layout(n: int) -> np.ndarray:
    """`n` nodes evenly spaced on a circle, the first at the top, clockwise."""

    if n < 2:
        return np.full((n, 2), 0.5)
    return 0.5 + (0.5 - NETWORK_LAYOUT_MARGIN) * _ring(n)


def _ring(n: int) -> np.ndarray:
    """`n` points evenly spaced on the unit circle, the first at the top, clockwise."""

    angles = np.pi / 2 - np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.column_stack([np.cos(angles), np.sin(angles)])


def _linear_map(values: list, low: float, high: float, missing: float) -> np.ndarray:
    """Values mapped linearly onto [low, high]; None and a degenerate range map to `missing`."""

    out = np.full(len(values), missing, dtype=float)
    given = [i for i, v in enumerate(values) if v is not None]
    if not given:
        return out
    known = np.array([values[i] for i in given], dtype=float)
    span = known.max() - known.min()
    if span > 0:
        out[given] = low + (known - known.min()) / span * (high - low)
    return out


class NetworkLayer(PointLabelMixin, Layer):
    """One network: every node and edge of a chart as a node-link diagram (ADR 0029).

    The layer owns its axes: a fixed 0–1 data space with equal aspect and the
    axis off, so the panel applies no furniture, scales, or limits around it.
    Positions are computed once at build time, so a redraw into another axes
    keeps the picture.
    """

    kind = "network"
    bare = True

    def __init__(self, chart: dict, settings: dict):
        data = chart["data"]
        self.edges = data["edges"]
        nodes = data.get("nodes")
        self.nodes = infer_network_nodes(self.edges) if nodes is None else nodes
        self.directed = bool(settings.get("directed"))
        self.layout = settings.get("layout") or NETWORK_LAYOUT.DEFAULT
        self.seed = 0 if settings.get("seed") is None else settings["seed"]
        # edges and edge values drawn per axes, the obstacles of BEST labels
        self._obstacles = {}
        self._init_point_labels()
        super().__init__(chart, settings)

    def _resolve_style(self) -> None:
        style = get_network_style(self.style)
        self.network_style = style
        self.edge_style = validate_network_edge_style(style.get("edge_style"))
        self._resolve_bare_labels()
        self.highlight_color = config["font_general_color"]

        ids = [node["id"] for node in self.nodes]
        index = {node_id: i for i, node_id in enumerate(ids)}
        # undirected reverse duplicates draw as one line; the first-seen wins
        drawn, seen = [], set()
        for record in self.edges:
            key = (record["source"], record["target"])
            if not self.directed:
                key = tuple(sorted(key, key=str))
            if key in seen:
                continue
            seen.add(key)
            drawn.append(record)
        self.drawn_edges = drawn
        self.pairs = [(index[e["source"]], index[e["target"]]) for e in drawn]
        self.weights = [record.get("weight") for record in drawn]
        # a node's degree (in/out when directed) counts its edges, or sums
        # their weights once any edge has one (an unweighted edge counts one)
        weighted = any(w is not None for w in self.weights)
        n = len(self.nodes)
        incoming, outgoing = [0] * n, [0] * n
        for (i, j), weight in zip(self.pairs, self.weights):
            share = weight if weighted and weight is not None else 1
            outgoing[i] += share
            incoming[j] += share
        # the hover datum per node; group and size ride along when given
        self.node_datums = []
        for k, node in enumerate(self.nodes):
            datum = {"label": node["id"] if not node.get("label") else node["label"]}
            if self.directed:
                datum.update({"in": incoming[k], "out": outgoing[k]})
            else:
                datum["degree"] = incoming[k] + outgoing[k]
            for key in ("group", "size"):
                if node.get(key) is not None:
                    datum[key] = node[key]
            self.node_datums.append(datum)
        self.groups = [node.get("group") for node in self.nodes]
        # the clusters behind the nodes: only the grouped layout has any
        self.clusters = []
        self.positions = self._layout()

        # encodings: sqrt(size) to marker area, weight to edge width
        sizes = [
            None if node.get("size") is None else math.sqrt(node["size"])
            for node in self.nodes
        ]
        self.areas = _linear_map(
            sizes, style["node_size_min"], style["node_size_max"], style["node_size"]
        )
        self.widths = _linear_map(
            self.weights,
            style["edge_width_min"],
            style["edge_width_max"],
            style["edge_width_min"],
        )

        # colors: one singular color, or the multiple cycle keyed by group with
        # an ungrouped node in the edge color so it reads as no group's member
        groups = self.groups
        self.group_names = list(dict.fromkeys(g for g in groups if g is not None))
        if style.get("node_color") is not None:
            base = style["node_color"]
            self.group_colors = {g: base for g in self.group_names}
        elif self.group_names:
            cycle = create_color_cycle(
                config["color_general_multiple"], len(self.group_names)
            )
            self.group_colors = {
                g: cycle[i]["color"] for i, g in enumerate(self.group_names)
            }
            base = style["edge_color"]
        else:
            base = create_color_cycle(config["color_general_singular"], 1)[0]["color"]
            self.group_colors = {}
        self.node_colors = [self.group_colors.get(g, base) for g in groups]
        # groups take the theme's marker cycle, as series do (ADR 0048); a chart
        # style that sets the node marker wins
        cycle = config.get("plot_marker_cycle")
        plain = (style["node_marker"], False)
        self.group_markers = {g: plain for g in self.group_names}
        if cycle and "plot_network_node_marker" not in self.style:
            self.group_markers = {
                g: _marker_entry(cycle[i % len(cycle)])
                for i, g in enumerate(self.group_names)
            }
        self.node_markers = [self.group_markers.get(g, plain) for g in groups]
        self.label_position = validate_node_label_position(
            self.settings.get("label_position")
            or config.get("chart_default_node_label_position")
        )
        roles = [node.get("emphasis") for node in self.nodes]
        self.muted = [role == EMPHASIS_BACKGROUND for role in roles]
        self.highlighted = [role == EMPHASIS_HIGHLIGHT for role in roles]

    def _layout(self) -> np.ndarray:
        if self.layout == NETWORK_LAYOUT.FIXED:
            return np.array([[node["x"], node["y"]] for node in self.nodes], float)
        if self.layout == NETWORK_LAYOUT.CIRCULAR:
            return circular_layout(len(self.nodes))
        if self.layout == NETWORK_LAYOUT.WEIGHTED:
            return spring_layout(
                len(self.nodes), self.pairs, self.seed, edge_strengths(self.weights)
            )
        if self.layout == NETWORK_LAYOUT.GROUPED:
            pos, self.clusters = grouped_layout(
                self.groups, self.pairs, self.weights, self.seed
            )
            return pos
        return spring_layout(len(self.nodes), self.pairs, self.seed)

    def legend_handles(self):
        if not self.group_names:
            return None
        handles = []
        for g in self.group_names:
            marker, hollow = self.group_markers[g]
            hollow_look = {}
            if hollow:
                hollow_look = {
                    "markerfacecolor": "none",
                    "markeredgewidth": HOLLOW_MARKER_EDGE_WIDTH,
                }
            handles.append(
                Line2D(
                    [],
                    [],
                    marker=marker,
                    linestyle="",
                    color=self.group_colors[g],
                    # half the default marker's diameter: a legend swatch, not a node
                    markersize=math.sqrt(self.network_style["node_size"]) / 2,
                    label=g,
                    **hollow_look,
                )
            )
        return handles

    def draw(self, ax: plt.Axes, ctx: DrawContext) -> None:
        style = self.network_style
        pos = self.positions
        pad = NETWORK_FIXED_PAD if self.layout == NETWORK_LAYOUT.FIXED else 0
        ax.set_xlim(-pad, 1 + pad)
        ax.set_ylim(-pad, 1 + pad)
        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")
        effects = _halo_effects(style.get("halo_width"), self.ground)
        muted, highlighted = self.muted, self.highlighted
        best = self.label_position == NETWORK_LABEL_POSITION.BEST
        # scatter sizes are the marker's bounding-box diameter squared
        radii = np.sqrt(self.areas) / 2
        curve = (
            0.0 if self.edge_style == ARROW_STYLE.STRAIGHT else style["edge_curve"]
        ) or 0.0
        connection = f"arc3,rad={curve}"
        pen = style.get("edge_ink_stroke")
        pen = [InkStroke(**pen)] if pen else []

        # a translucent disc in the group color behind each cluster, reaching
        # past the largest marker of the group (points to 0–1 data units)
        if style.get("group_alpha"):
            ax.apply_aspect()
            axis_pt = ax.get_window_extent().width * 72 / ax.figure.dpi
            ring = style.get("group_linestyle")
            for group, centre, radius in self.clusters:
                marker_pt = max(r for r, g in zip(radii, self.groups) if g == group)
                look = {
                    "facecolor": self.group_colors[group],
                    "edgecolor": "none",
                    "alpha": style["group_alpha"],
                }
                if ring is not None:
                    # a ring marks the cluster without tinting what it holds
                    look = {
                        "facecolor": "none",
                        "edgecolor": style["edge_color"],
                        "linestyle": ring,
                        "linewidth": NETWORK_RING_WIDTH,
                        "alpha": style["edge_alpha"],
                    }
                ax.add_patch(
                    Circle(
                        centre,
                        radius + marker_pt / axis_pt + NETWORK_CLUSTER_HALO_PAD,
                        zorder=1,
                        gid=f"group:{group}",
                        **look,
                    )
                )

        for record, (i, j), width in zip(self.drawn_edges, self.pairs, self.widths):
            edge_muted = muted[i] or muted[j]
            color = self.muted_color if edge_muted else style["edge_color"]
            alpha = self.muted_alpha if edge_muted else style["edge_alpha"]
            gid = f"edge:{record['source']}->{record['target']}"
            head = NETWORK_ARROW_HEAD_BASE + NETWORK_ARROW_HEAD_PER_WIDTH * width
            if self.directed and pen:
                # a stroked shaft with a small head lets the pen pressure show
                patch = FancyArrowPatch(
                    pos[i],
                    pos[j],
                    arrowstyle=(
                        f"-|>,head_length={head},"
                        f"head_width={NETWORK_INKED_HEAD_WIDTH * head}"
                    ),
                    mutation_scale=1,
                    connectionstyle=connection,
                    shrinkA=radii[i],
                    shrinkB=radii[j],
                    color=color,
                    linewidth=width,
                    alpha=alpha,
                    zorder=2,
                    gid=gid,
                )
            elif self.directed:
                # one filled polygon: the shaft and the head share an outline,
                # so the alpha never doubles where they meet
                patch = FancyArrowPatch(
                    pos[i],
                    pos[j],
                    arrowstyle=(
                        f"simple,tail_width={width},"
                        f"head_width={head},head_length={head}"
                    ),
                    mutation_scale=1,
                    connectionstyle=connection,
                    shrinkA=radii[i],
                    shrinkB=radii[j],
                    facecolor=color,
                    edgecolor="none",
                    linewidth=0,
                    alpha=alpha,
                    zorder=2,
                    gid=gid,
                )
            else:
                patch = FancyArrowPatch(
                    pos[i],
                    pos[j],
                    arrowstyle="-",
                    connectionstyle=connection,
                    color=color,
                    linewidth=width,
                    alpha=alpha,
                    zorder=2,
                    gid=gid,
                )
            patch.set_path_effects(pen)
            ax.add_patch(patch)
            if best:
                self._obstacles.setdefault(id(ax), []).append(patch)
            datum = {
                "label": None,
                "source": record["source"],
                "target": record["target"],
            }
            if record.get("weight") is not None:
                datum["weight"] = record["weight"]
            self.register_hover(patch, lambda _, datum=datum: datum)
            if self.show_values and record.get("weight") is not None:
                # the midpoint of the arc3 quadratic Bézier, not of the chord
                mid = (pos[i] + pos[j]) / 2
                dx, dy = pos[j] - pos[i]
                mid = mid + curve / 2 * np.array([dy, -dx])
                value = ax.text(
                    mid[0],
                    mid[1],
                    _format_value(self.value_format, record["weight"]),
                    ha="center",
                    va="center",
                    zorder=4,
                    path_effects=effects,
                    gid=f"value:{record['source']}->{record['target']}",
                    **{
                        **self.value_font,
                        "color": (
                            self.muted_color if edge_muted else self.value_font["color"]
                        ),
                    },
                )
                if best:
                    self._obstacles.setdefault(id(ax), []).append(value)

        face = [
            self.muted_color if muted[k] else color
            for k, color in enumerate(self.node_colors)
        ]
        alpha = [
            self.muted_alpha if muted[k] else style["node_alpha"]
            for k in range(len(self.nodes))
        ]
        rim_widths = np.broadcast_to(
            _marker_edge_widths(style["linewidth"], self.areas), len(self.nodes)
        )
        edges = [self.highlight_color if h else style["edgecolor"] for h in highlighted]
        widths = [
            style["highlight_linewidth"] if h else w
            for h, w in zip(highlighted, rim_widths)
        ]
        # one scatter per marker: a scatter draws a single shape
        for marker, hollow in dict.fromkeys(self.node_markers):
            ks = [
                k
                for k, entry in enumerate(self.node_markers)
                if entry == (marker, hollow)
            ]
            look = {
                "c": [face[k] for k in ks],
                "alpha": [alpha[k] for k in ks],
                "edgecolors": [edges[k] for k in ks],
                "linewidths": [widths[k] for k in ks],
            }
            if hollow:
                # the outline in the face color is the mark; a collection alpha
                # would fill "none" faces, so the alpha rides on the edge color
                look = {
                    "facecolors": "none",
                    "edgecolors": [
                        to_rgba(edges[k] if highlighted[k] else face[k], alpha[k])
                        for k in ks
                    ],
                    "linewidths": [
                        max(widths[k], HOLLOW_MARKER_EDGE_WIDTH) for k in ks
                    ],
                }
            points = ax.scatter(
                pos[ks, 0],
                pos[ks, 1],
                s=self.areas[ks],
                marker=marker,
                zorder=3,
                gid="nodes",
                **look,
            )
            self.register_hover(points, lambda i, ks=ks: self.node_datums[ks[i]])

        above = self.label_position == NETWORK_LABEL_POSITION.ABOVE
        for k, node in enumerate(self.nodes):
            label = node.get("label")
            label = node["id"] if label is None else label
            if label == "":
                continue
            font = {
                **self.label_style,
                "color": self.muted_color if muted[k] else self.label_style["color"],
            }
            if best:
                # the panel places it once every mark is drawn, clear of the rest
                self._record_points(
                    ax,
                    ctx,
                    pos[k : k + 1, 0],
                    pos[k : k + 1, 1],
                    self.areas[k : k + 1],
                    labels=[label],
                    font={
                        **font,
                        "path_effects": effects,
                        "gid": f"label:{node['id']}",
                    },
                    pad=NETWORK_LABEL_GAP,
                )
                continue
            # a name above its node sits clear of the marker, like a place name
            lift = (radii[k] + NETWORK_LABEL_GAP) / 72 if above else 0
            ax.text(
                pos[k, 0],
                pos[k, 1],
                label,
                transform=ax.transData
                + ScaledTranslation(0, lift, ax.figure.dpi_scale_trans),
                ha="center",
                va="bottom" if above else "center",
                zorder=5,
                path_effects=effects,
                gid=f"label:{node['id']}",
                **font,
            )

    def label_obstacles(self, ax) -> list:
        """The edges and edge values drawn into `ax`, as display-space boxes.

        A text is one box around its anchor; an edge is a chain of small boxes
        along its flattened path, so a label may sit in the bay between two
        edges where the path's own bounding box would forbid it.
        """

        ax.apply_aspect()
        px_per_pt = ax.figure.dpi / 72.0
        boxes = []
        for artist in self._obstacles.pop(id(ax), []):
            if isinstance(artist, Text):
                cx, cy = ax.transData.transform(artist.get_position())
                w, h = (
                    v * px_per_pt
                    for v in _text_size(artist.get_fontsize(), artist.get_text())
                )
                boxes.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
                continue
            half = max(artist.get_linewidth() * px_per_pt, 2.0) / 2
            path = artist.get_transform().transform_path(artist.get_path())
            previous = None
            for vertices, code in path.iter_segments(curves=False, simplify=False):
                point = np.asarray(vertices[-2:], float)
                if previous is not None and code == Path.LINETO:
                    span = point - previous
                    steps = max(int(np.hypot(*span) // NETWORK_OBSTACLE_STEP), 1)
                    for t in np.linspace(0, 1, steps + 1):
                        x, y = previous + span * t
                        boxes.append((x - half, y - half, x + half, y + half))
                previous = point
        return boxes


LAYER_TYPES = {
    "linechart": LineLayer,
    "barchart": BarLayer,
    # a pyramid is the bar seam under mirrored panel furniture (ADR 0017)
    "pyramidchart": BarLayer,
    "histogram": HistogramLayer,
    "kde": KdeLayer,
    "scatterchart": ScatterLayer,
    "boxplot": BoxLayer,
    "swarmplot": SwarmLayer,
    "violinplot": ViolinLayer,
    "ridgelineplot": RidgelineLayer,
    "heatmap": HeatmapLayer,
    "contourchart": ContourLayer,
    "hexbinchart": HexbinLayer,
    "stackedareachart": StackedAreaLayer,
    "bumpchart": BumpLayer,
    "sankeychart": SankeyLayer,
    "treemap": TreemapLayer,
    "networkchart": NetworkLayer,
    "calendarheatmap": CalendarHeatmapLayer,
    "ganttchart": GanttLayer,
    "dumbbellchart": DumbbellLayer,
}

RADIAL_LAYER_TYPES = {
    RADIAL_TYPE.LINE: RadialLineLayer,
    RADIAL_TYPE.BAR: RadialBarLayer,
    RADIAL_TYPE.SCATTER: RadialScatterLayer,
    RADIAL_TYPE.HISTOGRAM: RadialHistogramLayer,
}


def emphasis_rule_roles(rule: tuple, values: list) -> list:
    """The emphasis role of each value under a validated rule (ADR 0042).

    A matching value is highlighted, every other one muted. `above`/`below`
    are strict, `between` inclusive; `top`/`bottom` clamp to the value count
    and break ties by input order. A missing (NaN) value never matches.
    """

    key, bound, _ = rule
    values = [float(v) for v in values]
    if key == "above":
        matches = [v > bound for v in values]
    elif key == "below":
        matches = [v < bound for v in values]
    elif key == "between":
        matches = [bound[0] <= v <= bound[1] for v in values]
    else:
        sign = -1 if key == "top" else 1
        present = [i for i, v in enumerate(values) if not math.isnan(v)]
        picked = set(sorted(present, key=lambda i: sign * values[i])[:bound])
        matches = [i in picked for i in range(len(values))]
    return [EMPHASIS_HIGHLIGHT if m else EMPHASIS_BACKGROUND for m in matches]


def _bar_record_values(charts: List[dict], magnitude: bool) -> list:
    """`(label, value)` per drawn record of each chart; magnitudes when asked."""

    columns = []
    for chart in charts:
        if not isinstance(chart.get("data"), list):
            raise ValueError(
                "`sort` and `emphasis_rule` read bar records; pass `data` as a "
                "list of `{label, y}` dicts, not columns."
            )
        label_key = get_attr_value("label", chart, "label")
        y_key = get_attr_value("y", chart, "y")
        columns.append(
            [
                (
                    record.get(label_key),
                    abs(record[y_key]) if magnitude else record[y_key],
                )
                for record in _bar_records(chart)
            ]
        )
    return columns


def _sort_bar_charts(charts: List[dict], sort, sort_by, magnitude: bool) -> List[dict]:
    """The charts with their records in category order (ADR 0042).

    One order serves every chart: categories sort by their total across the
    charts, or by the value in the one chart `sort_by` names by subtitle;
    categories that chart lacks sort last. Ties keep input order.
    """

    validate_sort_by(sort, sort_by, [chart.get("subtitle") for chart in charts])
    if sort is None:
        return charts

    columns = _bar_record_values(charts, magnitude)
    keyed = [
        column
        for chart, column in zip(charts, columns)
        if sort_by is None or chart.get("subtitle") == sort_by
    ]
    totals = defaultdict(float)
    for column in keyed:
        for label, value in column:
            totals[label] += value
    categories = []
    for column in columns:
        for label, _ in column:
            if label not in categories:
                categories.append(label)
    sign = -1 if sort == SORT.DESCENDING else 1
    ordered = sorted(
        categories, key=lambda c: (c not in totals, sign * totals.get(c, 0))
    )
    rank = {label: i for i, label in enumerate(ordered)}

    sorted_charts = []
    for chart in charts:
        label_key = get_attr_value("label", chart, "label")
        data = sorted(
            chart["data"],
            key=lambda r: rank.get(
                r.get(label_key) if isinstance(r, dict) else None, len(rank)
            ),
        )
        sorted_charts.append({**chart, "data": data})
    return sorted_charts


# how a group or series rule summarises its values (ADR 0045)
EMPHASIS_RULE_SUMMARY_FUNCTIONS = {
    "mean": np.mean,
    "median": np.median,
    "min": np.min,
    "max": np.max,
    "sum": np.sum,
}


def _rule_summary(values, by: str, name: str) -> float:
    """One number for a unit's values; NaN when it has none to read."""

    if values is None:
        return math.nan
    try:
        values = np.asarray(values, dtype=float).ravel()
    except (TypeError, ValueError):
        raise ValueError(
            f"`emphasis_rule` reads numeric `{name}` values to summarise by "
            f"`{by}`; got non-numeric ones."
        ) from None
    values = values[~np.isnan(values)]
    if values.size == 0:
        return math.nan
    return float(EMPHASIS_RULE_SUMMARY_FUNCTIONS[by](values))


def _fill_role(target, key) -> Callable[[str], None]:
    """A setter writing a rule's role into `target[key]` unless one is set."""

    def fill(role):
        if target[key] is None:
            target[key] = role

    return fill


def _keep_role(role) -> None:
    """The setter of a unit whose explicit role wins over the rule."""


def _aligned_roles(chart: dict, n: int) -> Optional[list]:
    """A fillable copy of a chart's `emphasis` list aligned to `n` units.

    None when the chart's role is one string for all of them, or a list the
    layer will reject for its length; the rule then fills nothing there.
    """

    roles = chart.get("emphasis")
    if roles is None:
        roles = [None] * n
    if not isinstance(roles, list) or len(roles) != n:
        return None
    chart["emphasis"] = roles = list(roles)
    return roles


def _bar_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per drawn bar record, reading its own `y` (ADR 0042).

    A pyramid's negated left side reads as magnitudes.
    """

    columns = _bar_record_values(charts, bool(settings.get("pyramid")))
    filled, units = [], []
    for chart, column in zip(charts, columns):
        y_key = get_attr_value("y", chart, "y")
        data = [
            {"emphasis": None, **r} if _is_bar_record(r, y_key) else r
            for r in chart["data"]
        ]
        records = [r for r in data if _is_bar_record(r, y_key)]
        units += [
            (value, _fill_role(record, "emphasis"))
            for record, (_, value) in zip(records, column)
        ]
        filled.append({**chart, "data": data})
    return filled, units


def _gantt_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per task record, reading its duration in days (ADR 0049)."""

    filled, units = [], []
    for chart in charts:
        data = [
            {"emphasis": None, **r} if isinstance(r, dict) else r for r in chart["data"]
        ]
        tasks = gantt_tasks({"data": data})
        units += [
            (days, _fill_role(task, "emphasis"))
            for task, days in zip(tasks, gantt_durations(tasks))
        ]
        filled.append({**chart, "data": data})
    return filled, units


def _dumbbell_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per dumbbell record, reading its delta (ADR 0050)."""

    filled, units = [], []
    for chart in charts:
        records = [{"emphasis": None, **r} for r in dumbbell_records(chart)]
        units += [(r["end"] - r["start"], _fill_role(r, "emphasis")) for r in records]
        filled.append({**chart, "data": records})
    return filled, units


def _series_units(column: str) -> Callable:
    """The unit builder of a per-series front: each chart, by its `column`."""

    def units(charts: List[dict], settings: dict, by) -> tuple:
        filled = [{"emphasis": None, **chart} for chart in charts]
        return filled, [
            (
                _rule_summary(get_chart_data(column, chart), by, column),
                _fill_role(chart, "emphasis"),
            )
            for chart in filled
        ]

    return units


def _group_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per group label of each chart, by a summary of its values."""

    filled, units = [dict(chart) for chart in charts], []
    for chart in filled:
        grouped = grouped_values(chart)
        roles = _aligned_roles(chart, len(grouped))
        for i, values in enumerate(grouped.values()):
            fill = _keep_role if roles is None else _fill_role(roles, i)
            units.append((_rule_summary(values, by, "value"), fill))
    return filled, units


def _treemap_record_units(record: dict, inherited, units: list) -> dict:
    """A copy of a treemap record whose leaves register as rule units.

    A group's explicit role covers its subtree, so its leaves keep it.
    """

    record = {"emphasis": None, **record}
    role = record["emphasis"] or inherited
    if record.get("children") is None:
        fill = _fill_role(record, "emphasis") if role is None else _keep_role
        units.append((record["value"], fill))
    else:
        record["children"] = [
            _treemap_record_units(child, role, units) for child in record["children"]
        ]
    return record


def _treemap_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per leaf record, by its `value`; groups keep explicit roles."""

    filled, units = [], []
    for chart in charts:
        data = chart["data"]
        records = [_treemap_record_units(r, None, units) for r in data["data"]]
        filled.append({**chart, "data": {**data, "data": records}})
    return filled, units


def _network_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per node, by its `size`; a node without one raises."""

    filled, units = [], []
    for chart in charts:
        data = chart["data"]
        nodes = data.get("nodes")
        if nodes is None:
            nodes = infer_network_nodes(data["edges"])
        nodes = [{"emphasis": None, **node} for node in nodes]
        for node in nodes:
            if node.get("size") is None:
                raise ValueError(
                    "`emphasis_rule` reads each node's `size`; node "
                    f"{node['id']!r} has none."
                )
            units.append((node["size"], _fill_role(node, "emphasis")))
        filled.append({**chart, "data": {**data, "nodes": nodes}})
    return filled, units


def _parallel_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per data row, by its numeric `hue` value."""

    filled, units = [dict(chart) for chart in charts], []
    for chart in filled:
        hue = chart.get("hue")
        if hue is None:
            raise ValueError(
                "`emphasis_rule` reads each row's `hue` value; pass `hue` "
                "naming a numeric column."
            )
        rows = chart.get("data") or []
        roles = _aligned_roles(chart, len(rows))
        for i, row in enumerate(rows):
            value = row.get(hue)
            if not isinstance(value, Real) or isinstance(value, bool):
                raise ValueError(
                    f"`emphasis_rule` reads each row's `{hue}` value as a "
                    f"number; row {i} has {value!r}."
                )
            fill = _keep_role if roles is None else _fill_role(roles, i)
            units.append((value, fill))
    return filled, units


def _heatmap_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per cell, by its value; a blank cell never matches."""

    filled, units = [], []
    for chart in charts:
        z = get_chart_grid(chart, "heatmap", dtype=object)[2]
        roles = heatmap_cell_roles(chart, z)
        for i, row in enumerate(z):
            for j, value in enumerate(row):
                # a blank cell draws nothing to mute
                if value is None or math.isnan(value):
                    units.append((math.nan, _keep_role))
                else:
                    units.append((value, _fill_role(roles[i], j)))
        filled.append({**chart, "data": {**chart["data"], "emphasis": roles}})
    return filled, units


# per front: a rule's unit builder and default `by` (ADR 0045)
EMPHASIS_RULE_UNITS = {
    "barchart": (_bar_units, None),
    "pyramidchart": (_bar_units, None),
    "radialchart": (_bar_units, None),
    "treemap": (_treemap_units, None),
    "networkchart": (_network_units, None),
    "parallelcoords": (_parallel_units, None),
    "heatmap": (_heatmap_units, None),
    "boxplot": (_group_units, "median"),
    "violinplot": (_group_units, "median"),
    "swarmplot": (_group_units, "median"),
    "raincloudplot": (_group_units, "median"),
    "ridgelineplot": (_group_units, "median"),
    "linechart": (_series_units("y"), "mean"),
    "scatterchart": (_series_units("y"), "mean"),
    "stackedareachart": (_series_units("y"), "mean"),
    "bumpchart": (_series_units("y"), "mean"),
    "ganttchart": (_gantt_units, None),
    "dumbbellchart": (_dumbbell_units, None),
    "histogram": (_series_units("x"), "mean"),
    "contourchart": (_series_units("z"), "mean"),
}


def apply_emphasis_rule(chart_type: str, charts: List[dict], settings: dict) -> list:
    """The charts with the rule's role written on each unit that set none.

    The rule reads every unit of the charts as one pool, so a count picks
    units across the series and subplots; an explicit role wins.
    """

    units_of, by = EMPHASIS_RULE_UNITS[chart_type]
    rule = validate_emphasis_rule(settings.get("emphasis_rule"), by)
    if rule is None:
        return charts
    if chart_type == "bumpchart":
        # a bump chart reads ranks, best when lowest: `top` picks them (ADR 0046)
        rule = ({"top": "bottom", "bottom": "top"}.get(rule[0], rule[0]),) + rule[1:]
    charts, units = units_of(charts, settings, rule[2])
    roles = emphasis_rule_roles(rule, [value for value, _ in units])
    for (_, fill), role in zip(units, roles):
        fill(role)
    return charts


# the fronts whose records carry a value per category and sort by it
BAR_RECORD_CHARTS = ("barchart", "pyramidchart")


def build_layers(chart_type: str, charts: List[dict], settings: dict) -> List[Layer]:
    """Build the layers for a chart front; style resolution happens here."""

    visual = settings.get("radial_type") or RADIAL_TYPE.LINE
    bar_records = chart_type in BAR_RECORD_CHARTS or (
        chart_type == "radialchart" and visual == RADIAL_TYPE.BAR
    )
    if chart_type == "bumpchart":
        # the rule reads the ranks, so they come first
        charts = rank_bump_charts(charts, settings)
    if chart_type in EMPHASIS_RULE_UNITS and (
        chart_type != "radialchart" or bar_records
    ):
        # the rule breaks ties on input order, so it runs before the sort
        charts = apply_emphasis_rule(chart_type, charts, settings)
    if chart_type == "ganttchart":
        charts = sort_gantt_charts(charts, settings)
    if chart_type == "dumbbellchart":
        charts = sort_dumbbell_charts(charts, settings)
    if bar_records:
        charts = _sort_bar_charts(
            charts,
            validate_sort(settings.get("sort")),
            settings.get("sort_by"),
            bool(settings.get("pyramid")),
        )

    if chart_type == "parallelcoords":
        return [ParallelCoordsLayer(list(charts), settings)]

    if chart_type == "radialchart":
        if visual not in RADIAL_LAYER_TYPES:
            raise ValueError(
                f"Invalid radial `type` value {visual!r}. "
                f"Must be one of {sorted(RADIAL_LAYER_TYPES)}."
            )
        layer_cls = RADIAL_LAYER_TYPES[visual]
        return [layer_cls(chart, settings) for chart in charts]

    if chart_type == "raincloudplot":
        return [
            layer
            for chart in charts
            for layer in build_raincloud_layers(chart, settings)
        ]

    layer_cls = LAYER_TYPES[chart_type]
    layers = [layer_cls(chart, settings) for chart in charts]

    if chart_type == "ridgelineplot" and len(layers) > 1:
        # one grid range for every subplot, like the histogram's shared bins
        ranges = [r for r in (layer.padded_range() for layer in layers) if r]
        if ranges:
            shared = (min(r[0] for r in ranges), max(r[1] for r in ranges))
            for layer in layers:
                layer.shared_range = shared

    if (
        chart_type == "linechart"
        and settings.get("show_yerr")
        and settings.get("show_area")
    ):
        warnings.warn(
            "Both the `show_yerr` and `show_area` will be used. "
            + "Only one of them should be True."
        )
    return layers


def build_raincloud_layers(chart: dict, settings: dict) -> List[Layer]:
    """The cloud, rain, and box of one raincloud dataset (ADR 0021).

    The box is centered on the category position; the cloud keeps the high
    side past it (right when vertical, above when horizontal) and the rain
    falls on the low side.
    """

    cloud = ViolinLayer(
        chart,
        {
            **settings,
            # the box prints the median and the rain the extremes (ADR 0033)
            "show_values": False,
            "inner": None,
            "split": None,
            "side": 1,
            "offset": RAINCLOUD_CLOUD_OFFSET,
            "width": RAINCLOUD_CLOUD_WIDTH,
            "color_by_group": True,
        },
    )
    rain = SwarmLayer(
        chart,
        {
            **settings,
            "label_median": False,
            "offset": -RAINCLOUD_RAIN_OFFSET,
            "spread": RAINCLOUD_RAIN_SPREAD,
            "side": -1,
            "size": RAINCLOUD_RAIN_SIZE,
            "color_by_group": True,
        },
    )
    box = BoxLayer(
        chart,
        {
            **settings,
            "show_notch": None,
            "width": RAINCLOUD_BOX_WIDTH,
            "outline": True,
            "color_by_group": True,
            # the box reads over the rain
            "zorder": (rain.swarm_style.get("zorder") or 2) + 1,
        },
    )
    return [cloud, rain, box]


def layers_per_chart(layers: List[Layer]) -> List[List[Layer]]:
    """Group the layers by their source chart, in order; one list per dataset."""

    grouped = {}
    for layer in layers:
        grouped.setdefault(id(layer.chart), []).append(layer)
    return list(grouped.values())


# ================================================
# Layer Groups
# ================================================


class LayerGroup:
    """Layers from one source chart, plus the panel-level preferences for them."""

    def __init__(
        self,
        layers: List[Layer],
        *,
        palette: Union[str, List[str], None] = None,
        max_colors: Optional[int] = None,
        num_bins: Optional[int] = None,
        y_axis: str = "auto",
        z_order: Optional[float] = None,
        legend_label: Optional[str] = None,
        emphasis: Optional[str] = None,
        value_scale: Optional[str] = None,
        category_scale: Optional[str] = None,
    ):
        self.layers = layers
        self.palette = (
            palette if palette is not None else config["color_general_multiple"]
        )
        self.max_colors = max_colors if max_colors is not None else max(len(layers), 1)
        self.num_bins = num_bins or DEFAULT_NUM_BINS
        self.y_axis = y_axis
        self.z_order = z_order
        self.legend_label = legend_label
        self.emphasis = validate_emphasis(emphasis)
        # the source figure's scales, by role: they follow the group (ADR 0041)
        self.value_scale = value_scale
        self.category_scale = category_scale

    def with_prefs(
        self,
        *,
        y_axis,
        z_order,
        legend_label,
        emphasis=None,
        value_scale=None,
        category_scale=None,
    ) -> "LayerGroup":
        return LayerGroup(
            self.layers,
            palette=self.palette,
            max_colors=self.max_colors,
            num_bins=self.num_bins,
            y_axis=y_axis if y_axis is not None else self.y_axis,
            z_order=z_order if z_order is not None else self.z_order,
            legend_label=(
                legend_label if legend_label is not None else self.legend_label
            ),
            emphasis=emphasis if emphasis is not None else self.emphasis,
            value_scale=value_scale if value_scale is not None else self.value_scale,
            category_scale=(
                category_scale if category_scale is not None else self.category_scale
            ),
        )

    def layer_role(self, layer: Layer) -> Optional[str]:
        """The layer's effective emphasis role; the group's pref wins."""

        if self.emphasis is not None:
            return self.emphasis
        return layer.emphasis if isinstance(layer.emphasis, str) else None

    def data_range(self) -> tuple:
        """The combined y-range of the group's layers, for axis clustering."""

        lo, hi = [], []
        for layer in self.layers:
            rng = layer.y_range()
            if rng is not None:
                lo.append(rng[0])
                hi.append(rng[1])
        if not lo:
            return (0, 1)
        return (min(lo), max(hi))

    def hist_bins(self) -> Optional[np.ndarray]:
        """Shared bin edges across the group's histogram layers."""

        xall = [
            layer.x_values()
            for layer in self.layers
            if isinstance(layer, HistogramLayer)
        ]
        xall = [x for x in xall if x is not None]
        if not xall:
            return None
        return np.histogram(np.hstack(tuple(xall)), bins=self.num_bins)[1]


def group_from_chart(
    layers: List[Layer], settings: dict, mode: str = "multiple"
) -> LayerGroup:
    """Build a chart front's layer group; palettes are resolved here."""

    if mode == "singular":
        palette, max_colors = config["color_general_singular"], 1
    else:
        # one color per dataset: a raincloud's three layers share one chart
        n_charts = len(layers_per_chart(layers))
        palette, max_colors = config["color_general_multiple"], max(n_charts, 1)

    return LayerGroup(
        layers,
        palette=palette,
        max_colors=max_colors,
        num_bins=settings.get("num_bins"),
    )


def _hist_stack_slots(hist_layers: List[HistogramLayer], bins: np.ndarray) -> dict:
    """Per-layer stacked heights and bottoms on shared bin edges.

    Mirrors matplotlib's stacked-hist math: density normalizes the whole
    stack's area to 1, cumulative accumulates after the density transform.
    """

    first = hist_layers[0]
    density = bool(first.show_density)
    cumulative = bool(first.show_cumulative)
    counts = [
        np.histogram(layer.x_values(), bins=bins)[0].astype(float)
        for layer in hist_layers
    ]
    db = np.diff(bins)
    total = sum(c.sum() for c in counts)

    slots, bottom = {}, np.zeros(len(db))
    for layer, heights in zip(hist_layers, counts):
        if density and total > 0:
            heights = heights / db / total
        if cumulative:
            heights = np.cumsum(heights * db) if density else np.cumsum(heights)
        slots[id(layer)] = HistSlot(bins=bins, heights=heights, bottom=bottom)
        bottom = bottom + heights
    return slots


# ================================================
# Axis Assignment (scale clustering)
# ================================================


def _scale_compatible(range1: tuple, range2: tuple, threshold: float = 3.0) -> bool:
    """Check whether two data ranges have similar spans."""

    span1 = range1[1] - range1[0]
    span2 = range2[1] - range2[0]
    if span1 == 0 or span2 == 0:
        return True
    return max(span1, span2) / min(span1, span2) < threshold


def _cluster_by_scale_compatibility(
    ranges: List[tuple], threshold: float
) -> List[List[int]]:
    """Group mutually scale-compatible chart indices."""

    n = len(ranges)
    if n == 0:
        return []
    if n == 1:
        return [[0]]

    compatible = [[False] * n for _ in range(n)]
    for i in range(n):
        compatible[i][i] = True
        for j in range(i + 1, n):
            if _scale_compatible(ranges[i], ranges[j], threshold):
                compatible[i][j] = True
                compatible[j][i] = True

    groups = []
    assigned = [False] * n
    for i in range(n):
        if assigned[i]:
            continue
        group = [i]
        assigned[i] = True
        for j in range(i + 1, n):
            if not assigned[j] and all(compatible[j][k] for k in group):
                group.append(j)
                assigned[j] = True
        groups.append(group)
    return groups


def determine_axis_assignment(
    groups: List[LayerGroup], threshold: float, warn_scale_groups: bool = True
) -> List[str]:
    """Assign each layer group to the primary (left) or secondary (right) value axis."""

    n = len(groups)
    if n == 0:
        return []

    ranges = [g.data_range() for g in groups]
    prefs = [g.y_axis for g in groups]
    all_auto = all(p == "auto" for p in prefs)

    if all_auto and warn_scale_groups:
        clusters = _cluster_by_scale_compatibility(ranges, threshold)
        sorted_clusters = sorted(clusters, key=len, reverse=True)

        assignments = ["left"] * n
        if len(sorted_clusters) > 1:
            for idx in sorted_clusters[1]:
                assignments[idx] = "right"

        if len(sorted_clusters) > 2:
            warnings.warn(
                f"Found {len(sorted_clusters)} scale-incompatible groups but only 2 axes available. "
                f"Groups: {[len(g) for g in sorted_clusters]}. "
                "Some charts may be difficult to read. Consider using explicit y_axis assignment or Grid."
            )
        return assignments

    assignments = []
    for i, pref in enumerate(prefs):
        if pref in ["left", "right"]:
            assignments.append(pref)
        elif i == 0:
            assignments.append("left")
        else:
            left_compatible = any(
                assignments[j] == "left"
                and _scale_compatible(ranges[i], ranges[j], threshold)
                for j in range(i)
            )
            assignments.append("left" if left_compatible else "right")

    # an explicitly assigned pair is the user's call: warn on auto placements only
    for side in ("right", "left"):
        side_idx = [i for i, a in enumerate(assignments) if a == side]
        found = False
        for i in range(len(side_idx)):
            for j in range(i + 1, len(side_idx)):
                a, b = side_idx[i], side_idx[j]
                if prefs[a] != "auto" and prefs[b] != "auto":
                    continue
                if not _scale_compatible(ranges[a], ranges[b], threshold):
                    warnings.warn(
                        f"Charts at indices {a} and {b} are both on the {side} axis but have "
                        "incompatible scales. Consider using explicit y_axis assignment or Grid."
                    )
                    found = True
                    break
            if found:
                break

    return assignments


# ================================================
# Panel
# ================================================


class ScaledAxis(NamedTuple):
    """One panel axis as the log-scale check sees it."""

    key: str  # the literal settings key
    parameter: str  # the key as the user typed it
    role: str
    scale: Optional[str]
    twin: Optional[bool]  # the side whose groups it holds; None for both
    remedy: str  # the fix for a figure that only inherited the scale


def _style_assignments(entries: Optional[list]) -> Optional[defaultdict]:
    """Chart hash -> the next cycle entry, first come first served; None without."""

    if not entries:
        return None
    entry_iter = iter_cycle(entries)
    return defaultdict(lambda: next(entry_iter))


def _marker_entry(entry) -> tuple:
    """A marker cycle entry as `(marker, hollow)`."""

    if isinstance(entry, dict):
        return entry["marker"], bool(entry.get("hollow"))
    return entry, False


def _takes_hatch(layer: Layer) -> bool:
    """Whether the panel's hatch cycle reaches the layer's fills.

    Areas take it only when etched: a tiled hatch on a translucent area
    reads poorly (ADR 0048).
    """

    if isinstance(
        layer, (BarLayer, HistogramLayer, RadialBarLayer, RadialHistogramLayer)
    ):
        return True
    areas = (LineLayer, StackedAreaLayer, RadialLineLayer)
    return (
        isinstance(layer, areas)
        and not isinstance(layer, BumpLayer)
        and layer.etch is not None
    )


class Panel:
    """A group of layers sharing one coordinate space; owns all cross-layer concerns."""

    def __init__(self, groups: List[LayerGroup], settings: Optional[dict] = None):
        self.groups = groups
        self.settings = settings or {}
        # the axis kind is snapshotted at build, like the furniture (ADR 0037)
        self.x_kind = validate_axis_kinds([l.x_kind() for l in self.layers])
        self.value_kind = validate_axis_kinds(
            [l.value_kind() for l in self.layers], "value-axis"
        )
        self.temporal_axis = self._temporal_axis()
        self.date_axes = self._date_axes()
        for axis in ("x", "y"):
            validate_ticks_format(
                self.settings.get(f"{axis}ticks_format"), axis, axis in self.date_axes
            )

    @property
    def layers(self) -> List[Layer]:
        return [layer for group in self.groups for layer in group.layers]

    def _temporal_axis(self) -> Optional[str]:
        """The drawn axis ("x" or "y") that holds time; None when neither does."""

        if self.x_kind == AXIS_TEMPORAL:
            return "y" if self.horizontal else "x"
        if self.value_kind == AXIS_TEMPORAL:
            return "x" if self.horizontal else "y"
        return None

    def _date_axes(self) -> set:
        """The drawn axes whose ticks read as dates, by position or by label."""

        axes = set().union(*(l.date_label_axes() for l in self.layers))
        if self.temporal_axis is not None:
            axes.add(self.temporal_axis)
        return axes

    @property
    def horizontal(self) -> bool:
        """Whether the panel's value axis is x: true iff every orientable layer is.

        Raises:
            ValueError: If orientable layers of both orientations share the panel.
        """

        flags = {l.is_horizontal for l in self.layers if l.is_horizontal is not None}
        if len(flags) > 1:
            raise ValueError(
                "Cannot mix horizontal and vertical charts in one panel. "
                "One coordinate space holds one orientation; use `Grid` instead."
            )
        return flags == {True}

    @property
    def bare(self) -> bool:
        """Whether the layers own their axes: no furniture, scales, or limits."""

        layers = self.layers
        return bool(layers) and all(l.bare for l in layers)

    @property
    def projection(self) -> str:
        """The panel's coordinate space kind: "cartesian" or "polar".

        Raises:
            ValueError: If layers of both projections share the panel.
        """

        # text carrier layers have no projection; they follow the panel
        kinds = {l.projection for l in self.layers if l.projection is not None}
        if len(kinds) > 1:
            raise ValueError(
                "Cannot mix polar and cartesian charts in one panel. "
                "One coordinate space holds one projection; use `Grid` instead."
            )
        return "polar" if kinds == {"polar"} else "cartesian"

    # ---------------- furniture ----------------

    @staticmethod
    def snapshot_label_styles() -> dict:
        """Capture label text styles from the config at build time.

        Cell titles read as per-cell headings, hence the subtitle style.
        """

        return {
            "title": get_text_style("subtitle"),
            "xlabel": get_text_style("xlabel"),
            "ylabel": get_text_style("ylabel"),
        }

    @staticmethod
    def snapshot_hover_style() -> dict:
        """Capture the hover annotation look from the config at render time.

        The popup wears the theme's text annotation style (ADR 0018): the
        `plot_text_*` font, box, and connector color. Placement, and so the
        alignment, stays with the cursor; the connector is straight because
        the popup sits a few points from its mark.
        """

        text = get_plot_text_style({})
        text.pop("ha", None)
        text.pop("va", None)
        arrow = get_plot_text_arrow_style({})
        return {
            **text,
            "bbox": get_plot_text_box_style({}),
            "arrowprops": {
                "arrowstyle": arrow["arrowstyle"],
                "connectionstyle": "arc3",
                "color": arrow["color"],
                "linewidth": arrow["linewidth"],
                "shrinkB": 0,
            },
        }

    @staticmethod
    def snapshot_furniture() -> dict:
        """Capture spine/tick styling from the config at build time."""

        return {
            "spines": {
                axis: {
                    "linewidth": config["axes_spines_width"],
                    "visible": config[f"axes_spines_{axis}_visible"],
                    "zorder": config["axes_spines_zorder"],
                }
                for axis in ["top", "bottom", "left", "right"]
            },
            "ticks": {
                "width": config["axes_spines_width"],
                "length": config["axes_ticks_length"],
                "labelsize": config["axes_ticks_label_size"],
                "labelcolor": config["font_general_color"],
            },
            # ground and furniture colors (ADR 0048); None keeps matplotlib's
            "colors": {
                "figure": config.get("figure_facecolor"),
                "axes": config.get("axes_facecolor"),
                "spines": config.get("axes_spines_color"),
                "ticks": config.get("axes_ticks_color"),
            },
            # tick_params cannot set a font family; applied to the labels directly
            "font_family": resolve_font_family(),
            # the render-scoped rc attribute (ADR 0027); None means off
            "sketch_params": config.get("plot_sketch_params"),
        }

    def _text_halo(self) -> list:
        """The halo stroking polar texts, in the axes ground color."""

        colors = (self.settings.get("furniture") or {}).get("colors") or {}
        return _halo_effects(config.get("plot_value_halo_width"), colors.get("axes"))

    def _sketch_rc(self) -> dict:
        """The rc override for the path wobble, empty when it is off."""

        furniture = self.settings.get("furniture") or {}
        if furniture.get("sketch_params") is None:
            return {}
        return {"path.sketch": tuple(furniture["sketch_params"])}

    def _apply_furniture(
        self, ax: plt.Axes, axes_types=("xaxis", "yaxis"), spines=True
    ) -> None:
        furniture = self.settings.get("furniture")
        if furniture is None:
            return
        colors = furniture.get("colors") or {}
        if colors.get("figure") is not None:
            ax.figure.set_facecolor(colors["figure"])
        if colors.get("axes") is not None:
            ax.set_facecolor(colors["axes"])
        if self.bare:
            return
        if spines:
            ax.axis("on")
            if ax.name == "polar":
                # a polar axes has no top/bottom/left/right; every polar spine
                # ('polar', 'start', 'end', 'inner') wears the category-axis style
                for spine in ax.spines.values():
                    spine.set(**furniture["spines"]["bottom"])
            else:
                for axis, spine_style in furniture["spines"].items():
                    ax.spines[axis].set(**spine_style)
            # the spines predate the render, so the rc context never saw them
            sketch = self._sketch_rc().get("path.sketch")
            for spine in ax.spines.values():
                if sketch is not None:
                    spine.set_sketch_params(*sketch)
                if colors.get("spines") is not None:
                    spine.set_edgecolor(colors["spines"])
        ticks = dict(furniture["ticks"])
        if colors.get("ticks") is not None:
            ticks["color"] = colors["ticks"]
        for axis_type in axes_types:
            getattr(ax, axis_type).set_tick_params(which="major", **ticks)

    # ---------------- rendering ----------------

    def render(self, ax: plt.Axes) -> None:
        # an axes drawn earlier fixed the limits this one shares; autoscale
        # again, over the data of every axes that shares them
        for axis_name in ("x", "y"):
            if len(ax._shared_axes[axis_name].get_siblings(ax)) > 1:
                getattr(ax, f"set_autoscale{axis_name}_on")(True)
        # every artist created here copies the wobble from the rc context at
        # construction (ADR 0027); nothing global changes
        with rc_context(self._sketch_rc()):
            self._render(ax)

    def _render(self, ax: plt.Axes) -> None:
        s = self.settings

        # one dataset per kind: a violin and a box may share the positions
        for kind, name in (
            ("box", "box plot"),
            ("violin", "violin plot"),
            ("ridge", "ridgeline plot"),
        ):
            validate_single_dataset([l for l in self.layers if l.kind == kind], name)

        horizontal = self.horizontal
        polar = self.projection == "polar"
        self._apply_furniture(ax)

        # a locked aspect shrinks the axes box; colorbars must follow the box
        aspect_locked = (
            s.get("aspect_ratio") not in (None, ASPECT_RATIO.AUTO) and not polar
        )

        # twin-axis assignment: the secondary axis is always a value axis;
        # a polar panel has one value axis, so twins never apply
        assignments = ["left"] * len(self.groups)
        ax_right = None
        if s.get("twin_axes") and not polar:
            # text carrier groups hold no data: they stay on the primary axis
            # and never enter the scale clustering
            data_indices = [
                i
                for i, group in enumerate(self.groups)
                if any(l.kind != "text" for l in group.layers)
            ]
            data_assignments = determine_axis_assignment(
                [self.groups[i] for i in data_indices],
                s.get("auto_threshold", 3.0),
                s.get("warn_scale_groups", True),
            )
            for i, assignment in zip(data_indices, data_assignments):
                assignments[i] = assignment
            if "right" in assignments:
                ax_right = ax.twiny() if horizontal else ax.twinx()
                self._apply_furniture(
                    ax_right,
                    axes_types=("xaxis",) if horizontal else ("yaxis",),
                    spines=False,
                )

        # the host axis keeps a shared scale; the marks draw on a hidden twin
        # with their own (a scatter matrix diagonal, ADR 0051)
        if s.get("marks_on_twin") and not polar and ax_right is None:
            ax_right = ax.twinx()
            ax_right.axis("off")
            assignments = [
                "right" if any(l.kind != "text" for l in group.layers) else "left"
                for group in self.groups
            ]

        # bar slotting across every layer in the panel; radial bars share the
        # machinery — their slots are sector fractions, scaled at draw time
        bar_layers = [
            l for l in self.layers if isinstance(l, (BarLayer, RadialBarLayer))
        ]
        bar_mode = s.get("bar_mode") or "group"
        if bar_mode not in ["group", "stack", "overlay"]:
            warnings.warn(
                f"Invalid bar_mode '{bar_mode}'. Using 'group' instead. "
                "Valid options are: 'group', 'stack', 'overlay'."
            )
            bar_mode = "group"

        bar_slots = {}
        # the group spans the widest layer; each layer keeps its own
        # plot_bar_width inside its slot
        bar_width = max((l.bar_width for l in bar_layers), default=0.0)
        slot_width = bar_width / len(bar_layers) if bar_layers else bar_width
        if bar_layers and s.get("bar_slotting", True):
            if bar_mode == "group":
                if (
                    s.get("warn_thin_bars")
                    and len(bar_layers) > 1
                    and slot_width < 0.15
                ):
                    warnings.warn(
                        f"Bar width ({slot_width:.2f}) is very small with {len(bar_layers)} bar charts. "
                        "Consider using bar_mode='stack', bar_mode='overlay', or Grid for better readability."
                    )
                # the group centers on the category position, so numeric-x
                # layers and ticks line up with group centers
                for idx, layer in enumerate(bar_layers):
                    bar_slots[id(layer)] = BarSlot(
                        offset=(idx - (len(bar_layers) - 1) / 2) * slot_width,
                        width=layer.bar_width / len(bar_layers),
                    )
            elif bar_mode == "stack":
                bottoms = None
                first_labels = bar_layers[0].labels()
                if first_labels is not None:
                    bottoms = np.zeros(len(first_labels))
                for idx, layer in enumerate(bar_layers):
                    bar_slots[id(layer)] = BarSlot(
                        offset=0.0,
                        width=layer.bar_width,
                        bottom=None if bottoms is None else bottoms.copy(),
                        show_yerr=idx == len(bar_layers) - 1,
                    )
                    y = layer.y_values()
                    if bottoms is not None and y is not None:
                        bottoms = bottoms + np.array(y)
            else:  # overlay
                for layer in bar_layers:
                    bar_slots[id(layer)] = BarSlot(offset=0.0, width=layer.bar_width)

        bar_alpha = None
        # pyramid sides never truly overlap, so overlay slots keep full alpha
        if bar_mode == "overlay" and len(bar_layers) > 1 and not s.get("pyramid"):
            bar_alpha = s.get("bar_overlay_alpha")

        # bar_mode drives histograms too: "stack" stacks on shared bins,
        # "overlay"/"group" draw each series individually (ADR 0014)
        hist_pairs = [
            (group, l)
            for group in self.groups
            for l in group.layers
            if isinstance(l, HistogramLayer) and l.x_values() is not None
        ]
        hist_alpha = None
        if bar_mode != "stack" and len(hist_pairs) > 1:
            hist_alpha = s.get("hist_overlay_alpha")

        # stacking a muted background is meaningless: draw individually
        hist_slots = {}
        if (
            bar_mode == "stack"
            and len(hist_pairs) > 1
            and all(group.layer_role(l) is None for group, l in hist_pairs)
        ):
            stack_bins = s.get("hist_bins_override")
            if stack_bins is None:
                # panel-shared edges, pooled across every stacked layer
                stack_bins = np.histogram(
                    np.hstack(tuple(l.x_values() for _, l in hist_pairs)),
                    bins=hist_pairs[0][0].num_bins,
                )[1]
            hist_slots = _hist_stack_slots([l for _, l in hist_pairs], stack_bins)

        # stacked areas always stack; the baseline is a panel setting (ADR 0025)
        stack_layers = [l for l in self.layers if isinstance(l, StackedAreaLayer)]
        stack_slots = {}
        if stack_layers:
            stack_slots = _stack_slots(
                stack_layers, validate_baseline(s.get("baseline"))
            )

        zorder_defaults = s.get("zorder_defaults", {})

        # group layers share one category axis (ADR 0020)
        group_layers = [l for l in self.layers if isinstance(l, GroupLayer)]
        category_index = self.category_index(group_layers)
        dumbbell_count = sum(isinstance(l, DumbbellLayer) for l in group_layers)

        # hatch, line-style and marker cycles: per series, parallel to the
        # color cycle (ADR 0004, ADR 0048)
        hatch_assignments = _style_assignments(s.get("hatch_cycle"))
        # a theme file stores a dash tuple as a list; matplotlib wants the tuple
        linestyle_assignments = _style_assignments(
            [
                tuple(entry) if isinstance(entry, list) else entry
                for entry in s.get("linestyle_cycle") or []
            ]
        )
        marker_assignments = _style_assignments(
            [_marker_entry(entry) for entry in s.get("marker_cycle") or []]
        )

        # draw the layers group by group, in order
        # one color cycle per palette, pooled across the panel's groups, so
        # composed single-series figures draw in distinct colors
        def palette_key(group):
            return (
                tuple(group.palette)
                if isinstance(group.palette, list)
                else group.palette
            )

        # background layers do not consume a color-cycle slot
        pooled_colors = defaultdict(int)
        for group in self.groups:
            n_background = sum(
                1
                for l in group.layers
                if l.draws_all_muted(group.layer_role(l), group.emphasis)
            )
            pooled_colors[palette_key(group)] += max(group.max_colors - n_background, 0)
        cycles = {}
        for group in self.groups:
            key = palette_key(group)
            if key not in cycles:
                cycles[key] = create_color_cycle(
                    group.palette, max(pooled_colors[key], 1)
                )

        # panel-owned parallel normalization (ADR 0009); furniture draws once
        parallel_layers = [l for l in self.layers if isinstance(l, ParallelCoordsLayer)]
        parallel_stats = compute_parallel_stats(parallel_layers)
        parallel_axes_owner = parallel_layers[-1] if parallel_layers else None

        # hover targets ride on the figure drawn into, not on the layers a
        # source figure shares with every composition of it (ADR 0031)
        figure = ax.figure
        if getattr(figure, "_hover_targets", None) is None:
            figure._hover_targets = []
            figure._hover_style = self.snapshot_hover_style()
        hover_targets = figure._hover_targets
        group_axes = [ax_right if a == "right" else ax for a in assignments]
        size_extents = _size_extents(
            (layer, target_ax)
            for group, target_ax in zip(self.groups, group_axes)
            for layer in group.layers
        )
        # scales resolve before drawing: a log axis rejects its data up front
        scales = self._resolve_scales(ax_right, group_axes)
        self._validate_log_scales(scales, group_axes, ax_right)
        scalex, scaley, scale_right = scales
        # user limits name the host axes, so only host marks are hidden past them
        limit_marks = []
        for group, target_ax in zip(self.groups, group_axes):
            cycle = cycles[palette_key(group)]
            on_twin = ax_right is not None and target_ax is ax_right
            value_scale = scale_right if on_twin else (scalex if horizontal else scaley)
            category_scale = scaley if horizontal else scalex
            bins = s.get("hist_bins_override")
            if bins is None:
                bins = group.hist_bins()

            for layer in group.layers:
                z_order = group.z_order
                if z_order is None:
                    z_order = zorder_defaults.get(
                        "surface" if layer.surface else layer.kind
                    )

                role = group.layer_role(layer)
                muted = layer.draws_all_muted(role, group.emphasis)

                ctx = DrawContext(
                    # a text carrier lookup would advance the pooled cycle
                    # and shift the colors of later composed figures
                    color=(
                        None
                        if muted or layer.kind == "text"
                        else cycle[layer.chart_hash]["color"]
                    ),
                    z_order=z_order,
                    legend_label=NO_LEGEND if muted else group.legend_label,
                    alpha=(
                        bar_alpha
                        if isinstance(layer, (BarLayer, RadialBarLayer))
                        else (
                            hist_alpha
                            if isinstance(layer, (HistogramLayer, RadialHistogramLayer))
                            else None
                        )
                    ),
                    bar_slot=bar_slots.get(id(layer)),
                    hist_slot=hist_slots.get(id(layer)),
                    stack_slot=stack_slots.get(id(layer)),
                    bins=bins,
                    hatch=(
                        hatch_assignments[layer.chart_hash]
                        if hatch_assignments is not None and _takes_hatch(layer)
                        else None
                    ),
                    linestyle=(
                        linestyle_assignments[layer.chart_hash]
                        if linestyle_assignments is not None
                        and isinstance(layer, (LineLayer, RadialLineLayer))
                        else None
                    ),
                    marker=(
                        marker_assignments[layer.chart_hash]
                        if marker_assignments is not None
                        and isinstance(layer, (ScatterLayer, RadialScatterLayer))
                        else None
                    ),
                    emphasis=role,
                    panel_emphasis=group.emphasis,
                    parallel_stats=parallel_stats,
                    parallel_axes=layer is parallel_axes_owner,
                    transpose=horizontal and layer.is_horizontal is None,
                    category_index=category_index,
                    sole_dumbbell=dumbbell_count == 1,
                    aspect_locked=aspect_locked,
                    value_scale=value_scale,
                    category_scale=category_scale,
                    size_extent=size_extents.get(target_ax),
                )
                layer.draw(target_ax, ctx)
                hover_targets.extend(layer.take_hover_targets())
                marks = layer.take_limit_marks()
                if target_ax is ax:
                    limit_marks.extend(marks)

        if category_index:
            self._apply_category_ticks(ax, category_index, group_layers, horizontal)

        self._finalize(
            ax, ax_right, bar_layers, horizontal, scales, group_axes, limit_marks
        )

    @staticmethod
    def category_index(layers: List[Layer]) -> Optional[dict]:
        """Label -> position (0..n-1), the first-seen union across group layers."""

        index = {}
        for layer in layers:
            if isinstance(layer, GroupLayer):
                for label in layer.labels():
                    index.setdefault(label, len(index))
        return index or None

    def _category_labels(self, labels, axis: str) -> list:
        """Category labels as tick text; dates print through the axis' format."""

        labels = list(labels)
        if axis_kind(labels) != AXIS_TEMPORAL:
            return labels
        return date_labels(labels, self.settings.get(f"{axis}ticks_format"))

    def _apply_category_ticks(self, ax, index, group_layers, horizontal) -> None:
        # the first group layer's rotation applies; user ticks override later
        chart = group_layers[0].chart
        labels = self._category_labels(index.keys(), "y" if horizontal else "x")
        if horizontal:
            ax.set_yticks(list(index.values()))
            ax.set_yticklabels(labels, rotation=chart.get("ytickrotate", 0))
        else:
            ax.set_xticks(list(index.values()))
            ax.set_xticklabels(labels, rotation=chart.get("xtickrotate", 0))

    def _resolve_scales(self, ax_right, group_axes) -> tuple:
        """The literal x, y and twin value-axis scales (ADR 0041).

        Per axis, an explicit setting wins; otherwise the first group on that
        axis supplies its stamped scale, and a group built on another one
        warns. A group that set no scale was built linear.
        """

        s = self.settings
        horizontal = self.horizontal
        polar = self.projection == "polar"
        warn = s.get("warn_scale_conflict", True)
        if group_axes is None:
            group_axes = [None] * len(self.groups)
        # text carrier groups hold no data: they were built on no scale at all
        groups = [
            (group, ax_right is not None and axes is ax_right)
            for group, axes in zip(self.groups, group_axes)
            if any(l.kind != "text" for l in group.layers)
        ]

        def pick(explicit, stamps, message):
            if explicit:
                return explicit
            if not stamps:
                return None
            built = [scale or SCALE.LINEAR for scale in stamps]
            losers = sorted(set(built[1:]) - {built[0]})
            if losers and warn:
                warnings.warn(message(built[0], losers))
            return stamps[0]

        def value_conflict(winner, losers):
            return (
                f"Figures sharing one value axis were built with different "
                f"scales: '{winner}' (first in panel order) wins over "
                f"{losers}. Give each scale its own axis with the per-figure "
                '"y_axis" option and `scaley_right`, or set `scaley` '
                "explicitly."
            )

        def category_conflict(winner, losers):
            return (
                f"Figures were built with different category-axis scales: "
                f"'{winner}' (first in panel order) wins over {losers}. Set "
                "`scalex` explicitly to choose one."
            )

        category = pick(
            s.get("scaley" if horizontal else "scalex"),
            [g.category_scale for g, _ in groups],
            category_conflict,
        )
        value = pick(
            s.get("scalex" if horizontal else "scaley"),
            [g.value_scale for g, twin in groups if not twin],
            value_conflict,
        )
        if ax_right is None:
            # a polar panel has no twin, so the secondary scale is inert there
            if s.get("scaley_right") and warn and not polar:
                warnings.warn(
                    "`scaley_right` is set but the panel has no secondary value "
                    "axis: every figure landed on the primary axis. Assign a "
                    'figure with "y_axis": "right" to create it.'
                )
            value_right = None
        else:
            value_right = pick(
                s.get("scaley_right"),
                [g.value_scale for g, twin in groups if twin],
                value_conflict,
            )
        if horizontal:
            return value, category, value_right
        return category, value, value_right

    def _validate_log_scales(self, scales, group_axes, ax_right) -> None:
        """Reject raw data a resolved log scale cannot show (issue #147).

        Each axis checks only the groups drawn on it. The error names the
        setting as the user typed it: role keys, except the literal ones
        horizontal bar and histogram fronts take.
        """

        if self.bare:
            return
        s = self.settings
        horizontal = self.horizontal
        literal = horizontal and s.get("literal_scale_keys")
        scalex, scaley, scale_right = scales
        axes = [
            ScaledAxis(
                key="scalex" if horizontal else "scaley",
                parameter="scalex" if literal else "scaley",
                role="value",
                scale=scalex if horizontal else scaley,
                twin=False,
                remedy='Give it the secondary axis with "y_axis": "right" and '
                "`scaley_right`, or set `scaley` explicitly.",
            ),
            ScaledAxis(
                key="scaley_right",
                parameter="scaley_right",
                role="secondary value",
                scale=scale_right,
                twin=True,
                remedy='Move it to the primary axis with "y_axis": "left", or '
                "set `scaley_right` explicitly.",
            ),
        ]
        if self.projection != "polar":
            axes.append(
                ScaledAxis(
                    key="scaley" if horizontal else "scalex",
                    parameter="scaley" if literal else "scalex",
                    role="category",
                    scale=scaley if horizontal else scalex,
                    twin=None,
                    remedy="Set `scalex` explicitly to choose one.",
                )
            )

        for group, group_ax in zip(self.groups, group_axes):
            on_twin = ax_right is not None and group_ax is ax_right
            for axis in axes:
                if axis.scale != SCALE.LOG or axis.twin not in (None, on_twin):
                    continue
                category = axis.twin is None
                stamp = group.category_scale if category else group.value_scale
                hint = None
                if not s.get(axis.key) and stamp != SCALE.LOG:
                    hint = (
                        "The figure was built on another scale and inherited "
                        f"'log' from the first figure on this axis. {axis.remedy}"
                    )
                for layer in group.layers:
                    values = layer.category_data() if category else layer.value_data()
                    if axis_kind(values) == AXIS_NUMERIC:
                        validate_log_values(
                            axis.parameter, axis.role, axis.scale, values, hint
                        )

    def _apply_minor_value_grid(self, ax, horizontal: bool, value_scale) -> None:
        """Fainter gridlines between a dumbbell's labelled values (ADR 0050).

        Only on a gridded, linear value axis; the densest layer's split wins.
        """

        splits = max(
            (l.grid_minor for l in self.layers if isinstance(l, DumbbellLayer)),
            default=0,
        )
        name = "x" if horizontal else "y"
        if (
            splits < 2
            or self.settings["show_grid"] not in (name, "both")
            or value_scale not in (None, SCALE.LINEAR)
        ):
            return
        axis = ax.xaxis if horizontal else ax.yaxis
        axis.set_minor_locator(mticker.AutoMinorLocator(splits))
        ax.tick_params(axis=name, which="minor", length=0)
        style = dict(self.settings.get("grid_style", {}))
        style["alpha"] = style.get("alpha", 1.0) * MINOR_GRID_ALPHA_SCALE
        ax.grid(axis=name, which="minor", **style)

    def _finalize(
        self, ax, ax_right, bar_layers, horizontal, scales, group_axes, limit_marks
    ) -> None:
        """Apply the furniture; x/y keys are literal, `*_right` keys hit the twin."""

        s = self.settings
        layers = self.layers
        polar = self.projection == "polar"
        bare = self.bare

        # scales, per axis: an explicit setting beats the groups' stamps
        scalex, scaley, scale_right = scales
        value_scale = scalex if horizontal else scaley
        if layers and not bare and (scalex or scaley):
            layers[0].apply_scales(ax, scalex, scaley)
        if ax_right is not None and scale_right:
            (ax_right.set_xscale if horizontal else ax_right.set_yscale)(scale_right)

        # tick formats go first: explicit ticks and category labels override
        tick_labelers = {}
        if not bare and not polar:
            tick_labelers = self._apply_tick_formats(ax)

        # grid; the marks sit above it whatever z-order the panel gave them
        # (overlay defaults start at 1, below matplotlib's 2.5 gridlines)
        if s.get("show_grid") and not bare:
            ax.grid(axis=s["show_grid"], **s.get("grid_style", {}))
            ax.set_axisbelow(True)
            self._apply_minor_value_grid(ax, horizontal, value_scale)
        if s.get("date_period") and self.temporal_axis and not bare:
            # period edges are the minor ticks; the labelled centres draw no line
            axis = getattr(ax, f"{self.temporal_axis}axis")
            axis.grid(False, which="major")
            axis.grid(True, which="minor", **s.get("grid_style", {}))
            ax.set_axisbelow(True)
        if polar:
            # the r-value labels are redrawn above the marks in
            # _apply_radial_furniture
            ax.set_axisbelow(True)

        # the axes pinned to the data below keep their ends: no tick snap,
        # no legend headroom
        pinned = set()
        # line charts pin the category-axis limits to the union of their data ranges
        if s.get("tighten_xlim"):
            ranges = [
                layer.x_range()
                for layer in layers
                if isinstance(layer, (LineLayer, StackedAreaLayer))
            ]
            ranges = [r for r in ranges if r is not None]
            if ranges:
                lo, hi = min(r[0] for r in ranges), max(r[1] for r in ranges)
                # subplots sharing this axis pin it to all of their data
                axis_name = "y" if horizontal else "x"
                siblings = ax._shared_axes[axis_name].get_siblings(ax)
                if len(siblings) > 1:
                    shared = _shared_data_interval(ax, axis_name)
                    lo, hi = min(lo, shared[0]), max(hi, shared[1])
                (ax.set_ylim if horizontal else ax.set_xlim)(lo, hi)
                pinned.add(axis_name)

        # the y-axis is a rank axis only when every data layer draws ranks;
        # beside other charts it follows the panel as usual (ADR 0046)
        data_layers = [l for l in layers if l.kind != "text"]
        rank_axis = bool(data_layers) and all(
            isinstance(l, BumpLayer) for l in data_layers
        )
        rank_ranges = [r for r in (l.y_range() for l in data_layers) if r is not None]
        rank_axis = rank_axis and bool(rank_ranges) and not bare and not polar
        if rank_axis:
            # the end labels name the lines, so the rank axis carries no
            # furniture; whole-rank ticks still place the grid lines
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.tick_params(axis="y", which="both", left=False, labelleft=False)
            for side in ("left", "bottom"):
                ax.spines[side].set_visible(False)
            ax.set_ylim(0.5, max(r[1] for r in rank_ranges) + 0.5)

        # bar category ticks
        bar_ticks = s.get("bar_ticks")
        if bar_ticks and bar_layers and not polar:
            self._apply_bar_ticks(ax, bar_ticks, bar_layers)

        # angular category ticks: labels sit evenly around the circle, unless
        # tip labels carry them at the marks instead
        if polar:
            label_sets = [
                l.labels()
                for l in layers
                if isinstance(l, RadialLayer) and l.is_categorical
            ]
            label_sets = [lbl for lbl in label_sets if lbl is not None and len(lbl)]
            if label_sets:
                # the widest layer supplies the labels when counts differ
                cat_labels = max(label_sets, key=len)
                ax.set_xticks(_radial_theta(len(cat_labels)))
                if s.get("show_tip_labels"):
                    ax.set_xticklabels([""] * len(cat_labels))
                else:
                    ax.set_xticklabels(cat_labels)

        # user-provided tick positions; on a date-labelled category axis a
        # position names its category, so the tick keeps that label
        if not bare:
            for axis_name in self.date_axes - {self.temporal_axis}:
                axis = getattr(ax, f"{axis_name}axis")
                # the strings, not the tick texts: a later layer's ticks reuse them
                texts = {
                    loc: label.get_text()
                    for loc, label in zip(
                        axis.get_majorticklocs(), axis.get_majorticklabels()
                    )
                }
                tick_labelers[f"{axis_name}axis"] = lambda ticks, texts=texts: [
                    texts.get(t, str(t)) for t in ticks
                ]
            for layer in layers:
                configure_axis_ticks_position(ax, layer.chart, tick_labelers)

        # value-label headroom: expand the value axis so bar labels stay
        # inside; diverging bars get padding on both ends
        if polar:
            # tip texts run along the spokes; give them radial room so they
            # stay inside the border circle
            extra = 0.0
            if s.get("show_values"):
                extra += VALUE_HEADROOM_VERTICAL
            if s.get("show_tip_labels"):
                extra += RADIAL_TIP_LABEL_HEADROOM
            if extra:
                lo, hi = ax.get_ylim()
                ax.set_ylim(lo, hi + (hi - lo) * extra)
        else:
            # band and median labels sit inside the marks and need no room
            value_layers = [l for l in layers if l.labels_past_mark and l.show_values]
            if value_layers:
                lo, hi = ax.get_xlim() if horizontal else ax.get_ylim()
                pad = (hi - lo) * (
                    VALUE_HEADROOM_HORIZONTAL if horizontal else VALUE_HEADROOM_VERTICAL
                )
                below = lo < 0 or any(l.labels_below_range for l in value_layers)
                lo = lo - pad if below else lo
                hi = hi + pad
                (ax.set_xlim if horizontal else ax.set_ylim)(lo, hi)

        # pyramid mirror furniture reads the value axis after the headroom pad
        if s.get("pyramid"):
            self._apply_pyramid_mirror(ax)

        # a stack from zero sits on the axis floor, like bars (ADR 0025);
        # a log value axis cannot reach zero, so it keeps its own floor
        if (
            any(isinstance(l, StackedAreaLayer) for l in layers)
            and validate_baseline(s.get("baseline"))
            in (STACKED_AREA_BASELINE.ZERO, STACKED_AREA_BASELINE.PERCENT)
            and value_scale != "log"
        ):
            (ax.set_xlim if horizontal else ax.set_ylim)(0, None)
        # a stack alone fills its frame: the value axis ends exactly where the
        # stack does (a percent stack at 100), with no margin above it
        if (
            layers
            and all(isinstance(l, StackedAreaLayer) for l in layers)
            and value_scale != "log"
        ):
            lo, hi = ax.dataLim.intervalx if horizontal else ax.dataLim.intervaly
            if np.isfinite([lo, hi]).all() and hi > lo:
                (ax.set_xlim if horizontal else ax.set_ylim)(lo, hi)
                pinned.add("x" if horizontal else "y")

        # axis limits; a bare layer fixed its own
        limits = {k: s.get(k) for k in ("xmin", "xmax", "ymin", "ymax")}
        if not bare:
            configure_axis_limits(ax, limits)
            _hide_marks_past_limits(ax, limits, limit_marks)
        # rank 1 sits at the top, inverted after any user limits apply
        if rank_axis and not ax.yaxis_inverted():
            ax.invert_yaxis()
        # the first ridge row reads at the top; overlaid groups follow (ADR 0047)
        ridges = any(isinstance(l, RidgelineLayer) for l in layers)
        # the first task or dumbbell row reads at the top too (ADR 0049, 0050)
        rows_down = any(isinstance(l, (GanttLayer, DumbbellLayer)) for l in layers)
        if (
            (ridges or rows_down)
            and horizontal
            and not bare
            and not ax.yaxis_inverted()
        ):
            ax.invert_yaxis()
        if ax_right is not None and (
            s.get("ymin_right") is not None or s.get("ymax_right") is not None
        ):
            (ax_right.set_xlim if horizontal else ax_right.set_ylim)(
                s.get("ymin_right"), s.get("ymax_right")
            )

        # bump periods are discrete: one tick per period, none between, when
        # the user gave no ticks and the periods are numbers or categories
        # (dates keep theirs)
        if (
            layers
            and all(isinstance(l, BumpLayer) for l in layers)
            and self.temporal_axis is None
            and all(l.chart.get("xticks") is None for l in layers)
        ):
            periods = np.concatenate(
                [_axis_numbers(ax, horizontal, l.x_values()) for l in layers]
            )
            (ax.yaxis if horizontal else ax.xaxis).set_major_locator(
                PeriodTicks(periods)
            )

        # a continuous axis starts and ends on a tick: each free end of the
        # view moves outward to the next tick (a polar theta axis excepted),
        # or stops on the tick the data itself sits on; an axis pinned to
        # the data ends on the data
        # the display axes whose ends sit on the data, per axes; a pinned
        # axis counts only while the user sets no limit on it
        ends_on_data = {ax: set()}
        for axis_name in pinned:
            if all(s.get(f"{axis_name}{end}") is None for end in ("min", "max")):
                ends_on_data[ax].add(axis_name)
        if not bare and all(l.ticks_at_axis_ends for l in layers):
            for axis_name in ("y",) if polar else ("x", "y"):
                # ranks are whole positions with their own half-unit ends
                if (rank_axis and axis_name == "y") or axis_name in pinned:
                    continue
                # a polar r axis keeps its ring past the data
                fixed = tuple(
                    s.get(f"{axis_name}{end}") is not None for end in ("min", "max")
                )
                on_data = _snap_limits_to_ticks(
                    ax, axis_name, fixed, data_ends=not polar
                )
                if on_data and not any(fixed):
                    ends_on_data[ax].add(axis_name)
            if ax_right is not None:
                value_axis = "x" if horizontal else "y"
                fixed = tuple(
                    s.get(f"y{end}_right") is not None for end in ("min", "max")
                )
                if _snap_limits_to_ticks(ax_right, value_axis, fixed) and not any(
                    fixed
                ):
                    ends_on_data[ax_right] = {value_axis}

        # an axis end on the data puts marks on the frame: they draw whole
        # over it instead of half-clipped by it; an axis the user limits
        # keeps the clip, since the limit may cut the data on purpose
        for axes, dims in ends_on_data.items():
            if not dims:
                continue
            for layer in layers:
                if isinstance(layer, (LineLayer, UnclippedMarksMixin)):
                    layer.unclip_marks(axes, sorted(dims))

        # radial furniture reads the final r limits, so it follows them
        if polar:
            self._apply_radial_furniture(ax)

        # beeswarm packing reads the display transform, so it runs once the
        # scales and limits are final (ADR 0020); over ridges the points pack
        # on the side the ridges rise to, inside them (ADR 0047)
        swarm_side = (-1 if horizontal else 1) if ridges else 0
        swarms = defaultdict(list)
        for group, owner_ax in zip(self.groups, group_axes):
            for layer in group.layers:
                if isinstance(layer, SwarmLayer):
                    swarms[owner_ax].append(layer)
        for owner_ax, swarm_layers in swarms.items():
            pack_swarms(owner_ax, swarm_layers, swarm_side)

        # one reference declared for every chart of a figure draws once per
        # axes, so a line or text does not repeat and a band's tint does not
        # stack with the series count; each is read on its figure's axes
        pools = {}
        for group, owner_ax in zip(self.groups, group_axes):
            pooled = pools.setdefault(owner_ax, {key: [] for key in REF_KEYS})
            for layer in group.layers:
                for key in REF_KEYS:
                    for entry in getattr(layer, key):
                        if entry not in pooled[key]:
                            pooled[key].append(entry)

        # reference lines and bands, after scales and limits
        for owner_ax, pooled in pools.items():
            _draw_ref_lines(owner_ax, pooled["vlines"], pooled["hlines"])
        # the host axes sits under a twin, so every band lies beneath both
        # axes' marks (ADR 0036)
        for owner_ax, pooled in pools.items():
            vspans, hspans = pooled["vspans"], pooled["hspans"]
            if owner_ax is ax:
                _draw_ref_spans(ax, vspans, hspans, polar)
                continue
            # only the twin's value axis differs from the host's
            if horizontal:
                _draw_ref_spans(ax, [], hspans, polar)
                _draw_ref_spans(ax, vspans, [], polar, value_ax=owner_ax)
            else:
                _draw_ref_spans(ax, vspans, [], polar)
                _draw_ref_spans(ax, [], hspans, polar, value_ax=owner_ax)

        # a twin axes renders entirely above its host, so texts live on the
        # topmost axes while data coordinates read the owning layer's axes
        top_ax = ax_right if ax_right is not None else ax
        clearance = None
        if any(pooled["texts"] for pooled in pools.values()):
            clearance = self._clearance_points(group_axes, horizontal)
        for owner_ax, pooled in pools.items():
            _draw_texts(top_ax, pooled["texts"], owner_ax, clearance)

        # point labels are placed once every marker of the panel is drawn and
        # the limits are final, so the estimate sees the real display space
        self._place_point_labels(top_ax, group_axes)

        # aspect ratio (a polar axes keeps its own; a bare layer fixed its own)
        if s.get("aspect_ratio") and not polar and not bare:
            ax.set(adjustable="box", aspect=s["aspect_ratio"])

        # a cell inside a shared grid leaves its inner tick labels to the edge
        for axis in s.get("hide_ticklabels") or ():
            side = "labelbottom" if axis == "x" else "labelleft"
            ax.tick_params(axis=axis, **{side: False})
        # a cell holding only text has no scale to mark
        for axis in s.get("hide_ticks") or ():
            side = "bottom" if axis == "x" else "left"
            ax.tick_params(axis=axis, which="both", **{side: False})

        # panel-level labels (used when a panel renders into a grid cell)
        label_styles = s.get("label_styles", {})
        for key, action in [
            ("title", ax.set_title),
            ("xlabel", ax.set_xlabel),
            ("ylabel", ax.set_ylabel),
        ]:
            if s.get(key):
                style = dict(label_styles.get(key) or {})
                if polar and key != "title":
                    # clear the category labels sitting around the circle
                    style["labelpad"] = (
                        RADIAL_YLABEL_PAD if key == "ylabel" else RADIAL_XLABEL_PAD
                    )
                action(s[key], **style)
        if s.get("ylabel_right") and ax_right is not None:
            # the secondary value-axis label shares the primary label's text style
            (ax_right.set_xlabel if horizontal else ax_right.set_ylabel)(
                s["ylabel_right"], **(label_styles.get("ylabel") or {})
            )

        # legend: on the topmost axes, so right-axis marks never cover it
        if s.get("show_legend"):
            legend_style = {
                **s.get("legend_style", {}),
                "handler_map": LEGEND_HANDLER_MAP,
            }
            custom_handles = None
            for group in self.groups:
                for layer in group.layers:
                    # background layers carry no legend entries
                    if layer.draws_all_muted(group.layer_role(layer), group.emphasis):
                        continue
                    handles = getattr(layer, "legend_handles", lambda: None)()
                    if handles:
                        custom_handles = (custom_handles or []) + handles
            if custom_handles is not None:
                if bare and not s.get("legend_loc_explicit"):
                    # the marks fill the axes: the legend sits beside them
                    legend_style.update(
                        expand_legend_location(LEGEND_LOCATION.OUTSIDE_RIGHT)
                    )
                # the layers' own keys first, then references and composed marks
                if s.get("legend_mode") == "combined":
                    handles, labels = self._combined_legend_entries(
                        ax, ax_right, horizontal
                    )
                else:
                    handles, labels = ax.get_legend_handles_labels()
                    if ax_right is not None:
                        handles_right, labels_right = (
                            ax_right.get_legend_handles_labels()
                        )
                        handles, labels = handles + handles_right, labels + labels_right
                _draw_legend(
                    ax,
                    ax_right,
                    legend_style,
                    custom_handles + handles,
                    [h.get_label() for h in custom_handles] + labels,
                )
            elif s.get("legend_mode") == "combined":
                handles, labels = self._combined_legend_entries(
                    ax, ax_right, horizontal
                )
                if handles:
                    _draw_legend(ax, ax_right, legend_style, handles, labels)
            elif not any(isinstance(l, ParallelCoordsLayer) for l in layers):
                # parallel coords only carry a legend when hue groups exist;
                # unlabeled panels get no empty legend frame
                handles, labels = ax.get_legend_handles_labels()
                if labels:
                    _draw_legend(ax, ax_right, legend_style, handles, labels)

            legend = top_ax.get_legend()
            if legend is not None and not bare and "bbox_to_anchor" in legend_style:
                # an outside legend clears the axis furniture at draw time
                axes = [ax] + ([ax_right] if ax_right is not None else [])
                _defer_legend_fit(
                    top_ax, lambda renderer: _fit_outside_legend(legend, axes, renderer)
                )

        legend = top_ax.get_legend()
        if legend is not None and polar:
            # the polar border circle crosses the plot area; the legend sits
            # above the spine so it is never cut by the circle
            legend.set_zorder(self._spine_zorder() + RADIAL_LEGEND_Z_OVER_SPINE)
        elif legend is not None and not bare:
            # a legend over the marks gets headroom at draw time, once layout
            # has sized the axes; an explicit value-axis limit, or a stack
            # filling its frame, stays as set
            value_axis = "x" if horizontal else "y"
            value_max = s.get(f"{value_axis}max")
            if (
                value_max is None
                and value_axis not in pinned
                and (ax_right is None or s.get("ymax_right") is None)
            ):
                axes = [ax] + ([ax_right] if ax_right is not None else [])
                dim = 0 if horizontal else 1
                _defer_legend_fit(
                    top_ax, lambda renderer: _fit_legend(legend, axes, dim, renderer)
                )

        # tick labels and legend text cannot take the font family through
        # tick_params/legend kwargs; restyle them directly
        family = (s.get("furniture") or {}).get("font_family")
        if family:
            for target in [ax] + ([ax_right] if ax_right is not None else []):
                for label in target.get_xticklabels() + target.get_yticklabels():
                    label.set_fontfamily(family)
            # a date period's parent row lives on a secondary axes
            for child in ax.child_axes:
                child.tick_params(labelfontfamily=family)
            legend = top_ax.get_legend()
            if legend is not None:
                for text in legend.get_texts():
                    text.set_fontfamily(family)
                if legend.get_title() is not None:
                    legend.get_title().set_fontfamily(family)

    def _place_point_labels(self, top_ax, group_axes) -> None:
        """Gather every labelled layer's points and place their labels together."""

        px_per_pt = top_ax.figure.dpi / 72.0
        entries, obstacles = [], []
        for group, owner_ax in zip(self.groups, group_axes):
            for layer in group.layers:
                if not isinstance(layer, PointLabelMixin):
                    continue
                for xs, ys, sizes, labels, font, pad in layer.pending_labels(owner_ax):
                    centers = owner_ax.transData.transform(np.column_stack([xs, ys]))
                    # scatter sizes are marker areas in points squared
                    radii = np.sqrt(np.broadcast_to(sizes, len(xs))) / 2
                    for i, ((cx, cy), r) in enumerate(zip(centers, radii)):
                        rpx = r * px_per_pt
                        obstacles.append((cx - rpx, cy - rpx, cx + rpx, cy + rpx))
                        if labels is not None and labels[i] is not None:
                            entries.append(
                                (
                                    owner_ax,
                                    xs[i],
                                    ys[i],
                                    r,
                                    pad,
                                    labels[i],
                                    font,
                                    layer.label_spots,
                                )
                            )
                if layer.show_correlation:
                    obstacles.append(self._correlation_box(top_ax, layer))
                obstacles.extend(layer.label_obstacles(owner_ax))
        if entries:
            _draw_point_labels(top_ax, entries, obstacles)

    @staticmethod
    def _correlation_box(ax, layer) -> tuple:
        """The display-space box the layer's correlation readout occupies."""

        px_per_pt = ax.figure.dpi / 72.0
        fontsize = layer.correlation_font["fontsize"]
        w, h = (v * px_per_pt for v in _text_size(fontsize, CORRELATION_BOX_TEXT))
        # matplotlib pads a text box by 0.3 font sizes unless the boxstyle says
        pad = CORRELATION_BOX_PAD * fontsize * px_per_pt
        if layer.correlation_bbox is None:
            pad = 0.0
        x0, y1 = ax.transAxes.transform(CORRELATION_BOX_CORNER)
        return (x0 - pad, y1 - h - pad, x0 + w + pad, y1 + pad)

    def _clearance_points(self, group_axes, horizontal):
        """The panel's data in display coordinates, for connector scoring."""

        points = []
        for group, owner_ax in zip(self.groups, group_axes):
            for layer in group.layers:
                try:
                    xy = _layer_clearance_xy(layer, horizontal)
                except (TypeError, ValueError):
                    xy = None
                if xy is None or len(xy) == 0:
                    continue
                xy = xy[np.isfinite(xy).all(axis=1)]
                if len(xy):
                    points.append(owner_ax.transData.transform(xy))
        return np.vstack(points) if points else None

    def _apply_tick_formats(self, ax) -> dict:
        """Apply the temporal locator and the tick formats (ADR 0037).

        Returns one labeler per formatted axis, keyed like `ax.xaxis`, that
        turns explicit tick positions into text in the same format.
        """

        s = self.settings
        labelers = {}
        for axis_name in ("x", "y"):
            axis = getattr(ax, f"{axis_name}axis")
            fmt = s.get(f"{axis_name}ticks_format")
            temporal = self.temporal_axis == axis_name
            if not temporal and axis_name in self.date_axes:
                # dated category labels carry the format in their text
                continue
            locator = tz = None
            if temporal:
                # plotted datetimes leave their zone on the axis; a layer
                # drawing date numbers keeps it itself
                units = axis.get_units()
                tz = units if isinstance(units, tzinfo) else None
                if tz is None:
                    tz = next((l.x_tz for l in self.layers if l.x_tz), None)
                period = s.get("date_period")
                if period is not None:
                    origin = None
                    if period == GANTT_DATE_PERIOD.PROJECT_MONTH:
                        origin = self._project_origin(tz)
                    bounds = self._schedule_bounds()
                    if bounds is not None:
                        bounds = tuple(
                            None if s.get(key) is not None else value
                            for key, value in zip(("xmin", "xmax"), bounds)
                        )
                    _apply_date_period(ax, axis_name, period, fmt, tz, origin, bounds)
                    labelers[f"{axis_name}axis"] = lambda ticks, fmt=fmt: date_labels(
                        ticks, fmt
                    )
                    continue
                locator = self._schedule_ticks(tz) or mdates.AutoDateLocator(tz=tz)
                axis.set_major_locator(locator)
            formatter = _tick_formatter(fmt, temporal, locator, tz)
            if formatter is not None:
                axis.set_major_formatter(formatter)
            if temporal:
                labelers[f"{axis_name}axis"] = lambda ticks, fmt=fmt: date_labels(
                    ticks, fmt
                )
            elif formatter is not None:
                labelers[f"{axis_name}axis"] = lambda ticks, f=formatter: [
                    f(tick) for tick in ticks
                ]
        return labelers

    def _schedule_bounds(self):
        """A gantt panel's (first start, last end) as date numbers, else None."""

        if not self.layers or any(not isinstance(l, GanttLayer) for l in self.layers):
            return None
        ranges = [r for r in (l.y_range() for l in self.layers) if r is not None]
        if not ranges:
            return None
        return (min(r[0] for r in ranges), max(r[1] for r in ranges))

    def _schedule_ticks(self, tz):
        """A gantt panel's date ticks: first start to last end, regular between."""

        bounds = self._schedule_bounds()
        if bounds is None:
            return None
        ends = np.concatenate(
            [np.concatenate([l.starts, l.starts + l.durations]) for l in self.layers]
        )
        timed = any(d.time() != time() for d in mdates.num2date(ends, tz=tz))
        return ScheduleTicks(*bounds, tz, timed)

    def _project_origin(self, tz):
        """The project start: `xmin` when given, else the earliest task start."""

        start = self.settings.get("xmin")
        if start is None:
            starts = [
                float(np.min(l.starts))
                for l in self.layers
                if isinstance(l, GanttLayer) and len(l.starts)
            ]
            start = min(starts) if starts else 0.0
        if not isinstance(start, (int, float)):
            start = float(to_date_numbers([start])[0])
        return mdates.num2date(start, tz=tz)

    def _apply_pyramid_mirror(self, ax) -> None:
        """The pyramid's mirror furniture (ADR 0017).

        Symmetric value limits around zero, absolute-value tick display, and
        user ticks mirrored to both halves — both sides read as positive
        magnitudes.
        """

        s = self.settings

        limit = s.get("pyramid_xmax")
        if limit is None:
            lo, hi = ax.get_xlim()
            limit = max(abs(lo), abs(hi))
        ax.set_xlim(-limit, limit)

        fmt = s.get("xticks_format")
        magnitude = (
            (lambda value: f"{abs(value):g}")
            if _auto_format(fmt)
            else (lambda value: _format_value(fmt, abs(value)))
        )
        ax.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda value, _pos: magnitude(value))
        )

        ticks = s.get("pyramid_xticks")
        if ticks is not None:
            labels = s.get("pyramid_xticklabels")
            if labels is not None and len(labels) != len(ticks):
                warnings.warn(
                    "The values of `xticks` and `xticklabels` are of different lengths. "
                    "Please provide the same number of values. "
                    "Ignoring `xticklabels` values..."
                )
                labels = None
            label_at = {}
            for index, tick in enumerate(ticks):
                label = labels[index] if labels is not None else None
                label_at[-float(tick)] = label
                label_at[float(tick)] = label
            positions = sorted(label_at)
            ax.set_xticks(positions)
            if labels is not None:
                ax.set_xticklabels([label_at[p] for p in positions])
        rotation = s.get("pyramid_xtickrotate")
        if rotation:
            ax.xaxis.set_tick_params(labelrotation=rotation)

    def _apply_bar_ticks(self, ax, bar_ticks, bar_layers) -> None:
        gantt = next((l for l in bar_layers if isinstance(l, GanttLayer)), None)
        if gantt is not None:
            # task rows skip the header and gap rows, so they place themselves
            gantt.apply_row_ticks(ax)
            return
        # the widest layer supplies the labels when category counts differ
        layer = max(bar_layers, key=lambda l: len(l.labels()))
        labels = layer.labels()
        # ticks sit on the category positions; slotted groups center on them
        ticks_loc = np.arange(labels.shape[0])
        labels = self._category_labels(labels, "y" if layer.is_horizontal else "x")

        if bar_ticks == "group":
            rotation_default = 0
        else:  # one bar layer per subplot
            n_labels = len(labels)
            rotation_default = 90 if n_labels >= 7 else (45 if n_labels >= 4 else 0)

        if layer.is_horizontal:
            ax.set_yticks(ticks_loc, labels)
            ax.yaxis.set_major_locator(mticker.FixedLocator(list(ticks_loc)))
            ax.set_yticklabels(labels, rotation=layer.chart.get("ytickrotate", 0))
        else:
            ax.set_xticks(ticks_loc, labels)
            ax.xaxis.set_major_locator(mticker.FixedLocator(list(ticks_loc)))
            rotation = layer.chart.get("xtickrotate")
            if rotation is None:
                rotation = rotation_default
            ax.set_xticklabels(labels, rotation=rotation)

    def _apply_radial_furniture(self, ax) -> None:
        """Apply start angle, direction, and inner radius; elevate the r labels."""

        s = self.settings

        startangle = s.get("startangle")
        startangle = DEFAULT_STARTANGLE if startangle is None else startangle
        if isinstance(startangle, str):
            ax.set_theta_zero_location(startangle)
        else:
            # a numeric startangle is a compass bearing: degrees clockwise
            # from north, matching the compass-string form
            ax.set_theta_zero_location("N", offset=-float(startangle))

        direction = s.get("direction") or DEFAULT_DIRECTION
        ax.set_theta_direction(-1 if direction == RADIAL_DIRECTION.CLOCKWISE else 1)

        innerradius = s.get("innerradius") or 0.0
        if innerradius:
            rmin, rmax = ax.get_ylim()
            # r = rorigin maps to the center: the hole takes the given
            # fraction of the drawn radial extent
            ax.set_rorigin(rmin - innerradius / (1 - innerradius) * (rmax - rmin))

        if s.get("show_border") is False:
            for spine in ax.spines.values():
                spine.set_visible(False)

        self._elevate_radial_value_labels(ax)
        self._draw_radial_tip_texts(ax)

    def _spine_zorder(self) -> float:
        """The build-time spine zorder; the polar top-of-stack reference."""

        furniture = self.settings.get("furniture") or {}
        spines = furniture.get("spines") or {}
        return spines.get("bottom", {}).get("zorder", DEFAULT_SPINE_ZORDER)

    def _elevate_radial_value_labels(self, ax) -> None:
        """Redraw the r tick labels above the marks and the border, in black.

        The native axis draws grid lines and tick labels in one layer, so the
        labels cannot sit above the data while the grid stays below it.
        """

        rmin, rmax = ax.get_ylim()
        ticks = [t for t in ax.yaxis.get_ticklocs() if rmin < t <= rmax]
        if not ticks:
            return
        texts = ax.yaxis.get_major_formatter().format_ticks(ticks)
        ax.set_yticks(ticks, labels=[""] * len(ticks))

        furniture = self.settings.get("furniture") or {}
        tick_style = furniture.get("ticks", {})
        theta = np.deg2rad(ax.get_rlabel_position())
        # each label hangs just inside its ring, so the border circle passes
        # outside the outermost one instead of through it
        screen = ax.get_theta_direction() * theta + ax.get_theta_offset()
        size = FontProperties(size=tick_style.get("labelsize")).get_size_in_points()
        inset = (size / 2 + RADIAL_RLABEL_INSET) / 72
        inward = ScaledTranslation(
            -inset * np.cos(screen), -inset * np.sin(screen), ax.figure.dpi_scale_trans
        )
        for r, text in zip(ticks, texts):
            ax.text(
                theta,
                r,
                text,
                transform=ax.transData + inward,
                ha="center",
                va="center",
                fontsize=tick_style.get("labelsize"),
                fontfamily=furniture.get("font_family"),
                color="#000000",
                zorder=self._spine_zorder() + RADIAL_LABEL_Z_OVER_SPINE,
                path_effects=self._text_halo(),
            )

    def _draw_radial_tip_texts(self, ax) -> None:
        """Write values and category labels at the mark tips, along the spokes.

        Texts rotate with their spoke's final screen angle and flip on the
        left half so they always read outward.
        """

        s = self.settings
        show_values = s.get("show_values")
        show_tip_labels = s.get("show_tip_labels")
        if not show_values and not show_tip_labels:
            return
        tips = [
            tip
            for layer in self.layers
            if isinstance(layer, RadialLayer)
            for tip in layer._tips
        ]
        if not tips:
            return

        rmin, rmax = ax.get_ylim()
        span = (rmax - rmin) or 1.0
        z_order = self._spine_zorder() + RADIAL_LABEL_Z_OVER_SPINE
        furniture = s.get("furniture") or {}
        tick_style = furniture.get("ticks", {})
        family = furniture.get("font_family")
        offset = ax.get_theta_offset()
        direction = ax.get_theta_direction()

        def spoke_rotation(theta):
            screen = np.rad2deg(direction * theta + offset) % 360
            if 90 < screen <= 270:
                return screen + 180, "right"
            return screen, "left"

        if show_values:
            value_format = s.get("value_format") or DEFAULT_VALUE_LABEL_FORMAT
            value_style = s.get("tip_value_style") or {}
            for theta, r_tip, value, _ in tips:
                if value is None:
                    continue
                rotation, ha = spoke_rotation(theta)
                ax.text(
                    theta,
                    r_tip + RADIAL_TIP_VALUE_PAD * span,
                    _format_value(value_format, value),
                    rotation=rotation,
                    rotation_mode="anchor",
                    ha=ha,
                    va="center",
                    zorder=z_order,
                    fontfamily=family,
                    **value_style,
                )

        if show_tip_labels:
            label_sets = [
                l.labels()
                for l in self.layers
                if isinstance(l, RadialLayer) and l.is_categorical
            ]
            label_sets = [lbl for lbl in label_sets if lbl is not None and len(lbl)]
            if not label_sets:
                return
            cat_labels = max(label_sets, key=len)
            theta_positions = _radial_theta(len(cat_labels))
            # each label hugs the outermost mark on its own spoke
            outer = {}
            for _, r_tip, _, index in tips:
                if index is not None:
                    outer[index] = max(outer.get(index, rmin), r_tip)
            pad = RADIAL_TIP_LABEL_PAD + (
                RADIAL_TIP_VALUE_PAD * 2 if show_values else 0
            )
            for i, label in enumerate(cat_labels):
                if i not in outer:
                    continue
                rotation, ha = spoke_rotation(theta_positions[i])
                ax.text(
                    theta_positions[i],
                    outer[i] + pad * span,
                    str(label),
                    rotation=rotation,
                    rotation_mode="anchor",
                    ha=ha,
                    va="center",
                    zorder=z_order,
                    fontsize=tick_style.get("labelsize"),
                    color=tick_style.get("labelcolor"),
                    fontfamily=family,
                    path_effects=self._text_halo(),
                )

    @staticmethod
    def _combined_legend_entries(ax_left, ax_right, horizontal=False) -> tuple:
        """The legend handles and labels of both axes, labels tagged by side."""

        handles_left, labels_left = ax_left.get_legend_handles_labels()
        if ax_right is None:
            return handles_left, labels_left

        handles_right, labels_right = ax_right.get_legend_handles_labels()
        primary, secondary = ("B", "T") if horizontal else ("L", "R")
        labels_left = [f"{label} ({primary})" for label in labels_left]
        labels_right = [f"{label} ({secondary})" for label in labels_right]
        return handles_left + handles_right, labels_left + labels_right


# ================================================
# Panel Assembly for Chart Fronts
# ================================================


GROUP_CHART_TYPES = (
    "boxplot",
    "dumbbellchart",
    "violinplot",
    "swarmplot",
    "raincloudplot",
    "ridgelineplot",
)


def value_axis_grid(show_grid, horizontal: bool):
    """A theme's one-axis grid default, moved onto a horizontal value axis.

    Themes name the grid of an upright chart, whose values run along y; a
    dumbbell's gridlines follow its values whichever way they run (ADR 0050).
    """

    if not horizontal:
        return show_grid
    return {"x": "y", "y": "x"}.get(show_grid, show_grid)


def build_chart_panel_settings(
    chart_type: str, settings: dict, mode: str, first_style: dict
) -> dict:
    """Resolve panel-level settings for a chart front at build time.

    Modes: "single" (all layers on the figure's one axes), "subplot" (one layer
    per axes), "composition" (the metadata panel used by grids).
    """

    show_grid = settings.get("show_grid")
    # rasters (a heatmap, hexagons, filled contour bands) cover the grid, and a
    # bump chart's ranks read from the lines and labels: no grid unless asked
    gridless = chart_type in (
        "heatmap",
        "calendarheatmap",
        "hexbinchart",
        "bumpchart",
    ) or (chart_type == "contourchart" and settings.get("filled"))
    if show_grid is None and not gridless:
        show_grid = config.get("chart_default_show_grid")
        if chart_type == "dumbbellchart":
            orientation = settings.get("orientation") or DEFAULT_ORIENTATION
            show_grid = value_axis_grid(
                show_grid, orientation == ORIENTATION.HORIZONTAL
            )

    # the seam's scale keys are literal; group fronts mean the value axis
    scalex, scaley = settings.get("scalex"), settings.get("scaley")
    if (
        chart_type in GROUP_CHART_TYPES
        and settings.get("orientation") == ORIENTATION.HORIZONTAL
    ):
        scalex, scaley = scaley, scalex

    panel_settings = {
        "furniture": Panel.snapshot_furniture(),
        "scalex": scalex,
        "scaley": scaley,
        # horizontal bars and histograms take their scale keys literally
        "literal_scale_keys": chart_type not in GROUP_CHART_TYPES,
        "show_grid": show_grid,
        "grid_style": get_grid_style(first_style),
        "hatch_cycle": config.get("plot_hatch_cycle"),
        "linestyle_cycle": config.get("plot_linestyle_cycle"),
        "marker_cycle": config.get("plot_marker_cycle"),
        "xmin": settings.get("xmin"),
        "xmax": settings.get("xmax"),
        "ymin": settings.get("ymin"),
        "ymax": settings.get("ymax"),
        "xticks_format": settings.get("xticks_format"),
        "date_period": validate_date_period(settings.get("period")),
        "yticks_format": settings.get("yticks_format"),
        "aspect_ratio": (
            ASPECT_RATIO.AUTO
            if settings.get("aspect_ratio") is None
            else settings["aspect_ratio"]
        ),
        **get_legend_panel_settings(settings.get("legend")),
        # histograms stack by default; bars group (ADR 0014)
        "bar_mode": settings.get("bar_mode")
        or ("stack" if chart_type == "histogram" else "group"),
        "tighten_xlim": chart_type in ("linechart", "stackedareachart", "bumpchart"),
        # validated here so a bad value fails at the front, like the emphasis roles
        "baseline": validate_baseline(settings.get("baseline")),
        # radial furniture; only polar panels read these
        "startangle": settings.get("startangle"),
        "direction": settings.get("direction"),
        "innerradius": settings.get("innerradius"),
        "show_border": settings.get("show_border"),
        "show_values": _resolve_show_values(settings),
        "show_tip_labels": settings.get("show_tip_labels"),
        "value_format": settings.get("value_format"),
        # the tip texts set their own family, rotated along the spoke
        "tip_value_style": {
            k: v
            for k, v in _value_label_font(get_value_label_style(first_style)).items()
            if k != "family"
        },
    }

    if chart_type == "pyramidchart":
        # the mirror is panel furniture (ADR 0017): overlay slots give both
        # sides full width at offset zero, the panel owns limits and ticks
        panel_settings["pyramid"] = True
        panel_settings["bar_mode"] = "overlay"
        panel_settings["pyramid_xmax"] = settings.get("xmax")
        panel_settings["xmax"] = None
        panel_settings["pyramid_xticks"] = settings.get("xticks")
        panel_settings["pyramid_xticklabels"] = settings.get("xticklabels")
        panel_settings["pyramid_xtickrotate"] = settings.get("xtickrotate")

    if mode == "subplot":
        panel_settings["show_legend"] = False
        panel_settings["bar_slotting"] = False
        panel_settings["bar_ticks"] = "subplot"
    else:
        panel_settings["show_legend"] = settings.get("show_legend")
        panel_settings["bar_ticks"] = "group"

    if mode == "composition":
        panel_settings["hide_ticklabels"] = settings.get("hide_ticklabels")
        panel_settings["marks_on_twin"] = settings.get("marks_on_twin")
        panel_settings["hide_ticks"] = settings.get("hide_ticks")
        panel_settings["xlabel"] = settings.get("xlabel")
        panel_settings["ylabel"] = settings.get("ylabel")
        panel_settings["label_styles"] = Panel.snapshot_label_styles()

    return panel_settings
