"""The public composition vocabulary.

Two constructors mirror the internal drawing seam: `Panel` overlays rendered
figures into one coordinate space, `Grid` arranges them in rows and columns.
`Annotate` adds text annotations to an already rendered figure on the same
seam, so they survive both compositions.

Methods:
    Panel(charts, title, xlabel, ylabel_left, ylabel_right, figsize, show_legend, ...):
        Overlays rendered chart figures on a single plot with optional dual y-axes.
    Grid(charts, title, xlabel, ylabel, max_cols, figsize, sharex, sharey):
        Arranges rendered chart figures in a grid; nested rows define the layout.
    Annotate(figure, texts):
        Returns a new figure with text annotations added to a rendered figure.

"""

import math
import warnings
from typing import List, Dict, Optional, Tuple, Union, Any

import matplotlib.pyplot as plt

from ..config import config
from ..constants import BAR_MODE, FIG_SIZE
from ..typings import TextAttrs
from .figure import _grid_from_dicts, _figure_grid_layout_impl
from ._internal.config_helpers import get_grid_style, get_legend_style, get_text_style
from ._internal.figures import new_figure
from ._internal.layers import (
    Panel as _PanelSeam,
    LayerGroup,
    LineLayer,
    BarLayer,
    ScatterLayer,
    HistogramLayer,
    BoxLayer,
    ViolinLayer,
    ContourLayer,
    ParallelCoordsLayer,
    RadialLayer,
    GroupLayer,
    TextLayer,
)

OVERLAYABLE_LAYERS = (
    LineLayer,
    BarLayer,
    ScatterLayer,
    HistogramLayer,
    BoxLayer,
    ViolinLayer,
    ContourLayer,
    ParallelCoordsLayer,
    RadialLayer,
    GroupLayer,
    TextLayer,
)


