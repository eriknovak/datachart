from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import (
    infer_network_nodes,
    validate_network_records,
)
from ..typings import (
    EmphasisRuleAttrs,
    NetworkSingleChartAttrs,
    NetworkStyleAttrs,
    TextSettingAttrs,
    LegendSettingAttrs,
)
from ..constants import FIG_SIZE, NETWORK_LAYOUT, NETWORK_LABEL_POSITION, VALUE_FORMAT

# ================================================
# Main Chart Definition
# ================================================


def NetworkChart(
    data: Union[NetworkSingleChartAttrs, List[NetworkSingleChartAttrs]],
    *,
    layout: Optional[Union[NETWORK_LAYOUT, str]] = None,
    directed: Optional[bool] = None,
    seed: Optional[int] = None,
    label_position: Optional[Union[NETWORK_LABEL_POSITION, str]] = None,
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
    style: Optional[Union[NetworkStyleAttrs, List[Optional[NetworkStyleAttrs]]]] = None,
    texts: Optional[
        Union[
            TextSettingAttrs,
            List[TextSettingAttrs],
            List[Union[TextSettingAttrs, List[TextSettingAttrs], None]],
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

    Every edge is its own patch and the spring layout weighs every pair of
    nodes, so the chart is meant for networks that can be read, not for
    whole graphs. Without a problem: up to about 1,000 nodes and 3,000
    edges under the spring layout (a few seconds), up to about 5,000 nodes
    and 15,000 edges under the circular or fixed layout (under a minute).
    Beyond that the spring layout grows with the square of the node count —
    2,000 nodes take half a minute, 5,000 several minutes and gigabytes of
    memory — and every layout pays a few milliseconds per edge to draw and
    again to save. Aggregate or filter a larger graph first.

    !!! info "Added in v0.9.1"

    !!! info "Added in Unreleased"

        The `legend` parameter.
        The `emphasis_rule` parameter.
        The `label_position` parameter.

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
            `size` above zero, `group` (a node without one draws in the edge
            color beside grouped nodes), and `emphasis` role: `"background"`
            mutes the node, its label, and its edges, `"highlight"` strokes
            its border. `nodes` may be omitted; the node set is then read
            from the edges in first-seen order.
        layout: How the nodes are placed: a
            [`NETWORK_LAYOUT`][datachart.constants.NETWORK_LAYOUT] constant (default
            [`NETWORK_LAYOUT.SPRING`][datachart.constants.NETWORK_LAYOUT]); on a
            disconnected network, `SPRING` and `WEIGHTED` place each connected part
            on its own, side by side, with the unlinked nodes on a ring around them.
            `WEIGHTED` lets each edge's weight set how hard it pulls its nodes
            together; `GROUPED` clusters the nodes by `group`, arranges the clusters
            by the summed weight of the edges between them, and marks each with a
            disc in the group color (`plot_network_group_alpha`). `FIXED` reads each
            node's `x`/`y`, each between 0 and 1, and draws that space inside the
            margin the other layouts keep.
            The three spring layouts cost the square of the node count; past about
            1,000 nodes prefer `CIRCULAR` or `FIXED`.
        directed: Whether the edges end in an arrowhead at the target. When
            `False` (the default), an edge and its reverse draw as one line.
        seed: The seed of the spring layouts (default 0); another seed gives
            another arrangement of the same data.
        label_position: Where the node names print: a
            [`NETWORK_LABEL_POSITION`][datachart.constants.NETWORK_LABEL_POSITION] constant
            (default
            [`NETWORK_LABEL_POSITION.CENTER`][datachart.constants.NETWORK_LABEL_POSITION], or
            the theme's `chart_default_node_label_position`).
        show_values: Whether to write each edge's weight at its midpoint.
        value_format: The format of the edge values: a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] constant (default
            [`VALUE_FORMAT.DEFAULT`][datachart.constants.VALUE_FORMAT]) or any
            `"{x:.1f}"`, `"{:.1f}%"`, or `"%g"` style string.
        show_legend: Whether to list the node groups in a legend.
        legend: The per-figure legend setting: title, location, column count
            and alignment; each field falls back to the theme. See
            [`LegendSettingAttrs`][datachart.typings.LegendSettingAttrs].
        title: The title of the chart.
        subtitle: The subtitle(s) for individual charts.
        emphasis: Not supported: emphasis is set per node through its
            `emphasis` key. Passing a value raises `ValueError`.
        emphasis_rule: A rule that highlights the nodes matching it and mutes
            the rest: `{"above": v}` or `{"below": v}` (strict),
            `{"between": (lo, hi)}` (inclusive), `{"top": n}` or
            `{"bottom": n}`, read against each node's `size`; a node without one
            raises. A node's own `emphasis` key wins. The rule takes no `by`.
            See [`EmphasisRuleAttrs`][datachart.typings.EmphasisRuleAttrs].
        figsize: The size of the figure.
        subplots: Whether to show each chart in its own subplot; several
            charts always split into subplots.
        max_cols: Maximum number of columns in subplots.
        style: Style configuration(s) for the chart(s). The edge geometry,
            `plot_network_edge_style`, takes
            [`ARROW_STYLE.CURVE`][datachart.constants.ARROW_STYLE] (default) or
            [`ARROW_STYLE.STRAIGHT`][datachart.constants.ARROW_STYLE]; the arrowhead
            comes from `directed`.
        texts: Text annotation(s) to draw. Data coordinates are the 0–1 layout
            space, so under `FIXED` a text at a node's `x`/`y` lands on that node.

    Returns:
        The figure containing the network chart.

    Raises:
        ValueError: If `emphasis` is given, `layout` is unknown, the records
            are malformed (a node without an id or a repeated id, an edge
            naming an unknown node or joining a node to itself, a `size` or
            `weight` not above zero, a node without `x`/`y`, or with one
            outside 0–1, under the fixed layout, an `emphasis` that is not a
            role), or `plot_network_edge_style` is a headed connector look.

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
        nodes = dataset.get("nodes")
        if nodes is None:
            nodes = infer_network_nodes(dataset["edges"])
        validate_network_records(nodes, dataset["edges"], resolved_layout)

    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        style=style,
        texts=texts,
        is_2d_data=True,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "emphasis_rule": emphasis_rule,
        "title": title,
        "figsize": figsize,
        "subplots": subplots,
        "max_cols": max_cols,
        "layout": resolved_layout,
        "directed": directed,
        "seed": seed,
        "label_position": label_position,
        "show_values": show_values,
        "value_format": value_format,
        "show_legend": show_legend,
        "legend": legend,
    }

    return render_chart("networkchart", charts, settings)
