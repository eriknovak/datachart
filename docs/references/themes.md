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

Every theme is a complete [`StyleAttrs`](typings.md#datachart.typings.StyleAttrs) dictionary, named for its look and listed here by where it works best. Apply one with [`config.set_theme`](config.md#datachart.config.Config.set_theme) and the member of [`THEME`](constants.md#datachart.constants.THEME) in the last column; the [Theme Gallery](../how-to-guides/styling/theme-gallery.ipynb) shows each on six charts, and the [Themes guide](../how-to-guides/styling/themes.ipynb) shows how to adjust one or build your own. [`derive_theme`](#datachart.themes.derive_theme) rebuilds any theme's palettes from a lead, keeps its furniture, and composes [`TRAIT`](constants.md#datachart.constants.TRAIT) members on top; the harbor, muted, contrast, hatch, muted-hatch and slate-hatch themes are built that way from the default theme, a named `COLORS` lead and one or two traits. [`score_palette`](#datachart.themes.score_palette) reports how a series palette holds up for colour-blind readers; every predefined theme passes its gate.

| Theme                                                | Look                                                                  | Apply with |
| :--------------------------------------------------- | :-------------------------------------------------------------------- | :--------- |
| **Screen and presentations**                         |                                                                       |            |
| [`DEFAULT_THEME`](#datachart.themes.DEFAULT_THEME)     | softened Okabe–Ito palette, colour-blind safe, baseline furniture     | `THEME.DEFAULT` |
| [`MATERIAL_THEME`](#datachart.themes.MATERIAL_THEME)   | the Google hues re-stepped for deutan readers, light grid             | `THEME.MATERIAL` |
| [`MINIMAL_THEME`](#datachart.themes.MINIMAL_THEME)     | accent violet and five stepped greys, no spines, flat bars            | `THEME.MINIMAL` |
| [`HARBOR_THEME`](#datachart.themes.HARBOR_THEME)       | navy and amber in lightness steps, colour-blind safe                  | `THEME.HARBOR` |
| [`DARK_THEME`](#datachart.themes.DARK_THEME)           | bright marks on a near-black page, light furniture, Viridis value scale | `THEME.DARK` |
| **Print and black-and-white**                        |                                                                       |            |
| [`GREYSCALE_THEME`](#datachart.themes.GREYSCALE_THEME) | five greys with hatch, dash and marker cycles, for print without color | `THEME.GREYSCALE` |
| [`INK_THEME`](#datachart.themes.INK_THEME)             | lightness-stepped blues and greens, navy ink edges, print-ready       | `THEME.INK` |
| [`HATCH_THEME`](#datachart.themes.HATCH_THEME)         | a six-entry hatch cycle, black edges, light grid                      | `THEME.HATCH` |
| [`MUTED_THEME`](#datachart.themes.MUTED_THEME)         | Tol's muted colours, dash and marker cycles, colour-blind safe        | `THEME.MUTED` |
| [`CONTRAST_THEME`](#datachart.themes.CONTRAST_THEME)   | lightness-stepped colours plus hatches, print-safe                    | `THEME.CONTRAST` |
| [`MUTEDHATCH_THEME`](#datachart.themes.MUTEDHATCH_THEME) | Tol's muted colours under hatches, BuPu value scale | `THEME.MUTEDHATCH` |
| [`SLATEHATCH_THEME`](#datachart.themes.SLATEHATCH_THEME) | the hatch theme without rust, slate blue first, PuBu value scale | `THEME.SLATEHATCH` |
| **Illustrative**                                     |                                                                       |            |
| [`SKETCH_THEME`](#datachart.themes.SKETCH_THEME)       | hand-drawn: xkcd-style wobble and halo, Comic Neue font               | `THEME.SKETCH` |
| [`QUILL_THEME`](#datachart.themes.QUILL_THEME)         | black ink on white paper, pen-stroked lines, etched fills, IM Fell English font | `THEME.QUILL` |

## Deriving a Theme

::: datachart.themes.derive_theme

## Scoring a Palette

::: datachart.themes.score_palette

::: datachart.themes.PaletteScore

## Themes

::: datachart.themes.DEFAULT_THEME
::: datachart.themes.MATERIAL_THEME
::: datachart.themes.MINIMAL_THEME
::: datachart.themes.HARBOR_THEME
::: datachart.themes.DARK_THEME
::: datachart.themes.GREYSCALE_THEME
::: datachart.themes.INK_THEME
::: datachart.themes.HATCH_THEME
::: datachart.themes.MUTED_THEME
::: datachart.themes.CONTRAST_THEME
::: datachart.themes.MUTEDHATCH_THEME
::: datachart.themes.SLATEHATCH_THEME
::: datachart.themes.SKETCH_THEME
::: datachart.themes.QUILL_THEME
