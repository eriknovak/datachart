"""The single drawing seam: Layer, LayerGroup, Panel, DrawContext (ADR 0001).

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
from typing import List, Optional, Union

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from .colors import create_color_cycle, get_colormap
from .config_helpers import (
    get_attr_value,
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
    get_scatter_style,
    get_regression_style,
    get_box_style,
    get_box_outlier_style,
    get_box_median_style,
    get_box_whisker_style,
    get_box_cap_style,
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
    configure_axis_ticks_position,
    configure_axis_limits,
)
from ..stats import minimum, maximum
from ...constants import ASPECT_RATIO, ORIENTATION, VALFMT
from ...config import config

DEFAULT_NUM_BINS = 20
DEFAULT_ORIENTATION = ORIENTATION.VERTICAL
DEFAULT_VALFMT = VALFMT.DEFAULT
DEFAULT_CI_LEVEL = 0.95
DEFAULT_SIZE_RANGE = (20, 200)


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
class DrawContext:
    """Frozen per-layer instructions a Panel hands to a Layer at draw time."""

    color: Optional[str] = None
    z_order: Optional[float] = None
    legend_label: Optional[str] = None
    alpha: Optional[float] = None
    bar_slot: Optional[BarSlot] = None
    bins: Optional[np.ndarray] = None


# ================================================
# Layers
# ================================================


class Layer:
    """One drawable unit; owns its resolved style, knows nothing about siblings."""

    kind: str = ""

    def __init__(self, chart: dict, settings: dict):
        self.chart = chart
        self.settings = settings
        self.subtitle = chart.get("subtitle", None)
        self.style = chart.get("style", {}) or {}
        self.chart_hash = get_chart_hash(chart)
        self.vlines = _resolve_ref_lines(chart, "vlines")
        self.hlines = _resolve_ref_lines(chart, "hlines")
        self._resolve_style()

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

    def draw(self, ax, ctx):
        x = get_chart_data("x", self.chart)
        y = get_chart_data("y", self.chart)
        yerr = get_chart_data("yerr", self.chart)

        if x is None or y is None:
            return

        line_style = self._merge_color("color", ctx.color, self.line_style)
        if ctx.z_order is not None:
            line_style["zorder"] = ctx.z_order

        draw_yerr = (
            self.show_yerr and isinstance(yerr, np.ndarray) and len(yerr) == len(y)
        )

        if draw_yerr:
            area_style = self._merge_color("color", ctx.color, self.area_style)
            if ctx.z_order is not None:
                area_style["zorder"] = ctx.z_order - 0.1
            ax.fill_between(x, y - yerr, y + yerr, **area_style)

        if self.show_area:
            area_style = self._merge_color("color", ctx.color, self.area_style)
            if ctx.z_order is not None:
                area_style["zorder"] = ctx.z_order - 0.1
            drawstyle = line_style.get("drawstyle", "")
            step = drawstyle.split("-")[1] if "steps-" in drawstyle else None
            ax.fill_between(x, y, step=step, **area_style)

        ax.plot(x, y, **line_style, label=self.label(ctx))


class BarLayer(Layer):
    kind = "bar"

    def _resolve_style(self):
        orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.is_horizontal = orientation == ORIENTATION.HORIZONTAL
        self.bar_style = get_bar_style(self.style, self.is_horizontal)
        self.show_yerr = self.settings.get("show_yerr")
        self.show_values = self.settings.get("show_values")
        self.value_format = self.settings.get("value_format")
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
            ax.bar_label(
                bars,
                fmt=self.value_format,
                padding=self.value_padding,
                fontsize=self.value_fontsize,
                color=self.value_color,
            )


class HistogramLayer(Layer):
    kind = "histogram"

    def _resolve_style(self):
        self.hist_style = get_hist_style(self.style)
        self.orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.show_density = self.settings.get("show_density")
        self.show_cumulative = self.settings.get("show_cumulative")
        self.num_bins = self.settings.get("num_bins") or DEFAULT_NUM_BINS

    def x_values(self) -> Optional[np.ndarray]:
        return get_chart_data("x", self.chart)

    def y_range(self):
        x = self.x_values()
        if x is None or len(x) == 0:
            return None
        counts, _ = np.histogram(x, bins=self.num_bins)
        return (float(np.min(counts)), float(np.max(counts)))

    def draw(self, ax, ctx):
        x = self.x_values()
        if x is None:
            return

        hist_style = self._merge_color("color", ctx.color, self.hist_style)
        if ctx.z_order is not None:
            hist_style["zorder"] = ctx.z_order
        if ctx.alpha is not None:
            hist_style["alpha"] = ctx.alpha

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
        self.regression_style = get_regression_style({})
        self.regression_ci_alpha = config["plot_regression_ci_alpha"]
        self.annotation_color = config.get("plot_text_color", "black")
        self.annotation_fontsize = config.get("plot_annotation_fontsize", 10)

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

    def _draw_regression(self, ax, x, y, color):
        from scipy import stats as scipy_stats

        if len(x) == 0 or len(np.unique(x)) <= 1:
            return

        slope, intercept, _, _, _ = scipy_stats.linregress(x, y)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept

        reg_style = dict(self.regression_style)
        if color is not None:
            reg_style["color"] = color
        ax.plot(x_line, y_line, **reg_style)

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
            ax.fill_between(
                x_line,
                y_line - ci,
                y_line + ci,
                alpha=self.regression_ci_alpha,
                color=color,
            )

    def _draw_correlation(self, ax, x, y, color):
        from ..stats import correlation

        r = correlation(x, y)
        text_color = color if color else self.annotation_color
        ax.annotate(
            f"r = {r:.3f}",
            xy=(0.05, 0.95),
            xycoords="axes fraction",
            fontsize=self.annotation_fontsize,
            color=text_color,
            ha="left",
            va="top",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="white",
                edgecolor="gray",
                alpha=0.8,
            ),
        )

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
                ax.scatter(
                    x_data[mask],
                    y_data[mask],
                    s=group_sizes,
                    label=str(hue_val),
                    **group_style,
                )

            if self.show_correlation:
                self._draw_correlation(ax, x_data, y_data, color=None)
            if self.show_regression:
                self._draw_regression(ax, x_data, y_data, color=None)
        else:
            sizes = self._sizes(size_data)
            base_style = {k: v for k, v in scatter_style.items() if k != "s"}
            if base_style.get("c") is None:
                base_style["c"] = ctx.color

            ax.scatter(x_data, y_data, s=sizes, label=self.label(ctx), **base_style)

            color = base_style.get("c", base_style.get("color"))
            if self.show_regression:
                self._draw_regression(ax, x_data, y_data, color=color)
            if self.show_correlation:
                self._draw_correlation(ax, x_data, y_data, color=color)


class BoxLayer(Layer):
    kind = "box"

    def _resolve_style(self):
        self.orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.show_outliers = self.settings.get("show_outliers")
        self.show_notch = self.settings.get("show_notch")
        self.box_style = get_box_style(self.style)
        self.outlier_style = get_box_outlier_style(self.style)
        self.median_style = get_box_median_style(self.style)
        self.whisker_style = get_box_whisker_style(self.style)
        self.cap_style = get_box_cap_style(self.style)

    def apply_scales(self, ax, scalex, scaley):
        if scaley:
            if self.orientation == ORIENTATION.HORIZONTAL:
                ax.set_xscale(scaley)
            else:
                ax.set_yscale(scaley)

    def draw(self, ax, ctx):
        label_attr = get_attr_value("label", self.chart, "label")
        value_attr = get_attr_value("value", self.chart, "value")

        data = self.chart.get("data", [])
        labels, values = [], []
        if isinstance(data, list):
            grouped = {}
            for d in data:
                lbl, val = d.get(label_attr), d.get(value_attr)
                if lbl is not None and val is not None:
                    grouped.setdefault(lbl, []).append(val)
            labels = list(grouped.keys())
            values = [grouped[lbl] for lbl in labels]

        if len(values) == 0:
            warnings.warn("No data points found for box plot.")
            return

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
        for patch in bp["boxes"]:
            if box_style.get("facecolor"):
                patch.set_facecolor(box_style["facecolor"])
            if alpha is not None:
                patch.set_alpha(alpha)

        if self.orientation == ORIENTATION.HORIZONTAL:
            ax.set_yticks(range(1, len(labels) + 1))
            ax.set_yticklabels(labels, rotation=self.chart.get("ytickrotate", 0))
        else:
            ax.set_xticks(range(1, len(labels) + 1))
            ax.set_xticklabels(labels, rotation=self.chart.get("xtickrotate", 0))


class HeatmapLayer(Layer):
    kind = "heatmap"

    def _resolve_style(self):
        self.show_heatmap_values = self.settings.get("show_heatmap_values")
        self.show_colorbars = self.settings.get("show_colorbars")
        heatmap_style = get_heatmap_style(self.style)
        heatmap_style["cmap"] = get_colormap(heatmap_style["cmap"])
        self.heatmap_style = heatmap_style
        self.font_style = get_heatmap_font_style(self.style)

    def draw(self, ax, ctx):
        data = np.array(self.chart.get("data"))
        assert len(data.shape) == 2, "The `data` attribute is not a 2-dimensional array"

        data = [[(np.nan if item is None else item) for item in row] for row in data]
        valfmt = self.chart.get("valfmt", DEFAULT_VALFMT)
        colorbar = self.chart.get("colorbar", {})

        im = ax.imshow(
            data,
            norm=self.chart.get("norm", None),
            vmin=self.chart.get("vmin", None),
            vmax=self.chart.get("vmax", None),
            **self.heatmap_style,
        )

        if self.show_heatmap_values:
            if isinstance(valfmt, str):
                valfmt = mticker.StrMethodFormatter(valfmt)
            for i in range(len(data)):
                for j in range(len(data[i])):
                    ax.text(
                        j,
                        i,
                        valfmt(data[i][j], None),
                        ha="center",
                        va="center",
                        **self.font_style,
                    )

        if self.show_colorbars:
            orientation = colorbar.get("orientation", DEFAULT_ORIENTATION)
            # inset_axes keeps the colorbar aligned under constrained_layout
            if orientation == ORIENTATION.VERTICAL:
                cax = ax.inset_axes([1.05, 0, 0.05, 1])
            else:
                cax = ax.inset_axes([0, 1.05, 1, 0.05])
            ax.figure.colorbar(im, cax=cax, orientation=orientation)


class ParallelCoordsLayer(Layer):
    """One parallel-coords set; holds every chart's data as a single drawable."""

    kind = "parallelcoords"

    def __init__(self, charts: List[dict], settings: dict):
        self.charts = charts
        super().__init__(charts[0], settings)

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
        unique_hues = sorted(set(h for h in all_hues if h is not None))

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

    def legend_handles(self):
        if not self.unique_hues:
            return None
        return [
            plt.Line2D([0], [0], color=self.hue_colors[hue], linewidth=2, label=hue)
            for hue in self.unique_hues
        ]

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

        first_chart = self.charts[0]
        dimensions = first_chart.get("dimensions", None)
        hue_attr = first_chart.get("hue", "hue")

        if dimensions is None:
            sample = all_data[0]
            dimensions = [
                k for k, v in sample.items() if k != hue_attr and v is not None
            ]

        if len(dimensions) < 2:
            raise ValueError("Parallel coordinates requires at least 2 dimensions.")

        n_dims = len(dimensions)

        dim_values_raw = {
            dim: [d.get(dim, None) for d in all_data] for dim in dimensions
        }
        category_orders = first_chart.get("category_orders", None) or {}

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
                        cat: i / (len(categories) - 1)
                        for i, cat in enumerate(categories)
                    }
            else:
                dim_is_categorical[dim] = False

        dim_min, dim_max, normalized = {}, {}, {}
        for dim in dimensions:
            if dim_is_categorical[dim]:
                cat_map = dim_category_map[dim]
                normalized[dim] = np.array(
                    [
                        cat_map.get(v, np.nan) if v is not None else np.nan
                        for v in dim_values_raw[dim]
                    ]
                )
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
                range_val = dim_max[dim] - dim_min[dim]
                if range_val == 0:
                    normalized[dim] = np.zeros_like(vals)
                else:
                    normalized[dim] = (vals - dim_min[dim]) / range_val

        x_positions = np.arange(n_dims)

        for i, (data_point, hue_val, line_style) in enumerate(
            zip(all_data, all_hues, all_styles)
        ):
            y_vals = [normalized[dim][i] for dim in dimensions]
            line_color = self.hue_colors.get(hue_val, self.default_color)
            style = dict(line_style)
            if style.get("color") is None:
                style["color"] = line_color
            ax.plot(x_positions, y_vals, **style)

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


