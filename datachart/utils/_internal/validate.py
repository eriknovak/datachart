"""Validation of user-facing values.

Each function raises ``ValueError`` when a value is not one the charts accept,
so the fronts fail early with one message instead of deep inside matplotlib.
"""

import math
from collections import defaultdict
from datetime import date, datetime
from numbers import Real

from typing import List, Optional

import matplotlib.dates as mdates
import numpy as np

from ...constants import (
    ARROW_STYLE,
    BANDWIDTH,
    BASELINE,
    DATE_FORMAT,
    EMPHASIS,
    GANTT_SORT_KEY,
    GANTT_VALUE,
    LABEL_POSITION,
    NODE_LABEL_POSITION,
    NETWORK_LAYOUT,
    RANK,
    RIDGELINE_SCALE,
    SCALE,
    SORT,
    VIOLIN_INNER,
    WEEKDAY,
)

BANDWIDTH_RULES = (BANDWIDTH.SCOTT, BANDWIDTH.SILVERMAN)
# the kinds of axis a data column asks for (ADR 0037)
AXIS_TEMPORAL = "temporal"
AXIS_NUMERIC = "numeric"
AXIS_CATEGORICAL = "categorical"
EMPHASIS_ROLES = (EMPHASIS.BACKGROUND, EMPHASIS.HIGHLIGHT)
RANK_RULES = (RANK.VALUE_DESCENDING, RANK.VALUE_ASCENDING, RANK.GIVEN)
LABEL_POSITIONS = (LABEL_POSITION.START, LABEL_POSITION.END, LABEL_POSITION.BOTH)
NODE_LABEL_POSITIONS = (NODE_LABEL_POSITION.CENTER, NODE_LABEL_POSITION.ABOVE)
STACK_BASELINES = (
    BASELINE.ZERO,
    BASELINE.PERCENT,
    BASELINE.SYM,
    BASELINE.WIGGLE,
    BASELINE.WEIGHTED_WIGGLE,
)


def validate_bandwidth(bandwidth) -> None:
    """Raise unless `bandwidth` is None, a bandwidth rule, or a number."""

    if bandwidth is not None and not (
        bandwidth in BANDWIDTH_RULES
        or (isinstance(bandwidth, (int, float)) and not isinstance(bandwidth, bool))
    ):
        raise ValueError(
            f"Invalid `bandwidth` value {bandwidth!r}. "
            f"Must be None, one of {BANDWIDTH_RULES}, or a number."
        )


RIDGELINE_SCALES = (RIDGELINE_SCALE.PER_ROW, RIDGELINE_SCALE.COMMON)
RIDGELINE_INNERS = (VIOLIN_INNER.MEDIAN, VIOLIN_INNER.QUARTILES)


def validate_overlap(overlap) -> float:
    """Validate a ridgeline row overlap: a number in `[0, 1]` (ADR 0047)."""

    if (
        not isinstance(overlap, Real)
        or isinstance(overlap, bool)
        or not 0 <= overlap <= 1
    ):
        raise ValueError(f"Invalid `overlap` value {overlap!r}. Must be in [0, 1].")
    return float(overlap)


def validate_ridgeline_scale(normalize):
    """Validate a ridgeline density scale; None means `PER_ROW`."""

    if normalize is None:
        return RIDGELINE_SCALE.DEFAULT
    if normalize not in RIDGELINE_SCALES:
        raise ValueError(
            f"Invalid `normalize` value {normalize!r}. "
            f"Must be one of {RIDGELINE_SCALES} or None."
        )
    return normalize


def validate_ridgeline_inner(inner):
    """Validate the ridgeline inner marks: the violin's marks without the box."""

    if inner is not None and inner not in RIDGELINE_INNERS:
        raise ValueError(
            f"Invalid `inner` value {inner!r}. "
            f"Must be one of {RIDGELINE_INNERS} or None."
        )
    return inner


