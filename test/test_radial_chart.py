"""Tests for the RadialChart front and the projection-aware polar panel."""

import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

from datachart.charts import RadialChart
from datachart.constants import DIRECTION, RADIAL_TYPE

WIND = [
    {"label": d, "y": v}
    for d, v in zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"], range(1, 9))
]
WIND2 = [
    {"label": d, "y": v}
    for d, v in zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"], range(8, 0, -1))
]
ANGLES = [{"x": float(v)} for v in [10, 20, 100, 110, 200, 280, 350, 355]]


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


class TestFrontValidation:
    def test_scalex_raises(self):
        with pytest.raises(ValueError, match="scalex"):
            RadialChart(data=WIND, scalex="log")

    def test_vlines_raises(self):
        with pytest.raises(ValueError, match="vlines"):
            RadialChart(data=WIND, vlines={"x": 1})

    def test_hlines_raises(self):
        with pytest.raises(ValueError, match="hlines"):
            RadialChart(data=WIND, hlines={"y": 1})

    def test_unknown_type_raises(self):
        with pytest.raises(ValueError, match="type"):
            RadialChart(data=WIND, type="pie")

    def test_bad_direction_raises(self):
        with pytest.raises(ValueError, match="direction"):
            RadialChart(data=WIND, direction="widdershins")

    def test_innerradius_out_of_range_raises(self):
        with pytest.raises(ValueError, match="innerradius"):
            RadialChart(data=WIND, innerradius=1.0)

    def test_bad_startangle_string_raises(self):
        with pytest.raises(ValueError, match="startangle"):
            RadialChart(data=WIND, startangle="north")


class TestPolarAxes:
    def test_axes_are_polar(self):
        fig = RadialChart(data=WIND)
        assert fig.axes[0].name == "polar"

    def test_metadata_transport(self):
        fig = RadialChart(data=WIND)
        assert fig._chart_metadata["type"] == "radialchart"
        assert fig._chart_metadata["panel"].projection == "polar"

    def test_default_compass_furniture(self):
        ax = RadialChart(data=WIND).axes[0]
        assert ax.get_theta_offset() == pytest.approx(np.pi / 2)
        assert ax.get_theta_direction() == -1

    def test_startangle_compass_string(self):
        ax = RadialChart(data=WIND, startangle="E").axes[0]
        assert ax.get_theta_offset() == pytest.approx(0.0)

    def test_startangle_numeric_bearing(self):
        # a numeric startangle is a compass bearing: degrees clockwise from north
        ax = RadialChart(data=WIND, startangle=90).axes[0]
        assert ax.get_theta_offset() == pytest.approx(0.0)

    def test_counterclockwise_direction(self):
        ax = RadialChart(data=WIND, direction=DIRECTION.COUNTERCLOCKWISE).axes[0]
        assert ax.get_theta_direction() == 1

    def test_innerradius_moves_rorigin(self):
        ax = RadialChart(data=WIND, innerradius=0.3).axes[0]
        rmin, rmax = ax.get_ylim()
        expected = rmin - 0.3 / 0.7 * (rmax - rmin)
        assert ax.get_rorigin() == pytest.approx(expected)

    def test_scaley_log(self):
        ax = RadialChart(data=WIND, scaley="log").axes[0]
        assert ax.get_yscale() == "log"

    def test_ylim_setting(self):
        ax = RadialChart(data=WIND, ymin=0, ymax=20).axes[0]
        assert ax.get_ylim() == (0, 20)

    def test_subplots(self):
        fig = RadialChart(data=[WIND, WIND2], subplots=True, max_cols=2)
        polar_axes = [ax for ax in fig.axes if ax.name == "polar"]
        assert len(polar_axes) == 2


