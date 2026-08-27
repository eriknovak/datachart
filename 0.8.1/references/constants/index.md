# Constants Module

## datachart.constants

Module containing the `constants`.

The `constants` module provides a set of predefined constants used in the package. These include figure size, format, style, and other figure manipulation values.

| CLASS               | DESCRIPTION                                    |
| ------------------- | ---------------------------------------------- |
| `FIG_SIZE`          | The predefined figure sizes.                   |
| `FIG_FORMAT`        | The supported figure formats.                  |
| `FONT_STYLE`        | The supported font styles.                     |
| `FONT_WEIGHT`       | The supported font weights.                    |
| `LINE_MARKER`       | The supported line markers.                    |
| `LINE_STYLE`        | The supported line styles.                     |
| `ARROW_STYLE`       | The supported text annotation connector looks. |
| `LINE_DRAW_STYLE`   | The supported line draw styles.                |
| `HATCH_STYLE`       | The supported hatch styles.                    |
| `LEGEND_ALIGN`      | The supported legend alignments.               |
| `LEGEND_LOCATION`   | The supported legend locations.                |
| `HISTOGRAM_TYPE`    | The supported histogram types.                 |
| `BAR_MODE`          | The supported bar modes.                       |
| `COLORS`            | The predefined colors.                         |
| `NORMALIZE`         | The supported normalization options.           |
| `ORIENTATION`       | The supported orientations.                    |
| `VIOLIN_INNER`      | The supported violin inner marks.              |
| `BANDWIDTH`         | The supported kernel density bandwidth rules.  |
| `RADIAL_TYPE`       | The supported radial chart visuals.            |
| `SWARM_MODE`        | The supported swarm plot modes.                |
| `DIRECTION`         | The supported angular directions.              |
| `VALUE_FORMAT`      | The predefined value formats.                  |
| `THEME`             | The predefined themes.                         |
| `EMPHASIS`          | The supported emphasis roles.                  |
| `SHOW_GRID`         | The supported show grid options.               |
| `SCALE`             | The supported scale options.                   |
| `ASPECT_RATIO`      | The supported aspect ratio options.            |
| `COLORBAR_LOCATION` | The supported colorbar locations.              |

## Figure Constants

### datachart.constants.FIG_SIZE

The predefined figure sizes.

All values are `(width, height)` in inches, matplotlib's `figsize` unit. Paper figures are anchored to the printable area of an A4 page with standard 2.5 cm margins — a 6.3 x 9.7 in (16.0 x 24.6 cm) text block. `FULL` spans the text-block width; `HALF` spans one of two columns separated by a 0.3 in (0.8 cm) gap (3.0 in / 7.6 cm each). Widths cross with a height — `SHORT` (2.4 in / 6.1 cm), `MEDIUM` (4.8 in / 12.2 cm), or `TALL` (7.2 in / 18.3 cm). Passed as the `figsize` chart setting.

Examples:

```
>>> from datachart.constants import FIG_SIZE
>>> FIG_SIZE.DEFAULT
(6.4, 4.8)
```