def validate_ridge_marks(fill: bool, show_outline: bool) -> None:
    """Raise when a ridgeline would draw neither the fill nor the outline."""

    if not fill and not show_outline:
        raise ValueError(
            "`fill` and `show_outline` cannot both be False: no ridge would be drawn."
        )


def validate_span_bounds(span: dict, lo: str, hi: str) -> None:
    """Raise unless a reference band sets at least one of its two bounds."""

    if not isinstance(span, dict) or (span.get(lo) is None and span.get(hi) is None):
        raise ValueError(
            f"A reference band needs at least one bound: set `{lo}`, `{hi}`, or both."
        )


def validate_point_labels(label, show_values) -> None:
    """Raise when a scatter chart asks for point labels and value labels at once."""

    if label is not None and show_values:
        raise ValueError(
            "`label` and `show_values` cannot be combined: a point carries "
            "either its label or its value."
        )


def validate_value_step(step):
    """Validate a value-label step: None or a positive whole number."""

    if step is None:
        return None
    if isinstance(step, bool) or not isinstance(step, int) or step < 1:
        raise ValueError(
            f"Invalid `value_step` value {step!r}. Must be None or a positive integer."
        )
    return step


def validate_baseline(baseline):
    """Validate a stacked area baseline; None means the zero baseline."""

    if baseline is None:
        return BASELINE.ZERO
    if baseline not in STACK_BASELINES:
        raise ValueError(
            f"Invalid `baseline` value {baseline!r}. "
            f"Must be one of {STACK_BASELINES} or None."
        )
    return baseline


def validate_rank_by(rank_by):
    """Validate a bump chart ranking rule; None means highest value first."""

    if rank_by is None:
        return RANK.DEFAULT
    if rank_by not in RANK_RULES:
        raise ValueError(
            f"Invalid `rank_by` value {rank_by!r}. Must be one of {RANK_RULES} or None."
        )
    return rank_by


def validate_label_position(position):
    """Validate an end label position; None means beside the last point."""

    if position is None:
        return LABEL_POSITION.DEFAULT
    if position not in LABEL_POSITIONS:
        raise ValueError(
            f"Invalid `label_position` value {position!r}. "
            f"Must be one of {LABEL_POSITIONS} or None."
        )
    return position


def validate_node_label_position(position):
    """Validate a node label position; None means on the marker."""

    if position is None:
        return NODE_LABEL_POSITION.DEFAULT
    if position not in NODE_LABEL_POSITIONS:
        raise ValueError(
            f"Invalid `label_position` value {position!r}. "
            f"Must be one of {NODE_LABEL_POSITIONS} or None."
        )
    return position


def validate_line_curve(curve) -> float:
    """Validate a bump line curve: None (straight) or a number in [0, 1]."""

    if curve is None:
        return 0.0
    if not _is_number(curve) or not 0 <= curve <= 1:
        raise ValueError(
            f"Invalid `line_curve` value {curve!r}. Must be None or a number in [0, 1]."
        )
    return float(curve)


def validate_given_ranks(ranks) -> None:
    """Raise unless every present rank is a positive whole number; NaN is a gap."""

    for rank in ranks:
        if _is_number(rank) and math.isnan(rank):
            continue
        if not _is_number(rank) or not math.isfinite(rank) or rank < 1 or rank % 1:
            raise ValueError(
                f"`rank_by` GIVEN reads `y` as the rank, which must be a positive "
                f"integer; got {rank!r}."
            )


def validate_shared_x(columns) -> None:
    """Raise unless every `x` column holds the same values in the same order."""

    if not columns or columns[0] is None:
        raise ValueError("A stacked area chart requires the `x` and `y` columns.")
    first = list(columns[0])
    for i, column in enumerate(columns[1:], start=1):
        if column is None or list(column) != first:
            raise ValueError(
                "Every stacked area series must share the same `x` values in the "
                f"same order; series {i} differs from series 0."
            )


