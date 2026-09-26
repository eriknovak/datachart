---
status: accepted
---

# One category index per panel places every category layer by label

Bars, stacks and radial layers placed each value by its position in their own
record list, so series whose labels differed in order or set drew values under
the wrong tick (issue #302). We widen the category index of ADR 0020 to every
category-bearing layer in a panel — bars (stacked, grouped, overlaid, pyramid
sides), radial layers, and the group layers — so a panel has one category
axis and one map from label to position.

## Commitments

- **Union, first-seen order.** The index is the union of every category
  layer's labels in first-seen order; each layer looks its labels up in it.
  A series missing a label leaves that slot empty — no bar, no point, and
  nothing added to a stack there. Rejected: requiring every series to carry
  the first one's labels, which would turn partly overlapping series into
  an error.
- **Ticks and spokes come from the index**, never from one layer's labels.
- **A repeated label within one series raises** a `ValueError`: its slot
  would be ambiguous.
- **A radial line breaks at a missing label** rather than joining its
  neighbours, so no value is invented.
- **Category sort (ADR 0042) is unchanged** — it reorders the records, and
  each sorted chart also carries the full sorted category order, which the
  index reads in place of its labels. A series missing the first category
  would otherwise push that category behind its own.
- **Gantt rows are out of scope**: they place themselves by task.
