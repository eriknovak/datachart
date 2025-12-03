from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import chart_plot_wrapper, plot_heatmap
from ..typings import (
    HeatmapSingleChartAttrs,
    HeatmapStyleAttrs,
    HeatmapColorbarAttrs,
)
from ..constants import FIG_SIZE, ORIENTATION

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
    # Detect if data is for multiple heatmaps
    # A single heatmap has data as List[List[value]], multiple heatmaps have List[List[List[value]]]
    is_multi_chart = (
        isinstance(data, list)
        and len(data) > 0
        and isinstance(data[0], list)
        and len(data[0]) > 0
        and isinstance(data[0][0], list)
    )

    # Build the charts structure
    if is_multi_chart:
        charts = []
        for i, chart_data in enumerate(data):
            chart_dict = {"data": chart_data}

            # Add per-chart attributes
            if subtitle is not None and isinstance(subtitle, list):
                chart_dict["subtitle"] = subtitle[i] if i < len(subtitle) else None
            elif subtitle is not None:
                chart_dict["subtitle"] = subtitle

            if style is not None and isinstance(style, list):
                style_val = style[i] if i < len(style) else None
                chart_dict["style"] = style_val if style_val is not None else {}
            elif style is not None:
                chart_dict["style"] = style

            if norm is not None and isinstance(norm, list):
                chart_dict["norm"] = norm[i] if i < len(norm) else None
            elif norm is not None:
                chart_dict["norm"] = norm

            if vmin is not None and isinstance(vmin, list):
                chart_dict["vmin"] = vmin[i] if i < len(vmin) else None
            elif vmin is not None:
                chart_dict["vmin"] = vmin

            if vmax is not None and isinstance(vmax, list):
                chart_dict["vmax"] = vmax[i] if i < len(vmax) else None
            elif vmax is not None:
                chart_dict["vmax"] = vmax

            if valfmt is not None and isinstance(valfmt, list):
                chart_dict["valfmt"] = valfmt[i] if i < len(valfmt) else None
            elif valfmt is not None:
                chart_dict["valfmt"] = valfmt

            if xticks is not None and isinstance(xticks[0] if xticks else None, list):
                chart_dict["xticks"] = xticks[i] if i < len(xticks) else None
            elif xticks is not None:
                chart_dict["xticks"] = xticks

            if xticklabels is not None and isinstance(
                xticklabels[0] if xticklabels else None, list
            ):
                chart_dict["xticklabels"] = (
                    xticklabels[i] if i < len(xticklabels) else None
                )
            elif xticklabels is not None:
                chart_dict["xticklabels"] = xticklabels

            if xtickrotate is not None and isinstance(xtickrotate, list):
                chart_dict["xtickrotate"] = (
                    xtickrotate[i] if i < len(xtickrotate) else None
                )
            elif xtickrotate is not None:
                chart_dict["xtickrotate"] = xtickrotate

            if yticks is not None and isinstance(yticks[0] if yticks else None, list):
                chart_dict["yticks"] = yticks[i] if i < len(yticks) else None
            elif yticks is not None:
                chart_dict["yticks"] = yticks

            if yticklabels is not None and isinstance(
                yticklabels[0] if yticklabels else None, list
            ):
                chart_dict["yticklabels"] = (
                    yticklabels[i] if i < len(yticklabels) else None
                )
            elif yticklabels is not None:
                chart_dict["yticklabels"] = yticklabels

            if ytickrotate is not None and isinstance(ytickrotate, list):
                chart_dict["ytickrotate"] = (
                    ytickrotate[i] if i < len(ytickrotate) else None
                )
            elif ytickrotate is not None:
                chart_dict["ytickrotate"] = ytickrotate

            if colorbar is not None and isinstance(colorbar, list):
                chart_dict["colorbar"] = colorbar[i] if i < len(colorbar) else None
            elif colorbar is not None:
                chart_dict["colorbar"] = colorbar

            charts.append(chart_dict)
    else:
        # Single heatmap
        chart_dict = {"data": data}
        if subtitle is not None:
            chart_dict["subtitle"] = (
                subtitle
                if isinstance(subtitle, str)
                else (subtitle[0] if subtitle else None)
            )
        if style is not None:
            chart_dict["style"] = (
                style if isinstance(style, dict) else (style[0] if style else None)
            )
        if norm is not None:
            chart_dict["norm"] = (
                norm if isinstance(norm, str) else (norm[0] if norm else None)
            )
        if vmin is not None:
            chart_dict["vmin"] = (
                vmin if isinstance(vmin, (int, float)) else (vmin[0] if vmin else None)
            )
        if vmax is not None:
            chart_dict["vmax"] = (
                vmax if isinstance(vmax, (int, float)) else (vmax[0] if vmax else None)
            )
        if valfmt is not None:
            chart_dict["valfmt"] = (
                valfmt if isinstance(valfmt, str) else (valfmt[0] if valfmt else None)
            )
        if xticks is not None:
            chart_dict["xticks"] = xticks
        if xticklabels is not None:
            chart_dict["xticklabels"] = xticklabels
        if xtickrotate is not None:
            chart_dict["xtickrotate"] = (
                xtickrotate
                if isinstance(xtickrotate, int)
                else (xtickrotate[0] if xtickrotate else None)
            )
        if yticks is not None:
            chart_dict["yticks"] = yticks
        if yticklabels is not None:
            chart_dict["yticklabels"] = yticklabels
        if ytickrotate is not None:
            chart_dict["ytickrotate"] = (
                ytickrotate
                if isinstance(ytickrotate, int)
                else (ytickrotate[0] if ytickrotate else None)
            )
        if colorbar is not None:
            chart_dict["colorbar"] = (
                colorbar
                if isinstance(colorbar, dict)
                else (colorbar[0] if colorbar else None)
            )

        charts = chart_dict

    # Build the attrs dict for the internal API
    attrs = {
        "type": "heatmap",
        "charts": charts,
    }

    # Add global attributes
    if title is not None:
        attrs["title"] = title
    if xlabel is not None:
        attrs["xlabel"] = xlabel
    if ylabel is not None:
        attrs["ylabel"] = ylabel
    if figsize is not None:
        attrs["figsize"] = figsize
    if show_colorbars is not None:
        attrs["show_colorbars"] = show_colorbars
    if show_heatmap_values is not None:
        attrs["show_heatmap_values"] = show_heatmap_values
    if aspect_ratio is not None:
        attrs["aspect_ratio"] = aspect_ratio
    if subplots is not None:
        attrs["subplots"] = subplots
    if max_cols is not None:
        attrs["max_cols"] = max_cols
    if sharex is not None:
        attrs["sharex"] = sharex
    if sharey is not None:
        attrs["sharey"] = sharey

    return chart_plot_wrapper(plot_heatmap)(attrs)
