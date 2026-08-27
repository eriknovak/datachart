"""The single drawing seam: Layer, LayerGroup, Panel, DrawContext.

A Layer is one drawable unit that puts its marks on a matplotlib Axes. Its style
is resolved from the global config when the layer is built — never at draw time.
A Panel owns every cross-layer concern: color assignment, bar slotting, shared
histogram bins, axis scales and limits, grid, legend assembly, and twin-axis
(left/right) assignment. Layers are sibling-blind; a Panel hands each layer a
frozen DrawContext with its per-layer instructions.
"""

import json
import warnings
from collections import defaultdict
from dataclasses import dataclass
from itertools import cycle as iter_cycle
from typing import List, Optional, Union

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.mlab import GaussianKDE
from matplotlib.patches import Patch
from matplotlib.legend_handler import HandlerPathCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .colors import create_color_cycle, create_colormap, get_colormap
from .validate import validate_emphasis
from .config_helpers import (
    get_attr_value,
    resolve_font_family,
    get_area_style,
    get_grid_style,
    get_line_style,
    get_bar_style,
    get_hist_style,
    get_legend_style,
    get_vline_style,
    get_hline_style,
    get_heatmap_style,
    get_heatmap_font_style,
    get_heatmap_edge_style,
    get_contour_style,
    get_contour_label_style,
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
    get_plot_text_box_style,
    get_plot_text_arrow_style,
    configure_axis_ticks_position,
    configure_axis_limits,
)
from ..stats import minimum, maximum, contour_levels
from ...constants import (
    ASPECT_RATIO,
    DIRECTION,
    EMPHASIS,
    HISTOGRAM_TYPE,
    ORIENTATION,
    SWARM_MODE,
    RADIAL_TYPE,
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
DEFAULT_BAR_VALUE_FORMAT = "%g"
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
# matplotlib skips underscore-prefixed labels when assembling the legend
NO_LEGEND = "_nolegend_"
# radial furniture defaults: compass and calendar conventions (ADR 0015)
DEFAULT_STARTANGLE = "N"
DEFAULT_DIRECTION = DIRECTION.CLOCKWISE
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
# a soft halo keeps polar text legible over marks, grid spokes, and the border
RADIAL_TEXT_HALO = {
    "boxstyle": "round,pad=0.15",
    "facecolor": "#FFFFFF",
    "edgecolor": "none",
    "alpha": 0.6,
}
# extra radial room so tip labels stay inside the border circle
RADIAL_TIP_LABEL_HEADROOM = 0.25


def _scatter_legend_handle(legend_handle, orig_handle):
    legend_handle.update_from(orig_handle)
    size = getattr(orig_handle, "datachart_legend_size", None)
    if size is not None:
        legend_handle.set_sizes([size])


# bubble charts size markers by data; their legend entries keep the base size
LEGEND_HANDLER_MAP = {
    PathCollection: HandlerPathCollection(update_func=_scatter_legend_handle)
}
# fraction of the value-axis span added so bar value labels stay inside
VALUE_HEADROOM_VERTICAL = 0.08
VALUE_HEADROOM_HORIZONTAL = 0.12
# normalized cell value above which heatmap value text switches to white
HEATMAP_TEXT_CONTRAST_THRESHOLD = 0.55
# the low end of a sequential cmap vanishes on white: iso-lines sample from here
CONTOUR_LINE_CMAP_START = 0.3
# the cmap sample that stands in for a cmap-colored contour in the legend
CONTOUR_SWATCH = 0.7


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
        return super().default(obj)


def get_chart_hash(chart: dict) -> int:
    """Stable hash of a chart dictionary, used to key color assignment."""

    return hash(json.dumps(chart, sort_keys=True, cls=NumpyEncoder))


def _normalize_sizes(sizes: np.ndarray, size_range: tuple) -> np.ndarray:
    """Normalize size values to the specified (min, max) range."""

    min_size, max_size = size_range
    if sizes.max() == sizes.min():
        return np.full_like(sizes, (min_size + max_size) / 2, dtype=float)
    normalized = (sizes - sizes.min()) / (sizes.max() - sizes.min())
    return normalized * (max_size - min_size) + min_size


def _resolve_ref_lines(chart: dict, key: str) -> List[tuple]:
    """Resolve v/h reference-line styles at build time."""

    lines = chart.get(key)
    if lines is None:
        return []
    lines = lines if isinstance(lines, list) else [lines]
    get_style = get_vline_style if key == "vlines" else get_hline_style
    return [(line, get_style(line.get("style", {}))) for line in lines]


TEXT_COORDS = ("data", "axes")
# annotations sit above the data marks (zorder 3), below the panel furniture
TEXT_ANNOTATION_ZORDER = 5
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

        kwargs = dict(style["font"])
        kwargs["zorder"] = TEXT_ANNOTATION_ZORDER
        if style["bbox"] is not None:
            kwargs["bbox"] = dict(style["bbox"])

        target = text.get("target")
        if target is None:
            ax.annotate(content, xy=(x, y), xycoords=textcoords, **kwargs)
            continue

        text_tr = data_ax.transData if coords == "data" else ax.transAxes
        start = np.asarray(text_tr.transform((x, y)), dtype=float)
        end = np.asarray(data_ax.transData.transform(tuple(target)), dtype=float)
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
            xy=tuple(target),
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
            **style,
        )

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
            **style,
        )


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
class DrawContext:
    """Frozen per-layer instructions a Panel hands to a Layer at draw time."""

    color: Optional[str] = None
    z_order: Optional[float] = None
    legend_label: Optional[str] = None
    alpha: Optional[float] = None
    bar_slot: Optional[BarSlot] = None
    hist_slot: Optional[HistSlot] = None
    bins: Optional[np.ndarray] = None
    hatch: Optional[str] = None
    emphasis: Optional[str] = None
    parallel_stats: Optional[dict] = None
    parallel_axes: bool = True
    transpose: bool = False
    # label -> position of the panel's category axis (ADR 0020)
    category_index: Optional[dict] = None
    # the panel pins its aspect ratio, so colorbars size to the axes box
    aspect_locked: bool = False


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


