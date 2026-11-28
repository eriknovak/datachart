"""Bubble chart sizes and legends.

A bubble's area is proportional to its value on one scale per axes, the
largest bubbles draw first with every per-point datum paired, and legend
markers keep the base marker size, not the data size.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.collections import PathCollection
from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Annotation

from datachart.charts import ScatterChart
from datachart.config import config
from datachart.constants import EMPHASIS
from datachart.utils import Panel

BUBBLES = [
    {"x": i, "y": i, "population": population, "group": "a" if i % 2 else "b"}
    for i, population in enumerate([1, 50, 500, 1000])
]


@pytest.fixture(autouse=True)
def _close_figures():
    yield
    plt.close("all")


def _legend_sizes(fig):
    legend = fig.axes[0].get_legend()
    return [
        handle.get_sizes().tolist()
        for handle in legend.legend_handles
        if isinstance(handle, PathCollection)
    ]


def test_bubble_legend_uses_theme_marker_size():
    fig = ScatterChart(
        data=BUBBLES,
        hue="group",
        size="population",
        size_range=(20, 800),
        show_legend=True,
    )
    assert _legend_sizes(fig) == [[config["plot_scatter_size"]]] * 2


def test_bubble_legend_follows_style_marker_size():
    fig = ScatterChart(
        data=BUBBLES,
        subtitle="cities",
        size="population",
        style={"plot_scatter_size": 64},
        show_legend=True,
    )
    assert _legend_sizes(fig) == [[64]]


def test_plain_scatter_legend_keeps_marker_size():
    fig = ScatterChart(
        data=BUBBLES,
        hue="group",
        style={"plot_scatter_size": 64},
        show_legend=True,
    )
    assert _legend_sizes(fig) == [[64], [64]]


def _sizes_by_point(ax):
    """Each drawn point's marker area, keyed by its (x, y)."""
    sizes = {}
    for collection in ax.collections:
        areas = collection.get_sizes()
        for i, point in enumerate(collection.get_offsets()):
            sizes[tuple(point)] = float(areas[i if len(areas) > 1 else 0])
    return sizes


def test_equal_sizes_across_hue_groups_draw_equal():
    data = [
        {"x": 0, "y": 0, "size": 10, "group": "a"},
        {"x": 1, "y": 1, "size": 30, "group": "a"},
        {"x": 2, "y": 2, "size": 30, "group": "b"},
        {"x": 3, "y": 3, "size": 90, "group": "b"},
    ]
    fig = ScatterChart(data, hue="group", size="size", size_range=(20, 200))
    sizes = _sizes_by_point(fig.axes[0])
    assert sizes[(1.0, 1.0)] == pytest.approx(sizes[(2.0, 2.0)])
    assert sizes[(0.0, 0.0)] == pytest.approx(10 / 90 * 200)
    assert sizes[(3.0, 3.0)] == pytest.approx(200)


def test_composed_scatters_share_one_size_scale():
    small = ScatterChart(
        [{"x": 0, "y": 0, "size": 10}, {"x": 1, "y": 1, "size": 20}],
        size="size",
        size_range=(20, 200),
    )
    large = ScatterChart(
        [{"x": 2, "y": 2, "size": 20}, {"x": 3, "y": 3, "size": 110}],
        size="size",
        size_range=(20, 200),
    )
    sizes = _sizes_by_point(Panel([small, large]).axes[0])
    assert sizes[(1.0, 1.0)] == pytest.approx(sizes[(2.0, 2.0)])
    assert sizes[(0.0, 0.0)] == pytest.approx(20)
    assert sizes[(3.0, 3.0)] == pytest.approx(200)


def test_constant_sizes_draw_the_mid_size():
    data = [{"x": i, "y": i, "size": 5} for i in range(3)]
    fig = ScatterChart(data, size="size", size_range=(20, 200))
    assert set(_sizes_by_point(fig.axes[0]).values()) == {110.0}


def test_bubble_areas_are_proportional_to_values():
    data = [{"x": i, "y": i, "size": size} for i, size in enumerate([25, 50, 100])]
    fig = ScatterChart(data, size="size", size_range=(1, 200))
    sizes = _sizes_by_point(fig.axes[0])
    assert [sizes[(i, i)] for i in (0.0, 1.0, 2.0)] == pytest.approx([50, 100, 200])


def test_small_values_draw_at_the_floor():
    data = [{"x": 0, "y": 0, "size": 1}, {"x": 1, "y": 1, "size": 100}]
    fig = ScatterChart(data, size="size", size_range=(20, 200))
    assert _sizes_by_point(fig.axes[0])[(0.0, 0.0)] == pytest.approx(20)


