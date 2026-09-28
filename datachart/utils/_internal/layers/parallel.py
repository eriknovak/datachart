"""The parallel-coordinates layer."""

import warnings
from typing import Callable, List, Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from ..colors import create_color_cycle, create_colormap, get_colormap
from ..validate import AXIS_TEMPORAL, is_number
from ..config_helpers import (
    get_parallel_coords_style,
    get_parallel_axis_style,
    get_parallel_tick_style,
    get_parallel_tick_length,
    get_parallel_tick_label_style,
    get_parallel_tick_label_bbox,
    get_parallel_dim_label_style,
    get_parallel_dim_label_rotation,
    get_parallel_dim_label_pad,
    get_value_label_style,
)
from ....config import config
from .base import (
    EMPHASIS_BACKGROUND,
    Layer,
    _aligned_roles,
    _fill_role,
    _halo_effects,
    _keep_role,
    _resolve_texts,
    axis_kind,
    is_temporal,
)
from .ticks import _widen_to_ticks, date_labels


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
