import copy
import json
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Optional, Union

# import the schemas
from datachart.typings import StyleAttrs
from datachart.constants import THEME

# import the themes
from ..themes._base import BASE_THEME, STYLE_ALIASES, canonical_style
from ..themes import (
    DEFAULT_THEME,
    GREYSCALE_THEME,
    INK_THEME,
    HATCH_THEME,
    MINIMAL_THEME,
    MATERIAL_THEME,
    SKETCH_THEME,
)

THEMES = {
    THEME.DEFAULT: DEFAULT_THEME,
    THEME.GREYSCALE: GREYSCALE_THEME,
    THEME.INK: INK_THEME,
    THEME.HATCH: HATCH_THEME,
    THEME.MINIMAL: MINIMAL_THEME,
    THEME.MATERIAL: MATERIAL_THEME,
    THEME.SKETCH: SKETCH_THEME,
}

# bumped only when a reader of the current shape could misread an older file
THEME_FILE_VERSION = 1


class Config:
    """The class representing the configuration options.

    Attributes:
        config (StyleAttrs): The style configuration.

    Methods:
        set_theme(theme):
            Set the global configuration to match the theme.
        reset_config():
            Resets the global configuration.
        update_config(config):
            Updates the global configuration.
        override(config, **attrs):
            Applies attribute overrides for the duration of a `with` block.
        using_theme(theme):
            Applies a theme for the duration of a `with` block.
        register_theme(name, theme):
            Registers a custom theme for use with `set_theme`.
        list_themes():
            Lists the names `set_theme` accepts.
        save_theme(path, name):
            Writes a theme file.
        load_theme(path, name):
            Registers the theme in a theme file.
        get(attr, default):
            Gets the associated configuration attribute.

    """

    config: StyleAttrs

    def __init__(self):
        """Initializes the global configuration."""

        self.config = copy.deepcopy(DEFAULT_THEME)
        self.theme = THEME.DEFAULT

    def set_theme(self, theme: THEME) -> None:
        """Sets the global configuration to match the theme.

        Replaces the whole style configuration with a deep copy of the theme:
        one of the `THEME` constants or a name registered with `register_theme`.
        Use it to switch the look of every chart rendered afterwards; call
        `update_config` on top for per-attribute tweaks.

        !!! info "Added in v0.5.0"

        Examples:
            >>> from datachart.constants import THEME
            >>> from datachart.config import config
            >>> config.set_theme(THEME.DEFAULT)
            >>> config.get("theme")
            'default'

        Args:
            theme: The theme to be set.

        """
        if theme in THEMES:
            self.config = copy.deepcopy(THEMES[theme])
            self.theme = theme
        else:
            warnings.warn(
                f"Warning: {theme} is not a valid theme. Must be one of {list(THEMES)}. Reverting to last active theme..."
            )
            self.set_theme(self.theme)

    def register_theme(self, name: str, theme: StyleAttrs) -> None:
        """Registers a custom theme so it can be applied with `set_theme`.

        !!! info "Added in v0.8.1"

        The theme must define every attribute of the default theme; missing
        keys are filled from it, unknown keys are rejected.

        Examples:
            >>> from datachart.config import config
            >>> from datachart.themes import DEFAULT_THEME
            >>> config.register_theme("mine", {**DEFAULT_THEME, "font_general_size": 14})
            >>> config.set_theme("mine")
            >>> config.get("font_general_size")
            14

        Args:
            name: The theme name, later passed to `set_theme`.
            theme: The style attributes of the theme.

        """
        theme = canonical_style(theme)
        unknown = set(theme) - set(DEFAULT_THEME)
        if unknown:
            raise ValueError(f"Unknown theme attributes: {sorted(unknown)}")
        THEMES[name] = {**copy.deepcopy(DEFAULT_THEME), **copy.deepcopy(theme)}

    def reset_config(self) -> None:
        """Resets the global configuration.

        Restores the default theme, discarding the current theme and every
        `update_config` override, and resets the active theme name to match.
        Use it to return to a known state, for example at the start of a
        notebook section or between tests.

        Examples:
            >>> from datachart.config import config
            >>> config.reset_config()
            >>> config.get("theme")
            'default'

        """
        self.config = copy.deepcopy(DEFAULT_THEME)
        self.theme = THEME.DEFAULT

    def update_config(self, config: StyleAttrs) -> None:
        """Updates the global configuration.

        Overrides individual style attributes on top of the current theme; the
        change persists until the next `set_theme` or `reset_config`. Use it for
        global tweaks such as font family or default colors; unknown attribute
        names are skipped with a warning.

        Examples:
            >>> from datachart.config import config
            >>> config.update_config({"font_general_color": "#FFFFFF"})
            >>> config.get("font_general_color")
            '#FFFFFF'

        Args:
            config: The configuration attributes to be updated.

        """

        for key, val in canonical_style(config).items():
            if key not in self.config:
                print(f"Warning: Attribute '{key}' is not valid. Skipping attribute...")
                continue
            self.config[key] = val

    @contextmanager
    def _scope(self) -> Iterator[None]:
        """Restores the style dict and the active theme name on exit (ADR 0040)."""

        saved_config, saved_theme = self.config, self.theme
        self.config = copy.deepcopy(saved_config)
        try:
            yield
        finally:
            self.config, self.theme = saved_config, saved_theme

    @contextmanager
    def override(
        self, config: Optional[StyleAttrs] = None, **attrs: Any
    ) -> Iterator[None]:
        """Applies style overrides for the duration of a `with` block.

        On entry the attributes are applied the way `update_config` applies
        them; on exit the configuration that entered the block is restored,
        also when the block raises. Any `set_theme` or `update_config` performed
        inside the block is discarded at exit. Use it for a one-off figure that
        needs a different font or palette without touching the global state.
        The scope is plain save-and-restore on the global configuration: it is
        neither thread-safe nor async-safe.

        !!! info "Added in Unreleased"

        Examples:
            >>> from datachart.config import config
            >>> with config.override(font_general_size=14):
            ...     config.get("font_general_size")
            14
            >>> config.get("font_general_size")
            10

        Args:
            config: The attributes to override, as a dictionary.
            **attrs: The attributes to override, as keyword arguments.

        """
        overrides: dict = dict(config or {})
        overrides.update(attrs)
        with self._scope():
            self.update_config(overrides)
            yield

    @contextmanager
    def using_theme(self, theme: THEME) -> Iterator[None]:
        """Applies a theme for the duration of a `with` block.

        On entry the theme is applied the way `set_theme` applies it; on exit
        both the configuration and the active theme name that entered the
        block are restored, also when the block raises. Any `set_theme` or
        `update_config` performed inside the block is discarded at exit. The
        scope is plain save-and-restore on the global configuration: it is
        neither thread-safe nor async-safe.

        !!! info "Added in Unreleased"

        Examples:
            >>> from datachart.constants import THEME
            >>> from datachart.config import config
            >>> with config.using_theme(THEME.INK):
            ...     config.theme
            'ink'
            >>> config.theme
            'default'

        Args:
            theme: The theme to apply: one of the `THEME` constants or a
                registered name.

        """
        with self._scope():
            self.set_theme(theme)
            yield

    def list_themes(self) -> list:
        """Lists the theme names `set_theme` accepts.

        Returns the predefined themes in declaration order, followed by every
        name added with `register_theme` or `load_theme` in registration order.

        !!! info "Added in Unreleased"

        Examples:
            >>> from datachart.config import config
            >>> "default" in config.list_themes()
            True

        Returns:
            The theme names.

        """
        return list(THEMES)

    def save_theme(self, path: Union[str, Path], name: Optional[str] = None) -> None:
        """Writes a theme file.

        With no name the live configuration is saved, so a look assembled
        with `update_config` can be shared or committed directly; the file is
        named after its stem. With a name that registered theme is saved
        instead. The file is JSON and carries only the attributes that differ
        from the default theme, so it stays short and reviewable; load it back
        with `load_theme`. The parent directory must exist.

        !!! info "Added in Unreleased"

        Examples:
            >>> from datachart.config import config
            >>> config.update_config({"font_general_size": 14})
            >>> config.save_theme("house.json")
            >>> config.save_theme("ink.json", name="ink")

        Args:
            path: The file to write.
            name: The registered theme to save. Defaults to the live
                configuration.

        Raises:
            ValueError: If `name` is not a registered theme.

        """
        path = Path(path)
        if name is None:
            style, name = self.config, path.stem
        elif name in THEMES:
            style = THEMES[name]
        else:
            raise ValueError(
                f"Unknown theme: {name!r}. Must be one of {self.list_themes()}"
            )
        attributes = {
            key: val
            for key, val in canonical_style(style).items()
            if val != BASE_THEME.get(key)
        }
        data = {
            "name": name,
            "format_version": THEME_FILE_VERSION,
            "attributes": attributes,
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + "\n")

    def load_theme(self, path: Union[str, Path], name: Optional[str] = None) -> str:
        """Registers the theme held in a theme file and returns its name.

        The file is read as written by `save_theme` and registered through
        `register_theme`, so missing attributes are filled from the default
        theme, alias keys resolve to their canonical name, and unknown keys
        are rejected. The name is, in order of precedence, the `name`
        argument, the name in the file, or the file's stem; an existing theme
        of that name is replaced. Loading only registers: apply the theme with
        `set_theme` or `using_theme`.

        !!! info "Added in Unreleased"

        Examples:
            >>> from datachart.config import config
            >>> config.set_theme(config.load_theme("house.json"))
            >>> config.theme
            'house'

        Args:
            path: The theme file to read.
            name: The name to register the theme under. Defaults to the name
                in the file, then to the file's stem.

        Returns:
            The name the theme was registered under.

        Raises:
            ValueError: If the file is not a theme file, was written by a
                newer format, or holds an unknown attribute.

        """
        path = Path(path)
        data = json.loads(path.read_text())
        if not isinstance(data, dict) or not isinstance(data.get("attributes"), dict):
            raise ValueError(
                f"{path} is not a theme file: expected an object with 'attributes'"
            )
        if data.get("format_version") != THEME_FILE_VERSION:
            raise ValueError(
                f"{path} has theme file format {data.get('format_version')!r}; "
                f"this version of datachart reads format {THEME_FILE_VERSION}"
            )
        name = name or data.get("name") or path.stem
        self.register_theme(name, data["attributes"])
        return name

    def __getitem__(self, attr: str) -> Any:
        """Gets the associated configuration attribute.

        Examples:
            >>> from datachart.config import config
            >>> config["font_general_color"]
            '#FFFFFF'

        Args:
            attr: The attribute to retrieve.

        Returns:
            The attribute value if present. Otherwise, `None`.

        """
        attr = STYLE_ALIASES.get(attr, attr)
        return self.config[attr] if attr in self.config else None

    def get(self, attr: str, default: Any = None) -> Any:
        """Gets the associated configuration attribute.

        Reads one style attribute, falling back to `default` when it is not
        set. Use it to inspect the active configuration or to build style
        overrides relative to the current theme.

        Examples:
            >>> from datachart.config import config
            >>> config.get("font_general_color")
            '#FFFFFF'

        Args:
            attr: The attribute to retrieve.
            default: The value to return, if the attribute is not present in the config.

        Returns:
            The attribute value if present. Otherwise, returns the `default` value.

        """
        return self.config.get(STYLE_ALIASES.get(attr, attr), default)

    def __repr__(self):
        """Represents the configuration as a json string."""
        return json.dumps(self.config, ensure_ascii=False, indent=4)


config: Config = Config()
"""The configuration instance that the users should interact with."""
