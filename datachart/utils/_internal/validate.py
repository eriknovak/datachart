"""Validation of user-facing values.

Each function raises ``ValueError`` when a value is not one the charts accept,
so the fronts fail early with one message instead of deep inside matplotlib.
"""

from ...constants import BANDWIDTH, EMPHASIS

BANDWIDTH_RULES = (BANDWIDTH.SCOTT, BANDWIDTH.SILVERMAN)
EMPHASIS_ROLES = (EMPHASIS.BACKGROUND, EMPHASIS.HIGHLIGHT)


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


def validate_emphasis(value, context: str = "emphasis"):
    """Validate a single emphasis role; None means no emphasis."""

    if value is not None and value not in EMPHASIS_ROLES:
        raise ValueError(
            f"Invalid {context} value {value!r}. "
            f"Must be '{EMPHASIS.BACKGROUND}', '{EMPHASIS.HIGHLIGHT}', or None."
        )
    return value
