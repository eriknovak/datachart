---
title: ScatterChart
---

# ScatterChart

One point per observation, placed by two numeric variables. The [Scatter Chart guide](../../how-to-guides/charts/scatterchart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.ScatterChart
    options:
        heading_level: 3

## Data

Each record in `data` is a [`ScatterRecordAttrs`](#datachart.typings.ScatterRecordAttrs); the `emphasis`, `x`, `y`, `size`, `hue`, `annotation`, `xerr` and `yerr` parameters rename its keys.

::: datachart.typings.ScatterRecordAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`ScatterStyleAttrs`](#datachart.typings.ScatterStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](../typings.md#datachart.typings.ValueLabelStyleAttrs)), the regression line ([`RegressionStyleAttrs`](../typings.md#datachart.typings.RegressionStyleAttrs)), reference lines ([`VLineStyleAttrs`](../typings.md#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](../typings.md#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](../typings.md#datachart.typings.DLineStyleAttrs)), pairwise brackets ([`BracketStyleAttrs`](../typings.md#datachart.typings.BracketStyleAttrs)), reference bands ([`VSpanStyleAttrs`](../typings.md#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](../typings.md#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.ScatterStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `xticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |
| `emphasis` | [`EMPHASIS`](../constants.md#datachart.constants.EMPHASIS) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
| `scalex` | [`AXIS_SCALE`](../constants.md#datachart.constants.AXIS_SCALE) |
| `scaley` | [`AXIS_SCALE`](../constants.md#datachart.constants.AXIS_SCALE) |
| `yticks_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`DATE_FORMAT`](../constants.md#datachart.constants.DATE_FORMAT) |

## Composition

Whether the figure composes with each composition function.

| Function | Composes |
| :-- | :-- |
| [`Grid`](../utils/index.md#datachart.utils.Grid) | yes |
| [`Panel`](../utils/index.md#datachart.utils.Panel) | yes |
