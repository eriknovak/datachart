---
status: accepted
---

# Nested Panel figures flatten losslessly into the outer Panel

`Panel` output already passes `_extract_groups` (in `compose.py`) (its transport is
`{"type": "overlay", "panel": ...}`), so `Panel([Panel([f1, f2]), f3])` runs
today — but lossily: extraction rebuilt `LayerGroup`s without their per-figure
prefs, silently dropping the inner panel's `y_axis`, `z_order`, and
`legend_label`. We make nesting a first-class, lossless operation:
`Panel([Panel([f1, f2]), f3])` is equivalent to `Panel([f1, f2, f3])`.

## Commitments

- **Flattening identity.** A nested Panel contributes exactly its layer groups
  with their per-figure prefs preserved. Nesting composes to any depth, since
  every Panel figure stores flat merged groups.
- **Outer furniture wins.** The inner Panel's panel-level settings (title,
  labels, `bar_mode`, limits, legend, thresholds) are discarded; the outermost
  call's settings apply. The transport keeps carrying only what composition
  consumes.
- **Outer dict options override only when explicitly given.**
  `{"figure": inner_panel, "y_axis": "right"}` re-assigns all of the inner
  panel's groups; an omitted option leaves each inner group's own pref intact.
  For plain chart figures nothing changes — their groups carry default prefs.
- **`OverlayChart` inherits nesting silently** through the shared
  implementation; it stays deprecated and undocumented (removed from the docs
  reference).
- **Verified by equivalence**: unit tests assert nested == flat (groups, prefs,
  rendered pixels) and a golden case pins the rendering.
