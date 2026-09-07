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
tick styles, and `Panel.render()` applies them inside a scoped
`matplotlib.rc_context` around its artist creation. Spines predate the render,
so the furniture pass sets their sketch and halo directly. Because matplotlib
copies both values into each artist when it is created, `Panel` and `Grid`
composition redraws the look into new axes without any config access at draw
time — the same compose-time snapshot rule the furniture already follows.

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
- **Composition inherits via the compose-time snapshot.** A figure built under
  `SKETCH` stays sketched inside a `Grid` or `Panel` built under another theme;
  the composed figure's own furniture follows the theme active at compose time.

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
