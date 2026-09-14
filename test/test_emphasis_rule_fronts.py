"""Tests for emphasis rules on every front that carries emphasis (ADR 0045)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from datachart.charts import (
    BoxPlot,
    RaincloudPlot,
    SwarmPlot,
    Treemap,
    ViolinPlot,
    ContourChart,
    Heatmap,
    HexbinChart,
    Histogram,
    LineChart,
    NetworkChart,
    ParallelCoords,
    ScatterChart,
    StackedAreaChart,
)
from datachart.config import config

BG, HL = "background", "highlight"


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def layers(figure):
    return figure._chart_metadata["panel"].layers


def chart_roles(figure):
    return [layer.emphasis for layer in layers(figure)]


def series(*ys):
    return [[{"x": i, "y": y} for i, y in enumerate(values)] for values in ys]


# means 2, 5, 3; maxima 3, 9, 4
LINES = series([1.0, 2.0, 3.0], [1.0, 5.0, 9.0], [2.0, 3.0, 4.0])


class TestSeriesFronts:
    def test_line_defaults_to_mean(self):
        assert chart_roles(LineChart(LINES, emphasis_rule={"top": 1})) == [BG, HL, BG]

    def test_line_by_max(self):
        figure = LineChart(LINES, emphasis_rule={"above": 3.5, "by": "max"})
        assert chart_roles(figure) == [BG, HL, HL]

    def test_line_by_min(self):
        figure = LineChart(LINES, emphasis_rule={"bottom": 1, "by": "min"})
        # min 1, 1, 2: the tie breaks on input order
        assert chart_roles(figure) == [HL, BG, BG]

    def test_explicit_series_role_wins(self):
        figure = LineChart(LINES, emphasis=[HL, None, None], emphasis_rule={"top": 1})
        assert chart_roles(figure) == [HL, HL, BG]

    def test_rule_ranks_across_subplots(self):
        figure = LineChart(LINES, subplots=True, emphasis_rule={"top": 1})
        assert chart_roles(figure) == [BG, HL, BG]

    def test_muted_line_is_drawn_muted(self):
        figure = LineChart(LINES, emphasis_rule={"top": 1})
        muted = config["muted_alpha"]
        alphas = [line.get_alpha() for line in figure.axes[0].lines]
        assert [alpha == muted for alpha in alphas] == [True, False, True]

    def test_input_is_not_mutated(self):
        charts = series([1.0, 2.0])
        LineChart(charts, emphasis_rule={"top": 1})
        assert charts == series([1.0, 2.0])

    def test_scatter_summarises_y(self):
        points = [
            [{"x": 10.0, "y": 1.0}, {"x": 20.0, "y": 1.0}],
            [{"x": 0.0, "y": 5.0}, {"x": 1.0, "y": 5.0}],
        ]
        assert chart_roles(ScatterChart(points, emphasis_rule={"top": 1})) == [BG, HL]

    def test_stacked_area_reads_own_values(self):
        # stacked, the second series sits higher; its own mean is lower
        charts = series([5.0, 5.0], [1.0, 1.0])
        figure = StackedAreaChart(charts, emphasis_rule={"top": 1})
        assert chart_roles(figure) == [HL, BG]

    def test_histogram_summarises_raw_data(self):
        data = [[{"x": v} for v in [1, 2, 3]], [{"x": v} for v in [7, 8, 9]]]
        figure = Histogram(data, emphasis_rule={"below": 5})
        assert chart_roles(figure) == [HL, BG]

    def test_line_contours_read_z(self):
        grids = [
            {"x": [0, 1, 2], "y": [0, 1, 2], "z": [[0, 1, 2], [1, 2, 3], [2, 3, 4]]},
            {"x": [0, 1, 2], "y": [0, 1, 2], "z": [[5, 6, 7], [6, 7, 8], [7, 8, 9]]},
        ]
        figure = ContourChart(grids, emphasis_rule={"top": 1, "by": "sum"})
        assert chart_roles(figure) == [BG, HL]

    def test_filled_contours_reject_the_rule(self):
        grid = {"x": [0, 1], "y": [0, 1], "z": [[0, 1], [1, 2]]}
        with pytest.raises(ValueError, match="filled"):
            ContourChart(grid, filled=True, emphasis_rule={"top": 1})

    def test_unknown_by_raises_at_the_front(self):
        with pytest.raises(ValueError, match="`by`"):
            LineChart(LINES, emphasis_rule={"top": 1, "by": "mode"})


def groups(**values):
    return [
        {"label": label, "value": float(v)} for label, vs in values.items() for v in vs
    ]


# medians 2, 3, 8; means 2, 4, 6; maxima 3, 9, 9
GROUPS = groups(A=[1, 2, 3], B=[0, 3, 9], C=[0, 8, 9, 9, 4])


class TestGroupFronts:
    @pytest.mark.parametrize("front", [BoxPlot, ViolinPlot, SwarmPlot])
    def test_defaults_to_median(self, front):
        figure = front(GROUPS, emphasis_rule={"top": 1})
        assert chart_roles(figure) == [[BG, BG, HL]]

    def test_raincloud_layers_share_the_roles(self):
        figure = RaincloudPlot(GROUPS, emphasis_rule={"above": 2.5})
        assert chart_roles(figure) == [[BG, HL, HL]] * 3

    def test_by_mean(self):
        figure = BoxPlot(GROUPS, emphasis_rule={"between": (3, 5), "by": "mean"})
        assert chart_roles(figure) == [[BG, HL, BG]]

    def test_by_max_ties_keep_input_order(self):
        figure = BoxPlot(GROUPS, emphasis_rule={"top": 1, "by": "max"})
        assert chart_roles(figure) == [[BG, HL, BG]]

    def test_explicit_group_role_wins(self):
        figure = BoxPlot(GROUPS, emphasis=[HL, None, BG], emphasis_rule={"top": 1})
        assert chart_roles(figure) == [[HL, BG, BG]]

    def test_single_role_covers_every_group(self):
        figure = BoxPlot(GROUPS, emphasis=BG, emphasis_rule={"top": 1})
        assert chart_roles(figure) == [BG]

    def test_rule_ranks_across_charts(self):
        figure = BoxPlot(
            [groups(A=[1], B=[5]), groups(A=[9], B=[2])], emphasis_rule={"top": 1}
        )
        assert chart_roles(figure) == [[BG, BG], [HL, BG]]

    def test_length_mismatch_still_raises(self):
        with pytest.raises(ValueError, match="length"):
            BoxPlot(GROUPS, emphasis=[HL], emphasis_rule={"top": 1})

    def test_muted_box_is_drawn_muted(self):
        ax = BoxPlot(GROUPS, emphasis_rule={"top": 1}).axes[0]
        boxes = [p for p in ax.patches if hasattr(p, "get_path")]
        muted = config["muted_alpha"]
        assert [box.get_alpha() == muted for box in boxes] == [True, True, False]


TREE = {
    "data": [
        {"label": "a", "value": 5.0},
        {
            "label": "g",
            "children": [
                {"label": "b", "value": 9.0},
                {"label": "c", "value": 1.0},
            ],
        },
        {
            "label": "h",
            "emphasis": BG,
            "children": [{"label": "d", "value": 20.0}],
        },
    ]
}


def leaf_roles(records):
    roles = {}
    for record in records:
        if record.get("children") is None:
            roles[record["label"]] = record.get("emphasis")
        else:
            roles.update(leaf_roles(record["children"]))
    return roles


class TestRecordFronts:
    def test_treemap_reads_leaf_values(self):
        figure = Treemap(TREE, emphasis_rule={"top": 2})
        records = layers(figure)[0].records
        # d ranks first but keeps its group's explicit role
        assert leaf_roles(records) == {"a": BG, "b": HL, "c": BG, "d": None}

    def test_treemap_groups_keep_their_roles(self):
        records = layers(Treemap(TREE, emphasis_rule={"top": 2}))[0].records
        assert [r.get("emphasis") for r in records] == [BG, None, BG]

    def test_treemap_explicit_leaf_role_wins(self):
        tree = {
            "data": [
                {"label": "a", "value": 1.0, "emphasis": HL},
                {"label": "b", "value": 2.0},
            ]
        }
        records = layers(Treemap(tree, emphasis_rule={"top": 1}))[0].records
        assert leaf_roles(records) == {"a": HL, "b": HL}

    def test_treemap_rejects_by(self):
        with pytest.raises(ValueError, match="`by`"):
            Treemap(TREE, emphasis_rule={"top": 1, "by": "sum"})

    def test_treemap_input_is_not_mutated(self):
        tree = {"data": [{"label": "a", "value": 1.0}]}
        Treemap(tree, emphasis_rule={"top": 1})
        assert tree == {"data": [{"label": "a", "value": 1.0}]}

    def test_network_reads_node_size(self):
        network = {
            "nodes": [
                {"id": "a", "size": 1.0},
                {"id": "b", "size": 9.0},
                {"id": "c", "size": 4.0},
            ],
            "edges": [{"source": "a", "target": "b"}, {"source": "b", "target": "c"}],
        }
        layer = layers(NetworkChart(network, emphasis_rule={"above": 2}))[0]
        assert [node["emphasis"] for node in layer.nodes] == [BG, HL, HL]
        assert layer.muted == [True, False, False]

    def test_network_node_without_size_raises(self):
        network = {
            "nodes": [{"id": "a", "size": 1.0}, {"id": "b"}],
            "edges": [{"source": "a", "target": "b"}],
        }
        with pytest.raises(ValueError, match="size"):
            NetworkChart(network, emphasis_rule={"top": 1})

    def test_network_inferred_nodes_raise(self):
        network = {"edges": [{"source": "a", "target": "b"}]}
        with pytest.raises(ValueError, match="size"):
            NetworkChart(network, emphasis_rule={"top": 1})

    ROWS = [
        {"p": 1.0, "q": 2.0, "score": 3.0},
        {"p": 2.0, "q": 1.0, "score": 7.0},
        {"p": 3.0, "q": 3.0, "score": 5.0},
    ]

    def test_parallel_reads_hue(self):
        figure = ParallelCoords(self.ROWS, hue="score", emphasis_rule={"top": 2})
        assert layers(figure)[0].row_emphasis == [BG, HL, HL]

    def test_parallel_explicit_row_role_wins(self):
        figure = ParallelCoords(
            self.ROWS,
            hue="score",
            emphasis=[HL, None, None],
            emphasis_rule={"top": 1},
        )
        assert layers(figure)[0].row_emphasis == [HL, HL, BG]

    def test_parallel_without_hue_raises(self):
        with pytest.raises(ValueError, match="hue"):
            ParallelCoords(self.ROWS, emphasis_rule={"top": 1})

    def test_parallel_non_numeric_hue_raises(self):
        rows = [dict(row, kind="x") for row in self.ROWS]
        with pytest.raises(ValueError, match="number"):
            ParallelCoords(rows, hue="kind", emphasis_rule={"top": 1})


GRID = {"z": [[1.0, 5.0, None], [7.0, 2.0, 9.0]]}


def cell_patches(figure):
    """The (background, highlight) emphasis patches drawn over the cells."""
    patches = [p for p in figure.axes[0].patches if p.get_zorder() in (1, 2)]
    return (
        sum(p.get_zorder() == 1 for p in patches),
        sum(p.get_zorder() == 2 for p in patches),
    )


class TestCellFronts:
    def test_heatmap_rule_roles_cells(self):
        layer = layers(Heatmap(GRID, emphasis_rule={"above": 4}))[0]
        assert layer.cell_roles == [[BG, HL, None], [HL, BG, HL]]

    def test_heatmap_top_skips_blank_cells(self):
        layer = layers(Heatmap(GRID, emphasis_rule={"bottom": 5}))[0]
        assert layer.cell_roles == [[HL, HL, None], [HL, HL, HL]]

    def test_heatmap_explicit_cell_role_wins(self):
        grid = dict(GRID, emphasis=[[HL, None, None], [None, None, BG]])
        layer = layers(Heatmap(grid, emphasis_rule={"top": 1}))[0]
        assert layer.cell_roles == [[HL, BG, None], [BG, BG, BG]]

    def test_heatmap_cell_roles_without_rule(self):
        grid = dict(GRID, emphasis=[[BG, None, None], [None, HL, None]])
        assert cell_patches(Heatmap(grid)) == (1, 1)

    def test_heatmap_draws_veils_and_outlines(self):
        assert cell_patches(Heatmap(GRID, emphasis_rule={"top": 2})) == (3, 2)

    def test_heatmap_role_grid_shape_mismatch_raises(self):
        grid = dict(GRID, emphasis=[[BG, None]])
        with pytest.raises(ValueError, match="one role per cell"):
            Heatmap(grid)

    def test_heatmap_bad_cell_role_raises(self):
        grid = dict(GRID, emphasis=[[BG, None, None], [None, "bold", None]])
        with pytest.raises(ValueError, match="cell"):
            Heatmap(grid)

    def test_heatmap_rejects_by(self):
        with pytest.raises(ValueError, match="`by`"):
            Heatmap(GRID, emphasis_rule={"top": 1, "by": "max"})

    def test_heatmap_input_is_not_mutated(self):
        grid = {"z": [[1.0, 2.0]]}
        Heatmap(grid, emphasis_rule={"top": 1})
        assert grid == {"z": [[1.0, 2.0]]}

    POINTS = {
        "x": [0.0, 0.0, 0.0, 10.0, 10.0, 5.0],
        "y": [0.0, 0.0, 0.0, 10.0, 10.0, 5.0],
    }

    def test_hexbin_rule_mutes_bins(self):
        figure = HexbinChart(
            self.POINTS, gridsize=5, mincnt=1, emphasis_rule={"top": 1}
        )
        tiles, outline = figure.axes[0].collections[:2]
        assert len(tiles.get_offsets()) == 3
        assert len(outline.get_offsets()) == 1
        assert tiles.get_array() is None

    def test_hexbin_hover_keeps_bin_values(self):
        figure = HexbinChart(
            self.POINTS, gridsize=5, mincnt=1, emphasis_rule={"top": 1}
        )
        ((_, resolve),) = figure._hover_targets
        assert sorted(resolve([i])["count"] for i in range(3)) == [1.0, 2.0, 3.0]

    def test_hexbin_rejects_by(self):
        with pytest.raises(ValueError, match="`by`"):
            HexbinChart(self.POINTS, emphasis_rule={"top": 1, "by": "max"})
