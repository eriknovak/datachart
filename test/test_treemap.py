"""Tests for the treemap: style, validation, tiling, labels, emphasis, and composition."""

import unittest
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import Rectangle

from datachart.charts import Treemap, LineChart
from datachart.config import config
from datachart.constants import THEME, EMPHASIS
from datachart.utils import Panel, Grid
from datachart.utils._internal.config_helpers import get_treemap_style
from datachart.utils._internal.layers import _fit_text, _squarify, _wrap_label
from datachart.utils._internal.validate import validate_treemap_records

THEMES = [
    THEME.DEFAULT,
    THEME.GREYSCALE,
    THEME.INK,
    THEME.HATCH,
    THEME.MINIMAL,
    THEME.MATERIAL,
    THEME.SKETCH,
]

TREEMAP_KEYS = (
    "plot_treemap_edge_color",
    "plot_treemap_edge_width",
    "plot_treemap_group_edge_width",
    "plot_treemap_group_pad",
    "plot_treemap_level_shade",
    "plot_treemap_level_font_scale",
    "plot_treemap_min_fontsize",
    "plot_treemap_highlight_edge_width",
    "plot_treemap_label_halo_width",
)


def rec(label, value=None, children=None, emphasis=None):
    record = {"label": label}
    if value is not None:
        record["value"] = value
    if children is not None:
        record["children"] = children
    if emphasis is not None:
        record["emphasis"] = emphasis
    return record


FLAT = [rec("A", 40), rec("B", 30), rec("C", 20), rec("D", 10)]
NESTED = [
    rec("Asia", children=[rec("India", 1429), rec("China", 1426), rec("Japan", 123)]),
    rec("Africa", children=[rec("Nigeria", 224), rec("Ethiopia", 127)]),
    rec("Europe", children=[rec("Russia", 144), rec("Germany", 83)]),
    rec("Oceania", 45),
]
LINE = [{"x": 0, "y": 1}, {"x": 1, "y": 2}]


def deep(levels):
    """One record tree `levels` deep: A > B > C > ... with a leaf at the end."""
    record = rec("L%d" % levels, 1)
    for level in range(levels - 1, 0, -1):
        record = rec("L%d" % level, children=[record])
    return [record]


# a four-level tree: Asia > East Asia > China > Guangdong
DEEP = [
    rec(
        "Asia",
        children=[
            rec(
                "East Asia",
                children=[
                    rec(
                        "China", children=[rec("Guangdong", 127), rec("Shandong", 101)]
                    ),
                    rec("Japan", 123),
                ],
            ),
            rec("South Asia", children=[rec("India", 1429), rec("Pakistan", 240)]),
        ],
    ),
    rec("Africa", children=[rec("Nigeria", 224), rec("Ethiopia", 127)]),
    rec("Oceania", 45),
]


def _tiles(ax):
    """The leaf tiles keyed by label."""
    return {
        p.get_gid()[len("tile:") :]: p
        for p in ax.patches
        if isinstance(p, Rectangle) and (p.get_gid() or "").startswith("tile:")
    }


def _boxes(ax):
    """The group borders keyed by group label."""
    return {
        p.get_gid()[len("group:") :]: p
        for p in ax.patches
        if isinstance(p, Rectangle) and (p.get_gid() or "").startswith("group:")
    }


def _bands(ax):
    return {
        p.get_gid()[len("band:") :]: p
        for p in ax.patches
        if isinstance(p, Rectangle) and (p.get_gid() or "").startswith("band:")
    }


def _area(patch):
    return patch.get_width() * patch.get_height()


def _texts(ax):
    return [t.get_text() for t in ax.texts]


def _aspects(fig, ax):
    """Each tile's drawn width:height (or height:width) ratio, keyed by label."""
    fig.canvas.draw()
    fw, fh = fig.get_size_inches()
    pos = ax.get_position()
    pw, ph = fw * pos.width, fh * pos.height
    ratios = {}
    for label, tile in _tiles(ax).items():
        w, h = tile.get_width() * pw, tile.get_height() * ph
        ratios[label] = max(w / h, h / w)
    return ratios