def validate_axis_kinds(kinds, column: str = "`x`") -> Optional[str]:
    """The one axis kind the layers' `column` asks for; a temporal/numeric mix raises.

    Kinds are the `AXIS_*` values, or None for a layer without x. Time wins
    over category positions, which sit on their own index.
    """

    present = {kind for kind in kinds if kind is not None}
    if {AXIS_TEMPORAL, AXIS_NUMERIC} <= present:
        raise ValueError(
            f"Cannot mix temporal and numeric {column} values in one panel. "
            "Every chart sharing an axis must give datetimes or numbers, not both."
        )
    for kind in (AXIS_TEMPORAL, AXIS_NUMERIC, AXIS_CATEGORICAL):
        if kind in present:
            return kind
    return None


def validate_log_values(parameter: str, role: str, scale, values, hint=None) -> None:
    """Reject a value a `log` scale cannot show: zero or below.

    `parameter` is the scale setting as the user spells it, `role` the axis it
    addresses ("value", "category", "secondary value"). NaN and missing values
    are skipped; every other scale accepts any value.
    """

    if scale != SCALE.LOG or values is None:
        return
    values = np.asarray(values, dtype=float).ravel()
    offending = values[np.isfinite(values) & (values <= 0)]
    if offending.size == 0:
        return
    message = (
        f"`{parameter}` 'log' cannot show the value {offending[0]:g} on the "
        f"{role} axis: a log scale needs values above zero. Use 'symlog' or "
        "'asinh' for data at or below zero."
    )
    raise ValueError(f"{message} {hint}" if hint else message)


def validate_ticks_format(value, axis: str, dated: bool) -> None:
    """Raise unless a tick format can label the axis it is set on.

    A dated axis takes a `strftime` pattern; any other axis a value format,
    i.e. a `{x}`, `{}`, or `%` string that formats a number.
    """

    if value is None or value == DATE_FORMAT.AUTO:
        return
    name = f"`{axis}ticks_format`"
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a format string, got {value!r}.")
    if dated:
        if "{" in value or "%" not in value:
            raise ValueError(
                f"{name} {value!r} is a value format, but the {axis} axis holds "
                "dates. Pass a DATE_FORMAT member or a `strftime` pattern."
            )
        return
    try:
        if "{x" in value:
            value.format(x=1.0)
        elif "{" in value:
            value.format(1.0)
        else:
            value % (1.0,)
    except (ValueError, TypeError, KeyError, IndexError) as error:
        raise ValueError(
            f"{name} {value!r} cannot format a number ({error}). On a numeric "
            "axis pass a VALUE_FORMAT member or a `{x:.1f}`, `{:.1f}`, or "
            "`%.1f` style string; DATE_FORMAT patterns apply to datetime axes."
        ) from None


def validate_emphasis(value, context: str = "emphasis"):
    """Validate a single emphasis role; None means no emphasis."""

    if value is not None and value not in EMPHASIS_ROLES:
        raise ValueError(
            f"Invalid {context} value {value!r}. "
            f"Must be '{EMPHASIS.BACKGROUND}', '{EMPHASIS.HIGHLIGHT}', or None."
        )
    return value


SORT_ORDERS = (SORT.ASCENDING, SORT.DESCENDING)


def validate_sort(value):
    """Validate a category sort order; None (`SORT.NONE`) means input order."""

    if value is None:
        return None
    if value not in SORT_ORDERS:
        raise ValueError(
            f"Invalid `sort` value {value!r}. Must be one of {SORT_ORDERS} or None."
        )
    return value


def validate_sort_by(sort, sort_by, subtitles: list) -> None:
    """Raise unless `sort_by` names one of the series subtitles under a `sort`."""

    if sort_by is None:
        return
    if sort is None:
        raise ValueError("`sort_by` names the series to sort by; pass `sort` as well.")
    if sort_by not in subtitles:
        raise ValueError(
            f"`sort_by` {sort_by!r} names no series; the series subtitles "
            f"are {subtitles!r}."
        )


