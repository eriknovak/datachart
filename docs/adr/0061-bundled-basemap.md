---
status: accepted
---

# The basemap ships with the package and projects nothing

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
matplotlib, scipy and pypalettes. Downloading on first use breaks offline
rendering and contradicts the rule the use-case pages already follow, which
is to embed data rather than fetch it at build.

So the outlines ship in the wheel. `datachart/themes/_fonts` already ships
692 KB of TTFs as package data with its license beside it, and Natural Earth
is public domain with no restrictions, so this is the same move with a
smaller file.

## Commitments

- **Natural Earth 1:110m ships as package data**, converted to compressed
  float32 arrays of longitude and latitude with `NaN` separating one outline
  from the next — a format numpy reads with no new dependency. The script
  that converts the source shapefiles is committed beside the data, so the
  bundle is reproducible rather than a binary of unknown origin. The source
  license ships alongside it, as `OFL.txt` does for the fonts.
- **One bundled resolution; the finer ones on request.** 1:110m suits
  continental and regional figures and is wrong for a city. It is the
  default and the only set that ships. `resolution=` (a `BASEMAP_RESOLUTION`)
  asks for 1:50m or 1:10m, which are downloaded from the same pinned Natural
  Earth release the first time they are used, converted to the bundled
  format, and kept in a user cache (`DATACHART_CACHE_DIR`, else
  `$XDG_CACHE_HOME/datachart`, else `~/.cache/datachart`). A failed download
  raises one error naming the URL; nothing half-written stays in the cache.
  The download is opt-in, so the default map keeps working offline, and the
  docs never execute one, so the build never depends on the host.
  `geometry=` still accepts the caller's own outlines, for a scale Natural
  Earth does not have or a map that is not of the Earth.
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
- **Beside data, the basemap has no say over the limits.** A world of
  outlines under a regional hexbin would otherwise zoom the hexbin out to the
  globe. Alone, it frames its own outlines exactly.
- **`IMAGE_POSITION` becomes `DRAW_POSITION`.** ADR 0052 gives a chart prefix
  only to a constant one chart owns, and the basemap takes the same rung
  setting. The rename is free and carries no alias: `ImageChart` merged after
  0.10.2 and has never been released, so ADR 0010's deprecation policy does
  not apply.
- **`BASEMAP_FEATURE` picks what is drawn** — `COASTLINE`, `LAND`, `BORDERS`,
  `LAKES` — defaulting to coastline and land. `OCEAN` is the background an
  axes already has, and rivers at 1:110m are too coarse to read.
- **The basemap is furniture, not data.** `plot_basemap_*` styles resolve to
  muted greys, and the front takes no cycle color, legend entry or emphasis,
  for the reason `ImageChart` does not: it carries no series.

## Considered options

- **An optional `datachart[geo]` extra on cartopy.** Rejected: the `GeoAxes`
  model conflicts with `Panel`, and the system libraries are a real install
  burden for outlines.
- **Fetch and cache every resolution on first use, the default included.**
  Rejected: offline rendering of the default map breaks, and a docs build
  would depend on a third-party host. Fetching stays for the opt-in scales.
- **Bundle 1:50m or 1:10m as well.** Rejected: 5 and 28 MB of source for a
  sharpness most figures at this package's scale do not use; the caller who
  needs it pays the download once.
- **A projection parameter accepting Mercator and the conics.** Rejected: it
  is meaningless until every layer transforms, which is a far larger change
  than this issue asked for.
