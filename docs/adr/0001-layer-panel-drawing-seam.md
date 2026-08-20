---
status: accepted
---

# One Layer/Panel drawing seam; style resolved at construction

Drawing was implemented three times (`plot_engine` plot functions, `overlay`'s
`_plot_*_on_axis` copies, `figure.py`'s direct `CHART_PLOTTERS` calls plus private
overlay imports), and they drifted — z-order, legend labels, and bar modes existed
only in the overlay copy, and overlaid single-series bar charts collided at
identical x positions. We collapse all drawing behind one internal seam: a Layer
class per chart type with `draw(ax, ctx)`, and a Panel owning every cross-layer
concern (color assignment, bar slotting, scales, limits, legend, twin axes).

## Commitments

- **Style is resolved when a layer is built**, not at draw time. Layers never read
  the global `config` while drawing, so composition needs no save/overwrite/restore
  of the config singleton and no config snapshots.
- **The metadata transport carries Layer objects and panel settings.** The old
  raw-dict format and its reconstruction fallback in `figure.py` are deleted; both
  writer and reader ship in the same package, so cross-format figures cannot occur
  in-process.
- **Layers are sibling-blind.** Anything requiring knowledge of other layers
  (bar group offsets, color cycles, axis clustering) is a Panel job, passed down
  via a frozen DrawContext.
- **`draw` takes a `plt.Axes` directly.** No drawing port/backend abstraction:
  there is one adapter (matplotlib) and no second in sight.
- **Known output changes are accepted as fixes**, not regressions: overlaid bar
  charts gain proper group offsets (previously fully overlapping), bar grouping
  counts bars across all layers in a panel, and `bar_mode` (stack/overlay) becomes
  available outside `OverlayChart`.

## Considered options

A class per complex chart combination (LineBarChart, …) was rejected: combinations
grow combinatorially, while layering grows linearly along exactly two axes —
same coordinate space (Panel) and different coordinate space (grid placement).
