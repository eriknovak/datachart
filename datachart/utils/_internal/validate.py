"""Validation of user-facing values.

Each function raises ``ValueError`` when a value is not one the charts accept,
so the fronts fail early with one message instead of deep inside matplotlib.
"""

from collections import defaultdict
from numbers import Real

from ...constants import BANDWIDTH, BASELINE, EMPHASIS

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
