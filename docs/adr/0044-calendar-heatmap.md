---
status: accepted
---

# A calendar heatmap draws one panel per year through the heatmap's cell seam

A calendar heatmap (issue #130) shows a daily series as one cell per day,
weeks as columns and weekdays as rows, colored by value: commits, sales,
steps, rainfall. Users hand-built it with `Heatmap`, a computed week grid,
and month ticks worked out by hand. The pieces it needs already exist:
temporal detection (ADR 0037), the heatmap's cells, value labels (ADR
0033), and the colorbar setting (ADR 0035).

## Commitments

- **Input is a `{date, value}` dict per dataset.** `date` holds temporal
  objects only — `date`, `datetime`, `numpy.datetime64`, or pandas
  `Timestamp` — per ADR 0037; a string raises `ValueError` naming the
  accepted types, and no ISO parsing is added. A day absent from the list,
  or valued `None`, is a blank cell: no fill, not the colormap's low end.
- **Duplicate dates raise.** A date appearing twice raises `ValueError`
  naming the first duplicate. Summing or averaging silently would hide a
  data error; an `aggregate` setting is a possible later addition.
- **One panel per year, in year order.** Data spanning several years splits
  in the front into one chart per year and draws through the existing
  subplot layout (`CHART_CONFIGS`: `multiplot: False, subplots: True`), so
  `Grid` rebuilds the arrangement in a cell for free. `year=` keeps one
  year; a year without data raises. The years of one dataset share its
  value range unless `vmin`/`vmax` pin one, so a value takes the same color
  on every calendar. Each year panel is subtitled by its year, after the
  dataset's subtitle when one is given; `max_cols` defaults to 1 so the
  years stack.
- **One layer, the heatmap's seam.** `CalendarHeatmapLayer` subclasses
  `HeatmapLayer`: the cells are an `imshow` raster, the value labels and
  the colorbar are the heatmap's routines, and the style helpers take a
  key prefix so `plot_calendar_heatmap_*` reads through the same code as
  `plot_heatmap_*`. The layer adds only the year layout, the month
  separators, and the month and weekday labels. Value labels take the
  shared `show_values`/`value_format` vocabulary (ADR 0033).
- **A calendar spans the months holding data, whole months at a time.**
  A fourth-quarter series draws October to December, not nine blank
  months; a full year draws the year. Missing days inside that range are
  the blank cells.
- **Layout.** `week_start` is a `WEEKDAY` member (`MONDAY` or `SUNDAY`),
  defaulting to the theme's `plot_calendar_heatmap_week_start`. Month
  separators are stepped lines along the left edge of every month but the
  first, in `plot_calendar_heatmap_month_line_*`. Month labels sit over the
  middle of each month's weeks; every other weekday is labelled, since
  seven labels overlap at the default cell size. `show_month_labels` and
  `show_weekday_labels` turn them off. Cells default to
  `ASPECT_RATIO.EQUAL` and the default figure is wide and short, one row of
  height per row of calendars. The layer hides the spines and tick marks:
  the separators and cell borders are its only lines.
- **The colormap derives from the heatmap's.** `plot_calendar_heatmap_cmap`
  is `None` in the base theme and falls back to `plot_heatmap_cmap`, as the
  contour and hexbin colormaps do (ADR 0022, ADR 0024), so a theme that
  recolors its heatmap recolors its calendars without a second key.
- **A bare figure.** `Panel` rejects it with the "use `Grid`" message the
  other bare charts give (ADR 0026); `Grid` accepts it. The metadata
  transport carries the per-year panels only.

## Considered options

- *Parsing ISO date strings.* Rejected: ADR 0037 commits that strings are
  never dates, and a calendar taking strings would be the one front that
  differs.
- *Aggregating duplicate dates.* Rejected for now: the aggregate is a
  choice (sum, mean, last) the user should make; a later `aggregate`
  setting can add it without changing the strict default.
- *Splitting years inside the layer.* Rejected: the subplot layout counts
  charts, so a year is a chart; splitting in the front reuses the layout,
  the subtitles, and the `Grid` subplot rebuild unchanged.
- *A second cell implementation.* Rejected: the heatmap's raster, value
  labels, and colorbar already do the work; a prefix on the style helpers
  is the whole cost of sharing them.
- *Month labels on the first week of each month.* Rejected after the
  preview: a month starting mid-week puts its label over a column shared
  with the previous month.
- *Labelling all seven weekdays.* Rejected after the preview: the labels
  overlap at the default cell size; every other row reads cleanly.
- *Always drawing the full year.* Rejected after the preview: a partial
  series then sits in a field of empty months with separators through
  nothing.
- *Independent color scales per year.* Rejected: the years of one series
  are one dataset, and a reader compares them.
