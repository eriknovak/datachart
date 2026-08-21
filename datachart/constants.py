"""Module containing the `constants`.

The `constants` module provides a set of predefined constants used in the package.
These include figure size, format, style, and other figure manipulation values.

Classes:
    FIG_SIZE:           The predefined figure sizes.
    FIG_FORMAT:         The supported figure formats.
    FONT_STYLE:         The supported font styles.
    FONT_WEIGHT:        The supported font weights.
    LINE_MARKER:        The supported line markers.
    LINE_STYLE:         The supported line styles.
    LINE_DRAW_STYLE:    The supported line draw styles.
    HATCH_STYLE:        The supported hatch styles.
    LEGEND_ALIGN:       The supported legend alignments.
    LEGEND_LOCATION:    The supported legend locations.
    HISTOGRAM_TYPE:     The supported histogram types.
    COLORS:             The predefined colors.
    NORMALIZE:          The supported normalization options.
    ORIENTATION:        The supported orientations.
    VALUE_FORMAT:       The predefined value formats.
    THEME:              The predefined themes.
    EMPHASIS:           The supported emphasis roles.
    SHOW_GRID:          The supported show grid options.
    SCALE:              The supported scale options.
    ASPECT_RATIO:       The supported aspect ratio options.
    COLORBAR_LOCATION:  The supported colorbar locations.

"""


class FIG_SIZE:
    """The predefined figure sizes (ADR 0010).

    All values are `(width, height)` in inches, matplotlib's `figsize` unit.
    Paper figures are anchored to the A4 text block: `FULL` is its full width
    (8.2 in / 20.8 cm), `HALF` half of it (4.1 in / 10.4 cm), crossed with a
    height — `SHORT` (2.4 in / 6.1 cm), `MEDIUM` (4.8 in / 12.2 cm), or `TALL`
    (7.2 in / 18.3 cm).

    Examples:
        >>> from datachart.constants import FIG_SIZE
        >>> FIG_SIZE.DEFAULT
        (6.4, 4.8)

    Attributes:
        DEFAULT (Tuple[float, float]): The default figure size. Equals to `(6.4, 4.8)` in (16.3 x 12.2 cm).

        # Full-width paper figures (A4 text-block width)
        FULL_SHORT (Tuple[float, float]): The short, full-width figure size. Equals to `(8.2, 2.4)` in (20.8 x 6.1 cm).
        FULL_MEDIUM (Tuple[float, float]): The medium, full-width figure size. Equals to `(8.2, 4.8)` in (20.8 x 12.2 cm).
        FULL_TALL (Tuple[float, float]): The tall, full-width figure size. Equals to `(8.2, 7.2)` in (20.8 x 18.3 cm).

        # Half-width paper figures (for side-by-side placement)
        HALF_SHORT (Tuple[float, float]): The short, half-width figure size. Equals to `(4.1, 2.4)` in (10.4 x 6.1 cm).
        HALF_MEDIUM (Tuple[float, float]): The medium, half-width figure size. Equals to `(4.1, 4.8)` in (10.4 x 12.2 cm).
        HALF_TALL (Tuple[float, float]): The tall, half-width figure size. Equals to `(4.1, 7.2)` in (10.4 x 18.3 cm).
        HALF_SQUARE (Tuple[float, float]): The square, half-width figure size. Equals to `(4.1, 4.1)` in (10.4 x 10.4 cm).

        # A4 full pages
        A4_PORTRAIT (Tuple[float, float]): The A4 portrait figure size. Equals to `(8.2, 11.6)` in (20.8 x 29.5 cm).
        A4_LANDSCAPE (Tuple[float, float]): The A4 landscape figure size. Equals to `(11.6, 8.2)` in (29.5 x 20.8 cm).

        # Square
        SQUARE (Tuple[float, float]): The square figure size. Equals to `(4.8, 4.8)` in (12.2 x 12.2 cm).

        # Presentation slides
        SLIDE_16_9 (Tuple[float, float]): The 16:9 slide figure size (PowerPoint/Google Slides). Equals to `(13.33, 7.5)` in (33.9 x 19.1 cm).
        SLIDE_4_3 (Tuple[float, float]): The 4:3 slide figure size (PowerPoint/Google Slides). Equals to `(10.0, 7.5)` in (25.4 x 19.1 cm).
        BEAMER_16_9 (Tuple[float, float]): The 16:9 beamer frame figure size. Equals to `(6.3, 3.54)` in (16.0 x 9.0 cm).
        BEAMER_4_3 (Tuple[float, float]): The 4:3 beamer frame figure size. Equals to `(5.04, 3.78)` in (12.8 x 9.6 cm).

    """

    DEFAULT = (6.4, 4.8)

    # Full-width paper figures (A4 text-block width)
    FULL_SHORT = (8.2, 2.4)
    FULL_MEDIUM = (8.2, 4.8)
    FULL_TALL = (8.2, 7.2)

    # Half-width paper figures (for side-by-side placement)
    HALF_SHORT = (4.1, 2.4)
    HALF_MEDIUM = (4.1, 4.8)
    HALF_TALL = (4.1, 7.2)
    HALF_SQUARE = (4.1, 4.1)

    # A4 full pages
    A4_PORTRAIT = (8.2, 11.6)
    A4_LANDSCAPE = (11.6, 8.2)

    # Square
    SQUARE = (4.8, 4.8)

    # Presentation slides
    SLIDE_16_9 = (13.33, 7.5)
    SLIDE_4_3 = (10.0, 7.5)
    BEAMER_16_9 = (6.3, 3.54)
    BEAMER_4_3 = (5.04, 3.78)


