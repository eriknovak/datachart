"""Bubble chart legend markers keep the base marker size, not the data size."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
from matplotlib.collections import PathCollection

from datachart.charts import ScatterChart
from datachart.config import config

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
