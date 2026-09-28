"""The layer base: Layer, DrawContext, the mixins, ink effects, shared helpers."""

import hashlib
from contextlib import contextmanager
import json
import math
from datetime import date, tzinfo
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.container import BarContainer
from matplotlib.colors import to_hex, to_rgb
from matplotlib.markers import MarkerStyle
from matplotlib.patches import Patch
from matplotlib.path import Path
from matplotlib.transforms import (
    Bbox,
    IdentityTransform,
    ScaledTranslation,
    TransformedBbox,
    TransformedPath,
)
import matplotlib.patheffects as patheffects
from matplotlib.legend import Legend
from ..validate import (
    AXIS_CATEGORICAL,
    AXIS_NUMERIC,
    AXIS_TEMPORAL,
    is_missing,
    validate_emphasis,
    validate_axis_kinds,
    validate_bracket_ends,
    validate_span_bounds,
    validate_value_step,
)
from ..config_helpers import (
    resolve_font_family,
    get_etch,
    get_ink_stroke,
    get_legend_style,
    get_value_etch,
    get_sketch_halo,
    get_vline_style,
    get_hline_style,
    get_dline_style,
    get_bracket_style,
    get_bracket_tick,
    get_vspan_style,
    get_hspan_style,
    get_text_style,
    get_plot_text_style,
    get_value_label_style,
    get_plot_text_box_style,
    get_plot_text_arrow_style,
)
from ...stats import minimum, maximum
from ....constants import (
    LINE_LABEL_POSITION,
    EMPHASIS,
    LEGEND_LOCATION,
    ORIENTATION,
    VALUE_FORMAT,
)
from ....config import config

DEFAULT_NUM_BINS = 20


DEFAULT_ORIENTATION = ORIENTATION.VERTICAL


DEFAULT_VALUE_LABEL_FORMAT = "%g"


# emphasis roles (ADR 0009): background mutes, highlight bolds, None is today
EMPHASIS_BACKGROUND = EMPHASIS.BACKGROUND


EMPHASIS_HIGHLIGHT = EMPHASIS.HIGHLIGHT


# offsets keep emphasized layers among the data layers, below panel furniture
EMPHASIS_Z_OFFSET = {EMPHASIS_BACKGROUND: -0.5, EMPHASIS_HIGHLIGHT: 0.5}


MUTED_WIDTH_SCALE = 0.75


HIGHLIGHT_WIDTH_SCALE = 2.0


DEFAULT_MUTED_COLOR = "#CFCFCF"


DEFAULT_MUTED_ALPHA = 0.5


# estimated glyph width and line height as multiples of the font size
TEXT_WIDTH_PER_CHAR = 0.55


TEXT_LINE_HEIGHT = 1.2


# point labels: the gap between a marker's edge and its label, in points, and
# the candidate spots around the marker in preference order (ha, va, dx, dy)
POINT_LABEL_PAD = 3.0


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


# matplotlib skips underscore-prefixed labels when assembling the legend
NO_LEGEND = "_nolegend_"


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


LEGEND_HEADROOM_PAD_PT = 4.0


# value steps (ADR 0048): the legend swatch outline
STEP_LEGEND_EDGE_WIDTH = 0.8


ERROR_AXIS_SWAP = {"xerr": "yerr", "yerr": "xerr"}


# ================================================
# Data Helpers
# ================================================


def _chart_column(attr: str, chart: dict):
    """A data column's raw values: the dict form's sequence, else one per point."""

    if isinstance(chart["data"], dict):
        return chart["data"][attr] if attr in chart["data"] else None

    if isinstance(chart["data"], list):
        filtered = [d[attr] for d in chart["data"] if attr in d]
        return filtered or None

    return None


def get_chart_data(attr: str, chart: dict) -> Optional[np.ndarray]:
    """Extract a data column from a chart dictionary as a numpy array."""

    values = _chart_column(attr, chart)
    if values is None or isinstance(chart["data"], dict):
        return values
    return np.array(values)


