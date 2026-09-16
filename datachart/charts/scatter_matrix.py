import numbers
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from ..config import config
from ..utils.figure import _align_axes_columns, _apply_figure_labels, _render_grid_node
from ..utils.stats import correlation
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.colors import create_color_cycle
from ..utils._internal.config_helpers import get_legend_style
from ..utils._internal.figures import new_figure
from ..utils._internal.layers import (
    LayerGroup,
    Panel,
    TextLayer,
    build_chart_panel_settings,
)
from ..utils._internal.plot_engine import composition_panel
from ..typings import (
    LegendSettingAttrs,
    ScatterMatrixDataPointAttrs,
    StyleAttrs,
)
from ..constants import BAR_MODE, DIAGONAL, SHOW_GRID

# a matrix cell's side, in inches, when no figsize is given
CELL_SIZE = 2.2
# the share of a dimension's range padded onto each end of its limits
LIMIT_MARGIN = 0.05

# ================================================
# Data parsing
# ================================================


def _columns(data) -> Dict[str, list]:
    """The input as columns: a dict of equal-length lists, or records."""

    if isinstance(data, dict):
        lengths = {len(values) for values in data.values()}
        if len(lengths) > 1:
            raise ValueError(
                "Every column of the scatter matrix `data` must have the same "
                f"length; got lengths {sorted(lengths)}."
            )
        return {name: list(values) for name, values in data.items()}
    if isinstance(data, list) and all(isinstance(row, dict) for row in data):
        names = list(dict.fromkeys(name for row in data for name in row))
        return {name: [row.get(name) for row in data] for name in names}
    raise ValueError(
        "The scatter matrix `data` must be a dict of columns or a list of records."
    )


def _is_number(value) -> bool:
    return isinstance(value, numbers.Real) and not isinstance(value, bool)


def _is_numeric(values: list) -> bool:
    present = [v for v in values if v is not None]
    return bool(present) and all(_is_number(v) for v in present)


def _resolve_dimensions(
    columns: Dict[str, list], dimensions: Optional[List[str]], hue: Optional[str]
) -> List[str]:
    """The dimensions to plot: the given ones, or every numeric non-hue column."""

    if dimensions is None:
        dimensions = [
            name
            for name, values in columns.items()
            if name != hue and _is_numeric(values)
        ]
        if not dimensions:
            raise ValueError("The scatter matrix `data` has no numeric columns.")
        return dimensions
    if not dimensions:
        raise ValueError(
            "The scatter matrix `dimensions` must name at least one column."
        )
    for name in dimensions:
        if name not in columns:
            raise ValueError(f"Dimension {name!r} is not a column of `data`.")
        if name == hue:
            raise ValueError(
                f"Column {name!r} cannot be both a dimension and the `hue`."
            )
        if not _is_numeric(columns[name]):
            raise ValueError(f"Dimension {name!r} must hold numeric values.")
    return list(dimensions)


def _resolve_groups(columns: Dict[str, list], hue: Optional[str]) -> List[Tuple]:
    """(label, row mask) per hue group, in first-seen order; one unlabelled group without hue."""

    n_rows = len(next(iter(columns.values()), []))
    if hue is None:
        return [(None, np.ones(n_rows, dtype=bool))]
    if hue not in columns:
        raise ValueError(f"The `hue` column {hue!r} is not a column of `data`.")
    values = columns[hue]
    if any(v is None for v in values):
        raise ValueError(f"The `hue` column {hue!r} has missing values.")
    if _is_numeric(values):
        # a colour ramp has no clean reading across per-group curves (ADR 0051)
        raise ValueError(
            f"The `hue` column {hue!r} is numeric; the scatter matrix colours "
            "by categories only."
        )
    labels = np.array([str(v) for v in values], dtype=object)
    return [(label, labels == label) for label in dict.fromkeys(labels)]


def _as_floats(values: list) -> np.ndarray:
    return np.array([np.nan if v is None else v for v in values], dtype=float)


