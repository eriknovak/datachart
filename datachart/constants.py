"""Module containing the `constants`.

The `constants` module procides a set of predefined constants used in the package.
These include figure size, format, style, and other figure manipulation values.

Classes:
    FIG_SIZE:        The predefined figure sizes.
    FIG_FORMAT:      The supported figure formats.
    FONT_STYLE:      The supported font styles.
    FONT_WEIGHT:     The supported font weights.
    LINE_MARKER:     The supported line markers.
    LINE_STYLE:      The supported line styles.
    LINE_DRAW_STYLE: The supported line draw styles.
    HATCH_STYLE:     The supported hatch styles.
    LEGEND_ALIGN:    The supported legend alignments.
    HISTOGRAM_TYPE:  The supported histogram types.
    COLORS:          The predefined colors.
    NORMALIZE:       The supported normalization options.
    ORIENTATION:     The supported orientations.
    VALFMT:          The predefined value formats.
    THEME:           The predefined themes.
    SHOW_GRID:       The supported show grid options.

"""


class FIG_SIZE:
    """The predefined figure sizes.

    Examples:
        >>> from datachart.constants import FIG_SIZE
        >>> FIG_SIZE.DEFAULT
        (6.4, 4.8)

    Attributes:
        DEFAULT (Tuple[float, float]): The default figure size. Equals to `(6.4, 4.8)`.
        A4 (Tuple[float, float]): The A4 figure size. Equals to `(8.2, 11.6)`.
        A4_NARROW (Tuple[float, float]): The flat, full-width figure size. Equals to `(8.2, 2.4)`.
        A4_REGULAR (Tuple[float, float]): The regular, full-width figure size. Equals to `(8.2, 4.8)`.
        A4_WIDE (Tuple[float, float]): The tall, full-width figure size. Equals to `(8.2, 7.2)`.
        SQUARE (Tuple[float, float]): The regular square figure size. Equals to `(6.4, 6.4)`.
        SQUARE_SMALL (Tuple[float, float]): The small square figure size. Equals to `(4.8, 4.8)`.
        SQUARE_LARGE (Tuple[float, float]): The large square figure size. Equals to `(8.2, 8.2)`.

    """

    DEFAULT = (6.4, 4.8)
    A4 = (8.2, 11.6)
    A4_NARROW = (8.2, 2.4)
    A4_REGULAR = (8.2, 4.8)
    A4_WIDE = (8.2, 7.2)

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

    """

    DEFAULT = "png"
    SVG = "svg"
    PDF = "pdf"
    PNG = "png"
    WEBP = "webp"


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
        BOLD (str): The bold font weight. Equals to `"bold"`.
        HEAVY (str): The heavy font weight. Equals to `"heavy"`.
        ULTRA_HEAVY (str): The ultra heavy font weight. Equals to `"ultrabold"`.

    """

    DEFAULT = "normal"
    ULTRA_LIGHT = "ultralight"
    LIGHT = "light"
    NORMAL = "normal"
    BOLD = "bold"
    HEAVY = "heavy"
    ULTRA_HEAVY = "ultrabold"


class LINE_MARKER:
    """The supported line markers.

    Examples:
        >>> from datachart.constants import LINE_MARKER
        >>> LINE_MARKER.PIXEL
        ","

    Attributes:
        PIXEL (str): The pixel line marker. Equals to `","`.
        POINT (str): The point line marker. Equals to `"."`.
        CIRCLE (str): The circle line marker. Equals to `"o"`.
        TRIANGLE (str): The triangle line marker. Equals to `"^"`.
        SQUARE (str): The square line marker. Equals to `"s"`.
        PENTAGON (str): The pentagon line marker. Equals to `"p"`.
        HEXAGON (str): The hexagon line marker. Equals to `"h"`.
        STAR (str): The star line marker. Equals to `"*"`.
        CROSS (str): The cross line marker. Equals to `"x"`.
        PLUS (str): The plus line marker. Equals to `"+"`.

    """

    PIXEL = ","
    POINT = "."
    CIRCLE = "o"
    TRIANGLE = "^"
    SQUARE = "s"
    PENTAGON = "p"
    HEXAGON = "h"
    STAR = "*"
    CROSS = "x"
    PLUS = "+"


