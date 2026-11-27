---
status: accepted
---

# A grid gives each series label one colour across its cells

Each cell of a `Grid` draws through its own panel, and each panel builds its
own colour cycle (ADR 0001). A series named "C" is green in one cell and blue
in the next when the cells list their series in a different order. Readers
match series across cells by colour, so they read the wrong series, and the
author must pin colours by hand in every chart's `style` (issue #362). The
overflow warning of ADR 0075 has the same blind spot: each cell is checked
alone, so a grid whose cells together hold more distinct series than the
palette has colours never warns.

## Commitments

- **The grid builds one label-to-colour mapping before it draws.** `Grid`
  collects the panels of all its cells in grid order, depth first into nested
  grids and subplot figures, and builds `{palette: {label: colour}}`. The first
  appearance of a label decides its colour. A label whose series has its own
  colour (ADR 0077) maps to that colour and takes no palette slot. Any other
  label takes the next colour of its palette. The mapping is one per palette,
  so cells built under different themes map labels within their own palette.
- **The series label is the legend label of one series, else the
  subtitle.** A layer's label is its group's `legend_label` when set and the
  group holds one coloured dataset (one that takes a colour and is not drawn
  all muted), else the layer's `subtitle`. A legend label over several series
  names the figure, not each series, so each of those series is labelled by
  its own subtitle, or by none. A label matplotlib hides (a leading
  underscore, such as `NO_LEGEND`) counts as no label.
- **Only some layers join the mapping.** A layer joins when it takes a colour,
  is not drawn all muted, and has a label.
  Unlabelled, colourless and muted layers never read or claim the mapping. An
  unlabelled series keeps exactly the colour it draws today, even where that
  matches a label's colour.
- **The mapping reaches the cells as a render-only setting.** `Grid` passes it
  as the overrides of its top-level render call and never stores it on a cell
  node or in the figure metadata. A grid nested in a grid is therefore
  coloured by the outer grid's mapping, recomputed over the whole tree, and
  ADR 0006's transport is unchanged. A panel drawn alone, and `Panel`, get no
  mapping and are unchanged.
- **A cell still advances its own cycle.** A labelled series looks up its
  slot in the cell's cycle as before and then takes the label's colour, so an
  unlabelled series in the same cell keeps its colour. Colour is the only
  property shared: hatch, line-style and marker cycles stay per cell.
- **The grid legend lists each label once.** When the grid legend names no
  cell, it gathers the entries of the top-level cells in order and keeps the
  first handle per legend entry label, the text the legend shows. A legend that names a cell (the scatter matrix)
  keeps that cell's entries. This amends ADR 0070, whose grid legend took
  the entries of the first cell that had any.
- **The overflow warning counts distinct labels in a grid.** This amends ADR
  0075: where a grid carries the mapping, the warning fires once per palette
  when its distinct labels outnumber its colours, with the existing "N series"
  message. A cell's own warning counts only the layers the mapping did not
  colour, so cells that repeat the same labels within the palette raise none.
- **Colour across cells is a grid job above the panel.** This amends ADR 0001:
  `Panel` still owns the colours within one coordinate space, and `Grid` owns
  the colours that must agree between several. The seam is the render-only
  setting, not a second drawing path.

## Considered options

- **A user-supplied label-to-colour parameter.** Rejected: issue #362 puts it
  out of scope. It makes every author write what the grid can infer, and the
  inferred mapping does not close the door on adding one later.
- **Matching by chart hash across cells.** Rejected: the hash keys the chart's
  data, and the same label rarely carries the same data in two cells, so the
  same series would still change colour.
- **One pooled cycle for every cell.** Rejected: it colours unlabelled cells
  by position across the grid, so a chart's colours would depend on its
  neighbours, and an unlabelled figure would no longer look the same in a grid
  as alone.
