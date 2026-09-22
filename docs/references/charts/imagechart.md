---
title: ImageChart
---

# ImageChart

A picture in data coordinates, under or over the other charts. The [Image Chart guide](../../how-to-guides/charts/imagechart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.ImageChart
    options:
        heading_level: 3

## Data

Each record in `data` is a [`ImageDataAttrs`](#datachart.typings.ImageDataAttrs).

::: datachart.typings.ImageDataAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`ImageStyleAttrs`](#datachart.typings.ImageStyleAttrs). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.ImageStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `position` | [`IMAGE_POSITION`](../constants.md#datachart.constants.IMAGE_POSITION) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
