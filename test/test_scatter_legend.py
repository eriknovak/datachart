"""Bubble chart legend markers keep the base marker size, not the data size."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
from matplotlib.collections import PathCollection

from datachart.charts import ScatterChart
from datachart.config import config
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
    assert sizes[(0.0, 0.0)] == pytest.approx(20)
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