| ATTRIBUTE      | DESCRIPTION                                                                                                                        |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT`      | The default figure size. Equals to (6.4, 4.8) in (16.3 x 12.2 cm). **TYPE:** `Tuple[float, float]`                                 |
| `FULL_SHORT`   | The short, full-width figure size. Equals to (6.3, 2.4) in (16.0 x 6.1 cm). **TYPE:** `Tuple[float, float]`                        |
| `FULL_MEDIUM`  | The medium, full-width figure size. Equals to (6.3, 4.8) in (16.0 x 12.2 cm). **TYPE:** `Tuple[float, float]`                      |
| `FULL_TALL`    | The tall, full-width figure size. Equals to (6.3, 7.2) in (16.0 x 18.3 cm). **TYPE:** `Tuple[float, float]`                        |
| `HALF_SHORT`   | The short, half-width figure size. Equals to (3.0, 2.4) in (7.6 x 6.1 cm). **TYPE:** `Tuple[float, float]`                         |
| `HALF_MEDIUM`  | The medium, half-width figure size. Equals to (3.0, 4.8) in (7.6 x 12.2 cm). **TYPE:** `Tuple[float, float]`                       |
| `HALF_TALL`    | The tall, half-width figure size. Equals to (3.0, 7.2) in (7.6 x 18.3 cm). **TYPE:** `Tuple[float, float]`                         |
| `HALF_SQUARE`  | The square, half-width figure size. Equals to (3.0, 3.0) in (7.6 x 7.6 cm). **TYPE:** `Tuple[float, float]`                        |
| `A4_PORTRAIT`  | The A4 portrait printable-area figure size. Equals to (6.3, 9.7) in (16.0 x 24.6 cm). **TYPE:** `Tuple[float, float]`              |
| `A4_LANDSCAPE` | The A4 landscape printable-area figure size. Equals to (9.7, 6.3) in (24.6 x 16.0 cm). **TYPE:** `Tuple[float, float]`             |
| `SQUARE`       | The square figure size. Equals to (4.8, 4.8) in (12.2 x 12.2 cm). **TYPE:** `Tuple[float, float]`                                  |
| `SLIDE_16_9`   | The 16:9 slide figure size (PowerPoint/Google Slides). Equals to (13.33, 7.5) in (33.9 x 19.1 cm). **TYPE:** `Tuple[float, float]` |
| `SLIDE_4_3`    | The 4:3 slide figure size (PowerPoint/Google Slides). Equals to (10.0, 7.5) in (25.4 x 19.1 cm). **TYPE:** `Tuple[float, float]`   |
| `BEAMER_16_9`  | The 16:9 beamer frame figure size. Equals to (6.3, 3.54) in (16.0 x 9.0 cm). **TYPE:** `Tuple[float, float]`                       |
| `BEAMER_4_3`   | The 4:3 beamer frame figure size. Equals to (5.04, 3.78) in (12.8 x 9.6 cm). **TYPE:** `Tuple[float, float]`                       |

### datachart.constants.FIG_FORMAT

The supported figure formats.

Passed as the `format` argument of save_figure.

Examples:

```
>>> from datachart.constants import FIG_FORMAT
>>> FIG_FORMAT.DEFAULT
"png"
```

| ATTRIBUTE | DESCRIPTION                                                                |
| --------- | -------------------------------------------------------------------------- |
| `DEFAULT` | The default format. Same as FIG_FORMAT.PNG. **TYPE:** `str`                |
| `SVG`     | The svg format. Equals to "svg". **TYPE:** `str`                           |
| `PDF`     | The pdf format. Equals to "pdf". **TYPE:** `str`                           |
| `PNG`     | The png format. Equals to "png". **TYPE:** `str`                           |
| `WEBP`    | The webp format. Equals to "webp". **TYPE:** `str`                         |
| `EPS`     | The eps format (Encapsulated PostScript). Equals to "eps". **TYPE:** `str` |
| `JPG`     | The jpg format. Equals to "jpg". **TYPE:** `str`                           |
| `TIFF`    | The tiff format. Equals to "tiff". **TYPE:** `str`                         |

## Font Constants

### datachart.constants.FONT_STYLE

The supported font styles.

Examples:

```
>>> from datachart.constants import FONT_STYLE
>>> FONT_STYLE.DEFAULT
"normal"
```

| ATTRIBUTE | DESCRIPTION                                                        |
| --------- | ------------------------------------------------------------------ |
| `DEFAULT` | The default font style. Same as FONT_STYLE.NORMAL. **TYPE:** `str` |
| `NORMAL`  | The normal font style. Equals to "normal". **TYPE:** `str`         |
| `ITALIC`  | The italic font style. Equals to "italic". **TYPE:** `str`         |
| `OBLIQUE` | The oblique font style. Equals to "oblique". **TYPE:** `str`       |

### datachart.constants.FONT_WEIGHT

The supported font weights.

Used by the `font_*_weight` style attributes (general, title, subtitle, axis labels).

Examples:

```
>>> from datachart.constants import FONT_WEIGHT
>>> FONT_WEIGHT.DEFAULT
"normal"
```

| ATTRIBUTE     | DESCRIPTION                                                          |
| ------------- | -------------------------------------------------------------------- |
| `DEFAULT`     | The default font weight. Same as FONT_WEIGHT.NORMAL. **TYPE:** `str` |
| `ULTRA_LIGHT` | The ultra light font weight. Equals to "ultralight". **TYPE:** `str` |
| `LIGHT`       | The light font weight. Equals to "light". **TYPE:** `str`            |
| `NORMAL`      | The normal font weight. Equals to "normal". **TYPE:** `str`          |
| `MEDIUM`      | The medium font weight. Equals to "medium". **TYPE:** `str`          |
| `SEMIBOLD`    | The semibold font weight. Equals to "semibold". **TYPE:** `str`      |
| `BOLD`        | The bold font weight. Equals to "bold". **TYPE:** `str`              |
| `EXTRA_BOLD`  | The extra bold font weight. Equals to "extra bold". **TYPE:** `str`  |
| `HEAVY`       | The heavy font weight. Equals to "heavy". **TYPE:** `str`            |
| `BLACK`       | The black font weight. Equals to "black". **TYPE:** `str`            |

## Line Constants

### datachart.constants.LINE_MARKER

The supported line markers.

Used by the `plot_line_marker` (line charts) and `plot_scatter_marker` (scatter charts) style attributes.

Examples:

```
>>> from datachart.constants import LINE_MARKER
>>> LINE_MARKER.PIXEL
","
```

| ATTRIBUTE        | DESCRIPTION                                                    |
| ---------------- | -------------------------------------------------------------- |
| `NONE`           | No marker. Equals to "". **TYPE:** `str`                       |
| `PIXEL`          | The pixel line marker. Equals to ",". **TYPE:** `str`          |
| `POINT`          | The point line marker. Equals to ".". **TYPE:** `str`          |
| `CIRCLE`         | The circle line marker. Equals to "o". **TYPE:** `str`         |
| `DIAMOND`        | The diamond line marker. Equals to "D". **TYPE:** `str`        |
| `THIN_DIAMOND`   | The thin diamond line marker. Equals to "d". **TYPE:** `str`   |
| `TRIANGLE`       | The triangle (up) line marker. Equals to "^". **TYPE:** `str`  |
| `TRIANGLE_DOWN`  | The triangle down line marker. Equals to "v". **TYPE:** `str`  |
| `TRIANGLE_LEFT`  | The triangle left line marker. Equals to "\<". **TYPE:** `str` |
| `TRIANGLE_RIGHT` | The triangle right line marker. Equals to ">". **TYPE:** `str` |
| `SQUARE`         | The square line marker. Equals to "s". **TYPE:** `str`         |
| `PENTAGON`       | The pentagon line marker. Equals to "p". **TYPE:** `str`       |
| `HEXAGON`        | The hexagon line marker. Equals to "h". **TYPE:** `str`        |
| `STAR`           | The star line marker. Equals to "\*". **TYPE:** `str`          |
| `CROSS`          | The cross line marker. Equals to "x". **TYPE:** `str`          |
| `PLUS`           | The plus line marker. Equals to "+". **TYPE:** `str`           |
| `VLINE`          | The vertical line marker. Equals to "                          |
| `HLINE`          | The horizontal line marker. Equals to "\_". **TYPE:** `str`    |

### datachart.constants.LINE_STYLE

The supported line styles.

Used by the `plot_line_style` style attribute of line charts.

Examples:

```
>>> from datachart.constants import LINE_STYLE
>>> LINE_STYLE.SOLID
"-"
```

| ATTRIBUTE | DESCRIPTION                                             |
| --------- | ------------------------------------------------------- |
| `NONE`    | No line style. Equals to "". **TYPE:** `str`            |
| `SOLID`   | The solid line style. Equals to "-". **TYPE:** `str`    |
| `DASHED`  | The dashed line style. Equals to "--". **TYPE:** `str`  |
| `DASHDOT` | The dashdot line style. Equals to "-.". **TYPE:** `str` |
| `DOTTED`  | The dotted line style. Equals to ":". **TYPE:** `str`   |

### datachart.constants.LINE_DRAW_STYLE

The supported line draw styles.

Used by the `plot_line_drawstyle` style attribute of line charts.

Examples:

```
>>> from datachart.constants import LINE_DRAW_STYLE
>>> LINE_DRAW_STYLE.DEFAULT
"default"
```

| ATTRIBUTE    | DESCRIPTION                                                             |
| ------------ | ----------------------------------------------------------------------- |
| `DEFAULT`    | The default line draw style. Equals to "default". **TYPE:** `str`       |
| `STEPS_PRE`  | The pre-steps line draw style. Equals to "steps-pre". **TYPE:** `str`   |
| `STEPS_MID`  | The mid-steps line draw style. Equals to "steps-mid". **TYPE:** `str`   |
| `STEPS_POST` | The post-steps line draw style. Equals to "steps-post". **TYPE:** `str` |

### datachart.constants.ARROW_STYLE

The supported text annotation connector looks.

Used by the `plot_text_arrow_style` style attribute of text annotations. Each value names a complete connector look — the line shape, curvature, and the gap on the text side. A curved look bows toward the side with the most open space around the chart's data; `plot_text_arrow_curve` pins the bow exactly, and the other `plot_text_arrow_*` style attributes override single properties of the chosen look. A raw matplotlib arrow style string (e.g. `"-|>"`) is also accepted.

Examples:

```
>>> from datachart.constants import ARROW_STYLE
>>> ARROW_STYLE.CURVE
"curve"
```

| ATTRIBUTE     | DESCRIPTION                                                                                        |
| ------------- | -------------------------------------------------------------------------------------------------- |
| `CURVE`       | A curved plain line with a small text-side gap. The default. Equals to "curve". **TYPE:** `str`    |
| `CURVE_ARROW` | The same curve with an arrowhead at the target. Equals to "curve-arrow". **TYPE:** `str`           |
| `TOUCHING`    | A straight plain line starting flush at the text box border. Equals to "touching". **TYPE:** `str` |
| `ARROW`       | A straight line with an arrowhead at the target. Equals to "arrow". **TYPE:** `str`                |

## Style Constants

### datachart.constants.HATCH_STYLE

The supported hatch styles.

Used by the `plot_bar_hatch` and `plot_hist_hatch` style attributes, and by the `HATCH` theme's hatch cycle.

Examples:

```
>>> from datachart.constants import HATCH_STYLE
>>> HATCH_STYLE.DEFAULT
None
```

| ATTRIBUTE          | DESCRIPTION                                                      |
| ------------------ | ---------------------------------------------------------------- |
| `DEFAULT`          | The default hatch style. Equals to None. **TYPE:** `str`         |
| `DIAGONAL`         | The diagonal hatch style. Equals to "/". **TYPE:** `str`         |
| `BACK_DIAGONAL`    | The back diagonal hatch style. Equals to "\\". **TYPE:** `str`   |
| `VERTICAL`         | The vertical hatch style. Equals to "                            |
| `HORIZONTAL`       | The horizontal hatch style. Equals to "-". **TYPE:** `str`       |
| `CROSSED`          | The crossed hatch style. Equals to "+". **TYPE:** `str`          |
| `CROSSED_DIAGONAL` | The crossed diagonal hatch style. Equals to "x". **TYPE:** `str` |
| `DOTS`             | The dots hatch style. Equals to ".". **TYPE:** `str`             |
| `CIRCLES`          | The circles hatch style. Equals to "o". **TYPE:** `str`          |
| `STARS`            | The stars hatch style. Equals to "\*". **TYPE:** `str`           |

### datachart.constants.COLORS

The predefined colors using [pypalettes](https://y-sunflower.github.io/pypalettes/).

All palette names are valid pypalettes identifiers. You can use any of the 2500+ palettes available in pypalettes by passing the palette name as a string. Accepted anywhere a palette is: the `color_general_singular` and `color_general_multiple` config attributes, and the heatmap and parallel coords color settings. All predefined palettes are rendered in the [Colormaps guide](https://eriknovak.github.io/datachart/0.8.1/how-to-guides/styling/colormaps/index.md).

Examples:

```
>>> from datachart.constants import COLORS
>>> COLORS.Blues
'Blues'
```

| ATTRIBUTE        | DESCRIPTION                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| `Blues`          | Sequential blue palette. Equals to "Blues". **TYPE:** `str`                                       |
| `Greens`         | Sequential green palette. Equals to "Greens". **TYPE:** `str`                                     |
| `Oranges`        | Sequential orange palette. Equals to "Oranges". **TYPE:** `str`                                   |
| `Purples`        | Sequential purple palette. Equals to "Purples". **TYPE:** `str`                                   |
| `Reds`           | Sequential red palette. Equals to "Reds". **TYPE:** `str`                                         |
| `Sunset2`        | Multi-hue sunset palette. Equals to "Sunset2". **TYPE:** `str`                                    |
| `YlGnBu`         | Multi-hue yellow-green-blue palette. Equals to "YlGnBu". **TYPE:** `str`                          |
| `YlOrRd`         | Multi-hue yellow-orange-red palette. Equals to "YlOrRd". **TYPE:** `str`                          |
| `PuBuGn`         | Multi-hue purple-blue-green palette. Equals to "PuBuGn". **TYPE:** `str`                          |
| `GnBu`           | Multi-hue green-blue palette. Equals to "GnBu". **TYPE:** `str`                                   |
| `Egypt`          | Multi-hue Egypt palette. Equals to "Egypt". **TYPE:** `str`                                       |
| `Hiroshige`      | Multi-hue Hiroshige palette. Equals to "Hiroshige". **TYPE:** `str`                               |
| `Lake`           | Multi-hue lake palette. Equals to "Lake". **TYPE:** `str`                                         |
| `Neon`           | Multi-hue neon palette. Equals to "Neon". **TYPE:** `str`                                         |
| `RdBu`           | Diverging red-blue palette. Equals to "RdBu". **TYPE:** `str`                                     |
| `BrBG`           | Diverging brown-blue-green palette. Equals to "BrBG". **TYPE:** `str`                             |
| `PuOr`           | Diverging purple-orange palette. Equals to "PuOr". **TYPE:** `str`                                |
| `Spectral`       | Diverging spectral palette. Equals to "Spectral". **TYPE:** `str`                                 |
| `RdYlBu`         | Diverging red-yellow-blue palette. Equals to "RdYlBu". **TYPE:** `str`                            |
| `RdYlGn`         | Diverging red-yellow-green palette. Equals to "RdYlGn". **TYPE:** `str`                           |
| `Pastel`         | Soft pastel categorical palette. Equals to "Pastel". **TYPE:** `str`                              |
| `Set2`           | ColorBrewer Set2 categorical palette. Equals to "Set2". **TYPE:** `str`                           |
| `Accent`         | ColorBrewer Accent categorical palette. Equals to "Accent". **TYPE:** `str`                       |
| `Dark2`          | ColorBrewer Dark2 categorical palette. Equals to "Dark2". **TYPE:** `str`                         |
| `Paired`         | ColorBrewer Paired categorical palette (high contrast). Equals to "Paired". **TYPE:** `str`       |
| `Set1`           | ColorBrewer Set1 categorical palette (high contrast). Equals to "Set1". **TYPE:** `str`           |
| `Greys`          | Grayscale palette for monochrome visualizations. Equals to "Greys". **TYPE:** `str`               |
| `Viridis`        | Perceptually uniform, color-blind friendly. Equals to "Viridis". **TYPE:** `str`                  |
| `Cividis`        | Color-blind friendly (optimized for CVD). Equals to "Cividis". **TYPE:** `str`                    |
| `Inferno`        | Perceptually uniform, color-blind friendly. Equals to "Inferno". **TYPE:** `str`                  |
| `Plasma`         | Perceptually uniform, color-blind friendly. Equals to "Plasma". **TYPE:** `str`                   |
| `Magma`          | Perceptually uniform, color-blind friendly. Equals to "Magma". **TYPE:** `str`                    |
| `Turbo`          | Rainbow-like but perceptually better. Equals to "Turbo". **TYPE:** `str`                          |
| `OkabeIto`       | Okabe-Ito categorical palette, color-blind safe. Equals to "OkabeIto". **TYPE:** `str`            |
| `OkabeIto_Black` | Okabe-Ito palette including black. Equals to "OkabeIto_Black". **TYPE:** `str`                    |
| `Coolwarm`       | Diverging cool-warm palette. Equals to "coolwarm". **TYPE:** `str`                                |
| `Tab10`          | Tableau 10-color categorical palette. Equals to "tab10". **TYPE:** `str`                          |
| `Tab20`          | Tableau 20-color categorical palette. Equals to "tab20". **TYPE:** `str`                          |
| `PaperYlGnBu`    | Diversified YlGnBu categorical palette for publications. Equals to "PaperYlGnBu". **TYPE:** `str` |
| `PaperAccent`    | Two-color blue/red accent pair for publications. Equals to "PaperAccent". **TYPE:** `str`         |

### datachart.constants.THEME

The predefined themes.

Applied with config.set_theme. Every theme applied to the same set of charts is shown in the [Theme Gallery](https://eriknovak.github.io/datachart/0.8.1/how-to-guides/styling/theme-gallery/index.md).

Examples:

```
>>> from datachart.constants import THEME
>>> THEME.DEFAULT
"default"
```

| ATTRIBUTE   | DESCRIPTION                                                                                  |
| ----------- | -------------------------------------------------------------------------------------------- |
| `DEFAULT`   | The default theme. Equals to "default". **TYPE:** `str`                                      |
| `GREYSCALE` | The greyscale theme. Equals to "greyscale". **TYPE:** `str`                                  |
| `INK`       | The ink theme (dark-ink accents, print-ready). Equals to "ink". **TYPE:** `str`              |
| `HATCH`     | The hatch theme (hatch cycle, value labels, dotted grid). Equals to "hatch". **TYPE:** `str` |
| `MINIMAL`   | The minimal theme (accent blue, no spines, flat bars). Equals to "minimal". **TYPE:** `str`  |
| `MATERIAL`  | The material theme (Google palette, light grid). Equals to "material". **TYPE:** `str`       |

### datachart.constants.EMPHASIS

The supported emphasis roles.

Set per chart via the `emphasis` key in a charts list, or per figure via the `emphasis` argument of Panel.

Examples:

```
>>> from datachart.constants import EMPHASIS
>>> EMPHASIS.BACKGROUND
"background"
```

| ATTRIBUTE    | DESCRIPTION                                                                                                                                                |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BACKGROUND` | Mute a series into context: theme muted color, lowered alpha, thinner strokes, behind the others, no legend entry. Equals to "background". **TYPE:** `str` |
| `HIGHLIGHT`  | Bold a series and bring it to the front of the data layers; it keeps its color and legend entry. Equals to "highlight". **TYPE:** `str`                    |