class TestTreemapStyle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)

    def test_style_resolves_from_config(self):
        style = get_treemap_style({})
        self.assertEqual(style["edgecolor"], config["plot_treemap_edge_color"])
        self.assertEqual(style["level_shade"], config["plot_treemap_level_shade"])
        self.assertEqual(style["halo_width"], config["plot_treemap_label_halo_width"])

    def test_chart_style_overrides(self):
        style = get_treemap_style({"plot_treemap_group_pad": 0.05})
        self.assertEqual(style["group_pad"], 0.05)

    def test_every_theme_sets_the_treemap_keys(self):
        for theme in THEMES:
            config.set_theme(theme)
            for key in TREEMAP_KEYS:
                self.assertIn(key, config.config, f"{theme} lacks {key}")

    def test_edge_color_follows_bar_edges(self):
        for theme, color in (
            (THEME.GREYSCALE, "#000000"),
            (THEME.HATCH, "#000000"),
            (THEME.INK, "#0B1F44"),
        ):
            config.set_theme(theme)
            self.assertEqual(config["plot_treemap_edge_color"], color)


class TestValidation(unittest.TestCase):
    def test_valid_records_pass(self):
        validate_treemap_records(FLAT)
        validate_treemap_records(NESTED)
        validate_treemap_records(DEEP)
        validate_treemap_records(deep(4))
        # an inner group may carry its children's sum too
        validate_treemap_records(
            [rec("A", 3, children=[rec("a", 3, children=[rec("x", 1), rec("y", 2)])])]
        )
        # a parent may carry its children's sum
        validate_treemap_records([rec("A", 3, children=[rec("a", 1), rec("b", 2)])])
        validate_treemap_records([rec("A", 3.0, children=[rec("a", 1), rec("b", 2)])])

    def test_numpy_values_are_accepted(self):
        import numpy as np

        validate_treemap_records([rec("A", np.int64(3)), rec("B", np.float32(1.5))])

    def test_bad_records_raise(self):
        for records in (
            [],
            None,
            "A",
            [{"value": 1}],
            [{"label": "A"}],
            ["A"],
            [rec("A", 0)],
            [rec("A", -2)],
            [rec("A", "x")],
            [rec("A", True)],
            [rec("A", children=[])],
            deep(5),
            [rec("A", 5, children=[rec("a", 1), rec("b", 2)])],
            [rec("A", 1, emphasis="bold")],
            [rec("A", children=[rec("a", 1, emphasis="nope")])],
            [rec("A", 1), rec("A", 2)],
            [rec("A", children=[rec("a", 1), rec("a", 2)])],
            [rec("A", children=[rec("a", children=[rec("x", 1), rec("x", 2)])])],
        ):
            with self.subTest(records=records), self.assertRaises(ValueError):
                validate_treemap_records(records)

    def test_messages_name_the_rule(self):
        with self.assertRaisesRegex(ValueError, "greater than 0"):
            validate_treemap_records([rec("A", 0)])
        with self.assertRaisesRegex(ValueError, "four levels"):
            validate_treemap_records(deep(5))
        with self.assertRaisesRegex(ValueError, "sum"):
            validate_treemap_records([rec("A", 5, children=[rec("a", 1)])])
        with self.assertRaisesRegex(ValueError, "emphasis"):
            validate_treemap_records([rec("A", 1, emphasis="bold")])
        with self.assertRaisesRegex(ValueError, "unique"):
            validate_treemap_records([rec("A", 1), rec("A", 2)])
        with self.assertRaisesRegex(ValueError, "unique"):
            validate_treemap_records(
                [rec("A", children=[rec("a", children=[rec("x", 1), rec("x", 2)])])]
            )
        with self.assertRaisesRegex(ValueError, "sum"):
            validate_treemap_records(
                [rec("A", children=[rec("a", 5, children=[rec("x", 1)])])]
            )
        # the same label may recur across groups
        validate_treemap_records(
            [rec("A", children=[rec("Rest", 1)]), rec("B", children=[rec("Rest", 1)])]
        )

    def test_front_rejects_emphasis_and_bad_shape(self):
        with self.assertRaisesRegex(ValueError, "emphasis"):
            Treemap({"data": FLAT}, emphasis=EMPHASIS.HIGHLIGHT)
        with self.assertRaises(ValueError):
            Treemap(FLAT)
        with self.assertRaises(ValueError):
            Treemap({"links": FLAT})


