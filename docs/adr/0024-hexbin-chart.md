---
status: accepted
---

# HexbinChart bins dense scatter data into colormapped hexagons

A hexbin chart (issue #67) tiles the plane with hexagons and colors each by
the number of `(x, y)` points falling in it — the dense-scatter alternative
where a `ScatterChart` turns into an opaque blob. With an optional per-point
`c`, each hexagon shows an aggregate of `c` instead of a count.

## Commitments

- **Input is a list of column dicts `{x, y, c?}`**, built with
  `is_2d_data=True` like Heatmap and Contour — not ScatterChart's list of
  points. A list of charts grids them with `subplots=True` and otherwise
  overlays them on one axes; overlaying hexbins is allowed but not
  special-cased, since opaque tiles hide each other.
- **Counts by default; `c` switches to aggregation.** `reduce` is a chart
  attr taking a `HEXBIN_REDUCE` constant (`MEAN`, `SUM`, `MEDIAN`, `MIN`,
  `MAX`), default `MEAN` when `c` is given and ignored otherwise. Callables
  stay out of the public API.
- **Color scale reuses the raster attrs.** `norm`, `vmin`, `vmax`, `valfmt`,
  `colorbar` are per-chart attrs and `show_colorbars` a figure setting,
  exactly as for Heatmap and Contour; log-scaled counts are
  `norm=NORMALIZE.LOG`. Matplotlib's `bins="log"` and `extent` are not
  exposed.
- **`gridsize` and `mincnt` are chart attrs.** `gridsize` defaults to the
  `plot_hexbin_gridsize` config key (30); `mincnt` defaults to `None` (every
  hexagon drawn).
- **Style keys `plot_hexbin_cmap`, `_alpha`, `_edge_width`, `_edge_color`,
  `_gridsize`**, resolved once at build time; `cmap` falls back to
  `plot_heatmap_cmap`. Every theme sets all of them.
- **It is a raster for panel furniture.** The grid is suppressed under the
  tiles (gridlines sit above collections in matplotlib's z-order) and the
  colorbar goes through the shared `_draw_colorbar` inset. The layer is
  overlayable in `Panel` so lines, scatter, or contours can sit on top.

## Considered options

- *Hexbin as a `ScatterChart` mode.* Rejected: it needs a colormap, a
  colorbar, and a raster's furniture, none of which scatter has; it shares
  the input shape of the 2-D charts instead.
- *A `color_scale` setting for log counts.* Rejected: `norm` already does it
  for the other colormapped charts, and a second knob would drift.
- *`extent` per chart.* Rejected: the tiling follows the data; axis limits
  still crop the view.
