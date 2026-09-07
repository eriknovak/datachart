---
status: accepted
---

# `show(interactive=True)` is the single interactive opt-in, fed by a per-layer hover seam

Datachart figures are unmanaged and showing is explicit (ADR 0008): `show()`
displays a PNG payload in notebooks and a GUI window in scripts. Both are
static — nothing zooms, and no drawn mark maps back to its datum, because
layers draw onto the axes and keep no handle on the artists they create.
Issue #96 asks for zoom/pan and hover-to-inspect without changing the static
default.

We extend ADR 0008 rather than add a rendering path: `show()` gains a keyword
`interactive: bool = False`. With it, a notebook figure is displayed on an
`ipympl` widget canvas (the matplotlib toolbar gives zoom and pan) and a
script figure opens in its GUI window as before; on both, `mplcursors` is
attached in hover mode to the figure's *hover targets*. A hover target is an
`(artist, resolver)` pair a layer registers during `draw()`, where
`resolver(i)` returns the datum behind the artist's i-th element as an
ordered dict: the legend label, then the fields the mark stands for. The
panel collects the pairs right after each draw onto the figure being drawn
into, so `show()` builds the annotation — label line, then one `name: value`
line per field — without knowing chart types.

## Commitments

- **`show()` is the only opt-in.** No config key, no flag on chart fronts,
  `Panel`, or `Grid`. `show()` with no arguments is unchanged, pinned by the
  golden harness.
- **The seam lives on `Layer`, not `DrawContext`.** A layer calls
  `register_hover(artist, resolver)` from `draw()`; the panel calls
  `take_hover_targets()` after each draw. `DrawContext` stays frozen. A layer
  that registers nothing has no hover and causes no error — every chart type
  can adopt the seam in its own issue.
- **Targets ride on the figure, next to the transport.** The metadata dict is
  assembled by the callers after rendering, and grids render cells
  recursively, so the panel stores the pairs on `ax.figure._hover_targets`.
  They cannot stick to layers: a layer is shared by every figure it is
  redrawn into (source figure, Panel, Grid), and each figure has its own
  artists.
- **A datum is an ordered dict of named fields.** The `x` and `y` fields are
  axis coordinates: a transposed series or a horizontal bar reports its
  values under the axis they are drawn on, and `show()` names them off the
  artist's axes (own label, a shared sibling's for twins, the figure's
  sup-label, else `x`/`y`) and formats them with the axis' own coordinate
  formatter, so twin-axis series report the secondary label and
  category-axis points the category name. Every other field is shown under
  its own key, in insertion order, formatted as a plain value. A layer adds
  a field by adding a key; the annotation builder never learns chart types.
- **Every data layer registers; aggregate marks report their summary.** The
  mark the user hovers is the mark that answers, with what an explorer wants
  from it:

  | Layer                | Mark                | Fields after the label                          |
  | :------------------- | :------------------ | :---------------------------------------------- |
  | line, stacked area   | point               | `x`, `y` (own value, never the stack total)     |
  | scatter, swarm       | point               | `x`, `y`                                        |
  | bar                  | bar                 | `x`, `y` (own value, never the stack total)     |
  | histogram            | bin                 | `x` (bin range), `y` (count or density)         |
  | box, violin          | box / body          | `x` (category), `median`, `q1`, `q3`, `min`, `max` |
  | heatmap              | cell                | `x`, `y`, `value`                               |
  | contour              | level line          | `level`                                         |
  | hexbin               | hexagon             | `x`, `y` (cell center), `count`                 |
  | parallel coordinates | series line on axis | axis name, `value`                              |
  | radial line/bar/scatter/histogram | point / wedge | `angle` (category label when categorical), `radius` |
  | sankey               | node / link         | node: `flow`; link: `source`, `target`, `flow`  |
  | treemap              | tile                | `value`                                         |
  | network              | node / edge         | node: `degree` (`in` / `out` when directed; weight sum when weighted), then `group` and `size` when given; edge: `source`, `target`, `weight` |

  Text layers and reference lines decorate and register nothing. Polar axes
  carry no axis labels, so radial fields are shown under their own keys. A
  mark `mplcursors` cannot pick stays zoom/pan only and is documented as such
  rather than hand-rolled.
- **The annotation wears the theme's text annotation style.** The panel
  snapshots the `plot_text_*` font, box, and connector color from the config
  when it first renders into a figure (ADR 0018), so the popup matches the
  figure it sits on and the theme in force when the figure was built, not
  when it is shown.
- **Pyramid sides report the value as passed, positive.**
- **A missing dependency raises.** `show(interactive=True)` raises
  `ImportError` naming the missing package and the `datachart[interactive]`
  extra; there is no silent static fallback. Each path imports only what it
  uses: scripts need `mplcursors`, notebooks `ipympl` and `mplcursors`.
- **Notebook figures stay unmanaged.** The ipympl canvas and manager are
  built directly, not through the backend factory, so nothing lands in
  pyplot's registry or in ipympl's post-cell display queue; the widget
  replaces the static payload, never joins it.

## Considered options

A per-front `interactive` flag (`LineChart(..., interactive=True)`) was
rejected: interactivity is a property of the display, not the chart, and a
flag on every front, `Panel`, and `Grid` would have to be threaded through
composition. A matplotlib-to-web export (mpld3, plotly) was rejected: it is a
second rendering path with its own fidelity gaps, and it cannot reuse the
panel's artists. A hand-rolled hover on `motion_notify_event` was rejected in
favor of `mplcursors`: it already handles picking on lines, collections, and
bar containers, annotation placement, and the widget and GUI canvases alike.
Storing the datum on the artist (`artist.datachart_datum`) instead of a
resolver was rejected: a resolver keeps the per-element lookup lazy and lets
one artist — a line, a bar container — stand for many data points.
An explicit `fields: [(name, value), ...]` list instead of an ordered dict
was rejected when the seam widened beyond `x`/`y`: it would have invalidated
every existing resolver for no gain, since dict insertion order already
carries the field order. Pre-formatted text per layer was rejected: it moves
axis naming and value formatting into every layer.
