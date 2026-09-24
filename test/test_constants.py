import inspect
import re
import unittest
import warnings
from datetime import date, datetime, timedelta
from unittest import mock

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from datachart import constants
from datachart.charts import (
    BarChart,
    BasemapChart,
    BumpChart,
    CalendarHeatmap,
    ContourChart,
    DumbbellChart,
    GanttChart,
    Heatmap,
    HexbinChart,
    ImageChart,
    LineChart,
    NetworkChart,
    RadialChart,
    RidgelinePlot,
    ScatterMatrix,
    StackedAreaChart,
    SwarmPlot,
    ViolinPlot,
)
from datachart.constants import (
    BANDWIDTH,
    BASEMAP_FEATURE,
    Domain,
    LINE_DRAW_STYLE,
    LINE_MARKER,
    LINE_STYLE,
    ORIENTATION,
    SCATTER_MATRIX_DIAGONAL,
    SORT,
    VALUE_FORMAT,
)
from datachart.utils import Panel
from datachart.utils._internal import plot_engine


def constant_classes():
    return [
        cls
        for name, cls in vars(constants).items()
        if inspect.isclass(cls) and issubclass(cls, Domain) and cls is not Domain
    ]


class TestDomainBase(unittest.TestCase):
    def test_every_class_derives_from_the_base_and_has_a_default(self):
        public = [
            cls
            for name, cls in vars(constants).items()
            if inspect.isclass(cls)
            and cls.__module__ == constants.__name__
            and not name.startswith("_")
            and cls is not Domain
        ]
        self.assertGreater(len(public), 40)
        for cls in public:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(issubclass(cls, Domain))
                self.assertIn("DEFAULT", vars(cls))

    def test_members_are_the_public_values_in_order(self):
        self.assertEqual(ORIENTATION.members(), ("vertical", "horizontal"))
        self.assertEqual(SORT.members(), (None, "ascending", "descending"))

    def test_a_string_default_is_a_member(self):
        self.assertIn("default", LINE_DRAW_STYLE.members())

    def test_a_combined_default_is_not_a_member(self):
        self.assertNotIn(BASEMAP_FEATURE.DEFAULT, BASEMAP_FEATURE.members())

    def test_check_returns_a_member_and_the_equal_raw_string(self):
        self.assertEqual(ORIENTATION.check(ORIENTATION.HORIZONTAL, "o"), "horizontal")
        self.assertEqual(ORIENTATION.check("horizontal", "o"), "horizontal")

    def test_check_passes_none(self):
        self.assertIsNone(BANDWIDTH.check(None, "bandwidth"))

    def test_check_raises_one_shape(self):
        with self.assertRaises(ValueError) as caught:
            ORIENTATION.check("sideways", "orientation")
        self.assertEqual(
            str(caught.exception),
            "Invalid `orientation` value 'sideways'. "
            "Must be one of ('vertical', 'horizontal').",
        )

    def test_an_open_vocabulary_takes_its_form(self):
        self.assertEqual(VALUE_FORMAT.check("{x:.1f} km", "v"), "{x:.1f} km")
        self.assertEqual(VALUE_FORMAT.check("%.2f", "v"), "%.2f")
        with self.assertRaisesRegex(ValueError, "Invalid `v` value 'km'"):
            VALUE_FORMAT.check("km", "v")


class TestModuleDocstring(unittest.TestCase):
    def test_every_class_is_listed_with_its_reader(self):
        for cls in constant_classes():
            with self.subTest(cls=cls.__name__):
                self.assertIn(f"    {cls.__name__}:", constants.__doc__)


