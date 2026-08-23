"""Tests for the orientation-aware Panel."""

import warnings

import pytest
import numpy as np
import matplotlib.pyplot as plt

from datachart.charts import LineChart, BarChart, ScatterChart, Histogram
from datachart.constants import ORIENTATION
from datachart.utils import Panel, Grid
from datachart.utils._internal.layers import determine_axis_assignment

BARS = [{"label": c, "y": v * 100} for c, v in zip("ABCD", [1, 2, 3, 2])]
BARS2 = [{"label": c, "y": v * 100} for c, v in zip("ABCD", [2, 1, 2, 3])]
LINE_SMALL = [{"x": i, "y": i * 2} for i in range(4)]
LINE_LARGE = [{"x": i, "y": v} for i, v in enumerate([150, 250, 200, 300])]
LINE_HUGE = [{"x": i, "y": i * 1000} for i in range(4)]


def hbar(data=BARS, **kwargs):
    return BarChart(data=data, orientation=ORIENTATION.HORIZONTAL, **kwargs)


def vbar(data=BARS, **kwargs):
    return BarChart(data=data, **kwargs)


def render(fig):
    fig.canvas.draw()
    return fig.axes


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


class TestOrientationInference:
    def test_all_horizontal_bars_is_horizontal(self):
        panel = Panel([hbar(), hbar(BARS2)])._chart_metadata["panel"]
        assert panel.horizontal is True

    def test_horizontal_bars_and_line_is_horizontal(self):
        panel = Panel([hbar(), LineChart(data=LINE_LARGE)])._chart_metadata["panel"]
        assert panel.horizontal is True

    def test_lines_only_is_vertical(self):
        panel = Panel(
            [LineChart(data=LINE_SMALL), ScatterChart(data=LINE_LARGE)]
        )._chart_metadata["panel"]
        assert panel.horizontal is False

    def test_vertical_bars_and_line_is_vertical(self):
        panel = Panel([vbar(), LineChart(data=LINE_LARGE)])._chart_metadata["panel"]
        assert panel.horizontal is False

    def test_horizontal_histogram_is_horizontal(self):
        np.random.seed(0)
        fh = Histogram(
            data=[{"x": float(v)} for v in np.random.randn(50)],
            orientation=ORIENTATION.HORIZONTAL,
        )
        assert Panel([fh])._chart_metadata["panel"].horizontal is True


class TestMixedOrientation:
    def test_mixed_bars_raise(self):
        with pytest.raises(ValueError, match="orientation"):
            Panel([hbar(), vbar(BARS2)])

    def test_mixed_through_nesting_raises(self):
        inner = Panel([hbar(), hbar(BARS2)])
        with pytest.raises(ValueError, match="orientation"):
            Panel([inner, vbar()])

    def test_mixed_bar_and_histogram_raise(self):
        np.random.seed(0)
        fh = Histogram(
            data=[{"x": float(v)} for v in np.random.randn(50)],
            orientation=ORIENTATION.HORIZONTAL,
        )
        with pytest.raises(ValueError, match="orientation"):
            Panel([vbar(), fh])


class TestSecondaryValueAxis:
    def test_auto_assignment_twins_the_x_axis(self):
        fig = Panel([hbar(), LineChart(data=LINE_SMALL)], auto_secondary_axis=3.0)
        ax, ax_top = render(fig)
        assert ax.get_shared_y_axes().joined(ax, ax_top)
        assert not ax.get_shared_x_axes().joined(ax, ax_top)
        assert ax_top.get_xlim() != ax.get_xlim()
        assert ax_top.xaxis.get_ticks_position() == "top"

    def test_explicit_right_lands_on_top_axis(self):
        fig = Panel(
            [
                {"figure": hbar(), "y_axis": "left"},
                {"figure": LineChart(data=LINE_SMALL), "y_axis": "right"},
            ]
        )
        ax, ax_top = render(fig)
        assert len(ax_top.get_lines()) == 1
        assert ax_top.xaxis.get_ticks_position() == "top"

    def test_same_assignment_as_vertical(self):
        figs = lambda bar: [bar(), LineChart(data=LINE_SMALL)]
        vertical = Panel(figs(vbar))._chart_metadata["panel"].groups
        horizontal = Panel(figs(hbar))._chart_metadata["panel"].groups
        assert determine_axis_assignment(vertical, 3.0) == determine_axis_assignment(
            horizontal, 3.0
        )


