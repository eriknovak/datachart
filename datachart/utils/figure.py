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
from matplotlib.gridspec import GridSpec

from ..constants import FIG_FORMAT

# =====================================
# Helper functions
# =====================================


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
        combined_fig = plt.figure(figsize=figsize, constrained_layout=True)
        gs = GridSpec(max_row, max_col, figure=combined_fig)

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
        combined_fig, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=figsize,
            sharex=sharex,
            sharey=sharey,
            constrained_layout=True,
            squeeze=False,
        )

        axes = axes.flatten()

    # Process each figure: every figure's metadata carries a Panel that can
    # redraw the chart into any axes (the single drawing seam, ADR 0001).
    for idx, fig in enumerate(figures):
        if idx >= len(axes):
            break

        if not hasattr(fig, "_chart_metadata"):
            raise ValueError(
                f"Figure at index {idx} is missing chart metadata. "
                "This figure was likely not created by a datachart chart function."
            )

        metadata = fig._chart_metadata
        if metadata.get("type") is None:
            raise ValueError(
                f"Figure at index {idx} has invalid metadata: missing 'type'"
            )
        if metadata.get("type") == "grid":
            raise ValueError(
                f"Figure at index {idx} is a Grid figure; grid figures cannot be nested"
            )
        panel = metadata.get("panel")
        if panel is None:
            raise ValueError(
                f"Figure at index {idx} has invalid metadata: missing 'panel'"
            )

        target_ax = axes[idx]
        if not panel.layers:
            target_ax.axis("off")
            continue

        # a multi-subplot figure rebuilds its subplot arrangement in the cell
        subplot_panels = metadata.get("panels")
        if subplot_panels and len(subplot_panels) > 1:
            nrows_sub, ncols_sub = metadata.get("shape", (1, len(subplot_panels)))
            sub_gs = target_ax.get_subplotspec().subgridspec(nrows_sub, ncols_sub)
            target_ax.remove()
            for p_idx, subplot_panel in enumerate(subplot_panels):
                sub_ax = combined_fig.add_subplot(
                    sub_gs[p_idx // ncols_sub, p_idx % ncols_sub]
                )
                sub_ax.axis("off")
                subplot_panel.render(sub_ax)
            continue

        target_ax.axis("off")
        panel.render(target_ax)

    # Hide unused subplots (only applicable for uniform grid layout)
    if not layout_specs:
        for idx in range(n_figures, len(axes)):
            axes[idx].axis("off")

    # Add global title if provided
    if title:
        combined_fig.suptitle(title)

    # grid figures carry no panel and cannot be composed further (ADR 0002)
    combined_fig._chart_metadata = {"type": "grid"}

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
