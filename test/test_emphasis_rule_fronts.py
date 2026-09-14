"""Tests for emphasis rules on every front that carries emphasis (ADR 0045)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from datachart.charts import (
    BoxPlot,
    RaincloudPlot,
    SwarmPlot,
    ViolinPlot,
    ContourChart,
    Histogram,
    LineChart,
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
