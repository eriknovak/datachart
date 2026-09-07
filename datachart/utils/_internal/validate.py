"""Validation of user-facing values.

Each function raises ``ValueError`` when a value is not one the charts accept,
so the fronts fail early with one message instead of deep inside matplotlib.
"""

import math
from collections import defaultdict
from numbers import Real

from ...constants import ARROW_STYLE, BANDWIDTH, BASELINE, EMPHASIS, NETWORK_LAYOUT

BANDWIDTH_RULES = (BANDWIDTH.SCOTT, BANDWIDTH.SILVERMAN)
EMPHASIS_ROLES = (EMPHASIS.BACKGROUND, EMPHASIS.HIGHLIGHT)
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


def validate_emphasis(value, context: str = "emphasis"):
    """Validate a single emphasis role; None means no emphasis."""

    if value is not None and value not in EMPHASIS_ROLES:
        raise ValueError(
            f"Invalid {context} value {value!r}. "
            f"Must be '{EMPHASIS.BACKGROUND}', '{EMPHASIS.HIGHLIGHT}', or None."
        )
    return value


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


def sankey_node_order(links) -> list:
    """The node names in first-seen input order."""

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
    nodes = sankey_node_order(links)

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
    linked = set(sankey_node_order(links))
    missing = linked - set(named)
    extra = set(named) - linked
    if missing or extra:
        raise ValueError(
            "`nodes` must name exactly the nodes in `links`; "
            f"missing {sorted(missing)}, unknown {sorted(extra)}."
        )


def _positive_number(value) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool) and value > 0


def validate_treemap_records(records) -> None:
    """Raise unless `records` is a non-empty list of valid treemap records.

    A record is a dict with a `label` and either a `value` above zero or a
    `children` list of such records; children nest one level only, and a
    parent carrying a `value` must match its children's sum (ADR 0028). An
    `emphasis` key on any record takes the emphasis roles.
    """

    if not isinstance(records, list) or not records:
        raise ValueError("A treemap requires a non-empty `data` list of records.")
    for i, record in enumerate(records):
        _validate_treemap_record(record, f"Treemap record {i}", nested=False)
    _validate_unique_labels(records, "Treemap records")
    for record in records:
        if record.get("children") is not None:
            name = f"Treemap record {record['label']!r} children"
            _validate_unique_labels(record["children"], name)


def _validate_unique_labels(records, name: str) -> None:
    """Siblings are keyed by label: for colors, the legend, and the reader."""

    seen = set()
    for record in records:
        if record["label"] in seen:
            raise ValueError(
                f"{name} must have unique labels; {record['label']!r} repeats."
            )
        seen.add(record["label"])


def _validate_treemap_record(record, name: str, nested: bool) -> None:
    if not isinstance(record, dict) or "label" not in record:
        raise ValueError(f"{name} must be a dict with a `label`.")
    label = record["label"]
    validate_emphasis(record.get("emphasis"), f"{name} ({label!r}) `emphasis`")
    children = record.get("children")
    if children is None:
        if not _positive_number(record.get("value")):
            raise ValueError(f"{name} ({label!r}) must have a `value` greater than 0.")
        return
    if nested:
        raise ValueError(
            f"{name} ({label!r}) nests deeper than one level; "
            "a child cannot carry `children`."
        )
    if not isinstance(children, list) or not children:
        raise ValueError(f"{name} ({label!r}) must have a non-empty `children` list.")
    for j, child in enumerate(children):
        _validate_treemap_record(child, f"{name} ({label!r}) child {j}", nested=True)
    value = record.get("value")
    if value is not None:
        total = sum(child["value"] for child in children)
        if not _positive_number(value) or not math.isclose(value, total, rel_tol=1e-9):
            raise ValueError(
                f"{name} ({label!r}) has `value` {value!r} but its children sum "
                f"to {total!r}; omit the value or make it the sum."
            )


NETWORK_LAYOUTS = (NETWORK_LAYOUT.SPRING, NETWORK_LAYOUT.CIRCULAR, NETWORK_LAYOUT.FIXED)
# the headless connector looks; directedness owns the arrowhead (ADR 0029)
NETWORK_EDGE_STYLES = (ARROW_STYLE.CURVE, ARROW_STYLE.STRAIGHT)


def validate_network_records(nodes, edges, layout) -> list:
    """Validate a network's nodes, edges, and layout; return the node records.

    A node is a dict with a unique `id`; `size`, when given, is above zero,
    `emphasis` takes the emphasis roles, and under `NETWORK_LAYOUT.FIXED`
    every node carries `x` and `y`. An edge is a dict with a `source` and a
    `target` naming known nodes, never the same one, and a `weight` above
    zero when given. Without `nodes`, the node set is the edges' endpoints
    in first-seen order (ADR 0029).
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

    if nodes is None:
        seen = {}
        for record in edges:
            seen.setdefault(record["source"], None)
            seen.setdefault(record["target"], None)
        nodes = [{"id": node_id} for node_id in seen]
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
    return nodes


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
