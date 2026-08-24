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
</p>


---

**Documentation:** [https://eriknovak.github.io/datachart](https://eriknovak.github.io/datachart)

**Source code:** [https://github.com/eriknovak/datachart](https://github.com/eriknovak/datachart)

---

The datachart package is a python package for creating data visualizations, built on top of [matplotlib](https://matplotlib.org/). It is designed to be simple to use and highly customizable, i.e. it is easy to change the look and feel of the charts.

**Features:**

- **Charts.** Bar charts, line charts, scatter charts, histograms, heatmaps, box plots, pyramid charts, radial charts, and parallel coordinates — each created with a single function call from plain lists of dicts.
- **Composition.** Combine rendered charts with `Panel` (overlay charts on a single plot, with optional dual y-axes) and `Grid` (arrange charts in a grid; grids nest).
- **Themes & configuration.** Six predefined themes, each named for its visual trait, plus a global `config` for tweaking any style attribute — per-chart `style` overrides included.

## Requirements
Before starting the project make sure these requirements are available:

- [python]. The python programming language (v3.10 or higher).

## Install

```bash
pip install datachart
```

## Upgrade

```bash
pip install datachart --upgrade
```

## Example

Set a theme once and every chart follows it. The example below uses the `INK` theme:

```python
from datachart.charts import LineChart
from datachart.config import config
from datachart.constants import THEME

config.set_theme(THEME.INK)

figure = LineChart(
    [
        [{"x": x, "y": y} for x, y in enumerate([40, 45, 43, 50, 56, 54, 61])],
        [{"x": x, "y": y} for x, y in enumerate([38, 40, 44, 43, 48, 52, 55])],
    ],
    title="Line",
    subtitle=["Run 1", "Run 2"],
    show_legend=True,
)
```

The same theme, across chart types and composed with `Grid`:

<p align="center">
  <img src="https://raw.githubusercontent.com/eriknovak/datachart/main/docs/assets/imgs/example-ink.png" alt="INK theme example charts" width="720" />
</p>

More examples on how to use the `datachart` package are available
on the official [How-to Guides](https://eriknovak.github.io/datachart/how-to-guides/).

## Using with LLMs

The documentation is available in LLM-friendly formats:

- [llms.txt](https://eriknovak.github.io/datachart/llms.txt) — index of the documentation with descriptions
- [llms-full.txt](https://eriknovak.github.io/datachart/llms-full.txt) — full documentation in a single file
- Every documentation page is also available as plain markdown by appending `index.md` to its URL, e.g. [how-to-guides/charts/linechart/index.md](https://eriknovak.github.io/datachart/how-to-guides/charts/linechart/index.md)

You can also connect your AI assistant directly:

- [Context7](https://context7.com/eriknovak/datachart) — up-to-date, version-aware docs for AI coding assistants
- [GitMCP](https://gitmcp.io/eriknovak/datachart) — an MCP server serving this repository's documentation

[python]: https://www.python.org/
