---
title: ScatterMatrix
---

# ScatterMatrix

A scatter chart for every pair of dimensions, distributions on the diagonal. The [Scatter Matrix guide](../../how-to-guides/charts/scattermatrix.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.ScatterMatrix
    options:
        heading_level: 3

## Data

Each record in `data` is a [`ScatterMatrixDataPointAttrs`](#datachart.typings.ScatterMatrixDataPointAttrs); the `hue` parameter renames its keys.

::: datachart.typings.ScatterMatrixDataPointAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`StyleAttrs`](../typings.md#datachart.typings.StyleAttrs). Its own keys are those of [`ScatterMatrixStyleAttrs`](#datachart.typings.ScatterMatrixStyleAttrs). The chart also reads the shared groups it draws: the regression line ([`RegressionStyleAttrs`](../typings.md#datachart.typings.RegressionStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.ScatterMatrixStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `diagonal` | [`SCATTER_MATRIX_DIAGONAL`](../constants.md#datachart.constants.SCATTER_MATRIX_DIAGONAL) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
