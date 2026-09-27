"""The one record-reading seam: a front's `data` in, canonical chart dicts out.

The data shape and the front's `ChartKind` row alone decide how many charts
there are, and every record comes out under the row's canonical keys
(ADR 0069). A missing value (None, NaN, an infinity) reads as NaN, and a
record whose position is missing is dropped (ADR 0082).
"""

import warnings
from collections.abc import Iterable, Iterator
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from .chart_kinds import ChartKind, chart_kind
from .validate import is_missing

# extra attrs whose single value is itself a list, like the tick positions
LIST_TYPE_EXTRA_ATTRS = {"dimensions"}
# kept as lists: a group chart's `emphasis` holds one role per group
UNWRAP_EXEMPT_ATTRS = LIST_TYPE_EXTRA_ATTRS | {"emphasis"}


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


def _get_chart_marks(value: Any, index: int) -> Any:
    """Get the chart's marks from one or several marks, or those of each chart.

    A flat list of mark dicts belongs to every chart; a list holding a list
    or `None` gives its item at `index` to that chart.

    Args:
        value: One mark, a flat list of marks, or a list of each chart's marks.
        index: The chart's index.

    Returns:
        The chart's mark or marks.
    """
    if isinstance(value, list) and any(v is None or isinstance(v, list) for v in value):
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
        chart_dict["vlines"] = _get_chart_marks(vlines, index)

    if hlines is not None:
        chart_dict["hlines"] = _get_chart_marks(hlines, index)

    if dlines is not None:
        chart_dict["dlines"] = _get_chart_marks(dlines, index)
    if brackets is not None:
        chart_dict["brackets"] = _get_chart_marks(brackets, index)

    if vspans is not None:
        chart_dict["vspans"] = _get_chart_marks(vspans, index)

    if hspans is not None:
        chart_dict["hspans"] = _get_chart_marks(hspans, index)

    if texts is not None:
        chart_dict["texts"] = _get_chart_marks(texts, index)

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
        chart_dict["vlines"] = _get_chart_marks(vlines, 0)

    if hlines is not None:
        chart_dict["hlines"] = _get_chart_marks(hlines, 0)

    if dlines is not None:
        chart_dict["dlines"] = _get_chart_marks(dlines, 0)
    if brackets is not None:
        chart_dict["brackets"] = _get_chart_marks(brackets, 0)

    if vspans is not None:
        chart_dict["vspans"] = _get_chart_marks(vspans, 0)

    if hspans is not None:
        chart_dict["hspans"] = _get_chart_marks(hspans, 0)

    if texts is not None:
        chart_dict["texts"] = _get_chart_marks(texts, 0)

    # a one-element list is the one chart's value, like `subtitle` above
    for attr_name, attr_value in extra_attrs.items():
        if (
            attr_name not in UNWRAP_EXEMPT_ATTRS
            and isinstance(attr_value, list)
            and len(attr_value) == 1
        ):
            attr_value = attr_value[0]
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
    for dataset in datasets:
        if not (isinstance(dataset, dict) and all(k in dataset for k in keys)):
            shape = " and ".join(f"`{k}`" for k in keys)
            raise ValueError(
                f"{_front(kind)} `data` must be a dict"
                f"{' with ' + shape if shape else ''}, or a list of such dicts; "
                f"got {_type_name(dataset)}."
            )
    return datasets


def _record_datasets(kind: ChartKind, data: Any) -> Any:
    """A record front's `data`, its tuples and generators read as lists.

    Args:
        kind: The front's row.
        data: A list of records, a list of such lists, or a dict of columns.

    Returns:
        The data as records or lists of records, every sequence a list.

    Raises:
        ValueError: If the data has none of the three shapes, naming the
            first chart, record, or column that breaks it.
    """
    data = _as_list(data)
    if isinstance(data, dict):
        return _columns(kind, data, "data")
    if not isinstance(data, list):
        raise ValueError(
            f"{_front(kind)} `data` must be a list of records (dicts), a list "
            f"of such lists, or a dict of columns; got {_type_name(data)}."
        )
    data = [_as_list(chart) for chart in data]
    is_multi_chart = bool(data) and isinstance(data[0], list)
    for index, chart in enumerate(data if is_multi_chart else [data]):
        where = f"data[{index}]" if is_multi_chart else "data"
        if isinstance(chart, dict):
            data[index] = _columns(kind, chart, where)
            continue
        if not isinstance(chart, list):
            raise ValueError(
                f"{_front(kind)} `{where}` must be a list of records or a dict "
                f"of columns; got {_type_name(chart)}."
            )
        for position, record in enumerate(chart):
            if not isinstance(record, dict):
                raise ValueError(
                    f"{_front(kind)} record `{where}[{position}]` must be a "
                    f"dict; got {_type_name(record)}."
                )
    return data


