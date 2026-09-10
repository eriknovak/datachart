# Config

This section showcases how to use the [datachart.config](https://eriknovak.github.io/datachart/dev/references/config/index.md) module to customize the global style of the `datachart` package: applying a theme, changing single attributes, scoping a change to one block, and saving a look to a file so it can be shared or reloaded.

Let's start by importing the necessary functions to help us work with the `datachart.config` module.

```
from datachart.config import config
```

```
from datachart.charts import BarChart
from datachart.constants import FIG_SIZE, THEME
```

The `config` instance is a global configuration that the users can interact with. It allows them to customize the global style of the `datachart` package.

Furthermore, the instance is of the [datachart.config.Config](https://eriknovak.github.io/datachart/dev/references/config/#datachart.config.Config) class.

## The Configuration Instance

The instance holds one style attribute per key of [StyleAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.StyleAttrs) and the name of the active theme. Read an attribute with `config.get` or by indexing:

```
config.get("font_general_size"), config["color_general_multiple"]
```

```
config.theme
```

The attribute names are the keys of the live configuration; the reference page documents each one:

```
len(config.config), list(config.config)[:5]
```

Charts read the configuration when they are built, so every change below applies to the charts created after it. The examples use the heights of the five tallest mountains:

```
MOUNTAINS = [
    {"label": "Everest", "y": 8849},
    {"label": "K2", "y": 8611},
    {"label": "Kangchenjunga", "y": 8586},
    {"label": "Lhotse", "y": 8516},
    {"label": "Makalu", "y": 8485},
]


def mountains(title):
    return BarChart(
        data=MOUNTAINS,
        title=title,
        ylabel="Height [m]",
        ymin=8000,
        figsize=FIG_SIZE.FULL_SHORT,
    )
```

## Customizing the Configuration

| Task                                    | Method                     | Section                                     |
| --------------------------------------- | -------------------------- | ------------------------------------------- |
| Switch the look of every chart          | `set_theme`, `list_themes` | [Applying a Theme](#applying-a-theme)       |
| Change single attributes                | `update_config`            | [Updating Attributes](#updating-attributes) |
| Change the style for one block only     | `override`, `using_theme`  | [Scoping a Change](#scoping-a-change)       |
| Share a look as a file and load it back | `save_theme`, `load_theme` | [Theme Files](#theme-files)                 |
| Return to the default theme             | `reset_config`             | [Resetting](#resetting)                     |

### Applying a Theme

`list_themes` returns every name `set_theme` accepts: the predefined themes from [THEME](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME) plus any theme registered with `register_theme` or `load_theme`.

```
config.list_themes()
```

Applying a theme replaces the whole configuration and updates the active theme name; see the [themes guide](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/index.md) for the predefined themes and for registering your own.

```
config.set_theme(THEME.MINIMAL)
config.theme
```

```
mountains("The minimal theme").show()
```

### Updating Attributes

`update_config` changes individual attributes on top of the active theme. The change persists until the next `set_theme` or `reset_config`; unknown attribute names are skipped with a warning.

```
config.update_config({"font_title_size": 16, "color_general_singular": "#B5651D"})
mountains("Larger title, copper bars").show()
```

### Scoping a Change

A scope is a temporary style change that lasts for one `with` block: the configuration that entered the block is restored when it ends, also when the block raises. Any `set_theme` or `update_config` performed inside the block is discarded at exit.

`override` scopes attribute overrides, taking keyword arguments or a dictionary:

```
with config.override(font_title_size=10, color_general_singular="#4E79A7"):
    mountains("Inside the override scope").show()

mountains("After the override scope").show()
```

`using_theme` scopes a whole theme and restores the active theme name as well:

```
with config.using_theme(THEME.INK):
    print("inside:", config.theme)
    mountains("Inside the theme scope").show()

print("after:", config.theme)
```

The two nest in either order, each level restoring its own state. The scopes are plain save-and-restore on the global configuration, so they are neither thread-safe nor async-safe.

### Theme Files

`save_theme` writes a theme file: a JSON document carrying a name, a format version, and only the attributes that differ from the default theme, so the file stays short and reviewable. With no name it saves the live configuration, which lets a look assembled with `update_config` leave the process:

```
import tempfile
from pathlib import Path

folder = Path(tempfile.mkdtemp())
config.save_theme(folder / "house.json")
print((folder / "house.json").read_text())
```

A registered theme is saved by name:

```
config.save_theme(folder / "ink.json", name=THEME.INK)
```

`load_theme` registers the theme in a file and returns the name it registered under: the `name` argument, else the name in the file, else the file's stem. Loading only registers; apply the theme with `set_theme` or `using_theme`.

```
name = config.load_theme(folder / "house.json", name="house-v2")
config.set_theme(name)
config.theme, config["font_title_size"]
```

```
config.list_themes()
```

A file is validated the way `register_theme` validates a dictionary: missing attributes are filled from the default theme and an unknown attribute raises `ValueError`, so a hand-edited file cannot register a broken theme.

### Resetting

`reset_config` restores the default theme and resets the active theme name, discarding every override:

```
config.reset_config()
config.theme
```
