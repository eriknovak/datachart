from typing import Union, List, Optional, Tuple, Dict

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..typings import (
    ParallelCoordsDataPointAttrs,
    ParallelCoordsStyleAttrs,
    TextAttrs,
)
from ..constants import ASPECT_RATIO, EMPHASIS, FIG_SIZE, SHOW_GRID

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
    emphasis: Optional[Union[EMPHASIS, str, List[Optional[str]]]] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    show_legend: Optional[bool] = None,
    show_grid: Optional[Union[SHOW_GRID, str]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    style: Optional[
        Union[ParallelCoordsStyleAttrs, List[Optional[ParallelCoordsStyleAttrs]]]
    ] = None,
    dimensions: Optional[List[str]] = None,
    hue: Optional[Union[str, List[Optional[str]]]] = None,
    category_orders: Optional[Dict[str, List[str]]] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
) -> plt.Figure:
    """Creates the parallel coordinates chart.

    Parallel coordinates draw each record as a polyline across one vertical
    axis per dimension. Use it to explore multivariate data: clusters show as
    bundles of similar lines, and correlations between neighboring dimensions
    show as parallel or crossing segments. Works best with a handful of
    dimensions; color the records by group with `hue` to compare groups.

    !!! info "Added in v0.7.0"

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
        emphasis: The emphasis role(s), aligned with the data rows (a single
            value applies to every row): "background" mutes a row (theme muted
            color, lowered alpha, thinner line, behind the others, no hue
            legend entry), "highlight" bolds it and brings it to the front
            among the data rows, None leaves it unchanged.
        figsize: The size of the figure.
        show_legend: Whether to show the legend (for hue categories).
        show_grid: Which grid lines to show (e.g., "both", "x", "y").
        aspect_ratio: The aspect ratio of the axes ("auto" or "equal"). See
            `ASPECT_RATIO`.
        style: Style configuration(s) for the lines.
        dimensions: List of dimension names to include and their order. If None,
            all columns (except hue) are auto-detected.
        hue: The key name in data for line coloring. String values color
            categorically: data points with the same hue value get the same
            color from `color_parallel_hue`. Numeric values color continuously
            along the theme's `color_parallel_hue_continuous` ramp.
        category_orders: Dictionary mapping dimension names to lists of category
            values in the desired order. Example: {"rating": ["Low", "Medium", "High"]}.
            Categories not in the list will be appended at the end (sorted).
        texts: Text annotation(s) to draw.

    Returns:
        The figure containing the parallel coordinates chart.

    """
    # Build the charts structure using shared utility
    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        emphasis=emphasis,
        style=style,
        dimensions=dimensions,
        hue=hue,
        category_orders=category_orders,
        texts=texts,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "figsize": figsize,
        "show_legend": show_legend,
        "show_grid": show_grid,
        "aspect_ratio": aspect_ratio,
    }

    return render_chart("parallelcoords", charts, settings)