# the value each rule reads against: a count of records or a threshold
EMPHASIS_RULE_COUNTS = ("top", "bottom")
EMPHASIS_RULE_THRESHOLDS = ("above", "below", "between")
# how a group or series rule summarises its values into one (ADR 0045)
EMPHASIS_RULE_SUMMARIES = ("mean", "median", "min", "max", "sum")


def validate_emphasis_rule(rule, by: Optional[str] = None):
    """Validate an emphasis rule; None means no rule (ADR 0042, ADR 0045).

    A rule is a one-key dict: `above`/`below` a number (strict), `between`
    a `(lo, hi)` pair (inclusive), `top`/`bottom` a positive integer. On
    group and series fronts it may also carry a `by` summary.

    Args:
        rule: The rule to validate.
        by: The front's default summary; None when the front reads one value
            per unit and so rejects a `by` key.

    Returns:
        The `(key, value, by)` triple of the rule, or None.
    """

    if rule is None:
        return None
    if not isinstance(rule, dict):
        raise ValueError(
            f"Invalid `emphasis_rule` value {rule!r}. Must be a one-key dict: "
            f"one of {EMPHASIS_RULE_THRESHOLDS + EMPHASIS_RULE_COUNTS} to a value."
        )
    if "by" in rule:
        if by is None:
            raise ValueError(
                "`emphasis_rule` `by` summarises a group or series; this chart "
                "reads one value per record or cell, so it takes no `by`."
            )
        if rule["by"] not in EMPHASIS_RULE_SUMMARIES:
            raise ValueError(
                f"Invalid `emphasis_rule` `by` value {rule['by']!r}. "
                f"Must be one of {EMPHASIS_RULE_SUMMARIES}."
            )
        by = rule["by"]
        rule = {key: value for key, value in rule.items() if key != "by"}
    if len(rule) != 1:
        raise ValueError(
            f"`emphasis_rule` takes exactly one key, got {sorted(rule)!r}. "
            "Tag the records' `emphasis` directly to combine conditions."
        )
    ((key, value),) = rule.items()
    if key in EMPHASIS_RULE_COUNTS:
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(
                f"`emphasis_rule` `{key}` must be a positive integer, got {value!r}."
            )
    elif key == "between":
        bounds = value if isinstance(value, (tuple, list)) else ()
        if len(bounds) != 2 or not all(_is_number(bound) for bound in bounds):
            raise ValueError(
                f"`emphasis_rule` `between` takes a `(lo, hi)` pair of numbers, "
                f"got {value!r}."
            )
        if bounds[0] > bounds[1]:
            raise ValueError(
                f"`emphasis_rule` `between` bounds are reversed: lo {bounds[0]!r} "
                f"is above hi {bounds[1]!r}."
            )
    elif key in EMPHASIS_RULE_THRESHOLDS:
        if not _is_number(value):
            raise ValueError(
                f"`emphasis_rule` `{key}` must be a number, got {value!r}."
            )
    else:
        raise ValueError(
            f"Unknown `emphasis_rule` key `{key}`. "
            f"Must be one of {EMPHASIS_RULE_THRESHOLDS + EMPHASIS_RULE_COUNTS}."
        )
    return key, value, by


def _is_number(value) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool)


SANKEY_LINK_COLORS = ("source", "target", "grey")


def validate_sankey_links(links) -> None:
    """Raise unless `links` is a non-empty list of positive, non-self links."""

    if not isinstance(links, list) or not links:
        raise ValueError("A Sankey chart requires a non-empty `links` list.")
    for i, record in enumerate(links):
        if not isinstance(record, dict) or not all(
            key in record for key in ("source", "target", "value")
        ):
            raise ValueError(
                f"Sankey link {i} must be a dict with `source`, `target`, and `value`."
            )
        value = record["value"]
        if isinstance(value, bool) or not isinstance(value, Real) or not value > 0:
            raise ValueError(f"Sankey link {i} must have a `value` greater than 0.")
        if record["source"] == record["target"]:
            raise ValueError(
                f"Sankey link {i} joins {record['source']!r} to itself; "
                "self-links are not drawn."
            )


