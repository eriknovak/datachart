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
A panel has an orientation, inferred from its orientable layers (horizontal
only when all of them are); its value axis follows it.
_Avoid_: overlay (for the concept), subplot, axes group

**Value axis / category axis**:
The two axes of a panel named by role, not by letter: the value axis carries
the quantities (y in a vertical panel, x in a horizontal one), the category
axis the positions or labels. The secondary axis is always a second value axis
(`twinx` vertical, `twiny` horizontal); the `y_axis`, `ylabel_*`, `ymin*`/`ymax*`
parameters address the value axis in either orientation, `xlabel`/`xmin`/`xmax`
the category axis.
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
selected by its `type` parameter for the whole figure. The one figure-level
visual switch in the package; mixing visuals in one radial panel is `Panel`'s
job.
_Avoid_: radial chart type (for the parameter), sub-chart

**Bar slot**:
A bar layer's assigned lane within a category's group of bars. Slots divide the
bar width between the panel's bar layers, and the group is centered on the
category position — so numeric-x layers and ticks line up with group centers.
_Avoid_: bar offset (for the concept), dodge

**Category index**:
A panel's shared map from group label to position on the category axis, built
as the first-seen union of labels across its group-oriented layers (box,
swarm, later violin) and handed to each through the `DrawContext`. The panel
sets the category ticks from it once; layers never place their own groups.
_Avoid_: box positions, group order (for the map)

**Swarm**:
A `SwarmPlot` layer — every raw observation of a group drawn as a point at
that group's category-index position, spread across the category width in
one of two modes: `swarm` (beeswarm — non-overlapping offsets computed from
the marker size) or `strip` (seeded uniform jitter). Overlaid on a box of the
same groups it shares the center; several swarm layers overlay at the same
position in distinct colors rather than dodging.
_Avoid_: beeswarm (for the chart), strip plot (for the chart), dot plot

**DrawContext**:
The frozen per-layer instructions a panel hands to a layer at draw time — z-order,
legend label, assigned color, and bar slot placement.
_Avoid_: settings (for this), kwargs

**Chart front**:
A public chart function (`LineChart`, `BarChart`, …) — a thin front that validates
input and hands the engine an explicit charts structure and settings dict; it does
not draw, and its signature is the allowlist of what the chart supports.
_Avoid_: chart class, chart type (for the function), attrs dict

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
labels line up in `Panel`. Multiple datasets require subplots, as for boxes.
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
participation) to its panel and re-rendering. Rejects grid figures — annotate
the sources before composing.
_Avoid_: overlay text, label function

**Heatmap**:
A per-cell matrix (`Heatmap`: a 2-D `z` grid per chart with optional `x`, `y`
labels for its columns and rows) drawn as one colored cell per value at
integer positions. `x`/`y` are tick labels, not coordinates — uneven spacing
never changes cell size; that is the contour's job.
_Avoid_: matrix plot, image plot, colormesh

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

**Stacked area**:
Series filled on top of one another along an ordered axis
(`StackedAreaChart`: `LineChart`'s multi-series `{x, y}` input, identical
`x` across series). The stack offsets are a panel concern like bar slotting;
`baseline` (a `BASELINE` constant: `ZERO`, `PERCENT`, `SYM`, `WIGGLE`,
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

**Density estimate**:
A Gaussian kernel density (`stats.kde1d` → `{x, y}` points for `LineChart`,
`stats.kde2d` → an `{x, y, z}` dict for `ContourChart`) on a grid that extends
`cut` bandwidths past the data so the estimate tails off instead of being
clipped. `bandwidth` takes a `BANDWIDTH` rule or a scalar factor, as violins do.
_Avoid_: KDE plot, density chart (as a chart type)

**Level**:
One `z` value at which a contour line is drawn or a band boundary falls.
Defaults to matplotlib's auto count; a `CONTOUR_LEVELS` rule (`AUTO`, `RICE`,
`FD`), an int, or an explicit list overrides it. Rules are evaluated on the
per-axis grid resolution, never on the raw cell count.
_Avoid_: iso value, threshold, bin (for contours)

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

### Styling

**Theme**:
A complete, named set of style attributes (`DEFAULT`, `GREYSCALE`, `MINIMAL`,
`MATERIAL`, `INK`, `HATCH`). Applying one replaces the whole global
configuration. Themes are named for their visual trait, never for a use case
or audience.
_Avoid_: publication, academic, background (former role-based theme names)

**Emphasis**:
A per-chart (and, in `Panel`, per-figure) role — `"background"`, `"highlight"`,
or unset — deciding how a layer reads relative to its siblings: background
layers are muted and dropped from the legend, highlight layers are nudged
forward (front z-order, slightly bolder). Styling, not data.
_Avoid_: background theme, de-emphasis flag

**Muted**:
The style transform emphasis applies to a background layer: theme's muted color,
lowered alpha, thinner strokes, pushed-back z-order, no legend entry. Defined
once, derived from the active theme's `muted_*` attributes — never a separate
theme.
_Avoid_: greyed-out, background style

**Theme-level default**:
A nullable theme attribute that supplies the default for a per-chart setting
(grid visibility, bar value labels) when the chart call leaves it unset. An
explicit chart setting always wins.
_Avoid_: forced setting, theme override

**Hatch cycle**:
A theme-defined sequence of hatch patterns the panel assigns per bar/histogram
series, the same way it assigns colors. Off (`None`) in every theme but
`HATCH`; an explicit per-chart hatch style wins.
_Avoid_: hatch palette

**Figure size grid**:
The `FIG_SIZE` vocabulary: a width axis (`FULL_*` the A4 text block at
standard print margins, `HALF_*` one of its two columns, gap included; in/cm
stated in the docstring) crossed with a height axis (`SHORT`, `MEDIUM`,
`TALL`, `SQUARE`), plus the A4 printable area in both orientations, one
free-standing square, and slide frames (`SLIDE_*` PowerPoint-scale,
`BEAMER_*` LaTeX-scale). Height words describe heights; width words widths.
_Avoid_: narrow/regular/wide (former height suffixes), Letter sizes

**Style resolution**:
Collapsing `global config → theme → chart-specific style` into one concrete style,
performed once when a layer is built — never at draw time.
_Avoid_: config snapshot
