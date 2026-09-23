# Image Chart

An image chart places a picture in the coordinates of the data: its pixels stretch over an `extent`, the rectangle `(xmin, xmax, ymin, ymax)` it covers on the axes. On its own it is a picture with axes; its use is underneath another chart that shares those coordinates, so the marks have something to sit on: epicentres on the relief of a region, sensors on a floor plan, detections on a microscope image. This guide shows how to create image charts with the [datachart.charts.ImageChart](https://eriknovak.github.io/datachart/dev/references/charts/imagechart/#datachart.charts.ImageChart) function and how to compose them with other charts, starting with the basics and building up to worked examples on real data.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-image-chart), which maps common tasks to the parameter or style attribute that does the job.

```
import numpy as np

from datachart.charts import ImageChart, ScatterChart
from datachart.utils import Panel
```

## Basics

The examples in this guide share one dataset: the relief of the Aegean and Anatolia, between 34 and 42 degrees north and 19 and 45 degrees east, sampled every quarter degree from [NOAA's ETOPO](https://www.ncei.noaa.gov/products/etopo-global-relief-model) global model (public domain), and the 54 earthquakes of magnitude 5 and above that struck the region in 2023, from the [USGS earthquake catalogue](https://earthquake.usgs.gov/fdsnws/event/1/) (public domain). The hidden cell below holds both. `RELIEF` has `lat` and `lon` axes and a `z` row per latitude, in metres above sea level; `QUAKES` is one tuple per earthquake: the hours since the start of 2023, the latitude, the longitude, the depth in kilometres, and the magnitude.

The relief is a grid of 33 latitudes by 105 longitudes, the first row at the southern edge:

```
elevation = np.array(RELIEF["z"])
elevation.shape, RELIEF["lat"][:3], RELIEF["lon"][:3]
```

**Basic example.** An image chart takes a `{"image", "extent"}` dictionary. The image here is the 2-D elevation array, which is read through a colormap; the extent is the rectangle it covers, in degrees. Two details put the pixels in the right place. An image's first row is its top edge, while the grid's first row is its southern edge, so the rows are flipped with `[::-1]`. And each value is the centre of a quarter-degree cell, so the extent reaches half a step past the first and the last sample.

```
STEP = 0.25
# the pixels are cells centred on the samples, so the extent reaches half a step out
EXTENT = (
    RELIEF["lon"][0] - STEP / 2,
    RELIEF["lon"][-1] + STEP / 2,
    RELIEF["lat"][0] - STEP / 2,
    RELIEF["lat"][-1] + STEP / 2,
)

ImageChart(
    # the first row of an image is its top edge: north goes first
    data={"image": elevation[::-1], "extent": EXTENT},
).show()
```

## Customizing the Image Chart

Every customization is either a keyword argument of `ImageChart` or a `plot_image_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                 | Use                                              | See                                                                                               |
| ------------------------------------------ | ------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| add a title and axis labels                | `title`, `xlabel`, `ylabel`                      | [Title, axis labels and limits](#title-axis-labels-and-limits)                                    |
| show part of the picture                   | `xmin`, `xmax`, `ymin`, `ymax`                   | [Title, axis labels and limits](#title-axis-labels-and-limits)                                    |
| change the figure size or add a grid       | `figsize`, `show_grid`                           | [Figure size and grid](#figure-size-and-grid)                                                     |
| color a 2-D array                          | `style={"plot_image_cmap": ...}`, `vmin`, `vmax` | [Colormap and value range](#colormap-and-value-range)                                             |
| draw a photo, a file or an RGB array       | `data={"image": path \| PIL image \| array}`     | [Pictures](#pictures)                                                                             |
| smooth or keep the pixels                  | `style={"plot_image_interpolation": ...}`        | [Interpolation](#interpolation)                                                                   |
| fade the picture                           | `style={"plot_image_alpha": ...}`                | [Transparency](#transparency)                                                                     |
| keep the pixels square                     | `style={"plot_image_aspect": "equal"}`           | [Aspect](#aspect)                                                                                 |
| put the picture under or over other charts | `position`, `Panel`                              | [Composing with Panel](#composing-with-panel)                                                     |
| draw several pictures                      | a list of `data`, `subplots`                     | [Multiple Image Charts](#multiple-image-charts)                                                   |
| save the chart as an image                 | `save_figure`                                    | [Saving figures](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/saving/index.md) |

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values:

| Parameter      | Constant                                                                                                             |
| -------------- | -------------------------------------------------------------------------------------------------------------------- |
| `position`     | [`DRAW_POSITION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DRAW_POSITION) |
| `figsize`      | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)           |
| `show_grid`    | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)         |
| `aspect_ratio` | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)   |

