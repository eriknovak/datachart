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

# =====================================
# Test Attributes
# =====================================

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
            {"plot_line_color": "#FF0000"},
            [("color", "plot_line_color"), ("alpha", "plot_line_alpha")],
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
            self.assertEqual(config["fontsize"], _config[f"font_{key}_size"])
            self.assertEqual(config["fontweight"], _config[f"font_{key}_weight"])
            self.assertEqual(config["color"], _config[f"font_{key}_color"])
            self.assertEqual(config["style"], _config[f"font_{key}_style"])
            self.assertEqual(config["family"], "sans-serif")

    def test_get_line_style(self):
        config = get_line_style({"plot_line_color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot_line_alpha"])
        self.assertEqual(config["linewidth"], _config["plot_line_width"])
        self.assertEqual(config["linestyle"], _config["plot_line_style"])
        self.assertEqual("marker" not in config, True)
        self.assertEqual(config["drawstyle"], _config["plot_line_drawstyle"])
        self.assertEqual(config["zorder"], _config["plot_line_zorder"])

    def test_get_bar_style(self):
        config = get_bar_style({"plot_bar_color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot_bar_alpha"])
        self.assertEqual(config["width"], _config["plot_bar_width"])
        self.assertEqual("hatch" not in config, True)
        self.assertEqual(config["linewidth"], _config["plot_bar_edge_width"])
        self.assertEqual(config["edgecolor"], _config["plot_bar_edge_color"])
        self.assertEqual(config["ecolor"], _config["plot_bar_error_color"])
        self.assertEqual(config["zorder"], _config["plot_bar_zorder"])

        config = get_bar_style({"plot_bar_color": "#FF0000"}, is_horizontal=True)
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot_bar_alpha"])
        self.assertEqual(config["height"], _config["plot_bar_width"])
        self.assertEqual("hatch" not in config, True)
        self.assertEqual(config["linewidth"], _config["plot_bar_edge_width"])
        self.assertEqual(config["edgecolor"], _config["plot_bar_edge_color"])
        self.assertEqual(config["ecolor"], _config["plot_bar_error_color"])
        self.assertEqual(config["zorder"], _config["plot_bar_zorder"])

    def test_get_hist_style(self):
        config = get_hist_style({"plot_hist_color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot_hist_alpha"])
        self.assertEqual("fill" not in config, True)
        self.assertEqual("hatch" not in config, True)
        self.assertEqual(config["zorder"], _config["plot_hist_zorder"])
        self.assertEqual(config["histtype"], _config["plot_hist_type"])
        self.assertEqual(config["align"], _config["plot_hist_align"])
        self.assertEqual(config["linewidth"], _config["plot_hist_edge_width"])
        self.assertEqual(config["edgecolor"], _config["plot_hist_edge_color"])

    def test_get_area_style(self):
        config = get_area_style({"plot_area_color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot_area_alpha"])
        self.assertEqual(config["linewidth"], _config["plot_area_linewidth"])
        self.assertEqual("hatch" not in config, True)
        self.assertEqual(config["zorder"], _config["plot_area_zorder"])

    def test_get_grid_style(self):
        config = get_grid_style({"plot_grid_color": "#FF0000"})
        self.assertEqual(config["color"], "#FF0000")
        # default line style checkup
        self.assertEqual(config["alpha"], _config["plot_grid_alpha"])
        self.assertEqual(config["linewidth"], _config["plot_grid_linewidth"])
        self.assertEqual(config["linestyle"], _config["plot_grid_linestyle"])
        self.assertEqual(config["zorder"], _config["plot_grid_zorder"])

    def test_get_legend_style(self):
        config = get_legend_style()
        self.assertEqual(config["shadow"], _config["plot_legend_shadow"])
        self.assertEqual(config["frameon"], _config["plot_legend_frameon"])
        self.assertEqual(config["fontsize"], _config["plot_legend_font_size"])
        self.assertEqual(config["alignment"], _config["plot_legend_alignment"])
        self.assertEqual(config["title_fontsize"], _config["plot_legend_title_size"])
        self.assertEqual(config["labelcolor"], _config["plot_legend_label_color"])


if __name__ == "__main__":
    unittest.main()
