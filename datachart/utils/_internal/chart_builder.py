"""Shared utility for building chart data structures.

This module provides helper functions to reduce boilerplate in chart definitions.
"""

from typing import Any, Dict, List, Union

from .chart_kinds import chart_kind

# extra attrs whose single value is itself a list, like the tick positions
LIST_TYPE_EXTRA_ATTRS = {"dimensions"}


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
        if isinstance(value, list) and any(isinstance(v, list) for v in value):
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
    dlines: Any = None,
    brackets: Any = None,
    vspans: Any = None,
    hspans: Any = None,
    texts: Any = None,
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
        dlines: The diagonal lines.
        brackets: The pairwise comparison brackets.
        vspans: The vertical reference bands.
        hspans: The horizontal reference bands.
        texts: The text annotations.
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

    if dlines is not None:
        chart_dict["dlines"] = _get_indexed_value(dlines, index)
    if brackets is not None:
        chart_dict["brackets"] = _get_indexed_value(brackets, index)

    if vspans is not None:
        chart_dict["vspans"] = _get_indexed_value(vspans, index)

    if hspans is not None:
        chart_dict["hspans"] = _get_indexed_value(hspans, index)

    if texts is not None:
        chart_dict["texts"] = _get_indexed_value(texts, index)

    # Add extra chart-specific attributes
    for attr_name, attr_value in extra_attrs.items():
        if attr_value is not None:
            chart_dict[attr_name] = _get_indexed_value(
                attr_value, index, is_list_type=attr_name in LIST_TYPE_EXTRA_ATTRS
            )

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
    dlines: Any = None,
    brackets: Any = None,
    vspans: Any = None,
    hspans: Any = None,
    texts: Any = None,
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
        dlines: The diagonal lines.
        brackets: The pairwise comparison brackets.
        vspans: The vertical reference bands.
        hspans: The horizontal reference bands.
        texts: The text annotations.
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

    if dlines is not None:
        chart_dict["dlines"] = dlines
    if brackets is not None:
        chart_dict["brackets"] = brackets

    if vspans is not None:
        chart_dict["vspans"] = vspans

    if hspans is not None:
        chart_dict["hspans"] = hspans

    if texts is not None:
        chart_dict["texts"] = texts

    # Add extra chart-specific attributes (preserve as-is, don't transform)
    for attr_name, attr_value in extra_attrs.items():
        if attr_value is not None:
            chart_dict[attr_name] = attr_value

    return chart_dict


def dict_datasets(chart_type: str, data: Any) -> List[dict]:
    """One dict per chart, checked against the keys the front's row requires.

    Args:
        chart_type: The chart type whose row names the required keys.
        data: One chart's dict, or a list of them.

    Returns:
        The datasets as a list, one per chart.

    Raises:
        ValueError: If a dataset is not a dict or misses a required key.
    """
    kind = chart_kind(chart_type)
    datasets = data if isinstance(data, list) else [data]
    keys = kind.data_keys or ()
    if not all(isinstance(d, dict) and all(k in d for k in keys) for d in datasets):
        shape = "a dict"
        if len(keys) == 1:
            article = "an" if keys[0][0] in "aeiou" else "a"
            shape += f" with {article} `{keys[0]}` key"
        elif keys:
            shape += f" with {' and '.join(f'`{k}`' for k in keys)} keys"
        raise ValueError(
            f"{kind.label[0].upper()}{kind.label[1:]} `data` must be {shape}, "
            "or a list of such dicts."
        )
    return datasets


def build_charts_structure(
    chart_type: str,
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
    dlines: Any = None,
    brackets: Any = None,
    vspans: Any = None,
    hspans: Any = None,
    texts: Any = None,
    **extra_attrs: Any,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Build the charts structure for internal API.

    This handles both single-chart and multi-chart data formats; the front's
    `ChartKind` row says which shape one chart's data takes.

    Args:
        chart_type: The chart type whose row the data is read against.
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
        dlines: The diagonal lines.
        brackets: The pairwise comparison brackets.
        vspans: The vertical reference bands.
        hspans: The horizontal reference bands.
        texts: The text annotations.
        **extra_attrs: Extra chart-specific attributes.

    Returns:
        Either a single chart dict or a list of chart dicts.

    Raises:
        ValueError: If the chart type has no row, a parameter the row
            rejects is set, or the data misses the row's dict shape.
    """
    kind = chart_kind(chart_type)
    for name, reason in kind.rejects.items():
        if extra_attrs.get(name) is not None:
            raise ValueError(reason)
    if kind.data_keys is not None:
        dict_datasets(chart_type, data)

    # Detect if data is for multiple charts
    if kind.dict_data:
        # one chart is a dict (a grid, links, a tree); several are a list of them
        is_multi_chart = (
            isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict)
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
        "dlines": dlines,
        "brackets": brackets,
        "vspans": vspans,
        "hspans": hspans,
        "texts": texts,
        **extra_attrs,
    }

    if is_multi_chart:
        return [
            build_chart_dict_multi(i, chart_data, **common_args)
            for i, chart_data in enumerate(data)
        ]
    else:
        return build_chart_dict_single(data, **common_args)
