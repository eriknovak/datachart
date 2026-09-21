---
status: accepted
---

# A dark theme inverts the furniture, not the marks

Every shipped theme draws on a white figure, and the base furniture (spines,
ticks, grid, fonts, value labels, legend frame, heatmap frame) is tuned for
it. Slides, dashboards, and dark-mode documentation have no matching theme,
and a user cannot get there by overriding the two face colours (#244).
`DARK` is the first theme that sets `figure_facecolor` and `axes_facecolor`
to a dark value, and it sets the rule any later dark theme follows.

## Commitments

- **Named for the trait, not the palette.** The theme is `DARK` because the
  background is what a user is looking for, and its palettes may change
  without the name lying. `Neon` was the first candidate for the sequential
  map and failed the gallery's colour-blindness scoring (deutan 3.7, protan
  3.5, normal 7.8) besides running non-monotone in lightness, which a value
  scale cannot do; the map is `Viridis`. The diverging map is `Coolwarm`,
  the only one whose both ends stay clear of a near-black page.
- **Two-tone background.** The figure face is near-black and the axes face a
  step lighter, so the plotting area reads as a panel on the page the way it
  does on a light theme's white-on-white with spines.
- **Every furniture colour has a light counterpart.** A dark theme overrides
  every attribute whose base value is black or dark grey: spines, ticks, tick
  and axis-label fonts, grid, legend frame and labels, value labels,
  annotation text and boxes, heatmap and calendar-heatmap frame and edges,
  colorbar labels. Furniture is the set of attributes that contrast with the
  face; marks keep their own colours and cycles. The theme is complete on its
  own — no attribute waits for the user to fix its contrast.
- **Heatmap cell labels stay cell-relative.** A cell's label colour follows
  the luminance of the cell's own colour (white text on a dark cell), never
  the figure face. A light cell on a dark figure keeps dark text because the
  text sits on the cell, not on the page. The rule is unchanged by this theme.
- **The background is baked at figure creation.** `save_figure` never
  consults the config, so a `DARK` figure keeps its face in PNG and SVG and
  `transparent=True` drops it as on any theme. No saving code changes.

## Considered options

**Naming the theme after its palette (`NEON`)** was rejected, and the
rejection paid off immediately: the palette was a candidate under a
colour-blindness gate, `Neon` failed it, and a theme called `NEON` drawing in
Viridis would have been stranded. `Harbor` earns its name because there the
palette is the trait.

**A `dark` flag that inverts any theme** was rejected. Every theme tunes
its furniture to its face by hand; a mechanical inversion would give thirteen
untested variants and no one owning any of them.