## Legend Constants

### datachart.constants.LEGEND_ALIGN

The supported legend alignments.

Used by the `plot_legend_alignment` style attribute; aligns the legend's title and entries against each other.

Examples:

```
>>> from datachart.constants import LEGEND_ALIGN
>>> LEGEND_ALIGN.DEFAULT
"left"
```

| ATTRIBUTE | DESCRIPTION                                                              |
| --------- | ------------------------------------------------------------------------ |
| `DEFAULT` | The default legend alignment. Same as LEGEND_ALIGN.LEFT. **TYPE:** `str` |
| `CENTER`  | The center legend alignment. Equals to "center". **TYPE:** `str`         |
| `RIGHT`   | The right legend alignment. Equals to "right". **TYPE:** `str`           |
| `LEFT`    | The left legend alignment. Equals to "left". **TYPE:** `str`             |

### datachart.constants.LEGEND_LOCATION

The supported legend locations.

Used by the `plot_legend_location` style attribute; places the legend within the chart.

Examples:

```
>>> from datachart.constants import LEGEND_LOCATION
>>> LEGEND_LOCATION.BEST
"best"
```

| ATTRIBUTE      | DESCRIPTION                                                  |
| -------------- | ------------------------------------------------------------ |
| `BEST`         | Automatic best location. Equals to "best". **TYPE:** `str`   |
| `UPPER_RIGHT`  | Upper right corner. Equals to "upper right". **TYPE:** `str` |
| `UPPER_LEFT`   | Upper left corner. Equals to "upper left". **TYPE:** `str`   |
| `LOWER_LEFT`   | Lower left corner. Equals to "lower left". **TYPE:** `str`   |
| `LOWER_RIGHT`  | Lower right corner. Equals to "lower right". **TYPE:** `str` |
| `RIGHT`        | Center right. Equals to "right". **TYPE:** `str`             |
| `CENTER_LEFT`  | Center left. Equals to "center left". **TYPE:** `str`        |
| `CENTER_RIGHT` | Center right. Equals to "center right". **TYPE:** `str`      |
| `LOWER_CENTER` | Lower center. Equals to "lower center". **TYPE:** `str`      |
| `UPPER_CENTER` | Upper center. Equals to "upper center". **TYPE:** `str`      |
| `CENTER`       | Center. Equals to "center". **TYPE:** `str`                  |

