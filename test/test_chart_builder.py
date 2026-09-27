import copy
import unittest
from datetime import date

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from datachart.charts import (
    CalendarHeatmap,
    DumbbellChart,
    GanttChart,
    LineChart,
    ScatterChart,
)
from datachart.utils._internal.chart_builder import build_charts_structure
from datachart.utils._internal.chart_kinds import CHART_KINDS

# one well-formed dict of each grid front's data
GRIDS = {
    "calendarheatmap": {"date": [date(2024, 1, 1)], "value": [1.0]},
    "heatmap": {"z": [[1, 2], [3, 4]]},
    "contourchart": {"z": [[1, 2], [3, 4]]},
    "hexbinchart": {"x": [0, 1], "y": [1, 0]},
    "imagechart": {"image": [[0, 1], [1, 0]], "extent": (0, 1, 0, 1)},
    "basemapchart": {"lon": [0.0, 1.0], "lat": [0.0, 1.0]},
    "networkchart": {"edges": [{"source": "a", "target": "b"}]},
    "sankeychart": {"links": [{"source": "a", "target": "b", "value": 1}]},
    "treemap": {"data": [{"label": "a", "value": 1}]},
}


def record(kind, prefix=""):
    """A record carrying every canonical key of the row, under `prefix`."""

    return {f"{prefix}{key}": f"{key}-value" for key in kind.record_keys}


class TestRecordRows(unittest.TestCase):
    def test_every_row_is_covered(self):
        record_rows = {n for n, k in CHART_KINDS.items() if not k.dict_data}
        self.assertEqual(set(GRIDS), set(CHART_KINDS) - record_rows)

    def test_single_dataset_is_one_canonical_chart(self):
        for name, kind in CHART_KINDS.items():
            if kind.dict_data:
                continue
            with self.subTest(kind=name):
                data = [record(kind), {**record(kind), "emphasis": "highlight"}]
                self.assertEqual(build_charts_structure(name, data), [{"data": data}])

    def test_several_datasets_are_one_chart_each(self):
        for name, kind in CHART_KINDS.items():
            if kind.dict_data:
                continue
            with self.subTest(kind=name):
                data = [[record(kind)], [record(kind), record(kind)]]
                self.assertEqual(
                    build_charts_structure(name, data),
                    [{"data": data[0]}, {"data": data[1]}],
                )

    def test_remapped_keys_come_out_canonical(self):
        for name, kind in CHART_KINDS.items():
            if not kind.record_keys:
                continue
            with self.subTest(kind=name):
                data = [record(kind, prefix="my_")]
                remaps = {key: f"my_{key}" for key in kind.record_keys}
                self.assertEqual(
                    build_charts_structure(name, data, **remaps),
                    [{"data": [{**data[0], **record(kind)}]}],
                )

    def test_remaps_index_per_dataset(self):
        data = [[{"a": 1, "y": 2}], [{"b": 3, "y": 4}]]
        charts = build_charts_structure("linechart", data, x=["a", "b"])
        self.assertEqual(
            [chart["data"] for chart in charts],
            [[{"a": 1, "x": 1, "y": 2}], [{"b": 3, "x": 3, "y": 4}]],
        )

    def test_none_remap_leaves_the_dataset_without_the_key(self):
        data = [[{"x": 1, "y": 2, "yerr": 1}]] * 2
        charts = build_charts_structure("linechart", data, yerr=[None, "yerr"])
        self.assertEqual(charts[0]["data"], [{"x": 1, "y": 2}])
        self.assertEqual(charts[1]["data"], [{"x": 1, "y": 2, "yerr": 1}])

    def test_columns_are_renamed_too(self):
        charts = build_charts_structure("linechart", {"t": [1, 2], "y": [3, 4]}, x="t")
        records = [{"t": 1, "x": 1, "y": 3}, {"t": 2, "x": 2, "y": 4}]
        self.assertEqual(charts, [{"data": records}])

    def test_caller_records_are_not_mutated(self):
        data = [{"t": 1, "v": 2}]
        before = copy.deepcopy(data)
        build_charts_structure("linechart", data, x="t", y="v")
        self.assertEqual(data, before)


