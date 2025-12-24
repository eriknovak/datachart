"""Module for overlaying multiple charts on a single plot.

This module provides functionality to combine different chart types (LineChart, BarChart,
ScatterChart, Histogram) on a single plot with support for multiple y-axes.

Methods:
    OverlayChart(charts, title, xlabel, ylabel_left, ylabel_right, figsize, show_legend, auto_secondary_axis):
        Combines multiple chart figures into a single overlay plot with optional dual y-axes.

"""

import warnings
from typing import List, Dict, Optional, Tuple, Union, Any

import numpy as np
import matplotlib.pyplot as plt

from ..constants import FIG_SIZE
from ..config import config
from ._internal.plot_engine import (
    get_chart_data,
    plot_vlines,
    plot_hlines,
    has_multiple_subplots,
    custom_color_cycle,
    get_chart_hash,
)
from ._internal.config_helpers import (
    get_line_style,
    get_area_style,
    get_bar_style,
    get_hist_style,
    get_scatter_style,
    get_legend_style,
    get_grid_style,
    configure_axes_spines,
    configure_axis_ticks_style,
    configure_axis_limits,
)


# ================================================
# Helper Functions
# ================================================


def _extract_chart_data(figure: plt.Figure) -> Dict[str, Any]:
    """Extract chart metadata and data from a figure.

    Args:
        figure: The matplotlib Figure object with _chart_metadata attribute.

    Returns:
        Dictionary containing chart type, data, settings, and other metadata.

    Raises:
        ValueError: If figure is missing metadata.
    """
    if not hasattr(figure, "_chart_metadata"):
        raise ValueError(
            "Figure is missing chart metadata. "
            "This figure was likely not created by a datachart chart function."
        )

    metadata = figure._chart_metadata
    chart_type = metadata.get("type")
    charts = metadata.get("charts")

    if chart_type is None:
        raise ValueError("Figure has invalid metadata: missing 'type'")

    if charts is None:
        raise ValueError("Figure has invalid metadata: missing 'charts'")

    # Convert charts to list if it's a single dict
    if isinstance(charts, dict):
        charts_list = [charts]
    elif isinstance(charts, list):
        charts_list = charts
    else:
        charts_list = list(charts)

    return {
        "type": chart_type,
        "charts": charts_list,
        "metadata": metadata,
    }


def _get_data_range(chart_data: Dict[str, Any]) -> Tuple[float, float]:
    """Get the y-axis data range for a chart.

    Args:
        chart_data: Dictionary containing chart type and data.

    Returns:
        Tuple of (min_value, max_value) for the y-axis data.
    """
    chart_type = chart_data["type"]
    charts = chart_data["charts"]

    y_values = []

    for chart in charts:
        if chart_type == "linechart":
            y = get_chart_data("y", chart)
            if y is not None:
                y_values.extend(y)
        elif chart_type == "barchart":
            y = get_chart_data("y", chart)
            if y is not None:
                y_values.extend(y)
        elif chart_type == "scatterchart":
            y = get_chart_data("y", chart)
            if y is not None:
                y_values.extend(y)
        elif chart_type == "histogram":
            # For histogram, we need to compute the histogram values
            x = get_chart_data("x", chart)
            if x is not None:
                # Get histogram settings from metadata
                num_bins = chart_data["metadata"].get("num_bins", 20)
                hist_values, _ = np.histogram(x, bins=num_bins)
                y_values.extend(hist_values)

    if not y_values:
        return (0, 1)

    return (float(np.min(y_values)), float(np.max(y_values)))


def _scale_compatible(
    range1: Tuple[float, float], range2: Tuple[float, float], threshold: float = 3.0
) -> bool:
    """Check if two data ranges are compatible (similar scale).

    Args:
        range1: First range tuple (min, max).
        range2: Second range tuple (min, max).
        threshold: Ratio threshold for determining incompatibility.

    Returns:
        True if ranges are compatible, False otherwise.
    """
    # Calculate the span of each range
    span1 = range1[1] - range1[0]
    span2 = range2[1] - range2[0]

    # Avoid division by zero
    if span1 == 0 or span2 == 0:
        return True

    # Check if ratio exceeds threshold
    ratio = max(span1, span2) / min(span1, span2)
    return ratio < threshold


