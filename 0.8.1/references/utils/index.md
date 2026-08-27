# Utils Module

## datachart.utils

The module containing the `utils`.

The `utils` module provides a set of public utilities for the package.

This module exports only the public API intended for end users. Internal implementation details are located in the `_internal` submodule and should not be imported directly by external code.

| MODULE  | DESCRIPTION                                                                 |
| ------- | --------------------------------------------------------------------------- |
| `stats` | The module containing the statistics functions (count, mean, median, etc.). |

| FUNCTION      | DESCRIPTION                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| `save_figure` | Saves the figure into a file using the provided format parameters.          |
| `Panel`       | Overlays rendered chart figures on a single plot with optional dual y-axes. |
| `Grid`        | Arranges rendered chart figures in a grid; nested rows define the layout.   |
| `Annotate`    | Returns a new figure with text annotations added to a rendered figure.      |

## Functions

### datachart.utils.save_figure

```
save_figure(
    figure: plt.Figure,
    path: str,
    dpi: int = 300,
    format: FIG_FORMAT = None,
    transparent: bool = False,
) -> None
```

Save the figure to a file.

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

| PARAMETER     | DESCRIPTION                                                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `figure`      | The figure to save. **TYPE:** `plt.Figure`                                                                                           |
| `path`        | The path where the figure is saved. **TYPE:** `str`                                                                                  |
| `dpi`         | The DPI of the figure. **TYPE:** `int` **DEFAULT:** `300`                                                                            |
| `format`      | The format of the figure. If None, the format will be determined from the file extension. **TYPE:** `FIG_FORMAT` **DEFAULT:** `None` |
| `transparent` | Whether to make the background transparent. **TYPE:** `bool` **DEFAULT:** `False`                                                    |

### datachart.utils.Panel

```
Panel(
    charts: List[Union[plt.Figure, Dict[str, Any]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel_left: Optional[str] = None,
    ylabel_right: Optional[str] = None,
    figsize: Optional[
        Union[FIG_SIZE, Tuple[float, float]]
    ] = None,
    show_legend: Optional[bool] = False,
    show_grid: Optional[str] = None,
    auto_secondary_axis: Optional[float] = None,
    xmin: Optional[float] = None,
    xmax: Optional[float] = None,
    ymin: Optional[float] = None,
    ymax: Optional[float] = None,
    ymin_right: Optional[float] = None,
    ymax_right: Optional[float] = None,
    bar_mode: Optional[Union[BAR_MODE, str]] = None
) -> plt.Figure
```

Overlay rendered chart figures in one coordinate space.

Combines different chart types (LineChart, BarChart, ScatterChart, Histogram, BoxPlot, SwarmPlot) on a single plot, drawn in the order provided. Two value axes (primary and secondary) are supported for handling different scales.

A panel has an orientation, inferred from its figures: it is horizontal when every bar chart and histogram in it is horizontal, vertical otherwise. Mixing the two orientations raises `ValueError`. The *value axis* carries the quantities — y in a vertical panel, x in a horizontal one — and the *category axis* is the other. The parameters keep their spelling but address the axis by role: `ylabel_left`/`ylabel_right`, `ymin`/`ymax` and `ymin_right`/`ymax_right` set the primary/secondary value axis, `xlabel` and `xmin`/`xmax` the category axis. In a horizontal panel the secondary value axis sits at the top, so `"y_axis": "left"` means the bottom axis and `"right"` the top one, and the legend suffixes become `(B)`/`(T)`. Line and scatter figures follow the panel: in a horizontal panel their `x` runs along the category axis and their `y` along the value axis, so the same `LineChart` overlays vertical and horizontal bars.

Panel figures nest: `Panel([Panel([f1, f2]), f3])` is equivalent to `Panel([f1, f2, f3])`, to any depth. A nested panel contributes its figures with their per-figure options intact, while panel-level settings (title, labels, limits, ...) always come from the outermost call. Dict options on a nested panel override its per-figure options only when explicitly given.

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

