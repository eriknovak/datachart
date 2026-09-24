# datachart

A Python data visualization package built on matplotlib: a simple chart API over a
global style configuration, with composition of charts into overlays and grids.

## Language

### Composition

**Layer**:
One drawable unit — a single line, bar series, scatter series, histogram, box group,
heatmap matrix, or parallel-coords set — that knows how to put its marks on a
matplotlib Axes. Owns its resolved style, z-order, and legend label; knows nothing
about sibling layers.
_Avoid_: plotter, series (for the drawable), plot function

**Panel**:
A group of layers sharing one coordinate space. Owns everything cross-layer: color
assignment, bar slotting, shared parallel-coords normalization, axis scale and
limits, grid, ticks, legend assembly, and twin-axis assignment. Also the public composition front
(`datachart.utils.Panel`) that overlays rendered figures into one panel.
Panel figures nest: a nested panel flattens into the outer one, keeping its
per-figure prefs while the outermost call supplies all panel-level furniture.
Axis scale and bar mode are the exceptions: axis scale is stamped onto each
layer group as a pref rather than held as furniture, so it survives nesting
and follows its group to whichever axis twin assignment sends it to
(ADR 0041), and a source figure's own `bar_mode` is adopted by a panel that
sets none (ADR 0005). A dropped scale renders a clean but misleading chart
where a dropped label or limit is visible.
A panel has an orientation, inferred from its orientable layers (horizontal
only when all of them are); its value axis follows it.
_Avoid_: overlay (for the concept), subplot, axes group

**Value axis / category axis**:
The two axes of a panel named by role, not by letter: the value axis carries
the quantities (y in a vertical panel, x in a horizontal one), the category
axis the positions or labels. The secondary axis is always a second value axis
(`twinx` vertical, `twiny` horizontal); the `y_axis`, `ylabel_*`, `ymin*`/`ymax*`
and `scaley`/`scaley_right` parameters address the value axis in either
orientation, `xlabel`/`xmin`/`xmax`/`scalex` the category axis. The two value
axes scale independently; the category axis has no twin, so it has no
`scalex_right`.
_Avoid_: left/right axis (for the concept — those are the vertical spellings)

**Grid**:
An arrangement of figures in rows and columns — the public front
(`datachart.utils.Grid`) takes nested rows (the layout you can see; `None` for a
blank cell) or a flat list with `max_cols`/`layout_spec`, and redraws each
figure's panel into its cell. Grid figures nest inside Grid (never inside
Panel): a nested grid occupies one cell and rebuilds its own layout there in
the parent's gridspec, so its axes envelope aligns with sibling cells; its
title becomes a subtitle-sized heading row, its `xlabel`/`ylabel` a footer row
and a left column (figure-level `supxlabel`/`supylabel` at the top level), and
its axis sharing stays local.
_Avoid_: grid layout (for the front), figure grid

**Projection**:
The coordinate space kind of a panel — cartesian or polar. Inferred from the
panel's layers, carried on the metadata transport, and honored when composition
recreates axes: `Panel` merges like with like (mixed projections are an error,
as with orientations), `Grid` gives each cell its own projection.
_Avoid_: polar mode, chart geometry

**Radial visual**:
The mark family a `RadialChart` draws — line, bar, scatter, or histogram —
selected by its `mark` parameter for the whole figure. The one figure-level
visual switch in the package; mixing visuals in one radial panel is `Panel`'s
job.
_Avoid_: radial chart type, type (for the parameter), sub-chart

**Bar slot**:
A bar layer's assigned lane within a category's group of bars. Slots divide the
bar width between the panel's bar layers, and the group is centered on the
category position — so numeric-x layers and ticks line up with group centers.
_Avoid_: bar offset (for the concept), dodge

**Category index**:
A panel's shared map from group label to position on the category axis, built
as the first-seen union of labels across its group-oriented layers (box,
swarm, violin) and handed to each through the `DrawContext`. Positions are
0-based, the first group at 0 like the first bar. The panel sets the category
ticks from it once; layers never place their own groups.
_Avoid_: box positions, group order (for the map)

**Swarm**:
A `SwarmPlot` layer — every raw observation of a group drawn as a point at
that group's category-index position, spread across the category width in
one of two modes: `swarm` (beeswarm — non-overlapping offsets computed from
the marker size) or `strip` (seeded uniform jitter). Overlaid on a box of the
same groups it shares the center; several swarm layers overlay at the same
position in distinct colors rather than dodging, and pack as one cloud so no
point covers another.
_Avoid_: beeswarm (for the chart), strip plot (for the chart), dot plot

**DrawContext**:
The frozen per-layer instructions a panel hands to a layer at draw time — z-order,
legend label, assigned color, and bar slot placement.
_Avoid_: settings (for this), kwargs

**Surface**:
A filled layer that reads as background — stacked area bands, a filled contour,
hexbin tiles. In a `Panel` overlay it draws under the marks, and reference lines
always draw over it.
_Avoid_: raster (for this), fill layer