def _cluster_by_scale_compatibility(
    chart_configs: List[Dict[str, Any]], auto_threshold: float = 3.0
) -> List[List[int]]:
    """Cluster charts into groups based on scale compatibility.

    Uses a simple union-find approach to group charts that have compatible scales.

    Args:
        chart_configs: List of chart configuration dictionaries.
        auto_threshold: Threshold for automatic secondary axis detection.

    Returns:
        List of groups, where each group is a list of chart indices.
    """
    n = len(chart_configs)
    if n == 0:
        return []
    if n == 1:
        return [[0]]

    # Build adjacency matrix of compatible charts
    compatible = [[False] * n for _ in range(n)]
    for i in range(n):
        compatible[i][i] = True  # Chart is compatible with itself
        for j in range(i + 1, n):
            range_i = chart_configs[i]["data_range"]
            range_j = chart_configs[j]["data_range"]
            if _scale_compatible(range_i, range_j, auto_threshold):
                compatible[i][j] = True
                compatible[j][i] = True

    # Simple clustering: group charts that are mutually compatible
    groups = []
    assigned = [False] * n

    for i in range(n):
        if assigned[i]:
            continue

        # Start a new group
        group = [i]
        assigned[i] = True

        # Find all charts compatible with this group
        for j in range(i + 1, n):
            if assigned[j]:
                continue

            # Check if j is compatible with all charts in the current group
            if all(compatible[j][k] for k in group):
                group.append(j)
                assigned[j] = True

        groups.append(group)

    return groups


def _determine_axis_assignment(
    chart_configs: List[Dict[str, Any]], auto_threshold: float = 3.0
) -> List[str]:
    """Determine which axis (left or right) each chart should use.

    Uses a clustering-based approach when all charts have auto assignment.
    Falls back to sequential assignment when there are explicit assignments.

    Args:
        chart_configs: List of chart configuration dictionaries.
        auto_threshold: Threshold for automatic secondary axis detection.

    Returns:
        List of axis assignments ("left" or "right") for each chart.
    """
    n = len(chart_configs)
    if n == 0:
        return []

    # Check if all assignments are auto
    explicit_assignments = [
        chart_config.get("y_axis", "auto") for chart_config in chart_configs
    ]
    all_auto = all(a == "auto" for a in explicit_assignments)

    if all_auto and config.get("overlay_warn_scale_groups", True):
        # Use clustering-based approach for optimal grouping
        groups = _cluster_by_scale_compatibility(chart_configs, auto_threshold)

        # Sort groups by size (descending)
        sorted_groups = sorted(groups, key=len, reverse=True)

        # Assign groups to axes
        assignments = ["left"] * n
        if len(sorted_groups) > 1:
            # Assign second-largest group to right axis
            for chart_idx in sorted_groups[1]:
                assignments[chart_idx] = "right"

        # Warn if there are more than 2 groups
        if len(sorted_groups) > 2:
            warnings.warn(
                f"Found {len(sorted_groups)} scale-incompatible groups but only 2 axes available. "
                f"Groups: {[len(g) for g in sorted_groups]}. "
                "Some charts may be difficult to read. Consider using explicit y_axis assignment or FigureGridLayout."
            )
    else:
        # Use sequential assignment when there are explicit assignments
        assignments = []

        for i, chart_config in enumerate(chart_configs):
            # Check if explicit assignment is provided
            y_axis = chart_config.get("y_axis", "auto")

            if y_axis in ["left", "right"]:
                assignments.append(y_axis)
            else:
                # Auto mode: compare with charts already assigned to left axis
                current_range = chart_config["data_range"]

                # First chart always goes on left
                if i == 0:
                    assignments.append("left")
                else:
                    # Find existing left axis charts
                    left_compatible = False
                    for j in range(i):
                        if assignments[j] == "left":
                            prev_range = chart_configs[j]["data_range"]
                            if _scale_compatible(current_range, prev_range, auto_threshold):
                                left_compatible = True
                                break

                    # Assign to left if compatible, otherwise right
                    if left_compatible:
                        assignments.append("left")
                    else:
                        assignments.append("right")

        # Check for scale incompatibilities and issue warnings (only in non-clustering mode)
        left_charts = [i for i, a in enumerate(assignments) if a == "left"]
        right_charts = [i for i, a in enumerate(assignments) if a == "right"]

        # Warn if multiple charts on right axis have incompatible scales
        if len(right_charts) > 1:
            for i in range(len(right_charts)):
                for j in range(i + 1, len(right_charts)):
                    idx_i, idx_j = right_charts[i], right_charts[j]
                    if not _scale_compatible(
                        chart_configs[idx_i]["data_range"],
                        chart_configs[idx_j]["data_range"],
                        auto_threshold,
                    ):
                        warnings.warn(
                            f"Charts at indices {idx_i} and {idx_j} are both on the right axis but have "
                            "incompatible scales. Consider using explicit y_axis assignment or FigureGridLayout."
                        )
                        break

        # Warn if multiple charts on left axis have incompatible scales
        if len(left_charts) > 1:
            for i in range(len(left_charts)):
                for j in range(i + 1, len(left_charts)):
                    idx_i, idx_j = left_charts[i], left_charts[j]
                    if not _scale_compatible(
                        chart_configs[idx_i]["data_range"],
                        chart_configs[idx_j]["data_range"],
                        auto_threshold,
                    ):
                        warnings.warn(
                            f"Charts at indices {idx_i} and {idx_j} are both on the left axis but have "
                            "incompatible scales. Consider using explicit y_axis assignment or FigureGridLayout."
                        )
                        break

    return assignments


