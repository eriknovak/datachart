"""Shared utility for building chart data structures.

This module provides helper functions to reduce boilerplate in chart definitions.
"""

from typing import Any, Dict, List, Optional, Union


def _get_indexed_value(value: Any, index: int, is_list_type: bool = False) -> Any:
    """Get the value at the given index if it's a list, otherwise return the value.

    Args:
        value: The value or list of values.
        index: The index to retrieve.
        is_list_type: Whether the expected value type is a list itself (e.g., xticks).

    Returns:
        The indexed value or the original value.
    """
    if value is None:
        return None

    if is_list_type:
        # For list-type values like xticks, check if it's a list of lists
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], list):
            return value[index] if index < len(value) else None
        return value
    else:
        # For scalar-type values, check if it's a list
        if isinstance(value, list):
            return value[index] if index < len(value) else None
        return value


def _get_single_value(value: Any, expected_type: type) -> Any:
    """Get a single value, unwrapping from a list if needed.

    Args:
        value: The value or list of values.
        expected_type: The expected type of the single value.

    Returns:
        The single value.
    """
    if value is None:
        return None

    if isinstance(value, expected_type):
        return value

    if isinstance(value, list) and len(value) > 0:
        return value[0]

    return value


def build_chart_dict_multi(
    index: int,
    chart_data: Any,
    *,
    subtitle: Any = None,
    style: Any = None,
    xticks: Any = None,
    xticklabels: Any = None,
    xtickrotate: Any = None,
    yticks: Any = None,
    yticklabels: Any = None,
    ytickrotate: Any = None,
    vlines: Any = None,
    hlines: Any = None,
    **extra_attrs: Any,
) -> Dict[str, Any]:
    """Build a chart dictionary for multi-chart mode.

    Args:
        index: The chart index.
        chart_data: The data for this chart.
        subtitle: The subtitle(s).
        style: The style(s).
        xticks: The xtick positions.
        xticklabels: The xtick labels.
        xtickrotate: The xtick rotation.
        yticks: The ytick positions.
        yticklabels: The ytick labels.
        ytickrotate: The ytick rotation.
        vlines: The vertical lines.
        hlines: The horizontal lines.
        **extra_attrs: Extra chart-specific attributes.

    Returns:
        The chart dictionary.
    """
    chart_dict: Dict[str, Any] = {"data": chart_data}

    # Add common attributes
    if subtitle is not None:
        chart_dict["subtitle"] = _get_indexed_value(subtitle, index)

    if style is not None:
        style_val = _get_indexed_value(style, index)
        chart_dict["style"] = style_val if style_val is not None else {}

    if xticks is not None:
        chart_dict["xticks"] = _get_indexed_value(xticks, index, is_list_type=True)

    if xticklabels is not None:
        chart_dict["xticklabels"] = _get_indexed_value(
            xticklabels, index, is_list_type=True
        )

    if xtickrotate is not None:
        chart_dict["xtickrotate"] = _get_indexed_value(xtickrotate, index)

    if yticks is not None:
        chart_dict["yticks"] = _get_indexed_value(yticks, index, is_list_type=True)

    if yticklabels is not None:
        chart_dict["yticklabels"] = _get_indexed_value(
            yticklabels, index, is_list_type=True
        )

    if ytickrotate is not None:
        chart_dict["ytickrotate"] = _get_indexed_value(ytickrotate, index)

    if vlines is not None:
        chart_dict["vlines"] = _get_indexed_value(vlines, index)

    if hlines is not None:
        chart_dict["hlines"] = _get_indexed_value(hlines, index)

    # Add extra chart-specific attributes
    for attr_name, attr_value in extra_attrs.items():
        if attr_value is not None:
            chart_dict[attr_name] = _get_indexed_value(attr_value, index)

    return chart_dict


def build_chart_dict_single(
    data: Any,
    *,
    subtitle: Any = None,
    style: Any = None,
    xticks: Any = None,
    xticklabels: Any = None,
    xtickrotate: Any = None,
    yticks: Any = None,
    yticklabels: Any = None,
    ytickrotate: Any = None,
    vlines: Any = None,
    hlines: Any = None,
    **extra_attrs: Any,
) -> Dict[str, Any]:
    """Build a chart dictionary for single-chart mode.

    Args:
        data: The chart data.
        subtitle: The subtitle.
        style: The style.
        xticks: The xtick positions.
        xticklabels: The xtick labels.
        xtickrotate: The xtick rotation.
        yticks: The ytick positions.
        yticklabels: The ytick labels.
        ytickrotate: The ytick rotation.
        vlines: The vertical lines.
        hlines: The horizontal lines.
        **extra_attrs: Extra chart-specific attributes.

    Returns:
        The chart dictionary.
    """
    chart_dict: Dict[str, Any] = {"data": data}

    if subtitle is not None:
        chart_dict["subtitle"] = _get_single_value(subtitle, str)

    if style is not None:
        chart_dict["style"] = _get_single_value(style, dict)

    if xticks is not None:
        chart_dict["xticks"] = xticks

    if xticklabels is not None:
        chart_dict["xticklabels"] = xticklabels

    if xtickrotate is not None:
        chart_dict["xtickrotate"] = _get_single_value(xtickrotate, int)

    if yticks is not None:
        chart_dict["yticks"] = yticks

    if yticklabels is not None:
        chart_dict["yticklabels"] = yticklabels

    if ytickrotate is not None:
        chart_dict["ytickrotate"] = _get_single_value(ytickrotate, int)

    if vlines is not None:
        chart_dict["vlines"] = vlines

    if hlines is not None:
        chart_dict["hlines"] = hlines

    # Add extra chart-specific attributes (preserve as-is, don't transform)
    for attr_name, attr_value in extra_attrs.items():
        if attr_value is not None:
            chart_dict[attr_name] = attr_value

    return chart_dict


