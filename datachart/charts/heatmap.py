from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..typings import (
    HeatmapDataAttrs,
    HeatmapStyleAttrs,
    HeatmapColorbarAttrs,
    TextAttrs,
)
from ..constants import ASPECT_RATIO, FIG_SIZE, SHOW_GRID, VALUE_FORMAT

# ================================================
# Main Chart Definition
# ================================================


def Heatmap(
    data: Union[HeatmapDataAttrs, List[HeatmapDataAttrs]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: None = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_colorbars: Optional[bool] = None,
    show_heatmap_values: Optional[bool] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[HeatmapStyleAttrs, List[Optional[HeatmapStyleAttrs]]]] = None,
    norm: Optional[Union[str, List[Optional[str]]]] = None,
    vmin: Optional[Union[float, List[Optional[float]]]] = None,
    vmax: Optional[Union[float, List[Optional[float]]]] = None,
    valfmt: Optional[Union[VALUE_FORMAT, str, List[Optional[str]]]] = None,
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
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
) -> plt.Figure:
    """Creates the heatmap.

    A heatmap maps every cell of a 2-D matrix to a color, so structure in a
    grid of numbers (correlations, confusion matrices, feature-by-time tables)
    reads at a glance. Use it when both axes are categorical or gridded and
    the value is what matters; the color scale, colorbar, and cell value labels
    are all configurable.

    !!! info "Added in v0.4.0"

    Examples:
        >>> from datachart.charts import Heatmap
        >>> figure = Heatmap(
        ...     data={
        ...         "x": ["a", "b", "c"],
        ...         "y": ["p", "q", "r"],
        ...         "z": [
        ...             [1, 2, 3],
        ...             [4, 5, 6],
        ...             [7, 8, 9],
        ...         ],
        ...     },
        ...     title="Basic Heatmap",
        ...     xlabel="X",
        ...     ylabel="Y"
        ... )

    Args:
        data: The labelled grid(s) for the heatmap(s): one `{x, y, z}` dict,
            or a list of them for multiple heatmaps/subplots. `z` is the 2-D
            matrix of cell values (rows along `y`, columns along `x`; `None`
            cells stay blank); `x` and `y` are optional tick labels for its
            columns and rows (any values, the indices by default). An
            explicit `xticks`/`xticklabels` (`yticks`/`yticklabels`)
            overrides them.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts.
        emphasis: Not supported: a heatmap is a single raster layer with no
            series to mute or highlight. Passing a value raises `ValueError`.
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend (not typical for heatmaps).
        show_grid: Which grid lines to show (e.g., "both", "x", "y").
        show_colorbars: Whether to show the colorbar(s).
        show_heatmap_values: Whether to show values on the heatmap cells.
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            `ASPECT_RATIO`.
        subplots: Whether to create separate subplots for each heatmap.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the heatmap(s).
        norm: Value normalization method(s).
        vmin: Minimum value(s) for normalization.
        vmax: Maximum value(s) for normalization.
        valfmt: Format string(s) for cell values, with the value named `x`
            (e.g., `"{x:.1f}"`). See `VALUE_FORMAT`.
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        colorbar: Colorbar configuration(s).
        texts: Text annotation(s) to draw.

    Returns:
        The figure containing the heatmap.

    """
    if emphasis is not None:
        raise ValueError(
            "Heatmap does not support `emphasis`: a heatmap is a single "
            "raster layer with no series to mute or highlight."
        )

    if not all(
        isinstance(grid, dict) for grid in (data if isinstance(data, list) else [data])
    ):
        raise ValueError(
            'Heatmap `data` must be a `{"z": [[...], ...]}` dict with optional '
            '`"x"` column labels and `"y"` row labels, or a list of such dicts.'
        )

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
        texts=texts,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "figsize": figsize,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "show_legend": show_legend,
        "show_grid": show_grid,
        "aspect_ratio": aspect_ratio,
        "subplots": subplots,
        "max_cols": max_cols,
        "sharex": sharex,
        "sharey": sharey,
        "show_colorbars": show_colorbars,
        "show_heatmap_values": show_heatmap_values,
    }

    return render_chart("heatmap", charts, settings)