def _plot_line_on_axis(
    ax: plt.Axes,
    charts: List[Dict],
    settings: Dict,
    color_cycle: Any,
    z_order: int,
    color_override: Optional[str] = None,
    legend_label: Optional[str] = None,
) -> None:
    """Plot line chart on axis."""
    for chart in charts:
        x = get_chart_data("x", chart)
        y = get_chart_data("y", chart)
        yerr = get_chart_data("yerr", chart)

        if x is None or y is None:
            continue

        style = chart.get("style", {})
        chart_hash = get_chart_hash(chart)
        line_style = {**color_cycle[chart_hash], **get_line_style(style)}
        line_style["zorder"] = z_order

        if color_override:
            line_style["color"] = color_override

        # Handle error bars
        show_yerr = settings.get("show_yerr", False)
        if show_yerr and yerr is not None and len(yerr) == len(y):
            area_style = {**color_cycle[chart_hash], **get_area_style(style)}
            area_style["zorder"] = z_order - 0.1
            if color_override:
                area_style["color"] = color_override
            ymin = y - yerr
            ymax = y + yerr
            ax.fill_between(x, ymin, ymax, **area_style)

        # Handle area under curve
        show_area = settings.get("show_area", False)
        if show_area:
            area_style = {**color_cycle[chart_hash], **get_area_style(style)}
            area_style["zorder"] = z_order - 0.1
            if color_override:
                area_style["color"] = color_override
            step = (
                line_style["drawstyle"].split("-")[1]
                if "steps-" in line_style.get("drawstyle", "")
                else None
            )
            ax.fill_between(x, y, step=step, **area_style)

        # Use legend_label if provided, otherwise fall back to subtitle
        label = legend_label if legend_label is not None else chart.get("subtitle", None)
        ax.plot(x, y, **line_style, label=label)


