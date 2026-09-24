"""Tests for Panel axis scales (ADR 0041)."""

import warnings
from datetime import datetime

import numpy as np
import pytest
import matplotlib.pyplot as plt

from datachart.charts import (
    BarChart,
    BoxPlot,
    ContourChart,
    HexbinChart,
    Histogram,
    LineChart,
    RadialChart,
    RaincloudPlot,
    ScatterChart,
    StackedAreaChart,
    SwarmPlot,
    ViolinPlot,
)
from datachart.config import config
from datachart.constants import ORIENTATION, AXIS_SCALE
from datachart.utils import Panel, Grid, Annotate
from datachart.utils._internal.validate import validate_log_values

BARS = [{"label": c, "y": v} for c, v in zip("ABCD", [10, 20, 30, 20])]
LINE = [{"x": i, "y": v} for i, v in enumerate([1, 10, 100, 1000], 1)]
LINE2 = [{"x": i, "y": v} for i, v in enumerate([2, 20, 200, 2000], 1)]
LINE_SMALL = [{"x": i, "y": v} for i, v in enumerate([1, 2, 3, 2], 1)]
BOX = [{"label": c, "value": v} for c in "AB" for v in (1, 10, 100, 1000)]
WIND = [
    {"label": d, "y": v}
    for d, v in zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"], range(8, 0, -1))
]


def hbar(**kwargs):
    return BarChart(data=BARS, orientation=ORIENTATION.HORIZONTAL, **kwargs)


def render(fig):
    fig.canvas.draw()
    return fig.axes


def scales(ax):
    return ax.get_xscale(), ax.get_yscale()


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")
    config.reset_config()


class TestExplicitScales:
    def test_scaley_is_the_primary_value_axis(self):
        (ax,) = render(Panel([LineChart(data=LINE)], scaley=AXIS_SCALE.LOG))
        assert scales(ax) == ("linear", "log")

    def test_scalex_is_the_category_axis(self):
        (ax,) = render(Panel([LineChart(data=LINE)], scalex="log"))
        assert scales(ax) == ("log", "linear")

    def test_scaley_right_scales_only_the_secondary_axis(self):
        fig = Panel(
            [
                {"figure": BarChart(data=BARS), "y_axis": "left"},
                {"figure": LineChart(data=LINE), "y_axis": "right"},
            ],
            scaley_right="log",
        )
        ax, ax_right = render(fig)
        assert scales(ax) == ("linear", "linear")
        assert scales(ax_right) == ("linear", "log")

    def test_horizontal_panel_maps_by_role(self):
        fig = Panel(
            [
                {"figure": hbar(), "y_axis": "left"},
                {"figure": LineChart(data=LINE), "y_axis": "right"},
            ],
            scalex="symlog",
            scaley="log",
            scaley_right="asinh",
        )
        ax, ax_top = render(fig)
        assert scales(ax) == ("log", "symlog")
        assert scales(ax_top) == ("asinh", "symlog")

    def test_horizontal_box_plot_swaps_once(self):
        box = BoxPlot(data=BOX, orientation=ORIENTATION.HORIZONTAL)
        (ax,) = render(Panel([box], scaley="log"))
        assert scales(ax) == ("log", "linear")

    def test_horizontal_box_plot_keeps_its_own_log(self):
        box = BoxPlot(data=BOX, orientation=ORIENTATION.HORIZONTAL, scaley="log")
        (ax,) = render(Panel([box]))
        assert scales(ax) == ("log", "linear")


