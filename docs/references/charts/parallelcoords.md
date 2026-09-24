---
title: ParallelCoords
---

# ParallelCoords

Each record as a polyline across one axis per dimension. The [Parallel Coordinates guide](../../how-to-guides/charts/parallelcoords.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.ParallelCoords
    options:
        heading_level: 3

## Data

Each record in `data` is a [`ParallelCoordsDataPointAttrs`](#datachart.typings.ParallelCoordsDataPointAttrs); the `hue` parameter renames its keys.

::: datachart.typings.ParallelCoordsDataPointAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`ParallelCoordsStyleAttrs`](#datachart.typings.ParallelCoordsStyleAttrs). The chart also reads the shared groups it draws: text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.ParallelCoordsStyleAttrs
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
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |

## Composition

Whether the figure composes with each composition function.

| Function | Composes |
| :-- | :-- |
| [`Grid`](../utils/index.md#datachart.utils.Grid) | yes |
| [`Panel`](../utils/index.md#datachart.utils.Panel) | yes |
