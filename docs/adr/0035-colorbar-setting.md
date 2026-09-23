---
status: accepted
amended-by: [0043]
---

# The colorbar is a per-figure setting located by edge, and its type takes the setting suffix

`HeatmapColorbarAttrs` carries one field, `orientation`, and three fronts share
it: Heatmap, filled Contour, and Hexbin. From that one field the drawing code
derives an edge — vertical means right, horizontal means top — so two of the
four edges are unreachable. `COLORBAR_LOCATION` names all four and has been
consumed by nothing since it was introduced. There is no way to say what
quantity the bar encodes, which is the caption a colormapped figure most needs.

We make the colorbar a per-figure setting on the same terms ADR 0034 set for
the legend, and spend `COLORBAR_LOCATION` the way that ADR spent
`LEGEND_LOCATION`.

## Commitments

- **`ColorbarSettingAttrs` replaces `HeatmapColorbarAttrs`**, which stays as a
  deprecated alias. ADR 0034 reserved the `*SettingAttrs` suffix for per-figure
  settings passed to fronts and deferred renaming this type, calling it "its
  own change, not a rider on this one". This is that change. The name also
  drops `Heatmap`, which was never accurate — Contour and Hexbin take the same
  payload.
- **The payload is `label`, `location`, `format`, `ticks`, and `orientation`.**
  `None` in any field falls back to the same defaults the fronts resolve today,
  per ADR 0003.
- **`location` is the control; `orientation` is derived from it.** A caller who
  passes only `orientation` keeps today's behavior — vertical derives `right`,
  horizontal derives `top` — so the field stays public and accepted rather than
  deprecated. When both are given, `location` wins and orientation follows the
  edge. Removing `orientation` would break callers for a rename's worth of gain.
- **`format` is the one colorbar tick format.** Hexbin's `valfmt` documents
  itself as the colorbar tick format today, so it becomes the fallback:
  `format` wins when set, `valfmt` still applies when it is not. Heatmap's
  `valfmt` is unaffected — there it formats cell values, a different thing that
  happens to share a name.
- **The label font follows the `font_ylabel_*` theme keys.** The colorbar is an
  axis with a label; it borrows the family already spent on axis labels rather
  than growing a parallel one.
- **The colorbar belongs to the layer, so composition carries it.** A figure
  redrawn into a `Grid` cell keeps its label, edge, and format, because the
  panel redraws the layer that owns the bar.
- **The bar sits beside its axes, clear of the axis it crosses.** On an
  aspect-locked axes, where the layout engine would size the bar to the grid
  cell rather than the drawn box, the bar is a child axes placed from the
  axes' drawn box, padded past the tick labels on a left or bottom edge.
  Amended (issue #192): the placement is computed in display pixels, not
  inches against the figure box, because a `bbox_inches="tight"` save swaps
  the figure box and an inch-based divider then put the bar outside the
  saved area.
  Amended (issue #213): a single-axes figure with a left or bottom bar
  carries that edge's axis label on the axes, not the figure, so the label
  stays beside its ticks and the bar pads past it; a figure-level label sits
  at the figure edge, past the bar, where it reads as the bar's caption.
  Subplot figures keep the shared figure-level label.
- **Amended (issue #208): explicit `ticks` never move the bar's ends.**
  Positions outside the mapped value range are dropped silently, as
  matplotlib's own tick locator drops them; setting them would widen the bar
  so its colors no longer match the figure.

## Considered options

**Theme keys for the colorbar** — a `plot_colorbar_*` family mirroring
`plot_legend_*` — was rejected. ADR 0034 committed that nothing about the
legend becomes settable that a theme cannot also set, and the colorbar splits
where the legend did not: `label` and `format` describe the data, so no theme
can supply them, and `location` follows the label. Appearance the theme does
own — the label font — already resolves through `font_ylabel_*`. Adding four
keys across seven themes to hold data-specific strings would buy nothing.

**A `colorbar_label` argument on each front** was rejected. Three fronts
already pass one `colorbar` payload; a sibling argument would leave two places
to look and would not extend to `location` or `format` without four more.

**Deprecating `orientation` outright** was rejected on cost. It is public,
documented, and covers the two common edges correctly; deriving it costs one
mapping and breaks nobody.
