"""The public composition vocabulary (ADR 0002).

Two constructors mirror the internal drawing seam: `Panel` overlays rendered
figures into one coordinate space, `Grid` arranges them in rows and columns.

Methods:
    Panel(charts, title, xlabel, ylabel_left, ylabel_right, figsize, show_legend, ...):
        Overlays rendered chart figures on a single plot with optional dual y-axes.
    Grid(charts, title, max_cols, figsize, sharex, sharey):
        Arranges rendered chart figures in a grid; nested rows define the layout.

"""

import math
from typing import List, Dict, Optional, Tuple, Union, Any

import matplotlib.pyplot as plt

from ..constants import FIG_SIZE
from .overlay import _overlay_impl
from .figure import _grid_from_dicts, _figure_grid_layout_impl


def Panel(
    charts: List[Union[plt.Figure, Dict[str, Any]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel_left: Optional[str] = None,
    ylabel_right: Optional[str] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    show_legend: Optional[bool] = False,
    show_grid: Optional[str] = None,
    auto_secondary_axis: Optional[float] = None,
    xmin: Optional[float] = None,
    xmax: Optional[float] = None,
    ymin: Optional[float] = None,
    ymax: Optional[float] = None,
    ymin_right: Optional[float] = None,
    ymax_right: Optional[float] = None,
    bar_mode: Optional[str] = None,
) -> plt.Figure:
    """Overlay rendered chart figures in one coordinate space.

    Combines different chart types (LineChart, BarChart, ScatterChart, Histogram)
    on a single plot, drawn in the order provided. Multiple y-axes (left and
    right) are supported for handling different scales.

    Panel figures nest: ``Panel([Panel([f1, f2]), f3])`` is equivalent to
    ``Panel([f1, f2, f3])``, to any depth. A nested panel contributes its
    figures with their per-figure options intact, while panel-level settings
    (title, labels, limits, ...) always come from the outermost call. Dict
    options on a nested panel override its per-figure options only when
    explicitly given.

    Examples:
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

    Args:
        charts: The figures to overlay. Each item is either a bare matplotlib
            Figure created by a datachart chart function — including another
            Panel figure, which flattens into this one — or a dict with a
            "figure" key plus optional per-figure options:
            - "y_axis": "left", "right", or "auto" (chart figures default to
              "auto"; a nested panel's figures keep their own assignment)
            - "z_order": Integer for layering control (higher values on top)
            - "legend_label": Custom legend label (overrides chart subtitle)
        title: Title for the combined chart.
        xlabel: Label for x-axis.
        ylabel_left: Label for left y-axis.
        ylabel_right: Label for right y-axis (if using dual axes).
        figsize: Size of the figure (width, height) in inches.
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show ("x", "y", "both", or None).
        auto_secondary_axis: Threshold ratio for automatic secondary axis creation.
            Default is taken from config (overlay_auto_threshold, default 3.0).
        xmin: Minimum value for x-axis limits.
        xmax: Maximum value for x-axis limits.
        ymin: Minimum value for y-axis limits (applies to left y-axis).
        ymax: Maximum value for y-axis limits (applies to left y-axis).
        ymin_right: Minimum value for right y-axis limits.
        ymax_right: Maximum value for right y-axis limits.
        bar_mode: Bar chart overlay mode: "group" (side-by-side), "stack"
            (stacked), or "overlay" (overlapping). Default is taken from config
            (overlay_bar_mode, default "group").

    Returns:
        A matplotlib Figure containing the overlaid charts.

    Raises:
        ValueError: If charts is empty, an item is not a figure or a valid dict,
            or a figure cannot be overlaid (missing metadata, Grid figure).
    """
    items = []
    for i, item in enumerate(charts):
        if isinstance(item, plt.Figure):
            items.append({"figure": item})
        elif isinstance(item, dict):
            if "figure" not in item:
                raise ValueError(f"Chart at index {i} is missing 'figure' key")
            items.append(item)
        else:
            raise ValueError(f"Item at index {i} is not a matplotlib Figure or a dict")

    return _overlay_impl(
        items,
        title=title,
        xlabel=xlabel,
        ylabel_left=ylabel_left,
        ylabel_right=ylabel_right,
        figsize=figsize,
        show_legend=show_legend,
        show_grid=show_grid,
        auto_secondary_axis=auto_secondary_axis,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        ymin_right=ymin_right,
        ymax_right=ymax_right,
        bar_mode=bar_mode,
    )


def _grid_from_rows(
    rows: List[List[Optional[plt.Figure]]],
    *,
    title: Optional[str],
    figsize: Optional[Tuple[float, float]],
    sharex: bool,
    sharey: bool,
) -> plt.Figure:
    """Turn nested rows into layout specs: colspans via the LCM of row lengths."""
    widths = []
    for r, row in enumerate(rows):
        if len(row) == 0:
            raise ValueError(f"Row {r} is empty")
        widths.append(len(row))
    total = math.lcm(*widths)

    figures = []
    specs = []
    for r, row in enumerate(rows):
        span = total // len(row)
        for c, cell in enumerate(row):
            if cell is None:
                continue
            if not isinstance(cell, plt.Figure):
                raise ValueError(
                    f"Cell ({r}, {c}) is not a matplotlib Figure: in nested rows "
                    "the layout comes from position; use the flat form with "
                    "'layout_spec' dicts for custom placement"
                )
            figures.append(cell)
            specs.append({"row": r, "col": c * span, "rowspan": 1, "colspan": span})

    if not figures:
        raise ValueError("At least one chart is required")

    # scale by visual columns, not the LCM grid width
    if figsize is None:
        base = figures[0].get_size_inches()
        figsize = (base[0] * max(widths), base[1] * len(rows))

    return _figure_grid_layout_impl(
        figures=figures,
        title=title,
        layout_specs=specs,
        figsize=figsize,
        sharex=sharex,
        sharey=sharey,
    )


def Grid(
    charts: Union[
        List[Union[plt.Figure, Dict[str, Any]]],
        List[List[Optional[plt.Figure]]],
    ],
    *,
    title: Optional[str] = None,
    max_cols: int = 4,
    figsize: Optional[Tuple[float, float]] = None,
    sharex: bool = False,
    sharey: bool = False,
) -> plt.Figure:
    """Arrange rendered chart figures in a grid.

    Each figure's chart is redrawn into its grid cell. Nested rows define the
    layout directly: every inner list is one grid row, and a shorter row's
    cells stretch to fill the width. A flat list uses an automatic uniform
    grid governed by `max_cols`, with a `layout_spec` escape hatch for
    irregular grids (rowspans).

    Grids nest: a Grid figure placed in a cell occupies exactly that cell and
    rebuilds its internal layout inside it, to any depth. The nested grid
    keeps its own title (a heading spanning its subgrid) and its own
    sharex/sharey among its own cells; the outer grid's sharex/sharey applies
    only to its top-level cells. Panel figures also nest in a cell; the
    reverse — a Grid figure inside a Panel — stays an error.

    Examples:
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

    Args:
        charts: Either nested rows — each inner list is one grid row of bare
            matplotlib Figures (or None for a blank cell) — or a flat list
            whose items are bare figures or dicts with a "figure" key and an
            optional "layout_spec" dict ('row', 'col', 'rowspan', 'colspan').
            Nested rows and layout_spec cannot be mixed.
        title: Optional title for the combined figure.
        max_cols: Maximum number of columns for the flat-list automatic grid.
        figsize: Size of the combined figure (width, height) in inches.
            If None, calculated from the first figure's size.
        sharex: Whether to share the x-axis across all subplots.
        sharey: Whether to share the y-axis across all subplots.

    Returns:
        A new matplotlib Figure containing all charts in a grid layout.

    Raises:
        ValueError: If charts is empty, rows are mixed with flat items, a cell
            is invalid, or a figure cannot be composed (missing metadata).
    """
    if not charts:
        raise ValueError("At least one chart is required")

    if any(isinstance(item, (list, tuple)) for item in charts):
        if not all(isinstance(item, (list, tuple)) for item in charts):
            raise ValueError(
                "Grid items cannot mix nested rows with flat entries: "
                "use all nested rows or a flat list"
            )
        return _grid_from_rows(
            list(map(list, charts)),
            title=title,
            figsize=figsize,
            sharex=sharex,
            sharey=sharey,
        )

    items = []
    for i, item in enumerate(charts):
        if isinstance(item, plt.Figure):
            items.append({"figure": item})
        elif isinstance(item, dict):
            items.append(item)
        else:
            raise ValueError(f"Item at index {i} is not a matplotlib Figure or a dict")

    return _grid_from_dicts(
        items,
        title=title,
        max_cols=max_cols,
        figsize=figsize,
        sharex=sharex,
        sharey=sharey,
    )
