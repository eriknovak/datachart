---
status: accepted
---

# A gantt chart puts time on the value axis and stays a bare figure

A gantt chart (issue #131) shows a schedule: one horizontal bar per task
from its start to its end, rows grouped by category, optional progress fill,
dependency arrows, and a today line. Users hand-built it with `BarChart`
and matplotlib date numbers. The pieces exist: temporal detection (ADR
0037), bar slotting and per-record emphasis (ADR 0042 / 0045), reference
lines that take datetimes (ADR 0037), value labels (ADR 0033).

## Commitments

- **Input is a task record list.** `{task, start, end, group?, progress?,
  depends_on?}` per record, one list per chart. `start` and `end` are real
  temporal objects per ADR 0037 — a string raises `ValueError` naming the
  accepted types. `end < start`, a duplicate `task` name, a `progress`
  outside `[0, 1]`, and an unknown name in `depends_on` each raise one
  `ValueError`.
- **Time is a temporal value axis.** ADR 0037 resolves the panel's temporal
  axis from the layers' `x` kind. A gantt layer reports the kind of its
  *value* column instead, through a second layer hook; the panel's
  temporal-axis resolution reads both, so the value axis gets the date
  locator and formatter, `yticks_format` takes a `DATE_FORMAT`, and
  `ymin` / `ymax` — the value-axis limits in either orientation — take
  datetimes as the time window. The category axis holds the task rows.
- **Always horizontal, and a bare figure.** There is no `orientation`
  parameter, as for `PyramidChart`: a vertical gantt is rare and would
  double the label paths. The figure composes in `Grid` only; `Panel`
  rejects it. In a horizontal panel the secondary axis is a second *x*
  (`twiny`), so a line's `y` would land on the task rows: the LineChart
  overlay the issue named does not compose meaningfully. Planned-versus-
  actual (two gantt figures dodged through bar slots) is a follow-up, not
  a v1 commitment.
- **Row order is `sort` plus `sort_by`.** `sort` is a `SORT` member:
  `NONE` (default) keeps input order; `ASCENDING` / `DESCENDING` order by
  the key `sort_by` names. `sort_by` is `"start"` (default) or `"group"`:
  by `start`, every row orders by its start date; by `group`, rows cluster
  by group, groups ordered by their earliest start, tasks within a group by
  start. Both are value sorts — never by label (ADR 0042); a `sort_by` of
  `"group"` with no `group` keys raises.
- **Colour follows the group.** Without `group`, every bar takes the
  singular palette colour. With `group`, one colour per group from the
  multiple palette, in first-seen order, and one legend entry per group.
- **Progress is an inner bar.** A `progress` fraction draws a second,
  darker bar over that fraction of the range (`plot_gantt_progress_*`);
  a record without `progress` is a plain range. `show_values` is off,
  `"duration"` (whole days, through `value_format`), or `"progress"` (a
  percentage), placed past the bar end as bar labels are (ADR 0033).
- **Dependencies and today line are sugar over existing marks.**
  `show_dependencies` draws a `FancyArrowPatch` from each dependency's end
  to the dependent's start (`plot_gantt_dependency_*`), off by default.
  `show_today` draws a vertical reference line at `today` — `date.today()`
  when not given — through the reference-line machinery with
  `plot_gantt_today_*` style, so it lands on the temporal axis like any
  datetime `vlines` entry.
- **Emphasis is per record.** A task record's `emphasis` key carries an
  `EMPHASIS` role, like a bar record (ADR 0042); the front-level
  `emphasis` applies per figure; `emphasis_rule` reads the task's duration
  in days (a per-record front, so no `by`; ADR 0045).
- **One layer on the bar layer's drawing.** `GanttLayer` builds on
  `BarLayer` — `barh` with `left` at the start and width the duration —
  through the panel's bar slotting rather than copying it; the keys
  specific to a gantt live under `plot_gantt_*` (bar, progress, dependency
  arrow, today line, value labels, z-order), and themes override only
  identity keys. Listed under "trends and comparisons".

## Considered options

- *`orientation` with a vertical mode.* Rejected: rare, and every label
  and arrow placement would need a second path.
- *Overlayable in `Panel`.* Rejected for v1: the line overlay does not
  compose, and gantt-on-gantt needs slotting work with no request yet.
- *A `SORT.GROUP` member.* Rejected: group order is a `sort_by` key,
  not a sort direction — the same split `BarChart` already uses.