class Layer:
    """One drawable unit; owns its resolved style, knows nothing about siblings."""

    kind: str = ""
    # None for layers without an orientation; they follow the panel
    is_horizontal: Optional[bool] = None
    # the coordinate space the layer draws in; a panel property (ADR 0015)
    projection: str = "cartesian"

    def __init__(self, chart: dict, settings: dict):
        self.chart = chart
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
        self.muted_alpha = DEFAULT_MUTED_ALPHA if muted_alpha is None else muted_alpha
        self._resolve_style()

    def _resolve_emphasis(self, value):
        return validate_emphasis(value)

    def _resolve_style(self) -> None:
        """Collapse config → theme → chart style into concrete style dicts."""

    def label(self, ctx: DrawContext) -> Optional[str]:
        return ctx.legend_label if ctx.legend_label is not None else self.subtitle

    def draw(self, ax: plt.Axes, ctx: DrawContext) -> None:
        raise NotImplementedError

    def y_range(self) -> Optional[tuple]:
        """The (min, max) of the layer's y data, used for axis clustering."""
        return None

    def apply_scales(self, ax: plt.Axes, scalex, scaley) -> None:
        if scalex:
            ax.set_xscale(scalex)
        if scaley:
            ax.set_yscale(scaley)

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


class LineLayer(Layer):
    kind = "line"

    def _resolve_style(self):
        self.line_style = get_line_style(self.style)
        self.area_style = get_area_style(self.style)
        self.show_yerr = self.settings.get("show_yerr")
        self.show_area = self.settings.get("show_area")

    def y_range(self):
        y = get_chart_data("y", self.chart)
        if y is None or len(y) == 0:
            return None
        return (float(np.min(y)), float(np.max(y)))

    def x_range(self):
        x = get_chart_data("x", self.chart)
        if x is None or len(x) == 0:
            return None
        return (minimum(x), maximum(x))

    def _resolved_area_style(self, ctx):
        area_style = self._merge_color("color", ctx.color, self.area_style)
        if ctx.z_order is not None:
            area_style["zorder"] = ctx.z_order - 0.1
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            area_style["color"] = self.muted_color
        return area_style

    def draw(self, ax, ctx):
        x = get_chart_data("x", self.chart)
        y = get_chart_data("y", self.chart)
        yerr = get_chart_data("yerr", self.chart)

        if x is None or y is None:
            return

        line_style = self._merge_color("color", ctx.color, self.line_style)
        if ctx.z_order is not None:
            line_style["zorder"] = ctx.z_order
        self._apply_emphasis(line_style, ctx.emphasis)

        draw_yerr = (
            self.show_yerr and isinstance(yerr, np.ndarray) and len(yerr) == len(y)
        )

        plot, fill, _ = _oriented(ax, ctx.transpose)

        if draw_yerr:
            fill(x, y - yerr, y + yerr, **self._resolved_area_style(ctx))

        plot(x, y, **line_style, label=self.label(ctx))

        if self.show_area:
            drawstyle = line_style.get("drawstyle", "")
            step = drawstyle.split("-")[1] if "steps-" in drawstyle else None
            self._fill_to_floor(fill, ax, x, y, step, self._resolved_area_style(ctx))

    @staticmethod
    def _fill_to_floor(fill, ax, x, y, step, area_style):
        """Fill under the line past any plausible axis floor, outside the autoscale."""

        values = np.asarray(y, dtype=float)
        values = values[np.isfinite(values)]
        if values.size == 0:
            return
        floor = values.min() - AREA_FLOOR_FACTOR * max(np.abs(values).max(), 1.0)
        data_lim = ax.dataLim.frozen()
        fill(x, y, floor, step=step, **area_style)
        ax.dataLim.set(data_lim)


def _abs_bar_value_fmt(value_format):
    """A bar_label fmt callable that formats the absolute value.

    Pyramid sides draw as signed data but display positive magnitudes
    (ADR 0017); the resolved format applies after the sign is dropped.
    """

    def format_abs(value):
        magnitude = abs(value)
        if isinstance(value_format, mticker.Formatter):
            return value_format(magnitude)
        # printf first, {}-style on failure: mirrors bar_label's own fmt handling
        try:
            return value_format % (magnitude,)
        except (TypeError, ValueError):
            return value_format.format(magnitude)

    return format_abs


class BarLayer(Layer):
    kind = "bar"

    def _resolve_style(self):
        orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.is_horizontal = orientation == ORIENTATION.HORIZONTAL
        self.is_pyramid = bool(self.settings.get("pyramid"))
        self.bar_style = get_bar_style(self.style, self.is_horizontal)
        self.show_yerr = self.settings.get("show_yerr")
        show_values = self.settings.get("show_values")
        if show_values is None:
            show_values = config.get("chart_default_show_values")
        self.show_values = show_values
        value_format = self.settings.get("value_format")
        self.value_format = (
            DEFAULT_BAR_VALUE_FORMAT if value_format is None else value_format
        )
        self.value_font_family = resolve_font_family()
        self.log_offset = 1 if self.settings.get("scaley") == "log" else 0
        self.value_padding = self.style.get(
            "plot_bar_value_padding", config["plot_bar_value_padding"]
        )
        self.value_fontsize = self.style.get(
            "plot_bar_value_fontsize", config["plot_bar_value_fontsize"]
        )
        self.value_color = self.style.get(
            "plot_bar_value_color", config["plot_bar_value_color"]
        )

    def labels(self) -> Optional[np.ndarray]:
        return get_chart_data("label", self.chart)

    def y_values(self) -> Optional[np.ndarray]:
        return get_chart_data("y", self.chart)

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
        if ctx.hatch is not None and "hatch" not in bar_style:
            bar_style["hatch"] = ctx.hatch or None
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

        if self.show_values:
            value_format = self.value_format
            # VALUE_FORMAT strings name the value `x`, which bar_label's own
            # {}-style formatting cannot resolve
            if isinstance(value_format, str) and "{x" in value_format:
                value_format = mticker.StrMethodFormatter(value_format)
            if self.is_pyramid:
                value_format = _abs_bar_value_fmt(value_format)
            ax.bar_label(
                bars,
                fmt=value_format,
                padding=self.value_padding,
                fontsize=self.value_fontsize,
                color=self.value_color,
                family=self.value_font_family,
            )


class HistogramLayer(Layer):
    kind = "histogram"

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
        if ctx.hatch is not None and "hatch" not in hist_style:
            hist_style["hatch"] = ctx.hatch or None
        self._apply_emphasis(hist_style, ctx.emphasis)

        if ctx.hist_slot is not None:
            # weighted bin centers reproduce the precomputed stack heights
            # exactly; density/cumulative are already encoded in them
            slot = ctx.hist_slot
            ax.hist(
                (slot.bins[:-1] + slot.bins[1:]) / 2,
                bins=slot.bins,
                weights=slot.heights,
                bottom=slot.bottom,
                label=self.label(ctx),
                orientation=self.orientation,
                **hist_style,
            )
            return

        bins = ctx.bins if ctx.bins is not None else self.num_bins
        ax.hist(
            x,
            bins=bins,
            label=self.label(ctx),
            density=self.show_density,
            cumulative=self.show_cumulative,
            orientation=self.orientation,
            **hist_style,
        )