**Chart front**:
A public chart function (`LineChart`, `BarChart`, …) — its signature is the
allowlist of what the chart supports, its body is any check on what it names
and one engine call with its arguments; it builds no charts structure, no
settings dict, and does not draw.
_Avoid_: chart class, chart type (for the function), attrs dict, forwarding dict

**Key split**:
How the engine sorts a front's arguments: sixteen shared per-chart keys plus
the row's `chart_keys` are indexed against the charts; a row's `figure_keys`
pulls a shared key back to the figure (the pyramid's mirrored `xticks`); every
other argument is a figure setting by complement. Declared on the chart kind,
performed once in the engine, never re-decided in a front.
_Avoid_: forwarding, per-chart dict / settings dict (for the mechanism)

**Chart kind**:
The one record of what a chart front *is* — its layer class, record shape,
projection, group / bare / gridless flags, emphasis unit, multiplot and subplot
rules, rejected parameters, key split, legend default — held as a frozen
`ChartKind` row in one table and read through one accessor. The engine,
builder, and composition branch on the row, never on the chart-type string;
a front with no row fails before drawing.
_Avoid_: chart config, chart registry, chart-type table

**Setting payload**:
A dict a caller passes to a chart front to configure one per-figure element —
a reference line, band, text, legend, or colorbar — as opposed to the chart
dicts (data) or the theme's `plot_*` keys (style). Typed by a
`*SettingAttrs` TypedDict.
_Avoid_: plot attrs, style (for this)

**Pyramid**:
A back-to-back horizontal bar figure (`PyramidChart`): exactly two sides sharing
one category axis, drawn in opposite horizontal directions from a common zero
line. Always horizontal; one call makes one pyramid, small multiples come from
`Grid`, and `Panel` rejects pyramid figures.
_Avoid_: population pyramid (for the front), tornado chart, butterfly chart

**Side**:
One of a pyramid's two bar series — the first is the left side, the second the
right. Sides are supplied and displayed as positive quantities; users never
write or see a signed value.
_Avoid_: wing, half, direction

**Mirror**:
The pyramid's furniture treatment of the value axis: symmetric limits around
zero and absolute-value display on ticks and value labels, so both sides read
as positive magnitudes.
_Avoid_: negative axis, diverging axis

**Violin**:
A per-label kernel-density body (`ViolinPlot`) drawn at the same positions
and with the same API as a box group, so violin and box figures over the same
labels line up in `Panel`. Multiple datasets raise unless `subplots=True`, as
for boxes.
_Avoid_: density plot, bean plot

**Inner**:
The summary marks a violin draws inside its body from the data: `"box"` (thin
quartile bar, 1.5·IQR whisker, median dot), `"quartiles"` (dashed/dotted lines
clipped to the body), `"median"` (one line), or `None`. One enum, never
matplotlib's `showmeans`/`showextrema`/`quantiles` switches.
_Avoid_: inner box flag, show_median

**Split**:
A violin's two halves, one per distinct value of a named point key, colored
from the multiple palette and listed in the legend. Exactly two values;
otherwise an error. Declared by key name like `label`/`value`, never as
nested data.
_Avoid_: hue, half violin, paired violin

**Raincloud**:
A `RaincloudPlot` group — a cloud, a box, and its rain read together at one
category position: the box on the position, the cloud past it on the high
side, and the rain past it on the low side, so nothing overlaps. Assembled
from the violin, swarm, and box layers by the front; nothing new is drawn.
Each group takes its own palette color, shared by cloud, box, and rain.
_Avoid_: raincloud chart (for the front), half-violin plot, rain plot

**Cloud**:
The half of a raincloud's violin body kept on the high side — right in a
vertical plot, above in a horizontal one — with no inner marks; the box is
the summary.
_Avoid_: half violin (for the concept), density half

**Rain**:
A raincloud's swarm, starting just past the box on the side opposite the
cloud and packed one-sided away from it, over a band narrower than a
standalone swarm so it stays inside the category cell.
_Avoid_: strip (for the concept), drops

**Ridge**:
A per-label kernel-density curve of a `RidgelinePlot`, drawn from its row's
baseline on the category index and stacked with the other rows, first row
at the top, later rows above earlier ones. Evaluated through `kde1d` on one
grid shared by every ridge of the panel (ADR 0047).
_Avoid_: joy plot (for the front), density row, layer (for the curve)

**Row overlap**:
How far a ridge rises into its neighbour's row: a peak stands `1 + overlap`
slots above its baseline, so `0` makes rows touch and `0.5` sends each peak
half a row into the next. A front parameter in `[0, 1]` with a theme
default.
_Avoid_: scale (for this), spacing, height

**Ridge scale**:
Whether ridges share one density scale (`RIDGELINE_SCALE.COMMON`: the
tallest ridge reaches the peak height, the rest in proportion) or each is
scaled to the same peak (`PER_ROW`, the default: shapes compare). Passed
as `ridge_scale`; distinct from the heatmap's `COLOR_NORM` colormap norm.
_Avoid_: normalization, normalize (for the parameter), common scale (for
the enum)

**Reference line**:
A straight line drawn against the data as a marker, not a series — a threshold,
a date, a parity or chance line. Declared with the chart in three families by
what fixes the line: `vlines=` (an x position), `hlines=` (a y position), and
`dlines=` (a slope and an intercept, defaulting to the parity line `y = x`).
Stored on the layer, drawn by the panel after limits are set — so it survives
composition — and never takes a cycle color, a bar slot, or a legend entry
unless labelled. A diagonal line lives in data space: straight on linear axes
only.
_Avoid_: guide line, abline, parity line (for the setting; it is one value of it)

**Bracket**:
A pairwise-comparison mark on the category axis: a line spanning two
categories with a tick at each end pointing toward the data and an optional
text (a p-value, a star) centred beyond it. Declared with the chart
(`brackets=`) as a fourth reference-mark family; `from` and `to` name the
categories by label (or a numeric position), `y` optionally pins the
value-axis position. Unpinned brackets stack above the data in their span
without overlapping and grow the value axis to fit. Follows the panel
orientation. Stored on the layer, drawn by the panel after limits are set —
so it survives composition — and never takes a cycle color, a bar slot, or a
legend entry.
_Avoid_: significance bar, annotation bracket, hline pair (for the workaround)

**Text**:
A per-chart annotation — a string placed at a position (data coordinates by
default, axes-fraction on request) with an optional arrow to a target point,
a styleable font, background box, and connector. Declared with the chart
(`texts=`) like reference lines, stored on the layer, drawn by the panel after
limits are set — so it survives composition.
_Avoid_: annotation (for the API name), callout, note

**Annotate**:
The post-hoc front (`datachart.utils.Annotate`) that adds texts to an already
rendered figure by appending a carrier text layer (no data, no legend or color
participation) to its panel and re-rendering. On a multi-subplot figure each
text names its target with a `subplot` index (0-based, render order) and the
carrier rides that per-subplot panel only, never the combined panel; the
figure is rebuilt the way a grid cell rebuilds it. Rejects grid figures —
annotate the sources before composing.
_Avoid_: overlay text, label function, axes index (for `subplot`)

**Band**:
A shaded region behind the data marking an interval — a confidence range, a
recession period, an acceptable range. Declared with the chart (`vspans=` for
a band bounded on the x axis, `hspans=` for one bounded on the y axis) like
reference lines, stored on the layer, drawn by the panel over the grid and
under the marks — so it survives composition. An omitted bound runs to the
axis limit. On a polar axes a `vspan` is a wedge bounded in degrees and an
`hspan` an annulus bounded in radius.
_Avoid_: span (for the concept), region, shading, highlight

**Point label**:
A scatter point's name, read from the data key the `label` parameter names
(`label="name"`, off when unset) and drawn beside its marker in the text
font. The panel places all of a coordinate space's point labels at once,
after limits are final: each takes the spot around its marker with the least
overlap against every marker in the panel, the labels already placed, the
correlation box, and the axes edge. A crowded label is placed at its
least-overlap spot, never dropped; a background layer's labels take the muted
color.
_Avoid_: annotation (for this), tag, name label, adjusted text

**Error bar**:
A scatter point's uncertainty in either variable, read from the data keys the
`xerr` and `yerr` parameters name. A value is a distance from the point: one
number reaches the same distance both ways, a `[low, high]` pair reaches
`low` below and `high` above. A point without one draws none. Each side runs
from the edge of its marker outward, in the point's own colour — so a hue
group's bars match its markers — and dims with it under emphasis; hover
reports the distances beside the point's values. A bubble's size widens the
gap the bar starts at, never the bar. Scatter matrices, hexbins, and contours
have no error bars.
_Avoid_: error band (that is a line chart's `yerr`), confidence interval (for
the value), whisker, uncertainty range

**Bump chart**:
Rank over time (`BumpChart`: an `{x, y}` point list per series, one line
each) drawn with rank 1 at the top of an integer y-axis. `rank_by` (a `BUMP_RANK`
member) says whether `y` is already a rank (`GIVEN`) or a value ranked per
period (`VALUE_DESCENDING`, the default, highest first; `VALUE_ASCENDING`,
lowest first). A series absent at a period leaves a gap and is not ranked
there. Overlayable in `Panel` like a line chart.
_Avoid_: rank chart, slope chart (two periods only), ranking line chart

**Gantt chart**:
A schedule (`GanttChart`): one horizontal range bar per task from its `start`
to its `end` on a temporal value axis, one row per task on the category axis.
Always horizontal; a bare figure — `Grid` yes, `Panel` rejects it.
_Avoid_: timeline chart, schedule chart, range bar chart

**Task**:
One record of a gantt chart: a `task` name (its row label), a `start` and an
`end` (real temporal objects, never strings), and optionally a `group`, a
`progress` fraction, and the names it `depends_on`.
_Avoid_: activity, job, bar (for the record)

**Task group**:
The `group` a task belongs to: tasks of one group share a colour and a legend
entry, and `sort_by="group"` clusters their rows together, groups ordered by
their earliest start.
_Avoid_: resource, category (for the key), swimlane

**Dependency**:
A task named in another task's `depends_on`, drawn under `show_dependencies`
as an arrow from the dependency's end to the dependent's start.
_Avoid_: predecessor, link, edge (for the arrow)

**Today line**:
The vertical reference line a gantt chart draws at `today` (the current date
by default) under `show_today`, labelled by `today_label`.
_Avoid_: now line, current-date marker

**Milestone**:
A task whose `end` equals its `start`, drawn as a marker instead of a bar.
_Avoid_: event, zero-duration task

**Group header**:
Under `show_group_headers`, the row above a task group's rows naming the group,
with its summary bar from the group's first start to its last end.
_Avoid_: swimlane header, parent task

**Date period**:
The calendar unit (`period`: day, week, month, quarter, year) a date axis is
divided into: edge lines, a label centred in each period, and a row naming the
enclosing month or year.
_Avoid_: time bucket, date bin

**Dumbbell chart**:
A comparison (`DumbbellChart`): per category, a dot at `start` and a dot at
`end` joined by a connector, showing a change between two states or a range.
A group layer on the category index — it overlays other dumbbells and the
group fronts, not bars; `orientation` picks the category axis.
_Avoid_: range chart, connected dot plot, Cleveland dot plot (for the chart)

**Scatter matrix**:
A relationship view (`ScatterMatrix`): an n × n grid figure with a scatter
chart for every pair of numeric `dimensions` and each dimension's
distribution on the diagonal (histogram, KDE curve, or blank), optionally
coloured by a categorical `hue` with one figure-level legend on one of the
four outside edges, titled by the hue column. Composed from scatter and
histogram cells through the grid transport, so it nests in `Grid` and never
in `Panel`; by default it is at most a full page width wide (ADR 0051).
_Avoid_: pair plot, pairs plot, SPLOM (for the chart name)

**Upper triangle**:
The cells of a scatter matrix above the diagonal; they mirror the lower
triangle, so `show_correlation` replaces them with the Pearson r per hue
group and `lower_only` blanks them.
_Avoid_: mirror cells

**Endpoint**:
One of a dumbbell's two dots — the `start` or the `end` of every record.
The two endpoints share one colour and one legend entry each, named by the
chart's `start_name` / `end_name`; the legend is on by default only when a
name is given.
_Avoid_: state, side, series (for an endpoint)

**Connector**:
The line a dumbbell draws between a record's two endpoints; absent when they
coincide.
_Avoid_: link, bar (for the line), range line

**Direction arrow**:
The thin, optional arrow (`show_direction`) drawn beside a dumbbell's
connector, pointing from `start` to `end`; absent when the endpoints coincide.
_Avoid_: trend arrow, arrowhead (for the whole mark)

**Delta**:
`end - start` of one dumbbell record: a sort key (`sort_by="delta"`) and a
value label (`show_values="delta"`) printed at the connector midpoint.
_Avoid_: change, difference, gap

**End label**:
A series' label (its `subtitle`) printed beside its first and/or last point in the series
color (`show_labels`, with `label_position` a `BUMP_LABEL_POSITION` member), so the
line is named where it ends instead of in a legend.
_Avoid_: direct label (for this), line label, legend label

**Heatmap**:
A per-cell matrix (`Heatmap`: a 2-D `z` grid per chart with optional `x`, `y`
labels for its columns and rows) drawn as one colored cell per value at
integer positions. `x`/`y` are tick labels, not coordinates — uneven spacing
never changes cell size; that is the contour's job. A bare figure: rejected
in `Panel`, a cell in `Grid`.
_Avoid_: matrix plot, image plot, colormesh

**Calendar heatmap**:
A daily series (`CalendarHeatmap`: a `{date, value}` dict per dataset,
temporal dates only, each once) drawn as one cell per day, weeks as
columns and weekdays as rows from `week_start` (a `CALENDAR_WEEKDAY` member), with
stepped month separators and month/weekday labels. Data spanning several
years draws one panel per year sharing one value range; `year` keeps one.
The heatmap's cells, value labels, and colorbar, under
`plot_calendar_heatmap_*` keys. A bare figure: rejected in `Panel`, a cell
in `Grid`.
_Avoid_: contributions graph, GitHub calendar, date heatmap

**Centred norm**:
A heatmap value norm that fixes one value (`vcenter`, default `0`) to the
middle of the colormap: `COLOR_NORM.CENTERED` spans the same distance to each
side of it, `COLOR_NORM.TWOSLOPE` lets `vmin` and `vmax` sit at unequal
distances. Both draw with the theme's diverging colormap, so the sign of a
correlation or a difference reads as a hue and the centre as its neutral.
_Avoid_: diverging norm, symmetric norm, midpoint norm

**Diverging colormap**:
A theme's second heatmap colormap (`plot_heatmap_cmap_diverging`; the
calendar heatmap's derives from it): two hues meeting at a neutral middle,
taken by a centred norm in place of the sequential `plot_heatmap_cmap`. A
chart-level `plot_heatmap_cmap` still wins.
_Avoid_: bipolar colormap, signed colormap

**Contour**:
A gridded surface (`ContourChart`: 1-D `x`, `y` axes and a 2-D `z` grid per
chart) drawn as iso-lines in the chart's cycle color or, when `filled`, as
colormapped bands between levels. Lists overlay on one axes like histograms
do; `subplots=True` grids them. Also the 2-D density chart: `stats.kde2d`
estimates the grid, `ContourChart` draws it — there is no `KDEChart`.
_Avoid_: isoline chart, contourf chart, surface plot, KDE chart

**Hexbin**:
A hexagonal tiling of the plane (`HexbinChart`: 1-D `x`, `y` columns per
chart, optional `c`) colored per tile by point count or, with `c`, by a
`HEXBIN_REDUCE` aggregate. The dense-scatter alternative; shares the raster
color attrs (`norm`, `vmin`, `vmax`, `colorbar`) and furniture (grid off,
colorbar inset) with Heatmap and filled Contour.
_Avoid_: hex density plot, hexagonal heatmap, 2-D histogram

**Image**:
A picture placed in the data's coordinate space (`ImageChart`: a file path, a
PIL image, an RGB(A) array, or a 2-D array read through a colormap), anchored
by an `extent` (`xmin`, `xmax`, `ymin`, `ymax`) that its pixels stretch to
fill. Carries no series, so it takes no cycle color, no legend entry and no
emphasis. `position` (a `DRAW_POSITION` constant) picks its rung on the
draw-order ladder, `BELOW` every mark by default. Composed under or over
another chart with `Panel`, never declared on one.
_Avoid_: underlay, background, raster, watermark (that is one use of
`position=ABOVE`)

