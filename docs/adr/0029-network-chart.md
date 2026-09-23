---
status: accepted
amended-by: [0030]
---

# NetworkChart draws node-link diagrams from a nodes/edges dict through one layer

A network diagram (issue #95) shows relational data — dependencies,
co-occurrence, flows between peers — as nodes placed by a layout and joined by
edges. It is non-Cartesian like the Sankey (ADR 0026) and the treemap
(ADR 0028): the layer owns an axes-off 0–1 space and the axes carry nothing.

## Commitments

- **The front is `NetworkChart`**, type key `networkchart`, style prefix
  `plot_network_*`, layer `NetworkLayer`. "Graph" stays out of every
  identifier: it is a synonym for "chart" and would make `plot_graph_*`
  ambiguous next to the other `plot_*` keys.
- **Input is a `{nodes, edges}` chart dict.** A node record is `{id,
  label?, size?, group?, emphasis?}`; `label` defaults to `id`. An edge
  record is `{source, target, weight?}`. `nodes` may be omitted, in which
  case the node set is inferred from the edges in first-seen order. Duplicate
  ids, edges referencing unknown ids, and non-positive `size` or `weight`
  raise `ValueError` from `validate.py`. A list of chart dicts renders one
  network per subplot (`ChartKind`: `multiplot=False, subplots=True`).
- **Layout is a chart attribute, not style.** The front's `layout` argument
  takes a `NETWORK_LAYOUT` constant: `SPRING` (default), `CIRCULAR`, or
  `FIXED`. `FIXED` reads `x`/`y` from every node record and raises when one
  lacks them. Layout changes what the picture means, so it lives with the
  data, as `nodes` does on `SankeyChart`.
  Amended (issue #217): `FIXED` positions must lie in 0–1 and raise
  otherwise. They draw inside the same layout margin as the other layouts
  through one fixed affine map, never a fit to the data range, so relative
  placement stays the user's. The map is the view: the limits widen to
  $-m/(1-2m)$ and $1 + m/(1-2m)$ for margin $m$, so node positions, `texts`,
  value labels and hover share the user's 0–1 space and a text aimed at a
  node lands on it.
- **Spring layout is in-package.** Fruchterman–Reingold in numpy (numpy and
  scipy are already hard dependencies; `networkx` is not added). It is seeded
  by a `seed` front argument, default 0, so golden images and repeated renders
  are stable. Positions are normalised into the 0–1 space with a margin for
  markers and labels. Edge weight does not enter the layout.
  Amended (issue #216): a disconnected graph no longer runs one global pass,
  where isolates repel without bound and the fit squashes the real
  component. Each component of two or more nodes runs its own spring with
  the chart's seed and is packed like an ADR 0030 cluster (radius
  $0.3\sqrt{n_c / n}$, largest at the centre, pushed apart to $1.25\,(r_i +
  r_j)$ since components carry no halo); isolates sit evenly on a ring just
  outside the packed components, a one-node cluster's diameter apart. A
  connected graph takes the single pass unchanged.
- **`directed` is a front flag, default `False`.** Directed edges end in an
  arrowhead clipped at the target node's radius; `A→B` and `B→A` are two
  arrows. Undirected mode merges reverse duplicates into one line. A
  directed edge is one filled polygon (matplotlib's `simple` arrow, tail
  width = edge width, no stroke), never a stroked shaft plus a head: two
  translucent shapes double the alpha where they meet.
- **Edge geometry is an `ARROW_STYLE`.** `ARROW_STYLE` (ADR 0018) is the one
  connector constant in the package; it gains `STRAIGHT` (a straight plain
  line with the annotation gap; `TOUCHING` stays the flush variant, released
  in 0.8.0). `plot_network_edge_style` accepts only its two headless
  members, `CURVE` (default) and `STRAIGHT`; a headed member raises with a
  message pointing at `directed`, because directedness changes what a
  reverse pair means, not only how it looks. `plot_network_edge_curve`
  (default 0.2) is the `arc3` bow, sign picking the side, as
  `plot_text_arrow_curve` does for annotations; `STRAIGHT` ignores it. A
  curve bows each arrow of a reverse pair to its own side, so the pair reads
  as two edges and their values never collide. The `ARROW_STYLE` docstring
  and the annotations and network guides state which members each chart
  accepts.
- **Edge weight maps to width only**, linearly between
  `plot_network_edge_width_min` and `plot_network_edge_width_max`; an edge
  without `weight` draws at the minimum. Edges take
  `plot_network_edge_color` (the Sankey grey) at `plot_network_edge_alpha`.
- **Node size maps by square root to marker area**, between
  `plot_network_node_size_min` and `plot_network_node_size_max`; a node
  without `size` draws at `plot_network_node_size`. Nodes are a scatter and
  their style keys mirror `plot_scatter_*`: `plot_network_node_color`,
  `_alpha`, `_marker`, `_edge_color`, `_edge_width` (white stroke; GRAYSCALE,
  HATCH, INK override the color as for bars).
- **Colors.** Without `group`, every node takes one `color_general_singular`
  color. With `group`, nodes take the next `color_general_multiple` color
  keyed by group name in first-seen order, and `show_legend` (off by default)
  lists the groups.
- **Emphasis is per node**, via an `emphasis` key carrying an `EMPHASIS`
  role, as for treemap records. `background` mutes the node, its label, and
  every edge touching it; `highlight` strokes the node border in
  `font_general_color` at `plot_network_highlight_edge_width`. Roles are
  explicit: highlighting one node does not mute the others. The front's
  per-chart `emphasis` argument raises, as for Sankey and treemap.
- **Labels** are drawn at the node centre in `font_general_*` behind a white
  halo of `plot_network_label_halo_width` (2; 0 disables); an empty label
  draws nothing. `show_values` writes each edge's weight at its midpoint in
  the `plot_bar_value_*` style behind the same halo, formatted by
  `value_format`, off by default.
- **One `NetworkLayer` per chart**, no furniture: `axis("off")`, 0–1 data
  space with equal aspect, `"cartesian"` projection. `Panel` rejects network
  figures with a "use `Grid`" message; `Grid` accepts them as ordinary cells.
  `texts` annotations are placed in the 0–1 layout space.
  Amended (issue #217): under `FIXED` the view widens past 0–1 by the
  layout margin; the data space is still the 0–1 layout space.

## Considered options

- *`GraphChart`, `NetworkGraph`, `NodeLinkChart`.* Rejected: "graph chart"
  reads as "chart chart"; the bare-noun form (`Treemap`) is for single words;
  "node-link" is precise but unfamiliar.
- *Layout as a style key.* Rejected: a theme should not move the nodes.
- *Undirected only in v1.* Rejected: the motivating data (dependencies,
  flows) is directed, and arrowheads are a draw-time detail once positions
  exist.
- *A separate `EDGE_STYLE` constant.* Rejected: one constant for every
  connector in the package; annotations gain `STRAIGHT` for free.
- *Renaming `ARROW_STYLE` to `CONNECTOR_STYLE`.* Rejected: an alias to
  document and deprecate for no gain.
- *Dropping `TOUCHING` once `STRAIGHT` exists.* Rejected: it shipped in
  0.8.0 and is the only flush connector without a public gap key.
- *Straight edges by default.* Rejected after the preview: curves separate
  reverse pairs without an extra rule, and annotations already default to
  the curve.
- *Weight as spring attraction.* Rejected: a value users intend as a visual
  cue would move every node when edited.
- *`networkx` as an optional dependency.* Rejected: the spring layout is a
  few dozen lines of numpy and the package stays matplotlib-plus-numpy.
- *Random seed by default.* Rejected: golden-image tests and notebooks need
  a stable picture.
