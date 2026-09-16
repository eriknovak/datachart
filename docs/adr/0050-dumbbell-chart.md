---
status: accepted
---

# A dumbbell chart is a group layer on the category index, not a bar

A dumbbell chart (issue #135) shows two dots per category joined by a
connector — a before/after change or a min–max range. The dots are scatter
marks and the rows are categories, so two position models were available:
the bar slots a `BarChart` uses (0-based positions, dodged per layer) or the
panel category index the group fronts share (ADR 0020, 1-based, overlaid).

## Commitments

- **A `GroupLayer` on the category index.** Rows come from the panel's
  label → position map, so a dumbbell overlays other dumbbells and the
  group fronts at the category center; several dumbbell layers overlay in
  distinct cycle colours, never dodge. Overlaying a `BarChart` is out of
  scope: bars place categories through bar slots, and unifying the two
  models is its own task.
- **One input shape.** `{label, start, end, emphasis?}` records, one list
  per chart, numeric endpoints only. The two-series `BarChart` shape the
  issue floated is a one-line reshaping on the user's side and would add a
  second validation path. Endpoint names come from chart-level
  `start_name` / `end_name` (the glossary already uses "end label" for a
  series' label at its last point); the legend is on by default only when
  a name is given, as the gantt legend is only with a `group`.
- **`orientation` exists**, default horizontal. Unlike the gantt chart
  (ADR 0049) the category index sets the ticks on either axis, so the
  vertical form costs no second label path.
- **Sort mirrors the gantt chart.** `sort` is a `SORT` member and `sort_by`
  a `DUMBBELL_SORT_KEY` (`start` default, `end`, `delta`); `sort_by`
  without `sort` raises, as on the bar fronts (ADR 0042).
- **Own style family.** `plot_dumbbell_*` keys: start/end colour (`None`
  resolves to the `PaperAccent` pair), size, marker pair, edge width and
  colour, connector colour/width/style, value-label keys, zorder; the
  connector draws under the dots. Themes override only identity keys.
- **Value labels.** `show_values` is a `DUMBBELL_VALUE`: `NONE`,
  `ENDPOINTS` (past each dot, away from the connector), `DELTA` (at the
  connector midpoint). Coincident endpoints draw one dot, no connector,
  and a delta of zero.
- **Gridlines follow the values.** Themes name their default grid for an
  upright chart, where values run along y; a horizontal dumbbell moves that
  default onto x, in its front and in a `Panel`. An explicit `show_grid`
  stays literal.
- **Direction is an opt-in arrow beside the connector.** `show_direction`
  draws a thin `start` → `end` arrow above each horizontal dumbbell (right of
  a vertical one), styled by `plot_dumbbell_arrow_*`, so colour alone need
  not tell a rise from a fall. Arrowheads on the connector itself stay out:
  they would sit under the end dot. A delta label moves out past the arrow.