def validate_sankey_link_color(value):
    """Validate the `plot_sankey_link_color` mode; None means "source"."""

    if value is None:
        return "source"
    if value not in SANKEY_LINK_COLORS:
        raise ValueError(
            f"Invalid `plot_sankey_link_color` value {value!r}. "
            f"Must be one of {SANKEY_LINK_COLORS}."
        )
    return value


def first_seen_nodes(links) -> list:
    """The node names of source/target records in first-seen input order."""

    nodes = []
    for record in links:
        for node in (record["source"], record["target"]):
            if node not in nodes:
                nodes.append(node)
    return nodes


def infer_sankey_columns(links) -> list:
    """Columns as the longest path from any source; first-seen order within.

    Raises:
        ValueError: If the links form a cycle.
    """

    successors = defaultdict(list)
    predecessors = defaultdict(list)
    for record in links:
        successors[record["source"]].append(record["target"])
        predecessors[record["target"]].append(record["source"])
    nodes = first_seen_nodes(links)

    depth = {}

    def longest_path(node, trail):
        if node in trail:
            raise ValueError(
                "Sankey links must not form a cycle; "
                f"{node!r} flows back into itself."
            )
        if node not in depth:
            depth[node] = max(
                (longest_path(p, trail | {node}) + 1 for p in predecessors[node]),
                default=0,
            )
        return depth[node]

    for node in nodes:
        longest_path(node, frozenset())

    columns = [[] for _ in range(max(depth.values()) + 1)]
    for node in nodes:
        columns[depth[node]].append(node)
    return columns


def validate_sankey_nodes(nodes, links) -> None:
    """Raise unless `nodes` is a list of columns naming each link node once."""

    if not isinstance(nodes, list) or not all(isinstance(c, list) for c in nodes):
        raise ValueError(
            "`nodes` must be a list of columns, each a list of node names."
        )
    named = [node for column in nodes for node in column]
    if len(named) != len(set(named)):
        raise ValueError("`nodes` names a node more than once.")
    linked = set(first_seen_nodes(links))
    missing = linked - set(named)
    extra = set(named) - linked
    if missing or extra:
        raise ValueError(
            "`nodes` must name exactly the nodes in `links`; "
            f"missing {sorted(missing)}, unknown {sorted(extra)}."
        )


def _positive_number(value) -> bool:
    return _is_number(value) and value > 0


# the data list is level 1; a record nests to this depth (ADR 0032)
TREEMAP_MAX_DEPTH = 4


def treemap_record_total(record) -> float:
    """A record's value, or the sum of its descendants' for a group."""

    children = record.get("children")
    if children is None:
        return record["value"]
    return sum(treemap_record_total(child) for child in children)


def validate_treemap_records(records) -> None:
    """Raise unless `records` is a non-empty list of valid treemap records.

    A record is a dict with a `label` and either a `value` above zero or a
    `children` list of such records; records nest to `TREEMAP_MAX_DEPTH`
    levels, siblings have unique labels, and a parent carrying a `value`
    must match its children's total (ADR 0028, ADR 0032). An `emphasis`
    key on any record takes the emphasis roles.
    """

    if not isinstance(records, list) or not records:
        raise ValueError("A treemap requires a non-empty `data` list of records.")
    for i, record in enumerate(records):
        _validate_treemap_record(record, f"Treemap record {i}", depth=1)
    _validate_unique_labels(records, "Treemap records")


