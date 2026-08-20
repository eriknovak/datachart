---
status: accepted
---

# Public Panel/Grid composition fronts over the drawing seam

Composition is exposed as a chart-type-per-combination: `OverlayChart` for
same-axes overlays, `FigureGridLayout` for grids, plus the long-deprecated
`figure_grid_layout` — each with its own dict-wrapping convention. ADR 0001 gave
every rendered figure a Panel in its metadata transport, so figures already
compose mechanically; only the public vocabulary lags. We add two constructors
in `datachart.utils` that mirror the internal seam: `Panel([...])` for one
coordinate space, `Grid([[...]])` for arrangement. This is a public-API
repackaging — no drawing-path changes, golden parity must hold.

## Commitments

- **Users compose rendered figures**, as today. Chart fronts keep returning
  `plt.Figure`; no lazy chart object is introduced.
- **`Panel` items are bare figures or dicts.** A bare figure means all defaults;
  a dict (`{"figure": f, "y_axis": "right", ...}`) carries per-figure options
  (`y_axis`, `z_order`, `legend_label`). Panel-level kwargs are `OverlayChart`'s,
  unchanged.
- **`Grid` layout is visible in the argument.** Nested rows are the layout:
  cells are bare figures or `None` (blank cell); a shorter row's cells stretch —
  colspans via the LCM of row lengths (`[[a, b], [c, d, e]]` → width 6, spans
  3 and 2). A flat list means auto grid with `max_cols`, and only there may
  items be dicts with a `layout_spec` escape hatch (rowspan, irregular grids).
  Mixing nested rows with `layout_spec` is an error.
- **Nesting rules**: `Panel` output in a `Grid` cell is supported (overlay
  figures carry a panel). `Grid` output inside `Grid` or `Panel` is rejected
  with a clear error — grid figures carry no panel. Grid-in-Grid stays open.
- **The old fronts emit `DeprecationWarning`** (`OverlayChart`,
  `FigureGridLayout`, `figure_grid_layout`) and delegate to the new fronts;
  docs, examples, and notebooks move to the Panel/Grid vocabulary.
- **One latent fix rides along**: the GridSpec layout path passed booleans to
  `add_subplot(sharex=..., sharey=...)`, which matplotlib rejects; it now shares
  against the first axes. Nested rows use this path, so the fix is required —
  it also unbreaks `layout_spec` + `sharex`/`sharey` in the old fronts.
- **The name shadow is accepted.** Public `datachart.utils.Panel` (a front
  returning a figure) and internal `layers.Panel` (the renderer) never meet in
  a user namespace; renaming either would muddy the shared language.

## Considered options

Operator sugar (`fig1 + fig2`, `p1 | p2`) was rejected for now: `plt.Figure`
cannot overload operators, so it would force a wrapper object. A lazy
composition object was rejected as breaking figure-in/figure-out for no
drawing benefit.