def get_chart_observations(attr: str, chart: dict) -> Optional[np.ndarray]:
    """A data column as one flat pool of observations, NaN dropped.

    A point carries a single observation or a list of them, and the charts
    that bin or estimate over a sample read the lot as one series. Records
    are concatenated, so lists of unequal length never have to square into
    a grid (issue #233). A column of NaN alone is None: it draws nothing.
    """

    values = _chart_column(attr, chart)
    if values is None:
        return None
    if isinstance(chart["data"], dict):
        observations = np.ravel(values)
    else:
        flat = [np.ravel(value) for value in values]
        if not flat:
            return None
        observations = np.concatenate(flat)
    if observations.dtype.kind != "f":
        return observations
    finite = observations[~np.isnan(observations)]
    return finite if len(finite) else None


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles numpy arrays and types."""

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        if is_temporal(obj):
            return obj.isoformat() if isinstance(obj, date) else str(obj)
        # a formatter keys by identity: the same function hashes alike
        if callable(obj):
            return repr(obj)
        return super().default(obj)


def get_chart_hash(chart: dict) -> int:
    """Stable hash of a chart dictionary, used to key color assignment."""

    return hash(json.dumps(chart, sort_keys=True, cls=NumpyEncoder))


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
    if isinstance(values, np.ndarray) and values.dtype.kind in "fiu":
        return AXIS_NUMERIC
    # the first value decides; a temporal/numeric mix raises (ADR 0082)
    kinds = [
        (
            AXIS_TEMPORAL
            if is_temporal(value)
            else AXIS_CATEGORICAL if isinstance(value, str) else AXIS_NUMERIC
        )
        for value in values
        if not is_missing(value)
    ]
    validate_axis_kinds(kinds)
    return kinds[0] if kinds else None


# per family: the style resolver for a reference line
REF_LINE_STYLES = {
    "vlines": get_vline_style,
    "hlines": get_hline_style,
    "dlines": get_dline_style,
}


def _resolve_ref_lines(chart: dict, key: str) -> List[tuple]:
    """Resolve reference-line styles at build time."""

    lines = chart.get(key)
    if lines is None:
        return []
    lines = lines if isinstance(lines, list) else [lines]
    get_style = REF_LINE_STYLES[key]
    return [(line, get_style(line.get("style", {}) or {})) for line in lines]


def _resolve_brackets(chart: dict) -> List[tuple]:
    """Resolve pairwise bracket styles at build time (ADR 0059)."""

    brackets = chart.get("brackets")
    if brackets is None:
        return []
    brackets = brackets if isinstance(brackets, list) else [brackets]
    resolved = []
    for bracket in brackets:
        validate_bracket_ends(bracket)
        style = bracket.get("style") or {}
        line = get_bracket_style(style)
        # a plotted line would otherwise take the next color of the axes cycle
        line.setdefault("color", REF_CYCLE_COLOR)
        font = get_plot_text_style(style)
        # the text names the comparison the line draws, so it shares its color
        font["color"] = line["color"]
        resolved.append(
            (bracket, {"line": line, "tick": get_bracket_tick(style), "font": font})
        )
    return resolved


# per side: the bound keys and the style resolver; on polar a vspan is
# bounded in degrees, an hspan in radius
SPAN_SIDES = {
    "vspans": ("xmin", "xmax", get_vspan_style),
    "hspans": ("ymin", "ymax", get_hspan_style),
}


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


# annotations sit above the data marks (zorder 3), below the panel furniture
TEXT_ANNOTATION_ZORDER = 5


# an unset reference-line color: the first cycle color, without advancing it
REF_CYCLE_COLOR = "C0"


def _px_to_points(ax: plt.Axes, pixels: float) -> float:
    """A display distance in points, the unit the connector's gaps use."""

    return pixels * 72.0 / ax.figure.dpi


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