def _validate_unique_labels(records, name: str) -> None:
    """Siblings are keyed by label: for colors, the legend, and the reader."""

    seen = set()
    for record in records:
        if record["label"] in seen:
            raise ValueError(
                f"{name} must have unique labels; {record['label']!r} repeats."
            )
        seen.add(record["label"])


def _validate_treemap_record(record, name: str, depth: int) -> None:
    if not isinstance(record, dict) or "label" not in record:
        raise ValueError(f"{name} must be a dict with a `label`.")
    label = record["label"]
    validate_emphasis(record.get("emphasis"), f"{name} ({label!r}) `emphasis`")
    children = record.get("children")
    if children is None:
        if not _positive_number(record.get("value")):
            raise ValueError(f"{name} ({label!r}) must have a `value` greater than 0.")
        return
    if depth >= TREEMAP_MAX_DEPTH:
        raise ValueError(
            f"{name} ({label!r}) nests deeper than four levels; "
            "a record at the fourth level cannot carry `children`."
        )
    if not isinstance(children, list) or not children:
        raise ValueError(f"{name} ({label!r}) must have a non-empty `children` list.")
    for j, child in enumerate(children):
        _validate_treemap_record(child, f"{name} ({label!r}) child {j}", depth + 1)
    _validate_unique_labels(children, f"{name} ({label!r}) children")
    value = record.get("value")
    if value is not None:
        total = treemap_record_total(record)
        if not _positive_number(value) or not math.isclose(value, total, rel_tol=1e-9):
            raise ValueError(
                f"{name} ({label!r}) has `value` {value!r} but its children sum "
                f"to {total!r}; omit the value or make it the sum."
            )


NETWORK_LAYOUTS = (
    NETWORK_LAYOUT.SPRING,
    NETWORK_LAYOUT.WEIGHTED,
    NETWORK_LAYOUT.GROUPED,
    NETWORK_LAYOUT.CIRCULAR,
    NETWORK_LAYOUT.FIXED,
)
# the headless connector looks; directedness owns the arrowhead (ADR 0029)
NETWORK_EDGE_STYLES = (ARROW_STYLE.CURVE, ARROW_STYLE.STRAIGHT)


def infer_network_nodes(edges) -> list:
    """Node records for the edges' endpoints in first-seen order (ADR 0029)."""

    return [{"id": node_id} for node_id in first_seen_nodes(edges)]


def validate_network_records(nodes, edges, layout) -> None:
    """Raise unless the network's nodes, edges, and layout are well formed.

    A node is a dict with a unique `id`; `size`, when given, is above zero,
    `emphasis` takes the emphasis roles, and under `NETWORK_LAYOUT.FIXED`
    every node carries `x` and `y`. An edge is a dict with a `source` and a
    `target` naming known nodes, never the same one, and a `weight` above
    zero when given. `nodes` is the explicit list or the inferred one; it is
    never `None` here (ADR 0029).
    """

    if layout not in NETWORK_LAYOUTS:
        raise ValueError(
            f"Invalid network `layout` value {layout!r}. "
            f"Must be one of {NETWORK_LAYOUTS}."
        )
    if not isinstance(edges, list):
        raise ValueError("A network chart requires an `edges` list of records.")
    for i, record in enumerate(edges):
        name = f"Network edge {i}"
        if not isinstance(record, dict) or not all(
            key in record for key in ("source", "target")
        ):
            raise ValueError(f"{name} must be a dict with `source` and `target`.")
        weight = record.get("weight")
        if weight is not None and not _positive_number(weight):
            raise ValueError(f"{name} must have a `weight` greater than 0.")
        if record["source"] == record["target"]:
            raise ValueError(
                f"{name} joins {record['source']!r} to itself; "
                "self-loops are not drawn."
            )

    if not isinstance(nodes, list):
        raise ValueError("A network chart's `nodes` must be a list of records.")
    if not nodes:
        raise ValueError("A network chart requires at least one node.")

    ids = set()
    for i, record in enumerate(nodes):
        name = f"Network node {i}"
        if not isinstance(record, dict) or "id" not in record:
            raise ValueError(f"{name} must be a dict with an `id`.")
        node_id = record["id"]
        if node_id in ids:
            raise ValueError(
                f"Network nodes must have unique ids; {node_id!r} repeats."
            )
        ids.add(node_id)
        size = record.get("size")
        if size is not None and not _positive_number(size):
            raise ValueError(f"{name} ({node_id!r}) must have a `size` greater than 0.")
        validate_emphasis(record.get("emphasis"), f"{name} ({node_id!r}) `emphasis`")
        if layout == NETWORK_LAYOUT.FIXED:
            for key in ("x", "y"):
                if not isinstance(record.get(key), Real):
                    raise ValueError(
                        f"{name} ({node_id!r}) lacks `{key}`; the fixed layout "
                        "needs `x` and `y` on every node."
                    )

    for i, record in enumerate(edges):
        for key in ("source", "target"):
            if record[key] not in ids:
                raise ValueError(
                    f"Network edge {i} names an unknown node {record[key]!r} "
                    f"as its `{key}`."
                )