**Basemap**:
The land under a geographic chart (`BasemapChart`: coastlines, land fill,
country areas, country borders, lakes, rivers and roads, picked with
`BASEMAP_FEATURE`; `highlight` picks countries out by code), drawn from
Natural Earth outlines rather than computed. No outlines ship with the
package: every `BASEMAP_RESOLUTION` scale is downloaded on first use and kept
in the cache (ADR 0062).
Shares `DRAW_POSITION` with the image, `BELOW` by default. Composed under a chart
whose x and y are already longitude and latitude — it transforms nothing, so
the marks it sits under need no transform either.
_Avoid_: map, coastline chart, shapefile, geometry (for the front), tile layer

**Cache**:
The folder holding every asset the package downloads rather than ships: the
basemap outlines and the theme faces (ADR 0062, 0063). Located by
`DATACHART_CACHE_DIR`, else `datachart` under `XDG_CACHE_HOME` or `~/.cache`.
It is the user's to manage, and seedable in one command for a machine with no
network at render time. Nothing in the wheel is data; everything data is here.
_Avoid_: bundle, package data, assets folder, vendored data

**Geographic aspect**:
The axes shape that keeps a small region's proportions right when longitude
and latitude are plotted straight: one degree of longitude is narrowed by the
cosine of the mid latitude. Requested with `aspect_ratio="geographic"`, off
by default, and available to every chart rather than only the basemap.
_Avoid_: projection (it is not one), equal aspect, scale factor

