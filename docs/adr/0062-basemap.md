---
status: accepted
amended-by: [0063]
---

# The basemap draws unprojected outlines fetched into a cache

ADR 0060 delivered the image half of issue #263 and left the vector half
open: coastlines and borders under a chart whose x and y are longitude and
latitude. A pre-rendered map reaches those figures through `ImageChart`
already, but it has to be made somewhere, it does not rescale, and its edges
are pixels.

The two obvious routes both fail on this package's shape. `cartopy` is the
standard, but its model is `plt.axes(projection=...)` returning a `GeoAxes`,
while `render_chart` builds plain axes and `Panel` assumes it can draw any
layer into any of them; using cartopy only to read geometry would make GEOS
and PROJ system dependencies for a package that today needs numpy,
matplotlib, scipy and pypalettes. So the outlines are Natural Earth's, read
as plain arrays.

Where they live is the other half of the question, and the answer is the
cache rather than the wheel. The package is a drawing library, and a drawing
library's wheel should carry the code that draws and nothing else. Bundling
164 KB of outlines would buy offline rendering, a hermetic docs build, and a
file that still works in ten years; every one of those is worth having, and
every one of them is bought as well by a warm cache, which is the user's to
manage where a wheel is not. Issue #266 then asked for rivers and roads at
the finer scales, and the bundled-versus-fetched split was the awkward part
of that answer: seven features across three resolutions, some shipped and
some not, is a table no caller should have to learn. One rule collapses it.

`BasemapChart` merged after 0.10.2 and has never been released, so ADR 0010's
deprecation policy does not apply to anything decided here.

## Commitments

- **No outlines ship; every resolution is fetched.** `package-data` keeps only
  the fonts. Every resolution, 1:110m included, is downloaded from the pinned
  Natural Earth v5.1.2 release on first use, converted to compressed float32
  arrays of longitude and latitude with `NaN` separating one outline from the
  next — a format numpy reads with no new dependency — and kept in the cache.
  There is one code path where there were two, and `BASEMAP_RESOLUTION.LOW`
  stops being a special case in everything but its size. The conversion script
  is committed and points at the cache, so the format is reproducible from
  source rather than a binary of unknown origin. `geometry=` still accepts the
  caller's own outlines, for a scale Natural Earth does not have or a map that
  is not of the Earth.
- **The cache is load-bearing, so it is documented and seedable.**
  `DATACHART_CACHE_DIR`, else `$XDG_CACHE_HOME/datachart`, else
  `~/.cache/datachart`. A first render needs the network once. A script
  pre-warms the cache for a given resolution, which is the answer for an
  air-gapped install, a locked-down CI, and this repository's own builds; a
  failed download raises one error naming the URL and leaves nothing
  half-written.
- **This repository pre-warms rather than fetches ad hoc.** The docs build
  executes notebooks (`execute: true`) and six golden cases render maps, so
  both would otherwise hit a third-party host on every run. CI pre-warms the
  cache in one step and caches the directory by key, so the host is touched
  once per cache generation instead of once per build, and a contributor's
  second test run is offline.
- **The download timeout is 300 seconds, for every fetch.** 1:10m roads is a
  50 MB GeoJSON — nearly twice the 28 MB of the entire 1:10m outline source —
  and 60 seconds does not finish it on a domestic link, so the first caller to
  ask for roads would have got the download error instead of roads. A timeout
  is a ceiling, not a cost; one constant covers the 7.3 MB rivers fetch too,
  and a per-feature timeout would be a knob for a single layer.
- **No projection, in this front or anywhere.** Longitude goes on x and
  latitude on y, drawn straight. Every chart in the package draws in data
  coordinates, so a projected basemap under unprojected marks would be a
  misalignment bug; projecting the marks too would mean a transform on every
  layer, annotation and reference line. Plate carrée is the one case where
  the basemap and the data already agree, and it is the case that needs no
  code.
- **`aspect_ratio="geographic"` is the cartographic answer, and it belongs to
  every chart.** Drawing degrees straight stretches a region horizontally
  away from the equator; narrowing one degree of longitude by the cosine of
  the mid latitude fixes the proportions without being a projection. It is
  opt-in, so nothing changes for a caller whose axes are not geographic. The
  seismology page hand-rolls this exact factor today, which is the evidence
  that it belongs in the library. It is a value of the `aspect_ratio` setting
  the fronts already take, not a second `aspect` parameter beside it, and
  `Panel` takes the setting too so a composed map can ask for it.
- **Only charts of numbers share a panel with it.** A chart with categories
  or dates on x, its own axes (parallel coordinates) or a horizontal
  orientation has no longitude to put the map on, and composing one used to
  draw a meaningless slice of land. `Panel` raises one `ValueError` instead.
  A numeric chart that is not geographic (a histogram) cannot be told apart
  from a map and still composes.