class TestParameterRoles:
    def test_labels_follow_the_value_axis(self):
        fig = Panel(
            [
                {"figure": hbar(), "y_axis": "left"},
                {"figure": LineChart(data=LINE_SMALL), "y_axis": "right"},
            ],
            xlabel="category",
            ylabel_left="count",
            ylabel_right="value",
        )
        ax, ax_top = render(fig)
        assert ax.get_ylabel() == "category"
        assert ax.get_xlabel() == "count"
        assert ax_top.get_xlabel() == "value"
        assert ax_top.get_ylabel() == ""

    def test_limits_follow_the_value_axis(self):
        fig = Panel(
            [
                {"figure": hbar(), "y_axis": "left"},
                {"figure": LineChart(data=LINE_SMALL), "y_axis": "right"},
            ],
            xmin=-1,
            xmax=5,
            ymin=0,
            ymax=500,
            ymin_right=-2,
            ymax_right=10,
        )
        ax, ax_top = render(fig)
        assert ax.get_ylim() == (-1, 5)
        assert ax.get_xlim() == (0, 500)
        assert ax_top.get_xlim() == (-2, 10)
        assert ax_top.get_ylim() == (-1, 5)

    def test_vertical_panel_is_unchanged(self):
        fig = Panel(
            [
                {"figure": vbar(), "y_axis": "left"},
                {"figure": LineChart(data=LINE_SMALL), "y_axis": "right"},
            ],
            xlabel="category",
            ylabel_left="count",
            ylabel_right="value",
            xmin=-1,
            xmax=5,
            ymin=0,
            ymax=500,
            ymin_right=-2,
            ymax_right=10,
        )
        ax, ax_right = render(fig)
        assert ax.get_xlabel() == "category"
        assert ax.get_ylabel() == "count"
        assert ax_right.get_ylabel() == "value"
        assert ax.get_xlim() == (-1, 5)
        assert ax.get_ylim() == (0, 500)
        assert ax_right.get_ylim() == (-2, 10)

    def test_horizontal_is_the_transpose_of_vertical(self):
        def panel(bar):
            fig = Panel(
                [bar(), LineChart(data=LINE_SMALL)],
                xmin=-0.5,
                xmax=3.5,
                ymin=0,
                ymax=400,
                ymin_right=0,
                ymax_right=8,
            )
            return render(fig)

        v_ax, v_twin = panel(vbar)
        h_ax, h_twin = panel(hbar)
        assert h_ax.get_xlim() == v_ax.get_ylim()
        assert h_ax.get_ylim() == v_ax.get_xlim()
        assert h_twin.get_xlim() == v_twin.get_ylim()


class TestTranspose:
    def test_line_data_is_transposed(self):
        fig = Panel([hbar(), LineChart(data=LINE_LARGE)])
        ax = render(fig)[0]
        (line,) = ax.get_lines()
        assert list(line.get_xdata()) == [p["y"] for p in LINE_LARGE]
        assert list(line.get_ydata()) == [p["x"] for p in LINE_LARGE]

    def test_scatter_data_is_transposed(self):
        fig = Panel([hbar(), ScatterChart(data=LINE_LARGE)])
        ax = render(fig)[0]
        offsets = ax.collections[0].get_offsets()
        assert list(offsets[:, 0]) == [p["y"] for p in LINE_LARGE]
        assert list(offsets[:, 1]) == [p["x"] for p in LINE_LARGE]

    def test_line_yerr_and_area_transpose(self):
        data = [{**p, "yerr": 10} for p in LINE_LARGE]
        fig = Panel(
            [hbar(), LineChart(data=data, show_yerr=True, show_area=True)],
        )
        ax = render(fig)[0]
        # the error band and the area fill span the category axis (y)
        for poly in ax.collections:
            verts = poly.get_paths()[0].vertices
            assert verts[:, 1].min() <= 0 and verts[:, 1].max() >= 3
            assert verts[:, 0].max() > 100

    def test_standalone_line_is_untouched(self):
        fig = LineChart(data=LINE_LARGE)
        (line,) = render(fig)[0].get_lines()
        assert list(line.get_xdata()) == [p["x"] for p in LINE_LARGE]

    def test_vertical_panel_line_is_untouched(self):
        fig = Panel([vbar(), LineChart(data=LINE_LARGE)])
        (line,) = render(fig)[0].get_lines()
        assert list(line.get_xdata()) == [p["x"] for p in LINE_LARGE]

    def test_scatter_regression_transposes(self):
        fig = Panel([hbar(), ScatterChart(data=LINE_LARGE, show_regression=True)])
        ax = render(fig)[0]
        (reg,) = ax.get_lines()
        assert reg.get_ydata().min() >= 0 and reg.get_ydata().max() <= 3
        assert reg.get_xdata().max() > 100


