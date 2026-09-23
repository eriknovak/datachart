"""Module containing the `constants`.

The `constants` module provides a set of predefined constants used in the package.
These include figure size, format, style, and other figure manipulation values.

**Figure Constants**

Classes:
    FIG_SIZE:   The predefined figure sizes.
    FIG_FORMAT: The supported figure formats.

**Font Constants**

Classes:
    FONT_STYLE:  The supported font styles.
    FONT_WEIGHT: The supported font weights.

**Line Constants**

Classes:
    LINE_MARKER:     The supported line markers.
    LINE_STYLE:      The supported line styles.
    LINE_DRAW_STYLE: The supported line draw styles.
    ARROW_STYLE:     The supported text annotation connector looks.

**Style Constants**

Classes:
    HATCH_STYLE: The supported hatch styles.
    COLORS:      The predefined colors.
    THEME:       The predefined themes.
    EMPHASIS:    The supported emphasis roles.

**Legend Constants**

Classes:
    LEGEND_ALIGN:    The supported legend alignments.
    LEGEND_LOCATION: The supported legend locations.

**Chart Constants**

Classes:
    BAR_MODE:          The supported bar modes.
    SORT:              The supported category sort orders.
    NORMALIZE:         The supported normalization options.
    ORIENTATION:       The supported orientations.
    VIOLIN_INNER:      The supported violin inner marks.
    BANDWIDTH:         The supported kernel density bandwidth rules.
    SWARM_MODE:        The supported swarm plot modes.
    VALUE_FORMAT:      The predefined value formats.
    DATE_FORMAT:       The predefined date formats.
    SHOW_GRID:         The supported show grid options.
    SCALE:             The supported scale options.
    ASPECT_RATIO:      The supported aspect ratio options.
    COLORBAR_LOCATION: The supported colorbar locations.
    DRAW_POSITION:     The supported draw positions of the image and basemap.

**Chart-Specific Constants**

Classes:
    STACKED_AREA_BASELINE:   The supported stacked area baselines.
    BUMP_RANK:               The supported bump chart ranking rules.
    BUMP_LABEL_POSITION:     The supported end label positions.
    RADIAL_TYPE:             The supported radial chart visuals.
    RADIAL_DIRECTION:        The supported angular directions.
    CALENDAR_WEEKDAY:        The supported week start days.
    GANTT_DATE_PERIOD:       The supported date axis periods.
    GANTT_VALUE:             The supported gantt chart value labels.
    GANTT_SORT_KEY:          The supported gantt chart sort keys.
    GANTT_ARROW_ENTRY:       The supported gantt dependency arrow entries.
    DUMBBELL_VALUE:          The supported dumbbell chart value labels.
    DUMBBELL_SORT_KEY:       The supported dumbbell chart sort keys.
    HISTOGRAM_TYPE:          The supported histogram types.
    RIDGELINE_SCALE:         The supported ridgeline density scales.
    CONTOUR_LEVELS:          The supported contour level rules.
    HEXBIN_REDUCE:           The supported hexbin aggregations.
    NETWORK_LAYOUT:          The supported network chart layouts.
    NETWORK_LABEL_POSITION:     The supported network node label positions.
    SCATTER_MATRIX_DIAGONAL: The supported scatter matrix diagonal cells.
    BASEMAP_FEATURE:         The supported basemap features.
    BASEMAP_RESOLUTION:      The supported basemap outline resolutions.

"""


class FIG_SIZE:
    """The predefined figure sizes.

    All values are `(width, height)` in inches, matplotlib's `figsize` unit.
    Paper figures are anchored to the printable area of an A4 page with
    standard 2.5 cm margins — a 6.3 x 9.7 in (16.0 x 24.6 cm) text block.
    `FULL` spans the text-block width; `HALF` spans one of two columns
    separated by a 0.3 in (0.8 cm) gap (3.0 in / 7.6 cm each). Widths cross
    with a height — `SHORT` (2.4 in / 6.1 cm), `MEDIUM` (4.8 in / 12.2 cm),
    or `TALL` (7.2 in / 18.3 cm). Passed as the `figsize` chart setting.

    ![FIG_SIZE at a glance](../assets/imgs/fig-sizes.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import FIG_SIZE
        >>> FIG_SIZE.DEFAULT
        (6.4, 4.8)

    Attributes:
        DEFAULT (Tuple[float, float]): The default figure size. Equals to `(6.4, 4.8)` in (16.3 x 12.2 cm).
        FULL_SHORT (Tuple[float, float]): The short, full-width figure size. Equals to `(6.3, 2.4)` in (16.0 x 6.1 cm).
        FULL_MEDIUM (Tuple[float, float]): The medium, full-width figure size. Equals to `(6.3, 4.8)` in (16.0 x 12.2 cm).
        FULL_TALL (Tuple[float, float]): The tall, full-width figure size. Equals to `(6.3, 7.2)` in (16.0 x 18.3 cm).
        HALF_SHORT (Tuple[float, float]): The short, half-width figure size. Equals to `(3.0, 2.4)` in (7.6 x 6.1 cm).
        HALF_MEDIUM (Tuple[float, float]): The medium, half-width figure size. Equals to `(3.0, 4.8)` in (7.6 x 12.2 cm).
        HALF_TALL (Tuple[float, float]): The tall, half-width figure size. Equals to `(3.0, 7.2)` in (7.6 x 18.3 cm).
        HALF_SQUARE (Tuple[float, float]): The square, half-width figure size. Equals to `(3.0, 3.0)` in (7.6 x 7.6 cm).
        A4_PORTRAIT (Tuple[float, float]): The A4 portrait printable-area figure size. Equals to `(6.3, 9.7)` in (16.0 x 24.6 cm).
        A4_LANDSCAPE (Tuple[float, float]): The A4 landscape printable-area figure size. Equals to `(9.7, 6.3)` in (24.6 x 16.0 cm).
        SQUARE (Tuple[float, float]): The square figure size. Equals to `(4.8, 4.8)` in (12.2 x 12.2 cm).
        SLIDE_16_9 (Tuple[float, float]): The 16:9 slide figure size (PowerPoint/Google Slides). Equals to `(13.33, 7.5)` in (33.9 x 19.1 cm).
        SLIDE_4_3 (Tuple[float, float]): The 4:3 slide figure size (PowerPoint/Google Slides). Equals to `(10.0, 7.5)` in (25.4 x 19.1 cm).
        BEAMER_16_9 (Tuple[float, float]): The 16:9 beamer frame figure size. Equals to `(6.3, 3.54)` in (16.0 x 9.0 cm).
        BEAMER_4_3 (Tuple[float, float]): The 4:3 beamer frame figure size. Equals to `(5.04, 3.78)` in (12.8 x 9.6 cm).

    """

    DEFAULT = (6.4, 4.8)

    # Full-width paper figures (A4 text-block width)
    FULL_SHORT = (6.3, 2.4)
    FULL_MEDIUM = (6.3, 4.8)
    FULL_TALL = (6.3, 7.2)

    # Half-width paper figures (one of two columns, 0.3 in gap)
    HALF_SHORT = (3.0, 2.4)
    HALF_MEDIUM = (3.0, 4.8)
    HALF_TALL = (3.0, 7.2)
    HALF_SQUARE = (3.0, 3.0)

    # A4 printable area (2.5 cm margins)
    A4_PORTRAIT = (6.3, 9.7)
    A4_LANDSCAPE = (9.7, 6.3)

    # Square
    SQUARE = (4.8, 4.8)

    # Presentation slides
    SLIDE_16_9 = (13.33, 7.5)
    SLIDE_4_3 = (10.0, 7.5)
    BEAMER_16_9 = (6.3, 3.54)
    BEAMER_4_3 = (5.04, 3.78)


class FIG_FORMAT:
    """The supported figure formats.

    Passed as the `format` argument of [`save_figure`][datachart.utils.save_figure].

    Examples:
        >>> from datachart.constants import FIG_FORMAT
        >>> FIG_FORMAT.DEFAULT
        "png"

    Attributes:
        DEFAULT (str): The default format. Same as `FIG_FORMAT.PNG`.
        SVG (str): The svg format. Equals to `"svg"`.
        PDF (str): The pdf format. Equals to `"pdf"`.
        PNG (str): The png format. Equals to `"png"`.
        WEBP (str): The webp format. Equals to `"webp"`.
        EPS (str): The eps format (Encapsulated PostScript). Equals to `"eps"`.
        JPG (str): The jpg format. Equals to `"jpg"`.
        TIFF (str): The tiff format. Equals to `"tiff"`.

    """

    DEFAULT = "png"
    SVG = "svg"
    PDF = "pdf"
    PNG = "png"
    WEBP = "webp"
    EPS = "eps"
    JPG = "jpg"
    TIFF = "tiff"


