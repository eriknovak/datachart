---
status: accepted
---

# SwarmPlot aligns with boxes through a panel category index, not bar slots

`SwarmPlot` (issue #62) draws raw observations per group and is meant to be
overlaid on `BoxPlot` (and later `ViolinChart`, #61; `RaincloudChart`, #63).
Alignment needs one source of truth for group positions, and the obvious
candidate — the panel's bar slotting — dodges layers side by side, which is
the opposite of what a box + swarm overlay wants.

## Commitments

- **Category index in the panel.** The panel builds one label → position map
  (first-seen union across box/swarm layers), passes it via `DrawContext`,
  and sets category ticks once. `BoxLayer` is retrofitted to consume it and
  stops placing groups and ticks itself.
- **Overlay, never dodge.** Group-oriented layers all sit at the category
  center; multiple swarm layers overlay in distinct colors. Raincloud-style
  side offsets are a per-layer property set by that front, not panel slotting.
- **Beeswarm is pixel-accurate at draw time.** Offsets are computed in display
  space from the marker diameter after autoscaling, then clamped to ±0.4 of
  the category width — like seaborn, and unlike a size-blind data-space packing
  that drifts with figure size. Limits changed after draw can shift spacing
  slightly; documented, accepted.
- **Strip jitter is deterministic.** `jitter` is a fraction of the category
  width (default 0.4) with a fixed internal seed; no `seed` parameter in v1.
- **Own style family.** `plot_swarm_*` keys (color, alpha, size, marker,
  edge width/color, zorder) in every theme, so swarm points can be tuned
  apart from scatter marks.
- **Swarm draws above boxes.** `plot_swarm_zorder` sits above the box
  z-order in every theme so points stay legible over box fills and lines;
  a muted-box look is reached with `emphasis="background"` on the `BoxPlot`
  figure inside the `Panel`, not by a special overlay mode.
- **Per-group emphasis**, aligned with the group labels like `BoxPlot`, so
  an overlay can mute the same groups in both layers.