def build_charts_structure(
    data: Any,
    *,
    subtitle: Any = None,
    style: Any = None,
    xticks: Any = None,
    xticklabels: Any = None,
    xtickrotate: Any = None,
    yticks: Any = None,
    yticklabels: Any = None,
    ytickrotate: Any = None,
    vlines: Any = None,
    hlines: Any = None,
    is_2d_data: bool = False,
    **extra_attrs: Any,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Build the charts structure for internal API.

    This handles both single-chart and multi-chart data formats.

    Args:
        data: The chart data (single list or list of lists).
        subtitle: The subtitle(s).
        style: The style(s).
        xticks: The xtick positions.
        xticklabels: The xtick labels.
        xtickrotate: The xtick rotation.
        yticks: The ytick positions.
        yticklabels: The ytick labels.
        ytickrotate: The ytick rotation.
        vlines: The vertical lines.
        hlines: The horizontal lines.
        is_2d_data: If True, data for a single chart is 2D (e.g., heatmap).
            Multi-chart detection checks for 3D structure instead.
        **extra_attrs: Extra chart-specific attributes.

    Returns:
        Either a single chart dict or a list of chart dicts.
    """
    # Detect if data is for multiple charts
    if is_2d_data:
        # For 2D data (like heatmap), multi-chart means List[List[List[...]]]
        is_multi_chart = (
            isinstance(data, list)
            and len(data) > 0
            and isinstance(data[0], list)
            and len(data[0]) > 0
            and isinstance(data[0][0], list)
        )
    else:
        # For 1D data, multi-chart means List[List[...]]
        is_multi_chart = (
            isinstance(data, list) and len(data) > 0 and isinstance(data[0], list)
        )

    common_args = {
        "subtitle": subtitle,
        "style": style,
        "xticks": xticks,
        "xticklabels": xticklabels,
        "xtickrotate": xtickrotate,
        "yticks": yticks,
        "yticklabels": yticklabels,
        "ytickrotate": ytickrotate,
        "vlines": vlines,
        "hlines": hlines,
        **extra_attrs,
    }

    if is_multi_chart:
        return [
            build_chart_dict_multi(i, chart_data, **common_args)
            for i, chart_data in enumerate(data)
        ]
    else:
        return build_chart_dict_single(data, **common_args)


def build_attrs_dict(
    chart_type: str,
    charts: Union[Dict[str, Any], List[Dict[str, Any]]],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: Any = None,
    xmin: Any = None,
    xmax: Any = None,
    ymin: Any = None,
    ymax: Any = None,
    show_legend: Optional[bool] = None,
    show_grid: Any = None,
    aspect_ratio: Optional[str] = None,
    subplots: Optional[bool] = None,
    max_cols: Optional[int] = None,
    sharex: Optional[bool] = None,
    sharey: Optional[bool] = None,
    **extra_attrs: Any,
) -> Dict[str, Any]:
    """Build the attrs dictionary for the internal API.

    Args:
        chart_type: The type of chart (e.g., "linechart").
        charts: The charts structure.
        title: The title.
        xlabel: The x-axis label.
        ylabel: The y-axis label.
        figsize: The figure size.
        xmin: The minimum x-axis value.
        xmax: The maximum x-axis value.
        ymin: The minimum y-axis value.
        ymax: The maximum y-axis value.
        show_legend: Whether to show the legend.
        show_grid: Which grid lines to show.
        aspect_ratio: The aspect ratio.
        subplots: Whether to create subplots.
        max_cols: Maximum columns in subplots.
        sharex: Whether to share x-axis.
        sharey: Whether to share y-axis.
        **extra_attrs: Extra chart-specific attributes.

    Returns:
        The attrs dictionary.
    """
    attrs: Dict[str, Any] = {
        "type": chart_type,
        "charts": charts,
    }

    # Add common global attributes
    optional_attrs = {
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "figsize": figsize,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "show_legend": show_legend,
        "show_grid": show_grid,
        "aspect_ratio": aspect_ratio,
        "subplots": subplots,
        "max_cols": max_cols,
        "sharex": sharex,
        "sharey": sharey,
        **extra_attrs,
    }

    for key, value in optional_attrs.items():
        if value is not None:
            attrs[key] = value

    return attrs
