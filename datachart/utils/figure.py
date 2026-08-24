"""The module containing the commone `figure` utilites.

The `figure` module provides a set of utilities for manipulating the images.

Methods:
    save_figure(figure, path, dpi, format, transparent):
        Saves the figure into a file using the provided format parameters.
    FigureGridLayout(charts, title, max_cols, figsize, sharex, sharey):
        (Deprecated) Use datachart.utils.Grid instead, which delegates to the
        same implementation (`_grid_from_dicts`).
    figure_grid_layout(figures, title, layout_specs, max_cols, figsize, sharex, sharey):
        (Deprecated) Use datachart.utils.Grid instead.

"""

import math
import warnings
from typing import List, Optional, Tuple, Dict, Any

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, SubplotSpec

from ..constants import FIG_FORMAT
from ._internal.config_helpers import get_text_style
from ._internal.figures import new_figure

# =====================================
# Helper functions
# =====================================


def _cell_content(figure: plt.Figure, idx: int) -> Dict[str, Any]:
    """Build one transport cell's content from a figure's metadata.

    Returns one of: `{"grid": node}` for a nested grid figure, `{"panels", "shape"}`
    for a multi-subplot figure, or `{"panel": Panel}` for everything else.
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
        return {
            "panels": subplot_panels,
            "shape": metadata.get("shape", (1, len(subplot_panels))),
        }
    return {"panel": panel}


def _render_cell(owner: plt.Figure, cell: Dict[str, Any], target_ax: plt.Axes) -> None:
    """Draw one transport cell into its pre-created axes."""
    if "grid" in cell:
        subplot_spec = target_ax.get_subplotspec()
        target_ax.remove()
        _render_grid_node(owner, cell["grid"], subplot_spec)
        return

    # a multi-subplot figure rebuilds its subplot arrangement in the cell
    panels = cell.get("panels")
    if panels:
        nrows_sub, ncols_sub = cell["shape"]
        sub_gs = target_ax.get_subplotspec().subgridspec(nrows_sub, ncols_sub)
        target_ax.remove()
        for p_idx, subplot_panel in enumerate(panels):
            sub_ax = owner.add_subplot(
                sub_gs[p_idx // ncols_sub, p_idx % ncols_sub],
                projection=("polar" if subplot_panel.projection == "polar" else None),
            )
            sub_ax.axis("off")
            subplot_panel.render(sub_ax)
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


def _render_grid_node(
    owner: plt.Figure, node: Dict[str, Any], subplot_spec: SubplotSpec
) -> None:
    """Rebuild a nested grid inside one parent cell.

    The node is the nested grid figure's own metadata: its cell tree, layout
    shape, title, and sharex/sharey. The subgrid nests in the owner figure's
    gridspec so one constrained-layout pass aligns its axes envelope with
    sibling cells. A title reserves a thin heading row rendered in
    the subtitle style — a section heading, not the figure's title; sharing
    stays local to the node, anchored on its first shareable axes.
    """
    nrows, ncols = node["shape"]
    title = node.get("title")
    if title:
        # 0.12: thin heading row, roughly one subtitle text line (ADR 0007)
        sub_gs = subplot_spec.subgridspec(
            nrows + 1, ncols, height_ratios=[0.12] + [1] * nrows
        )
        heading_ax = owner.add_subplot(sub_gs[0, :])
        heading_ax.axis("off")
        heading_ax.text(
            0.5,
            0.0,
            title,
            ha="center",
            va="bottom",
            transform=heading_ax.transAxes,
            **get_text_style("subtitle"),
        )
        row_offset = 1
    else:
        sub_gs = subplot_spec.subgridspec(nrows, ncols)
        row_offset = 0

    first_ax = None
    for cell in node["cells"]:
        layout = cell["spec"]
        row = layout["row"] + row_offset
        cell_spec = sub_gs[
            row : row + layout["rowspan"],
            layout["col"] : layout["col"] + layout["colspan"],
        ]
        if "grid" in cell:
            _render_grid_node(owner, cell["grid"], cell_spec)
            continue
        # a multi-subplot cell's spanning axes is removed during render — it
        # must neither anchor nor join the share group (dead-axes crash);
        # polar cells swap their axes and share no cartesian limits either
        shareable = "panels" not in cell and (
            not cell["panel"].layers or cell["panel"].projection != "polar"
        )
        ax = owner.add_subplot(
            cell_spec,
            sharex=first_ax if node["sharex"] and shareable else None,
            sharey=first_ax if node["sharey"] and shareable else None,
        )
        if shareable and first_ax is None:
            first_ax = ax
        _render_cell(owner, cell, ax)


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
        ncols = ss.get_gridspec().ncols
        cols = ss.colspan
        width = x1 - x0
        x0, x1 = (
            x0 + width * cols.start / ncols,
            x0 + width * cols.stop / ncols,
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
        # fixed-aspect axes (polar, heatmaps) re-inset their box at draw time,
        # so their edges neither anchor nor follow a column
        if ss is None or ax.get_aspect() != "auto":
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
    if moved:
        figure.set_layout_engine("none")


def _figure_grid_layout_impl(
    figures: List[plt.Figure],
    *,
    title: Optional[str] = None,
    layout_specs: Optional[List[Dict[str, int]]] = None,
    max_cols: int = 4,
    figsize: Optional[Tuple[float, float]] = None,
    sharex: bool = False,
    sharey: bool = False,
) -> plt.Figure:
    """Internal implementation for figure grid layout.

    The core implementation behind every grid front: `Grid` (nested rows and
    flat form via `_grid_from_dicts`), `FigureGridLayout`, and the legacy
    `figure_grid_layout`.

    Args:
        figures: List of matplotlib Figure objects to combine.
        title: Optional title for the combined figure.
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

    # Add global title if provided
    if title:
        combined_fig.suptitle(title, **get_text_style("title"))

    _align_axes_columns(combined_fig)

    # the recursive cell tree lets this grid nest inside another Grid (ADR 0006)
    combined_fig._chart_metadata = {
        "type": "grid",
        "cells": cells,
        "shape": grid_shape,
        "title": title,
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
    format: FIG_FORMAT = None,
    transparent: bool = False,
) -> None:
    """Save the figure to a file.

    Examples:
        >>> # 1. create the figure
        >>> from datachart.charts import LineChart
        >>> figure = LineChart({...})

        >>> # 2. save the figure
        >>> from datachart.utils.figure import save_figure
        >>> from datachart.constants import FIG_FORMAT
        >>> path = "/path/to/save/chart.png"
        >>> save_figure(figure, path, dpi=300, format=FIG_FORMAT.PNG, transparent=True)

    Args:
        figure: The figure to save.
        path: The path where the figure is saved.
        dpi: The DPI of the figure.
        format: The format of the figure. If `None`, the format will be determined from the file extension.
        transparent: Whether to make the background transparent.
    """

    # save the figure to a file
    figure.savefig(path, dpi=dpi, format=format, transparent=transparent)


