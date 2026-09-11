"""Tests for Panel axis scales (ADR 0041)."""

import warnings

import pytest
import matplotlib.pyplot as plt

from datachart.charts import LineChart, BarChart, BoxPlot, RadialChart
from datachart.config import config
from datachart.constants import ORIENTATION, SCALE
from datachart.utils import Panel, Grid, Annotate

BARS = [{"label": c, "y": v} for c, v in zip("ABCD", [10, 20, 30, 20])]
LINE = [{"x": i, "y": v} for i, v in enumerate([1, 10, 100, 1000], 1)]
LINE2 = [{"x": i, "y": v} for i, v in enumerate([2, 20, 200, 2000], 1)]
LINE_SMALL = [{"x": i, "y": v} for i, v in enumerate([1, 2, 3, 2], 1)]
BOX = [{"label": c, "y": [1, 10, 100, 1000]} for c in "AB"]
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
        (ax,) = render(Panel([LineChart(data=LINE)], scaley=SCALE.LOG))
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
                    {"figure": LineChart(data=LINE), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "left"},
                ]
            )
        assert len(record) == 1
        assert "'linear'" in str(record[0].message)
        # the first figure was built linear, so linear wins
        assert scales(render(fig)[0]) == ("linear", "linear")

    def test_conflict_on_the_secondary_axis_warns_too(self):
        with pytest.warns(UserWarning, match=r"scaley_right") as record:
            fig = Panel(
                [
                    {"figure": BarChart(data=BARS), "y_axis": "left"},
                    {"figure": LineChart(data=LINE, scaley="log"), "y_axis": "right"},
                    {"figure": LineChart(data=LINE2), "y_axis": "right"},
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
                    {"figure": LineChart(data=LINE, scalex="log"), "y_axis": "left"},
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
