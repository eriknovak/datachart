import ast
import inspect
import textwrap
import unittest
from unittest import mock

import datachart.charts
from datachart.charts import (
    BasemapChart,
    BoxPlot,
    ContourChart,
    Heatmap,
    HexbinChart,
    LineChart,
    NetworkChart,
    RadialChart,
    RidgelinePlot,
)
from datachart.utils._internal import plot_engine
from datachart.utils._internal.chart_kinds import (
    CHART_KINDS,
    RECORD_KEYS,
    SHARED_PARAMETERS,
)

# the fronts that draw one panel through `render`; ScatterMatrix builds a grid
FRONTS = [name for name in datachart.charts.__all__ if name != "ScatterMatrix"]

# the figure-level settings every call below leaves unset
UNSET = dict.fromkeys(
    [
        "aspect_ratio",
        "emphasis_rule",
        "figsize",
        "legend",
        "max_cols",
        "sharex",
        "sharey",
        "show_grid",
        "xmax",
        "xmin",
        "xticks_format",
        "ylabel",
        "ymax",
        "ymin",
        "yticks_format",
    ]
)


def captured(front, *args, **kwargs):
    """The chart type, charts, and settings a front hands to `render_chart`."""

    with mock.patch.object(plot_engine, "render_chart") as render_chart:
        front(*args, **kwargs)
    return render_chart.call_args.args


class TestRowKeys(unittest.TestCase):
    def test_row_keys_name_front_parameters(self):
        for front in FRONTS:
            kind = CHART_KINDS[front.lower()]
            params = inspect.signature(getattr(datachart.charts, front)).parameters
            with self.subTest(front=front):
                self.assertLessEqual(kind.chart_keys | kind.figure_keys, set(params))

    def test_every_record_key_is_a_remap_parameter(self):
        for front in FRONTS:
            kind = CHART_KINDS[front.lower()]
            params = inspect.signature(getattr(datachart.charts, front)).parameters
            with self.subTest(front=front):
                self.assertLessEqual(set(kind.record_keys), set(params))

    def test_front_body_is_one_render_call(self):
        for front in FRONTS:
            source = inspect.getsource(getattr(datachart.charts, front))
            with self.subTest(front=front):
                self.assertNotIn("settings = {", source)
                self.assertNotIn("build_charts_structure(", source)
                self.assertIn("return render(", source)

    def test_params_copy_is_the_first_statement(self):
        # a local assigned before the copy would leak into the settings
        for front in FRONTS:
            tree = ast.parse(
                textwrap.dedent(inspect.getsource(getattr(datachart.charts, front)))
            )
            first = tree.body[0].body[1]
            with self.subTest(front=front):
                self.assertEqual(ast.unparse(first), "params = dict(locals())")


class TestSharedParameters(unittest.TestCase):
    def signatures(self):
        for front in datachart.charts.__all__:
            yield front, inspect.signature(getattr(datachart.charts, front)).parameters

    def test_fronts_conform_to_the_table(self):
        for front, params in self.signatures():
            kind = CHART_KINDS[front.lower()]
            for name, row in SHARED_PARAMETERS.items():
                if name not in params:
                    continue
                with self.subTest(front=front, parameter=name):
                    self.assertEqual(
                        params[name].annotation, row.signature_annotation(kind)
                    )
                    self.assertEqual(params[name].default, row.default)

    def test_every_row_is_shared(self):
        # a remap parameter is shared by its row, however many fronts take it
        counts = {name: 0 for name in SHARED_PARAMETERS if name not in RECORD_KEYS}
        for _, params in self.signatures():
            for name in counts.keys() & params.keys():
                counts[name] += 1
        for name, count in counts.items():
            with self.subTest(parameter=name):
                self.assertGreaterEqual(count, 2)