def _category_positions(labels, index: Optional[dict]) -> np.ndarray:
    """Each label's position on the panel's category axis, else its own index."""

    if not index:
        return np.arange(len(labels))
    return np.array([index[label] for label in labels], dtype=int)


def _fit_outside_legend(legend: Legend, axes: list, renderer) -> None:
    """Move an outside legend past the tick labels and axis labels on its side.

    An outside location anchors to the axes edge, where the axis furniture
    lives. Once layout has sized the axes, the legend shifts outward by the
    furniture's overhang on that side, as a fixed offset in inches so the
    re-layout that makes room for it keeps the gap. Above the axes, an axes
    title (a panel's title in a grid cell) is not furniture: the legend sits
    under it, and the title lifts to clear the legend.
    """

    box = legend.get_window_extent(renderer)
    ax_box = legend.axes.bbox
    pad = _legend_pad_px(legend.figure)
    if box.x0 >= ax_box.x1:
        side = "right"
    elif box.x1 <= ax_box.x0:
        side = "left"
    elif box.y0 >= ax_box.y1:
        side = "top"
    elif box.y1 <= ax_box.y0:
        side = "bottom"
    else:
        return
    titled = [ax for ax in axes if side == "top" and ax.title.get_text()]
    # read before hiding: a hidden title's position goes stale
    bottoms = [ax.title.get_window_extent(renderer).y0 for ax in titled]
    legend.set_in_layout(False)
    for ax in titled:
        ax.title.set_visible(False)
    try:
        furniture = Bbox.union([ax.get_tightbbox(renderer) for ax in axes])
    finally:
        legend.set_in_layout(True)
        for ax in titled:
            ax.title.set_visible(True)
    shift, direction = {
        "right": (furniture.x1 - ax_box.x1, (1, 0)),
        "left": (ax_box.x0 - furniture.x0, (-1, 0)),
        "top": (furniture.y1 - ax_box.y1, (0, 1)),
        "bottom": (ax_box.y0 - furniture.y0, (0, -1)),
    }[side]
    shift = shift + pad if shift > 0 else 0
    if shift:
        inches = shift / legend.figure.dpi
        offset = ScaledTranslation(
            direction[0] * inches, direction[1] * inches, legend.figure.dpi_scale_trans
        )
        # the anchor reads back in display space; the offset hangs off its
        # axes-fraction position so the re-layout keeps the gap
        anchor = legend.axes.transAxes.inverted().transform(
            legend.get_bbox_to_anchor().p0
        )
        legend.set_bbox_to_anchor(
            tuple(anchor), transform=legend.axes.transAxes + offset
        )
    for ax, bottom in zip(titled, bottoms):
        # matplotlib's own title offset, in inches, survives re-layout
        lift = box.y1 + shift + pad - bottom
        if lift > 0:
            points = ax.titleOffsetTrans.get_matrix()[1, 2] * 72 / ax.figure.dpi
            ax._set_title_offset_trans(points + lift * 72 / ax.figure.dpi)


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


def resolve_value_kind(settings: dict) -> Optional[str]:
    """The value label kind a range front prints; None when `show_values` is off."""

    return settings.get("value_kind") if resolve_show_values(settings) else None


def resolve_show_values(settings: dict) -> bool:
    """`show_values` as set, else the theme default for a front that takes it (ADR 0033)."""

    if "show_values" not in settings:
        return False
    return bool(theme_default(None, settings, "show_values"))


