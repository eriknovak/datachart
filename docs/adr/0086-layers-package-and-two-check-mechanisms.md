---
status: accepted
---

# The drawing seam is a package; a capability is a mixin, a group policy is a row field

`layers.py` holds ADR 0001's whole drawing seam in one module of 13,300
lines and 58 classes (issue #328). The design holds — one `Layer` per chart
type, `Panel` owning every cross-layer concern — but `Panel` asks
`isinstance(layer, <ConcreteLayer>)` at 33 sites, so every new chart type
edits `Panel`. The checks are of two kinds. Some ask what a layer can do on
its own, and three mixins already answer that (`PointLabelMixin`,
`EndLabelMixin`, `UnclippedMarksMixin`). Others ask what a group of layers
together makes the panel do — who shares a bar slot, whether rows stack
downward, whether a stacked baseline is shared — which no single layer can
answer.

## Commitments

- **`layers` becomes a package with the same public seam.**
  `datachart/utils/_internal/layers/` re-exports from `__init__.py` exactly
  the names the other internal modules import from `layers` today; no import
  outside the package changes. Modules, in dependency order: `base`
  (`Layer`, `DrawContext`, the mixins, `BarSlot`/`HistSlot`/`StackSlot`),
  `ticks` (the locators and formatters), then one per family — `line`
  (`LineLayer`, `BumpLayer`, `StackedAreaLayer`), `bar` (`BarLayer`,
  `GanttLayer`, `HistogramLayer`, `_LockedBarLocator`), `scatter`, `group`
  (`GroupLayer`, `BoxLayer`, `SwarmLayer`, `DumbbellLayer`, `ViolinLayer`,
  `RidgelineLayer`), `grid` (`HeatmapLayer`, `CalendarHeatmapLayer`,
  `ContourLayer`, `HexbinLayer`), `position` (`DrawPositionLayer`,
  `ImageLayer`, `BasemapLayer`), `parallel` (`ParallelCoordsLayer`),
  `radial` (`RadialLayer` and its four subclasses), `relational`
  (`SankeyLayer`, `TreemapLayer`, `NetworkLayer` and their helper types),
  `text` (`TextLayer`, `_TextHalo`, `InkStroke`, `Etch`) — and `panel`
  (`Panel`, `LayerGroup`, `ScaledAxis`) last, importing from every family.
  The split is a move: classes already sit adjacent by family in the file.
- **A capability is a mixin.** A check that asks whether a layer itself can
  do something — draw an end label, keep its marks unclipped, take a bar
  slot — reads an `isinstance` against a mixin from `base`, never a concrete
  class. The three existing mixins stay; checks of the same shape gain one
  (for instance a bar-slot mixin replacing `isinstance(l, (BarLayer,
  RadialBarLayer))`). A new chart type opts in by inheriting.
- **A group policy is a `ChartKind` field, stored on the layer.** A check
  that asks what a set of layers together makes the panel do — rows stack
  downward, stacked areas share a baseline, the panel's axis kind, a
  dumbbell's minor grid — reads a boolean the front's `ChartKind` row
  declares (ADR 0065), copied onto the layer at build so `Panel` reads
  `layer.<field>` and never names a class. A new chart type opts in on its
  row.
- **`Panel` names no concrete layer class.** After the two rules, the only
  `isinstance` calls left in `panel` are against `Layer`, the mixins, and
  non-layer values (lists, tz objects). A test asserts it.
- **Moved in module-sized commits, golden after each.** Each module move is
  its own commit and `test/golden/golden.py candidate` runs after each, so a
  break bisects to one move. The pixel diff is clean at every step; no
  rendered figure changes.

## Considered options

Every check as a `ChartKind` field was rejected: a per-layer capability
(can this layer draw an end label) is a property of the class, and a static
field duplicating it drifts. Every check as a mixin was rejected: "all these
layers stack" is not something a layer knows alone, and a mixin nobody
instantiates on its own is a flag in disguise. One file per class was
rejected: `Panel` would import from twenty modules for no gain. Moving the
import path callers use was rejected: the seam ADR 0001 drew is between the
fronts and the drawing, and this record does not move it.
