---
status: accepted
---

# A diagonal reference line is a third line family, defined by slope and intercept in data space

Reference lines are axis-aligned: `vlines` fixes an x, `hlines` fixes a y. A
line through the data space — the chance line on a ROC plot, the parity line
on a predicted-versus-true or calibration plot, the fit on a Q-Q plot — has to
be faked as a second series, which takes a cycle color, a legend entry, and a
bar slot (#246).

Reference lines resolve their style at build in `_resolve_ref_lines` and draw
from the panel in `_draw_ref_lines`, after scales and limits are set, pooled
per axes through `REF_KEYS`. The diagonal takes the same seam, so it survives
`Panel` and `Grid` for free.

## Commitments

- **A third family, not a generalisation of the two.** `dlines` sits beside
  `vlines` and `hlines` with its own `DLineSettingAttrs`, `DLineStyleAttrs`
  and `plot_dline_{color,style,width,alpha}` theme keys. A single line type
  carrying `x`, `y`, `slope` and `intercept` would make the wrong fields
  typable on every line, and the two existing families are already split down
  to separate style types and theme keys.
- **Slope and intercept, defaulting to parity.** `slope=1, intercept=0` are the
  defaults, so `dlines={}` draws `y = x`, the line the three motivating plots
  want. Two points were rejected: a Q-Q or calibration reference is computed
  as a slope and an intercept, and a point pair would be converted back.
- **Unclipped lines use `ax.axline`; clipped lines are a plotted segment.**
  Without `xmin`/`xmax` the line spans the axes and follows zoom, which is
  what a chance or parity line wants. With either bound the line becomes a
  segment between two computed endpoints, mirroring how `hlines` clips, and
  the limit-restore guard `_draw_ref_lines` already applies keeps the segment
  from widening the axes under autoscale. Two draw paths behind one setting
  are accepted because `axline` cannot be clipped to a data range. A
  non-linear axis takes the segment path too, sampled across the axis
  limits: `axline` refuses a slope where either scale is non-linear, and a
  two-point segment would draw the chord rather than the curve. The line
  then no longer follows the zoom, which only the unbounded linear case does.
- **Data space only.** The line is straight in data coordinates, so it curves
  on a log axis, where it is sampled rather than refused. The guide documents
  this; there is no transform option. A
  user who wants a straight line on a log axis knows the transform and can
  compute the slope and intercept in it.
- **Every front that takes `hlines` takes `dlines`.** Fifteen fronts today. A
  diagonal rarely makes sense on a box or swarm plot, but the seam is shared,
  the cost is a parameter, and a gap in the trio on some fronts would be the
  surprise (ADR 0045 makes the same call for emphasis rules).
- **Style defaults follow the horizontal line**, including `plot_dline_color`
  resolving `None` to matplotlib's first cycle color, as `plot_hline_color`
  does. Bands resolve `None` to the muted grey (ADR 0036); the line families
  do not, and the diagonal keeps parity with its siblings rather than
  changing one of three. Moving all three to the muted grey is a separate
  decision.
- **Draw order** is the reference-line rung of the ladder in ADR 0054.

## Considered options

**Generalising `hlines` with an optional `slope`** was rejected. It reads as
the smaller API, but it makes `y` mean "intercept" only when `slope` is
present, and the theme keys and typings would have to carry the diagonal's
semantics under the horizontal name.

**A dedicated `parity=True` flag** was rejected. It covers two of the three
motivating plots and none of the fitted Q-Q reference, and would be the only
reference setting that is not a dict.

**`axline` with a clip path for bounded lines** was rejected. It keeps one
draw path, but the clip is in display space and must be recomputed on every
limit change, which the panel does not own after render.
