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
    VALFMT:             The predefined value formats.
    THEME:              The predefined themes.
    SHOW_GRID:          The supported show grid options.
    SCALE:              The supported scale options.
    ASPECT_RATIO:       The supported aspect ratio options.
    COLORBAR_LOCATION:  The supported colorbar locations.

"""


class FIG_SIZE:
    """The predefined figure sizes.

    Examples:
        >>> from datachart.constants import FIG_SIZE
        >>> FIG_SIZE.DEFAULT
        (6.4, 4.8)

    Attributes:
        # Default
        DEFAULT (Tuple[float, float]): The default figure size. Equals to `(6.4, 4.8)`.

        # A4 formats
        A4_PORTRAIT (Tuple[float, float]): The A4 portrait figure size. Equals to `(8.2, 11.6)`.
        A4 (Tuple[float, float]): Alias for `A4_PORTRAIT`. Deprecated, use `A4_PORTRAIT` instead.
        A4_LANDSCAPE (Tuple[float, float]): The A4 landscape figure size. Equals to `(11.6, 8.2)`.
        A4_NARROW (Tuple[float, float]): The flat, full-width A4 figure size. Equals to `(8.2, 2.4)`.
        A4_REGULAR (Tuple[float, float]): The regular, full-width A4 figure size. Equals to `(8.2, 4.8)`.
        A4_WIDE (Tuple[float, float]): The tall, full-width A4 figure size. Equals to `(8.2, 7.2)`.

        # A4 half-width formats
        A4_HALF_PORTRAIT (Tuple[float, float]): The A4 half-width portrait figure size. Equals to `(4.1, 5.8)`.
        A4_HALF_LANDSCAPE (Tuple[float, float]): The A4 half-width landscape figure size. Equals to `(5.8, 4.1)`.
        A4_HALF_NARROW (Tuple[float, float]): The flat, half-width A4 figure size. Equals to `(4.1, 2.4)`.
        A4_HALF_REGULAR (Tuple[float, float]): The regular, half-width A4 figure size. Equals to `(4.1, 4.8)`.
        A4_HALF_WIDE (Tuple[float, float]): The tall, half-width A4 figure size. Equals to `(4.1, 7.2)`.

        # US Letter formats
        LETTER_PORTRAIT (Tuple[float, float]): The US Letter portrait figure size. Equals to `(8.5, 11.0)`.
        LETTER_LANDSCAPE (Tuple[float, float]): The US Letter landscape figure size. Equals to `(11.0, 8.5)`.
        LETTER_NARROW (Tuple[float, float]): The flat, full-width Letter figure size. Equals to `(8.5, 2.4)`.
        LETTER_REGULAR (Tuple[float, float]): The regular, full-width Letter figure size. Equals to `(8.5, 4.8)`.
        LETTER_WIDE (Tuple[float, float]): The tall, full-width Letter figure size. Equals to `(8.5, 7.2)`.

        # Tall formats
        TALL_NARROW (Tuple[float, float]): The moderately tall, narrow figure size. Equals to `(4.1, 6.0)`.
        TALL_REGULAR (Tuple[float, float]): The regular tall, narrow figure size. Equals to `(4.1, 8.0)`.
        TALL_WIDE (Tuple[float, float]): The very tall, narrow figure size. Equals to `(4.1, 11.6)`.

        # Square formats
        SQUARE (Tuple[float, float]): The regular square figure size. Equals to `(6.4, 6.4)`.
        SQUARE_SMALL (Tuple[float, float]): The small square figure size. Equals to `(4.8, 4.8)`.
        SQUARE_LARGE (Tuple[float, float]): The large square figure size. Equals to `(8.2, 8.2)`.

    """

    DEFAULT = (6.4, 4.8)

    # A4 formats
    A4_PORTRAIT = (8.2, 11.6)
    A4 = A4_PORTRAIT  # Backward compatibility alias
    A4_LANDSCAPE = (11.6, 8.2)
    A4_NARROW = (8.2, 2.4)
    A4_REGULAR = (8.2, 4.8)
    A4_WIDE = (8.2, 7.2)

    # A4 half-width formats
    A4_HALF_PORTRAIT = (4.1, 5.8)
    A4_HALF_LANDSCAPE = (5.8, 4.1)
    A4_HALF_NARROW = (4.1, 2.4)
    A4_HALF_REGULAR = (4.1, 4.8)
    A4_HALF_WIDE = (4.1, 7.2)

    # US Letter formats
    LETTER_PORTRAIT = (8.5, 11.0)
    LETTER_LANDSCAPE = (11.0, 8.5)
    LETTER_NARROW = (8.5, 2.4)
    LETTER_REGULAR = (8.5, 4.8)
    LETTER_WIDE = (8.5, 7.2)

    # Tall formats
    TALL_NARROW = (4.1, 6.0)
    TALL_REGULAR = (4.1, 8.0)
    TALL_WIDE = (4.1, 11.6)

    # Square formats
    SQUARE = (6.4, 6.4)
    SQUARE_SMALL = (4.8, 4.8)
    SQUARE_LARGE = (8.2, 8.2)


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
        DEMI_BOLD (str): The demibold font weight. Equals to `"demibold"`.
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
    DEMI_BOLD = "demibold"
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
        STEPS (str): The steps line draw style. Equals to `"steps-pre"`.
        STEPS_PRE (str): The pre-steps line draw style. Equals to `"steps-pre"`.
        STEPS_MID (str): The mid-steps line draw style. Equals to `"steps-mid"`.
        STEPS_POST (str): The post-steps line draw style. Equals to `"steps-post"`.

    """

    DEFAULT = "default"
    STEPS = "steps-pre"
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
        STEPFILLED (str): The stepfilled histogram style. Equals to `"stepfilled"`.

    """

    BAR = "bar"
    BAR_STACKED = "barstacked"
    STEP = "step"
    STEPFILLED = "stepfilled"


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

        # Additional Diverging
        Coolwarm (str): Diverging cool-warm palette. Equals to `"coolwarm"`.

        # Tableau palettes (Categorical)
        Tab10 (str): Tableau 10-color categorical palette. Equals to `"tab10"`.
        Tab20 (str): Tableau 20-color categorical palette. Equals to `"tab20"`.

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
    Egypt = "Egypt"
    Hiroshige = "Hiroshige"
    Lake = "Lake"
    Neon = "Neon"

    # Diverging
    GnBu = "GnBu"
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


class VALFMT:
    """The predefined value formats.

    Examples:
        >>> from datachart.constants import VALFMT
        >>> VALFMT.DEFAULT
        "{x}"

    Attributes:
        DEFAULT (str): The default value format. Equals to `"{x}"`.
        INTEGER (str): The integer value format. Equals to `"{x:d}"`.
        DECIMAL (str): The decimal value format (1 decimal place). Equals to `"{x:.1f}"`.
        DECIMAL_2 (str): The decimal value format (2 decimal places). Equals to `"{x:.2f}"`.
        DECIMAL_3 (str): The decimal value format (3 decimal places). Equals to `"{x:.3f}"`.
        PERCENT (str): The percentage value format (1 decimal place). Equals to `"{x:.1%}"`.
        PERCENT_INT (str): The percentage value format (no decimals). Equals to `"{x:.0%}"`.
        SCIENTIFIC (str): The scientific notation format. Equals to `"{x:.2e}"`.
        THOUSANDS (str): The thousands separator format. Equals to `"{x:,.0f}"`.

    """

    DEFAULT = "{x}"
    INTEGER = "{x:d}"
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

    """

    DEFAULT = "default"
    GREYSCALE = "greyscale"
    PUBLICATION = "publication"


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
