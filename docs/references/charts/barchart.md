---
title: BarChart
---

# BarChart

A value per category as bars; series grouped, stacked, or overlaid. The [Bar Chart guide](../../how-to-guides/charts/barchart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.BarChart
    options:
        heading_level: 3

## Data

Each record in `data` is a [`BarDataPointAttrs`](#datachart.typings.BarDataPointAttrs); the `emphasis`, `label`, `y` and `yerr` parameters rename its keys.

::: datachart.typings.BarDataPointAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`BarStyleAttrs`](#datachart.typings.BarStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](../typings.md#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](../typings.md#datachart.typings.VLineStyleAttrs) and [`HLineStyleAttrs`](../typings.md#datachart.typings.HLineStyleAttrs)), reference bands ([`VSpanStyleAttrs`](../typings.md#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](../typings.md#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.BarStyleAttrs
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
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
| `orientation` | [`ORIENTATION`](../constants.md#datachart.constants.ORIENTATION) |
| `bar_mode` | [`BAR_MODE`](../constants.md#datachart.constants.BAR_MODE) |
| `sort` | [`SORT`](../constants.md#datachart.constants.SORT) |
| `scalex` | [`SCALE`](../constants.md#datachart.constants.SCALE) |
| `scaley` | [`SCALE`](../constants.md#datachart.constants.SCALE) |
| `xticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `yticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
