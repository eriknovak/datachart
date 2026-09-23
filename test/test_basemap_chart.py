"""Tests for the basemap chart: features, geometry, draw order, composition,
and the geographic aspect every chart takes."""

import io
import json
import math
import os
import tempfile
import unittest
import warnings
from unittest import mock

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import PathPatch

from datachart.charts import BasemapChart, HexbinChart, LineChart, ScatterChart
from datachart.config import config
from datachart.constants import (
    ASPECT_RATIO,
    BASEMAP_FEATURE,
    BASEMAP_RESOLUTION,
    DRAW_POSITION,
    THEME,
)
from datachart.utils import Grid, Panel
from datachart.utils._internal import basemap
from datachart.utils._internal.basemap import (
    load_basemap,
    load_country_codes,
    load_outlines,
)
from datachart.utils._internal.layers import DRAW_ZORDER

# a square island with a square lake, and a line across it
ISLAND = {
    "lon": [0, 4, 4, 0, np.nan, 1, 1, 2, 2],
    "lat": [0, 0, 4, 4, np.nan, 1, 2, 2, 1],
    "feature": "land",
}
ROAD = {"lon": [0, 4], "lat": [2, 2], "feature": "coastline"}


def points():
    return [{"x": 20.0, "y": 38.0}, {"x": 30.0, "y": 40.0}]


def lines(figure):
    return [c for c in figure.axes[0].collections if isinstance(c, LineCollection)]


def fills(figure):
    return [p for p in figure.axes[0].patches if isinstance(p, PathPatch)]


def countries(figure):
    (collection,) = [
        c for c in figure.axes[0].collections if isinstance(c, PatchCollection)
    ]
    return collection


def pixel(figure, x, y):
    """The RGB color drawn at data point (x, y), from 0 to 1."""

    figure.canvas.draw()
    pixels = np.asarray(figure.canvas.buffer_rgba())
    px, py = figure.axes[0].transData.transform((x, y))
    return pixels[int(pixels.shape[0] - py), int(px), :3] / 255


EU = (
    "AUT BEL BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN IRL ITA LVA LTU LUX "
    "MLT NLD POL PRT ROU SVK SVN ESP SWE"
).split()


class TestBundledData(unittest.TestCase):
    def test_every_feature_loads_as_lon_lat_rows(self):
        for feature in ("coastline", "land", "borders", "lakes"):
            outlines = load_basemap(feature)
            self.assertEqual(outlines.ndim, 2)
            self.assertEqual(outlines.shape[1], 2)
            finite = outlines[np.isfinite(outlines).all(axis=1)]
            self.assertTrue((np.abs(finite[:, 0]) <= 180).all())
            self.assertTrue((np.abs(finite[:, 1]) <= 90).all())
            # several outlines, separated by NaN rows
            self.assertGreater(np.isnan(outlines[:, 0]).sum(), 1)


# a GeoJSON coastline of two lines, standing in for a Natural Earth download
COAST_JSON = json.dumps(
    {
        "type": "FeatureCollection",
        "features": [
            {"geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]}},
            {
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [[[2, 2], [3, 3]], [[4, 4], [5, 5]]],
                }
            },
        ],
    }
).encode()


