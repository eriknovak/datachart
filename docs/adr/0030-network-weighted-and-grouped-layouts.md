---
status: accepted
---

# NetworkChart gains the WEIGHTED and GROUPED layouts

`NETWORK_LAYOUT.SPRING` (ADR 0029) pulls every linked pair equally and knows
nothing of `group`, so a weighted or clustered network reads no differently
from an unweighted, flat one. Two opt-in layouts let the data shape the
picture: `WEIGHTED`, where an edge's weight sets how hard it pulls, and
`GROUPED`, where nodes cluster by their `group` and the clusters arrange by
how strongly they are linked.

## Commitments

- **Two new `NETWORK_LAYOUT` members**, `WEIGHTED` (`"weighted"`) and
  `GROUPED` (`"grouped"`). `SPRING` stays the default and is unchanged: the
  ADR 0029 rejection of weight as attraction holds for it. Weight moves nodes
  only when the user picks a layout named for it.
- **`WEIGHTED` is the spring solver with a per-edge pull.** The attraction of
  a linked pair is scaled by

  $$s(w) = 0.1 + 2.9\,\frac{w - w_{\min}}{w_{\max} - w_{\min}}$$

  so the lightest edge pulls at a tenth of the `SPRING` pull, the heaviest at
  three times, the rest linearly between; repulsion is untouched. An edge
  without `weight` pulls as the lightest given one, mirroring the width rule.
  With no weights, or all equal, `s = 1` and the picture is the `SPRING`
  picture. The bounds are internal constants, not style keys: a theme should
  not move the nodes. The equation is stated in the constant's docstring in
  LaTeX; mkdocs gains `pymdownx.arithmatex` and MathJax to render it.
- **`GROUPED` is two levels of spring.** Each group runs the plain `SPRING`
  solver on the edges inside it; a node without `group` is a group of one.
  The groups then run the `WEIGHTED` solver as nodes of a smaller network,
  an edge between two groups weighing the sum of the edges joining them (an
  edge without `weight` counts one). Every solver takes the chart's `seed`.
  Both levels add a pull toward the centre in proportion to a node's
  distance from it (gravity 3): a member with no edge inside its own group,
  or a group with no link to another, would otherwise drift without bound
  and squeeze the linked ones together, and a chain of groups (two strong
  links, one weak) would settle into a line across the square instead of
  folding into a compact shape. Clusters are placed at the group positions:
  a cluster's radius is $0.3\sqrt{n_g / n}$, overlapping clusters are
  pushed apart until their centres sit at least $2\,(r_i + r_j)$ apart,
  and each cluster then shrinks, if needed, to $0.8$ of its share of the gap
  to its nearest neighbour so clusters never touch. A group's spring fills a
  square, so its farthest node is scaled onto the cluster radius: every
  node lies within the disc, and the final fit keeps the discs, not only
  the nodes, inside the layout margin. Group order is first-seen, as for
  the legend.
- **Each named cluster is marked by a halo**: a disc in the group colour,
  the cluster radius plus the group's largest marker radius plus a pad of
  0.03, at `plot_network_group_alpha` (default 0.12; 0 disables it) under
  the edges. The marker term is converted from points at draw time, so the
  disc contains every marker whatever the figure size. Positions alone did not
  show the groups when the edges ran mostly between them, as in the guide's
  layered service example; the halo shows them on any data. A node without
  a group gets none. The halo is a style key because it changes only how
  the picture looks, never where the nodes are.
- **Cost.** `WEIGHTED` costs what `SPRING` costs. `GROUPED` costs the sum of
  the squared group sizes plus the squared group count, plus the push-apart
  over the groups: about the `SPRING` cost at worst (every node its own
  group), far less when groups are many and even. The documented size
  ceilings are unchanged; the guide lists the three spring layouts under one
  row.
- **A reverse pair pulls at its heavier edge.** Directed `A→B` and `B→A`
  are two drawn edges but one spring link; the link takes the larger pull.
- **A node without `group` draws in `plot_network_edge_color`** when any
  node has one. Previously it took the first group's colour and read as a
  member of it; `GROUPED` makes such nodes a visible concept, so the fix
  lands with it. Without groups nothing changes.

## Considered options

- *Weight as `w / w_max`.* Rejected after a preview: nothing pulls harder
  than under `SPRING`, only weaker, and the picture barely moves.
- *Weight as $(w / \bar{w})^2$.* Rejected: a strong effect, but one outlier
  weight flattens every other edge to nothing.
- *Anchored groups on a circle, one solver with a pull toward each group's
  anchor.* Rejected: costs the full `SPRING` solve plus the anchor term, and
  inter-group links do not influence where clusters sit.
- *Emergent groups through same-group pseudo-links.* Rejected: cluster
  positions are unpredictable and small groups wedge inside large ones.
- *Weighted springs inside a group too.* Rejected after a preview: a
  lightly linked member drifts to the cluster's edge and the cluster reads
  less as one unit; the plain spring keeps clusters compact.
- *An ungrouped node joins one shared "ungrouped" cluster.* Rejected: it
  invents a group the data does not have; a group of one reflects the data.
- *A combined weighted-and-grouped flag.* Rejected: `GROUPED` already
  weighs the links between groups, and layouts stay one constant.
- *Muting the edges between groups so the clusters stand out.* Rejected:
  weight already sets an edge's width, and alpha would then say two things.
- *Clusters evenly spaced on a ring.* Rejected: predictable and well
  separated, but drops what the layout is for, linked clusters sitting
  close.
