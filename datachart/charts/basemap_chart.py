from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import validate_draw_position
from ..typings import BasemapDataAttrs, BasemapStyleAttrs
from ..constants import (
    ASPECT_RATIO,
    BASEMAP_FEATURE,
    BASEMAP_RESOLUTION,
    DRAW_POSITION,
    FIG_SIZE,
    SHOW_GRID,
)

# ================================================
# Main Chart Definition
# ================================================


def BasemapChart(
    features: Optional[Union[BASEMAP_FEATURE, str, List[str]]] = None,
    *,
    resolution: Optional[Union[BASEMAP_RESOLUTION, str]] = None,
    geometry: Optional[Union[BasemapDataAttrs, List[BasemapDataAttrs]]] = None,
    position: Optional[Union[DRAW_POSITION, str]] = None,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    style: Optional[BasemapStyleAttrs] = None,
) -> plt.Figure:
    """Creates the basemap chart.

    A basemap chart draws the land under a geographic chart: coastlines, a
    land fill, the borders between countries and the large lakes, from the
    Natural Earth 1:110m outlines that ship with the package, so it needs no
    download and no extra dependency. Longitude runs along x and latitude
    along y, drawn straight; nothing is projected, so the marks composed
    over the map with `Panel` need no transform either — a hexbin of
    epicentres, a scatter of stations, a line of a ship's track.

    The map carries no series: it takes no cycle color, no legend entry and
    no emphasis, and its greys come from the theme. `position` decides where
    it sits in the draw order, under the gridlines and every mark by
    default. Composed with other charts it leaves the axis limits to their
    data; alone it frames its own outlines. `aspect_ratio="geographic"`
    narrows each degree of longitude by the cosine of the middle latitude,
    so a region keeps its proportions.

    The bundled outlines suit a continent or a region. `resolution` asks for
    the finer Natural Earth scales, which are downloaded the first time they
    are used and kept in a local cache. `geometry` takes your own longitude
    and latitude outlines in their place: a country's provinces, a coast at
    street scale, or a map that is not of the Earth.

    Examples:
        >>> from datachart.charts import BasemapChart, ScatterChart
        >>> from datachart.constants import ASPECT_RATIO, BASEMAP_FEATURE
        >>> from datachart.utils import Panel
        >>> figure = Panel(
        ...     [
        ...         BasemapChart([BASEMAP_FEATURE.LAND, BASEMAP_FEATURE.BORDERS]),
        ...         ScatterChart([{"x": 14.5, "y": 46.1}, {"x": 16.4, "y": 48.2}]),
        ...     ],
        ...     title="Two capitals",
        ...     xmin=5,
        ...     xmax=25,
        ...     ymin=40,
        ...     ymax=52,
        ...     aspect_ratio=ASPECT_RATIO.GEOGRAPHIC,
        ... )

    Args:
        features: The bundled features to draw: one name or a list of them,
            coastline and land by default. See
            [`BASEMAP_FEATURE`][datachart.constants.BASEMAP_FEATURE].
        resolution: The Natural Earth scale: `"110m"` (default) ships with the
            package, `"50m"` and `"10m"` are downloaded once on first use. See
            [`BASEMAP_RESOLUTION`][datachart.constants.BASEMAP_RESOLUTION].
        geometry: Your own outlines, drawn in place of the bundled ones: a
            `{"lon", "lat", "feature"}` dict, or a list of them. Cannot be
            combined with `features` or `resolution`. See
            [`BasemapDataAttrs`][datachart.typings.BasemapDataAttrs].
        position: Where the map sits in the draw order: `"below"` (default)
            under the gridlines and every mark, or `"above"` over the marks and
            under the reference lines. See
            [`DRAW_POSITION`][datachart.constants.DRAW_POSITION].
        title: The title of the chart.
        xlabel: The label of the x-axis.
        ylabel: The label of the y-axis.
        figsize: The size of the figure as (width, height) in inches. See
            [`FIG_SIZE`][datachart.constants.FIG_SIZE].
        xmin: The minimum value of the x-axis.
        xmax: The maximum value of the x-axis.
        ymin: The minimum value of the y-axis.
        ymax: The maximum value of the y-axis.
        show_grid: Which grid lines to show ("both", "x", "y"); `False` draws
            none. The grid draws over a map placed below. See
            [`SHOW_GRID`][datachart.constants.SHOW_GRID].
        aspect_ratio: The aspect ratio of the axes box; `"geographic"` keeps
            the region at true proportions. See
            [`ASPECT_RATIO`][datachart.constants.ASPECT_RATIO].
        style: Style configuration of the map. See
            [`BasemapStyleAttrs`][datachart.typings.BasemapStyleAttrs].

    Returns:
        The figure containing the basemap chart.

    Raises:
        ValueError: If a feature is not a `BASEMAP_FEATURE`, `resolution` is not
            a `BASEMAP_RESOLUTION`, `geometry` is not outlines of matching
            longitudes and latitudes or comes with `features` or `resolution`,
            `position` is not a `DRAW_POSITION`, or a geographic aspect meets a
            y-axis outside -90 to 90.
        RuntimeError: If a finer resolution is not cached and cannot be
            downloaded.

    """
    validate_draw_position(position)

    charts = build_charts_structure(
        {"features": features, "resolution": resolution, "geometry": geometry},
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
        "show_grid": show_grid,
        "aspect_ratio": aspect_ratio,
    }

    return render_chart("basemapchart", charts, settings)
