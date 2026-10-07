import copy
import json
import warnings
from contextlib import contextmanager
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Iterator, List, Optional, Union

# import the schemas
from datachart.typings import StyleAttrs
from datachart.constants import THEME

# import the themes
from ..themes._base import (
    complete_theme as _complete_theme,
)
from ..themes.score import warn_failing_palette as _warn_failing_palette
from ..themes import (
    DEFAULT_THEME,
    GREYSCALE_THEME,
    INK_THEME,
    HATCH_THEME,
    MINIMAL_THEME,
    MATERIAL_THEME,
    SKETCH_THEME,
    QUILL_THEME,
    HARBOR_THEME,
    MUTED_THEME,
    CONTRAST_THEME,
    MUTEDHATCH_THEME,
    SLATEHATCH_THEME,
    DARK_THEME,
)

__all__ = ["config", "Config"]

THEMES = {
    THEME.DEFAULT: DEFAULT_THEME,
    THEME.GREYSCALE: GREYSCALE_THEME,
    THEME.INK: INK_THEME,
    THEME.HATCH: HATCH_THEME,
    THEME.MINIMAL: MINIMAL_THEME,
    THEME.MATERIAL: MATERIAL_THEME,
    THEME.SKETCH: SKETCH_THEME,
    THEME.QUILL: QUILL_THEME,
    THEME.HARBOR: HARBOR_THEME,
    THEME.MUTED: MUTED_THEME,
    THEME.CONTRAST: CONTRAST_THEME,
    THEME.MUTEDHATCH: MUTEDHATCH_THEME,
    THEME.SLATEHATCH: SLATEHATCH_THEME,
    THEME.DARK: DARK_THEME,
}
# reset and set_theme("default") must never disagree
BUILTIN_THEMES = frozenset(THEMES)

# bumped only when a reader of the current shape could misread an older file
THEME_FILE_VERSION = 1

# an installed package registers themes under the first group and names the
# one to start the session in under the second (ADR 0088)
THEMES_ENTRY_POINT_GROUP = "datachart.themes"
DEFAULT_THEME_ENTRY_POINT_GROUP = "datachart.default_theme"