class FONT_STYLE:
    """The supported font styles.

    ![FONT_STYLE at a glance](../assets/imgs/const-font-style.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import FONT_STYLE
        >>> FONT_STYLE.DEFAULT
        "normal"

    Attributes:
        DEFAULT (str): The default font style. Same as `FONT_STYLE.NORMAL`.
        NORMAL (str): The normal font style. Equals to `"normal"`.
        ITALIC (str): The italic font style. Equals to `"italic"`.
        OBLIQUE (str): The oblique font style. Equals to `"oblique"`.

    """

    DEFAULT = "normal"
    NORMAL = "normal"
    ITALIC = "italic"
    OBLIQUE = "oblique"


class FONT_WEIGHT:
    """The supported font weights.

    Used by the `font_*_weight` style attributes (general, title, subtitle,
    axis labels).

    ![FONT_WEIGHT at a glance](../assets/imgs/const-font-weight.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import FONT_WEIGHT
        >>> FONT_WEIGHT.DEFAULT
        "normal"

    Attributes:
        DEFAULT (str): The default font weight. Same as `FONT_WEIGHT.NORMAL`.
        ULTRA_LIGHT (str): The ultra light font weight. Equals to `"ultralight"`.
        LIGHT (str): The light font weight. Equals to `"light"`.
        NORMAL (str): The normal font weight. Equals to `"normal"`.
        MEDIUM (str): The medium font weight. Equals to `"medium"`.
        SEMIBOLD (str): The semibold font weight. Equals to `"semibold"`.
        BOLD (str): The bold font weight. Equals to `"bold"`.
        EXTRA_BOLD (str): The extra bold font weight. Equals to `"extra bold"`.
        HEAVY (str): The heavy font weight. Equals to `"heavy"`.
        BLACK (str): The black font weight. Equals to `"black"`.

    """

    DEFAULT = "normal"
    ULTRA_LIGHT = "ultralight"
    LIGHT = "light"
    NORMAL = "normal"
    MEDIUM = "medium"
    SEMIBOLD = "semibold"
    BOLD = "bold"
    EXTRA_BOLD = "extra bold"
    HEAVY = "heavy"
    BLACK = "black"


class LINE_MARKER:
    """The supported line markers.

    Used by the `plot_line_marker` (line charts) and `plot_scatter_marker`
    (scatter charts) style attributes.

    ![LINE_MARKER at a glance](../assets/imgs/const-line-marker.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import LINE_MARKER
        >>> LINE_MARKER.PIXEL
        ","

    Attributes:
        NONE (str): No marker. Equals to `""`.
        PIXEL (str): The pixel line marker. Equals to `","`.
        POINT (str): The point line marker. Equals to `"."`.
        CIRCLE (str): The circle line marker. Equals to `"o"`.
        DIAMOND (str): The diamond line marker. Equals to `"D"`.
        THIN_DIAMOND (str): The thin diamond line marker. Equals to `"d"`.
        TRIANGLE (str): The triangle (up) line marker. Equals to `"^"`.
        TRIANGLE_DOWN (str): The triangle down line marker. Equals to `"v"`.
        TRIANGLE_LEFT (str): The triangle left line marker. Equals to `"<"`.
        TRIANGLE_RIGHT (str): The triangle right line marker. Equals to `">"`.
        SQUARE (str): The square line marker. Equals to `"s"`.
        PENTAGON (str): The pentagon line marker. Equals to `"p"`.
        HEXAGON (str): The hexagon line marker. Equals to `"h"`.
        STAR (str): The star line marker. Equals to `"*"`.
        CROSS (str): The cross line marker. Equals to `"x"`.
        PLUS (str): The plus line marker. Equals to `"+"`.
        VLINE (str): The vertical line marker. Equals to `"|"`.
        HLINE (str): The horizontal line marker. Equals to `"_"`.

    """

    NONE = ""
    PIXEL = ","
    POINT = "."
    CIRCLE = "o"
    DIAMOND = "D"
    THIN_DIAMOND = "d"
    TRIANGLE = "^"
    TRIANGLE_DOWN = "v"
    TRIANGLE_LEFT = "<"
    TRIANGLE_RIGHT = ">"
    SQUARE = "s"
    PENTAGON = "p"
    HEXAGON = "h"
    STAR = "*"
    CROSS = "x"
    PLUS = "+"
    VLINE = "|"
    HLINE = "_"


class LINE_STYLE:
    """The supported line styles.

    Used by the `plot_line_style` style attribute of line charts.

    ![LINE_STYLE at a glance](../assets/imgs/const-line-style.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import LINE_STYLE
        >>> LINE_STYLE.SOLID
        "-"

    Attributes:
        NONE (str): No line style. Equals to `""`.
        SOLID (str): The solid line style. Equals to `"-"`.
        DASHED (str): The dashed line style. Equals to `"--"`.
        DASHDOT (str): The dashdot line style. Equals to `"-."`.
        DOTTED (str): The dotted line style. Equals to `":"`.

    """

    NONE = ""
    SOLID = "-"
    DASHED = "--"
    DASHDOT = "-."
    DOTTED = ":"


class ARROW_STYLE:
    """The supported connector looks.

    The one constant for every drawn connector: the `plot_text_arrow_style`
    style attribute of text annotations and the `plot_network_edge_style`
    style attribute of network charts. Each value names a complete connector
    look — the line shape, curvature, and the gap on the text side. For an
    annotation, a curved look bows toward the side with the most open space
    around the chart's data; `plot_text_arrow_curve` pins the bow exactly,
    and the other `plot_text_arrow_*` style attributes override single
    properties of the chosen look. A raw matplotlib arrow style string
    (e.g. `"-|>"`) is also accepted. A network edge takes only the two
    headless looks, `CURVE` and `STRAIGHT`, bowed by
    `plot_network_edge_curve`; its arrowhead comes from the chart's
    `directed` argument.

    ![ARROW_STYLE at a glance](../assets/imgs/const-arrow-style.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import ARROW_STYLE
        >>> ARROW_STYLE.CURVE
        "curve"

    Attributes:
        CURVE (str): A curved plain line with a small text-side gap. The default. Text annotations and network edges. Equals to `"curve"`.
        CURVE_ARROW (str): The same curve with an arrowhead at the target. Text annotations only. Equals to `"curve-arrow"`.
        STRAIGHT (str): A straight plain line with a small text-side gap. Text annotations and network edges. Equals to `"straight"`.
        TOUCHING (str): A straight plain line starting flush at the text box border. Text annotations only. Equals to `"touching"`.
        ARROW (str): A straight line with an arrowhead at the target. Text annotations only. Equals to `"arrow"`.

    """

    CURVE = "curve"
    CURVE_ARROW = "curve-arrow"
    STRAIGHT = "straight"
    TOUCHING = "touching"
    ARROW = "arrow"


class LINE_DRAW_STYLE:
    """The supported line draw styles.

    Used by the `plot_line_drawstyle` style attribute of line charts.

    ![LINE_DRAW_STYLE at a glance](../assets/imgs/const-line-draw-style.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import LINE_DRAW_STYLE
        >>> LINE_DRAW_STYLE.DEFAULT
        "default"

    Attributes:
        DEFAULT (str): The default line draw style. Equals to `"default"`.
        STEPS_PRE (str): The pre-steps line draw style. Equals to `"steps-pre"`.
        STEPS_MID (str): The mid-steps line draw style. Equals to `"steps-mid"`.
        STEPS_POST (str): The post-steps line draw style. Equals to `"steps-post"`.

    """

    DEFAULT = "default"
    STEPS_PRE = "steps-pre"
    STEPS_MID = "steps-mid"
    STEPS_POST = "steps-post"


