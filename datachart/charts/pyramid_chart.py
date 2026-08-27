from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure, _get_indexed_value
from ..typings import (
    BarDataPointAttrs,
    BarStyleAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
    TextAttrs,
)
from ..constants import (
    FIG_SIZE,
    ORIENTATION,
    SHOW_GRID,
    VALUE_FORMAT,
)

# ================================================
# Main Chart Definition
# ================================================


def PyramidChart(
    data: List[List[BarDataPointAttrs]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_yerr: Optional[bool] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    style: Optional[Union[BarStyleAttrs, List[Optional[BarStyleAttrs]]]] = None,
    xticks: Optional[List[Union[int, float]]] = None,
    xticklabels: Optional[List[str]] = None,
    xtickrotate: Optional[int] = None,
    yticks: Optional[List[Union[int, float]]] = None,
    yticklabels: Optional[List[str]] = None,
    ytickrotate: Optional[int] = None,
    vlines: Optional[Union[VLinePlotAttrs, List[VLinePlotAttrs]]] = None,
    hlines: Optional[Union[HLinePlotAttrs, List[HLinePlotAttrs]]] = None,
    texts: Optional[Union[TextAttrs, List[TextAttrs]]] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    yerr: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates the pyramid chart.

    A pyramid chart draws exactly two series as horizontal bars mirrored
    around a shared category axis, the first series to the left and the second
    to the right: the classic age-sex population pyramid. Use it to compare
    the distribution of two groups over the same ordered categories, such as
    age bands, where the symmetry (or lack of it) is the message.

    Both series are supplied as positive values; value ticks and labels show
    absolute values. Unlike the other chart fronts, the axis parameters are
    spatial: `xlabel`, `xticks`, and `xmax` address the horizontal value axis,
    and `ylabel` the vertical category axis.

    !!! info "Added in v0.8.0"

    Examples:
        >>> from datachart.charts import PyramidChart
        >>> figure = PyramidChart(
        ...     data=[
        ...         [
        ...             {"label": "0-14", "y": 12},
        ...             {"label": "15-29", "y": 18},
        ...             {"label": "30-44", "y": 22},
        ...         ],
        ...         [
        ...             {"label": "0-14", "y": 11},
        ...             {"label": "15-29", "y": 19},
        ...             {"label": "30-44", "y": 24},
        ...         ],
        ...     ],
        ...     subtitle=["Group A", "Group B"],
        ...     title="Basic Pyramid Chart",
        ...     show_legend=True,
        ... )

    Args:
        data: Exactly two lists of data points — the first is the left side,
            the second the right. Values are positive for both sides; the
            chart mirrors the left side itself.
        title: The title of the chart.
        xlabel: The label of the horizontal value axis.
        ylabel: The label of the vertical category axis.
        subtitle: The names of the two sides. Used as legend labels.
        figsize: The size of the figure as (width, height) in inches. See `FIG_SIZE`.
        xmin: Not supported; the value axis is always symmetric around zero.
            Raises when passed.
        xmax: The maximum per-side value; the value axis spans (-xmax, xmax).
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show ("both", "x", "y"). See `SHOW_GRID`.
        show_yerr: Whether to show error bars on the bars.
        show_values: Whether to show bar value labels at the edge of each bar.
        value_format: Format string for bar value labels: a `VALUE_FORMAT`
            constant or any `"{x:.1f}"`, `"{:.1f}%"`, or `"%g"` style string.
        style: Style configuration(s) for the bars, per side.
        xticks: Custom value-axis tick positions, as positive values; each is
            mirrored to both halves.
        xticklabels: Custom value-axis tick labels (same length as `xticks`),
            applied to both mirrored halves.
        xtickrotate: Rotation angle for value-axis tick labels.
        yticks: Custom category-axis tick positions.
        yticklabels: Custom category-axis tick labels.
        ytickrotate: Rotation angle for category-axis tick labels.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        texts: Text annotation(s) to draw.
        label: The key name in data for label values (default: "label").
        y: The key name in data for the bar values (default: "y").
        yerr: The key name in data for the bar error values (default: "yerr").

    Returns:
        The figure containing the pyramid chart.

    """
    if xmin is not None:
        raise ValueError(
            "PyramidChart does not support `xmin`: "
            "the value axis is always symmetric around zero."
        )
    if not (
        isinstance(data, list)
        and len(data) == 2
        and all(isinstance(side, list) for side in data)
    ):
        raise ValueError(
            "PyramidChart takes exactly two data series: "
            "`data=[left_points, right_points]`."
        )
    if xticks is not None and any(tick < 0 for tick in xticks):
        raise ValueError(
            "PyramidChart `xticks` are positive positions; "
            "each is mirrored to both halves."
        )

    # the left side draws in the negative direction; users pass positive values
    left_y_key = _get_indexed_value(y, 0) or "y"
    left_side = [
        {**point, left_y_key: -point[left_y_key]} if left_y_key in point else point
        for point in data[0]
    ]

    charts = build_charts_structure(
        [left_side, data[1]],
        subtitle=subtitle,
        style=style,
        yticks=yticks,
        yticklabels=yticklabels,
        ytickrotate=ytickrotate,
        vlines=vlines,
        hlines=hlines,
        texts=texts,
        label=label,
        y=y,
        yerr=yerr,
    )

    # Figure-level settings; None values resolve to defaults downstream.
    # The pyramid marker routes the engine to the mirrored bar panel; xticks
    # stay out of the charts structure so the panel can mirror them.
    settings = {
        "pyramid": True,
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "figsize": figsize,
        "xmax": xmax,
        "show_legend": show_legend,
        "show_grid": show_grid,
        "show_yerr": show_yerr,
        "show_values": show_values,
        "value_format": value_format,
        "orientation": ORIENTATION.HORIZONTAL,
        "xticks": xticks,
        "xticklabels": xticklabels,
        "xtickrotate": xtickrotate,
    }

    return render_chart("pyramidchart", charts, settings)
