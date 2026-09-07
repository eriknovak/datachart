---
status: accepted
---

# Treemap tiles one level of nested part-of-whole data through one layer

A treemap (issue #94) shows composition — disk usage, a budget, population
by continent and country — as rectangles whose area is the value. It is
non-Cartesian like the Sankey (ADR 0026): the layer owns an axes-off 0–1
space and the axes carry nothing.

## Commitments

- **Input is a `data` list of `{label, value}` records.** A record may carry
  `children`, a list of records of the same shape, for one level of nesting;
  a child cannot carry `children`. A parent with `children` either omits
  `value` or carries one equal to the children's sum; a mismatch raises
  `ValueError`. Zero and negative values raise; a silently vanishing tile
  surprises more than an error. A list of chart dicts renders one treemap
  per subplot (`CHART_CONFIGS`: `multiplot: False, subplots: True`).
- **Squarify only.** Every level is sorted by value descending and tiled by
  the squarified algorithm in the axes' pixel aspect at draw time, read from
  the axes bbox, so tiles look square at any `figsize` and in a `Grid` cell.
  No algorithm knob.
- **One `TreemapLayer` per chart** holds every record and draws `Rectangle`
  patches, no furniture: `axis("off")`, 0–1 data space, `"cartesian"`
  projection. `Panel` rejects treemap figures with a "use `Grid`" message;
  `Grid` accepts them as ordinary cells.
- **Colors shade by level, not by rank.** Each top-level record takes the
  next `color_general_multiple` color keyed by label. Every child of a group
  shares one tint, `plot_treemap_level_shade` (0.35; 0 gives the flat group
  color) lighter than the group; siblings never differ in hue or alpha, so
  the depth is the only thing the tint encodes.
- **A group is a box.** Its header band sits on top and one border at
  `plot_treemap_group_edge_width` (1.0) encloses band and leaves, so their
  edges align. Leaves are separated by an edge stroke only
  (`plot_treemap_edge_color` white, `plot_treemap_edge_width` 0.6; GRAYSCALE,
  HATCH, INK override the color as for bars); the group border takes the
  same color, so every stroke in a treemap matches the theme's bar edge.
  Groups are separated by a data-space pad, `plot_treemap_group_pad` (0.02
  of the span).
- **Emphasis is per record**, not per chart: an `emphasis` key on any record
  (group or leaf; a leaf's role overrides its group's) takes the `EMPHASIS`
  roles. `background` mutes the tile (`muted_color`, `muted_alpha`, muted
  label); `highlight` draws the tile or group border in `font_general_color`
  at `plot_treemap_highlight_edge_width`, the border only, never bold text.
  Roles are explicit: highlighting one group does not mute the others. The
  front's per-chart `emphasis` argument raises, as for Sankey.
- **Labels.** A group draws a header band across its top in the
  `font_subtitle_*` style, band height from the font size, leaves tiled
  below it. When the group is too short for the band, the band font shrinks
  in steps to `plot_treemap_min_fontsize`; if it still does not fit, the
  group draws no band and no label, and `show_legend` is what names it.
  A label never sits over the leaves. A leaf label is centred in the tile
  in `font_general_*` scaled by `plot_treemap_level_font_scale` (0.85) per
  nesting level; `show_values` writes the value under it in the
  `plot_bar_value_*` style, scaled the same way, formatted by
  `value_format`, off by default. Every label, band included, is drawn in
  its font color over the white halo, never in white on the band.
- **Text fits or degrades in a fixed order**, measured in pixels: as is;
  wrapped at the space nearest the label's middle; shrunk in steps down to
  `plot_treemap_min_fontsize` (6). With `show_values` the ladder runs with
  the value first and without it second, so the value is dropped before the
  label. Only when nothing fits is nothing drawn. Text sits behind a white
  halo of `plot_treemap_label_halo_width` (2; 0 disables). No `show_labels`
  switch: empty labels do that.
- **`show_legend`** lists the top-level groups only, off by default; it
  rescues groups too small for a band.
- **`texts`** annotations are placed in the 0–1 tiling space.

## Considered options

- *Flat data only.* Rejected: composition data is naturally grouped, and a
  second level is where a treemap earns its place over a bar chart.
- *Unbounded nesting.* Rejected: unreadable at these figure sizes, and it
  makes the color and label rules recursive for no user.
- *Caller-ordered tiles.* Rejected: squarify needs descending values, and
  readers expect the largest tile top-left.
- *Selectable tiling (slice, dice).* Deferred until asked.
- *`highlight` mutes every other group.* Rejected: every other chart uses
  explicit roles per item; a relation would be a second emphasis model.
- *Front-level `emphasis="A"` naming a label.* Rejected: the role belongs
  with the record it describes, and the front argument keeps its per-chart
  meaning everywhere else.
- *Group label in a legend only.* Rejected: a band never collides with leaf
  labels and is the shape readers know from disk-usage tools.
- *Shading leaves by rank, largest darkest.* Rejected after the preview:
  siblings in different tints read as different categories, and the area
  already carries the rank.
- *Group border in the group color.* Shipped first, then dropped: a colored
  frame around a band of the same color reads as a second, heavier band
  edge, and it is the one stroke in the chart that does not match the bars.
- *Band over loose leaves, no group border.* Rejected after the preview:
  the band's edge and the stroked leaves' edge do not meet, so the band looks
  like it hangs over its children.
- *Drop any label that does not fit at its size.* Rejected after the
  preview: a nested treemap then has more blank tiles than named ones.
- *Bold text on `highlight`.* Rejected after the preview: the border is the
  signal; bolding shifts the label's fit and reads as a different font.
- *Corner label over the leaves when a group is too short for a band.*
  Rejected after the preview: it collides with the first leaf's label and
  reads as part of that tile.
- *White band text.* Rejected after the preview: one text color with one
  halo everywhere; a second text color per surface is a second rule.
- *Tiling the unit square regardless of aspect.* Rejected: squarify's
  promise only holds in pixel space.
