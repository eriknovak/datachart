from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render
from ..utils._internal.chart_builder import dict_datasets
from ..utils._internal.validate import validate_treemap_records
from ..typings import (
    EmphasisRuleAttrs,
    TreemapSingleChartAttrs,
    TreemapStyleAttrs,
    TextSettingAttrs,
    LegendSettingAttrs,
)
from ..constants import FIG_SIZE, VALUE_FORMAT

# ================================================
# Main Chart Definition
# ================================================


def Treemap(
    data: Union[TreemapSingleChartAttrs, List[TreemapSingleChartAttrs]],
    *,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    title: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: None = None,
    emphasis_rule: Optional[EmphasisRuleAttrs] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    style: Optional[Union[TreemapStyleAttrs, List[Optional[TreemapStyleAttrs]]]] = None,
    texts: Optional[
        Union[
            TextSettingAttrs,
            List[TextSettingAttrs],
            List[Union[TextSettingAttrs, List[TextSettingAttrs], None]],
        ]
    ] = None,
) -> plt.Figure:
    """Creates the treemap.

    A treemap tiles part-of-whole data as rectangles whose area is the
    value — disk usage by folder, a budget by line, population by continent
    and country. A record's `children` group it, up to four levels deep: a
    group is a box in its color with a header band, its children inset in a
    lighter tint. Every level is sorted largest first and tiled so the
    rectangles stay near square. Use it when the question is how a whole
    splits; for the values alone, or for more than a handful of small parts,
    use [`BarChart`][datachart.charts.BarChart].

    Examples:
        >>> from datachart.charts import Treemap
        >>> figure = Treemap(
        ...     data={
        ...         "data": [
        ...             {"label": "Asia", "children": [
        ...                 {"label": "India", "value": 1429},
        ...                 {"label": "China", "value": 1426},
        ...             ]},
        ...             {"label": "Africa", "value": 1460},
        ...             {"label": "Europe", "value": 742},
        ...         ]
        ...     },
        ...     title="Population, millions",
        ... )

    Args:
        data: The chart data: a `{"data": [...]}` dict whose records are
            `{"label", "value"}` dicts, or a list of such dicts drawing one
            treemap per subplot. A record may carry `children`, a list of
            records of the same shape, nesting up to four levels deep; a
            group then omits `value` or carries its children's sum. Any
            record may carry an `emphasis` role: `"background"` mutes the
            tile or group, `"highlight"` strokes its border; the role applies
            to the whole subtree, and a descendant's own role overrides it.
        show_values: Whether to write each tile's value under its label. A
            value that does not fit is dropped before the label.
        value_format: The format of the tile values: a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] constant (default
            [`VALUE_FORMAT.DEFAULT`][datachart.constants.VALUE_FORMAT]) or any
            `"{x:.1f}"`, `"{:.1f}%"`, or `"%g"` style string.
        show_legend: Whether to list the top-level records in a legend; it
            names the groups too short for a header band.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        title: The title of the chart.
        subtitle: The subtitle(s) for individual charts.
        emphasis: Not supported: emphasis is set per record through its
            `emphasis` key. Passing a value raises `ValueError`.
        emphasis_rule: A rule that highlights the leaf records matching it and mutes the
            rest: `{"above": v}` or `{"below": v}` (strict), `{"between": (lo, hi)}`
            (inclusive), `{"top": n}` or `{"bottom": n}`, read against each leaf's
            `value`. A record's own `emphasis` key wins, and so does a group's, over its
            whole subtree. The rule takes no `by`. See
            [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        figsize: The size of the figure.
        subplots: Whether to show each chart in its own subplot; several
            charts always split into subplots.
        max_cols: Maximum number of columns in subplots.
        style: Style configuration(s) for the chart(s).
        texts: Text annotation(s) to draw. The tiling spans 0–1 in both
            directions.

    Returns:
        The figure containing the treemap.

    Raises:
        ValueError: If `emphasis` is given, the records are malformed (a
            missing label, a value not above zero, a record nested past four
            levels, a group value that is not its children's sum), or a record's
            `emphasis` is not a role.

    """
    params = dict(locals())

    for dataset in dict_datasets("treemap", data):
        validate_treemap_records(dataset["data"])

    return render("treemap", params)
