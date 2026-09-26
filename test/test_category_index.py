"""One category index per panel places every category layer by label (ADR 0079)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

from datachart.charts import BarChart, BoxPlot, RadialChart
from datachart.constants import RADIAL_TYPE
from datachart.utils import Panel


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def _bars(pairs):
    return [{"label": label, "y": value} for label, value in pairs]


def _ticks(ax):
    return {t.get_text(): p for t, p in zip(ax.get_xticklabels(), ax.get_xticks())}


def _bar_extents(ax):
    """(center, bottom, top) of every drawn bar patch."""

    return sorted(
        (
            round(p.get_x() + p.get_width() / 2, 6),
            round(p.get_y(), 6),
            round(p.get_y() + p.get_height(), 6),
        )
        for p in ax.patches
    )


class TestStackedBars:
    def test_stack_by_label_not_by_index(self):
        fig = BarChart(
            data=[_bars([("A", 1), ("B", 2)]), _bars([("B", 7), ("A", 2)])],
            bar_mode="stack",
        )
        ax = fig.axes[0]
        ticks = _ticks(ax)
        assert _bar_extents(ax) == sorted(
            [
                (ticks["A"], 0, 1),
                (ticks["B"], 0, 2),
                (ticks["A"], 1, 3),
                (ticks["B"], 2, 9),
            ]
        )

    def test_stack_of_ragged_series_renders(self):
        fig = BarChart(
            data=[_bars([("A", 1), ("B", 2)]), _bars([("A", 3), ("B", 4), ("C", 5)])],
            bar_mode="stack",
        )
        ax = fig.axes[0]
        ticks = _ticks(ax)
        assert list(ticks) == ["A", "B", "C"]
        assert (ticks["C"], 0, 5) in _bar_extents(ax)

    def test_disjoint_labels_draw_no_phantom_bar(self):
        fig = BarChart(
            data=[_bars([("A", 1), ("B", 2)]), _bars([("C", 3), ("D", 4)])],
            bar_mode="stack",
        )
        ax = fig.axes[0]
        ticks = _ticks(ax)
        assert list(ticks) == ["A", "B", "C", "D"]
        assert _bar_extents(ax) == sorted(
            [
                (ticks["A"], 0, 1),
                (ticks["B"], 0, 2),
                (ticks["C"], 0, 3),
                (ticks["D"], 0, 4),
            ]
        )


class TestPanelCategories:
    def test_panel_ticks_are_the_union_of_labels(self):
        fig = Panel(
            [
                BarChart(data=_bars([("Q1", 1), ("Q2", 2)])),
                BarChart(data=_bars([("Q2", 3), ("Q3", 4)])),
            ],
            bar_mode="overlay",
        )
        ax = fig.axes[0]
        ticks = _ticks(ax)
        assert list(ticks) == ["Q1", "Q2", "Q3"]
        assert _bar_extents(ax) == sorted(
            [
                (ticks["Q1"], 0, 1),
                (ticks["Q2"], 0, 2),
                (ticks["Q2"], 0, 3),
                (ticks["Q3"], 0, 4),
            ]
        )

    def test_box_sits_at_the_bars_label(self):
        boxes = [{"label": "B", "value": v} for v in (1, 2, 3, 4)] + [
            {"label": "C", "value": v} for v in (5, 6, 7, 8)
        ]
        fig = Panel(
            [
                BarChart(data=_bars([("A", 1), ("B", 2)])),
                BoxPlot(data=boxes),
            ]
        )
        ax = fig.axes[0]
        ticks = _ticks(ax)
        assert list(ticks) == ["A", "B", "C"]
        # the box median line spans its category position; the box may
        # draw on the panel's twin axes
        medians = [
            line
            for axes in fig.axes
            for line in axes.lines
            if len(line.get_ydata()) == 2
            and np.allclose(line.get_ydata(), 2.5)
            and line.get_xdata()[0] != line.get_xdata()[1]
        ]
        assert medians
        assert np.mean(medians[0].get_xdata()) == pytest.approx(ticks["B"])


class TestSort:
    def test_sort_with_a_series_missing_the_first_category(self):
        fig = BarChart(
            data=[
                _bars([("B", 2), ("C", 1)]),
                _bars([("A", 9), ("B", 2), ("C", 1)]),
            ],
            bar_mode="stack",
            sort="descending",
        )
        ax = fig.axes[0]
        ticks = _ticks(ax)
        assert list(ticks) == ["A", "B", "C"]
        assert (ticks["A"], 0, 9) in _bar_extents(ax)
        assert (ticks["B"], 2, 4) in _bar_extents(ax)


class TestRepeatedLabel:
    def test_repeated_label_in_one_series_raises(self):
        with pytest.raises(ValueError, match="'A'"):
            BarChart(data=_bars([("A", 1), ("B", 2), ("A", 3)]))

    def test_repeated_radial_label_raises(self):
        with pytest.raises(ValueError, match="'N'"):
            RadialChart(data=_bars([("N", 1), ("E", 2), ("N", 3)]))


class TestRadial:
    def test_points_sit_on_the_spokes_of_the_union(self):
        three = _bars([("A", 1), ("B", 2), ("C", 3)])
        four = _bars([("A", 4), ("B", 5), ("C", 6), ("D", 7)])
        ax = RadialChart(data=[three, four], mark=RADIAL_TYPE.SCATTER).axes[0]
        spokes = np.linspace(0, 2 * np.pi, 4, endpoint=False)
        assert np.allclose(ax.get_xticks(), spokes)
        assert [t.get_text() for t in ax.get_xticklabels()] == list("ABCD")
        first = ax.collections[0].get_offsets()
        assert np.allclose(first[:, 0], spokes[[0, 1, 2]])

    def test_line_breaks_at_a_missing_label(self):
        three = _bars([("A", 1), ("B", 2), ("C", 3)])
        four = _bars([("A", 4), ("B", 5), ("C", 6), ("D", 7)])
        ax = RadialChart(data=[three, four], mark=RADIAL_TYPE.LINE).axes[0]
        line = ax.lines[0]
        theta, radius = line.get_xdata(), line.get_ydata()
        # four spokes plus the closing point; D is a gap
        assert len(theta) == 5
        assert np.isnan(radius[3])
        assert np.allclose(radius[[0, 1, 2, 4]], [1, 2, 3, 1])

    def test_radial_bars_stack_by_label(self):
        ax = RadialChart(
            data=[_bars([("A", 1), ("B", 2)]), _bars([("B", 7), ("A", 2)])],
            mark=RADIAL_TYPE.BAR,
            bar_mode="stack",
        ).axes[0]
        # a polar bar's y is its bottom, its height the value
        extents = sorted(
            (round(p.get_x() + p.get_width() / 2, 6), p.get_y(), p.get_height())
            for p in ax.patches
        )
        a, b = 0.0, round(np.pi, 6)
        assert extents == sorted([(a, 0, 1), (b, 0, 2), (a, 1, 2), (b, 2, 7)])
