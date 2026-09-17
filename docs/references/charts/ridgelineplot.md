---
title: RidgelinePlot
---

# RidgelinePlot

One density ridge per group, stacked and partly overlapping. The [Ridgeline Plot guide](../../how-to-guides/charts/ridgelineplot.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.RidgelinePlot
    options:
        heading_level: 3

## Data

Each record in `data` is a [`RidgelineDataPointAttrs`](#datachart.typings.RidgelineDataPointAttrs); the `label` and `value` parameters rename its keys.

::: datachart.typings.RidgelineDataPointAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`RidgelineStyleAttrs`](#datachart.typings.RidgelineStyleAttrs). The chart also reads the shared groups it draws: reference lines ([`VLineStyleAttrs`](../typings.md#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](../typings.md#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](../typings.md#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](../typings.md#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.RidgelineStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `normalize` | [`RIDGELINE_SCALE`](../constants.md#datachart.constants.RIDGELINE_SCALE) |
| `emphasis` | [`EMPHASIS`](../constants.md#datachart.constants.EMPHASIS) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
| `orientation` | [`ORIENTATION`](../constants.md#datachart.constants.ORIENTATION) |
| `scaley` | [`SCALE`](../constants.md#datachart.constants.SCALE) |
| `xticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `yticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `bandwidth` | [`BANDWIDTH`](../constants.md#datachart.constants.BANDWIDTH) |
| `inner` | [`VIOLIN_INNER`](../constants.md#datachart.constants.VIOLIN_INNER) |
| `sort` | [`SORT`](../constants.md#datachart.constants.SORT) |
