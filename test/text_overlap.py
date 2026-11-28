"""The overlap check the text-placement tests share: two drawn texts clash."""

from itertools import combinations

# two texts clash when their boxes overlap by more than this, in pixels, both ways
OVERLAP_TOLERANCE_PX = 1


def boxes_overlap(a, b) -> bool:
    """Two window extents overlap by more than the tolerance both ways."""

    return (
        min(a.x1, b.x1) - max(a.x0, b.x0) > OVERLAP_TOLERANCE_PX
        and min(a.y1, b.y1) - max(a.y0, b.y0) > OVERLAP_TOLERANCE_PX
    )


def overlapping_pairs(texts, renderer) -> list:
    """The (text, text) string pairs of `texts` whose drawn boxes overlap."""

    boxes = [(text.get_text(), text.get_window_extent(renderer)) for text in texts]
    return [
        (a, b)
        for (a, box_a), (b, box_b) in combinations(boxes, 2)
        if boxes_overlap(box_a, box_b)
    ]