class ScatterLayer(Layer):
    kind = "scatter"

    def _resolve_style(self):
        self.scatter_style = get_scatter_style(self.style)
        self.size_range = self.settings.get("size_range") or DEFAULT_SIZE_RANGE
        self.show_regression = self.settings.get("show_regression")
        self.show_ci = self.settings.get("show_ci")
        self.ci_level = self.settings.get("ci_level") or DEFAULT_CI_LEVEL
        self.show_correlation = self.settings.get("show_correlation")
        self.default_size = config["plot_scatter_size"]
        # a highlight edge contrasts in the theme's own text color
        self.highlight_edge_color = config.get("font_general_color") or "#000000"
        self.regression_style = get_regression_style({})
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

    def _sizes(self, size_data):
        if size_data is not None:
            return _normalize_sizes(size_data, self.size_range)
        return self.scatter_style.get("s", self.default_size)

    def _mark_legend_size(self, collection, size_data):
        if size_data is not None:
            collection.datachart_legend_size = self.scatter_style.get(
                "s", self.default_size
            )

    def _draw_regression(self, ax, x, y, color, transpose=False):
        from scipy import stats as scipy_stats

        if len(x) == 0 or len(np.unique(x)) <= 1:
            return

        plot, fill, _ = _oriented(ax, transpose)

        slope, intercept, _, _, _ = scipy_stats.linregress(x, y)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept

        reg_style = dict(self.regression_style)
        if color is not None:
            reg_style["color"] = color
        plot(x_line, y_line, **reg_style)

        if self.show_ci:
            n = len(x)
            t_val = scipy_stats.t.ppf((1 + self.ci_level) / 2, n - 2)
            y_pred = slope * x + intercept
            residuals = y - y_pred
            s_err = np.sqrt(np.sum(residuals**2) / (n - 2))
            x_mean = np.mean(x)
            ss_x = np.sum((x - x_mean) ** 2)
            se_line = s_err * np.sqrt(1 / n + (x_line - x_mean) ** 2 / ss_x)
            ci = t_val * se_line
            fill(
                x_line,
                y_line - ci,
                y_line + ci,
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
        ax.annotate(f"r = {r:.3f}", xy=(0.05, 0.95), xycoords="axes fraction", **font)

    def draw(self, ax, ctx):
        x_data = get_chart_data("x", self.chart)
        y_data = get_chart_data("y", self.chart)
        size_data = get_chart_data("size", self.chart)
        hue_data = get_chart_data("hue", self.chart)

        if x_data is None or y_data is None:
            return

        scatter_style = dict(self.scatter_style)
        if ctx.z_order is not None:
            scatter_style["zorder"] = ctx.z_order
        self._apply_emphasis(
            scatter_style, ctx.emphasis, width_key="linewidths", color_key=None
        )
        if ctx.emphasis == EMPHASIS_HIGHLIGHT:
            scatter_style["edgecolors"] = self.highlight_edge_color

        _, _, scatter = _oriented(ax, ctx.transpose)

        if hue_data is not None:
            unique_hues = np.unique(hue_data)

            for i, hue_val in enumerate(unique_hues):
                mask = hue_data == hue_val
                # sizes normalize within each hue group
                group_sizes = self._sizes(
                    size_data[mask] if size_data is not None else None
                )
                group_style = {k: v for k, v in scatter_style.items() if k != "s"}
                group_style["c"] = self.hue_colors[i]
                label = str(hue_val)
                if ctx.emphasis == EMPHASIS_BACKGROUND:
                    group_style["c"] = self.muted_color
                    label = NO_LEGEND
                collection = scatter(
                    x_data[mask],
                    y_data[mask],
                    s=group_sizes,
                    label=label,
                    **group_style,
                )
                self._mark_legend_size(collection, size_data)

            if self.show_correlation:
                self._draw_correlation(ax, x_data, y_data, color=None)
            if self.show_regression:
                self._draw_regression(
                    ax, x_data, y_data, color=None, transpose=ctx.transpose
                )
        else:
            sizes = self._sizes(size_data)
            base_style = {k: v for k, v in scatter_style.items() if k != "s"}
            if base_style.get("c") is None:
                base_style["c"] = ctx.color
            if ctx.emphasis == EMPHASIS_BACKGROUND:
                base_style["c"] = self.muted_color

            collection = scatter(
                x_data, y_data, s=sizes, label=self.label(ctx), **base_style
            )
            self._mark_legend_size(collection, size_data)

            color = base_style.get("c", base_style.get("color"))
            if self.show_regression:
                self._draw_regression(
                    ax, x_data, y_data, color=color, transpose=ctx.transpose
                )
            if self.show_correlation:
                self._draw_correlation(ax, x_data, y_data, color=color)


class GroupLayer(Layer):
    """A layer of labeled groups placed on the panel's category index."""

    def _resolve_emphasis(self, value):
        # group layers never dodge; emphasis aligns with the group labels
        if isinstance(value, list):
            for item in value:
                validate_emphasis(item)
            return value
        return validate_emphasis(value)

    def _resolve_style(self):
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

    def group_color(self, index: int, ctx_color: Optional[str]) -> Optional[str]:
        """The color of the group at `index`: its own palette slot, or the layer's."""

        if self.group_colors is None:
            return ctx_color
        return self.group_colors[index]["color"]

    def group_legend_handles(self, roles: list) -> Optional[list]:
        """One patch per group when coloring by group; background groups stay out."""

        if self.group_colors is None:
            return None
        return [
            Patch(facecolor=self.group_colors[i]["color"], label=str(label))
            for i, (label, role) in enumerate(zip(self.labels(), roles))
            if role != EMPHASIS_BACKGROUND
        ]

    def grouped_values(self) -> dict:
        """The layer's values keyed by label, in first-seen label order."""

        label_attr = get_attr_value("label", self.chart, "label")
        value_attr = get_attr_value("value", self.chart, "value")
        grouped = {}
        data = self.chart.get("data", [])
        if isinstance(data, list):
            for d in data:
                lbl, val = d.get(label_attr), d.get(value_attr)
                if lbl is not None and val is not None:
                    grouped.setdefault(lbl, []).append(val)
        return grouped

    def labels(self) -> list:
        return list(self.grouped_values().keys())

    def y_range(self):
        values = [v for vals in self.grouped_values().values() for v in vals]
        if not values:
            return None
        return (float(np.min(values)), float(np.max(values)))

    def apply_scales(self, ax, scalex, scaley):
        if scaley:
            if self.is_horizontal:
                ax.set_xscale(scaley)
            else:
                ax.set_yscale(scaley)

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

        if self.side:
            self._clip_to_side(bp, positions)
        self._apply_box_emphasis(bp, self._group_roles(labels, ctx.emphasis))

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


class SwarmLayer(GroupLayer):
    kind = "swarm"

    def _resolve_style(self):
        super()._resolve_style()
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

    def _offsets(self, ax, position: float, values: np.ndarray) -> np.ndarray:
        """Per-point offsets from the category center, in data units."""

        if self.mode == SWARM_MODE.STRIP:
            # the jitter width scales with the cell the points may spread over
            offsets = strip_offsets(
                len(values), self.jitter * self.max_offset / SWARM_MAX_OFFSET
            )
            return offsets if not self.side else (np.abs(offsets) * 2) * self.side

        size = self.swarm_style.get("s")
        if size is None:
            size = self.default_size
        diameter_px = np.sqrt(size) / 72 * ax.figure.dpi
        centers = np.full(len(values), position, dtype=float)
        points = (
            np.column_stack([values, centers])
            if self.is_horizontal
            else np.column_stack([centers, values])
        )
        px = ax.transData.transform(points)
        value_px = px[:, 0] if self.is_horizontal else px[:, 1]
        offsets_px = beeswarm_offsets(value_px, diameter_px, bool(self.side))
        # pixels per data unit along the category axis
        unit = ax.transData.transform([[0, 1]] if self.is_horizontal else [[1, 0]])
        origin = ax.transData.transform([[0, 0]])
        scale = (unit - origin)[0][1 if self.is_horizontal else 0]
        offsets = np.clip(offsets_px / scale, -self.max_offset, self.max_offset)
        return offsets if not self.side else offsets * self.side

    def draw(self, ax, ctx):
        grouped = self.grouped_values()
        labels = list(grouped.keys())
        if not labels:
            warnings.warn("No data points found for swarm plot.")
            return

        index = ctx.category_index
        roles = self._group_roles(labels, ctx.emphasis)

        base_style = dict(self.swarm_style)
        if ctx.z_order is not None:
            base_style["zorder"] = ctx.z_order
        if base_style.get("c") is None:
            base_style["c"] = ctx.color
        if base_style.get("s") is None:
            base_style["s"] = self.default_size

        # one collection per role with a single legend entry; colored by
        # group, one collection per label and the cloud's legend lists them
        positions = list(index.values())
        lo, hi = min(positions) - 0.5, max(positions) + 0.5
        if self.color_by_group:
            batches = [
                ([lbl], role, i) for i, (lbl, role) in enumerate(zip(labels, roles))
            ]
        else:
            batches = [
                ([lbl for lbl, r in zip(labels, roles) if r == role], role, None)
                for role in (None, EMPHASIS_HIGHLIGHT, EMPHASIS_BACKGROUND)
            ]
        legend_taken = self.color_by_group
        for members, role, group_index in batches:
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
                (index[lbl] + self.offset, np.asarray(grouped[lbl], dtype=float))
                for lbl in members
            ]
            centers = np.concatenate([np.full(len(v), pos) for pos, v in groups])
            values = np.concatenate([v for _, v in groups])
            x, y = (values, centers) if self.is_horizontal else (centers, values)
            collection = ax.scatter(x, y, label=label, **style)
            # the category axis spans every group edge to edge, like a box plot
            edges = (
                collection.sticky_edges.y
                if self.is_horizontal
                else collection.sticky_edges.x
            )
            edges[:] = [lo, hi]
            self._pending.setdefault(id(ax), []).append((collection, groups))
        interval = ax.dataLim.intervaly if self.is_horizontal else ax.dataLim.intervalx
        interval[:] = (min(interval[0], lo), max(interval[1], hi))

    def pack(self, ax) -> None:
        """Spread the points drawn into `ax`; the panel calls this once its view is final."""

        for collection, groups in self._pending.pop(id(ax), []):
            offsets = np.concatenate([self._offsets(ax, pos, v) for pos, v in groups])
            xy = np.asarray(collection.get_offsets()).copy()
            xy[:, 1 if self.is_horizontal else 0] += offsets
            collection.set_offsets(xy)


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


