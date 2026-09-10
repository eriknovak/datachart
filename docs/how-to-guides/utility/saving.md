---
title: Saving Figures
---

# Saving Figures

Every chart function returns a matplotlib figure. The [datachart.utils.save_figure](../../references/utils/index.md#datachart.utils.save_figure) function writes it to disk in the format given by its `format` argument or, when omitted, by the file extension. The theme is baked into the figure when it is created, so saving never consults the global `config`.

```python
from datachart.charts import LineChart
from datachart.utils import save_figure

figure = LineChart(
    data=[{"x": i, "y": i**2} for i in range(10)],
    subtitle="growth",
    xlabel="Step",
    ylabel="Value",
)
save_figure(figure, "chart.png", dpi=300)
```

## Choosing a format

- **Vector formats**, such as SVG and PDF. The marks are stored as shapes, so the figure stays crisp at any size and the file stays small for charts made of lines and bars. Use these for print, papers, and web pages.
- **Raster formats**, such as PNG. The figure is stored as pixels at the resolution set by `dpi`. Use `dpi=300` or higher for anything that will be printed or zoomed; the default is `300`.
- **`transparent=True`** drops the figure background, so the chart sits on whatever the page or slide behind it is colored.

The [FIG_FORMAT](../../references/constants.md#datachart.constants.FIG_FORMAT) constant lists every supported format.

## Writing several formats at once

A figure is often needed more than once: a PDF for the manuscript, a PNG for the preview, an SVG for the slides. Pass a list of formats and the same figure is written once per format.

```python
from datachart.constants import FIG_FORMAT

paths = save_figure(figure, "figures/growth", format=[FIG_FORMAT.PDF, FIG_FORMAT.PNG])
# ["figures/growth.pdf", "figures/growth.png"]
```

With a list, the path is a stem rather than a file name, and each format is appended to it. An extension on the stem is dropped when it names a supported format, so `figures/growth.png` and `figures/growth` behave the same; a dotted name such as `figures/growth.v2` keeps every part of itself and yields `figures/growth.v2.pdf`. A name that already exists is overwritten, and the parent directory must exist.

`save_figure` returns the paths it wrote, in the order the formats were given. It returns a list for a single format too, so the return value never changes shape.

`dpi` and `transparent` apply to every file in the call. Vector formats ignore `dpi`, so one call can carry a raster resolution alongside them without affecting the vector output. For different settings per format, make separate calls.

## Embedding in web pages

Export the figure as SVG with a transparent background:

```python
save_figure(figure, "chart.svg", transparent=True)
```

SVG is the right format for the web: it renders sharp on every screen density, it scales with the layout instead of being resized as an image, and for charts drawn from lines, bars, and text the file is usually smaller than a PNG of the same size. The transparent background lets the chart match the page in both light and dark color schemes.

There are two ways to put the SVG on a page:

- **As an image.** Reference the file from an `<img>` tag, the same as any picture. The chart is cached and reused across pages, its markup stays out of the HTML, and the page's CSS cannot reach into it. Prefer this when the chart is a static illustration.

    ```html
    <img src="chart.svg" alt="Value against step, growing quadratically" width="640">
    ```

- **Inline.** Paste the file's contents into the HTML directly. The chart becomes part of the document, so the page's CSS can restyle its strokes and fills, and text inside it is selectable and searchable. Prefer this when the chart should follow the page's styling or when there is a single chart per page. The markup is repeated on every page that shows it, so keep the number of inlined charts small.

    ```html
    <figure>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400">...</svg>
      <figcaption>Value against step.</figcaption>
    </figure>
    ```

When the page or platform cannot use SVG, save a PNG at `dpi=300` or higher and embed it the same way as the image above. Raster images blur when scaled up, so export at the largest size the page will display.

```python
save_figure(figure, "chart.png", dpi=300, transparent=True)
```

### Interactive web charts are out of scope

The exported file is a static picture. `datachart` does not render figures interactively in the browser: there is no HTML export, no embed snippet, and no zoom or hover on a web page. Interactivity is available in notebooks and GUI windows through `show(interactive=True)`, as described in the [interactive figures](interactive.md) section. For charts that zoom and hover inside a web page, use a browser-native library such as [d3](https://d3js.org/), [Plotly](https://plotly.com/javascript/), [Vega](https://vega.github.io/vega/), or [Bokeh](https://bokeh.org/).
