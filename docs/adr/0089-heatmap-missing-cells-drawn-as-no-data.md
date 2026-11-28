---
status: accepted
---

# A missing heatmap cell is drawn as a hatched "No data" cell, named beside the colorbar

ADR 0082 made a missing value not drawn, so a missing heatmap cell shows
the axes background. On the default `Blues` colormap the lowest values are
near-white too, and readers take a missing cell for a low value (issue
#355). A heatmap is the one front where the hole sits inside a field of
marks that fills the whole axes, so "not drawn" reads as a value. The cell
needs a look no colormap value can have, and the figure needs to say what
that look means.

## Commitments

- **A missing cell draws in a no-data style.** Every `None`, `NaN` and
  `±inf` cell of a `Heatmap` (ADR 0082's one category, "missing") draws as
  a unit square in a neutral face with a hatch. The squares are one
  collection, gid `missing-cells`, just under the value image in the draw
  order (ADR 0054), the way hexbin value steps sit under their tiles. The
  image keeps leaving those cells transparent, so the colormap and the
  norm never see them. No missing cell adds no artist.
- **Two theme keys carry the look.** `plot_heatmap_missing_color` and
  `plot_heatmap_missing_hatch`, named for their look (ADR 0071) and typed
  in `HeatmapStyleAttrs` (ADR 0072). The base value reaches every
  predefined theme through `make_theme` and `derive_theme` (ADR 0074):
  hatch `"//"`, and a colour that is each theme's own `muted_color`, so
  the no-data cell takes the grey the theme already uses for faded marks
  (`#CFCFCF`; the dark and quill themes set theirs to match). The hatch
  lines take the cell border colour, `plot_heatmap_edge_color`, or the
  frame colour when a theme sets none, so the cell reads as part of the
  grid rather than as a heavy mark on it. Quill also overrides the hatch,
  because its etched value steps already use `"//"`. A key in the chart's
  own `style` wins over the theme. The default face sits at OKLab ΔE 13
  from the light end of `Blues`, under the normal floor of 15; the hatch
  carries the rest of the difference, as it does on the `Greys` themes,
  where any grey sits inside the colormap. A first draft used `#BDBDBD`
  with hatch lines in the frame colour; it cleared the floor but drew the
  heaviest mark in the chart, out of step with the colour scheme.
- **A swatch names it beside the colorbar.** With a colorbar and at
  least one missing cell, a frameless one-entry legend reading "No data"
  sits on the colorbar axes, placed outward from the heatmap by edge. It
  rides the colorbar setting (ADR 0035) and adds no front parameter. Under
  etched value steps the step legend ends with the same entry.
- **Both keys `None` turn the style off.** No collection and no swatch
  draw, and a missing cell is not drawn as under ADR 0082. This is the
  opt-out for a matrix whose blank half is redundant, such as the upper
  triangle of a correlation matrix. A `None` colour with a hatch draws a
  transparent face; an empty hatch counts as `None`.
- **The calendar heatmap is out of scope.** `CalendarHeatmapLayer` sets
  `draws_missing_cells` off and leaves a day with no value empty (ADR
  0044). In a calendar, a day without a record often means "no event", not
  "unknown", so whether it is a no-data cell needs its own decision.
- **The mask is read at draw.** The layer resolves the style at build
  (style is resolved once, ADR 0001) and takes `np.isnan` of its value
  grid inside `draw`, never storing it. A later reorder of the grid and
  its role matrix carries the missing cells along with no other change.
- **Hover reports a missing cell.** The hover value of a missing cell is
  the text `"missing"`, not `None`. The calendar heatmap keeps `None`.
- **Emphasis never marks a missing cell, and fades it with the
  background.** Emphasis rules skip a missing cell as before, so none is
  outlined. When any cell carries the background role, the collection takes
  the layer's muted alpha (ADR 0045). An explicit role on a missing cell in
  the `emphasis` grid still applies.
- **This narrows ADR 0082 for an all-missing heatmap.** A subplot whose
  every cell is missing used to draw nothing, as "an empty series draws
  nothing"; a heatmap subplot now draws every cell as no data. The
  figure-level rule stands: a figure whose every cell is missing still
  raises "has nothing to draw".

## Considered options

- **The colormap's bad colour.** Rejected: a colour cannot carry a hatch,
  and any grey sits inside `Greys`, so the missing cell would match a real
  value on two of the predefined looks.
- **A front parameter** to switch the style or the swatch. Rejected: ADR
  0035 keeps the colorbar one setting, and the two theme keys already
  turn it off.
- **A colorbar extension triangle.** Rejected: matplotlib's extension
  means values outside the range, which is not what a missing cell is.