def validate_network_edge_style(value):
    """Validate the `plot_network_edge_style` look; None means the curve."""

    if value is None:
        return ARROW_STYLE.CURVE
    if value in (ARROW_STYLE.ARROW, ARROW_STYLE.CURVE_ARROW, ARROW_STYLE.TOUCHING):
        raise ValueError(
            f"`plot_network_edge_style` does not take {value!r}: a network edge "
            f"is headless, pass `directed=True` for arrowheads. Must be one of "
            f"{NETWORK_EDGE_STYLES}."
        )
    if value not in NETWORK_EDGE_STYLES:
        raise ValueError(
            f"Invalid `plot_network_edge_style` value {value!r}. "
            f"Must be one of {NETWORK_EDGE_STYLES}."
        )
    return value


# the temporal types a calendar date may be (ADR 0037); strings never parse
CALENDAR_DATE_TYPES = "`date`, `datetime`, `numpy.datetime64`, or pandas `Timestamp`"
WEEK_STARTS = (WEEKDAY.MONDAY, WEEKDAY.SUNDAY)


def validate_calendar_dates(dates) -> List[date]:
    """The calendar dates as `date` objects; a value that is not temporal raises."""

    normalized = []
    for value in dates:
        if isinstance(value, np.datetime64):
            value = value.astype("datetime64[us]").item()
        if isinstance(value, datetime):
            value = value.date()
        if not isinstance(value, date):
            raise ValueError(
                f"Invalid calendar date {value!r}. Dates must be "
                f"{CALENDAR_DATE_TYPES} objects; date strings are never parsed."
            )
        normalized.append(value)
    return normalized


def validate_unique_dates(dates: List[date]) -> None:
    """Raise when a calendar date appears twice, naming the first duplicate."""

    seen = set()
    for value in dates:
        if value in seen:
            raise ValueError(
                f"Duplicate calendar date {value.isoformat()}. Every date holds "
                "one value; aggregate the duplicates before charting."
            )
        seen.add(value)


def validate_calendar_year(year, years) -> None:
    """Raise unless `year` is None or one of the years the dates span."""

    if year is None:
        return
    if isinstance(year, bool) or not isinstance(year, int):
        raise ValueError(f"Invalid `year` value {year!r}. Must be an integer or None.")
    if year not in years:
        raise ValueError(
            f"No dates in year {year}; the data spans {min(years)}-{max(years)}."
        )


def validate_week_start(value):
    """Validate a calendar week start; None means the theme default."""

    if value is not None and value not in WEEK_STARTS:
        raise ValueError(
            f"Invalid `week_start` value {value!r}. Must be one of {WEEK_STARTS} or None."
        )
    return value