**Extent**:
The data-space rectangle an image's pixels are stretched to fill, given as
`(xmin, xmax, ymin, ymax)`. Participates in the panel's data limits like any
other layer's span, so an image wider than the data widens the axes; `xmin`
and the other limit settings narrow it back.
_Avoid_: bounds, bbox, footprint, georeference

**Stacked area**:
Series filled on top of one another along an ordered axis
(`StackedAreaChart`: `LineChart`'s multi-series `{x, y}` input, identical
`x` across series). The stack offsets are a panel concern like bar slotting;
`baseline` (a `STACKED_AREA_BASELINE` constant: `ZERO`, `PERCENT`, `SYM`, `WIGGLE`,
`WEIGHTED_WIGGLE`) picks where the first series starts, with `PERCENT`
normalising each `x` to 100 %.
_Avoid_: stackplot, streamgraph (only the wiggle baselines), 100 % chart,
area chart (that is `LineChart(show_area=True)`)

**Sankey**:
Weighted flows between nodes laid out in columns (`SankeyChart`: a `links`
list of `{source, target, value}` records; a node is its name). Columns are
the longest path from a source unless `nodes=[[...], ...]` sets them; ribbons
are Bézier patches whose height is the value, coloured by source. One layer
per chart, no furniture; rejected in `Panel`, a cell in `Grid`.
_Avoid_: flow chart, alluvial (that implies time-ordered axes), network graph

