---
status: accepted
---

# Themes may supply defaults for chart settings and per-series hatch cycles

Style attributes (`StyleAttrs`) and chart settings have been strictly separate:
themes style what is drawn, while settings (`show_grid`, `show_values`) decide
whether it is drawn at all. That boundary blocks whole theme identities — a
Material-style theme cannot show its signature light grid, and a minimal
benchmark theme cannot label bars, unless every chart call opts in.

We open the boundary in one narrow, explicit way: a theme may carry **nullable
defaults** for a small set of chart settings (grid visibility, bar value
labels). Resolution stays one-directional — an explicit chart setting always
wins; a theme default applies only when the call leaves the setting unset
(`None`). `None` in the theme means "no opinion", preserving today's behavior
for all existing themes.

The same release adds a **hatch cycle**: a theme-defined sequence of hatch
patterns assigned per bar/histogram series by the `Panel`, exactly parallel to
the color cycle (keyed by chart hash, delivered through the `DrawContext`).
An explicit per-chart hatch style wins over the cycle.

## Commitments

- **Settings still exist and still win.** Theme defaults never override an
  explicit setting, only fill its absence.
- **The set of theme-defaultable settings is enumerated**, not open-ended:
  grid visibility and bar value labels. Growing it requires revisiting this
  ADR.
- **Hatch assignment lives in the `Panel`**, beside color assignment — layers
  receive the resolved hatch via `DrawContext`, never consult the config at
  draw time.
- **A theme with `None` defaults and no hatch cycle behaves exactly as
  before** — the mechanism alone alters no output. The modernized themes that
  ship alongside this ADR do exercise it: every theme carries a muted grid
  default (`"y"`), `MINIMAL`/`MATERIAL`/`ACADEMIC` default bar value labels
  on, and `ACADEMIC` carries the only hatch cycle.

## Considered options

Keeping the boundary closed and documenting "pass `show_grid=...` with this
theme" was rejected: a theme that needs a usage manual is not a theme.
Promoting `show_grid`/`show_values` fully into `StyleAttrs` was rejected: it
would silently flip output for every existing caller and blur the
settings-are-per-chart rule everywhere, not just at the default.
