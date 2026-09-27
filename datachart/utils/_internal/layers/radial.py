"""Radial layers: the polar line, bar, scatter, and histogram."""

from typing import Callable, Optional
import numpy as np
from ..config_helpers import (
    get_area_style,
    get_line_style,
    get_bar_style,
    get_hist_style,
    get_scatter_style,
)
from ....constants import RADIAL_TYPE
from ....config import config
from .base import (
    AreaFillMixin,
    DEFAULT_NUM_BINS,
    EMPHASIS_BACKGROUND,
    EMPHASIS_HIGHLIGHT,
    Layer,
    _apply_cycle_hatch,
    _category_positions,
    _hollow_marker,
    _marker_edge_widths,
    _present_range,
    _record_emphasis,
    _scalar,
    _span_text,
    get_chart_data,
    get_chart_observations,
)

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


RADIAL_LAYER_TYPES = {
    RADIAL_TYPE.LINE: RadialLineLayer,
    RADIAL_TYPE.BAR: RadialBarLayer,
    RADIAL_TYPE.SCATTER: RadialScatterLayer,
    RADIAL_TYPE.HISTOGRAM: RadialHistogramLayer,
}
