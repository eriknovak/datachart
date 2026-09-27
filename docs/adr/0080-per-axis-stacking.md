---
status: accepted
---

# Each value axis of a Panel stacks only its own layers

In a `Panel` with a secondary value axis, stack bottoms, value-label headroom
and the stacked-area zero floor were computed once for the whole panel (issue
#303). A right-axis bar stacked on the left bars' heights, drawn in right-axis
units, so the right axis started at 1000 for bars of height 1 and 2. ADR 0041
already made the two value axes scale independently; a stack that crosses
them adds numbers measured in different units.

## Commitments

- **Stacks pool per resolved value axis.** Bar stack bottoms (ADR 0079),
  histogram stack bottoms (ADR 0014) and stacked-area bands (ADR 0025) each
  accumulate over the layers that twin assignment put on the same axis. A
  right-axis stack starts from zero, or from its own baseline, in right-axis
  units. A single-axis panel is one pool, so it renders as before.
- **What is shared stays shared.** The category axis has no twin, so the
  category index, the histogram bin edges and the bar slot width are still
  computed over the whole panel. Grouped and overlaid bars do not stack and
  are unchanged.
- **Axis furniture that follows a stack follows its axis.** Value-label
  headroom is added to each value axis that carries labelled bars, and the
  zero floor of a `ZERO` or `PERCENT` stack applies on each axis holding a
  stacked area, unless that axis is log.
- **`overlay_warn_scale_groups` gates only its warning.** Automatic axis
  assignment clusters by scale whether or not the warning is on; turning it
  off no longer switches to the sequential first-left placement.

## Considered options

- *Raise on a stack that spans both axes.* Rejected in triage: each side is
  a meaningful stack on its own, and the caller asked for both.
- *Keep one panel-wide stack and draw it on the primary axis.* Rejected: it
  discards the twin assignment the caller or the clustering chose, and puts
  a small series back on a scale where it reads as flat.
