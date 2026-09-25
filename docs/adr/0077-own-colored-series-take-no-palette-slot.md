---
status: accepted
---

# A series with its own colour draws none from the palette

ADR 0075 warns when more series draw from a cycling palette than it has
colours. The panel counted every colour-taking layer, so a stacked area
chart whose seven bands each set `plot_area_color` still warned that "colours
repeat" although none of its colours came from the palette, and the two guides
that colour their series by hand tripped the warning in every cell (issue
#297). A warning that is false where the author already did what it asks
teaches readers to ignore it where it is true.

## Commitments

- **A layer whose style sets its primary mark's colour takes no palette
  slot.** It does not advance the pooled colour cycle, so the series after it
  take the palette's colours in order as if it were not there, and it does not
  count toward the overflow warning, exactly as a background-emphasis layer
  already did not. The layer receives its own colour as the draw context's
  colour, so the marks that follow the series colour (an area fill under a
  line, a stack outline, error bars) follow it too. This amends ADR 0075: the
  warning's count is the series that draw from the palette, not the series
  that take a colour.
- **The primary mark is named per layer.** A layer class names the resolved
  style dictionary of its primary mark (`color_style`), and `own_color()`
  reads the colour set there: the line for the line, bump and radial line
  layers, the fill for the stacked area layer, the bar for the bar and radial
  bar layers, the bins for the histogram and radial histogram layers. A layer
  that colours by group or by a colormap (scatter hues, box and violin groups,
  contours, gantt groups, treemaps, networks) names none and keeps its cycle
  slot: its style colour is one input among several, not the series colour.

## Considered options

- **Count only for the warning and keep the slot.** Rejected: an explicitly
  coloured first series would still push the second onto the palette's second
  colour, so a two-series chart with one pinned colour would skip the
  palette's lead colour for no visible reason.
- **Pass `None` as the context colour, as for a muted layer.** Rejected: a
  stack outline or an area fill whose own colour is unset falls back to the
  context colour, and `None` there would hand the mark to matplotlib's default
  cycle in a colour from no palette of ours.
- **Leave the count alone and let the guides set a longer palette.**
  Rejected: it keeps a warning whose message is false, and it puts the fix in
  the notebooks where the next hand-coloured chart trips it again.
