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
  locator and formatter. The front's axis keys are spatial, as
  `PyramidChart`'s and a horizontal `BarChart`'s: `xticks_format` takes a
  `DATE_FORMAT` and `xmin` / `xmax` take datetimes as the time window. The
  category axis (y) holds the task rows, the first task at the top.
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
  `"group"` with no `group` keys raises, and a `sort_by` without `sort`
  raises as it does on the bar fronts.
- **Colour follows the group.** Without `group`, every bar takes the
  layer's cycle colour. With `group`, one colour (and, where the theme
  cycles hatches, one hatch) per group from the multiple palette, in
  first-seen order, and one legend entry per group; the legend is on by
  default only when a task carries a `group`.
- **Progress is an inner bar.** A `progress` fraction draws a second,
  darker bar over that fraction of the range (`plot_gantt_progress_*`);
  a record without `progress` is a plain range. `show_values` is off,
  `"duration"` (days, `"{x:.0f}d"` unless `value_format` is set), or
  `"progress"` (the fraction, `"{x:.0%}"` by default), placed past the bar
  end as bar labels are (ADR 0033). Several task lists draw one schedule
  per subplot.
- **Dependencies and today line are sugar over existing marks.**
  `show_dependencies` draws a `FancyArrowPatch` from each dependency's end
  to the dependent's start (`plot_gantt_dependency_*`), off by default. The
  arrow enters the dependent bar from the top (along the dependency's row,
  then onto the bar) or, with `plot_gantt_dependency_entry` `"left"`, from
  the left (down from the dependency's end, then into the start); a
  dependent starting no later than its dependency ends has no room on the
  left and enters from the top. `show_today` draws a vertical reference
  line at `today` — `date.today()` when not given — through the
  reference-line machinery with `plot_gantt_today_*` style, so it lands on
  the temporal axis like any datetime `vlines` entry; `today_label` prints
  a label at its foot.
- **A zero-length task is a milestone.** A task whose `end` equals its
  `start` draws a marker (`plot_gantt_milestone_*`) instead of an empty
  bar. Under `show_values` it prints its date — a milestone has no
  duration or progress to show — in the `xticks_format`, else as day and
  month. Arrows stop at the marker's edge.
- **Group headers are rows, not a second axis.** `show_group_headers`
  clusters each group's rows in first-seen order, after any `sort`, under
  a header row: the group name in bold on the task axis and a summary bar
  (`plot_gantt_summary_*`) from the group's first start to its last end,
  with `plot_gantt_group_gap` rows before every header but the first. The
  header already names the group, so the legend defaults off; headers
  without any `group` raise. The rows place their own ticks, since header
  and gap rows break the bar ticks' one-row-per-record index.
- **Date ticks run from the first start to the last end.** Without
  `period`, the first start and the last end are always ticks; regular
  ticks step between them in minutes or hours (only when the schedule
  carries times) or days from the first start, or on the first of the
  month for month steps, at most eight steps. Month ticks snap to the 1st
  because ticks stepped from a mid-month start repeated its day as labels.
- **A date axis can be divided into calendar periods.** `period`, a
  `GANTT_DATE_PERIOD` (day, week, month, quarter, year), swaps the concise
  date ticks for period furniture: minor ticks at the period edges carry
  the grid lines, major ticks label each period at the centre of its
  visible part, and a secondary axis one label row below names the
  enclosing month (for days and weeks) or year (for months and
  quarters). A period cut to a sliver by the view goes unlabelled.
  `xticks_format` sets the period labels. The panel owns it, like the
  temporal locator (ADR 0037), so only the setting is gantt-specific.
- **Emphasis is per record.** A task record's `emphasis` key carries an
  `EMPHASIS` role, like a bar record (ADR 0042); the front-level
  `emphasis` applies per figure; `emphasis_rule` reads the task's duration
  in days (a per-record front, so no `by`; ADR 0045).
- **One layer on the bar layer's drawing.** `GanttLayer` builds on
  `BarLayer` — `barh` with `left` at the start and width the duration —
  through the panel's bar slotting rather than copying it. The bars take
  the `plot_bar_*` color, alpha, edge, hatch and z-order keys and the
  shared value label keys; only what is specific to a gantt lives under
  `plot_gantt_*` (bar height, progress, dependency arrow, today line,
  summary bars, group gap, milestones), and themes override only identity
  keys. Listed under "trends and comparisons".

## Considered options

- *`orientation` with a vertical mode.* Rejected: rare, and every label
  and arrow placement would need a second path.
- *Overlayable in `Panel`.* Rejected for v1: the line overlay does not
  compose, and gantt-on-gantt needs slotting work with no request yet.
- *A `SORT.GROUP` member.* Rejected: group order is a `sort_by` key,
  not a sort direction — the same split `BarChart` already uses.
- *Period labels on the edge ticks.* Rejected: a label under an edge
  reads as the instant, not the span; centred labels read as the period,
  as project tools print them.
- *Group headers as a second category axis.* Rejected: a nested axis needs
  its own layout pass; header rows reuse the task axis and the bar drawing.