class TestAngularPlacement:
    def test_even_label_spacing(self):
        ax = RadialChart(data=WIND).axes[0]
        expected = np.linspace(0, 2 * np.pi, len(WIND), endpoint=False)
        assert np.allclose(ax.get_xticks(), expected)
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == [d["label"] for d in WIND]

    def test_line_closes_loop(self):
        ax = RadialChart(data=WIND).axes[0]
        (line,) = ax.lines
        theta, r = line.get_xdata(), line.get_ydata()
        assert len(theta) == len(WIND) + 1
        assert theta[-1] == pytest.approx(theta[0] + 2 * np.pi)
        assert r[-1] == r[0]

    def test_bar_sector_positions(self):
        ax = RadialChart(data=WIND, type=RADIAL_TYPE.BAR).axes[0]
        n = len(WIND)
        patches = ax.patches
        assert len(patches) == n
        centers = [p.get_x() + p.get_width() / 2 for p in patches]
        assert np.allclose(
            sorted(centers), np.linspace(0, 2 * np.pi, n, endpoint=False)
        )
        # each bar spans its plot_bar_width fraction of the sector
        assert all(p.get_width() < 2 * np.pi / n for p in patches)

    def test_stacked_bars(self):
        fig = RadialChart(data=[WIND, WIND2], type=RADIAL_TYPE.BAR, bar_mode="stack")
        patches = fig.axes[0].patches
        n = len(WIND)
        first, second = patches[:n], patches[n:]
        bottoms = sorted(p.get_y() for p in second)
        heights = sorted(p.get_height() for p in first)
        assert bottoms == heights

    def test_scatter_points_on_sectors(self):
        ax = RadialChart(data=WIND, type=RADIAL_TYPE.SCATTER).axes[0]
        offsets = ax.collections[0].get_offsets()
        assert np.allclose(
            sorted(offsets[:, 0]), np.linspace(0, 2 * np.pi, len(WIND), endpoint=False)
        )

    def test_histogram_bins_degrees_over_full_circle(self):
        ax = RadialChart(data=ANGLES, type=RADIAL_TYPE.HISTOGRAM, num_bins=4).axes[0]
        patches = ax.patches
        assert len(patches) == 4
        assert sum(p.get_width() for p in patches) == pytest.approx(2 * np.pi)
        # observations fall in their degree quadrants: [10,20]-> q1, [100,110]-> q2, ...
        counts = [p.get_height() for p in sorted(patches, key=lambda p: p.get_x())]
        assert counts == [2, 2, 1, 3]


class TestValueLabelEmphasis:
    def test_marks_sit_above_the_grid(self):
        ax = RadialChart(data=WIND, type=RADIAL_TYPE.BAR, show_grid="both").axes[0]
        assert ax.get_axisbelow() is True
        # the grid draws at the axis artists' zorder; every mark must beat it
        axis_z = max(ax.xaxis.get_zorder(), ax.yaxis.get_zorder())
        assert all(p.get_zorder() > axis_z for p in ax.patches)

    def test_value_labels_redrawn_on_top_in_black(self):
        ax = RadialChart(data=WIND, type=RADIAL_TYPE.BAR).axes[0]
        assert all(t.get_text() == "" for t in ax.get_yticklabels())
        elevated = [t for t in ax.texts if t.get_color() == "#000000"]
        assert elevated
        # above the marks AND the border circle, so nothing strikes through
        top_z = max(
            max(p.get_zorder() for p in ax.patches),
            ax.spines["polar"].get_zorder(),
        )
        assert all(t.get_zorder() > top_z for t in elevated)

    def test_legend_sits_above_the_border(self):
        fig = RadialChart(data=[WIND, WIND2], subtitle=["a", "b"], show_legend=True)
        ax = fig.axes[0]
        legend = ax.get_legend()
        assert legend.get_zorder() > ax.spines["polar"].get_zorder()

    def test_axis_labels_attach_to_the_axes(self):
        ax = RadialChart(data=WIND, ylabel="Wind speed (km/h)").axes[0]
        assert ax.get_ylabel() == "Wind speed (km/h)"
        assert ax.figure.get_supylabel() == ""

    def test_subplot_columns_anchor_toward_each_other(self):
        fig = RadialChart(data=[WIND, WIND2], subplots=True, max_cols=2)
        left, right = fig.axes[:2]
        assert left.get_anchor() == "E"
        assert right.get_anchor() == "W"