class HATCH_STYLE:
    """The supported hatch styles.

    Used by the `plot_bar_hatch` and `plot_hist_hatch` style attributes, and
    by the `HATCH` theme's hatch cycle.

    ![HATCH_STYLE at a glance](../assets/imgs/const-hatch-style.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import HATCH_STYLE
        >>> HATCH_STYLE.DEFAULT
        None

    Attributes:
        DEFAULT (str): The default hatch style. Equals to `None`.
        DIAGONAL (str): The diagonal hatch style. Equals to `"/"`.
        BACK_DIAGONAL (str): The back diagonal hatch style. Equals to `"\\\\"`.
        VERTICAL (str): The vertical hatch style. Equals to `"|"`.
        HORIZONTAL (str): The horizontal hatch style. Equals to `"-"`.
        CROSSED (str): The crossed hatch style. Equals to `"+"`.
        CROSSED_DIAGONAL (str): The crossed diagonal hatch style. Equals to `"x"`.
        DOTS (str): The dots hatch style. Equals to `"."`.
        CIRCLES (str): The circles hatch style. Equals to `"o"`.
        STARS (str): The stars hatch style. Equals to `"*"`.

    """

    DEFAULT = None
    DIAGONAL = "/"
    BACK_DIAGONAL = "\\"
    VERTICAL = "|"
    HORIZONTAL = "-"
    CROSSED = "+"
    CROSSED_DIAGONAL = "x"
    DOTS = "."
    CIRCLES = "o"
    STARS = "*"


class LEGEND_ALIGN:
    """The supported legend alignments.

    Used by the `plot_legend_alignment` style attribute; aligns the legend's
    title and entries against each other.

    ![LEGEND_ALIGN at a glance](../assets/imgs/const-legend-align.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import LEGEND_ALIGN
        >>> LEGEND_ALIGN.DEFAULT
        "left"

    Attributes:
        DEFAULT (str): The default legend alignment. Same as `LEGEND_ALIGN.LEFT`.
        CENTER (str): The center legend alignment. Equals to `"center"`.
        RIGHT (str): The right legend alignment. Equals to `"right"`.
        LEFT (str): The left legend alignment. Equals to `"left"`.

    """

    DEFAULT = "left"
    CENTER = "center"
    RIGHT = "right"
    LEFT = "left"


class LEGEND_LOCATION:
    """The supported legend locations.

    Used by the `plot_legend_location` style attribute and the `location`
    field of a chart's `legend` setting. The in-axes members place the legend
    within the chart; the `OUTSIDE_*` members place it beside the axes, on the
    named edge, with nothing clipped.

    ![LEGEND_LOCATION at a glance](../assets/imgs/const-legend-location.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import LEGEND_LOCATION
        >>> LEGEND_LOCATION.BEST
        "best"

    Attributes:
        BEST (str): Automatic best location. Equals to `"best"`.
        UPPER_RIGHT (str): Upper right corner. Equals to `"upper right"`.
        UPPER_LEFT (str): Upper left corner. Equals to `"upper left"`.
        LOWER_LEFT (str): Lower left corner. Equals to `"lower left"`.
        LOWER_RIGHT (str): Lower right corner. Equals to `"lower right"`.
        RIGHT (str): Center right. Equals to `"right"`.
        CENTER_LEFT (str): Center left. Equals to `"center left"`.
        CENTER_RIGHT (str): Center right. Equals to `"center right"`.
        LOWER_CENTER (str): Lower center. Equals to `"lower center"`.
        UPPER_CENTER (str): Upper center. Equals to `"upper center"`.
        CENTER (str): Center. Equals to `"center"`.
        OUTSIDE_RIGHT (str): Beside the right edge, top-aligned. Equals to `"outside right"`.
        OUTSIDE_LEFT (str): Beside the left edge, top-aligned. Equals to `"outside left"`.
        OUTSIDE_TOP (str): Above the axes, centered. Equals to `"outside top"`.
        OUTSIDE_BOTTOM (str): Below the axes, centered. Equals to `"outside bottom"`.
    """

    BEST = "best"
    UPPER_RIGHT = "upper right"
    UPPER_LEFT = "upper left"
    LOWER_LEFT = "lower left"
    LOWER_RIGHT = "lower right"
    RIGHT = "right"
    CENTER_LEFT = "center left"
    CENTER_RIGHT = "center right"
    LOWER_CENTER = "lower center"
    UPPER_CENTER = "upper center"
    CENTER = "center"
    OUTSIDE_RIGHT = "outside right"
    OUTSIDE_LEFT = "outside left"
    OUTSIDE_TOP = "outside top"
    OUTSIDE_BOTTOM = "outside bottom"


class HISTOGRAM_TYPE:
    """The supported histogram types.

    Passed as the `plot_hist_type` style attribute of histograms: how each
    series is rendered. How multiple series share the axis is the `bar_mode`
    setting's job — see `BAR_MODE`.

    ![HISTOGRAM_TYPE at a glance](../assets/imgs/const-histogram-type.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import HISTOGRAM_TYPE
        >>> HISTOGRAM_TYPE.BAR
        "bar"

    Attributes:
        BAR (str): The bar histogram style. Equals to `"bar"`.
        STEP (str): The step histogram style: an unfilled outline in the
            series color. Stacked series draw as `STEP_FILLED`, since a stack
            needs area. Equals to `"step"`.
        STEP_FILLED (str): The filled step histogram style. Equals to `"stepfilled"`.

    """

    BAR = "bar"
    STEP = "step"
    STEP_FILLED = "stepfilled"


class BAR_MODE:
    """The supported bar modes.

    Passed as the `bar_mode` setting of bar charts, histograms, and
    [`Panel`][datachart.utils.Panel]: how multiple series share the axis.
    Bar charts and panels default to `GROUP`; histograms default to `STACK`,
    and treat `GROUP` (which has no histogram meaning) as `OVERLAY`.

    ![BAR_MODE at a glance](../assets/imgs/const-bar-mode.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import BAR_MODE
        >>> BAR_MODE.DEFAULT
        "group"

    Attributes:
        DEFAULT (str): The default bar mode. Same as `BAR_MODE.GROUP`.
        GROUP (str): The series are drawn side by side. Equals to `"group"`.
        STACK (str): The series are stacked on top of each other. Equals to `"stack"`.
        OVERLAY (str): The series are drawn over each other at the same position. Equals to `"overlay"`.

    """

    DEFAULT = "group"
    GROUP = "group"
    STACK = "stack"
    OVERLAY = "overlay"


class SORT:
    """The supported category sort orders.

    Passed as the `sort` setting of the bar-type fronts (`BarChart`,
    `PyramidChart`, and the `RadialChart` bar visual): the order the
    categories are drawn in, by value. One order serves every series in the
    chart, keyed by the total across them or by the series `sort_by` names;
    ties keep input order.

    ![SORT at a glance](../assets/imgs/const-sort.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import SORT
        >>> SORT.DEFAULT
        None

    Attributes:
        DEFAULT (None): The default sort. Same as `SORT.NONE`.
        NONE (None): Input order. Equals to `None`.
        ASCENDING (str): Smallest value first. Equals to `"ascending"`.
        DESCENDING (str): Largest value first. Equals to `"descending"`.

    """

    DEFAULT = None
    NONE = None
    ASCENDING = "ascending"
    DESCENDING = "descending"