def theme_default(
    chart_type: Optional[str],
    settings: dict,
    name: str,
) -> Any:
    """The setting `name`, else the theme's default for it, else None (ADR 0071).

    A shared parameter's theme key comes from its `SharedParameter`, so
    `chart_type` may be None for one; a shared parameter without one, or a
    front's own parameter, takes its key from the `theme_defaults` of its
    row.
    """

    # chart_kinds imports this module, so the descriptor is read at call time
    from ..chart_kinds import SHARED_PARAMETERS, chart_kind

    value = settings.get(name)
    if value is not None:
        return value
    shared = SHARED_PARAMETERS.get(name)
    key = shared.theme_default if shared is not None else None
    if key is None and chart_type is not None:
        key = chart_kind(chart_type).theme_defaults.get(name)
    if key is None:
        return None
    return config.get(key)


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
    # `Panel` can carry the layer into another figure's coordinate space
    overlayable: bool = True
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
    # a layer that draws no series takes no color-cycle slot
    takes_color: bool = True
    # the resolved style dict of the layer's primary mark; a color set there
    # is the layer's own, so it takes no color-cycle slot either (ADR 0077)
    color_style: Optional[str] = None
    # the edge the layer's drawn colorbar takes; None when it draws none
    colorbar_edge: Optional[str] = None
    # the normalized position a value step must break on; None spaces them evenly
    step_centre: Optional[float] = None
    # (theta, radius, value, index) per radial mark, for the panel's tip texts
    _tips = ()
    # the layer's labels share the panel's one category axis (ADR 0079)
    on_category_axis: bool = False

    # group policies, set from the front's `ChartKind` row at build
    tighten_xlim: bool = False
    shared_bins: bool = False
    stacks: bool = False
    rank_axis: bool = False
    rows_down: bool = False
    rising_rows: bool = False
    paired: bool = False
    schedule_axis: bool = False
    shared_dimensions: bool = False
    map_underlay: bool = False

    def __init__(self, chart: dict, settings: dict):
        self.chart = chart
        # (artist, resolver) pairs registered by the draw in progress (ADR 0031)
        self._hover_targets = []
        # (artist, (x, y)) marks drawn past the axes, hidden past a user limit
        self._limit_marks = []
        self.settings = settings
        self.subtitle = chart.get("subtitle", None)
        self.style = chart.get("style", {}) or {}
        # the key of the layer's cycle entries; a picture would not serialize
        self.chart_hash = get_chart_hash(chart) if self.takes_color else None
        self.vlines = _resolve_ref_lines(chart, "vlines")
        self.hlines = _resolve_ref_lines(chart, "hlines")
        self.dlines = _resolve_ref_lines(chart, "dlines")
        self.brackets = _resolve_brackets(chart)
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
            get_value_label_style(self.style).get("halo_width"), self.ground
        )
        self.step_legend_style = None
        if self.value_etch_steps:
            self.step_legend_style = {
                **get_legend_style({"location": LEGEND_LOCATION.OUTSIDE_RIGHT}),
                "family": resolve_font_family(),
            }
        self._resolve_style()

    def _resolve_emphasis(self, value):
        return value

    @property
    def zorder_key(self) -> str:
        """The layer's rung in a Panel overlay's zorder table (ADR 0054)."""

        return "surface" if self.surface else self.kind

    def target_extent(self, ax: plt.Axes, point: tuple) -> Optional[float]:
        """Half the extent (points) of the mark this layer draws under `point`.

        A connector's target gap is capped to it, so the tip stops inside
        the mark it names. None when the layer has no mark there — most
        layers draw marks a 5 pt gap cannot overshoot.
        """

        return None

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

        self.show_values = resolve_show_values(self.settings)
        value_format = self.settings.get("value_format")
        self.value_format = (
            DEFAULT_VALUE_LABEL_FORMAT if value_format is None else value_format
        )
        self.value_step = validate_value_step(self.settings.get("value_step"))
        style = get_value_label_style(self.style)
        self.value_padding = style["padding"]
        self.value_font = value_label_font(style)

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

    def category_labels(self) -> Optional[list]:
        """The labels the layer places on the panel's category axis; None off it."""

        if not self.on_category_axis:
            return None
        labels = self.labels()
        return None if labels is None else list(labels)

    def bracket_values(self) -> Optional[dict]:
        """The values drawn at each category label, for bracket placement.

        None for a layer whose marks brackets do not stand on.
        """

        return None

    def size_values(self) -> Optional[np.ndarray]:
        """The data the layer's mark sizes scale from; None for fixed sizes."""

        return None

    def takes_hatch(self) -> bool:
        """Whether the panel's hatch cycle reaches the layer's fills."""

        return False

    def apply_row_ticks(self, ax, rotation: float) -> bool:
        """Place the layer's own row ticks; False leaves them to the panel."""

        return False

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
        edges = norm.inverse(step_edges(n, self.step_centre))
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

    def own_color(self) -> Optional[str]:
        """The color the layer's style sets for its primary mark, if any."""

        if self.color_style is None:
            return None
        return getattr(self, self.color_style).get("color")

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

    data = chart.get("data")
    if not isinstance(data, list):
        return []
    return [record for record in data if _is_bar_record(record, column)]


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


