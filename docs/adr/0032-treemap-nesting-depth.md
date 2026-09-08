---
status: accepted
---

# Treemap nests to four levels through the same group rules

ADR 0028 shipped `Treemap` with one level of `children` and rejected
unbounded nesting as unreadable at these figure sizes. Issue #100 asks for
deeper hierarchies — folders in folders, region → country → city. We bound
the depth instead of the feature: a record may nest to four levels, and the
group rules of ADR 0028 apply at every level unchanged, so nesting adds no
second rule for bands, tints, or emphasis.

## Commitments

- **Four levels, then an error.** The `data` list is level 1; a record's
  `children` are one level deeper. A record at level 4 carrying `children`
  raises `ValueError` naming the limit. The cap is the readability stance of
  ADR 0028 made concrete: four levels cover the hierarchies that asked for
  this, and a fifth is not legible at the default figure sizes.
- **A group is a group at any level.** An inner group is tiled inside its
  parent's leaf area exactly as a top-level group is tiled in the axes: its
  box is squarified among its siblings by total, its header band takes the
  same ladder (the band font shrinks in steps to `plot_treemap_min_fontsize`,
  and a group too short for a band draws a border only, no label), and one
  border at `plot_treemap_group_edge_width` encloses band and children.
  Groups are separated from their siblings by the stroke only; the data-space
  pad `plot_treemap_group_pad` stays a top-level gap, since an inner pad
  takes area from the leaves that have the least.
- **Tint and font compound per level.** Each level is
  `plot_treemap_level_shade` lighter than its parent, applied once more per
  level, and labels scale by `plot_treemap_level_font_scale` per level, both
  as the rules already read. A group's band keeps the group's own color.
- **Emphasis inherits all the way down.** A record's `emphasis` applies to
  its whole subtree; a descendant's own role overrides it, at any depth.
- **The legend stays top-level.** `show_legend` lists the level-1 records
  only: inner groups share their ancestor's hue, so a legend entry could not
  tell them apart. An inner group too short for a band is named by hover
  (ADR 0031) and by nothing else.
- **Hover reports every level.** Bands and tiles register at every depth,
  each with its label and total, as in ADR 0028.

## Considered options

- *Keep one level.* Rejected: the "Rest of" and `subplots` workarounds lose
  the hierarchy the treemap is chosen to show.
- *Unbounded nesting.* Rejected again: it forces a caller to discover the
  depth at which the chart stops being readable; a stated cap is a contract.
- *Three levels.* Rejected: region → country → city → district and
  folder trees reach four often enough to make three feel arbitrary.
- *No bands below the top level, border only.* Rejected: the band ladder
  already degrades to a border when short, so a separate rule for inner
  groups is a second rule for the same case.
- *Bands at every level regardless of height.* Rejected: this is what made
  nesting unreadable in ADR 0028's preview.
- *Group pad at every level.* Rejected: the pad exists to separate palette
  colors; inner groups share a hue and a pad there only shrinks the leaves.
- *Legend entries for inner groups.* Rejected: same hue, no distinguishable
  swatch.
