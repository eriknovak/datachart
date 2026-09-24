# BasemapChart

Coastlines, land, borders, lakes, rivers and roads under a chart of longitude and latitude. The [Basemap Chart guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/basemapchart/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.BasemapChart

```
BasemapChart(
    data: BASEMAP_FEATURE | str | list[str] | None = None,
    *,
    resolution: BASEMAP_RESOLUTION | str | None = None,
    highlight: str | list[str] | None = None,
    geometry: (
        BasemapDataAttrs | list[BasemapDataAttrs] | None
    ) = None,
    position: DRAW_POSITION | str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    xmin: int | float | None = None,
    xmax: int | float | None = None,
    ymin: int | float | None = None,
    ymax: int | float | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    style: BasemapStyleAttrs | None = None,
    features: (
        BASEMAP_FEATURE | str | list[str] | None
    ) = None
) -> plt.Figure
```

Creates the basemap chart.

A basemap chart draws the land under a geographic chart: coastlines, a land fill, the borders between countries, the large lakes, the rivers and the main roads, from the Natural Earth outlines. Each is downloaded the first time it is drawn and kept in a local cache, so a map needs the network once and no extra dependency. Longitude runs along x and latitude along y, drawn straight; nothing is projected, so the marks composed over the map with `Panel` need no transform either — a hexbin of epicentres, a scatter of stations, a line of a ship's track.

The map carries no series: it takes no cycle color, no legend entry and no emphasis, and its greys come from the theme. With the countries feature, `highlight` picks countries out by their three-letter code: the ones listed take the highlight color, the rest stay the land's grey. `position` decides where it sits in the draw order, under the gridlines and every mark by default. Composed with other charts it leaves the axis limits to their data; alone it frames its own outlines. `Panel` refuses to compose it with a chart that has categories or dates on an axis, or is horizontal, since that chart has no longitude to draw the map at. `aspect_ratio="geographic"` narrows each degree of longitude by the cosine of the middle latitude, so a region keeps its proportions.

The default 1:110m outlines suit a continent or a region; `resolution` asks for the finer Natural Earth scales, for a country or a coast. The roads exist at 1:10m alone, and a 1:110m river is only a few strokes across a continent. `geometry` takes your own longitude and latitude outlines in their place: a country's provinces, a coast at street scale, or a map that is not of the Earth.

Examples:

```
>>> from datachart.charts import BasemapChart, ScatterChart
>>> from datachart.constants import ASPECT_RATIO, BASEMAP_FEATURE
>>> from datachart.utils import Panel
>>> figure = Panel(
...     [
...         BasemapChart([BASEMAP_FEATURE.LAND, BASEMAP_FEATURE.BORDERS]),
...         ScatterChart([{"x": 14.5, "y": 46.1}, {"x": 16.4, "y": 48.2}]),
...     ],
...     title="Two capitals",
...     xmin=5,
...     xmax=25,
...     ymin=40,
...     ymax=52,
...     aspect_ratio=ASPECT_RATIO.GEOGRAPHIC,
... )
```

| PARAMETER      | DESCRIPTION                                                                                                                                                                                                          |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`         | The features to draw: one name or a list of them, coastline and land by default. See BASEMAP_FEATURE. **TYPE:** \`BASEMAP_FEATURE                                                                                    |
| `resolution`   | The Natural Earth scale: "110m" (default), "50m" or "10m", each downloaded once on first use. See BASEMAP_RESOLUTION. **TYPE:** \`BASEMAP_RESOLUTION                                                                 |
| `highlight`    | The countries to pick out, as Natural Earth's three-letter ADM0_A3 codes ("SVN", "FRA"); needs the "countries" feature. A code too small to draw at the chosen resolution warns. **TYPE:** \`str                     |
| `geometry`     | Your own outlines, drawn in place of Natural Earth's: a {"lon", "lat", "feature"} dict, or a list of them. Cannot be combined with data, resolution or highlight. See BasemapDataAttrs. **TYPE:** \`BasemapDataAttrs |
| `position`     | Where the map sits in the draw order: "below" (default) under the gridlines and every mark, or "above" over the marks and under the reference lines. See DRAW_POSITION. **TYPE:** \`DRAW_POSITION                    |
| `title`        | The title of the chart. **TYPE:** \`str                                                                                                                                                                              |
| `xlabel`       | The label of the x-axis. **TYPE:** \`str                                                                                                                                                                             |
| `ylabel`       | The label of the y-axis. **TYPE:** \`str                                                                                                                                                                             |
| `figsize`      | The size of the figure as (width, height) in inches. See FIG_SIZE. **TYPE:** \`FIG_SIZE                                                                                                                              |
| `xmin`         | The minimum value of the x-axis. **TYPE:** \`int                                                                                                                                                                     |
| `xmax`         | The maximum value of the x-axis. **TYPE:** \`int                                                                                                                                                                     |
| `ymin`         | The minimum value of the y-axis. **TYPE:** \`int                                                                                                                                                                     |
| `ymax`         | The maximum value of the y-axis. **TYPE:** \`int                                                                                                                                                                     |
| `show_grid`    | Which grid lines to show ("both", "x", "y"); False draws none. The grid draws over a map placed below. See SHOW_GRID. **TYPE:** \`SHOW_GRID                                                                          |
| `aspect_ratio` | The aspect ratio of the axes box; "geographic" keeps the region at true proportions. See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                      |
| `style`        | Style configuration of the map. See BasemapStyleAttrs. **TYPE:** \`BasemapStyleAttrs                                                                                                                                 |
| `features`     | Deprecated; use data. Removed in the next release. **TYPE:** \`BASEMAP_FEATURE                                                                                                                                       |

| RETURNS      | DESCRIPTION                              |
| ------------ | ---------------------------------------- |
| `plt.Figure` | The figure containing the basemap chart. |

| RAISES         | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError`   | If a feature is not a BASEMAP_FEATURE, resolution is not a BASEMAP_RESOLUTION, geometry is not outlines of matching longitudes and latitudes or comes with data, resolution or highlight, a highlight code is not three letters or comes without the countries feature, a feature is not published at resolution, position is not a DRAW_POSITION, or a geographic aspect meets a y-axis outside -90 to 90. |
| `RuntimeError` | If a feature is not cached and cannot be downloaded.                                                                                                                                                                                                                                                                                                                                                        |

## Data

Each record in `geometry` is a [`BasemapDataAttrs`](#datachart.typings.BasemapDataAttrs).

### datachart.typings.BasemapDataAttrs

Bases: `TypedDict`

The geometry attributes for the basemap chart.

| ATTRIBUTE | DESCRIPTION                                                                                                                                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lon`     | The longitudes of the outlines, drawn on the x-axis. A NaN separates one outline from the next. **TYPE:** `list[float]`                                                                                                                           |
| `lat`     | The latitudes of the outlines, drawn on the y-axis; as long as lon, with its NaN at the same places. **TYPE:** `list[float]`                                                                                                                      |
| `feature` | How the outlines are drawn and styled: "coastline" (default) or "borders" as lines, "land" or "lakes" as filled areas; "countries" needs Natural Earth's country codes and is not accepted here. See BASEMAP_FEATURE. **TYPE:** \`BASEMAP_FEATURE |

## Style

`style` takes the keys of [`BasemapStyleAttrs`](#datachart.typings.BasemapStyleAttrs). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.BasemapStyleAttrs

Bases: `TypedDict`

The typing for the basemap chart style.

| ATTRIBUTE                           | DESCRIPTION                                                                                            |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `plot_basemap_land_color`           | The fill color of the land, and of the countries highlight leaves out. **TYPE:** \`str                 |
| `plot_basemap_highlight_color`      | The fill color of the countries highlight picks out. **TYPE:** \`str                                   |
| `plot_basemap_highlight_edge_color` | The color of the outline around the countries highlight picks out, coast included. **TYPE:** \`str     |
| `plot_basemap_highlight_edge_width` | The width of that outline, in points; 0 (default) draws none. **TYPE:** \`float                        |
| `plot_basemap_coastline_color`      | The color of the coastlines. **TYPE:** \`str                                                           |
| `plot_basemap_coastline_width`      | The width of the coastlines, in points. **TYPE:** \`float                                              |
| `plot_basemap_border_color`         | The color of the borders between countries. **TYPE:** \`str                                            |
| `plot_basemap_border_width`         | The width of the borders, in points. **TYPE:** \`float                                                 |
| `plot_basemap_border_style`         | The line style of the borders. See LINE_STYLE. **TYPE:** \`LINE_STYLE                                  |
| `plot_basemap_lake_color`           | The fill color of the lakes; None takes the axes background, so a lake reads as water. **TYPE:** \`str |
| `plot_basemap_river_color`          | The color of the rivers. **TYPE:** \`str                                                               |
| `plot_basemap_river_width`          | The width of the rivers, in points. **TYPE:** \`float                                                  |
| `plot_basemap_road_color`           | The color of the roads. **TYPE:** \`str                                                                |
| `plot_basemap_road_width`           | The width of the roads, in points. **TYPE:** \`float                                                   |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter      | Constant                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `data`         | [`BASEMAP_FEATURE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.BASEMAP_FEATURE)       |
| `resolution`   | [`BASEMAP_RESOLUTION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.BASEMAP_RESOLUTION) |
| `position`     | [`DRAW_POSITION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.DRAW_POSITION)           |
| `figsize`      | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                     |
| `show_grid`    | [`SHOW_GRID`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.SHOW_GRID)                   |
| `aspect_ratio` | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)             |

## Composition

Whether the figure composes with each composition function.

| Function                                                                                     | Composes |
| -------------------------------------------------------------------------------------------- | -------- |
| [`Grid`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Grid)   | yes      |
| [`Panel`](https://eriknovak.github.io/datachart/dev/references/utils/#datachart.utils.Panel) | yes      |
