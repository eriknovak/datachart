---
status: accepted
---

# RadialChart is one front with a visual switch, on a projection-aware Panel

Radial charts (wind roses, circular bars, seasonal scatters, angular
histograms) draw the same marks as their cartesian cousins on a polar
coordinate space. Nothing in the package models a coordinate space today:
axes creation is projection-blind, `Panel` furniture assumes cartesian spines
and scales, and composition would silently redraw a polar figure onto a
rectilinear axes. We add one chart front and make the projection a property
of the panel.

## Commitments

- **One front, figure-level visual switch.** `RadialChart(data, type=...)`
  selects the mark family — `RADIAL_TYPE.LINE` (default), `BAR`, `SCATTER`,
  `HISTOGRAM` — for the whole figure. It is the first front with a visual
  switch; mixing visuals in one radial panel is `Panel`'s job, exactly as for
  cartesian charts. Area is `show_area` on line, stacking is `bar_mode` on
  bar — flags, never extra types.
- **Projection is a property of the panel.** A panel is polar when its layers
  are radial, cartesian otherwise; mixing projections in one panel raises
  `ValueError`, in the same place and spirit as mixed orientations
  (ADR 0012). The metadata transport carries the projection so `Panel` merges
  polar with polar and `Grid` creates each cell's axes with its own
  projection; polar and cartesian cells coexist in one grid.
- **Radial marks wear cartesian style keys.** A radial bar obeys
  `plot_bar_*`, a radial line `plot_line_*`, and so on — no `plot_radial_*`
  theme family. Every existing theme styles radial charts untouched.
- **Degrees are the user-facing angular unit.** Categorical labels place
  points evenly around the circle; histogram input is numeric angular
  observations in degrees, binned over [0, 360). Radians never appear in the
  API.
- **Compass and calendar conventions by default.** `startangle` (compass
  string or degrees, default `"N"`), `direction`
  (`DIRECTION.CLOCKWISE`/`COUNTERCLOCKWISE`, default clockwise) and
  `innerradius` (fraction 0–1 of the radial extent, default 0) are chart
  settings. Line visuals close their loop.
- **Impossible settings raise.** `scalex`, `vlines`/`hlines` and anything
  else a polar axes cannot honor raise `ValueError` when passed explicitly —
  the heatmap `emphasis` precedent — never a silent ignore. `subplots=True`
  is supported: one polar axes per chart.
