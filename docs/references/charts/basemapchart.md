---
title: BasemapChart
---

# BasemapChart

Coastlines, land, borders and lakes under a chart of longitude and latitude. The [Basemap Chart guide](../../how-to-guides/charts/basemapchart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.BasemapChart
    options:
        heading_level: 3

## Data

Each record in `geometry` is a [`BasemapDataAttrs`](#datachart.typings.BasemapDataAttrs).

::: datachart.typings.BasemapDataAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`BasemapStyleAttrs`](#datachart.typings.BasemapStyleAttrs). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.BasemapStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `features` | [`BASEMAP_FEATURE`](../constants.md#datachart.constants.BASEMAP_FEATURE) |
| `position` | [`DRAW_POSITION`](../constants.md#datachart.constants.DRAW_POSITION) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
