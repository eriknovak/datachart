# SankeyChart

Weighted flows between categories, as ribbons between node columns. The [Sankey Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/sankeychart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.SankeyChart

```
SankeyChart(
    data: (
        SankeySingleChartAttrs
        | list[SankeySingleChartAttrs]
    ),
    *,
    nodes: list[list[str]] | None = None,
    column_labels: list[str] | None = None,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    title: str | None = None,
    subtitle: str | list[str | None] | None = None,
    emphasis: None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    style: (
        SankeyStyleAttrs
        | list[SankeyStyleAttrs | None]
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

Creates the Sankey chart.

A Sankey diagram draws weighted flows between categories: nodes are bars laid out in columns and each flow is a ribbon whose height carries its value — label transitions between annotators, attrition through a signup funnel, energy from source to use. Use it when the question is where a quantity goes; for the totals per category alone use BarChart.

Examples:

```
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
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                      |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The chart data: a {"links": [...]} dict whose links are {"source", "target", "value"} records, or a list of such dicts drawing one Sankey per subplot. A node is the string that names it, which is also its drawn label. **TYPE:** \`SankeySingleChartAttrs                     |
| `nodes`         | The node columns, left to right, each a list of node names top to bottom. Must name every node in the links exactly once. When omitted, a node's column is its longest path from any source and nodes keep their first-seen order within a column. **TYPE:** \`list\[list[str]\] |
| `column_labels` | One heading per column, drawn above it; must match the number of columns. **TYPE:** \`list[str]                                                                                                                                                                                  |
| `show_values`   | Whether to write each flow's value on its ribbon. **TYPE:** \`bool                                                                                                                                                                                                               |
| `value_format`  | The format of the ribbon values: a VALUE_FORMAT constant (default VALUE_FORMAT.DEFAULT) or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                              |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                          |
| `subtitle`      | The subtitle(s) for individual charts. **TYPE:** \`str                                                                                                                                                                                                                           |
| `emphasis`      | Not supported: a Sankey has no series to mute or highlight. Passing a value raises ValueError. **TYPE:** `None` **DEFAULT:** `None`                                                                                                                                              |
| `figsize`       | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                     |
| `subplots`      | Whether to show each chart in its own subplot; several charts always split into subplots. **TYPE:** \`bool                                                                                                                                                                       |
| `max_cols`      | Maximum number of columns in subplots. **TYPE:** \`int                                                                                                                                                                                                                           |
| `style`         | Style configuration(s) for the chart(s). **TYPE:** \`SankeyStyleAttrs                                                                                                                                                                                                            |
| `texts`         | Text annotation(s) to draw. The columns span 0–1 horizontally and the tallest column 0–1 vertically. **TYPE:** \`TextSettingAttrs                                                                                                                                                |

| RETURNS      | DESCRIPTION                             |
| ------------ | --------------------------------------- |
| `plt.Figure` | The figure containing the Sankey chart. |

| RAISES       | DESCRIPTION                                                                                                                                                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If emphasis is given, the links are malformed (missing keys, a value not above zero, a self-link), the links form a cycle, nodes does not name exactly the linked nodes, or column_labels does not match the number of columns. |

## Data

`data` is one [`SankeySingleChartAttrs`](#datachart.typings.SankeySingleChartAttrs), or a list of them for subplots, with [`SankeyLinkAttrs`](#datachart.typings.SankeyLinkAttrs) inside.

### datachart.typings.SankeySingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the Sankey chart.

| ATTRIBUTE  | DESCRIPTION                                                                      |
| ---------- | -------------------------------------------------------------------------------- |
| `links`    | The flows; a node is the string that names it. **TYPE:** `list[SankeyLinkAttrs]` |
| `subtitle` | The subtitle of the chart. **TYPE:** \`str                                       |
| `style`    | The style of the chart. **TYPE:** \`SankeyStyleAttrs                             |
| `texts`    | The text annotations to be drawn. **TYPE:** \`TextSettingAttrs                   |

### datachart.typings.SankeyLinkAttrs

Bases: `TypedDict`

The link record attributes for the Sankey chart.

| ATTRIBUTE | DESCRIPTION                                                   |
| --------- | ------------------------------------------------------------- |
| `source`  | The node the flow leaves. **TYPE:** `str`                     |
| `target`  | The node the flow enters. **TYPE:** `str`                     |
| `value`   | The size of the flow; must be greater than 0. **TYPE:** \`int |

## Style

`style` takes the keys of [`SankeyStyleAttrs`](#datachart.typings.SankeyStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.SankeyStyleAttrs

Bases: `TypedDict`

The typing for the Sankey chart style.

| ATTRIBUTE                      | DESCRIPTION                                                                                    |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| `plot_sankey_node_width`       | The node bar width as a fraction of the horizontal span. **TYPE:** \`float                     |
| `plot_sankey_node_pad`         | The vertical span shared by the gaps of the tallest column. **TYPE:** \`float                  |
| `plot_sankey_node_edge_color`  | The node stroke color. **TYPE:** \`str                                                         |
| `plot_sankey_node_edge_width`  | The node stroke width. **TYPE:** \`float                                                       |
| `plot_sankey_link_color`       | Which node colors a ribbon: "source", "target", or "grey". **TYPE:** \`str                     |
| `plot_sankey_link_alpha`       | The ribbon alpha. **TYPE:** \`float                                                            |
| `plot_sankey_label_halo_width` | The width of the halo, in the axes face color, behind labels; 0 disables it. **TYPE:** \`float |
| `plot_sankey_node_fill`        | Whether the node bars are filled; False draws them as outlines. **TYPE:** \`bool               |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter      | Constant                                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------------------------ |
| `value_format` | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT) |
| `figsize`      | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)         |

## Composition

Whether the figure composes with each composition function.

| Function                                                                                     | Composes |
| -------------------------------------------------------------------------------------------- | -------- |
| [`Grid`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Grid)   | yes      |
| [`Panel`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) | no       |
