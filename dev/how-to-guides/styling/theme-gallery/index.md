# Theme Gallery

This gallery renders the same suite of example charts — the basic chart types plus research-style figures — under each of the six predefined themes, composed into one grid per chart group so the whole suite is visible at a glance. The groups follow the [charts index](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/index.md) — trends and comparisons, distributions, relationships, composition — so each tile sits next to the guide that documents it. The available themes are:

| Theme             | Character                                                  |
| ----------------- | ---------------------------------------------------------- |
| `THEME.DEFAULT`   | Tableau-style categorical palette, open spines, soft grid. |
| `THEME.GREYSCALE` | Monochrome, print-friendly.                                |
| `THEME.INK`       | Diversified YlGnBu palette with navy ink accents.          |
| `THEME.MINIMAL`   | Accent blue with deep grays, no spines, flat bars.         |
| `THEME.MATERIAL`  | Google palette, bottom spine only, light grid.             |
| `THEME.HATCH`     | Hatch cycle, black edges, dotted grid, value labels.       |

Themes also carry *defaults for chart settings*: every theme shows a muted y-grid unless a chart call sets `show_grid` itself, `MINIMAL`, `MATERIAL`, and `HATCH` label bar values by default, and `HATCH` hatches bar series via its hatch cycle — which is why the very same chart code below renders with grids, value labels, and hatches that differ per theme. An explicit setting always wins.

The small-multiples example is itself a `Grid`; grid figures nest inside `Grid`, so it takes one cell of each theme's composition grid.

The sample data shared by every theme suite is defined in a hidden cell.

The whole suite is built by one function (in a hidden cell), so every theme renders the exact same chart code — grids, value labels, and hatches come from the theme's own defaults. `pair` supplies the two accent colors used where a chart styles lines explicitly (trend/forecast/walk examples). Intermediate figures that only exist to feed a `Panel` are closed as we go, so only the group grids are displayed. The small-multiples `Grid` nests as one composition cell and rebuilds its own layout there; the nested charts on the block's edges keep their y-axes inline with the gallery column's axes.

## Default

The modernized default: Tableau-style palette, white bar edges, open spines, soft y-grid from the theme default.

### Trends and Comparisons

### Distributions

### Relationships

### Flows

```
gallery["Flows"].show()
```

### Composition

## Greyscale

Monochrome and print-friendly, with the same open spines and muted grid treatment.

### Trends and Comparisons

### Distributions

### Relationships

### Flows

```
gallery["Flows"].show()
```

### Composition

## Ink

The diversified YlGnBu palette (`COLORS.PaperYlGnBu`) with navy ink edges, print-ready.

### Trends and Comparisons

### Distributions

### Relationships

### Flows

```
gallery["Flows"].show()
```

### Composition

## Minimal

Accent blue with deep grays, no spines or tick marks, flat bars — and bar value labels on by default.

### Trends and Comparisons

### Distributions

### Relationships

### Flows

```
gallery["Flows"].show()
```

### Composition

## Material

The Google palette with a bottom spine only and a light solid grid; value labels default to on.

### Trends and Comparisons

### Distributions

### Relationships

### Flows

```
gallery["Flows"].show()
```

### Composition

## Hatch

Black edges, dotted grid — and the hatch cycle (`""`, `"//"`, `".."`) applied per bar series, so grouped bars stay distinguishable in black-and-white print.

### Trends and Comparisons

### Distributions

### Relationships

### Flows

```
gallery["Flows"].show()
```

### Composition

______________________________________________________________________

Applying a theme replaces the whole global configuration, so remember to call `config.set_theme(...)` (or `config.reset_config()`) before building the charts it should style. See the [themes how-to](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/index.md) for customizing themes attribute by attribute.

```
config.reset_config()
```
