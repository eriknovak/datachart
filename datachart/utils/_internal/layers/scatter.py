"""The scatter layer."""

from dataclasses import replace
from typing import Optional
import numpy as np
from matplotlib.patches import FancyArrowPatch
from ..colors import create_color_cycle
from ..validate import validate_error_distances
from ..config_helpers import (
    get_scatter_style,
    get_scatter_error_style,
    get_regression_style,
    get_plot_text_style,
    get_plot_text_box_style,
)
from ....constants import AXIS_SCALE
from ....config import config
from .base import (
    EMPHASIS_BACKGROUND,
    EMPHASIS_HIGHLIGHT,
    Layer,
    MARKER_ROLE_ORDER,
    NO_LEGEND,
    POINT_LABEL_PAD,
    PointLabelMixin,
    UnclippedMarksMixin,
    _draw_scatter_marks,
    _drawn_error_axis,
    _keyed_records,
    _oriented,
    _point_resolver,
    _present_range,
    _validated_record_roles,
    get_chart_data,
)

DEFAULT_CI_LEVEL = 0.95


DEFAULT_SIZE_RANGE = (20, 200)


# the correlation readout's corner, in axes fractions
CORRELATION_BOX_CORNER = (0.05, 0.95)


# an error bar sits this far under the markers it belongs to (ADR 0057)
ERROR_BAR_Z_STEP = 0.1


# the bar's cap, as a flat bracket at its far end; the width is in points
ERROR_CAP_STYLE = "-[,widthB={width},lengthB=0"


# the error columns a scatter point may carry, and the axis each is drawn
# along once a transposed panel has swapped the two
ERROR_KEYS = ("xerr", "yerr")


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
