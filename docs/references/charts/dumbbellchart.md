---
title: DumbbellChart
---

# DumbbellChart

Two values per category, a dot at each and a connector between them. The [Dumbbell Chart guide](../../how-to-guides/charts/dumbbellchart.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.DumbbellChart
    options:
        heading_level: 3

## Data

Each record in `data` is a [`DumbbellRecordAttrs`](#datachart.typings.DumbbellRecordAttrs); the `emphasis` parameter renames its keys.

::: datachart.typings.DumbbellRecordAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`DumbbellStyleAttrs`](#datachart.typings.DumbbellStyleAttrs). The chart also reads the shared groups it draws: value labels ([`ValueLabelStyleAttrs`](../typings.md#datachart.typings.ValueLabelStyleAttrs)), reference lines ([`VLineStyleAttrs`](../typings.md#datachart.typings.VLineStyleAttrs), [`HLineStyleAttrs`](../typings.md#datachart.typings.HLineStyleAttrs) and [`DLineStyleAttrs`](../typings.md#datachart.typings.DLineStyleAttrs)), pairwise brackets ([`BracketStyleAttrs`](../typings.md#datachart.typings.BracketStyleAttrs)), reference bands ([`VSpanStyleAttrs`](../typings.md#datachart.typings.VSpanStyleAttrs) and [`HSpanStyleAttrs`](../typings.md#datachart.typings.HSpanStyleAttrs)) and text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.DumbbellStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `value_kind` | [`DUMBBELL_VALUE`](../constants.md#datachart.constants.DUMBBELL_VALUE) |
| `sort_by` | [`DUMBBELL_SORT_KEY`](../constants.md#datachart.constants.DUMBBELL_SORT_KEY) |
| `marker` | [`LINE_MARKER`](../constants.md#datachart.constants.LINE_MARKER) |
| `connector_style` | [`LINE_STYLE`](../constants.md#datachart.constants.LINE_STYLE) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `orientation` | [`ORIENTATION`](../constants.md#datachart.constants.ORIENTATION) |
| `scaley` | [`AXIS_SCALE`](../constants.md#datachart.constants.AXIS_SCALE) |
| `legend={"location": ..., "alignment": ...}` | [`LEGEND_LOCATION`](../constants.md#datachart.constants.LEGEND_LOCATION), [`LEGEND_ALIGN`](../constants.md#datachart.constants.LEGEND_ALIGN) |
| `show_grid` | [`SHOW_GRID`](../constants.md#datachart.constants.SHOW_GRID) |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `sort` | [`SORT`](../constants.md#datachart.constants.SORT) |
| `emphasis` | [`EMPHASIS`](../constants.md#datachart.constants.EMPHASIS) |