class TestRequiredKeys(unittest.TestCase):
    def test_missing_key_names_front_record_and_key(self):
        for name, kind in CHART_KINDS.items():
            if not kind.required_keys:
                continue
            key = kind.required_keys[-1]
            with self.subTest(kind=name):
                partial = {k: v for k, v in record(kind).items() if k != key}
                label = f"{kind.label[0].upper()}{kind.label[1:]}"
                with self.assertRaisesRegex(
                    ValueError,
                    rf"^{label} record `data\[1\]` has no `{key}` key\.$",
                ):
                    build_charts_structure(name, [record(kind), partial])

    def test_several_datasets_name_the_dataset(self):
        with self.assertRaisesRegex(ValueError, r"`data\[1\]\[0\]` has no `y` key"):
            build_charts_structure("linechart", [[{"x": 0, "y": 0}], [{"x": 0}]])

    def test_missing_key_names_the_callers_key(self):
        with self.assertRaisesRegex(ValueError, "has no `value` key"):
            build_charts_structure("linechart", [{"x": 0}], y="value")


class TestGridRows(unittest.TestCase):
    def test_one_dict_is_one_chart_and_a_list_is_one_each(self):
        for name, grid in GRIDS.items():
            with self.subTest(kind=name):
                self.assertEqual(build_charts_structure(name, grid), [{"data": grid}])
                self.assertEqual(
                    build_charts_structure(name, [grid, grid]),
                    [{"data": grid}, {"data": grid}],
                )


class TestMalformedData(unittest.TestCase):
    RECORDS = [{"x": 1, "y": 2}, {"x": 2, "y": 3}]

    def assertRejects(self, chart_type, data, pattern):
        with self.assertRaisesRegex(ValueError, pattern):
            build_charts_structure(chart_type, data)

    def test_non_list_data_names_front_shape_and_type(self):
        for data, got in (
            (None, "NoneType"),
            (5, "int"),
            ("abc", "str"),
            (np.array([1, 2, 3]), "ndarray"),
        ):
            with self.subTest(data=data):
                self.assertRejects(
                    "linechart", data, rf"Line chart `data` must be .*records.*{got}"
                )

    def test_a_record_that_is_not_a_dict_is_named(self):
        self.assertRejects("linechart", [1, 2], r"`data\[0\]` must be a dict.*int")
        self.assertRejects(
            "linechart",
            [[{"x": 1, "y": 2}], [{"x": 1, "y": 2}, 5]],
            r"`data\[1\]\[1\]`",
        )

    def test_a_column_that_is_not_a_list_is_named(self):
        self.assertRejects("linechart", {"x": 1, "y": 2}, r"`data\['x'\]`.*int")

    def test_columns_read_as_records(self):
        columns = {"x": (1, 2), "y": np.array([3, 4])}
        self.assertEqual(
            build_charts_structure("linechart", columns),
            [{"data": [{"x": 1, "y": 3}, {"x": 2, "y": 4}]}],
        )

    def test_a_list_of_column_dicts_is_one_chart_each(self):
        charts = build_charts_structure(
            "linechart", [{"x": [1, 2], "y": [3, 4]}, {"x": [5], "y": [6]}]
        )
        self.assertEqual(
            charts,
            [
                {"data": [{"x": 1, "y": 3}, {"x": 2, "y": 4}]},
                {"data": [{"x": 5, "y": 6}]},
            ],
        )

    def test_a_record_with_a_list_value_stays_a_record(self):
        records = [{"x": 1, "y": 2, "yerr": [0.5, 1.0]}]
        self.assertEqual(
            build_charts_structure("linechart", records), [{"data": records}]
        )

    def test_columns_of_unequal_length_are_named(self):
        self.assertRejects(
            "linechart", {"x": [1, 2], "y": [3]}, r"equal lengths.*'x': 2, 'y': 1"
        )

    def test_scatter_draws_columns_like_records(self):
        figure = ScatterChart({"x": [1, 2], "y": [3, 4]})
        offsets = figure.axes[0].collections[0].get_offsets()
        self.assertEqual(offsets.tolist(), [[1, 3], [2, 4]])
        plt.close(figure)

    def test_empty_data_still_passes(self):
        self.assertEqual(build_charts_structure("linechart", []), [{"data": []}])

    def test_tuples_and_generators_read_as_lists(self):
        expected = build_charts_structure("linechart", self.RECORDS)
        for data in (tuple(self.RECORDS), (r for r in self.RECORDS)):
            with self.subTest(data=type(data).__name__):
                self.assertEqual(build_charts_structure("linechart", data), expected)
        nested = build_charts_structure("linechart", (tuple(self.RECORDS),) * 2)
        self.assertEqual(
            nested, build_charts_structure("linechart", [self.RECORDS] * 2)
        )

    def test_a_generator_draws_like_a_list(self):
        figure = LineChart(r for r in self.RECORDS)
        self.assertEqual(len(figure.axes[0].lines), 1)
        plt.close(figure)

    def test_a_generator_inside_a_grid_dict_reads_as_a_list(self):
        grid = {"z": (row for row in [[1, 2], [3, 4]])}
        self.assertEqual(
            build_charts_structure("heatmap", grid), [{"data": {"z": [[1, 2], [3, 4]]}}]
        )

    def test_grid_fronts_reject_a_non_dict(self):
        for name in GRIDS:
            # a basemap's data may also be a feature name or a list of them
            if name == "basemapchart":
                continue
            with self.subTest(kind=name):
                self.assertRejects(name, 5, "`data` must be a dict")


