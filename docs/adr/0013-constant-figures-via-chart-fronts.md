---
status: accepted
---

# Constant at-a-glance figures render through the chart fronts

The `const-*.svg` at-a-glance figures (ADR 0010's audit left most constants
without one) are extended to every visually meaningful constants class:
`BAR_MODE`, `HISTOGRAM_TYPE`, `ORIENTATION`, `SHOW_GRID`, `SCALE`,
`NORMALIZE`, `EMPHASIS`, `ASPECT_RATIO`. `FIG_FORMAT` (nothing to draw),
`COLORS` (Colormaps guide) and `THEME` (Theme Gallery) stay figure-less.

Where the constant is a chart or panel *setting*, the figure is produced by
calling the datachart fronts themselves (`BarChart`, `Histogram`, `Heatmap`,
`LineChart`, …) and saving the returned figure — not by re-drawing the
effect with raw matplotlib. Package-specific behavior (`EMPHASIS` muting
rules, bar slotting, shared bins) is then accurate by construction and
cannot drift from the implementation; the docs also show real package
output. Raw matplotlib remains only for constants that are matplotlib
pass-throughs with no front to exercise (fonts, markers, line styles).

Shared conventions stay: 7 in content width, monospace `CLASS.MEMBER`
labels, DEFAULT_THEME styling, one generator function per class in
`docs/assets/scripts/generate_constant_viz.py`. Comparison panels share one
dataset chosen to be legal for every member (heatmap values in (0, 1) so
LOGIT works; positive growth data for SCALE), with a footnote where a
member's distinguishing case (negatives for SYMLOG/ASINH) is not shown.

## Considered options

- **Raw matplotlib for all new figures** (existing script style). Rejected:
  hand-drawn `EMPHASIS`/`BAR_MODE` panels would silently drift from the
  package's actual rendering rules.
- **Per-member tuned datasets in comparison panels.** Rejected: the point
  of a comparison strip is the same data under different settings; a
  footnote covers the members whose strengths need different data.
