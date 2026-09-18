# Saving Figures

A chart that stays in a notebook reaches one reader. The [datachart.utils.save_figure](https://eriknovak.github.io/datachart/0.10.0/references/utils/#datachart.utils.save_figure) function writes the figure a chart function returns to disk, in one format or several, at the resolution the destination needs. This guide shows how to choose a format for where the figure is going, starting with the basics and building up to worked examples: a figure set for a manuscript, a slide, and a chart on a web page.

Looking for a specific task? Jump straight to the [quick reference](#choosing-the-output), which maps common destinations to the arguments that fit them.

## Basics

Every chart function returns a matplotlib figure. Pass it to `save_figure` with a path, and the extension picks the format. The theme is baked into the figure when it is created, so saving never consults the global `config`, and a figure saved later looks the way it did when it was drawn.

```
from datachart.charts import LineChart
from datachart.utils import save_figure

figure = LineChart(
    data=[{"x": i, "y": i**2} for i in range(10)],
    subtitle="growth",
    xlabel="Step",
    ylabel="Value",
)
save_figure(figure, "chart.png")
```

The function returns the list of paths it wrote, here `["chart.png"]`. The parent directory must exist, and a file that already exists is overwritten.

## Choosing the Output

The format, resolution and background are the three choices, and the destination decides each of them. The table maps the common destinations to the arguments that fit; the [FIG_FORMAT](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.FIG_FORMAT) constant lists every supported format.

| I want to…                                    | Use                                          | See                                                                                                         |
| --------------------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| put the figure in a paper or a printed report | `format=FIG_FORMAT.PDF` or `.svg`            | [Vector or raster](#vector-or-raster)                                                                       |
| upload it where only images are accepted      | `format=FIG_FORMAT.PNG`, `dpi=300` or higher | [Vector or raster](#vector-or-raster)                                                                       |
| lay it on a colored slide or page             | `transparent=True`                           | [Transparent background](#transparent-background)                                                           |
| write a PDF and a PNG of the same figure      | `format=[FIG_FORMAT.PDF, FIG_FORMAT.PNG]`    | [Several formats at once](#several-formats-at-once)                                                         |
| show it on a web page                         | SVG in an `<img>` tag, or inline             | [Embedding in web pages](#embedding-in-web-pages)                                                           |
| size it for the destination before saving     | `figsize` on the chart function              | [FIG_SIZE](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.FIG_SIZE) |

### Vector or raster

*Will the figure be scaled?* A **vector** format (PDF, SVG, EPS) stores the marks as shapes, so the figure stays crisp at any size and the file stays small for charts made of lines, bars and text. Use it for print, papers and web pages, and whenever the reader may zoom. A **raster** format (PNG, JPG, WEBP, TIFF) stores pixels at the resolution set by `dpi`, so it is the format for submission portals, chat, and slides that accept only images. The default `dpi` is 300, which prints cleanly; go higher for a figure that will be enlarged, and never below 150 for anything printed. Vector formats ignore `dpi`.

```
from datachart.constants import FIG_FORMAT

save_figure(figure, "chart.pdf")                       # vector, from the extension
save_figure(figure, "chart", format=FIG_FORMAT.PNG, dpi=600)  # raster, at 600 dots per inch
```

### Transparent background

*What is behind the figure?* By default the figure has the theme's background color, which is right on a white page and wrong on a colored slide, a dark web page, or a poster: the chart arrives in a white rectangle. `transparent=True` drops the figure background, so the chart sits on whatever is behind it.

```
save_figure(figure, "chart.png", transparent=True)
```

Text and marks keep their own colors, so a transparent figure meant for a dark background needs a theme with light text; the [Themes](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/styling/themes/index.md) guide shows how to set one before the chart is drawn.

### Several formats at once

*Who else needs this figure?* A figure is often needed more than once: a PDF for the manuscript, a PNG for the preview, an SVG for the slides. Pass a list of formats and the same figure is written once per format.

```
paths = save_figure(figure, "figures/growth", format=[FIG_FORMAT.PDF, FIG_FORMAT.PNG])
# ["figures/growth.pdf", "figures/growth.png"]
```

With a list, the path is a stem rather than a file name, and each format is appended to it. An extension on the stem is dropped when it names a supported format, so `figures/growth.png` and `figures/growth` behave the same; a dotted name such as `figures/growth.v2` keeps every part of itself and yields `figures/growth.v2.pdf`.

`save_figure` returns the paths it wrote, in the order the formats were given. It returns a list for a single format too, so the return value never changes shape. `dpi` and `transparent` apply to every file in the call; vector formats ignore `dpi`, so one call can carry a raster resolution alongside them. For different settings per format, make separate calls.

### Embedding in web pages

*Which screens will show it?* Export the figure as SVG with a transparent background:

```
save_figure(figure, "chart.svg", transparent=True)
```

SVG is the right format for the web: it renders sharp on every screen density, it scales with the layout instead of being resized as an image, and for charts drawn from lines, bars and text the file is usually smaller than a PNG of the same size. The transparent background lets the chart match the page in both light and dark color schemes.

There are two ways to put the SVG on a page:

- **As an image.** Reference the file from an `<img>` tag, the same as any picture. The chart is cached and reused across pages, its markup stays out of the HTML, and the page's CSS cannot reach into it. Prefer this when the chart is a static illustration.

  ```
  <img src="chart.svg" alt="Value against step, growing quadratically" width="640">
  ```

- **Inline.** Paste the file's contents into the HTML directly. The chart becomes part of the document, so the page's CSS can restyle its strokes and fills, and text inside it is selectable and searchable. Prefer this when the chart should follow the page's styling or when there is a single chart per page. The markup is repeated on every page that shows it, so keep the number of inlined charts small.

  ```
  <figure>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400">...</svg>
    <figcaption>Value against step.</figcaption>
  </figure>
  ```

When the page or platform cannot use SVG, save a PNG at `dpi=300` or higher and embed it the same way as the image above. Raster images blur when scaled up, so export at the largest size the page will display.

The exported file is a static picture. `datachart` does not render figures interactively in the browser: there is no HTML export, no embed snippet, and no zoom or hover on a web page. Interactivity is available in notebooks and GUI windows through `show(interactive=True)`, as described in the [Interactive Figures](https://eriknovak.github.io/datachart/0.10.0/how-to-guides/utility/interactive/index.md) guide. For charts that zoom and hover inside a web page, use a browser-native library such as [d3](https://d3js.org/), [Plotly](https://plotly.com/javascript/), [Vega](https://vega.github.io/vega/), or [Bokeh](https://bokeh.org/).

## Real-World Examples

The examples below put the arguments above to work on the three destinations a figure most often has. Each one names its destination, the constraint it imposes, and the call that meets it.

### Example 1: The Figure Set of a Manuscript (A Stem per Figure, Two Formats, One Size)

A journal wants every figure twice: as a PDF the typesetter places in the article, and as a PNG the submission portal shows to reviewers. The figures must share one width so their fonts print at the same size, and their files must be named after the figure they are. One loop over a dictionary of figures handles all of it: the figure size is fixed once, the stem is the figure's name, and the list of formats writes both files per figure. The returned paths make the file list for the cover letter.

```
from pathlib import Path

from datachart.charts import BarChart, LineChart, ScatterChart
from datachart.constants import FIG_FORMAT, FIG_SIZE
from datachart.utils import save_figure

# one figure per panel of the paper, at the journal's single-column width
figures = {
    "fig1_growth": LineChart(data=growth, xlabel="Day", ylabel="Cells (×10⁶)", figsize=FIG_SIZE.HALF_MEDIUM),
    "fig2_dose": ScatterChart(data=dose_response, xlabel="Dose (mg)", ylabel="Response", figsize=FIG_SIZE.HALF_MEDIUM),
    "fig3_groups": BarChart(data=group_means, xlabel="Group", ylabel="Mean", show_yerr=True, figsize=FIG_SIZE.HALF_MEDIUM),
}

out = Path("manuscript/figures")
out.mkdir(parents=True, exist_ok=True)

written = []
for name, figure in figures.items():
    written += save_figure(figure, str(out / name), format=[FIG_FORMAT.PDF, FIG_FORMAT.PNG], dpi=600)

written
# ["manuscript/figures/fig1_growth.pdf", "manuscript/figures/fig1_growth.png", ...]
```

The `dpi` applies to the PNG alone, so the vector PDF costs nothing extra, and 600 dots per inch keeps the PNG sharp when a reviewer zooms into it.

### Example 2: A Chart on a Slide (A Slide-Sized Figure with a Transparent Background)

A slide deck has a colored background and a wide aspect ratio, and a figure that ignores either looks pasted on: a white box, or a chart that fills half the slide with a font too small to read from the back of the room. Draw the figure at the slide's own size with [FIG_SIZE.SLIDE_16_9](https://eriknovak.github.io/datachart/0.10.0/references/constants/#datachart.constants.FIG_SIZE), so its fonts are sized for a slide, and save it with a transparent background so the slide's color shows through. PNG is the safe format for presentation software; `dpi=200` is plenty for a projector.

```
from datachart.charts import BarChart
from datachart.constants import FIG_SIZE
from datachart.utils import save_figure

figure = BarChart(
    data=quarterly_revenue,
    title="Revenue by quarter",
    ylabel="Revenue (M€)",
    show_values=True,
    figsize=FIG_SIZE.SLIDE_16_9,
)
save_figure(figure, "deck/revenue.png", dpi=200, transparent=True)
```

Insert the PNG at full slide width and it lands pixel for pixel, with no resizing and no white frame. For a deck that will also be printed as a handout, add `FIG_FORMAT.PDF` to a `format` list in the same call.

### Example 3: A Chart on a Documentation Page (SVG, Transparent, in an Image Tag)

A documentation site is read on phones and high-density laptop screens, in light and dark mode. The one export that serves all of them is a transparent SVG: it stays sharp at any density, scales with the page layout, and shows the page's own background in either color scheme. Draw the figure at the page's content width, save it next to the page, and reference it from an image tag with an `alt` text that says what the chart shows, so the page reads without it too.

```
from datachart.charts import LineChart
from datachart.constants import FIG_SIZE
from datachart.utils import save_figure

figure = LineChart(
    data=latency_by_release,
    subtitle=["p50", "p99"],
    xlabel="Release",
    ylabel="Latency (ms)",
    show_legend=True,
    figsize=FIG_SIZE.FULL_SHORT,
)
save_figure(figure, "docs/assets/latency.svg", transparent=True)
```

```
<img src="assets/latency.svg" alt="Median and tail latency per release; the tail halves after release 2.3" width="100%">
```

If the site's dark mode turns the page black, the theme's dark text disappears with it; either pick a theme with a mid-grey text color for the docs figures or export a second SVG under a dark theme and switch between the two with a `<picture>` element and a `prefers-color-scheme` media query.
