"""Tests for the unmanaged figure lifecycle (ADR 0008)."""

import warnings

import matplotlib

# show() opens a blocking GUI window on interactive backends
matplotlib.use("Agg", force=True)

import matplotlib.pyplot as plt

from datachart.charts import LineChart, BarChart
from datachart.utils import Panel, Grid


def _line_fig():
    return LineChart(data=[{"x": i, "y": i * 2} for i in range(5)])


def _bar_fig():
    return BarChart(data=[{"label": c, "y": v} for c, v in zip("ABCD", [3, 1, 4, 2])])


class TestUnmanagedFigures:
    """Figures never register with pyplot; rendering many leaks nothing."""

    def setup_method(self):
        plt.close("all")

    def test_charts_do_not_register_with_pyplot(self):
        """Rendering many charts registers nothing and trips no warning."""
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            figures = [_line_fig() for _ in range(25)]
        assert len(figures) == 25
        assert plt.get_fignums() == []

    def test_composition_does_not_register_with_pyplot(self):
        """Panel and both Grid layout branches register nothing."""
        Panel([_line_fig(), _bar_fig()])
        Grid([[_line_fig(), _bar_fig()]])
        Grid(
            [
                {
                    "figure": _line_fig(),
                    "layout_spec": {"row": 0, "col": 0, "rowspan": 1, "colspan": 1},
                },
                {
                    "figure": _bar_fig(),
                    "layout_spec": {"row": 0, "col": 1, "rowspan": 1, "colspan": 1},
                },
            ]
        )
        assert plt.get_fignums() == []

    def test_figures_are_matplotlib_figures(self):
        """The subclass passes isinstance checks against plt.Figure."""
        figure = _line_fig()
        assert isinstance(figure, plt.Figure)

    def test_figures_display_inline_via_repr_png(self):
        """The repr hook yields PNG bytes for inline display."""
        png = _line_fig()._repr_png_()
        assert png.startswith(b"\x89PNG")

    def test_plt_close_is_a_noop_on_unmanaged_figures(self):
        """plt.close on an unmanaged figure does nothing and raises nothing."""
        figure = _line_fig()
        plt.close(figure)
        assert plt.get_fignums() == []


class TestShow:
    """Figure.show adopts the figure into pyplot outside notebooks."""

    def setup_method(self):
        plt.close("all")

    def teardown_method(self):
        plt.close("all")

    def test_show_adopts_figure_into_pyplot(self):
        """show() registers the figure with pyplot's manager."""
        figure = _line_fig()
        with warnings.catch_warnings():
            # Agg is non-interactive; plt.show() warns instead of opening a window
            warnings.simplefilter("ignore")
            figure.show()
        managed = [plt.figure(num) for num in plt.get_fignums()]
        assert figure in managed

    def test_show_twice_does_not_duplicate_registration(self):
        """A second show() reuses the existing manager."""
        figure = _line_fig()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            figure.show()
            figure.show()
        assert len(plt.get_fignums()) == 1

    def test_plt_close_releases_adopted_figure(self):
        """plt.close releases a figure adopted by show()."""
        figure = _line_fig()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            figure.show()
        plt.close(figure)
        assert plt.get_fignums() == []
