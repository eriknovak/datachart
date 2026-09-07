---
title: Interactive Figures
---

# Interactive Figures

Every figure `datachart` returns is static until shown: `figure.show()` renders it inline in a notebook and opens a GUI window in a script. Pass `interactive=True` to `show()` to zoom, pan, and hover over the marks instead. The flag is the only switch — the chart functions, `Panel`, `Grid`, and the `config` know nothing about it, and a figure shown the default way is byte-for-byte unchanged.

```python
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

![A line chart on an ipympl canvas: hovering a point shows its legend label, step, and loss; the zoom tool magnifies the crossing of the lines](../../assets/imgs/interactive-show.gif)

The recording is static because the documentation site has no Python kernel behind it; run the snippet in a notebook to get the live widget.

## Installing the extra

Interactivity needs two optional packages, [ipympl](https://matplotlib.org/ipympl/) for the notebook widget canvas and [mplcursors](https://mplcursors.readthedocs.io/) for the hover annotations. Install them with the `interactive` extra:

```bash
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

| Chart                                         | Mark                        | Annotation                                                                 | Hovered                                                                                             |
| :-------------------------------------------- | :-------------------------- | :------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| [Line Chart](../charts/linechart.ipynb)       | line point                  | legend label, `x`, `y`                                                     | ![A line chart with a hovered point](../../assets/imgs/hover-line.png){ width="300" }               |
| [Stacked Area Chart](../charts/stackedareachart.ipynb) | band, at the nearest point | legend label, `x`, the series' own `y` (never the stack total)      | ![A stacked area chart with a hovered band](../../assets/imgs/hover-stackedarea.png){ width="300" } |
| [Bar Chart](../charts/barchart.ipynb)         | bar                         | legend label, category, the bar's own value (never the stack total)        | ![A grouped bar chart with a hovered bar](../../assets/imgs/hover-bar.png){ width="300" }           |
| [Pyramid Chart](../charts/pyramidchart.ipynb) | bar                         | legend label, category, the value as passed, positive                      | ![A pyramid chart with a hovered bar](../../assets/imgs/hover-pyramid.png){ width="300" }           |
| [Radial Chart](../charts/radialchart.ipynb)   | point, bar, or bin          | legend label, `angle` (the category, or a bin's degree range), `radius`    | ![A radial bar chart with a hovered bar](../../assets/imgs/hover-radial.png){ width="300" }         |
| [Histogram](../charts/histogram.ipynb)        | bin                         | legend label, the bin's range, its count (or density)                      | ![A histogram with a hovered bin](../../assets/imgs/hover-histogram.png){ width="300" }             |
| [Box Plot](../charts/boxplot.ipynb)           | box                         | legend label, category, `median`, `q1`, `q3`, `min`, `max`                 | ![A box plot with a hovered box](../../assets/imgs/hover-box.png){ width="300" }                    |
| [Violin Plot](../charts/violinplot.ipynb)     | body                        | legend label (or the split value), category, `median`, `q1`, `q3`, `min`, `max` | ![A violin plot with a hovered body](../../assets/imgs/hover-violin.png){ width="300" }        |
| [Swarm Plot](../charts/swarmplot.ipynb)       | point                       | legend label, category, value                                              | ![A swarm plot with a hovered point](../../assets/imgs/hover-swarm.png){ width="300" }              |
| [Raincloud Plot](../charts/raincloudplot.ipynb) | box, body, or rain point  | as the box, violin, and swarm marks                                        | ![A raincloud plot with a hovered box](../../assets/imgs/hover-raincloud.png){ width="300" }        |
| [Scatter Chart](../charts/scatterchart.ipynb) | point                       | legend label (or the `hue` group), `x`, `y`                                | ![A scatter chart with a hovered point](../../assets/imgs/hover-scatter.png){ width="300" }         |
| [Heatmap](../charts/heatmap.ipynb)            | cell                        | legend label, `x`, `y`, `value`                                            | ![A heatmap with a hovered cell](../../assets/imgs/hover-heatmap.png){ width="300" }                |
| [Contour Chart](../charts/contourchart.ipynb) | level line or filled band   | legend label, `level` (a band's two levels)                                | ![A contour chart with a hovered level line](../../assets/imgs/hover-contour.png){ width="300" }    |
| [Hexbin Chart](../charts/hexbinchart.ipynb)   | hexagon                     | legend label, `x`, `y` (the cell center), `count` (or the reduced `c` under its reducer's name) | ![A hexbin chart with a hovered hexagon](../../assets/imgs/hover-hexbin.png){ width="300" } |
| [Parallel Coordinates](../charts/parallelcoords.ipynb) | row line, at the nearest axis | the `hue` value (or the legend label), the axis name and the row's value there | ![A parallel coordinates chart with a hovered row](../../assets/imgs/hover-parallelcoords.png){ width="300" } |
| [Network Chart](../charts/networkchart.ipynb) | node or edge                | node: its label, `degree` (the weight sum when weighted); edge: `source`, `target`, `weight` | ![A network chart with a hovered node](../../assets/imgs/hover-network.png){ width="300" } |
| [Sankey Chart](../charts/sankeychart.ipynb)   | node or link                | node: its name, `flow`; link: `source`, `target`, `flow`                   | ![A sankey chart with a hovered link](../../assets/imgs/hover-sankey.png){ width="300" }            |
| [Treemap](../charts/treemap.ipynb)            | tile or group band          | its label, `value` (a band's group total)                                  | ![A treemap with a hovered tile](../../assets/imgs/hover-treemap.png){ width="300" }                |
