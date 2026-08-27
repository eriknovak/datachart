---
status: accepted
---

# SankeyChart draws weighted flows between column-ordered nodes through one layer

A Sankey diagram (issue #68) shows how quantities flow between categories —
label transitions between annotators, attrition through a pipeline. It is
non-Cartesian: nodes are bars laid out in columns, flows are ribbons whose
height carries the value, and the axes carry nothing.

## Commitments

- **Input is a `links` list.** A chart dict is `{"links": [{"source",
  "target", "value"}, ...]}`; a node is a string that is both its identity
  and its drawn label. A list of chart dicts renders one Sankey per subplot;
  there is no overlay semantics (`CHART_CONFIGS`: `multiplot: False,
  subplots: True`).
- **Columns are inferred, `nodes` overrides.** A node's column is its
  longest path from any source; leaves stay at their own depth rather than
  being pushed to the last column (pushing them stretched short-lived
  branches across the whole figure in the design preview). Vertical order
  within a column is first-seen input order. An explicit
  `nodes=[[...], [...], ...]` list of columns replaces both.
- **Cycles raise `ValueError`** from `validate.py`; back-edges are never
  dropped silently.
- **One `SankeyLayer` per chart** holds every link, like `ParallelCoordsLayer`.
  It computes node sizes (max of in/out flow), one height scale across all
  columns, node rectangles, and cubic-Bézier `PathPatch` ribbons; ribbons are
  stacked from the top of each node and drawn in order of endpoint height to
  reduce crossings. The layer draws no furniture: the axes stay
  `axis("off")` with a fixed 0–1 data space, projection stays `"cartesian"`.
- **`Panel` rejects Sankey figures explicitly** (as pyramids, ADR 0017);
  `Grid` accepts them as ordinary cells. `emphasis` is rejected at the front
  (no series to mute), as for heatmaps.
- **Colors.** Each node takes the next color from `color_general_multiple`
  in column-then-row order, keyed by node name. Ribbons take the source
  node's color by default; `plot_sankey_link_color` switches to `"target"`
  or `"grey"`, at `plot_sankey_link_alpha`.
- **Style keys** in `BASE_THEME`: `plot_sankey_node_width` (0.04 of the
  horizontal span), `plot_sankey_node_pad` (0.10 of the vertical span shared
  by the gaps of the tallest column), `plot_sankey_node_edge_color` /
  `plot_sankey_node_edge_width` (white, 0.6, a centred stroke — mirrors
  `plot_bar_edge_*`, and GRAYSCALE, HATCH, INK override the color the way
  they do for bars), `plot_sankey_link_color`, `plot_sankey_link_alpha`
  (0.4), `plot_sankey_label_halo_width` (2; a white halo behind labels so
  they stay legible over ribbons, 0 disables). Labels use `font_general_*`.
- **Labels** sit left of the first column and right of every other column.
  No value annotations.

## Considered options

- *Three parallel lists `sources`/`targets`/`values`.* Rejected: every other
  front takes a chart dict, and a link is one record.
- *Leaves in the last column.* Rejected after the design preview: a leaf
  reached in one hop is drawn as a ribbon spanning every later column.
- *Outward halo instead of a centred node stroke.* Rejected: the centred
  stroke matches bars and the ribbon meets the stroke line exactly.
- *Per-column node colors.* Rejected: per-node colors let ribbons be traced
  by source.
- *`matplotlib.sankey`.* Rejected: single-node, no multi-stage layout.
