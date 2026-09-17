"""The module containing the commone `figure` utilites.

The `figure` module provides a set of utilities for manipulating the images.

Methods:
    save_figure(figure, path, dpi, format, transparent):
        Saves the figure into one file per provided format.

"""

import math
import os
from typing import FrozenSet, List, Optional, Tuple, Union, Dict, Any

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, SubplotSpec

from ..constants import FIG_FORMAT
from ._internal.config_helpers import configure_labels, get_text_style
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


def _render_cell(owner: plt.Figure, cell: Dict[str, Any], target_ax: plt.Axes) -> None:
    """Draw one transport cell into its pre-created axes."""
    if "grid" in cell:
        subplot_spec = target_ax.get_subplotspec()
        target_ax.remove()
        _render_grid_node(owner, cell["grid"], subplot_spec)
        return

    # each cell's axes carries its panel's projection; polar cells swap
    # the pre-created rectilinear axes for a polar one in the same slot
    if cell["panel"].layers and cell["panel"].projection == "polar":
        subplot_spec = target_ax.get_subplotspec()
        target_ax.remove()
        target_ax = owner.add_subplot(subplot_spec, projection="polar")

    target_ax.axis("off")
    if cell["panel"].layers:
        cell["panel"].render(target_ax)


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
    owner: plt.Figure, node: Dict[str, Any], subplot_spec: SubplotSpec
) -> None:
    """Rebuild a nested grid inside one parent cell.

    The node is the nested grid figure's own metadata: its cell tree, layout
    shape, title, axis labels, and sharex/sharey. The subgrid nests in the
    owner figure's gridspec so one constrained-layout pass aligns its axes
    envelope with sibling cells. A title reserves a thin heading row rendered
    in the subtitle style — a section heading, not the figure's title — and
    the axis labels a footer row and a left column; sharing stays local to
    the node, anchored on its first shareable axes — or, for a `"col"` x or
    `"row"` y share, on the first one in the cell's column or row. A node
    `legend` — the entries of one cell's axes, for the whole grid — takes the
    outermost column or row on its `edge` (default right), inside the title.
    """
    nrows, ncols = node["shape"]
    title, xlabel, ylabel = node.get("title"), node.get("xlabel"), node.get("ylabel")
    legend = node.get("legend")
    edge = legend.get("edge", "right") if legend else None
    band = LABEL_ROW_HEIGHT
    heights = (
        ([band] if title else [])
        + ([band] if edge == "top" else [])
        + [1] * nrows
        + ([band] if xlabel else [])
        + ([band] if edge == "bottom" else [])
    )
    widths = (
        ([LEGEND_COLUMN_WIDTH] if edge == "left" else [])
        + ([band] if ylabel else [])
        + [1] * ncols
        + ([LEGEND_COLUMN_WIDTH] if edge == "right" else [])
    )
    sub_gs = subplot_spec.subgridspec(
        len(heights), len(widths), height_ratios=heights, width_ratios=widths
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

    legend_ax = None
    for index, cell in enumerate(node["cells"]):
        layout = cell["spec"]
        row = layout["row"] + row_offset
        col = layout["col"] + col_offset
        cell_spec = sub_gs[
            row : row + layout["rowspan"],
            col : col + layout["colspan"],
        ]
        if "grid" in cell:
            _render_grid_node(owner, cell["grid"], cell_spec)
            continue
        # polar cells swap their axes and share no cartesian limits
        shareable = not cell["panel"].layers or cell["panel"].projection != "polar"
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
        _render_cell(owner, cell, ax)
        if node.get("box_aspect"):
            ax.set_box_aspect(node["box_aspect"])
        if legend and index == legend["cell"]:
            legend_ax = ax

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
    """An invisible axes in `spec` carrying the legend of `source`'s entries."""
    # the marks may sit on a hidden twin of the cell's axes
    handles, labels = [], []
    for sibling in source._twinned_axes.get_siblings(source):
        entries = sibling.get_legend_handles_labels()
        handles += entries[0]
        labels += entries[1]
    if not labels:
        return
    ax = owner.add_subplot(spec)
    ax.axis("off")
    anchor, loc = LEGEND_ANCHORS[legend.get("edge", "right")]
    drawn = ax.legend(
        handles, labels, **legend["style"], loc=loc, bbox_to_anchor=anchor
    )
    if legend.get("family"):
        for text in drawn.get_texts() + [drawn.get_title()]:
            text.set_fontfamily(legend["family"])


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


def _figure_grid_layout_impl(
    figures: List[plt.Figure],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    layout_specs: Optional[List[Dict[str, int]]] = None,
    max_cols: int = 4,
    figsize: Optional[Tuple[float, float]] = None,
    sharex: bool = False,
    sharey: bool = False,
) -> plt.Figure:
    """Internal implementation for figure grid layout.

    The core implementation behind every grid front: `Grid` (nested rows and
    flat form via `_grid_from_dicts`).

    Args:
        figures: List of matplotlib Figure objects to combine.
        title: Optional title for the combined figure.
        xlabel: Optional x-axis label for the whole grid.
        ylabel: Optional y-axis label for the whole grid.
        layout_specs: Optional list of layout specifications for custom grid layouts.
        max_cols: Maximum number of columns in the grid layout.
        figsize: Size of the combined figure (width, height) in inches.
        sharex: Whether to share the x-axis across all subplots.
        sharey: Whether to share the y-axis across all subplots.

    Returns:
        A new matplotlib Figure containing all charts in a grid layout.
    """
    if not figures:
        raise ValueError("At least one figure is required")

    n_figures = len(figures)

    # Validate layout_specs if provided
    if layout_specs is not None:
        if len(layout_specs) != n_figures:
            raise ValueError(
                f"layout_specs length ({len(layout_specs)}) must match "
                f"figures length ({n_figures})"
            )

        # Validate each layout spec
        for idx, spec in enumerate(layout_specs):
            required_keys = {"row", "col", "rowspan", "colspan"}
            if not required_keys.issubset(spec.keys()):
                missing = required_keys - set(spec.keys())
                raise ValueError(
                    f"layout_specs[{idx}] missing required keys: {missing}"
                )

    # Create figure with custom or uniform layout
    if layout_specs:
        # Custom layout using GridSpec
        # Determine grid size from layout specs
        max_row = max(spec["row"] + spec["rowspan"] for spec in layout_specs)
        max_col = max(spec["col"] + spec["colspan"] for spec in layout_specs)

        # Calculate figure size if not provided
        if figsize is None:
            base_size = figures[0].get_size_inches()
            figsize = (base_size[0] * max_col, base_size[1] * max_row)

        # Create figure and GridSpec
        combined_fig = new_figure(figsize=figsize)
        gs = GridSpec(max_row, max_col, figure=combined_fig)
        grid_shape = (max_row, max_col)

        # Create axes based on layout specs
        axes = []
        for spec in layout_specs:
            ax = combined_fig.add_subplot(
                gs[
                    spec["row"] : spec["row"] + spec["rowspan"],
                    spec["col"] : spec["col"] + spec["colspan"],
                ],
                # add_subplot shares against an Axes, not a bool
                sharex=axes[0] if sharex and axes else None,
                sharey=axes[0] if sharey and axes else None,
            )
            axes.append(ax)
    else:
        # Uniform grid layout (original behavior)
        # Calculate grid layout
        nrows = math.ceil(n_figures / max_cols)
        ncols = min(max_cols, n_figures)

        # Calculate figure size if not provided
        if figsize is None:
            # Use the size of the first figure as a base
            base_size = figures[0].get_size_inches()
            figsize = (base_size[0] * ncols, base_size[1] * nrows)

        # Create new figure with subplots
        combined_fig = new_figure(figsize=figsize)
        axes = combined_fig.subplots(
            nrows=nrows,
            ncols=ncols,
            sharex=sharex,
            sharey=sharey,
            squeeze=False,
        )

        axes = axes.flatten()
        grid_shape = (nrows, ncols)

    # Process each figure: every figure's metadata carries a Panel that can
    # redraw the chart into any axes (the single drawing seam, ADR 0001),
    # or — for a nested grid figure — a recursive cell tree (ADR 0006).
    cells = []
    for idx, fig in enumerate(figures):
        if idx >= len(axes):
            break

        cell = _cell_content(fig, idx)
        cell["spec"] = (
            dict(layout_specs[idx])
            if layout_specs
            else {
                "row": idx // grid_shape[1],
                "col": idx % grid_shape[1],
                "rowspan": 1,
                "colspan": 1,
            }
        )
        cells.append(cell)
        _render_cell(combined_fig, cell, axes[idx])

    # Hide unused subplots (only applicable for uniform grid layout)
    if not layout_specs:
        for idx in range(n_figures, len(axes)):
            axes[idx].axis("off")

    # global title and axis labels, one per figure
    _apply_figure_labels(combined_fig, title, xlabel, ylabel)

    _align_axes_columns(combined_fig)

    # the recursive cell tree lets this grid nest inside another Grid (ADR 0006)
    combined_fig._chart_metadata = {
        "type": "grid",
        "cells": cells,
        "shape": grid_shape,
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "sharex": sharex,
        "sharey": sharey,
    }

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

    !!! info "Added in Unreleased"

        The list form of `format`, and the returned paths.

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
    max_cols: int = 4,
    figsize: Optional[Tuple[float, float]] = None,
    sharex: bool = False,
    sharey: bool = False,
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
        sharex=sharex,
        sharey=sharey,
    )
