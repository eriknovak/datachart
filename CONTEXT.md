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
assignment, bar slotting, axis scale and limits, grid, ticks, legend assembly, and
twin-axis (left/right) assignment. Also the public composition front
(`datachart.utils.Panel`) that overlays rendered figures into one panel.
_Avoid_: overlay (for the concept), subplot, axes group

**Grid**:
An arrangement of figures in rows and columns — the public front
(`datachart.utils.Grid`) takes nested rows (the layout you can see; `None` for a
blank cell) or a flat list with `max_cols`/`layout_spec`, and redraws each
figure's panel into its cell.
_Avoid_: grid layout (for the front), figure grid

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
raw attribute dicts.
_Avoid_: snapshot (for this), chart data

### Styling

**Theme**:
A complete, named set of style attributes (`DEFAULT`, `GREYSCALE`, `PUBLICATION`,
`BACKGROUND`). Applying one replaces the whole global configuration.

**Style resolution**:
Collapsing `global config → theme → chart-specific style` into one concrete style,
performed once when a layer is built — never at draw time.
_Avoid_: config snapshot
