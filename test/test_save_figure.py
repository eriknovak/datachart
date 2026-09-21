"""Tests for save_figure's path handling and multi-format writes (ADR 0039)."""

import os
import tempfile
import unittest

import matplotlib

matplotlib.use("Agg", force=True)

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from datachart.charts import LineChart
from datachart.config import config
from datachart.constants import FIG_FORMAT, THEME
from datachart.utils import save_figure


class TestSaveFigure(unittest.TestCase):
    def setUp(self):
        self.figure = LineChart(data=[{"x": i, "y": i * 2} for i in range(5)])
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.addCleanup(plt.close, "all")

    def path(self, name: str) -> str:
        return os.path.join(self.tmpdir.name, name)

    def test_several_formats_write_one_file_each(self):
        stem = self.path("fig1")
        paths = save_figure(self.figure, stem, format=[FIG_FORMAT.PDF, FIG_FORMAT.PNG])
        self.assertEqual(paths, [f"{stem}.pdf", f"{stem}.png"])
        for path in paths:
            self.assertTrue(os.path.isfile(path))

    def test_known_extension_is_stripped_from_the_stem(self):
        paths = save_figure(self.figure, self.path("fig1.png"), format=[FIG_FORMAT.PDF])
        self.assertEqual(paths, [self.path("fig1.pdf")])
        self.assertTrue(os.path.isfile(paths[0]))

    def test_dotted_name_keeps_every_part_of_itself(self):
        paths = save_figure(self.figure, self.path("fig.v2"), format=[FIG_FORMAT.PDF])
        self.assertEqual(paths, [self.path("fig.v2.pdf")])
        self.assertTrue(os.path.isfile(paths[0]))

    def test_repeated_format_writes_once_per_entry(self):
        stem = self.path("fig1")
        paths = save_figure(self.figure, stem, format=[FIG_FORMAT.PNG, FIG_FORMAT.PNG])
        self.assertEqual(paths, [f"{stem}.png", f"{stem}.png"])

    def test_single_format_uses_the_path_verbatim(self):
        path = self.path("fig1.png")
        self.assertEqual(save_figure(self.figure, path, format=FIG_FORMAT.PNG), [path])
        self.assertTrue(os.path.isfile(path))

    def test_format_inferred_from_the_extension(self):
        path = self.path("fig1.png")
        self.assertEqual(save_figure(self.figure, path), [path])
        self.assertTrue(os.path.isfile(path))

    def test_empty_format_list_raises(self):
        with self.assertRaises(ValueError) as ctx:
            save_figure(self.figure, self.path("fig1"), format=[])
        self.assertIn("format", str(ctx.exception))


class TestSaveFigureKeepsTheThemeGround(unittest.TestCase):
    """A dark figure carries its face into the file (ADR 0058)."""

    def setUp(self):
        config.set_theme(THEME.DARK)
        self.figure = LineChart(data=[{"x": i, "y": i * 2} for i in range(5)])
        self.face = mcolors.to_rgba(config["figure_facecolor"])
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.addCleanup(plt.close, "all")
        self.addCleanup(config.set_theme, THEME.DEFAULT)

    def path(self, name: str) -> str:
        return os.path.join(self.tmpdir.name, name)

    def corner(self, path):
        return tuple(plt.imread(path)[0][0])

    def test_png_keeps_the_dark_ground(self):
        path = self.path("dark.png")
        save_figure(self.figure, path, dpi=72)
        self.assertEqual(
            [round(c, 2) for c in self.corner(path)],
            [round(c, 2) for c in self.face],
        )

    def test_svg_keeps_the_dark_ground(self):
        path = self.path("dark.svg")
        save_figure(self.figure, path, format=FIG_FORMAT.SVG)
        with open(path) as handle:
            markup = handle.read()
        self.assertIn(config["figure_facecolor"].lower(), markup.lower())

    def test_transparent_drops_the_ground(self):
        path = self.path("clear.png")
        save_figure(self.figure, path, dpi=72, transparent=True)
        self.assertEqual(self.corner(path)[3], 0.0)


if __name__ == "__main__":
    unittest.main()
