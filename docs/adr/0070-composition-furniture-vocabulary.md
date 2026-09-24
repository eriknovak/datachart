---
status: accepted
---

# Panel and Grid take the chart fronts' furniture vocabulary

`Panel` and `Grid` do not speak the fronts' figure-level vocabulary (issue
#278). `Panel.show_legend` defaults to `False` where every front defaults to
`None` and lets the config decide; `Panel` has no `emphasis_rule`. `Grid`
takes seven parameters — `title`, `xlabel`, `ylabel`, `max_cols: int = 4`,
`figsize` without the `FIG_SIZE` union, `sharex: bool = False`, `sharey: bool
= False` — with no legend, grid, limits or aspect ratio, and its annotations
and defaults drift from the shared table of ADR 0067 because nothing checks
them. Eight fronts return figures `Panel` rejects (`ChartKind.overlayable` is
`False`) and no signature, docstring or reference page says so. The top-level
`Grid` lays its cells out through `subplots`/`GridSpec` while a nested grid,
a multi-subplot cell and `ScatterMatrix` all render through the node renderer
(`_render_grid_node`), which alone knows how to draw a grid-level legend.

## Commitments

- **The composition fronts are rows of the shared table.** `Panel` and
  `Grid` declare every shared parameter they take with the name, annotation
  and default of `SHARED_PARAMETERS`, and the conformance test of ADR 0067
  reads their signatures beside the chart fronts'. `Panel.show_legend`
  defaults to `None`, resolved against the config like a front's. `Grid`
  gains `show_legend`, `legend`, `show_grid`, `xmin`, `xmax`, `ymin`, `ymax`
  and `aspect_ratio`; `max_cols`, `sharex`, `sharey` and `figsize` take the
  shared annotations and `None` defaults, resolved at point of use (`max_cols`
  to 4, sharing to off). `xmin`/`xmax` stay outside the table (ADR 0067) and
  take `Panel`'s `Optional[float]`.
- **A rule is panel-level, a role is per figure.** `Panel` gains
  `emphasis_rule`, one rule across every composed layer, as on a front. The
  per-figure `"emphasis"` dict key stays: a role names one figure's layers.
  The rule reads one unit per composed layer that plots raw values, summarised
  by `by` (default mean, as on a series front); a layer that already carries a
  role — from its figure's `"emphasis"` key or its own records — keeps it.
- **Grid furniture applies to the figure and to every cell.** `title`,
  `xlabel`, `ylabel` and the legend are drawn once for the figure. `show_grid`,
  the limits and `aspect_ratio` override each cell's own setting only when
  the caller gave them — a cell keeps what its front resolved otherwise — and
  reach the cells of a nested grid the same way.
- **One grid legend, drawn by the node renderer.** `Grid(show_legend=True)`
  draws one legend for the whole grid from the first cell whose axes carry
  entries, on the edge `legend["location"]` names (right by default), through
  the node `legend` ScatterMatrix already uses. The top-level `Grid` renders
  through `_render_grid_node` like every nested grid, so there is one grid
  layout path; existing grid figures render pixel-identical.
- **The descriptor says what composes.** The reference page of every front
  prints a composition row from `ChartKind.overlayable`: `Grid: yes`,
  `Panel: yes/no`; `ScatterMatrix` adds `Annotate: no`. No new descriptor
  flag: `overlayable` already is the fact.
- **`ScatterMatrix` keeps its grid transport.** It is a grid of cells, so
  `Panel` and `Annotate` reject it as one; the reference page says so.

## Considered options

Keeping `Panel.show_legend = False` as a documented exception was rejected:
one table with an exception is not one table, and the flip is called out as
breaking. A panel-level `emphasis` parameter was rejected: a role for every
figure at once is a rule with no discriminator. Giving `ScatterMatrix` a
`panel` so `Annotate` accepts it was rejected: a matrix has no one axes to
annotate. A per-cell `show_legend` toggle for `Grid` was rejected: the
fronts' own subplot path already declines per-cell legends, and the grid
legend the node renderer draws is the composed figure's one legend.
