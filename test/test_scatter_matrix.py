"""Tests for the scatter matrix: inputs, cells, legend, composition (ADR 0051)."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PathCollection
from matplotlib.colors import to_hex

from datachart.charts import LineChart, ScatterMatrix
from datachart.config import config
from datachart.constants import DIAGONAL, THEME
from datachart.utils import Grid, Panel
from datachart.utils._internal.layers import (
    HistogramLayer,
    KdeLayer,
    ScatterLayer,
    TextLayer,
)

THEMES = [
    THEME.DEFAULT,
    THEME.GREYSCALE,
    THEME.INK,
    THEME.HATCH,
    THEME.MINIMAL,
    THEME.MATERIAL,
    THEME.SKETCH,
    THEME.QUILL,
]


def columns():
    rng = np.random.RandomState(3)
    a = rng.randn(30)
    return {
        "a": list(a),
        "name": [f"n{i}" for i in range(30)],
        "b": list(a + rng.randn(30)),
        "species": ["x", "y", "z"] * 10,
        "c": list(rng.randn(30)),
    }


def records():
    data = columns()
    return [dict(zip(data, row)) for row in zip(*data.values())]


def cell_kinds(figure):
    """The layer classes of each cell, keyed by (row, col)."""
    return {
        (c["spec"]["row"], c["spec"]["col"]): {type(l) for l in c["panel"].layers}
        for c in figure._chart_metadata["cells"]
    }


def cell_axes(figure):
    """The cell axes keyed by (row, col); legend axes and twins are left out."""
    shape = figure._chart_metadata["shape"]
    axes = {}
    for ax in figure.axes:
        ss = ax.get_subplotspec()
        if ss.colspan.start < shape[1]:
            # a host axes is added before its twin
            axes.setdefault((ss.rowspan.start, ss.colspan.start), ax)
    return axes


class TestScatterMatrixInputs(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_dimensions_default_to_numeric_non_hue_columns(self):
        figure = ScatterMatrix(columns(), hue="species")
        axes = cell_axes(figure)
        self.assertEqual(figure._chart_metadata["shape"], (3, 3))
        self.assertEqual([axes[(2, j)].get_xlabel() for j in range(3)], ["a", "b", "c"])
        self.assertEqual([axes[(i, 0)].get_ylabel() for i in range(3)], ["a", "b", "c"])

    def test_records_match_columns(self):
        a = ScatterMatrix(columns())._chart_metadata
        b = ScatterMatrix(records())._chart_metadata
        self.assertEqual(a["shape"], b["shape"])
        for ca, cb in zip(a["cells"], b["cells"]):
            self.assertEqual(ca["spec"], cb["spec"])
            self.assertEqual(
                [l.chart["data"] for l in ca["panel"].layers],
                [l.chart["data"] for l in cb["panel"].layers],
            )

    def test_dimensions_select_and_order(self):
        figure = ScatterMatrix(columns(), dimensions=["c", "a"])
        axes = cell_axes(figure)
        self.assertEqual(figure._chart_metadata["shape"], (2, 2))
        self.assertEqual([axes[(1, j)].get_xlabel() for j in range(2)], ["c", "a"])

    def test_numeric_hue_raises(self):
        with self.assertRaisesRegex(ValueError, "numeric"):
            ScatterMatrix(columns(), hue="a", dimensions=["b", "c"])

    def test_invalid_inputs_raise(self):
        cases = [
            ({"data": {"a": [1, 2], "b": [1]}}, "same length"),
            ({"data": "nope"}, "dict of columns"),
            ({"data": {"s": ["x", "y"]}}, "no numeric"),
            ({"data": columns(), "dimensions": ["zz"]}, "not a column"),
            ({"data": columns(), "dimensions": ["name"]}, "numeric values"),
            ({"data": columns(), "dimensions": []}, "at least one"),
            ({"data": columns(), "hue": "zz"}, "not a column"),
            ({"data": {"a": [1, 2], "h": ["x", None]}, "hue": "h"}, "missing"),
            (
                {"data": columns(), "hue": "species", "dimensions": ["species"]},
                "both",
            ),
            ({"data": columns(), "diagonal": "violin"}, "diagonal"),
        ]
        for kwargs, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    ScatterMatrix(**kwargs)

    def test_missing_values_drop_pairwise(self):
        data = {"a": [1.0, 2.0, None, 4.0], "b": [1.0, None, 3.0, 4.0]}
        figure = ScatterMatrix(data)
        (layer,) = [
            l
            for c in figure._chart_metadata["cells"]
            if (c["spec"]["row"], c["spec"]["col"]) == (1, 0)
            for l in c["panel"].layers
        ]
        self.assertEqual(len(layer.chart["data"]), 2)


class TestScatterMatrixCells(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_default_cells(self):
        kinds = cell_kinds(ScatterMatrix(columns()))
        self.assertEqual(len(kinds), 9)
        for (i, j), layers in kinds.items():
            expected = HistogramLayer if i == j else ScatterLayer
            self.assertEqual(layers, {expected})

    def test_diagonal_modes(self):
        for mode, expected in [
            (DIAGONAL.HIST, {HistogramLayer}),
            (DIAGONAL.KDE, {KdeLayer}),
            (DIAGONAL.NONE, set()),
        ]:
            with self.subTest(mode=mode):
                kinds = cell_kinds(ScatterMatrix(columns(), diagonal=mode))
                self.assertEqual(kinds[(1, 1)], expected)

    def test_kde_draws_one_curve_per_group(self):
        figure = ScatterMatrix(columns(), hue="species", diagonal=DIAGONAL.KDE)
        host = cell_axes(figure)[(0, 0)]
        (ax,) = [a for a in host._twinned_axes.get_siblings(host) if a is not host]
        self.assertEqual(len(ax.lines), 3)
        self.assertEqual(ax.get_ylim()[0], 0)

    def test_lower_only_blanks_upper_triangle(self):
        kinds = cell_kinds(
            ScatterMatrix(columns(), lower_only=True, show_correlation=True)
        )
        self.assertEqual(len(kinds), 9)
        for (i, j), layers in kinds.items():
            if i < j:
                self.assertEqual(layers, set())
        self.assertEqual(sum(1 for l in kinds.values() if l), 6)

    def test_lower_only_without_diagonal_trims_empty_edges(self):
        figure = ScatterMatrix(columns(), lower_only=True, diagonal=DIAGONAL.NONE)
        kinds = cell_kinds(figure)
        self.assertEqual(figure._chart_metadata["shape"], (2, 2))
        self.assertEqual(kinds[(0, 0)], {ScatterLayer})
        self.assertEqual(kinds[(0, 1)], set())
        axes = cell_axes(figure)
        self.assertEqual(axes[(0, 0)].get_ylabel(), "b")
        self.assertEqual(axes[(1, 1)].get_xlabel(), "b")

    def test_correlation_replaces_upper_triangle(self):
        figure = ScatterMatrix(
            columns(), hue="species", dimensions=["a", "b"], show_correlation=True
        )
        kinds = cell_kinds(figure)
        self.assertEqual(kinds[(0, 1)], {TextLayer})
        texts = [t.get_text() for t in cell_axes(figure)[(0, 1)].texts]
        self.assertEqual(len(texts), 3)
        data = columns()
        a, b = (np.array(data[k][0::3]) for k in ("a", "b"))
        self.assertEqual(texts[0], f"x: {np.corrcoef(a, b)[0, 1]:.2f}")
        ax = cell_axes(figure)[(0, 1)]
        figure.canvas.draw()
        ticks = ax.xaxis.get_major_ticks() + ax.yaxis.get_major_ticks()
        self.assertFalse(any(t.tick1line.get_visible() for t in ticks))
        # the scatter cells keep their tick marks
        scatter = cell_axes(figure)[(1, 0)]
        self.assertTrue(scatter.xaxis.get_major_ticks()[0].tick1line.get_visible())

    def test_correlation_without_hue_reads_r(self):
        figure = ScatterMatrix(columns(), dimensions=["a", "b"], show_correlation=True)
        texts = [t.get_text() for t in cell_axes(figure)[(0, 1)].texts]
        self.assertEqual(len(texts), 1)
        data = columns()
        self.assertEqual(texts[0], f"r = {np.corrcoef(data['a'], data['b'])[0, 1]:.2f}")

    def test_regression_line_per_group_in_group_color(self):
        figure = ScatterMatrix(
            columns(), hue="species", dimensions=["a", "b"], show_regression=True
        )
        ax = cell_axes(figure)[(1, 0)]
        self.assertEqual(len(ax.lines), 3)
        points = [c for c in ax.collections if isinstance(c, PathCollection)]
        self.assertEqual(
            [to_hex(l.get_color()) for l in ax.lines],
            [to_hex(c.get_facecolor()[0]) for c in points],
        )
        self.assertEqual(
            ax.lines[0].get_linewidth(),
            config["plot_scatter_matrix_regression_width"],
        )

    def test_pinned_regression_color_wins(self):
        figure = ScatterMatrix(
            columns(),
            hue="species",
            dimensions=["a", "b"],
            show_regression=True,
            style={"plot_scatter_matrix_regression_color": "#123456"},
        )
        ax = cell_axes(figure)[(1, 0)]
        self.assertEqual({to_hex(l.get_color()) for l in ax.lines}, {"#123456"})

    def test_hue_colors_match_across_cells(self):
        figure = ScatterMatrix(columns(), hue="species")
        axes = cell_axes(figure)
        colors = [
            [
                to_hex(c.get_facecolor()[0])
                for c in axes[key].collections
                if isinstance(c, PathCollection)
            ]
            for key in [(1, 0), (0, 2), (2, 1)]
        ]
        self.assertEqual(len(set(colors[0])), 3)
        self.assertEqual(colors[0], colors[1])
        self.assertEqual(colors[0], colors[2])

    def test_axes_share_by_column_and_row(self):
        figure = ScatterMatrix(columns())
        axes = cell_axes(figure)
        figure.canvas.draw()
        for j in range(3):
            for i in range(3):
                self.assertTrue(
                    axes[(i, j)].get_shared_x_axes().joined(axes[(i, j)], axes[(2, j)])
                )
                self.assertTrue(
                    axes[(j, i)].get_shared_y_axes().joined(axes[(j, i)], axes[(j, 0)])
                )
        self.assertFalse(
            axes[(0, 0)].get_shared_x_axes().joined(axes[(0, 0)], axes[(0, 1)])
        )
        # the diagonal shows its row's scale; its bars sit on a hidden twin
        self.assertEqual(axes[(1, 1)].get_ylim(), axes[(1, 0)].get_ylim())
        self.assertEqual(len(axes[(1, 1)].patches), 0)
        (twin,) = [
            a
            for a in axes[(1, 1)]._twinned_axes.get_siblings(axes[(1, 1)])
            if a is not axes[(1, 1)]
        ]
        self.assertGreater(len(twin.patches), 0)
        self.assertEqual(twin.get_ylim()[0], 0)

    def test_outer_tick_labels(self):
        figure = ScatterMatrix(columns(), show_correlation=True)
        axes = cell_axes(figure)
        figure.canvas.draw()

        def labelled(ax, axis):
            ticks = ax.get_xticklabels() if axis == "x" else ax.get_yticklabels()
            return any(t.get_visible() and t.get_text() for t in ticks)

        for i in range(3):
            self.assertTrue(labelled(axes[(i, 0)], "y"), i)
            self.assertTrue(labelled(axes[(2, i)], "x"), i)
        self.assertFalse(labelled(axes[(1, 1)], "x"))
        self.assertFalse(labelled(axes[(1, 2)], "y"))
        self.assertFalse(labelled(axes[(0, 1)], "x"))

    def test_blank_diagonal_moves_edge_labels_inward(self):
        figure = ScatterMatrix(columns(), diagonal=DIAGONAL.NONE)
        axes = cell_axes(figure)
        figure.canvas.draw()
        # row 0 and the last column have a blank outer cell
        self.assertEqual(axes[(0, 1)].get_ylabel(), "a")
        self.assertTrue(any(t.get_text() for t in axes[(0, 1)].get_yticklabels()))
        self.assertEqual(axes[(1, 2)].get_xlabel(), "c")
        self.assertTrue(any(t.get_text() for t in axes[(1, 2)].get_xticklabels()))
        self.assertEqual(axes[(2, 0)].get_xlabel(), "a")
        self.assertEqual(axes[(1, 2)].get_ylabel(), "")

    def test_unshared_axes_keep_their_tick_labels(self):
        figure = ScatterMatrix(columns(), sharex=False, sharey=False)
        axes = cell_axes(figure)
        figure.canvas.draw()
        self.assertTrue(any(t.get_text() for t in axes[(0, 1)].get_xticklabels()))
        self.assertTrue(any(t.get_text() for t in axes[(0, 1)].get_yticklabels()))
        self.assertIsNone(
            figure._chart_metadata["cells"][1]["panel"].settings.get("xmin")
        )
        self.assertFalse(
            axes[(0, 1)].get_shared_x_axes().joined(axes[(0, 1)], axes[(2, 1)])
        )
        # without a shared row the diagonal draws its counts on its own axis
        self.assertGreater(len(axes[(1, 1)].patches), 0)
        self.assertTrue(any(t.get_text() for t in axes[(1, 1)].get_yticklabels()))


class TestScatterMatrixLegend(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def legends(self, figure):
        return [ax.get_legend() for ax in figure.axes if ax.get_legend()]

    def test_one_figure_legend_with_hue(self):
        figure = ScatterMatrix(columns(), hue="species")
        (legend,) = self.legends(figure)
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["x", "y", "z"])

    def test_no_legend_without_hue_or_when_off(self):
        self.assertEqual(self.legends(ScatterMatrix(columns())), [])
        self.assertEqual(
            self.legends(ScatterMatrix(columns(), hue="species", show_legend=False)),
            [],
        )

    def test_legend_setting_title(self):
        figure = ScatterMatrix(columns(), hue="species", legend={"title": "Species"})
        (legend,) = self.legends(figure)
        self.assertEqual(legend.get_title().get_text(), "Species")

    def test_legend_wears_theme_font_with_blank_diagonal(self):
        config.set_theme(THEME.QUILL)
        try:
            figure = ScatterMatrix(columns(), hue="species", diagonal=DIAGONAL.NONE)
            (legend,) = self.legends(figure)
            family = legend.get_texts()[0].get_fontfamily()
            self.assertIn(config["font_general_serif"][0], family)
        finally:
            config.set_theme(THEME.DEFAULT)

    def test_single_dimension_takes_legend_from_diagonal(self):
        figure = ScatterMatrix(columns(), hue="species", dimensions=["a"])
        (legend,) = self.legends(figure)
        self.assertEqual(len(legend.get_texts()), 3)


class TestScatterMatrixComposition(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_grid_transport_shape(self):
        metadata = ScatterMatrix(columns(), title="M")._chart_metadata
        self.assertEqual(metadata["type"], "grid")
        self.assertEqual(metadata["shape"], (3, 3))
        self.assertEqual(metadata["title"], "M")
        self.assertEqual(len(metadata["cells"]), 9)
        self.assertEqual({k for c in metadata["cells"] for k in c}, {"panel", "spec"})

    def test_panel_rejects(self):
        with self.assertRaisesRegex(ValueError, "cannot be overlaid"):
            Panel([ScatterMatrix(columns())])

    def test_nests_in_grid(self):
        matrix = ScatterMatrix(columns(), hue="species", dimensions=["a", "b"])
        line = LineChart([{"x": 0, "y": 1}, {"x": 1, "y": 2}])
        figure = Grid([[line, matrix]])
        # the line, four matrix cells, two diagonal twins, and the legend
        self.assertEqual(len(figure.axes), 8)
        self.assertEqual(len([ax for ax in figure.axes if ax.get_legend()]), 1)
        outer = Grid([[figure]])
        self.assertEqual(len(outer.axes), 8)

    def test_nested_columns_keep_equal_widths(self):
        matrix = ScatterMatrix(columns(), hue="species", dimensions=["a", "b", "c"])
        line = LineChart([{"x": 0, "y": 1}, {"x": 1, "y": 2}])
        # a full row above puts outer column edges where a legend-blind
        # split of the matrix would also place one
        def spec(row, col, span=1):
            return {"row": row, "col": col, "rowspan": 1, "colspan": span}

        cells = [{"figure": line, "layout_spec": spec(0, c)} for c in range(3)]
        cells += [
            {"figure": line, "layout_spec": spec(1, 0)},
            {"figure": matrix, "layout_spec": spec(1, 1, 2)},
        ]
        figure = Grid(cells, figsize=(12, 8))
        figure.canvas.draw()
        bottom = [
            ax
            for ax in figure.axes
            if ax.get_xlabel() in ("a", "b", "c")
        ]
        widths = [ax.get_position().width for ax in bottom]
        self.assertEqual(len(widths), 3)
        self.assertAlmostEqual(min(widths) / max(widths), 1, delta=0.05)

    def test_renders_under_every_theme(self):
        for theme in THEMES:
            with self.subTest(theme=theme):
                config.set_theme(theme)
                figure = ScatterMatrix(
                    columns(),
                    hue="species",
                    diagonal=DIAGONAL.KDE,
                    show_correlation=True,
                    show_regression=True,
                )
                figure.canvas.draw()
                plt.close(figure)


if __name__ == "__main__":
    unittest.main()
