# Interactive Figures

Every figure `datachart` returns is static until shown: `figure.show()` renders it inline in a notebook and opens a GUI window in a script. Pass `interactive=True` to `show()` to zoom, pan, and hover over the marks instead. The flag is the only switch — the chart functions, `Panel`, `Grid`, and the `config` know nothing about it, and a figure shown the default way is byte-for-byte unchanged.

```
from datachart.charts import LineChart

figure = LineChart(
    data=[{"x": i, "y": i**2} for i in range(10)],
    subtitle="growth",
    xlabel="Step",
    ylabel="Value",
)
figure.show(interactive=True)
```

The figure above, shown in a notebook, hovered and zoomed:

The recording is static because the documentation site has no Python kernel behind it; run the snippet in a notebook to get the live widget.

## Installing the extra

Interactivity needs two optional packages, [ipympl](https://matplotlib.org/ipympl/) for the notebook widget canvas and [mplcursors](https://mplcursors.readthedocs.io/) for the hover annotations. Install them with the `interactive` extra:

```
pip install "datachart[interactive]"   # or: uv add "datachart[interactive]"
```

Without them `show(interactive=True)` raises an `ImportError` naming the missing package and the extra. It never falls back to a static figure.

## Zoom and pan

- **Notebooks.** The figure is displayed on an `ipympl` widget canvas with the matplotlib toolbar: zoom to a rectangle, pan, step back through views, and save. The widget takes the place of the static image, so nothing is displayed twice.
- **Scripts.** The figure opens in the GUI window it always did; the window's own toolbar provides the zoom and pan.

## Hover to inspect

Hovering a mark shows an annotation with the series' legend label on the first line — its `subtitle`, or the `legend_label` a `Panel` assigned — and one `name: value` line per field of the mark. A mark that stands for a data point reports its axis coordinates: the names are the axis labels of the chart when set (`xlabel`, `ylabel`, and a `Panel`'s `ylabel_left` / `ylabel_right`), and `x` / `y` otherwise; a series on a `Panel`'s secondary value axis reports the secondary label. Values are formatted the way the axis formats its coordinates, so a point on a category axis reports the category name. A mark that stands for an aggregate reports its summary under plain names — a box its `median` and quartiles, a histogram bin its range and count, a sankey link its endpoints and `flow`. The annotation wears the theme's text annotation style — the `plot_text_*` font, box, and connector — so it matches the figure it sits on.

Hover follows the marks through composition: it works on every series of a `Panel` overlay, including those on the secondary axis, and in every cell of a `Grid`. Text annotations and reference lines decorate the chart and carry no hover.

Every chart type has hover support. Filled marks — bars, bands, boxes, bodies, cells, hexagons, tiles, nodes, ribbons — pick anywhere inside; lines, outlines, and network edges pick within a few points of their stroke, as do the outline of a `step` histogram and the edges of a filled contour band.

| Chart                                                                                                          | Mark                          | Annotation                                                                                                                                                  |
| -------------------------------------------------------------------------------------------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Line Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/linechart/index.md)                | line point                    | legend label, `x`, `y`                                                                                                                                      |
| [Stacked Area Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/stackedareachart/index.md) | band, at the nearest point    | legend label, `x`, the series' own `y` (never the stack total)                                                                                              |
| [Bar Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/barchart/index.md)                  | bar                           | legend label, category, the bar's own value (never the stack total)                                                                                         |
| [Pyramid Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/pyramidchart/index.md)          | bar                           | legend label, category, the value as passed, positive                                                                                                       |
| [Radial Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/radialchart/index.md)            | point, bar, or bin            | legend label, `angle` (the category, or a bin's degree range), `radius`                                                                                     |
| [Histogram](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/histogram/index.md)                 | bin                           | legend label, the bin's range, its count (or density)                                                                                                       |
| [Box Plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/boxplot/index.md)                    | box                           | legend label, category, `median`, `q1`, `q3`, `min`, `max`                                                                                                  |
| [Violin Plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/violinplot/index.md)              | body                          | legend label (or the split value), category, `median`, `q1`, `q3`, `min`, `max`                                                                             |
| [Swarm Plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/swarmplot/index.md)                | point                         | legend label, category, value                                                                                                                               |
| [Raincloud Plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/raincloudplot/index.md)        | box, body, or rain point      | as the box, violin, and swarm marks                                                                                                                         |
| [Scatter Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md)          | point                         | legend label (or the `hue` group), `x`, `y`                                                                                                                 |
| [Heatmap](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/heatmap/index.md)                     | cell                          | legend label, `x`, `y`, `value`                                                                                                                             |
| [Contour Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/contourchart/index.md)          | level line or filled band     | legend label, `level` (a band's two levels)                                                                                                                 |
| [Hexbin Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/hexbinchart/index.md)            | hexagon                       | legend label, `x`, `y` (the cell center), `count` (or the reduced `c` under its reducer's name)                                                             |
| [Parallel Coordinates](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/parallelcoords/index.md) | row line, at the nearest axis | the `hue` value (or the legend label), the axis name and the row's value there                                                                              |
| [Network Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/networkchart/index.md)          | node or edge                  | node: its label, `degree` (`in` / `out` when directed, the weight sum when weighted), its `group` and `size` when given; edge: `source`, `target`, `weight` |
| [Sankey Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/sankeychart/index.md)            | node or link                  | node: its name, `flow`; link: `source`, `target`, `flow`                                                                                                    |
| [Treemap](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/treemap/index.md)                     | tile or group band            | its label, `value` (a band's group total)                                                                                                                   |

The annotation on each chart, from the figure shown with `show(interactive=True)` and a mark hovered:

| **Line Chart** — a hovered point | **Stacked Area Chart** — a hovered band |
| -------------------------------- | --------------------------------------- |
|                                  |                                         |

| **Bar Chart** — a hovered bar | **Pyramid Chart** — a hovered bar |
| ----------------------------- | --------------------------------- |
|                               |                                   |

| **Radial Chart** — a hovered bar | **Histogram** — a hovered bin |
| -------------------------------- | ----------------------------- |
|                                  |                               |

| **Box Plot** — a hovered box | **Violin Plot** — a hovered body |
| ---------------------------- | -------------------------------- |
|                              |                                  |

| **Swarm Plot** — a hovered point | **Raincloud Plot** — a hovered box |
| -------------------------------- | ---------------------------------- |
|                                  |                                    |

| **Scatter Chart** — a hovered point | **Heatmap** — a hovered cell |
| ----------------------------------- | ---------------------------- |
|                                     |                              |

| **Contour Chart** — a hovered level line | **Hexbin Chart** — a hovered hexagon |
| ---------------------------------------- | ------------------------------------ |
|                                          |                                      |

| **Parallel Coordinates** — a hovered row | **Network Chart** — a hovered node |
| ---------------------------------------- | ---------------------------------- |
|                                          |                                    |

| **Sankey Chart** — a hovered link | **Treemap** — a hovered tile |
| --------------------------------- | ---------------------------- |
|                                   |                              |