class FIG_FORMAT:
    """The supported figure formats.

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
        ULTRA_HEAVY (str): The ultra heavy font weight. Equals to `"ultrabold"`.
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
    ULTRA_HEAVY = "ultrabold"
    BLACK = "black"


class LINE_MARKER:
    """The supported line markers.

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


class LINE_DRAW_STYLE:
    """The supported line draw styles.

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


class HISTOGRAM_TYPE:
    """The supported histogram types.

    Examples:
        >>> from datachart.constants import HISTOGRAM_TYPE
        >>> HISTOGRAM_TYPE.BAR
        "bar"

    Attributes:
        BAR (str): The bar histogram style. Equals to `"bar"`.
        BAR_STACKED (str): The stacked bar histogram style. Equals to `"barstacked"`.
        STEP (str): The step histogram style. Equals to `"step"`.
        STEP_FILLED (str): The filled step histogram style. Equals to `"stepfilled"`.

    """

    BAR = "bar"
    BAR_STACKED = "barstacked"
    STEP = "step"
    STEP_FILLED = "stepfilled"


class COLORS:
    """The predefined colors using pypalettes (https://y-sunflower.github.io/pypalettes/).

    All palette names are valid pypalettes identifiers. You can use any of the 2500+
    palettes available in pypalettes by passing the palette name as a string.

    Examples:
        >>> from datachart.constants import COLORS
        >>> COLORS.Blues
        'Blues'

    Attributes:
        # Sequential (Single-hue)
        Blues (str): Sequential blue palette. Equals to `"Blues"`.
        Greens (str): Sequential green palette. Equals to `"Greens"`.
        Oranges (str): Sequential orange palette. Equals to `"Oranges"`.
        Purples (str): Sequential purple palette. Equals to `"Purples"`.
        Reds (str): Sequential red palette. Equals to `"Reds"`.

        # Sequential (Multi-hue)
        Sunset2 (str): Multi-hue sunset palette. Equals to `"Sunset2"`.
        YlGnBu (str): Multi-hue yellow-green-blue palette. Equals to `"YlGnBu"`.
        YlOrRd (str): Multi-hue yellow-orange-red palette. Equals to `"YlOrRd"`.
        PuBuGn (str): Multi-hue purple-blue-green palette. Equals to `"PuBuGn"`.
        GnBu (str): Multi-hue green-blue palette. Equals to `"GnBu"`.
        Egypt (str): Multi-hue Egypt palette. Equals to `"Egypt"`.
        Hiroshige (str): Multi-hue Hiroshige palette. Equals to `"Hiroshige"`.
        Lake (str): Multi-hue lake palette. Equals to `"Lake"`.
        Neon (str): Multi-hue neon palette. Equals to `"Neon"`.

        # Diverging
        RdBu (str): Diverging red-blue palette. Equals to `"RdBu"`.
        BrBG (str): Diverging brown-blue-green palette. Equals to `"BrBG"`.
        PuOr (str): Diverging purple-orange palette. Equals to `"PuOr"`.
        Spectral (str): Diverging spectral palette. Equals to `"Spectral"`.
        RdYlBu (str): Diverging red-yellow-blue palette. Equals to `"RdYlBu"`.
        RdYlGn (str): Diverging red-yellow-green palette. Equals to `"RdYlGn"`.

        # Categorical
        Pastel (str): Soft pastel categorical palette. Equals to `"Pastel"`.
        Set2 (str): ColorBrewer Set2 categorical palette. Equals to `"Set2"`.
        Accent (str): ColorBrewer Accent categorical palette. Equals to `"Accent"`.
        Dark2 (str): ColorBrewer Dark2 categorical palette. Equals to `"Dark2"`.
        Paired (str): ColorBrewer Paired categorical palette (high contrast). Equals to `"Paired"`.
        Set1 (str): ColorBrewer Set1 categorical palette (high contrast). Equals to `"Set1"`.

        # Grayscale (print-friendly)
        Greys (str): Grayscale palette for monochrome visualizations. Equals to `"Greys"`.

        # Color-blind friendly / Accessible
        Viridis (str): Perceptually uniform, color-blind friendly. Equals to `"Viridis"`.
        Cividis (str): Color-blind friendly (optimized for CVD). Equals to `"Cividis"`.
        Inferno (str): Perceptually uniform, color-blind friendly. Equals to `"Inferno"`.
        Plasma (str): Perceptually uniform, color-blind friendly. Equals to `"Plasma"`.
        Magma (str): Perceptually uniform, color-blind friendly. Equals to `"Magma"`.
        Turbo (str): Rainbow-like but perceptually better. Equals to `"Turbo"`.
        OkabeIto (str): Okabe-Ito categorical palette, color-blind safe. Equals to `"OkabeIto"`.
        OkabeIto_Black (str): Okabe-Ito palette including black. Equals to `"OkabeIto_Black"`.

        # Additional Diverging
        Coolwarm (str): Diverging cool-warm palette. Equals to `"coolwarm"`.

        # Tableau palettes (Categorical)
        Tab10 (str): Tableau 10-color categorical palette. Equals to `"tab10"`.
        Tab20 (str): Tableau 20-color categorical palette. Equals to `"tab20"`.

        # Custom datachart palettes
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
    PuBuGn = "PuBuGn"
    GnBu = "GnBu"
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
    Magma = "Magma"
    Turbo = "Turbo"
    OkabeIto = "OkabeIto"
    OkabeIto_Black = "OkabeIto_Black"

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

    """

    LINEAR = "linear"
    LOG = "log"
    SYMLOG = "symlog"
    ASINH = "asinh"
    LOGIT = "logit"


class ORIENTATION:
    """The supported orientations.

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


class VALUE_FORMAT:
    """The predefined value formats.

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


class THEME:
    """The predefined themes.

    Examples:
        >>> from datachart.constants import THEME
        >>> THEME.DEFAULT
        "default"

    Attributes:
        DEFAULT (str): The default theme. Equals to `"default"`.
        GREYSCALE (str): The greyscale theme. Equals to `"greyscale"`.
        INK (str): The ink theme (dark-ink accents, print-ready). Equals to `"ink"`.
        HATCH (str): The hatch theme (hatch cycle, value labels, dotted grid). Equals to `"hatch"`.
        MINIMAL (str): The minimal theme (accent blue, no spines, flat bars). Equals to `"minimal"`.
        MATERIAL (str): The material theme (Google palette, light grid). Equals to `"material"`.

    """

    DEFAULT = "default"
    GREYSCALE = "greyscale"
    INK = "ink"
    HATCH = "hatch"
    MINIMAL = "minimal"
    MATERIAL = "material"


class EMPHASIS:
    """The supported emphasis roles (ADR 0009).

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

    Examples:
        >>> from datachart.constants import SHOW_GRID
        >>> SHOW_GRID.DEFAULT
        None

    Attributes:
        DEFAULT (str): The default show grid. Same as `SHOW_GRID.NONE`.
        NONE (None): Do not show the grid. Equals to `None`.
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

    Examples:
        >>> from datachart.constants import ASPECT_RATIO
        >>> ASPECT_RATIO.DEFAULT
        "auto"

    Attributes:
        DEFAULT (str): The default aspect ratio. Same as `ASPECT_RATIO.AUTO`.
        AUTO (str): Automatic aspect ratio. Equals to `"auto"`.
        EQUAL (str): Equal aspect ratio (1:1). Equals to `"equal"`.

    """

    DEFAULT = "auto"
    AUTO = "auto"
    EQUAL = "equal"


class COLORBAR_LOCATION:
    """The supported colorbar locations.

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
