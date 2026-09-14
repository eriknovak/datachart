---
status: accepted
---

# A bump chart ranks per period and draws through the line layer

A bump chart (issue #134) shows rank over time: one line per entity, rank 1
at the top, a marker at every period, the entity named at the line's end.
League tables, popularity and market-share rankings are the common cases.
Users build one today from `LineChart` by ranking by hand, inverting the
axis, and placing text at the line ends.

## Commitments

- **Data follows `LineChart`.** A list of `{x, y}` points per series, series
  names from `subtitle`. The issue's `{"label", "x": [...], "y": [...]}`
  shape was dropped: a second series shape for one front would split the
  line-family API for no gain.
- **`rank_by` is a `RANK` member: `VALUE_DESCENDING` (default), `VALUE_ASCENDING`,
  `GIVEN`.** Descending gives rank 1 to the highest value, ascending to the
  lowest (lap times, golf scores); a caller negating data instead would also
  negate the numbers `show_values` prints. There is no bare `VALUE` member:
  naming the direction on every call site reads unambiguously. `GIVEN` takes
  `y` as the rank and raises `ValueError` on a non-integer or non-positive one.
- **Ranking is per period, over the series present there.** Ties keep input
  order, as sorting does everywhere (ADR 0042). A series with no point at a
  period leaves a gap in its line and takes no rank there.
- **The y-axis is the rank.** Integer ticks only, rank 1 at the top.
- **End labels are `show_labels: bool` plus `label_position`.** `show_labels`
  keeps the bool type `ContourChart` already gives it; `label_position` is a
  `LABEL_POSITION` member (`START`, `END` default, `BOTH`). A label prints
  beside the series' first and/or last point in its color; the legend is off
  by default when labels are on. The placement is written so `LineChart` can
  adopt it later, which this ADR does not do.
- **`line_curve` shapes the path, never the data.** A float in `[0, 1]`: `0`
  (default) draws straight segments, higher values a sigmoid between
  consecutive points through the same points. It is not the smoothing that
  `.out-of-scope/chart-front-smoothing.md` rejects — no value changes.
- **`emphasis_rule` reads ranks.** The series family of ADR 0045 applies, with
  the rank as the value read and `top` meaning best ranks: `{"top": 3}`
  highlights the three series with the best mean rank (`by` defaults to
  `"mean"`).
- **Shared vocabularies.** `xticks_format` formats periods (ADR 0037);
  `show_values`/`value_format` print the original `y` through the line placer
  (ADR 0033).
- **One layer on the line layer's drawing.** The bump layer builds on
  `LineLayer` rather than copying it; style keys live under `plot_bump_*`.
- **Overlayable.** The figure composes in `Panel` and `Grid` like a line chart.

## Considered options

- *`show_labels` taking the position enum.* Rejected: one setting name would
  carry a bool on `ContourChart` and an enum here.
- *Descending-only ranking.* Rejected: lower-is-better rankings are common
  and negating the data corrupts printed values.
