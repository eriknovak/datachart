"""Tests for per-figure legend settings and outside placements (ADR 0034)."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import BarChart, LineChart, Treemap
from datachart.config import config
from datachart.constants import LEGEND_LOCATION, THEME
from datachart.utils import Grid, Panel
from datachart.utils._internal.config_helpers import get_legend_style

LINES = [
    [{"x": 0, "y": 1}, {"x": 1, "y": 2}],
    [{"x": 0, "y": 2}, {"x": 1, "y": 1}],
]
BARS = [{"label": "A", "y": 3}, {"label": "B", "y": 5}]
RECORDS = {"data": [{"label": "A", "value": 3}, {"label": "B", "value": 5}]}


def legend_of(figure):
    """The one legend on a figure's topmost axes."""
    legends = [ax.get_legend() for ax in figure.axes if ax.get_legend()]
    assert len(legends) == 1, legends
    return legends[0]


class TestLegendStyle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_theme_supplies_title_and_ncols(self):
        """The theme names the legend title and column count."""
        style = get_legend_style()
        self.assertEqual(style["title"], "Legend")
        self.assertEqual(style["ncols"], 1)
        self.assertEqual(style["loc"], "best")

    def test_setting_overrides_theme_field_by_field(self):
        """A non-None setting field wins; a None field falls back to the theme."""
        config.update_config({"plot_legend_title": "Series", "plot_legend_ncols": 3})
        style = get_legend_style({"title": None, "ncols": 2, "location": None})
        self.assertEqual(style["title"], "Series")
        self.assertEqual(style["ncols"], 2)
        self.assertEqual(style["loc"], "best")
        self.assertEqual(style["alignment"], "left")

    def test_outside_location_expands_to_loc_and_anchor(self):
        """An outside member becomes a matplotlib loc plus an anchor, from either source."""
        style = get_legend_style({"location": LEGEND_LOCATION.OUTSIDE_RIGHT})
        self.assertEqual(style["loc"], "upper left")
        self.assertEqual(style["bbox_to_anchor"], (1.0, 1.0))

        config.update_config({"plot_legend_location": LEGEND_LOCATION.OUTSIDE_BOTTOM})
        style = get_legend_style()
        self.assertEqual(style["loc"], "upper center")
        self.assertEqual(style["bbox_to_anchor"], (0.5, 0.0))

    def test_inside_location_carries_no_anchor(self):
        """In-axes members pass straight through with no anchor."""
        style = get_legend_style({"location": LEGEND_LOCATION.UPPER_RIGHT})
        self.assertEqual(style["loc"], "upper right")
        self.assertNotIn("bbox_to_anchor", style)


class TestLegendSetting(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_default_title_is_legend(self):
        """With no setting the legend keeps its `Legend` title."""
        figure = LineChart(LINES, subtitle=["a", "b"], show_legend=True)
        self.assertEqual(legend_of(figure).get_title().get_text(), "Legend")

    def test_setting_overrides_title_columns_and_location(self):
        figure = LineChart(
            LINES,
            subtitle=["a", "b"],
            show_legend=True,
            legend={"title": "Series", "ncols": 2, "location": "upper right"},
        )
        legend = legend_of(figure)
        self.assertEqual(legend.get_title().get_text(), "Series")
        self.assertEqual(legend._ncols, 2)
        self.assertEqual(legend._loc, 1)

    def test_empty_title_draws_no_title(self):
        figure = LineChart(
            LINES, subtitle=["a", "b"], show_legend=True, legend={"title": ""}
        )
        self.assertFalse(legend_of(figure).get_title().get_visible())

    def test_outside_location_sits_beside_the_axes(self):
        """An outside legend lands fully outside the axes, unclipped by the figure."""
        figure = LineChart(
            LINES,
            subtitle=["a", "b"],
            show_legend=True,
            legend={"location": LEGEND_LOCATION.OUTSIDE_RIGHT},
        )
        figure.canvas.draw()
        renderer = figure.canvas.get_renderer()
        ax = figure.axes[0]
        box = legend_of(figure).get_window_extent(renderer)
        self.assertGreaterEqual(box.x0, ax.bbox.x1)
        self.assertLessEqual(box.x1, figure.bbox.x1)

    def test_outside_legend_clears_the_axis_furniture(self):
        """An outside legend sits past the tick labels and axis label, not over them."""
        for location, side in [
            (LEGEND_LOCATION.OUTSIDE_BOTTOM, "bottom"),
            (LEGEND_LOCATION.OUTSIDE_LEFT, "left"),
        ]:
            with self.subTest(side=side):
                figure = LineChart(
                    LINES,
                    subtitle=["a", "b"],
                    xlabel="x axis",
                    ylabel="y axis",
                    show_legend=True,
                    legend={"location": location},
                )
                figure.canvas.draw()
                renderer = figure.canvas.get_renderer()
                ax = figure.axes[0]
                legend = legend_of(figure)
                legend.set_in_layout(False)
                furniture = ax.get_tightbbox(renderer)
                box = legend.get_window_extent(renderer)
                if side == "bottom":
                    self.assertLessEqual(box.y1, furniture.y0)
                    self.assertGreaterEqual(box.y0, figure.bbox.y0)
                else:
                    self.assertLessEqual(box.x1, furniture.x0)
                    self.assertGreaterEqual(box.x0, figure.bbox.x0)

    def test_bare_panel_location_wins_over_the_pin(self):
        """A treemap keeps its outside pin unless the caller names a location."""
        pinned = Treemap(RECORDS, show_legend=True)
        self.assertEqual(legend_of(pinned)._loc, 2)
        self.assertEqual(
            tuple(legend_of(pinned).get_bbox_to_anchor().bounds[:2]),
            tuple(pinned.axes[0].bbox.bounds[:2] + pinned.axes[0].bbox.size),
        )
        placed = Treemap(RECORDS, show_legend=True, legend={"location": "lower left"})
        self.assertEqual(legend_of(placed)._loc, 3)

    def test_panel_front_takes_the_setting(self):
        figure = Panel(
            [BarChart(BARS, subtitle="bars"), LineChart(LINES[0], subtitle="line")],
            show_legend=True,
            legend={"title": "Mixed", "ncols": 2},
        )
        legend = legend_of(figure)
        self.assertEqual(legend.get_title().get_text(), "Mixed")
        self.assertEqual(legend._ncols, 2)

    def test_grid_cell_keeps_its_figure_setting(self):
        source = LineChart(
            LINES, subtitle=["a", "b"], show_legend=True, legend={"title": "Cell"}
        )
        figure = Grid([[source, None]])
        self.assertEqual(legend_of(figure).get_title().get_text(), "Cell")

    def test_subplots_keep_suppressing_the_legend(self):
        with self.assertWarns(UserWarning):
            figure = LineChart(
                LINES, subplots=True, show_legend=True, legend={"title": "x"}
            )
        self.assertTrue(all(ax.get_legend() is None for ax in figure.axes))


if __name__ == "__main__":
    unittest.main()
