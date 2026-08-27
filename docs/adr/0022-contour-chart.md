---
status: accepted
---

# ContourChart draws a gridded surface as lines or fills through one layer

A contour chart (issue #66) draws a 2-D grid `z` over axes `x`, `y` as
iso-lines (`ax.contour`) or filled bands (`ax.contourf`). It is the rendering
half of the 2-D density chart (issue #65): the density front only estimates a
grid and hands it to the same layer, so the two never fork a drawing path.

## Commitments

- **Input is a list of chart dicts, each `{x, y, z}`.** `x` and `y` are
  optional 1-D axes (index fallback), `z` a 2-D grid. Heatmap keeps its bare
  2-D list for now; migrating it to the same shape is a separate task, not
  this one.
- **Histogram semantics for lists, not Heatmap's.** Several charts overlay on
  one axes by default; `subplots=True` grids them. Each chart gets a legend
  entry (a proxy line) and, for line contours, `emphasis` works as for lines.
- **`filled` is a chart attr, default `False`.** Lines take the panel's cycle
  color, so a lone contour matches a lone line chart and several overlaid
  contours stay distinguishable. Fills take a colormap (`plot_contour_cmap`,
  default the heatmap cmap), turn the grid off, and may show a colorbar
  through the heatmap inset pattern. Lines only use the cmap when the user
  sets one, and then sample it from 0.3 upward — the low end of a sequential
  cmap vanishes on white.
- **Level count defaults to matplotlib's auto (~8 nice values).** A
  `CONTOUR_LEVELS` constant offers `AUTO`, `RICE`, and `FD`; `levels` also
  takes an int or an explicit list. The rule-based counts were prototyped on
  a 120×120 grid: Freedman–Diaconis and Rice on the cell count saturate at
  the 20-level cap and Sturges on the cell count gives 15 — all too dense —
  so every rule is evaluated on the per-axis resolution (`sqrt(cells)`),
  where Rice gives ~10 and FD ~19. None of them is truly data-derived: they
  scale with grid resolution, which is a rendering choice, hence auto stays
  the default and the rules are opt-ins.
- **Inline labels are opt-in.** `show_labels=True` runs `ax.clabel`, formatted
  by `valfmt` in the heatmap format-string convention.
- **One layer, no helper API.** `ContourLayer` reads the arrays from the chart
  dict; the density front builds that dict from a `stats.kde2d` estimate.

## Considered options

- *Contour as a Heatmap mode.* Rejected: a heatmap is a per-cell image with
  cell borders and value labels; contours interpolate between cells and
  overlay. Different layer, different furniture.
- *A data-derived level rule as the default.* Rejected on the prototype
  renders (above): every rule tracks grid resolution, not the surface.
