---
status: accepted
---

# Scatter error bars are distances drawn in the point's colour

`LineChart`, `BarChart`, and `RadialChart` points take `yerr`; scatter points
take `size`, `hue`, `label`, and `emphasis` and nothing for uncertainty.
Benchmark scores with confidence intervals, measurements uncertain in both
variables, and effect sizes with intervals are all scatter figures, and a
second series cannot fake the bar (#248).

## Commitments

- **`xerr` and `yerr` are distances, not bounds.** A number reaches the same
  distance both ways; a `[low, high]` pair reaches `low` below and `high`
  above. This is what matplotlib's `errorbar` takes and what the line and bar
  fronts already mean by `yerr`, so one word means one thing across the
  package. A confidence interval reported as endpoints is the user's
  subtraction; a bounds helper can come later without changing the key.
- **The bar takes the point's resolved colour.** `plot_scatter_error_color`
  defaults to `None`, which follows the point, so a hue group's bars match its
  markers and a composed panel keeps its series apart. The bar chart's fixed
  `plot_bar_error_color` exists because a bar's fill is already its colour and
  the whisker needs contrast against it; a scatter marker is small, and a bar
  in a foreign colour reads as a second series. Width and capsize have their
  own keys so a theme can thin or cap them.
- **The bar is a second artist with no marker of its own.** Drawn with
  `ax.errorbar(fmt="none")` one z-step under the scatter collection, so hover
  and emphasis keep addressing the scatter artists and the bar never occludes
  the marker. Emphasis dims the bar with its point rather than hiding it, so
  the picture stays stable under hover.
- **Scatter only.** `ScatterMatrix`, hexbin, and contour layers ignore the
  keys: a matrix cell has no room for bars and the raster layers aggregate
  the points away.

## Considered options

**Pairs as absolute bounds** was rejected. It reads naturally for a reported
interval but makes `yerr` mean two different things on two fronts, and a
symmetric number would still have to be a distance.

**Hiding a dimmed point's bars** was rejected. Emphasis is meant to be
readable while hovering; bars that vanish and return move the eye more than
bars that fade.
