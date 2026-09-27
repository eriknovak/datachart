"""The single drawing seam: Layer, LayerGroup, Panel, DrawContext.

A Layer is one drawable unit that puts its marks on a matplotlib Axes. Its style
is resolved from the global config when the layer is built — never at draw time.
A Panel owns every cross-layer concern: color assignment, bar slotting, shared
histogram bins, axis scales and limits, grid, legend assembly, and twin-axis
(left/right) assignment. Layers are sibling-blind; a Panel hands each layer a
frozen DrawContext with its per-layer instructions.
"""

import math
import warnings
from collections import defaultdict
from datetime import date, time, timedelta, tzinfo
from dataclasses import replace
from itertools import cycle as iter_cycle
from typing import Callable, List, NamedTuple, Optional, Tuple, Union
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
from matplotlib import cbook, rc_context
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator
from matplotlib.collections import (
    LineCollection,
    PatchCollection,
    PathCollection,
    PolyCollection,
)
from matplotlib.container import BarContainer
from matplotlib.colors import (
    CenteredNorm,
    LinearSegmentedColormap,
    TwoSlopeNorm,
    to_rgba,
    to_rgba_array,
)
from matplotlib.mlab import GaussianKDE
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, Patch, PathPatch, Rectangle
from matplotlib.path import Path
from matplotlib.text import Text
from matplotlib.transforms import (
    offset_copy,
    Bbox,
    ScaledTranslation,
    blended_transform_factory,
)
from matplotlib.legend import Legend
from matplotlib.legend_handler import (
    HandlerPatch,
    HandlerPathCollection,
    HandlerPolyCollection,
)
from ..basemap import load_basemap, load_country_codes
from ..colors import (
    create_color_cycle,
    create_colormap,
    get_colormap,
    get_discrete_colors,
)
from ..validate import (
    AXIS_NUMERIC,
    AXIS_TEMPORAL,
    infer_network_nodes,
    first_seen_nodes,
    infer_sankey_columns,
    is_missing,
    is_number,
    treemap_record_total,
    validate_contour_levels,
    validate_filled_levels,
    validate_emphasis,
    validate_error_distances,
    validate_emphasis_rule,
    validate_dumbbell_sort_by,
    validate_marker_pair,
    BASEMAP_FEATURES,
    BASEMAP_FILLED,
    validate_basemap_availability,
    validate_basemap_company,
    validate_basemap_features,
    validate_basemap_geometry,
    validate_basemap_highlight,
    validate_basemap_source,
    validate_geographic_latitudes,
    validate_image,
    validate_image_extent,
    validate_log_values,
    validate_overlap,
    validate_ridge_marks,
    validate_single_dataset,
    validate_network_edge_style,
    validate_sankey_link_color,
    validate_axis_kinds,
    validate_shared_x,
    validate_bracket_endpoint,
    validate_ticks_format,
    validate_two_slope_bounds,
)
from ..config_helpers import (
    get_heatmap_cmap,
    get_attr_value,
    resolve_font_family,
    get_area_style,
    get_sankey_style,
    get_treemap_style,
    get_network_style,
    get_line_style,
    get_bar_style,
    get_dumbbell_style,
    get_hist_style,
    expand_legend_location,
    get_heatmap_style,
    get_heatmap_font_style,
    get_heatmap_edge_style,
    get_calendar_month_line_style,
    get_contour_style,
    get_contour_label_style,
    get_hexbin_style,
    get_image_style,
    get_basemap_style,
    get_colorbar_setting,
    get_scatter_style,
    get_scatter_error_style,
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
from ...stats import iqr, kde1d
from ....constants import (
    ARROW_STYLE,
    ASPECT_RATIO,
    CALENDAR_WEEKDAY,
    COLORBAR_LOCATION,
    COLORS,
    CONTOUR_LEVELS,
    DUMBBELL_SORT_KEY,
    DUMBBELL_VALUE,
    GANTT_DATE_PERIOD,
    HEXBIN_REDUCE,
    BASEMAP_FEATURE,
    BASEMAP_RESOLUTION,
    BAR_MODE,
    DRAW_POSITION,
    LEGEND_LOCATION,
    NETWORK_LAYOUT,
    NETWORK_LABEL_POSITION,
    COLOR_NORM,
    ORIENTATION,
    RADIAL_DIRECTION,
    RADIAL_TYPE,
    RIDGELINE_SCALE,
    AXIS_SCALE,
    SORT,
    STACKED_AREA_BASELINE,
    SWARM_MODE,
    VALUE_FORMAT,
    VIOLIN_INNER,
)
from ....config import config
from .base import (
    AreaFillMixin,
    BarSlot,
    COLORBAR_FRACTION,
    DEFAULT_NUM_BINS,
    DEFAULT_ORIENTATION,
    DEFAULT_VALUE_LABEL_FORMAT,
    DrawContext,
    EMPHASIS_BACKGROUND,
    EMPHASIS_HIGHLIGHT,
    EMPHASIS_Z_OFFSET,
    EndLabelMixin,
    Etch,
    HIGHLIGHT_WIDTH_SCALE,
    HOLLOW_MARKER_EDGE_WIDTH,
    InkStroke,
    Layer,
    MARKER_EDGE_MAX_SHARE,
    MARKER_ROLE_ORDER,
    MUTED_WIDTH_SCALE,
    MarkClipBox,
    NO_LEGEND,
    NumpyEncoder,
    POINT_LABEL_PAD,
    POINT_LABEL_SPOTS,
    POINT_LABEL_SPOTS_VERTICAL,
    PointLabelMixin,
    REF_CYCLE_COLOR,
    SPAN_SIDES,
    TEXT_ANNOTATION_ZORDER,
    TEXT_LINE_HEIGHT,
    UnclippedMarksMixin,
    _aligned_roles,
    _annotate_value,
    _apply_cycle_hatch,
    _category_positions,
    _chart_column,
    _defer_legend_fit,
    _draw_scatter_marks,
    _drawn_error_axis,
    _fill_role,
    _fit_outside_legend,
    _format_value,
    _halo_effects,
    _hollow_marker,
    _keep_role,
    _keyed_records,
    _legend_pad_px,
    _lighten,
    _marker_edge_widths,
    _oriented,
    _point_resolver,
    _present_range,
    _px_to_points,
    _record_emphasis,
    _resolve_texts,
    _rule_summary,
    _scalar,
    _span_text,
    _step_label,
    _text_size,
    _validated_record_roles,
    _value_tab_bbox,
    axis_kind,
    emphasis_rule_roles,
    get_chart_data,
    get_chart_hash,
    get_chart_observations,
    is_temporal,
    resolve_show_values,
    resolve_value_kind,
    series_units,
    step_edges,
    theme_default,
    value_axis_grid,
    value_label_font,
)
from .ticks import (
    PeriodTicks,
    ScheduleTicks,
    _apply_date_period,
    _auto_format,
    _column_tz,
    _tick_formatter,
    _widen_to_ticks,
    date_labels,
    to_date_numbers,
)
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
    _LockedBarLocator,
    _hist_stack_slots,
    bar_units,
    gantt_units,
    sort_bar_charts,
    sort_gantt_charts,
)

DEFAULT_VALUE_FORMAT = VALUE_FORMAT.DEFAULT


DEFAULT_CI_LEVEL = 0.95


DEFAULT_SIZE_RANGE = (20, 200)


DEFAULT_SWARM_MODE = SWARM_MODE.SWARM


DEFAULT_SWARM_JITTER = 0.4


# swarm offsets stay inside the category cell, clear of its neighbors
SWARM_MAX_OFFSET = 0.4


# sankey labels: room past the outer columns, the gap to the node bar
SANKEY_LABEL_MARGIN = 0.2


SANKEY_LABEL_PAD = 0.01


# column headings sit this far above the tallest column
SANKEY_COLUMN_LABEL_PAD = 0.03


SANKEY_COLUMN_LABEL_HEADROOM = 0.1


# a ribbon value sits at the ribbon's end, before the node it enters, where no
# label lives; thin ribbons fall back to spots along the centreline
SANKEY_VALUE_POSITIONS = (0.8, 0.65, 0.5, 0.35, 0.2)


# an overlap below this many square pixels counts as a clear spot
POINT_LABEL_CLEAR = 1e-6


# a raincloud's extremes sit past their points along the value axis, clear of
# the box whiskers beside the rain (ADR 0033)
POINT_LABEL_SPOTS_HORIZONTAL = POINT_LABEL_SPOTS[:2]


# passes of the end-label spread per label; a chain resolves in about one each
END_LABEL_SPREAD_PASSES = 10


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


# radial furniture defaults: compass and calendar conventions (ADR 0015)
DEFAULT_STARTANGLE = "N"


DEFAULT_DIRECTION = RADIAL_DIRECTION.CLOCKWISE


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


# cell luminance below which heatmap value text switches to white
HEATMAP_TEXT_DARK_LUMINANCE = 0.5


# the norms that hold `vcenter` in the middle of a diverging cmap (ADR 0056)
CENTRED_NORMS = (COLOR_NORM.CENTERED, COLOR_NORM.TWOSLOPE)


# the low end of a sequential cmap vanishes on white: iso-lines sample from here
CONTOUR_LINE_CMAP_START = 0.3


# the cmap sample that stands in for a cmap-colored contour in the legend
CONTOUR_SWATCH = 0.7


# an error bar sits this far under the markers it belongs to (ADR 0057)
ERROR_BAR_Z_STEP = 0.1


# the bar's cap, as a flat bracket at its far end; the width is in points
ERROR_CAP_STYLE = "-[,widthB={width},lengthB=0"


# the error columns a scatter point may carry, and the axis each is drawn
# along once a transposed panel has swapped the two
ERROR_KEYS = ("xerr", "yerr")


def get_chart_grid(chart: dict, kind: str, dtype=float) -> tuple:
    """The validated (x, y, z) of a gridded chart; x and y are None when absent."""

    z = get_chart_data("z", chart)
    if z is None:
        raise ValueError(f"A {kind} chart requires the `z` grid in `data`.")
    if isinstance(z, (list, tuple)) and all(isinstance(r, (list, tuple)) for r in z):
        for index, row in enumerate(z[1:], start=1):
            if len(row) != len(z[0]):
                raise ValueError(
                    f"The {kind} `z` grid is ragged: row {index} has {len(row)} "
                    f"value(s), row 0 has {len(z[0])}."
                )
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


def _shared_siblings(ax, axis_name: str) -> list:
    """Every axes sharing `ax`'s `x` or `y` axis, `ax` included."""

    return getattr(ax, f"get_shared_{axis_name}_axes")().get_siblings(ax)


def _shared_data_interval(ax, axis_name: str) -> tuple:
    """The data range of an axis, across every axes that shares it."""

    intervals = [
        getattr(a.dataLim, f"interval{axis_name}")
        for a in _shared_siblings(ax, axis_name)
    ]
    intervals = [i for i in intervals if np.isfinite(i).all()]
    if not intervals:
        return tuple(sorted(getattr(ax, f"{axis_name}axis").get_data_interval()))
    return min(min(i) for i in intervals), max(max(i) for i in intervals)


def _single_value_limits(value: float, temporal: bool) -> Tuple[float, float]:
    """The view around an axis's one data value, which has no range to show.

    A temporal axis pads a day each side, its value a date or a date
    number; a number pads 5 % of itself, or half a unit at zero (ADR 0082).
    """

    if isinstance(value, np.datetime64):
        pad = np.timedelta64(1, "D")
    elif isinstance(value, date):
        pad = timedelta(days=1)
    else:
        pad = 1.0 if temporal else 0.05 * abs(value) or 0.5
    return value - pad, value + pad


def _pad_single_value(ax, axis_name: str, temporal: bool) -> None:
    """Pad an axis whose data is one value, so its view is never zero-wide."""

    lo, hi = _shared_data_interval(ax, axis_name)
    if not (np.isfinite([lo, hi]).all() and lo == hi):
        return
    lo, hi = _single_value_limits(lo, temporal)
    axis = getattr(ax, f"{axis_name}axis")
    bounds = (hi, lo) if axis.get_inverted() else (lo, hi)
    (ax.set_xlim if axis_name == "x" else ax.set_ylim)(*bounds)


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
    # a single value keeps the padding on both sides of it
    if not fixed[0] and new_lo < 0 <= data_lo and data_hi > data_lo:
        new_lo = 0.0
    if not fixed[1] and new_hi > 0 >= data_hi and data_hi > data_lo:
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