class TestLegend:
    def test_suffixes_are_bottom_top(self):
        fig = Panel(
            [
                {"figure": hbar(subtitle="bars"), "y_axis": "left"},
                {
                    "figure": LineChart(data=LINE_SMALL, subtitle="line"),
                    "y_axis": "right",
                },
            ],
            show_legend=True,
        )
        ax = render(fig)[0]
        labels = [t.get_text() for t in ax.get_legend().get_texts()]
        assert labels == ["bars (B)", "line (T)"]

    def test_vertical_suffixes_unchanged(self):
        fig = Panel(
            [
                {"figure": vbar(subtitle="bars"), "y_axis": "left"},
                {
                    "figure": LineChart(data=LINE_SMALL, subtitle="line"),
                    "y_axis": "right",
                },
            ],
            show_legend=True,
        )
        ax = render(fig)[0]
        labels = [t.get_text() for t in ax.get_legend().get_texts()]
        assert labels == ["bars (L)", "line (R)"]


class TestComposition:
    def test_horizontal_panel_in_grid(self):
        panel = Panel([hbar(), LineChart(data=LINE_SMALL)], title="h")
        fig = Grid([panel, vbar()], figsize=(10, 4))
        fig.canvas.draw()
        assert fig.axes[0].get_title() == "h"
        # the line sits on the cell's top value axis, transposed
        (line,) = [l for ax in fig.axes for l in ax.get_lines()]
        assert list(line.get_ydata()) == [p["x"] for p in LINE_SMALL]
        assert fig.axes[0].get_shared_y_axes().joined(fig.axes[0], line.axes)

    def test_nested_horizontal_panel_equals_flat(self):
        def pixels(compose):
            figs = [hbar(), hbar(BARS2), LineChart(data=LINE_SMALL)]
            fig = compose(figs)
            fig.canvas.draw()
            out = np.asarray(fig.canvas.buffer_rgba()).copy()
            plt.close("all")
            return out

        flat = pixels(Panel)
        nested = pixels(lambda figs: Panel([Panel(figs[:2]), figs[2]]))
        assert np.array_equal(flat, nested)

    def test_stacked_horizontal_bars_with_line(self):
        fig = Panel(
            [hbar(), hbar(BARS2), LineChart(data=LINE_SMALL)],
            bar_mode="stack",
            show_legend=True,
        )
        ax, ax_top = render(fig)
        # stacked bars extend along x; the line runs along the category axis
        assert max(p.get_width() + p.get_x() for p in ax.patches) >= 400
        (line,) = ax_top.get_lines()
        assert list(line.get_ydata()) == [p["x"] for p in LINE_SMALL]


class TestAssignmentWarnings:
    def test_no_warning_for_explicit_incompatible_pairs(self):
        groups = (
            Panel(
                [
                    {"figure": vbar(), "y_axis": "left"},
                    {"figure": LineChart(data=LINE_SMALL), "y_axis": "left"},
                ]
            )
            ._chart_metadata["panel"]
            .groups
        )
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            determine_axis_assignment(groups, 3.0)

    def test_warning_for_auto_incompatible_pairs_names_grid(self):
        groups = (
            Panel(
                [
                    {"figure": vbar(), "y_axis": "left"},
                    {"figure": LineChart(data=LINE_SMALL), "y_axis": "right"},
                    LineChart(data=LINE_HUGE),
                ]
            )
            ._chart_metadata["panel"]
            .groups
        )
        with pytest.warns(UserWarning, match="Grid") as record:
            assert determine_axis_assignment(groups, 3.0) == ["left", "right", "right"]
        assert not any("FigureGridLayout" in str(w.message) for w in record)
