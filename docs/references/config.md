---
title: Config Module
---

# Config Module

::: datachart.config
    options:
        members: False
        heading_level: 2

## Choosing a Method

One `config` instance holds the style every chart is drawn with. Its methods change that style for the rest of the session, for one block of code, or from a file; the [Themes guide](../how-to-guides/styling/themes.ipynb) walks through them on a chart.

| I want to…                                        | Call                                                      | See |
| :------------------------------------------------ | :-------------------------------------------------------- | :-- |
| switch the look of every chart                    | `config.set_theme(THEME.INK)`                             | [set_theme](#datachart.config.Config.set_theme) |
| change a few attributes on top of the theme       | `config.update_config({"font_general_size": 12})`         | [update_config](#datachart.config.Config.update_config) |
| change the look for one block of code             | `with config.override(...)`, `with config.using_theme(...)` | [override](#datachart.config.Config.override), [using_theme](#datachart.config.Config.using_theme) |
| go back to the default theme                      | `config.reset_config()`                                   | [reset_config](#datachart.config.Config.reset_config) |
| add a theme of my own                             | `config.register_theme(name, theme)`, then `set_theme(name)` | [register_theme](#datachart.config.Config.register_theme) |
| see which names `set_theme` accepts               | `config.list_themes()`                                    | [list_themes](#datachart.config.Config.list_themes) |
| share a theme as a file                           | `config.save_theme(path)`, `config.load_theme(path)`      | [save_theme](#datachart.config.Config.save_theme), [load_theme](#datachart.config.Config.load_theme) |
| read one attribute                                | `config.get("font_general_size")`                         | [get](#datachart.config.Config.get) |

The attribute names are the keys of [`StyleAttrs`](typings.md#datachart.typings.StyleAttrs): the theme-level keys on the [typings](typings.md#theme-style) page and each chart's own keys on its [reference page](charts/index.md). The theme names are the members of [`THEME`](constants.md#datachart.constants.THEME).

## Attributes

::: datachart.config.config

## Classes

::: datachart.config.Config
    options:
        filters: ["!^__init__$", "!^__repr__$"]
