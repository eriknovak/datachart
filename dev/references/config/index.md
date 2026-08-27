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

| METHOD           | DESCRIPTION                                      |
| ---------------- | ------------------------------------------------ |
| `set_theme`      | Set the global configuration to match the theme. |
| `reset_config`   | Resets the global configuration.                 |
| `update_config`  | Updates the global configuration.                |
| `register_theme` | Registers a custom theme for use with set_theme. |
| `get`            | Gets the associated configuration attribute.     |

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

Restores the default theme, discarding the current theme and every `update_config` override. Use it to return to a known state, for example at the start of a notebook section or between tests.

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