## Chart Constants

### datachart.constants.HISTOGRAM_TYPE

The supported histogram types.

Passed as the `plot_hist_type` style attribute of histograms: how each series is rendered. How multiple series share the axis is the `bar_mode` setting's job — see `BAR_MODE`.

Examples:

```
>>> from datachart.constants import HISTOGRAM_TYPE
>>> HISTOGRAM_TYPE.BAR
"bar"
```

| ATTRIBUTE     | DESCRIPTION                                                                                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `BAR`         | The bar histogram style. Equals to "bar". **TYPE:** `str`                                                                                                          |
| `STEP`        | The step histogram style: an unfilled outline in the series color. Stacked series draw as STEP_FILLED, since a stack needs area. Equals to "step". **TYPE:** `str` |
| `STEP_FILLED` | The filled step histogram style. Equals to "stepfilled". **TYPE:** `str`                                                                                           |

### datachart.constants.BAR_MODE

The supported bar modes.

Passed as the `bar_mode` setting of bar charts, histograms, and Panel: how multiple series share the axis. Bar charts and panels default to `GROUP`; histograms default to `STACK`, and treat `GROUP` (which has no histogram meaning) as `OVERLAY`.

Examples:

```
>>> from datachart.constants import BAR_MODE
>>> BAR_MODE.DEFAULT
"group"
```

