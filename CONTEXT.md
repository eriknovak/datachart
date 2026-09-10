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

**Band**:
A shaded region behind the data marking an interval — a confidence range, a
recession period, an acceptable range. Declared with the chart (`vspans=` for
a band bounded on the x axis, `hspans=` for one bounded on the y axis) like
reference lines, stored on the layer, drawn by the panel over the grid and
under the marks — so it survives composition. An omitted bound runs to the
axis limit. On a polar axes a `vspan` is a wedge and an `hspan` an annulus,
both bounded in degrees.
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

**Network**:
Relational data as a node-link diagram (`NetworkChart`: a `{nodes, edges}`
dict, a node `{id, label?, size?, group?, emphasis?}`, an edge `{source,
target, weight?}`; nodes may be inferred from edges). `layout` takes a
`NETWORK_LAYOUT` constant (`SPRING`, seeded in-package Fruchterman–Reingold;
`WEIGHTED`, the spring with each edge's pull set by its weight; `GROUPED`,
a plain spring inside each group and a weighted one between the groups;
`CIRCULAR`; `FIXED` from per-node `x`/`y`); `directed` adds arrowheads.
Weight maps to edge width, and to pull only under the two layouts named for
it; size by square root to marker area; `group` to the multiple color cycle,
an ungrouped node beside groups taking the edge color. A **cluster** is the
nodes of one group as `GROUPED` places them: a compact patch arranged by the
group's own edges, marked by a translucent disc in the group color (the
**halo**, `plot_network_group_alpha`). One layer per chart, no furniture; rejected in `Panel`, a
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
`MATERIAL`, `INK`, `HATCH`, `SKETCH`). Applying one replaces the whole global
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

**Marker edge rule**:
A filled marker (scatter, bubble, swarm, radial scatter, network node) keeps
its theme edge only while the stroke stays under a sixth of the marker
diameter; a smaller marker draws with no edge, per marker for data-sized
ones. A highlight edge is the emphasis cue and always stays. Hollow markers
(box outliers) are exempt — their edge is the marker.
_Avoid_: edge threshold, min marker size

**Value label**:
The number a chart prints beside a mark it has already drawn, turned on with
`show_values` and rendered through `value_format`. It is derived from the
data, unlike a text annotation, which the caller writes and positions. A
distribution chart's value label is its median.
_Avoid_: data label, annotation, callout

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

**Legend setting**:
The per-figure legend controls — title, location, column count, alignment —
passed to a front as `legend` and falling back to the theme's `plot_legend_*`
attributes field by field. An outside location is not a matplotlib location:
it expands, once, into a location plus an anchor that no public surface names
(ADR 0034).
_Avoid_: legend style (that is the theme-key family), bbox anchor

**Colorbar setting**:
The per-figure colorbar controls — label, location, tick format, tick
positions — passed to a front as `colorbar` on Heatmap, filled Contour, and
Hexbin. `location` is a `COLORBAR_LOCATION` edge and is what the bar follows;
`orientation` stays accepted and derives the edge when no location is given
(ADR 0035).
_Avoid_: color legend, colorbar style, scale bar

**Style resolution**:
Collapsing `global config → theme → chart-specific style` into one concrete style,
performed once when a layer is built — never at draw time.
_Avoid_: config snapshot
