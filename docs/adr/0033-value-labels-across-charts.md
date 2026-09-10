---
status: accepted
---

# Value labels are a cross-chart feature with per-geometry placement

`show_values` grew one chart at a time. Seven fronts carry it (bar, pyramid,
radial, sankey, treemap, network, and the heatmap under its own
`show_heatmap_values` name), behind six unrelated drawing implementations that
share only two formatter helpers. Only the bar layer honours the theme default
`chart_default_show_values`. Meanwhile the charts a reader most often wants
numbers on — line, scatter, histogram, stacked area, box, violin — have no way
to print a value beside a mark at all, and three planned charts (calendar
heatmap, gantt, dumbbell) each propose `show_values` again.

We make the value label a single feature of the library rather than a feature
of individual charts.

## Commitments

- **One vocabulary everywhere.** A front that has a value to print takes
  `show_values` and `value_format`, with `VALUE_FORMAT` constants as before.
  A shared `plot_value_*` style family replaces the bar-specific keys; the
  `plot_bar_value_*` names keep working as aliases so existing themes and
  user styles are unaffected.
- **The theme default covers every value label.** `chart_default_show_values`
  applies to every front that takes `show_values`, not only to bars. This
  supersedes ADR 0004's enumeration of the theme-defaultable settings, which
  named "grid visibility and bar value labels" and now reads "grid visibility
  and value labels". Resolution is unchanged: an explicit setting wins, and
  `None` in the theme is still no opinion.
- **Placement belongs to the geometry, not the chart.** Three placers cover
  everything: the panel-level collision-avoiding placer that scatter point
  labels already use, generalised from a scatter-only check to any layer that
  offers labelled points; matplotlib's own bar labelling for bars and
  histogram bins; and a band-midpoint placement for stacked area and for the
  box and violin median. A new chart picks a placer, it does not write one.
- **Line labels sit above or below the mark, never beside it.** A side label
  on a line falls on the line itself, between two points, and reads as
  belonging to either. The candidate spots for a line layer are therefore the
  vertical ones only; scatter keeps the full ring, having no connecting path
  to be confused with.
- **Density is bounded by a setting, not by hope.** `value_step` labels every
  Nth point, defaulting to a step that keeps a dense series readable. The
  collision placer degrades to least-overlap rather than dropping labels, so
  without a step a 200-point line would label into an unreadable mass.
- **A distribution chart labels one statistic.** Box and violin print the
  median beside the median line. Quartiles and whiskers crowd a narrow box,
  and the median is the number readers actually take from it.
- **Charts with no per-mark value stay out.** `ParallelCoords` has no mark
  value, `HexbinChart` has only bin counts already served by its colorbar, and
  `ContourChart` labels its iso-lines through `show_labels`. Adding
  `show_values` to them would name three different things.
- **Labels survive composition**, being drawn by the layer and the panel, as
  every other mark is.

## Considered options

Leaving the theme default bar-only was rejected: a theme that labels bars but
leaves lines and points bare is not a coherent visual identity, which is the
premise ADR 0004 opened the settings boundary for in the first place. The cost
is real — the themes that default value labels on repaint every line, scatter,
histogram and area figure, so their golden baselines change in one batch.

Keeping placement per chart, as the six existing implementations do, was
rejected: it is exactly what made the seventh chart expensive, and three more
are already queued behind it.