class TestCountries(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_bundled_codes_label_every_ring(self):
        codes = load_country_codes()
        rows = load_basemap("countries")
        rings = np.isnan(rows[:, 0]).sum() + 1
        self.assertEqual(len(codes), rings)
        self.assertIn("SVN", codes)
        # Natural Earth's ISO code is -99 for France; the admin code is not
        self.assertIn("FRA", codes)

    def test_countries_fill_in_the_land_color(self):
        collection = countries(BasemapChart("countries"))
        land = matplotlib.colors.to_rgba(config["plot_basemap_land_color"])
        faces = collection.get_facecolors()
        self.assertEqual(len(faces), len(set(load_country_codes())))
        np.testing.assert_allclose(faces, np.tile(land, (len(faces), 1)))

    def test_highlight_colors_the_listed_countries(self):
        figure = BasemapChart(
            [BASEMAP_FEATURE.COUNTRIES, BASEMAP_FEATURE.BORDERS],
            highlight=["svn", "AUT"],
            xmin=5,
            xmax=25,
            ymin=40,
            ymax=52,
        )
        highlight = matplotlib.colors.to_rgb(config["plot_basemap_highlight_color"])
        land = matplotlib.colors.to_rgb(config["plot_basemap_land_color"])
        # Ljubljana and Vienna against Zagreb and Munich
        for lon, lat, color in (
            (14.5, 46.05, highlight),
            (16.2, 48.1, highlight),
            (16.0, 45.6, land),
            (11.6, 48.1, land),
        ):
            np.testing.assert_allclose(pixel(figure, lon, lat), color, atol=0.03)

    def test_an_enclave_is_not_cancelled_by_its_host(self):
        figure = BasemapChart(
            "countries", highlight="LSO", xmin=24, xmax=32, ymin=-32, ymax=-26
        )
        highlight = matplotlib.colors.to_rgb(config["plot_basemap_highlight_color"])
        land = matplotlib.colors.to_rgb(config["plot_basemap_land_color"])
        np.testing.assert_allclose(pixel(figure, 28.3, -29.5), highlight, atol=0.03)
        np.testing.assert_allclose(pixel(figure, 25.5, -28.0), land, atol=0.03)

    def test_a_code_missing_at_the_scale_warns(self):
        with self.assertWarnsRegex(UserWarning, "MLT"):
            BasemapChart("countries", highlight=EU)

    def test_known_codes_do_not_warn(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            BasemapChart("countries", highlight=["SVN", "FRA"])

    def test_highlight_needs_the_countries_feature(self):
        with self.assertRaisesRegex(ValueError, "countries"):
            BasemapChart(highlight=["SVN"])

    def test_malformed_code_raises(self):
        for bad in (["Slovenia"], [5], ["SV"]):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, "highlight"):
                    BasemapChart("countries", highlight=bad)

    def test_geometry_takes_no_countries(self):
        with self.assertRaisesRegex(ValueError, "countries"):
            BasemapChart(
                geometry={"lon": [0, 1, 1], "lat": [0, 0, 1], "feature": "countries"}
            )

    def test_highlight_with_geometry_raises(self):
        with self.assertRaisesRegex(ValueError, "highlight"):
            BasemapChart(geometry=ROAD, highlight=["SVN"])


class TestDownloadedResolutions(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        env = mock.patch.dict(os.environ, {"DATACHART_CACHE_DIR": self.folder.name})
        env.start()
        self.addCleanup(env.stop)
        self.addCleanup(self.folder.cleanup)
        load_outlines.cache_clear()
        self.addCleanup(load_outlines.cache_clear)

    def tearDown(self):
        plt.close("all")

    def urlopen(self, **kwargs):
        return mock.patch.object(basemap.urllib.request, "urlopen", **kwargs)

    def test_bundled_resolution_never_downloads(self):
        with self.urlopen(side_effect=AssertionError("network")):
            load_basemap("coastline", BASEMAP_RESOLUTION.LOW)
            BasemapChart()

    def test_finer_resolution_downloads_once_into_the_cache(self):
        with self.urlopen(return_value=io.BytesIO(COAST_JSON)) as urlopen:
            rows = load_basemap("coastline", BASEMAP_RESOLUTION.MEDIUM)
        self.assertIn("ne_50m_coastline", urlopen.call_args[0][0])
        self.assertEqual(np.isnan(rows[:, 0]).sum(), 2)
        self.assertEqual(len(os.listdir(self.folder.name)), 1)

        load_outlines.cache_clear()
        with self.urlopen(side_effect=AssertionError("network")):
            cached = load_basemap("coastline", BASEMAP_RESOLUTION.MEDIUM)
        np.testing.assert_array_equal(cached, rows)

    def test_front_takes_the_resolution(self):
        with self.urlopen(return_value=io.BytesIO(COAST_JSON)) as urlopen:
            figure = BasemapChart("coastline", resolution=BASEMAP_RESOLUTION.HIGH)
        self.assertIn("ne_10m_coastline", urlopen.call_args[0][0])
        self.assertEqual(figure.axes[0].get_xlim(), (0.0, 5.0))

    def test_failed_download_raises_one_error(self):
        with self.urlopen(side_effect=OSError("offline")):
            with self.assertRaisesRegex(RuntimeError, "offline"):
                BasemapChart("coastline", resolution=BASEMAP_RESOLUTION.MEDIUM)
        self.assertEqual(os.listdir(self.folder.name), [])

    def test_downloaded_countries_keep_their_codes(self):
        collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "properties": {"ADM0_A3": code},
                    "geometry": {"type": "Polygon", "coordinates": [ring]},
                }
                for code, ring in (
                    ("AAA", [[0, 0], [1, 0], [1, 1], [0, 0]]),
                    ("BBB", [[2, 0], [3, 0], [3, 1], [2, 0]]),
                )
            ],
        }
        body = io.BytesIO(json.dumps(collection).encode())
        with self.urlopen(return_value=body) as urlopen:
            codes = load_country_codes(BASEMAP_RESOLUTION.MEDIUM)
        self.assertIn("ne_50m_admin_0_countries", urlopen.call_args[0][0])
        self.assertEqual(list(codes), ["AAA", "BBB"])

    def test_unknown_resolution_raises(self):
        with self.assertRaisesRegex(ValueError, "resolution"):
            BasemapChart(resolution="1m")

    def test_resolution_with_geometry_raises(self):
        with self.assertRaisesRegex(ValueError, "resolution"):
            BasemapChart(geometry=ROAD, resolution=BASEMAP_RESOLUTION.MEDIUM)


