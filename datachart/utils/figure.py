"""The module containing the commone `figure` utilites.

The `figure` module provides a set of utilities for manipulating the images.

Methods:
    save_figure(figure, path, dpi, format, transparent):
        Saves the figure into a file using the provided format parameters.
    FigureGridLayout(charts, title, max_cols, figsize, sharex, sharey):
        Combines multiple figure objects into a single grid layout with optional custom layouts.
    figure_grid_layout(figures, title, layout_specs, max_cols, figsize, sharex, sharey):
        (Deprecated) Legacy function for combining figures. Use FigureGridLayout instead.

"""

import math
import warnings
from typing import List, Optional, Tuple, Dict, Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

from ..constants import FIG_FORMAT, FIG_SIZE
from ._internal.plot_engine import CHART_PLOTTERS, get_settings, get_chart_settings
from ._internal.config_helpers import configure_labels

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

    This is the core implementation used by both FigureGridLayout and
    the legacy figure_grid_layout function.

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
                sharex=sharex if sharex else None,
                sharey=sharey if sharey else None,
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

    # Process each figure
    for idx, fig in enumerate(figures):
        if idx >= len(axes):
            break

        # Check for metadata
        if not hasattr(fig, "_chart_metadata"):
            raise ValueError(
                f"Figure at index {idx} is missing chart metadata. "
                "This figure was likely not created by a datachart chart function."
            )

        metadata = fig._chart_metadata
        chart_type = metadata.get("type")
        charts = metadata.get("charts")

        if chart_type is None:
            raise ValueError(
                f"Figure at index {idx} has invalid metadata: missing 'type'"
            )

        if charts is None:
            raise ValueError(
                f"Figure at index {idx} has invalid metadata: missing 'charts'"
            )

        # Special handling for overlay charts
        # Overlay charts store metadata and need to be re-rendered
        if chart_type == "overlay":
            # Import overlay rendering functions
            from .overlay import _plot_chart_on_axis, _combine_legends
            from ._internal.config_helpers import (
                configure_axes_spines,
                configure_axis_ticks_style,
                get_grid_style,
            )

            # Get the target axis
            target_ax = axes[idx]

            # Configure axes spines and ticks
            configure_axes_spines(target_ax)
            configure_axis_ticks_style(target_ax, "xaxis")
            configure_axis_ticks_style(target_ax, "yaxis")

            # Get overlay metadata
            axis_assignments = metadata.get("axis_assignments", [])
            needs_secondary = "right" in axis_assignments

            # Create secondary axis if needed
            target_ax_right = None
            if needs_secondary:
                target_ax_right = target_ax.twinx()
                configure_axis_ticks_style(target_ax_right, "yaxis")

            # Get the stored chart_configs if available (new format)
            chart_configs = metadata.get("chart_configs", None)

            if chart_configs is not None:
                # New format: use stored chart_configs
                for i, (chart_config, axis_assignment) in enumerate(
                    zip(chart_configs, axis_assignments)
                ):
                    target_axis = (
                        target_ax_right if axis_assignment == "right" else target_ax
                    )

                    _plot_chart_on_axis(
                        target_axis,
                        chart_config["chart_data"],
                        z_order=chart_config.get("z_order"),
                        legend_label=chart_config.get("legend_label"),
                        bar_mode=metadata.get("bar_mode", "group"),
                    )
            else:
                # Fallback for old format: try to reconstruct from flattened charts
                # This is a best-effort approach for backward compatibility
                overlay_charts = metadata.get("charts", [])

                # Group charts and plot them
                # Assume each chart is separate for backward compatibility
                for i, (chart, axis_assignment) in enumerate(
                    zip(overlay_charts, axis_assignments)
                ):
                    target_axis = (
                        target_ax_right if axis_assignment == "right" else target_ax
                    )

                    # Wrap each chart in a minimal chart_data structure
                    chart_data = {
                        "type": "linechart",  # Default fallback
                        "charts": [chart],
                        "metadata": metadata,
                    }

                    _plot_chart_on_axis(
                        target_axis,
                        chart_data,
                        z_order=None,
                    )

            # Configure labels
            if metadata.get("xlabel"):
                target_ax.set_xlabel(metadata["xlabel"])
            if metadata.get("ylabel"):
                target_ax.set_ylabel(metadata["ylabel"])
            if metadata.get("ylabel_right") and target_ax_right:
                target_ax_right.set_ylabel(metadata["ylabel_right"])
            if metadata.get("title"):
                target_ax.set_title(metadata["title"])

            # Configure axis limits
            if metadata.get("xmin") is not None or metadata.get("xmax") is not None:
                target_ax.set_xlim(
                    left=metadata.get("xmin"), right=metadata.get("xmax")
                )
            if metadata.get("ymin") is not None or metadata.get("ymax") is not None:
                target_ax.set_ylim(
                    bottom=metadata.get("ymin"), top=metadata.get("ymax")
                )
            if target_ax_right and (metadata.get("ymin_right") is not None or metadata.get("ymax_right") is not None):
                target_ax_right.set_ylim(
                    bottom=metadata.get("ymin_right"), top=metadata.get("ymax_right")
                )

            # Show grid if specified
            show_grid = metadata.get("show_grid")
            if show_grid:
                target_ax.grid(axis=show_grid, **get_grid_style({}))

            # Combine legends
            if metadata.get("show_legend", True):
                _combine_legends(target_ax, target_ax_right)

            # Show the axis
            target_ax.axis("on")
            if target_ax_right:
                target_ax_right.axis("on")

            continue

        # Get the appropriate plotter function
        if chart_type not in CHART_PLOTTERS:
            raise ValueError(
                f"Unknown chart type '{chart_type}' in figure at index {idx}"
            )

        plotter = CHART_PLOTTERS[chart_type]

        # Extract settings from metadata
        settings = get_settings(metadata)
        chart_settings = get_chart_settings(settings)

        # Convert charts to list if needed
        # Charts in metadata can be a dict (single chart) or list (multiple charts)
        if isinstance(charts, dict):
            charts_list = [charts]
        elif isinstance(charts, list):
            charts_list = charts
        else:
            # Handle numpy array or other iterable
            charts_list = list(charts)

        # Skip empty charts
        if len(charts_list) == 0:
            axes[idx].axis("off")
            continue

        # Get the target axis
        target_ax = axes[idx]

        # Hide the axis initially (will be configured by plotter)
        target_ax.axis("off")

        # Configure axes spines and ticks (matching chart_plot_wrapper behavior)
        from ._internal.config_helpers import (
            configure_axes_spines,
            configure_axis_ticks_style,
        )

        configure_axes_spines(target_ax)
        configure_axis_ticks_style(target_ax, "xaxis")
        configure_axis_ticks_style(target_ax, "yaxis")

        # Configure local chart labels (subtitle, xlabel, ylabel)
        # Use first chart's subtitle if available (for single-axis multi-series charts)
        first_chart = charts_list[0]
        if "subtitle" in first_chart:
            configure_labels(first_chart, [("subtitle", target_ax.set_title)])
        if settings.get("xlabel"):
            configure_labels(settings, [("xlabel", target_ax.set_xlabel)])
        if settings.get("ylabel"):
            configure_labels(settings, [("ylabel", target_ax.set_ylabel)])

        # Convert charts to numpy array format expected by plotters
        charts_array = np.array(charts_list)

        # For charts with multiple data series on a single axis (e.g., grouped bars),
        # we need to repeat the same axis for each chart, matching chart_plot_wrapper behavior
        axes_for_plotter = [target_ax for _ in range(len(charts_list))]

        plotter(
            combined_fig,
            axes_for_plotter,
            charts_array,
            settings=chart_settings,
        )

    # Hide unused subplots (only applicable for uniform grid layout)
    if not layout_specs:
        for idx in range(n_figures, len(axes)):
            axes[idx].axis("off")

    # Add global title if provided
    if title:
        combined_fig.suptitle(title)

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

    This function extracts chart metadata from each figure and recreates them
    in a grid layout. Supports mixing different chart types in the same grid.
    Each chart can have custom layout specifications or use automatic uniform grid.

    Examples:
        >>> from datachart.charts import LineChart, BarChart, ScatterChart
        >>> from datachart.utils import FigureGridLayout
        >>>
        >>> # Create individual charts
        >>> fig1 = LineChart(data=[{"x": i, "y": i**2} for i in range(10)], title="Line Chart")
        >>> fig2 = BarChart(data=[{"label": "A", "y": 10}, {"label": "B", "y": 20}], title="Bar Chart")
        >>> fig3 = ScatterChart(data=[{"x": i, "y": i*2} for i in range(10)], title="Scatter Chart")
        >>>
        >>> # Example 1: Automatic uniform grid layout
        >>> combined = FigureGridLayout(
        ...     charts=[
        ...         {"figure": fig1},
        ...         {"figure": fig2},
        ...         {"figure": fig3},
        ...     ],
        ...     title="Mixed Chart Grid",
        ...     max_cols=2,
        ...     figsize=(12, 8)
        ... )
        >>>
        >>> # Example 2: Custom layout with fig1 spanning full width on top
        >>> combined = FigureGridLayout(
        ...     charts=[
        ...         {"figure": fig1, "layout_spec": {"row": 0, "col": 0, "rowspan": 1, "colspan": 2}},
        ...         {"figure": fig2, "layout_spec": {"row": 1, "col": 0, "rowspan": 1, "colspan": 1}},
        ...         {"figure": fig3, "layout_spec": {"row": 1, "col": 1, "rowspan": 1, "colspan": 1}},
        ...     ],
        ...     title="Custom Layout",
        ...     figsize=(12, 8)
        ... )
        >>>
        >>> # Example 3: Mixed auto and custom layout
        >>> combined = FigureGridLayout(
        ...     charts=[
        ...         {"figure": fig1, "layout_spec": {"row": 0, "col": 0, "rowspan": 2, "colspan": 1}},
        ...         {"figure": fig2},  # Auto-placed
        ...         {"figure": fig3},  # Auto-placed
        ...     ],
        ...     title="Mixed Layout"
        ... )

    Args:
        charts: List of chart configuration dictionaries. Each dict must contain:
            - "figure": A matplotlib Figure from datachart chart functions
            - "layout_spec" (optional): Dict with keys 'row', 'col', 'rowspan', 'colspan'
                for custom grid positioning. If omitted, automatic uniform grid layout is used.
        title: Optional title for the combined figure.
        max_cols: Maximum number of columns for automatic grid layout (when layout_spec not provided).
        figsize: Size of the combined figure (width, height) in inches.
            If None, will be calculated based on input figures.
        sharex: Whether to share the x-axis across all subplots.
        sharey: Whether to share the y-axis across all subplots.

    Returns:
        A new matplotlib Figure containing all charts in a grid layout.

    Raises:
        ValueError: If charts list is empty, if a chart is missing 'figure' key,
            if a figure is missing metadata, or if layout_spec is invalid.
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
        "figure_grid_layout is deprecated. Use FigureGridLayout instead, "
        "which provides a cleaner API where figures and layout specs are combined.",
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
