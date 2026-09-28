"""Line family layers: line, bump, and stacked area."""

from typing import List, Optional
import numpy as np
import matplotlib.pyplot as plt
from ..validate import (
    AXIS_CATEGORICAL,
    is_number,
    validate_given_ranks,
    validate_line_curve,
)
from ..config_helpers import (
    get_area_style,
    get_bump_style,
    get_stackedarea_style,
    get_line_style,
)
from ....constants import BUMP_RANK, STACKED_AREA_BASELINE
from .base import (
    AreaFillMixin,
    EMPHASIS_BACKGROUND,
    EndLabelMixin,
    Layer,
    LineStyleCycleMixin,
    MarkClipBox,
    POINT_LABEL_PAD,
    POINT_LABEL_SPOTS_VERTICAL,
    PointLabelMixin,
    StackSlot,
    TEXT_ANNOTATION_ZORDER,
    TEXT_LINE_HEIGHT,
    UnclippedMarksMixin,
    _apply_cycle_hatch,
    _oriented,
    _point_resolver,
    _present_range,
    _scalar,
    _vertex_coordinate,
    axis_kind,
    get_chart_data,
)

# show_area fills this many data magnitudes below the line; the axes clip it,
# so the fill meets the floor whatever limits sharey, ymin or a re-render set
AREA_FLOOR_FACTOR = 1e6


def _nearest(positions, coordinate) -> int:
    """The index of the position closest to `coordinate`."""

    return int(np.nanargmin(np.abs(np.asarray(positions, dtype=float) - coordinate)))


def _column_range(chart: dict, attr: str) -> Optional[tuple]:
    """The (min, max) of a chart's data column; None when the column is absent."""

    values = get_chart_data(attr, chart)
    if values is None or axis_kind(values) == AXIS_CATEGORICAL:
        return None
    return _present_range(values)


def _mark_radius(line_style: dict) -> float:
    """Half the marker size of a line's points, or half its stroke when unmarked."""

    marker = line_style.get("marker")
    if marker in (None, "", "None", "none", " "):
        return (line_style.get("linewidth") or 1.0) / 2
    return (line_style.get("markersize") or plt.rcParams["lines.markersize"]) / 2


class LineLayer(
    PointLabelMixin,
    EndLabelMixin,
    AreaFillMixin,
    LineStyleCycleMixin,
    UnclippedMarksMixin,
    Layer,
):
    kind = "line"
    color_style = "line_style"
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
        self._resolve_end_labels(False, POINT_LABEL_PAD)

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

        if self.show_labels:
            axis = ax.yaxis if ctx.transpose else ax.xaxis
            self._draw_end_labels(
                ax,
                ctx,
                np.asarray(axis.convert_units(x), dtype=float),
                np.asarray(y, dtype=float),
                _mark_radius(line_style),
            )

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
        if not is_number(value):
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

    rank_by = settings.get("rank_by") or BUMP_RANK.DEFAULT
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

    def takes_hatch(self) -> bool:
        # a bump line fills no area
        return False

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
        self._resolve_value_labels()
        self._init_point_labels()
        self._resolve_end_labels(True, self.label_padding)

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

        self._draw_end_labels(ax, ctx, x, ranks, _mark_radius(line_style))


class StackedAreaLayer(EndLabelMixin, Layer):
    """One series of a stack; the panel computes its band (ADR 0025)."""

    kind = "stackedarea"
    color_style = "fill_style"
    surface = True
    # the stack fills its frame: both axes end on the data, not on a tick
    ticks_at_axis_ends = False

    def _resolve_style(self):
        style = get_stackedarea_style(self.style)
        self.outline = bool(style.pop("outline", False))
        self.fill_style = style
        self.line_style = get_line_style(self.style)
        self._resolve_value_labels()
        self._resolve_end_labels(False, POINT_LABEL_PAD)

    def takes_hatch(self) -> bool:
        # a tiled hatch on a translucent area reads poorly: etched areas only
        return self.etch is not None

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

        if self.show_labels:
            # a band is named at its midpoint, where its value labels sit
            mids = (ctx.stack_slot.top + ctx.stack_slot.bottom) / 2
            self._draw_end_labels(
                ax, ctx, np.asarray(axis.convert_units(x), dtype=float), mids, 0.0
            )

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
