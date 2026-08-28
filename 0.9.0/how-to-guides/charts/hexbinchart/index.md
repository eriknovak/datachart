# Hexbin Chart

This section showcases the hexbin chart. It contains examples of how to create hexbin charts using the [datachart.charts.HexbinChart](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.HexbinChart) function.

Looking for a specific customization? Jump straight to the [quick reference](#customizing-the-hexbin-chart), which maps common tasks to the parameter or style attribute that does the job.

As mentioned above, the hexbin charts are created using the `HexbinChart` function found in the [datachart.charts](https://eriknovak.github.io/datachart/0.9.0/references/charts/index.md) module. Let's import it:

```
from datachart.charts import HexbinChart
```

## Hexbin Chart Input Attributes

The `HexbinChart` function accepts keyword arguments for chart configuration. The main argument is `data`, which contains the points to bin. For a single hexbin chart, `data` is a dictionary with the `x` and `y` columns and an optional `c` column of per-point values; for multiple hexbin charts, `data` is a list of such dictionaries.

```
HexbinChart(
    data={                                              # The points to bin (or list of them for multiple charts)
        "x": List[Union[int, float]],                   # The x values of the points
        "y": List[Union[int, float]],                   # The y values of the points, one per x
        "c": Optional[List[Union[int, float]]],         # The value of each point; when given, the hexagons show its aggregate instead of the count
    },
    style={                                             # The style of the hexbin chart (optional)
        "plot_hexbin_cmap":       Optional[Union[str, List[str]]], # The colormap of the hexagons (the heatmap colormap by default)
        "plot_hexbin_alpha":      Optional[float],      # The alpha of the hexagons
        "plot_hexbin_edge_width": Optional[Union[int, float]], # The width of the hexagon edges (0, no edges, by default)
        "plot_hexbin_edge_color": Optional[str],        # The color of the hexagon edges
        "plot_hexbin_gridsize":   Optional[int],        # The number of hexagons across the x-axis when gridsize is not set
    },
    title: Optional[str],                               # The title of the chart
    xlabel: Optional[str],                              # The x-axis label
    ylabel: Optional[str],                              # The y-axis label
    subtitle: Optional[Union[str, List[str]]],          # The subtitle(s) of the charts
    figsize: Optional[Tuple[float, float]],             # The size of the figure
    xmin: Optional[Union[int, float]],                  # The minimum x-axis value
    xmax: Optional[Union[int, float]],                  # The maximum x-axis value
    ymin: Optional[Union[int, float]],                  # The minimum y-axis value
    ymax: Optional[Union[int, float]],                  # The maximum y-axis value
    show_grid: Optional[str],                           # Which grid lines to show ("both", "x", "y"); off by default
    show_colorbars: Optional[bool],                     # Whether to show the colorbar(s); on by default
    aspect_ratio: Optional[str],                        # The aspect ratio of the axes ("auto", "equal")
    scalex: Optional[str],                              # The x-axis scale ("linear", "log", ...)
    scaley: Optional[str],                              # The y-axis scale ("linear", "log", ...)
    subplots: Optional[bool],                           # Whether to create a separate subplot for each chart
    max_cols: Optional[int],                            # The maximum number of columns in the subplots
    sharex: Optional[bool],                             # Whether to share the x-axis across the subplots
    sharey: Optional[bool],                             # Whether to share the y-axis across the subplots
    gridsize: Optional[Union[int, List[int]]],          # The number of hexagons across the x-axis (30 by default)
    reduce: Optional[Union[str, List[str]]],            # How the c values in a hexagon collapse into its color ("mean", "sum", "median", "min", "max")
    mincnt: Optional[Union[int, List[int]]],            # The point count below which a hexagon stays blank
    norm: Optional[Union[str, List[str]]],              # The value normalization of the colormap
    vmin: Optional[Union[float, List[float]]],          # The minimum value of the colormap range
    vmax: Optional[Union[float, List[float]]],          # The maximum value of the colormap range
    valfmt: Optional[Union[str, List[str]]],            # The format of the colorbar tick labels (e.g. "{x:.0f}")
    xticks: Optional[List[Union[int, float]]],          # The x-axis tick positions
    xticklabels: Optional[List[str]],                   # The x-axis tick labels
    xtickrotate: Optional[int],                         # The rotation of the x-axis tick labels
    yticks: Optional[List[Union[int, float]]],          # The y-axis tick positions
    yticklabels: Optional[List[str]],                   # The y-axis tick labels
    ytickrotate: Optional[int],                         # The rotation of the y-axis tick labels
    vlines: Optional[Union[dict, List[dict]]],          # The vertical reference lines
    hlines: Optional[Union[dict, List[dict]]],          # The horizontal reference lines
    colorbar: Optional[Union[dict, List[dict]]],        # The colorbar configuration(s) ({"orientation": ...})
    texts: Optional[Union[dict, List[dict]]],           # The text annotations
)
```

For more details, see the [datachart.charts.HexbinChart](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.HexbinChart) function.

## Basics

The examples in this guide share one dataset: 8,000 apartment listings of a mid-sized city — the floor area of each apartment, its monthly rent, and the number of days it stayed on the market. The listings are simulated in the hidden cell below from the shape real rental markets have: floor areas cluster around 60 m² with a long tail of large apartments, the rent grows with the area at a rate that varies by district, and small, cheap apartments go fastest. Eight thousand points are far too many for a scatter chart to show anything but a blob; the hexbin chart bins them.

The data is a dictionary of columns: `x` holds the floor area of every listing, `y` its rent, and `c` its days on the market — one value per listing in each column. A `c` column switches the hexagons from counting the points to aggregating its values, so the hidden cell also keeps `points`, the `x` and `y` columns alone, for the charts that count:

```
{key: values[:5] for key, values in listings.items()}
```

**Basic example.** Only the `data` argument is required to draw the hexbin chart. The plane is tiled with hexagons and every hexagon is colored by the number of listings falling in it, with a colorbar mapping the colors back to counts. Every hexagon of the tiling is drawn, the empty ones at the lowest color, so a single far-off listing — one large, expensive apartment here — stretches the tiling over a lot of blank plane; the [Minimum count](#minimum-count) section trims it.

```
HexbinChart(
    # add the data to the chart
    data=points
).show()
```

## Customizing the Hexbin Chart

Every customization is either a keyword argument of `HexbinChart` or a `plot_hexbin_*` attribute of its `style` dictionary. The table maps common tasks to the one you need and links to the subsection that shows it.

| I want to…                                 | Use                                                              | See                                               |
| ------------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------- |
| add a title and axis labels                | `title`, `xlabel`, `ylabel`                                      | [Title and axis labels](#title-and-axis-labels)   |
| resize the figure                          | `figsize`                                                        | [Figure size and grid](#figure-size-and-grid)     |
| show the grid lines                        | `show_grid`                                                      | [Figure size and grid](#figure-size-and-grid)     |
| hide or reorient the colorbar              | `show_colorbars=False`, `colorbar={"orientation": ...}`          | [Colorbar](#colorbar)                             |
| make the hexagons larger or smaller        | `gridsize`                                                       | [Grid size](#grid-size)                           |
| leave the sparse hexagons blank            | `mincnt`                                                         | [Minimum count](#minimum-count)                   |
| spread heavy-tailed counts over the colors | `norm`, `vmin`, `vmax`                                           | [Normalization](#normalization)                   |
| color the hexagons by a value              | `data={"c": ...}`, `reduce`                                      | [Aggregating a value](#aggregating-a-value)       |
| change the colormap or draw hexagon edges  | `style={"plot_hexbin_cmap": ..., "plot_hexbin_edge_width": ...}` | [Hexagon style](#hexagon-style)                   |
| draw each dataset in its own subplot       | `subplots=True`, `max_cols`, `sharex`, `sharey`                  | [Multiple Hexbin Charts](#multiple-hexbin-charts) |
| draw points or lines over the hexagons     | `Panel`                                                          | [Composing hexbins](#composing-hexbins)           |
| keep one unit equal on both axes           | `aspect_ratio`                                                   | [Aspect ratio](#aspect-ratio)                     |
| mark a position with a reference line      | `vlines`, `hlines`                                               | [Reference lines](#reference-lines)               |
| render the chart in another theme          | `config.set_theme`                                               | [Themes](#themes)                                 |

### Title and axis labels

To add the chart title and axis labels, add the `title`, `xlabel` and `ylabel` attributes.

```
HexbinChart(
    data=points,
    # add the title
    title="Apartment listings",
    # add the x and y axis labels
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
).show()
```

### Figure size and grid

To change the figure size, add the `figsize` attribute. The `figsize` attribute can be a tuple (width, height), values are in inches. The `datachart` package provides a [datachart.constants.FIG_SIZE](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.FIG_SIZE) constant, which contains predefined figure sizes. The grid is off by default, as the hexagons would cover it; to show it anyway, add the `show_grid` attribute, which supports the values of the [datachart.constants.SHOW_GRID](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.SHOW_GRID) constant — the grid lines draw over the hexagons.

```
from datachart.constants import FIG_SIZE, SHOW_GRID
```

```
HexbinChart(
    data=points,
    title="Apartment listings",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    # add to determine the figure size
    figsize=FIG_SIZE.FULL_SHORT,
    # add to show the grid lines on both axes
    show_grid=SHOW_GRID.BOTH,
).show()
```

### Colorbar

The colorbar maps the hexagon colors back to their values and is drawn to the right of the chart by default. To hide it, set the `show_colorbars` attribute to `False`; to draw it horizontally instead, add the `colorbar` attribute with the [datachart.typings.HeatmapColorbarAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.HeatmapColorbarAttrs) typing, whose `orientation` takes a value of the [datachart.constants.ORIENTATION](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.ORIENTATION) constant. The `valfmt` attribute formats its tick labels with a format string with the value named `x`; the [datachart.constants.VALUE_FORMAT](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.VALUE_FORMAT) constant holds the common ones.

```
from datachart.constants import ORIENTATION, VALUE_FORMAT
```

```
HexbinChart(
    data=points,
    # draw the colorbar above the chart, with integer ticks
    colorbar={"orientation": ORIENTATION.HORIZONTAL},
    valfmt=VALUE_FORMAT.INTEGER,
    title="Apartment listings",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Grid size

The `gridsize` attribute sets how many hexagons tile the x-axis — 30 by default, from the `plot_hexbin_gridsize` config value. Fewer hexagons are larger and hold more points each, so the colors are smoother but the shape coarser; more hexagons resolve finer structure until they hold too few points to color reliably.

```
HexbinChart(
    data=points,
    # twelve large hexagons across the x-axis
    gridsize=12,
    title="Apartment listings",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

### Minimum count

Every hexagon of the tiling is drawn by default, including the empty ones at the lowest color, so the tiling fills the bounding box of the points. To leave the sparse hexagons blank, add the `mincnt` attribute: a hexagon is drawn only when at least that many points fall in it, which trims the tiling down to where the listings actually are.

```
HexbinChart(
    data=points,
    # blank hexagons with fewer than five listings
    mincnt=5,
    title="Apartment listings",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

### Normalization

The colors come from a two-step mapping: the hexagon values are first normalized to the 0–1 range, then each normalized value picks its color from the colormap. Counts are heavy-tailed — a few hexagons in the densest cluster hold dozens of listings while most hold a handful — so on the linear default nearly every hexagon draws in the palest shades. The `norm` attribute changes the normalization; the [datachart.constants.NORMALIZE](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.NORMALIZE) constant holds the supported values, and `NORMALIZE.LOG` spreads the counts so the tail of the distribution is visible. A log scale needs positive values, so pair it with `mincnt=1` to leave the empty hexagons out. The `vmin` and `vmax` attributes pin the range instead of taking it from the data.

```
from datachart.constants import NORMALIZE
```

```
HexbinChart(
    data=points,
    # log-scaled counts, so the sparse tail stays visible
    norm=NORMALIZE.LOG,
    mincnt=1,
    title="Apartment listings",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

### Aggregating a value

With a `c` column in the data, the hexagons show an aggregate of the `c` values of their points instead of the point count. The `reduce` attribute picks the aggregate with a value of the [datachart.constants.HEXBIN_REDUCE](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.HEXBIN_REDUCE) constant — the mean by default, or the sum, median, minimum, or maximum. Only the hexagons holding at least one point are drawn, as an empty hexagon has nothing to aggregate. Here `c` is the number of days a listing stayed on the market, so the chart below shows how long the apartments of every size and price took to rent: the mean rises with the floor area and, at every area, with the rent. A diverging colormap suits a value with a natural middle; the [Hexagon style](#hexagon-style) section shows how to set it.

```
from datachart.constants import HEXBIN_REDUCE
```

```
HexbinChart(
    # x, y, and the per-point c to aggregate
    data=listings,
    # the mean of the c values in every hexagon
    reduce=HEXBIN_REDUCE.MEAN,
    # aggregates of a few points are noisy; blank the sparse hexagons
    mincnt=3,
    title="Days on the market",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

The other aggregates answer other questions. The maximum finds the listings that stayed longest — the outliers — where the mean smooths them away:

```
HexbinChart(
    data=listings,
    # the longest-listed apartment in every hexagon
    reduce=HEXBIN_REDUCE.MAX,
    mincnt=3,
    title="Longest time on the market",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

### Hexagon style

To change the hexagon style, add the `style` attribute with the corresponding attributes. The supported attributes are shown in the [datachart.typings.HexbinStyleAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.HexbinStyleAttrs) typing. The `plot_hexbin_cmap` attribute sets the colormap — the heatmap colormap by default — from the [datachart.constants.COLORS](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.COLORS) constant or a list of colors; `plot_hexbin_edge_width` and `plot_hexbin_edge_color` draw an edge around every hexagon, which separates the tiles where the colors run together.

```
from datachart.constants import COLORS
```

```
HexbinChart(
    data=listings,
    reduce=HEXBIN_REDUCE.MEAN,
    mincnt=3,
    # define the style of the hexagons
    style={
        "plot_hexbin_cmap": COLORS.RdBu,
        "plot_hexbin_edge_width": 0.6,
        "plot_hexbin_edge_color": "#FFFFFF",
    },
    gridsize=20,
    title="Days on the market",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

!!! note "No emphasis"

```
A hexbin chart is a single colormapped layer, so it does not take the `emphasis` attribute of the series charts: there is no series color to mute or highlight. To draw attention to a region, overlay a marker or a reference line instead (see [Composing hexbins](#composing-hexbins) and [Reference lines](#reference-lines)).
```

## Multiple Hexbin Charts

To create multiple hexbin charts, pass a list of datasets to the `data` argument and add the `subplots` attribute to draw each in its own subplot. Hexagons are opaque, so several datasets on one axes would hide each other; subplots keep them comparable. The `subtitle` becomes the subplot title and the `title`, `xlabel` and `ylabel` are positioned to be global for all charts. The `max_cols` attribute limits the number of columns, and `sharex` and `sharey` share an axis across the subplots; a shared axis is labeled once, on the outer subplots only. Per-chart attributes like `subtitle`, `style`, `gridsize`, `reduce`, `mincnt`, `norm`, `vmin`, `vmax`, `valfmt` and `colorbar` can be passed as lists, where each element corresponds to a chart; a single value applies to every chart.

The listings split by district in the hidden cell, as `by_district` (with `c`) and `points_by_district` (without): the three per-m² rates of the simulation stand in for a cheap, a mid-priced, and an expensive district.

```
HexbinChart(
    # use a list of datasets to define multiple hexbin charts
    data=points_by_district,
    # one subplot title per chart
    subtitle=DISTRICTS,
    subplots=True,
    max_cols=3,
    # the same axes for every district
    sharex=True,
    sharey=True,
    # the same color range on every chart, so the shades are comparable
    vmin=0,
    vmax=60,
    mincnt=1,
    gridsize=20,
    title="Apartment listings by district",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=(12, 4),
).show()
```

## Composing hexbins

A hexbin figure composes like any other chart. [datachart.utils.Panel](https://eriknovak.github.io/datachart/0.9.0/references/utils/#datachart.utils.Panel) overlays it with other charts on shared axes — the natural pairing is a [datachart.charts.ScatterChart](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.ScatterChart) of a few points of interest drawn over the density of all of them, or a [datachart.charts.LineChart](https://eriknovak.github.io/datachart/0.9.0/references/charts/#datachart.charts.LineChart) of a fitted trend. Here a random sample of 60 listings sits on the hexagons, with white edges so the tiles read under the points; the hexbin's colorbar is left off, as the panel's legend labels the points.

```
from datachart.charts import ScatterChart
from datachart.utils import Panel

sample = rng.choice(N_LISTINGS, 60, replace=False)

Panel(
    [
        HexbinChart(
            data=points,
            style={"plot_hexbin_edge_width": 0.5, "plot_hexbin_edge_color": "#FFFFFF"},
            show_colorbars=False,
        ),
        # a sample of the listings, as points over the hexagons
        ScatterChart(
            data=[{"x": listings["x"][i], "y": listings["y"][i]} for i in sample],
            subtitle="Sampled listings",
        ),
    ],
    title="Apartment listings",
    xlabel="Floor area (m²)",
    ylabel_left="Rent (€/month)",
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

[datachart.utils.Grid](https://eriknovak.github.io/datachart/0.9.0/references/utils/#datachart.utils.Grid) arranges hexbin figures next to other figures. The count of the listings spans the top row; the days on the market and a histogram of the rents share the bottom one.

```
from datachart.charts import Histogram
from datachart.utils import Grid

Grid(
    [
        [HexbinChart(data=points, mincnt=1, norm=NORMALIZE.LOG, title="Listings")],
        [
            HexbinChart(
                data=listings,
                reduce=HEXBIN_REDUCE.MEAN,
                mincnt=3,
                title="Days on the market",
            ),
            Histogram(
                data=[{"x": value} for value in listings["y"]],
                title="Rent (€/month)",
            ),
        ],
    ],
    figsize=(10, 7),
).show()
```

## Additional Features

### Aspect ratio

By default the axes stretch to fill the figure, so the hexagons are regular on the screen but the two axes have different scales. When both axes share a unit — two coordinates, two scores on the same scale — add the `aspect_ratio` attribute with a value of the [datachart.constants.ASPECT_RATIO](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.ASPECT_RATIO) constant to keep one unit equal on both. The hidden cell scales the listings to z-scores, so both axes read in standard deviations.

```
from datachart.constants import ASPECT_RATIO
```

```
HexbinChart(
    data=standardized,
    # keep one unit equal on both axes
    aspect_ratio=ASPECT_RATIO.EQUAL,
    mincnt=1,
    title="Apartment listings (standardized)",
    xlabel="Floor area (z-score)",
    ylabel="Rent (z-score)",
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Reference lines

A reference line marks a position on the plane. To add vertical lines, add the `vlines` attribute with the [datachart.typings.VLinePlotAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.VLinePlotAttrs) typing; for horizontal lines, add the `hlines` attribute with the [datachart.typings.HLinePlotAttrs](https://eriknovak.github.io/datachart/0.9.0/references/typings/#datachart.typings.HLinePlotAttrs) typing. The lines below mark the median floor area and rent, which split the listings into four quadrants.

```
from datachart.constants import LINE_STYLE
```

```
HexbinChart(
    data=points,
    # the median area and rent, as dashed cross-hairs
    vlines={
        "x": float(np.median(listings["x"])),
        "label": "Median area",
        "style": {"plot_vline_style": LINE_STYLE.DASHED},
    },
    hlines={
        "y": float(np.median(listings["y"])),
        "label": "Median rent",
        "style": {"plot_hline_style": LINE_STYLE.DASHED},
    },
    mincnt=1,
    title="Apartment listings",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

### Themes

A theme sets the colormap and the furniture of every chart at once; see the [Theme Gallery](https://eriknovak.github.io/datachart/0.9.0/how-to-guides/styling/theme-gallery.ipynb) for the whole suite under each. Apply one with [datachart.config.Config.set_theme](https://eriknovak.github.io/datachart/0.9.0/references/config/#datachart.config.Config.set_theme) from the [datachart.constants.THEME](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.THEME) constant, and reset the configuration afterwards so the following charts draw in the default.

```
from datachart.config import config
from datachart.constants import THEME

config.set_theme(THEME.INK)

figure = HexbinChart(
    data=points,
    mincnt=1,
    title="Apartment listings",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_SHORT,
)

config.reset_config()
figure.show()
```

## Saving the Chart as an Image

To save the chart as an image, use the [datachart.utils.save_figure](https://eriknovak.github.io/datachart/0.9.0/references/utils#datachart.utils.save_figure) function.

```
from datachart.utils import save_figure

figure = HexbinChart(
    data=points,
    mincnt=1,
    norm=NORMALIZE.LOG,
    title="Apartment listings",
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=FIG_SIZE.FULL_MEDIUM,
)
save_figure(figure, "./fig_hexbin_chart.png", dpi=300)
```

The figure should be saved in the current working directory.

## Real-World Examples

The following examples put the features above to work on realistic data. Each one states what its data is and where it comes from; the data itself lives in a hidden cell.

### Example 1: Price per Square Meter Across the City (Aggregation, Diverging Colors, and a Trend)

`listings` from the sections above holds the area, rent, and days on the market of 8,000 apartments. The hidden cell derives the rent per square meter of every listing — the number a renter compares across sizes — and a linear fit of the rent on the area. Colored by the mean rent per square meter, the hexagons show what the counts hide: at every floor area the listings stack into three bands, one per district rate, and the expensive band grows thinner toward the large apartments. A diverging colormap centered on the city-wide mean by `vmin` and `vmax` splits the plane into the cheaper-than-average blues and the pricier reds, and the `Panel` lays the fitted rent over the tiles, pinned to the primary axis with `y_axis`.

```
from datachart.charts import LineChart

Panel(
    [
        HexbinChart(
            data={"x": listings["x"], "y": listings["y"], "c": per_m2},
            reduce=HEXBIN_REDUCE.MEAN,
            mincnt=3,
            # a diverging colormap centered on the city-wide mean; the "_r"
            # suffix reverses it, so the cheap side is blue
            style={"plot_hexbin_cmap": "RdBu_r"},
            vmin=CITY_MEAN - 5,
            vmax=CITY_MEAN + 5,
            valfmt="{x:.0f} €/m²",
            gridsize=24,
        ),
        {
            "figure": LineChart(
                data=fit,
                subtitle=f"Fitted rent ({slope:.1f} €/m² + {intercept:.0f} €)",
                style={"plot_line_color": "#1F1F1F", "plot_line_style": LINE_STYLE.DASHED},
            ),
            # the fit shares the hexbin's axes
            "y_axis": "left",
        },
    ],
    title="Rent per square meter",
    xlabel="Floor area (m²)",
    ylabel_left="Rent (€/month)",
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
).show()
```

### Example 2: Which Apartments Rent Fastest, by District (Subplots, Shared Range, and Log Counts)

`by_district` from the multiple-charts section splits the listings into the three districts. The top row counts the listings of every district on a log scale, so the sparse edges of the cheaper districts stay visible next to their dense cores; the bottom row shows the mean days on the market under one shared `vmin`/`vmax`, so the same shade means the same wait in every district. Read down a column: the center's apartments are fewer, pricier, and slower to rent at every size, while the outskirts turn over their small apartments within a couple of weeks. The two `HexbinChart` figures, each a row of subplots, stack as the two rows of a `Grid`.

```
Grid(
    [
        [
            HexbinChart(
                data=points_by_district,
                subtitle=DISTRICTS,
                subplots=True,
                max_cols=3,
                sharex=True,
                sharey=True,
                norm=NORMALIZE.LOG,
                mincnt=1,
                gridsize=18,
                title="Listings (log count)",
            )
        ],
        [
            HexbinChart(
                data=by_district,
                subtitle=DISTRICTS,
                subplots=True,
                max_cols=3,
                sharex=True,
                sharey=True,
                reduce=HEXBIN_REDUCE.MEAN,
                mincnt=3,
                # the same range on every chart, so the shades are comparable
                vmin=10,
                vmax=50,
                gridsize=18,
                style={"plot_hexbin_cmap": COLORS.YlOrRd},
                title="Days on the market (mean)",
            )
        ],
    ],
    xlabel="Floor area (m²)",
    ylabel="Rent (€/month)",
    figsize=(12, 8),
).show()
```
