from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render_chart
from ..utils._internal.chart_builder import build_charts_structure
from ..utils._internal.validate import validate_treemap_records
from ..typings import TreemapSingleChartAttrs, TreemapStyleAttrs, TextAttrs
from ..constants import FIG_SIZE, VALUE_FORMAT

# ================================================
# Main Chart Definition
# ================================================


def Treemap(
    data: Union[TreemapSingleChartAttrs, List[TreemapSingleChartAttrs]],
    *,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    show_legend: Optional[bool] = None,
    title: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: None = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    style: Optional[Union[TreemapStyleAttrs, List[Optional[TreemapStyleAttrs]]]] = None,
    texts: Optional[
        Union[
            TextAttrs,
            List[TextAttrs],
            List[Union[TextAttrs, List[TextAttrs], None]],
        ]
    ] = None,
) -> plt.Figure:
    """Creates the treemap.

    A treemap tiles part-of-whole data as rectangles whose area is the
    value — disk usage by folder, a budget by line, population by continent
    and country. A record's `children` add one level of grouping: the group
    is a bordered box with a header band, its tiles a lighter tint of the
    group color. Every level is sorted largest first and tiled so the
    rectangles stay near square. Use it when the question is how a whole
    splits; for the values alone, or for more than a handful of small parts,
    use [`BarChart`][datachart.charts.BarChart].

    !!! info "Added in v0.9.1"

    Examples:
        >>> from datachart.charts import Treemap
        >>> figure = Treemap(
        ...     data={
        ...         "data": [
        ...             {"label": "Asia", "children": [
        ...                 {"label": "India", "value": 1429},
        ...                 {"label": "China", "value": 1426},
        ...             ]},
        ...             {"label": "Africa", "value": 1460},
        ...             {"label": "Europe", "value": 742},
        ...         ]
        ...     },
        ...     title="Population, millions",
        ... )

    Args:
        data: The chart data: a `{"data": [...]}` dict whose records are
            `{"label", "value"}` dicts, or a list of such dicts drawing one
            treemap per subplot. A record may carry `children`, a list of
            records of the same shape, for one level of grouping; it then
            omits `value` or carries its children's sum. Any record may carry
            an `emphasis` role: `"background"` mutes the tile, `"highlight"`
            strokes its border; a child's role overrides its group's.
        show_values: Whether to write each tile's value under its label. A
            value that does not fit is dropped before the label.
        value_format: The format of the tile values: a `VALUE_FORMAT`
            constant (default `VALUE_FORMAT.DEFAULT`) or any `"{x:.1f}"`,
            `"{:.1f}%"`, or `"%g"` style string.
        show_legend: Whether to list the top-level records in a legend; it
            names the groups too short for a header band.
        title: The title of the chart.
        subtitle: The subtitle(s) for individual charts.
        emphasis: Not supported: emphasis is set per record through its
            `emphasis` key. Passing a value raises `ValueError`.
        figsize: The size of the figure.
        subplots: Whether to show each chart in its own subplot; several
            charts always split into subplots.
        max_cols: Maximum number of columns in subplots.
        style: Style configuration(s) for the chart(s).
        texts: Text annotation(s) to draw. The tiling spans 0–1 in both
            directions.

    Returns:
        The figure containing the treemap.

    Raises:
        ValueError: If `emphasis` is given, the records are malformed (a
            missing label, a value not above zero, a child with children, a
            group value that is not its children's sum), or a record's
            `emphasis` is not a role.

    """
    if emphasis is not None:
        raise ValueError(
            "Treemap does not support the `emphasis` argument: set the "
            "`emphasis` key on the records to mute or highlight instead."
        )

    datasets = data if isinstance(data, list) else [data]
    if not all(isinstance(d, dict) and "data" in d for d in datasets):
        raise ValueError(
            'Treemap `data` must be a `{"data": [...]}` dict, or a list of '
            "such dicts."
        )
    for dataset in datasets:
        validate_treemap_records(dataset["data"])

    charts = build_charts_structure(
        data,
        subtitle=subtitle,
        style=style,
        texts=texts,
        is_2d_data=True,
    )

    # Figure-level settings; None values resolve to defaults downstream
    settings = {
        "title": title,
        "figsize": figsize,
        "subplots": subplots,
        "max_cols": max_cols,
        "show_values": show_values,
        "value_format": value_format,
        "show_legend": show_legend,
    }

    return render_chart("treemap", charts, settings)
