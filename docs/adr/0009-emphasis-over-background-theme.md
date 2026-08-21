---
status: accepted
---

# Emphasis replaces the background theme; themes are named for their look

`THEME.BACKGROUND` existed to build highlight figures: render context charts
under a grey full-figure theme, render the highlighted chart normally, and
compose them in a `Panel`. That made a styling *relationship* (this layer is
context for that one) a *global* concern — it required switching the singleton
config between builds, hardcoded greys that clash with the other themes, and
restyled figure furniture that composition then had to ignore.

We replace it with **emphasis**, a per-chart role at both seams: an
`"emphasis"` key in a charts list, and an `emphasis=` list on `Panel` aligned
with its figures. Values: `"background"` (muted: theme's `muted_color`,
lowered alpha, thinner strokes, pushed-back z-order, excluded from the
legend), `"highlight"` (front z-order, slightly bolder), unset (as today).
The muted look derives from the active theme via `muted_*` style attributes,
so background layers harmonize with any theme. `THEME.BACKGROUND` is removed,
not deprecated.

For composed parallel-coords highlighting to be correct, per-dimension
normalization moves from the layer to the `Panel` (shared min/max across all
parallel layers, like shared histogram bins) — a single-layer panel keeps
today's output.

The same release renames the role-based themes to look-based names —
`PUBLICATION → INK`, `ACADEMIC → HATCH` (which also drops its serif fonts for
`INK`'s sans stack, making it a second publication-grade look rather than a
font niche). Hard rename, no aliases: pre-1.0, no known external users.

## Considered options

- **Keep a muting theme (or partial style overlay).** Rejected: emphasis is a
  relationship between layers in one panel, not a global style state; any
  config-switching workflow reintroduces ordering traps.
- **Boolean `muted` flag.** Rejected: `"highlight"` needs its own level —
  front z-order cannot be expressed by default styling.
- **Deprecation aliases for renamed themes.** Rejected as noise: no external
  users; the break is recorded in the 0.8.0 changelog.