class TestSquarify(unittest.TestCase):
    def test_areas_are_proportional_and_fill_the_rect(self):
        values = [40, 30, 20, 10]
        rects = _squarify(values, 0, 0, 2, 1)
        areas = [w * h for _, _, w, h in rects]
        self.assertAlmostEqual(sum(areas), 2)
        for value, area in zip(values, areas):
            self.assertAlmostEqual(area, 2 * value / 100)

    def test_largest_is_top_left(self):
        rects = _squarify([40, 30, 20, 10], 0, 0, 2, 1)
        x, y, w, h = rects[0]
        self.assertAlmostEqual(x, 0)
        self.assertAlmostEqual(y + h, 1)
        for ox, oy, ow, oh in rects[1:]:
            self.assertGreaterEqual(ox + 1e-9, x)
            self.assertLessEqual(oy + oh, 1 + 1e-9)

    def test_tiles_stay_near_square(self):
        rects = _squarify([1] * 6, 0, 0, 3, 2)
        for _, _, w, h in rects:
            self.assertLessEqual(max(w / h, h / w), 1.5)

    def test_single_value_fills_the_rect(self):
        self.assertEqual(_squarify([7], 1, 2, 3, 4), [(1, 2, 3, 4)])


class TestTextLadder(unittest.TestCase):
    def test_wrap_splits_at_the_middle_space(self):
        self.assertEqual(_wrap_label("Rest of Asia"), "Rest of\nAsia")
        self.assertEqual(_wrap_label("North America"), "North\nAmerica")
        self.assertIsNone(_wrap_label("India"))

    def test_ladder_order(self):
        big = (400, 200)
        self.assertEqual(
            _fit_text("India", "1,429", big, 10, 8, 6)[:2], ("India", "1,429")
        )
        # the value goes before the label
        short = (400, 16.5)
        label, value, size, _ = _fit_text("India", "1,429", short, 10, 8, 6)
        self.assertEqual((label, value), ("India", None))
        self.assertEqual(size, 10)
        # a wide label wraps before it shrinks
        narrow = (60, 60)
        label, _, size, _ = _fit_text("Rest of Asia", None, narrow, 10, 8, 6)
        self.assertEqual(label, "Rest of\nAsia")
        self.assertEqual(size, 10)
        # then shrinks
        tight = (40, 40)
        label, _, size, _ = _fit_text("Rest of Asia", None, tight, 10, 8, 6)
        self.assertLess(size, 10)
        self.assertGreaterEqual(size, 6)
        # then drops
        self.assertIsNone(_fit_text("Rest of Asia", None, (10, 10), 10, 8, 6))

    def test_value_never_shrinks_below_the_minimum(self):
        fit = _fit_text("Hello World", "1234567", (40, 28), 10, 8, 6)
        self.assertIsNotNone(fit)
        _, value, size, value_size = fit
        self.assertEqual(value, "1234567")
        self.assertGreaterEqual(value_size, 6)
        # the size drawn is the size that was measured to fit
        label_h = 1.2 * size * 2
        self.assertLessEqual(label_h + 1.2 * value_size, 28 - 4)


