"""Tests for the Sankey chart: style, column inference, validation, and composition."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Rectangle

from datachart.charts import SankeyChart, LineChart
from datachart.config import config
from datachart.constants import THEME
from datachart.utils import Panel, Grid
from datachart.utils._internal.config_helpers import get_sankey_style
from datachart.utils._internal.validate import (
    infer_sankey_columns,
    validate_sankey_links,
    validate_sankey_nodes,
)

THEMES = [
    THEME.DEFAULT,
    THEME.GREYSCALE,
    THEME.INK,
    THEME.HATCH,
    THEME.MINIMAL,
    THEME.MATERIAL,
]

SANKEY_KEYS = (
    "plot_sankey_node_width",
    "plot_sankey_node_pad",
    "plot_sankey_node_edge_color",
    "plot_sankey_node_edge_width",
    "plot_sankey_link_color",
    "plot_sankey_link_alpha",
    "plot_sankey_label_halo_width",
)


def link(source, target, value):
    return {"source": source, "target": target, "value": value}


FUNNEL = [
    link("Visited", "Signed up", 300),
    link("Visited", "Bounced", 700),
    link("Signed up", "Activated", 180),
    link("Signed up", "Churned", 120),
    link("Activated", "Paid", 90),
    link("Activated", "Free tier", 90),
]
CHAIN = [link("a", "b", 1), link("b", "c", 1), link("c", "d", 1)]


def _rects(ax):
    return [p for p in ax.patches if isinstance(p, Rectangle)]


def _ribbons(ax):
    return [p for p in ax.patches if isinstance(p, PathPatch)]


class TestSankeyStyle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)

    def test_style_resolves_from_config(self):
        style = get_sankey_style({})
        self.assertEqual(style["node_width"], config["plot_sankey_node_width"])
        self.assertEqual(style["link_color"], "source")
        self.assertEqual(style["halo_width"], config["plot_sankey_label_halo_width"])

    def test_chart_style_overrides(self):
        style = get_sankey_style({"plot_sankey_link_color": "grey"})
        self.assertEqual(style["link_color"], "grey")

    def test_every_theme_sets_the_sankey_keys(self):
        for theme in THEMES:
            config.set_theme(theme)
            for key in SANKEY_KEYS:
                self.assertIn(key, config.config, f"{theme} lacks {key}")

    def test_edge_color_follows_bar_edges(self):
        for theme, color in (
            (THEME.GREYSCALE, "#000000"),
            (THEME.HATCH, "#000000"),
            (THEME.INK, "#0B1F44"),
        ):
            config.set_theme(theme)
            self.assertEqual(config["plot_sankey_node_edge_color"], color)


class TestColumnInference(unittest.TestCase):
    def test_chain(self):
        self.assertEqual(infer_sankey_columns(CHAIN), [["a"], ["b"], ["c"], ["d"]])

    def test_branch_keeps_first_seen_order(self):
        links = [link("a", "c", 1), link("a", "b", 1), link("b", "d", 1)]
        self.assertEqual(infer_sankey_columns(links), [["a"], ["c", "b"], ["d"]])

    def test_leaf_stays_at_its_own_depth(self):
        self.assertEqual(
            infer_sankey_columns(FUNNEL),
            [
                ["Visited"],
                ["Signed up", "Bounced"],
                ["Activated", "Churned"],
                ["Paid", "Free tier"],
            ],
        )

    def test_longest_path_wins(self):
        links = [link("a", "b", 1), link("a", "c", 1), link("b", "c", 1)]
        self.assertEqual(infer_sankey_columns(links), [["a"], ["b"], ["c"]])

    def test_cycle_raises(self):
        with self.assertRaises(ValueError):
            infer_sankey_columns([link("a", "b", 1), link("b", "a", 1)])
        with self.assertRaises(ValueError):
            SankeyChart({"links": CHAIN + [link("d", "a", 1)]})


class TestValidation(unittest.TestCase):
    def test_bad_links_raise(self):
        for links in (
            [],
            [{"source": "a", "value": 1}],
            [link("a", "b", 0)],
            [link("a", "b", -2)],
            [link("a", "a", 1)],
            [{"source": "a", "target": "b", "value": "x"}],
        ):
            with self.subTest(links=links), self.assertRaises(ValueError):
                validate_sankey_links(links)

    def test_bad_data_shape_raises(self):
        with self.assertRaises(ValueError):
            SankeyChart(CHAIN)
        with self.assertRaises(ValueError):
            SankeyChart({"data": CHAIN})

    def test_explicit_nodes_must_cover_the_links(self):
        validate_sankey_nodes([["a"], ["b"], ["c", "d"]], CHAIN)
        for nodes in (
            [["a"], ["b"], ["c"]],
            [["a"], ["b"], ["c", "d", "e"]],
            [["a"], ["b", "b"], ["c", "d"]],
            [["a", "b", "c", "d"]][0],
        ):
            with self.subTest(nodes=nodes), self.assertRaises(ValueError):
                validate_sankey_nodes(nodes, CHAIN)

    def test_emphasis_raises(self):
        with self.assertRaises(ValueError):
            SankeyChart({"links": CHAIN}, emphasis="highlight")


class TestRendering(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_node_and_ribbon_counts(self):
        fig = SankeyChart({"links": FUNNEL})
        ax = fig.axes[0]
        self.assertEqual(len(_rects(ax)), 7)
        self.assertEqual(len(_ribbons(ax)), len(FUNNEL))
        self.assertEqual(len(ax.texts), 7)
        self.assertFalse(ax.axison)
        self.assertEqual(fig._chart_metadata["type"], "sankeychart")

    def test_explicit_nodes_set_the_columns(self):
        nodes = [
            ["Visited"],
            ["Bounced", "Signed up"],
            ["Churned", "Activated"],
            ["Free tier", "Paid"],
        ]
        fig = SankeyChart({"links": FUNNEL}, nodes=nodes)
        xs = {r.get_label(): r.get_x() for r in _rects(fig.axes[0])}
        self.assertEqual(xs["Bounced"], xs["Signed up"])
        self.assertLess(xs["Visited"], xs["Bounced"])
        self.assertLess(xs["Churned"], xs["Paid"])

    def test_node_height_is_max_of_in_and_out(self):
        fig = SankeyChart({"links": FUNNEL})
        heights = {r.get_label(): r.get_height() for r in _rects(fig.axes[0])}
        self.assertAlmostEqual(heights["Visited"], 1 - config["plot_sankey_node_pad"])
        self.assertAlmostEqual(heights["Signed up"], heights["Visited"] * 0.3)

    def test_no_halo_when_width_is_zero(self):
        fig = SankeyChart({"links": CHAIN}, style={"plot_sankey_label_halo_width": 0})
        self.assertEqual(fig.axes[0].texts[0].get_path_effects(), [])

    def test_link_color_modes(self):
        for mode in ("source", "target", "grey"):
            fig = SankeyChart({"links": CHAIN}, style={"plot_sankey_link_color": mode})
            self.assertEqual(len(_ribbons(fig.axes[0])), 3)
        with self.assertRaises(ValueError):
            SankeyChart({"links": CHAIN}, style={"plot_sankey_link_color": "nope"})

    def test_subplots(self):
        fig = SankeyChart(
            [{"links": CHAIN}, {"links": FUNNEL}],
            subtitle=["chain", "funnel"],
            subplots=True,
        )
        self.assertEqual(len(fig.axes), 2)
        self.assertEqual(len(_ribbons(fig.axes[0])), 3)
        self.assertEqual(len(_ribbons(fig.axes[1])), len(FUNNEL))
        self.assertEqual(fig.axes[0].get_title(), "chain")

    def test_several_charts_without_subplots_still_split(self):
        fig = SankeyChart([{"links": CHAIN}, {"links": FUNNEL}])
        self.assertEqual(len(fig.axes), 2)


class TestComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_rejects(self):
        sankey = SankeyChart({"links": CHAIN})
        line = LineChart([{"x": 0, "y": 1}, {"x": 1, "y": 2}])
        with self.assertRaisesRegex(ValueError, "Grid"):
            Panel([sankey, line])

    def test_grid_accepts(self):
        sankey = SankeyChart({"links": FUNNEL}, title="funnel")
        line = LineChart([{"x": 0, "y": 1}, {"x": 1, "y": 2}])
        grid = Grid([[sankey, line]])
        self.assertEqual(len(grid.axes), 2)
        self.assertEqual(len(_ribbons(grid.axes[0])), len(FUNNEL))
        self.assertFalse(grid.axes[0].axison)
        self.assertEqual(grid.axes[0].get_title(), "funnel")


if __name__ == "__main__":
    unittest.main()