def _plot_bar_on_axis(
    ax: plt.Axes,
    charts: List[Dict],
    settings: Dict,
    color_cycle: Any,
    z_order: int,
    color_override: Optional[str] = None,
    legend_label: Optional[str] = None,
    bar_mode: Optional[str] = None,
) -> None:
    """Plot bar chart on axis."""
    from ..constants import ORIENTATION

    orientation = settings.get("orientation", "vertical")
    is_horizontal = orientation == ORIENTATION.HORIZONTAL
    n_charts = len(charts)

    # Get bar_mode from config if not provided
    if bar_mode is None:
        bar_mode = config.get("overlay_bar_mode", "group")

    # Validate bar_mode
    if bar_mode not in ["group", "stack", "overlay"]:
        warnings.warn(
            f"Invalid bar_mode '{bar_mode}'. Using 'group' instead. "
            "Valid options are: 'group', 'stack', 'overlay'."
        )
        bar_mode = "group"

    # For group mode, adjust bar positions to avoid overlap
    if bar_mode == "group":
        x_width = config.get("plot_bar_width", 0.8) / n_charts
    else:
        # For stack and overlay modes, use full width
        x_width = config.get("plot_bar_width", 0.8)

    # Get overlay alpha
    alpha = config.get("overlay_bar_alpha", 0.7) if n_charts > 1 and bar_mode == "overlay" else None

    # For stacked bars, track cumulative bottoms
    bar_bottoms = None
    if bar_mode == "stack":
        # Get the number of positions from the first chart
        first_chart_labels = get_chart_data("label", charts[0])
        if first_chart_labels is not None:
            bar_bottoms = np.zeros(len(first_chart_labels))

    for idx, chart in enumerate(charts):
        y = get_chart_data("y", chart)
        labels = get_chart_data("label", chart)
        yerr = get_chart_data("yerr", chart)

        if y is None or labels is None:
            continue

        x = np.arange(len(labels))

        # Calculate x_offset based on mode
        if bar_mode == "group":
            x_offset = idx * x_width
        else:
            x_offset = 0  # No offset for stack and overlay

        style = chart.get("style", {})
        chart_hash = get_chart_hash(chart)
        bar_style = {**color_cycle[chart_hash], **get_bar_style(style, is_horizontal)}
        bar_style["zorder"] = z_order

        if color_override:
            bar_style["color"] = color_override

        if alpha is not None:
            bar_style["alpha"] = alpha

        # Set bar width
        tmp_attr = "height" if is_horizontal else "width"
        bar_style[tmp_attr] = x_width

        # Error bars (only on the top bar for stacked mode)
        show_yerr = settings.get("show_yerr", False)
        tmp_attr = "xerr" if is_horizontal else "yerr"
        # For stacked bars, only show error bars on the last chart
        show_error = show_yerr and yerr is not None and (bar_mode != "stack" or idx == len(charts) - 1)
        error_range = {tmp_attr: yerr if show_error else None}

        # Use legend_label if provided, otherwise fall back to subtitle
        label = legend_label if legend_label is not None else chart.get("subtitle", None)
        draw_func = ax.barh if is_horizontal else ax.bar

        # Add bottom parameter for stacked bars
        if bar_mode == "stack" and bar_bottoms is not None:
            bottom_attr = "left" if is_horizontal else "bottom"
            bar_style[bottom_attr] = bar_bottoms
            draw_func(x + x_offset, y, label=label, **error_range, **bar_style)
            # Update bottoms for next chart
            bar_bottoms = bar_bottoms + np.array(y)
        else:
            draw_func(x + x_offset, y, label=label, **error_range, **bar_style)


