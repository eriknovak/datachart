---
status: accepted
amended-by: [0062]
---

# An image is a chart front anchored by an extent, not a setting on other charts

Issue #263 asked for two things: a basemap under a geographic chart, and a
raster image under any chart whose marks share its coordinates — a heatmap
over a microscope image, a scatter over a floor plan, epicentres over relief.
Neither existed, so the reader got marks on a blank axes.

The obvious shape was a reference-mark family, `underlay=` beside `vspans=`
and `texts=`, resolved at build and drawn by the panel. That reaches only the
nine fronts routed through `REF_KEYS`, and it puts a picture in the same
bucket as a threshold line. An image is not a mark against the data; it is its
own drawable thing, and the package already has a seam for stacking drawable
things — `Panel` (ADR 0001). `ImageChart` is therefore a front like any other,
and `Panel(ImageChart(relief), HexbinChart(quakes))` is the whole story. Every
chart gains an image behind it, not just the geographic five.

## Commitments

- **`ImageChart` is a chart front**, in `datachart/charts/`, producing a figure
  with one `ImageLayer`. It has to produce a real figure with a panel for
  `Panel` to compose it, which is what a front does.
- **The name states the thing, not the position.** Every other front is named
  for what it draws; none is named for its z-order. `UnderlayImage` was
  rejected because the position is a parameter, so the name would lie the
  first time someone raised a watermark over the data. That gives up the
  `Underlay*` family a later basemap could have joined, which is the accepted
  cost of a name that stays true.
- **Not bare `Image`.** The docs teach `from datachart.charts import X` and
  never `import datachart as dc`, so `Image` would collide with `PIL.Image` —
  the import a user loading a picture has already made. `Raster` was rejected
  too: the `Surface` glossary entry already spends that word.
- **`position` is an `IMAGE_POSITION` constant, defaulting `BELOW`.** The
  draw-order ladder (ADR 0054) has rungs between the extremes, so a faint
  watermark above the grid but under the marks is a real third value a
  boolean could not grow into. `BELOW` sits at 0.25, under the gridlines at
  0.5, so the grid reads over the picture the way it reads over a band.
- **The extent participates in the data limits.** An image wider than the data
  widens the axes, like every other layer's span, and `xmin`/`xmax` narrow it
  back. A layer that quietly refused to grow the limits would read as a bug
  the first time an image went missing off-axes.
- **A 2-D array is accepted and read through a colormap**, although `Heatmap`
  and filled `ContourChart` also draw gridded fields. It is one branch in the
  same `imshow` call, and a raster elevation model under a chart is the
  motivating case from the issue. The difference that matters: `Heatmap`
  anchors cells to ticks, `ImageChart` anchors pixels to an extent.
- **The image never stretches the axes to suit itself.**
  `plot_image_aspect` defaults to `"auto"`, so the picture fills its extent
  and the axes keep the shape the data asked for.
- **Basemaps stay out.** Coastlines and borders as vector data need a new
  dependency and a projection story. A pre-rendered map image covers the case
  today through this front; issue #263 keeps the vector half.

## Considered options

- **A reference-mark family (`underlay=`).** Rejected: it reaches nine fronts
  instead of all of them, and a picture is not a mark against the data.
- **A `Panel`-level argument.** Rejected: a single chart would need
  composition to get an image, and `Panel` would gain a drawing path of its
  own, which ADR 0001 exists to prevent.
- **A `behind: bool` in place of the constant.** Rejected: the ladder has
  intermediate rungs and a boolean cannot name them.
