---
status: accepted
---

# A front parameter is snake_case, a mode is named for what it modes, and a toggle is `show_<singular>`

ADR 0067 unified one batch of drifted names and built the mechanism for
renames, but left a second batch in place (issue #322): `startangle` and
`innerradius` on the radial chart against `num_bins`, `ci_level` and
`week_start` everywhere else; `filled` on the contour against `fill` on the
ridgeline; `mode` on the swarm and raincloud against `bar_mode`; `mincnt` and
`gridsize` on the hexbin, matplotlib's own abbreviations; `show_colorbars`,
plural, on four fronts whose layers read one bool beside a singular
`colorbar` setting. Each is a one-off, and each renames after 1.0 would cost
a major version. The renames alone would not stop a third batch; the rule
does.

## Commitments

- **The naming rule.** A front parameter is `snake_case` with whole English
  words: no camelCase, no matplotlib abbreviation. A selector whose values
  are a `<THING>_MODE` domain is named `<thing>_mode`, so the parameter and
  its constant class share a stem. A boolean toggle is `show_<noun>` with the
  noun singular, matching the setting it toggles (`show_legend`/`legend`,
  `show_colorbar`/`colorbar`). A selector for something only its front has
  keeps its own noun (`layout`, `diagonal`, `rank_by`, `reduce`, `levels`) —
  ADR 0067's carve-out stands for those, and is narrowed here to exclude
  `mode`. This amends ADR 0067.
- **Seven renames under the rule.** `startangle` → `start_angle` and
  `innerradius` → `inner_radius` (radial); `filled` → `fill` (contour, joining
  the ridgeline's existing name); `mode` → `swarm_mode` (swarm, raincloud);
  `mincnt` → `min_count` and `gridsize` → `grid_size` (hexbin);
  `show_colorbars` → `show_colorbar` (heatmap, calendar heatmap, contour,
  hexbin). The style key `plot_hexbin_gridsize` is a theme attribute, not a
  front parameter, and is out of this record's scope.
- **Deprecated through ADR 0067's mechanism, out with the rest at 1.0.** Each
  old keyword stays in its front's signature, listed in the row's `renamed`
  mapping, and warns with a `DeprecationWarning` for one release; the release
  checklist removes it with the batch already there (`valfmt`, `type`,
  `normalize`, `features`, `show_heatmap_values`, `label`).
- **Every settled name on two or more fronts is a `SHARED_PARAMETERS` row**,
  so the conformance test guards it: `fill`, `swarm_mode`, `show_colorbar`
  join the table; the `mode` and `show_colorbars` rows go. One-front names
  (`start_angle`, `inner_radius`, `min_count`, `grid_size`) cannot drift and
  get no row.
- **The docs follow the table.** Guides, use cases and reference pages use
  the new names; the deprecated keyword appears only in the changelog.

## Considered options

Keeping `mode` under ADR 0067's carve-out was rejected: the carve-out's
argument was that one shared noun would blur five meanings, and
`swarm_mode` sharpens rather than blurs — it also makes the `bar_mode` /
`BAR_MODE` pairing a rule instead of one case. Keeping `gridsize` as one
English word was rejected: it sits beside `size_range` and `num_bins`, and
matplotlib's spelling is the only reason it exists. Keeping `mincnt` and
`gridsize` as pass-through names was rejected: the fronts document their own
meaning for both, so they are not pass-throughs. A rename without a recorded
rule was rejected: it fixes seven names and predicts nothing.