# the layer attributes holding pre-resolved references, pooled per axes
REF_KEYS = ("vlines", "hlines", "dlines", "brackets", "vspans", "hspans", "texts")


# polar wedge outline samples per degree: enough for the chord error to vanish
SPAN_SAMPLES_PER_DEGREE = 2


def _span_bounds(span: dict, key: str, limits: tuple) -> tuple:
    """A band's (lower, upper) bounds, an omitted one falling back to the limit."""

    lo_key, hi_key, _ = SPAN_SIDES[key]
    lo = span.get(lo_key)
    hi = span.get(hi_key)
    return (limits[0] if lo is None else lo, limits[1] if hi is None else hi)


TEXT_COORDS = ("data", "axes")


# reference lines sit above every mark (zorder 3), below annotations (ADR 0054)
REF_LINE_ZORDER = 3.5


# an image's or basemap's rung (ADR 0054, 0060, 0062): below under the
# gridlines (0.5), above over the marks (3) and under the reference lines
DRAW_ZORDER = {DRAW_POSITION.BELOW: 0.25, DRAW_POSITION.ABOVE: 3.25}


def draw_zorder_key(position: str) -> str:
    """An image's or basemap's key in a Panel overlay's zorder table."""

    return f"draw_{position}"


def _split_outlines(rows: np.ndarray) -> List[np.ndarray]:
    """The outlines of `NaN`-separated rows; empty ones dropped."""

    breaks = np.flatnonzero(np.isnan(rows).any(axis=1))
    parts = np.split(rows, breaks)
    return [part[np.isfinite(part).all(axis=1)] for part in parts if len(part)]


def _filled_path(outlines: List[np.ndarray]) -> Path:
    """One compound path of closed rings; a ring wound the other way is a hole."""

    rings = [ring for ring in outlines if len(ring) >= 3]
    vertices = np.concatenate([np.vstack([ring, ring[:1]]) for ring in rings])
    codes = np.concatenate(
        [
            [Path.MOVETO] + [Path.LINETO] * (len(ring) - 1) + [Path.CLOSEPOLY]
            for ring in rings
        ]
    )
    return Path(vertices, codes)


# a diagonal is straight in data space, so on a non-linear axis it is a curve
# in display space and has to be sampled (ADR 0055)
DLINE_CURVE_SAMPLES = 100


# a bracket clears the data in its span by this fraction of the data range,
# and every bracket it overlaps by this one (ADR 0059)
BRACKET_GAP = 0.03


BRACKET_STEP = 0.08


# the gap (points) between a bracket's span and its text
BRACKET_TEXT_PAD = 2.0


# connector placement (ADR 0018): the bow side and depth are chosen at draw
# time against the panel's data, unless plot_text_arrow_curve pins them
TEXT_BOW_CANDIDATES = (0.2, -0.2, 0.35, -0.35, 0.5, -0.5)


# beyond this clearance (px) an arc is "clear of the data"; flatter wins
TEXT_BOW_CLEARANCE_CAP = 14.0


# the final approach always meets the data at the target: score the body only
TEXT_BOW_BODY = 0.75


# approximate half-extent of the text box (px), for connector-length checks
TEXT_BOX_PAD = 18.0


# short connectors (px past the box) straighten with tiny gaps (points),
# then vanish once those two gaps leave nothing of the line to draw
TEXT_SHORT_STRAIGHT = 40.0


TEXT_SHORT_GAP = 1.5


TEXT_SHORT_NONE = 2 * TEXT_SHORT_GAP


def _points_to_px(ax: plt.Axes, points: float) -> float:
    """A distance in points as display pixels."""

    return points * ax.figure.dpi / 72.0


def _target_gap(
    ax: plt.Axes, target: tuple, layers: List["Layer"], gap: float
) -> float:
    """The connector's target gap, capped to the mark it points at (ADR 0018).

    A fixed gap overshoots a mark smaller than itself and lands the tip on
    the neighbour; the smallest half-extent reported under the point wins.
    """

    extents = [layer.target_extent(ax, target) for layer in layers]
    extents = [extent for extent in extents if extent is not None]
    return min([gap, *extents])


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
    ax: plt.Axes,
    texts: List[tuple],
    data_ax: plt.Axes = None,
    clearance=None,
    layers: List["Layer"] = (),
) -> None:
    """Draw the pre-resolved text annotations.

    The artists land on `ax` — the panel's topmost axes, so they cover
    twin-axis marks — while data coordinates read from `data_ax`, the
    owning layer's axes. `clearance` holds the panel's data in display
    coordinates; a curved connector left on its default bows toward the
    side with the most open space. `layers` are the layers drawn on
    `data_ax`, which size the gap a connector leaves at its target.
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

        # nothing shows once the two gaps that frame it eat the whole line
        if length < _points_to_px(ax, TEXT_SHORT_NONE):
            ax.annotate(content, xy=(x, y), xycoords=textcoords, **kwargs)
            continue

        arrowprops = dict(style["arrowprops"])
        curve = arrowprops.pop("curve")
        pinned = arrowprops.pop("curve_pinned")
        arrowprops["shrinkB"] = _target_gap(
            data_ax, target, layers, arrowprops["shrinkB"]
        )
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


def _draw_ref_lines(
    ax: plt.Axes, vlines: List[tuple], hlines: List[tuple], dlines: List[tuple]
) -> None:
    """Draw the pre-resolved vertical, horizontal and diagonal reference lines."""

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

    if dlines:
        # a diagonal is a marker, not data: it may not rescale either axis
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        straight = ax.get_xscale() == "linear" and ax.get_yscale() == "linear"
        for dline, style in dlines:
            slope = dline.get("slope")
            intercept = dline.get("intercept")
            # the parity line y = x is the default
            slope = 1 if slope is None else slope
            intercept = 0 if intercept is None else intercept
            xmin, xmax = dline.get("xmin"), dline.get("xmax")
            kwargs = {
                "label": dline.get("label", ""),
                # an unset color is the first cycle color, as the other two
                # families take; a plotted segment would otherwise draw the
                # next color of the axes cycle and advance it
                "color": REF_CYCLE_COLOR,
                **{"zorder": REF_LINE_ZORDER, **style},
            }
            if xmin is None and xmax is None and straight:
                # unbounded: the line spans the axes and follows the zoom
                ax.axline((0, intercept), slope=slope, **kwargs)
                continue
            # an omitted bound runs to the axis limit, as a band's does
            x0 = xlim[0] if xmin is None else xmin
            x1 = xlim[1] if xmax is None else xmax
            xs = np.linspace(x0, x1, 2 if straight else DLINE_CURVE_SAMPLES)
            ax.plot(xs, slope * xs + intercept, **kwargs)
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)


def _layer_category_labels(layer: "Layer") -> Optional[list]:
    """The labels a layer places on the panel's category axis (ADR 0079).

    None for a layer off that axis; Gantt rows place themselves by task.
    """

    if isinstance(layer, GanttLayer):
        return None
    if isinstance(layer, (GroupLayer, BarLayer)) or (
        isinstance(layer, RadialLayer) and layer.is_categorical
    ):
        labels = layer.labels()
        return None if labels is None else list(labels)
    return None


def _check_unique_labels(layer: "Layer", labels: list, number: int) -> None:
    """Raise when one series names a category twice: its slot is ambiguous."""

    seen = set()
    for label in labels:
        if label in seen:
            series = layer.chart.get("subtitle") or f"#{number}"
            raise ValueError(
                f"Category label '{label}' repeats in series {series}; each "
                "label may appear once per series."
            )
        seen.add(label)


def _sorted_category_order(layer: "Layer", labels: list) -> list:
    """The sort's category order (ADR 0042), else the layer's own labels.

    The order holds raw record labels; this chart's own read as `labels()`
    does, so a label array's type coercion cannot miss the index.
    """

    order = layer.chart.get("category_order")
    if not order:
        return labels
    own = dict(zip(_chart_column("label", layer.chart) or (), labels))
    return [own.get(label, label) for label in order]


def _bracket_categories(layers: List["Layer"], category_index: dict) -> tuple:
    """A panel's categories for bracket placement, as (positions, tops).

    `positions` maps a label to its place on the category axis: group and bar
    layers share the panel's category index (ADR 0079), and a layer off it
    places its labels in its own order. `tops` maps a position to the top of
    the data drawn there.
    """

    positions = dict(category_index)
    tops = {}
    for layer in layers:
        if isinstance(layer, GroupLayer):
            grouped = layer.grouped_values()
        elif isinstance(layer, BarLayer):
            labels, values = layer.labels(), layer.y_values()
            if labels is None or values is None:
                continue
            # a bar is one value at its label, where a group is many
            grouped = {label: [value] for label, value in zip(labels, values)}
        else:
            continue
        for position, (label, values) in enumerate(grouped.items()):
            positions.setdefault(label, position)
            if len(values):
                top = float(np.max(values))
                tops[label] = max(top, tops.get(label, top))
    return positions, {
        positions[label]: top
        for label, top in tops.items()
        if np.isfinite(top) and label in positions
    }


def _span_top(layer: "Layer", start: float, end: float) -> Optional[float]:
    """The top of a continuous layer's values between two category positions.

    None when the layer draws no paired numeric (x, y) data to read, which
    leaves the bracket clearing the whole panel instead.
    """

    xs, ys = get_chart_data("x", layer.chart), get_chart_data("y", layer.chart)
    if xs is None or ys is None or len(xs) != len(ys):
        return None
    if not np.issubdtype(np.asarray(xs).dtype, np.number):
        return None
    inside = np.asarray(ys)[(np.asarray(xs) >= start) & (np.asarray(xs) <= end)]
    return float(np.max(inside)) if len(inside) else None


def _bracket_base(layers, tops: dict, start: float, end: float, high: float) -> float:
    """The top of the data a bracket spans; the panel's own top without it."""

    spanned = [top for position, top in tops.items() if start <= position <= end]
    spanned += [
        top
        for top in (_span_top(layer, start, end) for layer in layers)
        if top is not None
    ]
    return max(spanned) if spanned else high


def _bracket_tick_tip(ax: plt.Axes, point: tuple, horizontal: bool, length: float):
    """`point` moved `length` points toward the data, on the value axis.

    Measured through the display transform at the bracket's own position, so
    the tick holds its length on a non-linear value axis too.
    """

    x, y = ax.transData.transform(point)
    offset = length * ax.figure.dpi / 72
    moved = (x - offset, y) if horizontal else (x, y - offset)
    return ax.transData.inverted().transform(moved)[0 if horizontal else 1]


def _value_limits(ax: plt.Axes, horizontal: bool) -> tuple:
    """The axes' limits on the value axis, whichever way the panel runs."""

    return ax.get_xlim() if horizontal else ax.get_ylim()


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


# the compass anchor of each legend location code, 1 to 10
_LEGEND_ANCHORS = (None, "NE", "NW", "SW", "SE", "E", "W", "E", "S", "N", "C")


def _anchored_legend_origin(legend: Legend, code: int, size, parent, renderer):
    """The lower-left corner of a legend box of `size` placed in `parent` at `code`.

    The box sits against the location code's side or corner of the parent,
    inset by the legend's border-axes padding, as matplotlib places a legend.
    """

    pad = legend.borderaxespad * renderer.points_to_pixels(
        legend.prop.get_size_in_points()
    )
    container = parent.padded(-pad, -pad)
    return size.anchored(_LEGEND_ANCHORS[code], container=container).p0


