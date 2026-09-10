# Config Module

## datachart.config

The module containing the `config`.

The `config` module contains the configuration objects, enabling the users to globally customize the chart and plot styles.

| ATTRIBUTE | DESCRIPTION                                    |
| --------- | ---------------------------------------------- |
| `config`  | The configuration instance. **TYPE:** `Config` |

| CLASS    | DESCRIPTION              |
| -------- | ------------------------ |
| `Config` | The configuration class. |

## Attributes

### datachart.config.config

```
config: Config = Config()
```

The configuration instance that the users should interact with.

## Classes

### datachart.config.Config

The class representing the configuration options.

| ATTRIBUTE | DESCRIPTION                                     |
| --------- | ----------------------------------------------- |
| `config`  | The style configuration. **TYPE:** `StyleAttrs` |
| `theme`   | The name of the active theme. **TYPE:** `str`   |

| METHOD           | DESCRIPTION                                                   |
| ---------------- | ------------------------------------------------------------- |
| `set_theme`      | Set the global configuration to match the theme.              |
| `reset_config`   | Resets the global configuration.                              |
| `update_config`  | Updates the global configuration.                             |
| `override`       | Applies attribute overrides for the duration of a with block. |
| `using_theme`    | Applies a theme for the duration of a with block.             |
| `register_theme` | Registers a custom theme for use with set_theme.              |
| `list_themes`    | Lists the names set_theme accepts.                            |
| `save_theme`     | Writes a theme file.                                          |
| `load_theme`     | Registers the theme in a theme file.                          |
| `get`            | Gets the associated configuration attribute.                  |

#### __init__

```
__init__()
```

Initializes the global configuration.

#### set_theme

```
set_theme(theme: THEME) -> None
```

Sets the global configuration to match the theme.

Replaces the whole style configuration with a deep copy of the theme: one of the `THEME` constants or a name registered with `register_theme`. Use it to switch the look of every chart rendered afterwards; call `update_config` on top for per-attribute tweaks.

Added in v0.5.0

Examples:

```
>>> from datachart.constants import THEME
>>> from datachart.config import config
>>> config.set_theme(THEME.DEFAULT)
>>> config.get("theme")
'default'
```

| PARAMETER | DESCRIPTION                            |
| --------- | -------------------------------------- |
| `theme`   | The theme to be set. **TYPE:** `THEME` |

#### register_theme

```
register_theme(name: str, theme: StyleAttrs) -> None
```

Registers a custom theme so it can be applied with `set_theme`.

Added in v0.8.1

The theme must define every attribute of the default theme; missing keys are filled from it, unknown keys are rejected.

Examples:

```
>>> from datachart.config import config
>>> from datachart.themes import DEFAULT_THEME
>>> config.register_theme("mine", {**DEFAULT_THEME, "font_general_size": 14})
>>> config.set_theme("mine")
>>> config.get("font_general_size")
14
```

| PARAMETER | DESCRIPTION                                                |
| --------- | ---------------------------------------------------------- |
| `name`    | The theme name, later passed to set_theme. **TYPE:** `str` |
| `theme`   | The style attributes of the theme. **TYPE:** `StyleAttrs`  |

#### reset_config

```
reset_config() -> None
```

Resets the global configuration.

Restores the default theme, discarding the current theme and every `update_config` override, and resets the active theme name to match. Use it to return to a known state, for example at the start of a notebook section or between tests.

Examples:

```
>>> from datachart.config import config
>>> config.reset_config()
>>> config.get("theme")
'default'
```

#### update_config

```
update_config(config: StyleAttrs) -> None
```

Updates the global configuration.

Overrides individual style attributes on top of the current theme; the change persists until the next `set_theme` or `reset_config`. Use it for global tweaks such as font family or default colors; unknown attribute names are skipped with a warning.

Examples:

```
>>> from datachart.config import config
>>> config.update_config({"font_general_color": "#FFFFFF"})
>>> config.get("font_general_color")
'#FFFFFF'
```

| PARAMETER | DESCRIPTION                                                        |
| --------- | ------------------------------------------------------------------ |
| `config`  | The configuration attributes to be updated. **TYPE:** `StyleAttrs` |

#### override

```
override(
    config: Optional[StyleAttrs] = None, **attrs: Any
) -> Iterator[None]
```

Applies style overrides for the duration of a `with` block.

On entry the attributes are applied the way `update_config` applies them; on exit the configuration that entered the block is restored, also when the block raises. Any `set_theme` or `update_config` performed inside the block is discarded at exit. Use it for a one-off figure that needs a different font or palette without touching the global state. The scope is plain save-and-restore on the global configuration: it is neither thread-safe nor async-safe.

Added in Unreleased

Examples:

```
>>> from datachart.config import config
>>> with config.override(font_general_size=14):
...     config.get("font_general_size")
14
>>> config.get("font_general_size")
10
```

| PARAMETER | DESCRIPTION                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------- |
| `config`  | The attributes to override, as a dictionary. **TYPE:** `Optional[StyleAttrs]` **DEFAULT:** `None` |
| `**attrs` | The attributes to override, as keyword arguments. **TYPE:** `Any` **DEFAULT:** `{}`               |

