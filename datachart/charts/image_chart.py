from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import validate_draw_position
from ..typings import ImageDataAttrs, ImageStyleAttrs
from ..constants import ASPECT_RATIO, FIG_SIZE, DRAW_POSITION, SHOW_GRID

# ================================================
# Main Chart Definition
# ================================================


def ImageChart(
    data: Union[ImageDataAttrs, List[ImageDataAttrs]],
    *,
    position: Optional[Union[DRAW_POSITION, str]] = None,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[ImageStyleAttrs, List[Optional[ImageStyleAttrs]]]] = None,
) -> plt.Figure:
    """Creates the image chart.

    An image chart places a picture in data coordinates: its pixels stretch
    to fill an `extent`, the `(xmin, xmax, ymin, ymax)` rectangle it covers
    on the axes. On its own it is a picture with axes; its use is under
    another chart that shares its coordinates, composed with `Panel` — a
    scatter of stations over a floor plan, a heatmap over a microscope
    image, epicentres over a relief grid. The picture is a file path, a PIL
    image, an RGB(A) array, or a 2-D array read through a colormap.

    The picture carries no series: it takes no cycle color, no legend entry
    and no emphasis. `position` decides where it sits in the draw order,
    under the gridlines and every mark by default, so the order of the
    figures in `Panel` never does. Its extent counts toward the axis
    limits like any other chart's data, and `xmin`, `xmax`, `ymin` and
    `ymax` narrow them back.

    Examples:
        >>> import numpy as np
        >>> from datachart.charts import ImageChart, ScatterChart
        >>> from datachart.utils import Panel
        >>> relief = np.outer(np.linspace(0, 1, 50), np.linspace(1, 0, 80))
        >>> figure = Panel(
        ...     [
        ...         ImageChart({"image": relief, "extent": (0, 8, 0, 5)}),
        ...         ScatterChart([{"x": 2, "y": 1}, {"x": 6, "y": 4}]),
        ...     ],
        ...     title="Stations on the relief",
        ... )

    Args:
        data: The picture and where it sits: a `{"image", "extent"}` dict, or a
            list of them to overlay several pictures or draw one per subplot. See
            [`ImageDataAttrs`][datachart.typings.ImageDataAttrs].
        position: Where the picture sits in the draw order: `"below"` (default)
            under the gridlines and every mark, or `"above"` over the marks and
            under the reference lines. See
            [`DRAW_POSITION`][datachart.constants.DRAW_POSITION].
        title: The title of the chart.
        xlabel: The label of the x-axis.
        ylabel: The label of the y-axis.
        subtitle: The subtitle of each chart.
        figsize: The size of the figure as (width, height) in inches. See
            [`FIG_SIZE`][datachart.constants.FIG_SIZE].
        xmin: The minimum value of the x-axis.
        xmax: The maximum value of the x-axis.
        ymin: The minimum value of the y-axis.
        ymax: The maximum value of the y-axis.
        vmin: The value at the low end of the colormap; a 2-D array only.
        vmax: The value at the high end of the colormap; a 2-D array only.
        show_grid: Which grid lines to show ("both", "x", "y"); `False` draws
            none. The grid draws over a picture placed below. See
            [`SHOW_GRID`][datachart.constants.SHOW_GRID].
        aspect_ratio: The aspect ratio of the axes box. See
            [`ASPECT_RATIO`][datachart.constants.ASPECT_RATIO].
        subplots: Whether to draw each picture in its own subplot.
        max_cols: The maximum number of subplot columns.
        sharex: Whether the subplots share the x-axis.
        sharey: Whether the subplots share the y-axis.
        style: Style configuration(s) for each chart. See
            [`ImageStyleAttrs`][datachart.typings.ImageStyleAttrs].

    Returns:
        The figure containing the image chart.

    Raises:
        ValueError: If the image is not a readable picture or array, the
            `extent` is missing, not four finite numbers, or has no width or
            height, or `position` is not an `DRAW_POSITION`.

    """
    validate_draw_position(position)

    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        style=style,
        is_2d_data=True,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "position": position,
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "figsize": figsize,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "vmin": vmin,
        "vmax": vmax,
        "show_grid": show_grid,
        "aspect_ratio": aspect_ratio,
        "subplots": subplots,
        "max_cols": max_cols,
        "sharex": sharex,
        "sharey": sharey,
    }

    return render_chart("imagechart", charts, settings)
