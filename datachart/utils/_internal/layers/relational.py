"""Relational layers: sankey, treemap, and network."""

import math
from collections import defaultdict
from typing import List, NamedTuple, Optional
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, Patch, PathPatch, Rectangle
from matplotlib.path import Path
from matplotlib.text import Text
from matplotlib.transforms import ScaledTranslation
from ..colors import create_color_cycle
from ..validate import (
    infer_network_nodes,
    first_seen_nodes,
    infer_sankey_columns,
    treemap_record_total,
    validate_network_edge_style,
    validate_sankey_link_color,
)
from ..config_helpers import (
    resolve_font_family,
    get_sankey_style,
    get_treemap_style,
    get_network_style,
    get_text_style,
)
from ....constants import ARROW_STYLE, NETWORK_LAYOUT, NETWORK_LABEL_POSITION
from ....config import config
from .base import (
    DrawContext,
    EMPHASIS_BACKGROUND,
    EMPHASIS_HIGHLIGHT,
    HOLLOW_MARKER_EDGE_WIDTH,
    InkStroke,
    Layer,
    PointLabelMixin,
    _fill_role,
    _format_value,
    _halo_effects,
    _keep_role,
    _lighten,
    _marker_edge_widths,
    _text_size,
    theme_default,
)

# sankey labels: room past the outer columns, the gap to the node bar
SANKEY_LABEL_MARGIN = 0.2


SANKEY_LABEL_PAD = 0.01


# column headings sit this far above the tallest column
SANKEY_COLUMN_LABEL_PAD = 0.03


SANKEY_COLUMN_LABEL_HEADROOM = 0.1


# a ribbon value sits at the ribbon's end, before the node it enters, where no
# label lives; thin ribbons fall back to spots along the centreline
SANKEY_VALUE_POSITIONS = (0.8, 0.65, 0.5, 0.35, 0.2)


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
            theme_default("networkchart", self.settings, "label_position")
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


def _marker_entry(entry) -> tuple:
    """A marker cycle entry as `(marker, hollow)`."""

    if isinstance(entry, dict):
        return entry["marker"], bool(entry.get("hollow"))
    return entry, False
