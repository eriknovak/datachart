---
title: NetworkChart
---

# NetworkChart

Nodes joined by edges, placed by a layout. The [Network Chart guide](../../how-to-guides/charts/networkchart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.NetworkChart
    options:
        heading_level: 3

## Data

`data` is one [`NetworkSingleChartAttrs`](#datachart.typings.NetworkSingleChartAttrs), or a list of them for subplots, with [`NetworkNodeAttrs`](#datachart.typings.NetworkNodeAttrs) and [`NetworkEdgeAttrs`](#datachart.typings.NetworkEdgeAttrs) inside.

::: datachart.typings.NetworkSingleChartAttrs
    options:
        heading_level: 3

::: datachart.typings.NetworkNodeAttrs
    options:
        heading_level: 3

::: datachart.typings.NetworkEdgeAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`NetworkStyleAttrs`](#datachart.typings.NetworkStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](../typings.md#datachart.typings.ValueLabelStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.NetworkStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `layout` | [`NETWORK_LAYOUT`](../constants.md#datachart.constants.NETWORK_LAYOUT) |
| `label_position` | [`NETWORK_LABEL_POSITION`](../constants.md#datachart.constants.NETWORK_LABEL_POSITION) |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
