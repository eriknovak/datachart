"""Tests for `show(interactive=True)` and the hover seam (ADR 0031)."""

import sys
import types
import warnings

import matplotlib

# show() opens a blocking GUI window on interactive backends
matplotlib.use("Agg", force=True)

import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.collections import PathCollection
from matplotlib.container import BarContainer
from matplotlib.lines import Line2D

from datachart.charts import (
    LineChart,
    BarChart,
    ScatterChart,
    Histogram,
    BoxPlot,
    PyramidChart,
)
from datachart.utils import Panel, Grid

LINE_DATA = [
    [{"x": i, "y": i * 2} for i in range(5)],
    [{"x": i, "y": i} for i in range(5)],
]
BAR_DATA = [
    [{"label": c, "y": v} for c, v in zip("ABC", [3, 1, 4])],
    [{"label": c, "y": v} for c, v in zip("ABC", [2, 5, 6])],
]


def _line_fig(**kwargs):
    return LineChart(data=LINE_DATA, subtitle=["fast", "slow"], **kwargs)


def _bar_fig(**kwargs):
    return BarChart(data=BAR_DATA, subtitle=["north", "south"], **kwargs)


def _targets(figure):
    return figure._hover_targets


def _pixel(ax, x, y):
    """The canvas pixel position of a data point, after a draw."""
    ax.figure.canvas.draw()
    return ax.transData.transform((x, y))


def _hover(figure, ax, x, y):
    """Move the mouse over a data point and return the annotation texts."""
    px, py = _pixel(ax, x, y)
    event = MouseEvent("motion_notify_event", figure.canvas, px, py)
    figure.canvas.callbacks.process("motion_notify_event", event)
    return [sel.annotation.get_text() for sel in figure._hover_cursor.selections]


def _show_interactive(figure):
    with warnings.catch_warnings():
        # Agg is non-interactive; plt.show() warns instead of opening a window
        warnings.simplefilter("ignore")
        figure.show(interactive=True)


class TestHoverSeam:
    """Layers register (artist, resolver) pairs on the figure they draw into."""

    def test_line_registers_one_target_per_series(self):
        targets = _targets(_line_fig())
        assert [type(a) for a, _ in targets] == [Line2D, Line2D]
        artist, resolver = targets[0]
        assert artist.get_label() == "fast"
        assert resolver(2) == {"label": "fast", "x": 2, "y": 4}

    def test_scatter_registers_one_target_per_series(self):
        figure = ScatterChart(
            data=[[{"x": i, "y": i * 3} for i in range(4)]] * 2,
            subtitle=["a", "b"],
        )
        targets = _targets(figure)
        assert [type(a) for a, _ in targets] == [PathCollection, PathCollection]
        assert targets[1][1](3) == {"label": "b", "x": 3, "y": 9}

    def test_scatter_hue_groups_register_per_hue(self):
        data = [{"x": i, "y": i, "hue": "g1" if i < 2 else "g2"} for i in range(4)]
        targets = _targets(ScatterChart(data=data))
        assert [r(0)["label"] for _, r in targets] == ["g1", "g2"]
        # indices are local to the hue group's points
        assert targets[1][1](1) == {"label": "g2", "x": 3, "y": 3}

    def test_bar_registers_container_reporting_own_value(self):
        for bar_mode in ("group", "stack", "overlay"):
            targets = _targets(_bar_fig(bar_mode=bar_mode))
            assert [type(a) for a, _ in targets] == [BarContainer, BarContainer]
            assert targets[1][1](1) == {"label": "south", "x": "B", "y": 5}

    def test_horizontal_bar_reports_value_on_the_drawn_x(self):
        targets = _targets(_bar_fig(orientation="horizontal"))
        assert targets[0][1](2) == {"label": "north", "x": 4, "y": "C"}

    def test_pyramid_bars_report_positive_values(self):
        figure = PyramidChart(data=BAR_DATA, subtitle=["left", "right"])
        targets = _targets(figure)
        assert targets[0][1](0)["x"] == 3

    def test_log_scale_bars_report_the_data_value(self):
        targets = _targets(_bar_fig(scaley="log"))
        assert targets[0][1](0)["y"] == 3

    def test_other_layers_register_nothing(self):
        hist = Histogram(
            data=[{"x": v} for v in np.random.default_rng(0).normal(size=30)]
        )
        box = BoxPlot(data=[{"label": "g", "value": v} for v in range(20)])
        assert _targets(hist) == []
        assert _targets(box) == []

    def test_composed_figures_register_their_own_targets(self):
        line, bar = _line_fig(), _bar_fig()
        panel = Panel([bar, line])
        grid = Grid([[line, bar]])
        assert len(_targets(panel)) == 4
        assert len(_targets(grid)) == 4
        # the source figures keep their own targets, on their own artists
        assert len(_targets(line)) == 2
        assert _targets(line)[0][0].figure is line
        assert _targets(panel)[2][0].figure is panel

    def test_line_in_horizontal_panel_swaps_axes(self):
        hbar = _bar_fig(orientation="horizontal")
        line = LineChart(data=[{"x": i, "y": i * 10} for i in range(3)])
        panel = Panel([hbar, line])
        resolver = _targets(panel)[2][1]
        assert resolver(1) == {"label": None, "x": 10, "y": 1}


