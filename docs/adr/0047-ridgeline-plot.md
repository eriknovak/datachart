---
status: accepted
---

# RidgelinePlot stacks per-label density ridges on the category index

A ridgeline plot (issue #133; joy plot) shows how one distribution shifts
across many groups: one density curve per label, rows stacked and partly
overlapping, so twenty groups read in the space a grid of histograms would
spend on four. `ViolinPlot` (ADR 0019) already draws a density per label on
the panel category index (ADR 0020); a ridgeline is the same data seen from
the side, with the rows allowed to overlap.

## Commitments

- **ViolinPlot's data, ViolinPlot's common parameters.** Flat
  `{"label", "value"}` points with the `label`/`value` key remaps, `subplots`
  for a list of lists, `emphasis`/`emphasis_rule` per label, ticks, limits,
  reference lines, and `bandwidth` as a `BANDWIDTH` rule or scalar. The
  issue's `{"label", "values": [...]}` shape was dropped: a second point
  shape for one front would split the group-family API for no gain.
- **Ridges evaluate through `kde1d`, on one shared grid.** The layer calls
  the stats function directly (`ViolinLayer` draws through matplotlib's
  `violinplot` and has no density code to share). Every ridge of a panel is
  evaluated on one grid spanning the union of the rows' padded ranges, or
  `xmin`/`xmax` when given, so curves align point for point. The subplots
  of one figure share that range, as histogram subplots share their bins.
- **Rows live on the category index; the first row is at the top.** Each
  label takes one slot of the panel category index (ADR 0020), so a
  `SwarmPlot` or `BoxPlot` over the same labels lines up in `Panel`. A
  ridge's baseline is its tick; over ridges the panel packs a swarm on the
  side the ridges rise to, so the points sit inside their own ridge. The
  panel inverts
  the category axis when it holds a horizontal ridge layer, so input order
  reads top to bottom as a joy plot does; overlaid group layers follow the
  same axis. A ridge draws above the row it rises into, so overlap reads as
  depth.
- **`overlap` is a float in `[0, 1]`, a front parameter with a theme
  default.** A ridge's peak rises `1 + overlap` slots above its baseline:
  `0` makes rows touch, `0.5` (the `plot_ridgeline_overlap` default) sends
  each peak half a row into its neighbour. Values outside `[0, 1]` raise
  `ValueError` from the validate module.
- **`normalize` is a `RIDGELINE_SCALE` member: `PER_ROW` (default) or
  `COMMON`.** Per-row scales every ridge to the same peak height, so shapes
  compare; common keeps one density scale, so the tallest ridge reaches the
  peak height and the others stay in proportion. The `NORMALIZE` enum is
  the heatmap colormap norm and is not reused.
- **`inner` reuses `VIOLIN_INNER` without `BOX`.** `"median"`,
  `"quartiles"`, or `None` (default); `"box"` raises `ValueError`. Marks
  are drawn by the layer from the data, clipped to the ridge height at that
  value, as the violin layer does (ADR 0019: one enum, not booleans, so the
  issue's `show_median`/`show_quartiles` were folded in).
- **`sort` reuses `SORT`, keyed by the row median.** `NONE` keeps input
  order, `ASCENDING`/`DESCENDING` order rows by median; ties keep input
  order (ADR 0042). Never a sort by label.
- **`fill` and `show_outline` are independent bools, both default `True`.**
  Both `False` raises `ValueError`: nothing would be drawn.
- **`orientation` defaults to `HORIZONTAL`.** The value axis is x and rows
  stack along y, the joy-plot form, ridges rising toward the top. `VERTICAL`
  keeps the category axis uninverted: the first row is at the left and each
  ridge rises rightward from its tick. A `Panel` mix with a sibling group figure needs
  the same orientation on both, as everywhere.
- **Style keys under `plot_ridgeline_*`.** `color`, `alpha`, `linewidth`,
  `edgecolor`, `overlap`, `inner_color`, `inner_linewidth`. Fill defaults to
  the palette cycle color, edge to the fill, inner marks to the theme font
  color. Every theme declares every key (ADR 0004); themes override only
  identity keys.
- **Emphasis follows the violin layer.** `"background"` mutes body and inner
  marks with the theme's muted attributes; `"highlight"` thickens the edge.
- **Overlayable.** A group chart type beside box, violin, swarm, and
  raincloud: the figure composes in `Panel` and `Grid`. Neighbouring ridges
  bleed across overlaid marks by design; the caller mutes rows with
  `emphasis` rather than through a special overlay mode.
- **Cut from v1**: split ridges (two groups per row), ridges filled by a
  gradient along the value axis, histogram-based ridges, a raw-point strip
  inside the ridge (a `SwarmPlot` overlay), a `seed` parameter.

## Considered options

- *Grid-only bare figure.* Rejected: the swarm overlay was the stated use,
  and rows already sit on the category index, so refusing `Panel` would cost
  a special case for no safety.
- *A ridgeline-only `sort="median"` literal.* Rejected: `SORT` already names
  "order the categories by value" for the bar fronts; one vocabulary.
- *Extracting density code from `ViolinLayer`.* Moot: that layer has none.