**Network**:
Relational data as a node-link diagram (`NetworkChart`: a `{nodes, edges}`
dict, a node `{id, label?, size?, group?, emphasis?}`, an edge `{source,
target, weight?}`; nodes may be inferred from edges). `layout` takes a
`NETWORK_LAYOUT` constant (`SPRING`, seeded in-package Fruchterman–Reingold;
`WEIGHTED`, the spring with each edge's pull set by its weight; `GROUPED`,
a plain spring inside each group and a weighted one between the groups;
`CIRCULAR`; `FIXED` from per-node `x`/`y` in 0–1, inset by the layout
margin like the others); `directed` adds arrowheads.
Weight maps to edge width, and to pull only under the two layouts named for
it; size by square root to marker area; `group` to the multiple color cycle,
an ungrouped node beside groups taking the edge color. A **cluster** is the
nodes of one group as `GROUPED` places them: a compact patch arranged by the
group's own edges, marked by a translucent disc in the group color (the
**halo**, `plot_network_group_alpha`). A **component** is a set of nodes
joined by edges to each other and to no other node; an **isolate** is a
component of one. Under `SPRING` and `WEIGHTED` a disconnected graph lays out
each component on its own, packs them like clusters, and rings the isolates
around them. One layer per chart, no furniture; rejected in `Panel`, a
cell in `Grid`. Scale: one patch per edge and an O(n²) spring layout —
comfortable up to ~1k nodes / 3k edges (spring, weighted, grouped) or ~5k /
15k (circular, fixed); documented as the practical ceiling, not enforced.
_Avoid_: graph (a synonym for chart), node-link diagram, force graph

