---
title: CalendarHeatmap
---

# CalendarHeatmap

One colored cell per day, weeks as columns and weekdays as rows. The [Calendar Heatmap guide](../../how-to-guides/charts/calendarheatmap.ipynb) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

::: datachart.charts.CalendarHeatmap
    options:
        heading_level: 3

## Data

Each record in `data` is a [`CalendarHeatmapDataAttrs`](#datachart.typings.CalendarHeatmapDataAttrs).

::: datachart.typings.CalendarHeatmapDataAttrs
    options:
        heading_level: 3

## Style

`style` takes the keys of [`CalendarHeatmapStyleAttrs`](#datachart.typings.CalendarHeatmapStyleAttrs). The chart also reads the shared groups it draws: text annotations ([`TextStyleAttrs`](../typings.md#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](../config.md).

::: datachart.typings.CalendarHeatmapStyleAttrs
    options:
        heading_level: 3

## Constants

The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.

| Parameter | Constant |
| :-- | :-- |
| `week_start` | [`CALENDAR_WEEKDAY`](../constants.md#datachart.constants.CALENDAR_WEEKDAY) |
| `figsize` | [`FIG_SIZE`](../constants.md#datachart.constants.FIG_SIZE) |
| `aspect_ratio` | [`ASPECT_RATIO`](../constants.md#datachart.constants.ASPECT_RATIO) |
| `value_format` | [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT) |
| `norm` | [`COLOR_NORM`](../constants.md#datachart.constants.COLOR_NORM) |
| `colorbar={"location": ..., "format": ..., "orientation": ...}` | [`COLORBAR_LOCATION`](../constants.md#datachart.constants.COLORBAR_LOCATION), [`VALUE_FORMAT`](../constants.md#datachart.constants.VALUE_FORMAT), [`ORIENTATION`](../constants.md#datachart.constants.ORIENTATION) |
