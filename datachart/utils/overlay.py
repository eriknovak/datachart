"""Module for overlaying multiple charts on a single plot.

This module provides functionality to combine different chart types (LineChart, BarChart,
ScatterChart, Histogram) on a single plot with support for multiple y-axes.

Methods:
    OverlayChart(charts, title, xlabel, ylabel_left, ylabel_right, figsize, show_legend, auto_secondary_axis):
        Combines multiple chart figures into a single overlay plot with optional dual y-axes.

"""

import warnings
from typing import List, Dict, Optional, Tuple, Union, Any

import matplotlib.pyplot as plt

from ..constants import FIG_SIZE
from ..config import config
from ._internal.config_helpers import get_grid_style, get_legend_style
from ._internal.layers import (
    Panel,
    LayerGroup,
    LineLayer,
    BarLayer,
    ScatterLayer,
    HistogramLayer,
)

OVERLAYABLE_LAYERS = (LineLayer, BarLayer, ScatterLayer, HistogramLayer)


def _extract_groups(figure: plt.Figure, index: int) -> List[LayerGroup]:
    """Pull the layer groups out of a figure's metadata transport.

    Args:
        figure: A figure created by a datachart chart function.
        index: The figure's position in the `charts` argument, for error messages.

    Returns:
        The figure's layer groups.

    Raises:
        ValueError: If the figure is missing or has invalid chart metadata.
    """
    if not hasattr(figure, "_chart_metadata"):
        raise ValueError(
            "Figure is missing chart metadata. "
            "This figure was likely not created by a datachart chart function."
        )

    metadata = figure._chart_metadata
    if metadata.get("type") is None:
        raise ValueError("Figure has invalid metadata: missing 'type'")
    if metadata.get("charts") is None:
        raise ValueError("Figure has invalid metadata: missing 'charts'")

    panel = metadata.get("panel")
    if panel is None:
        raise ValueError("Figure has invalid metadata: missing 'panel'")

    groups = []
    for group in panel.groups:
        supported = [l for l in group.layers if isinstance(l, OVERLAYABLE_LAYERS)]
        if len(supported) < len(group.layers):
            warnings.warn(
                f"Chart at index {index} contains layers of type "
                f"'{metadata.get('type')}' that cannot be overlaid. Skipping them..."
            )
        if supported:
            groups.append(
                LayerGroup(
                    supported,
                    palette=group.palette,
                    max_colors=group.max_colors,
                    num_bins=group.num_bins,
                )
            )
    return groups


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

    if auto_secondary_axis is None:
        auto_secondary_axis = config.get("overlay_auto_threshold", 3.0)
    if bar_mode is None:
        bar_mode = config.get("overlay_bar_mode", "group")
    if figsize is None:
        figsize = FIG_SIZE.DEFAULT

    # collect the layer groups from every source figure, tagged with prefs
    groups = []
    all_charts = []
    for i, chart_config in enumerate(charts):
        if "figure" not in chart_config:
            raise ValueError(f"Chart at index {i} is missing 'figure' key")

        figure = chart_config["figure"]
        for group in _extract_groups(figure, i):
            groups.append(
                group.with_prefs(
                    y_axis=chart_config.get("y_axis", "auto"),
                    z_order=chart_config.get("z_order", None),
                    legend_label=chart_config.get("legend_label", None),
                )
            )
        metadata_charts = figure._chart_metadata.get("charts")
        if isinstance(metadata_charts, dict):
            all_charts.append(metadata_charts)
        else:
            all_charts.extend(list(metadata_charts))

    # panel-level settings are resolved against the config here, at build time
    panel_settings = {
        "furniture": Panel.snapshot_furniture(),
        "twin_axes": True,
        "auto_threshold": auto_secondary_axis,
        "warn_scale_groups": config.get("overlay_warn_scale_groups", True),
        "warn_thin_bars": config.get("overlay_warn_thin_bars", True),
        "bar_mode": bar_mode,
        "bar_width": config.get("plot_bar_width", 0.8),
        "bar_overlay_alpha": config.get("overlay_bar_alpha", 0.7),
        "hist_mode": "overlay",
        "hist_overlay_alpha": config.get("overlay_hist_alpha", 0.6),
        "zorder_defaults": {
            "bar": config.get("overlay_default_zorder_bar", 1),
            "line": config.get("overlay_default_zorder_line", 2),
            "scatter": config.get("overlay_default_zorder_scatter", 2),
            "histogram": config.get("overlay_default_zorder_hist", 1),
        },
        "show_grid": show_grid,
        "grid_style": get_grid_style({}),
        "show_legend": show_legend,
        "legend_mode": "combined",
        "legend_style": get_legend_style(),
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel_left,
        "ylabel_right": ylabel_right,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "ymin_right": ymin_right,
        "ymax_right": ymax_right,
    }

    panel = Panel(groups, panel_settings)

    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
    # the panel title renders as the figure suptitle when the panel is the figure
    panel.settings = {**panel_settings, "title": None}
    panel.render(ax)
    panel.settings = panel_settings
    if title:
        fig.suptitle(title)

    fig._chart_metadata = {
        "type": "overlay",
        "charts": all_charts,
        "panel": panel,
        "title": title,
        "figsize": figsize,
    }

    return fig