The keys of the data dictionary are listed in [ImageDataAttrs](https://eriknovak.github.io/datachart/dev/references/charts/imagechart/#datachart.typings.ImageDataAttrs), the style attributes in [ImageStyleAttrs](https://eriknovak.github.io/datachart/dev/references/charts/imagechart/#datachart.typings.ImageStyleAttrs).

### Title, axis labels and limits

A picture in data coordinates carries units, and the axis labels say which: here, degrees of longitude and latitude. `title`, `xlabel` and `ylabel` add them. The extent sets the axis range, and `xmin`, `xmax`, `ymin` and `ymax` narrow it to part of the picture, which is how a report zooms into the region that matters without cropping the array. The chart below zooms into south-eastern Türkiye, where the year's two largest earthquakes struck.

```
ImageChart(
    data={"image": elevation[::-1], "extent": EXTENT},
    title="South-eastern Türkiye",
    xlabel="Longitude (°E)",
    ylabel="Latitude (°N)",
    # show only the corner of the relief around the mainshocks
    xmin=34,
    xmax=41,
    ymin=35,
    ymax=40,
).show()
```

### Figure size and grid

The region is three times as wide as it is tall, so the default, nearly square figure squeezes it. `figsize` takes a `(width, height)` tuple in inches or a preset from [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE). `show_grid` takes a [SHOW_GRID](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID) member; the grid draws over the picture, so it reads as a graticule of the map.

```
from datachart.constants import SHOW_GRID

ImageChart(
    data={"image": elevation[::-1], "extent": EXTENT},
    xlabel="Longitude (°E)",
    ylabel="Latitude (°N)",
    # a wide figure for a wide region, and a graticule over the relief
    figsize=(9.0, 3.6),
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Colormap and value range

A 2-D array has no colors of its own: each value is looked up in a colormap, grey by default so the picture stays behind the data. `plot_image_cmap` takes a [COLORS](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.COLORS) member, a matplotlib colormap name, or a list of colors (the [Colormaps](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/colormaps/index.md) guide shows them all). Elevation is signed, so a diverging colormap fits, and `vmin` and `vmax` set symmetrically about zero put sea level on its pale midpoint: the coastline appears without a coastline dataset. Without them the range comes from the data, and the midpoint lands wherever the data's middle happens to be.

```
ImageChart(
    data={"image": elevation[::-1], "extent": EXTENT},
    xlabel="Longitude (°E)",
    ylabel="Latitude (°N)",
    # a diverging colormap, with sea level on its midpoint
    style={"plot_image_cmap": "BrBG_r"},
    vmin=-4500,
    vmax=4500,
    figsize=(9.0, 3.6),
).show()
```

### Pictures

The picture does not have to be an array of values. `image` also takes an RGB or RGBA array of shape `(rows, columns, 3 or 4)`, which keeps its own colors, a PIL image, or the path of an image file, so a scanned map, a photograph or a floor plan goes in as it is. The cell below shades the relief into an RGB picture with matplotlib's `LightSource`, as a map renderer would, saves it as a PNG, and passes the path.

```
import os
import tempfile

import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

# a hill-shaded relief, rendered to an RGB picture
shaded = LightSource(azdeg=315, altdeg=45).shade(
    elevation[::-1], cmap=plt.get_cmap("gist_earth"), vert_exag=0.02, blend_mode="soft"
)
path = os.path.join(tempfile.mkdtemp(), "relief.png")
plt.imsave(path, shaded)

ImageChart(
    # the path of the saved picture
    data={"image": path, "extent": EXTENT},
    xlabel="Longitude (°E)",
    ylabel="Latitude (°N)",
    figsize=(9.0, 3.6),
).show()
```

### Interpolation

A quarter-degree grid is coarse: stretched over the axes, each value is a visible block. `plot_image_interpolation` decides how the pixels are resampled, using the names of matplotlib's `imshow`: `"nearest"` keeps every block sharp, which is honest about the resolution, while `"bilinear"` blends neighbouring values into a smooth surface, which reads better as a background. The default, `"antialiased"`, avoids moiré when a large picture is shrunk.

```
for interpolation in ["nearest", "bilinear"]:
    ImageChart(
        data={"image": elevation[::-1], "extent": EXTENT},
        title=f'plot_image_interpolation="{interpolation}"',
        # zoom in, so the pixels are large enough to see
        xmin=34,
        xmax=41,
        ymin=35,
        ymax=40,
        style={"plot_image_interpolation": interpolation},
        figsize=(6.0, 3.6),
    ).show()
```

### Transparency

A picture at full strength competes with the data drawn over it. `plot_image_alpha` fades it toward the axes background: below 1 the picture recedes and the marks win. The default is 1, because a faded picture is a choice about one figure, not a rule for every theme.

```
ImageChart(
    data={"image": elevation[::-1], "extent": EXTENT},
    xlabel="Longitude (°E)",
    ylabel="Latitude (°N)",
    # a faded relief, to sit behind the data
    style={"plot_image_alpha": 0.45},
    figsize=(9.0, 3.6),
).show()
```

### Aspect

By default the picture stretches to fill its extent, and the axes keep the shape the figure gives them; that is what lets an image sit under any chart without reshaping it. `plot_image_aspect="equal"` keeps each pixel square instead, so one unit on x is as long as one unit on y, and the axes shrink to fit. For a floor plan in metres or a microscope image in micrometres that is the correct shape; for degrees of longitude and latitude it is only approximately right.

```
ImageChart(
    data={"image": elevation[::-1], "extent": EXTENT},
    xlabel="Longitude (°E)",
    ylabel="Latitude (°N)",
    # square pixels: a degree is as long on both axes
    style={"plot_image_aspect": "equal"},
    figsize=(9.0, 3.6),
).show()
```

## Composing with Panel

An image chart is made to sit under another chart. [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) overlays figures in one coordinate space, and the image and the data meet there because they share the same units. The picture carries no series: it takes no color from the palette, adds no legend entry, and ignores emphasis, so the chart over it looks as it would alone. The extent counts toward the axis range like any other chart's data, so the axes cover both the picture and the marks.

`position` decides where the picture sits in the drawing order, with a [DRAW_POSITION](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DRAW_POSITION) member. The default, `DRAW_POSITION.BELOW`, puts it under the grid and every mark, whatever the order of the figures in `Panel`: below, the scatter chart comes first and still draws on top.

```
from datachart.constants import DRAW_POSITION

relief = ImageChart(
    data={"image": elevation[::-1], "extent": EXTENT},
    style={"plot_image_alpha": 0.6, "plot_image_interpolation": "bilinear"},
)
quakes = ScatterChart(
    [{"x": lon, "y": lat} for _, lat, lon, _, _ in QUAKES],
)

Panel(
    # the order does not matter: the image sits below by its position
    [quakes, relief],
    title="Earthquakes of magnitude 5 and above, 2023",
    xlabel="Longitude (°E)",
    ylabel_left="Latitude (°N)",
    figsize=(9.0, 3.6),
).show()
```

`DRAW_POSITION.ABOVE` draws the picture over the marks instead, and still under reference lines and text notes. Its use is a picture that is meant to cover: a watermark, or a mask. The mask below is an RGBA array, transparent over the study area around the 2023 mainshocks and a translucent grey everywhere else, so the rest of the region recedes without disappearing.

```
# transparent inside the study area, a translucent grey outside it
mask = np.zeros((*elevation.shape, 4))
mask[..., :3] = 0.95
mask[..., 3] = 0.6
lat = np.array(RELIEF["lat"])[::-1]
lon = np.array(RELIEF["lon"])
inside = ((lat >= 35.5) & (lat <= 39.5))[:, None] & ((lon >= 35) & (lon <= 40))[None, :]
mask[inside, 3] = 0

Panel(
    [
        relief,
        quakes,
        ImageChart({"image": mask, "extent": EXTENT}, position=DRAW_POSITION.ABOVE),
    ],
    title="The study area around the 2023 mainshocks",
    xlabel="Longitude (°E)",
    ylabel_left="Latitude (°N)",
    figsize=(9.0, 3.6),
).show()
```

## Multiple Image Charts

A list of dictionaries in `data` draws several pictures: overlaid on one axes by default, each placed by its own extent, or one per subplot with `subplots=True`. `subtitle` names each one, `max_cols` limits the subplots per row, and `sharex` and `sharey` put them on one axis range. `vmin` and `vmax` apply to every 2-D array, which keeps their colors comparable. Below, the land and the sea floor are split into two arrays and drawn side by side, each with the colormap that suits it.

```
land = np.where(elevation >= 0, elevation, np.nan)
sea = np.where(elevation < 0, elevation, np.nan)

ImageChart(
    data=[
        {"image": land[::-1], "extent": EXTENT},
        {"image": sea[::-1], "extent": EXTENT},
    ],
    subtitle=["Land", "Sea floor"],
    style=[{"plot_image_cmap": "YlOrBr"}, {"plot_image_cmap": "Blues_r"}],
    subplots=True,
    max_cols=1,
    sharex=True,
    figsize=(9.0, 6.0),
).show()
```

The empty cells of each array are `NaN`, which a colormap leaves transparent: the axes background shows through where the other half of the region is.

## Real-World Examples

### Where did the strongest earthquakes of 2023 strike? (relief under a bubble scatter, notes)

The first question of an earthquake report is where, and a map answers it better than bare coordinates. A faded, smoothed relief goes under a scatter chart whose bubble size is the magnitude, so the reader sees at once that the largest events sit on the mountain front of south-eastern Türkiye, and that the smaller ones trace the Hellenic arc south of Crete. A note names the Kahramanmaraş sequence.

```
main = max(QUAKES, key=lambda quake: quake[4])

bubbles = ScatterChart(
    # the bubble area grows with the energy of the earthquake
    [
        {"x": lon, "y": lat, "size": 4 ** (magnitude - 4.3)}
        for _, lat, lon, _, magnitude in QUAKES
    ],
    style={"plot_scatter_color": "#b2182b", "plot_scatter_alpha": 0.7},
    texts={
        "text": f"Kahramanmaraş, M{main[4]:.1f}",
        # the note sits in the axes corner, so it stays put when the view narrows
        "x": 0.78,
        "y": 0.88,
        "coords": "axes",
        "target": (main[2], main[1]),
    },
)

Panel(
    [relief, bubbles],
    title="The strongest earthquakes of 2023 sit on the mountain front",
    xlabel="Longitude (°E)",
    ylabel_left="Latitude (°N)",
    figsize=(9.0, 3.8),
).show()
```

### Which desks run warm? (a floor plan under sensor readings, equal aspect)

A building report places its readings on the floor plan, because a temperature means little until the reader knows which room it came from. The floor plan here is illustrative, drawn as an RGB array in the hidden cell below, and so are the twelve sensor readings. The plan is 20 by 12 metres, so the extent is in metres and `plot_image_aspect="equal"` keeps the rooms their true shape; the scatter chart colors each sensor by its temperature band.

```
def band(temperature):
    if temperature < 23:
        return "21 to 23 °C"
    return "23 to 25 °C" if temperature < 25 else "25 to 28 °C"


Panel(
    [
        ImageChart(
            {"image": PLAN, "extent": (0, 20, 0, 12)},
            # metres on both axes: keep the rooms their true shape
            style={"plot_image_aspect": "equal"},
        ),
        ScatterChart(
            [{"x": x, "y": y, "hue": band(t)} for x, y, t in SENSORS],
            style={"plot_scatter_size": 90},
        ),
    ],
    title="The east wing runs three degrees warmer",
    xlabel="Metres",
    ylabel_left="Metres",
    show_legend=True,
    legend={"title": "Temperature"},
    figsize=(8.0, 5.0),
).show()
```

### How does the aftershock zone compare with the region? (limits, Grid)

A report often pairs the overview with a close-up. The same composed panel, drawn twice with different limits, gives both; [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md) arranges them side by side. The limits narrow the axes to the zone around the mainshocks, and the relief and the bubbles follow, because both are drawn in the same coordinates.

```
from datachart.utils import Grid

overview = Panel([relief, bubbles], title="The region", figsize=(9.0, 3.8))
closeup = Panel(
    [relief, bubbles],
    title="The aftershock zone",
    # narrow the axes to the mainshocks; the picture follows
    xmin=35,
    xmax=40,
    ymin=35.5,
    ymax=39.5,
)

Grid(
    [[overview, closeup]],
    title="The 2023 earthquakes, regional and close-up",
    figsize=(12.0, 4.2),
).show()
```
