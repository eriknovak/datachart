<p align="center">
  <img src="https://raw.githubusercontent.com/eriknovak/datachart/main/docs/assets/imgs/logo.png" alt="logo" height="200" style="height:200px">
</p>

<p align="center">
  <i>Data visualization package, simple to use, highly customizable</i>
</p>

<p align="center">
  <a href="https://github.com/eriknovak/datachart/actions/workflows/unittests.yaml" target="_blank"><img
    src="https://github.com/eriknovak/datachart/actions/workflows/unittests.yaml/badge.svg" alt="Test"
  /></a>
  <a href="https://pypi.org/project/datachart" target="_blank"><img
    src="https://img.shields.io/pypi/v/datachart?color=%2334D058" alt="Package Package Index"
  /></a>
  <a href="https://pypi.org/project/datachart" target="_blank"><img
    src="https://img.shields.io/pypi/pyversions/datachart.svg?color=%2334D058" alt="Supported Python Versions"
  /></a>
  <a href="https://github.com/eriknovak/datachart/blob/main/LICENSE" target="_blank"><img
    src="https://img.shields.io/github/license/eriknovak/datachart?color=%2334D058" alt="License"
  /></a>
  <a href="https://github.com/eriknovak/datachart/blob/main/CHANGELOG.md" target="_blank"><img
    src="https://img.shields.io/badge/changelog-latest-%2334D058" alt="Changelog"
  /></a>
</p>

<p align="center">
  <a href="https://eriknovak.github.io/datachart"><b>Documentation</b></a> ·
  <a href="https://eriknovak.github.io/datachart/latest/how-to-guides/"><b>How-to Guides</b></a> ·
  <a href="https://eriknovak.github.io/datachart/latest/references/"><b>API Reference</b></a> ·
  <a href="https://github.com/eriknovak/datachart"><b>Source</b></a>
</p>

---