class Config:
    """The class representing the configuration options.

    Attributes:
        config (StyleAttrs): The style configuration.
        theme (str): The name of the active theme.

    Methods:
        set_theme(theme):
            Set the global configuration to match the theme.
        reset():
            Resets the global configuration.
        update(config):
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
        self._register_installed_themes()
        self._apply_installed_default()

    def _register_installed_themes(self) -> None:
        """Registers every theme an installed package advertises.

        A package lists its themes as entry points in the
        `datachart.themes` group, one per theme, the entry point name being
        the theme name and its object a theme dictionary or a callable
        returning one. A theme that fails to load or register is skipped with
        a warning, so a broken package never breaks `datachart`.
        """

        for entry in sorted(
            entry_points(group=THEMES_ENTRY_POINT_GROUP), key=lambda e: e.name
        ):
            try:
                theme = entry.load()
                if callable(theme):
                    theme = theme()
                self.register_theme(entry.name, theme)
            except Exception as error:
                warnings.warn(
                    f"Warning: skipping installed theme {entry.name!r}: {error}"
                )

    def _apply_installed_default(self) -> None:
        """Starts the session in the theme an installed package names.

        A package names the theme in the `datachart.default_theme` group;
        the entry point name is the theme name, its object is never loaded.
        With several packages the first name in sorted order wins, with a
        warning. An unknown name is skipped with a warning.
        """

        names = sorted(
            {
                entry.name
                for entry in entry_points(group=DEFAULT_THEME_ENTRY_POINT_GROUP)
            }
        )
        if not names:
            return
        if len(names) > 1:
            warnings.warn(
                f"Warning: several installed packages name a default theme {names}; "
                f"starting in {names[0]!r}."
            )
        if names[0] not in THEMES:
            warnings.warn(
                f"Warning: installed default theme {names[0]!r} is not a registered theme; "
                "starting in the default theme."
            )
            return
        self.set_theme(names[0])

    def set_theme(self, theme: Union[THEME, str]) -> None:
        """Sets the global configuration to match the theme.

        Replaces the whole style configuration with a deep copy of the theme: one of the
        [`THEME`][datachart.constants.THEME] constants or a name registered with
        `register_theme`. Use it to switch the look of every chart rendered afterwards;
        call `update` on top for per-attribute tweaks.

        Examples:
            >>> from datachart.constants import THEME
            >>> from datachart.config import config
            >>> config.set_theme(THEME.DEFAULT)
            >>> config.theme
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

        Missing attributes are filled from the default theme and unknown keys
        are rejected. A custom theme of the same name is replaced; the
        predefined theme names are reserved.

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

        Raises:
            ValueError: If `name` is a predefined theme or `theme` holds an
                unknown attribute.

        """
        if name in BUILTIN_THEMES:
            raise ValueError(
                f"{name!r} is a predefined theme and cannot be replaced; "
                "register the theme under another name."
            )
        THEMES[name] = _complete_theme(theme)
        _warn_failing_palette(THEMES[name])

    def reset(self) -> None:
        """Resets the global configuration.

        Restores the default theme, discarding the current theme and every
        `update` override, and resets the active theme name to match.
        Use it to return to a known state, for example at the start of a
        notebook section or between tests.

        Examples:
            >>> from datachart.config import config
            >>> config.reset()
            >>> config.theme
            'default'

        """
        self.config = copy.deepcopy(DEFAULT_THEME)
        self.theme = THEME.DEFAULT

    def update(self, config: StyleAttrs) -> None:
        """Updates the global configuration.

        Overrides individual style attributes on top of the current theme; the
        change persists until the next `set_theme` or `reset`. Use it for
        global tweaks such as font family or default colors; the values are
        copied, and unknown attribute names are skipped with a warning.

        Examples:
            >>> from datachart.config import config
            >>> config.update({"font_general_color": "#FFFFFF"})
            >>> config.get("font_general_color")
            '#FFFFFF'

        Args:
            config: The configuration attributes to be updated.

        """

        self._update(config, stacklevel=2)

    def _update(self, config: StyleAttrs, stacklevel: int) -> None:
        """`update`, warning at `stacklevel` counted from the caller."""

        for key, val in config.items():
            if key not in self.config:
                warnings.warn(
                    f"Attribute {key!r} is not valid. Skipping attribute...",
                    stacklevel=stacklevel + 1,
                )
                continue
            self.config[key] = copy.deepcopy(val)

    # both scopes restore wholesale, exceptions included (ADR 0040)
    @contextmanager
    def _scope(self) -> Iterator[None]:
        """Restores the style dict and the active theme name on exit."""

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

        On entry the attributes are applied the way `update` applies
        them; on exit the configuration that entered the block is restored,
        also when the block raises. Any `set_theme` or `update` performed
        inside the block is discarded at exit. Use it for a one-off figure that
        needs a different font or palette without touching the global state.
        The scope is plain save-and-restore on the global configuration: it is
        neither thread-safe nor async-safe.

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
            # this generator, contextmanager's `__enter__`, then the caller
            self._update(overrides, stacklevel=3)
            yield

    @contextmanager
    def using_theme(self, theme: Union[THEME, str]) -> Iterator[None]:
        """Applies a theme for the duration of a `with` block.

        On entry the theme is applied the way `set_theme` applies it; on exit
        both the configuration and the active theme name that entered the
        block are restored, also when the block raises. Any `set_theme` or
        `update` performed inside the block is discarded at exit. The
        scope is plain save-and-restore on the global configuration: it is
        neither thread-safe nor async-safe.

        Examples:
            >>> from datachart.constants import THEME
            >>> from datachart.config import config
            >>> with config.using_theme(THEME.INK):
            ...     config.theme
            'ink'
            >>> config.theme
            'default'

        Args:
            theme: The theme to apply: one of the [`THEME`][datachart.constants.THEME]
                constants or a registered name.

        """
        with self._scope():
            self.set_theme(theme)
            yield

    def list_themes(self) -> List[str]:
        """Lists the theme names `set_theme` accepts.

        Returns the predefined themes in declaration order, followed by every
        name added with `register_theme` or `load_theme` in registration order.

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
        with `update` can be shared or committed directly; the file is
        named after its stem. With a name that registered theme is saved
        instead. The file is JSON and carries only the attributes that differ
        from the default theme, so it stays short and reviewable; load it back
        with `load_theme`. The parent directory must exist.

        Examples:
            >>> from datachart.config import config
            >>> config.update({"font_general_size": 14})
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
            style, file_name = self.config, path.stem
        elif name in THEMES:
            style, file_name = THEMES[name], name
        else:
            raise ValueError(
                f"Unknown theme: {name!r}. Must be one of {self.list_themes()}"
            )
        # diffed against what register_theme fills missing keys from, so a
        # file loads back to exactly the style it was saved from
        attributes = {
            key: val for key, val in style.items() if val != DEFAULT_THEME.get(key)
        }
        data = {
            "name": file_name,
            "format_version": THEME_FILE_VERSION,
            "attributes": attributes,
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + "\n")

    def load_theme(self, path: Union[str, Path], name: Optional[str] = None) -> str:
        """Registers the theme held in a theme file and returns its name.

        The file is read as written by `save_theme` and registered through
        `register_theme`, so missing attributes are filled from the default
        theme and unknown keys are rejected. The name is, in order of precedence, the `name`
        argument, the name in the file, or the file's stem; an existing custom
        theme of that name is replaced, while a predefined theme's name is
        rejected, so a file saved from one loads only with a new `name`.
        Loading only registers: apply the theme with `set_theme` or
        `using_theme`.

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
            ValueError: If the file is not a theme file, states another
                format version, holds an unknown attribute, or would register
                under a predefined theme's name.

        """
        path = Path(path)
        data = json.loads(path.read_text())
        if not isinstance(data, dict) or not isinstance(data.get("attributes"), dict):
            raise ValueError(
                f"{path} is not a theme file: expected an object with 'attributes'"
            )
        if data.get("format_version") != THEME_FILE_VERSION:
            raise ValueError(
                f"{path} states theme file format {data.get('format_version')!r}; "
                f"expected {THEME_FILE_VERSION}"
            )
        name = name or data.get("name") or path.stem
        self.register_theme(name, data["attributes"])
        return name

    def __getitem__(self, attr: str) -> Any:
        """Gets the associated configuration attribute.

        Examples:
            >>> from datachart.config import config
            >>> config["font_general_color"]
            '#000000'

        Args:
            attr: The attribute to retrieve.

        Returns:
            The attribute value if present. Otherwise, `None`.

        """
        return self.config[attr] if attr in self.config else None

    def get(self, attr: str, default: Any = None) -> Any:
        """Gets the associated configuration attribute.

        Reads one style attribute, falling back to `default` when it is not
        set. Use it to inspect the active configuration or to build style
        overrides relative to the current theme.

        Examples:
            >>> from datachart.config import config
            >>> config.get("font_general_color")
            '#000000'

        Args:
            attr: The attribute to retrieve.
            default: The value to return, if the attribute is not present in the config.

        Returns:
            The attribute value if present. Otherwise, returns the `default` value.

        """
        return self.config.get(attr, default)

    def __repr__(self):
        """Represents the configuration as a json string."""
        return json.dumps(self.config, ensure_ascii=False, indent=4)


config: Config = Config()
"""The configuration instance that the users should interact with."""
