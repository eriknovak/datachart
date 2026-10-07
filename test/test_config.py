import copy
import json
import tempfile
import typing
import unittest
from pathlib import Path
from unittest import mock

from datachart.config import config
from datachart.config.configuration import THEMES, Config
from datachart.constants import THEME
from datachart.themes import DEFAULT_THEME, INK_THEME

# =====================================
# Test Config
# =====================================


class TestConfig(unittest.TestCase):
    def tearDown(self):
        config.reset()

    def test_initial_config(self):
        for key, val in DEFAULT_THEME.items():
            self.assertEqual(config[key], val)

    def test_update(self):
        updated_config = {"font_general_color": "#FFFFFF"}
        config.update(config=updated_config)
        for key, val in updated_config.items():
            self.assertEqual(config[key], val)

    def test_reset(self):
        config.reset()
        for key, val in DEFAULT_THEME.items():
            self.assertEqual(config[key], val)

    def test_reset_resets_theme_name(self):
        config.set_theme(THEME.INK)
        config.reset()
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
        config.reset()

    def test_register_theme_rejects_unknown_keys(self):
        with self.assertRaises(ValueError):
            config.register_theme("bad", {"not_a_key": 1})

    def test_register_theme_rejects_builtin_names(self):
        for name in (THEME.DEFAULT, THEME.INK, "dark"):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    config.register_theme(name, {"font_general_size": 42})
        config.reset()
        reset = copy.deepcopy(config.config)
        config.set_theme("default")
        self.assertEqual(config.config, reset)
        self.assertEqual(config.config, DEFAULT_THEME)

    def test_register_theme_replaces_a_custom_theme(self):
        config.register_theme("mine", {"font_general_size": 7})
        config.register_theme("mine", {"font_general_size": 9})
        config.set_theme("mine")
        self.assertEqual(config["font_general_size"], 9)

    def test_update_copies_its_values(self):
        colors = ["#111111", "#222222"]
        config.update({"color_general_multiple": colors})
        colors.append("#333333")
        self.assertEqual(config["color_general_multiple"], ["#111111", "#222222"])

    def test_update_warns_on_unknown_keys(self):
        with self.assertWarnsRegex(UserWarning, "not_a_key") as caught:
            config.update({"not_a_key": 1})
        self.assertEqual(caught.filename, __file__)
        self.assertNotIn("not_a_key", config.config)

    def test_deprecated_methods_are_gone(self):
        for old in ("update_config", "reset_config"):
            with self.subTest(old=old):
                self.assertFalse(hasattr(config, old))

    def test_theme_setters_accept_a_registered_name(self):
        for method in (Config.set_theme, Config.using_theme):
            with self.subTest(method=method.__name__):
                hint = typing.get_type_hints(method)["theme"]
                self.assertIn(str, typing.get_args(hint))
                self.assertIn(THEME, typing.get_args(hint))


class TestScopes(unittest.TestCase):
    def tearDown(self):
        config.reset()

    def test_override_applies_and_restores(self):
        config.update({"font_general_size": 8})
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
            config.update({"font_title_size": 99})
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
        config.update({"font_general_size": 8})
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
        config.reset()

    def test_list_themes(self):
        names = config.list_themes()
        for name in THEMES:
            self.assertIn(name, names)
        config.register_theme("listed", {"font_general_size": 7})
        self.assertIn("listed", config.list_themes())

    def test_live_config_round_trip(self):
        config.set_theme(THEME.MINIMAL)
        config.update({"font_general_size": 8, "font_general_color": "#333"})
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
        config.update({"font_general_size": 8})
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

    def test_load_builtin_name_raises_unless_renamed(self):
        path = self.dir / "ink.json"
        config.save_theme(path, name=THEME.INK)
        with self.assertRaises(ValueError):
            config.load_theme(path)
        self.assertEqual(config.load_theme(path, name="my-ink"), "my-ink")

    def test_load_unknown_key_raises(self):
        path = self.dir / "bad.json"
        path.write_text(
            json.dumps({"format_version": 1, "attributes": {"not_a_key": 1}})
        )
        with self.assertRaises(ValueError):
            config.load_theme(path)

    def test_load_other_format_version_raises(self):
        path = self.dir / "future.json"
        path.write_text(json.dumps({"format_version": 2, "attributes": {}}))
        with self.assertRaises(ValueError):
            config.load_theme(path)

    def test_load_malformed_file_raises(self):
        path = self.dir / "malformed.json"
        path.write_text(json.dumps({"font_general_size": 8}))
        with self.assertRaises(ValueError):
            config.load_theme(path)


