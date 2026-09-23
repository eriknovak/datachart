---
title: HexbinChart
---

# HexbinChart

Point density on the plane, as colored hexagons. The [Hexbin Chart guide](../../how-to-guides/charts/hexbinchart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.HexbinChart
    options:
        heading_level: 3

## Data

Each record in `data` is a [`HexbinDataAttrs`](#datachart.typings.HexbinDataAttrs).

::: datachart.typings.HexbinDataAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`HexbinStyleAttrs`](#datachart.typings.HexbinStyleAttrs). The chart also reads the shared groups it draws: reference lines ([`VLineStyleAttrs`](../typings.md#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](../typings.md#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](../typings.md#datachart.typings.DLineStyleAttrs)), pairwise brackets ([`BracketStyleAttrs`](../typings.md#datachart.typings.BracketStyleAttrs)), reference bands ([`VSpanStyleAttrs`](../typings.md#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](../typings.md#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.HexbinStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `reduce` | [`HEXBIN_REDUCE`](../constants.md#datachart.constants.HEXBIN_REDUCE) |
| `xticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
| `scalex` | [`SCALE`](../constants.md#datachart.constants.SCALE) |
| `scaley` | [`SCALE`](../constants.md#datachart.constants.SCALE) |
| `norm` | [`NORMALIZE`](../constants.md#datachart.constants.NORMALIZE) |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `yticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `colorbar={"location": ..., "format": ..., "orientation": ...}` | [`COLORBAR_LOCATION`](../constants.md#datachart.constants.COLORBAR_LOCATION), [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`ORIENTATION`](../constants.md#datachart.constants.ORIENTATION) |
