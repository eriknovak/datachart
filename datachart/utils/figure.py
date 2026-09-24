"""The module containing the commone `figure` utilites.

The `figure` module provides a set of utilities for manipulating the images.

Methods:
    save_figure(figure, path, dpi, format, transparent):
        Saves the figure into one file per provided format.

"""

import copy
import math
import os
from typing import FrozenSet, List, Mapping, Optional, Tuple, Union, Dict, Any

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, SubplotSpec

from ..constants import FIG_FORMAT, FIG_SIZE
from ._internal.config_helpers import (
    configure_labels,
    get_legend_style,
    get_text_style,
    resolve_font_family,
)
from ._internal.figures import new_figure
from ._internal.plot_engine import SUBPLOT_FURNITURE_KEYS

# =====================================
# Helper functions
# =====================================

# a grid legend column, as a fraction of a cell; layout widens it to fit
LEGEND_COLUMN_WIDTH = 0.3
# a thin grid row, roughly one text line, as a fraction of a cell (ADR 0007)
LABEL_ROW_HEIGHT = 0.12
# per grid legend edge: the legend's anchor point in its axes and its `loc`
LEGEND_ANCHORS = {
    "right": ((0.0, 0.5), "center left"),
    "left": ((1.0, 0.5), "center right"),
    "top": ((0.5, 0.0), "lower center"),
    "bottom": ((0.5, 1.0), "upper center"),
}


_FORMAT_EXTENSIONS: FrozenSet[str] = frozenset(
    value.lower()
    for name, value in vars(FIG_FORMAT).items()
    if not name.startswith("_") and isinstance(value, str)
)


def _figure_stem(path: str) -> str:
    """The path without its trailing format extension (ADR 0039).

    Only a suffix naming a supported format is stripped, so a dotted file
    name like `fig.v2` keeps every part of itself.
    """
    stem, extension = os.path.splitext(path)
    return stem if extension[1:].lower() in _FORMAT_EXTENSIONS else path


def _cell_content(figure: plt.Figure, idx: int) -> Dict[str, Any]:
    """Build one transport cell's content from a figure's metadata.

    Returns `{"grid": node}` for a nested grid figure or a multi-subplot
    figure, whose subplots rebuild as a grid node with the figure's title,
    axis labels, and sharing, or `{"panel": Panel}` for everything else.
    """
    if not hasattr(figure, "_chart_metadata"):
        raise ValueError(
            f"Figure at index {idx} is missing chart metadata. "
            "This figure was likely not created by a datachart chart function."
        )

    metadata = figure._chart_metadata
    if metadata.get("type") is None:
        raise ValueError(f"Figure at index {idx} has invalid metadata: missing 'type'")
    if metadata.get("type") == "grid":
        if "cells" not in metadata:
            raise ValueError(
                f"Figure at index {idx} is a Grid figure without a cell tree; "
                "it cannot be nested"
            )
        return {"grid": metadata}
    panel = metadata.get("panel")
    if panel is None:
        raise ValueError(f"Figure at index {idx} has invalid metadata: missing 'panel'")

    subplot_panels = metadata.get("panels")
    if panel.layers and subplot_panels and len(subplot_panels) > 1:
        return {"grid": _subplot_node(metadata, subplot_panels)}
    return {"panel": panel}


