---
status: accepted
---

# Themes set the violin inner, the strip jitter and the ridge marks

A few front parameters hard-coded their default in the signature (issue
#323): `ViolinPlot(inner=VIOLIN_INNER.BOX)`, `jitter=0.4` on `SwarmPlot` and
`RaincloudPlot`, and `RidgelinePlot(fill=True, show_outline=True)`. A theme
could not change them, although every other default of these fronts
resolves `None` against the config. ADR 0004 keeps the set of theme-backed
settings enumerated and ADR 0071 says it does not grow there; this record
grows it by four.

## Commitments

- **Four more theme defaults, named by ADR 0071's rule.** `chart_default_jitter`
  (a shared parameter, so no chart in the name),
  `chart_default_violin_inner`, `chart_default_ridgeline_fill` and
  `chart_default_ridgeline_show_outline`. The base theme holds today's
  values, so no theme draws differently.
- **`None` means "the theme decides", so "no inner marks" is a member.**
  `VIOLIN_INNER.NO_INNER = "none"` draws the body alone, on violins and ridges
  alike. It is named like `LINE_MARKER.NO_MARKER`, because a member named
  `NONE` is `None` on every constant class. `ViolinPlot(inner=None)` now takes
  the theme's inner, a box by default, where it drew the body alone before.
  `RidgelinePlot(inner=None)` still draws no marks: its inner has no theme
  default.
- **A raincloud's cloud asks for `"none"` explicitly.** It is built as a
  `ViolinLayer`; passing `None` would give it the theme's violin inner on
  top of the raincloud's own box.

## Considered options

- *Keep the four defaults fixed and record why.* Rejected: a theme like
  `MINIMAL` has a reason to drop the box or the ridge outline, and a
  signature default cannot be changed after 1.0 without changing the
  annotation.
- *A private sentinel default so that `None` keeps meaning "body only".*
  Rejected: it breaks ADR 0071's single rule that `None` defers to the
  theme, and the signature check of ADR 0067 would need a special case.
