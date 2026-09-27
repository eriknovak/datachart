import ast
import inspect
import textwrap
import unittest
import warnings
from datetime import date
from typing import Optional
from unittest import mock

import datachart.charts
from datachart.charts import (
    BasemapChart,
    BoxPlot,
    CalendarHeatmap,
    ContourChart,
    Heatmap,
    HexbinChart,
    LineChart,
    NetworkChart,
    RadialChart,
    RaincloudPlot,
    RidgelinePlot,
    ScatterChart,
    SwarmPlot,
)
from datachart.utils import Grid, Panel
from datachart.utils._internal import plot_engine
from datachart.themes._base import BASE_THEME
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
                # a deprecated name keeps the type it had
                if name not in params or name in kind.renamed:
                    continue
                with self.subTest(front=front, parameter=name):
                    self.assertEqual(
                        params[name].annotation, row.signature_annotation(kind)
                    )
                    self.assertEqual(params[name].default, row.default)

    def test_composition_fronts_conform_to_the_table(self):
        # a composition front has no row: it reads every value whole
        for front in (Panel, Grid):
            params = inspect.signature(front).parameters
            for name in params.keys() & SHARED_PARAMETERS.keys():
                row = SHARED_PARAMETERS[name]
                with self.subTest(front=front.__name__, parameter=name):
                    self.assertEqual(params[name].annotation, Optional[row.annotation])
                    self.assertEqual(params[name].default, row.default)

    def test_grid_takes_the_figure_furniture(self):
        params = inspect.signature(Grid).parameters
        furniture = {"show_legend", "legend", "show_grid", "aspect_ratio"}
        limits = {"xmin", "xmax", "ymin", "ymax"}
        self.assertLessEqual(furniture | limits, set(params))

    def test_settled_names_are_rows(self):
        self.assertLessEqual(
            {"fill", "swarm_mode", "show_colorbar"}, SHARED_PARAMETERS.keys()
        )
        self.assertFalse({"mode", "show_colorbars"} & SHARED_PARAMETERS.keys())

    def test_every_row_is_shared(self):
        # a remap parameter is shared by its row, however many fronts take it
        counts = {name: 0 for name in SHARED_PARAMETERS if name not in RECORD_KEYS}
        for _, params in self.signatures():
            for name in counts.keys() & params.keys():
                counts[name] += 1
        for name, count in counts.items():
            with self.subTest(parameter=name):
                self.assertGreaterEqual(count, 2)


class TestThemeDefaultKeys(unittest.TestCase):
    """A theme default is named for its parameter and, if one front's, its chart."""

    def descriptor_keys(self):
        keys = {
            f"chart_default_{p.name}": p.theme_default
            for p in SHARED_PARAMETERS.values()
            if p.theme_default is not None
        }
        for kind in CHART_KINDS.values():
            for parameter, key in kind.theme_defaults.items():
                self.assertIn(parameter, inspect.signature(front_of(kind)).parameters)
                # the chart is named as in its style keys, `plot_<chart>_*`
                chart = key[len("chart_default_") : -len(parameter) - 1]
                self.assertTrue(
                    any(k.startswith(f"plot_{chart}_") for k in BASE_THEME), key
                )
                keys[f"chart_default_{chart}_{parameter}"] = key
        return keys

    def test_keys_follow_the_rule(self):
        for expected, key in self.descriptor_keys().items():
            self.assertEqual(key, expected)

    def test_keys_are_the_base_theme_defaults(self):
        keys = set(self.descriptor_keys().values())
        self.assertLessEqual(keys, set(BASE_THEME))
        self.assertEqual(
            {k for k in BASE_THEME if k.startswith("chart_default_")}, keys
        )