def _columns(kind: ChartKind, data: dict, where: str) -> List[dict]:
    # a dict of columns reads as one record per row, so layers see one form
    columns = {key: _as_list(values) for key, values in data.items()}
    for key, values in columns.items():
        if not isinstance(values, (list, np.ndarray)):
            raise ValueError(
                f"{_front(kind)} column `{where}[{key!r}]` must be a list; "
                f"got {_type_name(values)}."
            )
    lengths = {key: len(values) for key, values in columns.items()}
    if len(set(lengths.values())) > 1:
        raise ValueError(
            f"{_front(kind)} columns in `{where}` must have equal lengths; "
            f"got {lengths}."
        )
    return [dict(zip(columns, row)) for row in zip(*columns.values())]


def _dict_datasets(data: Any) -> Any:
    # a generator in a dict reads once as a list; tuples already serialise
    data = _as_list(data)
    datasets = data if isinstance(data, list) else [data]
    read = [
        (
            {k: list(v) if isinstance(v, Iterator) else v for k, v in d.items()}
            if isinstance(d, dict)
            else d
        )
        for d in datasets
    ]
    return read if isinstance(data, list) else read[0]


def _as_list(value: Any) -> Any:
    # tuples and generators read as lists; dicts, strings and arrays stay whole
    if isinstance(value, Iterable) and not isinstance(
        value, (list, dict, str, bytes, np.ndarray)
    ):
        return list(value)
    return value


def _front(kind: ChartKind) -> str:
    return f"{kind.label[0].upper()}{kind.label[1:]}"


def _type_name(value: Any) -> str:
    return type(value).__name__


def _is_record_rows(kind: ChartKind, data: Any) -> bool:
    # one record per row: each data key holds one value, not a column
    return isinstance(data, list) and all(
        isinstance(record, dict)
        and all(k in record and not isinstance(record[k], list) for k in kind.data_keys)
        for record in data
    )


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
    required_keys: Optional[Tuple[str, ...]] = None,
    **extra_attrs: Any,
) -> List[Dict[str, Any]]:
    """Build the canonical chart dicts: the one record-reading seam (ADR 0069).

    The data shape and the front's `ChartKind` row alone decide how many
    charts there are; a record front's records come out under the row's
    canonical keys.

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
        required_keys: The record keys every record must carry; None takes
            the row's `required_keys`.
        **extra_attrs: Extra chart-specific attributes.

    Returns:
        One chart dict per dataset.

    Raises:
        ValueError: If the chart type has no row, the data misses the row's
            dict shape, a record misses a required key, or every value the
            data gives is missing.
    """
    kind = chart_kind(chart_type)
    data = _dict_datasets(data) if kind.dict_data else _record_datasets(kind, data)
    if kind.data_keys is not None and isinstance(data, list) and not data:
        # no datasets draw one empty panel, like a bar chart without records
        return []
    if kind.record_rows and _is_record_rows(kind, data):
        data = {key: [record.get(key) for record in data] for key in kind.data_keys}
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
        charts = [
            build_chart_dict_multi(i, chart_data, **common_args)
            for i, chart_data in enumerate(data)
        ]
    else:
        charts = [build_chart_dict_single(data, **common_args)]
    # a chart given data whose every value is missing has nothing to draw
    emptied = []
    if kind.record_keys:
        for index, chart in enumerate(charts):
            where = f"data[{index}]" if is_multi_chart else "data"
            records = canonical_records(kind, chart, where, required_keys)
            chart["data"] = _drawn_records(kind, records)
            emptied.append(bool(records) and not _has_values(kind, chart))
    elif kind.dict_data:
        for chart in charts:
            if isinstance(chart["data"], dict):
                chart["data"] = _drawn_columns(kind, chart["data"])
            emptied.append(not _has_values(kind, chart))
    else:
        # records of free-form keys: an infinity is missing like NaN
        for chart in charts:
            chart["data"] = [
                {k: _missing_as_nan(v) if v is not None else v for k, v in r.items()}
                for r in chart["data"]
            ]
    if charts and all(emptied) and len(emptied) == len(charts):
        raise ValueError(
            f"{_front(kind)} has nothing to draw: every value in `data` is "
            "missing (None, NaN, or inf)."
        )
    return charts


def _drawn_records(kind: ChartKind, records: List[dict]) -> List[dict]:
    # a missing position drops the record; a missing value stays as NaN
    drawn = []
    for record in records:
        if any(is_missing(record.get(key, 0)) for key in kind.position_keys):
            continue
        keys = [k for k in (*kind.position_keys, *kind.value_keys) if k in record]
        drawn.append({**record, **{key: _missing_as_nan(record[key]) for key in keys}})
    return drawn


