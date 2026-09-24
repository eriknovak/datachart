from datetime import datetime
from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render
from ..utils._internal.validate import validate_annotation
from ..typings import (
    EmphasisRuleAttrs,
    LegendSettingAttrs,
    ScatterDataPointAttrs,
    ScatterStyleAttrs,
    VLineSettingAttrs,
    HLineSettingAttrs,
    DLineSettingAttrs,
    BracketSettingAttrs,
    VSpanSettingAttrs,
    HSpanSettingAttrs,
    TextSettingAttrs,
)
from ..constants import (
    ASPECT_RATIO,
    EMPHASIS,
    FIG_SIZE,
    SHOW_GRID,
    AXIS_SCALE,
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
    emphasis_rule: Optional[EmphasisRuleAttrs] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float, datetime]] = None,
    xmax: Optional[Union[int, float, datetime]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    show_xerr: Optional[bool] = None,
    show_yerr: Optional[bool] = None,
    show_regression: Optional[bool] = None,
    show_ci: Optional[bool] = None,
    ci_level: Optional[float] = None,
    show_correlation: Optional[bool] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    value_step: Optional[int] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    scalex: Optional[Union[AXIS_SCALE, str]] = None,
    scaley: Optional[Union[AXIS_SCALE, str]] = None,
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
    dlines: Optional[
        Union[
            DLineSettingAttrs,
            List[DLineSettingAttrs],
            List[Union[DLineSettingAttrs, List[DLineSettingAttrs], None]],
        ]
    ] = None,
    brackets: Optional[
        Union[
            BracketSettingAttrs,
            List[BracketSettingAttrs],
            List[Union[BracketSettingAttrs, List[BracketSettingAttrs], None]],
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
    texts: Optional[
        Union[
            TextSettingAttrs,
            List[TextSettingAttrs],
            List[Union[TextSettingAttrs, List[TextSettingAttrs], None]],
        ]
    ] = None,
    x: Optional[Union[str, List[Optional[str]]]] = None,
    y: Optional[Union[str, List[Optional[str]]]] = None,
    size: Optional[Union[str, List[Optional[str]]]] = None,
    hue: Optional[Union[str, List[Optional[str]]]] = None,
    annotation: Optional[Union[str, List[Optional[str]]]] = None,
    xerr: Optional[Union[str, List[Optional[str]]]] = None,
    yerr: Optional[Union[str, List[Optional[str]]]] = None,
    size_range: Optional[Tuple[float, float]] = None,
    label: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates a scatter chart.

    Each point is one observation placed by two numeric variables, optionally
    with a third encoded as marker size. Use it to check whether two variables
    are related, spot clusters and outliers, and quantify the link with the
    optional regression line and correlation coefficient. For ordered series
    use [`LineChart`][datachart.charts.LineChart].

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
        >>> # Scatter with an annotation beside each point
        >>> figure = ScatterChart(
        ...     data=[
        ...         {"x": 1, "y": 5, "name": "A"},
        ...         {"x": 2, "y": 10, "name": "B"}
        ...     ],
        ...     annotation="name"
        ... )

    Args:
        data: The data points for the scatter chart(s). Can be a single list of data points
            for one chart, or a list of lists for multiple charts/subplots. A point
            may carry its own `emphasis` role, which wins over its chart's.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts. Used as legend labels.
        emphasis: The emphasis role(s) for individual charts, aligned like
            `style`: "background" mutes a chart (theme muted color, lowered
            alpha, behind the others, no legend entry), "highlight" gives
            it a contrasting edge and brings it to the front, None leaves
            it unchanged.
        emphasis_rule: A rule that highlights the series matching it and mutes the rest:
            `{"above": v}` or `{"below": v}` (strict), `{"between": (lo, hi)}`
            (inclusive), `{"top": n}` or `{"bottom": n}`, read against a summary of each
            series's own `y` values, chosen by `by`: `"mean"` (default), `"median"`,
            `"min"`, `"max"`, or `"sum"`. An explicit `emphasis` role wins, and a count
            ranks across every series. See
            [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        show_grid: Which grid lines to show (e.g., "both", "x", "y");
            `False` draws none.
        show_xerr: Whether to draw the x-axis error bars; `True` by default,
            so a point carrying the key gets its bar.
        show_yerr: Whether to draw the y-axis error bars, as `show_xerr`.
        show_regression: Whether to show the regression line.
        show_ci: Whether to show the confidence interval around the regression line.
        ci_level: The confidence interval level (default 0.95).
        show_correlation: Whether to show the Pearson correlation coefficient (r-value) as an annotation.
        show_values: Whether to print each point's y value beside it. Cannot be
            combined with `annotation`: a point carries its annotation or its
            value.
        value_format: Format string for the value labels: a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] constant or any
            `"{x:.1f}"`, `"{:.1f}%"`, or `"%g"` style string.
        value_step: Label every Nth point (`1` labels all of them). Defaults
            to the smallest step that keeps neighbouring labels apart.
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            [`ASPECT_RATIO`][datachart.constants.ASPECT_RATIO].
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
        xticks_format: The x-axis tick label format: a
            [`DATE_FORMAT`][datachart.constants.DATE_FORMAT] member or `strftime`
            pattern on a datetime axis, else a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] member or `"{x:.1f}"`
            style string.
        yticks_format: The y-axis tick label format, as `xticks_format`.
        vlines: Vertical line(s) to plot.
        hlines: Horizontal line(s) to plot.
        dlines: Diagonal line(s) to plot, by slope and intercept.
        brackets: Pairwise comparison bracket(s) to draw between two
            categories, with an optional text such as a p-value.
        vspans: Vertical reference band(s) to shade, between two x positions.
        hspans: Horizontal reference band(s) to shade, between two y positions.
        texts: Text annotation(s) to draw.
        x: The key name in data for x-axis values (default: "x").
        y: The key name in data for y-axis values (default: "y").
        size: The key name in data for marker size values (for bubble charts).
        hue: The key name in data for color grouping (categorical variable).
        annotation: The key name in data for the point annotations (default:
            "annotation"), aligned like `style` for multiple charts; `None` in
            the list leaves that chart unannotated. Each annotation is drawn
            beside its marker at the spot with the least overlap against the
            other markers, annotations, and the axes edge; points without the
            key stay unannotated.
        xerr: The key name in data for the x-axis error values (default: "xerr").
            The value is a distance from the point: one number reaches the same
            distance both ways, a `(low, high)` pair reaches `low` left and
            `high` right. A point without the key draws no bar. Each bar runs
            from the edge of its marker outward, in the point's own color,
            which `plot_scatter_error_color` overrides.
        yerr: The key name in data for the y-axis error values (default: "yerr"),
            read like `xerr`.
        size_range: Tuple of (min_size, max_size) for bubble charts (default: (20, 200)).
        label: Deprecated; use `annotation`. Removed in the next release.

    Returns:
        The figure containing the scatter chart.

    """
    params = dict(locals())

    validate_annotation(annotation if label is None else label, show_values)
    return render("scatterchart", params)
