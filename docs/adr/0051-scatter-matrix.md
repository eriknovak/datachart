---
status: accepted
---

# A scatter matrix is a grid figure composed from scatter and histogram cells

A scatter matrix (issue #132) shows every pair of numeric dimensions as a
scatter chart, with each dimension's distribution on the diagonal. The
n × n arrangement is a grid, not a coordinate space, so the chart cannot be
one layer: `ScatterMatrix` is a composition front that renders one cell
figure per pair through the existing fronts and assembles them with the
grid machinery `Grid` uses (ADR 0002, 0006).

## Commitments

- **A grid figure, not an overlayable one.** The front returns a figure with
  the recursive `{"type": "grid", "cells": [...]}` transport, so it nests
  inside `Grid` and is rejected by `Panel` like any grid figure. No matrix
  layer exists; the only new drawable is a KDE curve for the diagonal.
- **Cells are ordinary charts.** Off-diagonal cells are `ScatterChart`
  figures with one chart per hue group; the diagonal is a `Histogram`
  (`SCATTER_MATRIX_DIAGONAL.HIST`, default), a KDE curve from `stats.kde1d` per hue group
  (`SCATTER_MATRIX_DIAGONAL.KDE`), or blank (`SCATTER_MATRIX_DIAGONAL.NONE`). Every cell lists the hue
  groups in the same order, so the panel colour cycle gives the whole
  figure one group → colour map without a shared-cycle mechanism.
- **One legend.** Per-cell legends are off; a figure-level legend names
  the hue groups when `hue` is set (`show_legend` opts out).
- **Categorical hue only.** A numeric `hue` raises. The continuous ramp
  `ParallelCoords` offers has no clean reading across per-group KDEs and
  correlation text; a colorbar on a grid is a separate design.
- **The upper triangle carries the numbers (ggpairs convention).**
  `show_correlation` replaces upper-triangle scatters with the Pearson r
  (one line per hue group, from `stats.correlation`). `lower_only` blanks
  the upper triangle entirely and wins over `show_correlation`.
  `show_regression` draws a `stats.linear_fit` line per hue group in every
  scatter cell.
- **Axes share by column and row.** `sharex` links every cell of a column
  and `sharey` every cell of a row, both on by default, so each scale is
  labelled on the outer edge. A diagonal cell shares its row too: its
  visible axis shows the row's scale, while its histogram or density curve
  draws on a hidden twin axis with its own height. Tick labels show only on
  the outer edge; dimension names label the outer left column and bottom
  row.
- **Input shape.** One dict of columns or a list of records; `dimensions`
  selects and orders columns and defaults to every numeric non-hue column
  in input order.
- **Own style family.** `plot_scatter_matrix_*` keys: regression line
  colour/width/style, correlation text size/weight, KDE curve width/alpha,
  diagonal alpha. Themes override identity keys only. Cell marks take the
  scatter and histogram style families unchanged.
- **Category relationships**, guide notebook on the shared real dataset
  (ADR 0011), golden cases for default, hue, `lower_only`, each diagonal
  mode, and correlation + regression.

## Considered options

A `ScatterMatrixLayer` drawing the whole matrix into one axes with inset
axes was rejected: it would bypass the panel seam for every cell and
re-implement axis sharing, gridlines and legend furniture the grid path
already owns. Mirrored scatters in the upper triangle (seaborn default)
were rejected as carrying no information the lower triangle lacks.
