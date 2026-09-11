# Smoothing and trend settings on chart fronts

Chart fronts do not smooth or fit their own data. There is no `smooth`
setting, no `SMOOTHING` constant, and no `show_trend` on `LineChart`. The
`stats` module computes the smoothed or fitted series and the caller draws it
as another series — either as one more dataset of the same chart, or as its
own figure composed through `Panel`.

## Why this is out of scope

`datachart` already has both halves of the feature, and they compose without
new API. The smoothers keep the caller's index, so they draw as extra series
of one chart:

```python
series = {
    "daily sales": daily_sales,
    "rolling mean (7 days)": rolling_mean(daily_sales, window=7),
    "EWMA (alpha 0.2)": ewma(daily_sales, alpha=0.2),
}
LineChart(
    data=[[{"x": d, "y": v} for d, v in enumerate(vs)] for vs in series.values()],
    subtitle=list(series),
)
```

When the raw series should recede behind the smoothed one, that is what
emphasis is for (ADR 0009) — the muted look a `smooth` setting would have
hardcoded:

```python
Panel([
    LineChart(raw, emphasis="background"),
    LineChart(smoothed),
])
```

`loess` returns `{x, y}` points rather than an index-aligned series, so it
goes straight into a `LineChart` over the raw points, and `linear_fit` gives
the slope and intercept of a two-point line. A `smooth=` or `show_trend=`
setting would therefore buy one line of typing in exchange for a four-value
constant, three smoother parameters, a second style key family, and a
per-front decision about legend labels and colors on every chart that draws
series.

The one part no caller can reproduce is the confidence band around a fitted
line: it needs a per-x prediction standard error, and `bootstrap_ci`
resamples a single series' statistic instead. That band is deliberately left
to `ScatterChart`, where `show_regression` and `show_ci` already live. On a
line chart the band idiom is taken: `show_yerr` fills per-point error in the
series color, and a second translucent fill in the same color reads as a
third tone rather than a second meaning. A line chart keeps one band.

Reopening this would need a reason the composition recipe cannot serve — a
band whose meaning is unambiguous next to `show_yerr`, or a smoother that
cannot be expressed as a series.

## Prior requests

- #121 — "feat(linechart): trend line and smoothing"
