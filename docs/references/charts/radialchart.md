---
title: RadialChart
---

# RadialChart

Series on polar axes, as a radar line, an area, bars, or a histogram. The [Radial Chart guide](../../how-to-guides/charts/radialchart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.RadialChart
    options:
        heading_level: 3

## Data

Each record in `data` is a [`RadialRecordAttrs`](#datachart.typings.RadialRecordAttrs); the `label`, `x`, `y` and `yerr` parameters rename its keys.

::: datachart.typings.RadialRecordAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`LineStyleAttrs`](linechart.md#datachart.typings.LineStyleAttrs), [`BarStyleAttrs`](barchart.md#datachart.typings.BarStyleAttrs), [`HistStyleAttrs`](histogram.md#datachart.typings.HistStyleAttrs) and [`ScatterStyleAttrs`](scatterchart.md#datachart.typings.ScatterStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](../typings.md#datachart.typings.ValueLabelStyleAttrs)), the area fill ([`AreaStyleAttrs`](../typings.md#datachart.typings.AreaStyleAttrs)), reference lines ([`VLineStyleAttrs`](../typings.md#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](../typings.md#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](../typings.md#datachart.typings.DLineStyleAttrs)), pairwise brackets ([`BracketStyleAttrs`](../typings.md#datachart.typings.BracketStyleAttrs)), reference bands ([`VSpanStyleAttrs`](../typings.md#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](../typings.md#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `mark` | [`RADIAL_TYPE`](../constants.md#datachart.constants.RADIAL_TYPE) |
| `direction` | [`RADIAL_DIRECTION`](../constants.md#datachart.constants.RADIAL_DIRECTION) |
| `emphasis` | [`EMPHASIS`](../constants.md#datachart.constants.EMPHASIS) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `bar_mode` | [`BAR_MODE`](../constants.md#datachart.constants.BAR_MODE) |
| `sort` | [`SORT`](../constants.md#datachart.constants.SORT) |
| `scaley` | [`AXIS_SCALE`](../constants.md#datachart.constants.AXIS_SCALE) |

## Composition

Whether the figure composes with each composition function.

| Function | Composes |
| :-- | :-- |
| [`Grid`](../utils/index.md#datachart.utils.Grid) | yes |
| [`Panel`](../utils/index.md#datachart.utils.Panel) | yes |
