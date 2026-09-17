---
status: accepted
---

# Histogram stacking moves to bar_mode; step edges follow the series

Two `HISTOGRAM_TYPE` members did not do what they said. `BAR_STACKED` never
stacked: every histogram series draws through its own `ax.hist` call, and
matplotlib's `"barstacked"` only stacks arrays passed to one call, so the
member rendered identically to `BAR`. `STEP` was invisible under half the
themes: a step histogram is drawn as edge only, and the theme edge defaults
are fill-oriented — white in DEFAULT, width 0 in MATERIAL and MINIMAL.

`HISTOGRAM_TYPE` becomes strictly a per-series *render style* — `BAR`,
`STEP`, `STEP_FILLED` — and *how series share the axis* stays `bar_mode`'s
job, now for histograms too. The Histogram front accepts the `bar_mode`
setting; the `Panel` (owner of every cross-layer concern, ADR 0001)
accumulates per-bin bottoms across its histogram layers on the panel-shared
bin edges and hands each layer its offset through the `DrawContext`, exactly
parallel to bar-chart stack slotting. `BAR_STACKED` is removed, not aliased,
per the pre-1.0 policy of ADR 0010.

For `STEP`, the edge is the series mark itself, so the layer defaults the
edge color to the series cycle color — a theme cannot supply this, since a
fixed theme color would collapse a multi-series step histogram into one
color — and the edge width to the theme's `plot_line_width` (the step
outline is a line-like mark, and the existing key gives every theme control
without new config surface). Explicit per-chart `plot_hist_edge_*` styles
override both; filled types keep the fill-oriented theme edges unchanged.

A `STEP` outline is one open polygon matplotlib runs from zero, up over the
bins, and back down to zero. Two of those drops to zero state nothing the
data says, so the layer rewrites the polygon's vertices as soon as `ax.hist`
returns — for the plain outline only, since `STEP_FILLED` and a stacked slot
are areas and need their baseline to enclose anything at all.

The first is a cumulative view's closing drop. A running total never falls
back, so the vertical fall from the total to zero at the last edge reads as a
collapse to none; it goes, and the outline ends at its total. The opening
rise from zero stays, because a total does start there, and a plain
histogram keeps both closing segments — its fall to zero is a true count.

The second is any drop to zero on a log value axis, which has no zero to land
on: such a vertex is clipped to the axis floor, spiking at every empty bin and
at both ends. Those vertices become NaN, which the renderer draws as a break,
so the outline stops at the last occupied bin and resumes at the next one.
Hover is unaffected: only the value coordinate goes NaN, so a picked gap
vertex still carries its bin coordinate and names its empty bin.

## Considered options

- **Keep `BAR_STACKED` as the stacking trigger.** Rejected: a per-series
  style flag driving a cross-series concern is the incoherence that made it
  silently broken in the first place.
- **Remove stacking entirely.** Rejected: stacked histograms are genuinely
  useful, and the panel already owns the machinery (shared bins, stack
  bottoms for bars).
- **Theme keys for step edges** (e.g. `plot_hist_step_edge_color`).
  Rejected: the color must track the per-series cycle, which themes cannot
  know; a width-only key would duplicate what `plot_line_width` already
  expresses.
- **Run the log outline along the axis floor** instead of breaking it.
  Rejected: the floor is wherever the limits happen to fall, so the outline
  would draw a count that moves with the view.
- **Drop the closing segment of every step outline**, not just a cumulative
  one. Rejected: a plain histogram really does fall to zero past its last
  bin, and hiding that hides an empty tail.