def test_missing_size_drops_only_its_point():
    data = [
        {"x": 0, "y": 0, "size": 50},
        {"x": 1, "y": 1, "size": None},
        {"x": 2, "y": 2, "size": 100},
    ]
    fig = ScatterChart(data, size="size", size_range=(1, 200))
    sizes = _sizes_by_point(fig.axes[0])
    assert sizes == pytest.approx({(0.0, 0.0): 100, (2.0, 2.0): 200})


def test_record_without_size_key_draws_no_marker():
    data = [
        {"x": 0, "y": 0, "size": 50},
        {"x": 1, "y": 1},
        {"x": 2, "y": 2, "size": 100},
    ]
    fig = ScatterChart(data, size="size", size_range=(1, 200))
    sizes = _sizes_by_point(fig.axes[0])
    assert sizes == pytest.approx({(0.0, 0.0): 100, (2.0, 2.0): 200})


def test_negative_size_names_the_chart_and_value():
    data = [{"x": 0, "y": 0, "size": 5}, {"x": 1, "y": 1, "size": -3}]
    with pytest.raises(ValueError, match=r"(?s)-3.*cities|cities.*-3"):
        ScatterChart(data, subtitle="cities", size="size")


ORDERED = [
    {"x": i, "y": 10 * i, "size": size, "annotation": f"p{i}"}
    for i, size in enumerate([10, 100, 40, 70])
]


def _points(ax):
    return [c for c in ax.collections if len(c.get_offsets())]


def test_bubbles_draw_largest_first_with_sizes_paired():
    fig = ScatterChart(ORDERED, size="size", size_range=(1, 200))
    (collection,) = _points(fig.axes[0])
    assert collection.get_offsets().tolist() == [[1, 10], [3, 30], [2, 20], [0, 0]]
    assert collection.get_sizes().tolist() == pytest.approx([200, 140, 80, 20])


def test_each_emphasis_role_sorts_on_its_own():
    roles = [EMPHASIS.HIGHLIGHT, EMPHASIS.BACKGROUND] * 3
    data = [
        dict(x=i, y=i, size=size, emphasis=role)
        for i, (size, role) in enumerate(zip([10, 20, 90, 80, 50, 40], roles))
    ]
    fig = ScatterChart(data, size="size", size_range=(1, 90))
    highlighted, muted = _points(fig.axes[0])
    assert highlighted.get_offsets()[:, 0].tolist() == [2, 4, 0]
    assert muted.get_offsets()[:, 0].tolist() == [3, 5, 1]
    assert muted.get_zorder() < highlighted.get_zorder()


def test_hover_datum_follows_the_drawn_point():
    fig = ScatterChart(ORDERED, size="size")
    ((collection, resolve),) = fig._hover_targets
    for i, (x, y) in enumerate(collection.get_offsets()):
        assert (resolve(i)["x"], resolve(i)["y"]) == (x, y)


def test_point_labels_anchor_at_their_own_point():
    fig = ScatterChart(ORDERED, size="size")
    anchors = {
        text.get_text(): text.xy
        for text in fig.axes[0].texts
        if isinstance(text, Annotation)
    }
    assert anchors == {f"p{i}": (i, 10 * i) for i in range(4)}


def test_value_labels_anchor_at_their_own_point():
    data = [{key: r[key] for key in ("x", "y", "size")} for r in ORDERED]
    fig = ScatterChart(data, size="size", show_values=True, value_format="{x:.0f}")
    anchors = {text.get_text(): text.xy for text in fig.axes[0].texts}
    assert anchors == {str(10 * i): (i, 10 * i) for i in range(4)}


def test_regression_skips_a_point_without_size():
    data = [{"x": x, "y": x, "size": 10} for x in range(4)]
    data.append({"x": 4, "y": 100, "size": None})
    fig = ScatterChart(data, size="size", show_regression=True)
    (fit,) = fig.axes[0].get_lines()
    assert np.allclose(fit.get_ydata(), fit.get_xdata())


def test_error_bars_stay_with_their_point():
    data = [dict(record) for record in ORDERED]
    data[0]["yerr"] = 3
    fig = ScatterChart(data, size="size")
    ax = fig.axes[0]
    fig.canvas.draw()
    bars = [patch for patch in ax.patches if isinstance(patch, FancyArrowPatch)]
    ends = {tuple(np.round(bar.get_path().vertices[2], 6)) for bar in bars}
    assert ends == {(0.0, -3.0), (0.0, 3.0)}


def test_plain_scatter_keeps_data_order():
    data = [{"x": x, "y": x} for x in (3, 0, 2, 1)]
    (collection,) = _points(ScatterChart(data).axes[0])
    assert collection.get_offsets()[:, 0].tolist() == [3, 0, 2, 1]