def _drawn_error_axis(axis: str, transpose: bool) -> str:
    """The axis an error is drawn along; a transposed panel swaps the two."""

    return ERROR_AXIS_SWAP[axis] if transpose else axis


def _point_resolver(label, x, y, transpose: bool, errors=None) -> Callable[[int], dict]:
    """The hover resolver of a point series drawn from `x` and `y` arrays.

    The datum names the *drawn* axes: a transposed series (horizontal panel
    or bars) reports its `x` values under `y` and vice versa, so the axis
    labels on the artist's axes always describe the values. A point's error
    distances follow its values, under the axis they are drawn along.
    """

    def resolve(index: int) -> dict:
        x_val, y_val = _scalar(x[index]), _scalar(y[index])
        if transpose:
            x_val, y_val = y_val, x_val
        datum = {"label": label, "x": x_val, "y": y_val}
        for axis, distances in (errors or {}).items():
            if distances is None or np.isnan(distances[0][index]):
                continue
            low, high = float(distances[0][index]), float(distances[1][index])
            key = _drawn_error_axis(axis, transpose)
            datum[key] = low if low == high else f"-{low:g}/+{high:g}"
        return datum

    return resolve


def _scalar(value):
    """A plain Python scalar for a numpy element; anything else as is."""

    return value.item() if isinstance(value, np.generic) else value


def _span_text(low, high, fmt=lambda value: f"{value:g}") -> str:
    """A `low – high` span, each end formatted by `fmt`."""

    return f"{fmt(low).strip()} – {fmt(high).strip()}"


def _vertex_coordinate(vertices: np.ndarray, index, axis: int) -> float:
    """The coordinate along `axis` of a picked outline vertex.

    A polygon collection picks `(polygon, vertex)`, a patch outline the
    vertex alone; either wraps around the closing vertex.
    """

    vertex = index[-1] if isinstance(index, tuple) else index
    return float(vertices[vertex % len(vertices)][axis])


def _present_range(values) -> Optional[tuple]:
    """The (min, max) of the values present; None when every one is missing."""

    if values is None or len(values) == 0:
        return None
    lo = minimum(values)
    if isinstance(lo, float) and np.isnan(lo):
        return None
    return (lo, maximum(values))


def _plot_text_font() -> dict:
    """The plot text style as annotate kwargs, without its alignment."""

    return {k: v for k, v in get_plot_text_style({}).items() if k not in ("ha", "va")}


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
        self.label_font = _plot_text_font()
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