| ATTRIBUTE | DESCRIPTION                                                                                     |
| --------- | ----------------------------------------------------------------------------------------------- |
| `DEFAULT` | The default bar mode. Same as BAR_MODE.GROUP. **TYPE:** `str`                                   |
| `GROUP`   | The series are drawn side by side. Equals to "group". **TYPE:** `str`                           |
| `STACK`   | The series are stacked on top of each other. Equals to "stack". **TYPE:** `str`                 |
| `OVERLAY` | The series are drawn over each other at the same position. Equals to "overlay". **TYPE:** `str` |

### datachart.constants.NORMALIZE

The supported normalization options.

Passed as the heatmap's `norm` attribute: normalizes the cell values before they are mapped to colors. Distinct from SCALE, which sets an axis scale.

Examples:

```
>>> from datachart.constants import NORMALIZE
>>> NORMALIZE.LINEAR
"linear"
```

| ATTRIBUTE | DESCRIPTION                                                   |
| --------- | ------------------------------------------------------------- |
| `LINEAR`  | The linear normalization. Equals to "linear". **TYPE:** `str` |
| `LOG`     | The logistic normalization. Equals to "log". **TYPE:** `str`  |
| `SYMLOG`  | The symlog normalization. Equals to "symlog". **TYPE:** `str` |
| `ASINH`   | The asinh normalization. Equals to "asinh". **TYPE:** `str`   |
| `LOGIT`   | The logit normalization. Equals to "logit". **TYPE:** `str`   |