class COLORS:
    """The predefined colors using [pypalettes](https://y-sunflower.github.io/pypalettes/).

    All palette names are valid pypalettes identifiers. You can use any of the 2500+
    palettes available in pypalettes by passing the palette name as a string.
    Accepted anywhere a palette is: the `color_general_singular` and
    `color_general_multiple` config attributes, and the heatmap and parallel
    coords color settings. All predefined palettes are rendered in the
    [Colormaps guide](../../how-to-guides/styling/colormaps/).

    A single matplotlib color (`"#B5651D"`, `"tab:blue"`, `"rebeccapurple"`) is
    accepted in the same places and is used as a palette of one, repeated for
    every series that asks for a color. A name that is both a palette and a
    color, such as `"Red"` or `"pink"`, is read as the palette.

    Examples:
        >>> from datachart.constants import COLORS
        >>> COLORS.Blues
        'Blues'

    Attributes:
        Blues (str): Sequential blue palette. Equals to `"Blues"`.
        Greens (str): Sequential green palette. Equals to `"Greens"`.
        Oranges (str): Sequential orange palette. Equals to `"Oranges"`.
        Purples (str): Sequential purple palette. Equals to `"Purples"`.
        Reds (str): Sequential red palette. Equals to `"Reds"`.
        Sunset2 (str): Multi-hue sunset palette. Equals to `"Sunset2"`.
        YlGnBu (str): Multi-hue yellow-green-blue palette. Equals to `"YlGnBu"`.
        YlOrRd (str): Multi-hue yellow-orange-red palette. Equals to `"YlOrRd"`.
        YlOrBr (str): Multi-hue yellow-orange-brown palette. Equals to `"YlOrBr"`.
        PuBuGn (str): Multi-hue purple-blue-green palette. Equals to `"PuBuGn"`.
        GnBu (str): Multi-hue green-blue palette. Equals to `"GnBu"`.
        BuPu (str): Multi-hue blue-purple palette. Equals to `"BuPu"`.
        PuBu (str): Multi-hue purple-blue palette. Equals to `"PuBu"`.
        Egypt (str): Multi-hue Egypt palette. Equals to `"Egypt"`.
        Hiroshige (str): Multi-hue Hiroshige palette. Equals to `"Hiroshige"`.
        Lake (str): Multi-hue lake palette. Equals to `"Lake"`.
        Neon (str): Multi-hue neon palette. Equals to `"Neon"`.
        RdBu (str): Diverging red-blue palette. Equals to `"RdBu"`.
        BrBG (str): Diverging brown-blue-green palette. Equals to `"BrBG"`.
        PuOr (str): Diverging purple-orange palette. Equals to `"PuOr"`.
        Spectral (str): Diverging spectral palette. Equals to `"Spectral"`.
        RdYlBu (str): Diverging red-yellow-blue palette. Equals to `"RdYlBu"`.
        RdYlGn (str): Diverging red-yellow-green palette. Equals to `"RdYlGn"`.
        Pastel (str): Soft pastel categorical palette. Equals to `"Pastel"`.
        Set2 (str): ColorBrewer Set2 categorical palette. Equals to `"Set2"`.
        Accent (str): ColorBrewer Accent categorical palette. Equals to `"Accent"`.
        Dark2 (str): ColorBrewer Dark2 categorical palette. Equals to `"Dark2"`.
        Paired (str): ColorBrewer Paired categorical palette (high contrast). Equals to `"Paired"`.
        Set1 (str): ColorBrewer Set1 categorical palette (high contrast). Equals to `"Set1"`.
        Greys (str): Grayscale palette for monochrome visualizations. Equals to `"Greys"`.
        Viridis (str): Perceptually uniform, color-blind friendly. Equals to `"Viridis"`.
        Cividis (str): Color-blind friendly (optimized for CVD). Equals to `"Cividis"`.
        Inferno (str): Perceptually uniform, color-blind friendly. Equals to `"Inferno"`.
        Plasma (str): Perceptually uniform, color-blind friendly. Equals to `"Plasma"`.
        Magma (str): Perceptually uniform, color-blind friendly. Equals to `"magma"`.
        Turbo (str): Rainbow-like but perceptually better. Equals to `"turbo"`.
        OkabeIto (str): Okabe-Ito categorical palette, color-blind safe. Equals to `"OkabeIto"`.
        OkabeIto_Black (str): Okabe-Ito palette including black. Equals to `"OkabeIto_black"`.
        Coolwarm (str): Diverging cool-warm palette. Equals to `"coolwarm"`.
        Tab10 (str): Tableau 10-color categorical palette. Equals to `"tab10"`.
        Tab20 (str): Tableau 20-color categorical palette. Equals to `"tab20"`.
        PaperYlGnBu (str): Diversified YlGnBu categorical palette for publications. Equals to `"PaperYlGnBu"`.
        PaperAccent (str): Two-color blue/red accent pair for publications. Equals to `"PaperAccent"`.

    """

    # Sequential (Single-hue)
    Blues = "Blues"
    Greens = "Greens"
    Oranges = "Oranges"
    Purples = "Purples"
    Reds = "Reds"

    # Sequential (Multi-hue)
    Sunset2 = "Sunset2"
    YlGnBu = "YlGnBu"
    YlOrRd = "YlOrRd"
    YlOrBr = "YlOrBr"
    PuBuGn = "PuBuGn"
    GnBu = "GnBu"
    BuPu = "BuPu"
    PuBu = "PuBu"
    Egypt = "Egypt"
    Hiroshige = "Hiroshige"
    Lake = "Lake"
    Neon = "Neon"

    # Diverging
    RdBu = "RdBu"
    BrBG = "BrBG"
    PuOr = "PuOr"
    Spectral = "Spectral"
    RdYlBu = "RdYlBu"
    RdYlGn = "RdYlGn"

    # Categorical
    Pastel = "Pastel"
    Set2 = "Set2"
    Accent = "Accent"
    Dark2 = "Dark2"
    Paired = "Paired"
    Set1 = "Set1"

    # Grayscale (print-friendly)
    Greys = "Greys"

    # Color-blind friendly / Accessible
    Viridis = "Viridis"
    Cividis = "Cividis"
    Inferno = "Inferno"
    Plasma = "Plasma"
    Magma = "magma"
    Turbo = "turbo"
    OkabeIto = "OkabeIto"
    OkabeIto_Black = "OkabeIto_black"

    # Additional Diverging
    Coolwarm = "coolwarm"

    # Tableau palettes (Categorical)
    Tab10 = "tab10"
    Tab20 = "tab20"

    # Custom datachart palettes (registered locally, not in pypalettes)
    PaperYlGnBu = "PaperYlGnBu"
    PaperAccent = "PaperAccent"


class NORMALIZE:
    """The supported normalization options.

    Passed as the heatmap's `norm` attribute: normalizes the cell values
    before they are mapped to colors. Distinct from
    [`SCALE`][datachart.constants.SCALE], which sets an axis scale.

    ![NORMALIZE at a glance](../assets/imgs/const-normalize.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import NORMALIZE
        >>> NORMALIZE.LINEAR
        "linear"

    Attributes:
        LINEAR (str): The linear normalization. Equals to `"linear"`.
        LOG (str): The logistic normalization. Equals to `"log"`.
        SYMLOG (str): The symlog normalization. Equals to `"symlog"`.
        ASINH (str): The asinh normalization. Equals to `"asinh"`.
        LOGIT (str): The logit normalization. Equals to `"logit"`.
        CENTERED (str): The normalization holding `vcenter` in the middle of the
            colormap, the same distance to each side of it. Equals to `"centered"`.
        TWOSLOPE (str): The normalization holding `vcenter` in the middle of the
            colormap, with `vmin` and `vmax` at unequal distances from it.
            Equals to `"twoslope"`.

    `CENTERED` and `TWOSLOPE` are read by the heatmap and calendar heatmap,
    which draw them in the theme's diverging colormap; the other charts
    taking a `norm` support the first five.

    """

    LINEAR = "linear"
    LOG = "log"
    SYMLOG = "symlog"
    ASINH = "asinh"
    LOGIT = "logit"
    CENTERED = "centered"
    TWOSLOPE = "twoslope"


class ORIENTATION:
    """The supported orientations.

    Passed as the `orientation` setting of bar charts, histograms, box
    plots, and violin plots.

    ![ORIENTATION at a glance](../assets/imgs/const-orientation.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import ORIENTATION
        >>> ORIENTATION.HORIZONTAL
        "horizontal"

    Attributes:
        HORIZONTAL (str): The horizontal orientation. Equals to `"horizontal"`.
        VERTICAL (str): The vertical orientation. Equals to `"vertical"`.

    """

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class CALENDAR_WEEKDAY:
    """The supported week start days.

    Passed as the `week_start` setting of the calendar heatmap: the weekday
    drawn in the top row of every week column. The theme's
    `plot_calendar_heatmap_week_start` supplies the default.

    ![CALENDAR_WEEKDAY at a glance](../assets/imgs/const-weekday.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import CALENDAR_WEEKDAY
        >>> CALENDAR_WEEKDAY.MONDAY
        "monday"

    Attributes:
        MONDAY (str): Weeks run from Monday to Sunday. Equals to `"monday"`.
        SUNDAY (str): Weeks run from Sunday to Saturday. Equals to `"sunday"`.

    """

    MONDAY = "monday"
    SUNDAY = "sunday"


class SWARM_MODE:
    """The supported swarm plot modes.

    Passed as the `mode` setting of swarm plots: how the points of one group
    spread across the category width.

    ![SWARM_MODE at a glance](../assets/imgs/const-swarm-mode.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import SWARM_MODE
        >>> SWARM_MODE.SWARM
        "swarm"

    Attributes:
        SWARM (str): The beeswarm mode: non-overlapping offsets computed from
            the marker size. Equals to `"swarm"`.
        STRIP (str): The strip mode: seeded uniform jitter. Equals to `"strip"`.

    """

    SWARM = "swarm"
    STRIP = "strip"


