"""Tests for `show(interactive=True)` and the hover seam (ADR 0031)."""

import sys
import types
import warnings

import matplotlib

# show() opens a blocking GUI window on interactive backends
matplotlib.use("Agg", force=True)

import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.container import BarContainer
from matplotlib.contour import ContourSet
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Polygon

from datachart.charts import (
    LineChart,
    BarChart,
    ScatterChart,
    Histogram,
    BoxPlot,
    PyramidChart,
    StackedAreaChart,
    SwarmPlot,
    HexbinChart,
    Heatmap,
    ContourChart,
    ViolinPlot,
    ParallelCoords,
    SankeyChart,
    Treemap,
    NetworkChart,
    RadialChart,
)
from datachart.constants import HISTOGRAM_TYPE
from datachart.utils import Panel, Grid

LINE_DATA = [
    [{"x": i, "y": i * 2} for i in range(5)],
    [{"x": i, "y": i} for i in range(5)],
]
BAR_DATA = [
    [{"label": c, "y": v} for c, v in zip("ABC", [3, 1, 4])],
    [{"label": c, "y": v} for c, v in zip("ABC", [2, 5, 6])],
]


def _line_fig(**kwargs):
    return LineChart(data=LINE_DATA, subtitle=["fast", "slow"], **kwargs)


def _bar_fig(**kwargs):
    return BarChart(data=BAR_DATA, subtitle=["north", "south"], **kwargs)


def _targets(figure):
    return figure._hover_targets


def _pixel(ax, x, y):
    """The canvas pixel position of a data point, after a draw."""
    ax.figure.canvas.draw()
    return ax.transData.transform((x, y))


def _hover(figure, ax, x, y):
    """Move the mouse over a data point and return the annotation texts."""
    px, py = _pixel(ax, x, y)
    event = MouseEvent("motion_notify_event", figure.canvas, px, py)
    figure.canvas.callbacks.process("motion_notify_event", event)
    return [sel.annotation.get_text() for sel in figure._hover_cursor.selections]


def _show_interactive(figure):
    with warnings.catch_warnings():
        # Agg is non-interactive; plt.show() warns instead of opening a window
        warnings.simplefilter("ignore")
        figure.show(interactive=True)


class TestHoverSeam:
    """Layers register (artist, resolver) pairs on the figure they draw into."""

    def test_line_registers_one_target_per_series(self):
        targets = _targets(_line_fig())
        assert [type(a) for a, _ in targets] == [Line2D, Line2D]
        artist, resolver = targets[0]
        assert artist.get_label() == "fast"
        assert resolver(2) == {"label": "fast", "x": 2, "y": 4}

    def test_scatter_registers_one_target_per_series(self):
        figure = ScatterChart(
            data=[[{"x": i, "y": i * 3} for i in range(4)]] * 2,
            subtitle=["a", "b"],
        )
        targets = _targets(figure)
        assert [type(a) for a, _ in targets] == [PathCollection, PathCollection]
        assert targets[1][1](3) == {"label": "b", "x": 3, "y": 9}

    def test_scatter_hue_groups_register_per_hue(self):
        data = [{"x": i, "y": i, "hue": "g1" if i < 2 else "g2"} for i in range(4)]
        targets = _targets(ScatterChart(data=data))
        assert [r(0)["label"] for _, r in targets] == ["g1", "g2"]
        # indices are local to the hue group's points
        assert targets[1][1](1) == {"label": "g2", "x": 3, "y": 3}

    def test_bar_registers_container_reporting_own_value(self):
        for bar_mode in ("group", "stack", "overlay"):
            targets = _targets(_bar_fig(bar_mode=bar_mode))
            assert [type(a) for a, _ in targets] == [BarContainer, BarContainer]
            assert targets[1][1](1) == {"label": "south", "x": "B", "y": 5}

    def test_horizontal_bar_reports_value_on_the_drawn_x(self):
        targets = _targets(_bar_fig(orientation="horizontal"))
        assert targets[0][1](2) == {"label": "north", "x": 4, "y": "C"}

    def test_pyramid_bars_report_positive_values(self):
        figure = PyramidChart(data=BAR_DATA, subtitle=["left", "right"])
        targets = _targets(figure)
        assert targets[0][1](0)["x"] == 3

    def test_log_scale_bars_report_the_data_value(self):
        targets = _targets(_bar_fig(scaley="log"))
        assert targets[0][1](0)["y"] == 3

    def test_composed_figures_register_their_own_targets(self):
        line, bar = _line_fig(), _bar_fig()
        panel = Panel([bar, line])
        grid = Grid([[line, bar]])
        assert len(_targets(panel)) == 4
        assert len(_targets(grid)) == 4
        # the source figures keep their own targets, on their own artists
        assert len(_targets(line)) == 2
        assert _targets(line)[0][0].figure is line
        assert _targets(panel)[2][0].figure is panel

    def test_line_in_horizontal_panel_swaps_axes(self):
        hbar = _bar_fig(orientation="horizontal")
        line = LineChart(data=[{"x": i, "y": i * 10} for i in range(3)])
        panel = Panel([hbar, line])
        resolver = _targets(panel)[2][1]
        assert resolver(1) == {"label": None, "x": 10, "y": 1}


