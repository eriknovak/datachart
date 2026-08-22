"""The line chart's `show_area` fill reaches the bottom of the axes."""

import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
from matplotlib.collections import PolyCollection

from datachart.charts import LineChart
from datachart.constants import SCALE

TEMPERATURES = [{"x": i, "y": y} for i, y in enumerate([-0.5, 0.4, 2.9, 6.3, 10.6])]


@pytest.fixture(autouse=True)
def _close_figures():
    yield
    plt.close("all")


def _fill_bottom(ax):
    fills = [c for c in ax.collections if isinstance(c, PolyCollection)]
    assert len(fills) == 1
    return min(v[1] for path in fills[0].get_paths() for v in path.vertices)


def test_area_reaches_axis_bottom_with_negative_values():
    fig = LineChart(data=TEMPERATURES, show_area=True)
    ax = fig.axes[0]
    assert _fill_bottom(ax) <= ax.get_ylim()[0]


def test_area_does_not_change_autoscaled_limits():
    plain = LineChart(data=TEMPERATURES).axes[0].get_ylim()
    filled = LineChart(data=TEMPERATURES, show_area=True).axes[0].get_ylim()
    assert filled == plain


def test_area_reaches_explicit_ymin():
    fig = LineChart(data=TEMPERATURES, show_area=True, ymin=-20)
    ax = fig.axes[0]
    assert ax.get_ylim()[0] == -20
    assert _fill_bottom(ax) <= -20


def test_area_reaches_shared_bottom_across_subplots():
    fig = LineChart(
        data=[TEMPERATURES, [{"x": i, "y": y - 30} for i, y in enumerate(range(5))]],
        show_area=True,
        subplots=True,
        sharey=True,
    )
    axes = fig.axes[:2]
    assert axes[0].get_ylim() == axes[1].get_ylim()
    for ax in axes:
        assert _fill_bottom(ax) <= ax.get_ylim()[0]


def test_area_renders_on_log_scale_without_warnings():
    fig = LineChart(
        data=[{"x": i, "y": 10**i} for i in range(1, 5)],
        show_area=True,
        scaley=SCALE.LOG,
    )
    ax = fig.axes[0]
    assert ax.get_yscale() == "log"
    assert ax.get_ylim()[0] > 0
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        fig.canvas.draw()
    assert _fill_bottom(ax) <= ax.get_ylim()[0]
