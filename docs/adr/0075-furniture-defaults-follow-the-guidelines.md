---
status: accepted
amended-by: [0077]
---

# Furniture defaults follow the guidelines: no legend title, solid grids, and a warning when series outrun the palette

The themes follow the visualisation guidelines the gallery cites (recessive
furniture, identity never carried by colour alone), but three defaults did
not. Every legend carried the title "Legend", a word that says nothing the
box does not already say. Four print themes drew dotted grids, so the grid
competed with the dash cycle of the lines it sits under. And a seventh
series in a six-colour theme silently took the first series' colour, so two
series read as one and nothing told the author (issue #292).

## Commitments

- **A legend has no title unless the caller names one.** The base theme's
  `plot_legend_title` is `None`, the legend style resolver drops `None`
  keys, and no predefined theme sets a title. A theme key or the per-figure
  `legend` setting still names one, and a relationship view keeps naming
  its hue column, since there the title carries information.
- **A grid is a solid hairline one step off the face.** Every predefined
  theme draws its grid with the base's solid style; a theme tunes the grid's
  colour and alpha, never its dash. This amends ADR 0074's key-for-key
  equality of the six derived bundles: `MUTED`, `MUTEDHATCH`, `HATCH` and
  `SLATEHATCH` now differ from the dictionaries they replaced in the grid
  style, and their shared furniture dictionaries no longer carry it.
- **Series past the palette end warn.** `warn_palette_overflow(palette,
  count, what)` in the colours module raises a `UserWarning` when a cycling
  palette (a colour list, a custom palette, a plain colour) has fewer
  colours than the units drawing from it, naming both counts and suggesting
  emphasis, subplots or a longer palette. `create_color_cycle` calls it
  when told what the colours are for: the panel says `series` once per
  palette when it pools its groups, the scatter and parallel coordinates
  layers say `hue levels`, the gantt, raincloud, treemap and network
  layers `groups`, the sankey layer `nodes`; a cycle built without a
  purpose, for a swatch or a sample, stays silent. A composition renders
  its stored panels again and may warn again, or for the first time when
  pooling pushes two sources past the palette; Python's default filter
  shows a repeated message once. A pypalettes
  name interpolates its colormap rather than cycling, so it never warns:
  the colours differ, even if not by much. A one-colour palette never
  warns either: a one-ink theme (quill) or a plain-colour lead is
  monochrome by design and its etch and dash patterns carry identity. A
  print theme whose pattern cycles outlast its greys still warns, since
  the advice to mute or split applies there too.

## Considered options

- **Keep "Legend" and let themes opt out.** Rejected: no shipped theme
  wanted the title, and a default every theme overrides is not a default.
- **Warn from `get_discrete_colors`.** Rejected: it is called for legend
  swatches and samples as well as series, so one chart would warn several
  times from library frames. The panel's pooled count is the one place
  that knows how many series share a palette.
- **Extend the palette by interpolating past its end.** Rejected: an
  interpolated seventh colour lands between two tuned ones and fails the
  palette gate (ADR 0073) for the very readers the palette was stepped for;
  a warning leaves the fix with the author, who can mute, split or extend.
- **Keep the dotted grids as the print themes' signature.** Rejected: a
  dotted grid under dashed lines is two patterns competing, and greyscale
  print distinguishes a light solid hairline from the marks just as well.
