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
twin-axis (left/right) assignment.
_Avoid_: overlay (for the concept), subplot, axes group

**DrawContext**:
The frozen per-layer instructions a panel hands to a layer at draw time — z-order,
legend label, assigned color, and bar slot placement.
_Avoid_: settings (for this), kwargs

**Chart front**:
A public chart function (`LineChart`, `BarChart`, …) — a thin front that validates
input and builds layers; it does not draw.
_Avoid_: chart class, chart type (for the function)

**Metadata transport**:
The chart spec riding on a rendered figure (`figure._chart_metadata`) so composition
functions (`OverlayChart`, `FigureGridLayout`) can rebuild it. Carries layers and
panel settings, not raw attribute dicts.
_Avoid_: snapshot (for this), chart data

### Styling

**Theme**:
A complete, named set of style attributes (`DEFAULT`, `GREYSCALE`, `PUBLICATION`,
`BACKGROUND`). Applying one replaces the whole global configuration.

**Style resolution**:
Collapsing `global config → theme → chart-specific style` into one concrete style,
performed once when a layer is built — never at draw time.
_Avoid_: config snapshot
