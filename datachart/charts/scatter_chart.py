from datetime import datetime
from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import validate_point_labels
from ..typings import (
    LegendSettingAttrs,
    ScatterDataPointAttrs,
    ScatterStyleAttrs,
    VLinePlotAttrs,
    HLinePlotAttrs,
    VSpanPlotAttrs,
    HSpanPlotAttrs,
    TextAttrs,
)
from ..constants import (
    ASPECT_RATIO,
    EMPHASIS,
    FIG_SIZE,
    SHOW_GRID,
    SCALE,
    VALUE_FORMAT,
    DATE_FORMAT,
)

# ================================================
# Main Chart Definition
# ================================================


def ScatterChart(
    data: Union[List[ScatterDataPointAttrs], List[List[ScatterDataPointAttrs]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: Optional[Union[EMPHASIS, str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float, datetime]] = None,
    xmax: Optional[Union[int, float, datetime]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    show_regression: Optional[bool] = None,
    show_ci: Optional[bool] = None,
    ci_level: Optional[float] = None,
    show_correlation: Optional[bool] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    value_step: Optional[int] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[ScatterStyleAttrs, List[Optional[ScatterStyleAttrs]]]] = None,
    xticks: Optional[
        Union[
            List[Union[int, float, datetime]],
            List[List[Union[int, float, datetime]]],
        ]
    ] = None,
    xticklabels: Optional[Union[List[str], List[List[str]]]] = None,
    xtickrotate: Optional[Union[int, List[Optional[int]]]] = None,
    yticks: Optional[
        Union[List[Union[int, float]], List[List[Union[int, float]]]]
    ] = None,
    yticklabels: Optional[Union[List[str], List[List[str]]]] = None,
    ytickrotate: Optional[Union[int, List[Optional[int]]]] = None,
    xticks_format: Optional[Union[VALUE_FORMAT, DATE_FORMAT, str]] = None,
    yticks_format: Optional[Union[VALUE_FORMAT, DATE_FORMAT, str]] = None,
    vlines: Optional[
        Union[
            VLinePlotAttrs,
            List[VLinePlotAttrs],
            List[Union[VLinePlotAttrs, List[VLinePlotAttrs], None]],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLinePlotAttrs,
            List[HLinePlotAttrs],
            List[Union[HLinePlotAttrs, List[HLinePlotAttrs], None]],
        ]
    ] = None,
    vspans: Optional[
        Union[
            VSpanPlotAttrs,
            List[VSpanPlotAttrs],
            List[Union[VSpanPlotAttrs, List[VSpanPlotAttrs], None]],
        ]
    ] = None,
    hspans: Optional[
        Union[
            HSpanPlotAttrs,
            List[HSpanPlotAttrs],
            List[Union[HSpanPlotAttrs, List[HSpanPlotAttrs], None]],
        ]
    ] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
    x: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    size: Optional[Union[str, List[Optional[str]]]] = None,
    hue: Optional[Union[str, List[Optional[str]]]] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
    size_range: Optional[Tuple[float, float]] = None,
) -> plt.Figure:
    """Creates a scatter chart.

    Each point is one observation placed by two numeric variables, optionally
    with a third encoded as marker size. Use it to check whether two variables
    are related, spot clusters and outliers, and quantify the link with the
    optional regression line and correlation coefficient. For ordered series
    use [`LineChart`][datachart.charts.LineChart].

    !!! info "Added in v0.7.0"

    Examples:
        >>> from datachart.charts import ScatterChart
        >>> # Basic scatter plot
        >>> figure = ScatterChart(
        ...     data=[
        ...         {"x": 1, "y": 5},
        ...         {"x": 2, "y": 10},
        ...         {"x": 3, "y": 15},
        ...         {"x": 4, "y": 20},
        ...         {"x": 5, "y": 25}
        ...     ],
        ...     title="Basic Scatter Chart",
        ...     xlabel="X",
        ...     ylabel="Y"
        ... )
        >>>
        >>> # Scatter with hue grouping
        >>> figure = ScatterChart(
        ...     data=[
        ...         {"x": 1, "y": 5, "category": "A"},
        ...         {"x": 2, "y": 10, "category": "B"},
        ...     ],
        ...     hue="category",
        ...     show_legend=True
        ... )
        >>>
        >>> # Bubble chart with size variable
        >>> figure = ScatterChart(
        ...     data=[
        ...         {"x": 1, "y": 5, "pop": 100},
        ...         {"x": 2, "y": 10, "pop": 200}
        ...     ],
        ...     size="pop",
        ...     size_range=(20, 200)
        ... )
        >>>
        >>> # Scatter with regression line
        >>> figure = ScatterChart(
        ...     data=[...],
        ...     show_regression=True,
        ...     show_ci=True,
        ...     ci_level=0.95
        ... )
        >>>
        >>> # Scatter with correlation annotation
        >>> figure = ScatterChart(
        ...     data=[...],
        ...     show_correlation=True
        ... )
        >>>
        >>> # Scatter with a label beside each point
        >>> figure = ScatterChart(
        ...     data=[
        ...         {"x": 1, "y": 5, "name": "A"},
        ...         {"x": 2, "y": 10, "name": "B"}
        ...     ],
        ...     label="name"
        ... )

    !!! info "Added in Unreleased"

        The `xticks_format` and `yticks_format` tick formats.
        The `show_values`, `value_format`, `value_step` and `legend` parameters.
        The `vspans` and `hspans` reference bands.

    Args:
        data: The data points for the scatter chart(s). Can be a single list of data points
            for one chart, or a list of lists for multiple charts/subplots.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts. Used as legend labels.
        emphasis: The emphasis role(s) for individual charts, aligned like
            `style`: "background" mutes a chart (theme muted color, lowered
            alpha, behind the others, no legend entry), "highlight" gives
            it a contrasting edge and brings it to the front, None leaves
            it unchanged.
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            `LegendSettingAttrs`.
        show_grid: Which grid lines to show (e.g., "both", "x", "y").
        show_regression: Whether to show the regression line.
        show_ci: Whether to show the confidence interval around the regression line.
        ci_level: The confidence interval level (default 0.95).
        show_correlation: Whether to show the Pearson correlation coefficient (r-value) as an annotation.
        show_values: Whether to print each point's y value beside it. Cannot be
            combined with `label`: a point carries its label or its value.
        value_format: Format string for the value labels: a `VALUE_FORMAT`
            constant or any `"{x:.1f}"`, `"{:.1f}%"`, or `"%g"` style string.
        value_step: Label every Nth point (`1` labels all of them). Defaults
            to the smallest step that keeps neighbouring labels apart.
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            `ASPECT_RATIO`.
        scalex: The x-axis scale (e.g., "log", "linear").
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the scatter markers.
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        xticks_format: The x-axis tick label format: a `DATE_FORMAT` member
            or `strftime` pattern on a datetime axis, else a `VALUE_FORMAT`
            member or `"{x:.1f}"` style string.
        yticks_format: The y-axis tick label format, as `xticks_format`.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        vspans: Vertical reference band(s) to shade, between two x positions.
        hspans: Horizontal reference band(s) to shade, between two y positions.
        texts: Text annotation(s) to draw.
        x: The key name in data for x-axis values (default: "x").
        y: The key name in data for y-axis values (default: "y").
        size: The key name in data for marker size values (for bubble charts).
        hue: The key name in data for color grouping (categorical variable).
        label: The key name in data for the point labels (default: "label"),
            aligned like `style` for multiple charts; `None` in the list
            leaves that chart unlabelled. Each label is drawn beside its
            marker at the spot with the least overlap against the other
            markers, labels, and the axes edge; points without the key stay
            unlabelled.
        size_range: Tuple of (min_size, max_size) for bubble charts (default: (20, 200)).

    Returns:
        The figure containing the scatter chart.

    """
    # Build the charts structure using shared utility
    validate_point_labels(label, show_values)
    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        emphasis=emphasis,
        style=style,
        xticks=xticks,
        xticklabels=xticklabels,
        xtickrotate=xtickrotate,
        yticks=yticks,
        yticklabels=yticklabels,
        ytickrotate=ytickrotate,
        vlines=vlines,
        hlines=hlines,
        vspans=vspans,
        hspans=hspans,
        texts=texts,
        x=x,
        y=y,
        size=size,
        hue=hue,
        label=label,
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
        "legend": legend,
        "show_grid": show_grid,
        "aspect_ratio": aspect_ratio,
        "subplots": subplots,
        "max_cols": max_cols,
        "sharex": sharex,
        "sharey": sharey,
        "show_regression": show_regression,
        "show_ci": show_ci,
        "ci_level": ci_level,
        "show_correlation": show_correlation,
        "show_values": show_values,
        "value_format": value_format,
        "value_step": value_step,
        "scalex": scalex,
        "scaley": scaley,
        "size_range": size_range,
        "xticks_format": xticks_format,
        "yticks_format": yticks_format,
    }

    return render_chart("scatterchart", charts, settings)