### datachart.constants.ORIENTATION

The supported orientations.

Passed as the `orientation` setting of bar charts, histograms, box plots, and violin plots.

Examples:

```
>>> from datachart.constants import ORIENTATION
>>> ORIENTATION.HORIZONTAL
"horizontal"
```

| ATTRIBUTE    | DESCRIPTION                                                         |
| ------------ | ------------------------------------------------------------------- |
| `HORIZONTAL` | The horizontal orientation. Equals to "horizontal". **TYPE:** `str` |
| `VERTICAL`   | The vertical orientation. Equals to "vertical". **TYPE:** `str`     |

### datachart.constants.VIOLIN_INNER

The supported violin inner marks.

Passed as the `inner` setting of violin plots; `None` draws the body only.

Examples:

```
>>> from datachart.constants import VIOLIN_INNER
>>> VIOLIN_INNER.BOX
"box"
```

| ATTRIBUTE   | DESCRIPTION                                                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- |
| `BOX`       | A thin quartile bar, a 1.5·IQR whisker line, and a median dot. Equals to "box". **TYPE:** `str`                             |
| `QUARTILES` | A dashed median line and dotted first and third quartile lines, clipped to the body. Equals to "quartiles". **TYPE:** `str` |
| `MEDIAN`    | A single solid median line clipped to the body. Equals to "median". **TYPE:** `str`                                         |