**Connector style**:
The one constant for every drawn connector, `ARROW_STYLE`: geometry
(`CURVE`, `STRAIGHT`) crossed with an arrowhead (`CURVE_ARROW`, `ARROW`),
plus `TOUCHING` (straight, flush at the text box). Text annotations accept
every member; network edges accept only the headless two, since `directed`
owns the arrowhead. Each chart's docs say which members it takes.
_Avoid_: edge style (as a separate constant), line style (that is `LINE_STYLE`)

**Treemap**:
Part-of-whole data tiled as rectangles whose area is the value (`Treemap`: a
`data` list of `{label, value}` records, a record's `children` nesting to
four levels). Every level is sorted descending and squarified in the axes'
pixel aspect; a group at any level is a box filled in its color with a
header band that degrades to a border alone when short, its children inset
by a gutter of that color and sharing one tint a level lighter. Labels wrap, then shrink to
a minimum size, then drop. One layer per chart, no furniture; rejected in `Panel`, a cell in
`Grid`.
_Avoid_: tree map, tile chart, mosaic plot (that is a different encoding)

**Per-record emphasis**:
An `emphasis` key on a treemap record (group or leaf, leaf wins) or a network
node carrying an `EMPHASIS` role. Roles stay explicit per item: `highlight` bolds the tile's
border only, `background` mutes it (a node's edges with it), neither changes its
siblings. The front's per-chart `emphasis` argument is rejected for treemaps
and networks.
_Avoid_: focus, selected group

**Density estimate**:
A Gaussian kernel density (`stats.kde1d` → `{x, y}` points for `LineChart`,
`stats.kde2d` → an `{x, y, z}` dict for `ContourChart`) on a grid that extends
`cut` bandwidths past the data so the estimate tails off instead of being
clipped. `bandwidth` takes a `BANDWIDTH` rule or a scalar factor, as violins do.
_Avoid_: KDE plot, density chart (as a chart type)

**Smoother**:
A stats helper that turns a noisy series into a readable one — `rolling_mean`
and `ewma` return a `List[float]` aligned to the input index (`nan` until the
window fills), `loess` returns `{x, y}` points sorted by `x` for `LineChart`,
as `kde1d` does. Shapes follow each function's arity, not the chart that draws
them (ADR 0038).
_Avoid_: trend line (that is the drawn mark), moving average (for the group)

**Bin rule**:
A named rule that picks histogram bin edges from the data — `stats.histogram`
passes `bins` straight to `numpy.histogram_bin_edges`, so `"auto"`, `"fd"`,
`"rice"`, an integer, and an explicit edge list all work. Unrelated to the
`CONTOUR_LEVELS` rules of the same name, which count contour levels from grid
resolution; and the `Histogram` front still takes an integer `num_bins`.
_Avoid_: binning strategy, bin count (for the rule)

**Level**:
One `z` value at which a contour line is drawn or a band boundary falls.
Defaults to matplotlib's auto count; a `CONTOUR_LEVELS` rule (`AUTO`, `RICE`,
`FD`), an int, or an explicit list overrides it. Rules are evaluated on the
per-axis grid resolution, never on the raw cell count.
_Avoid_: iso value, threshold, bin (for contours)

**Category sort**:
The order the categories of a bar-type front are drawn in — input order by
default, ascending or descending by value under `sort`. One order serves every
series in the chart, keyed by the total across them or by the one series
`sort_by` names; a category that series does not carry sorts last, and ties
keep input order (ADR 0042). Box, violin and ridgeline fronts sort their
groups by median instead. Never a sort by label.
_Avoid_: ordering, rank, bar order

**Metadata transport**:
The chart spec riding on a rendered figure (`figure._chart_metadata`) so composition
functions (`Panel`, `Grid`) can rebuild it. Carries layers and panel settings, not
raw attribute dicts; grid figures carry a recursive cell tree instead of a panel.
_Avoid_: snapshot (for this), chart data

### Figure lifecycle

**Unmanaged figure**:
A figure datachart returns: owned by the caller and garbage-collected like any
object, never registered in pyplot's global figure manager. Creating one never
displays it and never accumulates global state; `plt.close` on it is a no-op.
_Avoid_: pyplot figure, open figure

