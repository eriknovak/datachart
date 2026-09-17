---
title: StackedAreaChart
---

# StackedAreaChart

Parts of a total along an ordered axis, filled on top of each other. The [Stacked Area Chart guide](../../how-to-guides/charts/stackedareachart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.StackedAreaChart
    options:
        heading_level: 3

## Data

Each record in `data` is a [`LineDataPointAttrs`](linechart.md#datachart.typings.LineDataPointAttrs); the `x` and `y` parameters rename its keys.

## Style

`style` takes the keys of [`StackedAreaStyleAttrs`](#datachart.typings.StackedAreaStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](../typings.md#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](../typings.md#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](../typings.md#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](../typings.md#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](../typings.md#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.StackedAreaStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `baseline` | [`STACKED_AREA_BASELINE`](../constants.md#datachart.constants.STACKED_AREA_BASELINE) |
| `emphasis` | [`EMPHASIS`](../constants.md#datachart.constants.EMPHASIS) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
| `scalex` | [`SCALE`](../constants.md#datachart.constants.SCALE) |
| `scaley` | [`SCALE`](../constants.md#datachart.constants.SCALE) |
| `xticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `yticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
