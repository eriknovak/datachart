# Theme Gallery

Each predefined theme has a card here: a strip of its color swatches with hex codes, the sequential colormap, and the font it sets in, followed by the same six signature charts rendered under that theme — grouped bars, lines, a fitted scatter, a box plot, a heatmap, and a twin-axis [`Panel`](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md). The six charts cover every trait a theme can differ in: palette, edges and fills, line strokes and markers, bodies, value scales, and the furniture around them (spines, grid, ticks, legend). The themes are grouped by where they work best:

| Theme                                                   | Character                                                                  |
| ------------------------------------------------------- | -------------------------------------------------------------------------- |
| [Screen and presentations](#screen-and-presentations)   |                                                                            |
| [`THEME.DEFAULT`](#default)                             | Tableau-style categorical palette, open spines, soft grid.                 |
| [`THEME.MATERIAL`](#material)                           | Google palette, bottom spine only, light grid.                             |
| [`THEME.MINIMAL`](#minimal)                             | Accent blue with deep grays, no spines, flat bars.                         |
| [Print and black-and-white](#print-and-black-and-white) |                                                                            |
| [`THEME.GREYSCALE`](#greyscale)                         | Monochrome, print-friendly.                                                |
| [`THEME.INK`](#ink)                                     | Diversified YlGnBu palette with navy ink accents.                          |
| [`THEME.HATCH`](#hatch)                                 | Hatch cycle, black edges, dotted grid.                                     |
| [Illustrative](#illustrative)                           |                                                                            |
| [`THEME.SKETCH`](#sketch)                               | Hand-drawn wobble and halo, Comic Neue font, no grid.                      |
| [`THEME.QUILL`](#quill)                                 | Black ink on white paper: pen strokes, etched fills, IM Fell English font. |

Themes also carry *defaults for chart settings*: every theme but `SKETCH` and `QUILL` shows a muted y-grid unless a chart call sets `show_grid` itself, and `HATCH` hatches bar series via its hatch cycle, which is why the very same chart code below renders with grids and hatches that differ per theme. An explicit setting always wins.

The sample data and the two helpers behind every card are defined in a hidden cell. `show_swatches()` reads the palette, sequential colormap and font straight from the active [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md), so the strip always matches the theme as shipped. `signature(pair)` builds the six charts with the very same code for every theme; `pair` supplies the two colors the twin-axis panel styles explicitly (one per axis), picked from the theme's own swatches. Each card opens with the one call that selects the theme.

## Screen and presentations

Colorful categorical palettes on light furniture, for notebooks, dashboards and slides.

### Default

The modernized default: Tableau-style palette, white bar edges, open spines, soft y-grid from the theme default.

Selected with [`THEME.DEFAULT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`DEFAULT_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.DEFAULT_THEME).

```
config.set_theme(THEME.DEFAULT)
show_swatches()
signature(pair=("#4E79A7", "#E15759")).show()
```

### Material

The Google palette with a bottom spine only and a light solid grid.

Selected with [`THEME.MATERIAL`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`MATERIAL_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.MATERIAL_THEME).

```
config.set_theme(THEME.MATERIAL)
show_swatches()
signature(pair=("#4285F4", "#EA4335")).show()
```

### Minimal

Accent blue with deep grays, no spines or tick marks, flat bars.

Selected with [`THEME.MINIMAL`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`MINIMAL_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.MINIMAL_THEME).

```
config.set_theme(THEME.MINIMAL)
show_swatches()
signature(pair=("#2B7FFF", "#525C66")).show()
```

## Print and black-and-white

Themes that survive a greyscale printer or photocopier: one that is monochrome by design, one whose palette stays distinct on paper, and one that tells series apart by pattern.

### Greyscale

Monochrome and print-friendly, with the same open spines and muted grid treatment.

Selected with [`THEME.GREYSCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`GREYSCALE_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.GREYSCALE_THEME).

```
config.set_theme(THEME.GREYSCALE)
show_swatches()
signature(pair=("#252525", "#969696")).show()
```

### Ink

The diversified YlGnBu palette (`COLORS.PaperYlGnBu`) with navy ink edges, print-ready.

Selected with [`THEME.INK`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`INK_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.INK_THEME).

```
config.set_theme(THEME.INK)
show_swatches()
signature(pair=("#225EA8", "#41B6C4")).show()
```

### Hatch

Black edges, dotted grid, and the hatch cycle (`""`, `"//"`, `".."`) applied per bar series, so grouped bars stay distinguishable in black-and-white print.

Selected with [`THEME.HATCH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`HATCH_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.HATCH_THEME).

```
config.set_theme(THEME.HATCH)
show_swatches()
signature(pair=("#5B84C4", "#C85450")).show()
```

## Illustrative

Hand-drawn looks for explainers, blog posts and talks, where a chart should read as a drawing rather than a measurement.

### Sketch

Hand-drawn: wobbled paths, series lines cut out by a white halo, thick spines and lines, no grid, and the bundled Comic Neue font, so the look is the same on every machine. The wobble and halo are theme attributes applied at render time, so nothing changes in matplotlib's global settings; the halo sits under line, radial and regression lines only, and a chart's `style` can set `plot_sketch_halo_width` to `0` where many lines overlap.

Selected with [`THEME.SKETCH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`SKETCH_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.SKETCH_THEME).

```
config.set_theme(THEME.SKETCH)
show_swatches()
signature(pair=("#2E86AB", "#E4572E")).show()
```

### Quill

Black ink on white paper, as a quill and an etching needle would draw it. There is one ink only, so series differ by line style, marker and etching, never by color. Series lines are broad-nib pen strokes whose width follows the pen's direction. Bars, areas and bodies are etched by hand instead of tiled with a hatch, with a faint ink wash under the bars and bodies. A value scale (heatmap, calendar, hexbin, filled contour) reads as steps of etch density; where a chart asks for a colorbar, a legend of the steps takes its place. Text is set in the bundled IM Fell English font, titles in its italic. Like the sketch look, every effect is a theme attribute applied at render time, so nothing changes in matplotlib's global settings.

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