def _plot_scatter_on_axis(
    ax: plt.Axes,
    charts: List[Dict],
    settings: Dict,
    color_cycle: Any,
    z_order: int,
    color_override: Optional[str] = None,
    legend_label: Optional[str] = None,
) -> None:
    """Plot scatter chart on axis."""
    for chart in charts:
        x = get_chart_data("x", chart)
        y = get_chart_data("y", chart)
        size_data = get_chart_data("size", chart)
        hue_data = get_chart_data("hue", chart)

        if x is None or y is None:
            continue

        style = chart.get("style", {})
        scatter_style = get_scatter_style(style)
        scatter_style["zorder"] = z_order

        # Handle size
        if size_data is not None:
            size_range = settings.get("size_range", (20, 200))
            sizes = _normalize_sizes(size_data, size_range)
        else:
            sizes = scatter_style.get("s", config["plot_scatter_size"])

        # Handle hue grouping
        if hue_data is not None:
            unique_hues = np.unique(hue_data)
            n_hues = len(unique_hues)
            hue_color_cycle = custom_color_cycle(False, n_hues)

            for i, hue_val in enumerate(unique_hues):
                mask = hue_data == hue_val
                x_group = x[mask]
                y_group = y[mask]

                if size_data is not None:
                    group_sizes = sizes[mask]
                else:
                    group_sizes = sizes

                group_style = {k: v for k, v in scatter_style.items() if k != "s"}
                group_color = hue_color_cycle[i]["color"]
                if color_override:
                    group_color = color_override
                group_style["c"] = group_color

                ax.scatter(
                    x_group, y_group, s=group_sizes, label=str(hue_val), **group_style
                )
        else:
            chart_hash = get_chart_hash(chart)
            base_style = {k: v for k, v in scatter_style.items() if k != "s"}
            if "c" not in base_style or base_style["c"] is None:
                base_style["c"] = color_cycle[chart_hash]["color"]

            if color_override:
                base_style["c"] = color_override

            # Use legend_label if provided, otherwise fall back to subtitle
            label = legend_label if legend_label is not None else chart.get("subtitle", None)
            ax.scatter(x, y, s=sizes, label=label, **base_style)


def _plot_histogram_on_axis(
    ax: plt.Axes,
    charts: List[Dict],
    settings: Dict,
    color_cycle: Any,
    z_order: int,
    color_override: Optional[str] = None,
    legend_label: Optional[str] = None,
) -> None:
    """Plot histogram on axis."""
    num_bins = settings.get("num_bins", 20)
    orientation = settings.get("orientation", "vertical")

    # Get overlay alpha
    alpha = config.get("overlay_hist_alpha", 0.6) if len(charts) > 1 else None

    # Normalize bin size for all charts
    xall = [get_chart_data("x", chart) for chart in charts]
    xall = [x for x in xall if x is not None]
    if not xall:
        return

    bins = np.histogram(np.hstack(tuple(xall)), bins=num_bins)[1]

    for idx, chart in enumerate(charts):
        x = get_chart_data("x", chart)
        if x is None:
            continue

        style = chart.get("style", {})
        chart_hash = get_chart_hash(chart)
        hist_style = {**color_cycle[chart_hash], **get_hist_style(style)}
        hist_style["zorder"] = z_order

        if color_override:
            hist_style["color"] = color_override

        if alpha is not None:
            hist_style["alpha"] = alpha

        # Use legend_label if provided, otherwise fall back to subtitle
        label = legend_label if legend_label is not None else chart.get("subtitle", None)
        ax.hist(
            x,
            bins=bins,
            label=label,
            density=settings.get("show_density", False),
            cumulative=settings.get("show_cumulative", False),
            orientation=orientation,
            **hist_style,
        )


def _normalize_sizes(sizes: np.ndarray, size_range: tuple) -> np.ndarray:
    """Normalize size values to the specified range."""
    min_size, max_size = size_range
    if sizes.max() == sizes.min():
        return np.full_like(sizes, (min_size + max_size) / 2, dtype=float)
    normalized = (sizes - sizes.min()) / (sizes.max() - sizes.min())
    return normalized * (max_size - min_size) + min_size


