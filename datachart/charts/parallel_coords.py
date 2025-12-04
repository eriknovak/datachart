from typing import Union, List, Optional, Tuple, Dict

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import chart_plot_wrapper, plot_parallel_coords
from ..utils._internal.chart_builder import build_charts_structure, build_attrs_dict
from ..typings import (
    ParallelCoordsDataPointAttrs,
    ParallelCoordsStyleAttrs,
)
from ..constants import FIG_SIZE, SHOW_GRID

# ================================================
# Main Chart Definition
# ================================================


def ParallelCoords(
    data: Union[
        List[ParallelCoordsDataPointAttrs], List[List[ParallelCoordsDataPointAttrs]]
    ],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    aspect_ratio: Optional[str] = None,
    style: Optional[
        Union[ParallelCoordsStyleAttrs, List[Optional[ParallelCoordsStyleAttrs]]]
    ] = None,
    dimensions: Optional[List[str]] = None,
    hue: Optional[Union[str, List[Optional[str]]]] = None,
    category_orders: Optional[Dict[str, List[str]]] = None,
) -> plt.Figure:
    """Creates the parallel coordinates chart.

    A parallel coordinates chart displays multivariate data by representing each
    variable as a vertical axis and connecting data points across all axes with
    lines. This is useful for visualizing patterns and relationships in high-dimensional
    data, and for comparing groups when using the `hue` parameter.

    Examples:
        >>> from datachart.charts import ParallelCoords
        >>> figure = ParallelCoords(
        ...     data=[
        ...         {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2, "species": "setosa"},
        ...         {"sepal_length": 4.9, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.2, "species": "setosa"},
        ...         {"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4, "species": "versicolor"},
        ...     ],
        ...     title="Iris Dataset",
        ...     hue="species",
        ...     dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"],
        ...     show_legend=True
        ... )

    Args:
        data: The data points for the chart. Each data point is a dictionary where
            keys are dimension names and values are numeric or string values. Can
            optionally include a hue key for categorical coloring.
        title: The title of the chart.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        subtitle: The subtitle(s) for individual charts.
        figsize: The size of the figure.
        show_legend: Whether to show the legend (for hue categories).
        show_grid: Which grid lines to show (e.g., "both", "x", "y").
        aspect_ratio: The aspect ratio of the chart.
        style: Style configuration(s) for the lines.
        dimensions: List of dimension names to include and their order. If None,
            all columns (except hue) are auto-detected.
        hue: The key name in data for categorical coloring. Data points with the
            same hue value will be colored the same.
        category_orders: Dictionary mapping dimension names to lists of category
            values in the desired order. Example: {"rating": ["Low", "Medium", "High"]}.
            Categories not in the list will be appended at the end (sorted).

    Returns:
        The figure containing the parallel coordinates chart.

    """
    # Build the charts structure using shared utility
    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        style=style,
        dimensions=dimensions,
        hue=hue,
        category_orders=category_orders,
    )

    # Build the attrs dict using shared utility
    attrs = build_attrs_dict(
        "parallelcoords",
        charts,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=figsize,
        show_legend=show_legend,
        show_grid=show_grid,
        aspect_ratio=aspect_ratio,
    )

    return chart_plot_wrapper(plot_parallel_coords)(attrs)