LAYER_TYPES = {
    "linechart": LineLayer,
    "barchart": BarLayer,
    "histogram": HistogramLayer,
    "scatterchart": ScatterLayer,
    "boxplot": BoxLayer,
    "heatmap": HeatmapLayer,
}


def build_layers(chart_type: str, charts: List[dict], settings: dict) -> List[Layer]:
    """Build the layers for a chart front; style resolution happens here."""

    if chart_type == "parallelcoords":
        return [ParallelCoordsLayer(list(charts), settings)]

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

    def with_prefs(self, *, y_axis, z_order, legend_label) -> "LayerGroup":
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
        )

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
        palette, max_colors = config["color_general_multiple"], max(len(layers), 1)

    return LayerGroup(
        layers,
        palette=palette,
        max_colors=max_colors,
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
    """Assign each layer group to the left or right y-axis."""

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
                "Some charts may be difficult to read. Consider using explicit y_axis assignment or FigureGridLayout."
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

    for side in ("right", "left"):
        side_idx = [i for i, a in enumerate(assignments) if a == side]
        found = False
        for i in range(len(side_idx)):
            for j in range(i + 1, len(side_idx)):
                a, b = side_idx[i], side_idx[j]
                if not _scale_compatible(ranges[a], ranges[b], threshold):
                    warnings.warn(
                        f"Charts at indices {a} and {b} are both on the {side} axis but have "
                        "incompatible scales. Consider using explicit y_axis assignment or FigureGridLayout."
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

    # ---------------- furniture ----------------

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
            },
        }

    def _apply_furniture(self, ax: plt.Axes, axes_types=("xaxis", "yaxis")) -> None:
        furniture = self.settings.get("furniture")
        if furniture is None:
            return
        if "xaxis" in axes_types:
            ax.axis("on")
            for axis, spine_style in furniture["spines"].items():
                ax.spines[axis].set(**spine_style)
        for axis_type in axes_types:
            getattr(ax, axis_type).set_tick_params(which="major", **furniture["ticks"])

    # ---------------- rendering ----------------

    def render(self, ax: plt.Axes) -> None:
        s = self.settings

        box_layers = [l for l in self.layers if isinstance(l, BoxLayer)]
        if len(box_layers) > 1:
            raise ValueError(
                "Multiple box plot datasets require `subplots=True`. "
                "Box plots do not support overlaying multiple datasets on a single axis."
            )

        self._apply_furniture(ax)

        # twin-axis assignment
        assignments = ["left"] * len(self.groups)
        ax_right = None
        if s.get("twin_axes"):
            assignments = determine_axis_assignment(
                self.groups,
                s.get("auto_threshold", 3.0),
                s.get("warn_scale_groups", True),
            )
            if "right" in assignments:
                ax_right = ax.twinx()
                self._apply_furniture(ax_right, axes_types=("yaxis",))

        # bar slotting across every layer in the panel
        bar_layers = [l for l in self.layers if isinstance(l, BarLayer)]
        bar_mode = s.get("bar_mode") or "group"
        if bar_mode not in ["group", "stack", "overlay"]:
            warnings.warn(
                f"Invalid bar_mode '{bar_mode}'. Using 'group' instead. "
                "Valid options are: 'group', 'stack', 'overlay'."
            )
            bar_mode = "group"

        bar_slots = {}
        bar_width = s.get("bar_width", 0.8)
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
                        "Consider using bar_mode='stack', bar_mode='overlay', or FigureGridLayout for better readability."
                    )
                for idx, layer in enumerate(bar_layers):
                    bar_slots[id(layer)] = BarSlot(
                        offset=idx * slot_width, width=slot_width
                    )
            elif bar_mode == "stack":
                bottoms = None
                first_labels = bar_layers[0].labels()
                if first_labels is not None:
                    bottoms = np.zeros(len(first_labels))
                for idx, layer in enumerate(bar_layers):
                    bar_slots[id(layer)] = BarSlot(
                        offset=0.0,
                        width=bar_width,
                        bottom=None if bottoms is None else bottoms.copy(),
                        show_yerr=idx == len(bar_layers) - 1,
                    )
                    y = layer.y_values()
                    if bottoms is not None and y is not None:
                        bottoms = bottoms + np.array(y)
            else:  # overlay
                for layer in bar_layers:
                    bar_slots[id(layer)] = BarSlot(offset=0.0, width=bar_width)

        bar_alpha = None
        if bar_mode == "overlay" and len(bar_layers) > 1:
            bar_alpha = s.get("bar_overlay_alpha")

        # histogram handling: shared bins per group, panel-wide overlay alpha
        hist_layers = [l for l in self.layers if isinstance(l, HistogramLayer)]
        hist_mode = s.get("hist_mode", "stack")
        hist_alpha = None
        if hist_mode == "overlay" and len(hist_layers) > 1:
            hist_alpha = s.get("hist_overlay_alpha")

        zorder_defaults = s.get("zorder_defaults", {})

        # draw the layers group by group, in order
        # one color cycle per palette, pooled across the panel's groups, so
        # composed single-series figures draw in distinct colors
        def palette_key(group):
            return (
                tuple(group.palette)
                if isinstance(group.palette, list)
                else group.palette
            )

        pooled_colors = defaultdict(int)
        for group in self.groups:
            pooled_colors[palette_key(group)] += group.max_colors
        cycles = {}
        for group in self.groups:
            key = palette_key(group)
            if key not in cycles:
                cycles[key] = create_color_cycle(group.palette, pooled_colors[key])

        group_axes = []
        for group, assignment in zip(self.groups, assignments):
            target_ax = ax_right if assignment == "right" else ax
            group_axes.append(target_ax)

            cycle = cycles[palette_key(group)]
            bins = s.get("hist_bins_override")
            if bins is None:
                bins = group.hist_bins()

            group_hists = [l for l in group.layers if isinstance(l, HistogramLayer)]
            if hist_mode == "stack" and len(group_hists) > 0:
                self._draw_hist_stack(target_ax, group, group_hists, cycle, bins)

            for layer in group.layers:
                if isinstance(layer, HistogramLayer) and hist_mode == "stack":
                    continue

                z_order = group.z_order
                if z_order is None:
                    z_order = zorder_defaults.get(layer.kind)

                ctx = DrawContext(
                    color=cycle[layer.chart_hash]["color"],
                    z_order=z_order,
                    legend_label=group.legend_label,
                    alpha=(
                        bar_alpha
                        if isinstance(layer, BarLayer)
                        else (hist_alpha if isinstance(layer, HistogramLayer) else None)
                    ),
                    bar_slot=bar_slots.get(id(layer)),
                    bins=bins,
                )
                layer.draw(target_ax, ctx)

        self._finalize(ax, ax_right, slot_width, bar_layers)

    def _draw_hist_stack(self, ax, group, hist_layers, cycle, bins) -> None:
        """Draw a group's histograms as one stacked call — a cross-layer concern."""

        first = hist_layers[0]
        xall, labels, colors = [], [], []
        for layer in hist_layers:
            xall.append(layer.x_values())
            labels.append(layer.subtitle)
            # the first layer's style is shared; only the cycle color varies
            colors.append(
                first.hist_style.get("color", cycle[layer.chart_hash]["color"])
            )

        hist_style = dict(first.hist_style)
        hist_style["color"] = colors if colors.count(None) == 0 else None

        ax.hist(
            xall,
            bins=bins if bins is not None else first.num_bins,
            label=labels,
            stacked=True,
            density=first.show_density,
            cumulative=first.show_cumulative,
            orientation=first.orientation,
            **{k: v for k, v in hist_style.items() if k != "color"},
            color=hist_style["color"],
        )

    def _finalize(self, ax, ax_right, slot_width, bar_layers) -> None:
        s = self.settings
        layers = self.layers

        # scales (a layer may remap them, e.g. horizontal box plots)
        if layers and (s.get("scalex") or s.get("scaley")):
            layers[0].apply_scales(ax, s.get("scalex"), s.get("scaley"))

        # grid
        if s.get("show_grid"):
            ax.grid(axis=s["show_grid"], **s.get("grid_style", {}))

        # line charts pin the x-limits to their data range
        if s.get("tighten_xlim"):
            for layer in layers:
                if isinstance(layer, LineLayer):
                    rng = layer.x_range()
                    if rng is not None:
                        ax.set_xlim(xmin=rng[0], xmax=rng[1])

        # bar category ticks
        bar_ticks = s.get("bar_ticks")
        if bar_ticks and bar_layers:
            self._apply_bar_ticks(ax, bar_ticks, slot_width, bar_layers)

        # user-provided tick positions
        for layer in layers:
            configure_axis_ticks_position(ax, layer.chart)

        # axis limits
        limits = {k: s.get(k) for k in ("xmin", "xmax", "ymin", "ymax")}
        configure_axis_limits(ax, limits)
        if ax_right is not None and (
            s.get("ymin_right") is not None or s.get("ymax_right") is not None
        ):
            ax_right.set_ylim(bottom=s.get("ymin_right"), top=s.get("ymax_right"))

        # reference lines
        for layer, target_ax in zip(layers, [ax] * len(layers)):
            _draw_ref_lines(target_ax, layer.vlines, layer.hlines)

        # aspect ratio
        if s.get("aspect_ratio"):
            ax.set(adjustable="box", aspect=s["aspect_ratio"])

        # panel-level labels (used when a panel renders into a grid cell)
        label_styles = s.get("label_styles", {})
        for key, action in [
            ("title", ax.set_title),
            ("xlabel", ax.set_xlabel),
            ("ylabel", ax.set_ylabel),
        ]:
            if s.get(key):
                action(s[key], **(label_styles.get(key) or {}))
        if s.get("ylabel_right") and ax_right is not None:
            ax_right.set_ylabel(s["ylabel_right"])

        # legend
        if s.get("show_legend"):
            legend_style = s.get("legend_style", {})
            custom_handles = None
            for layer in layers:
                handles = getattr(layer, "legend_handles", lambda: None)()
                if handles:
                    custom_handles = (custom_handles or []) + handles
            if custom_handles is not None:
                ax.legend(handles=custom_handles, title="Legend", **legend_style)
            elif s.get("legend_mode") == "combined":
                self._combine_legends(ax, ax_right, legend_style)
            elif not any(isinstance(l, ParallelCoordsLayer) for l in layers):
                # parallel coords only carry a legend when hue groups exist
                ax.legend(title="Legend", **legend_style)

    def _apply_bar_ticks(self, ax, bar_ticks, slot_width, bar_layers) -> None:
        is_horizontal = bar_layers[0].is_horizontal
        n = len(bar_layers)
        x_start = np.arange(max(len(l.labels()) for l in bar_layers))

        for layer in bar_layers:
            labels = layer.labels()
            x = np.arange(labels.shape[0])

            if bar_ticks == "group":
                ticks_loc = x_start + (n - 1) / 2 * slot_width
                rotation_default = 0
            else:  # one bar layer per subplot
                ticks_loc = x
                n_labels = labels.shape[0]
                rotation_default = 90 if n_labels >= 7 else (45 if n_labels >= 4 else 0)

            if is_horizontal:
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

    @staticmethod
    def _combine_legends(ax_left, ax_right, legend_style) -> None:
        handles_left, labels_left = ax_left.get_legend_handles_labels()

        if ax_right is not None:
            handles_right, labels_right = ax_right.get_legend_handles_labels()
            labels_left = [f"{label} (L)" for label in labels_left]
            labels_right = [f"{label} (R)" for label in labels_right]
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

    panel_settings = {
        "furniture": Panel.snapshot_furniture(),
        "scalex": settings.get("scalex"),
        "scaley": settings.get("scaley"),
        "show_grid": settings.get("show_grid"),
        "grid_style": get_grid_style(first_style),
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
        "bar_width": config["plot_bar_width"],
        "bar_mode": settings.get("bar_mode") or "group",
        "tighten_xlim": chart_type == "linechart",
    }

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
        panel_settings["label_styles"] = {
            "title": get_text_style("subtitle"),
            "xlabel": get_text_style("xlabel"),
            "ylabel": get_text_style("ylabel"),
        }

    return panel_settings
