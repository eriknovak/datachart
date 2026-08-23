"""Module for overlaying multiple charts on a single plot.

This module provides functionality to combine different chart types (LineChart, BarChart,
ScatterChart, Histogram) on a single plot with support for multiple y-axes.

Methods:
    OverlayChart(charts, title, xlabel, ylabel_left, ylabel_right, figsize, show_legend, auto_secondary_axis):
        (Deprecated) Use datachart.utils.Panel instead, which delegates to the
        same implementation (`_overlay_impl`).

"""

import warnings
from typing import List, Dict, Optional, Tuple, Union, Any

import matplotlib.pyplot as plt

from ..constants import BAR_MODE, FIG_SIZE
from ..config import config
from ._internal.config_helpers import get_grid_style, get_legend_style, get_text_style
from ._internal.figures import new_figure
from ._internal.layers import (
    Panel,
    LayerGroup,
    LineLayer,
    BarLayer,
    ScatterLayer,
    HistogramLayer,
    ParallelCoordsLayer,
)

OVERLAYABLE_LAYERS = (
    LineLayer,
    BarLayer,
    ScatterLayer,
    HistogramLayer,
    ParallelCoordsLayer,
)


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
    if metadata.get("type") == "grid":
        raise ValueError(
            f"Figure at index {index} is a Grid figure; grid figures cannot be overlaid"
        )
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
                    y_axis=group.y_axis,
                    z_order=group.z_order,
                    legend_label=group.legend_label,
                    emphasis=group.emphasis,
                )
            )
    return groups


def _overlay_impl(
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
    bar_mode: Optional[Union[BAR_MODE, str]] = None,
) -> plt.Figure:
    """Render the overlay panel for a normalized list of chart dicts.

    Shared implementation behind `Panel` and the deprecated `OverlayChart`;
    see `datachart.utils.Panel` for the full parameter documentation. Each
    chart dict must contain a "figure" key and may carry "y_axis",
    "z_order", and "legend_label".

    The label and limit parameters address the value and category axes by
    role; the panel's orientation (inferred from the layers, an error when
    mixed) decides which matplotlib axis each one lands on.
    """
    if not charts:
        raise ValueError("At least one chart is required")

    if auto_secondary_axis is None:
        auto_secondary_axis = config.get("overlay_auto_threshold", 3.0)
    if bar_mode is None:
        bar_mode = config.get("overlay_bar_mode", "group")
    if show_grid is None:
        show_grid = config.get("chart_default_show_grid")
    if figsize is None:
        figsize = FIG_SIZE.DEFAULT

    # collect the layer groups from every source figure, tagged with prefs
    groups = []
    for i, chart_config in enumerate(charts):
        if "figure" not in chart_config:
            raise ValueError(f"Chart at index {i} is missing 'figure' key")

        figure = chart_config["figure"]
        for group in _extract_groups(figure, i):
            # None leaves the group's own pref (from a nested panel) in place
            groups.append(
                group.with_prefs(
                    y_axis=chart_config.get("y_axis", None),
                    z_order=chart_config.get("z_order", None),
                    legend_label=chart_config.get("legend_label", None),
                    emphasis=chart_config.get("emphasis", None),
                )
            )

    # the panel takes literal x/y keys; the orientation (raises on a mix) maps them
    if Panel(groups).horizontal:
        xlabel, ylabel_left = ylabel_left, xlabel
        xmin, xmax, ymin, ymax = ymin, ymax, xmin, xmax

    # panel-level settings are resolved against the config here, at build time
    panel_settings = {
        "furniture": Panel.snapshot_furniture(),
        "twin_axes": True,
        "auto_threshold": auto_secondary_axis,
        "warn_scale_groups": config.get("overlay_warn_scale_groups", True),
        "warn_thin_bars": config.get("overlay_warn_thin_bars", True),
        "bar_mode": bar_mode,
        "bar_ticks": "group",
        "bar_width": config.get("plot_bar_width", 0.8),
        "bar_overlay_alpha": config.get("overlay_bar_alpha", 0.7),
        "hist_overlay_alpha": config.get("overlay_hist_alpha", 0.6),
        "zorder_defaults": {
            "bar": config.get("overlay_default_zorder_bar", 1),
            "line": config.get("overlay_default_zorder_line", 2),
            "scatter": config.get("overlay_default_zorder_scatter", 2),
            "histogram": config.get("overlay_default_zorder_hist", 1),
        },
        "show_grid": show_grid,
        "grid_style": get_grid_style({}),
        "hatch_cycle": config.get("plot_hatch_cycle"),
        "show_legend": show_legend,
        "legend_mode": "combined",
        "legend_style": get_legend_style(),
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel_left,
        "ylabel_right": ylabel_right,
        "label_styles": Panel.snapshot_label_styles(),
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "ymin_right": ymin_right,
        "ymax_right": ymax_right,
    }

    panel = Panel(groups, panel_settings)

    fig = new_figure(figsize=figsize)
    ax = fig.subplots()
    # the panel title renders as the figure suptitle when the panel is the figure
    panel.settings = {**panel_settings, "title": None}
    panel.render(ax)
    panel.settings = panel_settings
    if title:
        fig.suptitle(title, **get_text_style("title"))

    fig._chart_metadata = {
        "type": "overlay",
        "panel": panel,
    }

    return fig


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
    bar_mode: Optional[Union[BAR_MODE, str]] = None,
) -> plt.Figure:
    """Overlay multiple charts on a single plot with optional dual value axes.

    .. deprecated::
        Use :func:`datachart.utils.Panel` instead — same behavior, and it also
        accepts bare figures. This function only accepts dict items.

    The panel is horizontal when every bar chart and histogram in it is
    (mixing orientations raises ``ValueError``); the label and limit
    parameters then address the value axis (x) and category axis (y) by role,
    exactly as documented for `Panel`.

    Args:
        charts: List of chart configuration dictionaries. Each dict must contain
            a "figure" key and may contain "y_axis", "z_order", "legend_label".
        title: Title for the combined chart.
        xlabel: Label for the category axis.
        ylabel_left: Label for the primary value axis.
        ylabel_right: Label for the secondary value axis (if using dual axes).
        figsize: Size of the figure (width, height) in inches.
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show ("x", "y", "both", or None).
        auto_secondary_axis: Threshold ratio for automatic secondary axis creation.
        xmin: Minimum value for the category-axis limits.
        xmax: Maximum value for the category-axis limits.
        ymin: Minimum value for the primary value-axis limits.
        ymax: Maximum value for the primary value-axis limits.
        ymin_right: Minimum value for the secondary value-axis limits.
        ymax_right: Maximum value for the secondary value-axis limits.
        bar_mode: How bar and histogram series share the axis: "group",
            "stack", or "overlay". See `BAR_MODE`.

    Returns:
        A matplotlib Figure containing the overlaid charts.
    """
    warnings.warn(
        "OverlayChart is deprecated. Use datachart.utils.Panel instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _overlay_impl(
        charts,
        title=title,
        xlabel=xlabel,
        ylabel_left=ylabel_left,
        ylabel_right=ylabel_right,
        figsize=figsize,
        show_legend=show_legend,
        show_grid=show_grid,
        auto_secondary_axis=auto_secondary_axis,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        ymin_right=ymin_right,
        ymax_right=ymax_right,
        bar_mode=bar_mode,
    )
