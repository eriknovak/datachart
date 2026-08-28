from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import validate_sankey_links, validate_sankey_nodes
from ..typings import SankeySingleChartAttrs, SankeyStyleAttrs, TextAttrs
from ..constants import FIG_SIZE, VALUE_FORMAT

# ================================================
# Main Chart Definition
# ================================================


def SankeyChart(
    data: Union[SankeySingleChartAttrs, List[SankeySingleChartAttrs]],
    *,
    nodes: Optional[List[List[str]]] = None,
    column_labels: Optional[List[str]] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    title: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: None = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    style: Optional[Union[SankeyStyleAttrs, List[Optional[SankeyStyleAttrs]]]] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
) -> plt.Figure:
    """Creates the Sankey chart.

    A Sankey diagram draws weighted flows between categories: nodes are bars
    laid out in columns and each flow is a ribbon whose height carries its
    value — label transitions between annotators, attrition through a signup
    funnel, energy from source to use. Use it when the question is where a
    quantity goes; for the totals per category alone use
    [`BarChart`][datachart.charts.BarChart].

    !!! info "Added in 0.9.0"

    Examples:
        >>> from datachart.charts import SankeyChart
        >>> figure = SankeyChart(
        ...     data={
        ...         "links": [
        ...             {"source": "Visited", "target": "Signed up", "value": 300},
        ...             {"source": "Visited", "target": "Bounced", "value": 700},
        ...             {"source": "Signed up", "target": "Paid", "value": 90},
        ...             {"source": "Signed up", "target": "Churned", "value": 210},
        ...         ]
        ...     },
        ...     title="Signup funnel",
        ... )

    Args:
        data: The chart data: a `{"links": [...]}` dict whose links are
            `{"source", "target", "value"}` records, or a list of such dicts
            drawing one Sankey per subplot. A node is the string that names
            it, which is also its drawn label.
        nodes: The node columns, left to right, each a list of node names
            top to bottom. Must name every node in the links exactly once.
            When omitted, a node's column is its longest path from any
            source and nodes keep their first-seen order within a column.
        column_labels: One heading per column, drawn above it; must match the
            number of columns.
        show_values: Whether to write each flow's value on its ribbon.
        value_format: The format of the ribbon values: a `VALUE_FORMAT`
            constant (default `VALUE_FORMAT.DEFAULT`) or any `"{x:.1f}"`,
            `"{:.1f}%"`, or `"%g"` style string.
        title: The title of the chart.
        subtitle: The subtitle(s) for individual charts.
        emphasis: Not supported: a Sankey has no series to mute or
            highlight. Passing a value raises `ValueError`.
        figsize: The size of the figure.
        subplots: Whether to show each chart in its own subplot; several
            charts always split into subplots.
        max_cols: Maximum number of columns in subplots.
        style: Style configuration(s) for the chart(s).
        texts: Text annotation(s) to draw. The columns span 0–1 horizontally
            and the tallest column 0–1 vertically.

    Returns:
        The figure containing the Sankey chart.

    Raises:
        ValueError: If `emphasis` is given, the links are malformed (missing
            keys, a value not above zero, a self-link), the links form a
            cycle, `nodes` does not name exactly the linked nodes, or
            `column_labels` does not match the number of columns.

    """
    if emphasis is not None:
        raise ValueError(
            "SankeyChart does not support `emphasis`: a Sankey has no series "
            "to mute or highlight."
        )

    datasets = data if isinstance(data, list) else [data]
    if not all(isinstance(d, dict) and "links" in d for d in datasets):
        raise ValueError(
            'SankeyChart `data` must be a `{"links": [...]}` dict, or a list of '
            "such dicts."
        )
    for dataset in datasets:
        validate_sankey_links(dataset["links"])
        if nodes is not None:
            validate_sankey_nodes(nodes, dataset["links"])

    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        style=style,
        texts=texts,
        is_2d_data=True,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "title": title,
        "figsize": figsize,
        "subplots": subplots,
        "max_cols": max_cols,
        "nodes": nodes,
        "column_labels": column_labels,
        "show_values": show_values,
        "value_format": value_format,
    }

    return render_chart("sankeychart", charts, settings)
