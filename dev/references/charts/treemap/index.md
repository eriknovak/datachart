# Treemap

Part-of-whole data as nested rectangles sized by value. The [Treemap guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/treemap/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.Treemap

```
Treemap(
    data: (
        TreemapSingleChartAttrs
        | list[TreemapSingleChartAttrs]
    ),
    *,
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
        TreemapStyleAttrs
        | list[TreemapStyleAttrs | None]
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

Creates the treemap.

A treemap tiles part-of-whole data as rectangles whose area is the value — disk usage by folder, a budget by line, population by continent and country. A record's `children` group it, up to four levels deep: a group is a box in its color with a header band, its children inset in a lighter tint. Every level is sorted largest first and tiled so the rectangles stay near square. Use it when the question is how a whole splits; for the values alone, or for more than a handful of small parts, use BarChart.

Examples:

```
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
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | The chart data: a {"data": [...]} dict whose records are {"label", "value"} dicts, or a list of such dicts drawing one treemap per subplot. A record may carry children, a list of records of the same shape, nesting up to four levels deep; a group then omits value or carries its children's sum. Any record may carry an emphasis role: "background" mutes the tile or group, "highlight" strokes its border; the role applies to the whole subtree, and a descendant's own role overrides it. **TYPE:** \`TreemapSingleChartAttrs |
| `show_values`   | Whether to write each tile's value under its label. A value that does not fit is dropped before the label. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                             |
| `value_format`  | The format of the tile values: a VALUE_FORMAT constant (default VALUE_FORMAT.DEFAULT) or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                                                                                                                       |
| `show_legend`   | Whether to list the top-level records in a legend; it names the groups too short for a header band. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `legend`        | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                                                                                                                                  |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `subtitle`      | The subtitle(s) for individual charts. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `emphasis`      | Not supported: emphasis is set per record through its emphasis key. Passing a value raises ValueError. **TYPE:** `None` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                             |
| `emphasis_rule` | A rule that highlights the leaf records matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}, read against each leaf's value. A record's own emphasis key wins, and so does a group's, over its whole subtree. The rule takes no by. See EmphasisRuleAttrs. **TYPE:** \`EmphasisRuleAttrs                                                                                                                                                              |
| `figsize`       | The size of the figure. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `subplots`      | Whether to show each chart in its own subplot; several charts always split into subplots. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `max_cols`      | Maximum number of columns in subplots. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `style`         | Style configuration(s) for the chart(s). **TYPE:** \`TreemapStyleAttrs                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `texts`         | Text annotation(s) to draw. The tiling spans 0–1 in both directions. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                                                                       |

| RETURNS      | DESCRIPTION                        |
| ------------ | ---------------------------------- |
| `plt.Figure` | The figure containing the treemap. |

| RAISES       | DESCRIPTION                                                                                                                                                                                                      |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If emphasis is given, the records are malformed (a missing label, a value not above zero, a record nested past four levels, a group value that is not its children's sum), or a record's emphasis is not a role. |

## Data

`data` is one [`TreemapSingleChartAttrs`](#datachart.typings.TreemapSingleChartAttrs), or a list of them for subplots, with [`TreemapRecordAttrs`](#datachart.typings.TreemapRecordAttrs) inside.

### datachart.typings.TreemapSingleChartAttrs

Bases: `TypedDict`

The single chart attributes for the treemap.

| ATTRIBUTE  | DESCRIPTION                                                    |
| ---------- | -------------------------------------------------------------- |
| `data`     | The records to tile. **TYPE:** `list[TreemapRecordAttrs]`      |
| `subtitle` | The subtitle of the chart. **TYPE:** \`str                     |
| `style`    | The style of the chart. **TYPE:** \`TreemapStyleAttrs          |
| `texts`    | The text annotations to be drawn. **TYPE:** \`TextSettingAttrs |

### datachart.typings.TreemapRecordAttrs

Bases: `TypedDict`

The record attributes for the treemap.

| ATTRIBUTE  | DESCRIPTION                                                                                                   |
| ---------- | ------------------------------------------------------------------------------------------------------------- |
| `label`    | The drawn label of the tile or group. **TYPE:** `str`                                                         |
| `value`    | The size of the tile; must be greater than 0. A group omits it or carries its children's sum. **TYPE:** \`int |
| `children` | The records of a group, nesting up to four levels deep. **TYPE:** \`list[TreemapRecordAttrs]                  |
| `emphasis` | The emphasis role of the record and its subtree; a descendant's own role overrides it. **TYPE:** \`EMPHASIS   |

## Style

`style` takes the keys of [`TreemapStyleAttrs`](#datachart.typings.TreemapStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ValueLabelStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.TreemapStyleAttrs

Bases: `TypedDict`

The typing for the treemap style.

| ATTRIBUTE                           | DESCRIPTION                                                                                                                                                                                                                                                                               |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_treemap_edge_color`           | The stroke color of leaf tiles and group borders. **TYPE:** \`str                                                                                                                                                                                                                         |
| `plot_treemap_edge_width`           | The leaf tile stroke width. **TYPE:** \`float                                                                                                                                                                                                                                             |
| `plot_treemap_group_edge_width`     | The width of the border around a group. **TYPE:** \`float                                                                                                                                                                                                                                 |
| `plot_treemap_group_pad`            | The gap between top-level records and, at every level, the gutter between a group's border and its children, as a fraction of the span. **TYPE:** \`float                                                                                                                                 |
| `plot_treemap_level_shade`          | How much lighter than its parent each level is, 0 to 1, applied once more per level; 0 keeps the group color. **TYPE:** \`float                                                                                                                                                           |
| `plot_treemap_level_font_scale`     | The label font scale applied once more per nesting level. **TYPE:** \`float                                                                                                                                                                                                               |
| `plot_treemap_min_fontsize`         | The smallest font size a label shrinks to before it is dropped. **TYPE:** \`float                                                                                                                                                                                                         |
| `plot_treemap_highlight_edge_width` | The border width of a highlighted record. **TYPE:** \`float                                                                                                                                                                                                                               |
| `plot_treemap_label_halo_width`     | The width of the halo, in the axes face color, behind labels; 0 disables it. **TYPE:** \`float                                                                                                                                                                                            |
| `plot_treemap_etch_density`         | With plot_etch and a hatch cycle, how many times each nesting level repeats its top-level group's pattern, outermost first (a level past the list is blank); every box fills with the axes face so outer etching never shows through. None keeps the colored tiles. **TYPE:** \`list[int] |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                           |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                   |

## Composition

Whether the figure composes with each composition function.

| Function                                                                                     | Composes |
| -------------------------------------------------------------------------------------------- | -------- |
| [`Grid`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Grid)   | yes      |
| [`Panel`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) | no       |
