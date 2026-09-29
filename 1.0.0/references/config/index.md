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

## Choosing a Method

One `config` instance holds the style every chart is drawn with. Its methods change that style for the rest of the session, for one block of code, or from a file; the [Themes guide](https://eriknovak.github.io/datachart/1.0.0/how-to-guides/styling/themes/index.md) walks through them on a chart.

| I want to…                                  | Call                                                         | See                                                                                                  |
| ------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| switch the look of every chart              | `config.set_theme(THEME.INK)`                                | [set_theme](#datachart.config.Config.set_theme)                                                      |
| change a few attributes on top of the theme | `config.update({"font_general_size": 12})`                   | [update](#datachart.config.Config.update)                                                            |
| change the look for one block of code       | `with config.override(...)`, `with config.using_theme(...)`  | [override](#datachart.config.Config.override), [using_theme](#datachart.config.Config.using_theme)   |
| go back to the default theme                | `config.reset()`                                             | [reset](#datachart.config.Config.reset)                                                              |
| add a theme of my own                       | `config.register_theme(name, theme)`, then `set_theme(name)` | [register_theme](#datachart.config.Config.register_theme)                                            |
| see which names `set_theme` accepts         | `config.list_themes()`                                       | [list_themes](#datachart.config.Config.list_themes)                                                  |
| share a theme as a file                     | `config.save_theme(path)`, `config.load_theme(path)`         | [save_theme](#datachart.config.Config.save_theme), [load_theme](#datachart.config.Config.load_theme) |
| read one attribute                          | `config.get("font_general_size")`                            | [get](#datachart.config.Config.get)                                                                  |

The attribute names are the keys of [`StyleAttrs`](https://eriknovak.github.io/datachart/1.0.0/references/typings/#datachart.typings.StyleAttrs): the theme-level keys on the [typings](https://eriknovak.github.io/datachart/1.0.0/references/typings/#theme-style) page and each chart's own keys on its [reference page](https://eriknovak.github.io/datachart/1.0.0/references/charts/index.md). The theme names are the members of [`THEME`](https://eriknovak.github.io/datachart/1.0.0/references/constants/#datachart.constants.THEME).

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
| `reset`          | Resets the global configuration.                              |
| `update`         | Updates the global configuration.                             |
| `override`       | Applies attribute overrides for the duration of a with block. |
| `using_theme`    | Applies a theme for the duration of a with block.             |
| `register_theme` | Registers a custom theme for use with set_theme.              |
| `list_themes`    | Lists the names set_theme accepts.                            |
| `save_theme`     | Writes a theme file.                                          |
| `load_theme`     | Registers the theme in a theme file.                          |
| `get`            | Gets the associated configuration attribute.                  |

#### set_theme

```
set_theme(theme: THEME | str) -> None
```

Sets the global configuration to match the theme.

Replaces the whole style configuration with a deep copy of the theme: one of the THEME constants or a name registered with `register_theme`. Use it to switch the look of every chart rendered afterwards; call `update` on top for per-attribute tweaks.

Examples:

```
>>> from datachart.constants import THEME
>>> from datachart.config import config
>>> config.set_theme(THEME.DEFAULT)
>>> config.theme
'default'
```

| PARAMETER | DESCRIPTION                            |
| --------- | -------------------------------------- |
| `theme`   | The theme to be set. **TYPE:** \`THEME |

#### register_theme

```
register_theme(name: str, theme: StyleAttrs) -> None
```

Registers a custom theme so it can be applied with `set_theme`.

Missing attributes are filled from the default theme and unknown keys are rejected. A custom theme of the same name is replaced; the predefined theme names are reserved.

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

| RAISES       | DESCRIPTION                                                        |
| ------------ | ------------------------------------------------------------------ |
| `ValueError` | If name is a predefined theme or theme holds an unknown attribute. |

#### reset

```
reset() -> None
```

Resets the global configuration.

Restores the default theme, discarding the current theme and every `update` override, and resets the active theme name to match. Use it to return to a known state, for example at the start of a notebook section or between tests.

Examples:

```
>>> from datachart.config import config
>>> config.reset()
>>> config.theme
'default'
```

#### update

```
update(config: StyleAttrs) -> None
```

Updates the global configuration.

Overrides individual style attributes on top of the current theme; the change persists until the next `set_theme` or `reset`. Use it for global tweaks such as font family or default colors; the values are copied, and unknown attribute names are skipped with a warning.

Examples:

```
>>> from datachart.config import config
>>> config.update({"font_general_color": "#FFFFFF"})
>>> config.get("font_general_color")
'#FFFFFF'
```

| PARAMETER | DESCRIPTION                                                        |
| --------- | ------------------------------------------------------------------ |
| `config`  | The configuration attributes to be updated. **TYPE:** `StyleAttrs` |

#### \_update

```
_update(config: StyleAttrs, stacklevel: int) -> None
```

`update`, warning at `stacklevel` counted from the caller.

#### \_scope

```
_scope() -> Iterator[None]
```

Restores the style dict and the active theme name on exit.

#### override

```
override(
    config: StyleAttrs | None = None, **attrs: Any
) -> Iterator[None]
```

Applies style overrides for the duration of a `with` block.

On entry the attributes are applied the way `update` applies them; on exit the configuration that entered the block is restored, also when the block raises. Any `set_theme` or `update` performed inside the block is discarded at exit. Use it for a one-off figure that needs a different font or palette without touching the global state. The scope is plain save-and-restore on the global configuration: it is neither thread-safe nor async-safe.

Examples:

```
>>> from datachart.config import config
>>> with config.override(font_general_size=14):
...     config.get("font_general_size")
14
>>> config.get("font_general_size")
10
```

| PARAMETER | DESCRIPTION                                                                         |
| --------- | ----------------------------------------------------------------------------------- |
| `config`  | The attributes to override, as a dictionary. **TYPE:** \`StyleAttrs                 |
| `**attrs` | The attributes to override, as keyword arguments. **TYPE:** `Any` **DEFAULT:** `{}` |

#### using_theme

```
using_theme(theme: THEME | str) -> Iterator[None]
```

Applies a theme for the duration of a `with` block.

On entry the theme is applied the way `set_theme` applies it; on exit both the configuration and the active theme name that entered the block are restored, also when the block raises. Any `set_theme` or `update` performed inside the block is discarded at exit. The scope is plain save-and-restore on the global configuration: it is neither thread-safe nor async-safe.

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
| `theme`   | The theme to apply: one of the THEME constants or a registered name. **TYPE:** \`THEME |

#### list_themes

```
list_themes() -> list[str]
```

Lists the theme names `set_theme` accepts.

Returns the predefined themes in declaration order, followed by every name added with `register_theme` or `load_theme` in registration order.

Examples:

```
>>> from datachart.config import config
>>> "default" in config.list_themes()
True
```

| RETURNS     | DESCRIPTION      |
| ----------- | ---------------- |
| `list[str]` | The theme names. |

#### save_theme

```
save_theme(
    path: str | Path, name: str | None = None
) -> None
```

Writes a theme file.

With no name the live configuration is saved, so a look assembled with `update` can be shared or committed directly; the file is named after its stem. With a name that registered theme is saved instead. The file is JSON and carries only the attributes that differ from the default theme, so it stays short and reviewable; load it back with `load_theme`. The parent directory must exist.

Examples:

```
>>> from datachart.config import config
>>> config.update({"font_general_size": 14})
>>> config.save_theme("house.json")
>>> config.save_theme("ink.json", name="ink")
```

| PARAMETER | DESCRIPTION                                                                       |
| --------- | --------------------------------------------------------------------------------- |
| `path`    | The file to write. **TYPE:** \`str                                                |
| `name`    | The registered theme to save. Defaults to the live configuration. **TYPE:** \`str |

| RAISES       | DESCRIPTION                        |
| ------------ | ---------------------------------- |
| `ValueError` | If name is not a registered theme. |

#### load_theme

```
load_theme(
    path: str | Path, name: str | None = None
) -> str
```

Registers the theme held in a theme file and returns its name.

The file is read as written by `save_theme` and registered through `register_theme`, so missing attributes are filled from the default theme and unknown keys are rejected. The name is, in order of precedence, the `name` argument, the name in the file, or the file's stem; an existing custom theme of that name is replaced, while a predefined theme's name is rejected, so a file saved from one loads only with a new `name`. Loading only registers: apply the theme with `set_theme` or `using_theme`.

Examples:

```
>>> from datachart.config import config
>>> config.set_theme(config.load_theme("house.json"))
>>> config.theme
'house'
```

| PARAMETER | DESCRIPTION                                                                                                      |
| --------- | ---------------------------------------------------------------------------------------------------------------- |
| `path`    | The theme file to read. **TYPE:** \`str                                                                          |
| `name`    | The name to register the theme under. Defaults to the name in the file, then to the file's stem. **TYPE:** \`str |

| RETURNS | DESCRIPTION                              |
| ------- | ---------------------------------------- |
| `str`   | The name the theme was registered under. |

| RAISES       | DESCRIPTION                                                                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If the file is not a theme file, states another format version, holds an unknown attribute, or would register under a predefined theme's name. |

#### __getitem__

```
__getitem__(attr: str) -> Any
```

Gets the associated configuration attribute.

Examples:

```
>>> from datachart.config import config
>>> config["font_general_color"]
'#000000'
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
'#000000'
```

| PARAMETER | DESCRIPTION                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------- |
| `attr`    | The attribute to retrieve. **TYPE:** `str`                                                              |
| `default` | The value to return, if the attribute is not present in the config. **TYPE:** `Any` **DEFAULT:** `None` |

| RETURNS | DESCRIPTION                                                           |
| ------- | --------------------------------------------------------------------- |
| `Any`   | The attribute value if present. Otherwise, returns the default value. |
