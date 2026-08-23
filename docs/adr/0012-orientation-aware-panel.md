---
status: accepted
---

# A Panel has an orientation, inferred from its layers, and its value axis follows it

`Panel` renders every coordinate space in the vertical frame: the secondary axis
is always `twinx()`, auto axis assignment clusters on each group's *y* range,
`ylabel_*`/`ymin*`/`ymax*` always address the y-axis, and bar category ticks are
the only thing that swaps for `ORIENTATION.HORIZONTAL`. A panel of horizontal
bars therefore twins the *category* axis, a line overlaid on horizontal bars
must be built with its data transposed by hand, and a horizontal bar chart next
to a vertical one draws both into one frame without a word. We make orientation
a property of the panel.

## Commitments

- **Orientation is inferred, never passed.** A panel is horizontal when every
  orientable layer it holds (bar, histogram, box) is horizontal, vertical
  otherwise. Line, scatter and parallel-coords layers carry no orientation and
  follow the panel. `Panel` gains no `orientation` parameter.
- **Mixed orientations are an error.** Orientable layers of both orientations in
  one panel raise `ValueError`, in the same place and spirit as the
  "multiple box plot datasets require `subplots=True`" check. One coordinate
  space, one orientation.
- **Value axis and category axis.** The vocabulary is *value axis* (the axis
  carrying the quantities: y in a vertical panel, x in a horizontal one) and
  *category axis* (the other one). The secondary axis is always a second value
  axis: `twinx()` in a vertical panel, `twiny()` in a horizontal one. Auto
  assignment clusters on value ranges; legend suffixes stay `(L)`/`(R)` for a
  vertical panel and become `(B)`/`(T)` for a horizontal one.
- **Parameter names keep their spelling, the value axis keeps the meaning.**
  Per-figure `"y_axis"` (`"left"`/`"right"`), `ylabel_left`/`ylabel_right`,
  `ymin`/`ymax` and `ymin_right`/`ymax_right` address the primary/secondary
  value axis in either orientation; `xlabel`, `xmin`/`xmax` address the
  category axis. In a horizontal panel `"left"` means the bottom value axis and
  `"right"` the top one. The swap is documented in the `Panel` docstring and the
  Panel guide; no `x_axis`/`xlabel_top`-style twins are added.
- **Lines and scatters transpose with the panel.** In a horizontal panel a line
  or scatter layer draws its `x` along the category axis and its `y` along the
  value axis — the same `LineChart` data overlays vertical and horizontal bars.
  The transpose happens at draw time through the `DrawContext`; the layer's
  stored data and its standalone rendering are untouched.
- **Verified by equivalence.** A horizontal panel is the transpose of the
  vertical panel of the same figures: tests assert axis assignment, limits and
  labels land on the swapped axes, mixed orientations raise, and golden cases
  pin a horizontal bar+line panel with a secondary value axis.
