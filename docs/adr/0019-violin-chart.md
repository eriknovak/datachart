---
status: accepted
---

# ViolinChart mirrors BoxPlot and draws its inner marks itself

Box plots hide distribution shape; bio/ML publications default to violins.
We add one chart front that speaks the `BoxPlot` API and shares its
positioning contract, so the two compose in `Panel` without a new seam.

## Commitments

- **BoxPlot's shape, BoxPlot's contract.** `ViolinChart(data, ...)` takes
  the same `{"label", "value"}` points and the same common parameters as
  `BoxPlot` (`orientation`, `emphasis`, `scaley`, ticks, limits, `vlines`/
  `hlines`/`texts`, `label`/`value` key remaps). A list of lists requires
  `subplots=True`; there is no side-by-side dodging. Violins draw at
  positions 1…n in first-seen label order — the same implicit contract the
  box layer uses — so a `Panel` of violin + box figures over the same labels
  lines up. That contract is documented, not enforced by a seam; a
  categorical-position seam waits for a swarm layer.
- **`inner` is one enum, not booleans.** `inner="box" | "quartiles" |
  "median" | None`, default `"box"`. Box = thin Q1–Q3 bar, 1.5·IQR whisker
  line, median dot; quartiles = dashed median and dotted Q1/Q3 clipped to
  the body width at that value; median = one solid line; None = body only.
  Inner marks are drawn by the layer from the data, never via matplotlib's
  `showmeans`/`showextrema`/`quantiles` — those options are not exposed.
- **`bandwidth` is a front parameter.** `None` (matplotlib's scott),
  `"scott"`, `"silverman"`, or a scalar, passed through as `bw_method`.
  A data-shaping choice, so not a style key.
- **`split` is a data-key remap.** `split="sex"` names the point key whose
  exactly two distinct values become the left/right halves of each violin;
  more or fewer than two raises `ValueError`. Halves take colors from the
  multiple palette cycle in first-seen order, each keeps its own inner
  marks, and the legend lists the split values. Data stays flat — no nested
  structure for the two groups.
- **Style keys under `plot_violin_*`.** `color`, `alpha`, `linewidth`,
  `edgecolor`, `width`, `inner_color`, `inner_linewidth`, `median_color`,
  `median_size`. Fill defaults to the cycle color, edge to the fill, inner
  to the theme font color so it reads on any fill. Every theme declares
  every key (ADR 0004).
- **Emphasis follows the box layer.** Per-label roles: `"background"` mutes
  body and inner marks with the theme's muted attributes; `"highlight"`
  thickens the body edge.
- **Cut from v1**: dodged multi-dataset violins, mean/extrema marks,
  per-point strips inside the body (a swarm layer's job), `show_notch`,
  `show_outliers` (no fliers on a violin).