class ViolinLayer(GroupLayer):
    """A per-label KDE body with inner marks drawn from the data."""

    kind = "violin"

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
        if not self.split or not self.split_values:
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
        return list(grouped.keys()), grouped

    def draw(self, ax, ctx):
        labels, grouped = self._group()
        if len(labels) == 0:
            warnings.warn("No data points found for violin plot.")
            return

        body_style = dict(self.violin_style)
        width = body_style.pop("width")
        if body_style.get("facecolor") is None:
            body_style["facecolor"] = ctx.color
        roles = self._group_roles(labels, ctx.emphasis)
        # (split value, side): -1 draws the low half, +1 the high half, 0 both
        sides = list(zip(self.split_values, (-1, 1))) or [(None, self.side)]
        self._legend_roles = roles

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
                artists = [self._draw_body(ax, values, position, width, style, side)]
                artists += self._draw_inner(ax, values, position, width, side)
                self._apply_violin_emphasis(artists, roles[i])

    def _draw_body(self, ax, values, position, width, style, side):
        parts = ax.violinplot(
            [values],
            positions=[position],
            widths=width,
            orientation=self.orientation,
            bw_method=self.bandwidth,
            showextrema=False,
            showmedians=False,
            showmeans=False,
        )
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
        if side:
            axis = 1 if self.is_horizontal else 0
            clip = np.minimum if side < 0 else np.maximum
            for path in body.get_paths():
                path.vertices[:, axis] = clip(path.vertices[:, axis], position)
        return body

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

        if self.inner == VIOLIN_INNER.MEDIAN:
            return [span(median, "-")]
        return [span(q1, ":"), span(median, "--"), span(q3, ":")]

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


# the axes fraction a colorbar takes, and its gap from the axes
COLORBAR_FRACTION = 0.05
COLORBAR_PAD = 0.03
COLORBAR_DIVIDER_PAD = 0.1


