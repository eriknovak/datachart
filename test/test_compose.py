"""Tests for the public Panel/Grid composition fronts (ADR 0002)."""

import copy
import io
import warnings

import pytest
import matplotlib.pyplot as plt

from datachart.charts import LineChart, BarChart
from datachart.config import config
from datachart.constants import THEME
from datachart.utils import (
    Panel,
    Grid,
    OverlayChart,
    FigureGridLayout,
    figure_grid_layout,
)


def _png_bytes(figure):
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi=100)
    return buffer.getvalue()


def _line_fig():
    return LineChart(data=[{"x": i, "y": i * 2} for i in range(5)])


def _bar_fig():
    return BarChart(data=[{"label": c, "y": v} for c, v in zip("ABCD", [3, 1, 4, 2])])


class TestPanel:
    """Test suite for the Panel composition front."""

    def test_bare_figures_match_overlaychart(self):
        """Panel with bare figures renders identically to OverlayChart with dicts."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            old = OverlayChart(
                charts=[{"figure": _bar_fig()}, {"figure": _line_fig()}],
                title="Combined",
            )
        new = Panel([_bar_fig(), _line_fig()], title="Combined")
        assert _png_bytes(old) == _png_bytes(new)
        plt.close("all")

    def test_dict_items_pass_options(self):
        """Dict items carry per-figure options like y_axis."""
        fig = Panel(
            [
                {"figure": _bar_fig(), "y_axis": "left"},
                {"figure": _line_fig(), "y_axis": "right"},
            ],
            show_legend=True,
        )
        # a right axis assignment creates a twin axes
        assert len(fig.axes) == 2
        plt.close("all")

    def test_mixed_bare_and_dict_items(self):
        fig = Panel([_bar_fig(), {"figure": _line_fig(), "z_order": 5}])
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_rejects_dict_without_figure(self):
        with pytest.raises(ValueError, match="figure"):
            Panel([{"y_axis": "left"}])

    def test_rejects_non_figure_item(self):
        with pytest.raises(ValueError, match="index 0"):
            Panel(["not a figure"])

    def test_rejects_grid_figure(self):
        grid_fig = Grid([_line_fig(), _bar_fig()])
        with pytest.raises(ValueError, match="[Gg]rid"):
            Panel([grid_fig])
        plt.close("all")

    def test_rejects_empty_list(self):
        with pytest.raises(ValueError):
            Panel([])


class TestGroupedBarAlignment:
    """Grouped bars center on the category position, with category ticks."""

    @staticmethod
    def _bar_centers(ax):
        return sorted(p.get_x() + p.get_width() / 2 for p in ax.patches)

    def test_panel_bar_ticks_show_category_labels(self):
        fig = Panel([_bar_fig(), _bar_fig()])
        ax = fig.axes[0]
        assert [t.get_text() for t in ax.get_xticklabels()] == list("ABCD")
        assert list(ax.get_xticks()) == [0, 1, 2, 3]
        plt.close("all")

    def test_panel_grouped_bars_center_on_category(self):
        fig = Panel([_bar_fig(), _bar_fig()])
        centers = self._bar_centers(fig.axes[0])
        # two slots per category, symmetric around the category position
        for i in range(4):
            left, right = centers[2 * i], centers[2 * i + 1]
            assert (left + right) / 2 == pytest.approx(i)
        plt.close("all")

    def test_barchart_grouped_series_center_on_category(self):
        data = [{"label": c, "y": v} for c, v in zip("ABCD", [3, 1, 4, 2])]
        fig = BarChart(data=[data, data])
        ax = fig.axes[0]
        assert list(ax.get_xticks()) == [0, 1, 2, 3]
        centers = self._bar_centers(ax)
        for i in range(4):
            left, right = centers[2 * i], centers[2 * i + 1]
            assert (left + right) / 2 == pytest.approx(i)
        plt.close("all")


class TestGrid:
    """Test suite for the Grid composition front."""

    def test_flat_list_matches_figuregridlayout(self):
        """Grid with a flat list renders identically to FigureGridLayout."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            old = FigureGridLayout(
                charts=[{"figure": _line_fig()}, {"figure": _bar_fig()}],
                title="Grid",
            )
        new = Grid([_line_fig(), _bar_fig()], title="Grid")
        assert _png_bytes(old) == _png_bytes(new)
        plt.close("all")

    def test_nested_rows_define_layout(self):
        """Nested rows produce one grid row per list."""
        fig = Grid([[_line_fig(), _bar_fig()], [_line_fig()]])
        assert len(fig.axes) == 3
        specs = [ax.get_subplotspec() for ax in fig.axes]
        # two rows: the single bottom cell spans the full width
        assert specs[0].rowspan.start == 0
        assert specs[2].rowspan.start == 1
        assert specs[2].colspan == range(0, 2)
        plt.close("all")

    def test_uneven_rows_use_lcm_spans(self):
        """[[a, b], [c, d, e]] -> width 6: top cells span 3, bottom span 2."""
        fig = Grid([[_line_fig(), _bar_fig()], [_line_fig(), _bar_fig(), _line_fig()]])
        specs = [ax.get_subplotspec() for ax in fig.axes]
        assert specs[0].colspan == range(0, 3)
        assert specs[1].colspan == range(3, 6)
        assert specs[2].colspan == range(0, 2)
        assert specs[4].colspan == range(4, 6)
        plt.close("all")

    def test_none_leaves_blank_cell(self):
        fig = Grid([[_line_fig(), None], [_bar_fig(), _line_fig()]])
        assert len(fig.axes) == 3
        plt.close("all")

    def test_flat_dicts_with_layout_spec(self):
        fig = Grid(
            [
                {
                    "figure": _line_fig(),
                    "layout_spec": {"row": 0, "col": 0, "rowspan": 1, "colspan": 2},
                },
                {
                    "figure": _bar_fig(),
                    "layout_spec": {"row": 1, "col": 0, "rowspan": 1, "colspan": 1},
                },
                {
                    "figure": _line_fig(),
                    "layout_spec": {"row": 1, "col": 1, "rowspan": 1, "colspan": 1},
                },
            ]
        )
        assert len(fig.axes) == 3
        plt.close("all")

    def test_rejects_mixed_nested_and_flat(self):
        with pytest.raises(ValueError, match="nested"):
            Grid([[_line_fig()], _bar_fig()])

    def test_rejects_dict_in_nested_row(self):
        with pytest.raises(ValueError, match="layout"):
            Grid([[{"figure": _line_fig()}]])

    def test_rejects_empty_row(self):
        with pytest.raises(ValueError):
            Grid([[_line_fig()], []])

    def test_rejects_grid_in_grid(self):
        inner = Grid([_line_fig(), _bar_fig()])
        with pytest.raises(ValueError, match="[Gg]rid"):
            Grid([inner, _line_fig()])
        plt.close("all")

    def test_rejects_empty_list(self):
        with pytest.raises(ValueError):
            Grid([])

    def test_panel_output_nests_in_grid(self):
        panel_fig = Panel([_bar_fig(), _line_fig()])
        fig = Grid([[panel_fig, _line_fig()]])
        assert len(fig.axes) >= 2
        plt.close("all")