class VIOLIN_INNER:
    """The supported violin inner marks.

    Passed as the `inner` setting of violin plots; `None` draws the body only.

    ![VIOLIN_INNER at a glance](../assets/imgs/const-violin-inner.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import VIOLIN_INNER
        >>> VIOLIN_INNER.BOX
        "box"

    Attributes:
        BOX (str): A thin quartile bar, a 1.5·IQR whisker line, and a median
            dot. Equals to `"box"`.
        QUARTILES (str): A dashed median line and dotted first and third
            quartile lines, clipped to the body. Equals to `"quartiles"`.
        MEDIAN (str): A single solid median line clipped to the body. Equals
            to `"median"`.

    """

    BOX = "box"
    QUARTILES = "quartiles"
    MEDIAN = "median"


class RIDGELINE_SCALE:
    """The supported ridgeline density scales.

    Passed as the `ridge_scale` setting of ridgeline plots: whether every ridge
    is scaled to the same peak height, so their shapes compare, or all
    ridges share one density scale, so their heights compare.

    ![RIDGELINE_SCALE at a glance](../assets/imgs/const-ridgeline-scale.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import RIDGELINE_SCALE
        >>> RIDGELINE_SCALE.DEFAULT
        "per_row"

    Attributes:
        DEFAULT (str): The default scale. Same as `RIDGELINE_SCALE.PER_ROW`.
        PER_ROW (str): Every ridge reaches the same peak height. Equals to
            `"per_row"`.
        COMMON (str): One density scale: the tallest ridge reaches the peak
            height and the others stay in proportion. Equals to `"common"`.

    """

    DEFAULT = "per_row"
    PER_ROW = "per_row"
    COMMON = "common"


class BANDWIDTH:
    """The supported kernel density bandwidth rules.

    Passed as the `bandwidth` setting of violin plots: the rule of thumb that
    sizes the Gaussian kernel. A number is also accepted, as a factor applied
    to the standard deviation of the values — smaller is sharper, larger is
    smoother.

    ![BANDWIDTH at a glance](../assets/imgs/const-bandwidth.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import BANDWIDTH
        >>> BANDWIDTH.DEFAULT
        "scott"

    Attributes:
        DEFAULT (str): The default rule. Same as `BANDWIDTH.SCOTT`.
        SCOTT (str): Scott's rule of thumb, `n ** (-1/5)` times the standard
            deviation. Equals to `"scott"`.
        SILVERMAN (str): Silverman's rule of thumb, `(3n/4) ** (-1/5)` times
            the standard deviation — about 6% wider than Scott's, so the two
            look nearly the same. Equals to `"silverman"`.

    """

    DEFAULT = "scott"
    SCOTT = "scott"
    SILVERMAN = "silverman"


class CONTOUR_LEVELS:
    """The supported contour level rules.

    Passed as the `levels` setting of contour charts: the rule that picks how
    many iso-lines (or filled bands) cut the surface. An integer target count
    or an explicit list of level values is also accepted. Every rule is
    evaluated on the per-axis resolution of the grid (the square root of its
    cell count), so a finer grid draws more levels; the count is clamped to
    the 4–20 range and snapped to round values.

    ![CONTOUR_LEVELS at a glance](../assets/imgs/const-contour-levels.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import CONTOUR_LEVELS
        >>> CONTOUR_LEVELS.DEFAULT
        "auto"

    Attributes:
        DEFAULT (str): The default rule. Same as `CONTOUR_LEVELS.AUTO`.
        AUTO (str): Matplotlib's own choice, about eight round values across
            the surface. Equals to `"auto"`.
        RICE (str): The Rice rule, `2 * n ** (1/3)` levels — about ten on a
            120×120 grid. Equals to `"rice"`.
        FD (str): The Freedman–Diaconis rule, the value range over
            `2 * IQR * n ** (-1/3)` — about twice as dense as Rice on a
            120×120 grid. Equals to `"fd"`.

    """

    DEFAULT = "auto"
    AUTO = "auto"
    RICE = "rice"
    FD = "fd"


class HEXBIN_REDUCE:
    """The supported hexbin aggregations.

    Passed as the `reduce` attribute of hexbin charts: how the `c` values of
    the points in a hexagon collapse into the one value that colors it.
    Ignored without `c`, where every hexagon shows its point count.

    ![HEXBIN_REDUCE at a glance](../assets/imgs/const-hexbin-reduce.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import HEXBIN_REDUCE
        >>> HEXBIN_REDUCE.DEFAULT
        "mean"

    Attributes:
        DEFAULT (str): The default aggregation. Same as `HEXBIN_REDUCE.MEAN`.
        MEAN (str): The mean of the `c` values. Equals to `"mean"`.
        SUM (str): The sum of the `c` values. Equals to `"sum"`.
        MEDIAN (str): The median of the `c` values. Equals to `"median"`.
        MIN (str): The smallest `c` value. Equals to `"min"`.
        MAX (str): The largest `c` value. Equals to `"max"`.

    """

    DEFAULT = "mean"
    MEAN = "mean"
    SUM = "sum"
    MEDIAN = "median"
    MIN = "min"
    MAX = "max"


class BASEMAP_FEATURE:
    """The supported basemap features.

    Passed as the `features` of the basemap chart: which of the Natural
    Earth outlines are drawn. The ocean is not a feature; it is the axes
    background the land sits on. Every feature is drawn at every
    `BASEMAP_RESOLUTION` except the roads, which Natural Earth publishes at
    1:10 million alone.

    ![BASEMAP_FEATURE at a glance](../assets/imgs/const-basemap-feature.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import BASEMAP_FEATURE
        >>> BASEMAP_FEATURE.DEFAULT
        ("coastline", "land")

    Attributes:
        DEFAULT (Tuple[str, str]): The default features. Same as
            `(BASEMAP_FEATURE.COASTLINE, BASEMAP_FEATURE.LAND)`.
        COASTLINE (str): The coastlines, as lines. Equals to `"coastline"`.
        LAND (str): The land, as a filled area. Equals to `"land"`.
        COUNTRIES (str): The land, one filled area per country, so the
            `highlight` setting can pick countries out. Equals to
            `"countries"`.
        BORDERS (str): The land borders between countries, as lines. Equals
            to `"borders"`.
        LAKES (str): The large lakes, filled with the axes background.
            Equals to `"lakes"`.
        RIVERS (str): The rivers and the centerlines of the lakes they run
            through, as lines. At 1:110 million only the largest are a few
            strokes across a continent; a country wants a finer scale. Equals
            to `"rivers"`.
        ROADS (str): The main roads, as lines; 1:10 million only, about 50 MB
            on first use. Natural Earth maps North America and Europe in more
            detail than the rest of the world. Equals to `"roads"`.

    """

    DEFAULT = ("coastline", "land")
    COASTLINE = "coastline"
    LAND = "land"
    COUNTRIES = "countries"
    BORDERS = "borders"
    LAKES = "lakes"
    RIVERS = "rivers"
    ROADS = "roads"


class BASEMAP_RESOLUTION:
    """The supported basemap outline resolutions.

    Passed as the `resolution` of the basemap chart: the Natural Earth scale
    the outlines are drawn at. Each feature is downloaded the first time it
    is asked for at a scale and kept in a local cache, so a map needs the
    network once and never again. The cache folder is `DATACHART_CACHE_DIR`
    when that environment variable is set, else `datachart` under
    `XDG_CACHE_HOME` or `~/.cache`; a machine without the network works from
    a copy of a warm one.

    ![BASEMAP_RESOLUTION at a glance](../assets/imgs/const-basemap-resolution.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import BASEMAP_RESOLUTION
        >>> BASEMAP_RESOLUTION.DEFAULT
        "110m"

    Attributes:
        DEFAULT (str): The default resolution. Same as `BASEMAP_RESOLUTION.LOW`.
        LOW (str): 1:110 million, under 1 MB on first use; a continent or a
            region. Equals to `"110m"`.
        MEDIUM (str): 1:50 million, about 5 MB on first use; a country.
            Equals to `"50m"`.
        HIGH (str): 1:10 million, about 28 MB on first use, and 50 MB more
            for the roads; a coast or a city's surroundings. Equals to
            `"10m"`.

    """

    DEFAULT = "110m"
    LOW = "110m"
    MEDIUM = "50m"
    HIGH = "10m"


