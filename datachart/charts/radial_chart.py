from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..typings import (
    RadialDataPointAttrs,
    LineStyleAttrs,
    BarStyleAttrs,
    HistStyleAttrs,
    ScatterStyleAttrs,
    TextAttrs,
)
from ..constants import (
    BAR_MODE,
    DIRECTION,
    EMPHASIS,
    FIG_SIZE,
    RADIAL_TYPE,
    SCALE,
    SHOW_GRID,
)

_RADIAL_TYPES = (
    RADIAL_TYPE.LINE,
    RADIAL_TYPE.BAR,
    RADIAL_TYPE.SCATTER,
    RADIAL_TYPE.HISTOGRAM,
)
_DIRECTIONS = (DIRECTION.CLOCKWISE, DIRECTION.COUNTERCLOCKWISE)
_COMPASS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")

_RadialStyleAttrs = Union[
    LineStyleAttrs, BarStyleAttrs, HistStyleAttrs, ScatterStyleAttrs
]

# ================================================
# Main Chart Definition
# ================================================


def RadialChart(
    data: Union[List[RadialDataPointAttrs], List[List[RadialDataPointAttrs]]],
    *,
    type: Optional[Union[RADIAL_TYPE, str]] = None,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: Optional[Union[EMPHASIS, str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_yerr: Optional[bool] = None,
    show_area: Optional[bool] = None,
    show_values: Optional[bool] = None,
    show_tip_labels: Optional[bool] = None,
    show_border: Optional[bool] = None,
    value_format: Optional[str] = None,
    bar_mode: Optional[Union[BAR_MODE, str]] = None,
    num_bins: Optional[int] = None,
    startangle: Optional[Union[str, int, float]] = None,
    direction: Optional[Union[DIRECTION, str]] = None,
    innerradius: Optional[float] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[_RadialStyleAttrs, List[Optional[_RadialStyleAttrs]]]] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    vlines: Optional[dict] = None,
    hlines: Optional[dict] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    x: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    yerr: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates the radial chart.

    Examples:
        >>> from datachart.charts import RadialChart
        >>> figure = RadialChart(
        ...     data=[
        ...         {"label": "N", "y": 5},
        ...         {"label": "E", "y": 10},
        ...         {"label": "S", "y": 15},
        ...         {"label": "W", "y": 20}
        ...     ],
        ...     title="Basic Radial Chart"
        ... )

    Args:
        data: The data points for the radial chart(s). Can be a single list of data
            points for one chart, or a list of lists for multiple charts/subplots.
            The line, bar, and scatter visuals take `label`/`y` points whose labels
            are placed evenly around the circle; the histogram visual takes numeric
            `x` observations in degrees, binned over [0, 360).
        type: The visual the whole figure draws: "line" (default), "bar",
            "scatter", or "histogram". See `RADIAL_TYPE`.
        title: The title of the chart.
        xlabel: The angular-axis label.
        ylabel: The radial-axis label.
        subtitle: The subtitle(s) for individual charts. Used as legend labels.
        emphasis: The emphasis role(s) for individual charts, aligned like
            `style`: "background" mutes a chart, "highlight" bolds it, None
            leaves it unchanged.
        figsize: The size of the figure.
        ymin: The minimum radial-axis value.
        ymax: The maximum radial-axis value.
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show (e.g., "both", "x", "y").
        show_yerr: Whether to show the radial error band (line visual).
        show_area: Whether to fill the area inside the line (line visual).
        show_values: Whether to write each mark's value at its tip, rotated
            along the spoke.
        show_tip_labels: Whether to write the category labels at the mark
            tips, rotated along their spokes, instead of around the circle.
        show_border: Whether to draw the outer border circle. Defaults to the
            theme's spine visibility; `False` hides it.
        value_format: Format for the values written by `show_values` — a
            printf format (e.g. `"%.1f"`) or a `{x}`-style string. See
            `VALUE_FORMAT`.
        bar_mode: How multiple bar series share the circle: "group",
            "stack", or "overlay" (bar visual). See `BAR_MODE`.
        num_bins: The number of angular bins over [0, 360) (histogram visual).
        startangle: Where the first point sits: a compass location ("N", "NE",
            "E", "SE", "S", "SW", "W", "NW") or a numeric compass bearing in
            degrees clockwise from north. Defaults to "N".
        direction: Which way the angles increase: "clockwise" (default) or
            "counterclockwise". See `DIRECTION`.
        innerradius: The donut hole, as a fraction (0 <= f < 1) of the radial
            extent. Defaults to 0.
        scalex: Not supported; the angular axis has no scale. Raises when passed.
        scaley: The radial-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate polar subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the angular axis in subplots.
        sharey: Whether to share the radial axis in subplots.
        style: Style configuration(s) for the chart(s); radial visuals obey the
            matching cartesian style family (`plot_line_*`, `plot_bar_*`,
            `plot_hist_*`, `plot_scatter_*`).
        texts: Text annotation(s) to draw. On the polar axes, data
            coordinates are (angle in radians, radius); axes-fraction
            coordinates (`"coords": "axes"`) are often easier.
        vlines: Not supported on a polar axes. Raises when passed.
        hlines: Not supported on a polar axes. Raises when passed.
        label: The key name in data for the category labels (default: "label").
        x: The key name in data for the histogram observations (default: "x").
        y: The key name in data for radial values (default: "y").
        yerr: The key name in data for radial error values (default: "yerr").

    Returns:
        The figure containing the radial chart.

    """
    if scalex is not None:
        raise ValueError(
            "RadialChart does not support `scalex`: "
            "the angular axis has no scale to change."
        )
    if vlines is not None or hlines is not None:
        raise ValueError(
            "RadialChart does not support `vlines` and `hlines`: straight "
            "reference lines are geometrically meaningless on a polar axes."
        )
    radial_type = RADIAL_TYPE.LINE if type is None else type
    if radial_type not in _RADIAL_TYPES:
        raise ValueError(
            f"Invalid `type` value {radial_type!r}. Must be one of {_RADIAL_TYPES}."
        )
    if direction is not None and direction not in _DIRECTIONS:
        raise ValueError(
            f"Invalid `direction` value {direction!r}. Must be one of {_DIRECTIONS}."
        )
    if innerradius is not None and not 0 <= innerradius < 1:
        raise ValueError(
            f"Invalid `innerradius` value {innerradius!r}. "
            "Must be a fraction 0 <= f < 1 of the radial extent."
        )
    if isinstance(startangle, str) and startangle not in _COMPASS:
        raise ValueError(
            f"Invalid `startangle` value {startangle!r}. Must be a compass "
            f"location {_COMPASS} or a numeric bearing in degrees."
        )

    # Build the charts structure using shared utility
    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        emphasis=emphasis,
        style=style,
        texts=texts,
        label=label,
        x=x,
        y=y,
        yerr=yerr,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "radial_type": radial_type,
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "figsize": figsize,
        "ymin": ymin,
        "ymax": ymax,
        "show_legend": show_legend,
        "show_grid": show_grid,
        "show_yerr": show_yerr,
        "show_area": show_area,
        "show_values": show_values,
        "show_tip_labels": show_tip_labels,
        "show_border": show_border,
        "value_format": value_format,
        "bar_mode": bar_mode,
        "num_bins": num_bins,
        "startangle": startangle,
        "direction": direction,
        "innerradius": innerradius,
        "scaley": scaley,
        "subplots": subplots,
        "max_cols": max_cols,
        "sharex": sharex,
        "sharey": sharey,
    }

    return render_chart("radialchart", charts, settings)