**Show**:
The explicit act of displaying an unmanaged figure, via its `show()` method —
inline display in notebooks, a GUI window in scripts, and the only way a
figure appears in either. Defining a figure and showing it are separate
decisions; a figure left as a cell's last expression renders only its text
repr.
_Avoid_: plot (for the act), display (for the method name)

**Interactive figure**:
A figure shown with `show(interactive=True)`: zoomable and pannable — on an
`ipympl` widget canvas in notebooks, in the GUI window's toolbar in scripts —
with hover-to-inspect annotations on its hover targets. The flag on `show()`
is the only opt-in; chart fronts, `Panel`, `Grid`, and the config carry none,
and the default show is unchanged. Needs the `interactive` extra (`ipympl`,
`mplcursors`); a missing package raises, never falls back to static.
_Avoid_: widget mode, live figure, interactive backend (for the concept)

**Hover target**:
An `(artist, resolver)` pair a layer registers while drawing — a line, a
scatter collection, a bar container, a heatmap image, a box — where
`resolver(i)` returns the datum behind the artist's i-th element as an
ordered dict: the legend `label`, then the fields the mark stands for. The
`x` and `y` fields are named after the axes they are drawn on; every other
field (`value`, `median`, `count`, `angle`, …) is shown under its own key,
in insertion order. Aggregate marks report their summary — a box its
quartiles, a histogram bin its range and count, a sankey link its endpoints
and flow. The panel collects the pairs onto the figure it draws into, so
`show()` attaches hover cursors without knowing chart types; a layer that
registers nothing has no hover. Every data layer registers; text layers and
reference lines do not.
_Avoid_: pickable, tooltip source, hover artist

### Styling

**Theme**:
A complete, named set of style attributes (`DEFAULT`, `GREYSCALE`, `MINIMAL`,
`MATERIAL`, `INK`, `HATCH`, `SKETCH`, `QUILL`, `HARBOR`, `MUTED`, `CONTRAST`,
`MUTEDHATCH`, `SLATEHATCH`, `DARK`). Applying one replaces the whole global
configuration. Themes are named for their visual trait, never for a use case
or audience. A theme is complete on its own: every furniture colour matches
its face, so a dark theme carries light furniture (ADR 0058).
_Avoid_: publication, academic, background (former role-based theme names),
dark mode (a flag; `DARK` is a theme)

