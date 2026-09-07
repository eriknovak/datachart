---
status: accepted
---

# Render-scoped rc attributes in themes

Themes are `StyleAttrs` dicts: every attribute maps onto an artist property
the layers or the panel set explicitly. A hand-drawn look (matplotlib's
`path.sketch` wobble and a `path.effects` halo) does not fit that model: both
are rcParams that matplotlib copies into every artist at construction, not
properties a chart front could pass along. Until now the package never touched
rcParams, and the only way to a sketch look was `plt.xkcd()` around the whole
program — a global mutation that bleeds into unrelated figures and that
composition cannot reproduce.

We add **sketch attributes**: an enumerated pair of nullable theme attributes,
`plot_sketch_params` (the `(scale, length, randomness)` triple) and
`plot_sketch_halo_width` (the white stroke width). `None` in both means off.
`Panel.snapshot_furniture()` captures them at build time beside the spine and
tick styles. `Panel.render()` applies the wobble inside a scoped
`matplotlib.rc_context` around its artist creation, so matplotlib copies it
into every artist as it is made; spines predate the render, so the furniture
pass sets their sketch directly. The halo is deliberately narrower than
matplotlib's xkcd mode: `Panel.render()` strokes it under the line artists
after drawing, and text and patches stay clean — a halo around glyphs
thickens them (and vanishes on white text), and bars already carry an edge.
Both values live on the artists, so composition redraws the look into new
axes without any config access at draw time. `Grid` renders
each figure's stored panel, snapshot included, so a figure built under
`SKETCH` stays sketched in a grid built under another theme; the `Panel` front
builds one new panel and snapshots at compose time, so a composed panel wears
the theme active at the compose call — the same rule the furniture follows.

One carve-out: the `show_area` fill under a line reaches a floor far below
the axes, and the sketch filter would split that off-screen edge into millions
of wobble segments. The fill drops its sketch parameters; its only visible edge
sits under the wobbled line and its halo.

`THEME.SKETCH` is the first theme to set both. It also bundles Comic Neue
Regular and Bold (SIL OFL) as package data, registered with matplotlib's font
manager on import, so its font stack resolves on every machine.

## Commitments

- **The enumerated set is exactly wobble and halo.** A theme cannot carry
  arbitrary rcParams; growing the set requires revisiting this ADR.
- **`None` means off, and every existing theme keeps `None`**, so the
  mechanism alone alters no output — the golden baselines stay byte-identical.
- **Application lives in the `Panel`**, beside the furniture: no rc handling in
  the chart fronts, `render_chart`, or the layers.
- **No global rc mutation.** `rcParams["path.sketch"]` and
  `rcParams["path.effects"]` are unchanged after any render.
- **Composition follows the compose-time snapshot.** `Grid` keeps each
  figure's own snapshot, so a `SKETCH` figure stays sketched in a grid built
  under another theme; a `Panel` front snapshots when called, so the composed
  panel wears the theme active then, exactly as its furniture does.

## Considered options

- **Global `plt.xkcd()` / `rcParams` mutation in `set_theme`.** Rejected: it
  leaks into every figure the user draws, and composition could not restore it.
- **A free-form `rc` dict in the theme.** Rejected: an open escape hatch would
  let themes reach past the `StyleAttrs` contract and make output depend on
  arbitrary rcParams the panel cannot reason about.
- **A post-render pass setting sketch and path effects on every artist.**
  Rejected: it duplicates what matplotlib already does at construction and
  has to enumerate artist containers (patches, lines, collections, texts,
  colorbars) per chart type.
- **Asking users to install a handwriting font.** Rejected: the theme would
  fall back to Helvetica on most machines and lose its identity; Comic Neue is
  small and OFL-licensed. xkcd Script is CC BY-NC and is never bundled.
