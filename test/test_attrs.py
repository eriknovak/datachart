import unittest

from datachart.config import config as _config
from datachart.utils.attrs import (
    get_attr_value,
    create_config_dict,
    get_subplot_config,
    get_text_style,
    get_line_style,
    get_bar_style,
    get_hist_style,
    get_area_style,
    get_grid_style,
    get_legend_style,
)


class TestAttrs(unittest.TestCase):
    def test_get_attr_value(self):
        test = get_attr_value("test", {}, "test")
        self.assertEqual(test, "test")

        test = get_attr_value("test", {"test": "test2"}, "test")
        self.assertEqual(test, "test2")

        test = get_attr_value("test", {}, {"test": "test3"})
        self.assertEqual(test, "test3")

    def test_create_config_dict(self):
        config = create_config_dict(
            {"plot.line.color": "#FF0000"},
            [("color", "plot.line.color"), ("alpha", "plot.line.alpha")],
        )
        self.assertEqual(config["color"], "#FF0000")
        self.assertEqual(config["alpha"], 1.0)

    def test_get_subplot_config(self):
        # no subplot
        config = get_subplot_config("linechart", False)
        self.assertEqual(config["nrows"], 1)
        self.assertEqual(config["ncols"], 1)

        # with subplot and default number of charts
        config = get_subplot_config("linechart", True)
        self.assertEqual(config["nrows"], 1)
        self.assertEqual(config["ncols"], 1)

        # with two subplots
        config = get_subplot_config("linechart", True, 2)
        self.assertEqual(config["nrows"], 2)
        self.assertEqual(config["ncols"], 1)

        # with four subplots in three columns
        config = get_subplot_config("linechart", True, 4, 3)
        self.assertEqual(config["nrows"], 2)
        self.assertEqual(config["ncols"], 3)

    def test_get_text_style(self):
        for key in ["general", "title", "subtitle", "xlabel", "ylabel"]:
            config = get_text_style(key)
            self.assertEqual(config["fontsize"], _config[f"font.{key}.size"])
            self.assertEqual(config["fontweight"], _config[f"font.{key}.weight"])
            self.assertEqual(config["color"], _config[f"font.{key}.color"])
            self.assertEqual(config["style"], _config[f"font.{key}.style"])
            self.assertEqual(config["family"], "sans-serif")

    def test_get_line_style(self):
        config = get_line_style({"plot.line.color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot.line.alpha"])
        self.assertEqual(config["linewidth"], _config["plot.line.width"])
        self.assertEqual(config["linestyle"], _config["plot.line.style"])
        self.assertEqual("marker" not in config, True)
        self.assertEqual(config["drawstyle"], _config["plot.line.drawstyle"])
        self.assertEqual(config["zorder"], _config["plot.line.zorder"])

    def test_get_bar_style(self):
        config = get_bar_style({"plot.bar.color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot.bar.alpha"])
        self.assertEqual(config["width"], _config["plot.bar.width"])
        self.assertEqual("hatch" not in config, True)
        self.assertEqual(config["linewidth"], _config["plot.bar.edge.width"])
        self.assertEqual(config["edgecolor"], _config["plot.bar.edge.color"])
        self.assertEqual(config["ecolor"], _config["plot.bar.error.color"])
        self.assertEqual(config["zorder"], _config["plot.bar.zorder"])

        config = get_bar_style({"plot.bar.color": "#FF0000"}, is_horizontal=True)
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot.bar.alpha"])
        self.assertEqual(config["height"], _config["plot.bar.width"])
        self.assertEqual("hatch" not in config, True)
        self.assertEqual(config["linewidth"], _config["plot.bar.edge.width"])
        self.assertEqual(config["edgecolor"], _config["plot.bar.edge.color"])
        self.assertEqual(config["ecolor"], _config["plot.bar.error.color"])
        self.assertEqual(config["zorder"], _config["plot.bar.zorder"])

    def test_get_hist_style(self):
        config = get_hist_style({"plot.hist.color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot.hist.alpha"])
        self.assertEqual("fill" not in config, True)
        self.assertEqual("hatch" not in config, True)
        self.assertEqual(config["zorder"], _config["plot.hist.zorder"])
        self.assertEqual(config["histtype"], _config["plot.hist.type"])
        self.assertEqual(config["align"], _config["plot.hist.align"])
        self.assertEqual(config["linewidth"], _config["plot.hist.edge.width"])
        self.assertEqual(config["edgecolor"], _config["plot.hist.edge.color"])

    def test_get_area_style(self):
        config = get_area_style({"plot.area.color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot.area.alpha"])
        self.assertEqual(config["linewidth"], _config["plot.area.line.width"])
        self.assertEqual("hatch" not in config, True)
        self.assertEqual(config["zorder"], _config["plot.area.zorder"])

    def test_get_grid_style(self):
        config = get_grid_style({"plot.grid.color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot.grid.alpha"])
        self.assertEqual(config["linewidth"], _config["plot.grid.line.width"])
        self.assertEqual(config["linestyle"], _config["plot.grid.line.style"])
        self.assertEqual(config["zorder"], _config["plot.grid.zorder"])

    def test_get_legend_style(self):
        config = get_legend_style()
        self.assertEqual(config["shadow"], _config["plot.legend.shadow"])
        self.assertEqual(config["frameon"], _config["plot.legend.frameon"])
        self.assertEqual(config["fontsize"], _config["plot.legend.font.size"])
        self.assertEqual(config["alignment"], _config["plot.legend.alignment"])
        self.assertEqual(config["title_fontsize"], _config["plot.legend.title.size"])
        self.assertEqual(config["labelcolor"], _config["plot.legend.label.color"])


if __name__ == "__main__":
    unittest.main()
