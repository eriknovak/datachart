"""Tests for the network chart: style, validation, layouts, encoding, emphasis, and composition."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import ArrowStyle, Circle, FancyArrowPatch

from datachart.charts import NetworkChart, LineChart
from datachart.config import config
from datachart.constants import THEME, EMPHASIS, ARROW_STYLE, NETWORK_LAYOUT
from datachart.themes import DEFAULT_THEME
from datachart.utils import Panel, Grid
from datachart.utils._internal.config_helpers import (
    get_network_style,
    get_plot_text_arrow_style,
)
from datachart.utils._internal.layers import (
    circular_layout,
    edge_strengths,
    grouped_layout,
    spring_layout,
    NetworkLayer,
    NETWORK_PULL_MIN,
    NETWORK_PULL_MAX,
)
from datachart.utils._internal.validate import (
    infer_network_nodes,
    validate_network_edge_style,
    validate_network_records,
)

THEMES = [
    THEME.DEFAULT,
    THEME.GREYSCALE,
    THEME.INK,
    THEME.HATCH,
    THEME.MINIMAL,
    THEME.MATERIAL,
    THEME.SKETCH,
]

NETWORK_KEYS = (
    "plot_network_node_color",
    "plot_network_node_alpha",
    "plot_network_node_marker",
    "plot_network_node_size",
    "plot_network_node_size_min",
    "plot_network_node_size_max",
    "plot_network_node_edge_color",
    "plot_network_node_edge_width",
    "plot_network_edge_style",
    "plot_network_edge_curve",
    "plot_network_edge_color",
    "plot_network_edge_alpha",
    "plot_network_edge_width_min",
    "plot_network_edge_width_max",
    "plot_network_highlight_edge_width",
    "plot_network_label_halo_width",
    "plot_network_group_alpha",
)


def edge(source, target, weight=None):
    record = {"source": source, "target": target}
    if weight is not None:
        record["weight"] = weight
    return record


NODES = [{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}]
EDGES = [edge("A", "B"), edge("B", "C"), edge("C", "D"), edge("D", "A")]
DATA = {"nodes": NODES, "edges": EDGES}
LINE = [{"x": 0, "y": 1}, {"x": 1, "y": 2}]


def _nodes(ax):
    """The node scatter of the axes."""
    return [c for c in ax.collections if c.get_gid() == "nodes"][0]


def _edges(ax):
    """The edge patches keyed by `source->target`."""
    return {
        p.get_gid()[len("edge:") :]: p
        for p in ax.patches
        if isinstance(p, FancyArrowPatch) and (p.get_gid() or "").startswith("edge:")
    }


def _labels(ax):
    return {
        t.get_gid()[len("label:") :]: t
        for t in ax.texts
        if (t.get_gid() or "").startswith("label:")
    }


def _values(ax):
    return [t for t in ax.texts if (t.get_gid() or "").startswith("value:")]


def _positions(figure):
    return _nodes(figure.axes[0]).get_offsets().data.copy()


class TestNetworkStyle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)

    def test_style_resolves_from_config(self):
        style = get_network_style({})
        self.assertEqual(style["node_size"], 200)
        self.assertEqual(style["edge_style"], ARROW_STYLE.CURVE)
        self.assertEqual(style["edge_curve"], 0.2)
        self.assertEqual(style["edge_color"], "#9E9E9E")

    def test_chart_style_overrides(self):
        style = get_network_style({"plot_network_edge_width_max": 9})
        self.assertEqual(style["edge_width_max"], 9)

    def test_every_theme_sets_the_network_keys(self):
        for theme in THEMES:
            config.set_theme(theme)
            for key in NETWORK_KEYS:
                self.assertIn(key, config.config, f"{theme}: {key}")

    def test_node_edge_color_follows_bar_edges(self):
        for theme in (THEME.GREYSCALE, THEME.HATCH, THEME.INK):
            config.set_theme(theme)
            self.assertEqual(
                config["plot_network_node_edge_color"], config["plot_bar_edge_color"]
            )

    def test_every_theme_renders(self):
        for theme in THEMES:
            config.set_theme(theme)
            figure = NetworkChart(
                {
                    "nodes": [
                        {"id": "A", "group": "g", "size": 2, "emphasis": "highlight"},
                        {"id": "B", "emphasis": "background"},
                        {"id": "C"},
                    ],
                    "edges": [edge("A", "B", 1), edge("B", "C", 2)],
                },
                directed=True,
                show_values=True,
                show_legend=True,
            )
            self.assertEqual(len(figure.axes), 1)
            plt.close(figure)


class TestArrowStyleStraight(unittest.TestCase):
    def test_straight_is_a_gapped_headless_line(self):
        straight = get_plot_text_arrow_style(
            {"plot_text_arrow_style": ARROW_STYLE.STRAIGHT}
        )
        touching = get_plot_text_arrow_style(
            {"plot_text_arrow_style": ARROW_STYLE.TOUCHING}
        )
        self.assertEqual(straight["arrowstyle"], "-")
        self.assertEqual(straight["curve"], 0.0)
        self.assertGreater(straight["shrinkA"], 0)
        # TOUCHING keeps its flush start
        self.assertEqual(touching["arrowstyle"], "-")
        self.assertEqual(touching["shrinkA"], 0)

    def test_edge_style_accepts_only_headless_members(self):
        self.assertEqual(validate_network_edge_style(None), ARROW_STYLE.CURVE)
        self.assertEqual(
            validate_network_edge_style(ARROW_STYLE.STRAIGHT), ARROW_STYLE.STRAIGHT
        )
        for value in (ARROW_STYLE.ARROW, ARROW_STYLE.CURVE_ARROW, ARROW_STYLE.TOUCHING):
            with self.assertRaisesRegex(ValueError, "directed"):
                validate_network_edge_style(value)
        with self.assertRaisesRegex(ValueError, "plot_network_edge_style"):
            validate_network_edge_style("->")


class TestValidation(unittest.TestCase):
    def test_nodes_are_inferred_from_edges(self):
        nodes = infer_network_nodes(EDGES)
        self.assertEqual([n["id"] for n in nodes], ["A", "B", "C", "D"])
        validate_network_records(nodes, EDGES, NETWORK_LAYOUT.SPRING)

    def test_front_leaves_the_data_untouched(self):
        data = {"edges": [edge("A", "B")]}
        NetworkChart(data)
        self.assertEqual(data, {"edges": [edge("A", "B")]})

    def test_duplicate_ids_raise(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            validate_network_records(
                [{"id": "A"}, {"id": "A"}], [], NETWORK_LAYOUT.SPRING
            )

    def test_unknown_endpoint_raises(self):
        with self.assertRaisesRegex(ValueError, "'Z'"):
            validate_network_records(NODES, [edge("A", "Z")], NETWORK_LAYOUT.SPRING)

    def test_self_loop_raises(self):
        with self.assertRaisesRegex(ValueError, "itself"):
            validate_network_records(NODES, [edge("A", "A")], NETWORK_LAYOUT.SPRING)

    def test_non_positive_size_and_weight_raise(self):
        with self.assertRaisesRegex(ValueError, "size"):
            validate_network_records([{"id": "A", "size": 0}], [], "spring")
        with self.assertRaisesRegex(ValueError, "size"):
            validate_network_records([{"id": "A", "size": True}], [], "spring")
        with self.assertRaisesRegex(ValueError, "weight"):
            validate_network_records(NODES, [edge("A", "B", -1)], "spring")
        # numpy scalars are numbers
        validate_network_records(
            [{"id": "A", "size": np.float64(2)}, {"id": "B"}],
            [edge("A", "B", np.int64(3))],
            "spring",
        )

    def test_bad_records_raise(self):
        with self.assertRaisesRegex(ValueError, "`id`"):
            validate_network_records([{"label": "A"}], [], "spring")
        with self.assertRaisesRegex(ValueError, "`source`"):
            validate_network_records([{"id": "A"}], [{"source": "A"}], "spring")
        with self.assertRaisesRegex(ValueError, "emphasis"):
            validate_network_records([{"id": "A", "emphasis": "bold"}], [], "spring")
        with self.assertRaisesRegex(ValueError, "at least one node"):
            validate_network_records(infer_network_nodes([]), [], "spring")

    def test_fixed_layout_needs_x_and_y(self):
        with self.assertRaisesRegex(ValueError, "`x`"):
            validate_network_records([{"id": "A", "x": 0.5}], [], NETWORK_LAYOUT.FIXED)
        validate_network_records([{"id": "A", "x": 0.5, "y": 0.5}], [], "fixed")

    def test_every_layout_member_validates(self):
        for layout in ("spring", "weighted", "grouped", "circular"):
            validate_network_records([{"id": "A"}], [], layout)

    def test_unknown_layout_raises(self):
        with self.assertRaisesRegex(ValueError, "layout"):
            validate_network_records(NODES, EDGES, "shell")

    def test_front_rejects_emphasis_and_bad_shape(self):
        with self.assertRaisesRegex(ValueError, "emphasis"):
            NetworkChart(DATA, emphasis=EMPHASIS.HIGHLIGHT)
        with self.assertRaisesRegex(ValueError, "edges"):
            NetworkChart({"nodes": NODES})
        with self.assertRaisesRegex(ValueError, "edges"):
            NetworkChart(EDGES)


class TestLayouts(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_circular_places_nodes_on_a_circle(self):
        pos = circular_layout(6)
        radii = np.linalg.norm(pos - 0.5, axis=1)
        np.testing.assert_allclose(radii, radii[0])
        # the first node sits at the top
        np.testing.assert_allclose(pos[0], [0.5, 0.5 + radii[0]])

    def test_spring_is_seeded(self):
        pairs = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
        a = spring_layout(4, pairs, seed=0)
        b = spring_layout(4, pairs, seed=0)
        c = spring_layout(4, pairs, seed=7)
        np.testing.assert_array_equal(a, b)
        self.assertFalse(np.allclose(a, c))
        self.assertTrue((a >= 0).all() and (a <= 1).all())

    def test_spring_keeps_a_margin(self):
        pos = spring_layout(5, [(0, 1), (1, 2), (2, 3), (3, 4)], seed=1)
        self.assertGreaterEqual(pos.min(), 0.05)
        self.assertLessEqual(pos.max(), 0.95)
        # a single node sits at the centre
        np.testing.assert_allclose(spring_layout(1, [], seed=0), [[0.5, 0.5]])

    def test_seed_changes_the_picture(self):
        same = _positions(NetworkChart(DATA))
        again = _positions(NetworkChart(DATA))
        other = _positions(NetworkChart(DATA, seed=3))
        np.testing.assert_array_equal(same, again)
        self.assertFalse(np.allclose(same, other))

    def test_fixed_uses_the_given_positions(self):
        nodes = [{"id": "A", "x": 0.1, "y": 0.9}, {"id": "B", "x": 0.8, "y": 0.2}]
        figure = NetworkChart(
            {"nodes": nodes, "edges": [edge("A", "B")]}, layout=NETWORK_LAYOUT.FIXED
        )
        np.testing.assert_allclose(_positions(figure), [[0.1, 0.9], [0.8, 0.2]])
        with self.assertRaisesRegex(ValueError, "`y`"):
            NetworkChart(
                {"nodes": [{"id": "A", "x": 0.1}], "edges": []}, layout="fixed"
            )

    def test_edge_strengths_map_min_max_onto_the_pull_range(self):
        # the lightest pulls at the minimum, the heaviest at the maximum,
        # a missing weight as the lightest
        strengths = edge_strengths([1, 5, None, 3])
        self.assertAlmostEqual(strengths[0], NETWORK_PULL_MIN)
        self.assertAlmostEqual(strengths[1], NETWORK_PULL_MAX)
        self.assertAlmostEqual(strengths[2], NETWORK_PULL_MIN)
        self.assertAlmostEqual(strengths[3], (NETWORK_PULL_MIN + NETWORK_PULL_MAX) / 2)
        # no weights, or all equal: every edge pulls at one
        self.assertEqual(edge_strengths([None, None]), [1.0, 1.0])
        self.assertEqual(edge_strengths([2, 2, None]), [1.0, 1.0, 1.0])

    def test_weighted_without_weights_is_the_spring_picture(self):
        plain = _positions(NetworkChart(DATA))
        weighted = _positions(NetworkChart(DATA, layout=NETWORK_LAYOUT.WEIGHTED))
        np.testing.assert_array_equal(plain, weighted)

    def test_weighted_pulls_the_heavy_edge_short(self):
        # a path A-B-C-D: the heavy edge ends up the shortest
        edges = [edge("A", "B", 1), edge("B", "C", 9), edge("C", "D", 1)]
        pos = _positions(NetworkChart({"edges": edges}, layout="weighted"))
        lengths = np.linalg.norm(np.diff(pos, axis=0), axis=1)
        self.assertEqual(lengths.argmin(), 1)
        plain = _positions(NetworkChart({"edges": edges}))
        self.assertFalse(np.allclose(plain, pos))

    def test_grouped_keeps_clusters_apart(self):
        groups = ["x", "x", "x", "y", "y", None]
        pairs = [(0, 1), (1, 2), (3, 4), (2, 3), (4, 5)]
        pos, clusters = grouped_layout(groups, pairs, [None] * 5, seed=0)
        self.assertTrue((pos >= 0).all() and (pos <= 1).all())
        x, y, lone = pos[:3], pos[3:5], pos[5]
        # every node sits closer to its own cluster's centre than to the other's
        for point in x:
            self.assertLess(
                np.linalg.norm(point - x.mean(axis=0)),
                np.linalg.norm(point - y.mean(axis=0)),
            )
        for point in y:
            self.assertLess(
                np.linalg.norm(point - y.mean(axis=0)),
                np.linalg.norm(point - x.mean(axis=0)),
            )
        # the ungrouped node is a cluster of its own, apart from both
        self.assertGreater(np.linalg.norm(pos[:5] - lone, axis=1).min(), 0.05)

    def test_grouped_without_groups_is_one_cluster_per_node(self):
        # every node a group of one: the group level places them all
        pos, clusters = grouped_layout(
            [None] * 4, [(0, 1), (1, 2), (2, 3)], [None] * 3, 0
        )
        self.assertEqual(clusters, [])
        self.assertEqual(len({tuple(p) for p in pos.round(6)}), 4)
        self.assertTrue((pos >= 0).all() and (pos <= 1).all())

    def test_grouped_weighs_the_summed_links_between_groups(self):
        # x-y: three edges summing to 6 (a missing weight counts one);
        # x-z: one edge of 4. x sits nearer y.
        nodes = [{"id": n, "group": n[0]} for n in ("x1", "x2", "y1", "y2", "z1", "z2")]
        edges = [
            edge("x1", "x2"),
            edge("y1", "y2"),
            edge("z1", "z2"),
            edge("x1", "y1", 2),
            edge("x2", "y2", 3),
            edge("x1", "y2"),
            edge("x2", "z1", 4),
        ]
        pos = _positions(
            NetworkChart(
                {"nodes": nodes, "edges": edges}, layout=NETWORK_LAYOUT.GROUPED
            )
        )
        x, y, z = pos[:2].mean(axis=0), pos[2:4].mean(axis=0), pos[4:].mean(axis=0)
        self.assertLess(np.linalg.norm(x - y), np.linalg.norm(x - z))

    def test_grouped_holds_a_member_with_no_edge_inside_its_group(self):
        # c has no edge inside group x; gravity keeps it with its cluster,
        # and the linked pair a-b stays clear of each other
        groups = ["x", "x", "x", "y", "y", "y"]
        pairs = [(0, 1), (3, 4), (4, 5), (2, 3)]
        pos, _ = grouped_layout(groups, pairs, [None] * 4, seed=0)
        x, y = pos[:3], pos[3:]
        self.assertLess(
            np.linalg.norm(pos[2] - x.mean(axis=0)),
            np.linalg.norm(pos[2] - y.mean(axis=0)),
        )
        self.assertGreater(np.linalg.norm(pos[0] - pos[1]), 0.02)
        # a group with no link to any other still lands inside the space
        lone, _ = grouped_layout(["x", "x", "y", "y"], [(0, 1), (2, 3)], [None] * 2, 0)
        self.assertTrue((lone >= 0).all() and (lone <= 1).all())
        self.assertGreater(np.linalg.norm(lone[:2].mean(0) - lone[2:].mean(0)), 0.2)

    def test_grouped_is_seeded(self):
        data = {
            "nodes": [{"id": n, "group": n[0]} for n in ("a1", "a2", "b1", "b2")],
            "edges": [edge("a1", "a2"), edge("b1", "b2"), edge("a2", "b1")],
        }
        same = _positions(NetworkChart(data, layout="grouped"))
        again = _positions(NetworkChart(data, layout="grouped"))
        other = _positions(NetworkChart(data, layout="grouped", seed=3))
        np.testing.assert_array_equal(same, again)
        self.assertFalse(np.allclose(same, other))

    def test_circular_front(self):
        figure = NetworkChart(DATA, layout=NETWORK_LAYOUT.CIRCULAR)
        radii = np.linalg.norm(_positions(figure) - 0.5, axis=1)
        np.testing.assert_allclose(radii, radii[0])

    def test_axes_are_bare_and_square(self):
        ax = NetworkChart(DATA).axes[0]
        self.assertFalse(ax.axison)
        self.assertEqual(ax.get_xlim(), (0.0, 1.0))
        self.assertEqual(ax.get_ylim(), (0.0, 1.0))
        self.assertEqual(ax.get_aspect(), 1.0)


class TestEncoding(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_nodes_inferred_when_omitted(self):
        figure = NetworkChart({"edges": EDGES})
        self.assertEqual(len(_nodes(figure.axes[0]).get_offsets()), 4)
        self.assertEqual(sorted(_labels(figure.axes[0])), ["A", "B", "C", "D"])

    def test_undirected_edges_are_plain_lines_and_reverse_pairs_merge(self):
        ax = NetworkChart({"edges": [edge("A", "B"), edge("B", "A")]}).axes[0]
        edges = _edges(ax)
        self.assertEqual(list(edges), ["A->B"])
        self.assertIsInstance(edges["A->B"].get_arrowstyle(), ArrowStyle.Curve)

    def test_directed_edges_are_single_polygons(self):
        ax = NetworkChart(
            {"edges": [edge("A", "B"), edge("B", "A")]}, directed=True
        ).axes[0]
        edges = _edges(ax)
        self.assertEqual(sorted(edges), ["A->B", "B->A"])
        for patch in edges.values():
            self.assertIsInstance(patch.get_arrowstyle(), ArrowStyle.Simple)
            self.assertEqual(patch.get_linewidth(), 0)
            self.assertEqual(patch.get_edgecolor()[3], 0)

    def test_weight_maps_to_width(self):
        data = {"edges": [edge("A", "B", 1), edge("B", "C", 3), edge("C", "D")]}
        style = get_network_style({})
        ax = NetworkChart(data).axes[0]
        edges = _edges(ax)
        self.assertEqual(edges["A->B"].get_linewidth(), style["edge_width_min"])
        self.assertEqual(edges["B->C"].get_linewidth(), style["edge_width_max"])
        self.assertEqual(edges["C->D"].get_linewidth(), style["edge_width_min"])
        ax = NetworkChart(data, directed=True).axes[0]
        tails = {k: p.get_arrowstyle().tail_width for k, p in _edges(ax).items()}
        self.assertLess(tails["A->B"], tails["B->C"])
        self.assertEqual(tails["A->B"], style["edge_width_min"])

    def test_size_maps_by_sqrt_to_area(self):
        nodes = [
            {"id": "A", "size": 1},
            {"id": "B", "size": 4},
            {"id": "C", "size": 9},
            {"id": "D"},
        ]
        style = get_network_style({})
        sizes = _nodes(
            NetworkChart({"nodes": nodes, "edges": [edge("A", "B")]}).axes[0]
        ).get_sizes()
        self.assertEqual(sizes[0], style["node_size_min"])
        self.assertEqual(sizes[2], style["node_size_max"])
        # sqrt(4) is halfway between sqrt(1) and sqrt(9)
        self.assertAlmostEqual(
            sizes[1], (style["node_size_min"] + style["node_size_max"]) / 2
        )
        self.assertEqual(sizes[3], style["node_size"])

    def test_unsized_nodes_share_the_default_area(self):
        sizes = _nodes(NetworkChart(DATA).axes[0]).get_sizes()
        self.assertEqual(set(sizes), {get_network_style({})["node_size"]})

    def test_groups_take_the_multiple_cycle_and_the_legend(self):
        nodes = [
            {"id": "A", "group": "x"},
            {"id": "B", "group": "y"},
            {"id": "C", "group": "x"},
        ]
        figure = NetworkChart(
            {"nodes": nodes, "edges": [edge("A", "B")]}, show_legend=True
        )
        ax = figure.axes[0]
        colors = [to_rgb(c) for c in _nodes(ax).get_facecolors()]
        palette = [to_rgb(c) for c in DEFAULT_THEME["color_general_multiple"]]
        self.assertEqual(colors[0], palette[0])
        self.assertEqual(colors[1], palette[1])
        self.assertEqual(colors[2], palette[0])
        legend = ax.get_legend()
        self.assertIsNotNone(legend)
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["x", "y"])

    def test_ungrouped_nodes_share_the_singular_color(self):
        ax = NetworkChart(DATA, show_legend=True).axes[0]
        colors = {tuple(c) for c in _nodes(ax).get_facecolors()}
        self.assertEqual(len(colors), 1)
        self.assertIsNone(ax.get_legend())

    def test_grouped_draws_a_halo_behind_each_named_cluster(self):
        nodes = [{"id": "A", "group": "x"}, {"id": "B", "group": "x"}, {"id": "C"}]
        data = {"nodes": nodes, "edges": [edge("A", "B"), edge("B", "C")]}
        figure = NetworkChart(data, layout=NETWORK_LAYOUT.GROUPED)
        halos = [p for p in figure.axes[0].patches if isinstance(p, Circle)]
        self.assertEqual([p.get_gid() for p in halos], ["group:x"])
        halo = halos[0]
        self.assertEqual(halo.get_alpha(), DEFAULT_THEME["plot_network_group_alpha"])
        self.assertEqual(
            to_rgb(halo.get_facecolor()),
            to_rgb(DEFAULT_THEME["color_general_multiple"][0]),
        )
        # the disc, marker pad included, stays inside the axes
        self.assertGreaterEqual(min(halo.center) - halo.radius, 0.0)
        self.assertLessEqual(max(halo.center) + halo.radius, 1.0)
        # the cluster's nodes sit inside the disc, the ungrouped node outside
        pos = _positions(figure)
        inside = np.linalg.norm(pos - halo.center, axis=1) <= halo.radius
        self.assertEqual(inside.tolist(), [True, True, False])
        # zero alpha disables it; the other layouts never draw one
        for kwargs in (
            dict(layout="grouped", style={"plot_network_group_alpha": 0}),
            dict(layout="spring"),
        ):
            ax = NetworkChart(data, **kwargs).axes[0]
            self.assertFalse([p for p in ax.patches if isinstance(p, Circle)])

    def test_ungrouped_node_beside_groups_takes_the_edge_color(self):
        nodes = [{"id": "A", "group": "x"}, {"id": "B"}]
        ax = NetworkChart({"nodes": nodes, "edges": [edge("A", "B")]}).axes[0]
        colors = [to_rgb(c) for c in _nodes(ax).get_facecolors()]
        self.assertEqual(colors[0], to_rgb(DEFAULT_THEME["color_general_multiple"][0]))
        self.assertEqual(colors[1], to_rgb(DEFAULT_THEME["plot_network_edge_color"]))

    def test_show_values_writes_formatted_weights(self):
        data = {"edges": [edge("A", "B", 2.5), edge("B", "C")]}
        ax = NetworkChart(data, show_values=True, value_format="{x:.2f}").axes[0]
        self.assertEqual([t.get_text() for t in _values(ax)], ["2.50"])
        self.assertEqual(_values(NetworkChart(data).axes[0]), [])

    def test_value_sits_on_the_bowed_path(self):
        nodes = [{"id": "A", "x": 0.2, "y": 0.5}, {"id": "B", "x": 0.8, "y": 0.5}]
        data = {"nodes": nodes, "edges": [edge("A", "B", 1)]}
        curved = _values(NetworkChart(data, layout="fixed", show_values=True).axes[0])[
            0
        ]
        straight = _values(
            NetworkChart(
                data,
                layout="fixed",
                show_values=True,
                style={"plot_network_edge_style": ARROW_STYLE.STRAIGHT},
            ).axes[0]
        )[0]
        self.assertEqual(straight.get_position(), (0.5, 0.5))
        self.assertEqual(curved.get_position()[0], 0.5)
        self.assertNotEqual(curved.get_position()[1], 0.5)

    def test_labels_default_to_id_and_empty_draws_nothing(self):
        nodes = [{"id": "A", "label": "Alpha"}, {"id": "B", "label": ""}, {"id": "C"}]
        ax = NetworkChart({"nodes": nodes, "edges": [edge("A", "B")]}).axes[0]
        labels = _labels(ax)
        self.assertEqual(sorted(labels), ["A", "C"])
        self.assertEqual(labels["A"].get_text(), "Alpha")
        self.assertEqual(labels["C"].get_text(), "C")
        self.assertTrue(labels["A"].get_path_effects())

    def test_no_halo_when_width_is_zero(self):
        ax = NetworkChart(DATA, style={"plot_network_label_halo_width": 0}).axes[0]
        self.assertEqual(_labels(ax)["A"].get_path_effects(), [])

    def test_edge_style_and_curve(self):
        curved = _edges(NetworkChart(DATA).axes[0])["A->B"]
        self.assertAlmostEqual(curved.get_connectionstyle().rad, 0.2)
        flipped = _edges(
            NetworkChart(DATA, style={"plot_network_edge_curve": -0.4}).axes[0]
        )["A->B"]
        self.assertAlmostEqual(flipped.get_connectionstyle().rad, -0.4)
        straight = _edges(
            NetworkChart(
                DATA, style={"plot_network_edge_style": ARROW_STYLE.STRAIGHT}
            ).axes[0]
        )["A->B"]
        self.assertEqual(straight.get_connectionstyle().rad, 0.0)
        with self.assertRaisesRegex(ValueError, "directed"):
            NetworkChart(DATA, style={"plot_network_edge_style": ARROW_STYLE.ARROW})

    def test_directed_arrows_stop_at_the_target_radius(self):
        nodes = [{"id": "A", "size": 1}, {"id": "B", "size": 9}]
        ax = NetworkChart(
            {"nodes": nodes, "edges": [edge("A", "B")]}, directed=True
        ).axes[0]
        patch = _edges(ax)["A->B"]
        area = _nodes(ax).get_sizes()[1]
        # a scatter size is the marker's bounding-box diameter squared
        self.assertAlmostEqual(patch.shrinkB, np.sqrt(area) / 2)

    def test_subplots(self):
        figure = NetworkChart([DATA, {"edges": [edge("X", "Y")]}])
        self.assertEqual(len(figure.axes), 2)
        self.assertEqual(len(_nodes(figure.axes[1]).get_offsets()), 2)


class TestEmphasis(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_background_mutes_the_node_its_label_and_its_edges(self):
        nodes = [{"id": "A", "emphasis": "background"}, {"id": "B"}, {"id": "C"}]
        ax = NetworkChart(
            {"nodes": nodes, "edges": [edge("A", "B"), edge("B", "C")]}
        ).axes[0]
        muted = to_rgb(DEFAULT_THEME["muted_color"])
        scatter = _nodes(ax)
        faces = [to_rgb(c) for c in scatter.get_facecolors()]
        self.assertEqual(faces[0], muted)
        self.assertNotEqual(faces[1], muted)
        self.assertEqual(faces[1], faces[2])
        self.assertEqual(scatter.get_facecolors()[0][3], DEFAULT_THEME["muted_alpha"])
        self.assertEqual(to_rgb(_labels(ax)["A"].get_color()), muted)
        edges = _edges(ax)
        self.assertEqual(to_rgb(edges["A->B"].get_edgecolor()), muted)
        self.assertEqual(edges["A->B"].get_alpha(), DEFAULT_THEME["muted_alpha"])
        self.assertNotEqual(to_rgb(edges["B->C"].get_edgecolor()), muted)

    def test_highlight_strokes_the_node_only(self):
        nodes = [{"id": "A", "emphasis": "highlight"}, {"id": "B"}]
        ax = NetworkChart({"nodes": nodes, "edges": [edge("A", "B")]}).axes[0]
        scatter = _nodes(ax)
        style = get_network_style({})
        edge_colors = [to_rgb(c) for c in scatter.get_edgecolors()]
        widths = list(scatter.get_linewidths())
        self.assertEqual(edge_colors[0], to_rgb(DEFAULT_THEME["font_general_color"]))
        self.assertEqual(edge_colors[1], to_rgb(style["edgecolor"]))
        self.assertEqual(widths[0], style["highlight_linewidth"])
        self.assertEqual(widths[1], style["linewidth"])
        faces = scatter.get_facecolors()
        self.assertEqual(tuple(faces[0]), tuple(faces[1]))


class TestComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_rejects(self):
        network = NetworkChart(DATA)
        line = LineChart(LINE)
        with self.assertRaisesRegex(ValueError, "Grid"):
            Panel([network, line])

    def test_grid_accepts_and_keeps_the_layout(self):
        network = NetworkChart(DATA)
        line = LineChart(LINE)
        grid = Grid([[network, line]])
        self.assertEqual(len(grid.axes), 2)
        np.testing.assert_array_equal(
            _positions(network), _nodes(grid.axes[0]).get_offsets().data
        )
        self.assertFalse(grid.axes[0].axison)

    def test_layer_kind(self):
        panel = NetworkChart(DATA)._chart_metadata["panel"]
        layer = panel.layers[0]
        self.assertIsInstance(layer, NetworkLayer)
        self.assertEqual(layer.kind, "network")
        self.assertTrue(layer.bare)


if __name__ == "__main__":
    unittest.main()
