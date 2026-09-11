"""Tests for category sort and emphasis rules on the bar-type fronts (ADR 0042)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from datachart.charts import BarChart, PyramidChart, RadialChart
from datachart.config import config
from datachart.constants import EMPHASIS, RADIAL_TYPE, SORT
from datachart.utils._internal.layers import emphasis_rule_roles
from datachart.utils._internal.validate import validate_emphasis_rule, validate_sort

BAR1 = [{"label": c, "y": v} for c, v in zip("ABCD", [3.0, 5.0, 4.0, 1.0])]
BAR2 = [{"label": c, "y": v} for c, v in zip("ABCD", [2.0, 1.0, 6.0, 1.0])]
TOTALS = {"A": 5.0, "B": 6.0, "C": 10.0, "D": 2.0}


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def tick_labels(ax, axis="x"):
    labels = ax.get_xticklabels() if axis == "x" else ax.get_yticklabels()
    return [t.get_text() for t in labels]


def heights(container):
    return [patch.get_height() for patch in container]


def muted(container):
    return [patch.get_alpha() == config["muted_alpha"] for patch in container]


class TestSortConstant:
    def test_values(self):
        assert SORT.DEFAULT is None
        assert SORT.NONE is None
        assert SORT.ASCENDING == "ascending"
        assert SORT.DESCENDING == "descending"

    def test_validate_sort(self):
        assert validate_sort(None) is None
        assert validate_sort(SORT.ASCENDING) == "ascending"
        with pytest.raises(ValueError, match="sort"):
            validate_sort("up")


class TestValidateEmphasisRule:
    def test_none_passes_through(self):
        assert validate_emphasis_rule(None) is None

    @pytest.mark.parametrize(
        "rule",
        [{"above": 1}, {"below": 2.5}, {"between": (1, 3)}, {"top": 2}, {"bottom": 1}],
    )
    def test_valid_shapes(self, rule):
        key, value = next(iter(rule.items()))
        assert validate_emphasis_rule(rule) == (key, value)

    def test_not_a_dict(self):
        with pytest.raises(ValueError, match="one-key dict"):
            validate_emphasis_rule("top")

    def test_unknown_key(self):
        with pytest.raises(ValueError, match="`over`"):
            validate_emphasis_rule({"over": 3})

    def test_two_keys(self):
        with pytest.raises(ValueError, match="one key"):
            validate_emphasis_rule({"top": 3, "above": 1})

    def test_empty(self):
        with pytest.raises(ValueError, match="one key"):
            validate_emphasis_rule({})

    @pytest.mark.parametrize("n", [0, -1, 2.5, True, "3"])
    def test_count_must_be_positive_integer(self, n):
        with pytest.raises(ValueError, match="positive integer"):
            validate_emphasis_rule({"top": n})

    def test_threshold_must_be_number(self):
        with pytest.raises(ValueError, match="number"):
            validate_emphasis_rule({"above": "1"})

    def test_between_reversed(self):
        with pytest.raises(ValueError, match="reversed|lo"):
            validate_emphasis_rule({"between": (3, 1)})

    def test_between_needs_two_bounds(self):
        with pytest.raises(ValueError, match="between"):
            validate_emphasis_rule({"between": (1,)})


class TestRuleRoles:
    VALUES = [3.0, 5.0, 4.0, 1.0, 5.0]

    def roles(self, rule):
        return emphasis_rule_roles(validate_emphasis_rule(rule), self.VALUES)

    def test_above_is_strict(self):
        assert self.roles({"above": 4.0}) == [
            "background",
            "highlight",
            "background",
            "background",
            "highlight",
        ]

    def test_below_is_strict(self):
        assert self.roles({"below": 3.0}) == [
            "background",
            "background",
            "background",
            "highlight",
            "background",
        ]

    def test_between_is_inclusive(self):
        assert self.roles({"between": (3.0, 4.0)}) == [
            "highlight",
            "background",
            "highlight",
            "background",
            "background",
        ]

    def test_top_breaks_ties_by_input_order(self):
        # the two 5.0s tie for first; top 2 takes both, top 1 the earlier
        assert self.roles({"top": 2}) == [
            "background",
            "highlight",
            "background",
            "background",
            "highlight",
        ]
        assert self.roles({"top": 1}) == [
            "background",
            "highlight",
            "background",
            "background",
            "background",
        ]

    def test_bottom(self):
        assert self.roles({"bottom": 2}) == [
            "highlight",
            "background",
            "background",
            "highlight",
            "background",
        ]

    def test_count_clamps_to_record_count(self):
        assert self.roles({"top": 10}) == ["highlight"] * 5


class TestSortBars:
    def test_default_is_input_order(self):
        ax = BarChart(data=BAR1).axes[0]
        assert tick_labels(ax) == list("ABCD")
        assert heights(ax.containers[0]) == [3.0, 5.0, 4.0, 1.0]

    def test_ascending_single(self):
        ax = BarChart(data=BAR1, sort=SORT.ASCENDING).axes[0]
        assert tick_labels(ax) == list("DACB")
        assert heights(ax.containers[0]) == [1.0, 3.0, 4.0, 5.0]

    def test_descending_grouped_sorts_by_total(self):
        ax = BarChart(data=[BAR1, BAR2], sort=SORT.DESCENDING).axes[0]
        assert tick_labels(ax) == list("CBAD")
        assert heights(ax.containers[0]) == [4.0, 5.0, 3.0, 1.0]
        assert heights(ax.containers[1]) == [6.0, 1.0, 2.0, 1.0]

    def test_sort_by_one_series(self):
        ax = BarChart(
            data=[BAR1, BAR2],
            subtitle=["s1", "s2"],
            sort=SORT.DESCENDING,
            sort_by="s2",
        ).axes[0]
        assert tick_labels(ax) == list("CABD")

    def test_ties_keep_input_order(self):
        data = [{"label": c, "y": v} for c, v in zip("ABC", [2.0, 1.0, 2.0])]
        ax = BarChart(data=data, sort=SORT.DESCENDING).axes[0]
        assert tick_labels(ax) == list("ACB")

    def test_missing_category_sorts_last_in_input_order(self):
        partial = [{"label": c, "y": v} for c, v in zip("BC", [9.0, 1.0])]
        ax = BarChart(
            data=[BAR1, partial],
            subtitle=["s1", "s2"],
            sort=SORT.ASCENDING,
            sort_by="s2",
        ).axes[0]
        assert tick_labels(ax) == list("CBAD")

    def test_sort_by_unknown_series_raises(self):
        with pytest.raises(ValueError, match="sort_by"):
            BarChart(
                data=[BAR1, BAR2], subtitle=["s1", "s2"], sort="ascending", sort_by="s9"
            )

    def test_sort_by_without_sort_raises(self):
        with pytest.raises(ValueError, match="sort_by"):
            BarChart(data=[BAR1, BAR2], subtitle=["s1", "s2"], sort_by="s1")

    def test_invalid_sort_raises(self):
        with pytest.raises(ValueError, match="sort"):
            BarChart(data=BAR1, sort="up")

    def test_horizontal_sort_reorders_y_ticks(self):
        ax = BarChart(data=BAR1, sort=SORT.DESCENDING, orientation="horizontal").axes[0]
        assert tick_labels(ax, "y") == list("BCAD")

    def test_stacked_sort_by_total(self):
        ax = BarChart(data=[BAR1, BAR2], sort=SORT.ASCENDING, bar_mode="stack").axes[0]
        assert tick_labels(ax) == list("DABC")

    def test_input_data_is_not_mutated(self):
        data = [dict(record) for record in BAR1]
        BarChart(data=data, sort=SORT.ASCENDING, emphasis_rule={"top": 1})
        assert data == BAR1


class TestSortPyramidAndRadial:
    def test_pyramid_sorts_by_magnitude_total(self):
        left = [{"label": c, "y": v} for c, v in zip("ABC", [5.0, 1.0, 2.0])]
        right = [{"label": c, "y": v} for c, v in zip("ABC", [1.0, 1.0, 9.0])]
        ax = PyramidChart(data=[left, right], sort=SORT.DESCENDING).axes[0]
        assert tick_labels(ax, "y") == list("CAB")

    def test_radial_bar_sorts(self):
        wind = [{"label": d, "y": v} for d, v in zip(["N", "E", "S"], [2, 3, 1])]
        ax = RadialChart(data=wind, type=RADIAL_TYPE.BAR, sort=SORT.ASCENDING).axes[0]
        assert tick_labels(ax) == ["S", "N", "E"]

    def test_radial_line_rejects_sort(self):
        wind = [{"label": d, "y": v} for d, v in zip(["N", "E", "S"], [2, 3, 1])]
        with pytest.raises(ValueError, match="bar visual"):
            RadialChart(data=wind, sort=SORT.ASCENDING)
        with pytest.raises(ValueError, match="bar visual"):
            RadialChart(data=wind, emphasis_rule={"top": 1})


class TestEmphasisRuleBars:
    def test_top_mutes_the_rest(self):
        ax = BarChart(data=BAR1, emphasis_rule={"top": 2}).axes[0]
        assert muted(ax.containers[0]) == [True, False, False, True]

    def test_muted_bar_wears_muted_color(self):
        ax = BarChart(data=BAR1, emphasis_rule={"top": 1}).axes[0]
        bg, top = ax.containers[0].patches[0], ax.containers[0].patches[1]
        assert bg.get_facecolor() == matplotlib.colors.to_rgba(
            config["muted_color"], config["muted_alpha"]
        )
        assert top.get_facecolor() != bg.get_facecolor()
        assert top.get_zorder() > bg.get_zorder()

    def test_explicit_record_emphasis_wins(self):
        data = [dict(record) for record in BAR1]
        data[3]["emphasis"] = EMPHASIS.HIGHLIGHT
        ax = BarChart(data=data, emphasis_rule={"top": 1}).axes[0]
        assert muted(ax.containers[0]) == [True, False, True, False]

    def test_record_emphasis_without_rule(self):
        data = [dict(record) for record in BAR1]
        data[0]["emphasis"] = "background"
        ax = BarChart(data=data).axes[0]
        assert muted(ax.containers[0]) == [True, False, False, False]

    def test_bad_record_emphasis_raises(self):
        data = [dict(record) for record in BAR1]
        data[0]["emphasis"] = "bold"
        with pytest.raises(ValueError, match="emphasis"):
            BarChart(data=data)

    def test_chart_role_wins_over_record_roles(self):
        fig = BarChart(
            data=[BAR1, BAR2], emphasis=["background", None], emphasis_rule={"top": 1}
        )
        first, second = fig.axes[0].containers
        assert all(muted(first))
        assert muted(second) == [True, True, False, True]

    def test_single_series_keeps_legend_entry(self):
        fig = BarChart(
            data=BAR1, subtitle="s1", emphasis_rule={"top": 1}, show_legend=True
        )
        legend = fig.axes[0].get_legend()
        assert [t.get_text() for t in legend.get_texts()] == ["s1"]

    def test_only_muted_bars_lose_value_labels(self):
        ax = BarChart(data=BAR1, emphasis_rule={"top": 2}, show_values=True).axes[0]
        texts = [t.get_text() for t in ax.texts]
        assert texts == ["", "5", "4", ""]

    def test_sort_and_rule_are_independent(self):
        ax = BarChart(data=BAR1, sort=SORT.ASCENDING, emphasis_rule={"top": 1}).axes[0]
        assert tick_labels(ax) == list("DACB")
        assert muted(ax.containers[0]) == [True, True, True, False]

    def test_rule_reads_own_value_under_stack(self):
        ax = BarChart(
            data=[BAR1, BAR2], bar_mode="stack", emphasis_rule={"above": 4.5}
        ).axes[0]
        first, second = ax.containers
        assert muted(first) == [True, False, True, True]
        assert muted(second) == [True, True, False, True]

    def test_invalid_rule_raises_at_the_front(self):
        with pytest.raises(ValueError, match="emphasis_rule"):
            BarChart(data=BAR1, emphasis_rule={"top": 0})


class TestEmphasisRulePyramidAndRadial:
    def test_pyramid_rule_reads_magnitudes(self):
        left = [{"label": c, "y": v} for c, v in zip("ABC", [5.0, 1.0, 2.0])]
        right = [{"label": c, "y": v} for c, v in zip("ABC", [1.0, 1.0, 9.0])]
        ax = PyramidChart(data=[left, right], emphasis_rule={"above": 4.0}).axes[0]
        left_bars, right_bars = ax.containers
        assert muted(left_bars) == [False, True, True]
        assert muted(right_bars) == [True, True, False]

    def test_radial_bar_rule(self):
        wind = [{"label": d, "y": v} for d, v in zip(["N", "E", "S"], [2, 3, 1])]
        ax = RadialChart(
            data=wind, type=RADIAL_TYPE.BAR, emphasis_rule={"bottom": 1}
        ).axes[0]
        assert muted(ax.containers[0]) == [True, True, False]
