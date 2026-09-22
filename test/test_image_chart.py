"""Tests for the image chart: inputs, extent, draw order, and composition."""

import os
import tempfile
import unittest

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.image import AxesImage
from PIL import Image as PILImage

from datachart.charts import ImageChart, ScatterChart, LineChart
from datachart.config import config
from datachart.constants import IMAGE_POSITION, THEME
from datachart.config.configuration import THEMES
from datachart.utils import Panel, Grid
from datachart.utils._internal.layers import IMAGE_ZORDER, REF_LINE_ZORDER

EXTENT = (0.0, 10.0, -5.0, 5.0)


def rgb(height=4, width=6):
    rng = np.random.default_rng(0)
    return rng.integers(0, 255, (height, width, 3), dtype=np.uint8)


def field(height=4, width=6):
    return np.arange(height * width, dtype=float).reshape(height, width)


def images(figure):
    return [a for ax in figure.axes for a in ax.get_images()]


def points():
    return [{"x": 2.0, "y": 1.0}, {"x": 8.0, "y": -2.0}]


class TestImageInputs(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_rgb_array(self):
        figure = ImageChart({"image": rgb(), "extent": EXTENT})
        (image,) = images(figure)
        self.assertIsInstance(image, AxesImage)
        self.assertEqual(image.get_array().shape, (4, 6, 3))
        self.assertEqual(tuple(image.get_extent()), EXTENT)

    def test_rgba_array(self):
        rgba = np.zeros((3, 3, 4), dtype=np.uint8)
        figure = ImageChart({"image": rgba, "extent": EXTENT})
        self.assertEqual(images(figure)[0].get_array().shape, (3, 3, 4))

    def test_pil_image(self):
        picture = PILImage.fromarray(rgb())
        figure = ImageChart({"image": picture, "extent": EXTENT})
        self.assertEqual(images(figure)[0].get_array().shape, (4, 6, 3))

    def test_path(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "plan.png")
            PILImage.fromarray(rgb()).save(path)
            for source in (path, __import__("pathlib").Path(path)):
                figure = ImageChart({"image": source, "extent": EXTENT})
                self.assertEqual(images(figure)[0].get_array().shape, (4, 6, 3))

    def test_palette_image_reads_as_color(self):
        picture = PILImage.fromarray(rgb()).convert("P")
        figure = ImageChart({"image": picture, "extent": EXTENT})
        self.assertEqual(images(figure)[0].get_array().ndim, 3)

    def test_field_reads_through_the_theme_colormap(self):
        figure = ImageChart({"image": field(), "extent": EXTENT})
        (image,) = images(figure)
        self.assertEqual(image.get_cmap().name, config["plot_image_cmap"])

    def test_field_cmap_and_range(self):
        figure = ImageChart(
            {"image": field(), "extent": EXTENT},
            style={"plot_image_cmap": "viridis"},
            vmin=-10,
            vmax=40,
        )
        (image,) = images(figure)
        self.assertEqual(image.get_cmap().name, "viridis")
        self.assertEqual(image.get_clim(), (-10, 40))

    def test_first_row_is_the_top_edge(self):
        figure = ImageChart({"image": field(), "extent": EXTENT})
        self.assertEqual(images(figure)[0].origin, "upper")

    def test_unreadable_image_raises(self):
        for bad in (None, 5, np.zeros(4), np.zeros((2, 2, 5)), [[1, 2], [3]]):
            with self.assertRaises(ValueError):
                ImageChart({"image": bad, "extent": EXTENT})

    def test_missing_image_raises(self):
        with self.assertRaises(ValueError):
            ImageChart({"extent": EXTENT})


class TestImageExtent(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_extent_required(self):
        with self.assertRaisesRegex(ValueError, "extent"):
            ImageChart({"image": rgb()})

    def test_extent_four_numbers(self):
        for bad in ((0, 1, 2), (0, 1, 2, 3, 4), "0123", (0, 1, "a", 2)):
            with self.assertRaisesRegex(ValueError, "extent"):
                ImageChart({"image": rgb(), "extent": bad})

    def test_extent_finite(self):
        for bad in ((0, np.inf, 0, 1), (0, 1, np.nan, 1)):
            with self.assertRaisesRegex(ValueError, "finite"):
                ImageChart({"image": rgb(), "extent": bad})

    def test_extent_not_degenerate(self):
        with self.assertRaisesRegex(ValueError, "xmin"):
            ImageChart({"image": rgb(), "extent": (1, 1, 0, 1)})
        with self.assertRaisesRegex(ValueError, "ymin"):
            ImageChart({"image": rgb(), "extent": (0, 1, 2, 2)})

    def test_axes_hug_the_extent(self):
        figure = ImageChart({"image": rgb(), "extent": EXTENT})
        ax = figure.axes[0]
        self.assertEqual(ax.get_xlim(), (0.0, 10.0))
        self.assertEqual(ax.get_ylim(), (-5.0, 5.0))

    def test_extent_widens_the_panel_limits(self):
        figure = Panel(
            [
                ImageChart({"image": rgb(), "extent": (-20.0, 20.0, -10.0, 10.0)}),
                ScatterChart(points()),
            ]
        )
        xlo, xhi = figure.axes[0].get_xlim()
        ylo, yhi = figure.axes[0].get_ylim()
        self.assertLessEqual(xlo, -20.0)
        self.assertGreaterEqual(xhi, 20.0)
        self.assertLessEqual(ylo, -10.0)
        self.assertGreaterEqual(yhi, 10.0)

    def test_image_never_takes_the_twin_axis(self):
        figure = Panel(
            [
                ImageChart({"image": rgb(), "extent": (0.0, 10.0, -500.0, 500.0)}),
                ScatterChart(points()),
            ]
        )
        self.assertEqual(len(figure.axes), 1)

    def test_limits_narrow_it_back(self):
        figure = ImageChart({"image": rgb(), "extent": EXTENT}, xmin=2, xmax=4)
        self.assertEqual(figure.axes[0].get_xlim(), (2.0, 4.0))

    def test_aspect_auto_by_default(self):
        figure = ImageChart({"image": rgb(), "extent": (0, 100, 0, 1)})
        self.assertEqual(figure.axes[0].get_aspect(), "auto")


class TestImageDrawOrder(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_below_sits_under_the_gridlines(self):
        figure = ImageChart({"image": rgb(), "extent": EXTENT}, show_grid="both")
        ax = figure.axes[0]
        self.assertEqual(images(figure)[0].get_zorder(), IMAGE_ZORDER["below"])
        self.assertLess(IMAGE_ZORDER["below"], ax.xaxis.get_zorder())

    def test_above_sits_over_the_marks_under_reference_lines(self):
        figure = ImageChart(
            {"image": rgb(), "extent": EXTENT}, position=IMAGE_POSITION.ABOVE
        )
        z = images(figure)[0].get_zorder()
        self.assertEqual(z, IMAGE_ZORDER["above"])
        self.assertGreater(z, config["plot_scatter_zorder"])
        self.assertLess(z, REF_LINE_ZORDER)

    def test_invalid_position_raises(self):
        with self.assertRaisesRegex(ValueError, "position"):
            ImageChart({"image": rgb(), "extent": EXTENT}, position="middle")

    def test_panel_order_does_not_decide(self):
        image = ImageChart({"image": rgb(), "extent": EXTENT})
        scatter = ScatterChart(points())
        for figures in ([image, scatter], [scatter, image]):
            figure = Panel(figures)
            ax = figure.axes[0]
            image_z = ax.get_images()[0].get_zorder()
            mark_z = max(c.get_zorder() for c in ax.collections)
            self.assertEqual(image_z, IMAGE_ZORDER["below"])
            self.assertLess(image_z, mark_z)

    def test_panel_order_keeps_the_limits(self):
        line = LineChart([{"x": x, "y": x} for x in range(10)])
        image = ImageChart({"image": rgb(), "extent": (2.0, 7.0, 2.0, 7.0)})
        limits = [
            (figure.axes[0].get_xlim(), figure.axes[0].get_ylim())
            for figure in (Panel([line, image]), Panel([image, line]))
        ]
        self.assertEqual(limits[0], limits[1])
        self.assertLessEqual(limits[0][0][0], 0.0)
        self.assertGreaterEqual(limits[0][0][1], 9.0)

    def test_panel_above(self):
        image = ImageChart(
            {"image": rgb(), "extent": EXTENT}, position=IMAGE_POSITION.ABOVE
        )
        figure = Panel([image, ScatterChart(points())])
        ax = figure.axes[0]
        image_z = ax.get_images()[0].get_zorder()
        self.assertGreater(image_z, max(c.get_zorder() for c in ax.collections))

    def test_explicit_z_order_wins(self):
        image = ImageChart({"image": rgb(), "extent": EXTENT})
        figure = Panel([{"figure": image, "z_order": 7}, ScatterChart(points())])
        self.assertEqual(figure.axes[0].get_images()[0].get_zorder(), 7)


class TestImageCarriesNoSeries(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_takes_no_cycle_color(self):
        alone = ScatterChart(points()).axes[0].collections[0].get_facecolor()
        figure = Panel(
            [ImageChart({"image": rgb(), "extent": EXTENT}), ScatterChart(points())]
        )
        composed = figure.axes[0].collections[0].get_facecolor()
        np.testing.assert_allclose(composed, alone)

    def test_no_legend_entry(self):
        figure = Panel(
            [
                ImageChart({"image": rgb(), "extent": EXTENT}, subtitle="Plan"),
                LineChart([{"x": 1, "y": 1}, {"x": 2, "y": 2}], subtitle="Route"),
            ],
            show_legend=True,
        )
        texts = [t.get_text() for t in figure.axes[0].get_legend().get_texts()]
        self.assertEqual(texts, ["Route"])

    def test_emphasis_not_supported(self):
        with self.assertRaises(TypeError):
            ImageChart({"image": rgb(), "extent": EXTENT}, emphasis="background")

    def test_panel_emphasis_leaves_the_image(self):
        image = ImageChart({"image": rgb(), "extent": EXTENT})
        figure = Panel([{"figure": image, "emphasis": "background"}])
        self.assertEqual(figure.axes[0].get_images()[0].get_alpha(), 1.0)


class TestImageStyle(unittest.TestCase):
    def tearDown(self):
        config.set_theme(THEME.DEFAULT)
        plt.close("all")

    def test_alpha_and_interpolation(self):
        figure = ImageChart(
            {"image": rgb(), "extent": EXTENT},
            style={"plot_image_alpha": 0.4, "plot_image_interpolation": "nearest"},
        )
        (image,) = images(figure)
        self.assertEqual(image.get_alpha(), 0.4)
        self.assertEqual(image.get_interpolation(), "nearest")

    def test_alpha_one_draws_opaque(self):
        (image,) = images(ImageChart({"image": rgb(), "extent": EXTENT}))
        self.assertIn(image.get_alpha(), (None, 1.0))

    def test_every_theme_sets_the_image_keys(self):
        keys = [
            "plot_image_alpha",
            "plot_image_cmap",
            "plot_image_interpolation",
            "plot_image_aspect",
        ]
        for theme in THEMES:
            config.set_theme(theme)
            for key in keys:
                self.assertIn(key, config.config, f"{theme} lacks {key}")


class TestImageCompose(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_metadata_type(self):
        figure = ImageChart({"image": rgb(), "extent": EXTENT})
        self.assertEqual(figure._chart_metadata["type"], "imagechart")

    def test_grid_carries_the_layer(self):
        panel = Panel(
            [ImageChart({"image": rgb(), "extent": EXTENT}), ScatterChart(points())]
        )
        figure = Grid([panel, ImageChart({"image": field(), "extent": EXTENT})])
        self.assertEqual(sum(len(ax.get_images()) for ax in figure.axes), 2)

    def test_subplots(self):
        figure = ImageChart(
            [
                {"image": rgb(), "extent": EXTENT},
                {"image": field(), "extent": (0, 1, 0, 1)},
            ],
            subplots=True,
        )
        drawn = [ax for ax in figure.axes if ax.get_images()]
        self.assertEqual(len(drawn), 2)


if __name__ == "__main__":
    unittest.main()