def _grid_from_dicts(
    charts: List[Dict[str, Any]],
    *,
    title: Optional[str] = None,
    max_cols: int = 4,
    figsize: Optional[Tuple[float, float]] = None,
    sharex: bool = False,
    sharey: bool = False,
) -> plt.Figure:
    """Render chart dicts into a grid figure.

    Shared implementation behind `Grid`'s flat form and the deprecated
    `FigureGridLayout`; see `datachart.utils.Grid` for the full parameter
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
        layout_specs=layout_specs,
        max_cols=max_cols,
        figsize=figsize,
        sharex=sharex,
        sharey=sharey,
    )


def FigureGridLayout(
    charts: List[Dict[str, Any]],
    *,
    title: Optional[str] = None,
    max_cols: int = 4,
    figsize: Optional[Tuple[float, float]] = None,
    sharex: bool = False,
    sharey: bool = False,
) -> plt.Figure:
    """Combine multiple existing figure objects into a single grid layout.

    .. deprecated::
        Use :func:`datachart.utils.Grid` instead — same behavior, and it also
        accepts bare figures and nested rows that define the layout directly.

    Args:
        charts: List of chart configuration dictionaries. Each dict must contain
            a "figure" key and may contain a "layout_spec" dict with keys
            'row', 'col', 'rowspan', 'colspan' for custom grid positioning.
        title: Optional title for the combined figure.
        max_cols: Maximum number of columns for automatic grid layout.
        figsize: Size of the combined figure (width, height) in inches.
        sharex: Whether to share the x-axis across all subplots.
        sharey: Whether to share the y-axis across all subplots.

    Returns:
        A new matplotlib Figure containing all charts in a grid layout.
    """
    warnings.warn(
        "FigureGridLayout is deprecated. Use datachart.utils.Grid instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _grid_from_dicts(
        charts,
        title=title,
        max_cols=max_cols,
        figsize=figsize,
        sharex=sharex,
        sharey=sharey,
    )


# =====================================
# Legacy functions
# =====================================


def figure_grid_layout(
    figures: List[plt.Figure],
    *,
    title: Optional[str] = None,
    layout_specs: Optional[List[Dict[str, int]]] = None,
    max_cols: Optional[int] = 4,
    figsize: Optional[Tuple[float, float]] = None,
    sharex: Optional[bool] = False,
    sharey: Optional[bool] = False,
) -> plt.Figure:
    """Combine multiple existing figure objects into a single grid layout.

    .. deprecated::
        This function is deprecated. Use :func:`FigureGridLayout` instead,
        which provides a cleaner API where figures and layout specs are combined.

    This function extracts chart metadata from each figure and recreates them
    in a grid layout. Supports mixing different chart types in the same grid.

    Examples:
        >>> from datachart.charts import LineChart, BarChart, ScatterChart
        >>> from datachart.utils import figure_grid_layout
        >>>
        >>> # Create individual charts
        >>> fig1 = LineChart(data=[{"x": i, "y": i**2} for i in range(10)], title="Line Chart")
        >>> fig2 = BarChart(data=[{"label": "A", "y": 10}, {"label": "B", "y": 20}], title="Bar Chart")
        >>> fig3 = ScatterChart(data=[{"x": i, "y": i*2} for i in range(10)], title="Scatter Chart")
        >>>
        >>> # Example 1: Uniform grid layout (default behavior)
        >>> combined = figure_grid_layout(
        ...     [fig1, fig2, fig3],
        ...     title="Mixed Chart Grid",
        ...     max_cols=2,
        ...     figsize=(12, 8)
        ... )
        >>>
        >>> # Example 2: Custom layout with figure 1 spanning full width on top
        >>> layout_specs = [
        ...     {"row": 0, "col": 0, "rowspan": 1, "colspan": 2},  # fig1 spans 2 columns
        ...     {"row": 1, "col": 0, "rowspan": 1, "colspan": 1},  # fig2 left column
        ...     {"row": 1, "col": 1, "rowspan": 1, "colspan": 1},  # fig3 right column
        ... ]
        >>> combined = figure_grid_layout(
        ...     [fig1, fig2, fig3],
        ...     layout_specs=layout_specs,
        ...     title="Custom Layout",
        ...     figsize=(12, 8)
        ... )

    Args:
        figures: List of matplotlib Figure objects to combine. Each figure must have
            `_chart_metadata` attribute (automatically added by datachart chart functions).
        title: Optional title for the combined figure.
        layout_specs: Optional list of layout specifications for custom grid layouts.
            Each specification is a dict with keys: 'row', 'col', 'rowspan', 'colspan'.
            If provided, overrides max_cols. If None, creates uniform grid layout.
        max_cols: Maximum number of columns in the grid layout. Ignored if layout_specs is provided.
        figsize: Size of the combined figure (width, height) in inches.
            If None, will be calculated based on input figures.
        sharex: Whether to share the x-axis across all subplots.
        sharey: Whether to share the y-axis across all subplots.

    Returns:
        A new matplotlib Figure containing all charts in a grid layout.

    Raises:
        ValueError: If figures list is empty, if a figure is missing metadata,
            or if layout_specs length doesn't match figures length.
    """
    warnings.warn(
        "figure_grid_layout is deprecated. Use datachart.utils.Grid instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    return _figure_grid_layout_impl(
        figures=figures,
        title=title,
        layout_specs=layout_specs,
        max_cols=max_cols if max_cols is not None else 4,
        figsize=figsize,
        sharex=sharex if sharex is not None else False,
        sharey=sharey if sharey is not None else False,
    )