class EndLabelMixin:
    """Series named beside their line ends (ADR 0076).

    A layer prints each end label as it draws; the panel reads them back
    through `end_labels` once every layer has drawn and spreads the ones
    that overlap apart along the value axis.
    """

    def _resolve_end_labels(self, default: bool, pad: float) -> None:
        """The `show_labels` flag, its position, the label gap and font."""

        show = self.settings.get("show_labels")
        self.show_labels = default if show is None else bool(show)
        self.label_position = (
            self.settings.get("label_position") or LINE_LABEL_POSITION.DEFAULT
        )
        self.end_label_pad = pad
        # end labels wear the text font; the halo keeps them legible over lines
        self.end_label_font = _plot_text_font()
        # drawn labels per axes, consumed by the panel's spread
        self._end_labels = {}

    def _labels_at(self, end: str) -> bool:
        """Whether an end label prints at the `LINE_LABEL_POSITION.START` or `END`."""

        return bool(self.show_labels and self.subtitle) and self.label_position in (
            end,
            LINE_LABEL_POSITION.BOTH,
        )

    def _draw_end_labels(self, ax, ctx, x, y, radius: float) -> None:
        """Print the series name beside its first and/or last finite point.

        `x` and `y` are axis numbers along the category and value axes;
        `radius` is the mark's half size in points, which the gap clears.
        """

        present = np.flatnonzero(np.isfinite(x) & np.isfinite(y))
        if not len(present):
            return
        ends = []
        if self._labels_at(LINE_LABEL_POSITION.START):
            ends.append((present[0], -1))
        if self._labels_at(LINE_LABEL_POSITION.END):
            ends.append((present[-1], 1))
        gap = radius + self.end_label_pad
        font = dict(self.end_label_font)
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            font["color"] = self.muted_color
        for i, side in ends:
            xy = (y[i], x[i]) if ctx.transpose else (x[i], y[i])
            offset = (0, -side * gap) if ctx.transpose else (side * gap, 0)
            label = ax.annotate(
                self.subtitle,
                xy=xy,
                xytext=offset,
                textcoords="offset points",
                ha=("center" if ctx.transpose else "left" if side > 0 else "right"),
                va=("top" if side > 0 else "bottom") if ctx.transpose else "center",
                path_effects=self.value_halo,
                annotation_clip=False,
                zorder=TEXT_ANNOTATION_ZORDER,
                **font,
            )
            self.register_limit_mark(label, *xy)
            self._end_labels.setdefault(id(ax), []).append((side, label))

    def end_labels(self, ax) -> list:
        """The (side, annotation) pairs drawn into `ax`, forgotten once read."""

        return self._end_labels.pop(id(ax), [])


def _apply_cycle_hatch(style: dict, ctx: DrawContext) -> None:
    """Take the panel's cycle hatch unless the resolved style sets one."""

    if ctx.hatch is not None and "hatch" not in style:
        style["hatch"] = ctx.hatch or None


class AreaFillMixin:
    """The fill under a series line: cycle color and hatch, muted or not."""

    def takes_hatch(self) -> bool:
        # a tiled hatch on a translucent area reads poorly: etched areas only
        return self.etch is not None

    def _resolved_area_style(self, ctx):
        area_style = self._merge_color("color", ctx.color, self.area_style)
        if ctx.z_order is not None:
            area_style["zorder"] = ctx.z_order - 0.1
        _apply_cycle_hatch(area_style, ctx)
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            area_style["color"] = self.muted_color
        return area_style


class BarSlotMixin:
    """Bars the panel slots side by side and fades with its bar overlay alpha."""

    def takes_hatch(self) -> bool:
        return True


class BinnedMarksMixin:
    """Binned counts the panel fades with its histogram overlay alpha."""

    def takes_hatch(self) -> bool:
        return True


class LineStyleCycleMixin:
    """Series lines the panel's line-style cycle reaches."""


class MarkerCycleMixin:
    """Point marks the panel's marker cycle reaches."""


class PackedMarksMixin:
    """Marks the panel packs apart once its scales and limits are final."""


class CategoryGroupMixin:
    """Groups on the panel's shared category axis, which they label."""


class MarkClipBox(TransformedBbox):
    """The axes box grown by `pad` points along `dims`, read live with the layout."""

    def __init__(self, ax, pad: float, dims=("x", "y")):
        super().__init__(Bbox.unit(), ax.transAxes)
        self._figure, self._pad, self._dims = ax.figure, pad, tuple(dims)

    def get_points(self):
        pad = self._pad * self._figure.dpi / 72.0
        grow = [pad if "x" in self._dims else 0.0, pad if "y" in self._dims else 0.0]
        return super().get_points() + [[-grow[0], -grow[1]], grow]


