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
