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
- **The bar stops at the edge of its marker.** A marker draws translucent, so
  a bar run through it shows as a darker cross over the face. Each side is its
  own marker-less patch from the point outward, shrunk by the marker's radius
  in points — the same shrink the network chart stops an edge with at a node —
  so the gap holds whatever the axes, the figure size or a bubble's own size
  do afterwards. The patches sit a z-step under the markers, so hover and
  emphasis keep addressing the scatter artists. Emphasis dims the bar with its
  point rather than hiding it, so the picture stays stable under hover.
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

**One `errorbar` artist per axis, drawn under the markers** was rejected. It is
a single call and matplotlib's own default, but the bar crosses the marker and
a translucent face lets it through. **Masking it with an opaque disc under the
marker** was rejected with it: it hides the bar, but the marker then stops
blending with whatever it overlaps.
