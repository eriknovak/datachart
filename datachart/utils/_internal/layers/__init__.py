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
from itertools import cycle as iter_cycle
from typing import List, NamedTuple, Optional, Tuple, Union
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
from matplotlib import rc_context
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator
from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.container import BarContainer
from matplotlib.patches import Rectangle
from matplotlib.transforms import Bbox, ScaledTranslation, blended_transform_factory
from matplotlib.legend import Legend
from matplotlib.legend_handler import (
    HandlerPatch,
    HandlerPathCollection,
    HandlerPolyCollection,
)
from ..colors import create_color_cycle
from ..validate import (
    AXIS_NUMERIC,
    AXIS_TEMPORAL,
    is_number,
    validate_basemap_company,
    validate_geographic_latitudes,
    validate_log_values,
    validate_single_dataset,
    validate_axis_kinds,
    validate_shared_x,
    validate_bracket_endpoint,
    validate_ticks_format,
)
from ..config_helpers import (
    resolve_font_family,
    expand_legend_location,
    get_text_style,
    get_plot_text_style,
    get_plot_text_box_style,
    get_plot_text_arrow_style,
    configure_axis_ticks_position,
    configure_axis_limits,
)
from ....constants import (
    ASPECT_RATIO,
    GANTT_DATE_PERIOD,
    BAR_MODE,
    LEGEND_LOCATION,
    RADIAL_DIRECTION,
    AXIS_SCALE,
    STACKED_AREA_BASELINE,
)
from ....config import config
from .base import (
    BarSlot,
    DEFAULT_NUM_BINS,
    DEFAULT_ORIENTATION,
    DEFAULT_VALUE_LABEL_FORMAT,
    DrawContext,
    EndLabelMixin,
    Etch,
    HOLLOW_MARKER_EDGE_WIDTH,
    InkStroke,
    Layer,
    MARKER_EDGE_MAX_SHARE,
    MarkClipBox,
    NO_LEGEND,
    NumpyEncoder,
    PointLabelMixin,
    REF_CYCLE_COLOR,
    SPAN_SIDES,
    TEXT_ANNOTATION_ZORDER,
    TEXT_LINE_HEIGHT,
    UnclippedMarksMixin,
    _category_positions,
    _chart_column,
    _defer_legend_fit,
    _fit_outside_legend,
    _format_value,
    _halo_effects,
    _legend_pad_px,
    _marker_edge_widths,
    _rule_summary,
    _text_size,
    axis_kind,
    emphasis_rule_roles,
    get_chart_data,
    get_chart_hash,
    is_temporal,
    resolve_show_values,
    series_units,
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
    _hist_stack_slots,
    bar_units,
    gantt_units,
    sort_bar_charts,
    sort_gantt_charts,
)
from .scatter import CORRELATION_BOX_CORNER, ScatterLayer, _axis_numbers
from .group import (
    BoxLayer,
    DumbbellLayer,
    GroupLayer,
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
    pack_swarms,
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
from .parallel import ParallelCoordsLayer, compute_parallel_stats, parallel_units
from .radial import (
    RADIAL_LAYER_TYPES,
    RadialBarLayer,
    RadialHistogramLayer,
    RadialLayer,
    RadialLineLayer,
    RadialScatterLayer,
    _radial_theta,
)
from .relational import (
    NETWORK_PULL_MAX,
    NETWORK_PULL_MIN,
    NetworkLayer,
    SankeyLayer,
    TreemapLayer,
    _fit_text,
    _marker_entry,
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

# an overlap below this many square pixels counts as a clear spot
POINT_LABEL_CLEAR = 1e-6


# passes of the end-label spread per label; a chain resolves in about one each
END_LABEL_SPREAD_PASSES = 10


# the widest correlation readout, for reserving its corner box
CORRELATION_BOX_TEXT = "r = -0.000"


CORRELATION_BOX_PAD = 0.3


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


# a minor value gridline is this much fainter than a labelled one
MINOR_GRID_ALPHA_SCALE = 0.6


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
