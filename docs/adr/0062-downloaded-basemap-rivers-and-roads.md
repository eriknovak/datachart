---
status: accepted
---

# The wheel ships code, not data: every basemap resolution downloads

ADR 0061 committed the Natural Earth 1:110m outlines to the wheel as package
data, and listed fetching every resolution on first use among the options it
rejected. That commitment is reversed here, and the rejected option taken,
for a reason 0061 never weighed: what belongs in a distribution. The package
is a drawing library, and a drawing library's wheel should carry the code
that draws and nothing else. 0061 argued the bundle's merits — offline
rendering, a hermetic docs build, a file that works in ten years — and every
one of those still holds. They are now paid for by a warm cache rather than
by package data, which is where they belong: a cache is the user's to
manage, a wheel is not.

`BasemapChart` merged after 0.10.2 and has never been released, so ADR 0010's
deprecation policy does not apply and the reversal costs no alias.

Issue #266 asked for rivers and roads at the finer scales. Answering it meant
touching the same loader, and the bundled-versus-fetched split was the
awkward part of that answer: seven features across three resolutions, some
shipped and some not, is a table no caller should have to learn. Removing the
bundle collapses it to one rule.

## Commitments

- **No outlines ship.** `charts/_basemap/*.npz` leaves the wheel and
  `package-data` keeps only the fonts. Every resolution, 1:110m included, is
  downloaded from the pinned Natural Earth v5.1.2 release on first use,
  converted to the same `NaN`-separated float32 lon/lat arrays, and kept in
  the cache. There is one code path where there were two, and
  `BASEMAP_RESOLUTION.LOW` stops being a special case in everything but its
  size. The conversion script stays, repointed at the cache, so the format is
  still reproducible from source.
- **The cache becomes load-bearing, so it is documented and seedable.**
  `DATACHART_CACHE_DIR`, else `$XDG_CACHE_HOME/datachart`, else
  `~/.cache/datachart`, unchanged from 0061 — but it now carries the default
  map rather than an opt-in extra. A first render needs the network once. A
  script pre-warms the cache for a given resolution, which is the answer for
  an air-gapped install, a locked-down CI, and this repository's own builds;
  a failed download still raises one error naming the URL and leaves nothing
  half-written.
- **This repository pre-warms rather than fetches ad hoc.** The docs build
  executes notebooks (`execute: true`) and six golden cases render maps, so
  both would otherwise hit a third-party host on every run — the cost 0061
  correctly refused to pay. CI pre-warms the cache in one step and caches the
  directory by key, so the host is touched once per cache generation instead
  of once per build, and a contributor's second test run is offline.
- **The download timeout is 300 seconds, for every fetch.** 1:10m roads is a
  50 MB GeoJSON — nearly twice the 28 MB 0061 cited for the entire 1:10m
  source — and 60 seconds does not finish it on a domestic link, so the first
  caller to ask for roads would have got the download error instead of roads.
  A timeout is a ceiling, not a cost; one constant covers the 7.3 MB rivers
  fetch too, and a per-feature timeout would be a knob for a single layer.
- **`RIVERS` and `ROADS` join `BASEMAP_FEATURE`**, drawn as lines from
  Natural Earth's `rivers_lake_centerlines` and `roads`, with
  `plot_basemap_river_*` and `plot_basemap_road_*` styles resolving to the
  same muted furniture greys the rest of the basemap uses. Neither joins
  `BASEMAP_FEATURE.DEFAULT`.
- **A feature is offered per resolution, and asking outside that raises.**
  Rivers are offered at 1:50m and 1:10m, roads at 1:10m alone. Anything else
  raises one `ValueError` naming the resolutions that do carry the feature.
  The two exclusions are not the same kind of fact and the messages say so:
  Natural Earth publishes no `roads` layer below 1:10m, while 1:110m rivers
  exist and are 38 KB — they are refused because at that scale a river is a
  few strokes across a continent, which is 0061's legibility judgement and
  not an availability one. Recording the difference matters, because the day
  someone disagrees about legibility it should be clear that only taste
  stands in the way.
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

- **Keep the bundle exactly as 0061 has it.** Rejected: it is the whole
  question. 164 KB is a trivial saving and was never the argument — the
  argument is that a wheel carries code.
- **Ship the bundled file as a pre-seeded cache entry**, so the loader has one
  path but the data still ships. Rejected: it buys the code simplification
  and none of the principle, and leaves the wheel carrying a dataset under a
  different name.
- **Bundle 1:110m rivers too**, now that the 38 KB is known to be small.
  Rejected on 0061's own legibility grounds, which nothing here disturbs, and
  moot once nothing is bundled.
- **Defer roads to its own issue** on the strength of the 50 MB and Natural
  Earth's thin coverage outside North America and Europe. Rejected: the
  coverage caveat belongs in the docstring, and splitting a two-layer change
  across two reviews costs more than it saves.
- **A per-feature download timeout.** Rejected: one constant is enough, and
  the shape of the knob would outlive the one layer that motivated it.
