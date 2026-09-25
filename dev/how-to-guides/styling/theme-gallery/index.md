# Theme Gallery

Each predefined theme has a card here: a strip of its color swatches with hex codes, the sequential and diverging colormaps, and the font it sets in, its colour-blindness scores, and the same six signature charts rendered under that theme — grouped bars, lines, a fitted scatter, a box plot, a heatmap, and a twin-axis [`Panel`](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md). The six charts cover every trait a theme can differ in: palette, edges and fills, line strokes and markers, bodies, value scales, and the furniture around them (spines, grid, ticks, legend). The themes are grouped by where they work best:

| Theme                                                   | Character                                                                  |
| ------------------------------------------------------- | -------------------------------------------------------------------------- |
| [Screen and presentations](#screen-and-presentations)   |                                                                            |
| [`THEME.DEFAULT`](#default)                             | Softened Okabe–Ito palette, colour-blind safe, open spines, soft grid.     |
| [`THEME.MATERIAL`](#material)                           | Google hues re-stepped for deutan readers, bottom spine only, light grid.  |
| [`THEME.MINIMAL`](#minimal)                             | Accent violet with five stepped greys, no spines, flat bars.               |
| [`THEME.HARBOR`](#harbor)                               | Navy and amber in lightness steps, colour-blind safe.                      |
| [`THEME.DARK`](#dark)                                   | Bright marks on a near-black page, light furniture, Viridis value scale.   |
| [Print and black-and-white](#print-and-black-and-white) |                                                                            |
| [`THEME.GREYSCALE`](#greyscale)                         | Five greys with hatch, dash and marker cycles, print-friendly.             |
| [`THEME.INK`](#ink)                                     | Lightness-stepped YlGnBu palette with navy ink accents.                    |
| [`THEME.HATCH`](#hatch)                                 | Six-entry hatch cycle, black edges, dotted grid.                           |
| [`THEME.MUTED`](#muted)                                 | Tol's muted colours, dash and marker cycles, colour-blind safe.            |
| [`THEME.CONTRAST`](#contrast)                           | Lightness-stepped colours plus hatches, print-safe.                        |
| [`THEME.MUTEDHATCH`](#muted-hatch)                      | Tol's muted colours under hatches, BuPu value scale.                       |
| [`THEME.SLATEHATCH`](#slate-hatch)                      | The hatch theme without rust: slate blue first, PuBu value scale.          |
| [Illustrative](#illustrative)                           |                                                                            |
| [`THEME.SKETCH`](#sketch)                               | Hand-drawn wobble and halo, Comic Neue font, no grid.                      |
| [`THEME.QUILL`](#quill)                                 | Black ink on white paper: pen strokes, etched fills, IM Fell English font. |

Themes also carry *defaults for chart settings*: every theme but `SKETCH` and `QUILL` shows a muted y-grid unless a chart call sets `show_grid` itself, and `HATCH` hatches bar series via its hatch cycle, which is why the very same chart code below renders with grids and hatches that differ per theme. An explicit setting always wins.

A theme with a different hue is not a new card: `derive_theme` in the [Themes guide](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/#deriving-a-theme-from-a-colormap) rebuilds any theme's palettes from a colormap in [COLORS](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.COLORS) and keeps its furniture.

The sample data and the two helpers behind every card are defined in a hidden cell. `show_swatches()` reads the palette, the colormaps and the font straight from the active [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md), so the strip always matches the theme as shipped. It closes with the theme's colour-blindness scores from [`score_palette`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.score_palette), as explained in the next section; `cvd_table()` lists them for every theme. `signature(pair)` builds the six charts with the very same code for every theme; `pair` supplies the two colors the twin-axis panel styles explicitly (one per axis), picked from the theme's own swatches. Each card opens with the one call that selects the theme.

## Colour-blindness suitability

A reader compares any two series on a chart, so every theme is scored on its worst pair of palette colours, not only on neighbouring ones. Each colour is passed through the Machado, Oliveira and Fernandes (2009) simulation of deuteranopia, protanopia and tritanopia at full severity, and the distance between the two closest colours is measured in the OKLab colour space (ΔE, ×100). *Normal* is the same distance without simulation, and *greyscale gap* is the smallest lightness step between two colours once the chart is printed without colour.

A theme **passes** when the worst pair stays at ΔE 8 or more for both deutan and protan readers and at 15 or more for everyone; between 6 and 8 it is **weak**, acceptable only where a second cue (dashes, markers, hatches) tells the series apart; below that it **fails**. Tritan scores are reported but not gated, since that deficiency is rare. The scoring is [`score_palette`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.score_palette), the same function `register_theme` and `derive_theme` warn through when a palette fails, and a test holds every predefined theme to the gate. `QUILL` has one ink and no score; `GREYSCALE` and `MINIMAL` separate their greys by lightness alone, which every reader sees alike, and carry pattern cycles or an accent for the rest.

```
cvd_table()
```

## Screen and presentations

Colorful categorical palettes for notebooks, dashboards and slides, on light furniture except `DARK`, which inverts it.

### Default

The modernized default: a softened Okabe–Ito palette closed with charcoal, so every pair of series stays apart for colour-blind readers; white bar edges, open spines, soft y-grid from the theme default.

Selected with [`THEME.DEFAULT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`DEFAULT_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.DEFAULT_THEME).

```
config.set_theme(THEME.DEFAULT)
show_swatches()
signature(pair=("#3B76B0", "#C24E2A")).show()
```

### Material

The Google hues in brand order, blue, red, yellow, green, cyan and violet, re-stepped in lightness so red and green stay apart for deutan readers; a bottom spine only and a light solid grid.

Selected with [`THEME.MATERIAL`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`MATERIAL_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.MATERIAL_THEME).

```
config.set_theme(THEME.MATERIAL)
show_swatches()
signature(pair=("#1A73E8", "#BC261D")).show()
```

### Minimal

Accent violet with five greys stepped in lightness, dark and light interleaved, no spines or tick marks, flat bars.

Selected with [`THEME.MINIMAL`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`MINIMAL_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.MINIMAL_THEME).

```
config.set_theme(THEME.MINIMAL)
show_swatches()
signature(pair=("#7048E8", "#1B242C")).show()
```

### Harbor

Navy to sky and amber to sand, stepped in lightness, with taupe and near-black closing the set. Two hue families keep the chart reading as one palette, and every pair of series stays apart for deutan, protan and tritan readers.

Selected with [`THEME.HARBOR`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`HARBOR_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.HARBOR_THEME).

```
config.set_theme(THEME.HARBOR)
show_swatches()
signature(pair=("#1F4E79", "#D08C3A")).show()
```

### Dark

Azure, amber, mint, rose, violet and a near-white, each lifted clear of the page, on a near-black figure with the plotting area a step lighter. Every furniture colour — spines, ticks, fonts, grid, legend frame, value labels, annotation boxes, heatmap frame and separators — carries a light counterpart, so the theme is complete without a single override. The value scale is Viridis, which reads dark to light and so rises off the panel. A heatmap cell label still follows its own cell, so a light cell keeps dark text.

Selected with [`THEME.DARK`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`DARK_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.DARK_THEME).

```
config.set_theme(THEME.DARK)
show_swatches()
signature(pair=("#63A6DE", "#DC5470")).show()
```

## Print and black-and-white

Themes that survive a greyscale printer or photocopier: greys with pattern cycles, navy ink over lightness-stepped blues and greens, hatches over muted print tones, and four whose colours stay apart for colour-blind readers and carry dashes, markers or hatches for the greyscale print.

### Greyscale

Five slate greys 0.16 apart in lightness, with hatch, dash and marker cycles so a sixth series still differs on paper; the same open spines and muted grid treatment.

Selected with [`THEME.GREYSCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`GREYSCALE_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.GREYSCALE_THEME).

```
config.set_theme(THEME.GREYSCALE)
show_swatches()
signature(pair=("#1A232B", "#9EA9B4")).show()
```

### Ink

Five YlGnBu samples stepped in lightness (`COLORS.PaperYlGnBu`), darkest and lightest first, with navy ink edges, print-ready.

Selected with [`THEME.INK`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`INK_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.INK_THEME).

```
config.set_theme(THEME.INK)
show_swatches()
signature(pair=("#1E2E85", "#299DC1")).show()
```

### Hatch

Black edges, dotted grid, and a six-entry hatch cycle applied per bar series, so grouped bars stay distinguishable in black-and-white print; the green sits deep so it stays apart from rust for deutan readers.

Selected with [`THEME.HATCH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`HATCH_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.HATCH_THEME).

```
config.set_theme(THEME.HATCH)
show_swatches()
signature(pair=("#B5563A", "#5A6F86")).show()
```

### Muted

Indigo, cyan, sand, rose and wine from Paul Tol's muted scheme, every pair distinct for deutan, protan and tritan readers. Lines also differ by dash and scatter points by marker, bars carry black edges and the grid is dotted, so a figure survives a greyscale print.

Selected with [`THEME.MUTED`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`MUTED_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.MUTED_THEME).

```
config.set_theme(THEME.MUTED)
show_swatches()
signature(pair=("#332288", "#CC6677")).show()
```

### Contrast

Navy, straw, dusty rose, charcoal and grey, each a clear lightness step from the next, so a photocopy still tells the series apart; bars take a hatch cycle and black edges, lines a dash cycle, scatter points a marker cycle.

Selected with [`THEME.CONTRAST`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`CONTRAST_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.CONTRAST_THEME).

```
config.set_theme(THEME.CONTRAST)
show_swatches()
signature(pair=("#1F4E79", "#B45C6A")).show()
```

### Muted hatch

The five muted colours of `MUTED` under the hatch cycle of `CONTRAST`, so bars survive a greyscale print by pattern as well as colour. The value scale is BuPu, the family of indigo and wine, instead of YlOrBr.

Selected with [`THEME.MUTEDHATCH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`MUTEDHATCH_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.MUTEDHATCH_THEME).

```
config.set_theme(THEME.MUTEDHATCH)
show_swatches()
signature(pair=("#332288", "#CC6677")).show()
```

### Slate hatch

The `HATCH` theme without rust: slate blue, sand, wine, green, orchid and sky blue under black edges, hatches and a dotted grid, every pair distinct for deutan and protan readers. The value scale is PuBu.

Selected with [`THEME.SLATEHATCH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`SLATEHATCH_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.SLATEHATCH_THEME).

```
config.set_theme(THEME.SLATEHATCH)
show_swatches()
signature(pair=("#4F6D8F", "#743538")).show()
```

## Illustrative

Hand-drawn looks for explainers, blog posts and talks, where a chart should read as a drawing rather than a measurement.

### Sketch

Hand-drawn: wobbled paths, series lines cut out by a white halo, thick spines and lines, no grid, and the Comic Neue font, downloaded on first use, so the look is the same on every machine. The wobble and halo are theme attributes applied at render time, so nothing changes in matplotlib's global settings; the halo sits under line, radial and regression lines only, and a chart's `style` can set `plot_sketch_halo_width` to `0` where many lines overlap. The green is greyed towards sage so it stays apart from vermilion for deutan readers.

Selected with [`THEME.SKETCH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`SKETCH_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.SKETCH_THEME).

```
config.set_theme(THEME.SKETCH)
show_swatches()
signature(pair=("#3F84A3", "#E4572E")).show()
```

### Quill

Black ink on white paper, as a quill and an etching needle would draw it. There is one ink only, so series differ by line style, marker and etching, never by color. Series lines are broad-nib pen strokes whose width follows the pen's direction. Bars, areas and bodies are etched by hand instead of tiled with a hatch, with a faint ink wash under the bars and bodies. A value scale (heatmap, calendar, hexbin, filled contour) reads as steps of etch density; where a chart asks for a colorbar, a legend of the steps takes its place. Text is set in the IM Fell English font, downloaded on first use, titles in its italic. Like the sketch look, every effect is a theme attribute applied at render time, so nothing changes in matplotlib's global settings.

Selected with [`THEME.QUILL`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`QUILL_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.QUILL_THEME).

```
config.set_theme(THEME.QUILL)
show_swatches()
signature(pair=("#1A120A", "#1A120A")).show()
```

______________________________________________________________________

Applying a theme replaces the whole global configuration, so remember to call `config.set_theme(...)` (or `config.reset_config()`) before building the charts it should style. See the [themes how-to](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/index.md) for customizing themes attribute by attribute.

```
config.reset_config()
```