def _plot_chart_on_axis(
    ax: plt.Axes,
    chart_data: Dict[str, Any],
    z_order: Optional[int] = None,
    color_override: Optional[str] = None,
    legend_label: Optional[str] = None,
    bar_mode: Optional[str] = None,
) -> None:
    """Plot a chart on the specified axis.

    Args:
        ax: The matplotlib Axes to plot on.
        chart_data: Dictionary containing chart type and data.
        z_order: Optional z-order for layering control.
        color_override: Optional color to override chart colors.
        legend_label: Optional custom legend label to override subtitle.
        bar_mode: Bar chart overlay mode ("group", "stack", or "overlay").
    """
    chart_type = chart_data["type"]
    charts = chart_data["charts"]
    metadata = chart_data["metadata"]

    # Get settings from metadata
    settings = metadata

    # Determine if we have multiple subplots (should be False for overlay)
    has_multi = False

    # Preserve the current config and temporarily apply the chart's original config
    original_config = config.config.copy()
    original_theme = config.theme

    # If this chart has a saved config snapshot, apply it temporarily
    if "config_snapshot" in metadata:
        config.config = metadata["config_snapshot"].copy()
        if "theme" in metadata:
            config.theme = metadata["theme"]

    try:
        # Get default z-order based on chart type
        if z_order is None:
            if chart_type == "barchart":
                z_order = config.get("overlay_default_zorder_bar", 1)
            elif chart_type == "linechart":
                z_order = config.get("overlay_default_zorder_line", 2)
            elif chart_type == "scatterchart":
                z_order = config.get("overlay_default_zorder_scatter", 2)
            elif chart_type == "histogram":
                z_order = config.get("overlay_default_zorder_hist", 1)
            else:
                z_order = 1

        # Get color cycle
        color_cycle = custom_color_cycle(has_multi, len(charts))

        # Plot based on chart type
        if chart_type == "linechart":
            _plot_line_on_axis(
                ax, charts, settings, color_cycle, z_order, color_override, legend_label
            )
        elif chart_type == "barchart":
            _plot_bar_on_axis(
                ax, charts, settings, color_cycle, z_order, color_override, legend_label, bar_mode
            )
        elif chart_type == "scatterchart":
            _plot_scatter_on_axis(
                ax, charts, settings, color_cycle, z_order, color_override, legend_label
            )
        elif chart_type == "histogram":
            _plot_histogram_on_axis(
                ax, charts, settings, color_cycle, z_order, color_override, legend_label
            )
    finally:
        # Restore the original config
        config.config = original_config
        config.theme = original_theme


def _combine_legends(ax_left: plt.Axes, ax_right: Optional[plt.Axes] = None) -> None:
    """Combine legends from left and right axes.

    Args:
        ax_left: The left y-axis.
        ax_right: The optional right y-axis.
    """
    handles_left, labels_left = ax_left.get_legend_handles_labels()

    if ax_right is not None:
        handles_right, labels_right = ax_right.get_legend_handles_labels()
        # Append axis indicator to labels
        labels_left = [f"{label} (L)" for label in labels_left]
        labels_right = [f"{label} (R)" for label in labels_right]

        # Combine
        handles = handles_left + handles_right
        labels = labels_left + labels_right
    else:
        handles = handles_left
        labels = labels_left

    if handles:
        ax_left.legend(handles, labels, title="Legend", **get_legend_style())


# ================================================
# Main Overlay Function
# ================================================