- **Beside data, the basemap has no say over the limits.** A world of
  outlines under a regional hexbin would otherwise zoom the hexbin out to the
  globe. Alone, it frames its own outlines exactly.
- **`IMAGE_POSITION` becomes `DRAW_POSITION`.** ADR 0052 gives a chart prefix
  only to a constant one chart owns, and the basemap takes the same rung
  setting. The rename carries no alias: `ImageChart` merged after 0.10.2 and
  has never been released either.
- **`BASEMAP_FEATURE` picks what is drawn** — `COASTLINE`, `LAND`,
  `COUNTRIES`, `BORDERS`, `LAKES`, `RIVERS`, `ROADS` — defaulting to coastline
  and land. `OCEAN` is the background an axes already has. Rivers and roads
  are drawn as lines from Natural Earth's `rivers_lake_centerlines` and
  `roads`, and neither joins `BASEMAP_FEATURE.DEFAULT`.
- **A feature is offered wherever Natural Earth has it, and nowhere else.**
  Rivers are offered at all three scales; roads at 1:10m alone, because
  Natural Earth publishes no `roads` layer below it. Asking for a feature at
  a scale without it raises one `ValueError` naming the scales that do carry
  it. Availability is the only gate: the error never means "we think this
  would look bad". A river at 1:110m is a few strokes across a continent and
  will not suit most figures, but that is the caller's call to make on their
  own map, and the cost of letting them make it is a docstring sentence
  rather than a refusal. Gating a feature the data supports, on taste, is the
  kind of restriction a library earns nothing by keeping: it cannot be worked
  around except by leaving the front, and it leaves the caller arguing with
  their tools. The legibility caveat is documented where it helps and
  enforced nowhere.
- **The basemap is furniture, not data.** `plot_basemap_*` styles resolve to
  muted greys — `plot_basemap_river_*` and `plot_basemap_road_*` with them —
  and the front takes no cycle color, legend entry or emphasis, for the
  reason `ImageChart` does not: it carries no series.
- **Countries are picked out by code, not by emphasis.** `COUNTRIES` draws
  one area per country from Natural Earth's admin-0 polygons, keyed by
  `ADM0_A3` (its `ISO_A3` is `-99` for France and Norway). `highlight=` takes
  those codes and fills the listed countries with
  `plot_basemap_highlight_color`; the rest keep the land's grey. It is a
  selection on the map, not the series emphasis the other fronts take, so
  the map stays out of the palette and the legend. A code that the chosen
  scale does not draw (Malta at 1:110m) warns rather than raises, so one list
  of codes works at every resolution. Each country is its own patch, so an
  enclave such as Lesotho is not cancelled by its host's hole.
- **The fonts stay, and name the principle's next application.** The five OFL
  faces are 684 KB against the outlines' 164 KB, so the wheel is not empty
  until they go too. They are held back only because registration currently
  happens at `import datachart` — `themes/__init__.py` imports `sketch` and
  `quill`, both of which register at module level — and moving it late enough
  to fetch is a themes refactor that shares nothing with this loader.
  `register_bundled_fonts` already skips a face it cannot find and leaves the
  stack to its fallbacks, so the tolerance a fetched face needs is built. The
  work is issue #267.

## Considered options

- **Bundle the 1:110m outlines as package data** and download only the finer
  scales on request, which is what this front shipped with before its first
  release. Rejected: a wheel carries code, and the saving was never the
  argument — 164 KB is trivial either way. What the bundle actually bought,
  offline rendering and a hermetic docs build, a pre-warmed cache buys too,
  and the split left seven features across three resolutions with no single
  rule about which of them ship.
- **Bundle 1:50m or 1:10m as well.** Rejected with the bundle itself: 5 and
  28 MB of source for a sharpness most figures at this package's scale do not
  use.
- **Ship a bundled file as a pre-seeded cache entry**, so the loader has one
  path but the data still ships. Rejected: it buys the code simplification and
  none of the principle, and leaves the wheel carrying a dataset under a
  different name.
- **An optional `datachart[geo]` extra on cartopy.** Rejected: the `GeoAxes`
  model conflicts with `Panel`, and the system libraries are a real install
  burden for outlines.
- **Refuse rivers at 1:110m** on legibility grounds. Rejected: see above — a
  gate the data does not require is one the caller cannot route around, and a
  coarse river is a worse figure, not a broken one.
- **Defer roads to its own issue** on the strength of the 50 MB and Natural
  Earth's thin coverage outside North America and Europe. Rejected: the
  coverage caveat belongs in the docstring, and splitting a two-layer change
  across two reviews costs more than it saves.
- **A per-feature download timeout.** Rejected: one constant is enough, and
  the shape of the knob would outlive the one layer that motivated it.
- **A projection parameter accepting Mercator and the conics.** Rejected: it
  is meaningless until every layer transforms, which is a far larger change
  than this issue asked for.