class TestTipTexts:
    def test_tip_labels_replace_the_ring_labels(self):
        ax = RadialChart(data=WIND, type=RADIAL_TYPE.BAR, show_tip_labels=True).axes[0]
        assert all(t.get_text() == "" for t in ax.get_xticklabels())
        tip_texts = {t.get_text() for t in ax.texts}
        assert {d["label"] for d in WIND} <= tip_texts

    def test_tip_labels_sit_beyond_the_marks(self):
        ax = RadialChart(data=WIND, type=RADIAL_TYPE.BAR, show_tip_labels=True).axes[0]
        tops = {
            round(p.get_x() + p.get_width() / 2, 6): p.get_y() + p.get_height()
            for p in ax.patches
        }
        labels = {d["label"] for d in WIND}
        for t in ax.texts:
            if t.get_text() in labels:
                theta, r = t.get_position()
                assert r > tops[round(theta, 6)]

    def test_tip_labels_flip_on_the_left_half(self):
        ax = RadialChart(data=WIND, type=RADIAL_TYPE.BAR, show_tip_labels=True).axes[0]
        by_text = {t.get_text(): t for t in ax.texts}
        # N points up (screen 90°) and W sits on the left half (screen 180°)
        assert by_text["N"].get_ha() == "left"
        assert by_text["W"].get_ha() == "right"
        assert by_text["W"].get_rotation() != by_text["N"].get_rotation()

    def test_show_values_writes_each_value(self):
        ax = RadialChart(
            data=WIND, type=RADIAL_TYPE.BAR, show_values=True, value_format="{x:.1f}"
        ).axes[0]
        expected = {f"{d['y']:.1f}" for d in WIND}
        value_texts = [t for t in ax.texts if t.get_text() in expected]
        assert {t.get_text() for t in value_texts} == expected
        # the halo backs every tip text, like the axis value labels
        assert all(t.get_bbox_patch() is not None for t in value_texts)

    def test_tip_labels_carry_a_halo(self):
        ax = RadialChart(data=WIND, type=RADIAL_TYPE.BAR, show_tip_labels=True).axes[0]
        labels = {d["label"] for d in WIND}
        tip_texts = [t for t in ax.texts if t.get_text() in labels]
        assert tip_texts
        assert all(t.get_bbox_patch() is not None for t in tip_texts)

    def test_show_values_on_line_points(self):
        ax = RadialChart(data=WIND, show_values=True).axes[0]
        texts = {t.get_text() for t in ax.texts}
        assert {f"{d['y']:g}" for d in WIND} <= texts

    def test_stacked_values_per_segment(self):
        fig = RadialChart(
            data=[WIND, WIND2], type=RADIAL_TYPE.BAR, bar_mode="stack", show_values=True
        )
        texts = [t.get_text() for t in fig.axes[0].texts]
        for d in WIND:
            assert f"{d['y']:g}" in texts


class TestBorder:
    def test_border_shown_by_default(self):
        ax = RadialChart(data=WIND).axes[0]
        assert ax.spines["polar"].get_visible()

    def test_border_hidden_on_request(self):
        ax = RadialChart(data=WIND, show_border=False).axes[0]
        assert all(not spine.get_visible() for spine in ax.spines.values())


class TestRendering:
    def test_all_types_render(self):
        for radial_type, data in [
            (RADIAL_TYPE.LINE, WIND),
            (RADIAL_TYPE.BAR, WIND),
            (RADIAL_TYPE.SCATTER, WIND),
            (RADIAL_TYPE.HISTOGRAM, ANGLES),
        ]:
            fig = RadialChart(data=data, type=radial_type, title="t")
            fig.canvas.draw()
            plt.close(fig)

    def test_line_area_renders(self):
        fig = RadialChart(data=WIND, show_area=True)
        fig.canvas.draw()

    def test_legend_labels(self):
        fig = RadialChart(data=[WIND, WIND2], subtitle=["a", "b"], show_legend=True)
        legend = fig.axes[0].get_legend()
        assert [t.get_text() for t in legend.get_texts()] == ["a", "b"]
