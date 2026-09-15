---
status: accepted
---

# Ink rendering attributes in themes

ADR 0027 let a theme carry exactly two render-scoped attributes, the sketch
wobble and the halo, and nothing else past the `StyleAttrs` contract. A
quill-and-ink theme (`THEME.QUILL`) needs marks matplotlib has no
property for: a series line whose width varies along its length like a
broad-nib pen, fills etched by hand instead of tiled with a hatch, a value
scale drawn as etch density instead of a colormap, and ink-colored
furniture on a ground a theme can tint. It also needs series to differ by line
style and marker instead of color, since the theme owns one ink.

We extend the enumerated set, each attribute `None` (off) in every other
theme, so the mechanism alone alters no output.

**Path effects**, both in `layers.py` beside `_halo_effects`, both seeded from
the path (an etch also from its placement, since every bar shares one unit
square) so a redraw looks the same:

- `plot_ink_stroke` — a dict (`width_scale`, `nib_angle`, `nib_floor`,
  `wobble`, `taper`; `swell` and `noise` model pen pressure instead). The
  `InkStroke` effect draws a series line as a filled ribbon: the width is the nib projected on the travel direction, modulated
  by a slow wobble, tapered at the ends, split along the dash pattern, and
  capped against the axes height so small multiples never blob. It rides on
  the halo seam (`Layer._stroke_halo`), so exactly the series lines that take
  a halo take the stroke, and contour level lines take it too; legend handles
  inherit it through `update_from`.
- `plot_etch` — a dict (`spacing`, `jitter`, `angle_jitter`, `line_width`,
  `wash`, `color`). The `Etch` effect replaces a hatched patch's hatch tile
  with jittered lines clipped to its outline; the hatch string still selects
  the pattern and `.` stipples. Patches (bars, histograms, box, violin and
  ridgeline bodies) lay a `wash` of their face color over the axes ground
  under the lines; fills under lines (`show_area`, stacked areas) etch
  without a wash, so what sits beneath stays visible. It is attached where a
  layer draws a hatchable fill — never through `rcParams["path.effects"]`,
  which would route every text through path drawing.
- `plot_value_etch` — a dict (`washes`, `hatches`, one entry per step). With
  `plot_etch` on, the value-encoded cells of a heatmap, calendar heatmap,
  hexbin and filled contour draw one step per value range (wash and etch
  density) and a legend of the steps replaces the colorbar, placed outside
  right by the panel's outside-legend fit. A filled contour draws as a
  relief map: etched bands, its level lines with labels over them, and
  consecutive bands sharing a step merged into one legend entry.

**Ground and furniture colors**, applied by `Panel` beside the spines and
ticks (bare panels take the ground only): `figure_facecolor`,
`axes_facecolor`, `axes_spines_color`, `axes_ticks_color`,
`plot_legend_edge_color`, `plot_legend_face_color`. The label and value halo
(`_halo_effects`) takes the axes face color, so a halo never punches white
holes in a tinted ground.

**Cycles** (growing ADR 0004): `plot_linestyle_cycle` and
`plot_marker_cycle`, assigned by the panel per series keyed by chart hash,
delivered through the `DrawContext`, beside `plot_hatch_cycle`. The line
style reaches line, bump and radial line series; the marker reaches scatter
and radial scatter series (a marker entry is a marker string, or
`{"marker", "hollow"}` to draw it as an outline). A chart style that sets
its own line style or marker wins. With `plot_etch` on, the hatch cycle also
feeds line area fills and stacked areas, so each area etches its own
pattern; without it their fills are unchanged, so `HATCH` keeps its output.
`plot_box_hatch`, `plot_violin_hatch` and `plot_ridgeline_hatch` give the
bodies a pattern of their own.

**Chart-specific ink looks**, each an ordinary nullable style key:
`plot_sankey_node_fill` (nodes as outlines), `plot_treemap_etch_density`
(the top-level group's pattern repeated per depth; boxes fill with the
ground so outer etching never shows through), `plot_network_edge_ink_stroke`
(edges as pressure strokes: a directed edge draws as a stroked shaft so the
pressure shows) and `plot_network_group_linestyle` (a group hull as a ring,
not a tinted disc). Network node groups take the marker cycle's shapes, as
series do. The theme-defaultable settings grow by
`chart_default_node_label_position`, the network's node label placement.

## Commitments

- **The enumerated set grows by exactly these keys.** A theme still cannot
  carry arbitrary rcParams; growing the set again revisits this ADR.
- **`None` means off, and every existing theme keeps `None`**, so the golden
  baselines stay byte-identical.
- **Effects live on the artists**, resolved at build like the halo, so
  composition redraws the look without config access at draw time.
- **No global rc mutation**, as ADR 0027 commits.

## Considered options

- **rc `path.effects` for the etch.** The prototype's route. Rejected: every
  text, tick and spine goes through the effect's `draw_path`, which is slow
  and needs per-artist exceptions.
- **Encoding the series slot in near-identical ink colors.** The prototype's
  stand-in for the cycles: the color cycle handed out six inks one bit apart
  and hooks turned the slot into a line style. Rejected: it breaks any
  consumer that reads the color back, and a user palette cannot use it.
- **A free-form "ink" dict holding every knob.** Rejected: the chart-specific
  looks belong to their chart's style family, where a chart `style` can
  override them one key at a time.
