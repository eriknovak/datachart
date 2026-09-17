---
title: Heatmap
---

# Heatmap

A two-dimensional matrix as colored cells. The [Heatmap guide](../../how-to-guides/charts/heatmap.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.Heatmap
    options:
        heading_level: 3

## Data

Each record in `data` is a [`HeatmapDataAttrs`](#datachart.typings.HeatmapDataAttrs); the `emphasis` parameter renames its keys.

::: datachart.typings.HeatmapDataAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`HeatmapStyleAttrs`](#datachart.typings.HeatmapStyleAttrs). The chart also reads the shared groups it draws: text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.HeatmapStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
| `norm` | [`NORMALIZE`](../constants.md#datachart.constants.NORMALIZE) |
| `valfmt` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `xticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `yticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `colorbar={"location": ..., "format": ..., "orientation": ...}` | [`COLORBAR_LOCATION`](../constants.md#datachart.constants.COLORBAR_LOCATION), [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`ORIENTATION`](../constants.md#datachart.constants.ORIENTATION) |
