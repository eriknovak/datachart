---
status: accepted
---

# Annotation statistics degrade to nan, and every rule delegates to a library

The `stats` module grew as chart-adjacent scalars (`mean`, `iqr`,
`correlation`) plus two density estimators returning chart-ready shapes.
Adding a second wave of annotation helpers — interval estimates, rank
correlation, shape statistics, binning, smoothers, and a linear fit —
forced three conventions that were previously implicit and contradictory.

## Commitments

- **Degenerate data returns `nan`; malformed input raises.** A helper feeds
  an annotation on a chart that is already being drawn, so failing on a
  short or constant series would abort a figure over a value nobody plots.
  Fewer than two points, zero variance, and an empty list yield `nan`, a
  `(nan, nan)` interval, or a `nan`-filled series. Mismatched `x`/`y`
  lengths, a non-list argument, an unknown bin rule, a non-positive window,
  and an `alpha` or `frac` out of range still raise, because those are
  caller mistakes rather than thin data. This settles the split between
  `mean([])`, which returned `nan`, and `correlation([], [])`, which raised.
- **Statistical rules come from numpy and scipy, never hand-rolled.**
  `histogram` delegates its `bins` to `numpy.histogram_bin_edges`, which
  already implements `auto`, `fd`, `rice`, and the rest; the `auto`/`rice`/
  `fd` names in `contour_levels` (ADR 0022) are a separate rule set over
  grid resolution and stay separate. Spearman, skewness, kurtosis, the
  linear fit, and the bootstrap come from `scipy.stats`, imported lazily
  inside each function as the regression layer does. `loess` is the one
  exception: no dependency ships a LOWESS, and statsmodels is too heavy to
  add for one function, so a tricube-weighted local linear fit is written
  out here.
- **A smoother's return shape follows its own arity.** `rolling_mean` and
  `ewma` take one series and return a `List[float]` of the same length,
  aligned to the input index, `nan` where the window is not yet full.
  `loess` takes `x` and `y` and has no index to align to, so it returns
  `[{x, y}]` points sorted by `x`, the shape `kde1d` already established
  for a curve a `LineChart` can draw. Chart fronts that smooth (#121)
  consume these, so the shapes are fixed here rather than per front.