def _extract_groups(figure: plt.Figure, index: int) -> List[LayerGroup]:
    """Pull the layer groups out of a figure's metadata transport.

    Args:
        figure: A figure created by a datachart chart function.
        index: The figure's position in the `charts` argument, for error messages.

    Returns:
        The figure's layer groups.

    Raises:
        ValueError: If the figure is missing or has invalid chart metadata.
    """
    if not hasattr(figure, "_chart_metadata"):
        raise ValueError(
            "Figure is missing chart metadata. "
            "This figure was likely not created by a datachart chart function."
        )

    metadata = figure._chart_metadata
    if metadata.get("type") is None:
        raise ValueError("Figure has invalid metadata: missing 'type'")
    if metadata.get("type") == "grid":
        raise ValueError(
            f"Figure at index {index} is a Grid figure; grid figures cannot be overlaid"
        )
    if metadata.get("type") == "pyramidchart":
        # unmirrored data on a mirrored axis would silently mangle (ADR 0017)
        raise ValueError(
            f"Figure at index {index} is a pyramid figure; "
            "pyramid figures cannot be overlaid"
        )
    panel = metadata.get("panel")
    if panel is None:
        raise ValueError("Figure has invalid metadata: missing 'panel'")

    groups = []
    for group in panel.groups:
        supported = [l for l in group.layers if isinstance(l, OVERLAYABLE_LAYERS)]
        if len(supported) < len(group.layers):
            warnings.warn(
                f"Chart at index {index} contains layers of type "
                f"'{metadata.get('type')}' that cannot be overlaid. Skipping them..."
            )
        if supported:
            groups.append(
                LayerGroup(
                    supported,
                    palette=group.palette,
                    max_colors=group.max_colors,
                    num_bins=group.num_bins,
                    y_axis=group.y_axis,
                    z_order=group.z_order,
                    legend_label=group.legend_label,
                    emphasis=group.emphasis,
                )
            )
    return groups


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
    bar_mode: Optional[Union[BAR_MODE, str]] = None,
) -> plt.Figure:
    """Overlay rendered chart figures in one coordinate space.

    Combines different chart types (LineChart, BarChart, ScatterChart,
    Histogram, BoxPlot, SwarmPlot) on a single plot, drawn in the order
    provided. Two value axes (primary and secondary) are supported for
    handling different scales.

    A panel has an orientation, inferred from its figures: it is horizontal
    when every bar chart and histogram in it is horizontal, vertical otherwise.
    Mixing the two orientations raises ``ValueError``. The *value axis* carries
    the quantities — y in a vertical panel, x in a horizontal one — and the
    *category axis* is the other. The parameters keep their spelling but
    address the axis by role: ``ylabel_left``/``ylabel_right``, ``ymin``/``ymax``
    and ``ymin_right``/``ymax_right`` set the primary/secondary value axis,
    ``xlabel`` and ``xmin``/``xmax`` the category axis. In a horizontal panel
    the secondary value axis sits at the top, so ``"y_axis": "left"`` means the
    bottom axis and ``"right"`` the top one, and the legend suffixes become
    ``(B)``/``(T)``. Line and scatter figures follow the panel: in a horizontal
    panel their ``x`` runs along the category axis and their ``y`` along the
    value axis, so the same ``LineChart`` overlays vertical and horizontal bars.

    Panel figures nest: ``Panel([Panel([f1, f2]), f3])`` is equivalent to
    ``Panel([f1, f2, f3])``, to any depth. A nested panel contributes its
    figures with their per-figure options intact, while panel-level settings
    (title, labels, limits, ...) always come from the outermost call. Dict
    options on a nested panel override its per-figure options only when
    explicitly given.

    !!! info "Added in v0.8.0"

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

    Args:
        charts: The figures to overlay. Each item is either a bare matplotlib
            Figure created by a datachart chart function — including another
            Panel figure, which flattens into this one — or a dict with a
            "figure" key plus optional per-figure options:
            - "y_axis": "left", "right", or "auto" (chart figures default to
              "auto"; a nested panel's figures keep their own assignment).
              "left"/"right" name the primary/secondary value axis — the
              bottom/top axis in a horizontal panel
            - "z_order": Integer for layering control (higher values on top)
            - "legend_label": Custom legend label (overrides chart subtitle)
            - "emphasis": "background" or "highlight" role for every layer of
              this figure. Background layers are muted (theme muted color,
              lowered alpha, behind the others) and excluded from the legend;
              highlight layers are bolded and brought to the front among the
              data layers. A nested panel's figures keep their own roles.
        title: Title for the combined chart.
        xlabel: Label for the category axis.
        ylabel_left: Label for the primary value axis.
        ylabel_right: Label for the secondary value axis (if using dual axes).
        figsize: Size of the figure (width, height) in inches.
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show ("x", "y", "both", or None); these
            name the matplotlib axes literally.
        auto_secondary_axis: Threshold ratio for automatic secondary axis creation.
            Default is taken from config (overlay_auto_threshold, default 3.0).
        xmin: Minimum value for the category-axis limits.
        xmax: Maximum value for the category-axis limits.
        ymin: Minimum value for the primary value-axis limits.
        ymax: Maximum value for the primary value-axis limits.
        ymin_right: Minimum value for the secondary value-axis limits.
        ymax_right: Maximum value for the secondary value-axis limits.
        bar_mode: How bar and histogram series share the axis: "group"
            (side-by-side bars; histograms overlay), "stack" (stacked), or
            "overlay" (overlapping). Default is taken from config
            (overlay_bar_mode, default "group"). See `BAR_MODE`.

    Returns:
        A matplotlib Figure containing the overlaid charts.

    Raises:
        ValueError: If charts is empty, an item is not a figure or a valid dict,
            a figure cannot be overlaid (missing metadata, Grid figure), or the
            figures mix horizontal and vertical orientations.
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

    if not items:
        raise ValueError("At least one chart is required")

    if auto_secondary_axis is None:
        auto_secondary_axis = config.get("overlay_auto_threshold", 3.0)
    if bar_mode is None:
        bar_mode = config.get("overlay_bar_mode", "group")
    if show_grid is None:
        show_grid = config.get("chart_default_show_grid")
    if figsize is None:
        figsize = FIG_SIZE.DEFAULT

    # collect the layer groups from every source figure, tagged with prefs
    groups = []
    for i, chart_config in enumerate(items):
        for group in _extract_groups(chart_config["figure"], i):
            # None leaves the group's own pref (from a nested panel) in place
            groups.append(
                group.with_prefs(
                    y_axis=chart_config.get("y_axis", None),
                    z_order=chart_config.get("z_order", None),
                    legend_label=chart_config.get("legend_label", None),
                    emphasis=chart_config.get("emphasis", None),
                )
            )

    # the panel takes literal x/y keys; the orientation (raises on a mix) maps
    # them, and the projection (also raising on a mix) picks the axes kind
    probe = _PanelSeam(groups)
    projection = probe.projection
    if probe.horizontal:
        xlabel, ylabel_left = ylabel_left, xlabel
        xmin, xmax, ymin, ymax = ymin, ymax, xmin, xmax

    # panel-level settings are resolved against the config here, at build time
    panel_settings = {
        "furniture": _PanelSeam.snapshot_furniture(),
        "twin_axes": True,
        "auto_threshold": auto_secondary_axis,
        "warn_scale_groups": config.get("overlay_warn_scale_groups", True),
        "warn_thin_bars": config.get("overlay_warn_thin_bars", True),
        "bar_mode": bar_mode,
        "bar_ticks": "group",
        "bar_width": config.get("plot_bar_width", 0.8),
        "bar_overlay_alpha": config.get("overlay_bar_alpha", 0.7),
        "hist_overlay_alpha": config.get("overlay_hist_alpha", 0.6),
        "zorder_defaults": {
            "bar": config.get("overlay_default_zorder_bar", 1),
            "line": config.get("overlay_default_zorder_line", 2),
            "scatter": config.get("overlay_default_zorder_scatter", 2),
            "histogram": config.get("overlay_default_zorder_hist", 1),
        },
        "show_grid": show_grid,
        "grid_style": get_grid_style({}),
        "hatch_cycle": config.get("plot_hatch_cycle"),
        "show_legend": show_legend,
        "legend_mode": "combined",
        "legend_style": get_legend_style(),
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel_left,
        "ylabel_right": ylabel_right,
        "label_styles": _PanelSeam.snapshot_label_styles(),
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "ymin_right": ymin_right,
        "ymax_right": ymax_right,
    }

    if projection == "polar":
        # the merged panel keeps the first source figure's radial furniture
        source_settings = items[0]["figure"]._chart_metadata["panel"].settings
        for key in (
            "startangle",
            "direction",
            "innerradius",
            "show_border",
            "show_values",
            "show_tip_labels",
            "value_format",
            "tip_value_style",
        ):
            panel_settings[key] = source_settings.get(key)

    panel = _PanelSeam(groups, panel_settings)

    fig = new_figure(figsize=figsize)
    ax = fig.subplots(
        subplot_kw={"projection": "polar"} if projection == "polar" else None
    )
    # the panel title renders as the figure suptitle when the panel is the figure
    panel.settings = {**panel_settings, "title": None}
    panel.render(ax)
    panel.settings = panel_settings
    if title:
        fig.suptitle(title, **get_text_style("title"))

    fig._chart_metadata = {
        "type": "overlay",
        "panel": panel,
    }

    return fig


def Annotate(
    figure: plt.Figure,
    texts: Union[TextAttrs, List[TextAttrs]],
) -> plt.Figure:
    """Add text annotations to an already rendered figure.

    Returns a new figure with the annotations riding the figure's chart
    metadata, styled by the current theme at call time — so they follow
    themes and survive `Panel` and `Grid` composition. The source figure and
    its charts are never modified.

    Works on any figure whose charts share one coordinate space: chart
    figures (including polar ones) and `Panel` output. Grid figures and
    multi-subplot figures (`subplots=True`) are rejected — annotate the
    sources before composing.

    !!! info "Added in v0.8.0"

    Examples:
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

    Args:
        figure: A figure created by a datachart chart function or `Panel`.
        texts: The text annotation(s) to add. Each annotation places `text`
            at (`x`, `y`) — data coordinates by default, axes fractions with
            `"coords": "axes"` — draws a connector to the optional `target`
            data point, and takes a per-text `style` override.

    Returns:
        A new matplotlib Figure with the annotations added.

    Raises:
        ValueError: If the figure has no chart metadata, is a Grid figure,
            or is a multi-subplot figure.
    """
    metadata = getattr(figure, "_chart_metadata", None)
    if metadata is None or metadata.get("type") is None:
        raise ValueError(
            "Figure is missing chart metadata. "
            "This figure was likely not created by a datachart chart function."
        )
    if metadata.get("type") == "grid":
        raise ValueError(
            "Grid figures cannot be annotated; annotate the source figures "
            "before composing them with Grid."
        )
    if metadata.get("panels") is not None:
        raise ValueError(
            "Multi-subplot figures cannot be annotated: the texts have no "
            "single coordinate space to land in. Annotate single-chart "
            "figures before composing them."
        )
    panel = metadata.get("panel")
    if panel is None:
        raise ValueError("Figure has invalid metadata: missing 'panel'")

    # existing groups are shared, never mutated: the chart-hash -> color
    # invariant holds, and the carrier claims no color-cycle slot (ADR 0018)
    carrier = LayerGroup([TextLayer(texts)], max_colors=0)
    new_panel = _PanelSeam(panel.groups + [carrier], panel.settings)

    fig = new_figure(figsize=tuple(figure.get_size_inches()))
    ax = fig.subplots(
        subplot_kw=(
            {"projection": "polar"} if new_panel.projection == "polar" else None
        )
    )
    # the panel title renders as the figure suptitle when the panel is the figure
    title = panel.settings.get("title")
    new_panel.settings = {**panel.settings, "title": None}
    new_panel.render(ax)
    new_panel.settings = panel.settings
    if title:
        fig.suptitle(title, **get_text_style("title"))

    fig._chart_metadata = {
        "type": metadata["type"],
        "panel": new_panel,
    }

    return fig


def _grid_from_rows(
    rows: List[List[Optional[plt.Figure]]],
    *,
    title: Optional[str],
    xlabel: Optional[str],
    ylabel: Optional[str],
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
        xlabel=xlabel,
        ylabel=ylabel,
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
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
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

    !!! info "Added in v0.8.0"

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
        xlabel: Optional x-axis label for the whole grid, drawn once below
            every cell. A nested grid keeps its own as a footer of its cell.
        ylabel: Optional y-axis label for the whole grid, drawn once to the
            left of every cell. A nested grid keeps its own beside its cell.
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
            xlabel=xlabel,
            ylabel=ylabel,
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
        xlabel=xlabel,
        ylabel=ylabel,
        max_cols=max_cols,
        figsize=figsize,
        sharex=sharex,
        sharey=sharey,
    )
