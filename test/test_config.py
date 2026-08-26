import unittest

from datachart.config import config
from datachart.themes import DEFAULT_THEME

# =====================================
# Test Config
# =====================================


class TestConfig(unittest.TestCase):
    def test_initial_config(self):
        for key, val in DEFAULT_THEME.items():
            self.assertEqual(config[key], val)

    def test_update_config(self):
        updated_config = {"font_general_color": "#FFFFFF"}
        config.update_config(config=updated_config)
        for key, val in updated_config.items():
            self.assertEqual(config[key], val)

    def test_reset_config(self):
        config.reset_config()
        for key, val in DEFAULT_THEME.items():
            self.assertEqual(config[key], val)

    def test_register_theme(self):
        config.register_theme("custom", {**DEFAULT_THEME, "font_general_size": 42})
        config.set_theme("custom")
        self.assertEqual(config["font_general_size"], 42)
        config.set_theme("default")
        self.assertEqual(
            config["font_general_size"], DEFAULT_THEME["font_general_size"]
        )

    def test_register_theme_partial_fills_defaults(self):
        config.register_theme("partial", {"font_general_size": 7})
        config.set_theme("partial")
        self.assertEqual(config["font_general_size"], 7)
        self.assertEqual(
            config["font_general_family"], DEFAULT_THEME["font_general_family"]
        )
        config.reset_config()

    def test_register_theme_rejects_unknown_keys(self):
        with self.assertRaises(ValueError):
            config.register_theme("bad", {"not_a_key": 1})


if __name__ == "__main__":
    unittest.main()