def _limits(values: np.ndarray) -> Tuple[float, float]:
    """The padded (min, max) of a dimension's finite values."""

    finite = values[np.isfinite(values)]
    if len(finite) == 0:
        return (0.0, 1.0)
    lo, hi = float(finite.min()), float(finite.max())
    if lo == hi:
        return (lo - 0.5, hi + 0.5)
    pad = (hi - lo) * LIMIT_MARGIN
    return (lo - pad, hi + pad)


# ================================================
# Cells
# ================================================


def _blank() -> Panel:
    return Panel([], {})


def _scatter_panel(x, y, groups, style, settings) -> Panel:
    series = []
    for _, mask in groups:
        keep = mask & np.isfinite(x) & np.isfinite(y)
        series.append(
            [{"x": float(a), "y": float(b)} for a, b in zip(x[keep], y[keep])]
        )
    charts = build_charts_structure(
        series, subtitle=[label for label, _ in groups], style=style
    )
    return composition_panel("scatterchart", charts, settings)


def _diagonal_panel(values, groups, diagonal, style, settings) -> Panel:
    series = []
    for _, mask in groups:
        keep = mask & np.isfinite(values)
        series.append([{"x": float(v)} for v in values[keep]])
    charts = build_charts_structure(
        series, subtitle=[label for label, _ in groups], style=style
    )
    chart_type = "kde" if diagonal == DIAGONAL.KDE else "histogram"
    return composition_panel(chart_type, charts, settings)


def _correlation_panel(x, y, groups, colors, style, settings) -> Panel:
    """The Pearson r per hue group, stacked in the middle of the cell."""

    font = {
        **style,
        "plot_text_size": style.get(
            "plot_scatter_matrix_correlation_size",
            config["plot_scatter_matrix_correlation_size"],
        ),
        "plot_text_weight": style.get(
            "plot_scatter_matrix_correlation_weight",
            config["plot_scatter_matrix_correlation_weight"],
        ),
        "plot_text_halign": "center",
        "plot_text_box_visible": False,
    }
    step = 1 / (len(groups) + 1)
    texts = []
    for k, (label, mask) in enumerate(groups):
        keep = mask & np.isfinite(x) & np.isfinite(y)
        r = correlation(x[keep], y[keep]) if keep.sum() > 1 else np.nan
        value = "n/a" if np.isnan(r) else f"{r:.2f}"
        text_style = dict(font)
        if label is not None:
            text_style["plot_text_color"] = colors[k]
        texts.append(
            {
                "text": f"r = {value}" if label is None else f"{label}: {value}",
                "x": 0.5,
                "y": 1 - step * (k + 1),
                "coords": "axes",
                "style": text_style,
            }
        )
    carrier = LayerGroup([TextLayer(texts)], max_colors=0)
    panel_settings = build_chart_panel_settings(
        "scatterchart", settings, "composition", style
    )
    return Panel([carrier], {**panel_settings, "title": None})


# ================================================
# Main Chart Definition
# ================================================