class LINE_STYLE:
    """The supported line styles.

    Examples:
        >>> from datachart.constants import LINE_STYLE
        >>> LINE_STYLE.SOLID
        "-"

    Attributes:
        SOLID (str): The solid line style. Equals to `"-"`.
        DASHED (str): The dashed line style. Equals to `"--"`.
        DASHDOT (str): The dashdot line style. Equals to `"-."`.
        DOTTED (str): The dotted line style. Equals to `":"`.

    """

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


class HISTOGRAM_TYPE:
    """The supported histogram types.

    Examples:
        >>> from datachart.constants import HISTOGRAM_TYPE
        >>> HISTOGRAM_TYPE.BAR
        "bar"

    Attributes:
        BAR (str): The bar histogram style. Equals to `"bar"`.
        STEP (str): The step histogram style. Equals to `"step"`.
        STEPFILLED (str): The stepfilled histogram style. Equals to `"stepfilled"`.

    """

    BAR = "bar"
    STEP = "step"
    STEPFILLED = "stepfilled"


class COLORS:
    """The predefined colors.

    Examples:
        >>> from datachart.constants import COLORS
        >>> COLORS.Blue
        'blue'

    Attributes:
        Blue (str): The single-hue blue color. Equals to `"blue"`.
        Green (str): The single-hue green color. Equals to `"green"`.
        Orange (str): The single-hue orange color. Equals to `"orange"`.
        Purple (str): The single-hue purple color. Equals to `"purple"`.
        Grey (str): The single-hue grey color. Equals to `"grey"`.
        YlGnBu (str): The multi-hue yellow-green-blue colors. Equals to `"ylgnbu"`.
        YlGn (str): The multi-hue yellow-green colors. Equals to `"ylgn"`.
        BuGn (str): The multi-hue blue-green colors. Equals to `"bugn"`.
        GnBu (str): The multi-hue green-blue colors. Equals to `"gnbu"`.
        PuBu (str): The multi-hue purple-blue colors. Equals to `"pubu"`.
        RdPu (str): The diverging red-purple colors. Equals to `"rdbn"`.
        RdYlBu (str): The diverging red-yellow-blue colors. Equals to `"rdylbu"`.
        BrNg (str): The diverging brown-grey colors. Equals to `"brng"`.
        PuGn (str): The diverging purple-green colors. Equals to `"pugn"`.
        OrPu (str): The diverging orange-purple colors. Equals to `"puor"`.
        RdGy (str): The diverging red-gray colors. Equals to `"rdgy"`.
        RdYlGn (str): The diverging red-yellow-green colors. Equals to `"rdylgn"`.
        Spectral (str): The diverging spectral colors. Equals to `"spectral"`.
        MixedLight (str): The quantitative light color mix. Equals to `"mixed_light"`.
        MixedDark (str): The quantitative dark color mix. Equals to ` "mixed_dark"`.

    """

    Blue = "blue"
    Green = "green"
    Orange = "orange"
    Purple = "purple"
    Grey = "grey"
    YlGnBu = "ylgnbu"
    YlGn = "ylgn"
    BuGn = "bugn"
    GnBu = "gnbu"
    PuBu = "pubu"
    RdBn = "rdbn"
    RdYlBu = "rdylbu"
    BrGn = "brgn"
    PuGn = "pugn"
    OrPu = "orpu"
    RdGy = "rdgy"
    RdYlGn = "rdylgn"
    Spectral = "spectral"
    MixedLight = "mixed_light"
    MixedDark = "mixed_dark"


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
        DECIMAL (str): The decimal value format. Equals to `"{x:.1f}"`.
        PERCENT (str): The percentage value format. Equals to `"{x:.1%}"`.

    """

    DEFAULT = "{x}"
    INTEGER = "{x:d}"
    DECIMAL = "{x:.1f}"
    PERCENT = "{x:.1%}"


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
        LOGIT (str): The logit scale. Equals to `"logit"`.
        ASINH (str): The asinh scale. Equals to `"asinh"`.
    """

    DEFAULT = "linear"
    LINEAR = "linear"
    LOG = "log"
    SYMLOG = "symlog"
    ASINH = "asinh"
