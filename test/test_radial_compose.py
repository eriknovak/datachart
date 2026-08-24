"""Tests for composing radial figures: projection-aware Panel and Grid."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

from datachart.charts import LineChart, RadialChart
from datachart.constants import RADIAL_TYPE
from datachart.utils import Grid, Panel

WIND = [
    {"label": d, "y": v}
    for d, v in zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"], range(1, 9))
]
WIND2 = [
    {"label": d, "y": v}
    for d, v in zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"], range(8, 0, -1))
]
LINE = [{"x": i, "y": i * 2} for i in range(5)]


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


class TestPanelProjection:
    def test_two_radials_merge_on_one_polar_axes(self):
        fig = Panel([RadialChart(data=WIND), RadialChart(data=WIND2)])
        assert fig.axes[0].name == "polar"
        assert len(fig.axes[0].lines) == 2

    def test_mixed_projections_raise(self):
        with pytest.raises(ValueError, match="projection"):
            Panel([RadialChart(data=WIND), LineChart(data=LINE)])

    def test_merged_panel_keeps_radial_furniture(self):
        fig = Panel(
            [
                RadialChart(data=WIND, startangle="E"),
                RadialChart(data=WIND2, startangle="E"),
            ]
        )
        assert fig.axes[0].get_theta_offset() == pytest.approx(0.0)

    def test_mixed_visuals_in_one_panel(self):
        fig = Panel(
            [RadialChart(data=WIND), RadialChart(data=WIND2, type=RADIAL_TYPE.BAR)]
        )
        ax = fig.axes[0]
        assert len(ax.lines) == 1
        assert len(ax.patches) == len(WIND2)
        fig.canvas.draw()


class TestGridProjection:
    def test_polar_and_cartesian_cells_coexist(self):
        fig = Grid([RadialChart(data=WIND), LineChart(data=LINE)], max_cols=2)
        names = sorted(ax.name for ax in fig.axes)
        assert "polar" in names
        assert "rectilinear" in names
        fig.canvas.draw()

    def test_nested_rows_with_polar_cell(self):
        fig = Grid([[RadialChart(data=WIND)], [LineChart(data=LINE)]])
        assert any(ax.name == "polar" for ax in fig.axes)
        fig.canvas.draw()

    def test_polar_cell_draws_the_marks(self):
        fig = Grid([RadialChart(data=WIND, type=RADIAL_TYPE.BAR)])
        polar_ax = next(ax for ax in fig.axes if ax.name == "polar")
        assert len(polar_ax.patches) == len(WIND)

    def test_radial_subplots_figure_in_a_cell(self):
        radial = RadialChart(data=[WIND, WIND2], subplots=True, max_cols=2)
        fig = Grid([radial, LineChart(data=LINE)], max_cols=2)
        assert sum(ax.name == "polar" for ax in fig.axes) == 2
        fig.canvas.draw()
