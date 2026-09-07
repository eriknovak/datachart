# Theme Gallery

This gallery renders the same suite of example charts — the basic chart types plus research-style figures — under each of the seven predefined themes, composed into one grid per chart group so the whole suite is visible at a glance. The groups follow the [charts index](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/index.md) — trends and comparisons, distributions, relationships, composition — so each tile sits next to the guide that documents it. The available themes are:

| Theme                           | Character                                                  |
| ------------------------------- | ---------------------------------------------------------- |
| [`THEME.DEFAULT`](#default)     | Tableau-style categorical palette, open spines, soft grid. |
| [`THEME.GREYSCALE`](#greyscale) | Monochrome, print-friendly.                                |
| [`THEME.INK`](#ink)             | Diversified YlGnBu palette with navy ink accents.          |
| [`THEME.MINIMAL`](#minimal)     | Accent blue with deep grays, no spines, flat bars.         |
| [`THEME.MATERIAL`](#material)   | Google palette, bottom spine only, light grid.             |
| [`THEME.HATCH`](#hatch)         | Hatch cycle, black edges, dotted grid, value labels.       |
| [`THEME.SKETCH`](#sketch)       | Hand-drawn wobble and halo, Comic Neue font, no grid.      |

Themes also carry *defaults for chart settings*: every theme but `SKETCH` shows a muted y-grid unless a chart call sets `show_grid` itself, `MINIMAL`, `MATERIAL`, and `HATCH` label bar values by default, and `HATCH` hatches bar series via its hatch cycle — which is why the very same chart code below renders with grids, value labels, and hatches that differ per theme. An explicit setting always wins.

The small-multiples example is itself a `Grid`; grid figures nest inside `Grid`, so it takes one cell of each theme's composition grid.

The sample data shared by every theme suite is defined in a hidden cell.

Each theme section opens with the one call that selects it; the whole suite is then built by one function (in a hidden cell), so every theme renders the exact same chart code — grids, value labels, and hatches come from the theme's own defaults. `pair` supplies the two accent colors used where a chart styles lines explicitly (trend/forecast/walk examples). Intermediate figures that only exist to feed a `Panel` are closed as we go, so only the group grids are displayed. The small-multiples `Grid` nests as one composition cell and rebuilds its own layout there; the nested charts on the block's edges keep their y-axes inline with the gallery column's axes.

## Default

The modernized default: Tableau-style palette, white bar edges, open spines, soft y-grid from the theme default.

Selected with [`THEME.DEFAULT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`DEFAULT_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.DEFAULT_THEME).

```
from datachart.config import config
from datachart.constants import THEME

config.set_theme(THEME.DEFAULT)
```

### Trends and Comparisons

### Distributions

### Relationships

### Flows

### Part of a Whole

### Composition

## Greyscale

Monochrome and print-friendly, with the same open spines and muted grid treatment.

Selected with [`THEME.GREYSCALE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`GREYSCALE_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.GREYSCALE_THEME).

```
from datachart.config import config
from datachart.constants import THEME

config.set_theme(THEME.GREYSCALE)
```

### Trends and Comparisons

### Distributions

### Relationships

### Flows

### Part of a Whole

### Composition

## Ink

The diversified YlGnBu palette (`COLORS.PaperYlGnBu`) with navy ink edges, print-ready.

Selected with [`THEME.INK`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`INK_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.INK_THEME).

```
from datachart.config import config
from datachart.constants import THEME

config.set_theme(THEME.INK)
```

### Trends and Comparisons

### Distributions

### Relationships

### Flows

### Part of a Whole

### Composition

## Minimal

Accent blue with deep grays, no spines or tick marks, flat bars — and bar value labels on by default.

Selected with [`THEME.MINIMAL`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`MINIMAL_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.MINIMAL_THEME).

```
from datachart.config import config
from datachart.constants import THEME

config.set_theme(THEME.MINIMAL)
```

### Trends and Comparisons

### Distributions

### Relationships

### Flows

### Part of a Whole

### Composition

## Material

The Google palette with a bottom spine only and a light solid grid; value labels default to on.

Selected with [`THEME.MATERIAL`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`MATERIAL_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.MATERIAL_THEME).

```
from datachart.config import config
from datachart.constants import THEME

config.set_theme(THEME.MATERIAL)
```

### Trends and Comparisons

### Distributions

### Relationships

### Flows

### Part of a Whole

### Composition

## Hatch

Black edges, dotted grid — and the hatch cycle (`""`, `"//"`, `".."`) applied per bar series, so grouped bars stay distinguishable in black-and-white print.

Selected with [`THEME.HATCH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`HATCH_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.HATCH_THEME).

```
from datachart.config import config
from datachart.constants import THEME

config.set_theme(THEME.HATCH)
```

### Trends and Comparisons

### Distributions

### Relationships

### Flows

### Part of a Whole

### Composition

## Sketch

Hand-drawn: wobbled paths, series lines cut out by a white halo, thick spines and lines, no grid, and the bundled Comic Neue font, so the look is the same on every machine. The wobble and halo are theme attributes applied at render time, so nothing changes in matplotlib's global settings; the halo sits under line, radial and regression lines only, and a chart's `style` can set `plot_sketch_halo_width` to `0` where many lines overlap, as the random walks below do.

Selected with [`THEME.SKETCH`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME); the full attribute set is [`SKETCH_THEME`](https://eriknovak.github.io/datachart/dev/references/themes/#datachart.themes.SKETCH_THEME).

```
from datachart.config import config
from datachart.constants import THEME

config.set_theme(THEME.SKETCH)
```

### Trends and Comparisons

### Distributions

### Relationships

### Flows

### Part of a Whole

### Composition

______________________________________________________________________

Applying a theme replaces the whole global configuration, so remember to call `config.set_theme(...)` (or `config.reset_config()`) before building the charts it should style. See the [themes how-to](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/index.md) for customizing themes attribute by attribute.

```
config.reset_config()
```