def _fit_legend(
    legend: Legend, axes: list, dim: int, renderer, mirror: bool = False
) -> None:
    """Give a best-placed legend a clear slot at the end of the value axis.

    matplotlib picks the least-covered slot, which still hides marks when they
    fill the axes. The legend then moves to the slot along the value-axis end
    (top for a vertical panel, right for a horizontal one) whose marks reach
    least far, and every axes extends its value range so those marks end below
    the legend. Runs at draw time, once constrained layout has sized the axes.
    A fit that would squeeze the marks past LEGEND_HEADROOM_MAX keeps
    matplotlib's slot; the translucent frame still shows what it covers. A
    `mirror` axis, symmetric around zero, extends both of its halves.
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
    # the fixed point as the range scales: its low end, or a mirror's zero
    origin = axes[0].transData.transform((0, 0))[dim] if mirror else a0
    best = None
    for name in names:
        code = Legend.codes[name]
        l, b = _anchored_legend_origin(legend, code, size, anchor, renderer)
        slot = Bbox.from_bounds(l, b, box.width, box.height)
        reach = _marks_reach(slot, dim, bboxes, lines, offsets)
        reach = a0 if reach is None else min(reach, a1)
        floor = slot.get_points()[0, dim] - pad
        if floor <= origin:
            continue
        # scale the value range so the marks' reach maps just below the legend
        factor = max(1.0, (reach - origin) / (floor - origin))
        if best is None or factor < best[0]:
            best = (factor, code)
    if best is None or best[0] - 1 > LEGEND_HEADROOM_MAX:
        return
    factor, code = best
    for a in axes:
        axis = a.yaxis if dim == 1 else a.xaxis
        trans = axis.get_transform()
        lo, hi = a.get_ylim() if dim == 1 else a.get_xlim()
        if mirror:
            lo, hi = -hi * factor, hi * factor
        else:
            lo, hi = trans.transform([lo, hi])
            lo, hi = trans.inverted().transform([lo, lo + (hi - lo) * factor])
        (a.set_ylim if dim == 1 else a.set_xlim)(lo, hi)
    legend._set_loc(code)


def _axis_numbers(ax, transpose: bool, x) -> np.ndarray:
    """The drawn x data in axis units, so fits run on numbers when x is temporal."""

    axis = ax.yaxis if transpose else ax.xaxis
    return np.asarray(axis.convert_units(x), dtype=float)


def _masked_errors(errors: dict, mask) -> dict:
    """The error distances of the points `mask` picks, per axis."""

    return {
        axis: None if distances is None else distances[:, mask]
        for axis, distances in errors.items()
    }


def _spread_labels(labels: list, horizontal: bool) -> None:
    """Nudge overlapping annotations apart along the value axis.

    The value axis is y, or x when `horizontal`. Each label keeps its data
    anchor and moves only its point offset, which is centred on the anchor
    along that axis; a pair that overlaps splits the overlap between them,
    repeated until none is left.
    """

    axis = 0 if horizontal else 1
    px_per_pt = labels[0].figure.dpi / 72.0
    anchors, offsets, sizes = [], [], []
    for label in labels:
        anchors.append(label.axes.transData.transform(label.xy)[axis])
        offsets.append(label.xyann[axis] * px_per_pt)
        width, height = _text_size(label.get_fontsize(), label.get_text())
        sizes.append((width if horizontal else height) * px_per_pt)
    anchors, sizes = np.asarray(anchors), np.asarray(sizes)
    centers = anchors + np.asarray(offsets)
    order = np.argsort(centers, kind="stable")
    for _ in range(END_LABEL_SPREAD_PASSES * len(labels)):
        moved = False
        for a, b in zip(order[:-1], order[1:]):
            overlap = (sizes[a] + sizes[b]) / 2 - (centers[b] - centers[a])
            if overlap > POINT_LABEL_CLEAR:
                centers[a] -= overlap / 2
                centers[b] += overlap / 2
                moved = True
        if not moved:
            break
    for label, anchor, center in zip(labels, anchors, centers):
        offset = list(label.xyann)
        offset[axis] = (center - anchor) / px_per_pt
        label.xyann = tuple(offset)


class ScatterLayer(UnclippedMarksMixin, PointLabelMixin, Layer):
    kind = "scatter"
    record_roles_beat_layer = True

    def _resolve_style(self):
        self.scatter_style = get_scatter_style(self.style)
        self.error_style = get_scatter_error_style(self.style)
        # a point carrying the key gets its bar unless the front says otherwise
        self.show_errors = {
            axis: self.settings.get(f"show_{axis}") is not False for axis in ERROR_KEYS
        }
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
                config["color_general_multiple"], len(unique_hues), "hue levels"
            )
            self.hue_colors = [cycle[i]["color"] for i in range(len(unique_hues))]

    def y_range(self):
        return _present_range(get_chart_data("y", self.chart))

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

    def _point_column(self, key: str, n: int) -> Optional[list]:
        """One raw value per drawn point (None where the key is absent), or None.

        The records keyed by `x` are the drawn points; a column that names a
        different number of them names none of them.
        """

        values = [record.get(key) for record in _keyed_records(self.chart, "x")]
        if len(values) != n or all(value is None for value in values):
            return None
        return values

    def _point_labels(self, x_data) -> Optional[np.ndarray]:
        """One label per drawn point (None where the key is absent), or None."""

        labels = self._point_column("annotation", len(x_data))
        if labels is None:
            return None
        return np.array([None if l is None else str(l) for l in labels], dtype=object)

    def _error_distances(self, axis: str, n: int) -> Optional[np.ndarray]:
        """The `(2, n)` low/high distances of `axis`, NaN where a point has none."""

        if not self.show_errors[axis]:
            return None
        values = self._point_column(axis, n)
        if values is None:
            return None
        pairs = validate_error_distances(values, axis)
        return np.array(
            [(np.nan, np.nan) if pair is None else pair for pair in pairs], dtype=float
        ).T

    def _draw_errors(self, ax, ctx, x, y, sizes, errors: dict, style: dict) -> None:
        """One bar per point per side, each running from its marker's edge outward.

        A translucent marker shows whatever is drawn under it, so the bar
        stops at the marker rather than crossing it; the gap is the marker's
        radius in points, which the patch resolves at draw time and so keeps
        whatever the axes do afterwards. The bar wears the color the markers
        took, so a hue group's bars match it and a muted role's bars dim with
        it (ADR 0057).
        """

        color = self.error_style.get("ecolor") or style.get("c")
        capsize = self.error_style.get("capsize") or 0
        arrowstyle = ERROR_CAP_STYLE.format(width=2 * capsize) if capsize else "-"
        radii = np.broadcast_to(
            np.sqrt(np.asarray(sizes, dtype=float)) / 2, np.shape(x)
        )
        px, py = (y, x) if ctx.transpose else (x, y)
        px = np.asarray(ax.xaxis.convert_units(px), dtype=float)
        py = np.asarray(ax.yaxis.convert_units(py), dtype=float)
        ends = []
        for axis, distances in errors.items():
            if distances is None:
                continue
            step = (
                (1.0, 0.0)
                if _drawn_error_axis(axis, ctx.transpose) == "xerr"
                else (0.0, 1.0)
            )
            for index in np.flatnonzero(~np.isnan(distances[0])):
                point = np.array([px[index], py[index]])
                for reach in (-distances[0][index], distances[1][index]):
                    if reach == 0:
                        continue
                    end = point + reach * np.array(step)
                    ends.append(end)
                    ax.add_patch(
                        FancyArrowPatch(
                            point,
                            end,
                            arrowstyle=arrowstyle,
                            mutation_scale=1,
                            shrinkA=radii[index],
                            shrinkB=0,
                            color=color,
                            linewidth=self.error_style.get("elinewidth"),
                            alpha=style.get("alpha"),
                            zorder=style.get("zorder", 0) - ERROR_BAR_Z_STEP,
                        )
                    )
        # a patch draws where it is put; the axes learn the reach from the ends
        if ends:
            ax.update_datalim(ends)

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
        x_log = ctx.category_scale == AXIS_SCALE.LOG
        y_log = ctx.value_scale == AXIS_SCALE.LOG
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
        from ...stats import pearson

        r = pearson(x, y)
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

    def target_extent(self, ax, point) -> Optional[float]:
        """The radius of the marker `point` sits on; a connector stops in it."""

        return self.mark_radius(ax, point)

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
        errors = {axis: self._error_distances(axis, len(x_data)) for axis in ERROR_KEYS}
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
                errors=_masked_errors(errors, mask),
            )

        if not (self.show_regression or self.show_correlation):
            return
        x_fit = _axis_numbers(ax, ctx.transpose, x_data)
        y_fit = np.asarray(y_data, dtype=float)
        # a point missing a coordinate stays out of the fit and the correlation
        present = np.isfinite(x_fit) & np.isfinite(y_fit)
        if not present.any():
            raise ValueError(
                f"The scatter chart `{self.label(ctx)}` has no point with finite "
                "`x` and `y` values to fit."
            )
        x_fit, y_fit = x_fit[present], y_fit[present]
        if hue_data is not None:
            if self.show_correlation:
                self._draw_correlation(ax, x_fit, y_fit, color=None)
            if self.show_regression:
                self._draw_regression(ax, ctx, x_fit, y_fit, color=None)
            return
        color = (
            self.muted_color if ctx.emphasis == EMPHASIS_BACKGROUND else series_color
        )
        if self.show_regression:
            self._draw_regression(ax, ctx, x_fit, y_fit, color=color)
        if self.show_correlation:
            self._draw_correlation(ax, x_data[present], y_fit, color=color)

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
        errors,
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
            role_errors = _masked_errors(errors, picked)
            self._draw_errors(
                ax, ctx, x[picked], y[picked], role_sizes, role_errors, style
            )
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
                _point_resolver(
                    label, x[picked], y[picked], ctx.transpose, role_errors
                ),
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
    """A group chart's drawn records keyed by label, in first-seen label order.

    Records without a value are left out, NaN like None.
    """

    grouped = {}
    data = chart.get("data", [])
    if isinstance(data, list):
        for d in data:
            if d.get("label") is not None and not is_missing(d.get("value")):
                grouped.setdefault(d["label"], []).append(d)
    return grouped


def grouped_values(chart: dict) -> dict:
    """A group chart's values keyed by label, in first-seen label order."""

    return {
        label: [d["value"] for d in records]
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

    def warn_without_records(self, name: str) -> None:
        """Warn that the layer was given no records.

        Records whose values are all missing draw nothing, silently.
        """

        if not self.chart.get("data"):
            warnings.warn(f"No data points found for {name}.")

    def _resolve_style(self):
        if self.sorts_by_median:
            self.sort = self.settings.get("sort")
        self.orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.is_horizontal = self.orientation == ORIENTATION.HORIZONTAL
        # a raincloud colors its groups from the multiple palette (ADR 0021);
        # the cycle is built once so sibling layers of one chart agree
        self.color_by_group = bool(self.settings.get("color_by_group"))
        self.group_colors = (
            create_color_cycle(
                config["color_general_multiple"], max(len(self.labels()), 1), "groups"
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
        return _present_range(self.value_data())

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
            self.warn_without_records("box plot")
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
        self.swarm_mode = self.settings.get("swarm_mode") or DEFAULT_SWARM_MODE
        jitter = theme_default(None, self.settings, "jitter")
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
            self.warn_without_records("swarm plot")
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
            if layer.swarm_mode == SWARM_MODE.STRIP:
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

    sort = settings.get("sort")
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
        # the front validated the kind and filled its default
        self.value_mode = resolve_value_kind(self.settings)
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
        inner = VIOLIN_INNER.check(
            theme_default("violinplot", self.settings, "inner") or VIOLIN_INNER.DEFAULT,
            # the front checks a call's inner; only a theme's fails here
            "chart_default_violin_inner",
        )
        self.inner = None if inner == VIOLIN_INNER.NO_INNER else inner
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

        data = self.chart.get("data", [])
        grouped, split_values = {}, []
        if isinstance(data, list):
            for d in data:
                lbl, val = d.get("label"), d.get("value")
                if lbl is None or is_missing(val):
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
            self.warn_without_records("violin plot")
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
        if np.ptp(values) == 0:
            body = self._flat_body(ax, values[0], position, width)
        else:
            if scale == AXIS_SCALE.LOG:
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

    def _flat_body(self, ax, value, position, width) -> PolyCollection:
        """Values without spread have no density: a line across the body width."""

        ends = [(position - width / 2, value), (position + width / 2, value)]
        if self.is_horizontal:
            ends = [(v, c) for c, v in ends]
        body = PolyCollection([ends], closed=False)
        ax.add_collection(body)
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

        # marks span the body width at their value; flat, the full width
        flat = np.ptp(values) == 0
        if not flat:
            kde = GaussianKDE(values, self.bandwidth)
            grid = np.linspace(values.min(), values.max(), 100)
            peak = float(kde.evaluate(grid).max()) or 1.0

        def span(value, linestyle):
            h = width / 2
            if not flat:
                h *= float(kde.evaluate([value])[0]) / peak
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
        inner = self.settings.get("inner")
        self.inner = None if inner == VIOLIN_INNER.NO_INNER else inner
        self.ridge_scale = self.settings.get("ridge_scale") or RIDGELINE_SCALE.DEFAULT
        self.fill = theme_default("ridgelineplot", self.settings, "fill") is not False
        self.show_outline = (
            theme_default("ridgelineplot", self.settings, "show_outline") is not False
        )
        validate_ridge_marks(self.fill, self.show_outline)
        self.ridge_style = get_ridgeline_style(self.style)
        self.overlap = validate_overlap(
            theme_default("ridgelineplot", self.settings, "overlap", self.style)
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
            log = self.settings.get("scaley") == AXIS_SCALE.LOG
        ends = []
        for values in self.grouped_values().values():
            if len(values) < 2:
                continue
            fit = np.log10(values) if log else np.asarray(values, dtype=float)
            if np.ptp(fit) == 0:
                ends.append((fit[0], fit[0]))
                continue
            curve = kde1d(fit, bandwidth=self.bandwidth, grid_size=2)
            ends.append((curve["x"][0], curve["x"][-1]))
        if not ends:
            return None
        lo, hi = min(e[0] for e in ends), max(e[1] for e in ends)
        if lo == hi:
            # rows without spread alone: a unit of room around their value
            lo, hi = lo - 0.5, hi + 0.5
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
        lo, hi = _widen_to_ticks(ticks, lo, hi)
        axis = "x" if self.is_horizontal else "y"
        low, high = self.settings.get(f"{axis}min"), self.settings.get(f"{axis}max")
        return (lo if low is None else low, hi if high is None else high)

    def draw(self, ax, ctx):
        grouped = self.grouped_values()
        if not grouped:
            self.warn_without_records("ridgeline plot")
            return
        for label, values in grouped.items():
            if len(values) < 2:
                raise ValueError(
                    f"Ridge {label!r} needs at least two values to estimate a density."
                )

        roles = self.label_roles(ctx.emphasis)

        # on a log value axis the densities are estimated on log10 values
        log = ctx.value_scale == AXIS_SCALE.LOG
        lo, hi = self._grid_bounds(log)
        if log:
            grouped_fit = {k: np.log10(v) for k, v in grouped.items()}
            lo, hi = np.log10(lo), np.log10(hi)
        else:
            grouped_fit = grouped
        grid = np.linspace(lo, hi, RIDGE_GRIDSIZE)
        densities = [self._density(values, lo, hi) for values in grouped_fit.values()]
        if log:
            grid = np.power(10.0, grid)
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
                if self.ridge_scale == RIDGELINE_SCALE.COMMON
                else density.max()
            )
            heights = density / (float(scale) or 1.0) * peak
            position = ctx.category_index[label]
            baseline = position
            tops = baseline + rise * heights
            flat = np.ptp(values) == 0
            # a flat row's marks rise to the line standing in for its ridge
            inner_tops = np.full_like(grid, baseline + rise * peak) if flat else tops
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
            if flat:
                # a line at the value, the height of a full ridge, stands in
                value = values[0]
                xs, ys = [value, value], [baseline, inner_tops[0]]
                spike = ax.plot(
                    *((xs, ys) if self.is_horizontal else (ys, xs)),
                    color=edgecolor,
                    linewidth=style.get("linewidth"),
                    zorder=zorder + 2 * step / 3,
                )[0]
                artists.insert(0, ("outline", spike))
            artists += [
                ("mark", mark)
                for mark in self._draw_inner(
                    ax,
                    values,
                    grid,
                    baseline,
                    inner_tops,
                    zorder + step / 3,
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

    def _density(self, values, lo: float, hi: float) -> np.ndarray:
        """The row's density on the shared grid; a row without spread has none."""

        if np.ptp(values) == 0:
            return np.zeros(RIDGE_GRIDSIZE)
        curve = kde1d(
            values, bandwidth=self.bandwidth, grid_size=RIDGE_GRIDSIZE, xlim=(lo, hi)
        )
        return np.array(curve["y"])

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


COLORBAR_PAD = 0.03


def _draw_colorbar(
    ax: plt.Axes,
    mappable,
    setting: dict,
    aspect_locked: bool = False,
    centre: Optional[float] = None,
) -> None:
    """Draw a colorbar on the edge the resolved setting names (ADR 0035).

    `centre` is the value a centred norm holds fixed: the bar marks it
    alongside its even ticks, so the sign reads off the scale (ADR 0056).
    A `ticks` setting is the user's own list and replaces both.
    """

    colorbar = _place_colorbar(ax, mappable, setting, aspect_locked)
    fmt = _value_formatter(setting["format"])
    if fmt is not None:
        colorbar.formatter = fmt
        colorbar.update_ticks()
    ticks = setting["ticks"]
    if ticks is None and centre is not None:
        ticks = sorted(set(colorbar.get_ticks()) | {centre})
    if ticks is not None:
        # set_ticks widens the bar to every tick; keep it to the mapped range
        low, high = colorbar.vmin, colorbar.vmax
        slack = (high - low) * 1e-9
        colorbar.set_ticks([t for t in ticks if low - slack <= t <= high + slack])
    if setting["label"]:
        colorbar.set_label(setting["label"], **setting["label_style"])
    furniture = setting["furniture"]
    ticks_style = {"labelcolor": furniture["labelcolor"]}
    if furniture["color"] is not None:
        ticks_style["color"] = furniture["color"]
    colorbar.ax.tick_params(which="both", **ticks_style)
    if furniture["outline"] is not None:
        colorbar.outline.set_edgecolor(furniture["outline"])
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


def _value_formatter(valfmt):
    """A value format as a matplotlib formatter; None keeps the default.

    Takes all `_format_value` takes, so ticks print as value labels do,
    with the typographic minus of matplotlib's own formatters.
    """

    if valfmt is None or isinstance(valfmt, mticker.Formatter):
        return valfmt
    return mticker.FuncFormatter(
        lambda value, _pos=None: mticker.Formatter.fix_minus(
            _format_value(valfmt, value)
        )
    )


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


def _luminance(rgba) -> float:
    """The perceived brightness of a color, 0 (black) to 1 (white)."""

    r, g, b = rgba[:3]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def colormap_scaling(chart: dict) -> dict:
    """The `norm`, `vmin` and `vmax` a colormapped draw call takes.

    A centred norm is an instance holding `vcenter` in the middle of the
    colormap and carrying the bounds itself: `centered` folds them into one
    half-range each side of `vcenter`, `twoslope` keeps them apart.
    Any other norm passes by name beside the bounds.
    """

    norm, vmin, vmax = chart.get("norm"), chart.get("vmin"), chart.get("vmax")
    if norm not in CENTRED_NORMS:
        return {"norm": norm, "vmin": vmin, "vmax": vmax}
    vcenter = chart.get("vcenter")
    vcenter = 0.0 if vcenter is None else vcenter
    if norm == COLOR_NORM.TWOSLOPE:
        validate_two_slope_bounds(vcenter, vmin, vmax)
        return {"norm": TwoSlopeNorm(vcenter, vmin, vmax)}
    halfrange = max(
        (abs(bound - vcenter) for bound in (vmin, vmax) if bound is not None),
        default=None,
    )
    return {"norm": CenteredNorm(vcenter, halfrange)}


class HeatmapLayer(Layer):
    ticks_at_axis_ends = False
    kind = "heatmap"
    overlayable = False
    # the theme keys the cells, values, and borders read
    style_prefix = "plot_heatmap"

    def _resolve_style(self):
        self.show_colorbar = self.settings.get("show_colorbar")
        self.colorbar = get_colorbar_setting(self.chart.get("colorbar"))
        self.colorbar_edge = self._colorbar_edge(self.show_colorbar)
        self.centred = self.chart.get("norm") in CENTRED_NORMS
        self.scaling = colormap_scaling(self.chart)
        self.vcenter = self.scaling["norm"].vcenter if self.centred else None
        # every centred norm maps its centre to the middle of the colormap
        self.step_centre = 0.5 if self.centred else None
        heatmap_style = get_heatmap_style(self.style, self.style_prefix, self.centred)
        heatmap_style["cmap"] = get_colormap(heatmap_style["cmap"])
        self.heatmap_style = heatmap_style
        self.font_style = get_heatmap_font_style(self.style, self.style_prefix)
        self.edge_style = get_heatmap_edge_style(self.style, self.style_prefix)
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
        """The cell value switch, as set or the theme default, and its text."""

        self.show_cell_values = bool(resolve_show_values(self.settings))
        formatter = _value_formatter(
            self.chart.get("value_format", DEFAULT_VALUE_FORMAT)
        )
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

    def target_extent(self, ax, point) -> Optional[float]:
        """Half the smaller side of the cell holding `point`, in points.

        `imshow` centers cell (row, col) on (col, row), so a point rounds
        to its cell and the borders sit half a unit out.
        """

        col, row = round(point[0]), round(point[1])
        n_rows, n_cols = len(self.z), len(self.z[0]) if self.z else 0
        if not (0 <= row < n_rows and 0 <= col < n_cols):
            return None
        value = self.z[row][col]
        # a blank cell (off the calendar year, or a gap) draws no mark
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return None
        corners = ax.transData.transform(
            [(col - 0.5, row - 0.5), (col + 0.5, row + 0.5)]
        )
        width, height = np.abs(corners[1] - corners[0])
        return _px_to_points(ax, min(width, height) / 2)

    def draw(self, ax, ctx):
        data = self.z

        # the panel owns the aspect; imshow's own "equal" would size the
        # colorbar to a box the panel then stretches
        im = ax.imshow(
            data,
            aspect="auto",
            **self.scaling,
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

        if self.show_colorbar and self.value_etch_steps:
            self._draw_even_step_legend(ax, im.norm, self.colorbar["label"])
        elif self.show_colorbar:
            _draw_colorbar(ax, im, self.colorbar, ctx.aspect_locked, self.vcenter)

        self._draw_frame(ax)

    def _draw_cell_steps(self, ax, im) -> None:
        """The cells as etched value steps over the image, left clear for hover."""

        im.autoscale_None()
        values = np.asarray(self.z, dtype=float)
        steps = value_steps(
            im.norm(np.ma.masked_invalid(values)),
            len(self.value_etch_steps),
            self.step_centre,
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
        # an array: the image may already hold the per-cell fade array
        im.set_alpha(np.zeros(values.shape))

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

        tab = get_value_label_style(self.style).get("tab")
        if self.value_etch_steps:
            im.autoscale_None()
            steps = value_steps(
                im.norm(np.ma.masked_invalid(np.asarray(self.z, dtype=float))),
                len(self.value_etch_steps),
                self.step_centre,
            )
        for i, row in enumerate(self.z):
            for j, value in enumerate(row):
                if np.isnan(value):
                    continue
                font_style = dict(self.font_style)
                # a faded cell is light whatever its value
                if (
                    self.cell_roles[i][j] != EMPHASIS_BACKGROUND
                    and _luminance(im.cmap(im.norm(value)))
                    < HEATMAP_TEXT_DARK_LUMINANCE
                ):
                    font_style["color"] = "#FFFFFF"
                if self.value_etch_steps:
                    # a value over the etching reads through a halo of the
                    # ground, or a tab where the etching is lines that cross it
                    font_style["color"] = self.font_style.get("color")
                    hatch = self.value_etch_steps[steps[i][j]][1]
                    if tab and set(hatch) & set("/\\x+|-"):
                        font_style["bbox"] = _value_tab_bbox(tab)
                    else:
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
        self.week_start = (
            theme_default("calendarheatmap", self.settings, "week_start", self.style)
            or CALENDAR_WEEKDAY.DEFAULT
        )
        self.month_line_style = get_calendar_month_line_style(self.style)
        self.show_month_labels = _resolve_flag(self.settings, "show_month_labels")
        self.show_weekday_labels = _resolve_flag(self.settings, "show_weekday_labels")
        super()._resolve_style()

    def _resolve_cell_values(self) -> None:
        """The shared `show_values` and `value_format` vocabulary (ADR 0033)."""

        self.show_cell_values = resolve_show_values(self.settings)
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
        self.fill = bool(self.settings.get("fill"))
        self.surface = self.fill
        self.show_labels = self.settings.get("show_labels")
        self.show_colorbar = self.settings.get("show_colorbar")
        self.colorbar = get_colorbar_setting(self.chart.get("colorbar"))
        self.colorbar_edge = self._colorbar_edge(self.fill and self.show_colorbar)
        style = get_contour_style(self.style)
        self.centred = self.chart.get("norm") in CENTRED_NORMS
        self.scaling = colormap_scaling(self.chart)
        self.vcenter = self.scaling["norm"].vcenter if self.centred else None
        cmap = style.pop("cmap")
        if self.centred:
            cmap = get_heatmap_cmap(self.style, "plot_contour", diverging=True)
        self.cmap = get_colormap(cmap)
        # lines take a pinned contour cmap only, past its washed-out low end
        self.line_cmap = None
        cmap_pinned = get_attr_value("plot_contour_cmap", self.style, config)
        if not self.fill and cmap_pinned is not None:
            self.line_cmap = LinearSegmentedColormap.from_list(
                f"{self.cmap.name}_lines",
                self.cmap(np.linspace(CONTOUR_LINE_CMAP_START, 1, 256)),
            )
        self.contour_style = style
        self.label_style = get_contour_label_style(self.style)
        # clabel takes no font family; the level labels are restyled after
        self.label_family = resolve_font_family()
        self.x, self.y, self.z = self._grid()
        # a grid of missing values alone draws nothing
        self.empty = not np.isfinite(self.z).any()
        if self.empty:
            self.levels, self.extend, self.band_edges = None, "neither", None
            return
        self.levels = contour_levels(self.z, self.settings.get("levels"))
        if self.fill:
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
        if self.empty:
            return
        style = dict(self.contour_style)
        if ctx.z_order is not None:
            style["zorder"] = ctx.z_order
        scaling = dict(self.scaling)
        label = self.label(ctx)

        if self.fill:
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
            elif self.show_colorbar:
                _draw_colorbar(
                    ax, bands, self.colorbar, ctx.aspect_locked, self.vcenter
                )
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
        if not self.show_colorbar:
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
        scaling = dict(self.scaling)
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
            fmt = _value_formatter(self.chart.get("value_format"))
            if fmt is not None:
                label_style["fmt"] = fmt
            if ctx.emphasis == EMPHASIS_BACKGROUND:
                label_style["colors"] = self.muted_color
            # a relief's labels sit over the etching and read through a halo
            halo = self.value_halo if self.fill and self.value_etch_steps else []
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
        self.show_colorbar = self.settings.get("show_colorbar")
        # value_format is the tick format the colorbar setting falls back on
        self.colorbar = get_colorbar_setting(
            self.chart.get("colorbar"), self.chart.get("value_format")
        )
        self.colorbar_edge = self._colorbar_edge(self.show_colorbar)
        self.centred = self.chart.get("norm") in CENTRED_NORMS
        self.scaling = colormap_scaling(self.chart)
        self.vcenter = self.scaling["norm"].vcenter if self.centred else None
        style = get_hexbin_style(self.style)
        if self.centred:
            style["cmap"] = get_heatmap_cmap(self.style, "plot_hexbin", diverging=True)
        style["cmap"] = get_colormap(style["cmap"])
        self.hexbin_style = style
        self.x, self.y, self.c = self._columns()
        self.grid_size = self.chart.get("grid_size")
        if self.grid_size is None:
            self.grid_size = get_attr_value("plot_hexbin_gridsize", self.style, config)
        self.min_count = self.chart.get("min_count")
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
            gridsize=self.grid_size,
            # hexagons bin in the axes' scale; a later log scale would warp them
            xscale="log" if ctx.category_scale == AXIS_SCALE.LOG else "linear",
            yscale="log" if ctx.value_scale == AXIS_SCALE.LOG else "linear",
            reduce_C_function=self.reduce,
            mincnt=self.min_count,
            **self.scaling,
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
        if self.show_colorbar and self.value_etch_steps:
            self._draw_even_step_legend(ax, tiles.norm, self.colorbar["label"])
        elif self.show_colorbar:
            _draw_colorbar(ax, tiles, self.colorbar, ctx.aspect_locked, self.vcenter)

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


class DrawPositionLayer(Layer):
    """A layer that carries no series, on the rung its `DRAW_POSITION` picks.

    Takes no cycle color, no legend entry and no emphasis (ADR 0054, 0060).
    """

    takes_color = False
    position: str = DRAW_POSITION.DEFAULT

    @property
    def zorder_key(self) -> str:
        return draw_zorder_key(self.position)

    def rung(self, ctx) -> float:
        """The layer's zorder: its position's rung unless the panel set one."""

        return DRAW_ZORDER[self.position] if ctx.z_order is None else ctx.z_order


class ImageLayer(DrawPositionLayer):
    """A picture stretched over its extent in data coordinates (ADR 0060)."""

    # the picture fills its extent; the axes end where it does
    ticks_at_axis_ends = False

    kind = "image"

    def _resolve_style(self):
        data = self.chart.get("data") or {}
        self.image = validate_image(data.get("image"))
        self.extent = validate_image_extent(data.get("extent"))
        self.position = self.settings.get("position") or DRAW_POSITION.DEFAULT
        style = get_image_style(self.style)
        if self.image.ndim == 2:
            style["cmap"] = get_colormap(style["cmap"])
            style["vmin"] = self.settings.get("vmin")
            style["vmax"] = self.settings.get("vmax")
        else:
            # an RGB(A) picture carries its own colors
            style.pop("cmap", None)
        self.image_style = style

    def value_data(self):
        return np.array(self.extent[2:])

    def category_data(self):
        return np.array(self.extent[:2])

    def draw(self, ax, ctx):
        z_order = self.rung(ctx)
        ax.imshow(
            self.image,
            extent=self.extent,
            origin="upper",
            zorder=z_order,
            **self.image_style,
        )
        # imshow pins the view to the extent; earlier marks must count too
        ax.autoscale_view()


class BasemapLayer(DrawPositionLayer):
    """Coastlines, land, borders, lakes, rivers and roads in longitude and
    latitude (ADR 0062).

    Composed with data it leaves the limits to the data; alone it frames its
    own outlines.
    """

    kind = "basemap"

    def _resolve_style(self):
        data = self.chart.get("data") or {}
        geometry = data.get("geometry")
        validate_basemap_source(
            data.get("features"),
            geometry,
            data.get("resolution"),
            data.get("highlight"),
        )
        self.highlight = ()
        if geometry is None:
            features = validate_basemap_features(data.get("features"))
            resolution = data.get("resolution") or BASEMAP_RESOLUTION.DEFAULT
            validate_basemap_availability(features, resolution)
            outlines = [(f, load_basemap(f, resolution)) for f in features]
            self.highlight = validate_basemap_highlight(data.get("highlight"), features)
            if BASEMAP_FEATURE.COUNTRIES in features:
                self.country_codes = load_country_codes(resolution)
                self._warn_missing_countries(resolution)
        else:
            outlines = validate_basemap_geometry(geometry)
        # bottom up, the caller's order kept within one feature
        self.outlines = sorted(outlines, key=lambda o: BASEMAP_FEATURES.index(o[0]))
        self.position = self.settings.get("position") or DRAW_POSITION.DEFAULT
        self.feature_style = get_basemap_style(self.style)
        lakes = self.feature_style[BASEMAP_FEATURE.LAKES]
        lakes.setdefault("facecolor", self.ground)

    def _warn_missing_countries(self, resolution: str) -> None:
        """Warn about highlighted codes the map at this scale does not draw."""

        missing = sorted(set(self.highlight) - set(self.country_codes))
        if missing:
            warnings.warn(
                f"The basemap at 1:{resolution} draws no country coded "
                f"{missing}: too small at this scale, or not a Natural Earth "
                "ADM0_A3 code. A finer `resolution` may draw it."
            )

    def _draw_countries(self, ax, rows, z_order) -> list:
        """One patch per country, so an enclave keeps its own fill.

        Returns the paths of the highlighted countries, for their outline.
        """

        style = self.feature_style[BASEMAP_FEATURE.COUNTRIES]
        rings = defaultdict(list)
        for code, ring in zip(self.country_codes, _split_outlines(rows)):
            rings[code].append(ring)
        codes = list(rings)
        faces = [
            style["highlight"] if code in self.highlight else style["facecolor"]
            for code in codes
        ]
        paths = [_filled_path(rings[code]) for code in codes]
        ax.add_collection(
            PatchCollection(
                [PathPatch(path) for path in paths],
                facecolors=faces,
                edgecolors="none",
                zorder=z_order,
            ),
            autolim=False,
        )
        return [path for code, path in zip(codes, paths) if code in self.highlight]

    def bounds(self) -> tuple:
        """The `(xmin, xmax, ymin, ymax)` the outlines span."""

        rows = np.concatenate([rows for _, rows in self.outlines])
        rows = rows[np.isfinite(rows).all(axis=1)]
        (x0, y0), (x1, y1) = rows.min(axis=0), rows.max(axis=0)
        return float(x0), float(x1), float(y0), float(y1)

    def draw(self, ax, ctx):
        z_order = self.rung(ctx)
        highlighted = []
        for feature, rows in self.outlines:
            if feature == BASEMAP_FEATURE.COUNTRIES:
                highlighted = self._draw_countries(ax, rows, z_order)
                continue
            outlines = _split_outlines(rows)
            style = self.feature_style[feature]
            # a basemap never widens the view; a lone one frames it in render
            if feature in BASEMAP_FILLED:
                # add_artist, unlike add_patch, leaves the data limits alone
                ax.add_artist(
                    PathPatch(
                        _filled_path(outlines),
                        edgecolor="none",
                        zorder=z_order,
                        **style,
                    )
                )
            else:
                ax.add_collection(
                    LineCollection(outlines, zorder=z_order, **style), autolim=False
                )
        edge = self.feature_style[BASEMAP_FEATURE.COUNTRIES]
        if highlighted and edge.get("edge_width"):
            # added last, so the borders and the coastline never cross it
            ax.add_collection(
                PatchCollection(
                    [PathPatch(path) for path in highlighted],
                    facecolors="none",
                    edgecolors=edge["edge_color"],
                    linewidths=edge["edge_width"],
                    zorder=z_order,
                ),
                autolim=False,
            )


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
                self.row_emphasis.extend([roles] * n_rows)
            else:
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
                get_value_label_style(shared_style).get("halo_width"), self.ground
            )
        )
        self.dim_label_style = get_parallel_dim_label_style(shared_style)
        self.dim_label_rotation = get_parallel_dim_label_rotation(shared_style)
        self.dim_label_pad = get_parallel_dim_label_pad(shared_style)
        self.hue_palette = (
            config.get("color_parallel_hue") or config["color_general_multiple"]
        )

        # per-line styles are shared per source chart
        self.line_styles = [
            get_parallel_coords_style(c.get("style", {}) or {}) for c in self.charts
        ]

        all_hues = []
        for chart in self.charts:
            hue_attr = chart.get("hue", "hue")
            for d in chart.get("data", []):
                all_hues.append(d.get(hue_attr, None))

        non_null_hues = [h for h in all_hues if h is not None]
        self.continuous_hue = bool(non_null_hues) and all(
            is_number(h) for h in non_null_hues
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
            # the ramp spans every record: a rule mutes, it never rescales
            self.hue_min = float(min(non_null_hues))
            self.hue_max = float(max(non_null_hues))
            self.hue_colors = {}
            self.default_color = self.hue_cmap(0.5)
            self.unique_hues = []
            return

        # background rows are muted: they claim no hue color and no legend entry
        unique_hues = sorted(
            {
                h
                for h, role in zip(all_hues, self.row_emphasis)
                if h is not None and role != EMPHASIS_BACKGROUND
            }
        )

        if len(unique_hues) > 0:
            cycle = create_color_cycle(self.hue_palette, len(unique_hues), "hue levels")
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
        if not is_number(value):
            return np.nan
        range_val = stats["dim_max"][dim] - stats["dim_min"][dim]
        if range_val == 0:
            # one value sits mid-axis, on its single tick
            return 0.5
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
                ticks = [
                    (dim_category_map[dim][cat], text)
                    for cat, text in zip(categories, texts)
                ]
            else:
                dim_range = dim_max[dim] - dim_min[dim]
                values = stats["dim_ticks"].get(dim, []) if dim_range else []
                # a dimension holding one value keeps a single mid-axis tick
                ticks = (
                    [
                        ((value - dim_min[dim]) / dim_range, format_number(value))
                        for value in values
                    ]
                    if values
                    else [(0.5, format_number(dim_min[dim]))]
                )

            for tick_pos, text in ticks:
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


def _row_resolver(label, dimensions: list, row: dict) -> Callable[[int], dict]:
    """A parallel-coords row reports, under the axis nearest the pointer, its value there."""

    def resolve(index: int) -> dict:
        dim = dimensions[min(max(int(index), 0), len(dimensions) - 1)]
        return {"label": label, dim: row.get(dim)}

    return resolve


def _nice_dim_ticks(vmin: float, vmax: float) -> Tuple[float, float, List[float]]:
    """A numeric dimension's round tick values, and the span they enclose it with.

    The axis then starts and ends on a labelled round value, as a continuous
    cartesian axis does. A parallel axis carries no matplotlib axis of its own,
    so the ticks come straight from the locator. A locator that offers nothing
    to snap to leaves the axis on its data, labelled at both ends.
    """

    locator = MaxNLocator(nbins=5, steps=[1, 2, 2.5, 5, 10])
    ticks = np.asarray(locator.tick_values(vmin, vmax), dtype=float)
    if len(ticks) < 2:
        return vmin, vmax, [vmin, vmax]
    lo, hi = _widen_to_ticks(ticks, vmin, vmax)
    return lo, hi, [float(t) for t in ticks if lo <= t <= hi]


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
        # every key some record gives a value, in first-seen order
        hue_attr = layer.charts[0].get("hue", "hue")
        found = {}
        for chart in layer.charts:
            for d in chart.get("data", []) or []:
                found.update((k, None) for k, v in d.items() if v is not None)
        found.pop(hue_attr, None)
        return list(found)

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

    dim_min, dim_max, dim_ticks = {}, {}, {}
    for dim in dimensions:
        if dim_is_categorical[dim]:
            dim_min[dim] = 0
            dim_max[dim] = len(dim_categories[dim]) - 1
            continue
        vals = np.array(
            [v if is_number(v) else np.nan for v in dim_values_raw[dim]],
            dtype=float,
        )
        data_min, data_max = np.nanmin(vals), np.nanmax(vals)
        if data_min == data_max or not np.isfinite([data_min, data_max]).all():
            dim_min[dim], dim_max[dim], dim_ticks[dim] = data_min, data_max, []
        else:
            dim_min[dim], dim_max[dim], dim_ticks[dim] = _nice_dim_ticks(
                float(data_min), float(data_max)
            )

    return {
        "dimensions": dimensions,
        "is_categorical": dim_is_categorical,
        "categories": dim_categories,
        "category_map": dim_category_map,
        "dim_min": dim_min,
        "dim_max": dim_max,
        "dim_ticks": dim_ticks,
    }


# ================================================
# Radial Layers
# ================================================


def _radial_theta(n: int) -> np.ndarray:
    """Evenly spaced angular category positions, in radians."""

    return np.linspace(0, 2 * np.pi, n, endpoint=False)


def _on_spokes(values, positions, n: int, fill=np.nan, dtype=float) -> np.ndarray:
    """`values` spread over `n` spokes at `positions`; `fill` on the rest."""

    spread = np.full(n, fill, dtype=dtype)
    spread[positions] = values
    return spread


def _radial_spokes(labels, index: Optional[dict]) -> tuple:
    """Each label's spoke position and angle, and the spoke count (ADR 0079)."""

    positions = _category_positions(labels, index)
    n = len(index) if index else len(labels)
    return positions, _radial_theta(n)[positions], n


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
        return _present_range(get_chart_data("y", self.chart))

    def apply_scales(self, ax, scalex, scaley):
        # a polar axes rejects set_xscale; only the radial (value) axis scales
        if scaley:
            ax.set_yscale(scaley)


class RadialLineLayer(AreaFillMixin, RadialLayer):
    kind = "radial-line"
    color_style = "line_style"

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

        positions, angles, n = _radial_spokes(labels, ctx.category_index)
        self._tips = [
            (float(t), float(v), float(v), int(i))
            for i, t, v in zip(positions, angles, y)
        ]
        # a label the series lacks is a gap: the line breaks, inventing nothing
        theta = _radial_theta(n)
        y = _on_spokes(y, positions, n)
        spoke_labels = _on_spokes(labels, positions, n, fill=None, dtype=object)
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
        if (
            self.show_yerr
            and isinstance(yerr, np.ndarray)
            and len(yerr) == len(positions)
        ):
            yerr = _on_spokes(yerr, positions, n)
            yerr = np.append(yerr, yerr[0])
            band = ax.fill_between(
                theta, y - yerr, y + yerr, **self._resolved_area_style(ctx)
            )
            self._etch([band], wash=False)

        (line,) = ax.plot(theta, y, **line_style, label=self.label(ctx))
        self.register_hover(
            line, _radial_resolver(self.label(ctx), spoke_labels, y[:-1])
        )

        if self.show_area:
            # the fill reaches the center (or the inner_radius hole clips it)
            area = ax.fill_between(theta, 0.0, y, **self._resolved_area_style(ctx))
            self._etch([area], wash=False)


class RadialBarLayer(RadialLayer):
    kind = "radial-bar"
    color_style = "bar_style"
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

        positions, theta, n = _radial_spokes(labels, ctx.category_index)
        sector = 2 * np.pi / n

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
                int(i),
            )
            for i, t, r, v, role in zip(positions, theta, tops, y, roles)
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

        positions, theta, _ = _radial_spokes(labels, ctx.category_index)
        self._tips = [
            (float(t), float(v), float(v), int(i))
            for i, t, v in zip(positions, theta, y)
        ]
        points = ax.scatter(
            theta, y, label=self.label(ctx), **_hollow_marker(scatter_style)
        )
        self.register_hover(points, _radial_resolver(self.label(ctx), labels, y))


class RadialHistogramLayer(RadialLayer):
    kind = "radial-histogram"
    color_style = "hist_style"
    is_categorical = False

    def _resolve_style(self):
        hist_style = get_hist_style(self.style)
        # the rose draws through ax.bar; histtype/align are ax.hist-only knobs
        hist_style.pop("histtype", None)
        hist_style.pop("align", None)
        self.hist_style = hist_style
        self.num_bins = self.settings.get("num_bins") or DEFAULT_NUM_BINS

    def x_values(self) -> Optional[np.ndarray]:
        return get_chart_observations("x", self.chart)

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
    takes_color = False

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


def value_steps(normed, n: int, centre: Optional[float] = None) -> np.ndarray:
    """The step, 0 to `n - 1`, of each value normalized to [0, 1]; -1 where missing."""

    normed = np.ma.masked_invalid(np.ma.asarray(normed, dtype=float))
    values = normed.filled(0.0)
    if centre is None:
        steps = np.clip(np.floor(values * n), 0, n - 1).astype(int)
    else:
        inner = step_edges(n, centre)[1:-1]
        steps = np.clip(np.searchsorted(inner, values, side="right"), 0, n - 1)
    return np.where(np.ma.getmaskarray(normed), -1, steps)


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

    overlayable = False

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
        # a ribbon is a light wash the value reads on, so it takes no tab
        self.value_font.pop("bbox", None)
        # column headings read as per-column subtitles
        self.column_label_style = get_text_style("subtitle")
        # one color per node in first appearance across the links, so the
        # column order never recolors a node; unlinked nodes follow
        names = first_seen_nodes(self.links)
        names += [n for column in self.columns for n in column if n not in names]
        cycle = create_color_cycle(
            config["color_general_multiple"], len(names), "nodes"
        )
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
        # the node bars, and every label and value placed so far, for the
        # ribbon values to avoid
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
                occupied.append((box.x, box.bottom, box.x + node_width, box.top))
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
        # their curve to the first spot clear of the bars, the labels, and the
        # earlier values
        for _, line, text in sorted(values, key=lambda v: v[0], reverse=True):
            fontsize = self.value_font["fontsize"]
            x1, y1, x2, y2 = line
            candidates = [(x2 - SANKEY_LABEL_PAD, y2, "right")] + [
                (*_ribbon_centerline(*line, t), "center")
                for t in SANKEY_VALUE_POSITIONS
            ]
            for x, y, ha in candidates:
                box = _text_box(ax, x, y, text, fontsize, ha, halo)
                if not any(_overlap_area(box, other) for other in occupied):
                    break
            else:
                # nothing clear along the ribbon: the value is left out rather
                # than written over a bar or a neighbour; hover still reads it
                continue
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

    overlayable = False

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
        cycle = create_color_cycle(
            config["color_general_multiple"], len(self.groups), "groups"
        )
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
            **({"bbox": self.value_font["bbox"]} if "bbox" in self.value_font else {}),
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

    overlayable = False

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
                config["color_general_multiple"], len(self.group_names), "groups"
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
        self.label_position = (
            theme_default("networkchart", self.settings, "label_position", self.style)
            or NETWORK_LABEL_POSITION.DEFAULT
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
                # the outline in the face color is the mark, on paper so the
                # edges stop at its rim; the alpha rides on the colors, as a
                # collection alpha would fill the face
                look = {
                    "facecolors": [to_rgba(self.ground, alpha[k]) for k in ks],
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
            if style.get("label_family"):
                font["family"] = resolve_font_family(style["label_family"])
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


RADIAL_LAYER_TYPES = {
    RADIAL_TYPE.LINE: RadialLineLayer,
    RADIAL_TYPE.BAR: RadialBarLayer,
    RADIAL_TYPE.SCATTER: RadialScatterLayer,
    RADIAL_TYPE.HISTOGRAM: RadialHistogramLayer,
}


def dumbbell_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per dumbbell record, reading its delta (ADR 0050)."""

    filled, units = [], []
    for chart in charts:
        records = [{"emphasis": None, **r} for r in dumbbell_records(chart)]
        units += [(r["end"] - r["start"], _fill_role(r, "emphasis")) for r in records]
        filled.append({**chart, "data": records})
    return filled, units


def group_units(charts: List[dict], settings: dict, by) -> tuple:
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


def treemap_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per leaf record, by its `value`; groups keep explicit roles."""

    filled, units = [], []
    for chart in charts:
        data = chart["data"]
        records = [_treemap_record_units(r, None, units) for r in data["data"]]
        filled.append({**chart, "data": {**data, "data": records}})
    return filled, units


def network_units(charts: List[dict], settings: dict, by) -> tuple:
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


def parallel_units(charts: List[dict], settings: dict, by) -> tuple:
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
            if not is_number(value):
                raise ValueError(
                    f"`emphasis_rule` reads each row's `{hue}` value as a "
                    f"number; row {i} has {value!r}."
                )
            fill = _keep_role if roles is None else _fill_role(roles, i)
            units.append((value, fill))
    return filled, units


def heatmap_units(charts: List[dict], settings: dict, by) -> tuple:
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
            "inner": VIOLIN_INNER.NO_INNER,
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
        self.emphasis = emphasis
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


def group_from_chart(layers: List[Layer], settings: dict) -> LayerGroup:
    """Build a chart front's layer group; palettes are resolved here.

    Every group draws from the multiple palette, a subplot's single dataset
    included, so a series looks the same alone, in a subplot and in a grid
    cell (issue #183).
    """

    # one color per dataset (a raincloud's three layers share one chart);
    # a colorless dataset claims no slot of the pooled cycle
    n_charts = sum(chart[0].takes_color for chart in layers_per_chart(layers))
    return LayerGroup(
        layers,
        palette=config["color_general_multiple"],
        max_colors=n_charts,
        num_bins=settings.get("num_bins"),
    )


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

    # the flag silences the warning only; placement never depends on it
    if all_auto:
        clusters = _cluster_by_scale_compatibility(ranges, threshold)
        sorted_clusters = sorted(clusters, key=len, reverse=True)

        assignments = ["left"] * n
        if len(sorted_clusters) > 1:
            for idx in sorted_clusters[1]:
                assignments[idx] = "right"

        if warn_scale_groups and len(sorted_clusters) > 2:
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
            # None keeps matplotlib's rotation
            "label_rotate": {
                "xaxis": config.get("axes_xticks_label_rotate"),
                "yaxis": config.get("axes_yticks_label_rotate"),
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
        rotate = furniture.get("label_rotate") or {}
        for axis_type in axes_types:
            getattr(ax, axis_type).set_tick_params(which="major", **ticks)
            if rotate.get(axis_type) is not None:
                getattr(ax, axis_type).set_tick_params(labelrotation=rotate[axis_type])

    # ---------------- rendering ----------------

    def render(self, ax: plt.Axes) -> None:
        # an axes drawn earlier fixed the limits this one shares; autoscale
        # again, over the data of every axes that shares them
        for axis_name in ("x", "y"):
            if len(_shared_siblings(ax, axis_name)) > 1:
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
            validate_single_dataset(sum(l.kind == kind for l in self.layers), name)
        if any(isinstance(l, BasemapLayer) for l in self.layers):
            validate_basemap_company(
                [
                    l.kind
                    for l in self.layers
                    if l.takes_color and l.x_kind() != AXIS_NUMERIC
                ],
                self.horizontal,
            )

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
            # text carrier groups hold no data, and an image or a basemap
            # shares the data's coordinates: they stay on the primary axis and
            # never enter the scale clustering
            data_indices = [
                i
                for i, group in enumerate(self.groups)
                if any(l.takes_color for l in group.layers)
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

        # each value axis stacks only its own layers (ADR 0080)
        group_axes = [ax_right if a == "right" else ax for a in assignments]
        layer_axes = {
            id(layer): target_ax
            for group, target_ax in zip(self.groups, group_axes)
            for layer in group.layers
        }

        def by_axis(layers):
            pools = defaultdict(list)
            for layer in layers:
                pools[layer_axes[id(layer)]].append(layer)
            return pools.values()

        # bar slotting across every layer in the panel; radial bars share the
        # machinery — their slots are sector fractions, scaled at draw time
        bar_layers = [
            l for l in self.layers if isinstance(l, (BarLayer, RadialBarLayer))
        ]
        bar_mode = s.get("bar_mode") or BAR_MODE.DEFAULT
        # every category layer shares one category axis (ADR 0020, ADR 0079)
        category_index = self.category_index(self.layers)

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
                # bottoms accumulate per category slot, whatever the record order
                for stack in by_axis(bar_layers):
                    bottoms = np.zeros(len(category_index or ()))
                    for idx, layer in enumerate(stack):
                        labels, y = _layer_category_labels(layer), layer.y_values()
                        stacks = category_index is not None and labels is not None
                        positions = _category_positions(labels or (), category_index)
                        bar_slots[id(layer)] = BarSlot(
                            offset=0.0,
                            width=layer.bar_width,
                            bottom=bottoms[positions] if stacks else None,
                            show_yerr=idx == len(stack) - 1,
                        )
                        if stacks and y is not None:
                            # a missing bar adds nothing to the stack
                            heights = np.nan_to_num(np.asarray(y, dtype=float))
                            np.add.at(bottoms, positions, heights)
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
            for stack in by_axis(l for _, l in hist_pairs):
                hist_slots.update(_hist_stack_slots(stack, stack_bins))

        # stacked areas always stack; the baseline is a panel setting (ADR 0025)
        stack_layers = [l for l in self.layers if isinstance(l, StackedAreaLayer)]
        stack_slots = {}
        # both value axes share the one category axis, so every stack shares x
        if stack_layers:
            validate_shared_x([l.x_values() for l in stack_layers])
        for stack in by_axis(stack_layers):
            stack_slots.update(
                _stack_slots(stack, s.get("baseline") or STACKED_AREA_BASELINE.DEFAULT)
            )

        zorder_defaults = s.get("zorder_defaults", {})

        group_layers = [l for l in self.layers if isinstance(l, GroupLayer)]
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

        # background and own-colored layers do not consume a color-cycle slot
        pooled_colors = defaultdict(int)
        for group in self.groups:
            n_slotless = sum(
                1
                for l in group.layers
                if l.draws_all_muted(group.layer_role(l), group.emphasis)
                or l.own_color() is not None
            )
            pooled_colors[palette_key(group)] += max(group.max_colors - n_slotless, 0)
        cycles = {}
        for group in self.groups:
            key = palette_key(group)
            if key not in cycles:
                cycles[key] = create_color_cycle(
                    group.palette, max(pooled_colors[key], 1), "series"
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
                    z_order = zorder_defaults.get(layer.zorder_key)

                role = group.layer_role(layer)
                muted = layer.draws_all_muted(role, group.emphasis)

                own_color = layer.own_color()
                ctx = DrawContext(
                    # a colorless lookup would advance the pooled cycle and
                    # shift the colors of later composed figures
                    color=(
                        None
                        if muted or not layer.takes_color
                        else (
                            own_color
                            if own_color is not None
                            else cycle[layer.chart_hash]["color"]
                        )
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

        if category_index and group_layers:
            self._apply_category_ticks(ax, category_index, group_layers, horizontal)

        self._finalize(
            ax, ax_right, bar_layers, horizontal, scales, group_axes, limit_marks
        )

    @staticmethod
    def category_index(layers: List[Layer]) -> Optional[dict]:
        """Label -> position (0..n-1), the first-seen union of every category
        layer's labels (ADR 0079). A label repeated within one series raises.
        """

        index = {}
        category_layers = [
            (layer, labels)
            for layer in layers
            if (labels := _layer_category_labels(layer)) is not None
        ]
        for number, (layer, labels) in enumerate(category_layers, 1):
            _check_unique_labels(layer, labels, number)
            # a sorted series lacking the top category still leaves it first
            for label in [*_sorted_category_order(layer, labels), *labels]:
                index.setdefault(label, len(index))
        return index or None

    def _category_labels(self, labels, axis: str) -> list:
        """Category labels as tick text; dates print through the axis' format."""

        labels = list(labels)
        if axis_kind(labels) != AXIS_TEMPORAL:
            return labels
        return date_labels(labels, self.settings.get(f"{axis}ticks_format"))

    def _tick_rotation(self, axis: str, rotation, default: float = 0) -> float:
        """The tick-label rotation: the chart's, else the theme's, else `default`."""

        if rotation is not None:
            return rotation
        furniture = self.settings.get("furniture") or {}
        themed = (furniture.get("label_rotate") or {}).get(f"{axis}axis")
        return default if themed is None else themed

    def _apply_category_ticks(self, ax, index, group_layers, horizontal) -> None:
        # the first group layer's rotation applies; user ticks override later
        chart = group_layers[0].chart
        labels = self._category_labels(index.keys(), "y" if horizontal else "x")
        if horizontal:
            ax.set_yticks(list(index.values()))
            rotation = self._tick_rotation("y", chart.get("ytickrotate"))
            ax.set_yticklabels(labels, rotation=rotation)
        else:
            ax.set_xticks(list(index.values()))
            rotation = self._tick_rotation("x", chart.get("xtickrotate"))
            ax.set_xticklabels(labels, rotation=rotation)

    def _resolve_scales(self, ax_right, group_axes) -> tuple:
        """The literal x, y and twin value-axis scales (ADR 0041).

        Per axis, an explicit setting wins; otherwise the first group that
        stamped a scale supplies it, and a group stamped with another one
        warns. A group that set no scale has nothing to carry: it abstains
        and adopts whatever the axis resolves to.
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
            stamped = [scale for scale in stamps if scale]
            if not stamped:
                return None
            losers = sorted(set(stamped[1:]) - {stamped[0]})
            if losers and warn:
                warnings.warn(message(stamped[0], losers))
            return stamped[0]

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
                if axis.scale != AXIS_SCALE.LOG or axis.twin not in (None, on_twin):
                    continue
                category = axis.twin is None
                stamp = group.category_scale if category else group.value_scale
                hint = None
                if not s.get(axis.key) and stamp != AXIS_SCALE.LOG:
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

    def _radial_category_labels(self) -> Optional[list]:
        """The panel's category labels, in index order; the spokes follow them.

        `None` when no layer is categorical, as on a radial histogram.
        """

        index = self.category_index(self.layers)
        return list(index) if index else None

    def _apply_polar_grid_selection(self, ax, show_grid) -> None:
        """Draw only the polar grid set the user named (ADR 0015).

        Matplotlib's polar axes draw spokes and rings whatever `ax.grid`
        restyles, so the set left out is switched off by hand. Unset,
        `show_grid` never reaches here and both sets stay.
        """

        ax.xaxis.grid(show_grid in ("x", "both"))
        ax.yaxis.grid(show_grid in ("y", "both"))

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
            or value_scale not in (None, AXIS_SCALE.LINEAR)
        ):
            return
        axis = ax.xaxis if horizontal else ax.yaxis
        axis.set_minor_locator(mticker.AutoMinorLocator(splits))
        ax.tick_params(axis=name, which="minor", length=0)
        style = dict(self.settings.get("grid_style", {}))
        style["alpha"] = style.get("alpha", 1.0) * MINOR_GRID_ALPHA_SCALE
        ax.grid(axis=name, which="minor", **style)

    def _geographic_aspect(self, ax) -> float:
        """The aspect that narrows a degree of longitude by cos(mid latitude)."""

        lo, hi = ax.get_ylim()
        data = ax.dataLim.intervaly
        user_set = any(self.settings.get(k) is not None for k in ("ymin", "ymax"))
        if (
            not user_set
            and np.isfinite(data).all()
            and -90 <= min(data) <= max(data) <= 90
        ):
            # the autoscale margin may overshoot a pole the data stays within
            lo, hi = np.clip((lo, hi), -90, 90)
            ax.set_ylim(lo, hi)
        middle = validate_geographic_latitudes((lo, hi))
        return 1 / math.cos(math.radians(middle))

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
        # each value axis and the layers drawn on it; the host always counts
        value_axes = {ax: []}
        for group, owner_ax in zip(self.groups, group_axes):
            value_axes.setdefault(owner_ax, []).extend(group.layers)
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
        if polar and not bare and s.get("show_grid_explicit"):
            self._apply_polar_grid_selection(ax, s.get("show_grid"))
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
                siblings = _shared_siblings(ax, axis_name)
                if len(siblings) > 1:
                    shared = _shared_data_interval(ax, axis_name)
                    lo, hi = min(lo, shared[0]), max(hi, shared[1])
                if lo == hi:
                    temporal = self.temporal_axis == axis_name
                    lo, hi = _single_value_limits(lo, temporal)
                (ax.set_ylim if horizontal else ax.set_xlim)(lo, hi)
                pinned.add(axis_name)

        # the y-axis is a rank axis only when every data layer draws ranks;
        # beside other charts it follows the panel as usual (ADR 0046)
        data_layers = [l for l in layers if l.kind != "text"]

        # a lone basemap frames its outlines; beside data it frames nothing
        if data_layers and all(isinstance(l, BasemapLayer) for l in data_layers):
            bounds = np.array([l.bounds() for l in data_layers])
            x0, x1 = bounds[:, 0].min(), bounds[:, 1].max()
            y0, y1 = bounds[:, 2].min(), bounds[:, 3].max()
            ax.update_datalim([(x0, y0), (x1, y1)])
            ax.autoscale_view()
            # a flat outline keeps the autoscale's padding on its flat axis
            for axis_name, lo, hi in (("x", x0, x1), ("y", y0, y1)):
                if hi > lo:
                    getattr(ax, f"set_{axis_name}lim")(lo, hi)
                    pinned.add(axis_name)
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
            cat_labels = self._radial_category_labels()
            if cat_labels is not None:
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
            # band and median labels sit inside the marks and need no room;
            # each value axis pads for the labels it carries (ADR 0080)
            for owner_ax, owned in value_axes.items():
                value_layers = [
                    l for l in owned if l.labels_past_mark and l.show_values
                ]
                if not value_layers:
                    continue
                lo, hi = owner_ax.get_xlim() if horizontal else owner_ax.get_ylim()
                pad = (hi - lo) * (
                    VALUE_HEADROOM_HORIZONTAL if horizontal else VALUE_HEADROOM_VERTICAL
                )
                below = lo < 0 or any(l.labels_below_range for l in value_layers)
                lo = lo - pad if below else lo
                hi = hi + pad
                (owner_ax.set_xlim if horizontal else owner_ax.set_ylim)(lo, hi)

        # pyramid mirror furniture reads the value axis after the headroom pad
        if s.get("pyramid"):
            self._apply_pyramid_mirror(ax)

        # a stack from zero sits on the floor of its value axis, like bars
        # (ADR 0025, ADR 0080); a log value axis keeps its own floor
        if (s.get("baseline") or STACKED_AREA_BASELINE.DEFAULT) in (
            STACKED_AREA_BASELINE.ZERO,
            STACKED_AREA_BASELINE.PERCENT,
        ):
            for owner_ax, owned in value_axes.items():
                scale = scale_right if owner_ax is ax_right else value_scale
                if scale != "log" and any(
                    isinstance(l, StackedAreaLayer) for l in owned
                ):
                    (owner_ax.set_xlim if horizontal else owner_ax.set_ylim)(0, None)
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
        if not bare and not polar:
            for axis_name in ("x", "y"):
                if axis_name in pinned or (rank_axis and axis_name == "y"):
                    continue
                if all(s.get(f"{axis_name}{end}") is None for end in ("min", "max")):
                    temporal = self.temporal_axis == axis_name
                    _pad_single_value(ax, axis_name, temporal)
            if ax_right is not None and all(
                s.get(f"y{end}_right") is None for end in ("min", "max")
            ):
                _pad_single_value(ax_right, "x" if horizontal else "y", False)
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
                # a pyramid's `xmax` is mirrored onto both value ends, so it
                # pins them exactly; ticks may stop short of it
                if axis_name == "x" and s.get("pyramid_xmax") is not None:
                    fixed = (True, True)
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
        pooled_layers = defaultdict(list)
        for group, owner_ax in zip(self.groups, group_axes):
            pooled = pools.setdefault(owner_ax, {key: [] for key in REF_KEYS})
            pooled_layers[owner_ax].extend(group.layers)
            for layer in group.layers:
                for key in REF_KEYS:
                    for entry in getattr(layer, key):
                        if entry not in pooled[key]:
                            pooled[key].append(entry)

        # reference lines and bands, after scales and limits
        for owner_ax, pooled in pools.items():
            _draw_ref_lines(
                owner_ax, pooled["vlines"], pooled["hlines"], pooled["dlines"]
            )
        # a bracket reads the category positions and the data extent of its
        # axes, so it stacks above the marks it spans
        for owner_ax, pooled in pools.items():
            self._draw_brackets(
                owner_ax, pooled["brackets"], pooled_layers[owner_ax], horizontal
            )
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
            _draw_texts(
                top_ax, pooled["texts"], owner_ax, clearance, pooled_layers[owner_ax]
            )

        # point labels are placed once every marker of the panel is drawn and
        # the limits are final, so the estimate sees the real display space
        self._place_point_labels(top_ax, group_axes)
        self._spread_end_labels(group_axes, horizontal)

        # aspect ratio (a polar axes keeps its own; a bare layer fixed its own)
        if s.get("aspect_ratio") and not polar and not bare:
            aspect = s["aspect_ratio"]
            if aspect == ASPECT_RATIO.GEOGRAPHIC:
                aspect = self._geographic_aspect(ax)
            ax.set(adjustable="box", aspect=aspect)

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
            # a pyramid keeps its value max aside for the mirror
            value_max = s.get(f"{value_axis}max")
            if value_max is None and s.get("pyramid"):
                value_max = s.get("pyramid_xmax")
            if (
                value_max is None
                and value_axis not in pinned
                and (ax_right is None or s.get("ymax_right") is None)
            ):
                axes = [ax] + ([ax_right] if ax_right is not None else [])
                dim = 0 if horizontal else 1
                mirror = bool(s.get("pyramid"))
                _defer_legend_fit(
                    top_ax,
                    lambda renderer: _fit_legend(legend, axes, dim, renderer, mirror),
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
                        # a missing value draws no point, so no label either
                        if not np.isfinite([cx, cy]).all():
                            continue
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

    def _spread_end_labels(self, group_axes, horizontal) -> None:
        """Spread the visible end labels on each side of an axes apart."""

        sides = {}
        for group, owner_ax in zip(self.groups, group_axes):
            for layer in group.layers:
                if not isinstance(layer, EndLabelMixin):
                    continue
                for side, label in layer.end_labels(owner_ax):
                    if label.get_visible():
                        sides.setdefault((id(owner_ax), side), []).append(label)
        for labels in sides.values():
            if len(labels) > 1:
                _spread_labels(labels, horizontal)

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
        if not is_number(start):
            start = float(to_date_numbers([start])[0])
        return mdates.num2date(start, tz=tz)

    def _place_brackets(self, ax, brackets: List[tuple], layers, horizontal: bool):
        """Each bracket's (start, end, value), and the stack step (ADR 0059).

        A bracket without a `y` clears the data within its span by a gap, then
        climbs a step over every already placed bracket it overlaps, so the
        stack never covers itself. Both are fractions of the value-axis data
        range.
        """

        positions, tops = _bracket_categories(
            layers, self.category_index(self.layers) or {}
        )
        ranges = [r for r in (layer.y_range() for layer in layers) if r is not None]
        if ranges:
            low, high = min(r[0] for r in ranges), max(r[1] for r in ranges)
        else:
            low, high = _value_limits(ax, horizontal)
        extent = (high - low) or abs(high) or 1.0
        gap, step = extent * BRACKET_GAP, extent * BRACKET_STEP

        placed = []
        for bracket, _ in brackets:
            start = validate_bracket_endpoint(bracket.get("from"), positions)
            end = validate_bracket_endpoint(bracket.get("to"), positions)
            start, end = min(start, end), max(start, end)
            value = bracket.get("y")
            if value is None:
                value = _bracket_base(layers, tops, start, end, high) + gap
                for other_start, other_end, other_value in placed:
                    overlaps = min(end, other_end) >= max(start, other_start)
                    if overlaps and value < other_value + step:
                        value = other_value + step
            placed.append((start, end, float(value)))
        return placed, step

    def _draw_brackets(
        self, ax, brackets: List[tuple], layers: List["Layer"], horizontal: bool
    ) -> None:
        """Draw the pre-resolved pairwise comparison brackets (ADR 0059).

        Each bracket is one line artist — a tick, the span, a tick — and one
        text artist beyond it. The value axis grows to fit the topmost text,
        unless the chart sets its own limit there; a pyramid grows both ends,
        keeping the mirror it draws in (ADR 0017). Placement runs before the
        ticks are sized, because their length is in points and reads the
        final limits.
        """

        if not brackets:
            return

        s = self.settings
        placed, step = self._place_brackets(ax, brackets, layers, horizontal)
        # a pyramid moves the user's x limit aside to mirror it
        mirrored = bool(s.get("pyramid"))
        limit = (
            s.get("pyramid_xmax")
            if mirrored
            else s.get("xmax" if horizontal else "ymax")
        )
        low, high = _value_limits(ax, horizontal)
        room = max(value for _, _, value in placed) + step
        if limit is None and high > low and room > high:
            set_limits = ax.set_xlim if horizontal else ax.set_ylim
            set_limits(-room if mirrored else low, room)

        # the brackets are marks, not data: they may not rescale either axis
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        for (start, end, value), (bracket, style) in zip(placed, brackets):
            # the ticks point toward the data: down on a vertical chart, left
            # on a horizontal one
            point = (value, start) if horizontal else (start, value)
            tip = _bracket_tick_tip(ax, point, horizontal, style["tick"])
            span = ([tip, value, value, tip], [start, start, end, end])
            ax.plot(
                *(span if horizontal else (span[1], span[0])),
                **{"zorder": REF_LINE_ZORDER, **style["line"]},
            )
            text = bracket.get("text")
            if text is None:
                continue
            centre = (start + end) / 2
            ax.annotate(
                text,
                xy=(value, centre) if horizontal else (centre, value),
                xytext=(BRACKET_TEXT_PAD, 0) if horizontal else (0, BRACKET_TEXT_PAD),
                textcoords="offset points",
                zorder=REF_LINE_ZORDER,
                **{
                    **style["font"],
                    "ha": "left" if horizontal else "center",
                    "va": "center" if horizontal else "bottom",
                },
            )
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)

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
            gantt.apply_row_ticks(
                ax, self._tick_rotation("y", gantt.chart.get("ytickrotate"))
            )
            return
        # the panel's category index supplies the labels (ADR 0079)
        index = self.category_index(self.layers)
        if not index:
            return
        layer = bar_layers[0]
        # ticks sit on the category positions; slotted groups center on them
        ticks_loc = np.array(list(index.values()))
        labels = self._category_labels(
            index.keys(), "y" if layer.is_horizontal else "x"
        )

        if bar_ticks == "group":
            rotation_default = 0
        else:  # one bar layer per subplot
            n_labels = len(labels)
            rotation_default = 90 if n_labels >= 7 else (45 if n_labels >= 4 else 0)

        if layer.is_horizontal:
            ax.set_yticks(ticks_loc, labels)
            ax.yaxis.set_major_locator(mticker.FixedLocator(list(ticks_loc)))
            rotation = self._tick_rotation("y", layer.chart.get("ytickrotate"))
            ax.set_yticklabels(labels, rotation=rotation)
        else:
            ax.set_xticks(ticks_loc, labels)
            ax.xaxis.set_major_locator(mticker.FixedLocator(list(ticks_loc)))
            rotation = self._tick_rotation(
                "x", layer.chart.get("xtickrotate"), rotation_default
            )
            ax.set_xticklabels(labels, rotation=rotation)

    def _apply_radial_furniture(self, ax) -> None:
        """Apply start angle, direction, and inner radius; elevate the r labels."""

        s = self.settings

        start_angle = s.get("start_angle")
        start_angle = DEFAULT_STARTANGLE if start_angle is None else start_angle
        if isinstance(start_angle, str):
            ax.set_theta_zero_location(start_angle)
        else:
            # a numeric start_angle is a compass bearing: degrees clockwise
            # from north, matching the compass-string form
            ax.set_theta_zero_location("N", offset=-float(start_angle))

        direction = s.get("direction") or DEFAULT_DIRECTION
        ax.set_theta_direction(-1 if direction == RADIAL_DIRECTION.CLOCKWISE else 1)

        inner_radius = s.get("inner_radius") or 0.0
        if inner_radius:
            rmin, rmax = ax.get_ylim()
            # r = rorigin maps to the center: the hole takes the given
            # fraction of the drawn radial extent
            ax.set_rorigin(rmin - inner_radius / (1 - inner_radius) * (rmax - rmin))

        if s.get("show_border") is False:
            for spine in ax.spines.values():
                spine.set_visible(False)

        # the r tick labels sit midway between the first two spokes, clear of
        # both their gridlines and their category labels (issue #191); a
        # numeric angular axis keeps matplotlib's 22.5deg, midway on its grid
        cat_labels = self._radial_category_labels()
        if cat_labels is not None:
            ax.set_rlabel_position(180 / len(cat_labels))

        self._elevate_radial_value_labels(ax)
        self._draw_radial_tip_texts(ax)

    def _spine_zorder(self) -> float:
        """The build-time spine zorder; the polar top-of-stack reference."""

        furniture = self.settings.get("furniture") or {}
        spines = furniture.get("spines") or {}
        return spines.get("bottom", {}).get("zorder", DEFAULT_SPINE_ZORDER)

    def _elevate_radial_value_labels(self, ax) -> None:
        """Redraw the r tick labels above the marks and the border.

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
                color=tick_style.get("labelcolor"),
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
            cat_labels = self._radial_category_labels()
            if cat_labels is None:
                return
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

    def legend_entries(self, ax) -> tuple:
        """The legend handles and labels this panel drew on `ax` and its twins.

        A combined panel tags each label with its value axis, as its own
        legend does; otherwise the entries of every twin come in order.
        """

        # the marks may sit on a hidden twin of the axes
        twins = [twin for twin in ax._twinned_axes.get_siblings(ax) if twin is not ax]
        if self.settings.get("legend_mode") == "combined":
            ax_right = twins[0] if twins else None
            return self._combined_legend_entries(ax, ax_right, self.horizontal)
        handles, labels = ax.get_legend_handles_labels()
        for twin in twins:
            entries = twin.get_legend_handles_labels()
            handles, labels = handles + entries[0], labels + entries[1]
        return handles, labels

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
