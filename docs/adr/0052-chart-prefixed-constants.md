---
status: accepted
---

# A constant one chart owns carries that chart's prefix

`datachart.constants` mixed two naming rules. `GANTT_VALUE`, `DUMBBELL_SORT_KEY`
and `RADIAL_TYPE` said which chart they belong to; `DIAGONAL`, `BASELINE`,
`RANK`, `LABEL_POSITION`, `WEEKDAY`, `DIRECTION` and `DATE_PERIOD` read as
general although each is accepted by exactly one chart. A user browsing the
module could not tell which constant goes with which parameter, and no page
mapped charts to their constants.

One rule now holds: a constant accepted by a single chart carries that
chart's prefix (`SCATTER_MATRIX_DIAGONAL`, `STACKED_AREA_BASELINE`,
`BUMP_RANK`, `BUMP_LABEL_POSITION`, `CALENDAR_WEEKDAY`, `RADIAL_DIRECTION`,
`GANTT_DATE_PERIOD`); a constant several charts share carries none
(`SORT`, `ORIENTATION`, `BANDWIDTH`, `VIOLIN_INNER`, `SWARM_MODE`). The
module stays flat: family-shared constants would need an owner or a
duplicate under per-chart namespaces, and the general half would stay flat
anyway, leaving two places to look.

The map lives in the docs, generated from the chart fronts' signatures by
`docs/assets/scripts/generate_constants_by_chart.py`: a constants-by-chart
table on the constants reference, whose chart section is split into shared
and chart-specific constants, and a parameter-to-constant table under every
chart guide's quick reference. The script reruns whenever a front gains or
loses a constant-typed parameter.

The old names are removed, not aliased, under the ADR 0010 policy.

## Considered options

- **Per-chart namespaces** (`GANTT.VALUE.DURATION`). Rejected: three dotted
  levels, family-shared constants duplicated or arbitrarily owned, and the
  general constants still flat beside them.
- **Constants on the fronts** (`GanttChart.VALUE`). Rejected: the fronts are
  plain functions.
- **Hand-written tables.** Rejected: 24 guides plus the reference drift the
  first time a parameter changes; the script derives them from the code.