class TestBasemapFeatures(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_default_draws_coastline_and_land(self):
        figure = BasemapChart()
        self.assertEqual(len(lines(figure)), 1)
        self.assertEqual(len(fills(figure)), 1)

    def test_default_view_is_the_world(self):
        ax = BasemapChart().axes[0]
        self.assertAlmostEqual(ax.get_xlim()[0], -180, delta=1)
        self.assertAlmostEqual(ax.get_xlim()[1], 180, delta=1)
        self.assertGreaterEqual(ax.get_ylim()[0], -90)
        self.assertLessEqual(ax.get_ylim()[1], 90)

    def test_borders_and_lakes(self):
        figure = BasemapChart(
            [BASEMAP_FEATURE.BORDERS, BASEMAP_FEATURE.LAKES, BASEMAP_FEATURE.LAND]
        )
        self.assertEqual(len(lines(figure)), 1)
        self.assertEqual(len(fills(figure)), 2)

    def test_single_feature_string(self):
        figure = BasemapChart("coastline")
        self.assertEqual(len(lines(figure)), 1)
        self.assertEqual(len(fills(figure)), 0)

    def test_theme_styles(self):
        figure = BasemapChart([BASEMAP_FEATURE.COASTLINE, BASEMAP_FEATURE.LAND])
        (coast,) = lines(figure)
        (land,) = fills(figure)
        np.testing.assert_allclose(
            coast.get_colors()[0],
            matplotlib.colors.to_rgba(config["plot_basemap_coastline_color"]),
        )
        self.assertAlmostEqual(
            coast.get_linewidths()[0], config["plot_basemap_coastline_width"]
        )
        np.testing.assert_allclose(
            land.get_facecolor(),
            matplotlib.colors.to_rgba(config["plot_basemap_land_color"]),
        )

    def test_lakes_take_the_axes_ground_by_default(self):
        (lakes,) = fills(BasemapChart(BASEMAP_FEATURE.LAKES))
        np.testing.assert_allclose(
            lakes.get_facecolor(), matplotlib.colors.to_rgba("#FFFFFF")
        )

    def test_style_override(self):
        figure = BasemapChart(
            "coastline", style={"plot_basemap_coastline_color": "#FF0000"}
        )
        np.testing.assert_allclose(lines(figure)[0].get_colors()[0], (1, 0, 0, 1))

    def test_dark_theme_keeps_the_land_dark(self):
        config.set_theme(THEME.DARK)
        try:
            land = matplotlib.colors.to_rgb(config["plot_basemap_land_color"])
            self.assertLess(sum(land) / 3, 0.5)
        finally:
            config.set_theme(THEME.DEFAULT)

    def test_unknown_feature_raises(self):
        with self.assertRaisesRegex(ValueError, "rivers"):
            BasemapChart("rivers")

    def test_empty_features_raise(self):
        with self.assertRaisesRegex(ValueError, "feature"):
            BasemapChart([])


class TestBasemapGeometry(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_caller_geometry_replaces_the_bundle(self):
        figure = BasemapChart(geometry=[ISLAND, ROAD])
        self.assertEqual(len(fills(figure)), 1)
        self.assertEqual(len(lines(figure)), 1)
        ax = figure.axes[0]
        self.assertEqual(ax.get_xlim(), (0.0, 4.0))
        self.assertEqual(ax.get_ylim(), (0.0, 4.0))

    def test_single_geometry_dict(self):
        figure = BasemapChart(geometry=ROAD)
        self.assertEqual(len(lines(figure)), 1)

    def test_feature_defaults_to_coastline(self):
        figure = BasemapChart(geometry={"lon": [0, 1], "lat": [0, 1]})
        self.assertEqual(len(lines(figure)), 1)

    def test_hole_is_left_unfilled(self):
        figure = BasemapChart(geometry=ISLAND)
        figure.canvas.draw()
        pixels = np.asarray(figure.canvas.buffer_rgba())
        ax = figure.axes[0]

        def color(x, y):
            px, py = ax.transData.transform((x, y))
            return pixels[int(pixels.shape[0] - py), int(px), :3]

        land = matplotlib.colors.to_rgb(config["plot_basemap_land_color"])
        np.testing.assert_allclose(color(3.3, 3.3) / 255, land, atol=0.02)
        np.testing.assert_allclose(color(1.3, 1.7) / 255, (1, 1, 1), atol=0.02)

    def test_features_and_geometry_together_raise(self):
        with self.assertRaisesRegex(ValueError, "geometry"):
            BasemapChart("land", geometry=ROAD)

    def test_malformed_geometry_raises(self):
        for bad in (
            {"lon": [0, 1]},
            {"lon": [0, 1], "lat": [0]},
            {"lon": ["a", "b"], "lat": [0, 1]},
            {"lon": [0, 1], "lat": [0, 1], "feature": "rivers"},
            [ROAD, "coast"],
            {"lon": [], "lat": []},
            {"lon": [0, 1, 2], "lat": [np.nan] * 3},
            {"lon": [0, 1], "lat": [0, 1], "feature": "land"},
        ):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, "geometry"):
                    BasemapChart(geometry=bad)


class TestBasemapComposition(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_below_by_default(self):
        (coast,) = lines(BasemapChart("coastline"))
        self.assertEqual(coast.get_zorder(), DRAW_ZORDER["below"])

    def test_above(self):
        figure = BasemapChart("coastline", position=DRAW_POSITION.ABOVE)
        self.assertEqual(lines(figure)[0].get_zorder(), DRAW_ZORDER["above"])

    def test_invalid_position_raises(self):
        with self.assertRaisesRegex(ValueError, "position"):
            BasemapChart(position="middle")

    def test_under_marks_whatever_the_panel_order(self):
        for order in (0, 1):
            figures = [BasemapChart(), ScatterChart(points())]
            figure = Panel(figures if order == 0 else figures[::-1])
            ax = figure.axes[0]
            land = [p for p in ax.patches if isinstance(p, PathPatch)][0]
            marks = [c for c in ax.collections if not isinstance(c, LineCollection)]
            self.assertLess(land.get_zorder(), marks[0].get_zorder())

    def test_composed_leaves_the_limits_to_the_data(self):
        alone = ScatterChart(points()).axes[0]
        composed = Panel([BasemapChart(), ScatterChart(points())]).axes[0]
        self.assertEqual(composed.get_xlim(), alone.get_xlim())
        self.assertEqual(composed.get_ylim(), alone.get_ylim())

    def test_takes_no_cycle_color(self):
        alone = ScatterChart(points()).axes[0].collections[0].get_facecolor()
        composed = Panel([BasemapChart(), ScatterChart(points())]).axes[0]
        marks = [c for c in composed.collections if not isinstance(c, LineCollection)]
        np.testing.assert_allclose(marks[0].get_facecolor(), alone)

    def test_no_legend_entry(self):
        figure = Panel(
            [BasemapChart(), ScatterChart(points(), subtitle="Stations")],
            show_legend=True,
        )
        texts = [t.get_text() for t in figure.axes[0].get_legend().get_texts()]
        self.assertEqual(texts, ["Stations"])

    def test_twin_axes_leave_the_basemap_on_the_primary(self):
        line = LineChart([{"x": 20, "y": 1000}, {"x": 30, "y": 3000}])
        figure = Panel([BasemapChart(), ScatterChart(points()), line])
        self.assertTrue(lines(figure) or fills(figure))

    def test_in_a_grid_under_a_hexbin(self):
        rng = np.random.default_rng(0)
        hexbin = HexbinChart(
            {
                "x": rng.uniform(20, 40, 200).tolist(),
                "y": rng.uniform(34, 42, 200).tolist(),
            }
        )
        cell = Panel([BasemapChart(), hexbin])
        figure = Grid([[cell, ScatterChart(points())]])
        self.assertTrue(any(isinstance(p, PathPatch) for p in figure.axes[0].patches))


class TestGeographicAspect(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_chart_takes_the_cosine_of_the_mid_latitude(self):
        figure = ScatterChart(
            points(), aspect_ratio=ASPECT_RATIO.GEOGRAPHIC, ymin=30, ymax=50
        )
        ax = figure.axes[0]
        self.assertAlmostEqual(ax.get_aspect(), 1 / math.cos(math.radians(40)))

    def test_panel_setting(self):
        figure = Panel(
            [BasemapChart(), ScatterChart(points())],
            aspect_ratio=ASPECT_RATIO.GEOGRAPHIC,
            ymin=0,
            ymax=60,
        )
        ax = figure.axes[0]
        self.assertAlmostEqual(ax.get_aspect(), 1 / math.cos(math.radians(30)))

    def test_default_stays_auto(self):
        self.assertEqual(ScatterChart(points()).axes[0].get_aspect(), "auto")

    def test_outside_the_latitudes_raises(self):
        data = [{"x": 0, "y": 0}, {"x": 1, "y": 500}]
        with self.assertRaisesRegex(ValueError, "geographic"):
            ScatterChart(data, aspect_ratio=ASPECT_RATIO.GEOGRAPHIC)


if __name__ == "__main__":
    unittest.main()