def _draw_colorbar(
    ax: plt.Axes, mappable, colorbar: dict, aspect_locked: bool = False
) -> None:
    """Draw a colorbar beside (or above) the axes.

    The layout engine places it clear of titles and neighbouring axes; an
    aspect-locked axes instead carves it from its own box, which the engine
    would size to the grid cell rather than the box.
    """

    orientation = colorbar.get("orientation", DEFAULT_ORIENTATION)
    location = "right" if orientation == ORIENTATION.VERTICAL else "top"
    if aspect_locked:
        cax = make_axes_locatable(ax).append_axes(
            location, size=f"{COLORBAR_FRACTION:.0%}", pad=COLORBAR_DIVIDER_PAD
        )
        ax.figure.colorbar(mappable, cax=cax, orientation=orientation)
        return
    # the layout engine keeps a colorbar at its own aspect (20:1 by default),
    # which shortens it beside a narrow axes: size it to the axes slot instead
    bbox = ax.get_position()
    width, height = ax.figure.get_size_inches()
    if location == "right":
        aspect = (bbox.height * height) / (bbox.width * width * COLORBAR_FRACTION)
    else:
        aspect = (bbox.width * width) / (bbox.height * height * COLORBAR_FRACTION)
    ax.figure.colorbar(
        mappable,
        ax=ax,
        location=location,
        fraction=COLORBAR_FRACTION,
        pad=COLORBAR_PAD,
        aspect=aspect,
    )


def _value_formatter(valfmt):
    """A `{x}`-style format string as a matplotlib formatter; others pass."""

    if isinstance(valfmt, str) and "{x" in valfmt:
        return mticker.StrMethodFormatter(valfmt)
    return valfmt


class HeatmapLayer(Layer):
    kind = "heatmap"

    def _resolve_style(self):
        self.show_heatmap_values = self.settings.get("show_heatmap_values")
        self.show_colorbars = self.settings.get("show_colorbars")
        heatmap_style = get_heatmap_style(self.style)
        heatmap_style["cmap"] = get_colormap(heatmap_style["cmap"])
        self.heatmap_style = heatmap_style
        self.font_style = get_heatmap_font_style(self.style)
        self.edge_style = get_heatmap_edge_style(self.style)
        self.frame_color = self.style.get(
            "plot_heatmap_frame_color",
            config.get("plot_heatmap_frame_color") or "#000000",
        )
        self.frame_width = config.get("axes_spines_width") or 0.8
        # white value text only helps when the cmap's high end is actually dark
        r, g, b = heatmap_style["cmap"](1.0)[:3]
        self.contrast_values = (0.2126 * r + 0.7152 * g + 0.0722 * b) < 0.5
        x, y, self.z = self._grid()
        self._label_axes(x, y)

    def _grid(self) -> tuple:
        """The validated (x, y, z); x and y are None when not given, z lists."""

        x, y, z = get_chart_grid(self.chart, "heatmap", dtype=object)
        z = [[(np.nan if item is None else item) for item in row] for row in z]
        return x, y, z

    def _label_axes(self, x, y):
        # x/y default the tick attrs so the panel applies them like explicit ones
        chart = dict(self.chart)
        for axis, labels in (("x", x), ("y", y)):
            if labels is None or chart.get(f"{axis}ticks") is not None:
                continue
            chart[f"{axis}ticks"] = list(range(len(labels)))
            chart[f"{axis}ticklabels"] = chart.get(f"{axis}ticklabels") or [
                str(label) for label in labels
            ]
        self.chart = chart

    def draw(self, ax, ctx):
        data = self.z
        valfmt = self.chart.get("valfmt", DEFAULT_VALUE_FORMAT)
        colorbar = self.chart.get("colorbar", {})

        # the panel owns the aspect; imshow's own "equal" would size the
        # colorbar to a box the panel then stretches
        im = ax.imshow(
            data,
            aspect="auto",
            norm=self.chart.get("norm", None),
            vmin=self.chart.get("vmin", None),
            vmax=self.chart.get("vmax", None),
            **self.heatmap_style,
        )

        if self.show_heatmap_values:
            valfmt = _value_formatter(valfmt)
            for i in range(len(data)):
                for j in range(len(data[i])):
                    value = data[i][j]
                    font_style = dict(self.font_style)
                    if (
                        self.contrast_values
                        and not np.isnan(value)
                        and float(im.norm(value)) > HEATMAP_TEXT_CONTRAST_THRESHOLD
                    ):
                        font_style["color"] = "#FFFFFF"
                    ax.text(
                        j,
                        i,
                        valfmt(value, None),
                        ha="center",
                        va="center",
                        **font_style,
                    )

        if self.edge_style.get("linewidth"):
            self._draw_cell_borders(ax, len(data), len(data[0]))

        if self.show_colorbars:
            _draw_colorbar(ax, im, colorbar, ctx.aspect_locked)

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


