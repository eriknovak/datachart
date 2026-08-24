"""Tests for the PyramidChart front and the mirrored bar panel."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from datachart.charts import BarChart, PyramidChart
from datachart.utils import Grid, Panel

AGES = ["0-14", "15-29", "30-44", "45-59", "60+"]
LEFT = [{"label": a, "y": v} for a, v in zip(AGES, [12, 18, 22, 15, 9])]
RIGHT = [{"label": a, "y": v} for a, v in zip(AGES, [11, 19, 24, 16, 12])]


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


class TestFrontValidation:
    def test_flat_point_list_raises(self):
        with pytest.raises(ValueError, match="two"):
            PyramidChart(data=LEFT)

    def test_one_series_raises(self):
        with pytest.raises(ValueError, match="two"):
            PyramidChart(data=[LEFT])

    def test_three_series_raises(self):
        with pytest.raises(ValueError, match="two"):
            PyramidChart(data=[LEFT, RIGHT, LEFT])

    def test_xmin_raises(self):
        with pytest.raises(ValueError, match="xmin"):
            PyramidChart(data=[LEFT, RIGHT], xmin=-10)

    def test_negative_xticks_raise(self):
        with pytest.raises(ValueError, match="xticks"):
            PyramidChart(data=[LEFT, RIGHT], xticks=[-10, 0, 10])


class TestMirroredDrawing:
    def test_left_side_draws_negative_right_positive(self):
        figure = PyramidChart(data=[LEFT, RIGHT])
        ax = figure.axes[0]
        left_bars, right_bars = ax.containers
        assert all(patch.get_width() < 0 for patch in left_bars)
        assert all(patch.get_width() > 0 for patch in right_bars)

    def test_input_data_is_not_mutated(self):
        PyramidChart(data=[LEFT, RIGHT])
        assert all(point["y"] > 0 for point in LEFT)

    def test_both_sides_full_width_zero_offset(self):
        figure = PyramidChart(data=[LEFT, RIGHT])
        ax = figure.axes[0]
        left_bars, right_bars = ax.containers
        for left_patch, right_patch in zip(left_bars, right_bars):
            assert left_patch.get_y() == pytest.approx(right_patch.get_y())
            assert left_patch.get_height() == pytest.approx(right_patch.get_height())

    def test_no_overlay_alpha(self):
        pyramid_ax = PyramidChart(data=[LEFT, RIGHT]).axes[0]
        plain_ax = BarChart(data=LEFT).axes[0]
        plain_alpha = plain_ax.containers[0][0].get_alpha()
        for container in pyramid_ax.containers:
            assert container[0].get_alpha() == plain_alpha

    def test_value_limits_are_symmetric(self):
        figure = PyramidChart(data=[LEFT, RIGHT])
        lo, hi = figure.axes[0].get_xlim()
        assert lo == pytest.approx(-hi)
        assert hi >= 24

    def test_xmax_sets_per_side_limit(self):
        figure = PyramidChart(data=[LEFT, RIGHT], xmax=30)
        assert figure.axes[0].get_xlim() == pytest.approx((-30, 30))

    def test_value_ticks_show_absolute_values(self):
        figure = PyramidChart(data=[LEFT, RIGHT])
        formatter = figure.axes[0].xaxis.get_major_formatter()
        assert formatter(-10) == "10"
        assert formatter(10) == "10"

    def test_user_xticks_are_mirrored(self):
        figure = PyramidChart(data=[LEFT, RIGHT], xticks=[0, 10, 20])
        assert sorted(figure.axes[0].get_xticks()) == [-20, -10, 0, 10, 20]

    def test_user_xticklabels_apply_to_both_halves(self):
        figure = PyramidChart(
            data=[LEFT, RIGHT], xticks=[0, 10, 20], xticklabels=["0", "10k", "20k"]
        )
        labels = [t.get_text() for t in figure.axes[0].get_xticklabels()]
        assert labels == ["20k", "10k", "0", "10k", "20k"]

    def test_show_values_labels_are_absolute(self):
        figure = PyramidChart(data=[LEFT, RIGHT], show_values=True)
        texts = [t.get_text() for t in figure.axes[0].texts if t.get_text()]
        assert texts
        assert all(not text.startswith("-") for text in texts)

    def test_category_labels_on_left_edge(self):
        figure = PyramidChart(data=[LEFT, RIGHT])
        labels = [t.get_text() for t in figure.axes[0].get_yticklabels()]
        assert labels == AGES

    def test_subtitles_name_the_sides_in_legend(self):
        figure = PyramidChart(
            data=[LEFT, RIGHT], subtitle=["Group A", "Group B"], show_legend=True
        )
        legend = figure.axes[0].get_legend()
        assert [t.get_text() for t in legend.get_texts()] == ["Group A", "Group B"]

    def test_y_key_remap_negates_the_left_side(self):
        left = [{"label": a, "count": v} for a, v in zip(AGES, [1, 2, 3, 4, 5])]
        right = [{"label": a, "count": v} for a, v in zip(AGES, [5, 4, 3, 2, 1])]
        figure = PyramidChart(data=[left, right], y="count")
        left_bars, right_bars = figure.axes[0].containers
        assert all(patch.get_width() < 0 for patch in left_bars)
        assert all(patch.get_width() > 0 for patch in right_bars)


class TestComposition:
    def test_panel_rejects_pyramid_figures(self):
        figure = PyramidChart(data=[LEFT, RIGHT])
        with pytest.raises(ValueError, match="pyramid"):
            Panel([figure])

    def test_grid_accepts_pyramid_figures(self):
        pyramid = PyramidChart(data=[LEFT, RIGHT])
        other = PyramidChart(data=[RIGHT, LEFT])
        grid = Grid([pyramid, other])
        assert grid._chart_metadata["type"] == "grid"
        lo, hi = grid.axes[0].get_xlim()
        assert lo == pytest.approx(-hi)
