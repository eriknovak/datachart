---
status: accepted
---

# RaincloudPlot assembles the violin, swarm, and box layers with per-layer offsets

A raincloud (issue #63; PtitPrince) is a half violin, a strip of raw points,
and a box at each category. Every part already exists as a layer (ADR 0001,
0019, 0020), and ADR 0020 reserved side offsets as "a per-layer property set
by that front, not panel slotting". The alternative — a fourth `RaincloudLayer`
that redraws all three — would fork three drawing paths.

## Commitments

- **A chart type, not a composition front.** `build_layers("raincloudplot")`
  yields `[ViolinLayer, SwarmLayer, BoxLayer]` per dataset and the figure
  renders through `render_chart` like every other front, so subplots, figure
  labels, and the `_chart_metadata` transport come for free and the figure
  composes in `Panel`/`Grid`. The public `Panel()` is not the entry point:
  the sibling fronts expose no offsets, and the figure would carry
  `type: "overlay"`.
- **Offsets are layer settings with fixed values.** `ViolinLayer` gains a
  `side` setting (the clipping `split` already does); `SwarmLayer` and
  `BoxLayer` gain a category offset and, for the swarm, a spread. The
  raincloud front sets them from constants in `layers.py`: the cloud keeps the
  full body width on one side, the box is the rain-side half of a ≈ 0.15 wide
  box on the cloud's seam, the rain starts right past the box and packs
  one-sided, away from the box, over ≈ 0.16. No user knob in v1.
- **Cloud left when vertical, above when horizontal.** The rain and box take
  the opposite side. The horizontal case follows the raincloud paper's layout.
- **The box is a half outline between the cloud and the rain.** Clipped to
  the rain's side of its center, so the three parts never overlap. No fill;
  edges, median, whiskers, and caps in the theme font color; outliers on by default as
  circles (`show_outliers=True`). The cloud draws with `inner=None`.
- **Per-group colors.** A `color_by_group` layer setting, turned on by the
  raincloud front only, makes the violin and swarm layers cycle the multiple
  palette per label instead of taking one `ctx.color`; the legend lists one
  entry per group. The sibling fronts keep one color per dataset.
- **Front surface.** `RaincloudPlot` takes the `SwarmPlot` common parameters
  plus `mode`/`jitter` (rain), `bandwidth` (cloud), and `show_outliers`
  (box); `orientation` defaults to vertical like the siblings. Cut:
  `inner`, `show_notch`, `split`, a public `side` on `ViolinPlot`.
- **One flat style dict, no new theme keys.** `RaincloudStyleAttrs` is the
  union of `plot_violin_*`, `plot_swarm_*`, and `plot_box_*`, each key routed
  to its layer. No constant is introduced; `SWARM_MODE` and `BANDWIDTH` are
  reused.
- **Emphasis per group**, applied to all three parts of the group together.