class STACKED_AREA_BASELINE:
    """The supported stacked area baselines.

    Passed as the `baseline` attribute of stacked area charts: where the
    first series starts, and so how the whole stack sits on the y-axis.

    ![STACKED_AREA_BASELINE at a glance](../assets/imgs/const-baseline.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import STACKED_AREA_BASELINE
        >>> STACKED_AREA_BASELINE.DEFAULT
        "zero"

    Attributes:
        DEFAULT (str): The default baseline. Same as `STACKED_AREA_BASELINE.ZERO`.
        ZERO (str): The stack starts at zero. Equals to `"zero"`.
        PERCENT (str): Each `x` is normalised so the stack spans 0 to 100. Equals to `"percent"`.
        SYM (str): The stack is centred on zero. Equals to `"sym"`.
        WIGGLE (str): The baseline minimises the sum of squared slopes. Equals to `"wiggle"`.
        WEIGHTED_WIGGLE (str): The baseline minimises the size-weighted sum of squared slopes. Equals to `"weighted_wiggle"`.

    """

    DEFAULT = "zero"
    ZERO = "zero"
    PERCENT = "percent"
    SYM = "sym"
    WIGGLE = "wiggle"
    WEIGHTED_WIGGLE = "weighted_wiggle"


class NETWORK_LAYOUT:
    """The supported network chart layouts.

    Passed as the `layout` attribute of network charts: the rule that places
    the nodes in the 0–1 layout space. Layout changes what the picture
    means, so it is a chart attribute and not a style key.

    ![NETWORK_LAYOUT at a glance](../assets/imgs/const-network-layout.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import NETWORK_LAYOUT
        >>> NETWORK_LAYOUT.DEFAULT
        "spring"

    Under `WEIGHTED`, and between the groups of `GROUPED`, an edge of weight
    $w$ pulls its nodes together at $s(w)$ times the `SPRING` pull:

    $$s(w) = 0.1 + 2.9\\,\\frac{w - w_{\\min}}{w_{\\max} - w_{\\min}}$$

    The lightest edge pulls at a tenth, the heaviest at three times, the rest
    linearly between; an edge without a weight pulls as the lightest. With no
    weights, or all equal, every edge pulls at one and the picture is the
    `SPRING` picture.

    Attributes:
        DEFAULT (str): The default layout. Same as `NETWORK_LAYOUT.SPRING`.
        SPRING (str): A force-directed (Fruchterman–Reingold) layout: linked
            nodes pull together, every pair pushes apart. Seeded by the chart's
            `seed` argument, so the same data renders the same picture. Costs
            the square of the node count: fine up to about 1,000 nodes, slow
            and memory-hungry past that. Equals to `"spring"`.
        WEIGHTED (str): The spring layout with each edge's pull set by its
            weight, as above: heavy edges draw their nodes close, light ones
            let them drift. Same cost as `SPRING`. Equals to `"weighted"`.
        GROUPED (str): The nodes clustered by their `group`, a node without
            one being a group of its own. Each group is laid out by the
            spring on its own edges; the groups are then laid out as a
            smaller network by the weighted spring, an edge between two
            groups weighing the sum of the edges joining them, so strongly
            linked clusters sit close. A translucent disc in the group color
            marks each cluster (`plot_network_group_alpha`; 0 disables it).
            Costs about what `SPRING` costs at worst, far less when the
            groups are many. Equals to `"grouped"`.
        CIRCULAR (str): The nodes evenly spaced on a circle in input order,
            starting at the top. Equals to `"circular"`.
        FIXED (str): Each node at its own `x`/`y`, in the 0–1 layout space;
            a node without them raises. Equals to `"fixed"`.

    """

    DEFAULT = "spring"
    SPRING = "spring"
    WEIGHTED = "weighted"
    GROUPED = "grouped"
    CIRCULAR = "circular"
    FIXED = "fixed"


class BUMP_RANK:
    """The supported bump chart ranking rules.

    Passed as the `rank_by` setting of the bump chart: whether each series'
    `y` is already a rank or a value ranked per period, over the series
    present there. Ties keep input order.

    ![BUMP_RANK at a glance](../assets/imgs/const-rank.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import BUMP_RANK
        >>> BUMP_RANK.DEFAULT
        "value_descending"

    Attributes:
        DEFAULT (str): The default ranking. Same as `BUMP_RANK.VALUE_DESCENDING`.
        VALUE_DESCENDING (str): The highest value ranks first. Equals to `"value_descending"`.
        VALUE_ASCENDING (str): The lowest value ranks first. Equals to `"value_ascending"`.
        GIVEN (str): `y` is the rank, a positive integer. Equals to `"given"`.

    """

    DEFAULT = "value_descending"
    VALUE_DESCENDING = "value_descending"
    VALUE_ASCENDING = "value_ascending"
    GIVEN = "given"


class BUMP_LABEL_POSITION:
    """The supported end label positions.

    Passed as the `label_position` setting of the bump chart: beside which
    end of each line its series label prints.

    ![BUMP_LABEL_POSITION at a glance](../assets/imgs/const-label-position.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import BUMP_LABEL_POSITION
        >>> BUMP_LABEL_POSITION.DEFAULT
        "end"

    Attributes:
        DEFAULT (str): The default position. Same as `BUMP_LABEL_POSITION.END`.
        START (str): Beside the first point. Equals to `"start"`.
        END (str): Beside the last point. Equals to `"end"`.
        BOTH (str): Beside the first and the last point. Equals to `"both"`.

    """

    DEFAULT = "end"
    START = "start"
    END = "end"
    BOTH = "both"


class NETWORK_LABEL_POSITION:
    """The supported node label positions.

    Passed as the `label_position` setting of the network chart: where each
    node's name prints against its marker.

    ![NETWORK_LABEL_POSITION at a glance](../assets/imgs/const-network-label-position.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import NETWORK_LABEL_POSITION
        >>> NETWORK_LABEL_POSITION.DEFAULT
        "center"

    Attributes:
        DEFAULT (str): The default position. Same as `NETWORK_LABEL_POSITION.CENTER`.
        CENTER (str): On the marker. Equals to `"center"`.
        ABOVE (str): Above the marker, clear of it, like a place name on a map.
            Equals to `"above"`.
        BEST (str): Beside the marker, at the spot with the least overlap
            with other nodes, edges, and labels, as scatter point labels are
            placed. Equals to `"best"`.

    """

    DEFAULT = "center"
    CENTER = "center"
    ABOVE = "above"
    BEST = "best"


class GANTT_VALUE:
    """The supported gantt chart value labels.

    Passed as the `value_kind` setting of the gantt chart: what each bar
    prints past its end when `show_values` is on.

    ![GANTT_VALUE at a glance](../assets/imgs/const-gantt-value.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import GANTT_VALUE
        >>> GANTT_VALUE.DURATION
        "duration"

    Attributes:
        DEFAULT (str): The default label. Same as `GANTT_VALUE.DURATION`.
        NONE (None): Equals to `None`, which `value_kind` reads as `DEFAULT`.
        DURATION (str): The task's duration in days. Equals to `"duration"`.
        PROGRESS (str): The task's progress as a percentage. Equals to `"progress"`.

    """

    DEFAULT = "duration"
    NONE = None
    DURATION = "duration"
    PROGRESS = "progress"


class GANTT_SORT_KEY:
    """The supported gantt chart sort keys.

    Passed as the `sort_by` setting of the gantt chart: what a `sort` other
    than `SORT.NONE` orders the task rows by.

    ![GANTT_SORT_KEY at a glance](../assets/imgs/const-gantt-sort-key.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import GANTT_SORT_KEY
        >>> GANTT_SORT_KEY.DEFAULT
        "start"

    Attributes:
        DEFAULT (str): The default key. Same as `GANTT_SORT_KEY.START`.
        START (str): Every row by its start. Equals to `"start"`.
        GROUP (str): Rows clustered by group, groups by their earliest start
            and tasks within a group by start. Equals to `"group"`.

    """

    DEFAULT = "start"
    START = "start"
    GROUP = "group"


class GANTT_ARROW_ENTRY:
    """The supported gantt dependency arrow entries.

    Passed as the `plot_gantt_dependency_entry` style attribute of the gantt
    chart: which side of the dependent task a dependency arrow enters.

    ![GANTT_ARROW_ENTRY at a glance](../assets/imgs/const-gantt-arrow-entry.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import GANTT_ARROW_ENTRY
        >>> GANTT_ARROW_ENTRY.DEFAULT
        "top"

    Attributes:
        DEFAULT (str): The default entry. Same as `GANTT_ARROW_ENTRY.TOP`.
        TOP (str): Along the dependency's row, then down (or up) onto the
            dependent bar's start. Equals to `"top"`.
        LEFT (str): Down (or up) from the dependency's end, then into the
            dependent bar's start from the left. Equals to `"left"`.

    """

    DEFAULT = "top"
    TOP = "top"
    LEFT = "left"