class TestShowInteractive:
    """show(interactive=True) attaches hover cursors and keeps the static path."""

    def setup_method(self):
        plt.close("all")

    def teardown_method(self):
        plt.close("all")

    def test_default_show_registers_no_cursor(self):
        figure = _line_fig()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            figure.show()
        assert not hasattr(figure, "_hover_cursor")

    def test_script_path_adopts_and_attaches_cursor(self):
        figure = _line_fig(xlabel="Step", ylabel="Loss")
        _show_interactive(figure)
        managed = [plt.figure(num) for num in plt.get_fignums()]
        assert figure in managed
        texts = _hover(figure, figure.axes[0], 3, 6)
        assert texts == ["fast\nStep: 3\nLoss: 6"]

    def test_axis_names_default_to_x_and_y(self):
        figure = _line_fig()
        _show_interactive(figure)
        texts = _hover(figure, figure.axes[0], 1, 1)
        assert texts == ["slow\nx: 1\ny: 1"]

    def test_bar_hover_reports_category_and_height(self):
        figure = BarChart(
            data=BAR_DATA[0], xlabel="Region", ylabel="Count", subtitle="north"
        )
        _show_interactive(figure)
        # bar index 1 ("B") sits at x=1, hover halfway up
        texts = _hover(figure, figure.axes[0], 1, 0.5)
        assert texts == ["north\nRegion: B\nCount: 1"]

    def test_show_twice_attaches_one_cursor(self):
        figure = _line_fig()
        _show_interactive(figure)
        first = figure._hover_cursor
        _show_interactive(figure)
        assert figure._hover_cursor is first
        assert len(plt.get_fignums()) == 1

    def test_twin_axis_series_use_the_right_label(self):
        bar = BarChart(data=BAR_DATA[0], subtitle="count")
        line = LineChart(
            data=[{"x": i, "y": v} for i, v in enumerate([100, 300, 200])],
            subtitle="average",
        )
        panel = Panel(
            [bar, {"figure": line, "y_axis": "right"}],
            xlabel="Region",
            ylabel_left="Count",
            ylabel_right="Average",
        )
        _show_interactive(panel)
        left, right = panel.axes[0], panel.axes[1]
        assert _hover(panel, right, 1, 300) == ["average\nRegion: B\nAverage: 300"]
        assert _hover(panel, left, 2, 2) == ["count\nRegion: C\nCount: 4"]

    def test_grid_cells_all_have_hover(self):
        grid = Grid(
            [[_line_fig(xlabel="Step", ylabel="Loss"), _bar_fig(xlabel="Region")]],
            ylabel="Value",
        )
        _show_interactive(grid)
        line_ax, bar_ax = grid.axes[0], grid.axes[1]
        assert _hover(grid, line_ax, 4, 8) == ["fast\nStep: 4\nLoss: 8"]
        # the grid-level ylabel names the axis the cell left unlabeled
        assert _hover(grid, bar_ax, 0, 0.5)[0].startswith("north\nRegion: A\nValue: ")

    def test_missing_mplcursors_raises_import_error(self, monkeypatch):
        monkeypatch.setitem(sys.modules, "mplcursors", None)
        with pytest.raises(ImportError, match=r"datachart\[interactive\]"):
            _line_fig().show(interactive=True)
        assert plt.get_fignums() == []


class TestShowInteractiveNotebook:
    """In a Jupyter kernel, show(interactive=True) displays an ipympl canvas."""

    @pytest.fixture
    def kernel(self, monkeypatch):
        import IPython.core.getipython
        import IPython.display

        shell = type("ZMQInteractiveShell", (), {})()
        monkeypatch.setattr(IPython.core.getipython, "get_ipython", lambda: shell)
        displays = []
        monkeypatch.setattr(
            IPython.display, "display", lambda *args, **kwargs: displays.append(args)
        )
        return displays

    @pytest.fixture
    def fake_ipympl(self, monkeypatch):
        shown = []

        class FakeCanvas(FigureCanvasAgg):
            _closed = True

        class FakeManager:
            def __init__(self, canvas, num):
                self.canvas = canvas
                self.num = num
                canvas.manager = self

            def show(self):
                shown.append(self)

        module = types.ModuleType("ipympl.backend_nbagg")
        module.Canvas = FakeCanvas
        module.FigureManager = FakeManager
        monkeypatch.setitem(sys.modules, "ipympl", types.ModuleType("ipympl"))
        monkeypatch.setitem(sys.modules, "ipympl.backend_nbagg", module)
        return shown

    def test_interactive_show_displays_widget_canvas(self, kernel, fake_ipympl):
        figure = _line_fig()
        figure.show(interactive=True)
        assert len(fake_ipympl) == 1
        manager = fake_ipympl[0]
        assert manager.canvas is figure.canvas
        assert type(figure.canvas).__name__ == "FakeCanvas"
        # no static PNG payload alongside the widget
        assert kernel == []
        assert plt.get_fignums() == []
        assert _hover(figure, figure.axes[0], 2, 4) == ["fast\nx: 2\ny: 4"]

    def test_interactive_show_twice_reuses_the_manager(self, kernel, fake_ipympl):
        figure = _line_fig()
        figure.show(interactive=True)
        figure.show(interactive=True)
        assert len(fake_ipympl) == 2
        assert fake_ipympl[0] is fake_ipympl[1]

    def test_default_show_stays_static(self, kernel, fake_ipympl):
        figure = _line_fig()
        figure.show()
        assert fake_ipympl == []
        assert len(kernel) == 1

    def test_missing_ipympl_raises_import_error(self, kernel, monkeypatch):
        monkeypatch.setitem(sys.modules, "ipympl", None)
        with pytest.raises(ImportError, match=r"ipympl.*datachart\[interactive\]"):
            _line_fig().show(interactive=True)
        assert kernel == []
