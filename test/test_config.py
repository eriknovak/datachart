import copy
import json
import tempfile
import unittest
from pathlib import Path

from datachart.config import config
from datachart.config.configuration import THEMES
from datachart.constants import THEME
from datachart.themes import DEFAULT_THEME

# =====================================
# Test Config
# =====================================


class TestConfig(unittest.TestCase):
    def tearDown(self):
        config.reset_config()

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

    def test_reset_config_resets_theme_name(self):
        config.set_theme(THEME.INK)
        config.reset_config()
        self.assertEqual(config.theme, THEME.DEFAULT)
        self.assertEqual(config.config, DEFAULT_THEME)

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


class TestScopes(unittest.TestCase):
    def tearDown(self):
        config.reset_config()

    def test_override_applies_and_restores(self):
        config.update_config({"font_general_size": 8})
        with config.override(font_general_size=20, font_title_size=30):
            self.assertEqual(config["font_general_size"], 20)
            self.assertEqual(config["font_title_size"], 30)
        self.assertEqual(config["font_general_size"], 8)
        self.assertEqual(config["font_title_size"], DEFAULT_THEME["font_title_size"])

    def test_override_accepts_dict(self):
        with config.override({"font_general_size": 20}):
            self.assertEqual(config["font_general_size"], 20)
        self.assertEqual(
            config["font_general_size"], DEFAULT_THEME["font_general_size"]
        )

    def test_override_restores_after_exception(self):
        before = copy.deepcopy(config.config)
        with self.assertRaises(RuntimeError):
            with config.override(font_general_size=20):
                raise RuntimeError("boom")
        self.assertEqual(config.config, before)

    def test_override_discards_inner_changes(self):
        before = copy.deepcopy(config.config)
        with config.override(font_general_size=20):
            config.update_config({"font_title_size": 99})
            config.set_theme(THEME.INK)
        self.assertEqual(config.config, before)
        self.assertEqual(config.theme, THEME.DEFAULT)

    def test_using_theme_applies_and_restores(self):
        with config.using_theme(THEME.INK):
            self.assertEqual(config.theme, THEME.INK)
            self.assertEqual(config.config, THEMES[THEME.INK])
        self.assertEqual(config.theme, THEME.DEFAULT)
        self.assertEqual(config.config, DEFAULT_THEME)

    def test_using_theme_restores_after_exception(self):
        config.set_theme(THEME.MINIMAL)
        config.update_config({"font_general_size": 8})
        before = copy.deepcopy(config.config)
        with self.assertRaises(RuntimeError):
            with config.using_theme(THEME.INK):
                raise RuntimeError("boom")
        self.assertEqual(config.theme, THEME.MINIMAL)
        self.assertEqual(config.config, before)

    def test_nesting_override_inside_theme(self):
        with config.using_theme(THEME.INK):
            with config.override(font_general_size=20):
                self.assertEqual(config["font_general_size"], 20)
                self.assertEqual(config.theme, THEME.INK)
            self.assertEqual(config.config, THEMES[THEME.INK])
        self.assertEqual(config.config, DEFAULT_THEME)
        self.assertEqual(config.theme, THEME.DEFAULT)

    def test_nesting_theme_inside_override(self):
        with config.override(font_general_size=20):
            with config.using_theme(THEME.INK):
                self.assertEqual(config.theme, THEME.INK)
                self.assertEqual(config.config, THEMES[THEME.INK])
            self.assertEqual(config["font_general_size"], 20)
            self.assertEqual(config.theme, THEME.DEFAULT)
        self.assertEqual(config.config, DEFAULT_THEME)


class TestThemeFiles(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()
        config.reset_config()

    def test_list_themes(self):
        names = config.list_themes()
        for name in THEMES:
            self.assertIn(name, names)
        config.register_theme("listed", {"font_general_size": 7})
        self.assertIn("listed", config.list_themes())

    def test_live_config_round_trip(self):
        config.set_theme(THEME.MINIMAL)
        config.update_config({"font_general_size": 8, "font_general_color": "#333"})
        original = copy.deepcopy(config.config)
        path = self.dir / "house.json"
        config.save_theme(path)
        name = config.load_theme(path, name="house-copy")
        self.assertEqual(name, "house-copy")
        config.set_theme(name)
        self.assertEqual(config.config, original)

    def test_builtin_round_trip(self):
        for name, theme in list(THEMES.items()):
            with self.subTest(theme=name):
                path = self.dir / f"{name}.json"
                config.save_theme(path, name=name)
                loaded = config.load_theme(path, name=f"{name}-copy")
                config.set_theme(loaded)
                self.assertEqual(config.config, theme)

    def test_saved_file_holds_only_the_diff(self):
        config.update_config({"font_general_size": 8})
        path = self.dir / "diff.json"
        config.save_theme(path)
        data = json.loads(path.read_text())
        self.assertEqual(data["attributes"], {"font_general_size": 8})
        self.assertEqual(data["name"], "diff")
        self.assertIn("format_version", data)

    def test_saving_default_theme_writes_empty_attributes(self):
        path = self.dir / "default.json"
        config.save_theme(path, name=THEME.DEFAULT)
        self.assertEqual(json.loads(path.read_text())["attributes"], {})

    def test_save_accepts_string_path(self):
        path = str(self.dir / "as-string.json")
        config.save_theme(path)
        self.assertTrue(Path(path).exists())

    def test_save_unknown_name_raises(self):
        with self.assertRaises(ValueError):
            config.save_theme(self.dir / "x.json", name="no-such-theme")

    def test_load_name_precedence(self):
        path = self.dir / "stem.json"
        path.write_text(json.dumps({"format_version": 1, "attributes": {}}))
        self.assertEqual(config.load_theme(path), "stem")
        path.write_text(
            json.dumps({"name": "in-file", "format_version": 1, "attributes": {}})
        )
        self.assertEqual(config.load_theme(path), "in-file")
        self.assertEqual(config.load_theme(path, name="caller"), "caller")
        for name in ("stem", "in-file", "caller"):
            self.assertIn(name, config.list_themes())

    def test_load_unknown_key_raises(self):
        path = self.dir / "bad.json"
        path.write_text(
            json.dumps({"format_version": 1, "attributes": {"not_a_key": 1}})
        )
        with self.assertRaises(ValueError):
            config.load_theme(path)

    def test_load_malformed_file_raises(self):
        path = self.dir / "malformed.json"
        path.write_text(json.dumps({"font_general_size": 8}))
        with self.assertRaises(ValueError):
            config.load_theme(path)

    def test_load_canonicalises_alias_keys(self):
        path = self.dir / "alias.json"
        path.write_text(
            json.dumps(
                {"format_version": 1, "attributes": {"plot_bar_value_fontsize": 3}}
            )
        )
        config.set_theme(config.load_theme(path))
        self.assertEqual(config["plot_value_fontsize"], 3)
        self.assertNotIn("plot_bar_value_fontsize", config.config)


if __name__ == "__main__":
    unittest.main()
