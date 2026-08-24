---
status: accepted
---

# PyramidChart is a mirrored two-series bar front speaking spatial axes

Population-pyramid figures are technically reachable through `BarChart` today —
`orientation="horizontal"`, `bar_mode="overlay"`, hand-negated left-side data,
hand-mirrored tick labels, hand-set symmetric limits — but overlay mode forces
translucency on both series, every visible number goes negative on the left,
and no seam owns the back-to-back semantics. We add one chart front and make
the mirror a property of the panel's furniture.

## Commitments

- **One front, exactly two sides.** `PyramidChart(data=[left, right], ...)`
  takes exactly two series of `{"label", "y"}` points (any other count raises
  `ValueError`); the first is the left side, the second the right.
  `subtitle=[...]` names the sides in the legend — side names are arbitrary
  groups, never assumed to be demographic sexes. One call makes one pyramid:
  no `subplots`; small multiples come from `Grid`.
- **Positive in, absolute out.** Users pass positive values for both sides;
  the front negates the left side internally. Every visible number — value
  ticks, `show_values` labels — displays the absolute value. Pre-negated
  input is not a supported mode.
- **Mirror is panel furniture over the bar seam.** The pyramid draws with the
  existing bar layer machinery (ADR 0001) at full width on both sides — no
  overlay alpha, no new mark family, `plot_bar_*` styling and the multiple
  palette cycle apply untouched (ADR 0004). The panel supplies the mirror:
  symmetric value limits from the data max and absolute-value tick formatting.
- **Spatial axis spelling, deviating from ADR 0012.** `xlabel`, `xticks`,
  `xmax` address the horizontal (value) axis and `ylabel` the vertical
  (category) axis — what the user sees, not the axis role. The deviation is
  deliberate and confined to this front: a pyramid is never re-oriented, so
  the role spelling buys nothing and costs intuition. `xmax` sets the
  per-side maximum; `xmin` raises `ValueError` (the ADR 0015 impossible-
  settings precedent); `ymin`/`ymax` do not exist in the signature.
- **User ticks are positive and mirrored.** `xticks=[0, 1, 2, 3]` places
  ticks at ±those positions with absolute labels; `xticklabels` (same length
  as `xticks`) applies to both mirrored halves. Users never write signed
  positions.
- **Grid yes, Panel no.** The metadata transport carries the pyramid panel so
  `Grid` composes small multiples for free; `Panel` rejects pyramid figures
  with `ValueError` (the ADR 0006 grid-figure precedent) — overlaying
  unmirrored data onto a mirrored axis would silently mangle it.
- **Kept surface**: `title`, `subtitle`, `figsize`, `show_legend`,
  `show_grid`, `show_values`, `value_format`, `style` (bar styles per side),
  tick controls, `vlines`/`hlines`, `yerr`/`show_yerr` (mirrored `xerr` is
  symmetric, so error bars come free), and the `label`/`y`/`yerr` key remaps.
- **Cut from v1**: center-gap category labels and per-side headers (later
  options — labels sit at the left edge for now), surplus/overlap shading,
  `orientation`, `bar_mode`, `scalex`/`scaley` (log on a mirrored axis is
  ill-defined), `emphasis`, `subplots`/`max_cols`/`sharex`/`sharey`.
