from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import chart_plot_wrapper, plot_heatmap
from ..utils._internal.chart_builder import build_charts_structure, build_attrs_dict
from ..typings import (
    HeatmapStyleAttrs,
    HeatmapColorbarAttrs,
)
from ..constants import FIG_SIZE

# ================================================
# Main Chart Definition
# ================================================


def Heatmap(
    data: Union[
        List[List[Union[int, float, None]]], List[List[List[Union[int, float, None]]]]
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    show_colorbars: Optional[bool] = None,
    show_heatmap_values: Optional[bool] = None,
    aspect_ratio: Optional[str] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[HeatmapStyleAttrs, List[Optional[HeatmapStyleAttrs]]]] = None,
    norm: Optional[Union[str, List[Optional[str]]]] = None,
    vmin: Optional[Union[float, List[Optional[float]]]] = None,
    vmax: Optional[Union[float, List[Optional[float]]]] = None,
    valfmt: Optional[Union[str, List[Optional[str]]]] = None,
    xticks: Optional[
        Union[List[Union[int, float]], List[List[Union[int, float]]]]
    ] = None,
    xticklabels: Optional[Union[List[str], List[List[str]]]] = None,
    xtickrotate: Optional[Union[int, List[Optional[int]]]] = None,
    yticks: Optional[
        Union[List[Union[int, float]], List[List[Union[int, float]]]]
    ] = None,
    yticklabels: Optional[Union[List[str], List[List[str]]]] = None,
    ytickrotate: Optional[Union[int, List[Optional[int]]]] = None,
    colorbar: Optional[
        Union[HeatmapColorbarAttrs, List[Optional[HeatmapColorbarAttrs]]]
    ] = None,
) -> plt.Figure:
    """Creates the heatmap.

    Examples:
        >>> from datachart.charts import Heatmap
        >>> figure = Heatmap(
        ...     data=[
        ...         [1, 2, 3],
        ...         [4, 5, 6],
        ...         [7, 8, 9]
        ...     ],
        ...     title="Basic Heatmap",
        ...     xlabel="X",
        ...     ylabel="Y"
        ... )

    Args:
        data: The data matrix for the heatmap(s). Can be a 2D array for one heatmap,
            or a list of 2D arrays for multiple heatmaps/subplots.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts.
        figsize: The size of the figure.
        show_colorbars: Whether to show the colorbar(s).
        show_heatmap_values: Whether to show values on the heatmap cells.
        aspect_ratio: The aspect ratio of the chart.
        subplots: Whether to create separate subplots for each heatmap.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the heatmap(s).
        norm: Value normalization method(s).
        vmin: Minimum value(s) for normalization.
        vmax: Maximum value(s) for normalization.
        valfmt: Format string(s) for cell values.
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        colorbar: Colorbar configuration(s).

    Returns:
        The figure containing the heatmap.

    """
    # Build the charts structure using shared utility
    # Note: Heatmap data is 2D for single chart, so we use is_2d_data=True
    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        style=style,
        xticks=xticks,
        xticklabels=xticklabels,
        xtickrotate=xtickrotate,
        yticks=yticks,
        yticklabels=yticklabels,
        ytickrotate=ytickrotate,
        is_2d_data=True,
        norm=norm,
        vmin=vmin,
        vmax=vmax,
        valfmt=valfmt,
        colorbar=colorbar,
    )

    # Build the attrs dict using shared utility
    attrs = build_attrs_dict(
        "heatmap",
        charts,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=figsize,
        aspect_ratio=aspect_ratio,
        subplots=subplots,
        max_cols=max_cols,
        sharex=sharex,
        sharey=sharey,
        show_colorbars=show_colorbars,
        show_heatmap_values=show_heatmap_values,
    )

    return chart_plot_wrapper(plot_heatmap)(attrs)