#### using_theme

```
using_theme(theme: THEME) -> Iterator[None]
```

Applies a theme for the duration of a `with` block.

On entry the theme is applied the way `set_theme` applies it; on exit both the configuration and the active theme name that entered the block are restored, also when the block raises. Any `set_theme` or `update_config` performed inside the block is discarded at exit. The scope is plain save-and-restore on the global configuration: it is neither thread-safe nor async-safe.

Added in Unreleased

Examples:

```
>>> from datachart.constants import THEME
>>> from datachart.config import config
>>> with config.using_theme(THEME.INK):
...     config.theme
'ink'
>>> config.theme
'default'
```

| PARAMETER | DESCRIPTION                                                                            |
| --------- | -------------------------------------------------------------------------------------- |
| `theme`   | The theme to apply: one of the THEME constants or a registered name. **TYPE:** `THEME` |

#### list_themes

```
list_themes() -> List[str]
```

Lists the theme names `set_theme` accepts.

Returns the predefined themes in declaration order, followed by every name added with `register_theme` or `load_theme` in registration order.

Added in Unreleased

Examples:

```
>>> from datachart.config import config
>>> "default" in config.list_themes()
True
```

| RETURNS     | DESCRIPTION      |
| ----------- | ---------------- |
| `List[str]` | The theme names. |

#### save_theme

```
save_theme(
    path: Union[str, Path], name: Optional[str] = None
) -> None
```

Writes a theme file.

With no name the live configuration is saved, so a look assembled with `update_config` can be shared or committed directly; the file is named after its stem. With a name that registered theme is saved instead. The file is JSON and carries only the attributes that differ from the default theme, so it stays short and reviewable; load it back with `load_theme`. The parent directory must exist.

Added in Unreleased

Examples:

```
>>> from datachart.config import config
>>> config.update_config({"font_general_size": 14})
>>> config.save_theme("house.json")
>>> config.save_theme("ink.json", name="ink")
```

| PARAMETER | DESCRIPTION                                                                                                     |
| --------- | --------------------------------------------------------------------------------------------------------------- |
| `path`    | The file to write. **TYPE:** `Union[str, Path]`                                                                 |
| `name`    | The registered theme to save. Defaults to the live configuration. **TYPE:** `Optional[str]` **DEFAULT:** `None` |

| RAISES       | DESCRIPTION                        |
| ------------ | ---------------------------------- |
| `ValueError` | If name is not a registered theme. |

#### load_theme

```
load_theme(
    path: Union[str, Path], name: Optional[str] = None
) -> str
```

Registers the theme held in a theme file and returns its name.

The file is read as written by `save_theme` and registered through `register_theme`, so missing attributes are filled from the default theme, alias keys resolve to their canonical name, and unknown keys are rejected. The name is, in order of precedence, the `name` argument, the name in the file, or the file's stem; an existing theme of that name is replaced. Loading only registers: apply the theme with `set_theme` or `using_theme`.

Added in Unreleased

Examples:

```
>>> from datachart.config import config
>>> config.set_theme(config.load_theme("house.json"))
>>> config.theme
'house'
```

| PARAMETER | DESCRIPTION                                                                                                                                    |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `path`    | The theme file to read. **TYPE:** `Union[str, Path]`                                                                                           |
| `name`    | The name to register the theme under. Defaults to the name in the file, then to the file's stem. **TYPE:** `Optional[str]` **DEFAULT:** `None` |

| RETURNS | DESCRIPTION                              |
| ------- | ---------------------------------------- |
| `str`   | The name the theme was registered under. |

| RAISES       | DESCRIPTION                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------- |
| `ValueError` | If the file is not a theme file, states another format version, or holds an unknown attribute. |

#### __getitem__

```
__getitem__(attr: str) -> Any
```

Gets the associated configuration attribute.

Examples:

```
>>> from datachart.config import config
>>> config["font_general_color"]
'#FFFFFF'
```

| PARAMETER | DESCRIPTION                                |
| --------- | ------------------------------------------ |
| `attr`    | The attribute to retrieve. **TYPE:** `str` |

| RETURNS | DESCRIPTION                                      |
| ------- | ------------------------------------------------ |
| `Any`   | The attribute value if present. Otherwise, None. |

#### get

```
get(attr: str, default: Any = None) -> Any
```

Gets the associated configuration attribute.

Reads one style attribute, falling back to `default` when it is not set. Use it to inspect the active configuration or to build style overrides relative to the current theme.

Examples:

```
>>> from datachart.config import config
>>> config.get("font_general_color")
'#FFFFFF'
```

| PARAMETER | DESCRIPTION                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------- |
| `attr`    | The attribute to retrieve. **TYPE:** `str`                                                              |
| `default` | The value to return, if the attribute is not present in the config. **TYPE:** `Any` **DEFAULT:** `None` |

| RETURNS | DESCRIPTION                                                           |
| ------- | --------------------------------------------------------------------- |
| `Any`   | The attribute value if present. Otherwise, returns the default value. |

#### __repr__

```
__repr__()
```

Represents the configuration as a json string.