| PARAMETER             | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `charts`              | The figures to overlay. Each item is either a bare matplotlib Figure created by a datachart chart function — including another Panel figure, which flattens into this one — or a dict with a "figure" key plus optional per-figure options: - "y_axis": "left", "right", or "auto" (chart figures default to "auto"; a nested panel's figures keep their own assignment). "left"/"right" name the primary/secondary value axis — the bottom/top axis in a horizontal panel - "z_order": Integer for layering control (higher values on top) - "legend_label": Custom legend label (overrides chart subtitle) - "emphasis": "background" or "highlight" role for every layer of this figure. Background layers are muted (theme muted color, lowered alpha, behind the others) and excluded from the legend; highlight layers are bolded and brought to the front among the data layers. A nested panel's figures keep their own roles. **TYPE:** `List[Union[plt.Figure, Dict[str, Any]]]` |
| `title`               | Title for the combined chart. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `xlabel`              | Label for the category axis. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `ylabel_left`         | Label for the primary value axis. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `ylabel_right`        | Label for the secondary value axis (if using dual axes). **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `figsize`             | Size of the figure (width, height) in inches. **TYPE:** `Optional[Union[FIG_SIZE, Tuple[float, float]]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `show_legend`         | Whether to show the legend. **TYPE:** `Optional[bool]` **DEFAULT:** `False`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `show_grid`           | Which grid lines to show ("x", "y", "both", or None); these name the matplotlib axes literally. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `auto_secondary_axis` | Threshold ratio for automatic secondary axis creation. Default is taken from config (overlay_auto_threshold, default 3.0). **TYPE:** `Optional[float]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `xmin`                | Minimum value for the category-axis limits. **TYPE:** `Optional[float]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `xmax`                | Maximum value for the category-axis limits. **TYPE:** `Optional[float]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `ymin`                | Minimum value for the primary value-axis limits. **TYPE:** `Optional[float]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymax`                | Maximum value for the primary value-axis limits. **TYPE:** `Optional[float]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `ymin_right`          | Minimum value for the secondary value-axis limits. **TYPE:** `Optional[float]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `ymax_right`          | Maximum value for the secondary value-axis limits. **TYPE:** `Optional[float]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `bar_mode`            | How bar and histogram series share the axis: "group" (side-by-side bars; histograms overlay), "stack" (stacked), or "overlay" (overlapping). Default is taken from config (overlay_bar_mode, default "group"). See BAR_MODE. **TYPE:** `Optional[Union[BAR_MODE, str]]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

| RETURNS      | DESCRIPTION                                         |
| ------------ | --------------------------------------------------- |
| `plt.Figure` | A matplotlib Figure containing the overlaid charts. |

| RAISES       | DESCRIPTION                                                                                                                                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If charts is empty, an item is not a figure or a valid dict, a figure cannot be overlaid (missing metadata, Grid figure), or the figures mix horizontal and vertical orientations. |

### datachart.utils.Grid

```
Grid(
    charts: Union[
        List[Union[plt.Figure, Dict[str, Any]]],
        List[List[Optional[plt.Figure]]],
    ],
    *,
    title: Optional[str] = None,
    max_cols: int = 4,
    figsize: Optional[Tuple[float, float]] = None,
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

| PARAMETER  | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `charts`   | Either nested rows — each inner list is one grid row of bare matplotlib Figures (or None for a blank cell) — or a flat list whose items are bare figures or dicts with a "figure" key and an optional "layout_spec" dict ('row', 'col', 'rowspan', 'colspan'). Nested rows and layout_spec cannot be mixed. **TYPE:** `Union[List[Union[plt.Figure, Dict[str, Any]]], List[List[Optional[plt.Figure]]]]` |
| `title`    | Optional title for the combined figure. **TYPE:** `Optional[str]` **DEFAULT:** `None`                                                                                                                                                                                                                                                                                                                    |
| `max_cols` | Maximum number of columns for the flat-list automatic grid. **TYPE:** `int` **DEFAULT:** `4`                                                                                                                                                                                                                                                                                                             |
| `figsize`  | Size of the combined figure (width, height) in inches. If None, calculated from the first figure's size. **TYPE:** `Optional[Tuple[float, float]]` **DEFAULT:** `None`                                                                                                                                                                                                                                   |
| `sharex`   | Whether to share the x-axis across all subplots. **TYPE:** `bool` **DEFAULT:** `False`                                                                                                                                                                                                                                                                                                                   |
| `sharey`   | Whether to share the y-axis across all subplots. **TYPE:** `bool` **DEFAULT:** `False`                                                                                                                                                                                                                                                                                                                   |

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
    texts: Union[TextAttrs, List[TextAttrs]],
) -> plt.Figure
```

Add text annotations to an already rendered figure.

Returns a new figure with the annotations riding the figure's chart metadata, styled by the current theme at call time — so they follow themes and survive `Panel` and `Grid` composition. The source figure and its charts are never modified.

Works on any figure whose charts share one coordinate space: chart figures (including polar ones) and `Panel` output. Grid figures and multi-subplot figures (`subplots=True`) are rejected — annotate the sources before composing.

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
```

| PARAMETER | DESCRIPTION                                                                                                                                                                                                                                                                        |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `figure`  | A figure created by a datachart chart function or Panel. **TYPE:** `plt.Figure`                                                                                                                                                                                                    |
| `texts`   | The text annotation(s) to add. Each annotation places text at (x, y) — data coordinates by default, axes fractions with "coords": "axes" — draws a connector to the optional target data point, and takes a per-text style override. **TYPE:** `Union[TextAttrs, List[TextAttrs]]` |

| RETURNS      | DESCRIPTION                                         |
| ------------ | --------------------------------------------------- |
| `plt.Figure` | A new matplotlib Figure with the annotations added. |

| RAISES       | DESCRIPTION                                                                          |
| ------------ | ------------------------------------------------------------------------------------ |
| `ValueError` | If the figure has no chart metadata, is a Grid figure, or is a multi-subplot figure. |