class TestStyleFreeze:
    """Layer styles freeze at chart build, and composing never touches the config.

    Swapping the global theme between building a chart and composing it must not
    change the composed output (CONTEXT.md: "Style resolution"). Panel-level
    furniture is resolved when the panel is built — at the compose call — so
    these scenarios keep grid/legend off, where the freeze is fully observable.
    """

    # fixture instead of the file's inline plt.close: reset must survive a failed assert
    @pytest.fixture(autouse=True)
    def _reset_config(self):
        yield
        config.reset_config()
        plt.close("all")

    def test_panel_ignores_theme_swap(self):
        bar, line = _bar_fig(), _line_fig()
        before = _png_bytes(Panel([bar, line]))
        config.set_theme(THEME.GREYSCALE)
        after = _png_bytes(Panel([bar, line]))
        assert before == after

    def test_grid_ignores_theme_swap(self):
        bar, line = _bar_fig(), _line_fig()
        before = _png_bytes(Grid([[bar, line]]))
        config.set_theme(THEME.GREYSCALE)
        after = _png_bytes(Grid([[bar, line]]))
        assert before == after

    def test_compose_does_not_mutate_config(self):
        """The retired save/restore dance: composing must leave the config alone."""
        snapshot = copy.deepcopy(config.config)
        Panel([_bar_fig(), _line_fig()], show_grid="both", show_legend=True)
        Grid([[_bar_fig(), _line_fig()]])
        assert config.config == snapshot


class TestDeprecations:
    """The old composition fronts warn and delegate."""

    def test_overlaychart_warns(self):
        with pytest.warns(DeprecationWarning, match="Panel"):
            fig = OverlayChart(charts=[{"figure": _line_fig()}])
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_figuregridlayout_warns(self):
        with pytest.warns(DeprecationWarning, match="Grid"):
            fig = FigureGridLayout(charts=[{"figure": _line_fig()}])
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_figure_grid_layout_warns(self):
        with pytest.warns(DeprecationWarning, match="Grid"):
            fig = figure_grid_layout([_line_fig()])
        assert isinstance(fig, plt.Figure)
        plt.close("all")
