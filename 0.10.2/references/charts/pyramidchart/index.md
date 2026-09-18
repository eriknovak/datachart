# PyramidChart

Two series as horizontal bars mirrored around a shared category axis. The [Pyramid Chart guide](https://eriknovak.github.io/datachart/0.10.2/how-to-guides/charts/pyramidchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.PyramidChart

```
PyramidChart(
    data: list[list[BarDataPointAttrs]],
    *,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    subtitle: str | list[str | None] | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    xmin: int | float | None = None,
    xmax: int | float | None = None,
    show_legend: bool | None = None,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    show_yerr: bool | None = None,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    sort: SORT | str | None = None,
    sort_by: str | None = None,
    emphasis_rule: EmphasisRuleAttrs | None = None,
    style: (
        BarStyleAttrs | list[BarStyleAttrs | None] | None
    ) = None,
    xticks: list[int | float] | None = None,
    xticklabels: list[str] | None = None,
    xtickrotate: int | None = None,
    yticks: list[int | float] | None = None,
    yticklabels: list[str] | None = None,
    ytickrotate: int | None = None,
    xticks_format: (
        VALUE_FORMAT | DATE_FORMAT | str | None
    ) = None,
    yticks_format: (
        VALUE_FORMAT | DATE_FORMAT | str | None
    ) = None,
    vlines: (
        VLineSettingAttrs | list[VLineSettingAttrs] | None
    ) = None,
    hlines: (
        HLineSettingAttrs | list[HLineSettingAttrs] | None
    ) = None,
    vspans: (
        VSpanSettingAttrs | list[VSpanSettingAttrs] | None
    ) = None,
    hspans: (
        HSpanSettingAttrs | list[HSpanSettingAttrs] | None
    ) = None,
    texts: (
        TextSettingAttrs | list[TextSettingAttrs] | None
    ) = None,
    label: str | list[str | None] | None = None,
    y: str | list[str | None] | None = None,
    yerr: str | list[str | None] | None = None
) -> plt.Figure
```

Creates the pyramid chart.

A pyramid chart draws exactly two series as horizontal bars mirrored around a shared category axis, the first series to the left and the second to the right: the classic age-sex population pyramid. Use it to compare the distribution of two groups over the same ordered categories, such as age bands, where the symmetry (or lack of it) is the message.

Both series are supplied as positive values; value ticks and labels show absolute values. Unlike the other chart fronts, the axis parameters are spatial: `xlabel`, `xticks`, and `xmax` address the horizontal value axis, and `ylabel` the vertical category axis.

Examples:

```
>>> from datachart.charts import PyramidChart
>>> figure = PyramidChart(
...     data=[
...         [
...             {"label": "0-14", "y": 12},
...             {"label": "15-29", "y": 18},
...             {"label": "30-44", "y": 22},
...         ],
...         [
...             {"label": "0-14", "y": 11},
...             {"label": "15-29", "y": 19},
...             {"label": "30-44", "y": 24},
...         ],
...     ],
...     subtitle=["Group A", "Group B"],
...     title="Basic Pyramid Chart",
...     show_legend=True,
... )
```

| PARAMETER       | DESCRIPTION                                                                                                                                                                                                                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`          | Exactly two lists of data points — the first is the left side, the second the right. Values are positive for both sides; the chart mirrors the left side itself. **TYPE:** `list[list[BarDataPointAttrs]]`                                                                                    |
| `title`         | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                       |
| `xlabel`        | The label of the horizontal value axis. **TYPE:** \`str                                                                                                                                                                                                                                       |
| `ylabel`        | The label of the vertical category axis. **TYPE:** \`str                                                                                                                                                                                                                                      |
| `subtitle`      | The names of the two sides. Used as legend labels. **TYPE:** \`str                                                                                                                                                                                                                            |
| `figsize`       | The size of the figure as (width, height) in inches. See FIG_SIZE. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                       |
| `xmin`          | Not supported; the value axis is always symmetric around zero. Raises when passed. **TYPE:** \`int                                                                                                                                                                                            |
| `xmax`          | The maximum per-side value; the value axis spans (-xmax, xmax). **TYPE:** \`int                                                                                                                                                                                                               |
| `show_legend`   | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                  |
| `legend`        | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                        |
| `show_grid`     | Which grid lines to show ("both", "x", "y"); False draws none. See SHOW_GRID. **TYPE:** \`SHOW_GRID                                                                                                                                                                                           |
| `show_yerr`     | Whether to show error bars on the bars. **TYPE:** \`bool                                                                                                                                                                                                                                      |
| `show_values`   | Whether to show bar value labels at the edge of each bar. **TYPE:** \`bool                                                                                                                                                                                                                    |
| `value_format`  | Format string for bar value labels: a VALUE_FORMAT constant or any "{x:.1f}", "{:.1f}%", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                       |
| `sort`          | The order the categories are drawn in: None (input order), "ascending", or "descending" by value. One order serves both sides, keyed by the total of the two; ties keep input order. See SORT. **TYPE:** \`SORT                                                                               |
| `sort_by`       | The subtitle of the one side whose values key the sort instead of the total. A category that side lacks sorts last. **TYPE:** \`str                                                                                                                                                           |
| `emphasis_rule` | A one-key dict that highlights the bars matching it and mutes the rest: {"above": v} or {"below": v} (strict), {"between": (lo, hi)} (inclusive), {"top": n} or {"bottom": n}. Reads each bar's positive value; a record's own emphasis key wins over the rule. **TYPE:** \`EmphasisRuleAttrs |
| `style`         | Style configuration(s) for the bars, per side. **TYPE:** \`BarStyleAttrs                                                                                                                                                                                                                      |
| `xticks`        | Custom value-axis tick positions, as positive values; each is mirrored to both halves. **TYPE:** \`list\[int                                                                                                                                                                                  |
| `xticklabels`   | Custom value-axis tick labels (same length as xticks), applied to both mirrored halves. **TYPE:** \`list[str]                                                                                                                                                                                 |
| `xtickrotate`   | Rotation angle for value-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                    |
| `yticks`        | Custom category-axis tick positions. **TYPE:** \`list\[int                                                                                                                                                                                                                                    |
| `yticklabels`   | Custom category-axis tick labels. **TYPE:** \`list[str]                                                                                                                                                                                                                                       |
| `ytickrotate`   | Rotation angle for category-axis tick labels. **TYPE:** \`int                                                                                                                                                                                                                                 |
| `xticks_format` | The x-axis tick label format: a DATE_FORMAT member or strftime pattern on a datetime axis, else a VALUE_FORMAT member or "{x:.1f}" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                     |
| `yticks_format` | The y-axis tick label format, as xticks_format. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                      |
| `vlines`        | Vertical line(s) to plot. **TYPE:** \`VLineSettingAttrs                                                                                                                                                                                                                                       |
| `hlines`        | Horizontal line(s) to plot. **TYPE:** \`HLineSettingAttrs                                                                                                                                                                                                                                     |
| `vspans`        | Vertical reference band(s) to shade, between two x positions. **TYPE:** \`VSpanSettingAttrs                                                                                                                                                                                                   |
| `hspans`        | Horizontal reference band(s) to shade, between two y positions. **TYPE:** \`HSpanSettingAttrs                                                                                                                                                                                                 |
| `texts`         | Text annotation(s) to draw. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                                                                      |
| `label`         | The key name in data for label values (default: "label"). **TYPE:** \`str                                                                                                                                                                                                                     |
| `y`             | The key name in data for the bar values (default: "y"). **TYPE:** \`str                                                                                                                                                                                                                       |
| `yerr`          | The key name in data for the bar error values (default: "yerr"). **TYPE:** \`str                                                                                                                                                                                                              |

| RETURNS      | DESCRIPTION                              |
| ------------ | ---------------------------------------- |
| `plt.Figure` | The figure containing the pyramid chart. |

## Data

Each record in `data` is a [`BarDataPointAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/charts/barchart/#datachart.typings.BarDataPointAttrs); the `label`, `y` and `yerr` parameters rename its keys.

## Style

`style` takes the keys of [`BarStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/charts/barchart/#datachart.typings.BarStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/0.10.2/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/0.10.2/references/config/index.md).

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/0.10.2/references/constants/index.md) that lists its values.

| Parameter                                    | Constant                                                                                                                                                                                                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `figsize`                                    | [`FIG_SIZE`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                      |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.LEGEND_ALIGN) |
| `show_grid`                                  | [`SHOW_GRID`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SHOW_GRID)                                                                                                                                    |
| `value_format`                               | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                              |
| `sort`                                       | [`SORT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.SORT)                                                                                                                                              |
| `xticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.DATE_FORMAT)         |
| `yticks_format`                              | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](https://eriknovak.github.io/datachart/0.10.2/references/constants/#datachart.constants.DATE_FORMAT)         |