GROUP_DATA = [{"label": "A", "value": v} for v in [1, 2, 3, 4, 10]] + [
    {"label": "B", "value": v} for v in [5, 6, 7]
]


def _vertex_near(collection, x, transpose=False):
    """The index of the polygon vertex closest to `x` along the band's x axis."""
    vertices = collection.get_paths()[0].vertices[:, 1 if transpose else 0]
    return int(np.argmin(np.abs(vertices - x)))


class TestCartesianLayers:
    """Point and bin layers on cartesian axes register their marks."""

    def test_stacked_area_band_reports_own_value_at_nearest_x(self):
        figure = StackedAreaChart(
            data=[
                [{"x": i, "y": i + 1} for i in range(4)],
                [{"x": i, "y": 10} for i in range(4)],
            ],
            subtitle=["low", "high"],
        )
        targets = _targets(figure)
        assert [type(a).__mro__[1] for a, _ in targets] == [PolyCollection] * 2
        band, resolver = targets[1]
        assert resolver((0, _vertex_near(band, 2))) == {
            "label": "high",
            "x": 2,
            "y": 10,
        }

    def test_histogram_bins_report_range_and_count(self):
        figure = Histogram(
            data=[{"x": v} for v in [0, 1, 2, 2, 3, 3, 3, 4, 5, 10]],
            num_bins=5,
            subtitle="values",
        )
        ((bars, resolver),) = _targets(figure)
        assert isinstance(bars, BarContainer)
        ax = figure.axes[0]
        edges = f"{ax.format_xdata(2.0).strip()} – {ax.format_xdata(4.0).strip()}"
        assert resolver(1) == {"label": "values", "x": edges, "y": 5}

    def test_horizontal_and_stacked_histograms_report_own_heights(self):
        data = [[{"x": v} for v in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]] * 2
        stacked = Histogram(
            data=data, num_bins=5, bar_mode="stack", subtitle=["a", "b"]
        )
        assert [r(0)["y"] for _, r in _targets(stacked)] == [2, 2]
        horizontal = Histogram(
            data=data[0], num_bins=5, orientation="horizontal", subtitle="a"
        )
        ((_, resolver),) = _targets(horizontal)
        assert resolver(0)["x"] == 2 and "–" in resolver(0)["y"]

    def test_step_histogram_outline_names_the_bin_of_a_vertex(self):
        figure = Histogram(
            data=[{"x": v} for v in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
            num_bins=5,
            style={"plot_hist_type": HISTOGRAM_TYPE.STEP},
        )
        ((outline, resolver),) = _targets(figure)
        assert isinstance(outline, Polygon)
        # vertex 3 sits on the second bin's top edge, at x=2..4
        vertex_x = outline.get_xy()[3][0]
        assert 2 <= vertex_x <= 4
        assert resolver(3)["y"] == 2

    def test_swarm_points_report_category_and_value(self):
        figure = SwarmPlot(data=GROUP_DATA, subtitle="scores")
        ((points, resolver),) = _targets(figure)
        assert isinstance(points, PathCollection)
        assert resolver(4) == {"label": "scores", "x": "A", "y": 10}
        assert resolver(6) == {"label": "scores", "x": "B", "y": 6}
        horizontal = SwarmPlot(data=GROUP_DATA, orientation="horizontal")
        assert _targets(horizontal)[0][1](0) == {"label": None, "x": 1, "y": "A"}

    def test_hexbin_hexagons_report_center_and_count(self):
        rng = np.random.default_rng(0)
        figure = HexbinChart(
            data={"x": rng.random(200), "y": rng.random(200)}, gridsize=4
        )
        ((tiles, resolver),) = _targets(figure)
        assert isinstance(tiles, PolyCollection)
        datum = resolver((3, 0))
        cx, cy = tiles.get_offsets()[3]
        assert datum == {
            "label": None,
            "x": cx,
            "y": cy,
            "count": int(tiles.get_array()[3]),
        }

    def test_hexbin_reduced_values_name_the_reducer(self):
        figure = HexbinChart(
            data={"x": [0, 0.1, 1, 1.1], "y": [0, 0.1, 1, 1.1], "c": [2, 4, 6, 8]},
            gridsize=2,
            reduce="mean",
        )
        ((tiles, resolver),) = _targets(figure)
        assert list(resolver((0, 0))) == ["label", "x", "y", "mean"]

    def test_heatmap_cells_report_labels_and_value(self):
        figure = Heatmap(
            data={"x": ["a", "b"], "y": ["p", "q"], "z": [[1, 2], [3, None]]},
            subtitle="grid",
        )
        ((image, resolver),) = _targets(figure)
        assert isinstance(image, AxesImage)
        assert resolver((1, 0)) == {"label": "grid", "x": "a", "y": "q", "value": 3}
        unlabeled = Heatmap(data={"z": [[1, 2], [3, 4]]})
        assert _targets(unlabeled)[0][1]((0, 1)) == {
            "label": None,
            "x": 1,
            "y": 0,
            "value": 2,
        }

    def test_contour_lines_and_bands_report_their_level(self):
        z = [[0, 1, 4], [1, 2, 5], [4, 5, 8]]
        lines = ContourChart(data={"z": z}, levels=[1, 3, 5], subtitle="height")
        ((contours, resolver),) = _targets(lines)
        assert isinstance(contours, ContourSet)
        assert resolver((1, 0.4)) == {"label": "height", "level": 3}
        filled = ContourChart(data={"z": z}, levels=[1, 3, 5], filled=True)
        ((bands, resolver),) = _targets(filled)
        assert resolver((0, 2)) == {"label": None, "level": "1 – 3"}


SUMMARY_A = {"median": 3, "q1": 2, "q3": 4, "min": 1, "max": 10}


class TestAggregateLayers:
    """Aggregate and structural marks report their summary."""

    def test_box_reports_category_and_five_numbers(self):
        figure = BoxPlot(data=GROUP_DATA, subtitle="scores")
        ((boxes, resolver),) = _targets(figure)
        assert isinstance(boxes, BarContainer) and len(boxes) == 2
        assert resolver(0) == {"label": "scores", "x": "A", **SUMMARY_A}
        horizontal = BoxPlot(data=GROUP_DATA, orientation="horizontal")
        datum = _targets(horizontal)[0][1](1)
        assert list(datum) == ["label", "y", "median", "q1", "q3", "min", "max"]
        assert datum["y"] == "B"

    def test_violin_bodies_report_the_same_summary(self):
        figure = ViolinPlot(data=GROUP_DATA, subtitle="scores")
        targets = _targets(figure)
        assert all(isinstance(a, PolyCollection) for a, _ in targets)
        assert len(targets) == 2
        assert targets[0][1]((0, 7)) == {"label": "scores", "x": "A", **SUMMARY_A}
        assert targets[1][1]((0, 0))["median"] == 6

    def test_split_violins_report_the_split_value(self):
        data = [
            {"label": "A", "value": v, "side": s} for v, s in zip(range(8), "LLLLRRRR")
        ]
        figure = ViolinPlot(data=data, split="side")
        assert [r((0, 0))["label"] for _, r in _targets(figure)] == ["L", "R"]

    def test_parallel_rows_report_the_axis_under_the_pointer(self):
        figure = ParallelCoords(
            data=[
                {"a": 1, "b": 2, "c": 3, "kind": "k1"},
                {"a": 4, "b": 5, "c": 6, "kind": "k2"},
            ],
            dimensions=["a", "b", "c"],
            hue="kind",
        )
        targets = _targets(figure)
        assert [type(a) for a, _ in targets] == [Line2D, Line2D]
        assert targets[1][1](2) == {"label": "k2", "c": 6}
        assert targets[0][1](0) == {"label": "k1", "a": 1}
        unhued = ParallelCoords(data=[{"a": 1, "b": 2}], subtitle="rows")
        assert _targets(unhued)[0][1](1) == {"label": "rows", "b": 2}

    def test_sankey_nodes_and_links_report_flows(self):
        figure = SankeyChart(
            data={
                "links": [
                    {"source": "A", "target": "X", "value": 3},
                    {"source": "A", "target": "Y", "value": 1},
                    {"source": "B", "target": "Y", "value": 2},
                ]
            }
        )
        (nodes, node_resolver), (links, link_resolver) = _targets(figure)
        assert isinstance(nodes, BarContainer) and len(nodes) == 4
        assert node_resolver(0) == {"label": "A", "flow": 4}
        assert node_resolver(3) == {"label": "Y", "flow": 3}
        assert len(links) == 3
        datums = [link_resolver(i) for i in range(3)]
        assert {"label": None, "source": "B", "target": "Y", "flow": 2} in datums

    def test_treemap_tiles_and_bands_report_values(self):
        figure = Treemap(
            data={
                "data": [
                    {
                        "label": "Asia",
                        "children": [
                            {"label": "India", "value": 30},
                            {"label": "China", "value": 20},
                        ],
                    },
                    {"label": "Africa", "value": 10},
                ]
            }
        )
        ((tiles, resolver),) = _targets(figure)
        assert isinstance(tiles, BarContainer)
        datums = [resolver(i) for i in range(len(tiles))]
        assert {"label": "India", "value": 30} in datums
        assert {"label": "Africa", "value": 10} in datums
        # the group's band stands for the group total
        assert {"label": "Asia", "value": 50} in datums

    def test_network_nodes_report_degree_and_edges_their_endpoints(self):
        weighted = NetworkChart(
            data={
                "edges": [
                    {"source": "a", "target": "b", "weight": 2},
                    {"source": "a", "target": "c", "weight": 3},
                ]
            }
        )
        targets = _targets(weighted)
        edges = [r for a, r in targets if isinstance(a, FancyArrowPatch)]
        ((nodes, node_resolver),) = [
            (a, r) for a, r in targets if isinstance(a, PathCollection)
        ]
        assert len(edges) == 2
        assert edges[0](0) == {"label": None, "source": "a", "target": "b", "weight": 2}
        assert node_resolver(0) == {"label": "a", "degree": 5}
        assert node_resolver(1) == {"label": "b", "degree": 2}
        directed = NetworkChart(
            data={
                "nodes": [
                    {"id": "a", "group": "core", "size": 40},
                    {"id": "b", "group": "core"},
                    {"id": "c"},
                ],
                "edges": [
                    {"source": "a", "target": "b", "weight": 2},
                    {"source": "c", "target": "a", "weight": 3},
                    {"source": "a", "target": "c", "weight": 1},
                ],
            },
            directed=True,
        )
        node = [r for a, r in _targets(directed) if isinstance(a, PathCollection)][0]
        # a directed node splits its degree; group and size ride along when given
        assert node(0) == {"label": "a", "in": 3, "out": 3, "group": "core", "size": 40}
        assert node(1) == {"label": "b", "in": 2, "out": 0, "group": "core"}
        assert node(2) == {"label": "c", "in": 1, "out": 3}
        unweighted = NetworkChart(
            data={
                "nodes": [{"id": "a", "label": "Alpha"}, {"id": "b"}, {"id": "c"}],
                "edges": [
                    {"source": "a", "target": "b"},
                    {"source": "a", "target": "c"},
                ],
            }
        )
        targets = _targets(unweighted)
        node = [r for a, r in targets if isinstance(a, PathCollection)][0]
        edge = [r for a, r in targets if isinstance(a, FancyArrowPatch)][0]
        assert node(0) == {"label": "Alpha", "degree": 2}
        assert edge(0) == {"label": None, "source": "a", "target": "b"}


RADIAL_DATA = [{"label": l, "y": v} for l, v in zip("NESW", [5, 10, 15, 20])]


class TestRadialLayers:
    """Radial marks report their angle and radius under their own keys."""

    def test_radial_marks_report_angle_and_radius(self):
        ((line, resolver),) = _targets(RadialChart(data=RADIAL_DATA, subtitle="wind"))
        assert isinstance(line, Line2D)
        assert resolver(1) == {"label": "wind", "angle": "E", "radius": 10}
        # the closing point repeats the first
        assert resolver(4) == resolver(0)
        ((bars, resolver),) = _targets(RadialChart(data=RADIAL_DATA, type="bar"))
        assert isinstance(bars, BarContainer)
        assert resolver(3) == {"label": None, "angle": "W", "radius": 20}
        ((points, resolver),) = _targets(RadialChart(data=RADIAL_DATA, type="scatter"))
        assert isinstance(points, PathCollection)
        assert resolver(2) == {"label": None, "angle": "S", "radius": 15}

    def test_stacked_radial_bars_report_their_own_value(self):
        figure = RadialChart(
            data=[RADIAL_DATA, RADIAL_DATA], type="bar", bar_mode="stack"
        )
        assert [r(0)["radius"] for _, r in _targets(figure)] == [5, 5]

    def test_radial_histogram_bins_report_degree_ranges(self):
        figure = RadialChart(
            data=[{"x": d} for d in [5, 10, 100, 200, 350]],
            type="histogram",
            num_bins=4,
        )
        ((bars, resolver),) = _targets(figure)
        assert isinstance(bars, BarContainer)
        assert resolver(0) == {"label": None, "angle": "0° – 90°", "radius": 2}


class TestHoverText:
    """The annotation lists the datum's fields in order; x and y are axis coordinates."""

    def test_named_fields_follow_the_axes_in_insertion_order(self):
        from datachart.utils._internal.figures import _hover_text

        figure = _line_fig(xlabel="Step")
        (line, _), *_ = _targets(figure)
        datum = {"label": "fast", "x": 2, "median": 4.5, "y": 3, "count": 7}
        assert _hover_text(line, datum) == "fast\nStep: 2\nmedian: 4.5\ny: 3\ncount: 7"

    def test_plain_values_read_as_numbers_or_text(self):
        from datachart.utils._internal.figures import _hover_text

        (line, _), *_ = _targets(_line_fig())
        datum = {"label": None, "level": 0.30000000000000004, "flow": 1200.0, "q": "A"}
        assert _hover_text(line, datum) == "level: 0.3\nflow: 1200\nq: A"

    def test_axis_only_datum_is_unchanged(self):
        from datachart.utils._internal.figures import _hover_text

        (line, _), *_ = _targets(_line_fig(ylabel="Loss"))
        assert (
            _hover_text(line, {"label": "fast", "x": 1, "y": 2})
            == "fast\nx: 1\nLoss: 2"
        )


class TestShowInteractive:
    """show(interactive=True) attaches hover cursors and keeps the static path."""

    def setup_method(self):
        plt.close("all")

    def teardown_method(self):
        plt.close("all")

    def test_default_show_registers_no_cursor(self):
        figure = _line_fig()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            figure.show()
        assert not hasattr(figure, "_hover_cursor")

    def test_script_path_adopts_and_attaches_cursor(self):
        figure = _line_fig(xlabel="Step", ylabel="Loss")
        _show_interactive(figure)
        managed = [plt.figure(num) for num in plt.get_fignums()]
        assert figure in managed
        texts = _hover(figure, figure.axes[0], 3, 6)
        assert texts == ["fast\nStep: 3\nLoss: 6"]

    def test_axis_names_default_to_x_and_y(self):
        figure = _line_fig()
        _show_interactive(figure)
        texts = _hover(figure, figure.axes[0], 1, 1)
        assert texts == ["slow\nx: 1\ny: 1"]

    def test_bar_hover_reports_category_and_height(self):
        figure = BarChart(
            data=BAR_DATA[0], xlabel="Region", ylabel="Count", subtitle="north"
        )
        _show_interactive(figure)
        # bar index 1 ("B") sits at x=1, hover halfway up
        texts = _hover(figure, figure.axes[0], 1, 0.5)
        assert texts == ["north\nRegion: B\nCount: 1"]

    def test_show_twice_attaches_one_cursor(self):
        figure = _line_fig()
        _show_interactive(figure)
        first = figure._hover_cursor
        _show_interactive(figure)
        assert figure._hover_cursor is first
        assert len(plt.get_fignums()) == 1

    def test_twin_axis_series_use_the_right_label(self):
        bar = BarChart(data=BAR_DATA[0], subtitle="count")
        line = LineChart(
            data=[{"x": i, "y": v} for i, v in enumerate([100, 300, 200])],
            subtitle="average",
        )
        panel = Panel(
            [bar, {"figure": line, "y_axis": "right"}],
            xlabel="Region",
            ylabel_left="Count",
            ylabel_right="Average",
        )
        _show_interactive(panel)
        left, right = panel.axes[0], panel.axes[1]
        assert _hover(panel, right, 1, 300) == ["average\nRegion: B\nAverage: 300"]
        assert _hover(panel, left, 2, 2) == ["count\nRegion: C\nCount: 4"]

    def test_grid_cells_all_have_hover(self):
        grid = Grid(
            [[_line_fig(xlabel="Step", ylabel="Loss"), _bar_fig(xlabel="Region")]],
            ylabel="Value",
        )
        _show_interactive(grid)
        line_ax, bar_ax = grid.axes[0], grid.axes[1]
        assert _hover(grid, line_ax, 4, 8) == ["fast\nStep: 4\nLoss: 8"]
        # the grid-level ylabel names the axis the cell left unlabeled
        assert _hover(grid, bar_ax, 0, 0.5)[0].startswith("north\nRegion: A\nValue: ")

    def test_hover_annotation_wears_the_theme_at_build_time(self):
        from matplotlib.colors import to_hex
        from datachart.config import config
        from datachart.constants import THEME

        config.set_theme(THEME.INK)
        try:
            ink = _line_fig()
        finally:
            config.set_theme(THEME.DEFAULT)
        default = _line_fig()
        themed = ((ink, "#000000", "#000000"), (default, "#b4bcc4", "#7f8c8d"))
        for figure, box_edge, arrow in themed:
            _show_interactive(figure)
            _hover(figure, figure.axes[0], 2, 4)
            annotation = figure._hover_cursor.selections[0].annotation
            assert to_hex(annotation.get_bbox_patch().get_edgecolor()) == box_edge
            assert to_hex(annotation.arrow_patch.get_edgecolor()) == arrow
            assert annotation.get_fontsize() == config["plot_text_size"]
            assert annotation.get_fontfamily() != ["sans-serif"]

    def test_step_line_hover_snaps_to_the_source_point(self):
        figure = LineChart(
            data=LINE_DATA[0],
            subtitle="steps",
            style={"plot_line_drawstyle": "steps-post"},
        )
        _show_interactive(figure)
        # on the riser between x=1 and x=2, which the post step draws at x=2
        texts = _hover(figure, figure.axes[0], 2, 3)
        assert texts == ["steps\nx: 1\ny: 2"]

    def test_shared_grid_axes_keep_their_own_labels(self):
        grid = Grid(
            [[_line_fig(ylabel="Apples"), _line_fig()]], sharey=True, sharex=True
        )
        _show_interactive(grid)
        assert _hover(grid, grid.axes[1], 2, 4) == ["fast\nx: 2\ny: 4"]

    def test_interactive_after_static_show_rebinds_the_cursor(self):
        figure = _line_fig()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            figure.show()
        _show_interactive(figure)
        first = figure._hover_cursor
        old_canvas = figure.canvas
        # a fresh canvas gets a fresh cursor; the stale one is disconnected
        figure.set_canvas(FigureCanvasAgg(figure))
        _show_interactive(figure)
        assert figure._hover_cursor is not first
        px, py = _pixel(figure.axes[0], 2, 4)
        event = MouseEvent("motion_notify_event", old_canvas, px, py)
        old_canvas.callbacks.process("motion_notify_event", event)
        assert first.selections == ()

    def test_band_and_hexagon_hover_pick_by_containment(self):
        area = StackedAreaChart(
            data=[
                [{"x": i, "y": 2} for i in range(4)],
                [{"x": i, "y": i + 1} for i in range(4)],
            ],
            subtitle=["base", "growth"],
            ylabel="Visits",
        )
        _show_interactive(area)
        # inside the upper band, between x=1 and x=2 but nearer 2
        texts = _hover(area, area.axes[0], 1.8, 3.5)
        visits = area.axes[0].format_ydata(3).strip()
        assert texts == [f"growth\nx: 2\nVisits: {visits}"]
        rng = np.random.default_rng(1)
        hexbin = HexbinChart(
            data={"x": rng.random(300), "y": rng.random(300)}, gridsize=3
        )
        _show_interactive(hexbin)
        ((tiles, _),) = _targets(hexbin)
        cx, cy = tiles.get_offsets()[4]
        texts = _hover(hexbin, hexbin.axes[0], cx, cy)
        ax = hexbin.axes[0]
        x, y = ax.format_xdata(cx).strip(), ax.format_ydata(cy).strip()
        assert texts == [f"x: {x}\ny: {y}\ncount: {int(tiles.get_array()[4])}"]

    def test_box_hover_picks_the_body_by_containment(self):
        figure = BoxPlot(data=GROUP_DATA, subtitle="scores", xlabel="Group")
        _show_interactive(figure)
        # the first box sits at position 1 and spans q1..q3 = 2..4
        assert _hover(figure, figure.axes[0], 1, 3) == [
            "scores\nGroup: A\nmedian: 3\nq1: 2\nq3: 4\nmin: 1\nmax: 10"
        ]

    def test_network_edge_hover_picks_the_outline(self):
        figure = NetworkChart(
            data={
                "nodes": [
                    {"id": "a", "x": 0.2, "y": 0.5},
                    {"id": "b", "x": 0.8, "y": 0.5},
                ],
                "edges": [{"source": "a", "target": "b", "weight": 4}],
            },
            layout="fixed",
            style={"plot_network_edge_style": "straight"},
        )
        _show_interactive(figure)
        assert _hover(figure, figure.axes[0], 0.5, 0.5) == [
            "source: a\ntarget: b\nweight: 4"
        ]

    def test_radial_bar_hover_names_the_category(self):
        figure = RadialChart(data=RADIAL_DATA, type="bar", subtitle="wind")
        _show_interactive(figure)
        # the "E" bar sits a quarter turn in and reaches radius 10
        assert _hover(figure, figure.axes[0], np.pi / 2, 5) == [
            "wind\nangle: E\nradius: 10"
        ]

    def test_heatmap_hover_reports_the_cell(self):
        figure = Heatmap(
            data={"x": ["a", "b"], "y": ["p", "q"], "z": [[1, 2], [3, 4]]},
            xlabel="Col",
            ylabel="Row",
        )
        _show_interactive(figure)
        assert _hover(figure, figure.axes[0], 1, 0) == ["Col: b\nRow: p\nvalue: 2"]

    def test_missing_mplcursors_raises_import_error(self, monkeypatch):
        monkeypatch.setitem(sys.modules, "mplcursors", None)
        with pytest.raises(ImportError, match=r"datachart\[interactive\]"):
            _line_fig().show(interactive=True)
        assert plt.get_fignums() == []


class TestShowInteractiveNotebook:
    """In a Jupyter kernel, show(interactive=True) displays an ipympl canvas."""

    @pytest.fixture
    def kernel(self, monkeypatch):
        import IPython.core.getipython
        import IPython.display

        shell = type("ZMQInteractiveShell", (), {})()
        monkeypatch.setattr(IPython.core.getipython, "get_ipython", lambda: shell)
        displays = []
        monkeypatch.setattr(
            IPython.display, "display", lambda *args, **kwargs: displays.append(args)
        )
        return displays

    @pytest.fixture
    def fake_ipympl(self, monkeypatch):
        shown = []

        class FakeCanvas(FigureCanvasAgg):
            _closed = True

        class FakeManager:
            def __init__(self, canvas, num):
                self.canvas = canvas
                self.num = num
                canvas.manager = self

            def show(self):
                shown.append(self)

        module = types.ModuleType("ipympl.backend_nbagg")
        module.Canvas = FakeCanvas
        module.FigureManager = FakeManager
        monkeypatch.setitem(sys.modules, "ipympl", types.ModuleType("ipympl"))
        monkeypatch.setitem(sys.modules, "ipympl.backend_nbagg", module)
        return shown

    def test_interactive_show_displays_widget_canvas(self, kernel, fake_ipympl):
        figure = _line_fig()
        figure.show(interactive=True)
        assert len(fake_ipympl) == 1
        manager = fake_ipympl[0]
        assert manager.canvas is figure.canvas
        assert type(figure.canvas).__name__ == "FakeCanvas"
        # no static PNG payload alongside the widget
        assert kernel == []
        assert plt.get_fignums() == []
        assert _hover(figure, figure.axes[0], 2, 4) == ["fast\nx: 2\ny: 4"]

    def test_widget_toolbar_deprecation_is_silenced(self, kernel, monkeypatch):
        import ipympl.backend_nbagg

        pytest.importorskip("ipympl")
        monkeypatch.setattr(
            ipympl.backend_nbagg.FigureManager, "show", lambda self: None
        )
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            _line_fig().show(interactive=True)

    def test_interactive_show_twice_reuses_the_manager(self, kernel, fake_ipympl):
        figure = _line_fig()
        figure.show(interactive=True)
        figure.show(interactive=True)
        assert len(fake_ipympl) == 2
        assert fake_ipympl[0] is fake_ipympl[1]

    def test_default_show_stays_static(self, kernel, fake_ipympl):
        figure = _line_fig()
        figure.show()
        assert fake_ipympl == []
        assert len(kernel) == 1

    def test_missing_ipympl_raises_import_error(self, kernel, monkeypatch):
        monkeypatch.setitem(sys.modules, "ipympl", None)
        monkeypatch.setitem(sys.modules, "ipympl.backend_nbagg", None)
        with pytest.raises(ImportError, match=r"ipympl.*datachart\[interactive\]"):
            _line_fig().show(interactive=True)
        assert kernel == []
