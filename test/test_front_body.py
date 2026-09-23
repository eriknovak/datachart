import inspect
import unittest
from unittest import mock

import datachart.charts
from datachart.charts import BoxPlot, Heatmap, LineChart, NetworkChart
from datachart.utils._internal import plot_engine
from datachart.utils._internal.chart_kinds import CHART_KINDS

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

    def test_front_body_is_one_render_call(self):
        for front in FRONTS:
            source = inspect.getsource(getattr(datachart.charts, front))
            with self.subTest(front=front):
                self.assertNotIn("settings = {", source)
                self.assertNotIn("build_charts_structure(", source)
                self.assertIn("return render(", source)


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
            emphasis=["primary", None],
            title="T",
            xlabel="X",
            show_legend=True,
            subplots=True,
            show_area=True,
        )
        self.assertEqual(chart_type, "linechart")
        shared = {"x": "x", "y": "y", "yerr": "e"}
        self.assertEqual(
            charts,
            [
                {
                    "data": [{"x": 0, "y": 1}],
                    "subtitle": "a",
                    "emphasis": "primary",
                    "xticks": [0, 1],
                    "xtickrotate": 10,
                    **shared,
                },
                {
                    "data": [{"x": 0, "y": 2}],
                    "subtitle": "b",
                    "emphasis": None,
                    "xticks": [2],
                    "xtickrotate": 20,
                    **shared,
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
            {
                "data": [{"label": "a", "value": 1}],
                "hlines": {"y": 1},
                "label": "label",
                "style": {"plot_box_color": "red"},
                "value": "value",
            },
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
            valfmt="{x:.1f}",
            colorbar={"location": "right"},
            xticklabels=["a", "b"],
            title="T",
            show_colorbars=True,
        )
        self.assertEqual(chart_type, "heatmap")
        self.assertEqual(
            charts,
            {
                "data": {"z": [[1, 2], [3, 4]]},
                "subtitle": "s",
                "vmin": 0,
                "vmax": 4,
                "valfmt": "{x:.1f}",
                "colorbar": {"location": "right"},
                "xticklabels": ["a", "b"],
            },
        )
        self.assertEqual(
            settings,
            {
                **UNSET,
                "title": "T",
                "show_colorbars": True,
                "show_heatmap_values": None,
                "show_legend": None,
                "subplots": None,
                "xlabel": None,
            },
        )


class TestDictShape(unittest.TestCase):
    def test_missing_key_names_front_and_key(self):
        with self.assertRaisesRegex(
            ValueError, r"^Network `data` must be a dict with an `edges` key"
        ):
            NetworkChart({"nodes": []})

    def test_non_dict_names_front(self):
        with self.assertRaisesRegex(ValueError, r"^Heatmap `data` must be a dict with a `z` key"):
            Heatmap([[1, 2]])


if __name__ == "__main__":
    unittest.main()
