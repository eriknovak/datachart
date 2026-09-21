---
status: accepted
---

# A centred norm selects the theme's diverging colormap

`Heatmap` and `CalendarHeatmap` pass `norm` straight to matplotlib, and every
theme sets one sequential `plot_heatmap_cmap`. A correlation matrix or a
model-difference heatmap runs the sequential map from its minimum: zero lands
on an arbitrary shade and the sign is invisible. Users get the centred form
only by passing a `CenteredNorm` instance and a diverging map by hand, which
also bypasses the theme (#247).

## Commitments

- **Two named norms, resolved in the layer.** `NORMALIZE.CENTERED` builds a
  `CenteredNorm` around `vcenter` (a new front parameter, default `0`); a
  given `vmin`/`vmax` sets the half-range to the larger distance from
  `vcenter`, so the scale stays symmetric. `NORMALIZE.TWOSLOPE` builds a
  `TwoSlopeNorm(vcenter, vmin, vmax)` for the asymmetric case. Every other
  `norm` string keeps going to matplotlib verbatim, with `vmin`/`vmax` beside
  it as today. The two are resolved at build, so the norm survives `Panel`
  and `Grid` like every other resolved style.
- **A second theme-level colormap, not a flag on the first.** Every theme
  sets `plot_heatmap_cmap_diverging`; `plot_calendar_heatmap_cmap_diverging`
  is `None` and derives from it, mirroring the sequential pair (ADR 0044). A
  centred or two-slope norm takes the diverging map. A `plot_heatmap_cmap`
  given in the chart's own `style` still wins, because an explicit chart
  colormap is the one thing the user typed; the theme's sequential map never
  applies under a centred norm.
- **Every theme gets a real diverging map, including the hue-less ones.** The
  grayscale and quill themes (sequential `Greys`) and the Cividis themes take
  `RdBu` like the rest. A diverging map's job is to show sign, which a
  gray-only ramp cannot; the per-cell label rule already judges each cell's
  luminance, so both dark ends stay readable. Themes whose sequential map is
  blue-led (`Blues`, `YlGnBu`, `PuBu`, `BuPu`) take `PuOr` or `BrBG` so the
  two maps read apart in the gallery.
- **The value legend places a step edge at the centre.** Under a centred norm
  the even-step legend recomputes its edges so one falls on `vcenter`, and the
  plain colorbar adds a tick there. A legend that straddles zero with one step
  would hide the sign the norm exists to show.

## Considered options

**Auto-detecting a signed matrix and centring silently** was rejected. A
matrix that happens to span zero is not always a signed one, and the theme's
sequential map would change under a user's feet as their data moved.

**Reusing `plot_heatmap_cmap` with a diverging default in every theme** was
rejected. The sequential map is the right default for counts and intensities,
which are most heatmaps; making every heatmap diverging to serve the
correlation case inverts the common and the rare.

**Accepting a matplotlib norm instance and leaving the colormap to the user**
is what exists today and was rejected as the only path: it works, but
bypasses the theme entirely, so a theme switch leaves the diverging map
behind.
