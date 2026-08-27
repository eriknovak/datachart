"""Tests for the public Panel/Grid composition fronts (ADR 0002)."""

import copy
import io

import pytest
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpecFromSubplotSpec

from datachart.charts import LineChart, BarChart
from datachart.config import config
from datachart.constants import BAR_MODE, THEME, VALUE_FORMAT
from datachart.utils import (
    Panel,
    Grid,
)
from datachart.utils._internal.config_helpers import get_text_style


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

    def test_bare_figures_match_dict_items(self):
        """Panel with bare figures renders identically to dict items."""
        old = Panel(
            [{"figure": _bar_fig()}, {"figure": _line_fig()}],
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
    def _assert_pairs_center_on_categories(ax, n):
        centers = sorted(p.get_x() + p.get_width() / 2 for p in ax.patches)
        # two slots per category, symmetric around the category position
        for i in range(n):
            left, right = centers[2 * i], centers[2 * i + 1]
            assert (left + right) / 2 == pytest.approx(i)

    def test_panel_bar_ticks_show_category_labels(self):
        fig = Panel([_bar_fig(), _bar_fig()])
        ax = fig.axes[0]
        assert [t.get_text() for t in ax.get_xticklabels()] == list("ABCD")
        assert list(ax.get_xticks()) == [0, 1, 2, 3]
        plt.close("all")

    def test_panel_grouped_bars_center_on_category(self):
        fig = Panel([_bar_fig(), _bar_fig()])
        self._assert_pairs_center_on_categories(fig.axes[0], 4)
        plt.close("all")

    def test_barchart_grouped_series_center_on_category(self):
        data = [{"label": c, "y": v} for c, v in zip("ABCD", [3, 1, 4, 2])]
        fig = BarChart(data=[data, data])
        ax = fig.axes[0]
        assert list(ax.get_xticks()) == [0, 1, 2, 3]
        self._assert_pairs_center_on_categories(ax, 4)
        plt.close("all")

    def test_panel_ragged_categories_use_widest_labels(self):
        short = BarChart(data=[{"label": c, "y": v} for c, v in zip("AB", [2, 5])])
        fig = Panel([_bar_fig(), short])
        ax = fig.axes[0]
        assert [t.get_text() for t in ax.get_xticklabels()] == list("ABCD")
        plt.close("all")

    def test_panel_stacked_bars_center_on_category(self):
        fig = Panel([_bar_fig(), _bar_fig()], bar_mode="stack")
        centers = {round(p.get_x() + p.get_width() / 2, 6) for p in fig.axes[0].patches}
        assert centers == {0, 1, 2, 3}
        plt.close("all")


class TestGrid:
    """Test suite for the Grid composition front."""

    def test_flat_list_matches_figuregridlayout(self):
        """Grid with bare figures renders identically to dict items."""
        old = Grid(
            [{"figure": _line_fig()}, {"figure": _bar_fig()}],
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

    def test_rejects_empty_list(self):
        with pytest.raises(ValueError):
            Grid([])

    def test_panel_output_nests_in_grid(self):
        panel_fig = Panel([_bar_fig(), _line_fig()])
        fig = Grid([[panel_fig, _line_fig()]])
        assert len(fig.axes) >= 2
        plt.close("all")

    def test_panel_output_nests_in_flat_grid(self):
        panel_fig = Panel([_bar_fig(), _line_fig()])
        fig = Grid([panel_fig, _line_fig()])
        assert len(fig.axes) == 2
        plt.close("all")


def _nested_axes(fig):
    """Axes rendered through a nested gridspec (heading axes included)."""
    return [
        ax
        for ax in fig.axes
        if isinstance(ax.get_subplotspec().get_gridspec(), GridSpecFromSubplotSpec)
    ]


class TestNestedGrid:
    """Grid figures nest inside Grid via the recursive cell tree (ADR 0006),
    rendered in the parent's gridspec so cell envelopes align (ADR 0007)."""

    def test_grid_axis_labels_drawn_once(self):
        f1 = LineChart(data=[{"x": 0, "y": 1}, {"x": 1, "y": 2}])
        f2 = LineChart(data=[{"x": 0, "y": 2}, {"x": 1, "y": 1}])
        grid = Grid([f1, f2], xlabel="Day", ylabel="Articles")
        assert grid._supxlabel.get_text() == "Day"
        assert grid._supylabel.get_text() == "Articles"
        assert grid._chart_metadata["xlabel"] == "Day"
        # nested, the labels render as text in the cell rather than figure labels
        outer = Grid([grid, f1])
        assert outer._supxlabel is None
        texts = [t.get_text() for ax in outer.axes for t in ax.texts]
        assert "Day" in texts
        assert "Articles" in texts
        for fig in (f1, f2, grid, outer):
            plt.close(fig)

    def test_grid_metadata_carries_cell_tree(self):
        fig = Grid([_line_fig(), _bar_fig()], title="Inner", sharex=True)
        md = fig._chart_metadata
        assert md["type"] == "grid"
        assert md["title"] == "Inner"
        assert md["sharex"] is True
        assert md["sharey"] is False
        assert md["shape"] == (1, 2)
        assert [c["spec"] for c in md["cells"]] == [
            {"row": 0, "col": 0, "rowspan": 1, "colspan": 1},
            {"row": 0, "col": 1, "rowspan": 1, "colspan": 1},
        ]
        assert all("panel" in c for c in md["cells"])
        plt.close("all")

    def test_grid_nests_in_grid(self):
        inner = Grid([_line_fig(), _bar_fig()])
        fig = Grid([inner, _line_fig()])
        # the nested grid occupies one cell and rebuilds its two cells inside it
        assert len(fig.axes) == 3
        cells = fig._chart_metadata["cells"]
        assert "grid" in cells[0]
        assert "panel" in cells[1]
        assert len(cells[0]["grid"]["cells"]) == 2
        plt.close("all")

    def test_nesting_composes_to_depth_three(self):
        level1 = Grid([_line_fig(), _bar_fig()])
        level2 = Grid([level1, _line_fig()])
        level3 = Grid([level2, _bar_fig()])
        assert len(level3.axes) == 4
        node = level3._chart_metadata["cells"][0]["grid"]
        assert "grid" in node["cells"][0]
        assert len(node["cells"][0]["grid"]["cells"]) == 2
        plt.close("all")

    def test_nested_grid_in_nested_rows(self):
        inner = Grid([[_line_fig(), _bar_fig()]])
        fig = Grid([[inner, _line_fig()], [_bar_fig()]])
        assert len(fig.axes) == 4
        plt.close("all")

    def test_blank_cells_preserved_inside_nested_grid(self):
        inner = Grid([[_line_fig(), None], [_bar_fig(), _line_fig()]])
        fig = Grid([inner, _bar_fig()])
        # the inner blank cell stays blank: only 3 inner axes plus 1 outer
        assert len(fig.axes) == 4
        plt.close("all")

    def test_nested_grid_renders_in_parent_figure(self):
        inner = Grid([_line_fig(), _bar_fig()], title="Inner")
        fig = Grid([inner, _line_fig()])
        assert not fig.subfigs
        assert all(ax.figure is fig for ax in fig.axes)
        plt.close("all")

    def test_nested_grid_axes_align_with_host_columns(self):
        # a two-column nested grid spanning a two-column host row: each inner
        # chart's spines line up with the host column above it
        inner = Grid([[_line_fig(), _bar_fig()]], title="Inner")
        fig = Grid([[_line_fig(), _bar_fig()], [inner]])
        nested = _nested_axes(fig)
        inner_charts = sorted(
            (ax for ax in nested if ax.axison), key=lambda ax: ax.get_position().x0
        )
        outer_charts = sorted(
            (ax for ax in fig.axes if ax not in nested),
            key=lambda ax: ax.get_position().x0,
        )
        assert len(inner_charts) == len(outer_charts) == 2
        for outer, inner_ax in zip(outer_charts, inner_charts):
            assert outer.get_position().x0 == pytest.approx(
                inner_ax.get_position().x0, abs=1e-6
            )
            assert outer.get_position().x1 == pytest.approx(
                inner_ax.get_position().x1, abs=1e-6
            )
        plt.close("all")

    def test_nested_title_renders_in_heading_row(self):
        inner = Grid([_line_fig(), _bar_fig()], title="Inner")
        fig = Grid([inner, _line_fig()])
        headings = [
            ax for ax in fig.axes if any(t.get_text() == "Inner" for t in ax.texts)
        ]
        assert len(headings) == 1
        hax = headings[0]
        assert not hax.axison
        # the heading occupies a reserved extra top row spanning the subgrid
        spec = hax.get_subplotspec()
        assert spec.get_gridspec().get_geometry() == (2, 2)
        assert spec.rowspan == range(0, 1)
        assert spec.colspan == range(0, 2)
        # demoted from title: inside a composition it is a section heading
        text = next(t for t in hax.texts if t.get_text() == "Inner")
        subtitle = get_text_style("subtitle")
        assert text.get_fontsize() == subtitle["fontsize"]
        assert text.get_fontweight() == subtitle["fontweight"]
        assert text.get_color() == subtitle["color"]
        plt.close("all")

    def test_untitled_nested_grid_reserves_no_heading_row(self):
        inner = Grid([_line_fig(), _bar_fig()])
        fig = Grid([inner, _line_fig()])
        nested = _nested_axes(fig)
        assert len(nested) == 2
        # the subgrid keeps the node's own shape — no heading row
        assert all(
            ax.get_subplotspec().get_gridspec().get_geometry() == (1, 2)
            for ax in nested
        )
        plt.close("all")

    def test_untitled_nested_grid_aligns_with_siblings(self):
        inner = Grid([_line_fig(), _line_fig()])
        fig = Grid([inner, _bar_fig()])
        fig.canvas.draw()
        sibling = next(ax for ax in fig.axes if ax not in _nested_axes(fig))
        for ax in _nested_axes(fig):
            assert ax.get_position().y1 == pytest.approx(
                sibling.get_position().y1, abs=1e-3
            )
            assert ax.get_position().y0 == pytest.approx(
                sibling.get_position().y0, abs=1e-3
            )
        plt.close("all")

    def test_titled_nested_grid_aligns_bottom_top_pays_heading(self):
        inner = Grid([_line_fig(), _line_fig()], title="Inner")
        fig = Grid([inner, _bar_fig()])
        fig.canvas.draw()
        sibling = next(ax for ax in fig.axes if ax not in _nested_axes(fig))
        cells = [ax for ax in _nested_axes(fig) if ax.axison]
        for ax in cells:
            assert ax.get_position().y0 == pytest.approx(
                sibling.get_position().y0, abs=1e-3
            )
            # the top edge sits lower by the heading row only
            assert ax.get_position().y1 < sibling.get_position().y1
        plt.close("all")

    def test_nested_grid_alone_in_row_keeps_row_height(self):
        inner = Grid([_line_fig(), _line_fig()])
        fig = Grid([_bar_fig(), _bar_fig(), _bar_fig(), inner], max_cols=3)
        fig.canvas.draw()
        sibling = next(ax for ax in fig.axes if ax not in _nested_axes(fig))
        nested = [ax for ax in _nested_axes(fig) if ax.axison]
        envelope = max(ax.get_position().y1 for ax in nested) - min(
            ax.get_position().y0 for ax in nested
        )
        assert envelope == pytest.approx(sibling.get_position().height, abs=1e-2)
        plt.close("all")

    def test_nested_grid_keeps_own_furniture(self):
        inner = Grid([_line_fig(), _line_fig()], title="Inner", sharey=True)
        outer = Grid([inner, _bar_fig()], title="Outer")
        assert outer._suptitle.get_text() == "Outer"
        # the nested title renders as a heading spanning the subgrid
        assert any(
            t.get_text() == "Inner" for ax in _nested_axes(outer) for t in ax.texts
        )
        # inner sharey holds among the inner cells only
        in_a, in_b = [ax for ax in _nested_axes(outer) if ax.axison]
        assert in_a.get_shared_y_axes().joined(in_a, in_b)
        outer_ax = next(ax for ax in outer.axes if ax not in _nested_axes(outer))
        assert not in_a.get_shared_y_axes().joined(in_a, outer_ax)
        plt.close("all")

    def test_parent_sharing_stops_at_nesting_boundary(self):
        inner = Grid([_line_fig(), _line_fig()])
        outer = Grid([_line_fig(), inner, _line_fig()], sharex=True)
        top = [ax for ax in outer.axes if ax not in _nested_axes(outer)]
        assert top[0].get_shared_x_axes().joined(top[0], top[1])
        in_a, in_b = _nested_axes(outer)
        assert not in_a.get_shared_x_axes().joined(in_a, in_b)
        assert not in_a.get_shared_x_axes().joined(in_a, top[0])
        plt.close("all")

    def test_multi_subplot_figure_nests_inside_nested_grid(self):
        sub = LineChart(
            data=[[{"x": i, "y": i} for i in range(5)] for _ in range(2)],
            subplots=True,
        )
        inner = Grid([sub, _bar_fig()])
        fig = Grid([inner, _line_fig()])
        # 2 subplot axes + 1 bar + 1 outer line
        assert len(fig.axes) == 4
        plt.close("all")

    def test_nested_sharing_skips_multi_subplot_cells(self):
        # a multi-subplot cell's spanning axes is removed during render, so it
        # must never anchor the nested grid's sharex/sharey group
        sub = LineChart(
            data=[[{"x": i, "y": i} for i in range(5)] for _ in range(2)],
            subplots=True,
        )
        inner = Grid([sub, _line_fig(), _line_fig()], sharex=True)
        fig = Grid([inner, _bar_fig()])
        # creation order inside the subgrid: 2 subplot axes, then 2 line axes
        in_axes = _nested_axes(fig)
        assert len(in_axes) == 4
        line_a, line_b = in_axes[2], in_axes[3]
        assert line_a.get_shared_x_axes().joined(line_a, line_b)
        assert not line_a.get_shared_x_axes().joined(line_a, in_axes[0])
        plt.close("all")

    def test_grid_in_panel_still_raises(self):
        grid_fig = Grid([_line_fig(), _bar_fig()])
        with pytest.raises(ValueError, match="[Gg]rid"):
            Panel([grid_fig])
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


def _bar_widths(figure):
    return [round(p.get_width(), 3) for p in figure.axes[0].patches]


class TestBarWidth:
    """A per-chart plot_bar_width style must reach the drawn bars."""

    data = [{"label": "a", "y": 1}, {"label": "b", "y": 2}]

    def test_single_chart_style_width(self):
        figure = BarChart(data=self.data, style={"plot_bar_width": 0.4})
        assert _bar_widths(figure) == [0.4, 0.4]
        plt.close(figure)

    def test_grouped_layers_keep_own_width(self):
        figure = BarChart(
            data=[self.data, self.data],
            style=[{"plot_bar_width": 0.8}, {"plot_bar_width": 0.4}],
        )
        assert _bar_widths(figure) == [0.4, 0.4, 0.2, 0.2]
        plt.close(figure)

    def test_stacked_layers_keep_own_width(self):
        figure = BarChart(
            data=[self.data, self.data],
            style=[{"plot_bar_width": 0.8}, {"plot_bar_width": 0.4}],
            bar_mode=BAR_MODE.STACK,
        )
        assert _bar_widths(figure) == [0.8, 0.8, 0.4, 0.4]
        plt.close(figure)

    def test_horizontal_style_width(self):
        figure = BarChart(
            data=self.data, style={"plot_bar_width": 0.4}, orientation="horizontal"
        )
        assert [round(p.get_height(), 3) for p in figure.axes[0].patches] == [0.4, 0.4]
        plt.close(figure)

    def test_config_width_still_applies(self):
        config.update_config({"plot_bar_width": 0.5})
        try:
            figure = BarChart(data=[self.data, self.data])
            assert _bar_widths(figure) == [0.25, 0.25, 0.25, 0.25]
            plt.close(figure)
        finally:
            config.reset_config()


class TestBarValueFormat:
    """value_format accepts VALUE_FORMAT ({x}-style), {}-style, and %-style."""

    data = [{"label": "a", "y": 1234.5}, {"label": "b", "y": 0.25}]

    def _labels(self, value_format):
        figure = BarChart(data=self.data, show_values=True, value_format=value_format)
        labels = [t.get_text() for t in figure.axes[0].texts]
        plt.close(figure)
        return labels

    def test_value_format_constant(self):
        assert self._labels(VALUE_FORMAT.THOUSANDS) == ["1,234", "0"]
        assert self._labels(VALUE_FORMAT.PERCENT_INT) == ["123450%", "25%"]

    def test_positional_and_percent_styles(self):
        assert self._labels("{:.1f}%") == ["1234.5%", "0.2%"]
        assert self._labels("%g") == ["1234.5", "0.25"]
