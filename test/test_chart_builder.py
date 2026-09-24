import copy
import unittest
from datetime import date

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datachart.charts import CalendarHeatmap, DumbbellChart, GanttChart, LineChart
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
        self.assertEqual(charts, [{"data": {"t": [1, 2], "x": [1, 2], "y": [3, 4]}}])

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


if __name__ == "__main__":
    unittest.main()
