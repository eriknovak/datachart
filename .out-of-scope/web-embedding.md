# Interactive web embedding

datachart does not provide an HTML export, embed snippet, or interactive
browser rendering of its figures. Web publishing is served by the existing
static export: `save_figure(figure, "chart.svg", transparent=True)` yields a
self-contained SVG that drops into any page via `<img>` or inline markup.

## Why this is out of scope

datachart is a matplotlib library for publication-grade static charts, with
notebook and GUI exploration through `figure.show(interactive=True)`
(ADR 0031, `mplcursors` + `ipympl`). Browser interactivity has no sound
matplotlib path:

- `WebAgg` needs a running Python server; `ipympl` needs a live kernel.
  Neither produces something a static host page can embed.
- `mpld3` re-renders a subset of matplotlib artists in JavaScript. Hexbin,
  contour, treemap, sankey, network, hatch themes, and constrained layouts
  fall outside that subset, so output would silently degrade per chart type.
  The `mplcursors` hover seam does not transfer to it either; every
  interaction would be re-implemented in JS.

Supporting this would mean a second rendering path with its own
compatibility matrix, against ADR 0001's single drawing seam, for a feature
that browser-native libraries (d3, Plotly, Vega, Bokeh) already do well.
Users who need interactive web charts should build them there.

The one worthwhile remainder, a docs section on SVG embedding, is tracked
separately.

## Prior requests

- #97 — "feat(embedding): make plots embeddable in webpages"