class DUMBBELL_VALUE:
    """The supported dumbbell chart value labels.

    Passed as the `value_kind` setting of the dumbbell chart: what each
    record prints when `show_values` is on.

    ![DUMBBELL_VALUE at a glance](../assets/imgs/const-dumbbell-value.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import DUMBBELL_VALUE
        >>> DUMBBELL_VALUE.DELTA
        "delta"

    Attributes:
        DEFAULT (str): The default label. Same as `DUMBBELL_VALUE.ENDPOINTS`.
        NONE (None): Equals to `None`, which `value_kind` reads as `DEFAULT`.
        ENDPOINTS (str): Each endpoint's value, past its dot, away from the
            connector. Equals to `"endpoints"`.
        DELTA (str): The record's `end - start`, at the connector midpoint.
            Equals to `"delta"`.

    """

    DEFAULT = "endpoints"
    NONE = None
    ENDPOINTS = "endpoints"
    DELTA = "delta"


class DUMBBELL_SORT_KEY:
    """The supported dumbbell chart sort keys.

    Passed as the `sort_by` setting of the dumbbell chart: what a `sort`
    other than `SORT.NONE` orders the categories by.

    ![DUMBBELL_SORT_KEY at a glance](../assets/imgs/const-dumbbell-sort-key.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import DUMBBELL_SORT_KEY
        >>> DUMBBELL_SORT_KEY.DEFAULT
        "start"

    Attributes:
        DEFAULT (str): The default key. Same as `DUMBBELL_SORT_KEY.START`.
        START (str): Each category by its `start`. Equals to `"start"`.
        END (str): Each category by its `end`. Equals to `"end"`.
        DELTA (str): Each category by its `end - start`. Equals to `"delta"`.

    """

    DEFAULT = "start"
    START = "start"
    END = "end"
    DELTA = "delta"


class SCATTER_MATRIX_DIAGONAL:
    """The supported scatter matrix diagonal cells.

    Passed as the `diagonal` setting of the scatter matrix: what each
    dimension's own cell shows.

    ![SCATTER_MATRIX_DIAGONAL at a glance](../assets/imgs/const-diagonal.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import SCATTER_MATRIX_DIAGONAL
        >>> SCATTER_MATRIX_DIAGONAL.DEFAULT
        "hist"

    Attributes:
        DEFAULT (str): The default diagonal. Same as `SCATTER_MATRIX_DIAGONAL.HIST`.
        HIST (str): A histogram of the dimension, one per hue group.
            Equals to `"hist"`.
        KDE (str): A kernel density curve of the dimension, one per hue
            group. Equals to `"kde"`.
        NONE (str): A blank cell. Equals to `"none"`.

    """

    DEFAULT = "hist"
    HIST = "hist"
    KDE = "kde"
    NONE = "none"


class GANTT_DATE_PERIOD:
    """The supported date axis periods.

    Passed as the `period` setting of the gantt chart: the calendar period
    the date axis is divided into. Lines mark the period edges, each period
    is labelled at its centre, and a second row names the enclosing period.

    ![GANTT_DATE_PERIOD at a glance](../assets/imgs/const-date-period.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import GANTT_DATE_PERIOD
        >>> GANTT_DATE_PERIOD.MONTH
        "month"

    Attributes:
        NONE (None): Concise date ticks, no period edges. Equals to `None`.
        DAY (str): Days, under their month. Equals to `"day"`.
        WEEK (str): ISO weeks starting on Monday, under their month. Equals to `"week"`.
        MONTH (str): Months, under their year. Equals to `"month"`.
        QUARTER (str): Quarters, under their year. Equals to `"quarter"`.
        YEAR (str): Years. Equals to `"year"`.
        PROJECT_MONTH (str): Months counted from the project start, M1, M2, …,
            under their project year, Y1, Y2, …. The start is `xmin` when
            given, else the earliest task start. Equals to `"project_month"`.

    """

    NONE = None
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    PROJECT_MONTH = "project_month"


class RADIAL_TYPE:
    """The supported radial chart visuals.

    Passed as the `type` setting of radial charts: the mark family the whole
    figure draws. The area visual is the line visual with `show_area=True`;
    stacked bars are the bar visual with `bar_mode="stack"`.

    ![RADIAL_TYPE at a glance](../assets/imgs/const-radial-type.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import RADIAL_TYPE
        >>> RADIAL_TYPE.LINE
        "line"

    Attributes:
        LINE (str): The line (radar) visual. Equals to `"line"`.
        BAR (str): The bar visual, one sector per label. Equals to `"bar"`.
        SCATTER (str): The scatter visual. Equals to `"scatter"`.
        HISTOGRAM (str): The angular histogram (wind rose) visual. Equals to `"histogram"`.

    """

    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"


class RADIAL_DIRECTION:
    """The supported angular directions.

    Passed as the `direction` setting of radial charts: which way the angles
    increase around the circle.

    ![RADIAL_DIRECTION at a glance](../assets/imgs/const-direction.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import RADIAL_DIRECTION
        >>> RADIAL_DIRECTION.CLOCKWISE
        "clockwise"

    Attributes:
        CLOCKWISE (str): The angles increase clockwise. Equals to `"clockwise"`.
        COUNTERCLOCKWISE (str): The angles increase counterclockwise. Equals to `"counterclockwise"`.

    """

    CLOCKWISE = "clockwise"
    COUNTERCLOCKWISE = "counterclockwise"


class VALUE_FORMAT:
    """The predefined value formats.

    Passed as the `value_format` attribute of every chart that takes
    `show_values` (the value labels printed beside its marks) or as the
    heatmap's `valfmt` attribute (the values drawn in the cells).

    ![VALUE_FORMAT at a glance](../assets/imgs/const-value-format.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import VALUE_FORMAT
        >>> VALUE_FORMAT.DEFAULT
        "{x}"

    Attributes:
        DEFAULT (str): The default value format. Equals to `"{x}"`.
        INTEGER (str): The integer value format (works on floats too). Equals to `"{x:.0f}"`.
        DECIMAL (str): The decimal value format (1 decimal place). Equals to `"{x:.1f}"`.
        DECIMAL_2 (str): The decimal value format (2 decimal places). Equals to `"{x:.2f}"`.
        DECIMAL_3 (str): The decimal value format (3 decimal places). Equals to `"{x:.3f}"`.
        PERCENT (str): The percentage value format (1 decimal place). Equals to `"{x:.1%}"`.
        PERCENT_INT (str): The percentage value format (no decimals). Equals to `"{x:.0%}"`.
        SCIENTIFIC (str): The scientific notation format. Equals to `"{x:.2e}"`.
        THOUSANDS (str): The thousands separator format. Equals to `"{x:,.0f}"`.

    """

    DEFAULT = "{x}"
    INTEGER = "{x:.0f}"
    DECIMAL = "{x:.1f}"
    DECIMAL_2 = "{x:.2f}"
    DECIMAL_3 = "{x:.3f}"
    PERCENT = "{x:.1%}"
    PERCENT_INT = "{x:.0%}"
    SCIENTIFIC = "{x:.2e}"
    THOUSANDS = "{x:,.0f}"


class DATE_FORMAT:
    """The predefined date formats.

    Passed as the `xticks_format` or `yticks_format` attribute of a chart
    whose axis holds datetime values, to label its ticks. Every member but
    `AUTO` is a `strftime` pattern; any other pattern is accepted as well.
    On a time axis `AUTO` picks concise, non-repeating labels for the visible
    span; on a category axis with date labels it prints the ISO date, plus
    the time when any label carries one.

    ![DATE_FORMAT at a glance](../assets/imgs/const-date-format.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import DATE_FORMAT
        >>> DATE_FORMAT.YEAR_MONTH
        "%Y-%m"

    Attributes:
        AUTO (str): Pick the labels from the visible span: concise, non-repeating. Equals to `"auto"`.
        ISO (str): The ISO 8601 date. Equals to `"%Y-%m-%d"`.
        YEAR (str): The four-digit year. Equals to `"%Y"`.
        YEAR_MONTH (str): The year and month. Equals to `"%Y-%m"`.
        MONTH_DAY (str): The month and day. Equals to `"%m-%d"`.
        DAY (str): The day of the month. Equals to `"%d"`.
        TIME (str): The hour and minute. Equals to `"%H:%M"`.

    """

    AUTO = "auto"
    ISO = "%Y-%m-%d"
    YEAR = "%Y"
    YEAR_MONTH = "%Y-%m"
    MONTH_DAY = "%m-%d"
    DAY = "%d"
    TIME = "%H:%M"


