from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import validate_network_records
from ..typings import NetworkSingleChartAttrs, NetworkStyleAttrs, TextAttrs
from ..constants import FIG_SIZE, NETWORK_LAYOUT, VALUE_FORMAT

# ================================================
# Main Chart Definition
# ================================================


def NetworkChart(
    data: Union[NetworkSingleChartAttrs, List[NetworkSingleChartAttrs]],
    *,
    layout: Optional[Union[NETWORK_LAYOUT, str]] = None,
    directed: Optional[bool] = None,
    seed: Optional[int] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    show_legend: Optional[bool] = None,
    title: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: None = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    style: Optional[Union[NetworkStyleAttrs, List[Optional[NetworkStyleAttrs]]]] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
) -> plt.Figure:
    """Creates the network chart.

    A network chart draws relational data as a node-link diagram — module
    dependencies, who works with whom, co-occurring terms, flows between
    peers. Nodes are placed by a layout and joined by edges; an edge's weight
    sets its width, a node's size its marker area, its group its color. Use
    it when the question is what is connected to what; for weighted flows
    through ordered stages use [`SankeyChart`][datachart.charts.SankeyChart].

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.charts import NetworkChart
        >>> figure = NetworkChart(
        ...     data={
        ...         "edges": [
        ...             {"source": "core", "target": "utils"},
        ...             {"source": "cli", "target": "core"},
        ...             {"source": "api", "target": "core"},
        ...             {"source": "web", "target": "api"},
        ...         ]
        ...     },
        ...     directed=True,
        ...     title="Module dependencies",
        ... )

    Args:
        data: The chart data: a `{"nodes": [...], "edges": [...]}` dict, or a
            list of such dicts drawing one network per subplot. An edge is a
            `{"source", "target"}` record naming node ids, with an optional
            `weight` above zero. A node is an `{"id"}` record with an optional
            `label` (defaults to the id; an empty string draws nothing),
            `size` above zero, `group`, and `emphasis` role: `"background"`
            mutes the node, its label, and its edges, `"highlight"` strokes
            its border. `nodes` may be omitted; the node set is then read
            from the edges in first-seen order.
        layout: How the nodes are placed: a `NETWORK_LAYOUT` constant
            (default `NETWORK_LAYOUT.SPRING`). `FIXED` reads each node's
            `x`/`y` in the 0–1 layout space.
        directed: Whether the edges end in an arrowhead at the target. When
            `False` (the default), an edge and its reverse draw as one line.
        seed: The seed of the spring layout (default 0); another seed gives
            another arrangement of the same data.
        show_values: Whether to write each edge's weight at its midpoint.
        value_format: The format of the edge values: a `VALUE_FORMAT`
            constant (default `VALUE_FORMAT.DEFAULT`) or any `"{x:.1f}"`,
            `"{:.1f}%"`, or `"%g"` style string.
        show_legend: Whether to list the node groups in a legend.
        title: The title of the chart.
        subtitle: The subtitle(s) for individual charts.
        emphasis: Not supported: emphasis is set per node through its
            `emphasis` key. Passing a value raises `ValueError`.
        figsize: The size of the figure.
        subplots: Whether to show each chart in its own subplot; several
            charts always split into subplots.
        max_cols: Maximum number of columns in subplots.
        style: Style configuration(s) for the chart(s). The edge geometry,
            `plot_network_edge_style`, takes `ARROW_STYLE.CURVE` (default)
            or `ARROW_STYLE.STRAIGHT`; the arrowhead comes from `directed`.
        texts: Text annotation(s) to draw. The layout spans 0–1 in both
            directions.

    Returns:
        The figure containing the network chart.

    Raises:
        ValueError: If `emphasis` is given, `layout` is unknown, the records
            are malformed (a node without an id or a repeated id, an edge
            naming an unknown node or joining a node to itself, a `size` or
            `weight` not above zero, a node without `x`/`y` under the fixed
            layout, an `emphasis` that is not a role), or
            `plot_network_edge_style` is a headed connector look.

    """
    if emphasis is not None:
        raise ValueError(
            "NetworkChart does not support the `emphasis` argument: set the "
            "`emphasis` key on the nodes to mute or highlight instead."
        )

    datasets = data if isinstance(data, list) else [data]
    if not all(isinstance(d, dict) and "edges" in d for d in datasets):
        raise ValueError(
            'NetworkChart `data` must be a `{"nodes": [...], "edges": [...]}` '
            "dict, or a list of such dicts."
        )
    resolved_layout = NETWORK_LAYOUT.DEFAULT if layout is None else layout
    for dataset in datasets:
        dataset["nodes"] = validate_network_records(
            dataset.get("nodes"), dataset["edges"], resolved_layout
        )

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
        "layout": resolved_layout,
        "directed": directed,
        "seed": seed,
        "show_values": show_values,
        "value_format": value_format,
        "show_legend": show_legend,
    }

    return render_chart("networkchart", charts, settings)