def _drawn_columns(kind: ChartKind, data: dict) -> dict:
    # a grid front's columns drop the rows whose position is missing
    positions = [data[key] for key in kind.position_keys if key in data]
    kept = [
        index
        for index, row in enumerate(zip(*positions))
        if not any(is_missing(value) for value in row)
    ]
    if positions and len(kept) < len(positions[0]):
        size = len(positions[0])
        data = {
            key: (
                [values[index] for index in kept]
                if isinstance(values, (list, np.ndarray)) and len(values) == size
                else values
            )
            for key, values in data.items()
        }
    return {
        **data,
        **{k: _missing_as_nan(data[k]) for k in kind.value_keys if k in data},
    }


def _has_values(kind: ChartKind, chart: dict) -> bool:
    # the value keys decide, or the position keys where a record has none

    data = chart.get("data")
    if isinstance(data, dict):
        columns = [data]
    elif isinstance(data, list):
        columns = [record for record in data if isinstance(record, dict)]
    else:
        return True
    for keys in (kind.value_keys, kind.position_keys):
        cells = [column[key] for column in columns for key in keys if key in column]
        if cells:
            return any(_holds_a_value(cell) for cell in cells)
    return not kind.position_keys


def _holds_a_value(cell: Any) -> bool:
    if isinstance(cell, (list, tuple, np.ndarray)):
        return any(_holds_a_value(value) for value in cell)
    return not is_missing(cell)


def _missing_as_nan(value: Any) -> Any:
    """A value, list, or grid with each missing number as NaN.

    Finite numbers keep their type, so an integer grid still prints its
    values as integers; dates and strings are left as given.
    """

    if isinstance(value, np.ndarray):
        if value.dtype.kind == "f" and not np.isfinite(value).all():
            return np.where(np.isfinite(value), value, np.nan)
        if value.dtype.kind == "O":
            return np.array([_missing_as_nan(v) for v in value], dtype=object)
        return value
    if isinstance(value, (list, tuple)):
        return type(value)(_missing_as_nan(v) for v in value)
    if is_missing(value) and not isinstance(value, np.datetime64):
        return np.nan
    return value


def canonical_records(
    kind: ChartKind,
    chart: dict,
    where: str,
    required_keys: Optional[Tuple[str, ...]] = None,
) -> Any:
    """The chart's records copied under the row's canonical keys (ADR 0069).

    Pops the chart's remap parameters: each names the caller's key for one
    canonical key, which it defaults to; None in a per-chart list leaves
    that chart without the key. The caller's records are never
    mutated; keys the row does not declare, like `emphasis`, carry over.
    Records carrying a key the row has `renamed`, and not its new name,
    are read under the old name with a warning, unless another record key
    already reads the old one; the chart's `renamed` maps each such new
    name to the old one it read.

    Args:
        kind: The front's row, declaring the record keys.
        chart: One chart dict, its `data` a list of records.
        where: How the error names the chart's records, e.g. `"data[1]"`.
        required_keys: The record keys every record must carry; None takes
            the row's `required_keys`.

    Returns:
        The chart's data under canonical keys.

    Raises:
        ValueError: If a record misses a required key.
    """
    sources = {key: chart.pop(key) if key in chart else key for key in kind.record_keys}
    data = chart["data"]
    for old, new in kind.renamed.items():
        if (
            new in kind.record_keys
            and sources[new] == new
            and old not in sources.values()
            and any(old in record for record in data)
            and not any(new in record for record in data)
        ):
            warnings.warn(
                f"The `{old}` record key is deprecated and will be removed in "
                f"the next release; use `{new}` instead.",
                DeprecationWarning,
                stacklevel=5,
            )
            sources[new] = old
            # the row's `check_records` validates it like the parameter
            chart.setdefault("renamed", {})[new] = old
    required = kind.required_keys if required_keys is None else required_keys
    for index, record in enumerate(data):
        for key in required:
            if sources[key] is not None and sources[key] not in record:
                raise ValueError(
                    f"{_front(kind)} record "
                    f"`{where}[{index}]` has no `{sources[key]}` key."
                )
    return [_canonical(record, sources) for record in data]


def _canonical(record: dict, sources: Dict[str, str]) -> dict:
    # a remapped canonical key takes its source's value; the rest carry over
    moved = {k for k, src in sources.items() if src != k}
    canonical = {k: v for k, v in record.items() if k not in moved}
    canonical.update(
        (k, record[src])
        for k, src in sources.items()
        if src is not None and src != k and src in record
    )
    return canonical