def ScatterMatrix(
    data: Union[Dict[str, List[Any]], List[ScatterMatrixDataPointAttrs]],
    *,
    dimensions: Optional[List[str]] = None,
    hue: Optional[str] = None,
    diagonal: Optional[Union[DIAGONAL, str]] = None,
    lower_only: Optional[bool] = None,
    show_regression: Optional[bool] = None,
    show_correlation: Optional[bool] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    title: Optional[str] = None,
    figsize: Optional[Tuple[float, float]] = None,
    show_legend: Optional[bool] = None,
    legend: Optional[LegendSettingAttrs] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    style: Optional[StyleAttrs] = None,
) -> plt.Figure:
    """Creates a scatter matrix.

    Every pair of numeric dimensions gets a scatter chart, and each
    dimension's own distribution sits on the diagonal. Use it to scan many
    variables for relationships, clusters and outliers at once, optionally
    split by a categorical `hue`. For two variables use
    [`ScatterChart`][datachart.charts.ScatterChart]; for many dimensions
    per observation read as lines, use
    [`ParallelCoords`][datachart.charts.ParallelCoords].

    The figure is a grid: it nests inside
    [`Grid`][datachart.utils.Grid] and cannot be overlaid with
    [`Panel`][datachart.utils.Panel].

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.charts import ScatterMatrix
        >>> figure = ScatterMatrix(
        ...     data={
        ...         "length": [5.1, 4.9, 6.3, 5.8, 7.1, 6.5],
        ...         "width": [3.5, 3.0, 3.3, 2.7, 3.0, 3.2],
        ...         "petal": [1.4, 1.4, 6.0, 5.1, 5.9, 5.1],
        ...         "species": ["a", "a", "b", "b", "b", "b"],
        ...     },
        ...     hue="species",
        ... )
        >>>
        >>> # correlations above the diagonal, regression lines below
        >>> figure = ScatterMatrix(
        ...     data=records,
        ...     diagonal="kde",
        ...     show_correlation=True,
        ...     show_regression=True,
        ... )

    Args:
        data: The observations: a dict of equal-length columns, or a list of
            records. Missing values (`None`) are left out pair by pair.
        dimensions: The numeric columns to plot, in order. Defaults to every
            numeric column except the `hue`, in input order.
        hue: The column whose categories colour the points, one colour per
            category and one legend for the whole figure. A numeric column
            raises.
        diagonal: What each dimension's own cell shows: a histogram
            (`"hist"`, default), a density curve (`"kde"`), or nothing
            (`"none"`). See `DIAGONAL`.
        lower_only: Whether to leave the cells above the diagonal empty.
            Wins over `show_correlation`.
        show_regression: Whether to draw a least-squares line per hue group
            in every scatter cell.
        show_correlation: Whether to replace the scatters above the diagonal
            with the Pearson correlation of each hue group.
        sharex: Whether the cells of a column share their x limits and only
            the bottom row labels its ticks (default `True`).
        sharey: Whether the cells of a row share their y limits and only the
            left column labels its ticks (default `True`). The diagonal
            cells never share it: their axis is a count or a density.
        title: The title of the figure.
        figsize: The size of the figure. Defaults to 2.2 inches per cell.
        show_legend: Whether to show the legend of the hue groups (default
            `True` when `hue` is set).
        legend: The legend setting: title, column count and alignment; the
            legend sits to the right of the matrix. See `LegendSettingAttrs`.
        show_grid: Which grid lines to show in the cells (e.g., "both", "x",
            "y").
        style: Style attributes for every cell: the scatter, histogram,
            plot text and `plot_scatter_matrix_*` keys. See
            `ScatterMatrixStyleAttrs`.

    Returns:
        The figure containing the scatter matrix.

    Raises:
        ValueError: If `data` is malformed or has no numeric column, a
            dimension is missing or not numeric, or `hue` is missing, has
            missing values, or is numeric.

    """
    columns = _columns(data)
    dims = _resolve_dimensions(columns, dimensions, hue)
    groups = _resolve_groups(columns, hue)
    diagonal = DIAGONAL.DEFAULT if diagonal is None else diagonal
    if diagonal not in (DIAGONAL.HIST, DIAGONAL.KDE, DIAGONAL.NONE):
        raise ValueError(
            f"Invalid `diagonal` value {diagonal!r}. "
            f"Must be one of {[DIAGONAL.HIST, DIAGONAL.KDE, DIAGONAL.NONE]}."
        )
    sharex = True if sharex is None else sharex
    sharey = True if sharey is None else sharey
    show_legend = hue is not None if show_legend is None else show_legend
    style = dict(style or {})

    values = {name: _as_floats(columns[name]) for name in dims}
    limits = {name: _limits(values[name]) for name in dims}
    palette = config["color_general_multiple"]
    cycle = create_color_cycle(palette, len(groups))
    colors = [cycle[k]["color"] for k in range(len(groups))]
    regression_style = {
        "plot_regression_color": style.get(
            "plot_scatter_matrix_regression_color",
            config["plot_scatter_matrix_regression_color"],
        ),
        "plot_regression_width": style.get(
            "plot_scatter_matrix_regression_width",
            config["plot_scatter_matrix_regression_width"],
        ),
        "plot_regression_style": style.get(
            "plot_scatter_matrix_regression_style",
            config["plot_scatter_matrix_regression_style"],
        ),
    }
    diagonal_style = {
        "plot_hist_alpha": style.get(
            "plot_scatter_matrix_diagonal_alpha",
            config["plot_scatter_matrix_diagonal_alpha"],
        ),
        **style,
    }

    n = len(dims)
    blank = [
        [
            (i == j and diagonal == DIAGONAL.NONE) or (i < j and bool(lower_only))
            for j in range(n)
        ]
        for i in range(n)
    ]
    # the edge labels go to the outermost drawn cell of each column and row
    drawn = [[not cell for cell in row] for row in blank]
    bottom = [
        max((i for i in range(n) if drawn[i][j]), default=n - 1) for j in range(n)
    ]
    left = [min((j for j in range(n) if drawn[i][j]), default=0) for i in range(n)]
    # a blank diagonal under lower_only leaves the top row and right column empty
    trim = 1 if lower_only and diagonal == DIAGONAL.NONE and n > 1 else 0
    cells, kinds = [], []
    for i in range(trim, n):
        for j in range(n - trim):
            xdim, ydim = dims[j], dims[i]
            outer_x, outer_y = i == bottom[j], j == left[i]
            hidden = []
            if sharex and not outer_x:
                hidden.append("x")
            if (sharey and not outer_y) or i == j:
                hidden.append("y")
            settings = {
                # an empty title keeps a hue group's name off the cell
                "title": "",
                "xlabel": xdim if outer_x else None,
                "ylabel": ydim if outer_y else None,
                "show_legend": False,
                "show_grid": show_grid,
                "hide_ticklabels": hidden,
            }
            if sharex:
                settings["xmin"], settings["xmax"] = limits[xdim]
            if sharey and i != j:
                settings["ymin"], settings["ymax"] = limits[ydim]

            if blank[i][j]:
                kind, panel = "blank", _blank()
            elif i == j:
                kind = "diagonal"
                settings["bar_mode"] = BAR_MODE.OVERLAY
                settings["kde_xlim"] = limits[xdim]
                panel = _diagonal_panel(
                    values[xdim], groups, diagonal, diagonal_style, settings
                )
            elif i < j and show_correlation:
                kind = "correlation"
                settings["show_grid"] = False
                settings["hide_ticklabels"] = ["x", "y"]
                panel = _correlation_panel(
                    values[xdim], values[ydim], groups, colors, style, settings
                )
            else:
                kind = "scatter"
                settings["show_regression"] = show_regression
                settings["regression_style"] = regression_style
                panel = _scatter_panel(
                    values[xdim], values[ydim], groups, style, settings
                )
            kinds.append(kind)
            cells.append(
                {
                    "panel": panel,
                    "spec": {"row": i - trim, "col": j, "rowspan": 1, "colspan": 1},
                }
            )
    # any cell drawing every hue group can lend its entries to the legend
    legend_cell = next(
        (
            k
            for kind in ("scatter", "diagonal")
            for k, c in enumerate(kinds)
            if c == kind
        ),
        None,
    )

    node_legend = None
    if show_legend and hue is not None and legend_cell is not None:
        node_legend = {
            "cell": legend_cell,
            "style": {
                k: v
                for k, v in get_legend_style(legend).items()
                if k not in ("loc", "bbox_to_anchor")
            },
            "family": cells[0]["panel"]
            .settings.get("furniture", {})
            .get("font_family"),
        }

    node = {
        "type": "grid",
        "cells": cells,
        "shape": (n - trim, n - trim),
        "title": title,
        "xlabel": None,
        "ylabel": None,
        "sharex": False,
        "sharey": False,
        "legend": node_legend,
    }

    size = n - trim
    if figsize is None:
        figsize = (CELL_SIZE * size + (1.2 if node_legend else 0), CELL_SIZE * size)
    figure = new_figure(figsize=figsize)
    # the figure title is the suptitle; nested, the node renders it as a heading
    _render_grid_node(figure, {**node, "title": None}, GridSpec(1, 1, figure=figure)[0])
    _apply_figure_labels(figure, title, None, None)
    _align_axes_columns(figure)
    figure._chart_metadata = node
    return figure