def front_of(kind):
    """The front rendering under `kind`, found by its one render call."""

    for name in FRONTS:
        front = getattr(datachart.charts, name)
        if f'render("{kind.name}"' in inspect.getsource(front):
            return front
    raise AssertionError(f"no front renders {kind.name!r}")


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
                "show_labels": None,
                "label_position": None,
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
            show_colorbar=True,
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
                "show_colorbar": True,
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
NAMED = [{"x": 0, "y": 1, "name": "a"}, {"x": 1, "y": 2, "name": "b"}]
DAYS = {"date": [date(2024, 1, 1), date(2024, 1, 2)], "value": [1, 2]}

# front, its data, the deprecated name, the new name, and a value for both
RENAMES = [
    (Heatmap, GRID, "show_heatmap_values", "show_values", True),
    (Heatmap, GRID, "valfmt", "value_format", "{x:.2f}"),
    (ContourChart, GRID, "valfmt", "value_format", "{x:.2f}"),
    (HexbinChart, POINTS, "valfmt", "value_format", "{x:.2f}"),
    (RidgelinePlot, GROUPS, "normalize", "ridge_scale", "common"),
    (RadialChart, WIND, "type", "mark", "bar"),
    (ScatterChart, NAMED, "label", "annotation", "name"),
    (RadialChart, WIND, "startangle", "start_angle", "E"),
    (RadialChart, WIND, "innerradius", "inner_radius", 0.3),
    (ContourChart, GRID, "filled", "fill", True),
    (SwarmPlot, GROUPS, "mode", "swarm_mode", "strip"),
    (RaincloudPlot, GROUPS, "mode", "swarm_mode", "strip"),
    (HexbinChart, POINTS, "mincnt", "min_count", 2),
    (HexbinChart, POINTS, "gridsize", "grid_size", 5),
    (Heatmap, GRID, "show_colorbars", "show_colorbar", False),
    (CalendarHeatmap, DAYS, "show_colorbars", "show_colorbar", True),
    (ContourChart, GRID, "show_colorbars", "show_colorbar", False),
    (HexbinChart, POINTS, "show_colorbars", "show_colorbar", False),
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

    def test_old_name_warns_once(self):
        for front, data, old, _, value in RENAMES:
            with self.subTest(front=front.__name__, name=old):
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always")
                    captured(front, data, **{old: value})
                deprecations = [
                    w for w in caught if issubclass(w.category, DeprecationWarning)
                ]
                self.assertEqual(len(deprecations), 1)
                self.assertIn(f"`{old}`", str(deprecations[0].message))

    def test_old_name_is_listed_in_its_row(self):
        for front, _, old, new, _ in RENAMES:
            with self.subTest(front=front.__name__, name=old):
                self.assertEqual(CHART_KINDS[front.__name__.lower()].renamed[old], new)

    def test_basemap_features_is_data(self):
        expected = captured(BasemapChart, "land")
        with self.assertWarnsRegex(DeprecationWarning, "`data`"):
            got = captured(BasemapChart, features="land")
        self.assertEqual(got, expected)

    def test_both_names_raise(self):
        with self.assertWarns(DeprecationWarning):
            with self.assertRaisesRegex(ValueError, "`show_values` only"):
                Heatmap(GRID, show_values=True, show_heatmap_values=True)

    def test_old_name_warns_before_its_value_is_checked(self):
        bad = [
            (RadialChart, WIND, {"innerradius": 1.0}, "`inner_radius`"),
            (RadialChart, WIND, {"startangle": "north"}, "`start_angle`"),
            (
                ContourChart,
                GRID,
                {"filled": True, "emphasis_rule": {"top": 1}},
                "`fill",
            ),
        ]
        for front, data, kwargs, message in bad:
            with self.subTest(front=front.__name__, kwargs=kwargs):
                with self.assertWarns(DeprecationWarning):
                    with self.assertRaisesRegex(ValueError, message):
                        front(data, **kwargs)

    def test_both_names_raise_for_every_rename(self):
        for front, data, old, new, value in RENAMES:
            with self.subTest(front=front.__name__, name=old):
                with self.assertWarns(DeprecationWarning):
                    with self.assertRaisesRegex(ValueError, f"`{new}` only"):
                        front(data, **{old: value, new: value})


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