class THEME:
    """The predefined themes.

    Applied with [`config.set_theme`][datachart.config.Config.set_theme].
    Every theme applied to the same set of
    charts is shown in the
    [Theme Gallery](../../how-to-guides/styling/theme-gallery/).

    Examples:
        >>> from datachart.constants import THEME
        >>> THEME.DEFAULT
        "default"

    Attributes:
        DEFAULT (str): The default theme. Equals to `"default"`.
        GREYSCALE (str): The greyscale theme. Equals to `"greyscale"`.
        INK (str): The ink theme (dark-ink accents, print-ready). Equals to `"ink"`.
        HATCH (str): The hatch theme (hatch cycle, value labels, dotted grid). Equals to `"hatch"`.
        MINIMAL (str): The minimal theme (accent violet, no spines, flat bars). Equals to `"minimal"`.
        MATERIAL (str): The material theme (Google palette, light grid). Equals to `"material"`.
        SKETCH (str): The sketch theme (hand-drawn, xkcd-style wobble and halo,
            Comic Neue font). Equals to `"sketch"`.
        QUILL (str): The quill theme (black ink on white paper: pen-stroked lines,
            etched fills, IM Fell English font). Equals to `"quill"`.
        HARBOR (str): The harbor theme (navy and amber in lightness steps,
            colour-blind safe). Equals to `"harbor"`.
        MUTED (str): The muted theme (Tol's muted colours, dash and marker
            cycles, colour-blind safe). Equals to `"muted"`.
        CONTRAST (str): The contrast theme (lightness-stepped colours plus
            hatches, print-safe). Equals to `"contrast"`.
        MUTEDHATCH (str): The muted-hatch theme (Tol's muted colours under
            hatches, BuPu value scale). Equals to `"mutedhatch"`.
        SLATEHATCH (str): The slate-hatch theme (the hatch theme without rust,
            slate blue first, PuBu value scale). Equals to `"slatehatch"`.
        DARK (str): The dark theme (bright marks on a near-black page, light
            furniture, Viridis value scale). Equals to `"dark"`.
    """

    DEFAULT = "default"
    GREYSCALE = "greyscale"
    INK = "ink"
    HATCH = "hatch"
    MINIMAL = "minimal"
    MATERIAL = "material"
    SKETCH = "sketch"
    QUILL = "quill"
    HARBOR = "harbor"
    MUTED = "muted"
    CONTRAST = "contrast"
    MUTEDHATCH = "mutedhatch"
    SLATEHATCH = "slatehatch"
    DARK = "dark"


class EMPHASIS:
    """The supported emphasis roles.

    Set per chart via the `emphasis` key in a charts list, or per figure via
    the `emphasis` argument of [`Panel`][datachart.utils.Panel].

    ![EMPHASIS at a glance](../assets/imgs/const-emphasis.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import EMPHASIS
        >>> EMPHASIS.BACKGROUND
        "background"

    Attributes:
        BACKGROUND (str): Mute a series into context: theme muted color, lowered
            alpha, thinner strokes, behind the others, no legend entry.
            Equals to `"background"`.
        HIGHLIGHT (str): Bold a series and bring it to the front of the data
            layers; it keeps its color and legend entry. Equals to `"highlight"`.

    """

    BACKGROUND = "background"
    HIGHLIGHT = "highlight"


class SHOW_GRID:
    """The supported show grid options.

    Passed as the `show_grid` chart setting: which grid lines to draw. When
    unset (or `NONE`), the theme's `chart_default_show_grid` fills in. The
    members name a set to draw, so there is no member for "no grid at all":
    pass `False` for that.

    ![SHOW_GRID at a glance](../assets/imgs/const-show-grid.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import SHOW_GRID
        >>> SHOW_GRID.DEFAULT
        None

    Attributes:
        DEFAULT (str): The default show grid. Same as `SHOW_GRID.NONE`.
        NONE (None): No explicit grid; the theme default applies. Equals to `None`.
        X (str): Show the x-axis grid. Equals to `"x"`.
        Y (str): Show the y-axis grid. Equals to `"y"`.
        BOTH (str): Show both the x- and y-axis grid. Equals to `"both"`.

    """

    DEFAULT = None
    NONE = None
    X = "x"
    Y = "y"
    BOTH = "both"


class SCALE:
    """The supported scale options.

    Passed as the `scalex`/`scaley` chart settings to set an axis scale.
    Distinct from [`NORMALIZE`][datachart.constants.NORMALIZE], which
    normalizes heatmap colors.

    ![SCALE at a glance](../assets/imgs/const-scale.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import SCALE
        >>> SCALE.DEFAULT
        "linear"

    Attributes:
        DEFAULT (str): The default scale. Same as `SCALE.LINEAR`.
        LINEAR (str): The linear scale. Equals to `"linear"`.
        LOG (str): The log scale. Equals to `"log"`.
        SYMLOG (str): The symlog scale. Equals to `"symlog"`.
        ASINH (str): The asinh scale. Equals to `"asinh"`.

    """

    DEFAULT = "linear"
    LINEAR = "linear"
    LOG = "log"
    SYMLOG = "symlog"
    ASINH = "asinh"


class ASPECT_RATIO:
    """The supported aspect ratio options.

    Passed as the `aspect_ratio` chart setting: the ratio of the y-unit to
    the x-unit on screen.

    ![ASPECT_RATIO at a glance](../assets/imgs/const-aspect-ratio.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import ASPECT_RATIO
        >>> ASPECT_RATIO.DEFAULT
        "auto"

    Attributes:
        DEFAULT (str): The default aspect ratio. Same as `ASPECT_RATIO.AUTO`.
        AUTO (str): Automatic aspect ratio. Equals to `"auto"`.
        EQUAL (str): Equal aspect ratio (1:1). Equals to `"equal"`.
        GEOGRAPHIC (str): Longitude on x and latitude on y at true
            proportions: one degree of longitude is narrowed by the cosine
            of the latitude in the middle of the y-axis. The y-axis must
            stay within -90 and 90. Equals to `"geographic"`.

    """

    DEFAULT = "auto"
    AUTO = "auto"
    EQUAL = "equal"
    GEOGRAPHIC = "geographic"


class COLORBAR_LOCATION:
    """The supported colorbar locations.

    Used by the `location` field of a chart's `colorbar` setting
    (`ColorbarSettingAttrs`): the chart edge the bar sits on.

    ![COLORBAR_LOCATION at a glance](../assets/imgs/const-colorbar-location.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import COLORBAR_LOCATION
        >>> COLORBAR_LOCATION.RIGHT
        "right"

    Attributes:
        RIGHT (str): Right side of the chart. Equals to `"right"`.
        LEFT (str): Left side of the chart. Equals to `"left"`.
        TOP (str): Top of the chart. Equals to `"top"`.
        BOTTOM (str): Bottom of the chart. Equals to `"bottom"`.

    """

    RIGHT = "right"
    LEFT = "left"
    TOP = "top"
    BOTTOM = "bottom"


class DRAW_POSITION:
    """The supported draw positions of the image and basemap.

    Passed as the `position` setting of the image chart and the basemap
    chart: where the picture or the map sits in the draw order of the axes
    it shares with other charts. The position decides it, never the order
    of the figures in `Panel`.

    ![DRAW_POSITION at a glance](../assets/imgs/const-draw-position.svg){ width="100%" }

    Examples:
        >>> from datachart.constants import DRAW_POSITION
        >>> DRAW_POSITION.DEFAULT
        "below"

    Attributes:
        DEFAULT (str): The default position. Same as `DRAW_POSITION.BELOW`.
        BELOW (str): Under every mark and under the gridlines, so the grid and
            the data read over the picture. Equals to `"below"`.
        ABOVE (str): Over the marks, under the reference lines and the text
            annotations; a watermark or a mask. Equals to `"above"`.

    """

    DEFAULT = "below"
    BELOW = "below"
    ABOVE = "above"
