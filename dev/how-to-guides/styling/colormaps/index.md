# Colormaps

A palette is named wherever a theme asks for colors: the two general palettes, the heatmap colormap, and the parallel-coordinates hues. The name is resolved through [pypalettes](https://y-sunflower.github.io/pypalettes/), which gives access to over 2500 palettes; the [COLORS](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.COLORS) constant is a curated selection of them, rendered on this page. Which kind of palette a role wants:

| Role                                              | Attribute                                             | Kind                    |
| ------------------------------------------------- | ----------------------------------------------------- | ----------------------- |
| Series sharing one axes                           | `color_general_multiple`                              | Categorical             |
| Single-color roles (network nodes, parallel ramp) | `color_general_singular`                              | Sequential              |
| Heatmap cells                                     | `plot_heatmap_cmap`                                   | Sequential              |
| Heatmap cells under a centred norm                | `plot_heatmap_cmap_diverging`                         | Diverging               |
| Parallel-coordinates hue                          | `color_parallel_hue`, `color_parallel_hue_continuous` | Categorical, sequential |

A palette asked for one color gives its last one, so a sequential palette yields one strong color and a graded set when several are asked for. The calendar heatmap, hexbin, and contour colormaps follow the heatmap's unless set. A heatmap drawn with `norm="centered"` or `norm="twoslope"` takes `plot_heatmap_cmap_diverging` in place of `plot_heatmap_cmap`, so a signed matrix reads its sign as a hue; see the [Heatmap guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/heatmap/#normalization). See the [Themes](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/index.md) guide for setting these attributes and building a theme around them.

Each palette below is shown as a continuous strip and as the six colors a chart with six series receives; hover a swatch for its hex code. A palette is passed as its `COLORS` value, or as the plain name string. A chip names a predefined theme that uses the palette and the role it plays there, and links to the theme's card in the [Theme Gallery](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/theme-gallery/index.md).

```
from datachart.constants import COLORS
```

## Sequential, Single Hue

One hue from light to dark, ordered by magnitude. The natural `color_general_singular` palette: a role that needs one color takes the dark end. Also the safest heatmap colormap.

## Sequential, Multiple Hues

Light to dark through two or more hues, which separates neighbouring values better than a single hue. Suited to heatmaps and value scales; the last color still serves a single series.

## Diverging

Two hues meeting at a neutral center, for values with a meaningful midpoint: differences from a baseline, correlations, gains and losses. Use with a heatmap `norm` centred on that value.

## Categorical

Distinct hues of similar weight, for series that are different in kind rather than in amount: the `color_general_multiple` palette. The six colors shown are the ones six series receive.

## Perceptually Uniform and Color-Blind Safe

Equal steps in value read as equal steps in color, and the palettes stay distinguishable under the common forms of color-vision deficiency. The first six are sequential, the Okabe-Ito pair categorical.

## Greyscale

For print and black-and-white reproduction; the greyscale themes pair it with hatching or markers to keep series apart.

## Datachart's Own

Two palettes registered by datachart rather than pypalettes, made for the ink theme's publication look. They cycle through their exact colors instead of interpolating, so the series colors are always the ones listed.

## Beyond the Constant

Any pypalettes name works where a `COLORS` value does. So does a single matplotlib color, which is a palette of one and repeats for every series, and a list of hex colors, which cycles through its exact colors like datachart's own palettes. The list is how the predefined themes define most of their series palettes, and how a custom theme states its own:

```
palettes("Antique", "#B5651D", ["#0B3954", "#FF6663", "#E0FF4F"])
```

## Using a Palette in a Theme

A palette is set through the attributes in the table above, here for one figure with `override`; a theme sets the same attributes once. The heatmap takes its own colormap, the bars the general series palette:

```
from datachart.charts import BarChart, Heatmap
from datachart.config import config
from datachart.utils import Grid

CELLS = {"z": [[r * c for c in range(1, 8)] for r in range(1, 7)]}
BARS = [[{"label": f"Q{q}", "y": 30 + 12 * s + 7 * q} for q in range(1, 5)] for s in range(4)]

with config.override(plot_heatmap_cmap=COLORS.Cividis, color_general_multiple=COLORS.OkabeIto):
    Grid(
        [[
            Heatmap(data=CELLS, title="Cividis cells", show_values=True),
            BarChart(data=BARS, title="Okabe-Ito series", subtitle=["A", "B", "C", "D"], show_legend=True),
        ]],
        figsize=(9, 3.2),
    ).show()
```