class TestNoneMeansUnset(unittest.TestCase):
    def test_every_none_member_is_none(self):
        for cls in constant_classes():
            if "NONE" in vars(cls):
                with self.subTest(cls=cls.__name__):
                    self.assertIsNone(vars(cls)["NONE"])

    def test_renamed_members_warn_and_resolve(self):
        for cls, old, new in [
            (LINE_MARKER, "NONE", "NO_MARKER"),
            (LINE_STYLE, "NONE", "NO_LINE"),
            (SCATTER_MATRIX_DIAGONAL, "NONE", "BLANK"),
        ]:
            with self.subTest(cls=cls.__name__):
                with self.assertWarns(DeprecationWarning):
                    value = getattr(cls, old)
                self.assertEqual(value, getattr(cls, new))

    def test_renamed_classes_warn_and_resolve(self):
        for old, new in [("SCALE", "AXIS_SCALE"), ("NORMALIZE", "COLOR_NORM")]:
            with self.subTest(old=old):
                with self.assertWarns(DeprecationWarning):
                    cls = getattr(constants, old)
                self.assertIs(cls, getattr(constants, new))

    def test_a_current_member_does_not_warn(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            self.assertEqual(LINE_MARKER.NO_MARKER, "")


LINE = [{"x": 1, "y": 2}, {"x": 2, "y": 3}]
BARS = [{"label": "a", "y": 1}, {"label": "b", "y": 2}]
GROUPS = [{"label": "a", "value": v} for v in (1.0, 2.0, 3.0)]
GRID = {"z": [[1.0, 2.0], [3.0, 4.0]]}
POINTS = [{"x": float(i), "y": float(i % 3)} for i in range(10)]
START = datetime(2024, 1, 1)
TASKS = [{"task": "a", "start": START, "end": START + timedelta(days=2)}]
RANGES = [{"label": "a", "start": 1, "end": 2}]
EDGES = {"edges": [{"source": "A", "target": "B"}]}
CALENDAR = {"date": [date(2024, 1, 1), date(2024, 1, 2)], "value": [1, 2]}
IMAGE = {"image": np.zeros((2, 2)), "extent": (0.0, 1.0, 0.0, 1.0)}
COLUMNS = {"a": [1.0, 2.0, 3.0], "b": [2.0, 1.0, 3.0]}

# one front per shared constant-typed parameter, and every front-own one
CASES = [
    ("orientation", BarChart, BARS),
    ("scalex", LineChart, LINE),
    ("scaley", LineChart, LINE),
    ("aspect_ratio", LineChart, LINE),
    ("value_format", BarChart, BARS),
    ("bar_mode", BarChart, BARS),
    ("mode", SwarmPlot, GROUPS),
    ("emphasis", LineChart, LINE),
    ("sort", BarChart, BARS),
    ("show_grid", LineChart, LINE),
    ("position", ImageChart, IMAGE),
    ("bandwidth", ViolinPlot, GROUPS),
    ("figsize", LineChart, LINE),
    ("norm", Heatmap, GRID),
    ("yticks_format", LineChart, LINE),
    ("xticks_format", LineChart, LINE),
    ("baseline", StackedAreaChart, LINE),
    ("rank_by", BumpChart, LINE),
    ("label_position", BumpChart, LINE),
    ("ridge_scale", RidgelinePlot, GROUPS),
    ("inner", RidgelinePlot, GROUPS),
    ("inner", ViolinPlot, GROUPS),
    ("mark", RadialChart, BARS),
    ("direction", RadialChart, BARS),
    ("levels", ContourChart, GRID),
    ("reduce", HexbinChart, POINTS),
    ("week_start", CalendarHeatmap, CALENDAR),
    ("period", GanttChart, TASKS),
    ("value_kind", GanttChart, TASKS),
    ("sort_by", GanttChart, TASKS),
    ("value_kind", DumbbellChart, RANGES),
    ("sort_by", DumbbellChart, RANGES),
    ("connector_style", DumbbellChart, RANGES),
    ("layout", NetworkChart, EDGES),
    ("label_position", NetworkChart, EDGES),
    ("resolution", BasemapChart, "land"),
    ("diagonal", ScatterMatrix, COLUMNS),
]

SHAPE = r"^Invalid `{}` value 'bogus'\. Must be one of \("


class TestFrontsCheckConstantDomains(unittest.TestCase):
    def setUp(self):
        plt.close("all")

    def test_a_bad_value_raises_before_any_figure(self):
        for name, front, data in CASES:
            with self.subTest(front=front.__name__, parameter=name):
                with mock.patch.object(plot_engine, "render_chart") as render_chart:
                    with self.assertRaisesRegex(
                        ValueError, SHAPE.format(re.escape(name))
                    ):
                        # a sort key alone raises before its domain is read
                        extra = {"sort": "ascending"} if name == "sort_by" else {}
                        front(data, **{name: "bogus"}, **extra)
                render_chart.assert_not_called()
                self.assertEqual(plt.get_fignums(), [])

    def test_basemap_features_are_checked_element_wise(self):
        with self.assertRaisesRegex(ValueError, SHAPE.format(r"data\[1\]")):
            BasemapChart(["land", "bogus"])

    def test_dumbbell_markers_are_checked_element_wise(self):
        with self.assertRaisesRegex(ValueError, SHAPE.format(r"marker\[0\]")):
            DumbbellChart(RANGES, marker=("bogus", "o"))

    def test_a_per_chart_list_names_the_bad_element(self):
        with self.assertRaisesRegex(ValueError, SHAPE.format(r"emphasis\[1\]")):
            LineChart([LINE, LINE], emphasis=["highlight", "bogus"])

    def test_a_raw_string_is_the_member(self):
        a = BarChart(BARS, orientation="horizontal")
        b = BarChart(BARS, orientation=ORIENTATION.HORIZONTAL)
        self.assertEqual(
            [t.get_text() for t in a.axes[0].get_yticklabels()],
            [t.get_text() for t in b.axes[0].get_yticklabels()],
        )

    def test_other_types_the_parameter_takes_pass(self):
        LineChart(LINE, show_grid=False, figsize=(3.0, 2.0))
        ViolinPlot(GROUPS, bandwidth=0.5)
        BarChart(BARS, value_format=lambda v: f"{v} km", show_values=True)

    def test_a_bandwidth_of_another_type_raises_at_the_front(self):
        for front in (ViolinPlot, RidgelinePlot):
            with self.subTest(front=front.__name__):
                with self.assertRaisesRegex(
                    ValueError, r"Invalid `bandwidth` value \[1\]"
                ):
                    front(GROUPS, bandwidth=[1])

    def test_bar_mode_stacked_raises_without_a_warning(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaisesRegex(
                ValueError, r"^Invalid `bar_mode` value 'stacked'\."
            ):
                BarChart(BARS, bar_mode="stacked")

    def test_panel_checks_an_item_emphasis(self):
        with self.assertRaisesRegex(ValueError, SHAPE.format("emphasis")):
            Panel([{"figure": LineChart(LINE), "emphasis": "bogus"}])

    def test_panel_checks_its_constant_parameters(self):
        figure = LineChart(LINE)
        for name in ("scalex", "scaley", "scaley_right", "bar_mode", "show_grid"):
            with self.subTest(parameter=name):
                with self.assertRaisesRegex(ValueError, SHAPE.format(name)):
                    Panel([figure], **{name: "bogus"})


if __name__ == "__main__":
    unittest.main()
