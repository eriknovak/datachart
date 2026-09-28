"""Grouped-distribution layers: box, swarm, dumbbell, violin, ridgeline."""

import warnings
from collections import defaultdict
from typing import List, Optional
import numpy as np
from matplotlib import cbook
import matplotlib.ticker as mticker
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.mlab import GaussianKDE
from matplotlib.patches import Patch
from matplotlib.transforms import offset_copy
from ..colors import create_color_cycle, get_discrete_colors
from ..validate import (
    is_missing,
    validate_dumbbell_sort_by,
    validate_marker_pair,
    validate_overlap,
    validate_ridge_marks,
)
from ..config_helpers import (
    get_dumbbell_style,
    get_box_style,
    get_box_outlier_style,
    get_box_median_style,
    get_box_whisker_style,
    get_box_cap_style,
    get_swarm_style,
    get_violin_style,
    get_violin_inner_style,
    get_ridgeline_style,
)
from ...stats import kde1d
from ....constants import (
    COLORS,
    DUMBBELL_SORT_KEY,
    DUMBBELL_VALUE,
    ORIENTATION,
    RIDGELINE_SCALE,
    AXIS_SCALE,
    SORT,
    SWARM_MODE,
    VIOLIN_INNER,
)
from ....config import config
from .base import (
    CategoryGroupMixin,
    DEFAULT_ORIENTATION,
    DrawContext,
    EMPHASIS_BACKGROUND,
    EMPHASIS_HIGHLIGHT,
    HIGHLIGHT_WIDTH_SCALE,
    Layer,
    MARKER_ROLE_ORDER,
    MUTED_WIDTH_SCALE,
    NO_LEGEND,
    POINT_LABEL_SPOTS,
    POINT_LABEL_SPOTS_VERTICAL,
    PackedMarksMixin,
    PointLabelMixin,
    TEXT_ANNOTATION_ZORDER,
    UnclippedMarksMixin,
    _aligned_roles,
    _annotate_value,
    _draw_scatter_marks,
    _fill_role,
    _format_value,
    _keep_role,
    _lighten,
    _point_resolver,
    _present_range,
    _rule_summary,
    _validated_record_roles,
    resolve_value_kind,
    theme_default,
)
from .ticks import _widen_to_ticks

DEFAULT_SWARM_MODE = SWARM_MODE.SWARM


DEFAULT_SWARM_JITTER = 0.4


# swarm offsets stay inside the category cell, clear of its neighbors
SWARM_MAX_OFFSET = 0.4


# a raincloud's extremes sit past their points along the value axis, clear of
# the box whiskers beside the rain (ADR 0033)
POINT_LABEL_SPOTS_HORIZONTAL = POINT_LABEL_SPOTS[:2]


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


class GroupLayer(CategoryGroupMixin, Layer):
    """A layer of labeled groups placed on the panel's category index."""

    on_category_axis = True

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

    def bracket_values(self) -> dict:
        return self.grouped_values()

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


class SwarmLayer(UnclippedMarksMixin, PointLabelMixin, PackedMarksMixin, GroupLayer):
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
            theme_default("ridgelineplot", self.settings, "overlap")
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
