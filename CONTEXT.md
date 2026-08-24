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
title becomes a subtitle-sized heading row and its axis sharing stays local.
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

**DrawContext**:
The frozen per-layer instructions a panel hands to a layer at draw time — z-order,
legend label, assigned color, and bar slot placement.
_Avoid_: settings (for this), kwargs

**Chart front**:
A public chart function (`LineChart`, `BarChart`, …) — a thin front that validates
input and hands the engine an explicit charts structure and settings dict; it does
not draw, and its signature is the allowlist of what the chart supports.
_Avoid_: chart class, chart type (for the function), attrs dict

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
