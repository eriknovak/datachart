from datetime import datetime
from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..typings import (
    EmphasisRuleAttrs,
    HexbinDataAttrs,
    HexbinStyleAttrs,
    ColorbarSettingAttrs,
    LegendSettingAttrs,
    VLineSettingAttrs,
    HLineSettingAttrs,
    VSpanSettingAttrs,
    HSpanSettingAttrs,
    TextSettingAttrs,
)
from ..constants import (
    DATE_FORMAT,
    ASPECT_RATIO,
    FIG_SIZE,
    HEXBIN_REDUCE,
    SHOW_GRID,
    SCALE,
    VALUE_FORMAT,
)

# ================================================
# Main Chart Definition
# ================================================


def HexbinChart(
    data: Union[HexbinDataAttrs, List[HexbinDataAttrs]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: None = None,
    emphasis_rule: Optional[EmphasisRuleAttrs] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float, datetime]] = None,
    xmax: Optional[Union[int, float, datetime]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    show_colorbars: bool = True,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[SCALE, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[Union[HexbinStyleAttrs, List[Optional[HexbinStyleAttrs]]]] = None,
    gridsize: Optional[Union[int, List[Optional[int]]]] = None,
    reduce: Optional[Union[HEXBIN_REDUCE, str, List[Optional[str]]]] = None,
    mincnt: Optional[Union[int, List[Optional[int]]]] = None,
    norm: Optional[Union[str, List[Optional[str]]]] = None,
    vmin: Optional[Union[float, List[Optional[float]]]] = None,
    vmax: Optional[Union[float, List[Optional[float]]]] = None,
    valfmt: Optional[Union[VALUE_FORMAT, str, List[Optional[str]]]] = None,
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
            VLineSettingAttrs,
            List[VLineSettingAttrs],
            List[Union[VLineSettingAttrs, List[VLineSettingAttrs], None]],
        ]
    ] = None,
    hlines: Optional[
        Union[
            HLineSettingAttrs,
            List[HLineSettingAttrs],
            List[Union[HLineSettingAttrs, List[HLineSettingAttrs], None]],
        ]
    ] = None,
    vspans: Optional[
        Union[
            VSpanSettingAttrs,
            List[VSpanSettingAttrs],
            List[Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]],
        ]
    ] = None,
    hspans: Optional[
        Union[
            HSpanSettingAttrs,
            List[HSpanSettingAttrs],
            List[Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]],
        ]
    ] = None,
    colorbar: Optional[
        Union[ColorbarSettingAttrs, List[Optional[ColorbarSettingAttrs]]]
    ] = None,
    texts: Optional[
        Union[
            TextSettingAttrs,
            List[TextSettingAttrs],
            List[Union[TextSettingAttrs, List[TextSettingAttrs], None]],
        ]
    ] = None,
) -> plt.Figure:
    """Creates the hexbin chart.

    A hexbin chart tiles the plane with hexagons and colors each by the number
    of points falling in it — or, with a per-point `c`, by an aggregate of
    those values. Use it where a scatter chart turns into an opaque blob:
    thousands of points, overlapping clusters, or a value that varies across
    the plane. For the points themselves use
    [`ScatterChart`][datachart.charts.ScatterChart]; for a smooth density
    estimate use [`ContourChart`][datachart.charts.ContourChart] on
    [`stats.kde2d`][datachart.utils.stats.kde2d].

    !!! info "Added in v0.9.0"

    !!! info "Added in Unreleased"

        The `xticks_format` and `yticks_format` tick formats.
        The `label`, `location`, `format`, and `ticks` fields of the
        `colorbar` setting.
        The `vspans` and `hspans` reference bands.
        The `emphasis_rule` parameter.
        The `show_legend` and `legend` parameters.

    Examples:
        >>> from datachart.charts import HexbinChart
        >>> figure = HexbinChart(
        ...     data={
        ...         "x": [0.1, 0.4, 0.5, 1.2, 1.3, 2.0],
        ...         "y": [0.2, 0.3, 0.6, 1.1, 1.4, 2.1],
        ...     },
        ...     title="Basic Hexbin Chart",
        ...     xlabel="X",
        ...     ylabel="Y"
        ... )

    Args:
        data: The points to bin: a dictionary with the `x` and `y` columns and
            an optional `c` column of per-point values, or a list of them for
            multiple charts/subplots.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts.
        emphasis: Not supported: a hexbin chart is a single colormapped layer
            with no series to mute or highlight. Passing a value raises
            `ValueError`.
        emphasis_rule: A rule that highlights the bins matching it and mutes the
            rest: `{"above": v}` or `{"below": v}` (strict),
            `{"between": (lo, hi)}` (inclusive), `{"top": n}` or
            `{"bottom": n}`, read against each bin's aggregated value (its
            count, or `c` reduced by `reduce`). Bins exist only once drawn, so a
            count ranks the bins of each chart on its own, and an empty bin
            never matches. The rule takes no `by`. See
            [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend; it lists the labelled reference
            lines and bands.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        show_grid: Which grid lines to show (e.g., "both", "x", "y"); `False`
            draws none. Off by default: the hexagons cover it.
        show_colorbars: Whether to show the colorbar(s).
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            [`ASPECT_RATIO`][datachart.constants.ASPECT_RATIO].
        scalex: The x-axis scale (e.g., "log", "linear").
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s) for the hexbin chart(s).
        gridsize: The number of hexagons across the x-axis; the
            `plot_hexbin_gridsize` config value by default.
        reduce: How the `c` values in a hexagon collapse into its color, one of
            [`HEXBIN_REDUCE`][datachart.constants.HEXBIN_REDUCE] (the mean by default).
            Ignored without `c`, where every hexagon shows its point count.
        mincnt: The point count below which a hexagon stays blank; every
            hexagon is drawn by default.
        norm: Value normalization method(s) of the colormap; `"log"` spreads
            heavy-tailed counts.
        vmin: Minimum value(s) for normalization.
        vmax: Maximum value(s) for normalization.
        valfmt: Format string(s) for the colorbar tick labels, with the value named `x`
            (e.g., `"{x:.0f}"`). See [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT].
            The `format` field of the `colorbar` setting wins when set.
        xticks: Custom x-axis tick positions.
        xticklabels: Custom x-axis tick labels.
        xtickrotate: Rotation angle for x-axis tick labels.
        yticks: Custom y-axis tick positions.
        yticklabels: Custom y-axis tick labels.
        ytickrotate: Rotation angle for y-axis tick labels.
        xticks_format: The x-axis tick label format: a
            [`DATE_FORMAT`][datachart.constants.DATE_FORMAT] member or `strftime`
            pattern on a datetime axis, else a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] member or `"{x:.1f}"`
            style string.
        yticks_format: The y-axis tick label format, as `xticks_format`.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        vspans: Vertical reference band(s) to shade, between two x positions.
        hspans: Horizontal reference band(s) to shade, between two y positions.
        colorbar: The colorbar setting(s): label, location, tick format, and tick
            positions. See
            [`ColorbarSettingAttrs`][datachart.typings.ColorbarSettingAttrs].
        texts: Text annotation(s) to draw.

    Returns:
        The figure containing the hexbin chart.

    """
    if emphasis is not None:
        raise ValueError(
            "HexbinChart does not support `emphasis`: a hexbin chart is a single "
            "colormapped layer with no series to mute or highlight."
        )

    # Build the charts structure using shared utility
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
        vlines=vlines,
        hlines=hlines,
        vspans=vspans,
        hspans=hspans,
        texts=texts,
        is_2d_data=True,
        gridsize=gridsize,
        reduce=reduce,
        mincnt=mincnt,
        norm=norm,
        vmin=vmin,
        vmax=vmax,
        valfmt=valfmt,
        colorbar=colorbar,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "emphasis_rule": emphasis_rule,
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
        "show_colorbars": show_colorbars,
        "scalex": scalex,
        "scaley": scaley,
        "xticks_format": xticks_format,
        "yticks_format": yticks_format,
    }

    return render_chart("hexbinchart", charts, settings)