class TestRenderSplit(unittest.TestCase):
    def test_point_list_indexes_per_chart_lists(self):
        chart_type, charts, settings = captured(
            LineChart,
            [[{"x": 0, "y": 1}], [{"x": 0, "y": 2}]],
            subtitle=["a", "b"],
            x="x",
            y=["y", "y"],
            yerr="e",
            xticks=[[0, 1], [2]],
            xtickrotate=[10, 20],
            emphasis=["highlight", None],
            title="T",
            xlabel="X",
            show_legend=True,
            subplots=True,
            show_area=True,
        )
        self.assertEqual(chart_type, "linechart")
        self.assertEqual(
            charts,
            [
                {
                    "data": [{"x": 0, "y": 1}],
                    "subtitle": "a",
                    "emphasis": "highlight",
                    "xticks": [0, 1],
                    "xtickrotate": 10,
                },
                {
                    "data": [{"x": 0, "y": 2}],
                    "subtitle": "b",
                    "emphasis": None,
                    "xticks": [2],
                    "xtickrotate": 20,
                },
            ],
        )
        self.assertEqual(
            settings,
            {
                **UNSET,
                "title": "T",
                "xlabel": "X",
                "show_legend": True,
                "subplots": True,
                "show_area": True,
                "scalex": None,
                "scaley": None,
                "show_values": None,
                "show_yerr": None,
                "value_format": None,
                "value_step": None,
            },
        )

    def test_group_list_keeps_one_chart(self):
        chart_type, charts, settings = captured(
            BoxPlot,
            [{"label": "a", "value": 1}],
            label="label",
            value="value",
            style={"plot_box_color": "red"},
            hlines={"y": 1},
            title="T",
            orientation="horizontal",
            show_notch=True,
        )
        self.assertEqual(chart_type, "boxplot")
        self.assertEqual(
            charts,
            [
                {
                    "data": [{"label": "a", "value": 1}],
                    "hlines": {"y": 1},
                    "style": {"plot_box_color": "red"},
                }
            ],
        )
        self.assertEqual(
            settings,
            {
                **UNSET,
                "title": "T",
                "orientation": "horizontal",
                "show_notch": True,
                "scaley": None,
                "show_legend": None,
                "show_outliers": None,
                "show_values": None,
                "sort": None,
                "subplots": None,
                "value_format": None,
                "xlabel": None,
            },
        )

    def test_dict_data_is_one_chart(self):
        chart_type, charts, settings = captured(
            Heatmap,
            {"z": [[1, 2], [3, 4]]},
            subtitle="s",
            vmin=0,
            vmax=4,
            value_format="{x:.1f}",
            colorbar={"location": "right"},
            xticklabels=["a", "b"],
            title="T",
            show_colorbars=True,
        )
        self.assertEqual(chart_type, "heatmap")
        self.assertEqual(
            charts,
            [
                {
                    "data": {"z": [[1, 2], [3, 4]]},
                    "subtitle": "s",
                    "vmin": 0,
                    "vmax": 4,
                    "value_format": "{x:.1f}",
                    "colorbar": {"location": "right"},
                    "xticklabels": ["a", "b"],
                }
            ],
        )
        self.assertEqual(
            settings,
            {
                **UNSET,
                "title": "T",
                "show_colorbars": True,
                "show_values": None,
                "show_legend": None,
                "subplots": None,
                "xlabel": None,
            },
        )


GRID = {"z": [[1, 2], [3, 4]]}
POINTS = {"x": [0, 1, 2], "y": [0, 1, 2]}
GROUPS = [{"label": "a", "value": v} for v in (1, 2, 3, 5)]
WIND = [{"label": "N", "y": 1}, {"label": "E", "y": 2}, {"label": "S", "y": 3}]

# front, its data, the deprecated name, the new name, and a value for both
RENAMES = [
    (Heatmap, GRID, "show_heatmap_values", "show_values", True),
    (Heatmap, GRID, "valfmt", "value_format", "{x:.2f}"),
    (ContourChart, GRID, "valfmt", "value_format", "{x:.2f}"),
    (HexbinChart, POINTS, "valfmt", "value_format", "{x:.2f}"),
    (RidgelinePlot, GROUPS, "normalize", "ridge_scale", "common"),
    (RadialChart, WIND, "type", "mark", "bar"),
]


class TestDeprecatedNames(unittest.TestCase):
    def test_old_name_warns_at_the_caller_and_maps_to_the_new(self):
        for front, data, old, new, value in RENAMES:
            with self.subTest(front=front.__name__, name=old):
                expected = captured(front, data, **{new: value})
                with self.assertWarnsRegex(DeprecationWarning, f"`{new}`") as caught:
                    got = captured(front, data, **{old: value})
                self.assertEqual(caught.filename, __file__)
                self.assertEqual(got, expected)

    def test_basemap_features_is_data(self):
        expected = captured(BasemapChart, "land")
        with self.assertWarnsRegex(DeprecationWarning, "`data`"):
            got = captured(BasemapChart, features="land")
        self.assertEqual(got, expected)

    def test_both_names_raise(self):
        with self.assertWarns(DeprecationWarning):
            with self.assertRaisesRegex(ValueError, "`show_values` only"):
                Heatmap(GRID, show_values=True, show_heatmap_values=True)


class TestDictShape(unittest.TestCase):
    def test_missing_key_names_front_and_key(self):
        with self.assertRaisesRegex(
            ValueError, r"^Network `data` must be a dict with `edges`"
        ):
            NetworkChart({"nodes": []})

    def test_non_dict_names_front(self):
        with self.assertRaisesRegex(
            ValueError, r"^Heatmap `data` must be a dict with `z`"
        ):
            Heatmap([[1, 2]])


if __name__ == "__main__":
    unittest.main()
