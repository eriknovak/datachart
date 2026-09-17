---
title: Treemap
---

# Treemap

Part-of-whole data as nested rectangles sized by value. The [Treemap guide](../../how-to-guides/charts/treemap.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.Treemap
    options:
        heading_level: 3

## Data

`data` is one [`TreemapSingleChartAttrs`](#datachart.typings.TreemapSingleChartAttrs), or a list of them for subplots, with [`TreemapRecordAttrs`](#datachart.typings.TreemapRecordAttrs) inside.

::: datachart.typings.TreemapSingleChartAttrs
    options:
        heading_level: 3

::: datachart.typings.TreemapRecordAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`TreemapStyleAttrs`](#datachart.typings.TreemapStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](../typings.md#datachart.typings.ValueLabelStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.TreemapStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
