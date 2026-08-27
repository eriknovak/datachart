---
status: accepted
---

# StackedAreaChart stacks series over an ordered axis with a panel-computed baseline

A stacked area chart (issue #64) shows how a total splits into parts along an
ordered axis — class proportions over time, traffic by channel per year. It
takes `LineChart`'s multi-series input and fills each series on top of the
previous one, like matplotlib's `stackplot`.

## Commitments

- **Input is a list of series, each a list of `{x, y}` points**, exactly
  `LineChart`'s multi-series shape (`x`/`y` key renames included). Every
  series must carry the same `x` values in the same order; ragged input
  raises `ValueError` rather than aligning on a union — stacking over
  silently zero-filled gaps misleads.
- **`baseline` is the only stacking knob**, a `BASELINE` constant: `ZERO`
  (default), `PERCENT` (each `x` normalised to 100 %), `SYM` (centred on
  zero), `WIGGLE`, `WEIGHTED_WIGGLE`. There is no separate `normalize` flag;
  a fifth baseline value keeps the parameter space one-dimensional.
- **Stacking is a panel concern, like bar slotting.** `Panel.render`
  collects every stacked-area layer in the panel, validates shared `x`,
  computes the first-layer offset for the baseline and the cumulative tops,
  and hands each layer its `(bottom, top)` band through a frozen
  `DrawContext` record; the layer only calls `fill_between`. Stacked areas
  always stack — `bar_mode` does not apply to them. `baseline` is a panel
  setting; in `Panel` composition the first figure's value wins, mirroring
  `bar_mode`. Other layer kinds overlay the stack normally.
- **Axis limits follow the baseline.** `x` is tightened to the data like
  `LineChart`; for `ZERO` and `PERCENT` the y-axis bottom is pinned to 0 (no
  autoscale margin below the stack), as bars do. `SYM` and the wiggles keep
  the default margins.
- **`subplots=True` unstacks**: one single-series area per subplot, drawn
  from the singular palette, bottom pinned to 0.
- **Style reuses the area and line keys.** The fill takes `plot_area_*`
  (color, hatch, zorder) with its own `plot_stackedarea_alpha` (0.8 — the
  0.25 of `plot_area_alpha` is tuned for a band under a line and washes out
  when stacked); the optional outline takes `plot_line_*`, switched by
  `plot_stackedarea_outline` (`False`). Both new keys live in `BASE_THEME`
  only; no sibling theme overrides them.
- **Series order is stack order.** The first series sits at the bottom; the
  legend lists bottom→top in input order, with no reversal.
- **`emphasis` roles apply** through the shared muting path: non-highlighted
  bands take the muted alpha, like lines.

## Considered options

- *`normalize=True` next to `baseline`.* Rejected: it only combines with
  `ZERO`, so users would have to learn which pairs are valid; `PERCENT` as a
  baseline value has no invalid combinations.
- *`show_stack` mode on `LineChart`.* Rejected: stacking changes what `y`
  means for every series and needs cross-layer offsets; a front whose name
  says so is clearer than a mode that silently rewrites the data.
- *Aligning ragged `x` on the union with zeros.* Rejected: a missing
  observation is not a zero share.
- *Reusing `plot_area_alpha` unchanged.* Rejected after the design preview:
  stacked bands at 0.25 are unreadable.
