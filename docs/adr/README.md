# Architecture decision records

Every design decision in `datachart` that was hard to reverse, surprising
without context, or the result of a real trade-off. These are internal records:
`docs/adr/` is excluded from the built site, and nothing mkdocs renders may
reference them. Code comments cite them freely.

## How to read an entry

An ADR keeps its number for good. Code comments, issue threads and merged pull
requests cite by number, so a record is never renumbered, and it is never
deleted to resolve a disagreement with a later one. Two frontmatter fields tell
you whether what you are reading still holds (ADR 0064):

| Frontmatter | What it means |
|---|---|
| `status: accepted` | The record governs as written. |
| `amended-by: [0045]` | Still governs, except where the listed later ADRs changed it. Read both. |
| `status: superseded by ADR 0045` | Nothing of it stands. Read the successor instead. No ADR carries this today. |

An amendment is a *changed* commitment. An ADR that builds on an earlier one,
extends it consistently, or fulfils a follow-up the earlier one already named
adds no tag; one that reverses, narrows, widens or replaces a commitment does.

`test/test_adr_index.py` fails if this index falls out of step with the files,
or if a `status:` or `amended-by:` value does not resolve.

### Numbering gaps

- **0061** — the bundled basemap, folded into
  [0062](0062-basemap.md) before its first release. The outlines it committed to
  the wheel never shipped, so there was no history to keep and only two records
  contradicting each other. Its citations moved to 0062. See 0064 for why this
  is the only fold.

## Drawing seam and figure lifecycle

- [0001](0001-layer-panel-drawing-seam.md) — One Layer/Panel drawing seam; style resolved at construction
- [0003](0003-explicit-settings-seam.md) — Chart fronts pass explicit settings; the attrs dict is retired
- [0008](0008-unmanaged-figures.md) — Figures are unmanaged; showing is explicit via `Figure.show()` (amended by [0031](0031-interactive-show-hover-seam.md))
- [0031](0031-interactive-show-hover-seam.md) — `show(interactive=True)` is the single interactive opt-in, fed by a per-layer hover seam
- [0054](0054-draw-order-ladder.md) — Draw order is a fixed ladder: surfaces at the bottom, reference lines near the top (amended by [0060](0060-image-chart.md))

## Composition: Panel and Grid

- [0002](0002-panel-grid-composition-fronts.md) — Public Panel/Grid composition fronts over the drawing seam (amended by [0006](0006-grid-in-grid-nesting.md))
- [0005](0005-nested-panel-flattening.md) — Nested Panel figures flatten losslessly into the outer Panel
- [0006](0006-grid-in-grid-nesting.md) — Grid figures nest inside Grid via a recursive cell-tree transport (amended by [0007](0007-nested-grid-alignment.md))
- [0007](0007-nested-grid-alignment.md) — Nested grids render in the parent gridspec, with a reserved heading row
- [0012](0012-orientation-aware-panel.md) — A Panel has an orientation, inferred from its layers, and its value axis follows it (amended by [0017](0017-pyramid-chart.md))
- [0041](0041-panel-axis-scales.md) — Panel takes axis scales, and a layer group carries its source figure's scale

## Emphasis and category order

- [0009](0009-emphasis-over-background-theme.md) — Emphasis replaces the background theme; themes are named for their look (amended by [0042](0042-category-sort-and-emphasis-rules.md))
- [0042](0042-category-sort-and-emphasis-rules.md) — Bar-type fronts sort their categories, and a rule fills in per-record emphasis (amended by [0045](0045-emphasis-rules-on-every-front.md))
- [0045](0045-emphasis-rules-on-every-front.md) — Emphasis rules reach every front, each selecting its own unit

## Themes and styling

- [0004](0004-theme-driven-defaults-and-cycles.md) — Themes may supply defaults for chart settings and per-series hatch cycles (amended by [0033](0033-value-labels-across-charts.md), [0048](0048-ink-rendering-attributes-in-themes.md))
- [0027](0027-render-scoped-rc-attributes-in-themes.md) — Render-scoped rc attributes in themes (amended by [0048](0048-ink-rendering-attributes-in-themes.md))
- [0040](0040-json-theme-files-and-config-scopes.md) — Themes travel as JSON diff files, and temporary style changes are context-managed scopes
- [0048](0048-ink-rendering-attributes-in-themes.md) — Ink rendering attributes in themes
- [0058](0058-dark-theme.md) — A dark theme inverts the furniture, not the marks

See also 0009, which names the themes for their look, and 0063, which moves the
theme faces out of the wheel.

## Settings and constants

- [0010](0010-fig-size-grid-and-constants-audit.md) — FIG_SIZE becomes a small A4-anchored grid; constants audit fixes
- [0034](0034-per-figure-legend-settings.md) — The legend is a per-figure setting, and outside locations expand to two matplotlib arguments
- [0035](0035-colorbar-setting.md) — The colorbar is a per-figure setting located by edge, and its type takes the setting suffix (amended by [0043](0043-setting-payloads-take-the-setting-suffix.md))
- [0043](0043-setting-payloads-take-the-setting-suffix.md) — Every setting payload takes the `*SettingAttrs` suffix, old names warn for one release
- [0052](0052-chart-prefixed-constants.md) — A constant one chart owns carries that chart's prefix