The datachart package is a python package for creating data visualizations, built on top of [matplotlib](https://matplotlib.org/). It is designed to be simple to use and highly customizable, i.e. it is easy to change the look and feel of the charts.

**Features:**

- **Charts.** Chart types for trends, comparisons, distributions, relationships, and flows — each created with a single function call from plain lists of dicts. See [Charts](#charts).
- **Composition.** Combine rendered charts with `Panel` (overlay charts on a single plot, with optional dual y-axes) and `Grid` (arrange charts in a grid; grids nest). See [Composition](#composition).
- **Themes & configuration.** Predefined themes, each named for its visual trait, plus a global `config` for tweaking any style attribute — per-chart `style` overrides included. See [Themes](#themes).

## Quick start

```bash
pip install datachart   # or: uv add datachart
```

Every chart takes a list of series, each a list of dicts. Set a theme once and every chart follows it:

```python
from datachart.charts import LineChart
from datachart.config import config
from datachart.constants import THEME
from datachart.utils import save_figure

config.set_theme(THEME.INK)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
signups = [420, 465, 430, 510, 560, 545, 610]
churned = [380, 400, 440, 435, 480, 520, 550]

figure = LineChart(
    [
        [{"x": x, "y": y} for x, y in enumerate(signups)],
        [{"x": x, "y": y} for x, y in enumerate(churned)],
    ],
    title="Monthly signups vs. churn",
    subtitle=["Signups", "Churned"],
    xlabel="Month",
    ylabel="Users",
    xticks=list(range(len(months))),
    xticklabels=months,
    show_legend=True,
)
save_figure(figure, "line.png")
```

<p align="center">
  <img src="https://raw.githubusercontent.com/eriknovak/datachart/main/docs/assets/imgs/example-quickstart.png" alt="Quick start line chart" width="560" />
</p>

`figure` is a plain matplotlib `Figure`, so anything matplotlib can do with it still works.

## Charts

Every chart is a single function call taking plain lists of dicts, and every
function accepts a list of series to overlay or a `subplots=True` flag to
split them apart. The dict keys per chart are listed in each guide.

| Family            | Charts                                                                     | Use for                                                                |
| ----------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Trends**        | [LineChart], [StackedAreaChart]                                            | values over an ordered axis; area for part-of-whole over time          |
| **Comparisons**   | [BarChart], [PyramidChart], [RadialChart]                                  | category totals, paired populations, cyclic/periodic values            |
| **Distributions** | [Histogram], [BoxPlot], [ViolinPlot], [SwarmPlot], [RaincloudPlot]         | shape and spread of one variable, per group                            |
| **Relationships** | [ScatterChart], [Heatmap], [ContourChart], [HexbinChart], [ParallelCoords] | two-variable correlation, matrices, dense 2-D density, many dimensions |
| **Flows**         | [SankeyChart]                                                              | quantities moving between stages                                       |

## Composition

Rendered figures compose. [`Grid`][grid-guide] arranges them in a grid (nested lists define rows; grids nest), and [`Panel`][panel-guide] overlays charts on one plot, with an optional secondary y-axis. Four chart types, one theme, one grid — with a `Panel` in the last cell:

```python
import numpy as np

from datachart.charts import BarChart, Histogram, LineChart, ScatterChart
from datachart.config import config
from datachart.constants import LEGEND_LOCATION, THEME
from datachart.utils import Grid, Panel, save_figure

config.set_theme(THEME.INK)
rng = np.random.default_rng(0)

line = LineChart(
    [[{"x": x, "y": 50 + a * np.sin(x / 3) + x} for x in range(21)] for a in (20, 12, 5)],
    title="Line", subtitle=["Run 1", "Run 2", "Run 3"], show_legend=True,
)
bars = BarChart(
    [[{"label": f"Bench {b}", "y": y} for b, y in zip("ABCD", ys)]
     for ys in ([66, 59, 77, 83], [65, 58, 78, 82])],
    title="Grouped bar", subtitle=["Model A", "Model B"], show_legend=True,
)
scatter = ScatterChart(
    [[{"x": x, "y": y} for x, y in zip(rng.normal(cx, 1.2, 60), rng.normal(cy, 1, 60))]
     for cx, cy in ((3, 4), (7, 7), (10, 3))],
    title="Scatter", subtitle=["C1", "C2", "C3"], show_legend=True,
)

# Panel overlays figures on one axes; the line gets its own y-axis on the right
samples = np.sort(rng.normal(55, 12, 500))
hist = Histogram([{"x": x} for x in samples], subtitle="Count")
cdf = LineChart(
    [{"x": x, "y": 100 * i / len(samples)} for i, x in enumerate(samples, 1)],
    subtitle="Cumulative %",
)
config.update_config({"plot_legend_location": LEGEND_LOCATION.UPPER_LEFT})
overlay = Panel(
    [hist, cdf], title="Histogram + line", ylabel_right="%",
    auto_secondary_axis=1, show_legend=True,
)

# Grid arranges figures in cells; nested lists define the rows
figure = Grid([[line, bars], [scatter, overlay]], title="INK theme")
save_figure(figure, "grid.png")
```

<p align="center">
  <img src="https://raw.githubusercontent.com/eriknovak/datachart/main/docs/assets/imgs/example-ink.png" alt="Line, grouped bar, scatter, and a histogram+line panel in a 2x2 grid, INK theme" width="720" />
</p>

## Themes

Predefined themes, applied with `config.set_theme(THEME.<NAME>)`. Any attribute can then be tweaked globally via `config.update_config(...)` or per chart via the `style` argument — see the [themes][themes-guide], [config][config-guide], and [theme gallery][gallery-guide] guides.

<p align="center">
  <img src="https://raw.githubusercontent.com/eriknovak/datachart/main/docs/assets/imgs/example-themes.png" alt="The same grouped bar chart across the predefined themes" width="720" />
</p>

More examples on how to use the `datachart` package are available
on the official [How-to Guides](https://eriknovak.github.io/datachart/latest/how-to-guides/).

## Install

Requires [python] 3.10 or higher.

```bash
pip install -U datachart
```

With [uv]:

```bash
uv add datachart
```

## Using with LLMs

The documentation is available in LLM-friendly formats:

- [llms.txt](https://eriknovak.github.io/datachart/latest/llms.txt) — index of the documentation with descriptions
- [llms-full.txt](https://eriknovak.github.io/datachart/latest/llms-full.txt) — full documentation in a single file
- Every documentation page is also available as plain markdown by appending `index.md` to its URL, e.g. [how-to-guides/charts/linechart/index.md](https://eriknovak.github.io/datachart/latest/how-to-guides/charts/linechart/index.md)

You can also connect your AI assistant directly:

- [Context7](https://context7.com/eriknovak/datachart) — up-to-date, version-aware docs for AI coding assistants
- [GitMCP](https://gitmcp.io/eriknovak/datachart) — an MCP server serving this repository's documentation

## Contributing

Bug reports, feature requests, and pull requests are welcome — open an
[issue](https://github.com/eriknovak/datachart/issues) to report a problem or
propose a chart, theme, or option you are missing.

To work on the package locally:

```bash
git clone https://github.com/eriknovak/datachart.git
cd datachart
uv sync --group dev                  # package + dev dependencies
python -m unittest discover test     # unit tests
pytest                               # documentation notebooks
mkdocs serve                         # docs at http://127.0.0.1:8000
```

Code is formatted with `black`; the pre-commit hook runs it for you.

[python]: https://www.python.org/
[uv]: https://docs.astral.sh/uv/
[LineChart]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/linechart/
[StackedAreaChart]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/stackedareachart/
[BarChart]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/barchart/
[PyramidChart]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/pyramidchart/
[RadialChart]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/radialchart/
[Histogram]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/histogram/
[BoxPlot]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/boxplot/
[ViolinPlot]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/violinplot/
[SwarmPlot]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/swarmplot/
[RaincloudPlot]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/raincloudplot/
[ScatterChart]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/scatterchart/
[Heatmap]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/heatmap/
[ContourChart]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/contourchart/
[HexbinChart]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/hexbinchart/
[ParallelCoords]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/parallelcoords/
[SankeyChart]: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/sankeychart/
[panel-guide]: https://eriknovak.github.io/datachart/latest/how-to-guides/utility/panel/
[grid-guide]: https://eriknovak.github.io/datachart/latest/how-to-guides/utility/grid/
[themes-guide]: https://eriknovak.github.io/datachart/latest/how-to-guides/styling/themes/
[config-guide]: https://eriknovak.github.io/datachart/latest/how-to-guides/styling/config/
[gallery-guide]: https://eriknovak.github.io/datachart/latest/how-to-guides/styling/theme-gallery/