# one layer for lines and fills, shared with the density front (ADR 0022)
class ContourLayer(Layer):
    """A gridded surface drawn as iso-lines or filled bands."""

    kind = "contour"

    def _resolve_style(self):
        self.filled = bool(self.settings.get("filled"))
        self.show_labels = self.settings.get("show_labels")
        self.show_colorbars = self.settings.get("show_colorbars")
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
        self.x, self.y, self.z = self._grid()
        self.levels = contour_levels(self.z, self.settings.get("levels"))

    def _grid(self) -> tuple:
        """The validated (x, y, z) arrays; x and y default to the indices."""

        x, y, z = get_chart_grid(self.chart, "contour")
        n_rows, n_cols = z.shape
        x = np.arange(n_cols) if x is None else x.astype(float)
        y = np.arange(n_rows) if y is None else y.astype(float)
        return x, y, z

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
                cmap=self.cmap,
                **scaling,
                **style,
            )
            # a legend proxy: the contour set itself carries no legend handle
            ax.fill_between([], [], [], color=self.cmap(CONTOUR_SWATCH), label=label)
            if self.show_colorbars:
                _draw_colorbar(
                    ax, bands, self.chart.get("colorbar", {}), ctx.aspect_locked
                )
            return

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
        ax.plot(
            [],
            [],
            color=color,
            linewidth=style["linewidths"],
            linestyle=style["linestyles"],
            label=label,
        )
        if self.show_labels:
            label_style = dict(self.label_style)
            fmt = _value_formatter(self.chart.get("valfmt"))
            if fmt is not None:
                label_style["fmt"] = fmt
            if ctx.emphasis == EMPHASIS_BACKGROUND:
                label_style["colors"] = self.muted_color
            ax.clabel(lines, **label_style)


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
            ax.plot(x_positions, y_vals, **style)

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
                for cat in dim_categories[dim]:
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
                        str(cat),
                        ha=label_ha,
                        va="center",
                        bbox=self.tick_label_bbox,
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
                        zorder=tick_zorder + 1,
                        **self.tick_label_style,
                    )


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

    def layer_dimensions(layer):
        first_chart = layer.charts[0]
        dimensions = first_chart.get("dimensions", None)
        if dimensions is not None:
            return list(dimensions)
        hue_attr = first_chart.get("hue", "hue")
        for chart in layer.charts:
            for d in chart.get("data", []) or []:
                return [k for k, v in d.items() if k != hue_attr and v is not None]
        return []

    dimensions = layer_dimensions(layers[0])
    for layer in layers[1:]:
        if layer_dimensions(layer) != dimensions:
            raise ValueError(
                "Composed parallel coordinates charts must share the same "
                f"dimensions; got {dimensions} and {layer_dimensions(layer)}."
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
        if len(non_none) > 0 and isinstance(non_none[0], str):
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

    def y_range(self):
        y = get_chart_data("y", self.chart)
        if y is None or len(y) == 0:
            return None
        return (float(np.min(y)), float(np.max(y)))

    def apply_scales(self, ax, scalex, scaley):
        # a polar axes rejects set_xscale; only the radial (value) axis scales
        if scaley:
            ax.set_yscale(scaley)


class RadialLineLayer(RadialLayer):
    kind = "radial-line"

    def _resolve_style(self):
        self.line_style = get_line_style(self.style)
        self.area_style = get_area_style(self.style)
        self.show_yerr = self.settings.get("show_yerr")
        self.show_area = self.settings.get("show_area")

    def _resolved_area_style(self, ctx):
        area_style = self._merge_color("color", ctx.color, self.area_style)
        if ctx.z_order is not None:
            area_style["zorder"] = ctx.z_order - 0.1
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            area_style["color"] = self.muted_color
        return area_style

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
        self._apply_emphasis(line_style, ctx.emphasis)

        yerr = get_chart_data("yerr", self.chart)
        if self.show_yerr and isinstance(yerr, np.ndarray) and len(yerr) == len(y) - 1:
            yerr = np.append(yerr, yerr[0])
            ax.fill_between(theta, y - yerr, y + yerr, **self._resolved_area_style(ctx))

        ax.plot(theta, y, **line_style, label=self.label(ctx))

        if self.show_area:
            # the fill reaches the center (or the innerradius hole clips it)
            ax.fill_between(theta, 0.0, y, **self._resolved_area_style(ctx))


class RadialBarLayer(RadialLayer):
    kind = "radial-bar"
    show_values = False

    def _resolve_style(self):
        self.bar_style = get_bar_style(self.style)
        self.show_yerr = self.settings.get("show_yerr")

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
        if ctx.hatch is not None and "hatch" not in bar_style:
            bar_style["hatch"] = ctx.hatch or None
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
        self._tips = [
            (float(t + theta_offset), float(r), float(v), i)
            for i, (t, r, v) in enumerate(zip(theta, tops, y))
        ]

        ax.bar(theta + theta_offset, y, yerr=yerr, label=self.label(ctx), **bar_style)


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
        self._apply_emphasis(
            scatter_style, ctx.emphasis, width_key="linewidths", color_key=None
        )
        if ctx.emphasis == EMPHASIS_HIGHLIGHT:
            scatter_style["edgecolors"] = self.highlight_edge_color
        if scatter_style.get("c") is None:
            scatter_style["c"] = ctx.color
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            scatter_style["c"] = self.muted_color

        theta = _radial_theta(len(y))
        self._tips = [
            (float(t), float(v), float(v), i) for i, (t, v) in enumerate(zip(theta, y))
        ]
        ax.scatter(theta, y, label=self.label(ctx), **scatter_style)


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
        if ctx.hatch is not None and "hatch" not in hist_style:
            hist_style["hatch"] = ctx.hatch or None
        self._apply_emphasis(hist_style, ctx.emphasis, width_key="linewidth")

        counts, edges = binned
        theta_edges = np.deg2rad(edges)
        centers = (theta_edges[:-1] + theta_edges[1:]) / 2
        self._tips = [
            (float(c), float(n), float(n), None) for c, n in zip(centers, counts)
        ]
        ax.bar(
            centers,
            counts,
            width=np.diff(theta_edges),
            label=self.label(ctx),
            **hist_style,
        )


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


LAYER_TYPES = {
    "linechart": LineLayer,
    "barchart": BarLayer,
    # a pyramid is the bar seam under mirrored panel furniture (ADR 0017)
    "pyramidchart": BarLayer,
    "histogram": HistogramLayer,
    "scatterchart": ScatterLayer,
    "boxplot": BoxLayer,
    "swarmplot": SwarmLayer,
    "violinplot": ViolinLayer,
    "heatmap": HeatmapLayer,
    "contourchart": ContourLayer,
}

RADIAL_LAYER_TYPES = {
    RADIAL_TYPE.LINE: RadialLineLayer,
    RADIAL_TYPE.BAR: RadialBarLayer,
    RADIAL_TYPE.SCATTER: RadialScatterLayer,
    RADIAL_TYPE.HISTOGRAM: RadialHistogramLayer,
}


def build_layers(chart_type: str, charts: List[dict], settings: dict) -> List[Layer]:
    """Build the layers for a chart front; style resolution happens here."""

    if chart_type == "parallelcoords":
        return [ParallelCoordsLayer(list(charts), settings)]

    if chart_type == "radialchart":
        visual = settings.get("radial_type") or RADIAL_TYPE.LINE
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

    def with_prefs(
        self, *, y_axis, z_order, legend_label, emphasis=None
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


class Panel:
    """A group of layers sharing one coordinate space; owns all cross-layer concerns."""

    def __init__(self, groups: List[LayerGroup], settings: Optional[dict] = None):
        self.groups = groups
        self.settings = settings or {}

    @property
    def layers(self) -> List[Layer]:
        return [layer for group in self.groups for layer in group.layers]

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
            # tick_params cannot set a font family; applied to the labels directly
            "font_family": resolve_font_family(),
        }

    def _apply_furniture(
        self, ax: plt.Axes, axes_types=("xaxis", "yaxis"), spines=True
    ) -> None:
        furniture = self.settings.get("furniture")
        if furniture is None:
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
        for axis_type in axes_types:
            getattr(ax, axis_type).set_tick_params(which="major", **furniture["ticks"])

    # ---------------- rendering ----------------

    def render(self, ax: plt.Axes) -> None:
        s = self.settings

        # one dataset per kind: a violin and a box may share the positions
        for kind, name in (("box", "box plot"), ("violin", "violin plot")):
            if sum(1 for l in self.layers if l.kind == kind) > 1:
                raise ValueError(
                    f"Multiple {name} datasets require `subplots=True`. "
                    f"{name.capitalize()}s do not support overlaying multiple "
                    "datasets on a single axis."
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

        zorder_defaults = s.get("zorder_defaults", {})

        # group layers share one category axis (ADR 0020)
        group_layers = [l for l in self.layers if isinstance(l, GroupLayer)]
        category_index = self.category_index(group_layers)

        # hatch cycle: per bar/histogram series, parallel to the color cycle
        hatch_patterns = s.get("hatch_cycle")
        hatch_assignments = None
        if hatch_patterns:
            hatch_iter = iter_cycle(hatch_patterns)
            hatch_assignments = defaultdict(lambda: next(hatch_iter))

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
                1 for l in group.layers if group.layer_role(l) == EMPHASIS_BACKGROUND
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

        group_axes = []
        for group, assignment in zip(self.groups, assignments):
            target_ax = ax_right if assignment == "right" else ax
            group_axes.append(target_ax)

            cycle = cycles[palette_key(group)]
            bins = s.get("hist_bins_override")
            if bins is None:
                bins = group.hist_bins()

            for layer in group.layers:
                z_order = group.z_order
                if z_order is None:
                    z_order = zorder_defaults.get(layer.kind)

                role = group.layer_role(layer)

                ctx = DrawContext(
                    # a text carrier lookup would advance the pooled cycle
                    # and shift the colors of later composed figures
                    color=(
                        None
                        if role == EMPHASIS_BACKGROUND or layer.kind == "text"
                        else cycle[layer.chart_hash]["color"]
                    ),
                    z_order=z_order,
                    legend_label=(
                        NO_LEGEND if role == EMPHASIS_BACKGROUND else group.legend_label
                    ),
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
                    bins=bins,
                    hatch=(
                        hatch_assignments[layer.chart_hash]
                        if hatch_assignments is not None
                        and isinstance(
                            layer,
                            (
                                BarLayer,
                                HistogramLayer,
                                RadialBarLayer,
                                RadialHistogramLayer,
                            ),
                        )
                        else None
                    ),
                    emphasis=role,
                    parallel_stats=parallel_stats,
                    parallel_axes=layer is parallel_axes_owner,
                    transpose=horizontal and layer.is_horizontal is None,
                    category_index=category_index,
                    aspect_locked=aspect_locked,
                )
                layer.draw(target_ax, ctx)

        if category_index:
            self._apply_category_ticks(ax, category_index, group_layers, horizontal)

        self._finalize(ax, ax_right, bar_layers, horizontal, group_axes)

    @staticmethod
    def category_index(layers: List[Layer]) -> Optional[dict]:
        """Label -> position (1..n), the first-seen union across group layers."""

        index = {}
        for layer in layers:
            if isinstance(layer, GroupLayer):
                for label in layer.labels():
                    index.setdefault(label, len(index) + 1)
        return index or None

    @staticmethod
    def _apply_category_ticks(ax, index, group_layers, horizontal) -> None:
        # the first group layer's rotation applies; user ticks override later
        chart = group_layers[0].chart
        labels = list(index.keys())
        if horizontal:
            ax.set_yticks(list(index.values()))
            ax.set_yticklabels(labels, rotation=chart.get("ytickrotate", 0))
        else:
            ax.set_xticks(list(index.values()))
            ax.set_xticklabels(labels, rotation=chart.get("xtickrotate", 0))

    def _finalize(self, ax, ax_right, bar_layers, horizontal, group_axes=None) -> None:
        """Apply the furniture; x/y keys are literal, `*_right` keys hit the twin."""

        s = self.settings
        layers = self.layers
        polar = self.projection == "polar"

        # scales (a layer may remap them, e.g. horizontal box plots)
        if layers and (s.get("scalex") or s.get("scaley")):
            layers[0].apply_scales(ax, s.get("scalex"), s.get("scaley"))

        # grid
        if s.get("show_grid"):
            ax.grid(axis=s["show_grid"], **s.get("grid_style", {}))
        if polar:
            # the marks sit above the grid; the r-value labels are redrawn
            # above the marks in _apply_radial_furniture
            ax.set_axisbelow(True)

        # line charts pin the category-axis limits to their data range
        if s.get("tighten_xlim"):
            set_category_lim = ax.set_ylim if horizontal else ax.set_xlim
            for layer in layers:
                if isinstance(layer, LineLayer):
                    rng = layer.x_range()
                    if rng is not None:
                        set_category_lim(rng[0], rng[1])

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

        # user-provided tick positions
        for layer in layers:
            configure_axis_ticks_position(ax, layer.chart)

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
            value_layers = [l for l in bar_layers if l.show_values]
            if value_layers:
                lo, hi = ax.get_xlim() if horizontal else ax.get_ylim()
                pad = (hi - lo) * (
                    VALUE_HEADROOM_HORIZONTAL if horizontal else VALUE_HEADROOM_VERTICAL
                )
                lo = lo - pad if lo < 0 else lo
                hi = hi + pad
                (ax.set_xlim if horizontal else ax.set_ylim)(lo, hi)

        # pyramid mirror furniture reads the value axis after the headroom pad
        if s.get("pyramid"):
            self._apply_pyramid_mirror(ax)

        # axis limits
        limits = {k: s.get(k) for k in ("xmin", "xmax", "ymin", "ymax")}
        configure_axis_limits(ax, limits)
        if ax_right is not None and (
            s.get("ymin_right") is not None or s.get("ymax_right") is not None
        ):
            (ax_right.set_xlim if horizontal else ax_right.set_ylim)(
                s.get("ymin_right"), s.get("ymax_right")
            )

        # radial furniture reads the final r limits, so it follows them
        if polar:
            self._apply_radial_furniture(ax)

        # beeswarm packing reads the display transform, so it runs once the
        # scales and limits are final (ADR 0020)
        if group_axes is None:
            group_axes = [ax] * len(self.groups)
        for group, owner_ax in zip(self.groups, group_axes):
            for layer in group.layers:
                if isinstance(layer, SwarmLayer):
                    layer.pack(owner_ax)

        # reference lines and text annotations, after scales and limits
        for layer, target_ax in zip(layers, [ax] * len(layers)):
            _draw_ref_lines(target_ax, layer.vlines, layer.hlines)

        # a twin axes renders entirely above its host, so texts live on the
        # topmost axes while data coordinates read the owning layer's axes
        top_ax = ax_right if ax_right is not None else ax
        clearance = None
        if any(layer.texts for layer in layers):
            clearance = self._clearance_points(group_axes, horizontal)
        for group, owner_ax in zip(self.groups, group_axes):
            for layer in group.layers:
                _draw_texts(top_ax, layer.texts, owner_ax, clearance)

        # aspect ratio (a polar axes keeps its own fixed aspect)
        if s.get("aspect_ratio") and not polar:
            ax.set(adjustable="box", aspect=s["aspect_ratio"])

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

        # legend
        if s.get("show_legend"):
            legend_style = {
                **s.get("legend_style", {}),
                "handler_map": LEGEND_HANDLER_MAP,
            }
            custom_handles = None
            for group in self.groups:
                for layer in group.layers:
                    # background layers carry no legend entries
                    if group.layer_role(layer) == EMPHASIS_BACKGROUND:
                        continue
                    handles = getattr(layer, "legend_handles", lambda: None)()
                    if handles:
                        custom_handles = (custom_handles or []) + handles
            if custom_handles is not None:
                ax.legend(handles=custom_handles, title="Legend", **legend_style)
            elif s.get("legend_mode") == "combined":
                self._combine_legends(ax, ax_right, legend_style, horizontal)
            elif not any(isinstance(l, ParallelCoordsLayer) for l in layers):
                # parallel coords only carry a legend when hue groups exist;
                # unlabeled panels get no empty legend frame
                if ax.get_legend_handles_labels()[1]:
                    ax.legend(title="Legend", **legend_style)

        # the polar border circle crosses the plot area; the legend covers it
        # fully — above the spine, with an opaque frame so nothing shows through
        if polar:
            legend = ax.get_legend()
            if legend is not None:
                legend.set_zorder(self._spine_zorder() + RADIAL_LEGEND_Z_OVER_SPINE)
                legend.get_frame().set_alpha(1.0)

        # tick labels and legend text cannot take the font family through
        # tick_params/legend kwargs; restyle them directly
        family = (s.get("furniture") or {}).get("font_family")
        if family:
            for target in [ax] + ([ax_right] if ax_right is not None else []):
                for label in target.get_xticklabels() + target.get_yticklabels():
                    label.set_fontfamily(family)
            legend = ax.get_legend()
            if legend is not None:
                for text in legend.get_texts():
                    text.set_fontfamily(family)
                if legend.get_title() is not None:
                    legend.get_title().set_fontfamily(family)

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

        ax.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda value, _pos: f"{abs(value):g}")
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
        # the widest layer supplies the labels when category counts differ
        layer = max(bar_layers, key=lambda l: len(l.labels()))
        labels = layer.labels()
        # ticks sit on the category positions; slotted groups center on them
        ticks_loc = np.arange(labels.shape[0])

        if bar_ticks == "group":
            rotation_default = 0
        else:  # one bar layer per subplot
            n_labels = labels.shape[0]
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
        ax.set_theta_direction(-1 if direction == DIRECTION.CLOCKWISE else 1)

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
        for r, text in zip(ticks, texts):
            ax.text(
                theta,
                r,
                text,
                ha="center",
                va="center",
                fontsize=tick_style.get("labelsize"),
                fontfamily=furniture.get("font_family"),
                color="#000000",
                zorder=self._spine_zorder() + RADIAL_LABEL_Z_OVER_SPINE,
                bbox=RADIAL_TEXT_HALO,
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
            value_format = s.get("value_format") or DEFAULT_BAR_VALUE_FORMAT
            # VALUE_FORMAT strings name the value `x` (see BarLayer.draw)
            if isinstance(value_format, str) and "{x" in value_format:
                formatter = mticker.StrMethodFormatter(value_format)

                def format_value(v):
                    return formatter(v, None)

            else:

                def format_value(v):
                    return value_format % v

            value_style = s.get("tip_value_style") or {}
            for theta, r_tip, value, _ in tips:
                rotation, ha = spoke_rotation(theta)
                ax.text(
                    theta,
                    r_tip + RADIAL_TIP_VALUE_PAD * span,
                    format_value(value),
                    rotation=rotation,
                    rotation_mode="anchor",
                    ha=ha,
                    va="center",
                    zorder=z_order,
                    fontfamily=family,
                    bbox=RADIAL_TEXT_HALO,
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
                    bbox=RADIAL_TEXT_HALO,
                )

    @staticmethod
    def _combine_legends(ax_left, ax_right, legend_style, horizontal=False) -> None:
        handles_left, labels_left = ax_left.get_legend_handles_labels()

        if ax_right is not None:
            handles_right, labels_right = ax_right.get_legend_handles_labels()
            primary, secondary = ("B", "T") if horizontal else ("L", "R")
            labels_left = [f"{label} ({primary})" for label in labels_left]
            labels_right = [f"{label} ({secondary})" for label in labels_right]
            handles = handles_left + handles_right
            labels = labels_left + labels_right
        else:
            handles, labels = handles_left, labels_left

        if handles:
            ax_left.legend(handles, labels, title="Legend", **legend_style)


# ================================================
# Panel Assembly for Chart Fronts
# ================================================


def build_chart_panel_settings(
    chart_type: str, settings: dict, mode: str, first_style: dict
) -> dict:
    """Resolve panel-level settings for a chart front at build time.

    Modes: "single" (all layers on the figure's one axes), "subplot" (one layer
    per axes), "composition" (the metadata panel used by grids).
    """

    show_grid = settings.get("show_grid")
    # rasters (a heatmap, filled contour bands) cover the grid: leave it off
    raster = chart_type == "heatmap" or (
        chart_type == "contourchart" and settings.get("filled")
    )
    if show_grid is None and not raster:
        show_grid = config.get("chart_default_show_grid")

    panel_settings = {
        "furniture": Panel.snapshot_furniture(),
        "scalex": settings.get("scalex"),
        "scaley": settings.get("scaley"),
        "show_grid": show_grid,
        "grid_style": get_grid_style(first_style),
        "hatch_cycle": config.get("plot_hatch_cycle"),
        "xmin": settings.get("xmin"),
        "xmax": settings.get("xmax"),
        "ymin": settings.get("ymin"),
        "ymax": settings.get("ymax"),
        "aspect_ratio": (
            ASPECT_RATIO.AUTO
            if settings.get("aspect_ratio") is None
            else settings["aspect_ratio"]
        ),
        "legend_style": get_legend_style(),
        # histograms stack by default; bars group (ADR 0014)
        "bar_mode": settings.get("bar_mode")
        or ("stack" if chart_type == "histogram" else "group"),
        "tighten_xlim": chart_type == "linechart",
        # radial furniture; only polar panels read these
        "startangle": settings.get("startangle"),
        "direction": settings.get("direction"),
        "innerradius": settings.get("innerradius"),
        "show_border": settings.get("show_border"),
        "show_values": settings.get("show_values"),
        "show_tip_labels": settings.get("show_tip_labels"),
        "value_format": settings.get("value_format"),
        "tip_value_style": {
            "fontsize": config["plot_bar_value_fontsize"],
            "color": config["plot_bar_value_color"],
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
        panel_settings["xlabel"] = settings.get("xlabel")
        panel_settings["ylabel"] = settings.get("ylabel")
        panel_settings["label_styles"] = Panel.snapshot_label_styles()

    return panel_settings