class TestRendering(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_flat_tiles_are_proportional_largest_top_left(self):
        # the pad shaves every box, so the tiling is checked without it
        fig = Treemap({"data": FLAT}, style={"plot_treemap_group_pad": 0})
        ax = fig.axes[0]
        tiles = _tiles(ax)
        self.assertEqual(set(tiles), {"A", "B", "C", "D"})
        areas = {k: _area(p) for k, p in tiles.items()}
        self.assertAlmostEqual(areas["A"] / areas["D"], 4, delta=0.2)
        self.assertAlmostEqual(areas["B"] / areas["C"], 1.5, delta=0.1)
        a = tiles["A"]
        for other in ("B", "C", "D"):
            self.assertGreaterEqual(tiles[other].get_x() + 1e-9, a.get_x())
            self.assertLessEqual(
                tiles[other].get_y() + tiles[other].get_height(),
                a.get_y() + a.get_height() + 1e-9,
            )
        self.assertFalse(ax.axison)
        self.assertEqual(fig._chart_metadata["type"], "treemap")
        self.assertEqual(set(_texts(ax)), {"A", "B", "C", "D"})

    def test_input_order_does_not_matter(self):
        fig = Treemap({"data": list(reversed(FLAT))})
        tiles = _tiles(fig.axes[0])
        self.assertAlmostEqual(tiles["A"].get_x(), 0, delta=0.02)

    def test_nested_groups_are_boxes_with_bands(self):
        fig = Treemap({"data": NESTED}, figsize=(8, 5))
        ax = fig.axes[0]
        boxes, bands, tiles = _boxes(ax), _bands(ax), _tiles(ax)
        self.assertEqual(set(boxes), {"Asia", "Africa", "Europe"})
        self.assertEqual(set(bands), {"Asia", "Africa", "Europe"})
        self.assertIn("Oceania", tiles)
        self.assertIn("India", tiles)
        # the band sits on the box's top edge, the leaves below it
        asia, band = boxes["Asia"], bands["Asia"]
        self.assertAlmostEqual(
            band.get_y() + band.get_height(), asia.get_y() + asia.get_height()
        )
        self.assertLessEqual(
            tiles["India"].get_y() + tiles["India"].get_height(), band.get_y() + 1e-9
        )
        # the border is the tile stroke; the leaves share one tint lighter
        # than the band's group color
        self.assertEqual(
            to_rgb(asia.get_edgecolor()), to_rgb(config["plot_treemap_edge_color"])
        )
        group_rgb = to_rgb(band.get_facecolor())
        leaf_rgbs = {
            to_rgb(tiles[k].get_facecolor()) for k in ("India", "China", "Japan")
        }
        self.assertEqual(len(leaf_rgbs), 1)
        leaf_rgb = leaf_rgbs.pop()
        self.assertGreater(sum(leaf_rgb), sum(group_rgb))
        # a leaf's area is its share of the group's inner area
        self.assertAlmostEqual(
            _area(tiles["India"]) / _area(tiles["Japan"]), 1429 / 123, delta=0.5
        )

    def test_group_pad_separates_groups(self):
        fig = Treemap({"data": NESTED}, figsize=(8, 5))
        boxes = _boxes(fig.axes[0])
        xs = sorted(b.get_x() for b in boxes.values())
        rights = sorted(b.get_x() + b.get_width() for b in boxes.values())
        # every box is inset from the tiling span by half a pad
        pad = config["plot_treemap_group_pad"]
        self.assertAlmostEqual(xs[0], pad / 2)
        self.assertAlmostEqual(rights[-1], 1 - pad / 2)

    def test_zero_shade_keeps_group_color(self):
        fig = Treemap({"data": NESTED}, style={"plot_treemap_level_shade": 0})
        ax = fig.axes[0]
        self.assertEqual(
            to_rgb(_tiles(ax)["India"].get_facecolor()),
            to_rgb(_bands(ax)["Asia"].get_facecolor()),
        )

    def test_background_mutes_only_that_record(self):
        data = [rec("A", 40, emphasis="background"), rec("B", 30), rec("C", 20)]
        fig = Treemap({"data": data})
        tiles = _tiles(fig.axes[0])
        self.assertEqual(
            to_rgb(tiles["A"].get_facecolor()), to_rgb(config["muted_color"])
        )
        self.assertEqual(tiles["A"].get_alpha(), config["muted_alpha"])
        self.assertNotEqual(
            to_rgb(tiles["B"].get_facecolor()), to_rgb(config["muted_color"])
        )
        self.assertIsNone(tiles["B"].get_alpha())

    def test_highlight_is_the_border_only(self):
        data = [rec("A", 40, emphasis="highlight"), rec("B", 30), rec("C", 20)]
        fig = Treemap({"data": data})
        ax = fig.axes[0]
        tiles = _tiles(ax)
        self.assertEqual(
            to_rgb(tiles["A"].get_edgecolor()), to_rgb(config["font_general_color"])
        )
        self.assertEqual(
            tiles["A"].get_linewidth(), config["plot_treemap_highlight_edge_width"]
        )
        self.assertEqual(
            to_rgb(tiles["B"].get_edgecolor()),
            to_rgb(config["plot_treemap_edge_color"]),
        )
        self.assertEqual(tiles["B"].get_linewidth(), config["plot_treemap_edge_width"])
        weights = {t.get_text(): t.get_fontweight() for t in ax.texts}
        self.assertEqual(weights["A"], weights["B"])

    def test_group_emphasis_and_leaf_override(self):
        data = [
            rec(
                "Asia",
                emphasis="background",
                children=[rec("India", 1429, emphasis="highlight"), rec("China", 1426)],
            ),
            rec(
                "Africa",
                emphasis="highlight",
                children=[rec("Nigeria", 224), rec("Egypt", 113)],
            ),
            rec("Europe", children=[rec("Russia", 144)]),
        ]
        fig = Treemap({"data": data}, figsize=(8, 5))
        ax = fig.axes[0]
        tiles, boxes = _tiles(ax), _boxes(ax)
        muted = to_rgb(config["muted_color"])
        self.assertEqual(to_rgb(tiles["China"].get_facecolor()), muted)
        self.assertEqual(to_rgb(_bands(ax)["Asia"].get_facecolor()), muted)
        self.assertEqual(
            to_rgb(boxes["Asia"].get_edgecolor()),
            to_rgb(config["plot_treemap_edge_color"]),
        )
        self.assertNotEqual(to_rgb(tiles["India"].get_facecolor()), muted)
        self.assertEqual(
            to_rgb(tiles["India"].get_edgecolor()), to_rgb(config["font_general_color"])
        )
        self.assertEqual(
            boxes["Africa"].get_linewidth(), config["plot_treemap_highlight_edge_width"]
        )
        # a highlighted group strokes its leaves too; a muted group mutes them
        self.assertEqual(
            tiles["Nigeria"].get_linewidth(),
            config["plot_treemap_highlight_edge_width"],
        )
        self.assertEqual(
            to_rgb(tiles["Nigeria"].get_edgecolor()),
            to_rgb(config["font_general_color"]),
        )
        self.assertEqual(
            to_rgb(boxes["Africa"].get_edgecolor()),
            to_rgb(config["font_general_color"]),
        )
        self.assertEqual(
            boxes["Europe"].get_linewidth(), config["plot_treemap_group_edge_width"]
        )
        self.assertNotEqual(to_rgb(tiles["Nigeria"].get_facecolor()), muted)

    def test_unfit_labels_are_dropped_and_values_go_first(self):
        data = [rec("Big", 1000), rec("A very long label indeed", 1)]
        fig = Treemap({"data": data}, figsize=(4, 3))
        self.assertEqual(_texts(fig.axes[0]), ["Big"])
        data = [rec("Big", 100), rec("Mid", 20), rec("Small", 6)]
        # no shrinking: the value fits or it goes
        fig = Treemap(
            {"data": data},
            figsize=(4, 1.5),
            show_values=True,
            style={"plot_treemap_min_fontsize": config["font_general_size"]},
        )
        texts = _texts(fig.axes[0])
        self.assertIn("Big", texts)
        self.assertIn("100", texts)
        self.assertIn("Small", texts)
        self.assertNotIn("6", texts)

    def test_value_format(self):
        fig = Treemap({"data": FLAT}, show_values=True, value_format="{x:.1f}k")
        self.assertIn("40.0k", _texts(fig.axes[0]))
        fig = Treemap({"data": FLAT}, show_values=True, value_format="%d!")
        self.assertIn("40!", _texts(fig.axes[0]))

    def test_leaf_font_shrinks_per_level(self):
        fig = Treemap({"data": NESTED}, figsize=(8, 5))
        sizes = {t.get_text(): t.get_fontsize() for t in fig.axes[0].texts}
        general = config["font_general_size"]
        self.assertAlmostEqual(sizes["Oceania"], general)
        self.assertAlmostEqual(
            sizes["India"], general * config["plot_treemap_level_font_scale"]
        )
        self.assertAlmostEqual(sizes["Asia"], config["font_subtitle_size"])

    def test_band_text_uses_its_font_color_over_a_halo(self):
        fig = Treemap({"data": NESTED}, figsize=(8, 5))
        text = {t.get_text(): t for t in fig.axes[0].texts}["Asia"]
        self.assertEqual(
            to_rgb(text.get_color()), to_rgb(config["font_subtitle_color"])
        )
        self.assertEqual(len(text.get_path_effects()), 1)

    def test_no_halo_when_width_is_zero(self):
        fig = Treemap({"data": FLAT}, style={"plot_treemap_label_halo_width": 0})
        self.assertEqual(fig.axes[0].texts[0].get_path_effects(), [])

    def test_short_group_has_no_band_and_no_label(self):
        data = [
            rec("Big", 1000),
            rec("Mid", 60),
            rec("Tiny group", children=[rec("a", 1), rec("b", 1)]),
        ]
        fig = Treemap({"data": data}, figsize=(4, 3))
        ax = fig.axes[0]
        self.assertNotIn("Tiny group", _bands(ax))
        self.assertIn("Tiny group", _boxes(ax))
        self.assertNotIn("Tiny group", _texts(ax))

    def test_legend_lists_groups_only(self):
        fig = Treemap({"data": NESTED}, show_legend=True)
        legend = fig.axes[0].get_legend()
        self.assertIsNotNone(legend)
        labels = [t.get_text() for t in legend.get_texts()]
        self.assertEqual(labels, ["Asia", "Africa", "Europe", "Oceania"])
        # the tiles fill the axes, so the legend sits beside them
        self.assertEqual(legend._loc, 2)
        self.assertGreaterEqual(legend.get_bbox_to_anchor().x0, legend.axes.bbox.x1)
        self.assertIsNone(Treemap({"data": NESTED}).axes[0].get_legend())

    def test_texts_in_unit_space(self):
        fig = Treemap({"data": FLAT}, texts={"x": 0.5, "y": 0.5, "text": "note"})
        ax = fig.axes[0]
        self.assertIn("note", _texts(ax))
        self.assertEqual(ax.get_xlim(), (0, 1))
        self.assertEqual(ax.get_ylim(), (0, 1))

    def test_subplots(self):
        fig = Treemap([{"data": FLAT}, {"data": NESTED}], subtitle=["flat", "nested"])
        self.assertEqual(len(fig.axes), 2)
        self.assertEqual(set(_tiles(fig.axes[0])), {"A", "B", "C", "D"})
        self.assertIn("India", _tiles(fig.axes[1]))
        self.assertEqual(fig.axes[0].get_title(), "flat")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            Treemap([{"data": FLAT}, {"data": NESTED}], show_legend=True)
        self.assertTrue(any("show_legend" in str(w.message) for w in caught))

    def test_every_theme_renders(self):
        for theme in THEMES:
            config.set_theme(theme)
            fig = Treemap({"data": NESTED}, show_values=True, show_legend=True)
            self.assertIn("India", _tiles(fig.axes[0]))
            plt.close(fig)

    def test_sketch_draws_no_group_border(self):
        config.set_theme(THEME.SKETCH)
        fig = Treemap({"data": NESTED}, figsize=(8, 5))
        boxes = _boxes(fig.axes[0])
        self.assertEqual(boxes["Asia"].get_linewidth(), 0)
        # the highlight border is a separate width, so it still shows
        data = [rec("A", emphasis="highlight", children=[rec("a", 1)]), rec("B", 1)]
        fig = Treemap({"data": data})
        self.assertGreater(_boxes(fig.axes[0])["A"].get_linewidth(), 0)

    def test_dark_edge_themes_stroke_leaves_dark(self):
        config.set_theme(THEME.GREYSCALE)
        fig = Treemap({"data": FLAT})
        self.assertEqual(to_rgb(_tiles(fig.axes[0])["A"].get_edgecolor()), (0, 0, 0))

    def test_wide_and_square_figures_keep_tiles_near_square(self):
        for figsize in ((8, 3), (5, 5)):
            fig = Treemap({"data": FLAT}, figsize=figsize)
            ratios = _aspects(fig, fig.axes[0])
            # the largest tile is near square; the last, smallest one is the
            # worst squarify can do and varies with the renderer's metrics
            self.assertLessEqual(ratios["A"], 2.0, figsize)
            self.assertLessEqual(max(ratios.values()), 3.0, figsize)


class TestDeepNesting(unittest.TestCase):
    """Groups below the top level follow the top-level rules (ADR 0032)."""

    def tearDown(self):
        plt.close("all")

    def test_inner_groups_are_boxes_inside_their_parent(self):
        fig = Treemap({"data": DEEP}, figsize=(8, 5))
        ax = fig.axes[0]
        boxes, tiles = _boxes(ax), _tiles(ax)
        self.assertEqual(
            set(boxes), {"Asia", "East Asia", "China", "South Asia", "Africa"}
        )
        self.assertEqual(
            set(tiles),
            {"Guangdong", "Shandong", "Japan", "India", "Pakistan"}
            | {"Nigeria", "Ethiopia", "Oceania"},
        )
        asia, east, china = boxes["Asia"], boxes["East Asia"], boxes["China"]
        for inner, outer in ((east, asia), (china, east)):
            self.assertGreaterEqual(inner.get_x() + 1e-9, outer.get_x())
            self.assertGreaterEqual(inner.get_y() + 1e-9, outer.get_y())
            self.assertLessEqual(
                inner.get_x() + inner.get_width(),
                outer.get_x() + outer.get_width() + 1e-9,
            )
            self.assertLessEqual(
                inner.get_y() + inner.get_height(),
                outer.get_y() + outer.get_height() + 1e-9,
            )
        # an inner group's area is its share of the parent's inner area
        self.assertAlmostEqual(
            _area(boxes["South Asia"]) / _area(east), 1669 / 351, delta=0.5
        )
        self.assertAlmostEqual(
            _area(tiles["Guangdong"]) / _area(tiles["Shandong"]), 127 / 101, delta=0.05
        )

    def test_inner_groups_have_no_pad(self):
        fig = Treemap({"data": DEEP}, figsize=(8, 5))
        ax = fig.axes[0]
        boxes, bands = _boxes(ax), _bands(ax)
        asia, band = boxes["Asia"], bands["Asia"]
        inner = _area(asia) - _area(band)
        # the children fill the parent's area under the band exactly
        self.assertAlmostEqual(
            _area(boxes["East Asia"]) + _area(boxes["South Asia"]), inner
        )
        self.assertAlmostEqual(
            _area(boxes["China"]) + _area(_tiles(ax)["Japan"]),
            _area(boxes["East Asia"]) - _area(bands["East Asia"]),
        )
        # the level-1 pad is unchanged
        pad = config["plot_treemap_group_pad"]
        xs = sorted(b.get_x() for k, b in boxes.items() if k in ("Asia", "Africa"))
        self.assertAlmostEqual(xs[0], pad / 2)

    def test_inner_band_ladder_degrades_to_a_border(self):
        fig = Treemap({"data": DEEP}, figsize=(8, 5))
        ax = fig.axes[0]
        boxes, bands, texts = _boxes(ax), _bands(ax), _texts(ax)
        # a tall inner group has a band on its top edge, with its label
        self.assertIn("East Asia", bands)
        self.assertIn("East Asia", texts)
        box, band = boxes["East Asia"], bands["East Asia"]
        self.assertAlmostEqual(
            band.get_y() + band.get_height(), box.get_y() + box.get_height()
        )
        self.assertEqual(box.get_linewidth(), config["plot_treemap_group_edge_width"])
        # a short inner group draws its border only, and no label
        data = [
            rec(
                "Asia",
                children=[
                    rec("Big", 1000),
                    rec("Tiny group", children=[rec("a", 1), rec("b", 1)]),
                ],
            ),
            rec("Africa", 500),
        ]
        fig = Treemap({"data": data}, figsize=(4, 3))
        ax = fig.axes[0]
        self.assertIn("Tiny group", _boxes(ax))
        self.assertNotIn("Tiny group", _bands(ax))
        self.assertNotIn("Tiny group", _texts(ax))
        self.assertEqual(
            _boxes(ax)["Tiny group"].get_linewidth(),
            config["plot_treemap_group_edge_width"],
        )

    def test_tint_compounds_per_level(self):
        fig = Treemap({"data": DEEP}, figsize=(8, 5))
        ax = fig.axes[0]
        bands, tiles = _bands(ax), _tiles(ax)
        shade = config["plot_treemap_level_shade"]
        group = to_rgb(bands["Asia"].get_facecolor())
        # an inner band keeps its own level's color
        level2 = to_rgb(bands["East Asia"].get_facecolor())
        level3 = to_rgb(tiles["Japan"].get_facecolor())
        level4 = to_rgb(tiles["Guangdong"].get_facecolor())
        for parent, child in ((group, level2), (level2, level3), (level3, level4)):
            for p, c in zip(parent, child):
                self.assertAlmostEqual(c, p + (1 - p) * shade, places=2)
        fig = Treemap(
            {"data": DEEP}, figsize=(8, 5), style={"plot_treemap_level_shade": 0}
        )
        ax = fig.axes[0]
        bands, tiles = _bands(ax), _tiles(ax)
        for label in ("East Asia", "China"):
            self.assertEqual(to_rgb(bands[label].get_facecolor()), group)
        for label in ("Guangdong", "Japan", "India"):
            self.assertEqual(to_rgb(tiles[label].get_facecolor()), group)

    def test_label_font_scales_per_level(self):
        fig = Treemap({"data": DEEP}, figsize=(8, 5), show_values=True)
        sizes = {t.get_text(): t.get_fontsize() for t in fig.axes[0].texts}
        general = config["font_general_size"]
        scale = config["plot_treemap_level_font_scale"]
        self.assertAlmostEqual(sizes["Oceania"], general)
        self.assertAlmostEqual(sizes["Nigeria"], general * scale)
        self.assertAlmostEqual(sizes["Japan"], general * scale**2)
        self.assertAlmostEqual(sizes["Guangdong"], general * scale**3)
        # a band label starts from the subtitle size scaled the same way
        subtitle = config["font_subtitle_size"]
        self.assertAlmostEqual(sizes["Asia"], subtitle)
        self.assertAlmostEqual(sizes["East Asia"], subtitle * scale)
        self.assertAlmostEqual(sizes["China"], subtitle * scale**2)
        # values scale the same way
        self.assertAlmostEqual(sizes["45"], config["plot_bar_value_fontsize"])
        self.assertAlmostEqual(sizes["224"], config["plot_bar_value_fontsize"] * scale)

    def test_emphasis_inherits_down_the_subtree(self):
        data = [
            rec(
                "Asia",
                children=[
                    rec(
                        "East Asia",
                        emphasis="background",
                        children=[
                            rec(
                                "China",
                                children=[
                                    rec("Guangdong", 127, emphasis="highlight"),
                                    rec("Shandong", 101),
                                ],
                            ),
                            rec("Japan", 123),
                        ],
                    ),
                    rec(
                        "South Asia",
                        emphasis="highlight",
                        children=[rec("India", 1429), rec("Pakistan", 240)],
                    ),
                ],
            ),
            rec("Africa", children=[rec("Nigeria", 224)]),
        ]
        fig = Treemap({"data": data}, figsize=(8, 5))
        ax = fig.axes[0]
        boxes, bands, tiles = _boxes(ax), _bands(ax), _tiles(ax)
        muted = to_rgb(config["muted_color"])
        stroke = to_rgb(config["font_general_color"])
        # background on a level-2 group mutes its band and every tile under it
        self.assertEqual(to_rgb(bands["East Asia"].get_facecolor()), muted)
        self.assertEqual(to_rgb(tiles["Japan"].get_facecolor()), muted)
        self.assertEqual(to_rgb(tiles["Shandong"].get_facecolor()), muted)
        self.assertEqual(boxes["China"].get_alpha(), config["muted_alpha"])
        # a level-4 leaf's own role wins
        self.assertNotEqual(to_rgb(tiles["Guangdong"].get_facecolor()), muted)
        self.assertEqual(to_rgb(tiles["Guangdong"].get_edgecolor()), stroke)
        # highlight on an inner group strokes its border and its leaves
        self.assertEqual(to_rgb(boxes["South Asia"].get_edgecolor()), stroke)
        self.assertEqual(
            boxes["South Asia"].get_linewidth(),
            config["plot_treemap_highlight_edge_width"],
        )
        self.assertEqual(to_rgb(tiles["India"].get_edgecolor()), stroke)
        # the ancestors and the unrelated group are untouched
        self.assertNotEqual(to_rgb(bands["Asia"].get_facecolor()), muted)
        self.assertEqual(
            to_rgb(boxes["Asia"].get_edgecolor()),
            to_rgb(config["plot_treemap_edge_color"]),
        )
        self.assertNotEqual(to_rgb(tiles["Nigeria"].get_facecolor()), muted)

    def test_legend_stays_top_level(self):
        fig = Treemap({"data": DEEP}, show_legend=True)
        legend = fig.axes[0].get_legend()
        labels = [t.get_text() for t in legend.get_texts()]
        self.assertEqual(labels, ["Asia", "Africa", "Oceania"])

    def test_deep_tree_in_every_theme_and_in_a_grid(self):
        for theme in THEMES:
            config.set_theme(theme)
            fig = Treemap({"data": DEEP}, show_values=True)
            self.assertIn("Guangdong", _tiles(fig.axes[0]))
            plt.close(fig)
        config.set_theme(THEME.DEFAULT)
        grid = Grid([[Treemap({"data": DEEP}), LineChart(LINE)]])
        self.assertIn("China", _boxes(grid.axes[0]))


class TestComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_panel_rejects(self):
        treemap = Treemap({"data": FLAT})
        line = LineChart(LINE)
        with self.assertRaisesRegex(ValueError, "Grid"):
            Panel([treemap, line])

    def test_grid_accepts(self):
        treemap = Treemap({"data": NESTED}, title="world")
        line = LineChart(LINE)
        grid = Grid([[treemap, line]])
        self.assertEqual(len(grid.axes), 2)
        self.assertIn("India", _tiles(grid.axes[0]))
        self.assertFalse(grid.axes[0].axison)
        self.assertEqual(grid.axes[0].get_title(), "world")

    def test_grid_cell_tiles_in_its_own_aspect(self):
        treemap = Treemap(
            {"data": FLAT}, figsize=(3, 6), style={"plot_treemap_group_pad": 0}
        )
        grid = Grid([[treemap, LineChart(LINE)]], figsize=(10, 4))
        ratios = _aspects(grid, grid.axes[0])
        self.assertLessEqual(ratios["A"], 2.0)
        self.assertLessEqual(max(ratios.values()), 3.0)


if __name__ == "__main__":
    unittest.main()