## Axes, scales, and colormaps

- [0037](0037-temporal-axis.md) — The axis kind is a panel snapshot, and date strings are never parsed
- [0056](0056-centred-norm-and-diverging-colormap.md) — A centred norm selects the theme's diverging colormap

## Annotations and reference marks

- [0018](0018-text-annotations.md) — Text annotations ride the layer, with a post-hoc Annotate front
- [0033](0033-value-labels-across-charts.md) — Value labels are a cross-chart feature with per-geometry placement
- [0036](0036-reference-bands.md) — A reference band is a span type per axis, drawn over the grid and under the marks
- [0038](0038-stats-annotation-helpers.md) — Annotation statistics degrade to nan, and every rule delegates to a library
- [0055](0055-diagonal-reference-lines.md) — A diagonal reference line is a third line family, defined by slope and intercept in data space
- [0059](0059-pairwise-brackets.md) — A pairwise bracket is a fourth reference-mark family, placed on the category axis and stacked automatically

## Chart fronts

- [0014](0014-histogram-stacking-and-step-defaults.md) — Histogram stacking moves to bar_mode; step edges follow the series
- [0015](0015-radial-chart.md) — RadialChart is one front with a visual switch, on a projection-aware Panel (amended by [0052](0052-chart-prefixed-constants.md))
- [0017](0017-pyramid-chart.md) — PyramidChart is a mirrored two-series bar front speaking spatial axes
- [0019](0019-violin-plot.md) — ViolinPlot mirrors BoxPlot and draws its inner marks itself
- [0020](0020-swarm-plot-category-index.md) — SwarmPlot aligns with boxes through a panel category index, not bar slots
- [0021](0021-raincloud-plot.md) — RaincloudPlot assembles the violin, swarm, and box layers with per-layer offsets
- [0022](0022-contour-chart.md) — ContourChart draws a gridded surface as lines or fills through one layer
- [0023](0023-heatmap-chart-dicts.md) — Heatmap takes `{x, y, z}` chart dicts; `x` and `y` are labels, not coordinates
- [0024](0024-hexbin-chart.md) — HexbinChart bins dense scatter data into colormapped hexagons (amended by [0035](0035-colorbar-setting.md))
- [0025](0025-stacked-area-chart.md) — StackedAreaChart stacks series over an ordered axis with a panel-computed baseline (amended by [0052](0052-chart-prefixed-constants.md))
- [0026](0026-sankey-chart.md) — SankeyChart draws weighted flows between column-ordered nodes through one layer
- [0028](0028-treemap-chart.md) — Treemap tiles one level of nested part-of-whole data through one layer (amended by [0032](0032-treemap-nesting-depth.md))
- [0029](0029-network-chart.md) — NetworkChart draws node-link diagrams from a nodes/edges dict through one layer (amended by [0030](0030-network-weighted-and-grouped-layouts.md))
- [0030](0030-network-weighted-and-grouped-layouts.md) — NetworkChart gains the WEIGHTED and GROUPED layouts
- [0032](0032-treemap-nesting-depth.md) — Treemap nests to four levels through the same group rules
- [0044](0044-calendar-heatmap.md) — A calendar heatmap draws one panel per year through the heatmap's cell seam (amended by [0052](0052-chart-prefixed-constants.md))
- [0046](0046-bump-chart.md) — A bump chart ranks per period and draws through the line layer (amended by [0052](0052-chart-prefixed-constants.md))
- [0047](0047-ridgeline-plot.md) — RidgelinePlot stacks per-label density ridges on the category index
- [0049](0049-gantt-chart.md) — A gantt chart puts time on the value axis and stays a bare figure (amended by [0052](0052-chart-prefixed-constants.md))
- [0050](0050-dumbbell-chart.md) — A dumbbell chart is a group layer on the category index, not a bar
- [0051](0051-scatter-matrix.md) — A scatter matrix is a grid figure composed from scatter and histogram cells (amended by [0052](0052-chart-prefixed-constants.md))
- [0057](0057-scatter-error-bars.md) — Scatter error bars are distances drawn in the point's colour
- [0060](0060-image-chart.md) — An image is a chart front anchored by an extent, not a setting on other charts (amended by [0062](0062-basemap.md))
- [0062](0062-basemap.md) — The basemap draws unprojected outlines fetched into a cache (amended by [0063](0063-downloaded-theme-fonts.md))

## Distribution and packaging

- [0063](0063-downloaded-theme-fonts.md) — The wheel ships no data: the theme faces download too

See also 0062, which set the principle on the basemap outlines and holds the
cache's own commitments.

## Docs and tooling

- [0011](0011-chart-guide-structure.md) — Chart how-to guides share one structure with real-world data
- [0013](0013-constant-figures-via-chart-fronts.md) — Constant at-a-glance figures render through the chart fronts
- [0016](0016-llms-txt-generation.md) — llms.txt is generated at docs build, with hand-written descriptions guarded by the nav
- [0053](0053-per-chart-reference-pages.md) — The API reference is organized per chart, with clickable signatures
- [0064](0064-adr-supersession-signal.md) — A superseded ADR says so in its frontmatter; the records are not merged

## Utilities

- [0039](0039-multi-format-save-figure.md) — `save_figure` takes a list of formats, treats the path as a stem, and always returns the written paths
