"""The module containing the commone `figure` utilites.

The `figure` module provides a set of utilities for manipulating the images.

Methods:
    save_figure(figure, path, dpi, format, transparent):
        Saves the figure into a file using the provided format parameters.
    combine_figures(figures, title, layout_specs, max_cols, figsize, sharex, sharey):
        Combines multiple figure objects into a single grid layout with optional custom layouts.

"""

import math
from typing import List, Optional, Tuple, Dict

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

from ..constants import FIG_FORMAT, FIG_SIZE
from ._internal.plot_engine import CHART_PLOTTERS, get_settings, get_chart_settings
from ._internal.config_helpers import configure_labels

# =====================================
# Helper functions
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


def combine_figures(
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

    This function extracts chart metadata from each figure and recreates them
    in a grid layout. Supports mixing different chart types in the same grid.

    Examples:
        >>> from datachart.charts import LineChart, BarChart, ScatterChart
        >>> from datachart.utils import combine_figures
        >>>
        >>> # Create individual charts
        >>> fig1 = LineChart(data=[{"x": i, "y": i**2} for i in range(10)], title="Line Chart")
        >>> fig2 = BarChart(data=[{"label": "A", "y": 10}, {"label": "B", "y": 20}], title="Bar Chart")
        >>> fig3 = ScatterChart(data=[{"x": i, "y": i*2} for i in range(10)], title="Scatter Chart")
        >>>
        >>> # Example 1: Uniform grid layout (default behavior)
        >>> combined = combine_figures(
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
        >>> combined = combine_figures(
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

        # For figures with multiple subplots, extract only the first chart
        # (since we're placing one chart per grid position)
        if len(charts_list) > 0:
            chart_data = charts_list[0]
        else:
            # Empty chart, skip this position
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
        if "subtitle" in chart_data:
            configure_labels(chart_data, [("subtitle", target_ax.set_title)])
        if settings.get("xlabel"):
            configure_labels(settings, [("xlabel", target_ax.set_xlabel)])
        if settings.get("ylabel"):
            configure_labels(settings, [("ylabel", target_ax.set_ylabel)])

        # Call the plotter function with single chart and single axis
        # Convert chart_data to numpy array format expected by plotters
        charts_array = np.array([chart_data])
        plotter(
            combined_fig,
            [target_ax],
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
