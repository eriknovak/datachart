---
status: accepted
---

# Emphasis rules reach every front, each selecting its own unit

ADR 0042 gave `emphasis_rule` to the bar-type fronts only, because the other
fronts carry emphasis in different shapes — per series, per group label, per
record — and a value threshold means something different in each. This
extends the rule to every front that carries emphasis, plus heatmap and
hexbin, and fixes per family what the rule selects and what number it reads
(issue #151).

## Commitments

- **The rule selects the unit the front already assigns emphasis to.** No
  front changes its emphasis shape to fit the rule:

  | Family | Fronts | Unit | Value read |
  |---|---|---|---|
  | Per record | bar, pyramid, radial (bar) | bar record | `y` (ADR 0042) |
  | Per record | treemap | leaf record | `value` |
  | Per record | network | node | `size`; missing raises |
  | Per record | parallel coords | data row | the `hue` column; no `hue` or non-numeric raises |
  | Per cell | heatmap | cell | the cell value |
  | Per cell | hexbin | bin | the bin's aggregated value |
  | Per group | box, violin, swarm, raincloud | group label | summary of the group's values |
  | Per series | line, scatter, stacked area, histogram, contour (lines) | series | summary of the series' values |

- **A parallel-coords hue scale spans every record.** The continuous ramp
  reads the whole `hue` column, background rows included; the rule mutes, it
  does not rescale. A categorical hue still skips background rows in the color
  assignment and the legend.
- **Group and series rules take an optional `by` summary**: `"mean"`,
  `"median"`, `"min"`, `"max"`, `"sum"`. Groups default to `"median"`, what a
  box already draws; series default to `"mean"`. This amends ADR 0042's
  one-key shape: the rule is one comparison key plus, on these fronts only,
  `by`. A `by` on a per-record or per-cell front raises — a record has one
  value, there is nothing to summarise.
- **A series summary reads the series' own values**, never the stacked
  position, as bar records do under ADR 0042. Scatter summarises `y`,
  histogram the raw data, contour `z`.
- **Heatmap cells gain an explicit role** — the per-cell primitive the rule
  fills in, as bar records gained one. Hexbin bins are computed at draw time
  and cannot be addressed by the caller, so hexbin takes the rule only.
- **Everything else in ADR 0042 holds on every front**: an explicit role wins
  over the rule, a match is `HIGHLIGHT` and a non-match `BACKGROUND`, `top`
  and `bottom` rank across every unit in one call, and ties keep input order.
- **Filled contours still reject emphasis, and so the rule.** Calendar
  heatmap and sankey stay without emphasis.

## Considered options

- *A fixed summary per family, no `by`.* Rejected: "highlight groups whose
  worst case exceeds X" is as common as a median threshold, and the choice is
  one small, closed key rather than a second mechanism.
- *Scatter emphasis per point.* Rejected: scatter emphasis is per series
  today, and changing its unit would break every existing call.
  Amended (issues #204, #219): scatter and swarm records gain an optional
  `emphasis` key, additive to the series or group role — the rule's unit is
  unchanged. A record's own key wins over its series or group role, whether
  explicit or filled by the rule; a role set on the figure in `Panel` wins
  over the record.
- *Parallel coords reading its first dimension.* Rejected: dimensions have
  unrelated scales and order, so "first" is arbitrary. `hue` is the column
  the caller already chose to colour rows by.
