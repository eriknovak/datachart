from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render
from ..utils._internal.validate import validate_bandwidth
from ..typings import (
    EmphasisRuleAttrs,
    LegendSettingAttrs,
    RaincloudDataPointAttrs,
    RaincloudStyleAttrs,
    VLineSettingAttrs,
    HLineSettingAttrs,
    DLineSettingAttrs,
    BracketSettingAttrs,
    VSpanSettingAttrs,
    HSpanSettingAttrs,
    TextSettingAttrs,
)
from ..constants import (
    VALUE_FORMAT,
    DATE_FORMAT,
    ASPECT_RATIO,
    BANDWIDTH,
    EMPHASIS,
    FIG_SIZE,
    SHOW_GRID,
    ORIENTATION,
    SCALE,
    SWARM_MODE,
)

# ================================================
# Main Chart Definition
# ================================================


def RaincloudPlot(
    data: Union[List[RaincloudDataPointAttrs], List[List[RaincloudDataPointAttrs]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: Optional[Union[EMPHASIS, str, List[Optional[str]]]] = None,
    emphasis_rule: Optional[EmphasisRuleAttrs] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    xmin: Optional[Union[int, float]] = None,
    xmax: Optional[Union[int, float]] = None,
    ymin: Optional[Union[int, float]] = None,
    ymax: Optional[Union[int, float]] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str, bool]] = None,
    show_outliers: Optional[bool] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    mode: Optional[Union[SWARM_MODE, str]] = None,
    jitter: float = 0.4,
    bandwidth: Optional[Union[BANDWIDTH, str, float]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    orientation: Optional[Union[ORIENTATION, str]] = None,
    scaley: Optional[Union[SCALE, str]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    style: Optional[
        Union[RaincloudStyleAttrs, List[Optional[RaincloudStyleAttrs]]]
    ] = None,
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
    label: Optional[Union[str, List[Optional[str]]]] = None,
    value: Optional[Union[str, List[Optional[str]]]] = None,
) -> plt.Figure:
    """Creates the raincloud plot.

    A raincloud plot draws each group as a cloud (a half violin of its
    density), its rain (the raw observations), and a box (the quartile
    summary) side by side at one category position, all in the group's palette
    color. Use it when you want the shape, the summary statistics, and the
    individual observations in a single view, for example when reporting
    experimental results per condition. Vertical rainclouds keep the cloud on
    the right; horizontal ones keep it above.

    Examples:
        >>> from datachart.charts import RaincloudPlot
        >>> figure = RaincloudPlot(
        ...     data=[
        ...         {"label": "Group A", "value": 10},
        ...         {"label": "Group A", "value": 15},
        ...         {"label": "Group A", "value": 12},
        ...         {"label": "Group B", "value": 20},
        ...         {"label": "Group B", "value": 25},
        ...         {"label": "Group B", "value": 22},
        ...     ],
        ...     title="Basic Raincloud Plot",
        ...     xlabel="Group",
        ...     ylabel="Value"
        ... )

    Args:
        data: The data points for the raincloud plot(s). Can be a single list of
            data points for one chart, or a list of lists for multiple charts
            (drawn as subplots). Each data point should have a `label`
            (category) and `value` (numeric).
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts.
        emphasis: The emphasis role(s), aligned with the group labels of one
            call (a single value applies to every group): "background" mutes
            a group's cloud, rain, and box, "highlight" bolds their edges,
            None leaves them unchanged.
        emphasis_rule: A rule that highlights the groups matching it and mutes the rest:
            `{"above": v}` or `{"below": v}` (strict), `{"between": (lo, hi)}`
            (inclusive), `{"top": n}` or `{"bottom": n}`, read against a summary of each
            group's values, chosen by `by`: `"median"` (default), `"mean"`, `"min"`,
            `"max"`, or `"sum"`. An explicit `emphasis` role wins, and a count ranks
            across every group of every chart. See
            [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        figsize: The size of the figure.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend; one entry per group.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        show_grid: Which grid lines to show (e.g., "both", "x", "y");
            `False` draws none.
        show_outliers: Whether the box shows outliers.
        show_values: Whether to print each group's median beside its box, and
            its minimum and maximum beside the rain points holding them.
        value_format: Format string for the value labels: a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] constant or any
            `"{x:.1f}"`, `"{:.1f}%"`, or `"%g"` style string.
        mode: How the rain spreads across its width. See
            [`SWARM_MODE`][datachart.constants.SWARM_MODE]: "swarm" packs the points so
            none overlap; "strip" jitters them uniformly.
        jitter: The strip jitter width, as a fraction of the category width
            like `SwarmPlot`, scaled down to the rain's narrower cell. Only
            used with `mode="strip"`.
        bandwidth: The cloud's KDE bandwidth: None or "scott" (Scott's rule),
            "silverman" (Silverman's rule), or a scalar factor. See
            [`BANDWIDTH`][datachart.constants.BANDWIDTH].
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            [`ASPECT_RATIO`][datachart.constants.ASPECT_RATIO].
        orientation: The orientation of the rainclouds (vertical or horizontal).
        scaley: The y-axis scale (e.g., "log", "linear").
        subplots: Whether to create separate subplots for each chart.
        max_cols: Maximum number of columns in subplots (when subplots=True).
        sharex: Whether to share the x-axis in subplots.
        sharey: Whether to share the y-axis in subplots.
        style: Style configuration(s); the violin keys style the cloud, the
            swarm keys the rain, and the box keys the box.
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
        label: The key name in data for label/category values (default: "label").
        value: The key name in data for numeric values (default: "value").

    Returns:
        The figure containing the raincloud plot.

    """
    params = dict(locals())

    validate_bandwidth(bandwidth)

    return render("raincloudplot", params)
