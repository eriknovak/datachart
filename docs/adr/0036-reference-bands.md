---
status: accepted
---

# A reference band is a span type per axis, drawn over the grid and under the marks

Fronts accept `vlines` and `hlines` for reference lines. There is no way to
shade a region — a confidence interval, a recession period, an acceptable
range — without dropping to matplotlib and losing composition with it.

Reference lines resolve their style at build in `_resolve_ref_lines` and draw
from the panel in `_draw_ref_lines`, after scales and limits are set. Bands
take the same seam, so a banded figure survives `Panel` and `Grid` for free.

## Commitments

- **Two span types, not one.** `VSpanPlotAttrs` carries `xmin` and `xmax`,
  `HSpanPlotAttrs` carries `ymin` and `ymax`, with `VSpanStyleAttrs` and
  `HSpanStyleAttrs` beside them. Reference lines are already split this way,
  down to separate style types and separate theme key families, and a single
  type carrying either pair would make the wrong fields typable on both.
- **An omitted bound falls back to the axis limit.** `vlines` already defaults
  `ymin` and `ymax` to the current limits, so `xmin` alone reads as "from here
  to the right edge" — which is what an above-threshold band wants. At least
  one bound is required; a span with neither is a mistake, not a full-axes
  tint, and raises `ValueError` from `validate.py`.
- **The band draws over the grid and under the marks**, at zorder 1.75 against
  gridlines at 1.5, with `plot_vspan_alpha` 0.25 so the gridlines read through
  it. The band is one translucent wash over the furniture rather than a
  background the grid floats on. `plot_vspan_color` defaults to `None` and
  resolves to the muted grey, so an unstyled band sits behind the data without
  competing with the color cycle.
- **`plot_{v,h}span_zorder` is a theme key**, the first zorder any theme can
  set. Every other zorder in the package is computed — from the stacking order
  of a group, or from an emphasis role — and stays that way. This one is
  exposed because moving a band in front of the data is a legitimate thing to
  want and there is no other handle for it.
- **Hatch pairs with an edge.** `plot_{v,h}span_hatch` gains
  `plot_{v,h}span_edge_color` and `plot_{v,h}span_edge_width` alongside it.
  matplotlib draws a hatch in the patch edge color, and every existing hatch
  key already pairs with one — `plot_bar_hatch` with `plot_bar_edge_color`,
  `plot_hist_hatch` with `plot_hist_edge_color`. Without the pair a themed
  hatch would render in the matplotlib default.
- **RadialChart takes bands although it rejects reference lines.** ADR 0015
  raises on `vlines` and `hlines` there because a straight line across a polar
  axes is geometrically meaningless. A band is not: `vspans` is an angular
  wedge bounded in theta over the full radius, `hspans` an annulus bounded in
  radius over the full circle. Both draw with `fill_between`, because
  `axvspan` and `axhspan` measure their perpendicular extent in axes fractions
  and go wrong on a polar axes.
- **Radial bounds are degrees.** `RadialLayer` states its contract as "angles
  are degrees in, radians internally", and `RadialHistogramLayer` already
  takes degree edges. Degrees also survive a continuous radial axis, which is
  under consideration and would have no categories to index.
- **The panel draws bands on the host axes**, the same target
  `_draw_ref_lines` uses. A twin axes renders entirely above its host, so a
  band on the host sits under both axes' marks, which is where a background
  band belongs.
- **A `label` puts the band in the legend** as a patch handle, through the
  same `get_legend_handles_labels` path reference lines use.

## Considered options

**One `SpanPlotAttrs` for both axes** was rejected. It reads as the smaller
API, but it breaks the symmetry with the reference lines the bands sit beside
and it types `ymin` onto a vertical span.

**Category-index bounds on radial** was rejected. ADR 0020 chose category
index for swarm placement, so the precedent exists, but it would make `vspans`
mean one thing under a categorical radial chart and another under a radial
histogram, which has no categories at all.

**Drawing the band under the grid** was rejected. It is the simpler stacking
rule and needs no alpha to stay legible, but the gridlines then sit on top of
the band and the figure reads as two separate surfaces.
