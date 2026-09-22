# ImageChart

A picture in data coordinates, under or over the other charts. The [Image Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/imagechart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.ImageChart

```
ImageChart(
    data: ImageDataAttrs | list[ImageDataAttrs],
    *,
    position: IMAGE_POSITION | str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    subtitle: str | list[str | None] | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    xmin: int | float | None = None,
    xmax: int | float | None = None,
    ymin: int | float | None = None,
    ymax: int | float | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    subplots: bool | None = None,
    max_cols: int | None = None,
    sharex: bool | None = None,
    sharey: bool | None = None,
    style: (
        ImageStyleAttrs
        | list[ImageStyleAttrs | None]
        | None
    ) = None
) -> plt.Figure
```

Creates the image chart.

An image chart places a picture in data coordinates: its pixels stretch to fill an `extent`, the `(xmin, xmax, ymin, ymax)` rectangle it covers on the axes. On its own it is a picture with axes; its use is under another chart that shares its coordinates, composed with `Panel` — a scatter of stations over a floor plan, a heatmap over a microscope image, epicentres over a relief grid. The picture is a file path, a PIL image, an RGB(A) array, or a 2-D array read through a colormap.

The picture carries no series: it takes no cycle color, no legend entry and no emphasis. `position` decides where it sits in the draw order, under the gridlines and every mark by default, so the order of the figures in `Panel` never does. Its extent counts toward the axis limits like any other chart's data, and `xmin`, `xmax`, `ymin` and `ymax` narrow them back.

Examples:

```
>>> import numpy as np
>>> from datachart.charts import ImageChart, ScatterChart
>>> from datachart.utils import Panel
>>> relief = np.outer(np.linspace(0, 1, 50), np.linspace(1, 0, 80))
>>> figure = Panel(
...     [
...         ImageChart({"image": relief, "extent": (0, 8, 0, 5)}),
...         ScatterChart([{"x": 2, "y": 1}, {"x": 6, "y": 4}]),
...     ],
...     title="Stations on the relief",
... )
```

| PARAMETER      | DESCRIPTION                                                                                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`         | The picture and where it sits: a {"image", "extent"} dict, or a list of them to overlay several pictures or draw one per subplot. See ImageDataAttrs. **TYPE:** \`ImageDataAttrs                        |
| `position`     | Where the picture sits in the draw order: "below" (default) under the gridlines and every mark, or "above" over the marks and under the reference lines. See IMAGE_POSITION. **TYPE:** \`IMAGE_POSITION |
| `title`        | The title of the chart. **TYPE:** \`str                                                                                                                                                                 |
| `xlabel`       | The label of the x-axis. **TYPE:** \`str                                                                                                                                                                |
| `ylabel`       | The label of the y-axis. **TYPE:** \`str                                                                                                                                                                |
| `subtitle`     | The subtitle of each chart. **TYPE:** \`str                                                                                                                                                             |
| `figsize`      | The size of the figure as (width, height) in inches. See FIG_SIZE. **TYPE:** \`FIG_SIZE                                                                                                                 |
| `xmin`         | The minimum value of the x-axis. **TYPE:** \`int                                                                                                                                                        |
| `xmax`         | The maximum value of the x-axis. **TYPE:** \`int                                                                                                                                                        |
| `ymin`         | The minimum value of the y-axis. **TYPE:** \`int                                                                                                                                                        |
| `ymax`         | The maximum value of the y-axis. **TYPE:** \`int                                                                                                                                                        |
| `vmin`         | The value at the low end of the colormap; a 2-D array only. **TYPE:** \`float                                                                                                                           |
| `vmax`         | The value at the high end of the colormap; a 2-D array only. **TYPE:** \`float                                                                                                                          |
| `show_grid`    | Which grid lines to show ("both", "x", "y"); False draws none. The grid draws over a picture placed below. See SHOW_GRID. **TYPE:** \`SHOW_GRID                                                         |
| `aspect_ratio` | The aspect ratio of the axes box. See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                            |
| `subplots`     | Whether to draw each picture in its own subplot. **TYPE:** \`bool                                                                                                                                       |
| `max_cols`     | The maximum number of subplot columns. **TYPE:** \`int                                                                                                                                                  |
| `sharex`       | Whether the subplots share the x-axis. **TYPE:** \`bool                                                                                                                                                 |
| `sharey`       | Whether the subplots share the y-axis. **TYPE:** \`bool                                                                                                                                                 |
| `style`        | Style configuration(s) for each chart. See ImageStyleAttrs. **TYPE:** \`ImageStyleAttrs                                                                                                                 |

| RETURNS      | DESCRIPTION                            |
| ------------ | -------------------------------------- |
| `plt.Figure` | The figure containing the image chart. |

| RAISES       | DESCRIPTION                                                                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If the image is not a readable picture or array, the extent is missing, not four finite numbers, or has no width or height, or position is not an IMAGE_POSITION. |

## Data

Each record in `data` is a [`ImageDataAttrs`](#datachart.typings.ImageDataAttrs).

### datachart.typings.ImageDataAttrs

Bases: `TypedDict`

The data attributes for the image chart.

| ATTRIBUTE | DESCRIPTION                                                                                                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `image`   | The picture: a path to an image file, a PIL image, an RGB(A) array of shape (rows, columns, 3 or 4), or a 2-D array read through the plot_image_cmap colormap. The first row is the top edge. **TYPE:** \`str                        |
| `extent`  | The data-space rectangle the pixels stretch to fill, as (xmin, xmax, ymin, ymax): four finite numbers, xmin different from xmax and ymin from ymax. A reversed pair flips the picture. **TYPE:** `tuple[float, float, float, float]` |

## Style

`style` takes the keys of [`ImageStyleAttrs`](#datachart.typings.ImageStyleAttrs). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.ImageStyleAttrs

Bases: `TypedDict`

The typing for the image chart style.

| ATTRIBUTE                  | DESCRIPTION                                                                                                                                                                             |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_image_alpha`         | The alpha value of the picture; below 1 lets the axes ground show through. **TYPE:** \`float                                                                                            |
| `plot_image_cmap`          | The colormap a 2-D array is read through (palette name, single color, list of hex colors, or colormap); an RGB(A) picture ignores it. **TYPE:** \`str                                   |
| `plot_image_interpolation` | How the pixels are resampled to the axes, as matplotlib's imshow names it ("antialiased", "nearest", "bilinear", ...). **TYPE:** \`str                                                  |
| `plot_image_aspect`        | The aspect of the pixels: "auto" stretches the picture to fill its extent and leaves the axes shape to the data; "equal" keeps the pixels square and reshapes the axes. **TYPE:** \`str |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter      | Constant                                                                                                               |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `position`     | [`IMAGE_POSITION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.IMAGE_POSITION) |
| `figsize`      | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)             |
| `show_grid`    | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)           |
| `aspect_ratio` | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)     |