def OverlayChart(
    charts: List[Dict[str, Any]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel_left: Optional[str] = None,
    ylabel_right: Optional[str] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    show_legend: Optional[bool] = False,
    show_grid: Optional[str] = None,
    auto_secondary_axis: Optional[float] = None,
    xmin: Optional[float] = None,
    xmax: Optional[float] = None,
    ymin: Optional[float] = None,
    ymax: Optional[float] = None,
    ymin_right: Optional[float] = None,
    ymax_right: Optional[float] = None,
    bar_mode: Optional[str] = None,
) -> plt.Figure:
    """Overlay multiple charts on a single plot with optional dual y-axes.

    This function combines different chart types (LineChart, BarChart, ScatterChart, Histogram)
    on a single plot. Charts are drawn in the order provided. Multiple y-axes (left and right)
    are supported for handling different scales.

    Examples:
        >>> from datachart.charts import LineChart, BarChart
        >>> from datachart.utils import OverlayChart
        >>>
        >>> # Create individual charts
        >>> bar_fig = BarChart(
        ...     data=[{"label": "A", "y": 100}, {"label": "B", "y": 200}],
        ... )
        >>> line_fig = LineChart(
        ...     data=[{"x": 0, "y": 5}, {"x": 1, "y": 15}],
        ... )
        >>>
        >>> # Combine with dual axes
        >>> combined_fig = OverlayChart(
        ...     charts=[
        ...         {"figure": bar_fig, "y_axis": "left"},
        ...         {"figure": line_fig, "y_axis": "right"},
        ...     ],
        ...     title="Sales Analysis",
        ...     xlabel="Category",
        ...     ylabel_left="Count",
        ...     ylabel_right="Average",
        ...     show_legend=True,
        ... )
        >>>
        >>> # Automatic axis assignment
        >>> combined_fig = OverlayChart(
        ...     charts=[
        ...         {"figure": bar_fig},
        ...         {"figure": line_fig},
        ...     ],
        ...     title="Automatic Axis Assignment",
        ...     auto_secondary_axis=3.0,  # threshold
        ... )

    Args:
        charts: List of chart configuration dictionaries. Each dict must contain:
            - "figure": A matplotlib Figure from datachart chart functions
            - "y_axis" (optional): "left", "right", or "auto" (default: "auto")
            - "z_order" (optional): Integer for layering control (higher values on top)
            - "legend_label" (optional): Custom legend label (overrides chart subtitle)
        title: Title for the combined chart.
        xlabel: Label for x-axis.
        ylabel_left: Label for left y-axis.
        ylabel_right: Label for right y-axis (if using dual axes).
        figsize: Size of the figure (width, height) in inches.
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show ("x", "y", "both", or None).
        auto_secondary_axis: Threshold ratio for automatic secondary axis creation.
            If the ratio of data ranges exceeds this threshold, a secondary axis is created.
            Default is taken from config (overlay_auto_threshold, default 3.0).
        xmin: Minimum value for x-axis limits.
        xmax: Maximum value for x-axis limits.
        ymin: Minimum value for y-axis limits (applies to left y-axis).
        ymax: Maximum value for y-axis limits (applies to left y-axis).
        ymin_right: Minimum value for right y-axis limits.
        ymax_right: Maximum value for right y-axis limits.
        bar_mode: Bar chart overlay mode: "group" (side-by-side), "stack" (stacked), or "overlay" (overlapping).
            Default is taken from config (overlay_bar_mode, default "group").

    Returns:
        A matplotlib Figure containing the overlaid charts.

    Raises:
        ValueError: If charts list is empty or if figures are missing metadata.
    """
    if not charts:
        raise ValueError("At least one chart is required")

    # Require user to specify auto_secondary_axis
    if auto_secondary_axis is None:
        auto_secondary_axis = config.get("overlay_auto_threshold", 3.0)

    # Get default bar_mode from config if not provided
    if bar_mode is None:
        bar_mode = config.get("overlay_bar_mode", "group")

    # Get default figsize from config if not provided
    if figsize is None:
        figsize = FIG_SIZE.DEFAULT

    # Extract data from all figures
    chart_configs = []
    for i, chart_config in enumerate(charts):
        if "figure" not in chart_config:
            raise ValueError(f"Chart at index {i} is missing 'figure' key")

        figure = chart_config["figure"]
        chart_data = _extract_chart_data(figure)
        data_range = _get_data_range(chart_data)

        chart_configs.append(
            {
                "chart_data": chart_data,
                "data_range": data_range,
                "y_axis": chart_config.get("y_axis", "auto"),
                "z_order": chart_config.get("z_order", None),
                "legend_label": chart_config.get("legend_label", None),
            }
        )

    # Determine axis assignments
    axis_assignments = _determine_axis_assignment(chart_configs, auto_secondary_axis)

    # Check if we need a secondary axis
    needs_secondary = "right" in axis_assignments

    # Warn about cramped bar charts
    if bar_mode == "group" and config.get("overlay_warn_thin_bars", True):
        # Count bar charts
        bar_chart_count = sum(
            1 for cc in chart_configs if cc["chart_data"]["type"] == "barchart"
        )
        if bar_chart_count > 1:
            x_width = config.get("plot_bar_width", 0.8) / bar_chart_count
            if x_width < 0.15:
                warnings.warn(
                    f"Bar width ({x_width:.2f}) is very small with {bar_chart_count} bar charts. "
                    "Consider using bar_mode='stack', bar_mode='overlay', or FigureGridLayout for better readability."
                )

    # Create figure and axes
    fig, ax_left = plt.subplots(figsize=figsize, constrained_layout=True)

    # Configure axes
    configure_axes_spines(ax_left)
    configure_axis_ticks_style(ax_left, "xaxis")
    configure_axis_ticks_style(ax_left, "yaxis")

    # Create secondary axis if needed
    ax_right = None
    if needs_secondary:
        ax_right = ax_left.twinx()
        configure_axis_ticks_style(ax_right, "yaxis")

    # Plot each chart on the appropriate axis
    for i, (chart_config, axis_assignment) in enumerate(
        zip(chart_configs, axis_assignments)
    ):
        target_ax = ax_right if axis_assignment == "right" else ax_left

        _plot_chart_on_axis(
            target_ax,
            chart_config["chart_data"],
            z_order=chart_config["z_order"],
            legend_label=chart_config["legend_label"],
            bar_mode=bar_mode,
        )

    # Configure labels
    if xlabel:
        ax_left.set_xlabel(xlabel)
    if ylabel_left:
        ax_left.set_ylabel(ylabel_left)
    if ylabel_right and ax_right:
        ax_right.set_ylabel(ylabel_right)
    if title:
        fig.suptitle(title)

    # Configure axis limits
    if xmin is not None or xmax is not None:
        ax_left.set_xlim(left=xmin, right=xmax)
    if ymin is not None or ymax is not None:
        ax_left.set_ylim(bottom=ymin, top=ymax)
    if ax_right and (ymin_right is not None or ymax_right is not None):
        ax_right.set_ylim(bottom=ymin_right, top=ymax_right)

    # Show grid
    if show_grid:
        ax_left.grid(axis=show_grid, **get_grid_style({}))

    # Combine legends
    if show_legend:
        _combine_legends(ax_left, ax_right)

    # Store chart metadata for compatibility with FigureGridLayout
    # Extract all charts from the input figures
    all_charts = []
    for chart_config in chart_configs:
        chart_data = chart_config["chart_data"]
        all_charts.extend(chart_data["charts"])

    # Store chart_configs for proper reconstruction in FigureGridLayout
    # This preserves the grouping and type information
    stored_chart_configs = []
    for chart_config in chart_configs:
        stored_chart_configs.append(
            {
                "chart_data": chart_config["chart_data"],
                "z_order": chart_config.get("z_order"),
                "legend_label": chart_config.get("legend_label"),
            }
        )

    fig._chart_metadata = {
        "type": "overlay",
        "charts": all_charts,
        "chart_configs": stored_chart_configs,  # Store structured data
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel_left,
        "ylabel_right": ylabel_right,
        "figsize": figsize,
        "show_legend": show_legend,
        "show_grid": show_grid,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "ymin_right": ymin_right,
        "ymax_right": ymax_right,
        "bar_mode": bar_mode,
        "auto_secondary_axis": auto_secondary_axis,
        "axis_assignments": axis_assignments,
        "theme": config.theme,
        "config_snapshot": config.config.copy(),
    }

    return fig
