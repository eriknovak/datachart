---
status: accepted
---

# End labels are the line family's direct-label mode

`show_values` labels every point of a line, which the guidelines call noise;
the sparing form, one label at the end of each series, existed only on
`BumpChart`. A line chart with a legend still made the reader match colours
back and forth between the box and the lines (issue #293). ADR 0046 wrote the
bump chart's placement "so `LineChart` can adopt it later"; this record does
that, and settles the two things a line end needs that a rank end never did:
a colour that keeps the text legible over other lines, and a way to keep
labels apart when series end at the same value.

## Commitments

- **`show_labels` and `label_position` on `LineChart` and
  `StackedAreaChart`.** One label per series, its `subtitle`, beside its last
  present point; `label_position` a `LINE_LABEL_POSITION` member (`START`,
  `END` default, `BOTH`). Off by default on both fronts; the bump chart keeps
  its labels on. A stacked band is named at its midpoint at the band's end.
  The legend defaults of the line and stacked area charts do not change: end
  labels supplement the legend. The bump chart keeps turning its legend off
  when labelled, since its bare rank axis leaves the labels as the only
  naming.
- **An end label prints in the text colour with the value-label halo.** The
  font is the plot text style, the colour `plot_text_color`, and the halo
  `plot_value_halo_width` in the ground colour; a background-emphasis series
  takes the muted colour. This amends ADR 0046, whose labels printed in the
  series colour: text never wears the series colour, and the line end beside
  the label already carries identity. The gap between the end and its label
  is the mark radius plus the bump chart's `plot_bump_label_padding` there
  and the point-label pad elsewhere.
- **Overlapping end labels spread along the value axis.** Once every layer
  of a panel has drawn, the panel gathers the end labels of one axes on one
  side, sorts them along the value axis and pushes overlapping neighbours
  apart by their estimated text height, moving each of a pair half the
  overlap until none remains. A label never moves along the category axis:
  it stays beside the end it names. The bump chart takes the same pass,
  where whole ranks leave it nothing to do.
- **`LINE_LABEL_POSITION` is the domain; `BUMP_LABEL_POSITION` its
  deprecated alias.** This amends ADR 0052, under which a constant several
  charts share carries no prefix: a constant one chart family owns carries
  the family's prefix, since the bare `LABEL_POSITION` would read as the
  domain of every `label_position`, and the network chart's is another
  (`NETWORK_LABEL_POSITION`). The constants-by-chart generator lists a
  family-owned constant as chart-specific on each of its fronts. The alias
  goes through the constants module's deprecated-alias hook and is removed
  at the next release.

## Considered options

- **Place end labels through the panel's point-label placer.** Rejected: it
  tries spots all around a mark, so a crowded end would put a name left of
  or above the line's last point, where it no longer reads as the name at
  the end. A one-dimensional spread keeps every label beside its end.
- **Keep the series colour, as the bump chart drew.** Rejected: the
  guidelines keep text in the text tokens, and a series-coloured word over
  a neighbouring line of another colour is the least legible case, exactly
  where a halo in the ground colour reads.
- **Turn the legend off when labels are on, as the bump chart does.**
  Rejected for the line and stacked area charts: the issue keeps the legend,
  and a legend still names a series whose end lies past a user limit or under
  another label's spread.
- **Reuse `BUMP_LABEL_POSITION` unchanged.** Rejected: a line chart taking a
  bump-named constant reads as borrowing, and ADR 0052 prefixes a constant
  by its owner, which is now the line family.
- **An unprefixed `LABEL_POSITION`, as ADR 0052 names shared constants.**
  Rejected: `label_position` is also a network chart parameter with its own
  domain, so the bare name would claim a generality it does not have.
