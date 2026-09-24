# Utils Module

## datachart.utils

The module containing the `utils`.

The `utils` module provides a set of public utilities for the package: the composition of finished figures (`Panel`, `Grid`, `Annotate`), saving them (`save_figure`), and the statistics behind the charts (`stats`).

This module exports only the public API intended for end users. Internal implementation details are located in the `_internal` submodule and should not be imported directly by external code.

## Choosing a Utility

Everything here takes or returns the figure a chart function returns: three ways to compose finished figures, one to save them, and the statistics behind them.

| I want to…                                                            | Use                                                                                  | Guide                                                                                                    |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| draw several charts in one coordinate space, with a second value axis | [`Panel`](#datachart.utils.Panel)                                                    | [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md)                  |
| lay charts out side by side or in rows                                | [`Grid`](#datachart.utils.Grid)                                                      | [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)                    |
| add notes to a figure that is already drawn                           | [`Annotate`](#datachart.utils.Annotate)                                              | [Text Annotations](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/annotations/index.md) |
| write a figure to disk, in one format or several                      | [`save_figure`](#datachart.utils.save_figure)                                        | [Saving Figures](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/saving/index.md)        |
| compute the number a chart shows                                      | [`stats`](https://eriknovak.github.io/datachart/dev/references/utils/stats/index.md) | [Statistics](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/stats/index.md)             |

## Composition

### datachart.utils.Panel

```
Panel(
    charts: list[plt.Figure | dict[str, Any]],
    *,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel_left: str | None = None,
    ylabel_right: str | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    show_legend: bool | None = False,
    legend: LegendSettingAttrs | None = None,
    show_grid: SHOW_GRID | str | bool | None = None,
    auto_secondary_axis: float | None = None,
    xmin: float | None = None,
    xmax: float | None = None,
    ymin: float | None = None,
    ymax: float | None = None,
    ymin_right: float | None = None,
    ymax_right: float | None = None,
    scalex: AXIS_SCALE | str | None = None,
    scaley: AXIS_SCALE | str | None = None,
    scaley_right: AXIS_SCALE | str | None = None,
    bar_mode: BAR_MODE | str | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None
) -> plt.Figure
```

Overlay rendered chart figures in one coordinate space.

Combines different chart types (LineChart, BarChart, ScatterChart, Histogram, BoxPlot, SwarmPlot) on a single plot, drawn in the order provided. Two value axes (primary and secondary) are supported for handling different scales.

A panel has an orientation, inferred from its figures: it is horizontal when every bar chart and histogram in it is horizontal, vertical otherwise. Mixing the two orientations raises `ValueError`. The *value axis* carries the quantities — y in a vertical panel, x in a horizontal one — and the *category axis* is the other. The parameters keep their spelling but address the axis by role: `ylabel_left`/`ylabel_right`, `ymin`/`ymax`, `ymin_right`/`ymax_right` and `scaley`/`scaley_right` set the primary/secondary value axis, `xlabel`, `xmin`/`xmax` and `scalex` the category axis. In a horizontal panel the secondary value axis sits at the top, so `"y_axis": "left"` means the bottom axis and `"right"` the top one, and the legend suffixes become `(B)`/`(T)`. Line and scatter figures follow the panel: in a horizontal panel their `x` runs along the category axis and their `y` along the value axis, so the same `LineChart` overlays vertical and horizontal bars.

Each axis keeps the scale its figures were built with: a figure drawn with `scaley="log"` stays log in the panel, on whichever value axis it lands. A figure that set no scale takes the one its axis resolves to. The panel's own `scalex`, `scaley` and `scaley_right` override that per axis; where two figures on one axis each set a different scale, the first one wins and the panel warns (`overlay_warn_scale_conflict` in the config). The two value axes scale independently, so linear bars on the primary axis against a log line on the secondary one is one panel.

Panel figures nest: `Panel([Panel([f1, f2]), f3])` is equivalent to `Panel([f1, f2, f3])`, to any depth. A nested panel contributes its figures with their per-figure options, axis scales and `bar_mode` intact, while the other panel-level settings (title, labels, limits, ...) always come from the outermost call. Dict options on a nested panel override its per-figure options only when explicitly given.

Examples:

```
>>> from datachart.charts import LineChart, BarChart
>>> from datachart.utils import Panel
>>>
>>> bar_fig = BarChart(data=[{"label": "A", "y": 100}, {"label": "B", "y": 200}])
>>> line_fig = LineChart(data=[{"x": 0, "y": 5}, {"x": 1, "y": 15}])
>>>
>>> # Bare figures: automatic axis assignment
>>> combined = Panel([bar_fig, line_fig], title="Sales Analysis")
>>>
>>> # Panels nest: add a figure to an existing panel
>>> extended = Panel([combined, line_fig])
>>>
>>> # Dicts carry per-figure options
>>> combined = Panel(
...     [
...         {"figure": bar_fig, "y_axis": "left"},
...         {"figure": line_fig, "y_axis": "right"},
...     ],
...     ylabel_left="Count",
...     ylabel_right="Average",
...     show_legend=True,
... )
>>>
>>> # Each value axis scales on its own: linear bars, a log line
>>> combined = Panel(
...     [
...         {"figure": bar_fig, "y_axis": "left"},
...         {"figure": line_fig, "y_axis": "right"},
...     ],
...     scaley_right="log",
... )
>>>
>>> # Horizontal bars make a horizontal panel: the line runs along the
>>> # categories and "right" is the top value axis
>>> hbar_fig = BarChart(
...     data=[{"label": "A", "y": 100}, {"label": "B", "y": 200}],
...     orientation="horizontal",
... )
>>> combined = Panel(
...     [hbar_fig, {"figure": line_fig, "y_axis": "right"}],
...     xlabel="Category",
...     ylabel_left="Count",
...     ylabel_right="Average",
... )
```

| PARAMETER             | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `charts`              | The figures to overlay. Each item is either a bare matplotlib Figure created by a datachart chart function — including another Panel figure, which flattens into this one — or a dict with a "figure" key plus optional per-figure options: - "y_axis": "left", "right", or "auto" (chart figures default to "auto"; a nested panel's figures keep their own assignment). "left"/"right" name the primary/secondary value axis — the bottom/top axis in a horizontal panel - "z_order": Integer for layering control (higher values on top) - "legend_label": Custom legend label (overrides chart subtitle) - "emphasis": "background" or "highlight" role for every layer of this figure. Background layers are muted (theme muted color, lowered alpha, behind the others) and excluded from the legend; highlight layers are bolded and brought to the front among the data layers. A nested panel's figures keep their own roles. **TYPE:** \`list\[plt.Figure |
| `title`               | Title for the combined chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `xlabel`              | Label for the category axis. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `ylabel_left`         | Label for the primary value axis. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `ylabel_right`        | Label for the secondary value axis (if using dual axes). **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `figsize`             | Size of the figure (width, height) in inches. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `show_legend`         | Whether to show the legend. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `legend`              | The per-figure legend setting: title, location, column count and alignment; each field falls back to the theme. See LegendSettingAttrs. **TYPE:** \`LegendSettingAttrs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `show_grid`           | Which grid lines to show ("x", "y", "both", or None); False draws none. These name the matplotlib axes literally. **TYPE:** \`SHOW_GRID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `auto_secondary_axis` | Threshold ratio for automatic secondary axis creation. Default is taken from config (overlay_auto_threshold, default 3.0). **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `xmin`                | Minimum value for the category-axis limits. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `xmax`                | Maximum value for the category-axis limits. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `ymin`                | Minimum value for the primary value-axis limits. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `ymax`                | Maximum value for the primary value-axis limits. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `ymin_right`          | Minimum value for the secondary value-axis limits. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `ymax_right`          | Maximum value for the secondary value-axis limits. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `scalex`              | The category-axis scale ("linear", "log", "symlog", "asinh"). Default: the scale of the first figure that was built with one. See AXIS_SCALE. **TYPE:** \`AXIS_SCALE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `scaley`              | The primary value-axis scale. Default: the scale of the first figure on that axis that was built with one. **TYPE:** \`AXIS_SCALE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `scaley_right`        | The secondary value-axis scale. Default: the scale of the first figure on that axis that was built with one. Inert on a polar panel, which has no secondary axis. **TYPE:** \`AXIS_SCALE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `bar_mode`            | How bar and histogram series share the axis: "group" (side-by-side bars; histograms overlay), "stack" (stacked), or "overlay" (overlapping). Default: the mode of the first figure that was built with one, then the config (overlay_bar_mode, default "group"). See BAR_MODE. **TYPE:** \`BAR_MODE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `aspect_ratio`        | The aspect ratio of the axes box; "geographic" keeps a map of longitude against latitude at true proportions. Default: "auto". See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

| RETURNS      | DESCRIPTION                                         |
| ------------ | --------------------------------------------------- |
| `plt.Figure` | A matplotlib Figure containing the overlaid charts. |

| RAISES       | DESCRIPTION                                                                                                                                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If charts is empty, an item is not a figure or a valid dict, a figure cannot be overlaid (missing metadata, Grid figure), or the figures mix horizontal and vertical orientations. |

### datachart.utils.Grid

```
Grid(
    charts: (
        list[plt.Figure | dict[str, Any]]
        | list[list[plt.Figure | None]]
    ),
    *,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    max_cols: int = 4,
    figsize: tuple[float, float] | None = None,
    sharex: bool = False,
    sharey: bool = False
) -> plt.Figure
```

Arrange rendered chart figures in a grid.

Each figure's chart is redrawn into its grid cell. Nested rows define the layout directly: every inner list is one grid row, and a shorter row's cells stretch to fill the width. A flat list uses an automatic uniform grid governed by `max_cols`, with a `layout_spec` escape hatch for irregular grids (rowspans).

Grids nest: a Grid figure placed in a cell occupies exactly that cell and rebuilds its internal layout inside it, to any depth. The nested grid keeps its own title (a heading spanning its subgrid) and its own sharex/sharey among its own cells; the outer grid's sharex/sharey applies only to its top-level cells. Panel figures also nest in a cell; the reverse — a Grid figure inside a Panel — stays an error.

Examples:

```
>>> from datachart.charts import LineChart, BarChart, ScatterChart
>>> from datachart.utils import Grid
>>>
>>> fig1 = LineChart(data=[{"x": i, "y": i**2} for i in range(10)], title="Line")
>>> fig2 = BarChart(data=[{"label": "A", "y": 10}, {"label": "B", "y": 20}], title="Bar")
>>> fig3 = ScatterChart(data=[{"x": i, "y": i * 2} for i in range(10)], title="Scatter")
>>>
>>> # Nested rows are the layout: fig1 spans the full top row
>>> combined = Grid([[fig1], [fig2, fig3]], title="Dashboard")
>>>
>>> # None leaves a blank cell
>>> combined = Grid([[fig1, fig2], [fig3, None]])
>>>
>>> # Flat list: automatic uniform grid
>>> combined = Grid([fig1, fig2, fig3], max_cols=2)
>>>
>>> # Grids nest: a grid figure occupies one cell of the outer grid
>>> inner = Grid([[fig1, fig2], [fig3]], title="Inner")
>>> combined = Grid([inner, fig1], title="Outer")
>>>
>>> # Nested rows can hold grid (and Panel) figures too
>>> combined = Grid([[inner, fig1], [fig2]])
>>>
>>> # Flat list with the layout_spec escape hatch (rowspans)
>>> combined = Grid(
...     [
...         {"figure": fig1, "layout_spec": {"row": 0, "col": 0, "rowspan": 2, "colspan": 1}},
...         {"figure": fig2, "layout_spec": {"row": 0, "col": 1, "rowspan": 1, "colspan": 1}},
...         {"figure": fig3, "layout_spec": {"row": 1, "col": 1, "rowspan": 1, "colspan": 1}},
...     ]
... )
```

| PARAMETER  | DESCRIPTION                                                                                                                                                                                                                                                                                                                              |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `charts`   | Either nested rows — each inner list is one grid row of bare matplotlib Figures (or None for a blank cell) — or a flat list whose items are bare figures or dicts with a "figure" key and an optional "layout_spec" dict ('row', 'col', 'rowspan', 'colspan'). Nested rows and layout_spec cannot be mixed. **TYPE:** \`list\[plt.Figure |
| `title`    | Optional title for the combined figure. **TYPE:** \`str                                                                                                                                                                                                                                                                                  |
| `xlabel`   | Optional x-axis label for the whole grid, drawn once below every cell. A nested grid keeps its own as a footer of its cell. **TYPE:** \`str                                                                                                                                                                                              |
| `ylabel`   | Optional y-axis label for the whole grid, drawn once to the left of every cell. A nested grid keeps its own beside its cell. **TYPE:** \`str                                                                                                                                                                                             |
| `max_cols` | Maximum number of columns for the flat-list automatic grid. **TYPE:** `int` **DEFAULT:** `4`                                                                                                                                                                                                                                             |
| `figsize`  | Size of the combined figure (width, height) in inches. If None, calculated from the first figure's size. **TYPE:** \`tuple[float, float]                                                                                                                                                                                                 |
| `sharex`   | Whether to share the x-axis across all subplots. **TYPE:** `bool` **DEFAULT:** `False`                                                                                                                                                                                                                                                   |
| `sharey`   | Whether to share the y-axis across all subplots. **TYPE:** `bool` **DEFAULT:** `False`                                                                                                                                                                                                                                                   |

| RETURNS      | DESCRIPTION                                                     |
| ------------ | --------------------------------------------------------------- |
| `plt.Figure` | A new matplotlib Figure containing all charts in a grid layout. |

| RAISES       | DESCRIPTION                                                                                                               |
| ------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If charts is empty, rows are mixed with flat items, a cell is invalid, or a figure cannot be composed (missing metadata). |

### datachart.utils.Annotate

```
Annotate(
    figure: plt.Figure,
    texts: TextSettingAttrs | list[TextSettingAttrs],
) -> plt.Figure
```

Add text annotations to an already rendered figure.

Returns a new figure with the annotations riding the figure's chart metadata, styled by the current theme at call time — so they follow themes and survive `Panel` and `Grid` composition. The source figure and its charts are never modified.

Works on chart figures (including polar ones), `Panel` output, and multi-subplot figures (`subplots=True`). On a multi-subplot figure every text names its target with a 0-based `subplot` index in render order; the figure is redrawn with the same subplot layout — each subplot scales on its own, without the source's `sharex`/`sharey`, which a `Grid` cell of the result restores — and the texts ride the per-subplot panels only, so they show in `Grid` cells but not in a `Panel` overlay of the figure. Grid figures are rejected — annotate the sources before composing.

Examples:

```
>>> from datachart.charts import LineChart
>>> from datachart.utils import Annotate
>>>
>>> figure = LineChart(data=[{"x": i, "y": i**2} for i in range(10)])
>>> annotated = Annotate(
...     figure,
...     texts={
...         "text": "growth accelerates",
...         "x": 4,
...         "y": 60,
...         "target": (7, 49),
...     },
... )
>>>
>>> # a multi-subplot figure: each text names its subplot
>>> series = [[{"x": i, "y": k * i} for i in range(10)] for k in (1, 2, 3)]
>>> annotated = Annotate(
...     LineChart(data=series, subplots=True),
...     texts={"text": "steepest", "x": 2, "y": 20, "subplot": 2},
... )
```

| PARAMETER | DESCRIPTION                                                                                                                                                                                                                                                                                                                        |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `figure`  | A figure created by a datachart chart function or Panel. **TYPE:** `plt.Figure`                                                                                                                                                                                                                                                    |
| `texts`   | The text annotation(s) to add. Each annotation places text at (x, y) — data coordinates by default, axes fractions with "coords": "axes" — draws a connector to the optional target data point, and takes a per-text style override. On a multi-subplot figure each one also names its subplot index. **TYPE:** \`TextSettingAttrs |

| RETURNS      | DESCRIPTION                                         |
| ------------ | --------------------------------------------------- |
| `plt.Figure` | A new matplotlib Figure with the annotations added. |

| RAISES       | DESCRIPTION                                                                                                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If the figure has no chart metadata or is a Grid figure; if a text names a subplot on a single-panel figure; if, on a multi-subplot figure, a text names no subplot or one out of range. |

## Output

### datachart.utils.save_figure

```
save_figure(
    figure: plt.Figure,
    path: str,
    dpi: int = 300,
    format: FIG_FORMAT | list[FIG_FORMAT] | None = None,
    transparent: bool = False,
) -> list[str]
```

Save the figure to one or more files.

Writes the rendered figure to disk in the format given by `format` or, when omitted, by the file extension. Use a vector format (PDF, SVG) for print and papers, PNG with `dpi` >= 300 for raster deliverables, and `transparent=True` to drop the figure background for slides and web pages. The theme is already baked into the figure, so saving never consults the global config.

Pass a list of formats to write the same figure several times in one call. `path` is then a stem: its extension is dropped when it names a supported format, and one file per format is written next to it. `dpi` and `transparent` apply to every file.

Examples:

```
>>> # 1. create the figure
>>> from datachart.charts import LineChart
>>> figure = LineChart({...})
```

```
>>> # 2. save the figure
>>> from datachart.utils.figure import save_figure
>>> from datachart.constants import FIG_FORMAT
>>> path = "/path/to/save/chart.png"
>>> save_figure(figure, path, dpi=300, format=FIG_FORMAT.PNG, transparent=True)
```

```
>>> # 3. save the same figure as a PDF and a PNG
>>> save_figure(figure, "/path/to/save/chart", format=[FIG_FORMAT.PDF, FIG_FORMAT.PNG])
['/path/to/save/chart.pdf', '/path/to/save/chart.png']
```

| PARAMETER     | DESCRIPTION                                                                                                                                     |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `figure`      | The figure to save. **TYPE:** `plt.Figure`                                                                                                      |
| `path`        | The path where the figure is saved. A stem when format is a list. **TYPE:** `str`                                                               |
| `dpi`         | The DPI of the figure. **TYPE:** `int` **DEFAULT:** `300`                                                                                       |
| `format`      | The format of the figure, or a list of formats to write. If None, the format will be determined from the file extension. **TYPE:** \`FIG_FORMAT |
| `transparent` | Whether to make the background transparent. **TYPE:** `bool` **DEFAULT:** `False`                                                               |

| RETURNS     | DESCRIPTION                                             |
| ----------- | ------------------------------------------------------- |
| `list[str]` | The paths written, in the order the formats were given. |

| RAISES       | DESCRIPTION                 |
| ------------ | --------------------------- |
| `ValueError` | If format is an empty list. |