class TestFrontsThroughTheBuilder(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_calendar_splits_per_year(self):
        data = {"date": [date(2023, 6, 1), date(2024, 6, 1)], "value": [1, 2]}
        figure = CalendarHeatmap(data)
        titles = [ax.get_title() for ax in figure.axes if ax.get_title()]
        self.assertEqual(titles, ["2023", "2024"])

    def test_several_dumbbell_datasets_draw_one_subplot_each(self):
        rows = [{"label": "a", "start": 1, "end": 2}]
        figure = DumbbellChart([rows, rows], subplots=True)
        self.assertEqual(len([ax for ax in figure.axes if ax.axison]), 2)

    def test_remapped_gantt_matches_canonical(self):
        tasks = [{"task": "a", "start": date(2024, 1, 1), "end": date(2024, 1, 5)}]
        renamed = [
            {"name": t["task"], "from": t["start"], "to": t["end"]} for t in tasks
        ]
        canonical = GanttChart(tasks)
        remapped = GanttChart(renamed, task="name", start="from", end="to")
        self.assertEqual(
            [t.get_text() for t in canonical.axes[0].get_yticklabels()],
            [t.get_text() for t in remapped.axes[0].get_yticklabels()],
        )

    def test_remapped_line_matches_canonical(self):
        canonical = LineChart([{"x": 0, "y": 1}, {"x": 1, "y": 3}])
        remapped = LineChart([{"t": 0, "v": 1}, {"t": 1, "v": 3}], x="t", y="v")
        self.assertEqual(
            canonical.axes[0].lines[0].get_xydata().tolist(),
            remapped.axes[0].lines[0].get_xydata().tolist(),
        )


MARK_PARAMETERS = (
    "vlines",
    "hlines",
    "dlines",
    "brackets",
    "vspans",
    "hspans",
    "texts",
)
LINE = [{"x": 0, "y": 1}, {"x": 1, "y": 3}]


class TestMarkLists(unittest.TestCase):
    """A flat mark list is every chart's; a list holding lists is per chart."""

    def tearDown(self):
        plt.close("all")

    def marks(self, name, value):
        charts = build_charts_structure("linechart", [LINE, LINE], **{name: value})
        return [chart.get(name) for chart in charts]

    def test_flat_list_goes_to_every_chart(self):
        for name in MARK_PARAMETERS:
            with self.subTest(parameter=name):
                flat = [{"n": 0}, {"n": 1}, {"n": 2}]
                self.assertEqual(self.marks(name, flat), [flat, flat])

    def test_one_dict_goes_to_every_chart(self):
        for name in MARK_PARAMETERS:
            with self.subTest(parameter=name):
                self.assertEqual(self.marks(name, {"n": 0}), [{"n": 0}, {"n": 0}])

    def test_list_of_lists_is_per_chart(self):
        for name in MARK_PARAMETERS:
            with self.subTest(parameter=name):
                nested = [[{"n": 0}], [{"n": 1}, {"n": 2}]]
                self.assertEqual(self.marks(name, nested), nested)

    def test_mixed_list_is_per_chart(self):
        for name in MARK_PARAMETERS:
            with self.subTest(parameter=name):
                mixed = [{"n": 0}, None]
                self.assertEqual(self.marks(name, mixed), [{"n": 0}, None])

    def test_one_chart_takes_the_first_of_each_charts_marks(self):
        charts = build_charts_structure(
            "linechart", LINE, vlines=[[{"n": 0}, {"n": 1}]]
        )
        self.assertEqual(charts[0]["vlines"], [{"n": 0}, {"n": 1}])

    def vline_positions(self, ax):
        return sorted(
            float(segment[0][0])
            for collection in ax.collections
            for segment in collection.get_segments()
        )

    def test_flat_vlines_draw_in_full_on_one_axes(self):
        vlines = [{"x": 1}, {"x": 2}, {"x": 3}]
        figure = LineChart([LINE, LINE], vlines=vlines)
        self.assertEqual(self.vline_positions(figure.axes[0]), [1, 2, 3])

    def test_flat_vlines_draw_in_full_on_every_subplot(self):
        vlines = [{"x": 1}, {"x": 2}, {"x": 3}]
        figure = LineChart([LINE, LINE], vlines=vlines, subplots=True)
        axes = [ax for ax in figure.axes if ax.axison]
        self.assertEqual(len(axes), 2)
        for ax in axes:
            self.assertEqual(self.vline_positions(ax), [1, 2, 3])

    def test_nested_vlines_draw_per_subplot(self):
        vlines = [[{"x": 1}], [{"x": 2}, {"x": 3}]]
        figure = LineChart([LINE, LINE], vlines=vlines, subplots=True)
        axes = [ax for ax in figure.axes if ax.axison]
        self.assertEqual(self.vline_positions(axes[0]), [1])
        self.assertEqual(self.vline_positions(axes[1]), [2, 3])


MISSING = (None, float("nan"), float("inf"), -float("inf"))


def finite_record(kind):
    """A record whose position and value keys hold the number 1."""

    keys = set(kind.position_keys) | set(kind.value_keys)
    return {**record(kind), **{key: 1 for key in keys}}


class TestMissingValues(unittest.TestCase):
    def record_rows(self):
        for name, kind in CHART_KINDS.items():
            if not kind.dict_data and kind.record_keys:
                yield name, kind

    def test_every_record_row_declares_a_position(self):
        for name, kind in self.record_rows():
            with self.subTest(kind=name):
                self.assertTrue(kind.position_keys)
                self.assertLessEqual(set(kind.position_keys), set(kind.record_keys))
                self.assertLessEqual(set(kind.value_keys), set(kind.record_keys))

    def test_a_missing_position_drops_the_record(self):
        for name, kind in self.record_rows():
            for key in kind.position_keys:
                for missing in MISSING:
                    with self.subTest(kind=name, key=key, missing=missing):
                        kept = finite_record(kind)
                        data = [kept, {**kept, key: missing}]
                        (chart,) = build_charts_structure(name, data)
                        self.assertEqual(chart["data"], [kept])

    def test_a_missing_value_reads_as_nan(self):
        for name, kind in self.record_rows():
            for key in kind.value_keys:
                for missing in MISSING:
                    with self.subTest(kind=name, key=key, missing=missing):
                        kept = finite_record(kind)
                        data = [{**kept, key: missing}, kept]
                        (chart,) = build_charts_structure(name, data)
                        self.assertTrue(np.isnan(chart["data"][0][key]))
                        self.assertEqual(chart["data"][1], kept)

    def test_finite_values_keep_their_type(self):
        data = [{"x": 1, "y": 2}, {"x": 2, "y": 3.5}]
        (chart,) = build_charts_structure("linechart", data)
        self.assertEqual(chart["data"], data)
        self.assertIsInstance(chart["data"][0]["y"], int)

    def test_a_list_of_observations_reads_missing_as_nan(self):
        (chart,) = build_charts_structure("histogram", [{"x": [1, None, np.inf]}])
        x = chart["data"][0]["x"]
        self.assertEqual(x[0], 1)
        self.assertTrue(np.isnan(x[1:]).all())

    def test_a_missing_date_drops_the_record(self):
        kept = {"x": date(2024, 1, 1), "y": 1}
        data = [kept, {"x": np.datetime64("NaT"), "y": 2}]
        (chart,) = build_charts_structure("linechart", data)
        self.assertEqual(chart["data"], [kept])

    def test_an_absent_key_still_raises(self):
        with self.assertRaisesRegex(ValueError, "record `data\\[0\\]` has no `y`"):
            build_charts_structure("linechart", [{"x": 1}])

    def test_every_value_missing_raises(self):
        for data in (
            [{"x": 1, "y": None}, {"x": None, "y": 1}],
            [[{"x": None, "y": 1}]],
        ):
            with self.subTest(data=data):
                with self.assertRaisesRegex(
                    ValueError, "Line chart has nothing to draw"
                ):
                    build_charts_structure("linechart", data)
        with self.assertRaisesRegex(ValueError, "Heatmap has nothing to draw"):
            build_charts_structure("heatmap", {"z": [[None, np.nan]]})

    def test_one_chart_with_values_is_enough(self):
        data = [[{"x": 1, "y": None}], [{"x": 1, "y": 2}]]
        charts = build_charts_structure("linechart", data)
        self.assertEqual(len(charts), 2)

    def test_empty_data_is_not_missing(self):
        self.assertEqual(build_charts_structure("linechart", []), [{"data": []}])

    def test_caller_records_are_not_mutated(self):
        data = [{"x": 1, "y": None}, {"x": None, "y": 1}, {"x": 2, "y": 3}]
        before = copy.deepcopy(data)
        build_charts_structure("linechart", data)
        self.assertEqual(data, before)

    def test_a_grid_reads_a_missing_cell_as_nan(self):
        for name in ("heatmap", "contourchart"):
            for missing in MISSING:
                with self.subTest(kind=name, missing=missing):
                    grid = {"z": [[1, missing], [3, 4]]}
                    (chart,) = build_charts_structure(name, grid)
                    z = chart["data"]["z"]
                    self.assertIsInstance(z[0][0], int)
                    self.assertTrue(np.isnan(z[0][1]))
        array = np.array([[1.0, np.inf], [3.0, 4.0]])
        (chart,) = build_charts_structure("heatmap", {"z": array})
        self.assertTrue(np.isnan(chart["data"]["z"][0, 1]))
        self.assertTrue(np.isinf(array[0, 1]))

    def test_a_finite_grid_is_left_as_given(self):
        for name, grid in GRIDS.items():
            with self.subTest(kind=name):
                self.assertEqual(build_charts_structure(name, grid), [{"data": grid}])

    def test_a_missing_grid_position_drops_the_row(self):
        (chart,) = build_charts_structure(
            "hexbinchart", {"x": [0, None, 2], "y": [1, 1, np.inf], "c": [1, 2, 3]}
        )
        self.assertEqual(chart["data"], {"x": [0], "y": [1], "c": [1]})
        (chart,) = build_charts_structure(
            "calendarheatmap",
            {"date": [date(2024, 1, 1), None, date(2024, 1, 3)], "value": [None, 2, 3]},
        )
        self.assertEqual(chart["data"]["date"], [date(2024, 1, 1), date(2024, 1, 3)])
        self.assertTrue(np.isnan(chart["data"]["value"][0]))
        self.assertEqual(chart["data"]["value"][1], 3)


if __name__ == "__main__":
    unittest.main()
