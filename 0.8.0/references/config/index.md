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

| METHOD          | DESCRIPTION                                      |
| --------------- | ------------------------------------------------ |
| `set_theme`     | Set the global configuration to match the theme. |
| `reset_config`  | Resets the global configuration.                 |
| `update_config` | Updates the global configuration.                |
| `get`           | Gets the associated configuration attribute.     |

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

#### reset_config

```
reset_config() -> None
```

Resets the global configuration.

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