if __name__ == "__main__":
    unittest.main()


# =====================================
# Test installed themes
# =====================================


PLUGIN_THEME = {"font_general_size": 33}


def plugin_theme_factory():
    return {"font_general_size": 34}


class _FakeEntryPoint:
    def __init__(self, name, obj):
        self.name = name
        self._obj = obj

    def load(self):
        if isinstance(self._obj, Exception):
            raise self._obj
        return self._obj


def _with_entry_points(themes=(), defaults=()):
    from datachart.config import configuration

    groups = {
        configuration.THEMES_ENTRY_POINT_GROUP: list(themes),
        configuration.DEFAULT_THEME_ENTRY_POINT_GROUP: list(defaults),
    }
    return mock.patch.object(
        configuration, "entry_points", lambda group: groups.get(group, [])
    )


class TestInstalledThemes(unittest.TestCase):
    def tearDown(self):
        THEMES.pop("acme", None)
        THEMES.pop("acme-factory", None)
        config.reset()

    def test_entry_point_theme_is_registered(self):
        with _with_entry_points(themes=[_FakeEntryPoint("acme", PLUGIN_THEME)]):
            fresh = Config()
        self.assertIn("acme", fresh.list_themes())
        self.assertEqual(THEMES["acme"]["font_general_size"], 33)
        self.assertEqual(fresh.theme, THEME.DEFAULT)

    def test_entry_point_callable_is_called(self):
        entry = _FakeEntryPoint("acme-factory", plugin_theme_factory)
        with _with_entry_points(themes=[entry]):
            Config()
        self.assertEqual(THEMES["acme-factory"]["font_general_size"], 34)

    def test_default_entry_point_starts_the_session_in_that_theme(self):
        themes = [_FakeEntryPoint("acme", PLUGIN_THEME)]
        defaults = [_FakeEntryPoint("acme", None)]
        with _with_entry_points(themes=themes, defaults=defaults):
            fresh = Config()
        self.assertEqual(fresh.theme, "acme")
        self.assertEqual(fresh.get("font_general_size"), 33)
        fresh.reset()
        self.assertEqual(fresh.theme, THEME.DEFAULT)

    def test_default_entry_point_accepts_a_builtin_name(self):
        with _with_entry_points(defaults=[_FakeEntryPoint("ink", None)]):
            fresh = Config()
        self.assertEqual(fresh.theme, THEME.INK)

    def test_broken_entry_point_warns_and_is_skipped(self):
        entries = [
            _FakeEntryPoint("acme", RuntimeError("boom")),
            _FakeEntryPoint("ink", PLUGIN_THEME),
            _FakeEntryPoint("acme-factory", {"not_a_key": 1}),
        ]
        with _with_entry_points(themes=entries):
            with self.assertWarns(UserWarning) as caught:
                fresh = Config()
        messages = [str(w.message) for w in caught.warnings]
        self.assertEqual(len(messages), 3)
        self.assertNotIn("acme", fresh.list_themes())
        self.assertNotIn("acme-factory", fresh.list_themes())
        self.assertEqual(
            THEMES[THEME.INK]["font_general_size"], INK_THEME["font_general_size"]
        )

    def test_unknown_default_warns_and_keeps_default(self):
        with _with_entry_points(defaults=[_FakeEntryPoint("missing", None)]):
            with self.assertWarns(UserWarning):
                fresh = Config()
        self.assertEqual(fresh.theme, THEME.DEFAULT)

    def test_several_defaults_warn_and_take_the_first_name(self):
        defaults = [_FakeEntryPoint("minimal", None), _FakeEntryPoint("ink", None)]
        with _with_entry_points(defaults=defaults):
            with self.assertWarns(UserWarning):
                fresh = Config()
        self.assertEqual(fresh.theme, THEME.INK)
