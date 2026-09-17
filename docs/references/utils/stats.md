---
title: Stats Module
---

# Stats Module

::: datachart.utils.stats
    options:
        members: False
        heading_level: 2

## Choosing a Function

Every function takes plain Python lists and returns a number, a pair, or lists ready to feed back into a chart. The groups below match the [Statistics guide](../../how-to-guides/utility/stats.ipynb), which shows each one on a chart.

| I want to…                                     | Use |
| :--------------------------------------------- | :-- |
| a center, count, or total                      | [`mean`](#datachart.utils.stats.mean), [`median`](#datachart.utils.stats.median), [`mode`](#datachart.utils.stats.mode), [`count`](#datachart.utils.stats.count), [`sum_values`](#datachart.utils.stats.sum_values) |
| how far the values spread                      | [`stdev`](#datachart.utils.stats.stdev), [`variance`](#datachart.utils.stats.variance), [`quantile`](#datachart.utils.stats.quantile), [`iqr`](#datachart.utils.stats.iqr), [`minimum`](#datachart.utils.stats.minimum), [`maximum`](#datachart.utils.stats.maximum) |
| the shape of a distribution                    | [`skewness`](#datachart.utils.stats.skewness), [`kurtosis`](#datachart.utils.stats.kurtosis) |
| how two variables move together                | [`correlation`](#datachart.utils.stats.correlation), [`spearman`](#datachart.utils.stats.spearman) |
| a trend line                                   | [`linear_fit`](#datachart.utils.stats.linear_fit) |
| an interval around a statistic                 | [`bootstrap_ci`](#datachart.utils.stats.bootstrap_ci) |
| bins for a histogram                           | [`histogram`](#datachart.utils.stats.histogram) |
| a smoothed series                              | [`rolling_mean`](#datachart.utils.stats.rolling_mean), [`ewma`](#datachart.utils.stats.ewma), [`loess`](#datachart.utils.stats.loess) |
| a density curve or surface                     | [`kde1d`](#datachart.utils.stats.kde1d), [`kde2d`](#datachart.utils.stats.kde2d) |

## Center

::: datachart.utils.stats.count
::: datachart.utils.stats.sum_values
::: datachart.utils.stats.mean
::: datachart.utils.stats.median
::: datachart.utils.stats.mode

## Spread

::: datachart.utils.stats.stdev
::: datachart.utils.stats.variance
::: datachart.utils.stats.quantile
::: datachart.utils.stats.iqr
::: datachart.utils.stats.minimum
::: datachart.utils.stats.maximum

## Shape

::: datachart.utils.stats.skewness
::: datachart.utils.stats.kurtosis

## Association

::: datachart.utils.stats.correlation
::: datachart.utils.stats.spearman

## Trend Line

::: datachart.utils.stats.linear_fit

## Confidence Intervals

::: datachart.utils.stats.bootstrap_ci

## Binning

::: datachart.utils.stats.histogram

## Smoothing

::: datachart.utils.stats.rolling_mean
::: datachart.utils.stats.ewma
::: datachart.utils.stats.loess

## Density Estimates

::: datachart.utils.stats.kde1d
::: datachart.utils.stats.kde2d