**Lead**:
The colour source a theme's palettes descend from: a sequential colormap
(the value scale is the lead itself, the series palette and the parallel
coords ramp are sampled from it) or a categorical palette (the series
palette is the lead, the value scale is the base's). A lead is sequential
when its lightness runs one way; a diverging map is never a lead.
_Avoid_: primary colour, accent, brand colour

**Derived theme**:
A theme built from a base theme and a lead: the base's furniture, fonts,
hatches and rendering unchanged, its lead-dependent palettes rebuilt from the
new lead. It is a plain theme dictionary, applied like any hand-written one.
_Avoid_: theme variant, recoloured theme, sub-theme

**Font stack**:
The ordered face names a theme offers for a generic family, resolved to the
ones this machine can actually use and closed with the generic family itself.
A face a theme calls its own is downloaded into the cache the first time a
stack naming it is resolved; one that cannot be fetched warns and drops out,
leaving the next name in the stack to carry the text (ADR 0063).
_Avoid_: font family (the generic one), typeface list, bundled font

**Furniture**:
Everything the panel dresses an axes with around the marks: spines, ticks,
axis and tick fonts, grid, limits, legend, value labels, annotation text,
heatmap frame and edges, colorbar labels. Its colours contrast with the face
rather than carry data; marks and their colour cycles are not furniture.
_Avoid_: chrome, decorations

**Active theme**:
The name of the theme last applied, held on the configuration as `theme` and
kept in step with the style dictionary — `set_theme`, `reset_config`, and a
theme scope all move the two together.
_Avoid_: current theme, selected theme

**Theme file**:
A JSON document carrying a theme's name, a format version, and only the style
attributes that differ from the base theme (ADR 0040). It is a portable theme,
not a dump of the live configuration, and loading one registers it without
applying it.
_Avoid_: config file, theme export, style sheet

**Scope**:
A context-managed temporary style change — `override` for attributes,
`using_theme` for a whole theme — that restores the state that entered it when
the block ends, exceptions included. Changes made inside the block are
discarded at exit (ADR 0040).
_Avoid_: temporary config, config stack, style context

**Emphasis**:
A role — `"background"`, `"highlight"`, or unset — deciding how something
reads relative to its siblings: background is muted and dropped from the
legend, highlight is nudged forward (front z-order, slightly bolder). Styling,
not data. Set per chart, per figure in `Panel`, per group label on the group
fronts, per record on the fronts whose records carry an `emphasis` key
(treemap, network, bar, scatter, swarm), or per cell on a heatmap. A scatter or
swarm record's own role wins over its series or group role.
_Avoid_: background theme, de-emphasis flag

**Emphasis rule**:
A dict with one comparison — `above`, `below`, `between`, `top`, or `bottom` —
that reads a value for each emphasis unit of a front (record, cell, group
label, or series) and assigns it `"highlight"` when it matches and
`"background"` when it does not. Groups and series are reduced to one value by
a summary, chosen with an optional `by`. Sugar over the explicit roles, which
win wherever one is set (ADR 0042, ADR 0045).
_Avoid_: threshold, emphasis filter, highlight rule

**Muted**:
The style transform emphasis applies to a background layer: theme's muted color,
lowered alpha, thinner strokes, pushed-back z-order, no legend entry. Defined
once, derived from the active theme's `muted_*` attributes — never a separate
theme.
_Avoid_: greyed-out, background style

**Marker edge rule**:
A filled marker (scatter, bubble, swarm, radial scatter, network node) keeps
its theme edge only while the stroke stays under a sixth of the marker
diameter; a smaller marker draws with no edge, per marker for data-sized
ones. A highlight edge is the emphasis cue and always stays. Hollow markers
(box outliers) and unfilled ones (`"x"`, `"+"`) are exempt — their edge is
the marker, drawn in the series color.
_Avoid_: edge threshold, min marker size

**Value label**:
The number a chart prints beside a mark it has already drawn, turned on with
`show_values` and rendered through `value_format`. It is derived from the
data, unlike a text annotation, which the caller writes and positions. A
distribution chart's value label is its median. `show_values` only says
whether; a front with more than one candidate number (the gantt's duration
or end, the dumbbell's endpoints or delta) picks which through `value_kind`.
_Avoid_: data label, annotation, callout

**Shared parameter**:
A front parameter that means the same thing on every front that has it —
`show_values`, `value_format`, `orientation`, `figsize`, `texts`, the
colormap `norm` and `vcenter`, and their peers. It carries one name, one
type and one signature default everywhere; a front that needs its own
default (the dumbbell's horizontal orientation) supplies it behind the
signature, never in it. A parameter that selects something only one front
has — the network's `layout`, the swarm's `mode`, the scatter matrix's
`diagonal`, the bump's `rank_by`, the radial's `mark` — is not shared and
keeps its own noun.
_Avoid_: common parameter, variant (for the per-front selectors)

**Theme-level default**:
A nullable theme attribute that supplies the default for a per-chart setting
(grid visibility, value labels) when the chart call leaves it unset. An
explicit chart setting always wins.
_Avoid_: forced setting, theme override

**Sketch attributes**:
The theme's hand-drawn look: the path wobble, snapshotted by the panel and
applied inside a scoped rc context, and the halo, a layer style stroked under
series lines only; `None` means off. The set is exactly those two attributes;
nothing global changes.
_Avoid_: xkcd mode, rc theme

**Ink attributes**:
The theme's quill-and-ink look (ADR 0048): the ink stroke (a series
line drawn as a broad-nib ribbon), the etch (a hatched fill drawn as
hand-etched lines over a wash), and the value etch (a value scale drawn as
wash-and-etch steps with a step legend in place of the colorbar). Each rides
on its artists; `None` means off.
_Avoid_: fantasy mode, rc path effects

**Hatch cycle**:
A theme-defined sequence of hatch patterns the panel assigns per bar/histogram
series, the same way it assigns colors; etched areas take it too (ADR 0048).
Off (`None`) in every theme but `HATCH` and `QUILL`; an explicit per-chart
hatch style wins.
_Avoid_: hatch palette

**Figure size grid**:
The `FIG_SIZE` vocabulary: a width axis (`FULL_*` the A4 text block at
standard print margins, `HALF_*` one of its two columns, gap included; in/cm
stated in the docstring) crossed with a height axis (`SHORT`, `MEDIUM`,
`TALL`, `SQUARE`), plus the A4 printable area in both orientations, one
free-standing square, and slide frames (`SLIDE_*` PowerPoint-scale,
`BEAMER_*` LaTeX-scale). Height words describe heights; width words widths.
_Avoid_: narrow/regular/wide (former height suffixes), Letter sizes

**Legend setting**:
The per-figure legend controls — title, location, column count, alignment —
passed to a front as `legend` and falling back to the theme's `plot_legend_*`
attributes field by field. An outside location is not a matplotlib location:
it expands, once, into a location plus an anchor that no public surface names
(ADR 0034). An outside-top legend sits between a title and the axes.
_Avoid_: legend style (that is the theme-key family), bbox anchor

**Colorbar setting**:
The per-figure colorbar controls — label, location, tick format, tick
positions — passed to a front as `colorbar` on Heatmap, filled Contour, and
Hexbin. `location` is a `COLORBAR_LOCATION` edge and is what the bar follows;
`orientation` stays accepted and derives the edge when no location is given
(ADR 0035). A left or bottom bar on a single-axes figure moves that axis label
onto the axes, beside its ticks; tick positions outside the mapped value range
are not drawn.
_Avoid_: color legend, colorbar style, scale bar

**Style resolution**:
Collapsing `global config → theme → chart-specific style` into one concrete style,
performed once when a layer is built — never at draw time.
_Avoid_: config snapshot