class TestStampedScales:
    def test_source_figure_scale_is_kept(self):
        (ax,) = render(Panel([LineChart(data=LINE, scaley="log")]))
        assert scales(ax) == ("linear", "log")

    def test_source_category_scale_is_kept(self):
        (ax,) = render(Panel([LineChart(data=LINE, scalex="log")]))
        assert scales(ax) == ("log", "linear")

    def test_explicit_overrides_stamped(self):
        fig = Panel([LineChart(data=LINE, scaley="log")], scaley="linear")
        (ax,) = render(fig)
        assert scales(ax) == ("linear", "linear")

    def test_explicit_scaley_leaves_the_secondary_inheriting(self):
        fig = Panel(
            [
                {"figure": BarChart(data=BARS), "y_axis": "left"},
                {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "right"},
            ],
            scaley="symlog",
        )
        ax, ax_right = render(fig)
        assert scales(ax) == ("linear", "symlog")
        assert scales(ax_right) == ("linear", "log")

    def test_log_group_auto_assigned_right_keeps_its_scale(self):
        big = [{"x": i, "y": v} for i, v in enumerate([10, 100, 1000, 10000])]
        fig = Panel([BarChart(data=BARS), LineChart(data=big, scaley="log")])
        ax, ax_right = render(fig)
        assert len(ax_right.get_lines()) == 1
        assert scales(ax) == ("linear", "linear")
        assert scales(ax_right) == ("linear", "log")

    def test_first_group_on_the_axis_wins(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fig = Panel(
                [
                    {"figure": LineChart(data=LINE, scaley="symlog"), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "left"},
                ]
            )
        (ax,) = render(fig)
        assert scales(ax) == ("linear", "symlog")

    def test_stamp_follows_the_group_into_a_horizontal_panel(self):
        fig = Panel([hbar(), LineChart(data=LINE_SMALL, scaley="log")])
        ax, ax_top = render(fig)
        assert scales(ax) == ("linear", "linear")
        assert scales(ax_top) == ("log", "linear")

    def test_horizontal_bar_scale_is_kept(self):
        (ax,) = render(Panel([hbar(scalex="log")]))
        assert scales(ax) == ("log", "linear")

    def test_stamp_survives_nesting(self):
        inner = Panel(
            [
                LineChart(data=LINE, scaley="log"),
                {"figure": LineChart(data=LINE2), "y_axis": "right"},
            ]
        )
        outer = Panel(
            [inner, {"figure": LineChart(data=LINE_SMALL), "y_axis": "right"}]
        )
        groups = outer._chart_metadata["panel"].groups
        assert [g.value_scale for g in groups] == ["log", None, None]
        ax, ax_right = render(outer)
        assert scales(ax) == ("linear", "log")
        assert scales(ax_right) == ("linear", "linear")

    def test_inner_explicit_scale_survives_nesting(self):
        inner = Panel([LineChart(data=LINE), LineChart(data=LINE2)], scaley="log")
        outer = Panel(
            [inner, {"figure": LineChart(data=LINE_SMALL), "y_axis": "right"}]
        )
        groups = outer._chart_metadata["panel"].groups
        assert [g.value_scale for g in groups] == ["log", "log", None]
        ax, ax_right = render(outer)
        assert scales(ax) == ("linear", "log")
        assert scales(ax_right) == ("linear", "linear")

    def test_inner_scaley_right_reaches_its_right_groups(self):
        inner = Panel(
            [
                {"figure": BarChart(data=BARS), "y_axis": "left"},
                {"figure": LineChart(data=LINE), "y_axis": "right"},
            ],
            scaley_right="log",
        )
        outer = Panel([inner, {"figure": LineChart(data=LINE_SMALL), "y_axis": "left"}])
        groups = outer._chart_metadata["panel"].groups
        assert [g.value_scale for g in groups] == [None, "log", None]
        ax, ax_right = render(outer)
        assert scales(ax) == ("linear", "linear")
        assert scales(ax_right) == ("linear", "log")

    def test_unset_first_adopts_the_log_behind_it(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            fig = Panel(
                [
                    {"figure": LineChart(data=LINE), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "left"},
                ]
            )
        assert scales(render(fig)[0]) == ("linear", "log")

    def test_log_first_keeps_its_scale_over_an_unset_figure(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            fig = Panel(
                [
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "left"},
                    {"figure": LineChart(data=LINE2), "y_axis": "left"},
                ]
            )
        assert scales(render(fig)[0]) == ("linear", "log")

    def test_unset_first_on_the_secondary_axis_adopts_too(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            fig = Panel(
                [
                    {"figure": BarChart(data=BARS), "y_axis": "left"},
                    {"figure": LineChart(data=LINE2), "y_axis": "right"},
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "right"},
                ]
            )
        ax, ax_right = render(fig)
        assert scales(ax) == ("linear", "linear")
        assert scales(ax_right) == ("linear", "log")

    def test_unset_category_scale_adopts_too(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            fig = Panel(
                [
                    {"figure": LineChart(data=LINE), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scalex="log"), "y_axis": "left"},
                ]
            )
        assert scales(render(fig)[0]) == ("log", "linear")

    def test_no_figure_sets_a_scale_leaves_the_axes_default(self):
        fig = Panel([LineChart(data=LINE), LineChart(data=LINE2)])
        assert scales(render(fig)[0]) == ("linear", "linear")

    def test_stamp_survives_grid_and_annotate(self):
        panel = Panel([LineChart(data=LINE, scaley="log")])
        annotated = Annotate(panel, texts={"text": "t", "x": 1, "y": 10})
        assert scales(render(annotated)[0]) == ("linear", "log")
        grid = Grid([panel, LineChart(data=LINE)])
        assert scales(render(grid)[0]) == ("linear", "log")


class TestWarnings:
    def test_value_axis_conflict_names_the_remedy(self):
        with pytest.warns(UserWarning, match=r"y_axis.*scaley_right") as record:
            fig = Panel(
                [
                    {"figure": LineChart(data=LINE, scaley="symlog"), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "left"},
                ]
            )
        assert len(record) == 1
        assert "'symlog'" in str(record[0].message)
        # the first figure that set a scale wins
        assert scales(render(fig)[0]) == ("linear", "symlog")

    def test_conflict_on_the_secondary_axis_warns_too(self):
        with pytest.warns(UserWarning, match=r"scaley_right") as record:
            fig = Panel(
                [
                    {"figure": BarChart(data=BARS), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "right"},
                    {
                        "figure": LineChart(data=LINE2, scaley="symlog"),
                        "y_axis": "right",
                    },
                ]
            )
        assert len(record) == 1
        ax, ax_right = render(fig)
        assert scales(ax_right) == ("linear", "log")

    def test_category_axis_conflict_names_the_winner(self):
        with pytest.warns(UserWarning, match=r"category.*'log'") as record:
            Panel(
                [
                    {"figure": LineChart(data=LINE, scalex="log"), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scalex="symlog"), "y_axis": "left"},
                ]
            )
        assert len(record) == 1
        assert "scaley_right" not in str(record[0].message)

    def test_one_panel_warns_per_axis(self):
        with pytest.warns(UserWarning) as record:
            Panel(
                [
                    {
                        "figure": LineChart(data=LINE, scalex="log", scaley="symlog"),
                        "y_axis": "left",
                    },
                    {
                        "figure": LineChart(data=LINE, scalex="symlog", scaley="log"),
                        "y_axis": "left",
                    },
                ]
            )
        assert len(record) == 2

    def test_explicit_scale_silences_the_conflict(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            Panel(
                [
                    {"figure": LineChart(data=LINE), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "left"},
                ],
                scaley="log",
            )

    def test_agreeing_scales_do_not_warn(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            Panel(
                [
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "left"},
                ]
            )

    def test_scaley_right_without_a_twin_warns(self):
        with pytest.warns(UserWarning, match="scaley_right"):
            Panel([LineChart(data=LINE)], scaley_right="log")

    def test_scaley_right_on_polar_is_inert(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            fig = Panel([RadialChart(data=WIND)], scaley_right="log")
        (ax,) = render(fig)
        assert ax.get_yscale() == "linear"

    def test_config_key_silences_the_conflict_only(self):
        config.update_config({"overlay_warn_scale_conflict": False})
        huge = [{"x": i, "y": v} for i, v in enumerate([1, 10, 1000, 100000])]
        with pytest.warns(UserWarning) as record:
            Panel(
                [
                    LineChart(data=LINE_SMALL),
                    {"figure": LineChart(data=huge, scaley="log"), "y_axis": "left"},
                ]
            )
        messages = [str(w.message) for w in record]
        assert not any("scaley_right" in m for m in messages)
        assert any("incompatible scales" in m for m in messages)

    def test_config_key_silences_the_missing_twin(self):
        config.update_config({"overlay_warn_scale_conflict": False})
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            Panel([LineChart(data=LINE)], scaley_right="log")


class TestLogValidator:
    @pytest.mark.parametrize("scale", [None, "linear", "symlog", "asinh"])
    def test_other_scales_accept_any_value(self, scale):
        validate_log_values("scaley", "value", scale, [-1, 0, 5])

    def test_log_accepts_positive_values(self):
        validate_log_values("scaley", "value", AXIS_SCALE.LOG, [0.1, 1, 1000])

    def test_nan_and_missing_are_ignored(self):
        validate_log_values("scaley", "value", AXIS_SCALE.LOG, [1, None, np.nan, 3])

    @pytest.mark.parametrize("bad", [0, -2.5])
    def test_non_positive_raises_with_parameter_scale_and_value(self, bad):
        with pytest.raises(ValueError) as error:
            validate_log_values("scalex", "category", AXIS_SCALE.LOG, [1, bad, 3])
        message = str(error.value)
        assert "`scalex` 'log'" in message
        assert f"value {bad:g} on the category axis" in message
        assert "'symlog' or 'asinh'" in message

    def test_hint_is_appended(self):
        with pytest.raises(ValueError, match=r"zero\. Move it\.$"):
            validate_log_values("scaley", "value", AXIS_SCALE.LOG, [0], hint="Move it.")


ZERO_LINE = [{"x": 1, "y": 0}, {"x": 2, "y": 100}]
ZERO_GROUPS = [{"label": c, "value": v} for c in "AB" for v in [0, 10, 100]]
POS_GROUPS = [{"label": c, "value": v} for c in "AB" for v in [1, 10, 100]]


class TestLogScaleRejectsNonPositive:
    @pytest.mark.parametrize(
        "front, kwargs",
        [
            (LineChart, {"data": ZERO_LINE}),
            (ScatterChart, {"data": ZERO_LINE}),
            (BarChart, {"data": [{"label": "A", "y": 0}, {"label": "B", "y": 3}]}),
            (BoxPlot, {"data": ZERO_GROUPS}),
            (ViolinPlot, {"data": ZERO_GROUPS}),
            (SwarmPlot, {"data": ZERO_GROUPS}),
            (RaincloudPlot, {"data": ZERO_GROUPS}),
            (RadialChart, {"data": [{"label": "A", "y": 0}, {"label": "B", "y": 3}]}),
            (HexbinChart, {"data": {"x": [1, 2, 3], "y": [0, 1, 2]}}),
            (ContourChart, {"data": {"z": [[1, 2], [3, 4]]}}),
        ],
    )
    def test_front_scaley_raises(self, front, kwargs):
        with pytest.raises(ValueError, match=r"`scaley` 'log' cannot show the value"):
            front(**kwargs, scaley="log")

    @pytest.mark.parametrize(
        "front, data",
        [
            (LineChart, [{"x": 0, "y": 1}, {"x": 2, "y": 100}]),
            (ScatterChart, [{"x": -1, "y": 1}, {"x": 2, "y": 100}]),
            (StackedAreaChart, [{"x": 0, "y": 1}, {"x": 2, "y": 100}]),
            (Histogram, [{"x": 0}, {"x": 2}, {"x": 3}]),
            (HexbinChart, {"x": [0, 2, 3], "y": [1, 1, 2]}),
            (ContourChart, {"z": [[1, 2], [3, 4]]}),
        ],
    )
    def test_front_scalex_raises(self, front, data):
        with pytest.raises(ValueError, match=r"`scalex` 'log' .* category axis"):
            front(data=data, scalex="log")

    def test_positive_data_renders(self):
        render(LineChart(data=LINE, scalex="log", scaley="log"))
        render(BoxPlot(data=POS_GROUPS, scaley="log"))

    def test_categorical_and_temporal_axes_are_not_checked(self):
        render(BarChart(data=BARS, scalex="log"))
        days = [{"x": datetime(2024, 1, d), "y": d} for d in (1, 2, 3)]
        render(LineChart(data=days, scalex="log"))

    def test_histogram_empty_bins_on_a_log_count_axis_render(self):
        data = [{"x": v} for v in [1, 1, 1, 50, 100]]
        render(Histogram(data=data, num_bins=20, scaley="log"))

    def test_violin_kde_below_zero_is_not_checked(self):
        render(ViolinPlot(data=POS_GROUPS, scaley="log"))

    def test_stacked_area_tops_are_not_checked(self):
        first = [{"x": 1, "y": 5}, {"x": 2, "y": 6}]
        second = [{"x": 1, "y": 0}, {"x": 2, "y": 3}]
        render(StackedAreaChart(data=[first, second], scaley="log"))

    def test_horizontal_group_chart_names_scaley_on_the_value_axis(self):
        with pytest.raises(ValueError) as error:
            BoxPlot(data=ZERO_GROUPS, orientation=ORIENTATION.HORIZONTAL, scaley="log")
        assert "`scaley` 'log' cannot show the value 0 on the value axis" in str(
            error.value
        )

    def test_horizontal_bar_names_the_literal_key_it_takes(self):
        bars = [{"label": "A", "y": 0}, {"label": "B", "y": 3}]
        with pytest.raises(ValueError, match=r"`scalex` .* on the value axis"):
            BarChart(data=bars, orientation=ORIENTATION.HORIZONTAL, scalex="log")

    def test_horizontal_panel_names_scaley_on_the_value_axis(self):
        bars = [{"label": "A", "y": 0}, {"label": "B", "y": 3}]
        with pytest.raises(ValueError, match=r"`scaley` .* on the value axis"):
            Panel(
                [BarChart(data=bars, orientation=ORIENTATION.HORIZONTAL)], scaley="log"
            )

    def test_horizontal_histogram_names_scaley_on_the_category_axis(self):
        with pytest.raises(ValueError, match=r"`scaley` .* category axis"):
            Histogram(
                data=[{"x": 0}, {"x": 2}],
                orientation=ORIENTATION.HORIZONTAL,
                scaley="log",
            )

    def test_nan_values_are_ignored(self):
        data = [{"x": 1, "y": float("nan")}, {"x": 2, "y": 100}, {"x": 3, "y": 10}]
        render(LineChart(data=data, scaley="log"))

    def test_panel_explicit_log_raises(self):
        with pytest.raises(ValueError, match=r"`scaley` 'log'") as error:
            Panel([LineChart(data=ZERO_LINE)], scaley="log")
        assert "y_axis" not in str(error.value)

    def test_panel_explicit_scalex_raises(self):
        line = [{"x": 0, "y": 1}, {"x": 2, "y": 100}]
        with pytest.raises(ValueError, match=r"`scalex` 'log' .* category axis"):
            Panel([LineChart(data=line)], scalex="log")

    def test_inherited_log_over_a_linear_figure_raises_with_the_hint(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with pytest.raises(ValueError) as error:
                Panel(
                    [
                        {
                            "figure": LineChart(data=LINE, scaley="log"),
                            "y_axis": "left",
                        },
                        {"figure": LineChart(data=ZERO_LINE), "y_axis": "left"},
                    ]
                )
        message = str(error.value)
        assert "`scaley` 'log' cannot show the value 0 on the value axis" in message
        assert '"y_axis": "right"' in message
        assert "scaley_right" in message

    def test_inherited_log_on_the_secondary_axis_hints_the_primary(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with pytest.raises(ValueError) as error:
                Panel(
                    [
                        {"figure": BarChart(data=BARS), "y_axis": "left"},
                        {
                            "figure": LineChart(data=LINE, scaley="log"),
                            "y_axis": "right",
                        },
                        {"figure": LineChart(data=ZERO_LINE), "y_axis": "right"},
                    ]
                )
        message = str(error.value)
        assert "`scaley_right` 'log'" in message
        assert '"y_axis": "left"' in message

    def test_scaley_right_checks_only_the_secondary_axis(self):
        zero_bars = [{"label": "A", "y": 0}, {"label": "B", "y": 3}]
        render(
            Panel(
                [
                    {"figure": BarChart(data=zero_bars), "y_axis": "left"},
                    {"figure": LineChart(data=LINE), "y_axis": "right"},
                ],
                scaley_right="log",
            )
        )
        with pytest.raises(ValueError, match=r"`scaley_right` 'log' .* secondary"):
            Panel(
                [
                    {"figure": BarChart(data=BARS), "y_axis": "left"},
                    {"figure": LineChart(data=ZERO_LINE), "y_axis": "right"},
                ],
                scaley_right="log",
            )

    def test_primary_log_ignores_the_secondary_axis(self):
        render(
            Panel(
                [
                    {"figure": LineChart(data=LINE), "y_axis": "left"},
                    {"figure": LineChart(data=ZERO_LINE), "y_axis": "right"},
                ],
                scaley="log",
            )
        )

    def test_grid_of_a_bad_figure_raises(self):
        with pytest.raises(ValueError, match=r"`scaley` 'log'"):
            Grid([LineChart(data=LINE), LineChart(data=ZERO_LINE, scaley="log")])


def test_regression_fits_in_log_space():
    """A log x axis fits y against log10(x) (issue #175)."""
    xs = np.logspace(0, 3, 20)
    data = [{"x": float(x), "y": float(2 + 3 * np.log10(x))} for x in xs]
    figure = ScatterChart(data=data, show_regression=True, scalex="log")
    (line,) = figure.axes[0].lines
    x, y = (np.asarray(v, float) for v in line.get_data())
    np.testing.assert_allclose(y, 2 + 3 * np.log10(x), atol=1e-9)
    plt.close("all")


def test_hline_spans_the_final_log_axis():
    """An hline's default span reaches both ends of a log x axis (issue #175)."""
    data = [{"x": float(x), "y": float(x)} for x in np.logspace(0, 3, 20)]
    figure = ScatterChart(data=data, scalex="log", hlines={"y": 10, "label": "h"})
    ax = figure.axes[0]
    figure.canvas.draw()
    (line,) = [c for c in ax.collections if c.get_label() == "h"]
    np.testing.assert_allclose(line.get_segments()[0][:, 0], ax.get_xlim())
    plt.close("all")
