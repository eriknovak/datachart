---
title: Themes Module
---

# Themes Module

::: datachart.themes
    options:
        members: False
        heading_level: 2
        annotations_path: brief

## Choosing a Theme

Every theme is a complete [`StyleAttrs`](typings.md#datachart.typings.StyleAttrs) dictionary, named for its visual trait. Apply one with [`config.set_theme`](config.md#datachart.config.Config.set_theme) and the member of [`THEME`](constants.md#datachart.constants.THEME) in the last column; the [Theme Gallery](../how-to-guides/styling/theme-gallery.ipynb) shows each on six charts, and the [Themes guide](../how-to-guides/styling/themes.ipynb) shows how to adjust one or build your own.

| Theme                                                | Look                                                                  | Apply with |
| :--------------------------------------------------- | :-------------------------------------------------------------------- | :--------- |
| [`DEFAULT_THEME`](#datachart.themes.DEFAULT_THEME)     | the package's baseline palette and furniture                          | `THEME.DEFAULT` |
| [`GREYSCALE_THEME`](#datachart.themes.GREYSCALE_THEME) | greys only, for print without color                                   | `THEME.GREYSCALE` |
| [`INK_THEME`](#datachart.themes.INK_THEME)             | dark-ink accents, print-ready                                         | `THEME.INK` |
| [`HATCH_THEME`](#datachart.themes.HATCH_THEME)         | a hatch cycle, black edges, dotted grid                               | `THEME.HATCH` |
| [`MINIMAL_THEME`](#datachart.themes.MINIMAL_THEME)     | accent violet, no spines, flat bars                                   | `THEME.MINIMAL` |
| [`MATERIAL_THEME`](#datachart.themes.MATERIAL_THEME)   | the Google palette, light grid                                        | `THEME.MATERIAL` |
| [`SKETCH_THEME`](#datachart.themes.SKETCH_THEME)       | hand-drawn: xkcd-style wobble and halo, Comic Neue font               | `THEME.SKETCH` |
| [`QUILL_THEME`](#datachart.themes.QUILL_THEME)         | black ink on white paper, pen-stroked lines, etched fills, IM Fell English font | `THEME.QUILL` |
| [`HARBOR_THEME`](#datachart.themes.HARBOR_THEME)       | navy and amber in lightness steps, colour-blind safe                  | `THEME.HARBOR` |
| [`MUTED_THEME`](#datachart.themes.MUTED_THEME)         | Tol's muted colours, dash and marker cycles, colour-blind safe        | `THEME.MUTED` |
| [`CONTRAST_THEME`](#datachart.themes.CONTRAST_THEME)   | lightness-stepped colours plus hatches, print-safe                    | `THEME.CONTRAST` |

## Themes

::: datachart.themes.DEFAULT_THEME
::: datachart.themes.GREYSCALE_THEME
::: datachart.themes.INK_THEME
::: datachart.themes.HATCH_THEME
::: datachart.themes.MINIMAL_THEME
::: datachart.themes.MATERIAL_THEME
::: datachart.themes.SKETCH_THEME
::: datachart.themes.QUILL_THEME
::: datachart.themes.HARBOR_THEME
::: datachart.themes.MUTED_THEME
::: datachart.themes.CONTRAST_THEME