class UnclippedMarksMixin:
    """A layer whose scatter marks may draw whole over an axis end on the data."""

    def mark_radius(self, ax, point) -> Optional[float]:
        """The radius (points) of the mark at `point`; None when it sits on none.

        The collections carry the sizes the panel finally gave them, so a
        sized series answers for the very marker under the point. The
        smallest mark covering it wins, as the tightest one to stop inside.
        """

        target = np.asarray(ax.transData.transform(point), dtype=float)
        radii = []
        for collection in getattr(self, "_marks", {}).get(id(ax), ()):
            offsets = collection.get_offsets()
            sizes = np.asarray(collection.get_sizes(), dtype=float)
            if not len(offsets) or not sizes.size:
                continue
            drawn = collection.get_offset_transform().transform(offsets)
            index = int(np.argmin(np.hypot(*(drawn - target).T)))
            radius = float(np.sqrt(sizes[index % sizes.size]) / 2)
            if _px_to_points(ax, float(np.hypot(*(drawn[index] - target)))) <= radius:
                radii.append(radius)
        return min(radii) if radii else None

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


# the axes fraction a colorbar takes, and its gap from the axes
COLORBAR_FRACTION = 0.05


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


def step_edges(n: int, centre: Optional[float] = None) -> np.ndarray:
    """The `n + 1` normalized edges of `n` value steps; `centre` always gets one.

    Without a centre the steps are evenly spaced. With one they are evenly
    spaced on each side of it, so a diverging scale never runs a single step
    across its middle (ADR 0056).
    """

    if centre is None or not 0 < centre < 1:
        return np.linspace(0.0, 1.0, n + 1)
    below = min(max(int(round(n * centre)), 1), n - 1)
    return np.concatenate(
        [
            np.linspace(0.0, centre, below + 1),
            np.linspace(centre, 1.0, n - below + 1)[1:],
        ]
    )


def _step_label(low, high) -> str:
    """A value step's range, each end to three significant digits."""

    return " – ".join(f"{float(f'{value:.3g}'):g}" for value in (low, high))


def value_label_font(style: dict) -> dict:
    """The text kwargs of a value label from its resolved `plot_value_*` style."""

    font = {
        "fontsize": style["fontsize"],
        "color": style["color"],
        "family": resolve_font_family(),
        "path_effects": _halo_effects(
            style.get("halo_width"), config.get("axes_facecolor")
        ),
    }
    if style.get("tab"):
        font["bbox"] = _value_tab_bbox(style["tab"])
    return font


def _value_tab_bbox(tab: dict) -> dict:
    """The text `bbox` kwargs of a `plot_value_tab` setting."""

    return {
        "boxstyle": f"round,pad={tab['pad']},rounding_size={tab['rounding']}",
        "facecolor": tab["facecolor"],
        "edgecolor": tab["edgecolor"],
        "linewidth": tab["line_width"],
    }


def _text_size(fontsize, text) -> tuple:
    """A text's estimated (width, height) in points."""

    lines = text.split("\n")
    return (
        TEXT_WIDTH_PER_CHAR * fontsize * max(len(line) for line in lines),
        TEXT_LINE_HEIGHT * fontsize * len(lines),
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


def _lighten(color, amount: float) -> str:
    """The color moved `amount` (0–1) of the way to white."""

    return to_hex(tuple(c + (1 - c) * amount for c in to_rgb(color)))


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


def series_units(column: str) -> Callable:
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


# ================================================
# Panel Assembly for Chart Fronts
# ================================================


def value_axis_grid(show_grid, horizontal: bool):
    """A theme's one-axis grid default, moved onto a horizontal value axis.

    Themes name the grid of an upright chart, whose values run along y; a
    dumbbell's gridlines follow its values whichever way they run (ADR 0050).
    """

    if not horizontal:
        return show_grid
    return {"x": "y", "y": "x"}.get(show_grid, show_grid)
