# Theme Gallery

This gallery renders the same suite of example charts — the basic chart types plus research-style figures — under each of the six predefined themes, composed into a single grid per theme so the whole suite is visible at a glance. The available themes are:

| Theme             | Character                                                  |
| ----------------- | ---------------------------------------------------------- |
| `THEME.DEFAULT`   | Tableau-style categorical palette, open spines, soft grid. |
| `THEME.GREYSCALE` | Monochrome, print-friendly.                                |
| `THEME.INK`       | Diversified YlGnBu palette with navy ink accents.          |
| `THEME.MINIMAL`   | Accent blue with deep grays, no spines, flat bars.         |
| `THEME.MATERIAL`  | Google palette, bottom spine only, light grid.             |
| `THEME.HATCH`     | Hatch cycle, black edges, dotted grid, value labels.       |

Themes also carry *defaults for chart settings*: every theme shows a muted y-grid unless a chart call sets `show_grid` itself, `MINIMAL`, `MATERIAL`, and `HATCH` label bar values by default, and `HATCH` hatches bar series via its hatch cycle — which is why the very same chart code below renders with grids, value labels, and hatches that differ per theme. An explicit setting always wins.

The small-multiples example is itself a `Grid`; grid figures nest inside `Grid` (ADR 0006), so it takes the final cell of each theme's gallery grid.

The sample data shared by every theme suite is defined in a hidden cell.

The whole suite is built by one function (in a hidden cell), so every theme renders the exact same chart code — grids, value labels, and hatches come from the theme's own defaults. `pair` supplies the two accent colors used where a chart styles lines explicitly (trend/forecast/walk examples). Intermediate figures that only exist to feed a `Panel` are closed as we go, so only the final grid is displayed. The small-multiples `Grid` nests as the last gallery cell and rebuilds its own layout there; the nested charts on the block's edges keep their y-axes inline with the gallery column's axes.

## Default

The modernized default: Tableau-style palette, white bar edges, open spines, soft y-grid from the theme default.

```
grid = render_gallery(THEME.DEFAULT, pair=("#4E79A7", "#E15759"))
grid.show()
```

## Greyscale

Monochrome and print-friendly, with the same open spines and muted grid treatment.

```
grid = render_gallery(THEME.GREYSCALE, pair=("#252525", "#969696"))
grid.show()
```

## Ink

The diversified YlGnBu palette (`COLORS.PaperYlGnBu`) with navy ink edges, print-ready.

```
grid = render_gallery(THEME.INK, pair=("#225EA8", "#41B6C4"))
grid.show()
```

## Minimal

Accent blue with deep grays, no spines or tick marks, flat bars — and bar value labels on by default.

```
grid = render_gallery(THEME.MINIMAL, pair=("#2B7FFF", "#525C66"))
grid.show()
```

## Material

The Google palette with a bottom spine only and a light solid grid; value labels default to on.

```
grid = render_gallery(THEME.MATERIAL, pair=("#4285F4", "#EA4335"))
grid.show()
```

## Hatch

Black edges, dotted grid — and the hatch cycle (`""`, `"//"`, `".."`) applied per bar series, so grouped bars stay distinguishable in black-and-white print.

```
grid = render_gallery(THEME.HATCH, pair=("#5B84C4", "#C85450"))
grid.show()
```

______________________________________________________________________

Applying a theme replaces the whole global configuration, so remember to call `config.set_theme(...)` (or `config.reset_config()`) before building the charts it should style. See the [themes how-to](https://eriknovak.github.io/datachart/0.8.1/how-to-guides/styling/themes/index.md) for customizing themes attribute by attribute.

```
config.reset_config()
```