GANTT_VALUES = (GANTT_VALUE.DURATION, GANTT_VALUE.PROGRESS)
GANTT_SORT_KEYS = (GANTT_SORT_KEY.START, GANTT_SORT_KEY.GROUP)


def validate_gantt_show_values(value):
    """Validate a gantt value label; None or False prints none."""

    if value is None or value is False:
        return None
    if value not in GANTT_VALUES:
        raise ValueError(
            f"Invalid `show_values` value {value!r}. "
            f"Must be one of {GANTT_VALUES} or None."
        )
    return value


def validate_gantt_sort_by(sort, sort_by) -> str:
    """Validate a gantt sort key; None means by start."""

    if sort_by is None:
        return GANTT_SORT_KEY.DEFAULT
    if sort_by not in GANTT_SORT_KEYS:
        raise ValueError(
            f"Invalid `sort_by` value {sort_by!r}. "
            f"Must be one of {GANTT_SORT_KEYS} or None."
        )
    if sort is None:
        raise ValueError("`sort_by` names the key to sort by; pass `sort` as well.")
    return sort_by


def _task_time(record: dict, key: str, index: int) -> float:
    """A task's `start` or `end` as a date number; a non-temporal value raises."""

    value = record.get(key)
    # a datetime is a date; pandas Timestamps are datetimes
    if not isinstance(value, (date, np.datetime64)):
        raise ValueError(
            f"Invalid `{key}` value {value!r} in task record {index}. Must be "
            f"{CALENDAR_DATE_TYPES} objects; date strings are never parsed."
        )
    return float(mdates.date2num(value))


def validate_gantt_tasks(records) -> None:
    """Raise unless `records` is a list of well-formed, consistent task records.

    Each record names a unique `task`, a temporal `start` and `end` with the
    end never before the start, an optional `progress` in [0, 1], and a
    `depends_on` list naming only tasks of the same chart.
    """

    if not isinstance(records, list) or not records:
        raise ValueError(
            "GanttChart `data` must be a non-empty list of task records "
            "`{task, start, end}`, or a list of such lists."
        )
    names = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict) or not isinstance(record.get("task"), str):
            raise ValueError(
                f"Task record {index} must be a dict with a string `task` name; "
                f"got {record!r}."
            )
        name = record["task"]
        if name in names:
            raise ValueError(
                f"Duplicate task name {name!r}. Every task names one row; "
                "give each task a unique name."
            )
        names.add(name)
        start = _task_time(record, "start", index)
        end = _task_time(record, "end", index)
        if end < start:
            raise ValueError(
                f"Task {name!r} ends before it starts: `end` {record['end']!r} "
                f"is before `start` {record['start']!r}."
            )
        progress = record.get("progress")
        if progress is not None and (
            not _is_number(progress) or not 0 <= progress <= 1
        ):
            raise ValueError(
                f"Invalid `progress` value {progress!r} for task {name!r}. "
                "Must be a number in [0, 1] or None."
            )
        validate_emphasis(record.get("emphasis"), f"task {name!r} `emphasis`")
    for record in records:
        depends_on = record.get("depends_on")
        if depends_on is None:
            continue
        if not isinstance(depends_on, list):
            raise ValueError(
                f"`depends_on` of task {record['task']!r} must be a list of task "
                f"names; got {depends_on!r}."
            )
        for dependency in depends_on:
            if dependency not in names:
                raise ValueError(
                    f"Task {record['task']!r} depends on unknown task "
                    f"{dependency!r}. `depends_on` names tasks of the same chart."
                )


def validate_gantt_groups(records, sort_by) -> None:
    """Raise when rows sort by group but no task carries a `group`."""

    if sort_by == GANTT_SORT_KEY.GROUP and not any(
        record.get("group") is not None for record in records
    ):
        raise ValueError(
            '`sort_by="group"` clusters the rows by task group, but no task '
            "carries a `group` key."
        )
