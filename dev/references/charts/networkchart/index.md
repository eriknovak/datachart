# NetworkChart

Nodes joined by edges, placed by a layout. The [Network Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/networkchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.NetworkChart

```
NetworkChart(
    data: (
        NetworkSingleChartAttrs
        | list[NetworkSingleChartAttrs]
    ),
    *,
    layout: NETWORK_LAYOUT | str | None = None,
    directed: bool | None = None,
    seed: int | None = None,
    label_position: (
        NETWORK_LABEL_POSITION | str | None
    ) = None,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    title: str | None = None,
    subtitle: str | list[str | None] | None = None,
    emphasis: None = None,
    emphasis_rule: EmphasisRuleAttrs | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    style: (
        NetworkStyleAttrs
        | list[NetworkStyleAttrs | None]
        | None
    ) = None,
    texts: (
        TextSettingAttrs
        | list[TextSettingAttrs]
        | list[
            TextSettingAttrs | list[TextSettingAttrs] | None
        ]
        | None
    ) = None
) -> plt.Figure
```

Creates the network chart.

A network chart draws relational data as a node-link diagram — module dependencies, who works with whom, co-occurring terms, flows between peers. Nodes are placed by a layout and joined by edges; an edge's weight sets its width, a node's size its marker area, its group its color. Use it when the question is what is connected to what; for weighted flows through ordered stages use SankeyChart.

Every edge is its own patch and the spring layout weighs every pair of nodes, so the chart is meant for networks that can be read, not for whole graphs. Without a problem: up to about 1,000 nodes and 3,000 edges under the spring layout (a few seconds), up to about 5,000 nodes and 15,000 edges under the circular or fixed layout (under a minute). Beyond that the spring layout grows with the square of the node count — 2,000 nodes take half a minute, 5,000 several minutes and gigabytes of memory — and every layout pays a few milliseconds per edge to draw and again to save. Aggregate or filter a larger graph first.

Examples:

```
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
```

| PARAMETER        | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`           | The chart data: a {"nodes": [...], "edges": [...]} dict, or a list of such dicts drawing one network per subplot. An edge is a {"source", "target"} record naming node ids, with an optional weight above zero. A node is an {"id"} record with an optional label (defaults to the id; an empty string draws nothing), size above zero, group (a node without one draws in the edge color beside grouped nodes), and emphasis role: "background" mutes the node, its label, and its edges, "highlight" strokes its border. nodes may be omitted; the node set is then read from the edges in first-seen order. **TYPE:** \`NetworkSingleChartAttrs                                                                                                               |
| `layout`         | How the nodes are placed: a NETWORK_LAYOUT constant (default NETWORK_LAYOUT.SPRING); on a disconnected network, SPRING and WEIGHTED place each connected part on its own, side by side, with the unlinked nodes on a ring around them. WEIGHTED lets each edge's weight set how hard it pulls its nodes together; GROUPED clusters the nodes by group, arranges the clusters by the summed weight of the edges between them, and marks each with a disc in the group color (plot_network_group_alpha). FIXED reads each node's x/y, each between 0 and 1, and draws that space inside the margin the other layouts keep. The three spring layouts cost the square of the node count; past about 1,000 nodes prefer CIRCULAR or FIXED. **TYPE:** \`NETWORK_LAYOUT |
| `directed`       | Whether the edges end in an arrowhead at the target. When False (the default), an edge and its reverse draw as one line. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `seed`           | The seed of the spring layouts (default 0); another seed gives another arrangement of the same data. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `label_position` | Where the node names print: a NETWORK_LABEL_POSITION constant (default NETWORK_LABEL_POSITION.CENTER, or the theme's chart_default_network_label_position). **TYPE:** \`NETWORK_LABEL_POSITION                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `show_values`    | Whether to write each edge's weight at its midpoint. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `value_format`   | The format of the edge values: a VALUE_FORMAT constant (default VALUE_FORMAT.DEFAULT) or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `show_legend`    | Whether to list the node groups in a legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `legend`         | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `title`          | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `subtitle`       | The subtitle(s) for individual charts. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `emphasis`       | Not supported: emphasis is set per node through its emphasis key. Passing a value raises ValueError. **TYPE:** `None` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `emphasis_rule`  | A rule that highlights the nodes matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against each node's size; a node without one raises. A node's own emphasis key wins. The rule takes no by. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `figsize`        | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `subplots`       | Whether to show each chart in its own subplot; several charts always split into subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `max_cols`       | Maximum number of columns in subplots. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `style`          | Style configuration(s) for the chart(s). The edge geometry, plot_network_edge_style, takes ARROW_STYLE.CURVE (default) or ARROW_STYLE.STRAIGHT; the arrowhead comes from directed. **TYPE:** \`NetworkStyleAttrs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `texts`          | Text annotation(s) to draw. Data coordinates are the 0–1 layout space, so under FIXED a text at a node's x/y lands on that node. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

| RETURNS      | DESCRIPTION                              |
| ------------ | ---------------------------------------- |
| `plt.Figure` | The figure containing the network chart. |

| RAISES       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                          |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If emphasis is given, layout is unknown, the records are malformed (a node without an id or a repeated id, an edge naming an unknown node or joining a node to itself, a size or weight not above zero, a node without x/y, or with one outside 0–1, under the fixed layout, an emphasis that is not a role), or plot_network_edge_style is a headed connector look. |

## Data

`data` is one [`NetworkSingleChartAttrs`](#datachart.typings.NetworkSingleChartAttrs), or a list of them for subplots, with [`NetworkNodeAttrs`](#datachart.typings.NetworkNodeAttrs) and [`NetworkEdgeAttrs`](#datachart.typings.NetworkEdgeAttrs) inside.

### datachart.typings.NetworkSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the network chart.

| ATTRIBUTE  | DESCRIPTION                                                                         |
| ---------- | ----------------------------------------------------------------------------------- |
| `nodes`    | The nodes; inferred from the edges when omitted. **TYPE:** \`list[NetworkNodeAttrs] |
| `edges`    | The edges. **TYPE:** `list[NetworkEdgeAttrs]`                                       |
| `subtitle` | The subtitle of the chart. **TYPE:** \`str                                          |
| `style`    | The style of the chart. **TYPE:** \`NetworkStyleAttrs                               |
| `texts`    | The text annotations to be drawn. **TYPE:** \`TextSettingAttrs                      |

### datachart.typings.NetworkNodeAttrs

Bases: `TypedDict`

The node record attributes for the network chart.

| ATTRIBUTE  | DESCRIPTION                                                                                          |
| ---------- | ---------------------------------------------------------------------------------------------------- |
| `id`       | The node identifier the edges refer to; unique within a chart. **TYPE:** `str`                       |
| `label`    | The drawn label; defaults to id. An empty string draws nothing. **TYPE:** \`str                      |
| `size`     | The node size, mapped by square root to marker area; must be greater than 0. **TYPE:** \`int         |
| `group`    | The group the node is colored by. **TYPE:** \`str                                                    |
| `emphasis` | The emphasis role of the node. **TYPE:** \`EMPHASIS                                                  |
| `x`        | The node's horizontal position in the 0–1 layout space; NETWORK_LAYOUT.FIXED only. **TYPE:** \`float |
| `y`        | The node's vertical position in the 0–1 layout space; NETWORK_LAYOUT.FIXED only. **TYPE:** \`float   |

### datachart.typings.NetworkEdgeAttrs

Bases: `TypedDict`

The edge record attributes for the network chart.

| ATTRIBUTE | DESCRIPTION                                                                                                             |
| --------- | ----------------------------------------------------------------------------------------------------------------------- |
| `source`  | The id of the node the edge leaves. **TYPE:** `str`                                                                     |
| `target`  | The id of the node the edge enters. **TYPE:** `str`                                                                     |
| `weight`  | The edge weight, mapped to its width and, under the weighted layouts, its pull; must be greater than 0. **TYPE:** \`int |

## Style

`style` takes the keys of [`NetworkStyleAttrs`](#datachart.typings.NetworkStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.NetworkStyleAttrs

Bases: `TypedDict`

The typing for the network chart style.

| ATTRIBUTE                           | DESCRIPTION                                                                                                                                                                                                                                 |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_network_node_color`           | The node marker color; overrides the color cycle. **TYPE:** \`str                                                                                                                                                                           |
| `plot_network_node_alpha`           | The alpha value of the node markers. **TYPE:** \`float                                                                                                                                                                                      |
| `plot_network_node_marker`          | The node marker shape. **TYPE:** \`LINE_MARKER                                                                                                                                                                                              |
| `plot_network_node_size`            | The marker area of a node without size. **TYPE:** \`int                                                                                                                                                                                     |
| `plot_network_node_size_min`        | The marker area of the smallest sized node. **TYPE:** \`int                                                                                                                                                                                 |
| `plot_network_node_size_max`        | The marker area of the largest sized node. **TYPE:** \`int                                                                                                                                                                                  |
| `plot_network_node_edge_color`      | The node stroke color. **TYPE:** \`str                                                                                                                                                                                                      |
| `plot_network_node_edge_width`      | The node stroke width. **TYPE:** \`int                                                                                                                                                                                                      |
| `plot_network_edge_style`           | The edge geometry: ARROW_STYLE.CURVE or ARROW_STYLE.STRAIGHT. **TYPE:** \`ARROW_STYLE                                                                                                                                                       |
| `plot_network_edge_curve`           | The bow of a curved edge; the sign picks the side. **TYPE:** \`float                                                                                                                                                                        |
| `plot_network_edge_color`           | The edge color. **TYPE:** \`str                                                                                                                                                                                                             |
| `plot_network_edge_alpha`           | The edge alpha. **TYPE:** \`float                                                                                                                                                                                                           |
| `plot_network_edge_width_min`       | The width of the lightest edge, and of an edge without weight. **TYPE:** \`int                                                                                                                                                              |
| `plot_network_edge_width_max`       | The width of the heaviest edge. **TYPE:** \`int                                                                                                                                                                                             |
| `plot_network_highlight_edge_width` | The stroke width of a highlighted node. **TYPE:** \`float                                                                                                                                                                                   |
| `plot_network_label_halo_width`     | The width of the halo, in the axes face color, behind labels; 0 disables it. **TYPE:** \`float                                                                                                                                              |
| `plot_network_label_family`         | The font family of the node labels; None keeps the general font. **TYPE:** \`str                                                                                                                                                            |
| `plot_network_group_alpha`          | The alpha of the disc in the group color behind each cluster of the grouped layout; 0 disables it. **TYPE:** \`float                                                                                                                        |
| `plot_network_group_linestyle`      | Draws each cluster's mark as a ring in this line style and the edge color instead of a disc. None draws the disc. **TYPE:** \`LINE_STYLE                                                                                                    |
| `plot_network_edge_ink_stroke`      | The pen the edges are drawn with, as for plot_ink_stroke, plus swell (the pressure swell amplitude) and noise (the grain); a directed edge draws as a stroked shaft with a small head. None draws plain edges. **TYPE:** \`dict[str, float] |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `layout`                                     | [`NETWORK_LAYOUT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.NETWORK_LAYOUT)                                                                                                                       |
| `label_position`                             | [`NETWORK_LABEL_POSITION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.NETWORK_LABEL_POSITION)                                                                                                       |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |

## Composition

Whether the figure composes with each composition function.

| Function                                                                                     | Composes |
| -------------------------------------------------------------------------------------------- | -------- |
| [`Grid`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Grid)   | yes      |
| [`Panel`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) | no       |