def _subplot_node(metadata: Dict[str, Any], panels: List[Any]) -> Dict[str, Any]:
    """A multi-subplot figure's metadata as a grid node, one cell per subplot."""
    shape = metadata.get("shape", (1, len(panels)))
    ncols = shape[1]
    cells = [
        {
            "panel": panel,
            "spec": {"row": i // ncols, "col": i % ncols, "rowspan": 1, "colspan": 1},
        }
        for i, panel in enumerate(panels)
    ]
    return {
        "type": "grid",
        "cells": cells,
        "shape": shape,
        **{key: metadata.get(key) for key in SUBPLOT_FURNITURE_KEYS},
    }


def _render_cell(
    owner: plt.Figure,
    cell: Dict[str, Any],
    target_ax: plt.Axes,
    overrides: Optional[Dict[str, Any]] = None,
) -> Optional[plt.Axes]:
    """Draw one transport cell into its pre-created axes.

    `overrides` are the enclosing grids' furniture, laid over the cell
    panel's own settings for this draw only; the stored panel keeps its own.
    Returns the axes the panel drew into; None for a nested grid.
    """
    if "grid" in cell:
        subplot_spec = target_ax.get_subplotspec()
        target_ax.remove()
        _render_grid_node(owner, cell["grid"], subplot_spec, overrides)
        return None

    # each cell's axes carries its panel's projection; polar cells swap
    # the pre-created rectilinear axes for a polar one in the same slot
    if cell["panel"].layers and cell["panel"].projection == "polar":
        subplot_spec = target_ax.get_subplotspec()
        target_ax.remove()
        target_ax = owner.add_subplot(subplot_spec, projection="polar")

    target_ax.axis("off")
    panel = cell["panel"]
    if panel.layers:
        if overrides:
            panel = copy.copy(panel)
            panel.settings = {**panel.settings, **overrides}
        panel.render(target_ax)
    return target_ax


def _render_subplot_panels(
    owner: plt.Figure,
    panels: List[Any],
    shape: Tuple[int, int],
    subplot_spec: SubplotSpec,
) -> None:
    """Draw a multi-subplot figure's per-subplot panels into `subplot_spec`.

    The panels fill a `shape` subgrid of the spec in render order, each on
    its own axes with its own projection; `Annotate` redraws a subplot
    figure this way, while a `Grid` cell rebuilds it as a grid node.
    """
    nrows, ncols = shape
    sub_gs = subplot_spec.subgridspec(nrows, ncols)
    for idx, panel in enumerate(panels):
        ax = owner.add_subplot(
            sub_gs[idx // ncols, idx % ncols],
            projection=("polar" if panel.projection == "polar" else None),
        )
        ax.axis("off")
        panel.render(ax)


def _apply_figure_labels(
    figure: plt.Figure,
    title: Optional[str],
    xlabel: Optional[str],
    ylabel: Optional[str],
) -> None:
    """Set the figure-level title and axis labels that are given, themed."""
    labels = {"title": title, "xlabel": xlabel, "ylabel": ylabel}
    configure_labels(
        {key: text for key, text in labels.items() if text},
        [
            ("title", figure.suptitle),
            ("xlabel", figure.supxlabel),
            ("ylabel", figure.supylabel),
        ],
    )


def _render_grid_node(
    owner: plt.Figure,
    node: Dict[str, Any],
    subplot_spec: Optional[SubplotSpec],
    overrides: Optional[Dict[str, Any]] = None,
) -> None:
    """Rebuild a nested grid inside one parent cell, or fill the owner figure.

    The node is the nested grid figure's own metadata: its cell tree, layout
    shape, title, axis labels, and sharex/sharey. The subgrid nests in the
    owner figure's gridspec so one constrained-layout pass aligns its axes
    envelope with sibling cells. A title reserves a thin heading row rendered
    in the subtitle style — a section heading, not the figure's title — and
    the axis labels a footer row and a left column; sharing stays local to
    the node, anchored on its first shareable axes — or, for a `"col"` x or
    `"row"` y share, on the first one in the cell's column or row. A node
    `legend` — the entries of one cell's axes, for the whole grid — takes the
    outermost column or row on its `edge` (default right), inside the title;
    with no `cell`, the first cell whose axes carry entries lends them. The
    node's `overrides` — and, over them, an enclosing grid's — are laid over
    every cell's panel settings, to any depth.
    """
    overrides = {**node.get("overrides", {}), **(overrides or {})}
    nrows, ncols = node["shape"]
    title, xlabel, ylabel = node.get("title"), node.get("xlabel"), node.get("ylabel")
    legend = node.get("legend")
    edge = legend.get("edge", "right") if legend else None
    heights = (
        ([LABEL_ROW_HEIGHT] if title else [])
        + ([LABEL_ROW_HEIGHT] if edge == "top" else [])
        + [1] * nrows
        + ([LABEL_ROW_HEIGHT] if xlabel else [])
        + ([LABEL_ROW_HEIGHT] if edge == "bottom" else [])
    )
    widths = (
        ([LEGEND_COLUMN_WIDTH] if edge == "left" else [])
        + ([LABEL_ROW_HEIGHT] if ylabel else [])
        + [1] * ncols
        + ([LEGEND_COLUMN_WIDTH] if edge == "right" else [])
    )
    ratios = {"height_ratios": heights, "width_ratios": widths}
    # with no parent cell the grid lays out on the figure's own gridspec
    sub_gs = (
        GridSpec(len(heights), len(widths), figure=owner, **ratios)
        if subplot_spec is None
        else subplot_spec.subgridspec(len(heights), len(widths), **ratios)
    )
    row_offset = (1 if title else 0) + (1 if edge == "top" else 0)
    col_offset = (1 if edge == "left" else 0) + (1 if ylabel else 0)
    body_rows = slice(row_offset, row_offset + nrows)
    body_cols = slice(col_offset, col_offset + ncols)
    if title:
        _label_axes(
            owner,
            sub_gs[0, body_cols],
            title,
            (0.5, 0.0),
            "center",
            "bottom",
            "subtitle",
        )
    if xlabel:
        _label_axes(
            owner,
            sub_gs[row_offset + nrows, body_cols],
            xlabel,
            (0.5, 1.0),
            "center",
            "top",
            "xlabel",
        )
    if ylabel:
        _label_axes(
            owner,
            sub_gs[body_rows, col_offset - 1],
            ylabel,
            (1.0, 0.5),
            "right",
            "center",
            "ylabel",
            90,
        )

    anchors: Dict[Tuple[str, Any], plt.Axes] = {}

    def share_key(mode, layout):
        if mode == "col":
            return ("col", layout["col"])
        if mode == "row":
            return ("row", layout["row"])
        return ("all", None) if mode else None

    # every cell's axes exists before any draws: a cell that measures its
    # text against the layout sees the whole grid
    placed = []
    for cell in node["cells"]:
        layout = cell["spec"]
        row = layout["row"] + row_offset
        col = layout["col"] + col_offset
        cell_spec = sub_gs[
            row : row + layout["rowspan"],
            col : col + layout["colspan"],
        ]
        # grid and polar cells swap their axes and share no cartesian limits
        shareable = "panel" in cell and (
            not cell["panel"].layers or cell["panel"].projection != "polar"
        )
        keys = {
            axis: share_key(node[f"share{axis}"], layout) if shareable else None
            for axis in ("x", "y")
        }
        ax = owner.add_subplot(
            cell_spec,
            sharex=anchors.get(keys["x"]),
            sharey=anchors.get(keys["y"]),
        )
        for key in keys.values():
            if key is not None:
                anchors.setdefault(key, ax)
        placed.append(ax)

    cell_axes = {}
    for index, (cell, ax) in enumerate(zip(node["cells"], placed)):
        ax = _render_cell(owner, cell, ax, overrides)
        if ax is None:
            continue
        if node.get("box_aspect"):
            ax.set_box_aspect(node["box_aspect"])
        cell_axes[index] = ax

    legend_ax = None
    if legend and legend.get("cell") is not None:
        legend_ax = cell_axes.get(legend["cell"])
    elif legend:
        legend_ax = next(
            (ax for ax in cell_axes.values() if _legend_entries(ax)[1]), None
        )
    if legend_ax is not None:
        spec = {
            "right": sub_gs[body_rows, -1],
            "left": sub_gs[body_rows, 0],
            "top": sub_gs[row_offset - 1, body_cols],
            "bottom": sub_gs[-1, body_cols],
        }[edge]
        _legend_axes(owner, spec, legend_ax, legend)


def _label_axes(
    owner: plt.Figure,
    spec: SubplotSpec,
    text: str,
    xy: Tuple[float, float],
    ha: str,
    va: str,
    text_type: str,
    rotation: int = 0,
) -> None:
    """An invisible axes in `spec` carrying one label of a nested grid."""
    ax = owner.add_subplot(spec)
    ax.axis("off")
    ax.text(
        *xy,
        text,
        ha=ha,
        va=va,
        rotation=rotation,
        transform=ax.transAxes,
        **get_text_style(text_type),
    )


def _legend_axes(
    owner: plt.Figure, spec: SubplotSpec, source: plt.Axes, legend: Dict[str, Any]
) -> None:
    """An invisible axes in `spec` carrying the legend of `source`'s entries.

    A row legend with no column count lays its entries side by side.
    """
    handles, labels = _legend_entries(source)
    if not labels:
        return
    ax = owner.add_subplot(spec)
    ax.axis("off")
    edge = legend.get("edge", "right")
    anchor, loc = LEGEND_ANCHORS[edge]
    style = legend["style"]
    if edge in ("top", "bottom"):
        style = {"ncols": len(labels), **style}
    drawn = ax.legend(handles, labels, **style, loc=loc, bbox_to_anchor=anchor)
    if legend.get("family"):
        for text in drawn.get_texts() + [drawn.get_title()]:
            text.set_fontfamily(legend["family"])


def _legend_entries(source: plt.Axes) -> Tuple[list, list]:
    """The legend handles and labels of a cell's axes and its twins."""
    # the marks may sit on a hidden twin of the cell's axes
    handles, labels = [], []
    for sibling in source._twinned_axes.get_siblings(source):
        entries = sibling.get_legend_handles_labels()
        handles += entries[0]
        labels += entries[1]
    return handles, labels


def node_legend(
    legend: Optional[Mapping[str, Any]], edge: str, cell: Optional[int] = None, **style
) -> Dict[str, Any]:
    """A grid node's `legend`: the themed legend style on one `edge`.

    `style` entries override the resolved legend style; `cell` names the cell
    lending its entries, or None for the first cell that has any.
    """
    resolved = {
        k: v
        for k, v in get_legend_style(legend).items()
        if k not in ("loc", "bbox_to_anchor")
    }
    return {
        "cell": cell,
        "edge": edge,
        "style": {**resolved, **style},
        "family": resolve_font_family(),
    }


def _column_window(subplot_spec: SubplotSpec) -> Tuple[float, float]:
    """The horizontal span of a gridspec cell as fractions of the figure width."""
    chain = []
    ss = subplot_spec
    while ss is not None:
        chain.append(ss)
        # a subgridspec's parent cell; None once the outermost gridspec is reached
        ss = getattr(ss.get_gridspec(), "_subplot_spec", None)
    x0, x1 = 0.0, 1.0
    for ss in reversed(chain):
        gs = ss.get_gridspec()
        # a legend column is narrower: edges follow the width ratios
        ratios = gs.get_width_ratios() or [1] * gs.ncols
        edges = np.concatenate([[0.0], np.cumsum(ratios)]) / sum(ratios)
        cols = ss.colspan
        width = x1 - x0
        x0, x1 = (
            x0 + width * edges[cols.start],
            x0 + width * edges[cols.stop],
        )
    return (x0, x1)


def _align_axes_columns(figure: plt.Figure) -> None:
    """Align axes columns across gridspec nesting levels.

    Constrained layout aligns margins only within one gridspec level, so axes
    inside a nested grid or a multi-subplot cell drift horizontally from the
    host grid's columns. After the layout solves, axes whose cells start (or
    end) on the same fractional column edge are pinned to a shared spine
    position; when that moves anything, the layout is frozen so the alignment
    survives later draws.
    """
    figure.canvas.draw()

    lefts: Dict[float, List[plt.Axes]] = {}
    rights: Dict[float, List[plt.Axes]] = {}
    for ax in figure.axes:
        get_ss = getattr(ax, "get_subplotspec", None)
        ss = get_ss() if get_ss is not None else None
        # fixed-aspect axes (polar, heatmaps, square matrix cells) re-inset
        # their box at draw time, so their edges neither anchor nor follow a column
        if ss is None or ax.get_aspect() != "auto" or ax.get_box_aspect():
            continue
        x0f, x1f = _column_window(ss)
        lefts.setdefault(round(x0f, 6), []).append(ax)
        rights.setdefault(round(x1f, 6), []).append(ax)

    moved = False
    for group in lefts.values():
        target = max(ax.get_position().x0 for ax in group)
        for ax in group:
            pos = ax.get_position()
            if abs(pos.x0 - target) > 1e-9 and pos.x1 - target > 0.01:
                ax.set_position([target, pos.y0, pos.x1 - target, pos.height])
                moved = True
    for group in rights.values():
        target = min(ax.get_position().x1 for ax in group)
        for ax in group:
            pos = ax.get_position()
            if abs(pos.x1 - target) > 1e-9 and target - pos.x0 > 0.01:
                ax.set_position([pos.x0, pos.y0, target - pos.x0, pos.height])
                moved = True
    if _pack_square_cells(figure) or moved:
        figure.set_layout_engine("none")


def _pack_square_cells(figure: plt.Figure) -> bool:
    """Close the slack around fixed-aspect cells so a matrix reads as a block.

    A square cell sits centred in its layout slot, and a slot wider than tall
    leaves its slack as a horizontal gap far wider than the vertical one. The
    cells of one nested grid are re-laid at the smaller of the two gaps in
    both directions, centred where the grid was; the layout is then frozen
    by the caller. Returns whether anything moved.
    """

    groups: Dict[Any, Dict[Tuple[int, int], List[plt.Axes]]] = {}
    for ax in figure.axes:
        get_ss = getattr(ax, "get_subplotspec", None)
        ss = get_ss() if get_ss is not None else None
        if ss is None or not ax.get_box_aspect():
            continue
        cell = (ss.rowspan.start, ss.colspan.start)
        groups.setdefault(ss.get_gridspec(), {}).setdefault(cell, []).append(ax)

    moved = False
    for cells in groups.values():
        rows = sorted({r for r, _ in cells})
        cols = sorted({c for _, c in cells})
        if len(rows) < 2 and len(cols) < 2:
            continue
        pos = {cell: axes[0].get_position() for cell, axes in cells.items()}
        side_w = min(p.width for p in pos.values())
        side_h = min(p.height for p in pos.values())
        x0 = {c: min(p.x0 for (_, cc), p in pos.items() if cc == c) for c in cols}
        y0 = {r: min(p.y0 for (rr, _), p in pos.items() if rr == r) for r in rows}
        gaps = [x0[b] - x0[a] - side_w for a, b in zip(cols, cols[1:])]
        gaps += [y0[a] - y0[b] - side_h for a, b in zip(rows, rows[1:])]
        gap = max(min(gaps), 0.0)
        # centre the packed block over the grid's current extent
        left = min(x0.values())
        right = max(x0.values()) + side_w
        top = max(y0.values()) + side_h
        bottom = min(y0.values())
        width = len(cols) * side_w + (len(cols) - 1) * gap
        height = len(rows) * side_h + (len(rows) - 1) * gap
        start_x = left + (right - left - width) / 2
        start_y = bottom + (top - bottom - height) / 2
        for (r, c), axes in cells.items():
            new_x = start_x + cols.index(c) * (side_w + gap)
            new_y = start_y + (len(rows) - 1 - rows.index(r)) * (side_h + gap)
            for ax in axes:
                p = ax.get_position()
                if abs(p.x0 - new_x) > 1e-9 or abs(p.y0 - new_y) > 1e-9:
                    ax.set_position([new_x, new_y, side_w, side_h])
                    moved = True
    return moved


# the grid legend edge each legend location selects; any other takes the right
GRID_LEGEND_EDGES = {
    "outside left": "left",
    "center left": "left",
    "outside top": "top",
    "upper center": "top",
    "outside bottom": "bottom",
    "lower center": "bottom",
}
# the grid furniture laid over every cell's own panel settings
CELL_OVERRIDE_KEYS = ("show_grid", "xmin", "xmax", "ymin", "ymax", "aspect_ratio")


def _figure_grid_layout_impl(
    figures: List[plt.Figure],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    layout_specs: Optional[List[Dict[str, int]]] = None,
    max_cols: Optional[int] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[Dict[str, Any]] = None,
    show_grid: Optional[Any] = None,
    xmin: Optional[float] = None,
    xmax: Optional[float] = None,
    ymin: Optional[float] = None,
    ymax: Optional[float] = None,
    aspect_ratio: Optional[str] = None,
) -> plt.Figure:
    """Internal implementation for figure grid layout.

    The core implementation behind every grid front: `Grid` (nested rows and
    flat form via `_grid_from_dicts`). The grid renders as one node, like a
    nested grid; its title and axis labels stay figure-level.

    Args:
        figures: List of matplotlib Figure objects to combine.
        title: Optional title for the combined figure.
        xlabel: Optional x-axis label for the whole grid.
        ylabel: Optional y-axis label for the whole grid.
        layout_specs: Optional list of layout specifications for custom grid layouts.
        max_cols: Maximum number of columns in the grid layout; default 4.
        figsize: Size of the combined figure (width, height) in inches.
        sharex: Whether to share the x-axis across all subplots.
        sharey: Whether to share the y-axis across all subplots.
        show_legend: Whether to draw one legend for the whole grid.
        legend: The legend setting; its location picks the grid edge.
        show_grid, xmin, xmax, ymin, ymax, aspect_ratio: Laid over every
            cell's own setting when given.

    Returns:
        A new matplotlib Figure containing all charts in a grid layout.
    """
    if not figures:
        raise ValueError("At least one figure is required")

    n_figures = len(figures)

    if layout_specs is not None:
        if len(layout_specs) != n_figures:
            raise ValueError(
                f"layout_specs length ({len(layout_specs)}) must match "
                f"figures length ({n_figures})"
            )
        for idx, spec in enumerate(layout_specs):
            required_keys = {"row", "col", "rowspan", "colspan"}
            if not required_keys.issubset(spec.keys()):
                missing = required_keys - set(spec.keys())
                raise ValueError(
                    f"layout_specs[{idx}] missing required keys: {missing}"
                )

    if layout_specs:
        specs = [dict(spec) for spec in layout_specs]
        nrows = max(spec["row"] + spec["rowspan"] for spec in specs)
        ncols = max(spec["col"] + spec["colspan"] for spec in specs)
    else:
        max_cols = 4 if max_cols is None else max_cols
        nrows = math.ceil(n_figures / max_cols)
        ncols = min(max_cols, n_figures)
        specs = [
            {"row": idx // ncols, "col": idx % ncols, "rowspan": 1, "colspan": 1}
            for idx in range(n_figures)
        ]

    if figsize is None:
        base_size = figures[0].get_size_inches()
        figsize = (base_size[0] * ncols, base_size[1] * nrows)

    # every figure's metadata carries a Panel that redraws the chart into any
    # axes (ADR 0001), or — for a nested grid figure — a cell tree (ADR 0006)
    cells = []
    for idx, (fig, spec) in enumerate(zip(figures, specs)):
        cell = _cell_content(fig, idx)
        cell["spec"] = spec
        cells.append(cell)

    grid_legend = None
    if show_legend:
        location = (legend or {}).get("location")
        grid_legend = node_legend(legend, GRID_LEGEND_EDGES.get(location, "right"))
    given = {
        "show_grid": show_grid,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "aspect_ratio": aspect_ratio,
    }
    overrides = {key: value for key, value in given.items() if value is not None}
    if "show_grid" in overrides:
        # an explicit value, as a front's: a polar cell draws only what it names
        overrides["show_grid_explicit"] = True

    # the recursive cell tree lets this grid nest inside another Grid (ADR 0006)
    node = {
        "type": "grid",
        "cells": cells,
        "shape": (nrows, ncols),
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "sharex": bool(sharex),
        "sharey": bool(sharey),
        "legend": grid_legend,
        "overrides": overrides,
    }

    combined_fig = new_figure(figsize=figsize)
    # the labels are the figure's; nested, the node renders them in its cell
    _render_grid_node(
        combined_fig,
        {**node, "title": None, "xlabel": None, "ylabel": None},
        None,
    )
    _apply_figure_labels(combined_fig, title, xlabel, ylabel)
    _align_axes_columns(combined_fig)

    combined_fig._chart_metadata = node
    return combined_fig


# =====================================
# Main functions
# =====================================


def save_figure(
    figure: plt.Figure,
    path: str,
    dpi: int = 300,
    format: Optional[Union[FIG_FORMAT, List[FIG_FORMAT]]] = None,
    transparent: bool = False,
) -> List[str]:
    """Save the figure to one or more files.

    Writes the rendered figure to disk in the format given by `format` or,
    when omitted, by the file extension. Use a vector format (PDF, SVG) for
    print and papers, PNG with `dpi` >= 300 for raster deliverables, and
    `transparent=True` to drop the figure background for slides and web
    pages. The theme is already baked into the figure, so saving never
    consults the global config.

    Pass a list of formats to write the same figure several times in one
    call. `path` is then a stem: its extension is dropped when it names a
    supported format, and one file per format is written next to it.
    `dpi` and `transparent` apply to every file.

    Examples:
        >>> # 1. create the figure
        >>> from datachart.charts import LineChart
        >>> figure = LineChart({...})

        >>> # 2. save the figure
        >>> from datachart.utils.figure import save_figure
        >>> from datachart.constants import FIG_FORMAT
        >>> path = "/path/to/save/chart.png"
        >>> save_figure(figure, path, dpi=300, format=FIG_FORMAT.PNG, transparent=True)

        >>> # 3. save the same figure as a PDF and a PNG
        >>> save_figure(figure, "/path/to/save/chart", format=[FIG_FORMAT.PDF, FIG_FORMAT.PNG])
        ['/path/to/save/chart.pdf', '/path/to/save/chart.png']

    Args:
        figure: The figure to save.
        path: The path where the figure is saved. A stem when `format` is a list.
        dpi: The DPI of the figure.
        format: The format of the figure, or a list of formats to write. If `None`, the format will be determined from the file extension.
        transparent: Whether to make the background transparent.

    Returns:
        The paths written, in the order the formats were given.

    Raises:
        ValueError: If `format` is an empty list.
    """

    if isinstance(format, list):
        if not format:
            raise ValueError("The `format` list is empty: name at least one format")
        formats = format
        stem = _figure_stem(path)
        paths = [f"{stem}.{fmt}" for fmt in formats]
    else:
        formats, paths = [format], [path]

    # save the figure to one file per format
    for out_path, out_format in zip(paths, formats):
        figure.savefig(out_path, dpi=dpi, format=out_format, transparent=transparent)
    return paths


def _grid_from_dicts(
    charts: List[Dict[str, Any]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    max_cols: Optional[int] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    **furniture: Any,
) -> plt.Figure:
    """Render chart dicts into a grid figure.

    Implementation behind `Grid`'s flat form; see `datachart.utils.Grid` for the full parameter
    documentation. Each chart dict must contain a "figure" key and may
    carry a "layout_spec" dict — all charts or none.
    """
    if not charts:
        raise ValueError("At least one chart is required")

    n_charts = len(charts)

    # Validate and extract figures and layout_specs
    figures = []
    layout_specs = []
    has_custom_layout = False

    for idx, chart_config in enumerate(charts):
        if "figure" not in chart_config:
            raise ValueError(f"Chart at index {idx} is missing 'figure' key")

        figures.append(chart_config["figure"])

        # Check if custom layout_spec is provided
        if "layout_spec" in chart_config:
            has_custom_layout = True
            spec = chart_config["layout_spec"]

            # Validate layout spec
            required_keys = {"row", "col", "rowspan", "colspan"}
            if not required_keys.issubset(spec.keys()):
                missing = required_keys - set(spec.keys())
                raise ValueError(
                    f"charts[{idx}]['layout_spec'] missing required keys: {missing}"
                )

            layout_specs.append(spec)
        else:
            layout_specs.append(None)

    # Determine if we're using custom or automatic layout
    if has_custom_layout:
        # If any chart has custom layout, all must have custom layout
        if any(spec is None for spec in layout_specs):
            raise ValueError(
                "When using custom layout, all charts must have 'layout_spec'. "
                "Mix of custom and automatic layout is not supported."
            )
        use_custom_layout = True
    else:
        use_custom_layout = False
        layout_specs = None

    # Call the underlying implementation
    return _figure_grid_layout_impl(
        figures=figures,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        layout_specs=layout_specs,
        max_cols=max_cols,
        figsize=figsize,
        **furniture,
    )