### datachart.constants.BANDWIDTH

The supported kernel density bandwidth rules.

Passed as the `bandwidth` setting of violin plots: the rule of thumb that sizes the Gaussian kernel. A number is also accepted, as a factor applied to the standard deviation of the values — smaller is sharper, larger is smoother.

Examples:

```
>>> from datachart.constants import BANDWIDTH
>>> BANDWIDTH.DEFAULT
"scott"
```

| ATTRIBUTE   | DESCRIPTION                                                                                                                                                                       |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DEFAULT`   | The default rule. Same as BANDWIDTH.SCOTT. **TYPE:** `str`                                                                                                                        |
| `SCOTT`     | Scott's rule of thumb, n \*\* (-1/5) times the standard deviation. Equals to "scott". **TYPE:** `str`                                                                             |
| `SILVERMAN` | Silverman's rule of thumb, (3n/4) \*\* (-1/5) times the standard deviation — about 6% wider than Scott's, so the two look nearly the same. Equals to "silverman". **TYPE:** `str` |

### datachart.constants.RADIAL_TYPE

The supported radial chart visuals.

Passed as the `type` setting of radial charts: the mark family the whole figure draws. The area visual is the line visual with `show_area=True`; stacked bars are the bar visual with `bar_mode="stack"`.

Examples:

```
>>> from datachart.constants import RADIAL_TYPE
>>> RADIAL_TYPE.LINE
"line"
```

| ATTRIBUTE   | DESCRIPTION                                                                      |
| ----------- | -------------------------------------------------------------------------------- |
| `LINE`      | The line (radar) visual. Equals to "line". **TYPE:** `str`                       |
| `BAR`       | The bar visual, one sector per label. Equals to "bar". **TYPE:** `str`           |
| `SCATTER`   | The scatter visual. Equals to "scatter". **TYPE:** `str`                         |
| `HISTOGRAM` | The angular histogram (wind rose) visual. Equals to "histogram". **TYPE:** `str` |

### datachart.constants.SWARM_MODE

The supported swarm plot modes.

Passed as the `mode` setting of swarm plots: how the points of one group spread across the category width.

Examples:

```
>>> from datachart.constants import SWARM_MODE
>>> SWARM_MODE.SWARM
"swarm"
```

| ATTRIBUTE | DESCRIPTION                                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------ |
| `SWARM`   | The beeswarm mode: non-overlapping offsets computed from the marker size. Equals to "swarm". **TYPE:** `str` |
| `STRIP`   | The strip mode: seeded uniform jitter. Equals to "strip". **TYPE:** `str`                                    |

### datachart.constants.DIRECTION

The supported angular directions.

Passed as the `direction` setting of radial charts: which way the angles increase around the circle.

Examples:

```
>>> from datachart.constants import DIRECTION
>>> DIRECTION.CLOCKWISE
"clockwise"
```

| ATTRIBUTE          | DESCRIPTION                                                                         |
| ------------------ | ----------------------------------------------------------------------------------- |
| `CLOCKWISE`        | The angles increase clockwise. Equals to "clockwise". **TYPE:** `str`               |
| `COUNTERCLOCKWISE` | The angles increase counterclockwise. Equals to "counterclockwise". **TYPE:** `str` |

### datachart.constants.VALUE_FORMAT

The predefined value formats.

Passed as the heatmap's `valfmt` attribute (the values drawn in the cells) or the bar chart's `value_format` attribute (the bar value labels).

Examples:

```
>>> from datachart.constants import VALUE_FORMAT
>>> VALUE_FORMAT.DEFAULT
"{x}"
```

| ATTRIBUTE     | DESCRIPTION                                                                          |
| ------------- | ------------------------------------------------------------------------------------ |
| `DEFAULT`     | The default value format. Equals to "{x}". **TYPE:** `str`                           |
| `INTEGER`     | The integer value format (works on floats too). Equals to "{x:.0f}". **TYPE:** `str` |
| `DECIMAL`     | The decimal value format (1 decimal place). Equals to "{x:.1f}". **TYPE:** `str`     |
| `DECIMAL_2`   | The decimal value format (2 decimal places). Equals to "{x:.2f}". **TYPE:** `str`    |
| `DECIMAL_3`   | The decimal value format (3 decimal places). Equals to "{x:.3f}". **TYPE:** `str`    |
| `PERCENT`     | The percentage value format (1 decimal place). Equals to "{x:.1%}". **TYPE:** `str`  |
| `PERCENT_INT` | The percentage value format (no decimals). Equals to "{x:.0%}". **TYPE:** `str`      |
| `SCIENTIFIC`  | The scientific notation format. Equals to "{x:.2e}". **TYPE:** `str`                 |
| `THOUSANDS`   | The thousands separator format. Equals to "{x:,.0f}". **TYPE:** `str`                |

### datachart.constants.SHOW_GRID

The supported show grid options.

Passed as the `show_grid` chart setting: which grid lines to draw. When unset (or `NONE`), the theme's `chart_default_show_grid` fills in.

Examples:

```
>>> from datachart.constants import SHOW_GRID
>>> SHOW_GRID.DEFAULT
None
```

| ATTRIBUTE | DESCRIPTION                                                                   |
| --------- | ----------------------------------------------------------------------------- |
| `DEFAULT` | The default show grid. Same as SHOW_GRID.NONE. **TYPE:** `str`                |
| `NONE`    | No explicit grid; the theme default applies. Equals to None. **TYPE:** `None` |
| `X`       | Show the x-axis grid. Equals to "x". **TYPE:** `str`                          |
| `Y`       | Show the y-axis grid. Equals to "y". **TYPE:** `str`                          |
| `BOTH`    | Show both the x- and y-axis grid. Equals to "both". **TYPE:** `str`           |

### datachart.constants.SCALE

The supported scale options.

Passed as the `scalex`/`scaley` chart settings to set an axis scale. Distinct from NORMALIZE, which normalizes heatmap colors.

Examples:

```
>>> from datachart.constants import SCALE
>>> SCALE.DEFAULT
"linear"
```

| ATTRIBUTE | DESCRIPTION                                              |
| --------- | -------------------------------------------------------- |
| `DEFAULT` | The default scale. Same as SCALE.LINEAR. **TYPE:** `str` |
| `LINEAR`  | The linear scale. Equals to "linear". **TYPE:** `str`    |
| `LOG`     | The log scale. Equals to "log". **TYPE:** `str`          |
| `SYMLOG`  | The symlog scale. Equals to "symlog". **TYPE:** `str`    |
| `ASINH`   | The asinh scale. Equals to "asinh". **TYPE:** `str`      |

### datachart.constants.ASPECT_RATIO

The supported aspect ratio options.

Passed as the `aspect_ratio` chart setting: the ratio of the y-unit to the x-unit on screen.

Examples:

```
>>> from datachart.constants import ASPECT_RATIO
>>> ASPECT_RATIO.DEFAULT
"auto"
```

| ATTRIBUTE | DESCRIPTION                                                          |
| --------- | -------------------------------------------------------------------- |
| `DEFAULT` | The default aspect ratio. Same as ASPECT_RATIO.AUTO. **TYPE:** `str` |
| `AUTO`    | Automatic aspect ratio. Equals to "auto". **TYPE:** `str`            |
| `EQUAL`   | Equal aspect ratio (1:1). Equals to "equal". **TYPE:** `str`         |

### datachart.constants.COLORBAR_LOCATION

The supported colorbar locations.

Examples:

```
>>> from datachart.constants import COLORBAR_LOCATION
>>> COLORBAR_LOCATION.RIGHT
"right"
```

| ATTRIBUTE | DESCRIPTION                                                 |
| --------- | ----------------------------------------------------------- |
| `RIGHT`   | Right side of the chart. Equals to "right". **TYPE:** `str` |
| `LEFT`    | Left side of the chart. Equals to "left". **TYPE:** `str`   |
| `TOP`     | Top of the chart. Equals to "top". **TYPE:** `str`          |
| `BOTTOM`  | Bottom of the chart. Equals to "bottom". **TYPE:** `str`    |
