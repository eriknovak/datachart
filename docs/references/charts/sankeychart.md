---
title: SankeyChart
---

# SankeyChart

Weighted flows between categories, as ribbons between node columns. The [Sankey Chart guide](../../how-to-guides/charts/sankeychart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.SankeyChart
    options:
        heading_level: 3

## Data

`data` is one [`SankeySingleChartAttrs`](#datachart.typings.SankeySingleChartAttrs), or a list of them for subplots, with [`SankeyLinkAttrs`](#datachart.typings.SankeyLinkAttrs) inside.

::: datachart.typings.SankeySingleChartAttrs
    options:
        heading_level: 3

::: datachart.typings.SankeyLinkAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`SankeyStyleAttrs`](#datachart.typings.SankeyStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](../typings.md#datachart.typings.ValueLabelStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.SankeyStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
