---
title: RaincloudPlot
---

# RaincloudPlot

A half violin, the raw points, and a box per group. The [Raincloud Plot guide](../../how-to-guides/charts/raincloudplot.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.RaincloudPlot
    options:
        heading_level: 3

## Data

Each record in `data` is a [`RaincloudDataPointAttrs`](#datachart.typings.RaincloudDataPointAttrs); the `label` and `value` parameters rename its keys.

::: datachart.typings.RaincloudDataPointAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`RaincloudStyleAttrs`](#datachart.typings.RaincloudStyleAttrs). RaincloudStyleAttrs is the union of [`ViolinStyleAttrs`](violinplot.md#datachart.typings.ViolinStyleAttrs), [`SwarmStyleAttrs`](swarmplot.md#datachart.typings.SwarmStyleAttrs) and [`BoxStyleAttrs`](boxplot.md#datachart.typings.BoxStyleAttrs), one per part of the chart. The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](../typings.md#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](../typings.md#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](../typings.md#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](../typings.md#datachart.typings.DLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](../typings.md#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](../typings.md#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.RaincloudStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `emphasis` | [`EMPHASIS`](../constants.md#datachart.constants.EMPHASIS) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `mode` | [`SWARM_MODE`](../constants.md#datachart.constants.SWARM_MODE) |
| `bandwidth` | [`BANDWIDTH`](../constants.md#datachart.constants.BANDWIDTH) |
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
| `orientation` | [`ORIENTATION`](../constants.md#datachart.constants.ORIENTATION) |
| `scaley` | [`SCALE`](../constants.md#datachart.constants.SCALE) |
| `xticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `yticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
